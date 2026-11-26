# Fixture test record

2026-11-26 UTC. No operating-system run; no VM or installation used.

Command: `./selftest/run.sh`, executed in `confos.slice` with MemoryMax=512M and
CPUQuota=100%. The wrapper used `systemd-run --user --slice=confos.slice --wait
--pipe --collect` and the finite unit `confos-cases-fixtures`. No detached job.

Observed output from the original fixture check:

```
Ran 48 tests
OK
Ran 5 tests
OK
Ran 3 tests
OK
VALID: 86 portable case definitions
CATALOGUE PASS: 86 cases; 153 source IDs; 34 statement labels
SELFTEST PASS (fixtures only; no operating-system run)
```

56 tests cover derivation, comparison, inventory fixtures, request/response
matching, failure propagation, reporting, CLI entry points and the tiny payloads.
Small C payloads compile with `-std=c11 -Wall -Wextra -Werror`; harmless reader and
value modes run, and the staged recipe builds version 2 with a wget-shaped fetcher.
No network fetch, persistent-script execution or policy probe occurs on the host.
Temporary outputs are deleted by their fixture contexts.

Sensitivity checks include a planted unrecorded object; changed named values;
missing files/fields; failed or absent observations; same-path/different-byte
processes; recorded executable across namespaces; port attribution; direct vs
data input; opening boundaries and symlink escape; shared ownership; external
account provenance; kernel parameters, modules and both radio settings. Relational
queries cannot be satisfied by adapter-supplied True without operands. A payload
update cannot stand in for a system update. Reports label fixtures and preserve
every fail/unobserved row as request evidence.

During construction two comparison tests initially shared mutable dictionaries
between expected and observed fixture state. Their mutations changed both sides;
the fixtures were corrected to deep-copy observations. The catalogue check also
initially included TABLE.md's E1–E3 evidence-set labels as statements; it now
checks exactly the 34 statement rows. These were checker-development defects,
not observations of an operating system.

Independent review/acceptance is still pending. These tests verify the checking
programs on controlled evidence, not the new system, optional facilities,
real-hardware actions, native adapter bindings or a hypothesis verdict.

## Standalone publication check

2026-11-26 UTC. The revised set includes STATEMENT-LABELS.json, with the 34
statement labels and source checksum from records-confos/TABLE.md. The checker
reads that snapshot. README.md describes the public repository layout and the
remaining native bindings. Working correspondence is excluded. Fixture home paths use the example account
/home/user; published files contain no work-coordination role or message-file
references beyond the permitted builder, case party, search and review roles.

After `python3 -B tools/freeze.py`, the following command copied exactly the
files in PUBLICATION.txt into an empty temporary directory, verified checksums,
ran the self-test there, and deleted the directory. It ran within the inherited
confos.slice. No files from the historical stand were copied or read by the
self-test. Run this from the root of the set:

```sh
python3 -B - <<'PY'
from pathlib import Path
import shutil, subprocess, tempfile
root = Path.cwd()
names = (root / 'PUBLICATION.txt').read_text().splitlines()
with tempfile.TemporaryDirectory(prefix='publication-check-', dir=root) as tmp:
    dest = Path(tmp)
    for name in names:
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / name, target)
    assert sorted(str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file()) == sorted(names)
    sums = subprocess.run(['sha256sum', '-c', 'SHA256SUMS'], cwd=dest, capture_output=True, text=True)
    assert sums.returncode == 0, sums.stdout + sums.stderr
    print(f'PUBLICATION COPY: {len(names)} files; checksums PASS')
    test = subprocess.run(['./selftest/run.sh'], cwd=dest, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (root / 'selftest/LAST.txt').write_text(test.stdout)
    print(test.stdout, end='')
    assert test.returncode == 0, test.returncode
assert not dest.exists()
print('PUBLICATION SELFTEST PASS; temporary copy deleted')
PY
```

Observed output (individual test names and durations omitted):

```text
PUBLICATION COPY: 58 files; checksums PASS
Ran 48 tests
OK
Ran 5 tests
OK
Ran 3 tests
OK
VALID: 86 portable case definitions
CATALOGUE PASS: 86 cases; 153 source IDs; 34 statement labels
SELFTEST PASS (fixtures only; no operating-system run)
PUBLICATION SELFTEST PASS; temporary copy deleted
```

Exit status: 0. The 58 files comprise 56 hashed inputs plus SHA256SUMS and
PUBLICATION.txt. The manifest and checksum list do not hash themselves.
