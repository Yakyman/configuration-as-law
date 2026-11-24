import csv,random,sys
rows=list(csv.DictReader(open(sys.argv[1]),delimiter='\t',quoting=csv.QUOTE_NONE))
elig=[(i+2,r) for i,r in enumerate(rows) if r['result'] in ('consistent','settled by the order')]
rnd=random.Random(int(sys.argv[2]))
pick=sorted(rnd.sample(elig,30),key=lambda x:x[0])
print('seed',sys.argv[2],'eligible',len(elig))
for ln,r in pick:
    print(f"\n## file line {ln}: {r['sentence_A']} x {r['sentence_B']} [{r['result']}]")
    for k in ('object_tried','effect_A','effect_B','reason','source'): print(f"  {k}: {r[k]}")
