import csv, sys
from collections import Counter
r=list(csv.DictReader(open(sys.argv[1]),delimiter='\t'))
print(Counter(x['found_files'] for x in r))
print('nometa',sum(1 for x in r if not x['repo']))
print('code>0',sum(1 for x in r if int(x['n_code'])>0))
print('doc only',sum(1 for x in r if x['found_files']=='yes' and int(x['n_code'])==0 and x['data_classes']==''))
print('data',sum(1 for x in r if int(x['n_code'])==0 and x['data_classes']!=''))
for x in r:
  if x['found_files']=='no': print('NF',x['pkg'],x['version'],x['repo'],x['desc'])
