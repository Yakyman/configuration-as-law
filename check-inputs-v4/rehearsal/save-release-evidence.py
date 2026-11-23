from pathlib import Path
import urllib.request,urllib.error,json,datetime
out=Path(__file__).resolve().parents[1]/'raw/fx-release-evidence'
out.mkdir(exist_ok=True)
urls={'talos-releases.json':'https://api.github.com/repos/siderolabs/talos/releases?per_page=10','nixos-stable.headers':'https://channels.nixos.org/nixos-stable','nixos-26.11.headers':'https://channels.nixos.org/nixos-26.11','void-live.html':'https://repo-default.voidlinux.org/live/','void-current.html':'https://repo-default.voidlinux.org/live/current/','void-enterprise.html':'https://repo-default.voidlinux.org/live/20250401/'}
record=[]
for name,url in urls.items():
 try:r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'release-evidence'}),timeout=30)
 except urllib.error.HTTPError as e:r=e
 except Exception as e:record.append({'name':name,'url':url,'error':str(e)});continue
 data=r.read(20000000)
 if name.endswith('.headers'):data=(str(r.status)+'\n'+str(r.headers)).encode()
 if name.endswith('.json'):
  rows=json.loads(data)
  data=(json.dumps([{'tag_name':x['tag_name'],'published_at':x['published_at'],'prerelease':x['prerelease'],'draft':x['draft'],'html_url':x['html_url']} for x in rows],indent=2)+'\n').encode()
 (out/name).write_bytes(data)
 record.append({'name':name,'url':url,'final_url':r.url,'status':r.status,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(data),'selection':'release metadata fields only' if name.endswith('.json') else 'headers only' if name.endswith('.headers') else 'full bounded page'})
(out/'retrieval.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
