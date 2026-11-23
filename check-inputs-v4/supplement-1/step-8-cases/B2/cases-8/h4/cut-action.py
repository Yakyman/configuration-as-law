#!/usr/bin/env python3
"""Host controller: cut the existing virtual NIC during one ordinary action."""
import argparse, importlib.util, json, pathlib, socket, subprocess, sys, time

def qmp(vm, command, arguments=None):
    with socket.socket(socket.AF_UNIX) as sock:
        sock.settimeout(10)
        sock.connect(str(vm / 'qmp.sock'))
        stream = sock.makefile('rwb')
        json.loads(stream.readline())
        replies = []
        for name, args in [('qmp_capabilities', None), (command, arguments)]:
            request = {'execute': name}
            if args is not None: request['arguments'] = args
            stream.write((json.dumps(request)+'\n').encode()); stream.flush()
            while True:
                answer = json.loads(stream.readline())
                replies.append(answer)
                if 'error' in answer: raise RuntimeError(str(answer))
                if 'return' in answer: break
        return replies

GUEST = r'''
import json, pathlib, subprocess, time, traceback
from datetime import datetime, timezone

def stamp(): return datetime.now(timezone.utc).isoformat()
def serial(word):
    with open('/dev/ttyS0', 'w') as stream:
        stream.write('\n'+TOKEN+' '+word+'\n'); stream.flush()
def links():
    result = {}
    for p in pathlib.Path('/sys/class/net').iterdir():
        if p.name == 'lo': continue
        try: result[p.name] = (p/'carrier').read_text().strip()
        except OSError as error: result[p.name] = repr(error)
    return result

def find_action():
    matches = []
    for directory in pathlib.Path('/proc').iterdir():
        if not directory.name.isdecimal(): continue
        try:
            argv = (directory/'cmdline').read_bytes().split(b'\0')
            if MATCH.encode() in argv:
                status = (directory/'status').read_text()
                matches.append({'pid': int(directory.name), 'argv': [x.decode(errors='replace') for x in argv if x], 'status': status})
        except (OSError, ProcessLookupError): pass
    return matches

record = {'label': LABEL, 'command': COMMAND, 'started_utc': stamp(),
          'boot_id': pathlib.Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
          'carrier_before': links()}
child = None
try:
    child = subprocess.Popen(['/usr/sbin/runuser','-u','stand','--',
                              '/usr/local/bin/stand-shell','-c',COMMAND],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    deadline = time.monotonic()+240
    while time.monotonic()<deadline:
        active = find_action()
        if active: break
        if child.poll() is not None: break
        time.sleep(0.005)
    record['active_before_cut'] = active
    if not active:
        raise RuntimeError('selected action was not observed active; no cut requested')
    record['ready_utc'] = stamp(); serial('CUT_READY')
    deadline = time.monotonic()+30
    while time.monotonic()<deadline:
        carrier = links()
        if carrier and all(v=='0' for v in carrier.values()): break
        time.sleep(0.005)
    record['carrier_at_cut'] = carrier
    record['active_at_cut'] = find_action()
    record['cut_seen_utc'] = stamp()
    record['valid_cut'] = bool(record['active_at_cut']) and bool(carrier) and all(v=='0' for v in carrier.values())
    stdout, stderr = child.communicate(timeout=1200)
    record['exit'] = child.returncode
    record['stdout'] = stdout.decode(errors='replace'); record['stderr'] = stderr.decode(errors='replace')
    record['finished_utc'] = stamp()
    record['carrier_before_observation'] = links()
    namespace = {'__name__': 's8_observer'}
    exec(OBSERVER, namespace)
    record['disconnected_observation'] = namespace['collect']()
    record['carrier_after_observation'] = links()
    record['observation_finished_utc'] = stamp()
except BaseException:
    record['controller_error'] = traceback.format_exc()
    if child is not None:
        try:
            stdout, stderr = child.communicate(timeout=15)
            record.update(exit=child.returncode, stdout=stdout.decode(errors='replace'), stderr=stderr.decode(errors='replace'))
        except subprocess.TimeoutExpired: record['action_still_running'] = True
finally:
    serial('OBSERVATION_DONE')
# Keep disconnected observations in memory until the host has restored the NIC.
deadline = time.monotonic()+120
while time.monotonic()<deadline:
    carrier = links()
    if carrier and all(v=='1' for v in carrier.values()): break
    time.sleep(0.1)
record['carrier_at_output'] = carrier
record['output_utc'] = stamp()
print(json.dumps(record, sort_keys=True), flush=True)
'''

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('vm'); parser.add_argument('label'); parser.add_argument('command'); parser.add_argument('match')
    parser.add_argument('--observer', type=pathlib.Path, required=True)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    root = pathlib.Path.cwd(); vm = root/'vms'/args.vm
    spec = importlib.util.spec_from_file_location('s8_lab', root/'lab.py')
    lab = importlib.util.module_from_spec(spec); spec.loader.exec_module(lab)
    args.output.mkdir(parents=True, exist_ok=False)
    token = 'S8H4_'+args.label
    prefix = '\n'.join(name+' = '+repr(value) for name,value in {
        'TOKEN':token, 'LABEL':args.label, 'COMMAND':args.command, 'MATCH':args.match,
        'OBSERVER':args.observer.read_text()}.items())+'\n'
    console = vm/'console.log'; offset = console.stat().st_size
    events = []
    def event(kind, **values):
        events.append(dict(utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()), event=kind, **values))
        (args.output/'host-events.json').write_text(json.dumps(events,indent=2)+'\n')
    with (args.output/'guest.json').open('wb') as stdout, (args.output/'guest.stderr').open('wb') as stderr:
        process = subprocess.Popen(lab.ssh(vm,root=True)+['python3 -B -'], stdin=subprocess.PIPE,stdout=stdout,stderr=stderr)
        process.stdin.write((prefix+GUEST).encode()); process.stdin.close()
        cut = False
        text = ''
        try:
            deadline = time.monotonic()+1500
            while time.monotonic()<deadline:
                with console.open('rb') as stream:
                    stream.seek(offset); text = stream.read().decode(errors='replace')
                if token+' CUT_READY' in text and not cut:
                    event('cut-request', command={'execute':'set_link','arguments':{'name':'net0','up':False}})
                    event('cut-response', replies=qmp(vm,'set_link',{'name':'net0','up':False}))
                    cut = True
                if token+' OBSERVATION_DONE' in text:
                    event('disconnected-observation-complete'); break
                if process.poll() is not None: raise RuntimeError('guest transport exited before serial completion')
                time.sleep(0.01)
            else: raise RuntimeError('timed out waiting for disconnected observation')
        except BaseException as error:
            event('controller-error', error=str(error))
            raise
        finally:
            event('restore-request', command={'execute':'set_link','arguments':{'name':'net0','up':True}})
            restore_error = None
            try:
                event('restore-response', replies=qmp(vm,'set_link',{'name':'net0','up':True}))
            except BaseException as error:
                restore_error = str(error)
                event('restore-error', error=restore_error)
            try:
                result = process.wait(timeout=150)
            except subprocess.TimeoutExpired:
                event('transport-timeout')
                process.terminate()
                try: result = process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    event('transport-termination-timeout')
                    process.kill(); result = process.wait(timeout=10)
            event('transport-finished', exit=result)
            (args.output/'console-markers.txt').write_text('\n'.join(line for line in text.splitlines() if token in line)+'\n')
            if restore_error is not None:
                raise RuntimeError('NIC restoration failed; preserve evidence and destroy the owned guest')

if __name__ == '__main__': main()
