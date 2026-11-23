import urllib.request,concurrent.futures,re,pathlib
items={'tw-ncurses':'https://raw.githubusercontent.com/openSUSE/ncurses/master/ncurses.spec','tw-timezone':'https://raw.githubusercontent.com/openSUSE/openSUSE/master/packages/t/timezone/timezone.spec','tw-hwdata':'https://raw.githubusercontent.com/openSUSE/openSUSE/master/packages/h/hwdata/hwdata.spec','tw-kcolorscheme':'https://raw.githubusercontent.com/openSUSE/openSUSE/master/packages/k/kcolorscheme/kcolorscheme.spec','tw-desktop':'https://raw.githubusercontent.com/openSUSE/openSUSE/master/packages/d/desktop-data-openSUSE/desktop-data-openSUSE.spec'}
def get(kv):
 k,u=kv
 try:
  s=urllib.request.urlopen(u,timeout=12).read().decode();print(k,'ok',len(s));pathlib.Path('D1/review/cards14-raw/'+k+'.spec').write_text(s)
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:list(e.map(get,items.items()))
