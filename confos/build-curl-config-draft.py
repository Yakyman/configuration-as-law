#!/usr/bin/python3
"""Private one-job curl CLI build using exact original shared libcurl."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import urllib.request

root = Path.cwd()
work = root/'interpreter-inputs/curl-config-draft'
size = int(subprocess.check_output(['du','-sx','-B1',str(root)], text=True).split()[0])
assert size <= 48*1024**3 and size+1024**3 < 60*1024**3, size
deps = work/'dependencies'
if not deps.exists():
    shutil.copytree(root/'interpreter-inputs/git/dependencies/root', deps, symlinks=True)
index = (root/'interpreter-inputs/git/dependencies/apt/lists/snapshot.debian.org_archive_debian_20261123T000000Z_dists_trixie_main_binary-amd64_Packages').read_text()
archives = work/'dependency-archives'; archives.mkdir(exist_ok=True)
for name, checksum in [
    ('libcurl4-openssl-dev_8.14.1-2+deb13u7_amd64.deb','65f5a11aa2d8c21019ea0cc6953b5ea25585fa9fd129b1da23d376e32d642adc'),
    ('libcurl4t64_8.14.1-2+deb13u7_amd64.deb','4f89bd3e7a33bbd8f7422817a8a8e2233c9e194fda9c331e33bf98705f525bfc'),
]:
    assert checksum in index and name in index
    path = archives/name
    if not path.exists():
        url = 'https://snapshot.debian.org/archive/debian/20261123T000000Z/pool/main/c/curl/'+name
        with urllib.request.urlopen(url, timeout=90) as response: data=response.read()
        assert hashlib.sha256(data).hexdigest()==checksum
        path.write_bytes(data)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==checksum
    subprocess.run(['dpkg-deb','-x',str(path),str(deps)],check=True)
tree = work/'build-tree'
if not tree.exists(): shutil.copytree(work/'source',tree,symlinks=True)
for name in ('tool_parsecfg.c','confos-curl-config-policy.h'):
    shutil.copyfile(work/'patched/src'/name, tree/'src'/name)
lib = deps/'usr/lib/x86_64-linux-gnu'
env = {**os.environ, 'LC_ALL':'C','TZ':'UTC','SOURCE_DATE_EPOCH':'1795392000',
       'LD_LIBRARY_PATH':str(lib), 'PKG_CONFIG_LIBDIR':str(lib/'pkgconfig'),
       'PKG_CONFIG_SYSROOT_DIR':str(deps), 'DEB_BUILD_MAINT_OPTIONS':'hardening=+all'}
def run(args):
    print('RUN',args,flush=True)
    subprocess.run(args,cwd=tree,env=env,check=True)
def flags(kind):
    return subprocess.check_output(['dpkg-buildflags','--get',kind],env=env,text=True).strip()
env['CFLAGS'] = flags('CFLAGS')+f' -ffile-prefix-map={tree}=/usr/src/curl -D_DEB_HOST_ARCH=\\"x86_64-linux-gnu\\" -DCURL_PATCHSTAMP=\\"8.14.1-2+deb13u7\\"'
env['CPPFLAGS'] = flags('CPPFLAGS')+f' -I{deps}/usr/include -I{deps}/usr/include/x86_64-linux-gnu'
env['LDFLAGS'] = flags('LDFLAGS')+f' -Wl,--no-undefined -L{lib} -Wl,-rpath-link,{lib}'
args = ['./configure','--build=x86_64-linux-gnu','--prefix=/usr','--includedir=/usr/include/x86_64-linux-gnu',
        '--mandir=/usr/share/man','--infodir=/usr/share/info','--sysconfdir=/etc','--localstatedir=/var',
        '--libdir=/usr/lib/x86_64-linux-gnu','--runstatedir=/run','--disable-option-checking',
        '--disable-silent-rules','--disable-maintainer-mode','--disable-dependency-tracking',
        '--disable-symbol-hiding','--enable-versioned-symbols','--enable-threaded-resolver',
        '--with-lber-lib=lber','--with-gssapi='+str(deps/'usr'),'--with-nghttp2',
        '--with-zsh-functions-dir=/usr/share/zsh/vendor-completions',
        '--with-fish-functions-dir=/usr/share/fish/vendor_completions.d',
        '--with-ca-path=/etc/ssl/certs','--with-ca-bundle=/etc/ssl/certs/ca-certificates.crt',
        '--without-libssh','--with-libssh2','--with-openssl','--with-openssl-quic','--with-nghttp3']
provenance = {'configure':args,'environment':{k:env[k] for k in ('CFLAGS','CPPFLAGS','LDFLAGS','PKG_CONFIG_LIBDIR','PKG_CONFIG_SYSROOT_DIR')},
              'compiler':subprocess.check_output(['gcc','--version'],text=True),
              'original_configure':subprocess.check_output([str(deps/'usr/bin/curl-config'),'--configure'],text=True),
              'dependency_archives':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                  [*(root/'interpreter-inputs/git/dependencies/apt/archives').glob('*.deb'),*archives.glob('*.deb')]}}
(work/'build-provenance.json').write_text(json.dumps(provenance,indent=2).replace(str(root),'<build>')+'\n')
run(['autoreconf','-fi'])
run(args)
# Build only the command, linking the original shared library, never a rebuilt
# libcurl or an automatically selected host copy. Override its generated .la prerequisite.
run(['make','-j1','-C','src','curl','curl_DEPENDENCIES=',f'curl_LDADD={lib}/libcurl.so -lz'])
candidate = work/'candidate'; candidate.mkdir(exist_ok=True)
shutil.copyfile(tree/'src/curl',candidate/'curl'); (candidate/'curl').chmod(0o755)
for label, path in [('original',work/'original-package/usr/bin/curl'),('candidate',candidate/'curl')]:
    output=subprocess.check_output([str(path),'--version'],env=env,text=True)
    (work/(label+'-version.txt')).write_text(output)
    (work/(label+'-dynamic.txt')).write_text(subprocess.check_output(['readelf','-d',str(path)],text=True))
    print(label,hashlib.sha256(path.read_bytes()).hexdigest(),output,flush=True)
print('CURL_CONFIG_CLI_BUILD_FINISHED; comparison and controls still required',flush=True)
