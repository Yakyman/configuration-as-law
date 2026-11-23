"""Supervised finite application, durable report authority and crash reconciliation."""
import json, os, pathlib, select, signal, time

PHASES=('prepare','frozen','quiesce','files','accounts','rules','policy','jobs','readback','commit-ready')
TEST=pathlib.Path('/run/stand-test.json')
READY=pathlib.Path('/run/stand-ready')
IN_WORKER=False

def settings():
    if not TEST.exists():return {}
    s=TEST.stat()
    if s.st_uid or s.st_mode & 0o022:raise ValueError('unsafe test setting')
    return json.loads(TEST.read_text())

def checkpoint(name):
    if not IN_WORKER:return
    import stand as s
    s.atomic('/run/stand-phase',name+'\n')
    cfg=settings()
    if cfg.get('fail_at')==name:raise RuntimeError('injected failure at '+name)
    if cfg.get('stall_at')==name:
        while True:time.sleep(1)

def report():
    import stand as s
    p=s.ROOT/'last-success.json'
    return json.loads(p.read_text()) if p.exists() else None

def generation():
    import stand as s
    item=report()
    return s.ROOT/'generations'/item['declaration'] if item else (s.current_dir() if s.CURRENT.exists() else None)

def recovery():
    """Caller holds application lock; the durable success report is authoritative."""
    import stand as s
    pending=s.ROOT/'pending.json'
    item=json.loads(pending.read_text()) if pending.exists() else None
    target=generation()
    if target is None:raise RuntimeError('no completed declaration for restoration')
    rows=s.load(target)
    candidate=s.ROOT/'generations'/item['candidate'] if item and item.get('candidate') else target
    # Candidate is the possible live source, even if only some of its steps ran.
    old=s.load(candidate) if candidate.exists() else rows
    s.activate(rows,target,old,candidate)
    bad=[r['id'] for r in s.verify(target,False) if not r['ok']]
    if bad:raise RuntimeError('restoration mismatch: '+','.join(bad))
    s.select(target)
    pending.unlink(missing_ok=True);s.syncdir(s.ROOT)
    s.atomic(READY,target.name+'\n')
    return target

def identity(pid):
    try:
        fields=pathlib.Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()
        return fields[19] if fields[0]!='Z' else None
    except (OSError,IndexError):return None

def terminate(pid,expected=None):
    if not pid:return
    if expected is not None and identity(pid)!=expected:return
    try:os.killpg(pid,signal.SIGKILL)
    except ProcessLookupError:pass
    try:os.kill(pid,signal.SIGKILL)
    except ProcessLookupError:pass
    deadline=time.monotonic()+10
    while time.monotonic()<deadline:
        try:
            if os.waitpid(pid,os.WNOHANG)[0]:return
        except ChildProcessError:return
        time.sleep(.02)
    raise RuntimeError('worker did not terminate')

def apply(source):
    import stand as s
    global IN_WORKER
    if (s.ROOT/'pending.json').exists():recovery()
    previous=generation()
    old=s.load(previous) if previous else []
    cfg=settings()
    # Production activation has 55 minutes; the remaining five minutes are the
    # restoration budget. Tests shorten worker time only, not backend semantics.
    timeout=float(cfg.get('timeout_seconds',3300))
    total=float(cfg.get('deadline_seconds',3600))
    if not 1<=timeout<=3300:raise ValueError('invalid test timeout')
    if not timeout<total<=3600:raise ValueError('invalid total deadline')
    started=time.monotonic()
    s.atomic(s.ROOT/'pending.json',s.canonical({'previous':previous.name if previous else None,
        'candidate':None,'supervisor':os.getpid(),'supervisor_identity':identity(os.getpid()),'worker':None,'deadline':started+timeout,
        'recovery_deadline':started+total})+'\n')
    reader,writer=os.pipe()
    gate_read,gate_write=os.pipe()
    pid=os.fork()
    if not pid:
        os.close(reader);os.close(gate_write);os.setsid();IN_WORKER=True
        os.read(gate_read,1);os.close(gate_read)
        try:
            checkpoint('prepare')
            target,rows,ident=s.freeze(source)
            import system_channels
            factory=system_channels.expected_factory(rows,target)
            new={r['id']:r for r in rows}
            for key,row in factory.items():
                if new.get(key)!=row:raise ValueError('factory line change/removal unsupported: '+key)
            for row in rows:
                if row['type']=='port' and row['id'] not in factory:raise ValueError('standalone listener creation unsupported')
            s.atomic(s.ROOT/'pending.json',s.canonical({'previous':previous.name if previous else None,
                'candidate':ident,'supervisor':os.getppid(),'supervisor_identity':identity(os.getppid()),
                'worker':os.getpid(),'worker_identity':identity(os.getpid()),
                'deadline':started+timeout,'recovery_deadline':started+total})+'\n')
            checkpoint('frozen')
            killed=s.activate(rows,target,old,previous)
            bad=[r['id'] for r in s.verify(target,False) if not r['ok']]
            if bad:raise RuntimeError('readback mismatch: '+','.join(bad))
            checkpoint('readback');checkpoint('commit-ready')
            result={'ok':True,'target':ident,'terminated':killed}
        except BaseException as e:result={'ok':False,'error':str(e)}
        os.write(writer,(json.dumps(result)+'\n').encode());os.close(writer);os._exit(0)
    os.close(writer);os.close(gate_read)
    # The worker's durable journal update records its group. The independent
    # watchdog also needs the PID during inert preparation.
    item=json.loads((s.ROOT/'pending.json').read_text())
    if not item.get('worker'):
        item['worker']=pid;item['worker_identity']=identity(pid)
        s.atomic(s.ROOT/'pending.json',s.canonical(item)+'\n')
    os.write(gate_write,b'1');os.close(gate_write)
    handlers={}
    def interrupted(signum,frame):raise InterruptedError('application interrupted')
    for sig in (signal.SIGTERM,signal.SIGHUP,signal.SIGINT):
        handlers[sig]=signal.signal(sig,interrupted)
    committed=False
    try:
        ready,_,_=select.select([reader],[],[],timeout)
        if not ready:raise TimeoutError('worker silence watchdog expired')
        data=b''
        while not data.endswith(b'\n'):
            part=os.read(reader,65536)
            if not part:break
            data+=part
        result=json.loads(data)
        os.waitpid(pid,0);pid=None
        if not result['ok']:raise RuntimeError(result['error'])
        target=s.ROOT/'generations'/result['target']
        # No worker can mutate after ready. Flush the realization before the
        # report. Selection without a report is recoverable as the old state.
        s.select(target);os.sync()
        item={'status':'SUCCESS','declaration':target.name,
              'time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
              'terminated':result['terminated']}
        s.atomic(s.ROOT/'last-success.json',s.canonical(item)+'\n')
        committed=True
        # The durable local report completes application; stdout forwards it.
        (s.ROOT/'pending.json').unlink(missing_ok=True);s.syncdir(s.ROOT)
        s.atomic(READY,target.name+'\n')
        print('SUCCESS '+target.name,flush=True)
        return 0
    except BaseException as error:
        terminate(pid);pid=None
        if committed:
            # Never claim failure/restore an old generation after a success
            # record was published, even when the caller closed stdout.
            return 0
        try:
            item=json.loads((s.ROOT/'pending.json').read_text())
            item['deadline']=item['recovery_deadline']-5
            s.atomic(s.ROOT/'pending.json',s.canonical(item)+'\n')
            if previous:
                recovery()
                print('FAILED restored previous declaration: '+str(error),flush=True)
            else:
                print('FAILED initial application: '+str(error),flush=True)
            return 1
        except BaseException as restore:
            READY.unlink(missing_ok=True)
            print('FAILED recovery incomplete: '+str(error)+'; '+str(restore),flush=True)
            return 1
    finally:
        os.close(reader)
        for sig,handler in handlers.items():signal.signal(sig,handler)

def watchdog():
    """Independent systemd timer recovers a dead or overdue supervisor."""
    import stand as s
    p=s.ROOT/'pending.json'
    if not p.exists():return 0
    item=json.loads(p.read_text());pid=item.get('supervisor')
    alive=pid and identity(pid)==item.get('supervisor_identity')
    if alive and time.monotonic()<item['deadline']+5:return 0
    if alive:
        try:os.kill(pid,signal.SIGKILL)
        except ProcessLookupError:pass
    terminate(item.get('worker'),item.get('worker_identity'))
    with s.transaction():recovery()
    print('WATCHDOG restored durable declaration',flush=True)
    return 0
