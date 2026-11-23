#!/usr/bin/env python3
"""Single synthetic check of handoff and controller-death GUI cleanup."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

actions = Path(__file__).resolve().parents[1] / 'actions'
sys.path.insert(0, str(actions))
from gui_guard import live_members

child = "import os,signal,time; p=os.fork(); signal.signal(signal.SIGTERM,signal.SIG_IGN); os._exit(0) if p else time.sleep(120)"
controller_source = """import os,sys,time
sys.path.insert(0,sys.argv[1])
from gui_guard import start
p=start([sys.executable,'-c',sys.argv[2]],dict(os.environ))
print(p.pid,flush=True)
time.sleep(120)
"""
controller = subprocess.Popen([sys.executable, '-c', controller_source, str(actions), child],
                              stdout=subprocess.PIPE, text=True)
group = None
try:
    group = int(controller.stdout.readline())
    time.sleep(2)
    handoff = group in live_members(group) and len(live_members(group)) >= 2
    controller.kill()
    controller.wait(timeout=5)
    deadline = time.monotonic() + 22
    while live_members(group) and time.monotonic() < deadline:
        time.sleep(0.2)
    cleaned = not live_members(group)
    result = {'handoff_guardian_and_child_alive': handoff,
              'controller_killed': controller.returncode == -signal.SIGKILL,
              'no_live_group_members_after_eof': cleaned}
    print(json.dumps(result, sort_keys=True))
    assert all(result.values())
finally:
    if controller.poll() is None:
        controller.kill()
        controller.wait()
    if group is not None and live_members(group):
        os.killpg(group, signal.SIGKILL)
