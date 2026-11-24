import json,sys
d=json.load(open(sys.argv[1]))['files']
rows=[json.loads(l) for l in d['/var/lib/stand/current/machine.jsonl'].splitlines() if l.strip()]
seen={}
for r in rows:
    t=r['type']; k=(t, r.get('backend'), 'files_manifest' in r, bool(r.get('package_identity')))
    if k in seen: continue
    seen[k]=1
    s={a:(b if not isinstance(b,(list,dict)) or len(json.dumps(b))<300 else (type(b).__name__+' len %d first %s'%(len(b), json.dumps(b[0] if isinstance(b,list) and b else '')[:300]))) for a,b in r.items() if a!='content_b64'}
    print(json.dumps(s)[:1500]); print()
