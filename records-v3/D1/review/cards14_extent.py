import csv,sys,re,json,pathlib,collections
csv.field_size_limit(sys.maxsize)
r=list(csv.DictReader(open('D1/compare/joined.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE));a={x['id']:x for x in csv.DictReader(open('D1/adjudication/rows.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE)}
extra={'fedora':{'glibc-all-langpacks'},'mint':{'liblouis-data','libthai-data','libx11-data','libopenal-data'}}
exclude={'gpg-pubkey','ca-certificates-mozilla','libtirpc-common','/etc/ssl'}
uncertain={'fedora':{'dns-root-data','blivet-data','evolution-ews-langpacks'},'mint':{'poppler-data','libexttextcat-data','liblangtag-common','liblouisutdml-data','espeak-ng-data:amd64','fontconfig-config'},'tumbleweed':{'terminfo-base','hwdata','timezone','kf6-kcolorscheme','desktop-data-openSUSE'}}
out=[]
for x in r:
 n=x['name'].split(':',1)[-1] if x['name'].startswith(('root:','user:')) else x['name']; old=a.get(x['id'],{})
 state=reason=''
 if old.get('hole') in ('1','2'):
  state='EXCLUDED:MUST' if n in exclude else 'CONFIRMED';reason=old['note']
 elif n in extra.get(x['machine'],set()):
  state='CONFIRMED';reason='Same data-only reference-table kind as source card 2; public package file list checked in cards-1-4.md.'
 elif n in uncertain.get(x['machine'],set()):
  state='UNCERTAIN';reason='Whole-table kind/name match; exact payload or multiple installed readers not established; not counted.'
 if state:out.append([x['id'],x['machine'],x['kind'],x['name'],old.get('hole',''),state,reason])
with open('D1/review/cards-1-4-extent.tsv','w') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['id','machine','kind','name','source_card','membership','evidence']);w.writerows(out)
print(collections.Counter(x[5] for x in out));print(collections.Counter(x[1] for x in out if x[5]=='CONFIRMED'))
# Keep package file lists rather than unrelated website page material.
for p in pathlib.Path('D1/review/cards14-raw').glob('*.html'):
 s=p.read_text();m=re.search(r'<pre>(.*?)</pre>',s,re.S)
 if m:p.with_suffix('.txt').write_text('Source: https://packages.ubuntu.com/noble/all/'+p.stem+'/filelist\n'+m.group(1).strip()+'\n')
 p.unlink()
