#!/usr/bin/env python3
"""Derive the two exact development fragments from the committed history 2."""
import hashlib, json, pathlib
root = pathlib.Path(__file__).resolve().parent
original = (root.parent/'h2/history.sh').read_text()
round_start = 'for round in 1 2 3; do\n'
phase_start = '  for phase in original edited; do\n'
phase_end = '  done\ndone\n'
cut = '    stand-build build source:h2-hello\n'
assert original.count(round_start) == original.count(phase_start) == original.count(phase_end) == original.count(cut) == 1
head, rounds = original.split(round_start)
fetch, rest = rounds.split(phase_start)
phase, tail = rest.split(phase_end)
prior, following = phase.split(cut)
prefix = head + 'round=1\nphase=original\n' + fetch + prior
# Restore only shell-local state across invocations; no repeated fetch/import/run.
suffix = '#!/bin/bash\nset -eu\nexport LC_ALL=C\nexport PYTHONDONTWRITEBYTECODE=1\ncd /home/stand/step8-h2\nround=1\nphase=original\n' + following
suffix += 'phase=edited\n' + phase
suffix += 'for round in 2 3; do\n' + rounds
outputs = {'development-prefix.sh': prefix, 'development-suffix.sh': suffix}
for name, content in outputs.items():
    (root/name).write_text(content)
(root/'development-split.json').write_text(json.dumps({
    'history2_sha256': hashlib.sha256(original.encode()).hexdigest(),
    'interrupted_command': cut.strip(),
    'prefix': 'Round 1 original: fetch, exact source specification, source admission; excludes first stand-build.',
    'suffix': 'Round 1 original: binary admission and run; round 1 edited complete; rounds 2 and 3 complete.',
    'shell_state_restored': ['LC_ALL=C', 'PYTHONDONTWRITEBYTECODE=1', 'cwd=/home/stand/step8-h2', 'round=1', 'phase=original'],
    'files': {name: hashlib.sha256(content.encode()).hexdigest() for name,content in outputs.items()},
}, indent=2)+'\n')
