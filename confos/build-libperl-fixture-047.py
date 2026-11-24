#!/usr/bin/python3
import hashlib,json,shutil,subprocess as sp
from pathlib import Path
root=Path.cwd();source=root;work=root/'libperl-047-fixture'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
assert Path('VERSION').read_text()=='0.47\n'
assert not work.exists();work.mkdir()
inputs=work/'inputs';shutil.copytree(source/'examples',inputs)
sp.run(['gcc','-O2','-Wall','-Wextra','-Werror','-Wl,--build-id=none','-o',str(inputs/'embedded-perl'),str(root/'embedded-perl-probe.c'),'-ldl'],check=True)
sp.run(['readelf','-d',str(inputs/'embedded-perl')],check=True)
code=b'open my $m, ">", "/tmp/embedded-perl-marker" or die $!; print $m "ran"; close $m; print "EMBEDDED-PERL-CODE ", $>, "\\n";\n'
(inputs/'recorded.pl').write_bytes(code)
shutil.copyfile(root/'libperl-guest-private-probe.py',inputs/'probe.py')
rows=[r for r in (inputs/'development.conf').read_text().splitlines() if r.startswith(('base ','snapshot ','account ','authorized-key '))]
rows.append('package libperl5.40 5.40.1-6+deb13u1')
for name,target,mode in [('embedded-perl','/usr/local/bin/embedded-perl','0755'),('recorded.pl','/usr/local/share/embedded-recorded.pl','0644'),('probe.py','/usr/local/bin/embedded-perl-private-probe.py','0644')]:
 rows.append(f'file {target} {mode} 0:0 {sha(inputs/name)} {name}')
(inputs/'declaration.conf').write_text('\n'.join(rows)+'\n')
sp.run(['bash','build.sh',str(inputs/'declaration.conf'),'images/libperl-047.qcow2'],check=True)
assert sha(root/'images/libperl-047.work/root/usr/lib/x86_64-linux-gnu/libperl.so.5.40.1')=='9055c106dbe1ab867bb2832956a558c3e1d51f2918581c6e192f978a806df3c8'
print('CANONICAL47 LIBPERL FIXTURE BUILT')
