"""Align beats to ai33 word timestamps.
Usage: python3 ib_align.py <EP>   (beats/beats.tsv + audio/voice.json -> build/beat_times.json)
Output: {"ids":[...], "starts":[...], "ends":[...], "dur": last_word_end}  (voice-file seconds)."""
import sys, os, json, re, difflib
EP=os.path.abspath(sys.argv[1]); os.makedirs(os.path.join(EP,'build'),exist_ok=True)
beats=[l.rstrip('\n').split('\t') for l in open(os.path.join(EP,'beats','beats.tsv'),encoding='utf-8') if l.strip()]
J=json.load(open(os.path.join(EP,'audio','voice.json'))); W=J[0]['words'] if isinstance(J,list) else J['words']
norm=lambda s: re.sub(r"[^a-z0-9']","",s.lower())
vw=[(norm(w.get('text') or w.get('word','')),float(w['start']),float(w['end'])) for w in W if w.get('type','word')=='word']
vw=[w for w in vw if w[0]]
sw=[];owner=[]
for i,(bid,wc,text) in enumerate(beats):
    for t in text.split():
        t=norm(t)
        if t: sw.append(t); owner.append(i)
sm=difflib.SequenceMatcher(None,sw,[w[0] for w in vw],autojunk=False)
mp={}
for a,b,n in sm.get_matching_blocks():
    for k in range(n): mp[a+k]=b+k
starts=[None]*len(beats); ends=[None]*len(beats)
for si,bi in enumerate(owner):
    if si in mp:
        v=vw[mp[si]]
        if starts[bi] is None: starts[bi]=v[1]
        ends[bi]=v[2]
matched=set(owner[s] for s in mp)
for i in range(len(beats)):
    if starts[i] is None: starts[i]=ends[i-1] if i else 0.0
    if ends[i] is None:
        nxt=next((starts[j] for j in range(i+1,len(beats)) if starts[j] is not None),None)
        ends[i]=nxt if nxt else starts[i]+1.0
miss=[beats[i][0] for i in range(len(beats)) if i not in matched]
json.dump({'ids':[b[0] for b in beats],'starts':starts,'ends':ends,'dur':vw[-1][2]},open(os.path.join(EP,'build','beat_times.json'),'w'))
ratio=len(mp)/max(1,len(sw))
print('beats',len(beats),'word match %.1f%%'%(100*ratio),'unmatched beats',miss[:10],'voice end',vw[-1][2])
if ratio<0.9: print('WARN: voice does not match beats.tsv well - regenerate beats or voice')
