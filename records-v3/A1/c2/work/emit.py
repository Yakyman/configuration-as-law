"""Append decided rows to c2/part-1.tsv (keeps existing rows; skips ids already written)."""
import csv,os,sys
OUT='c2/part-1.tsv'
HDR=['id','decision','sentences','what_it_does','basis','reason']
def written():
    if not os.path.exists(OUT): return set()
    return {r[0] for r in csv.reader(open(OUT),delimiter='\t')}-{'id'}
def emit(rows):
    have=written()
    new=not os.path.exists(OUT)
    with open(OUT,'a',newline='') as f:
        if new: f.write('\t'.join(HDR)+'\n')
        n=0
        for r in rows:
            if r[0] in have: continue
            assert len(r)==6, r
            for x in r: assert '\t' not in x and '\n' not in x, r
            assert r[1] in ('MUST','NOT','HOLE','UNKNOWN','MIXED'), r
            assert len(r[3].split())<=15, ('what too long',r)
            assert len(r[5].split())<=30, ('reason too long',r)
            f.write('\t'.join(r)+'\n'); have.add(r[0]); n+=1
    return n
def inrows():
    return [r for r in csv.reader(open('in/part-1.tsv'),delimiter='\t')][1:]
