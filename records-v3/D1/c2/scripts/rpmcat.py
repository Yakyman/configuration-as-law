import json,gzip,re,sys,collections
CODE=[r'^/usr/s?bin/', r'^/usr/libexec/', r'\.so(\.[0-9.]+)?$', r'\.ko(\.(xz|zst|gz))?$', r'\.(py|pyc|pm|pl|rb|lua|tcl|js|mjs|sh|bash|elc?|jar|class|go|php)$',
      r'^/usr/lib/systemd/(system-generators|user-generators|system-shutdown|system-sleep)/', r'^/etc/profile\.d/', r'^/usr/lib/kernel/install\.d/', r'^/boot/vmlinuz', r'^/usr/lib/modules/[^/]+/vmlinuz',
      r'\.efi$', r'^/usr/lib/dracut/modules\.d/.*', r'^/usr/share/gnome-shell/extensions/', r'^/etc/X11/xinit/', r'\.(typelib)$']
code=[re.compile(p) for p in CODE]
def iscode(p): return any(c.search(p) for c in code)
for l in gzip.open(sys.argv[1],'rt'):
    d=json.loads(l)
    fs=[p for p,t in d.get('files',[]) if t!='d']
    c=[p for p in fs if iscode(p)]
    print('\t'.join([d['name'], 'CODE' if c else ('NOFILES' if not fs else 'DATA'), str(len(fs)), str(len(c)), (c[0] if c else (fs[0] if fs else '')), (d.get('summary') or '')]))
