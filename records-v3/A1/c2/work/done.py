import csv,collections
c=collections.Counter(r[1] for r in list(csv.reader(open('c2/part-1.tsv'),delimiter='\t'))[1:])
open('c2/part-1.done','w').write(''.join(f'{k}\t{c.get(k,0)}\n' for k in ['MUST','NOT','HOLE','UNKNOWN','MIXED'])+f'TOTAL\t{sum(c.values())}\n')
