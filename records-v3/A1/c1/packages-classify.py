import csv,json,re,pathlib
rows=[r for r in csv.DictReader(open('A1/in/part-1.tsv'),delimiter='\t') if r['kind']=='package']
docs={d['id']:d for d in map(json.loads,open('A1/c1/package-docs.jsonl'))}
# These require individual inspection, not the executable-code rule.
special=set('WALinuxAgent-udev adcli-selinux amd-gpu-firmware amd-ucode-firmware audit-rules azure-vm-utils bash-color-prompt ca-certificates console-login-helper-messages container-selinux containers-common containers-common-extra coreutils-common crypto-policies dbus-common efi-filesystem elfutils-default-yama-scope fedora-gpg-keys fedora-release-common fedora-release-coreos fedora-release-identity-coreos fedora-repos fedora-repos-archive filesystem fuse-common glibc-minimal-langpack gnulib-l10n google-compute-engine-guest-configs-udev grub2-common hwdata ignition-grub intel-gpu-firmware kbd-legacy kbd-misc kernel libreport-filesystem linux-firmware linux-firmware-whence moby-filesystem nano-default-editor ncurses-base nftables-services nvidia-gpu-firmware passt-selinux pcre2-syntax publicsuffix-list-dafsa qed-firmware rdma-core-common samba-common selinux-policy selinux-policy-targeted setup shared-mime-info tzdata vim-data xkeyboard-config iptables-services'.split())
p=pathlib.Path('A1/c1/part-1.packages.tsv');done=set()
if p.exists():done={r['id'] for r in csv.DictReader(p.open(),delimiter='\t')}
with p.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not p.stat().st_size:w.writerow('id decision sentences what_it_does basis reason'.split())
 for r in rows:
  d=docs.get(r['id'],{})
  if r['id'] in done or 'summary' not in d or r['name'] in special:continue
  s=d['summary'];fun=s if len(s.split())<=15 else 'Provides '+r['name']+' executable functionality.'
  lib= bool(re.search(r'librar|\bAPI\b',s,re.I)) or r['name'].startswith('lib') or r['name'] in 'cyrus-sasl-gssapi duktape fstrm glibc-gconv-extra gnutls json-c nss nss-altfiles nss-softokn nss-sysinit nspr ngtcp2 ngtcp2-crypto-gnutls protobuf-c sssd-ad sssd-ipa sssd-krb5 sssd-common-pac sssd-ldap sssd-nfs-idmap tpm2-tss tpm2-tss-fapi wasmedge-rt'.split()
  script=r['name'] in 'bash-completion afterburn-dracut clevis-dracut clevis-systemd cloud-utils-growpart dracut-network dracut-squash console-login-helper-messages-issuegen console-login-helper-messages-motdgen console-login-helper-messages-profile pkgconf-m4'.split()
  sentences='S2.2-1,S2.2-2,S2.2-10' if lib or script else 'S2.2-1,S2.2-2,S2.2-9'
  reason='Supplies executable code run with the loading program’s rights; removing it removes that implementation.' if lib or script else 'Supplies an executable program; removing it makes its provided operation unavailable.'
  w.writerow([r['id'],'MUST',sentences,fun,'doc:'+d['url'],reason]);f.flush()
print('Written',sum(1 for _ in p.open())-1)
print('Pending',[(r['name'],docs.get(r['id'],{}).get('error','special')) for r in rows if r['id'] not in {z['id'] for z in csv.DictReader(p.open(),delimiter='\t')}])
