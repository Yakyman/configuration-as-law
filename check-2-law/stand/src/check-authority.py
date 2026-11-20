#!/usr/bin/env python3
"""VM-only Check 5 integration harness. JSONL evidence on stdout; no hypothesis verdict."""
import hashlib
import json
import os
from pathlib import Path
import pwd
import shlex
import subprocess
import sys

ROOT = Path('/etc/cal/root.json')
CURRENT = Path('/var/lib/cal/current.json')
PERSONAL = {u: Path('/home') / u / 'declaration.json' for u in ('alice', 'bob')}
failures = []


def digest():
    return hashlib.sha256(CURRENT.read_bytes()).hexdigest() if CURRENT.exists() else None


def current():
    return json.loads(CURRENT.read_text())


def event(label, argv, expected='success', unchanged=False, predicate=None):
    before = digest()
    generations_before = sorted(p.name for p in Path('/var/lib/cal/generations').glob('*.json'))
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=180)
        rc, stdout, stderr = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as exc:
        rc, stdout, stderr = 124, str(exc.stdout or ''), str(exc.stderr or '') + '\nTIMEOUT'
    after = digest()
    checks = {'exit_matches': rc == 0 if expected == 'success' else rc != 0}
    if unchanged:
        checks['current_unchanged'] = before == after
        checks['generations_unchanged'] = generations_before == sorted(p.name for p in Path('/var/lib/cal/generations').glob('*.json'))
    if predicate:
        try:
            checks['state_assertion'] = bool(predicate())
        except Exception as exc:
            checks['state_assertion'] = False
            stderr += '\nstate assertion exception: ' + repr(exc)
    passed = all(checks.values())
    if not passed:
        failures.append(label)
    print(json.dumps(dict(event=label, command=argv, expected=expected,
                          observed='assertions passed' if passed else 'assertions failed',
                          returncode=rc, stdout=stdout, stderr=stderr,
                          before_current_sha256=before, after_current_sha256=after,
                          assertions=checks)), flush=True)
    return passed


def user(label, command, **kwargs):
    return event(label, ['runuser', '-u', 'alice', '--', '/usr/local/bin/cal-login', '-c', command], **kwargs)


def personal(label, doc, **kwargs):
    command = 'printf "%s\\n" ' + shlex.quote(json.dumps(doc)) + ' > /home/alice/declaration.json && /usr/local/bin/calctl apply'
    return user(label, command, **kwargs)


def configure(label, programs=None, policies=None):
    # Clearing personal declarations before changing constitution prevents a stale
    # personal conflict from invalidating the policy setup itself.
    personal(label + '-clear-personal', {'programs': {}})
    doc = {'archive': 'keep', 'programs': programs or {}, 'policies': policies or {},
           'allow_channels': {}, 'shared': {}}
    command = 'printf "%s\\n" ' + shlex.quote(json.dumps(doc)) + ' > /etc/cal/root.json && /usr/local/bin/calctl apply'
    if not event(label, ['/bin/bash', '-c', command]):
        raise RuntimeError('policy setup failed: ' + label)


def has_program(name, version='1'):
    item = current()['programs'].get(name, {})
    return item.get('version') == version and 'alice' in item.get('owners', [])


def main():
    if os.geteuid() != 0 or not Path('/run/cal.sock').exists():
        raise SystemExit('Run as root only inside the prepared disposable cal VM')
    saved = {}
    for path in [ROOT, *PERSONAL.values(), Path('/home/alice/downloaded')]:
        saved[path] = (path.read_bytes(), path.stat().st_uid, path.stat().st_gid, path.stat().st_mode & 0o7777) if path.exists() else None
    try:
        # Root bootstrap is evidence, not an ordinary-user success case.
        for name, path in PERSONAL.items():
            account = pwd.getpwnam(name)
            path.write_text('{"programs": {}}\n')
            os.chown(path, account.pw_uid, account.pw_gid)
            os.chmod(path, 0o600)
        ROOT.write_text(json.dumps({'archive': 'keep', 'programs': {}, 'policies': {}, 'allow_channels': {}, 'shared': {}}))
        if not event('bootstrap-empty-declarations', ['/usr/local/bin/calctl', 'apply']):
            raise RuntimeError('bootstrap failed')

        personal('no-lists-add-hello', {'programs': {'hello': {'version': '1'}}}, predicate=lambda: has_program('hello'))
        user('no-lists-run-hello', '/usr/bin/hello')
        user('no-lists-unix-files', 'set -e; printf authority > /home/alice/authority-data; test "$(cat /home/alice/authority-data)" = authority; mv /home/alice/authority-data /home/alice/authority-renamed; chmod 600 /home/alice/authority-renamed; test "$(stat -c %a /home/alice/authority-renamed)" = 600; rm /home/alice/authority-renamed')
        # Keep §9.6's Unix execution expectation; a P4 denial is NOT a pass here.
        user('no-lists-prepare-own-executable', 'set -e; cp /usr/bin/hello /home/alice/downloaded; chmod 755 /home/alice/downloaded; id; cat /proc/self/attr/current; stat -c "%a %u %g %i %s" /home/alice/downloaded; sha256sum /home/alice/downloaded')
        copied = Path('/home/alice/downloaded')
        fingerprint = (copied.read_bytes(), copied.stat().st_mode, copied.stat().st_uid, copied.stat().st_gid, copied.stat().st_ino)
        same_file = lambda: fingerprint == (copied.read_bytes(), copied.stat().st_mode, copied.stat().st_uid, copied.stat().st_gid, copied.stat().st_ino)
        user('no-lists-unix-execute-own-file', '/home/alice/downloaded', unchanged=True, predicate=same_file)
        doc = json.loads(ROOT.read_text())
        doc['allow_channels'] = {'alice': ['download']}
        ROOT.write_text(json.dumps(doc))
        event('no-lists-add-download-exception', ['/usr/local/bin/calctl', 'apply'], predicate=same_file)
        user('no-lists-same-file-with-exception', '/home/alice/downloaded', unchanged=True, predicate=same_file)
        doc['allow_channels'] = {}
        ROOT.write_text(json.dumps(doc))
        event('no-lists-revoke-download-exception', ['/usr/local/bin/calctl', 'apply'], predicate=same_file)
        bob_before = PERSONAL['bob'].read_bytes()
        user('other-user-declaration-protected', 'printf forbidden > /home/bob/declaration.json', expected='denied', unchanged=True,
             predicate=lambda: PERSONAL['bob'].read_bytes() == bob_before)
        root_before = ROOT.read_bytes()
        user('root-declaration-protected', 'printf forbidden > /etc/cal/root.json', expected='denied', unchanged=True,
             predicate=lambda: ROOT.read_bytes() == root_before)

        configure('root-hello-version-1', programs={'hello': {'version': '1', 'scope': 'system'}})
        personal('reject-root-version-conflict', {'programs': {'hello': {'version': '2'}}}, expected='denied', unchanged=True)
        personal('reject-personal-archive-override', {'programs': {}, 'archive': 'delete'}, expected='denied', unchanged=True)
        personal('reject-personal-policies-override', {'programs': {}, 'policies': {'alice': {'allowlist': ['hello']}}}, expected='denied', unchanged=True)
        personal('reject-personal-system-scope', {'programs': {'figlet': {'version': '1', 'scope': 'system'}}}, expected='denied', unchanged=True)

        configure('set-root-allowlist', policies={'alice': {'allowlist': ['hello']}})
        personal('allowlist-permits-hello', {'programs': {'hello': {'version': '1'}}}, predicate=lambda: has_program('hello'))
        user('allowlist-run-hello', '/usr/bin/hello')
        personal('allowlist-rejects-figlet', {'programs': {'figlet': {'version': '1'}}}, expected='denied', unchanged=True)

        configure('set-root-denylist', policies={'alice': {'denylist': ['hello']}})
        personal('denylist-rejects-hello', {'programs': {'hello': {'version': '1'}}}, expected='denied', unchanged=True)
        personal('denylist-permits-figlet', {'programs': {'figlet': {'version': '1'}}}, predicate=lambda: has_program('figlet'))
        user('denylist-run-figlet', '/usr/bin/figlet authority')

        event('root-manual-write-and-dac-override', ['/bin/bash', '-c', 'set -e; printf root-authority > /root/cal-authority-probe; chmod 000 /root/cal-authority-probe; test "$(cat /root/cal-authority-probe)" = root-authority; rm /root/cal-authority-probe'], unchanged=True)
        # Unconfined root may edit personal files despite list policies; application
        # of contradictory declarations remains a separate validation operation.
        event('root-manual-personal-write', ['/bin/bash', '-c', 'printf \'{"programs": {}}\\n\' > /home/alice/declaration.json'], unchanged=True,
              predicate=lambda: json.loads(PERSONAL['alice'].read_text()) == {'programs': {}})
        event('root-apply-after-manual-edit', ['/usr/local/bin/calctl', 'apply'])
        event('managed-root-worker-probe-check2', ['/usr/local/lib/cal/worker', '--probe'], expected='denied', unchanged=True,
              predicate=lambda: not Path('/usr/local/lib/cal/illegal-root-program-write').exists())
    except Exception as exc:
        failures.append('harness-exception')
        print(json.dumps({'event': 'harness-exception', 'error': repr(exc)}), flush=True)
    finally:
        for path, old in saved.items():
            if old is None:
                path.unlink(missing_ok=True)
            else:
                content, uid, gid, mode = old
                path.write_bytes(content)
                os.chown(path, uid, gid)
                os.chmod(path, mode)
        event('cleanup-restore-declarations-and-apply', ['/usr/local/bin/calctl', 'apply'])
        for name in ('authority-data', 'authority-renamed'):
            (Path('/home/alice') / name).unlink(missing_ok=True)
        Path('/root/cal-authority-probe').unlink(missing_ok=True)
        print(json.dumps({'event': 'SUMMARY', 'failures': failures, 'failure_count': len(failures),
                          'note': 'Assertion results only; no hypothesis outcome. no-lists-unix-execute-own-file tests the full Unix execution condition, not just file operations. Its failure is retained for P7 vs P1/P4 attribution; not an expected-success waiver. Saved generations retained as evidence.'}), flush=True)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
