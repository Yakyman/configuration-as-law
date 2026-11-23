import json,re,sys,os
pk=[l.split('\t')[0] for l in open('in/raw/coreos/packages.tsv')]
out={}
for p in pk:
    d=json.load(open(f'c2/raw/mdapi/{p}.json'))
    fl=[]
    for e in (d.get('files') or []):
        names=e['filenames'].split('/'); types=e['filetypes']
        for n,t in zip(names,types): fl.append((e['dirname']+'/'+n,t))
    ex=[f for f,t in fl if t=='f' and (re.match(r'/usr/(s?bin|libexec)/',f) or re.search(r'\.so(\.\d+)*$',f) or f.endswith('.ko.xz') or re.match(r'/usr/lib/systemd/(system|user)/[^/]+\.(service|socket|timer|path|mount)$',f) or re.match(r'/usr/lib/systemd/systemd-',f))]
    fw=[f for f,t in fl if t=='f' and f.startswith('/usr/lib/firmware/')]
    other=[f for f,t in fl if t=='f' and not f.startswith('/usr/lib/.build-id') and not re.match(r'/usr/share/(doc|licenses|man|info|locale)/',f)]
    out[p]=dict(n=len(fl),ex=ex[:3],nex=len(ex),fw=len(fw),other=other[:12],nother=len(other))
json.dump(out,open('c2/work/pkgclass.json','w'),indent=0)
for p,v in out.items():
    if v['nex']==0: print(p,v['n'],'fw=',v['fw'],v['nother'],v['other'])
