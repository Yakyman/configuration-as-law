#!/usr/bin/python3
"""Private pinned OpenSSH config-reader build; no host package changes."""
import difflib,hashlib,json,os,re,shutil,subprocess as sp
from pathlib import Path
root=Path.cwd();work=root/'interpreter-inputs/ssh-reader-draft'
assert int(sp.check_output(['du','-sx','-B1',str(root)]).split()[0])+4*1024**3<60*1024**3
apt=work/'apt';deps=work/'dependencies';archives=apt/'archives'
apt.mkdir(exist_ok=True);archives.mkdir(exist_ok=True);(archives/'partial').mkdir(exist_ok=True)
if not (apt/'lists').exists():shutil.copytree(root/'interpreter-inputs/git/dependencies/apt/lists',apt/'lists')
(apt/'sources.list').write_text('deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20261123T000000Z/ trixie main\n')
(apt/'status').touch()
options=['-o',f'Dir::State={apt}','-o',f'Dir::State::status={apt}/status','-o',f'Dir::State::lists={apt}/lists',
 '-o',f'Dir::Cache::archives={archives}','-o',f'Dir::Etc::sourcelist={apt}/sources.list','-o','Dir::Etc::sourceparts=-',
 '-o','APT::Get::List-Cleanup=0','-o','Debug::NoLocking=1','-o','APT::Install-Recommends=false']
packages=['libaudit-dev','libedit-dev','libfido2-dev','libkrb5-dev','libpam0g-dev','libselinux1-dev','libssl-dev','libwrap0-dev','libwtmpdb-dev','zlib1g-dev']
sp.run(['apt-get',*options,'--download-only','-y','install',*packages],check=True)
for archive in sorted(archives.glob('*.deb')):sp.run(['dpkg-deb','-x',str(archive),str(deps)],check=True)
tree=work/'build-tree';assert not tree.exists();shutil.copytree(work/'source',tree,symlinks=True)
path=tree/'readconf.c';original=path.read_text()
anchor='\tif ((f = fopen(filename, "r")) == NULL)\n\t\treturn 0;\n'
assert original.count(anchor)==1
patched=original.replace('#include "includes.h"','#include "includes.h"\n#include "confos-ssh-reader-policy.h"')
assert patched!=original
patched=patched.replace(anchor,anchor+'\tif (!confos_code_fd_allowed(fileno(f))) {\n\t\tfclose(f);\n\t\tfatal("%s: saved configuration input denied", filename);\n\t}\n')
path.write_text(patched)
header=root/'code-file-policy.h';assert hashlib.sha256(header.read_bytes()).hexdigest()=='64e344ca44ea9859708b0f84fe3c8a41c6a56942eafc3e05a75a1f00434fbea2'
shutil.copyfile(header,tree/'confos-ssh-reader-policy.h')
(work/'ssh-reader.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),patched.splitlines(True),fromfile='a/readconf.c',tofile='b/readconf.c')))
lib=deps/'usr/lib/x86_64-linux-gnu'
env={**os.environ,'LC_ALL':'C','TZ':'UTC','SOURCE_DATE_EPOCH':'1795392000','LD_LIBRARY_PATH':str(lib),
 'PKG_CONFIG_LIBDIR':str(lib/'pkgconfig'),'PKG_CONFIG_SYSROOT_DIR':str(deps),'DEB_BUILD_MAINT_OPTIONS':'hardening=+all'}
def flags(kind):return sp.check_output(['dpkg-buildflags','--get',kind],env=env,text=True).strip()
env['CPPFLAGS']=flags('CPPFLAGS')+f' -I{deps}/usr/include -I{deps}/usr/include/x86_64-linux-gnu'
env['CFLAGS']=flags('CFLAGS')+f' -ffile-prefix-map={tree}=/usr/src/openssh -DSSH_EXTRAVERSION=\\"Debian-7+deb13u4\\"'
env['LDFLAGS']='-Wl,--as-needed '+flags('LDFLAGS')+f' -L{lib} -Wl,-rpath-link,{lib}'
args=['./configure','--prefix=/usr','--sysconfdir=/etc/ssh','--libexecdir=/usr/lib/openssh','--disable-strip',
 '--with-mantype=doc','--with-4in6','--with-privsep-path=/run/sshd','--with-pid-dir=/run','ac_cv_func_mkdtemp=no',
 'PATH_PASSWD_PROG=/usr/bin/passwd','--with-tcp-wrappers','--with-pam','--with-libedit','--with-kerberos5='+str(deps/'usr'),
 '--with-ssl-engine','--with-wtmpdb','--with-selinux','--with-audit=linux','--with-security-key-builtin',
 '--with-xauth=/usr/bin/xauth','--with-default-path=/usr/local/bin:/usr/bin:/bin:/usr/games',
 '--with-superuser-path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin']
(work/'build-provenance.json').write_text(json.dumps({'configure':args,'environment':{k:env[k] for k in ('CFLAGS','CPPFLAGS','LDFLAGS','PKG_CONFIG_LIBDIR','PKG_CONFIG_SYSROOT_DIR')},
 'toolchain':sp.check_output(['dpkg-query','-W','gcc-14','binutils','libc6-dev','libc6','make','autoconf'],text=True),
 'archives':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in archives.glob('*.deb')}},indent=2).replace(str(root),'<build>')+'\n')
for cmd in (['autoreconf','-fi'],args):
 print('RUN',cmd,flush=True);sp.run(cmd,cwd=tree,env=env,check=True)
config=tree/'config.h';config.write_text(re.sub(r'^.*#define USE_BTMP .*$', '/* #undef USE_BTMP */',config.read_text(),flags=re.M))
sp.run(['make','-j1','ASKPASS_PROGRAM=/usr/bin/ssh-askpass','ssh'],cwd=tree,env=env,check=True)
candidate=work/'candidate';candidate.mkdir(exist_ok=True);shutil.copyfile(tree/'ssh',candidate/'ssh');(candidate/'ssh').chmod(0o755)
report={}
for label,path in [('original',work/'original/usr/bin/ssh'),('candidate',candidate/'ssh')]:
 dynamic=sp.check_output(['readelf','-d',str(path)],text=True)
 symbols=sp.check_output(['readelf','-W','--dyn-syms',str(path)],text=True)
 versions=sp.check_output(['readelf','-V',str(path)],text=True)
 report[label]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'needed':sorted(re.findall(r'\(NEEDED\).*\[(.*?)\]',dynamic)),
 'versions':sorted(set(re.findall(r'Name: (\S+)',versions))),
 'exports':sorted(line.split()[7] for line in symbols.splitlines() if len(line.split())>=8 and line.split()[4] in ('GLOBAL','WEAK') and line.split()[6]!='UND'),
 'version':sp.check_output([str(path),'-V'],stderr=sp.STDOUT,env=env,text=True),
 'queries':{q:sp.check_output([str(path),'-Q',q],env=env,text=True) for q in ('cipher','cipher-auth','mac','kex','key','key-sig','sig','protocol-version')}}
 (work/(label+'-symbols.txt')).write_text(symbols);(work/(label+'-dynamic.txt')).write_text(dynamic)
(work/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
for field in ('needed','versions','exports','version','queries'):assert report['original'][field]==report['candidate'][field],field
print('SSH_READER_NATIVE_FEATURES_ABI_PASS',report['candidate']['sha256'],flush=True)
