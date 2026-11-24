#!/usr/bin/env python3
"""Run the complete original suite and BC1 regressions on fresh server VMs."""
import hashlib,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
phase=sys.argv[1]
if phase not in ('integration','rebuilt'):raise SystemExit('integration or rebuilt required')
out=ROOT/'raw'/phase
out.mkdir(parents=True,exist_ok=True)
if (out/'round1.jsonl').exists():raise SystemExit('observation already exists')
def run(args,log,script=None):
    with (out/log).open('wb') as stream:
        result=subprocess.run(list(map(str,args)),cwd=ROOT,input=script,stdout=stream,stderr=subprocess.STDOUT,
                              env={**os.environ,'STAND_EVIDENCE_DIR':phase+'/original'})
    print(log+' EXIT '+str(result.returncode),flush=True)
    return result.returncode
status=run([sys.executable,ROOT/'build/development.py'],'original-console.log')
name='bc1-'+phase
try:
    status|=run([sys.executable,ROOT/'lab.py','new',name,'stand'],'new.log')
    if (ROOT/'vms'/name/'meta.json').exists():
        status|=run([sys.executable,ROOT/'lab.py','run',name,'--root'],'round1.jsonl',
                    b'#!/usr/bin/python3 -I\n'+(ROOT/'build/round1-selftest.py').read_bytes())
        run([sys.executable,ROOT/'lab.py','run',name,'--root'],'policy-state.log',b'''set -eu
date -u +%FT%TZ
sudo -l -U stand
cat /etc/stand/backend-paths.json
cat /etc/dbus-1/system.d/zz-stand.conf
cat /etc/polkit-1/rules.d/00-stand.rules
/usr/bin/systemctl is-enabled user@.service cron.service atd.service || true
/usr/bin/systemctl is-active user@1000.service cron.service atd.service || true
stat -c '%a %U %G %n' /usr/bin/apt-get /usr/bin/dpkg /usr/lib/systemd/systemd /var/lib/stand/generations
''')
finally:
    if (ROOT/'vms'/name).exists():
        if run([sys.executable,ROOT/'lab.py','destroy',name],'destroy.log'):
            run([sys.executable,ROOT/'lab.py','kill',name],'kill.log')
            run([sys.executable,ROOT/'lab.py','destroy',name],'destroy-after-kill.log')
with (ROOT/'base/stand.qcow2').open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
(out/'summary.json').write_text(json.dumps({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
    'suite_exit':status,'image_sha256':digest,'vms_remaining':[p.name for p in (ROOT/'vms').glob('*')]},indent=2)+'\n')
raise SystemExit(status)
