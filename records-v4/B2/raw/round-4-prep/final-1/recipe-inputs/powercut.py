#!/usr/bin/env python3
"""One builder add/change/remove cut each, not the actual check's repeated trials."""
import importlib.util,json,os,pathlib,signal,subprocess,sys,time
r=pathlib.Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('lab',r/'lab.py');lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
vm=r/'vms'/sys.argv[1]
for phase in ('add','change','remove'):
    print('PHASE '+phase+' UTC '+time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),flush=True)
    subprocess.run([sys.executable,str(r/'lab.py'),'run',vm.name,'--root'],input=('python3 -B /usr/local/lib/stand/selftest.py prepare-'+phase+'\n').encode(),check=True)
    proc=subprocess.Popen(lab.ssh(vm,root=True)+['sudo -n /usr/local/bin/stand-apply /var/lib/stand/cut-'+phase],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
    seen=False
    for line in proc.stdout:
        if line.startswith('SUCCESS '):
            received=time.monotonic_ns();reported=line.split()[1];pid=lab.live(vm)
            if not pid:raise RuntimeError('VM disappeared before cut')
            os.kill(pid,signal.SIGKILL);cut=time.monotonic_ns();seen=True
            print(line.strip(),flush=True)
            print('POWER_CUT signal=SIGKILL delay_from_marker_ms='+str((cut-received)/1e6),flush=True)
            break
        print(line,end='',flush=True)
    proc.wait(timeout=20)
    if not seen:raise RuntimeError('no success report; no cut performed')
    limit=time.monotonic()+10
    while lab.live(vm) and time.monotonic()<limit:time.sleep(.05)
    subprocess.run([sys.executable,str(r/'lab.py'),'start',vm.name],check=True)
    subprocess.run([sys.executable,str(r/'lab.py'),'run',vm.name,'--root'],input=('set -eu\nselected=$(basename "$(readlink -f /var/lib/stand/current)")\nprintf "REPORTED '+reported+' SELECTED %s\\n" "$selected"\ntest "$selected" = '+reported+'\nstand-verify\n').encode(),check=True)
    print('BOOT_VERIFIED '+phase,flush=True)
