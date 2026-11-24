#!/usr/bin/python3
import hashlib,json,shutil,subprocess as sp,tarfile
from pathlib import Path
root=Path.cwd();work=root/'libperl-guest-private';source=work/'source'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
archive=root/'releases/confos-0.45-source.tar.gz'
assert sha(archive)=='85f0992d602dd8adeed161f893a8d2ff0348047c826f5d42f7e011d83b3d5f86'
assert int(sp.check_output(['du','-sx','-B1',str(root)]).split()[0])+6*1024**3<60*1024**3
assert not work.exists();source.mkdir(parents=True)
with tarfile.open(archive) as tar:
 members=[m for m in tar.getmembers() if len(Path(m.name).parts)==1 or Path(m.name).parts[0] in ('components','examples','packages')]
 assert sum(m.size for m in members)<2*1024**3
 tar.extractall(source,members=members,filter='data')
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
(work/'composition.json').write_text(json.dumps({'source_sha256':sha(archive),'probe_source_sha256':sha(root/'embedded-perl-probe.c'),'binary_sha256':sha(inputs/'embedded-perl'),'declaration_sha256':sha(inputs/'declaration.conf')},indent=2)+'\n')
import gzip,os,re,sys
sys.path.insert(0,str(source));import assemble
rows,snapshot=assemble.parse(inputs/'declaration.conf')
debs=assemble.packages(work/'disk.work',rows,snapshot)
deb=next(p for p in debs if p.name.startswith('libperl5.40_'))
sp.run(['dpkg-deb','-x',str(deb),str(work/'original')],check=True)
original=work/'original/usr/lib/x86_64-linux-gnu/libperl.so.5.40.1'
candidate=root/'interpreter-inputs/libperl-private/candidate.so'
def symbols(path):
 return {line.split()[0]:line.split()[1] for line in sp.check_output(['nm','-D','--defined-only','--format=posix',str(path)],text=True).splitlines()}
old,new=symbols(original),symbols(candidate)
missing=sorted(set(old)-set(new));changed={k:[old[k],new[k]] for k in old.keys()&new.keys() if old[k]!=new[k]}
report={'original_sha256':sha(original),'candidate_sha256':sha(candidate),'package_sha256':sha(deb),'missing_symbols':missing,'changed_symbol_types':changed,'added_symbols':sorted(set(new)-set(old))}
def object_sizes(path):
 fields=[line.split() for line in sp.check_output(['nm','-D','-S','--defined-only','--format=posix',str(path)],text=True).splitlines()]
 return {r[0]:r[3] for r in fields if len(r)>=4 and r[1] in 'BbDdRrSsGgVv'}
old_sizes,new_sizes=object_sizes(original),object_sizes(candidate)
report['changed_exported_object_sizes']={k:[value,new_sizes.get(k)] for k,value in old_sizes.items() if new_sizes.get(k)!=value}
def needed(path):return sorted(re.findall(r'Shared library: \[(.*?)\]',sp.check_output(['readelf','-d',str(path)],text=True)))
report['original_needed']=needed(original);report['candidate_needed']=needed(candidate)
(work/'abi.json').write_text(json.dumps(report,indent=2)+'\n')
for label,path in [('original',original),('candidate',candidate)]:
 for suffix,args in [('dynamic',['readelf','-d']),('symbols',['nm','-D','--defined-only']),('versions',['readelf','--version-info'])]:
  (work/(label+'-'+suffix+'.txt')).write_bytes(sp.check_output([*args,str(path)]))
assert not missing and not changed,report
assert not report['changed_exported_object_sizes'],report
assert report['original_needed']==report['candidate_needed'],report
package=source/'packages/confos-code-readers_0.45_amd64.deb';stage=work/'component'
sp.run(['dpkg-deb','-R',str(package),str(stage)],check=True)
directory=stage/'usr/lib/confos/reader-overrides';manifest=directory/'manifest.json'
entries=json.loads(manifest.read_text());assert not any(e['target']=='/usr/lib/x86_64-linux-gnu/libperl.so.5.40.1' for e in entries)
entry={'package':'libperl5.40','source_version':'5.40.1-6+deb13u1','target':'/usr/lib/x86_64-linux-gnu/libperl.so.5.40.1','mode':0o644,'original_sha256':sha(original),'sha256':sha(candidate),'payload':'private-libperl.gz'}
(directory/entry['payload']).write_bytes(gzip.compress(candidate.read_bytes(),mtime=1795392000))
manifest.write_text(json.dumps(entries+[entry],sort_keys=True,indent=2)+'\n')
for p in [*stage.rglob('*'),stage]:os.utime(p,(1795392000,1795392000),follow_symlinks=False)
sp.run(['dpkg-deb','--root-owner-group','-Zxz','-z6','--build',str(stage),str(package)],check=True,env={**os.environ,'SOURCE_DATE_EPOCH':'1795392000'})
package.with_suffix('.deb.sha256').write_text(sha(package)+'\n')
(work/'override.json').write_text(json.dumps(entry,indent=2)+'\n')
sp.run(['bash','build.sh',str(inputs/'declaration.conf'),str(work/'disk.qcow2')],cwd=source,check=True)
sp.run(['readelf','-d',str(work/'disk.work/root/usr/lib/x86_64-linux-gnu/libperl.so.5.40')],check=True)
print('EMBEDDED_PERL_PRIVATE45_FIXTURE_BUILT',flush=True)
