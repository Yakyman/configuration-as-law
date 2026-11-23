exec(open('D1/review/cards14_scan.py').read().split('for h in ')[0])
for m in ['fedora','mint','tumbleweed']:
 ns={x['name'].split(':',1)[-1]:x for x in r if x['machine']==m and x['kind'].startswith('L1:package') and x['id'] not in a and re.search(r'font|theme|lang|l10n|data|dict|terminfo|color|locale|zone|magic|suffix|cmap|netconfig',x['name'],re.I)}
 print(m, '\n'+' '.join(ns))
