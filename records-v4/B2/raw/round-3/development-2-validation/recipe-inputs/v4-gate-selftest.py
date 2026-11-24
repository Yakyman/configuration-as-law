#!/usr/bin/python3 -B
"""Observe the cgroup freezer gate and ordinary callers across transactions."""
import hashlib,json,os,pathlib,selectors,shlex,signal,subprocess,sys,time
sys.dont_write_bytecode=True
sys.path.insert(0,'/usr/local/lib/stand')
import stand
import codeboundary
stand.POLICY=codeboundary
P=pathlib.Path
PAUSED=P('/run/stand-shell-paused.json')
PENDING=P('/var/lib/stand/pending.json')
REPORT=P('/var/lib/stand/last-success.json')
CGROOT=P('/sys/fs/cgroup')
FIXTURE=P('/usr/local/share/stand/dev/worker-1.json')
failures=[]

def out(**row):
    row['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    print(json.dumps(row,sort_keys=True),flush=True)

def result(ident,passed,**details):
    out(phase='result',id=ident,passed=bool(passed),**details)
    if not passed:failures.append(ident)

def cgroup(pid):
    for line in P('/proc',str(pid),'cgroup').read_text().splitlines():
        if line.startswith('0::'):return line[3:]
    raise RuntimeError('unified cgroup entry unavailable')

def frozen_state():
    """Read the journal and the kernel freezer acknowledgement, never task T."""
    try:
        journal=json.loads(PAUSED.read_text());groups=journal['groups']
        states={}
        for original,child in groups.items():
            if not child.startswith('/') or child!=original.rstrip('/')+'/.stand-freeze':
                raise ValueError('unexpected freezer path')
            directory=CGROOT/child.lstrip('/')
            events=dict(line.split() for line in (directory/'cgroup.events').read_text().splitlines())
            states[child]={'events':events,'freeze':(directory/'cgroup.freeze').read_text().strip()}
        return journal,states,bool(groups) and all(s['events'].get('frozen')=='1' and s['freeze']=='1' for s in states.values())
    except (FileNotFoundError,ProcessLookupError,json.JSONDecodeError):return {},{},False

def restored_groups(journal):
    return all(not (CGROOT/child.lstrip('/')).exists() for child in journal.get('groups',{}).values())

def kill_group(process):
    if process is None:return
    try:os.killpg(process.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    try:process.wait(timeout=10)
    except subprocess.TimeoutExpired:raise RuntimeError('test process group did not terminate after SIGKILL')

def bounded(argv,timeout=180):
    process=subprocess.Popen(argv,start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        stdout,stderr=process.communicate(timeout=timeout)
        return subprocess.CompletedProcess(argv,process.returncode,stdout,stderr)
    except subprocess.TimeoutExpired:
        kill_group(process)
        raise RuntimeError('bounded test invocation timed out: '+shlex.join(argv))

def shell_argv(command):
    return ['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-shell','-c',command]

def readback(want=None,removed=None):
    rows={r['id']:r for r in stand.load(stand.current_dir())}
    report=json.loads(REPORT.read_text())
    checks=stand.verify(emit=False)
    ok=report.get('status')=='SUCCESS' and report.get('declaration')==stand.current_dir().name and all(c['ok'] for c in checks)
    observed=None
    if want is not None:
        observed=stand.observe(want,stand.current_dir())
        ok=ok and rows.get(want['id'])==want and observed[0]
    if removed is not None:
        ok=ok and removed['id'] not in rows and all(not P(f['path']).exists() for f in removed['files'])
    return ok,{'report':report,'generation':stand.current_dir().name,
               'required_row':want,'required_observation':observed,
               'removed_id':removed['id'] if removed else None,
               'readback_count':len(checks),'readback_failures':[c for c in checks if not c['ok']]}

def heartbeat_gate(worker):
    tick=P('/tmp/v4-shell-heartbeats');pidfile=P('/tmp/v4-shell-heartbeat.pid')
    tick.unlink(missing_ok=True);pidfile.unlink(missing_ok=True)
    command="printf '%s\\n' \"$$\" > /tmp/v4-shell-heartbeat.pid; while :; do printf x >> /tmp/v4-shell-heartbeats; sleep .05; done"
    out(phase='expected',id='APPLY-SHELL-GATE',command=command,
        expected='Kernel cgroup.events acknowledges frozen=1 throughout realization; heartbeat stops; new shell entry refuses; after success heartbeat resumes in original cgroup and private freezer children/journal disappear.')
    observer=subprocess.Popen(shell_argv(command),start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    mutation=None
    try:
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            if pidfile.exists() and tick.exists() and tick.stat().st_size>=3:break
            time.sleep(.05)
        if not pidfile.exists() or not tick.exists() or tick.stat().st_size<3:raise RuntimeError('heartbeat startup failed')
        observed_pid=int(pidfile.read_text());original=cgroup(observed_pid)
        observer_group=cgroup(observer.pid)
        previous_report=REPORT.read_bytes()
        mutation=subprocess.Popen(['/usr/local/bin/stand-pkg','install',str(FIXTURE)],
                                  start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        deadline=time.monotonic()+30;journal={};states={};ack=False
        while time.monotonic()<deadline and mutation.poll() is None:
            journal,states,ack=frozen_state()
            if ack and cgroup(observed_pid) in journal['groups'].values():break
            time.sleep(.02)
        if not ack:raise RuntimeError('kernel freezer acknowledgement not observed')
        frozen_group=cgroup(observed_pid);size=tick.stat().st_size
        entry=bounded(shell_argv('printf PREMATURE'),timeout=20)
        samples=[];freeze_samples=[];deadline=time.monotonic()+240
        while mutation.poll() is None and time.monotonic()<deadline:
            current,kernel,frozen=frozen_state()
            if PENDING.exists() and frozen and REPORT.read_bytes()==previous_report:
                sample=tick.stat().st_size
                # Both observations must lie before report publication; do not
                # mistake a correctly resumed heartbeat for an in-flight write.
                after,after_kernel,after_frozen=frozen_state()
                if PENDING.exists() and after_frozen and REPORT.read_bytes()==previous_report:
                    samples.append(sample);freeze_samples.append(all(v['events'].get('frozen')=='1' for v in after_kernel.values()))
            time.sleep(.05)
        if mutation.poll() is None:raise RuntimeError('application timed out while checking freezer gate')
        stdout,stderr=mutation.communicate(timeout=10)
        deadline=time.monotonic()+10
        while tick.stat().st_size==size and time.monotonic()<deadline:time.sleep(.05)
        actual_group=cgroup(observed_pid)
        actual_observer_group=cgroup(observer.pid)
        good,details=readback(want=worker)
        passed=(len(samples)>10 and all(n==size for n in samples) and all(freeze_samples)
                and entry.returncode!=0 and mutation.returncode==0
                and stdout.startswith('SUCCESS '+details['report']['declaration'])
                and tick.stat().st_size>size and not PAUSED.exists()
                and actual_group==original and actual_observer_group==observer_group
                and restored_groups(journal) and good)
        result('APPLY-SHELL-GATE',passed,journal=journal,kernel_at_pause=states,
               observer_pid=observer.pid,shell_pid=observed_pid,original_cgroup=original,
               frozen_cgroup=frozen_group,restored_cgroup=actual_group,
               observer_original_cgroup=observer_group,observer_restored_cgroup=actual_observer_group,
               heartbeat_size_at_pause=size,sample_count=len(samples),sample_values=sorted(set(samples)),
               entry_exit=entry.returncode,entry_stdout=entry.stdout,entry_stderr=entry.stderr,
               apply_exit=mutation.returncode,apply_stdout=stdout,apply_stderr=stderr,
               resumed=tick.stat().st_size>size,journal_removed=not PAUSED.exists(),
               freezer_children_removed=restored_groups(journal),**details)
    finally:
        if mutation is not None and mutation.poll() is None:kill_group(mutation)
        kill_group(observer)
        tick.unlink(missing_ok=True);pidfile.unlink(missing_ok=True)
    out(phase='expected',id='GATE-FIXTURE-REMOVAL',expected='Remove the recorded gate fixture; declaration and actual executable absent, report valid, freezer journal gone.')
    remove=bounded(['/usr/local/bin/stand-pkg','remove',worker['id']],timeout=240)
    good,details=readback(removed=worker)
    result('GATE-FIXTURE-REMOVAL',remove.returncode==0 and good and not PAUSED.exists(),
           output=remove.stdout,stderr=remove.stderr,journal_removed=not PAUSED.exists(),**details)

def nested_caller(ident,commands,worker):
    """A real ordinary Python parent must survive both synchronous mutations.

    The caller emits completion and waits for a root readback acknowledgement.
    This allows exact installed-state inspection before the next removal call.
    No saved Python script is evaluated by the ordinary process.
    """
    source='''import json,os,pathlib,subprocess,sys
commands=COMMANDS
before=pathlib.Path('/proc/self/cgroup').read_text()
print(json.dumps({'event':'caller-start','pid':os.getpid(),'cgroup':before}),flush=True)
for index,command in enumerate(commands):
 p=subprocess.run(command,capture_output=True,text=True,timeout=180)
 after=pathlib.Path('/proc/self/cgroup').read_text()
 print(json.dumps({'event':'caller-return','index':index,'pid':os.getpid(),'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'before_cgroup':before,'after_cgroup':after}),flush=True)
 if sys.stdin.readline().strip()!='CONTINUE':raise SystemExit(90)
 if p.returncode:raise SystemExit(p.returncode)
print(json.dumps({'event':'caller-complete','pid':os.getpid(),'cgroup':pathlib.Path('/proc/self/cgroup').read_text()}),flush=True)
'''.replace('COMMANDS',repr(commands))
    command=shlex.join(['/usr/bin/python3','-B','-c',source])
    out(phase='expected',id=ident,command=command,package_commands=commands,
        expected='Ordinary Python subprocess.run parent resumes after add and remove; exact row/readback and successful report match; caller cgroup restored after each; no freezer journal/children remain.')
    caller=subprocess.Popen(shell_argv(command),start_new_session=True,stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
    selector=selectors.DefaultSelector();selector.register(caller.stdout,selectors.EVENT_READ)
    start=None;complete=None;returns=[];journals={};lines=[];passed=True
    deadline=time.monotonic()+480
    try:
        while time.monotonic()<deadline:
            # Preserve the actual journal during each transaction so removal of
            # all private children can be checked after the return, not inferred.
            if PAUSED.exists():
                try:
                    live=json.loads(PAUSED.read_text())
                    journals.update(live.get('groups',{}))
                except FileNotFoundError:pass
            events=selector.select(.05)
            if events:
                line=caller.stdout.readline()
                if not line:
                    if caller.poll() is not None:break
                    continue
                lines.append(line.rstrip())
                try:row=json.loads(line)
                except json.JSONDecodeError:continue
                if row.get('event')=='caller-start':start=row
                elif row.get('event')=='caller-return':
                    index=row['index']
                    good,details=readback(want=worker if index==0 else None,removed=worker if index==1 else None)
                    restored=row['before_cgroup']==row['after_cgroup'] and start is not None and row['after_cgroup']==start['cgroup']
                    clean=not PAUSED.exists() and restored_groups({'groups':journals})
                    exact_success=row['stdout'].startswith('SUCCESS '+details['report']['declaration'])
                    accepted=row['rc']==0 and good and restored and clean and exact_success
                    passed=passed and accepted
                    returns.append(row)
                    result(ident+'-'+('INSTALL' if index==0 else 'REMOVE'),accepted,
                           caller_return=row,cgroup_restored=restored,journal_removed=not PAUSED.exists(),
                           freezer_children_removed=restored_groups({'groups':journals}),**details)
                    caller.stdin.write('CONTINUE\n');caller.stdin.flush()
                elif row.get('event')=='caller-complete':complete=row
            if caller.poll() is not None and not events:break
        if caller.poll() is None:
            kill_group(caller)
            raise RuntimeError('ordinary subprocess caller timed out; own process group terminated')
        passed=(passed and caller.returncode==0 and len(returns)==2 and complete is not None
                and start is not None and complete['cgroup']==start['cgroup'] and not PAUSED.exists()
                and restored_groups({'groups':journals}))
        result(ident,passed,caller_exit=caller.returncode,caller_start=start,caller_complete=complete,
               return_count=len(returns),observed_freezer_groups=journals,output=lines,
               journal_removed=not PAUSED.exists(),freezer_children_removed=restored_groups({'groups':journals}))
    finally:
        selector.close()
        if caller.poll() is None:kill_group(caller)
        caller.stdin.close();caller.stdout.close()

def main():
    if os.geteuid()!=0:raise RuntimeError('root controller required')
    worker=json.loads(FIXTURE.read_text())
    initial=(stand.current_dir()/'machine.jsonl').read_bytes()
    if any(r['id']==worker['id'] for r in stand.load(stand.current_dir())):raise RuntimeError('fresh guest without development worker required')
    heartbeat_gate(worker)
    nested_caller('NESTED-BROKER-CALLER',[
        ['/usr/local/bin/stand-pkg','install',str(FIXTURE)],
        ['/usr/local/bin/stand-pkg','remove',worker['id']]],worker)
    nested_caller('NESTED-EDITOR-CALLER',[
        ['/usr/local/bin/v4-editor','package-install',str(FIXTURE)],
        ['/usr/local/bin/v4-editor','package-remove',worker['id']]],worker)
    good,details=readback(removed=worker)
    restored=(stand.current_dir()/'machine.jsonl').read_bytes()==initial
    result('GATE-FINAL-RESTORATION',good and restored and not PAUSED.exists(),
           declaration_restored=restored,journal_removed=not PAUSED.exists(),**details)
    out(phase='summary',passed=not failures,failures=failures)
    return int(bool(failures))

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as error:
        out(phase='summary',passed=False,failures=failures,error=str(error));sys.exit(1)
