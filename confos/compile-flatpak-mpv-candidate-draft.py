#!/usr/bin/python3
"""Compile only patched mpv/libmpv in retained SDK, then compare original runtime."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
recipe=Path('prepare-flatpak-mpv-dependency-headers-draft.py').read_text()
exec(recipe[recipe.index('root = Path.cwd()'):recipe.index('import sys')])
overlay=work/'development-overlay'
exec(recipe[recipe.index('base = '):recipe.index('module=entry')])
build=work/'mpv-zimg-configure'
subprocess.run(base+['meson','setup','--reconfigure','--clearcache','/work/mpv-zimg-configure','/work/mpv','--prefix=/app','--libdir=lib','--wrap-mode=nofallback','-Dbackend_max_links=1',*find(manifest,'mpv')['config-opts'],'-Dsixel=enabled'],check=True)
subprocess.run(base+['ninja','-C','/work/mpv-zimg-configure','-j1','mpv','libmpv.so.2.6.0'],check=True)
candidate=work/'candidate'
for name in ('mpv','libmpv.so.2.6.0'):
    shutil.copyfile(build/name,candidate/name)
    shutil.copymode(build/name,candidate/name)
runtime=root/'interpreter-inputs/flatpak-analysis/root/usr/lib/confos/flatpak/runtime/org.freedesktop.Platform/x86_64/26.08/df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c/files'
runbase=['bwrap','--unshare-all','--die-with-parent','--clearenv','--ro-bind',str(runtime),'/usr','--ro-bind',str(app),'/app','--symlink','usr/bin','/bin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--setenv','PATH','/app/bin:/usr/bin','--setenv','HOME','/tmp','--setenv','LC_ALL','C','--setenv','LD_LIBRARY_PATH','/app/lib:/usr/lib/x86_64-linux-gnu']
features={}
for changed in (False,True):
    command=runbase.copy()
    if changed:
        for name,target in (('mpv','bin/mpv'),('libmpv.so.2.6.0','lib/libmpv.so.2.6.0'),('libluajit-5.1.so.2.1.1781966178','lib/libluajit-5.1.so.2.1.1781966178')):
            command+=['--ro-bind',str(candidate/name),'/app/'+target]
    result=subprocess.run(command+['/app/bin/mpv','--no-config','--load-scripts=no','-v','--idle=no'],capture_output=True,text=True,timeout=30)
    output=result.stdout+result.stderr
    print('RUNTIME_CONTROL_PATCHED',changed,'RC',result.returncode,flush=True)
    print(output,flush=True)
    assert result.returncode == 0
    match=re.search(r'List of enabled features:\s*(.*)',output)
    assert match, 'feature list missing'
    features[str(changed)]=sorted(match[1].split())
def symbols(path):
    output=subprocess.check_output(['readelf','--dyn-syms','--wide',str(path)],text=True)
    return {f[7] for line in output.splitlines() if len(f:=line.split())>=8 and f[4] in ('GLOBAL','WEAK') and f[6]!='UND'}
abi={}
for name,target in (('mpv','bin/mpv'),('libmpv.so.2.6.0','lib/libmpv.so.2.6.0')):
    old,new=symbols(app/target),symbols(candidate/name)
    abi[name]={'missing_exports':sorted(old-new),'added_exports':sorted(new-old),'sha256':hashlib.sha256((candidate/name).read_bytes()).hexdigest()}
    for kind,path in (('original',app/target),('candidate',candidate/name)):
        details=subprocess.check_output(['readelf','-d','-V',str(path)],text=True).replace(str(root),'<build>')
        (work/(name+'-'+kind+'-abi.txt')).write_text(details)
    print('ABI_COMPARISON',name,json.dumps(abi[name]),flush=True)
missing=sorted(set(features['False'])-set(features['True']))
added=sorted(set(features['True'])-set(features['False']))
print('FEATURES_MISSING',missing,'FEATURES_ADDED',added,flush=True)
report={'features':features,'missing_features':missing,'added_features':added,'abi':abi,'compiler':'retained SDK GCC 16.2.0; original complete build toolchain not independently established'}
(work/'mpv-candidate-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
assert not missing and not added, 'feature set differs'
assert all(not row['missing_exports'] for row in abi.values())
print('MPV_LIBMPV_CANDIDATE_ABI_FEATURE_CONTROLS_PASS; confinement untested',flush=True)
