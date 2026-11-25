#!/usr/bin/python3
"""Write casedefs_search.py and search-cases.md: the P4 cases made from the successes of the search.

Plan, Section 9.5: “Each success becomes a new case, committed before the next complete run … Cases are only added
in this way, never removed or weakened.” The successes (order of the review, 2026-11-25 00:38 UTC):

  - search/routes-0.32.tsv: every row whose group is `direct` and whose result begins with `RAN`;
  - search/attempts-0.32.tsv: rows 202, 234, 241 (row 256 is counted `RAN` by the catalogue only because its last
    command ended with status 0; its recorded output is the refusal; it is not a success and gets no case);
  - the builder's own finding: saved Basic macro libraries run (build/IMPOSSIBLE.md, the section on saved
    LibreOffice Basic profile libraries: the two `libreoffice … macro:///Standard.Module1.Main` commands; the
    library files of build/lo-macro-private-inputs.py).

Nothing is retyped: the attempt of each route case is the route's own script (search/routes/NNN-*.sh or
search/attempts/NNN-*.sh), sent as the search sent it (PHASE=try, as the account or through `sudo -n bash -c`), and
the probe is the condition of the script's own `RESULT RAN` line. The table rows are cross-checked with the evidence
files: a direct route whose evidence says `RESULT RAN` and that is missing from the selection stops the program.

usage: make-search-cases.py SEARCH_DIR BUILD_DIR OUT_DIR
"""
import hashlib
import importlib.util
import pprint
import re
import shlex
import sys
from pathlib import Path

search, build, out = (Path(a) for a in sys.argv[1:4])
HOME = '/home/person'
ATTEMPTS_TAKEN = {'202', '234', '241'}
ATTEMPTS_NOT = {'256': 'counted RAN by the catalogue only because its last command ended with status 0; its '
                       'recorded output is the refusal (nsenter: reassociate to namespaces failed: Operation not '
                       'permitted); not a success'}
# built-in tools of installation and configuration (S8.1-7) used by an attempt: S8.3-7 is evaluated both ways (Q13)
TOOLS = {'111': 'apt-get', '202': 'apt-mark', '234': 'crontab'}
inputs = {}


def read(p):
    b = p.read_bytes()
    inputs[str(p.relative_to(p.parents[1]))] = hashlib.sha256(b).hexdigest()
    return b.decode()


def rows(tsv):
    """Rows of a search table that start with a three-digit id (the tables have a few broken continuation lines of
    long reasons; they hold no row of a direct route that ran — cross-checked with the evidence below)."""
    lines = read(tsv).splitlines()
    head = lines[0].split('\t')
    for line in lines[1:]:
        if re.match(r'^\d{3}\t', line):
            f = line.split('\t')
            if len(f) == len(head):
                yield dict(zip(head, f))


def script_of(kind, rid):
    found = sorted((search / kind).glob(f'{rid}-*.sh'))
    assert len(found) == 1, (kind, rid, found)
    return found[0]


def headers(text):
    h = {}
    for line in text.splitlines():
        m = re.match(r'# (ID|NAME|PROGRAM|GROUP|AS|RESTART|COMMAND|NOTE|CHANNEL|BREAKING-CANDIDATE): ?(.*)$', line)
        if m:
            h[m.group(1)] = m.group(2)
    return h


def condition(text):
    m = re.findall(r'^if (.+); then echo "RESULT RAN"; else echo "RESULT REFUSED', text, re.M)
    assert len(m) == 1, m
    return m[0]


def tilde(p):
    return '~' + p[len(HOME):] if p.startswith(HOME) else p


PATH = re.compile(r'(?:~|/home/person|/tmp|\$D)(?:/[A-Za-z0-9._@+-]+)+')


def made_of(text, rid, cond):
    """What the route's typed commands create: its folder W (the search's harness makes it, cds into it and writes
    the command's output there) and every path its setup and command name outside W, except the marks of the
    condition (those are the payload's effect, never the person's). Type `obeyed` for all: material unless
    something obeys it or a direct route executes it (the stricter of the two types of casedefs.MADE)."""
    w = f'{HOME}/r/{rid}'
    body = text.split('if [ "$PHASE" = try ]; then', 1)[1].split('\nelse\n', 1)[0]
    var = {'D': v for v in re.findall(r'\bD=([^ ;]+);', body)}
    marks = set(PATH.findall(cond)) | {f'/tmp/mark-{rid}'}
    paths = []
    for p in PATH.findall(body):
        if p.startswith('$D'):
            if 'D' not in var:
                continue
            p = var['D'] + p[2:]
        p = p.replace('~', HOME, 1) if p.startswith('~') else p
        if p in marks or p == w or p.startswith(w + '/') or p.startswith('/tmp/mark'):
            continue
        if p not in paths:
            paths.append(p)
    for d in var.values():
        d = d.replace('~', HOME, 1) if d.startswith('~') else d
        if d not in paths:
            paths.append(d)
    made = [('obeyed', '~/r'), ('obeyed', tilde(w)), ('obeyed', tilde(w) + '/**')]
    for p in paths:
        made.append(('obeyed', tilde(p)))
    return made


cases, md, skipped = [], [], []
evidence_ran = set()
for ev in sorted((search / 'evidence' / '0.32').glob('[0-9][0-9][0-9]-*.txt')):
    if re.search(r'^RESULT RAN', ev.read_text(errors='replace'), re.M):
        evidence_ran.add(ev.name[:3])

sel = []
for r in rows(search / 'routes-0.32.tsv'):
    if r['group'] == 'direct' and r['result'].startswith('RAN'):
        sel.append(('routes', r))
for r in rows(search / 'attempts-0.32.tsv'):
    if r['result'].startswith('RAN'):
        if r['id'] in ATTEMPTS_TAKEN:
            sel.append(('attempts', r))
        else:
            skipped.append((r['id'], ATTEMPTS_NOT[r['id']]))
assert {r['id'] for _, r in sel if _ == 'attempts'} == ATTEMPTS_TAKEN
# cross-check: every route whose evidence ran is selected, or is a data route, or is the attempt left out
for rid in sorted(evidence_ran):
    kind = 'routes' if int(rid) < 200 else 'attempts'
    h = headers(script_of(kind, rid).read_text())
    if h['GROUP'] == 'direct' and rid not in ATTEMPTS_NOT:
        assert any(r['id'] == rid for _, r in sel), f'route {rid} ran by its evidence but is not selected'

for kind, r in sel:
    rid = r['id']
    sp = script_of(kind, rid)
    text = read(sp)
    h = headers(text)
    assert h['COMMAND'] == r['command'], (rid, 'the table and the script differ')
    assert h['RESTART'] == 'no', rid
    who = 'R' if h['AS'] == 'root' else 'U'
    cond = condition(text)
    steps = []
    if who == 'R':
        # search/tools/run-routes.py: “the account makes the folder of the payload” before a root route
        steps.append(('ATTEMPT', 'U', f'mkdir -p {HOME}/r/{rid} && chmod 0777 {HOME}/r {HOME}/r/{rid}'))
    steps.append(('ATTEMPT', who, 'PHASE=try\n' + text))
    steps.append(('PROBE', who, cond, 'exit0'))
    cid = f'P4-S-{rid}'
    c = dict(id=cid, part='P4', table=f'search/{kind}-0.32.tsv', row=rid, script=f'search/{kind}/{sp.name}',
             program=h['PROGRAM'], channel=h.get('CHANNEL', ''), steps=steps, made=made_of(text, rid, cond))
    if rid in TOOLS:
        c['tool'] = TOOLS[rid]
    cases.append(c)
    md.append(f'| {cid} | `{c["table"]}` row {rid}: {h["PROGRAM"]}, as {h["AS"]} | the script `{c["script"]}` with '
              f'`PHASE=try` (its command: `{h["COMMAND"].replace("|", chr(92) + "|")}`) | '
              f'`{who}: {cond.replace("|", chr(92) + "|")}` |')

# the builder's finding: saved LibreOffice Basic profile libraries
imp = read(build / 'IMPOSSIBLE.md')
sec = imp.split('## 2026-11-24: saved LibreOffice Basic profile libraries', 1)[1].split('\n## ', 1)[0]
cmds = re.findall(r'^(libreoffice -env:UserInstallation=\S+ --headless --norestore macro:///Standard\.Module1\.Main)$',
                  sec, re.M)
assert len(cmds) == 2, cmds
markers = re.findall(r'/tmp/lo-macro-[a-z]+-marker', sec)
markers = list(dict.fromkeys(markers))
assert markers == ['/tmp/lo-macro-basic-marker', '/tmp/lo-macro-shell-marker'], markers
read(build / 'lo-macro-private-inputs.py')
spec = importlib.util.spec_from_file_location('fixtures', build / 'lo-macro-private-inputs.py')
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)
for k, cmd in enumerate(cmds, 1):
    # the builder's account is `user`; the account of the test declaration is `person`
    cmd = cmd.replace('file:///home/user/', f'file://{HOME}/')
    prof = re.search(r'-env:UserInstallation=file://(\S+)', cmd).group(1)
    write = [f'mkdir -p {prof}/user/basic/Standard']
    for name, body in fx.FILES.items():
        write.append(f'printf %s {shlex.quote(body)} > {prof}/user/basic/{name}')
    cid = f'P4-S-LO-{k}'
    steps = [('L+', 'package libreoffice-writer'), ('APPLY',),
             # the builder's probe: “After native profile initialization, the probe saved …” (its own timeout too)
             ('ATTEMPT', 'U', f'timeout -k 2 120 libreoffice -env:UserInstallation=file://{prof} --headless '
                              '--terminate_after_init'),
             ('ATTEMPT', 'U', ' && '.join(write)),
             ('ATTEMPT', 'U', 'timeout -k 2 120 ' + cmd)] + [('PROBE', 'U', f'test -e {m}', 'exit0') for m in markers]
    made = [('obeyed', tilde(prof) + '/user/basic/Standard')] + \
           [('obeyed', tilde(prof) + '/user/basic/' + n) for n in fx.FILES]
    cases.append(dict(id=cid, part='P4', table='build/IMPOSSIBLE.md', row='saved LibreOffice Basic profile libraries',
                      script='build/lo-macro-private-inputs.py', program='libreoffice (saved Basic library)',
                      channel='C9', steps=steps, made=made, line_first=True))
    md.append(f'| {cid} | `build/IMPOSSIBLE.md`, saved LibreOffice Basic profile libraries, command {k} | '
              f'`L+ package libreoffice-writer`; `APPLY`; `INV {cid}-pre`; `U: libreoffice '
              f'-env:UserInstallation=file://{prof} --headless --terminate_after_init`; the three library files '
              f'of `build/lo-macro-private-inputs.py` written by `printf` into `{prof}/user/basic/`; `U: {cmd}` | '
              + '; '.join(f'`U: test -e {m}`' for m in markers) + ' |')

src = ('# Written by tools/make-search-cases.py — do not edit; run the program again.\n'
       '# Inputs (sha256):\n' + ''.join(f'#   {k}  {v}\n' for k, v in sorted(inputs.items())) +
       '# Not taken: ' + '; '.join(f'attempt {k}: {v}' for k, v in skipped) + '\n'
       'SEARCH_CASES = ' + pprint.pformat(cases, width=118, sort_dicts=False) + '\n')
(out / 'casedefs_search.py').write_text(src)
(out / 'search-cases.md').write_text('\n'.join(md) + '\n')
print(f'{len(cases)} cases: ' + ' '.join(c['id'] for c in cases))
print('not taken: ' + '; '.join(f'{k} ({v[:60]}…)' for k, v in skipped))
