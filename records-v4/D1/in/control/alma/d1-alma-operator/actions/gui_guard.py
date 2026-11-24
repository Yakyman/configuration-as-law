#!/usr/bin/env python3
"""Own-group GUI supervision; no inventory or application output is interpreted."""
# https://docs.python.org/3/library/subprocess.html
# https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import time


def live_members(group, exclude=None):
    members = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isdecimal() or int(entry.name) == exclude:
            continue
        try:
            if os.getpgid(int(entry.name)) != group:
                continue
            fields = (entry / 'stat').read_text().rsplit(')', 1)[1].split()
            if fields[0] not in ('Z', 'X', 'x'):
                members.append(int(entry.name))
        except (FileNotFoundError, ProcessLookupError):
            pass
    return members


def start(command, env):
    # A new group, but the existing batch session: outer session cleanup retains
    # authority. Closing this pipe, including on controller death, requests stop.
    return subprocess.Popen([sys.executable, str(Path(__file__).resolve()), *command],
                            stdin=subprocess.PIPE, env=env, process_group=0)


def stop(process):
    if process.stdin is not None:
        process.stdin.close()
    try:
        process.wait(timeout=22)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)
    deadline = time.monotonic() + 5
    while live_members(process.pid):
        if time.monotonic() >= deadline:
            raise RuntimeError('GUI process group remains after cleanup')
        time.sleep(0.1)
    if process.returncode == 70:
        raise RuntimeError('GUI supervisor could not certify cleanup')


def guard(command):
    stopping = False
    def request_stop(*_):
        nonlocal stopping
        stopping = True
    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGHUP, request_stop)
    group = os.getpgrp()
    assert group == os.getpid(), 'Supervisor must own its group'
    child = subprocess.Popen(command, stdin=subprocess.DEVNULL)
    try:
        while not stopping:
            if select.select([sys.stdin.buffer], [], [], 0.2)[0]:
                if not os.read(0, 4096):
                    stopping = True
            result = child.poll()
            # Wrapper exit is not application exit if it handed off to a child.
            if result is not None and not live_members(group, os.getpid()):
                return result if result >= 0 else 128 - result
    finally:
        os.killpg(group, signal.SIGTERM)
        deadline = time.monotonic() + 10
        while live_members(group, os.getpid()) and time.monotonic() < deadline:
            child.poll()
            time.sleep(0.1)
        deadline = time.monotonic() + 5
        while live_members(group, os.getpid()):
            for pid in live_members(group, os.getpid()):
                try:
                    if os.getpgid(pid) == group:
                        os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            child.poll()
            if time.monotonic() >= deadline:
                raise RuntimeError('GUI child group could not be stopped')
            time.sleep(0.1)
        child.wait(timeout=5)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(guard(sys.argv[1:]))
    except Exception as error:
        print('GUI supervisor:', str(error), file=sys.stderr)
        raise SystemExit(70)
