import csv,json,collections,pathlib
p=pathlib.Path('D1/c1'); head=['id','decision','sentences','what_it_does','basis','reason']
inp=list(csv.DictReader(open('D1/in/part-tumbleweed.tsv'),delimiter='\t'))
source={x['id']:x for x in inp}
a=list(csv.DictReader((p/'part-tumbleweed.rpm-a.tsv').open(),delimiter='\t'))
b=list(csv.DictReader((p/'part-tumbleweed.rpm-b.tsv').open(),delimiter='\t'))
aa={source[x['id']]['members']:x for x in a};bb={source[x['id']]['members']:x for x in b}
assert len(a)==len(b)==2390 and aa.keys()==bb.keys()
f=json.load((p/'part-tumbleweed.rpm-a.filelists.json').open()); fileurl=f['url']
# Literal row-by-row resolutions of the current c1 subdivisions, not another classification.
use_b=set('''iso-codes libnl-config libpaper tesseract-ocr-common Mesa PackageKit-branding-openSUSE dbus-1 grub2 openssl ruby flatpak-remote-flathub kf6-purpose-services kscreenlocker6-imports libkleo libksieve libsemanage-conf plasma6-branding-openSUSE sddm-branding-openSUSE sddm-qt6-branding-openSUSE gtk3-metatheme-adwaita gtk3-metatheme-breeze6 gtk4-metatheme-breeze6 metatheme-adwaita-common metatheme-breeze6-common libplasma6-desktoptheme'''.split())
# Translated interface catalogs expose the same content-versus-localized-output boundary
# as the Flatpak Locale objects. Descriptive documentation remains content.
translations={source[x['id']]['name'].split(':',1)[1] for x in a if x['what_it_does']=='Supplies translated interface text'}
translations.discard('iso-codes')
# Fixed final examples are recorded in the notes; each rule applies to paired membership.
def fresh(dec,sent,what,reason,url=fileurl):
 return dict(decision=dec,sentences=sent,what_it_does=what,basis='doc:'+url,reason=reason)
overrides={
'libkmahjongg':fresh('NOT','S2.2-4','Supplies Mahjongg backgrounds, tile artwork and descriptive theme metadata.','Only the supplied artwork and descriptions become unavailable; filelists establish no game implementation in this package.'),
'NetworkManager-branding-openSUSE':fresh('MUST','S2.2-1,S2.2-2','Configures connectivity probes that affect route metrics and other applications.','Connectivity results change default-route metrics and are exposed to other applications; effects are not confined inside NetworkManager.','https://networkmanager.dev/docs/api/latest/NetworkManager.conf.html'),
'chrony-pool-openSUSE':fresh('MUST','S2.2-1,S2.2-2','Selects the NTP server pool for system clock synchronization.','The configured sources govern the system clock used by other programs; this is not a setting confined inside chrony.'),
'rpm-plugin-selinux':fresh('MUST','S2.2-1,S2.2-2','Configures selection of the RPM SELinux transaction plugin.','The configuration selects labeling of installed files and scriptlets; effects extend beyond RPM. The package itself does not contain plugin code.','https://rpm.org/docs/6.0.x/man/rpm-plugin-selinux.8'),
'dbus-broker-block-restart':fresh('MUST','S2.2-1','Prevents service-manager restart of the system and user message buses.','The service drop-ins constrain restarting separate message-bus processes; their effects are not confined inside one program.'),
'yast2-theme-breeze':fresh('MUST','S2.2-10,S2.2-13','Supplies theme artwork and a shell helper that creates symbolic links.','The packaged Bash script invokes filesystem commands with interpreter rights; executable code remains code even when packaged with theme assets.','https://raw.githubusercontent.com/yast/yast-theme/master/icons/breeze/make-symlinks.sh'),
'libreoffice-filters-optional':fresh('UNKNOWN','S2.2-10,S2.2-11,S3-2','Supplies XSLT import and export transformations for office documents.','Transformation code is established, but evidence does not establish whether this processor confines it or grants the program’s full rights.'),
'ksysguardsystemstats6-data':fresh('NOT','S2.2-4','Describes the system statistics service D-Bus interface.','The package supplies an interface-description XML document, not the service implementation or its activation policy.'),
'kf6-kconfigwidgets':fresh('HOLE','S2.2-2,S2.2-4','Supplies locale descriptions used to construct language-selection interfaces.','Removal loses language-selection descriptions or the ability to present those choices; the text does not distinguish this content from interface capability.'),
}
for name in ['systemd-default-settings','systemd-default-settings-branding-openSUSE','systemd-presets-branding-openSUSE','systemd-presets-common-SUSE']:
 overrides[name]=fresh('MUST','S2.2-1,S2.2-2','Configures service-manager defaults or service activation presets.','These values govern other services and processes; being read by one manager does not confine their effects inside that manager.')
# These are row-specific, separately reviewed settings, not a new name-pattern rule.
# Their existing a decisions establish shared schemas, device profiles and actual directory layouts.
res=[];audit=[]
for k,ar in aa.items():
 br=bb[k];name=source[ar['id']]['name'].split(':',1)[1]
 final=dict(ar); mode='retained first-half functional rule'
 if name in use_b:final=dict(br);mode='specific interface/settings or dependency-metadata boundary'
 if name in translations:
  final=fresh('HOLE','S2.2-2,S2.2-4','Supplies translated interface text.','Removal loses translated-output capability or only translated content; the text does not distinguish those readings.');mode='translated-interface boundary'
 if name in overrides:final=overrides[name];mode='individual factual and textual resolution'
 if ar['decision']!=br['decision'] or name in overrides or name in translations:
  audit.append(dict(name=name,ids=[ar['id'],br['id']],a=ar['decision'],b=br['decision'],final=final['decision'],mode=mode,reason=final['reason']))
 for old in [ar,br]:
  row={'id':old['id'],**{c:final[c] for c in head if c!='id'}}
  assert len(row['what_it_does'].split())<=15,row
  assert len(row['reason'].split())<=30,row
  res.append(row)
with (p/'part-tumbleweed.rpm-final.tsv').open('w',newline='') as out:
 w=csv.DictWriter(out,fieldnames=head,delimiter='\t',lineterminator='\n');w.writeheader()
 for x in res:w.writerow(x);out.flush()
(p/'part-tumbleweed.reconciliation.json').write_text(json.dumps(audit,indent=2))
print('RPM resolved:',len(res),dict(collections.Counter(x['decision'] for x in res)))
print('Translation packages',len(translations))
