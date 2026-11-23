import json,collections
g=json.load(open('in/raw/coreos/unowned-groups.json'))
E='/'+'etc'
m=g[E+'/systemd']
for f in m[30:]: print(f['type'],f['path'],f['target'][:70])
c=collections.Counter('/'.join(f['path'].split('/')[:6]) for f in g[E+'/selinux']); print(c.most_common(15))
print([ (f['path'],f['size']) for f in g['/boot/grub2'] if not f['path'].endswith('.mod')][:40])
for k in ['/var/cache/rpm-ostree','/var/lib/NetworkManager','/var/lib/nfs','/var/lib/rpm-ostree','/var/lib/systemd','/var/roothome','/var/home/census/.ssh','/var/home/census/Documents','/var/log/journal','/boot/ostree','/boot/loader.0',E+'/dconf']:
    print('==',k); [print('  ',f['type'],f['path'],f['target'][:50],f['size']) for f in g[k][:14]]
