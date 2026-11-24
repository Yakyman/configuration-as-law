#!/usr/bin/python3
"""Private sealed41 original-route reproduction and guarded-reader controls."""
import errno,hashlib,json,os,pty,subprocess as sp
from pathlib import Path
assert os.geteuid()!=0
assert Path('/proc/self/attr/current').read_text().strip()=='confos-session (enforce)'
recorded=Path('/usr/local/share/ed-reader-draft')
meta=json.loads((recorded/'expected.json').read_text())
original='/usr/local/libexec/ed-reader-original';candidate='/usr/bin/ed'
for path,key in [(original,'original_sha256'),(candidate,'sha256'),('/usr/bin/red','red_sha256')]:
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==meta[key],path
assert sp.check_output([original,'--version'])==sp.check_output([candidate,'--version'])
print('ED_READER_EXACT_GUEST_PAYLOAD_VERSION_RED_PASS',flush=True)
work=Path('/home/user/ed-reader-material');work.mkdir(exist_ok=True)
bad=Path('/tmp/ed-reader-unrecorded');positive=Path('/tmp/ed-reader-recorded')
commands=work/'commands';commands.write_text('!touch /tmp/ed-reader-unrecorded\nQ\n')
count=0
def run(label,binary=candidate,source=None,typed=None,marker=None,denied=False,args=(),error=None):
    global count
    if marker:marker.unlink(missing_ok=True)
    stream=source.open() if source else None
    try:result=sp.run([binary,'-s',*args],stdin=stream,input=typed,text=True,capture_output=True,cwd=work,timeout=10)
    finally:
        if stream:stream.close()
    output=result.stdout+result.stderr
    print('ED CONTROL',label,'EXIT',result.returncode,'OUTPUT',repr(output),'MARKER',marker.exists() if marker else None,flush=True)
    if denied:
        assert result.returncode!=0 and 'ConfOS: Permission denied for saved code input' in output,label
        if marker:assert not marker.exists(),label
    elif error:
        assert result.returncode!=0 and error in output and 'ConfOS: Permission denied for saved code input' not in output,label
        if marker:assert not marker.exists(),label
    else:
        assert result.returncode==0,(label,output)
        if marker:assert marker.exists(),label
    count+=1
    return output

run('sealed41 original route089 regular stdin',binary=original,source=commands,marker=bad)
print('ED_READER_ORIGINAL_SAVED_COMMAND_ROUTE_REPRODUCED',flush=True)
run('candidate regular stdin',source=commands,marker=bad,denied=True)
for label,path in [('tmp',Path('/tmp/ed-reader-commands')),('shm',Path('/dev/shm/ed-reader-commands'))]:
    path.write_bytes(commands.read_bytes())
    try:run('candidate '+label,source=path,marker=bad,denied=True)
    finally:path.unlink()
alias=work/'symlink';alias.unlink(missing_ok=True);alias.symlink_to(commands)
hard=work/'hardlink';hard.unlink(missing_ok=True);os.link(commands,hard)
for path in (alias,hard):run('candidate '+path.name,source=path,marker=bad,denied=True)
for prefix in ('/proc/self/fd/','/dev/fd/'):
    with commands.open() as stream:
        run('candidate '+prefix,source=Path(prefix+str(stream.fileno())),marker=bad,denied=True)
run('recorded command file',source=recorded/'positive.ed',marker=positive)
with (recorded/'positive.ed').open() as stream:
    run('recorded descriptor alias',source=Path('/proc/self/fd/'+str(stream.fileno())),marker=positive)
run('typed command pipe',typed='!touch /tmp/ed-reader-recorded\nQ\n',marker=positive)
run('explicit data producer R4',typed=commands.read_text(),marker=bad)

# Actual terminal input stays interactive, not merely a regular-fd exception.
positive.unlink(missing_ok=True)
master,slave=pty.openpty()
process=sp.Popen([candidate,'-s'],stdin=slave,stdout=slave,stderr=slave,cwd=work)
os.close(slave)
try:
    os.write(master,b'!touch /tmp/ed-reader-recorded\nQ\n')
    assert process.wait(timeout=10)==0 and positive.exists()
    output=b''
    while True:
        try:chunk=os.read(master,4096)
        except OSError as exc:
            if exc.errno==errno.EIO:break
            raise
        if not chunk:break
        output+=chunk
    print('ED CONTROL terminal input OUTPUT',repr(output),flush=True);count+=1
finally:
    if process.poll() is None:process.kill();process.wait()
    os.close(master)

document=work/'document';result=work/'result'
data_marker=Path('/tmp/ed-reader-document-not-code');data_marker.unlink(missing_ok=True)
data='alpha\n!touch /tmp/ed-reader-document-not-code\n';document.write_text(data)
for binary in (original,candidate):
    result.unlink(missing_ok=True)
    run('document argument edit '+binary,binary=binary,args=(str(document),),typed='1s/alpha/beta/\nw '+str(result)+'\nQ\n')
    assert result.read_text()==data.replace('alpha','beta') and not data_marker.exists()
    result.unlink()
    run('read/write document data '+binary,binary=binary,typed='r '+str(document)+'\nw '+str(result)+'\nQ\n')
    assert result.read_text()==data and not data_marker.exists()
run('red regular command stream',binary='/usr/bin/red',source=commands,denied=True,marker=bad)
run('red typed shell remains restricted',binary='/usr/bin/red',typed='H\n!touch /tmp/ed-reader-unrecorded\nQ\n',error='Shell access restricted',marker=bad)
run('red recorded shell remains restricted',binary='/usr/bin/red',source=recorded/'restricted.ed',error='Shell access restricted',marker=bad)
run('red typed relative document editing',binary='/usr/bin/red',args=('document',),typed='1s/alpha/gamma/\nw red-result\nQ\n')
assert (work/'red-result').read_text()==data.replace('alpha','gamma') and not data_marker.exists()
run('ordinary syntax error distinguished',typed='H\nZ\nQ\n',error='Unknown command')
print('ED_READER_PRIVATE41_GUEST_MATRIX_PASS',count,flush=True)
