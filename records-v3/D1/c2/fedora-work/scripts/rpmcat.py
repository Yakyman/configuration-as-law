# Categorise each installed rpm by its file list (Fedora 45 repository metadata).
import json,gzip,re,sys
CODE=[r'^/usr/lib/\.build-id/', r'^/s?bin/', r'^/usr/s?bin/', r'^/usr/libexec/', r'^/usr/lib/cups/(backend|filter)/', r'^/usr/lib/udev/[^/]+$',
      r'\.so(\.[0-9.]+)?$', r'\.ko(\.(xz|zst|gz))?$', r'\.(py|pyc|pm|pl|rb|lua|tcl|js|mjs|sh|bash|csh|elc?|jar|class|php|typelib)$',
      r'^/usr/lib/systemd/(system-generators|user-generators|system-shutdown|system-sleep)/', r'^/etc/profile\.d/', r'^/usr/lib/kernel/install\.d/',
      r'^/boot/vmlinuz', r'^/usr/lib/modules/[^/]+/vmlinuz', r'\.efi$', r'^/usr/lib/dracut/modules\.d/', r'^/usr/share/gnome-shell/extensions/']
EXCL=r'^/usr/share/(doc|licenses|help|man)/'
UNIT=r'^/usr/lib/systemd/(system|user)/[^/]+\.(service|socket|timer|path|mount|target|slice)$'
code=[re.compile(p) for p in CODE]
for l in gzip.open(sys.argv[1],'rt'):
    d=json.loads(l)
    fs=[p for p,t in d.get('files',[]) if t!='d']
    c=[p for p in fs if not re.match(EXCL,p) and any(x.search(p) for x in code)]
    u=[p for p in fs if re.match(UNIT,p)]
    cat='CODE' if c else ('UNIT' if u else ('NOFILES' if not fs else 'DATA'))
    print('\t'.join([d['name'], cat, str(len(fs)), str(len(c)), (c[0] if c else (u[0] if u else (fs[0] if fs else ''))), (d.get('summary') or '')]))
