import csv,pathlib,collections,re,json
csv.field_size_limit(10000000)
base=pathlib.Path('D1/c1'); p=base/'part-alma.tsv'
header=['id','decision','sentences','what_it_does','basis','reason']
allowed=['INSTALLED-OWN','INSTALLED-PACKAGE','INSTALLED-DERIVED','PROGRAM-OWN','PROGRAM-DERIVED','SETTING-OWN','SETTING-DEFAULT','RECORD','MATERIAL','RUNTIME','ACTION','GAP-NONE','GAP-TWO','UNKNOWN','MIXED']
source=list(csv.DictReader(open('D1/in/part-alma.tsv'),delimiter='\t'))
with p.open() as f:
 reader=csv.DictReader(f,delimiter='\t');assert reader.fieldnames==header;out=list(reader)
srcids=[r['id'] for r in source];ids=[r['id'] for r in out]
assert len(srcids)==len(ids)==len(set(ids))==len(set(srcids))
assert set(srcids)==set(ids)
sids=set(re.findall(r'\*\*(S8\.[123]-\d+)\*\*',pathlib.Path('SENTENCES.md').read_text()))
for r in out:
 assert set(r)==set(header),r['id']
 assert r['decision'] in allowed,r['id']
 assert len(r['what_it_does'].split())<=15,(r['id'],'what_it_does')
 assert len(r['reason'].split())<=30,(r['id'],'reason')
 assert set(r['sentences'].split(','))<=sids,r['id']
 assert r['basis'] in ['evidence','none'] or r['basis'].startswith(('raw:','doc:')),r['id']
 for v in r.values():assert '\t' not in v and '\n' not in v and '\r' not in v,r['id']
counts=collections.Counter(r['decision'] for r in out)
report={'input_rows':len(source),'output_rows':len(out),'id_sets_equal':True,'ids_unique':True,'decisions_valid':True,'field_word_limits_valid':True,'sentence_ids_valid':True,'counts':{d:counts[d] for d in allowed}}
(base/'part-alma.validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
# Completion marker written only upon explicit final invocation after review.
if __name__=='__main__':
 import sys
 if '--done' in sys.argv:(base/'part-alma.done').write_text('decision\tcount\n'+''.join(f'{d}\t{counts[d]}\n' for d in allowed))
