"""Shared helpers: local settings, UTC times, evidence of every command."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import threading

CASES_DIR = Path(__file__).resolve().parent.parent


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def load_env(path=None):
    """Read KEY=VALUE lines of cases/local.env (machine-specific values, not published)."""
    path = Path(path) if path else CASES_DIR / 'local.env'
    env = {}
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip()
    return env


def home_path(relative):
    """Paths of local.env are relative to the home directory of the account that runs the runner."""
    p = Path(relative)
    return p if p.is_absolute() else Path.home() / p


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


HOME_TEXT = str(Path.home())


def scrub(value):
    """Evidence is published: the home directory of the host account is written as `~` (COMMON.md)."""
    if isinstance(value, bytes):
        return value.replace(HOME_TEXT.encode(), b"~")
    if isinstance(value, str):
        return value.replace(HOME_TEXT, "~")
    if isinstance(value, list):
        return [scrub(v) for v in value]
    return value


class RunnerError(Exception):
    """A step outside the implementation failed (download, slot, the runner itself): outcome unobserved."""


class Evidence:
    """One evidence directory per case. Every command: its text, stdout, stderr, exit, UTC start and end."""

    def __init__(self, directory):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.n = 0
        self.lock = threading.Lock()
        self.log_path = self.dir / 'log.txt'
        self.jsonl = self.dir / 'commands.jsonl'

    def note(self, text):
        with self.lock:
            with open(self.log_path, 'a') as log:
                log.write(f'{utc()} NOTE {scrub(text)}\n')

    def record(self, where, command, start, end, exit_code, stdout, stderr, extra=None):
        with self.lock:
            self.n += 1
            n = self.n
        base = f'{n:04d}'
        out_name, err_name = base + '.out', base + '.err'
        stdout = scrub(stdout if isinstance(stdout, bytes) else stdout.encode())
        stderr = scrub(stderr if isinstance(stderr, bytes) else stderr.encode())
        command = scrub(command)
        (self.dir / out_name).write_bytes(stdout)
        (self.dir / err_name).write_bytes(stderr)
        entry = {'n': n, 'where': where, 'command': command, 'start': start, 'end': end,
                 'exit': exit_code, 'stdout': out_name, 'stderr': err_name}
        if extra:
            entry.update(extra)
        with self.lock:
            with open(self.jsonl, 'a') as stream:
                stream.write(json.dumps(entry, sort_keys=True) + '\n')
            with open(self.log_path, 'a') as log:
                shown = command if isinstance(command, str) else ' '.join(map(str, command))
                log.write(f'{start} [{n:04d}] {where}$ {shown}\n{end} [{n:04d}] exit={exit_code}\n')
        return n

    def host(self, argv, timeout=3600, input_bytes=None, cwd=None, env=None):
        """Run a command on the host and record it. Returns (exit, stdout bytes, stderr bytes)."""
        start = utc()
        try:
            p = subprocess.run([str(a) for a in argv], input=input_bytes, capture_output=True,
                               timeout=timeout, cwd=cwd, env=env)
            code, out, err = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            code, out, err = 124, e.stdout or b'', (e.stderr or b'') + b'\n[runner] timeout\n'
        except OSError as e:
            code, out, err = 127, b'', str(e).encode()
        self.record('H', [str(a) for a in argv], start, utc(), code, out, err)
        return code, out, err
