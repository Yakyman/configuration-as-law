import csv,random,json,sys,collections
csv.field_size_limit(10**9)
random.seed(1122)
inp={r['id']:r for r in csv.DictReader(open('../../in/part-fedora.tsv'),delimiter='\t')}
out={l.split('\t')[0]:l.rstrip('\n').split('\t') for l in open('../part-fedora.tsv') if not l.startswith('id\t')}
src={l.split('\t')[0]:l.split('\t')[5] for l in open('tables/rpm-decisions.tsv')}
groups=collections.defaultdict(list)
for i,r in inp.items():
    k=r['kind']
    if k=='L1:package:rpm':
        s=src[r['name'].split(':',1)[1]]
        if s.startswith('manual'): continue
        k='rpm/'+s
    if k in ('L1:service','L1:user-service'): k+=('/notfound' if 'not-found' in r['members'] else '/loaded')
    groups[k].append(i)
for k,v in sorted(groups.items()):
    if len(v)<5 and not k.startswith('rpm'): continue
    print('##',k,len(v))
    for i in random.sample(v,min(10,len(v))):
        o=out[i]; print('  ',i,'|',inp[i]['name'][:60],'|',o[1],'|',o[3])
