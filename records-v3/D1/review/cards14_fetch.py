import urllib.request,pathlib,concurrent.futures,re
p=pathlib.Path('D1/review/cards14-raw');p.mkdir(exist_ok=True)
names='poppler-data liblouis-data libthai-data libx11-data libglib2.0-data libgdata-common libgphoto2-l10n krb5-locales libexttextcat-data libopenal-data liblangtag-common liblouisutdml-data espeak-ng-data fontconfig-config gnome-desktop3-data evolution-data-server-common cinnamon-desktop-data'.split()
def get(n):
 u='https://packages.ubuntu.com/noble/all/'+n+'/filelist'
 try:
  s=urllib.request.urlopen(u,timeout=20).read().decode();(p/(n+'.html')).write_text(s)
  f=re.search(r'<pre>(.*?)</pre>',s,re.S); ls=f.group(1).strip().splitlines() if f else []
  print(n,len(ls),' | '.join([x for x in ls if not any(t in x for t in ['/share/doc/','/share/locale/'])][:12]),flush=True)
 except Exception as e:print(n,type(e).__name__,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:list(e.map(get,names))
