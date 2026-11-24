import json,sys
d={x['path']:x for x in json.load(open(sys.argv[1]))['all_differences']}
c=d['/evidence/commands']; n=0
for a,b in zip(c['left'],c['right']):
    if a!=b:
        n+=1
        same = {k:a[k] for k in a if k!='stdout'}=={k:b[k] for k in b if k!='stdout'} and sorted(a['stdout'].splitlines())==sorted(b['stdout'].splitlines())
        print(a['argv'], 'only line order differs:', same)
print('differing commands', n)
