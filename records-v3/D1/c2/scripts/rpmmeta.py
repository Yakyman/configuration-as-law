# Usage: python3 -I rpmmeta.py installed.tsv out.jsonl   (run in the folder holding the four sqlite files)
import sqlite3, sys, json
inst=[l.rstrip('\n').split('\t') for l in open(sys.argv[1]) if l.strip()]
dbs=[]
for tag in ('upd','rel'):
    p=sqlite3.connect(f'{tag}-primary.sqlite'); f=sqlite3.connect(f'{tag}-filelists.sqlite')
    dbs.append((tag,p,f))
out=open(sys.argv[2],'w')
for name,vr,arch in inst:
    ver,rel=vr.rsplit('-',1)
    hit=None
    for exact in (True,False):
        for tag,p,f in dbs:
            q='select pkgKey,pkgId,version,release,summary,description,url,rpm_group,rpm_sourcerpm from packages where name=? and arch=?'
            args=[name,arch]
            if exact: q+=' and version=? and release=?'; args+= [ver,rel]
            r=p.execute(q,args).fetchone()
            if r: hit=(tag,exact,r,f); break
        if hit: break
    if not hit:
        out.write(json.dumps({'name':name,'arch':arch,'vr':vr,'found':False})+'\n'); continue
    tag,exact,r,f=hit
    pkgkey_f=f.execute('select pkgKey from packages where pkgId=?',(r[1],)).fetchone()
    files=[]
    if pkgkey_f:
        for d,names,types in f.execute('select dirname,filenames,filetypes from filelist where pkgKey=?',(pkgkey_f[0],)):
            ns=names.split('/')
            for n,t in zip(ns,types):
                files.append((d.rstrip('/')+'/'+n, t))
    out.write(json.dumps({'name':name,'arch':arch,'vr':vr,'found':True,'repo':tag,'exact':exact,
        'matched':r[2]+'-'+r[3],'summary':r[4],'description':(r[5] or '')[:600],'url':r[6],'srpm':r[8],
        'files':files})+'\n')
