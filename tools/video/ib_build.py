"""IronBehemoth episode builder (ffmpeg).
  python3 ib_build.py <EP> shotmap            -> build/shotmap.txt (one shot per beat, auto visuals; edit after)
  python3 ib_build.py <EP> check              -> list beats with missing assets
  python3 ib_build.py <EP> render [--preview] [--jobs N] [--test i,j]
     render refuses to run (exit 2) while any asset, gfx, voice or music is missing - report the list to the owner.
Inputs in <EP>:
  build/ib.json         config (see DEFAULTS)
  build/beat_times.json from ib_align.py
  beats/<csv>           owner template CSV (beat_id, asset_id, itemType, ..., provider, path)
  audio/voice.mp3, audio/music.mp3, build/sfx.txt (optional), gfx/ (ib_gfx.py, subscribe, endcard)
Shotmap line:  B001[+B002] <visual> <motion> [off=S speed=X zoom=Z] [overlay@t0@dur ...]
  visual : auto | path/relative/to/EP[@off] | gfx:card_x.png | seqv:endcard | black
  motion : in | out | left | right | none
  overlay: ov_x.png@1.5@5  lt_x.png@0.5@4  chapter_x.png@0.2@3  title.png@0.25@4.6  seq:subscribe@0.4
           (t0 seconds from shot start, or a beat id Bxxx = that beat's start)
sfx.txt line:  <file> <Bxxx[+/-sec] | t=sec> <volume> [duration]   (file in audio/sfx/ or tools/video/common/sfx/)
Auto SFX: chapter -> whoosh+impact, ov/lt -> click, seq:subscribe -> 1 click + bell, endcard -> whoosh+impact."""
import os, sys, json, csv, glob, hashlib, subprocess, time
from concurrent.futures import ThreadPoolExecutor
TOOLS = os.path.dirname(os.path.abspath(__file__)); COMMON = os.path.join(TOOLS, 'common')
EP = os.path.abspath(sys.argv[1]); CMD = sys.argv[2]
BD = os.path.join(EP, 'build'); GF = os.path.join(EP, 'gfx')
DEFAULTS = dict(ep='000', name='Tank', csv='', voice='audio/voice.mp3', music='audio/music.mp3', music_ss=0.0, music_vol=0.22,
                tempo=1.0, delay=0.6, end_at='', endcard_tail=10.0, skip_ai=[], delogo=[1132, 572, 58, 58], delogo_providers=['flow', 'veo', 'google'],
                duck=[], loudness=-15, merge_under=1.6)
CFG = dict(DEFAULTS); CFG.update(json.load(open(os.path.join(BD, 'ib.json'))) if os.path.exists(os.path.join(BD, 'ib.json')) else {})
PREVIEW = '--preview' in sys.argv
JOBS = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 3
W, H, FPS = (1280, 720, 30) if PREVIEW else (1920, 1080, 30)
T = os.path.join(BD, '_tmp'); os.makedirs(T, exist_ok=True)
GRADE = "eq=contrast=1.06:saturation=0.78:gamma=1.04,colorbalance=rs=0.03:bs=-0.03:rh=0.03:bh=-0.03"
GRADE_PHOTO = "eq=contrast=1.08:saturation=0.75:gamma=1.02,colorbalance=rs=0.03:bs=-0.04"
VEXT = ('.mp4', '.mov', '.webm', '.m4v', '.mkv')

# ---------- CSV + asset lookup ----------
def load_rows():
    p = os.path.join(EP, CFG['csv']) if CFG['csv'] else (sorted(glob.glob(os.path.join(EP, 'beats', 'beats_*.csv'))) or [''])[0]
    if not p or not os.path.exists(p): return {}
    out = {}
    for r in csv.DictReader(open(p, encoding='utf-8-sig')):
        out.setdefault(r['beat_id'], r)
    return out
ROWS = load_rows()
SEARCH = [os.path.join(EP, 'beats', 'footage'), os.path.join(EP, 'footage'), os.path.join(EP, 'assets')]
def find_asset(bid):
    r = ROWS.get(bid, {})
    p = (r.get('path') or '').strip()
    if p:
        if not os.path.isabs(p) and not p[1:3] == ':\\': p = os.path.join(EP, p)
        if os.path.exists(p): return p
        base = p.replace('\\', '/').split('/')[-1]
        for d in SEARCH:
            if os.path.exists(os.path.join(d, base)): return os.path.join(d, base)
    keys = [r.get('asset_id') or '', bid + '_']
    for d in SEARCH:
        if not os.path.isdir(d): continue
        for f in sorted(os.listdir(d)):
            if any(k and f.startswith(k) for k in keys): return os.path.join(d, f)
    return None
def is_flow(bid):   # Google Flow / Veo downloads carry a sparkle watermark; Muse clips do not
    pv = (ROWS.get(bid, {}).get('provider') or '').lower()
    return is_ai(bid) and any(k in pv for k in CFG['delogo_providers']) and 'muse' not in pv
def is_ai(bid): return (ROWS.get(bid, {}).get('itemType') or ROWS.get(bid, {}).get('item_type') or '') == 'veo3'

# ---------- timing ----------
if not os.path.exists(os.path.join(BD, 'beat_times.json')):
    if CMD == 'check':   # asset check straight from the CSV, before voice/alignment exist
        miss = [f"{b}({r.get('itemType', '?')})" for b, r in sorted(ROWS.items()) if not find_asset(b)]
        print('beats', len(ROWS), 'missing', len(miss)); print(' '.join(miss)); sys.exit(1 if miss else 0)
    sys.exit('build/beat_times.json missing - run ib_align.py first')
BT = json.load(open(os.path.join(BD, 'beat_times.json')))
IDS = BT.get('ids') or [f'B{i+1:03d}' for i in range(len(BT['starts']))]
def ot(v): return v / CFG['tempo'] + CFG['delay']
START = {b: ot(BT['starts'][i]) for i, b in enumerate(IDS)}; START[IDS[0]] = 0.0
END_AT = CFG['end_at'] or IDS[-1]
VOICE_CUT = BT['ends'][IDS.index(END_AT)] + 0.25
END_VOICE = ot(BT['ends'][IDS.index(END_AT)])
TOTAL = END_VOICE + CFG['endcard_tail']
def S(b, dt=0.0): return START[b] + dt

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(' '.join(cmd)[:600] + '\n' + r.stderr[-1500:])
def probe_wh(p):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip()
    try: w, h = o.split(',')[:2]; return int(w), int(h)
    except Exception: return 0, 0

# ---------- shotmap ----------
def cmd_shotmap():
    out = os.path.join(BD, 'shotmap.txt')
    if os.path.exists(out) and '--force' not in sys.argv: sys.exit('shotmap.txt exists (use --force to overwrite)')
    lines = ['# beat[+beat] visual motion [off= speed= zoom=] [overlay@t0@dur ...]  -- generated ' + time.strftime('%Y-%m-%d')]
    ids = IDS[:IDS.index(END_AT) + 1]; i = 0; mot = ['in', 'out', 'left', 'right']
    while i < len(ids):
        grp = [ids[i]]
        # merge very short beats into the next one
        while i + 1 < len(ids) and (BT['ends'][IDS.index(grp[-1])] - BT['starts'][IDS.index(grp[0])]) < CFG['merge_under']:
            i += 1; grp.append(ids[i])
        a = find_asset(grp[0])
        vis = os.path.relpath(a, EP) if a else 'auto'
        m = 'in' if (a and a.lower().endswith(VEXT)) else mot[i % 4]
        lines.append(f"{'+'.join(grp)} {vis} {m}"); i += 1
    lines.append(f"{END_AT}_END seqv:endcard none seq:subscribe@1.0")
    open(out, 'w').write('\n'.join(lines) + '\n'); print('wrote', out, len(lines) - 1, 'shots')

def parse_map():
    shots = []
    for ln in open(os.path.join(BD, 'shotmap.txt')):
        ln = ln.split('#')[0].strip() if not ln.strip().startswith('#') else ''
        if not ln: continue
        p = ln.split(); ids = p[0].split('+'); vis = p[1]; motion = p[2] if len(p) > 2 else 'in'
        opts, ovs = {}, []
        for o in p[3:]:
            if '=' in o and '@' not in o: k, v = o.split('='); opts[k] = float(v)
            else: name, t0, *d = o.split('@'); ovs.append((name, t0, float(d[0]) if d else None))
        shots.append([ids, vis, motion, opts, ovs, ln])
    out = []
    for k, (ids, vis, motion, opts, ovs, ln) in enumerate(shots):
        end_shot = ids[0].endswith('_END')
        bid = ids[0].replace('_END', '')
        if bid not in START: raise SystemExit(f'unknown beat {bid} in shotmap')
        a = S(bid)
        b = S(shots[k + 1][0][0].replace('_END', '')) if k + 1 < len(shots) else TOTAL
        if b <= a: continue
        src, kind = None, None
        if vis == 'auto':
            src = find_asset(bid)
            if src and bid in CFG['skip_ai'] and is_ai(bid): src = None
        elif vis.startswith('gfx:'): src = os.path.join(GF, vis[4:]); kind = 'card'
        elif vis.startswith('seqv:'): src = os.path.join(GF, vis[5:]); kind = 'seqv'
        elif vis == 'black': src = 'BLACK'; kind = 'black'
        else:
            if '@' in vis: vis, off = vis.split('@'); opts.setdefault('off', float(off))
            src = os.path.join(EP, vis)
        if src and src != 'BLACK' and kind is None: kind = 'vid' if src.lower().endswith(VEXT) else 'img'
        ov2 = []
        for name, t0, d in ovs:
            t = S(t0) - a if t0.startswith('B') else float(t0)
            ov2.append((name, t, d))
        out.append(dict(sid='_'.join(ids), a=a, b=b, src=src, kind=kind, motion=motion, opts=opts, ovs=ov2,
                        ai=is_ai(bid), flow=is_flow(bid), key=ln))
    return out

def shot(s):
    dur = s['b'] - s['a']; n = max(1, int(round(dur * FPS)))
    h = hashlib.md5((s['key'] + f"{dur:.3f}{W}{s['src']}{os.path.getmtime(s['src']) if s['src'] and os.path.exists(s['src']) else 0}").encode()).hexdigest()[:8]
    out = os.path.join(T, f"{s['sid']}_{W}_{h}.mp4")
    if os.path.exists(out): return out
    src, kind, o = s['src'], s['kind'], s['opts']
    if not src or src == 'BLACK' or (kind != 'seqv' and not os.path.exists(src)):
        inputs = ['-f', 'lavfi', '-i', f"color=c=0x15161a:s={W}x{H}:r={FPS}:d={dur:.3f}"]
        fnt = os.path.join(COMMON, 'fonts', 'Oswald.ttf').replace(':', '\\:')
        v = f"[0:v]drawtext=fontfile='{fnt}':text='MISSING {s['sid']}':fontcolor=0xE0662B:fontsize={H//14}:x=(w-tw)/2:y=(h-th)/2" if kind != 'card' and s['src'] != 'BLACK' else '[0:v]null'
    elif kind == 'seqv':
        inputs = ['-framerate', str(FPS), '-i', os.path.join(src, '%04d.jpg')]
        v = f"[0:v]scale={W}:{H},fps={FPS},tpad=stop_mode=clone:stop_duration=30"
    elif kind == 'card':
        inputs = ['-loop', '1', '-i', src]; v = f"[0:v]scale={W}:{H},fps={FPS}"
    elif kind == 'img':
        zmax = 1.12; m = s['motion'] if s['motion'] in ('in', 'out', 'left', 'right', 'none') else 'in'
        zz = {'in': f"zoom='1+{zmax-1}*on/{n}'", 'out': f"zoom='{zmax}-{zmax-1}*on/{n}'", 'left': f"zoom='{zmax}'", 'right': f"zoom='{zmax}'", 'none': "zoom='1'"}[m]
        x = {'left': f"x='(iw-iw/zoom)*(1-on/{n})'", 'right': f"x='(iw-iw/zoom)*on/{n}'"}.get(m, "x='iw/2-(iw/zoom/2)'")
        inputs = ['-i', src]
        v = (f"[0:v]scale={int(W*1.5)}:{int(H*1.5)}:force_original_aspect_ratio=increase,crop={int(W*1.5)}:{int(H*1.5)},"
             f"zoompan={zz}:{x}:y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},{GRADE_PHOTO},vignette=PI/6")
    else:
        sp = o.get('speed', 1.0); z = o.get('zoom', 1.06 if s['ai'] else 1.04)
        inputs = ['-stream_loop', '-1', '-ss', str(o.get('off', 0.0)), '-i', src]
        dl = ''
        if s['flow'] and CFG['delogo']:
            sw, sh = probe_wh(src)
            if sw:
                f = sw / 1280; x, y, w, hh = [int(round(c * f)) for c in CFG['delogo']]
                if x + w < sw and y + hh < sh: dl = f"delogo=x={x}:y={y}:w={w}:h={hh},"
        v = f"[0:v]{dl}setpts=PTS/{sp},scale={int(W*z)}:{int(H*z)}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setpts=PTS-STARTPTS,{GRADE}"
    fc = v + f",trim=duration={dur:.4f},setsar=1,format=yuv420p,fade=t=in:st=0:d=0.15,fade=t=out:st={max(dur-0.15,0):.3f}:d=0.15[base]"
    last = 'base'; i = 1
    for png, t0, d in s['ovs']:
        if png.startswith('seq:'):
            inputs += ['-framerate', '30', '-i', os.path.join(GF, png[4:], '%04d.png')]
            fc += f";[{i}:v]scale={W}:{H},format=rgba,fps={FPS},setpts=PTS+{t0}/TB[o{i}];[{last}][o{i}]overlay=0:0:eof_action=pass[v{i}]"
        else:
            d = min(d or 5, dur - t0 - 0.2)
            if d < 0.8: continue
            inputs += ['-loop', '1', '-t', f'{dur:.3f}', '-i', os.path.join(GF, png)]
            fc += f";[{i}:v]scale={W}:{H},format=rgba,fade=t=in:st={t0}:d=0.35:alpha=1,fade=t=out:st={t0+d-0.35}:d=0.35:alpha=1[o{i}];[{last}][o{i}]overlay=0:0:shortest=1[v{i}]"
        last = f'v{i}'; i += 1
    run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', fc, '-map', f'[{last}]', '-t', f'{dur:.4f}', '-r', str(FPS),
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-g', str(FPS), out])
    return out

def sfx_file(f):
    for d in (os.path.join(EP, 'audio', 'sfx'), os.path.join(COMMON, 'sfx')):
        if os.path.exists(os.path.join(d, f)): return os.path.join(d, f)
    return None

def sfx_plan(shots):
    e = []
    p = os.path.join(BD, 'sfx.txt')
    if os.path.exists(p):
        for ln in open(p):
            ln = ln.split('#')[0].strip()
            if not ln: continue
            q = ln.split(); f, at, vol = q[0], q[1], float(q[2]); dd = float(q[3]) if len(q) > 3 else None
            if at.startswith('t='): t = float(at[2:])
            else:
                for sgn in '+-':
                    if sgn in at[1:]:
                        b, dt = at.split(sgn, 1); t = S(b, float(dt) * (1 if sgn == '+' else -1)); break
                else: t = S(at)
            e.append((f, t, vol, dd))
    for s in shots:
        for png, t0, d in s['ovs']:
            t = s['a'] + t0
            if png.startswith('chapter_'): e += [('sfx_whoosh.mp3', t, 0.6, None), ('sfx_impact.mp3', t + 0.25, 0.45, None)]
            elif png.startswith(('ov_', 'lt_')): e.append(('sfx_click.mp3', t, 0.35, None))
            elif png.startswith('seq:subscribe'): e += [('sfx_click_single.mp3', t + 1.45, 0.8, None), ('sfx_bell.mp3', t + 1.75, 0.55, None)]
        if s['kind'] == 'seqv': e += [('sfx_whoosh.mp3', s['a'] + 0.45, 0.45, None), ('sfx_impact.mp3', s['a'] + 1.2, 0.4, None)]
    return e

def ensure_gfx(shots):
    env = dict(os.environ, IB_EP=EP)
    if any(png.startswith('seq:subscribe') for s in shots for png, _, _ in s['ovs']) and not os.path.isdir(os.path.join(GF, 'subscribe')):
        subprocess.run([sys.executable, os.path.join(TOOLS, 'make_subscribe.py')], env=env, check=True)
    for s in shots:
        if s['kind'] == 'seqv' and s['src'].endswith('endcard'):
            need = s['b'] - s['a'] + 0.5
            stamp = os.path.join(GF, 'endcard', '.dur')
            have = float(open(stamp).read()) if os.path.exists(stamp) else 0
            if abs(have - need) > 0.2:
                subprocess.run([sys.executable, os.path.join(TOOLS, 'make_endcard.py'), f'{need:.2f}'], env=env, check=True)
                open(stamp, 'w').write(f'{need:.2f}')

def cmd_check():
    shots = parse_map() if os.path.exists(os.path.join(BD, 'shotmap.txt')) else []
    if shots:
        m = missing_list(shots); print('missing', len(m)); print(' '.join(m)); return
    miss = []
    for b in IDS[:IDS.index(END_AT) + 1]:
        if not find_asset(b): miss.append(f"{b}({ROWS.get(b, {}).get('itemType', '?')})")
    print('beats', IDS.index(END_AT) + 1, 'missing', len(miss)); print(' '.join(miss))

def missing_list(shots):
    miss = []
    for s in shots:
        if s['kind'] in ('card', 'seqv'):
            if s['kind'] == 'card' and not os.path.exists(s['src']): miss.append(f"{s['sid']}(gfx {os.path.basename(s['src'])})")
            continue
        if s['src'] == 'BLACK': continue
        if not s['src'] or not os.path.exists(s['src']):
            b = s['sid'].split('_')[0]; miss.append(f"{b}({ROWS.get(b, {}).get('itemType', '?')})")
        for png, _, _ in s['ovs']:
            if not png.startswith('seq:') and not os.path.exists(os.path.join(GF, png)): miss.append(f"{s['sid']}(gfx {png})")
    for f in (CFG['voice'], CFG['music']):
        if not os.path.exists(os.path.join(EP, f)): miss.append(f)
    return miss

def cmd_render():
    t0 = time.time(); shots = parse_map()
    miss = missing_list(shots)
    if miss:
        print('STOP: not rendering, missing', len(miss), 'items:'); print(' '.join(miss)); sys.exit(2)
    ensure_gfx(shots)
    print('shots', len(shots), 'total', round(TOTAL, 2), flush=True)
    if '--test' in sys.argv:
        for k in map(int, sys.argv[sys.argv.index('--test') + 1].split(',')): print(shots[k]['sid'], shot(shots[k]))
        return
    done = [0]
    def job(s):
        o = shot(s); done[0] += 1
        if done[0] % 10 == 0: print('rendered', done[0], round(time.time() - t0), flush=True)
        return o
    with ThreadPoolExecutor(JOBS) as ex: clips = list(ex.map(job, shots))
    lst = os.path.join(T, f'list_{W}.txt'); open(lst, 'w').write(''.join(f"file '{c}'\n" for c in clips))
    vid = os.path.join(T, f'video_{W}.mp4'); run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid])
    D = CFG['delay']; aud = ['-i', os.path.join(EP, CFG['voice'])]; fc = []; mix = []
    fc.append(f"[1:a]atrim=0:{VOICE_CUT:.3f},afade=t=out:st={VOICE_CUT-0.2:.3f}:d=0.2,atempo={CFG['tempo']},adelay={int(D*1000)}|{int(D*1000)},"
              "highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=10:release=200,equalizer=f=180:t=q:w=1:g=2,asplit=2[vo][vsc]"); mix.append('[vo]')
    i = 2
    mp = os.path.join(EP, CFG['music'])
    if os.path.exists(mp):
        aud += ['-stream_loop', '-1', '-ss', str(CFG['music_ss']), '-i', mp]
        duck = ''.join(f",volume='if(between(t,{S(b,x0):.2f},{S(b,x1):.2f}),0.15,1)':eval=frame" for b, x0, x1 in CFG['duck'])
        fc.append(f"[{i}:a]volume={CFG['music_vol']}{duck},afade=t=in:d=2,afade=t=out:st={TOTAL-3:.2f}:d=3[mu0]")
        fc.append("[mu0][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[mu]"); mix.append('[mu]'); i += 1
    else: print('WARN no music', mp)
    for f, t, vol, dd in sfx_plan(shots):
        p = sfx_file(f)
        if not p or t < 0 or t > TOTAL: print('skip sfx', f, round(t, 2)); continue
        aud += ['-i', p]
        fc.append(f"[{i}:a]" + (f"atrim=0:{dd:.2f},afade=t=out:st={max(dd-1.2,0):.2f}:d=1.2," if dd else '') + f"volume={vol},adelay={int(t*1000)}|{int(t*1000)}[s{i}]")
        mix.append(f'[s{i}]'); i += 1
    L = CFG['loudness']
    fc.append(''.join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{TOTAL:.3f},alimiter=limit=0.9:level=disabled,"
              f"loudnorm=I={L}:TP=-3:LRA=11,alimiter=limit=0.6:level=disabled,afade=t=out:st={TOTAL-2:.2f}:d=2[a]")
    sc = os.path.join(T, 'mix.txt'); open(sc, 'w').write(';'.join(fc))
    os.makedirs(os.path.join(EP, 'full'), exist_ok=True)
    out = os.path.join(EP, 'full', f"IB{CFG['ep']}_{CFG['name'].replace(' ', '_')}_{'720p_preview' if PREVIEW else '1080p'}.mp4")
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', vid, *aud, '-filter_complex_script', sc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', f'{TOTAL:.3f}', '-movflags', '+faststart', out])
    print('done', out, round(TOTAL, 2), 'sec', round(time.time() - t0), 's', flush=True)

{'shotmap': cmd_shotmap, 'render': cmd_render, 'check': cmd_check}[CMD]()
