import csv,collections,sys
csv.field_size_limit(10**9)
rows=list(csv.DictReader(open(sys.argv[1]),delimiter='\t'))
by=collections.defaultdict(list)
for r in rows: by[r['kind']].append(r)
skip=set(sys.argv[2:])
for k,v in by.items():
    if k in skip: continue
    print('==',k,len(v))
    for r in v[:3]+v[-1:]:
        print('  ',r['id'],'|',r['name'],'|',r['members'][:250],'|',r['evidence'][:100])
