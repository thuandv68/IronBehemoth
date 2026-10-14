"""Decode a browser download bundle into files.
Usage: python3 ib_unbundle.py <bundle.json> <out_dir>
Bundle: {"files": {"name.ext": "<base64>", ...}, ...other keys kept in _meta.json}
Also accepts the ai33 bundle {"audio_b64": "...", "transcript": {...}} -> voice.mp3 + voice.json"""
import sys, os, json, base64
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
J = json.load(open(src, encoding='utf-8'))
n = 0
for name, b in (J.get('files') or {}).items():
    if ',' in b[:80] and b.startswith('data:'): b = b.split(',', 1)[1]
    open(os.path.join(out, os.path.basename(name)), 'wb').write(base64.b64decode(b)); n += 1
if 'audio_b64' in J:
    open(os.path.join(out, 'voice.mp3'), 'wb').write(base64.b64decode(J['audio_b64'])); n += 1
    json.dump(J.get('transcript'), open(os.path.join(out, 'voice.json'), 'w'), ensure_ascii=False); n += 1
meta = {k: v for k, v in J.items() if k not in ('files', 'audio_b64', 'transcript')}
if meta: json.dump(meta, open(os.path.join(out, '_meta.json'), 'w'), ensure_ascii=False, indent=1)
print('wrote', n, 'files to', out)
