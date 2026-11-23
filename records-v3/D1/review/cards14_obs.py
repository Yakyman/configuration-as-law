import urllib.request,concurrent.futures,re,pathlib
pk=['ncurses','timezone','hwdata','kf6-kcolorscheme','desktop-data-openSUSE']
def get(k):
 u='https://api.opensuse.org/public/source/openSUSE:Factory/'+k+'/'+k+'.spec'
 try:
  s=urllib.request.urlopen(u,timeout=15).read().decode();start=s.find('%files'); excerpt=s[start:] if start>=0 else s;excerpt=re.sub(r'^#.*\n','',excerpt,flags=re.M)
  pathlib.Path('D1/review/cards14-raw/tw-'+k+'.txt').write_text('Source: '+u+'\n'+excerpt);print(k,excerpt[:4500])
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:list(e.map(get,pk))
