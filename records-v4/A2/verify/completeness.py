import csv,itertools,collections,sys
base=sys.argv[1]
rows=list(csv.DictReader(open(base+'/PAIRS.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE))
ids=[r['id'] for r in csv.DictReader(open(base+'/PAIR_SENTENCES.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)]
print(len(ids),ids)
pairs=collections.Counter(frozenset((r['sentence_A'],r['sentence_B'])) for r in rows)
exp=set(frozenset(p) for p in itertools.combinations(ids,2))
print('rows',len(rows),'unique',len(pairs),'dups',[tuple(p) for p,c in pairs.items() if c>1],'missing',len(exp-set(pairs)),'extra',len(set(pairs)-exp))
print(collections.Counter(r['result'] for r in rows))
print(len(set(r['object_tried'] for r in rows)),'distinct objects')
for o,c in collections.Counter(r['object_tried'] for r in rows).most_common(40): print(c,o[:140])
for o,c in collections.Counter(r['reason'] for r in rows).most_common(10): print(c,o[:200])
