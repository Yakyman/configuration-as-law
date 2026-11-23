# Usage: python3 -I revdeps.py installed.tsv name...   -> installed packages that require something the named package provides (release repo metadata)
import sqlite3,sys
inst=set(l.split('\t')[0] for l in open(sys.argv[1]))
p=sqlite3.connect('rel-primary.sqlite')
for n in sys.argv[2:]:
    r=p.execute('select pkgKey from packages where name=? order by arch="x86_64" desc',(n,)).fetchone()
    if not r: print(n,'NOTFOUND'); continue
    provs=[x[0] for x in p.execute('select name from provides where pkgKey=?',(r[0],))]
    files=[]
    who=set()
    for pr in set(provs+[n]):
        for (k,) in p.execute('select pkgKey from requires where name=?',(pr,)):
            nm=p.execute('select name from packages where pkgKey=?',(k,)).fetchone()[0]
            if nm in inst and nm!=n: who.add(nm)
    print(n,'<-',' '.join(sorted(who)) or '(none)')
