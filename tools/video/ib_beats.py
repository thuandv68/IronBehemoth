"""IronBehemoth beat tool.
  split : python3 ib_beats.py split <EP> [--clip 8|10] [--wpm 148]
          script.md -> beats/beats.tsv  (Bxxx<TAB>words<TAB>text) + beats/meta.json
          clip 8 = Veo 3 / Google Flow (max 20 words/beat), clip 10 = Muse (max 24 words/beat).
          Max words = clip * wpm / 60; sentences longer than max+2 split at commas; units under 6 words merge.
  csv   : python3 ib_beats.py csv <EP> <NNN_slug>
          beats/beats.tsv + beats/beatmap.json + beats/locks.json -> beats/beats_<NNN_slug>.csv
Output columns (template raw/assets/mau_beat.csv):
  beat_id,asset_id,itemType,visual_query,min_media_length,max_media_length,avoid,script,provider,path
  asset_id = Bnnn_Annn (one asset per beat); provider/path left empty for the owner to fill.
beatmap.json: {"B001": {"type": "veo3|footage|image", "desc": "visible scene in English",
                        "camera": "Slow push-in at one steady speed" (veo3, optional),
                        "tank": true/false (optional, auto), "crew": true/false (optional, auto)}}
locks.json  : {"CLIP_SECONDS": (default = clip from split), "STYLE": "...", "TANK": "...", "CREW": "...", "AVOID_AI": "...", "AVOID_AI_TANK": "...",
               "AVOID_WW2": "...", "AVOID_GEN": "...", "MIN_LEN": 8, "MAX_LEN": 15, "WPM": 148}
"""
import sys, os, re, json, csv
CMD, EP = sys.argv[1], os.path.abspath(sys.argv[2])
B = os.path.join(EP, 'beats'); os.makedirs(B, exist_ok=True)

def sentences(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z"\'])', text) if s.strip()]

def split_long(s, maxw):
    w = s.split()
    if len(w) <= maxw: return [s]
    parts, cur = [], []
    for tok in w:
        cur.append(tok)
        if tok.endswith((',', ';', ':')) and len(cur) >= 8: parts.append(' '.join(cur)); cur = []
    if cur: parts.append(' '.join(cur))
    out = []
    for p in parts:   # hard split if still too long
        pw = p.split()
        while len(pw) > maxw: out.append(' '.join(pw[:maxw-2])); pw = pw[maxw-2:]
        if pw: out.append(' '.join(pw))
    return out

def arg(k, d):
    return type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
if CMD == 'split':
    CLIP = arg('--clip', 8); WPM = arg('--wpm', 148); MAXW = int(CLIP * WPM / 60)
    raw = open(os.path.join(EP, 'script.md'), encoding='utf-8').read()
    raw = '\n'.join(l for l in raw.splitlines() if not l.lstrip().startswith('#'))
    units = []
    for s in sentences(raw): units += split_long(s, MAXW + 2)
    beats = []
    for u in units:
        n = len(u.split())
        if beats and (n < 6 or len(beats[-1].split()) < 6) and len(beats[-1].split()) + n <= MAXW: beats[-1] += ' ' + u
        else: beats.append(u)
    with open(os.path.join(B, 'beats.tsv'), 'w', encoding='utf-8') as f:
        for i, t in enumerate(beats): f.write(f'B{i+1:03d}\t{len(t.split())}\t{t}\n')
    tot = sum(len(t.split()) for t in beats)
    json.dump({'clip': CLIP, 'wpm': WPM, 'max_words': MAXW}, open(os.path.join(B, 'meta.json'), 'w'))
    over = [i + 1 for i, t in enumerate(beats) if len(t.split()) > MAXW + 2]
    print('clip', CLIP, 's, max words', MAXW, '| beats', len(beats), 'words', tot, 'est min', round(tot / WPM, 2), '| over-long', over[:10])

elif CMD == 'csv':
    slug = sys.argv[3]
    beats = [l.rstrip('\n').split('\t') for l in open(os.path.join(B, 'beats.tsv'), encoding='utf-8') if l.strip()]
    M = json.load(open(os.path.join(B, 'beatmap.json'), encoding='utf-8'))
    L = json.load(open(os.path.join(B, 'locks.json'), encoding='utf-8'))
    meta = json.load(open(os.path.join(B, 'meta.json'))) if os.path.exists(os.path.join(B, 'meta.json')) else {}
    secs = L.get('CLIP_SECONDS', meta.get('clip', 8))
    TK = re.compile(r'\b(tank|sturmtiger|tiger|panther|sherman|t-34|turret|casemate|gun|barrel|tracks?|hull|vehicle|mortar|breech|armou?r|mantlet|hatch)\b', re.I)
    CR = re.compile(r'\b(crew|crewman|crewmen|driver|gunner|loader|commander|radio operator|soldiers|men|mechanics?)\b', re.I)
    rows, cnt = [], {}
    for bid, wc, text in beats:
        m = M[bid]; typ = m['type']; desc = m['desc'].strip().rstrip('.')
        d = desc[0].upper() + desc[1:]
        tanky = m.get('tank', bool(TK.search(desc))); crewy = m.get('crew', bool(CR.search(desc)) and 'no crew' not in desc.lower())
        r = dict(ref_image='', beat_id=bid, asset_id=f'{bid}_A{bid[1:]}', itemType=typ, script=text, provider='', path='',
                 min_media_length='', max_media_length='')
        if typ == 'veo3':
            cam = m.get('camera', 'Slow push-in at one steady speed').rstrip('.')
            r['visual_query'] = (f"{cam}, single continuous {secs}-second take, no cuts. {d}. "
                                 + (L['TANK'] + ' ' if tanky else '') + (L['CREW'] + ' ' if crewy else '')
                                 + L['STYLE'] + ' One uninterrupted shot.')
            r['avoid'] = L['AVOID_AI_TANK'] if tanky else L['AVOID_AI']
        else:
            r['visual_query'] = desc
            r['avoid'] = L['AVOID_WW2'] if tanky else L['AVOID_GEN']
            if typ == 'footage': r['min_media_length'], r['max_media_length'] = str(L.get('MIN_LEN', 8)), str(L.get('MAX_LEN', 15))
        if m.get('avoid'): r['avoid'] = m['avoid']
        r['ref_image'] = m.get('ref', '')
        cnt[typ] = cnt.get(typ, 0) + 1; rows.append(r)
    cols = ['beat_id', 'asset_id', 'itemType', 'visual_query', 'min_media_length', 'max_media_length', 'avoid', 'script', 'provider', 'path'] + (['ref_image'] if any(M[b].get('ref') for b in M) else [])
    out = os.path.join(B, f'beats_{slug}.csv')
    with open(out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    runs, k = [], 0
    for i in range(1, len(rows) + 1):
        if i == len(rows) or rows[i]['itemType'] != rows[k]['itemType']:
            if i - k > 3: runs.append(f"{rows[k]['beat_id']}..{rows[i-1]['beat_id']} {rows[k]['itemType']} x{i-k}")
            k = i
    wpm = L.get('WPM', 148); words = sum(int(b[1]) for b in beats)
    print(out, len(rows), cnt, 'words', words, 'est min', round(words / wpm, 2))
    if runs: print('WARN runs >3 same type:', '; '.join(runs))
