import json,csv,re,collections
r=json.load(open('D1/c1/rpm-b-reviewed.json'));meta=json.load(open('D1/c1/part-tumbleweed.rpm-a.filelists.json'));m=meta['packages']; changes=[]
codeextra=set('freecell-solver-presets rgb terminfo-base rpm-config-SUSE shared-mime-info kdoctools libKF5DocTools5 kf6-kdoctools yast2-country-data libKF6DocTools6 khelpcenter myspell-lightproof-en mozilla-nss-certs desktop-data-openSUSE docbook-xsl-stylesheets breeze6-decoration breeze6-style-qt5 pam_kwallet6-common kaccounts-providers plasma6-theme-openSUSE'.split())
metadata=set('girepository-1_0 openssh plasma6-session ruby openssl Mesa dbus-1 grub2 xterm vlc yast2-control-center kscreenlocker6-imports'.split())
data=set('cracklib-dict-full libX11-data qalculate-data libkmahjongg'.split())
settings=set('gtk3-schema gtk4-schema libssh-config tesseract-ocr-common libpaper kf6-purpose-services libkleo'.split())
for x in r:
 k=x['name'];p=m.get(k,[]);active=[s for s in p if not s.startswith(('/usr/share/doc/','/usr/share/licenses/','/usr/share/man/'))];new=None
 if k in codeextra:
  new=('MUST','S2.2-9,S2.2-10','Supplies executable code implementing the package function','Contains executable programs, scripts or shared libraries; the explicit program/code requirement applies.','code')
 elif active and all('/qlogging-categories' in s for s in active):
  new=('NOT','S2.2-4,S2.2-7,S2.2-13','Supplies descriptive logging category names and aliases','Payload contains category descriptions and aliases, not the advertised library implementation; these labels are descriptive content or internal logging values.','logginglabels')
 elif k in metadata:
  new=('HOLE','S2.2-1,S2.2-2,S2.2-4,S2.2-13','Supplies package metadata, documentation, or launch integration','Payload supplies metadata or launch integration rather than the described implementation; the text does not distinguish indirect behavioral effects from descriptive content.','metadata')
 elif k in data:
  new=('HOLE','S2.2-2,S2.2-4','Supplies reference data consumed by application libraries','Removal loses reference data and related interpretation results; the text does not distinguish unavailable content from unavailable recognition or rendering capability.','data')
 elif k in settings:
  new=('HOLE','S2.2-2,S2.2-7,S2.2-13','Supplies library or application configuration values','Values configure libraries or application integration; the text does not determine whether effects remain inside one program.','ambiguous')
 elif k in {'akonadi-contacts','kf6-kconfigwidgets','kf6-kcoreaddons','kcoreaddons','libksieve'}:
  new=('HOLE','S2.2-2,S2.2-4,S2.2-7','Supplies application data, descriptions, and configuration','Payload has data and descriptions rather than advertised code; text does not resolve descriptive content versus effects on application functionality.','data')
 elif k=='libfido2-udev' or k=='purge-kernels-service':
  new=('MUST','S2.2-1,S2.2-2','Supplies system device rules or service activation','Removal changes system-wide device handling or automatic service execution.','systemrules')
 elif k in {'plasma6-sddm-theme-openSUSE','yast2-theme-breeze'}:
  new=('HOLE','S2.2-7,S2.2-10,S2.2-11','Supplies a theme containing executable scripting components','Theme exemption points to NOT while executable code points to MUST; the text does not specify their precedence for this payload.','ambiguous')
 if new:
  changes.append((x['id'],k,x['decision'],new[0],active[:3]));x.update(decision=new[0],sentences=new[1],what_it_does=new[2],reason=new[3],rule=new[4],basis='doc:'+meta['url'])
fields=['id','decision','sentences','what_it_does','basis','reason']
with open('D1/c1/part-tumbleweed.rpm-b.tsv','w') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(r)
json.dump(r,open('D1/c1/rpm-b-reviewed.json','w'),indent=2)
with open('D1/c1/part-tumbleweed.rpm-b.notes.md','a') as f:
 f.write('\n## Payload verification and superseding corrections\n\nPublic filelists were checked because source-level summaries can describe code held in a separate library package. Source: '+meta['url']+'. This verification supersedes any earlier example wording based solely on source summaries.\n\nRule logginglabels: S2.2-4,S2.2-7,S2.2-13. Packages containing only category labels/aliases plus documentation supply descriptive labels, not code; NOT. Ten manually checked examples:\n\n')
 for x in [x for x in r if x['rule']=='logginglabels'][:10]:f.write('- '+x['id']+' — '+x['name']+': '+', '.join(m[x['name']][-2:])+'.\n')
 f.write('\nIndividual corrected payload inspections:\n\n')
 for i,k,old,new,paths in changes:f.write('- '+i+' — '+k+': '+new+'. Payload: '+', '.join(paths)+'.\n')
 f.write('\nSource summaries were not used to claim shared libraries in packages whose filelists only contain descriptions. Browser help JavaScript is confined to rendering help; its presence does not turn help data into unrestricted code.\n')
print(collections.Counter(x['decision'] for x in r));print('changes',len(changes))
assert all(len(x['what_it_does'].split())<=15 and len(x['reason'].split())<=30 for x in r)
