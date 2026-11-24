import csv, sys, json
csv.field_size_limit(10**9)
rows = list(csv.DictReader(open(sys.argv[1]), delimiter='\t'))
kinds = sys.argv[2].split(',') if len(sys.argv) > 2 else None
width = int(sys.argv[3]) if len(sys.argv) > 3 else 80
for r in rows:
    if kinds and not any(k in r['kind'] for k in kinds):
        continue
    print(r['id'], '|', r['kind'], '|', r['name'][:120], '|', r['members'][:width].replace('\n', ' '), '|', r['evidence'][:100])
