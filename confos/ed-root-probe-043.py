#!/usr/bin/python3
"""Root command-input proof with exact refusal, data and recorded positives."""
import os,subprocess,tempfile
from pathlib import Path
assert os.geteuid()==0
assert Path('/proc/self/attr/current').read_text().strip()=='confos-session (enforce)'
marker=Path('/tmp/ed-reader-root-marker');marker.unlink(missing_ok=True)
with tempfile.NamedTemporaryFile(mode='w+',dir='/tmp') as command:
    command.write('!touch /tmp/ed-reader-root-marker\nQ\n');command.flush();command.seek(0)
    result=subprocess.run(['/usr/bin/ed','-s'],stdin=command,text=True,capture_output=True)
    print('ROOT ED REGULAR',result.returncode,repr(result.stdout),repr(result.stderr),flush=True)
    assert result.returncode and 'ConfOS: Permission denied for saved code input' in result.stderr+result.stdout
    assert not marker.exists()
result=subprocess.run(['/usr/bin/ed','-s'],input='!touch /tmp/ed-reader-root-marker\nQ\n',text=True,capture_output=True)
assert result.returncode==0 and marker.exists();marker.unlink()
positive=Path('/tmp/ed-reader-recorded');positive.unlink(missing_ok=True)
with open('/usr/local/share/ed-reader-draft/positive.ed') as stream:
    result=subprocess.run(['/usr/bin/ed','-s'],stdin=stream,text=True,capture_output=True)
assert result.returncode==0 and positive.exists()
positive.unlink()
print('ROOT ED REGULAR REFUSAL TYPED PIPE RECORDED POSITIVE PASS',flush=True)
