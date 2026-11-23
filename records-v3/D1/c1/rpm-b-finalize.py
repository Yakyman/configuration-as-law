exec(open('D1/c1/rpm-b-classify.py').read().split('result=[];unresolved=[]')[0])
pre=json.load(open('D1/c1/rpm-b-preliminary.json')); by={x['id']:x for x in pre}
forced_code=set('libtdb1 libsqlite3-0 liblmdb-0_9_35 libgdbm6 libeot0 libfontenc1 lzop libkfont0 libgdbm_compat4 libldb2 libdb-4_8 libfreetype6 libfontconfig1 fontconfig libXfont2-2 perl-WWW-RobotRules sqlite3 libsqlite3-0-x86-64-v3 libdb-4_8-x86-64-v3 libcrack2 cracklib vim-data vim-data-common xrdb kbd wtmpdb libcfitsio10 libKF6BreezeIcons6 kf6-kiconthemes libKF6IconThemes6 libKF6IconWidgets6 libKF5IconThemes5 mkfontscale fonts-config PackageKit-gtk3-module kf6-purpose-services pkgconf-m4 glibc-gconv-modules-extra systemd-rpm-macros fwupd-efi cnf-bash gcr-ssh-agent layer-shell-qt6 signon-kwallet-extension qqc2-breeze-style6 grantleetheme kgamma6 bolt pipewire-modules-0_3 accountsservice NetworkManager-pptp NetworkManager-openvpn NetworkManager-openconnect purge-kernels-service xdg-desktop-portal PackageKit-gstreamer-plugin vlc-codec-gstreamer grub2-i386-pc cups-pk-helper grub2 kf6-baloo-kioslaves ffmpegthumbs flatpak-kcm6 vlc discover6-notifier plasma6-session gvisor-tap-vsock'.split())
more_data=set('ksysguardsystemstats6-data myspell-lightproof-en media-player-info desktop-data-openSUSE xmlcharent iso_ent docbook_4 tesseract-ocr-traineddata-eng google-poppins-fonts gsettings-desktop-schemas libkdegames libreoffice-l10n-en'.split())
more_settings=set('breeze6-cursors ktnef-debug-categories yast2-trans-stats metatheme-breeze6-common gtk3-metatheme-breeze6 gtk4-metatheme-breeze6 breeze6-wallpapers metatheme-adwaita-common gtk3-metatheme-adwaita yast2-qt-branding-openSUSE plymouth-theme-spinner yast2-theme plymouth-theme-bgrt plymouth-branding-openSUSE grub2-branding-openSUSE plasma6-sddm-theme-openSUSE sddm-qt6-branding-openSUSE sddm-branding-openSUSE plasma6-branding-openSUSE libcontainers-default-policy'.split())
more_system=set('libldap-data netcfg systemd-default-settings-branding-openSUSE systemd-default-settings displaymanager-sysconfig gio-branding-openSUSE xkeyboard-config libcontainers-common'.split())
ambiguous=set('breeze6 breeze6-decoration breeze6-style-qt5 libplasma6-desktoptheme plasma6-theme-openSUSE augeas-lenses docbook-xsl-stylesheets mozilla-nss-certs ca-certificates-mozilla'.split())
unknown=set('pam_kwallet6-common kaccounts-providers'.split())
# Complete individual residual reviews and correct false lexical matches.
for r in rows:
 k=r['name'].split(':',1)[1];v=m.get(k,{});s=v.get('summary','');d=v.get('description','');old=by.get(r['id'])
 typ=None
 if k in forced_code:typ='code'
 elif k in more_data:typ='data'
 elif k in more_settings:typ='settings'
 elif k in more_system:typ='systemrules'
 elif k in ambiguous:typ='ambiguous'
 elif k in unknown:typ='unknown'
 elif k.startswith('patterns-'):typ='metadata'
 elif not old and k.startswith('lib'):typ='code'
 elif not old and k=='dbus-1-common':typ='systemrules'
 if typ:
  template=next((x for x in pre if x['rule']==typ),None)
  if template:x={a:b for a,b in template.items()}
  elif typ=='unknown':x={'decision':'UNKNOWN','sentences':'S3-1,S3-2','reason':'Documentation names support files or providers without establishing whether they are executable code or passive values; ownership inventory is empty.','rule':typ}
  else:x={'decision':'HOLE','sentences':'S2.2-2,S2.2-7,S2.2-10,S2.2-11,S2.2-13','reason':'Documented themes, transformations, or trust data affect behavior; the text does not determine whether interface confinement or single-program settings exemption applies.','rule':typ}
  x.update(id=r['id'],name=k,what_it_does=' '.join(s.replace('\\n',' ').split()[:15]),basis='doc:'+meta['source']);by[r['id']]=x
 elif not old:raise Exception(k)
 if k=='gpg-pubkey':by[r['id']]['basis']='doc:https://rpm.org/docs/6.0.x/man/rpmkeys.8'
# Do not claim broad source description for empty supporting metadata.
fields=['id','decision','sentences','what_it_does','basis','reason']; out=pathlib.Path('D1/c1/part-tumbleweed.rpm-b.tsv')
seen={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
with out.open('a',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore',lineterminator='\n')
 if not seen:w.writeheader()
 for r in rows:
  x=by[r['id']]
  assert len(x['what_it_does'].split())<=15 and len(x['reason'].split())<=30,(x['name'],x['reason'])
  if x['id'] not in seen:w.writerow(x);f.flush()
json.dump(list(by.values()),open('D1/c1/rpm-b-reviewed.json','w'),indent=2)
print(collections.Counter(x['decision'] for x in by.values()));print(collections.Counter(x['rule'] for x in by.values()))
