import json
fa=json.load(open('D1/adjudication/work/A/filelists-A.json')); fb=json.load(open('D1/adjudication/work/b_fl/filelists-B.json'))
for names,fs in [('glibc-all-langpacks cracklib-dicts langtable blivet-data evolution-ews-langpacks google-noto-fonts-common',fa),('libtirpc-netconfig terminfo-base hwdata timezone kf6-kcolorscheme desktop-data-openSUSE',fb)]:
 for n in names.split():
  vs=[v for k,v in fs.items() if k.split('|')[0]==n]
  print(n,'FOUND' if vs else 'MISSING')
  for v in vs:
   a=v['files']; print('count',len(a),'first',a[:8])
