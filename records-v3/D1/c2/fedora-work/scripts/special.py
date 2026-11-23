import json,gzip,re,sys
sys.path.insert(0,'')
CODE=[r'^/usr/lib/\.build-id/', r'^/s?bin/', r'^/usr/s?bin/', r'^/usr/libexec/', r'^/usr/lib/cups/(backend|filter)/', r'^/usr/lib/udev/[^/]+$',
      r'\.so(\.[0-9.]+)?$', r'\.ko(\.(xz|zst|gz))?$', r'\.(py|pyc|pm|pl|rb|lua|tcl|js|mjs|sh|bash|csh|elc?|jar|class|php|typelib)$',
      r'^/usr/lib/systemd/(system-generators|user-generators|system-shutdown|system-sleep)/', r'^/etc/profile\.d/', r'^/usr/lib/kernel/install\.d/',
      r'^/boot/vmlinuz', r'^/usr/lib/modules/[^/]+/vmlinuz', r'\.efi$', r'^/usr/lib/dracut/modules\.d/', r'^/usr/share/gnome-shell/extensions/']
EXCL=r'^/usr/share/(doc|licenses|help|man)/'
code=[re.compile(p) for p in CODE]
SPECIAL=re.compile(r'(\.efi$|^/usr/share/(edk2|seabios|qemu|ipxe|cockpit|yelp|javascript|gnome-shell/extensions)/|\.js$|\.typelib$|\.jar$|^/boot/|^/usr/lib/grub/)')
for l in gzip.open(sys.argv[1],'rt'):
    d=json.loads(l)
    fs=[p for p,t in d.get('files',[]) if t!='d']
    c=[p for p in fs if not re.match(EXCL,p) and any(x.search(p) for x in code)]
    if c and all(SPECIAL.search(p) for p in c):
        print(d['name'],len(c),c[:3],'|',d['summary'])
