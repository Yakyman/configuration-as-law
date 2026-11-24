#!/usr/bin/python3
"""Prepare a sealed44 derivative with exactly one optional library override."""
from pathlib import Path
text=Path('embedded-python-private-build.py').read_text().replace("work=root/'embedded-python-private'","work=root/'libpython-guest-private'")
text=text.replace("root/'embedded-python-private-probe.py'","root/'libpython-guest-private-probe.py'")
anchor="sp.run(['bash','build.sh',str(inputs/'declaration.conf'),str(work/'disk.qcow2')],cwd=source,check=True)"
insert='''
import gzip,os,re,sys
sys.path.insert(0,str(source));import assemble
rows,snapshot=assemble.parse(inputs/'declaration.conf')
debs=assemble.packages(work/'disk.work',rows,snapshot)
deb=next(p for p in debs if p.name.startswith('libpython3.13_'))
sp.run(['dpkg-deb','-x',str(deb),str(work/'original')],check=True)
original=work/'original/usr/lib/x86_64-linux-gnu/libpython3.13.so.1.0'
candidate=root/'interpreter-inputs/libpython-private/candidate.so'
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
def needed(path):return sorted(re.findall(r'Shared library: \\[(.*?)\\]',sp.check_output(['readelf','-d',str(path)],text=True)))
report['original_needed']=needed(original);report['candidate_needed']=needed(candidate)
(work/'abi.json').write_text(json.dumps(report,indent=2)+'\\n')
for label,path in [('original',original),('candidate',candidate)]:
 for suffix,args in [('dynamic',['readelf','-d']),('symbols',['nm','-D','--defined-only']),('versions',['readelf','--version-info'])]:
  (work/(label+'-'+suffix+'.txt')).write_bytes(sp.check_output([*args,str(path)]))
assert not missing and not changed,report
assert not report['changed_exported_object_sizes'],report
assert report['original_needed']==report['candidate_needed'],report
package=source/'packages/confos-code-readers_0.44_amd64.deb';stage=work/'component'
sp.run(['dpkg-deb','-R',str(package),str(stage)],check=True)
directory=stage/'usr/lib/confos/reader-overrides';manifest=directory/'manifest.json'
entries=json.loads(manifest.read_text());assert not any(e['target']=='/usr/lib/x86_64-linux-gnu/libpython3.13.so.1.0' for e in entries)
entry={'package':'libpython3.13','source_version':'3.13.5-2+deb13u5','target':'/usr/lib/x86_64-linux-gnu/libpython3.13.so.1.0','mode':0o644,'original_sha256':sha(original),'sha256':sha(candidate),'payload':'private-libpython.gz'}
(directory/entry['payload']).write_bytes(gzip.compress(candidate.read_bytes(),mtime=1795392000))
manifest.write_text(json.dumps(entries+[entry],sort_keys=True,indent=2)+'\\n')
for p in [*stage.rglob('*'),stage]:os.utime(p,(1795392000,1795392000),follow_symlinks=False)
sp.run(['dpkg-deb','--root-owner-group','-Zxz','-z6','--build',str(stage),str(package)],check=True,env={**os.environ,'SOURCE_DATE_EPOCH':'1795392000'})
package.with_suffix('.deb.sha256').write_text(sha(package)+'\\n')
(work/'override.json').write_text(json.dumps(entry,indent=2)+'\\n')
'''
assert text.count(anchor)==1
text=text.replace(anchor,insert+anchor).replace('EMBEDDED_PYTHON_PRIVATE44_FIXTURE_BUILT','PRIVATE_LIBPYTHON_GUEST_FIXTURE_BUILT')
Path('libpython-guest-private-build.py').write_text(text)
probe=Path('embedded-python-private-probe.py').read_text()
probe=probe.replace("  assert result.returncode==0 and marker.exists(),(root,name)","  if name in ('saved-home','saved-tmp','regular-stdin'):\n   assert result.returncode!=0 and not marker.exists(),(root,name)\n   assert b'Permission denied' in result.stderr\n  else:assert result.returncode==0 and marker.exists(),(root,name)")
probe=probe.replace('EMBEDDED_PYTHON_SAVED_CODE_BYPASS_CONFIRMED','PRIVATE_LIBPYTHON_SAVED_CODE_REFUSED_CONTROLS_PASS')
Path('libpython-guest-private-probe.py').write_text(probe)
print('LIBPYTHON PRIVATE GUEST RECIPES PREPARED')
