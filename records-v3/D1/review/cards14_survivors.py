exec(open('D1/review/cards14_finalextent.py').read().split('out=[]')[0])
for n in ['fonts-noto-color-emoji','fonts-ubuntu','mint-translations','ncurses-base','mint-l-icons']:
 print('\nTARGET',n,meta.get(('mint',n)))
 for user,vs in mi.items():
  if user not in installed['mint']:continue
  for v in vs:
   hit={k:v[k] for k in ['Depends','Pre-Depends','Recommends'] if n in v.get(k,'')}
   if hit:print(user,'installed',installed['mint'][user],'evidence',v['Version'],hit)
