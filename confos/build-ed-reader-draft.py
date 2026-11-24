#!/usr/bin/python3
"""Pinned private GNU ed command-descriptor guard, one compiler job."""
import difflib,hashlib,json,os,re,shutil,subprocess as sp
from pathlib import Path
root=Path.cwd();work=root/'interpreter-inputs/ed-reader-draft';tree=work/'build-tree'
assert int(sp.check_output(['du','-sx','-B1',str(root)]).split()[0])+1024**3<60*1024**3
assert not tree.exists();shutil.copytree(work/'source',tree)
path=tree/'main_loop.c';original=path.read_text()
assert hashlib.sha256(path.read_bytes()).hexdigest()=='30525f10919a1e841566aef56c6b2c447f2f037604fb9e0ae29875fe67f3f92a'
header=root/'code-file-policy.h'
assert hashlib.sha256(header.read_bytes()).hexdigest()=='64e344ca44ea9859708b0f84fe3c8a41c6a56942eafc3e05a75a1f00434fbea2'
patched=original
for before,after in [
 ('#include "ed.h"','#include "ed.h"\nextern int ed_command_fd_allowed( int fd );'),
 ('    ibufp = get_stdin_line( &len );','    if( !ed_command_fd_allowed( fileno( stdin ) ) ) return 2;\n    ibufp = get_stdin_line( &len );'),
 ('      *ibufpp = get_stdin_line( &len );','      if( !ed_command_fd_allowed( fileno( stdin ) ) ) return ERR;\n      *ibufpp = get_stdin_line( &len );')]:
    assert patched.count(before)==1,before
    patched=patched.replace(before,after)
path.write_text(patched);shutil.copyfile(header,tree/'confos-ed-reader-policy.h')
(tree/'confos-ed-reader-policy.c').write_text('#define _GNU_SOURCE 1\n#include "confos-ed-reader-policy.h"\nint ed_command_fd_allowed(int fd) { return confos_code_fd_allowed(fd); }\n')
makefile=tree/'Makefile.in';mk=makefile.read_text();assert mk.count('objs = buffer.o')==1;makefile.write_text(mk.replace('objs = buffer.o','objs = confos-ed-reader-policy.o buffer.o'))
(work/'ed-reader.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),patched.splitlines(True),fromfile='a/main_loop.c',tofile='b/main_loop.c')))
env={**os.environ,'DEB_BUILD_MAINT_OPTIONS':'hardening=+all','LC_ALL':'C','TZ':'UTC','SOURCE_DATE_EPOCH':'1795392000'}
flags={kind:sp.check_output(['dpkg-buildflags','--get',kind],env=env,text=True).strip() for kind in ('CPPFLAGS','CFLAGS','LDFLAGS')}
flags['CFLAGS']+=' -ffile-prefix-map='+str(tree)+'=/usr/src/ed'
args=['./configure','--prefix=/usr','--bindir=/usr/bin','--mandir=/usr/share/man','--infodir=/usr/share/info',*['%s=%s'%item for item in flags.items()]]
(work/'build-provenance.json').write_text(json.dumps({'configure':args,'compiler':sp.check_output(['gcc','--version'],text=True),
    'toolchain_packages':sp.check_output(['dpkg-query','-W','gcc-14','binutils','libc6-dev','libc6','make','dpkg-dev'],text=True)},indent=2).replace(str(root),'<build>')+'\n')
for command in (args,['make','-j1'],['make','-j1','check']):
    print('RUN',command,flush=True);sp.run(command,cwd=tree,env=env,check=True)
candidate=work/'candidate';candidate.mkdir(exist_ok=True)
for name in ('ed','red'):shutil.copyfile(tree/name,candidate/name);(candidate/name).chmod(0o755)
assert (candidate/'red').read_bytes()==(work/'original/usr/bin/red').read_bytes()
report={}
for label,executable in [('original',work/'original/usr/bin/ed'),('candidate',candidate/'ed')]:
    dynamic=sp.check_output(['readelf','-d',str(executable)],text=True)
    symbols=sp.check_output(['readelf','--dyn-syms','--wide',str(executable)],text=True)
    versions=sp.check_output(['readelf','-V',str(executable)],text=True)
    report[label]={'sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),'needed':sorted(re.findall(r'\(NEEDED\).*\[(.*?)\]',dynamic)),
        'versions':sorted(set(re.findall(r'Name: (\S+)',versions))),
        'exports':sorted(line.split()[7] for line in symbols.splitlines() if len(line.split())>=8 and line.split()[4] in ('GLOBAL','WEAK') and line.split()[6]!='UND'),
        'version':sp.check_output([str(executable),'--version'],text=True)}
    (work/(label+'-dynamic.txt')).write_text(dynamic)
assert report['original']['needed']==report['candidate']['needed']
assert report['original']['version']==report['candidate']['version']
assert report['original']['exports']==report['candidate']['exports']
assert not set(report['candidate']['versions'])-set(report['original']['versions'])
(work/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print('ED_READER_NATIVE_BUILD_UPSTREAM_TESTS_ABI_PASS',report['candidate']['sha256'],flush=True)
