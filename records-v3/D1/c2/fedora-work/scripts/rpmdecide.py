# Decide each installed rpm: manual table first, then name patterns, then file-category rules.
import csv,re,sys,json,gzip
mac={}
for l in open('tables/macros.tsv'):
    k,d,s,w,r=l.rstrip('\n').split('\t'); mac[k]=(d,s,w,r)
man={}
for l in open('tables/rpm-manual.tsv'):
    f=l.rstrip('\n').split('\t')+['']*5
    man[f[0]]=f[1:5]
cat={}
for l in open('raw/rpmcat.tsv'):
    f=l.rstrip('\n').split('\t'); cat[f[0]]=f
srpm={}
for l in gzip.open('raw/fedora-rpm-meta.jsonl.gz','rt'):
    d=json.loads(l); srpm[d['name']]=((d.get('srpm') or '').rsplit('-',2)[0], d.get('summary') or '')
R1=('MUST','S2.2-2,S2.2-9,S2.2-10','Ships executable code: ','Package installs programs, libraries or interpreted code that runs with its own or a host program\'s rights; after removal that code cannot run, so something becomes impossible.')
def short(s,n=15):
    w=s.split(); return ' '.join(w[:n])
def decide(name):
    if name in man:
        m=man[name]
        if m[0] in mac:
            d,s,w,r=mac[m[0]]; return (d,s,(m[3] or m[2] or w),r,'manual:'+m[0])
        return (m[0],m[1],m[2],m[3],'manual')
    if name.startswith('default-fonts-'):
        d,s,w,r=mac['META']; return (d,s,w,r,'pattern:META')
    if re.match(r'^(google-noto-.*-fonts|urw-base35-.*-fonts)$',name) and cat[name][1]=='DATA':
        d,s,w,r=mac['FONT']; return (d,s,w,r,'pattern:FONT')
    c=cat[name][1]
    if c=='CODE':
        d,s,w,r=R1; return (d,s,short(w+srpm[name][1],15),r,'rule:R-RPM-CODE')
    if c=='UNIT':
        d,s,w,r=mac['UNIT']; return (d,s,w,r,'rule:UNIT')
    return None
out=open(sys.argv[1],'w')
miss=[]
for name in cat:
    x=decide(name)
    if not x: miss.append((name,cat[name][1],cat[name][5])); continue
    out.write('\t'.join([name]+list(x)+['doc:https://packages.fedoraproject.org/pkgs/%s/%s/'%(srpm[name][0] or name,name)])+'\n')
for m in miss: print('MISSING',*m)
