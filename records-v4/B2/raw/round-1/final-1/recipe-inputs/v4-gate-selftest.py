#!/usr/bin/python3 -B
"""Observe concurrent ordinary execution across a declaration transaction."""
import json,os,pathlib,signal,subprocess,time
P=pathlib.Path
def out(**r):
    r['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());print(json.dumps(r,sort_keys=True),flush=True)
tick=P('/tmp/v4-shell-heartbeats');tick.unlink(missing_ok=True)
command="while :; do printf x >> /tmp/v4-shell-heartbeats; sleep .05; done"
out(phase='expected',id='APPLY-SHELL-GATE',command=command,expected='existing shell stops throughout realization, then resumes only after report; new entry refuses while pending')
observer=subprocess.Popen(['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-shell','-c',command],start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
deadline=time.monotonic()+10
while (not tick.exists() or tick.stat().st_size<3) and time.monotonic()<deadline:time.sleep(.05)
try:
    previous_report=P('/var/lib/stand/last-success.json').read_bytes()
    mutation=subprocess.Popen(['/usr/local/bin/stand-pkg','install','/usr/local/share/stand/dev/worker-1.json'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    pending=P('/var/lib/stand/pending.json');paused=P('/run/stand-shell-paused.json')
    deadline=time.monotonic()+15;identities={}
    while time.monotonic()<deadline:
        if paused.exists():
            identities=json.loads(paused.read_text())
            if identities and all(P('/proc',pid,'stat').read_text().split(') ',1)[1][0] in ('T','t') for pid in identities):break
        time.sleep(.02)
    size=tick.stat().st_size
    entry=subprocess.run(['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-shell','-c','printf PREMATURE'],capture_output=True,text=True)
    samples=[]
    while mutation.poll() is None:
        if pending.exists() and paused.exists() and P('/var/lib/stand/last-success.json').read_bytes()==previous_report:
            sample=tick.stat().st_size
            if pending.exists() and paused.exists() and P('/var/lib/stand/last-success.json').read_bytes()==previous_report:samples.append(sample)
        time.sleep(.05)
    stdout,stderr=mutation.communicate(timeout=30)
    deadline=time.monotonic()+5
    while tick.stat().st_size==size and time.monotonic()<deadline:time.sleep(.05)
    report=json.loads(P('/var/lib/stand/last-success.json').read_text())
    passed=bool(identities) and len(samples)>10 and all(n==size for n in samples) and entry.returncode!=0 and mutation.returncode==0 and stdout.startswith('SUCCESS '+report['declaration']) and tick.stat().st_size>size and not paused.exists()
    out(phase='result',id='APPLY-SHELL-GATE',passed=passed,paused_pids=identities,heartbeat_size_at_pause=size,sample_count=len(samples),sample_values=sorted(set(samples)),entry_exit=entry.returncode,entry_stdout=entry.stdout,entry_stderr=entry.stderr,apply_exit=mutation.returncode,apply_stdout=stdout,apply_stderr=stderr,report=report,resumed=tick.stat().st_size>size)
finally:
    os.killpg(observer.pid,signal.SIGKILL);observer.wait();tick.unlink(missing_ok=True)
remove=subprocess.run(['/usr/local/bin/stand-pkg','remove','dev-worker'],capture_output=True,text=True)
out(phase='result',id='GATE-FIXTURE-REMOVAL',passed=remove.returncode==0,output=remove.stdout,stderr=remove.stderr)
raise SystemExit(int(not passed or remove.returncode!=0))
