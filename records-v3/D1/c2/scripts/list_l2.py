import csv,json,sys
csv.field_size_limit(10**9)
r=list(csv.DictReader(open(sys.argv[1]),delimiter='\t'))
for x in r:
    if x['kind']=='L2:stored-outside-packages':
        m=json.loads(x['members'])
        print(x['name'], len(m), ' '.join(str(i) for i in m[:8])[:260])
