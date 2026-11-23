import csv,json,sys
csv.field_size_limit(10**9)
rows=list(csv.DictReader(open(sys.argv[1]),delimiter='\t'))
fs=open(sys.argv[2],'rb').read().split(b'\0')
typ={}
for i in range(0,len(fs)-5,6):
    typ[fs[i].decode('utf-8','replace')]=(fs[i+1].decode(),fs[i+2].decode(),fs[i+5].decode('utf-8','replace'))
dirs=set(x['name'] for x in rows if x['kind']=='L2:stored-outside-packages')
out=open(sys.argv[3],'w')
n=0
for x in rows:
    if x['kind']!='L2:stored-outside-packages': continue
    for m in json.loads(x['members']):
        t=typ.get(m,('?','?',''))
        if m in dirs: continue
        n+=1
        out.write(f"{x['name']}\t{m}\t{t[0]}\t{t[1]}\t{t[2]}\n")
print(n, len(dirs))
