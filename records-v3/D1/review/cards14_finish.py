import csv,collections,pathlib,re
p=pathlib.Path('D1/review/cards-1-4-extent.tsv');rs=list(csv.DictReader(p.open(),delimiter='\t'))
for r in rs:
 n=r['name'].split(':',1)[-1]
 if r['machine']=='tumbleweed' and n=='desktop-translations':r['membership']='EXCLUDED:MUST';r['evidence']='Exact RPM header Supplements includes yast2-control-center, installed 5.0.3-1.6; S2.2-1 package selection. cards14-raw/tumbleweed-desktop-translations-header.json'
 if r['machine']=='mint' and n in ['dmz-cursor-theme','fonts-noto-cjk','wamerican','yaru-theme-icon']:
  r['membership']='EXCLUDED:MUST';r['evidence']='Exact installed-version package has maintainer scripts executed by a shell with package-manager rights; S2.2-10. cards14-raw/mint-'+n+'-control.json'
 if r['machine']=='mint' and n=='ncurses-base':r['membership']='EXCLUDED:MUST';r['evidence']='Exact installed-version Essential: yes metadata governs package-removal authorization, independently of terminfo payload; S2.2-1. cards14-raw/mint-ncurses-base-control.json'
 if r['machine']=='mint' and n=='fonts-noto-color-emoji':r['membership']='CONFIRMED';r['evidence']='Exact installed 2.047-0ubuntu0.24.04.1 control: no Depends/Pre-Depends/Recommends/Suggests/Conflicts/Breaks/Replaces/Provides/Essential/Protected; no scripts/triggers. No reverse dependency in downloaded installed-package metadata. Font payload remains content/capability boundary. cards14-raw/mint-fonts-noto-color-emoji-control.json'
 if r['membership']=='UNKNOWN' and n in ['fonts-ubuntu','mint-translations','mint-l-icons']:r['evidence']='No forward dependency; a current different-version installed-consumer source names a reverse dependency, but exact installed consumer version unavailable (404): plymouth-label, mint-common or mint-l-theme respectively. Cannot prove or dismiss whole-package operational metadata.'
with p.open('w') as f:w=csv.DictWriter(f,fieldnames=rs[0],delimiter='\t');w.writeheader();w.writerows(rs)
print(collections.Counter((r['machine'],r['membership']) for r in rs));print('SOURCE',collections.Counter((r['source_card'],r['membership']) for r in rs))
ex=['fedora-825992c02de7410b9de93d54','tumbleweed-25d4e59fef6a08262890c4c4','fedora-f6384d9de305cf7440d4a349','tumbleweed-d8620423f05d02d99e676201','mint-f029447dfa5b81e83920cfc2','fedora-e94d6040fe6b71468614c285','tumbleweed-819b570cdea5ea55df85afe1','fedora-1616320aeaca00e35b428e9b','tumbleweed-eaa3bb18d4c9f9d9e224e05d','mint-cef67297df4b26083898d0be','tumbleweed-856378d1c349da9571edbf48','tumbleweed-cb6bae922bf2ef3c7006b5b6','tumbleweed-d8740b0efbb387551a5f8266','mint-ef80a80feb7709633f6d40e4']
by={r['id']:r for r in rs}
for i in ex:
 r=by[i];print(i,r['name'],r['membership'],r['evidence'])
for r in rs:
 if r['membership']=='CONFIRMED':print('CONFIRMED_ID',r['id'])
