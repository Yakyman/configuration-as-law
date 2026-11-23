import base64,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parent.parent
lines=['set -eu','mkdir -p /tmp/c1-parser-test']
for name in ('main.py','parser-tests.py'):
 data=base64.b64encode((root/'collector'/name).read_bytes()).decode();lines.append("printf %s '"+data+"' | base64 -d > /tmp/c1-parser-test/"+name)
lines+=['cd /tmp/c1-parser-test','python3 -B parser-tests.py','ss -H -lntu','rm -rf /tmp/c1-parser-test']
subprocess.run([str(root/'lab.sh'),'run','col-debian','--root'],input=('\n'.join(lines)+'\n').encode(),check=True,timeout=30)
