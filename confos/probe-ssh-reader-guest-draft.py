#!/usr/bin/python3
"""Exact private original/candidate config routes and explicit-data controls."""
import errno,hashlib,json,os,subprocess as sp
from pathlib import Path
assert os.geteuid()!=0
assert Path('/proc/self/attr/current').read_text().strip()=='confos-session (enforce)'
recorded=Path('/usr/local/share/ssh-reader-draft');meta=json.loads((recorded/'expected.json').read_text())
original='/usr/local/libexec/ssh-reader-original';candidate='/usr/bin/ssh'
for path,key in [(original,'original_sha256'),(candidate,'sha256')]:assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==meta[key]
for args in (['-V'],['-Q','cipher'],['-Q','kex'],['-Q','key'],['-Q','mac']):
 a=sp.run([original,*args],capture_output=True,check=True);b=sp.run([candidate,*args],capture_output=True,check=True)
 assert (a.stdout,a.stderr)==(b.stdout,b.stderr),args
print('SSH_READER_GUEST_EXACT_HASH_VERSION_NATIVE_QUERIES_PASS',flush=True)
work=Path('/home/user/ssh-reader-material');work.mkdir(exist_ok=True)
marker=Path('/tmp/ssh-reader-marker')
proxy='Host ssh-reader-test\n ProxyCommand touch /tmp/ssh-reader-marker\n'
match='Match exec "touch /tmp/ssh-reader-marker"\n'
for name,data in [('proxy.conf',proxy),('match.conf',match)]: (work/name).write_text(data)
count=0
def run(label,binary=candidate,config=None,query=True,expected_marker=False,denied=False,typed=None,extra=(),pass_fds=(),stdin=None):
 global count
 marker.unlink(missing_ok=True)
 args=[binary]
 if config is not None:args+=['-F',str(config)]
 args+=['-o','ConnectTimeout=1','-o','BatchMode=yes',*extra]
 if query:args+=['-G']
 args+=['ssh-reader-test']
 result=sp.run(args,input=typed,stdin=stdin,text=True,capture_output=True,cwd=work,pass_fds=pass_fds,timeout=8)
 output=result.stdout+result.stderr
 print('SSH CONTROL',label,'EXIT',result.returncode,'MARKER',marker.exists(),'STDERR',repr(result.stderr),flush=True)
 assert marker.exists()==expected_marker,label
 if denied:assert result.returncode!=0 and 'ConfOS: Permission denied for saved code input' in output,label
 else:
  assert 'ConfOS: Permission denied for saved code input' not in output,label
  assert result.returncode==(0 if query else 255),(label,output)
 count+=1
 return result
run('original route107 ProxyCommand',binary=original,config=work/'proxy.conf',query=False,expected_marker=True)
run('original route108 Match exec',binary=original,config=work/'match.conf',expected_marker=True)
print('SSH_READER_ORIGINAL_ROUTES107_108_REPRODUCED',flush=True)
run('candidate ProxyCommand config',config=work/'proxy.conf',query=False,denied=True)
run('candidate Match exec config',config=work/'match.conf',denied=True)
alias=work/'alias';alias.unlink(missing_ok=True);alias.symlink_to(work/'match.conf')
run('symlink config',config=alias,denied=True)
for prefix in ('/proc/self/fd/','/dev/fd/'):
 for binary in (original,candidate):
  with (work/'match.conf').open() as stream:
   run('regular descriptor alias '+prefix+' '+binary,binary=binary,config=prefix+'0',stdin=stream,
       expected_marker=(binary==original),denied=(binary==candidate))
with (work/'match.conf').open() as stream:run('regular stdin config',config='/dev/stdin',stdin=stream,denied=True)
run('typed config pipe R4',config='/dev/stdin',typed=match,expected_marker=True)
run('explicit producer config pipe R4',config='/dev/stdin',typed=(work/'match.conf').read_text(),expected_marker=True)
run('typed ProxyCommand option',config='/dev/null',query=False,extra=('-o','ProxyCommand=touch /tmp/ssh-reader-marker'),expected_marker=True)
for binary in (original,candidate):
 result=sp.run([binary,'-F','/dev/null','-o','Match exec true','-G','ssh-reader-test'],text=True,capture_output=True)
 assert result.returncode!=0 and 'directive not supported as a command-line option' in result.stderr
 assert 'ConfOS: Permission denied' not in result.stderr
 print('SSH CONTROL native unsupported Match option',binary,result.returncode,repr(result.stderr),flush=True);count+=1
run('recorded Match config',config=recorded/'match.conf',expected_marker=True)
run('recorded Proxy config',config=recorded/'proxy.conf',query=False,expected_marker=True)
run('recorded nested includes',config=recorded/'include-positive.conf',expected_marker=True)
run('recorded include to mutable config',config=recorded/'include-negative.conf',denied=True)
auto=Path('/home/user/.ssh/config');auto.parent.mkdir(exist_ok=True);assert not auto.exists()
try:
 auto.write_text(match)
except OSError as error:
 assert error.errno==errno.EROFS,error
 print('SSH CONTROL automatic user config creation denied by read-only mount',error.errno,flush=True)
 count+=1
else:
 run('original automatic user config',binary=original,expected_marker=True)
 run('candidate automatic user config',denied=True)
 auto.unlink()
# A disposable fixture-only key proves successful ordinary localhost transport.
for binary in (original,candidate):
 result=sp.run([binary,'-F','/dev/null','-i','/usr/local/share/ssh-reader-draft/connection-key',
  '-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null',
  '-o','ConnectTimeout=3','sshcheck@127.0.0.1','printf SSH_READER_CONNECTION_OK'],text=True,capture_output=True,timeout=10)
 print('SSH CONNECTION',binary,'EXIT',result.returncode,'OUT',repr(result.stdout),'ERR',repr(result.stderr),flush=True)
 assert result.returncode==0 and result.stdout=='SSH_READER_CONNECTION_OK';count+=1
print('SSH_READER_PRIVATE42_GUEST_MATRIX_PASS',count,flush=True)
