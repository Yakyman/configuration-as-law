# Complete run 3

Written by the case party. Times in UTC.

## Departures from the plan, stated before the results

1. **One pinned component of release 0.55 is not the latest at the time of the commit of the inputs**
   (2026-11-25 04:59:45 UTC): `libzstd1` is pinned at 1.5.7+dfsg-1; the archive has 1.5.7+dfsg-1+deb13u1 — the
   same departure as in run 2. The kernel (`linux-image-amd64` 6.12.118-1) is the same as the archive.
   What the lock check read, and when (`python3 -I tools/lock-check.py` on the 0.55 source, lock
   `components/20261123T000000Z.txt`):
   - At the time of the commit of the inputs of this run (`--at 20261125T045945Z`) the newest states are debian
     `20261125T023159Z` and debian-security `20261125T043418Z`; at the time of the commit of the sixth freeze
     (`--at 20261125T040254Z`) debian `20261125T023159Z` and debian-security `20261125T035622Z`. Both read at
     06:31 UTC, every index fetched with status 200 and checked against its Release file: of 113 components 108 are
     the same as the archive, 4 are the implementation's own (`absent`), 1 is newer in the archive (`libzstd1`)
     (`ready/f11/lock-check-0.55-at-20261125T045945Z-retry-20261125T063129Z.tsv`, `.reads.jsonl`; the same for
     `…T040254Z…`).
   - Before 06:31 UTC these two security states could not be read: snapshot.debian.org listed them, but their
     `dists/trixie-security/InRelease` answered 404 (04:06–04:10 UTC and 05:02 UTC; `curl -sL` →
     `…/file/3b34d02d…/InRelease` and `…/file/84efe1e0…/InRelease` 404, while the state `20261125T022259Z` answered
     200). On those reads the tool counted the security index as empty without saying so and printed
     `linux-image-amd64` as `older`; that was the tool's defect, not a finding (`QUESTIONS.md`, Q15). The readable
     result of 04:07 UTC (`--at 20261125T034456Z`, security `20261125T022259Z`,
     `ready/f9/lock-check-0.55-readable.tsv`) is the same as the one above.
2. **The commit of the sixth freeze (2026-11-25 04:02:54 UTC, `98a32e74…`) was followed by no complete run.** Before
   the run, the development run `dev-18` of P4-S-135, P4-S-136 and P4-S-167 on 0.55 from the sixth freeze
   (04:06–04:14 UTC) had all nine rows `fail` by one object: the process of the recorded mpv, which the frozen
   `inventory` knew only by the path `/app/bin/mpv` of the application's own mount namespace and which the frozen
   `compare` therefore counted as past the declaration. That was a path the case party's programs could not place,
   not the implementation's defect. The party that directed the work ordered the repair (order 7, 04:21 UTC): `CORRECTIONS.md` [f7] — a
   process is placed by the checksum of the file it executes; the seventh freeze (`run/src16`), committed with
   release 0.55 unchanged as `39533ee3…` at 04:59:45 UTC. This run is from the seventh freeze.

## Checks before the run

- Specificity test of the seventh freeze on 0.55: `SPECIFICITY TEST PASS` 20 of 20 (04:42:22–04:55:45 UTC, run
  `spec-20261125T044222Z`, `ready/f10/specificity-0.55.txt`).
- `dev-18-f7b`: P4-S-135, P4-S-136, P4-S-167 on 0.55 from `run/src16` (04:42–04:51 UTC, `../runs/dev-18-f7b`): no row
  `fail` or `unobserved` (P4 and P1 of 135 and 136 `pass`; 167 `undecided` by Q12; UND `undecided`).
- The other tests of the seventh freeze (`READY.md`, S7.2): planted-object test of `inventory` `RESULT: PASS`
  (04:42:37–04:48:28 UTC), runner self-test `SELFTEST PASS` (04:42:27–04:47:05 UTC), the compare fixtures `RESULT:
  PASS` (04:41 UTC).

## What the development run `dev-17-full` showed on release 0.54 (not an observation of the check)

From the sixth freeze, 02:31–04:05 UTC, stopped at the order of run 3 (`../runs/dev-17-full`, 137 rows,
`../runs/dev-17-full-rest`, 54 rows): OW-1 to OW-9 `pass` (OW-2, OW-3, OW-8 of run 2 repaired), OW-10 and OW-11
`unobserved` (real hardware), every other row `pass` or `undecided` except the nine rows of P4-S-135, 136 and 167
(`fail` by the mpv process, the defect of the case party's programs repaired in [f7]) and nine rows `unobserved` only
because the stop interrupted P2-REM-3, P2-NET-1 and P4-C2-2.

## The run

- Inputs: commit `39533ee3b74d845f5ff434688d0fbc4c37ff9fe9` of the repository of records, 2026-11-25 04:59:45 UTC
  (folders `confos/`, release 0.55, and `confos-check/`, the seventh freeze of the programs).
- Release 0.55 source archive SHA256 `eb901118dc725dfbadfc46ee56069f4fa631903fdb08eec25bf763f6a12acdd1`, checked on the
  server by the run's script before the run.
- Programs: the seventh freeze (`run/src16`); `sha256sum -c src16.sha256` by the run's script before the run: every
  file OK; no program changed while the run was going.
- Command: `run --source confos-0.55-source.tar.gz --name run-3 --max-vms 5` (every case of `CASES.md` of the
  seventh freeze, 124 IDs, nothing skipped), with `CASES_SLOT_WAIT=14400`.
- Time: 2026-11-25 05:01:28 – 07:14:31 UTC (exit 0); at most 5 machines at once (slots 1–5; the sixth was free for
  the search); every machine of the run stopped and its work folder removed at the end (07:14:35 UTC: no
  `qemu-system` process on the server, `run/work/run-3` gone).
- Results: `runs/run-3/results.tsv` on the server (458 rows); every evidence path below is relative to `runs/run-3/`.
  `runs/run-3` stays on the server until the review has read it.
- The list for the builder (case ID, command, output of every row that did not pass): `REQUESTS.md`, entry 19.

## Rows by part and outcome

| part | pass | fail | unobserved | undecided | all |
|---|---|---|---|---|---|
| OW | 9 | 0 | 2 | 0 | 11 |
| P1 | 128 | 0 | 0 | 24 | 152 |
| P2 | 43 | 0 | 0 | 0 | 43 |
| P4 | 24 | 0 | 0 | 67 | 91 |
| REM | 5 | 0 | 0 | 0 | 5 |
| REPRO | 2 | 0 | 1 | 0 | 3 |
| UND | 1 | 0 | 0 | 152 | 153 |
| all | 212 | 0 | 3 | 243 | 458 |

## Rows that are not `pass` because of a program of the case party

None. The defect that stopped run 3 on the sixth freeze is repaired in the seventh (`CORRECTIONS.md`, [f7]), and its
rows here are: `P4-S-135` and `P4-S-136` `pass` with their `P1:` rows `pass`; `P4-S-167` and its `P1:` row
`undecided` by Q12 only (`mpv.conf`, an object that only an interpreter its form does not name accepts); the process
of the recorded mpv is placed by the checksum of the file it executes in each of them.

## Rows that are not `pass` because of the plan or the implementation

- No row is `fail`. OW-1 to OW-9 `pass` (OW-2, OW-3 and OW-8, `fail` in run 2, are repaired in the implementation).
- `OW-10`, `OW-11` `unobserved`: not performed in this run: real hardware (plan, Section 9.3; the rules of the work, item 6).
- `REPRO-2b` `unobserved`: the case asks for account lines without the numeric identifiers; the implementation's
  `account` kind requires them (`build/DECLARATION.md`), so the case is “not expressible” (`CASES.md`, REPRO-2b).
- 67 P4 rows `undecided`. 36 depend on S8.3-7 only: a built-in tool refused, and nothing of the attempt is in force
  (reading A met, reading B not; R3 of the review). 10 are `undecided` by Q3: a declaration file changed although the
  runner did not write it — the built-in tool recorded the request in the declaration (`build/CHOICES.md`; how the
  plan counts a line written by a tool of the implementation is applied by the review, the rules of the work, item 1); P4-BT-5
  also carries Q6. The change of each, the declaration read from the disk after the attempt against `D-test` (`diff`
  of `D-test/declaration.conf` and `CASE/decl-CASE/state-declaration.conf`, both sorted): P4-C1-2 adds `package hello
  2.10-5`; P4-C1-4 removes `package ed 1.21.1-1`; P4-C2-3 adds `pip pyjokes 0.8.3 …`; P4-C3-4 adds `npm semver 7.6.3
  …`; P4-BT-1 adds `account p4user 1001 1001 - /bin/bash /home/p4user`; P4-BT-4 adds `group p4group 1001`; P4-BT-5
  adds `file /etc/sudoers.d/confos-local 0440 0:0 …`; P4-BT-9 changes `setting hostname confos-test` to `setting
  hostname p4host`; P4-BT-12 adds `setting module:dummy loaded`; P4-BT-13 adds `setting sysctl:net.ipv4.ip_forward
  1`. (P4-BT-4 and P4-BT-12 are new in this list since run 2: `groupadd` and `modprobe` record from release 0.50.)
  21 depend on Q11 or Q12 (an object that only a data route, or only an interpreter its form does not name,
  executes): Q12 only 12, Q11 only 6, both 3.
- The cases of the search (P4-S, new in the sixth freeze, 19 cases): `P4-S-089`, `P4-S-090`, `P4-S-107`,
  `P4-S-108`, `P4-S-135`, `P4-S-136` `pass`; the other 13 `undecided` (S8.3-7: 111, 202, 234; Q11: 160, 161, 166;
  Q12: 056, 167, 241, LO-1, LO-2; Q11 and Q12: 054, 162). Their `P1:` and `UND:` rows: 11 `pass`, 31 `undecided`.
- 24 P1 rows `undecided`, all by `QUESTION` objects (Q11, Q12) or `BOTHWAYS` (Q2), listed with their kind and path.
- 152 UND rows `undecided`: met against the reference installation and not under the derivation from the
  declaration alone (D1, D3–D6); 24 of them, whose reading against the reference installation is itself undecided by
  `QUESTION` objects, list them.

## Every row that is not `pass`

Form: row, part, outcome, the questions its outcome text names, one sentence, the evidence file. Under each P1 or
UND row that is `undecided` because of `QUESTION` objects: each object with its kind from the routes of its
comparison (`data-only`: only a data route executed it, Q11; `any-only`: only an interpreter that its form does
not name accepted it, Q12), its path and the comparison table.

- `UND:OW-1-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-1/UND:OW-1-apply-1.outcome.txt`
- `UND:OW-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-1/UND:OW-1.outcome.txt`
- `UND:OW-2-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-2/UND:OW-2-apply-1.outcome.txt`
- `UND:OW-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-2/UND:OW-2.outcome.txt`
- `UND:OW-2-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-2/UND:OW-2-apply-2.outcome.txt`
- `UND:OW-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-2/UND:OW-3.outcome.txt`
- `UND:OW-4-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-4/UND:OW-4-apply-1.outcome.txt`
- `P1:OW-4` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 193, 'QUESTION': 2}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `OW-4/P1:OW-4.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/023twfoe.default/times.json (`OW-4/inv-OW-4/compare-p1.tsv`)
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/mcav45g4.default-esr/times.json (`OW-4/inv-OW-4/compare-p1.tsv`)
- `UND:OW-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 2}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `OW-4/UND:OW-4.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/023twfoe.default/times.json (`OW-4/inv-OW-4/compare-und-reference.tsv`)
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/mcav45g4.default-esr/times.json (`OW-4/inv-OW-4/compare-und-reference.tsv`)
- `UND:OW-5-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-5/UND:OW-5-apply-1.outcome.txt`
- `UND:OW-5` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-5/UND:OW-5.outcome.txt`
- `P1:OW-6` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `OW-6/P1:OW-6.outcome.txt`
  - QUESTION `any-only` file /state/home/person/h (`OW-6/inv-OW-6/compare-p1.tsv`)
- `UND:OW-6` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `OW-6/UND:OW-6.outcome.txt`
  - QUESTION `any-only` file /state/home/person/h (`OW-6/inv-OW-6/compare-und-reference.tsv`)
- `UND:OW-7-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-7/UND:OW-7-apply-1.outcome.txt`
- `UND:OW-7-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-7/UND:OW-7-apply-2.outcome.txt`
- `UND:OW-7-apply-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-7/UND:OW-7-apply-3.outcome.txt`
- `UND:OW-7-apply-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-7/UND:OW-7-apply-4.outcome.txt`
- `UND:OW-7-apply-5` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-7/UND:OW-7-apply-5.outcome.txt`
- `UND:OW-7-apply-6` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-7/UND:OW-7-apply-6.outcome.txt`
- `UND:OW-7` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-7/UND:OW-7.outcome.txt`
- `UND:OW-8-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-8/UND:OW-8-apply-1.outcome.txt`
- `UND:OW-8-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-8/UND:OW-8-apply-2.outcome.txt`
- `P1:OW-8` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 187, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `OW-8/P1:OW-8.outcome.txt`
  - QUESTION `data-only` file /state/home/person/game-direct/linuxgsm.sh (`OW-8/inv-OW-8/compare-p1.tsv`)
- `UND:OW-8` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `OW-8/UND:OW-8.outcome.txt`
  - QUESTION `data-only` file /state/home/person/game-direct/linuxgsm.sh (`OW-8/inv-OW-8/compare-und-reference.tsv`)
- `UND:OW-9-a` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-9/UND:OW-9-a.outcome.txt`
- `UND:OW-9-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-9/UND:OW-9-apply-2.outcome.txt`
- `UND:OW-9` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-9/UND:OW-9.outcome.txt`
- `OW-10` (OW) **unobserved** [-]: not performed in this run: real hardware — `OW-10/OW-10.outcome.txt`
- `OW-11` (OW) **unobserved** [-]: not performed in this run: real hardware — `OW-11/OW-11.outcome.txt`
- `UND:P1-0` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P1-0/UND:P1-0.outcome.txt`
- `UND:P2-ADD-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P2-ADD-1/UND:P2-ADD-1.outcome.txt`
- `UND:P2-ADD-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P2-ADD-2/UND:P2-ADD-2.outcome.txt`
- `UND:P2-ADD-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P2-ADD-3/UND:P2-ADD-3.outcome.txt`
- `UND:P2-CHG-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P2-CHG-1/UND:P2-CHG-1.outcome.txt`
- `UND:P2-CHG-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P2-CHG-2/UND:P2-CHG-2.outcome.txt`
- `UND:P2-CHG-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P2-CHG-3/UND:P2-CHG-3.outcome.txt`
- `UND:P2-REM-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P2-REM-1/UND:P2-REM-1.outcome.txt`
- `UND:P2-REM-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P2-REM-2/UND:P2-REM-2.outcome.txt`
- `UND:P2-REM-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P2-REM-3/UND:P2-REM-3.outcome.txt`
- `UND:P2-NET-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P2-NET-1/UND:P2-NET-1.outcome.txt`
- `P4-C1-1` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (apt-get) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C1-1/P4-C1-1.outcome.txt`
- `UND:P4-C1-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-1/UND:P4-C1-1.outcome.txt`
- `P4-C1-2` (P4) **undecided** [Q3]: a declaration file changed although the runner did not write it (QUESTIONS.md Q3) — `P4-C1-2/P4-C1-2.outcome.txt`
- `UND:P4-C1-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-2/UND:P4-C1-2.outcome.txt`
- `P4-C1-3` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (dpkg) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C1-3/P4-C1-3.outcome.txt`
- `UND:P4-C1-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-3/UND:P4-C1-3.outcome.txt`
- `P4-C1-4` (P4) **undecided** [Q3]: a declaration file changed although the runner did not write it (QUESTIONS.md Q3) — `P4-C1-4/P4-C1-4.outcome.txt`
- `UND:P4-C1-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-4/UND:P4-C1-4.outcome.txt`
- `P4-C1-5` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (dpkg) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C1-5/P4-C1-5.outcome.txt`
- `UND:P4-C1-5` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-5/UND:P4-C1-5.outcome.txt`
- `P4-C1-6` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (dpkg-deb) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C1-6/P4-C1-6.outcome.txt`
- `UND:P4-C1-6` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-6/UND:P4-C1-6.outcome.txt`
- `P4-C2-1` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (pip) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C2-1/P4-C2-1.outcome.txt`
- `UND:P4-C2-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C2-1/UND:P4-C2-1.outcome.txt`
- `P4-C2-2` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (venv, pip) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C2-2/P4-C2-2.outcome.txt`
- `UND:P4-C2-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C2-2/UND:P4-C2-2.outcome.txt`
- `P4-C2-3` (P4) **undecided** [Q3]: a declaration file changed although the runner did not write it (QUESTIONS.md Q3) — `P4-C2-3/P4-C2-3.outcome.txt`
- `UND:P4-C2-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C2-3/UND:P4-C2-3.outcome.txt`
- `P4-C2-4` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (pip) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C2-4/P4-C2-4.outcome.txt`
- `UND:P4-C2-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C2-4/UND:P4-C2-4.outcome.txt`
- `P4-C3-1` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (npm) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C3-1/P4-C3-1.outcome.txt`
- `UND:P4-C3-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C3-1/UND:P4-C3-1.outcome.txt`
- `P4-C3-2` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (npm) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C3-2/P4-C3-2.outcome.txt`
- `UND:P4-C3-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C3-2/UND:P4-C3-2.outcome.txt`
- `P4-C3-3` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (npx) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C3-3/P4-C3-3.outcome.txt`
- `UND:P4-C3-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C3-3/UND:P4-C3-3.outcome.txt`
- `P4-C3-4` (P4) **undecided** [Q3]: a declaration file changed although the runner did not write it (QUESTIONS.md Q3) | not counted (no change): `R: semver 1.2.3` held before the attempt too — `P4-C3-4/P4-C3-4.outcome.txt`
- `UND:P4-C3-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C3-4/UND:P4-C3-4.outcome.txt`
- `P4-C4-1` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (flatpak) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C4-1/P4-C4-1.outcome.txt`
- `UND:P4-C4-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C4-1/UND:P4-C4-1.outcome.txt`
- `P4-C4-2` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (flatpak) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C4-2/P4-C4-2.outcome.txt`
- `UND:P4-C4-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C4-2/UND:P4-C4-2.outcome.txt`
- `P4-C4-3` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (flatpak) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C4-3/P4-C4-3.outcome.txt`
- `UND:P4-C4-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C4-3/UND:P4-C4-3.outcome.txt`
- `UND:P4-C5-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C5-1/UND:P4-C5-1.outcome.txt`
- `UND:P4-C5-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C5-2/UND:P4-C5-2.outcome.txt`
- `UND:P4-C6-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C6-1/UND:P4-C6-1.outcome.txt`
- `UND:P4-C6-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C6-2/UND:P4-C6-2.outcome.txt`
- `UND:P4-C6-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C6-3/UND:P4-C6-3.outcome.txt`
- `UND:P4-C6-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C6-4/UND:P4-C6-4.outcome.txt`
- `UND:P4-C6-5` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C6-5/UND:P4-C6-5.outcome.txt`
- `UND:P4-C6-6` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C6-6/UND:P4-C6-6.outcome.txt`
- `UND:P4-C7-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C7-1/UND:P4-C7-1.outcome.txt`
- `UND:P4-C7-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C7-2/UND:P4-C7-2.outcome.txt`
- `UND:P4-C7-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C7-3/UND:P4-C7-3.outcome.txt`
- `P4-C8-1` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 6 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-C8-1/P4-C8-1.outcome.txt`
- `P1:P4-C8-1` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-C8-1/P1:P4-C8-1.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/p4.service (`P4-C8-1/inv-P4-C8-1/compare-p1.tsv`)
- `UND:P4-C8-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-C8-1/UND:P4-C8-1.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/p4.service (`P4-C8-1/inv-P4-C8-1/compare-und-reference.tsv`)
- `P4-C8-2` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (systemd-run --user) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C8-2/P4-C8-2.outcome.txt`
- `UND:P4-C8-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C8-2/UND:P4-C8-2.outcome.txt`
- `P4-C8-3` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (systemd-run --user) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C8-3/P4-C8-3.outcome.txt`
- `UND:P4-C8-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C8-3/UND:P4-C8-3.outcome.txt`
- `P4-C8-4` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (crontab) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C8-4/P4-C8-4.outcome.txt`
- `UND:P4-C8-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C8-4/UND:P4-C8-4.outcome.txt`
- `P4-C8-5` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (crontab) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C8-5/P4-C8-5.outcome.txt`
- `UND:P4-C8-5` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C8-5/UND:P4-C8-5.outcome.txt`
- `P4-C8-6` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (systemctl) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C8-6/P4-C8-6.outcome.txt`
- `UND:P4-C8-6` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C8-6/UND:P4-C8-6.outcome.txt`
- `P4-C8-7` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (systemctl) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C8-7/P4-C8-7.outcome.txt`
- `UND:P4-C8-7` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C8-7/UND:P4-C8-7.outcome.txt`
- `P4-C8-8` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (loginctl) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C8-8/P4-C8-8.outcome.txt`
- `UND:P4-C8-8` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C8-8/UND:P4-C8-8.outcome.txt`
- `P4-C8-9` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (at) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies; note: if `at` is not present the attempt cannot run — `P4-C8-9/P4-C8-9.outcome.txt`
- `UND:P4-C8-9` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C8-9/UND:P4-C8-9.outcome.txt`
- `P4-C9-1` (P4) **undecided** [Q11]: met under one reading only: Q11: an object that only a data route executes | 3 object(s) of attempt-effect.tsv concern these questions | 3 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 3 count against (attempt-effect.tsv) — `P4-C9-1/P4-C9-1.outcome.txt`
- `P1:P4-C9-1` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 3}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-C9-1/P1:P4-C9-1.outcome.txt`
  - QUESTION `data-only` file /state/home/person/f.sh (`P4-C9-1/inv-P4-C9-1/compare-p1.tsv`)
  - QUESTION `data-only` vfile /dev/shm/f.sh (`P4-C9-1/inv-P4-C9-1/compare-p1.tsv`)
  - QUESTION `data-only` vfile /tmp/f.sh (`P4-C9-1/inv-P4-C9-1/compare-p1.tsv`)
- `UND:P4-C9-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 3}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-C9-1/UND:P4-C9-1.outcome.txt`
  - QUESTION `data-only` file /state/home/person/f.sh (`P4-C9-1/inv-P4-C9-1/compare-und-reference.tsv`)
  - QUESTION `data-only` vfile /dev/shm/f.sh (`P4-C9-1/inv-P4-C9-1/compare-und-reference.tsv`)
  - QUESTION `data-only` vfile /tmp/f.sh (`P4-C9-1/inv-P4-C9-1/compare-und-reference.tsv`)
- `P4-C9-2` (P4) **undecided** [Q11]: met under one reading only: Q11: an object that only a data route executes | 3 object(s) of attempt-effect.tsv concern these questions | 3 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 3 count against (attempt-effect.tsv) — `P4-C9-2/P4-C9-2.outcome.txt`
- `P1:P4-C9-2` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 3}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-C9-2/P1:P4-C9-2.outcome.txt`
  - QUESTION `data-only` file /state/home/person/f.py (`P4-C9-2/inv-P4-C9-2/compare-p1.tsv`)
  - QUESTION `data-only` vfile /dev/shm/f.py (`P4-C9-2/inv-P4-C9-2/compare-p1.tsv`)
  - QUESTION `data-only` vfile /tmp/f.py (`P4-C9-2/inv-P4-C9-2/compare-p1.tsv`)
- `UND:P4-C9-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 3}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-C9-2/UND:P4-C9-2.outcome.txt`
  - QUESTION `data-only` file /state/home/person/f.py (`P4-C9-2/inv-P4-C9-2/compare-und-reference.tsv`)
  - QUESTION `data-only` vfile /dev/shm/f.py (`P4-C9-2/inv-P4-C9-2/compare-und-reference.tsv`)
  - QUESTION `data-only` vfile /tmp/f.py (`P4-C9-2/inv-P4-C9-2/compare-und-reference.tsv`)
- `P4-C9-3` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 3 object(s) of attempt-effect.tsv concern these questions | 3 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 3 count against (attempt-effect.tsv) — `P4-C9-3/P4-C9-3.outcome.txt`
- `P1:P4-C9-3` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 3}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-C9-3/P1:P4-C9-3.outcome.txt`
  - QUESTION `any-only` file /state/home/person/f.pl (`P4-C9-3/inv-P4-C9-3/compare-p1.tsv`)
  - QUESTION `any-only` vfile /dev/shm/f.pl (`P4-C9-3/inv-P4-C9-3/compare-p1.tsv`)
  - QUESTION `any-only` vfile /tmp/f.pl (`P4-C9-3/inv-P4-C9-3/compare-p1.tsv`)
- `UND:P4-C9-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 3}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-C9-3/UND:P4-C9-3.outcome.txt`
  - QUESTION `any-only` file /state/home/person/f.pl (`P4-C9-3/inv-P4-C9-3/compare-und-reference.tsv`)
  - QUESTION `any-only` vfile /dev/shm/f.pl (`P4-C9-3/inv-P4-C9-3/compare-und-reference.tsv`)
  - QUESTION `any-only` vfile /tmp/f.pl (`P4-C9-3/inv-P4-C9-3/compare-und-reference.tsv`)
- `P4-C9-4` (P4) **undecided** [Q11]: met under one reading only: Q11: an object that only a data route executes | 1 object(s) of attempt-effect.tsv concern these questions | 1 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-C9-4/P4-C9-4.outcome.txt`
- `P1:P4-C9-4` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-C9-4/P1:P4-C9-4.outcome.txt`
  - QUESTION `data-only` file /state/home/person/s.sh (`P4-C9-4/inv-P4-C9-4/compare-p1.tsv`)
- `UND:P4-C9-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-C9-4/UND:P4-C9-4.outcome.txt`
  - QUESTION `data-only` file /state/home/person/s.sh (`P4-C9-4/inv-P4-C9-4/compare-und-reference.tsv`)
- `UND:P4-C9-5` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C9-5/UND:P4-C9-5.outcome.txt`
- `UND:P4-C10-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C10-1/UND:P4-C10-1.outcome.txt`
- `UND:P4-C10-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C10-2/UND:P4-C10-2.outcome.txt`
- `UND:P4-C10-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C10-3/UND:P4-C10-3.outcome.txt`
- `P4-C10-4` (P4) **undecided** [Q11, Q12]: met under one reading only: Q11: an object that only a data route executes; Q12: an object that only an interpreter its form does not name accepts | 16 object(s) of attempt-effect.tsv concern these questions | 29 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 16 count against (attempt-effect.tsv) — `P4-C10-4/P4-C10-4.outcome.txt`
- `P1:P4-C10-4` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 16}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-C10-4/P1:P4-C10-4.outcome.txt`
  - QUESTION `any-only` file /state/home/person/r/.git/HEAD (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `any-only` file /state/home/person/r/.git/config (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/applypatch-msg.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/commit-msg.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/post-update.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-applypatch.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-commit.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-merge-commit.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-push.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-rebase.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-receive.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/prepare-commit-msg.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/push-to-checkout.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/sendemail-validate.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/update.sample (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
  - QUESTION `any-only` file /state/home/person/r/.git/info/exclude (`P4-C10-4/inv-P4-C10-4/compare-p1.tsv`)
- `UND:P4-C10-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 16}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-C10-4/UND:P4-C10-4.outcome.txt`
  - QUESTION `any-only` file /state/home/person/r/.git/HEAD (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `any-only` file /state/home/person/r/.git/config (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/applypatch-msg.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/commit-msg.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/post-update.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-applypatch.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-commit.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-merge-commit.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-push.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-rebase.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/pre-receive.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/prepare-commit-msg.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/push-to-checkout.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/sendemail-validate.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/.git/hooks/update.sample (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
  - QUESTION `any-only` file /state/home/person/r/.git/info/exclude (`P4-C10-4/inv-P4-C10-4/compare-und-reference.tsv`)
- `UND:P4-C10-5` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C10-5/UND:P4-C10-5.outcome.txt`
- `UND:P4-C10-6` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C10-6/UND:P4-C10-6.outcome.txt`
- `P4-C10-7` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 2 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-C10-7/P4-C10-7.outcome.txt`
- `P1:P4-C10-7` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-C10-7/P1:P4-C10-7.outcome.txt`
  - QUESTION `any-only` file /state/home/person/k (`P4-C10-7/inv-P4-C10-7/compare-p1.tsv`)
- `UND:P4-C10-7` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-C10-7/UND:P4-C10-7.outcome.txt`
  - QUESTION `any-only` file /state/home/person/k (`P4-C10-7/inv-P4-C10-7/compare-und-reference.tsv`)
- `P4-C11-1` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (podman) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C11-1/P4-C11-1.outcome.txt`
- `UND:P4-C11-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C11-1/UND:P4-C11-1.outcome.txt`
- `P4-C11-2` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (podman) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C11-2/P4-C11-2.outcome.txt`
- `UND:P4-C11-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C11-2/UND:P4-C11-2.outcome.txt`
- `P4-C11-3` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (podman) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C11-3/P4-C11-3.outcome.txt`
- `UND:P4-C11-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C11-3/UND:P4-C11-3.outcome.txt`
- `P4-C11-4` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 4 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-C11-4/P4-C11-4.outcome.txt`
- `P1:P4-C11-4` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-C11-4/P1:P4-C11-4.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/containers/systemd/p4q.container (`P4-C11-4/inv-P4-C11-4/compare-p1.tsv`)
- `UND:P4-C11-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-C11-4/UND:P4-C11-4.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/containers/systemd/p4q.container (`P4-C11-4/inv-P4-C11-4/compare-und-reference.tsv`)
- `P4-BT-1` (P4) **undecided** [Q3]: a declaration file changed although the runner did not write it (QUESTIONS.md Q3) — `P4-BT-1/P4-BT-1.outcome.txt`
- `UND:P4-BT-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-1/UND:P4-BT-1.outcome.txt`
- `P4-BT-2` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (usermod) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-2/P4-BT-2.outcome.txt`
- `UND:P4-BT-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-2/UND:P4-BT-2.outcome.txt`
- `P4-BT-3` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (chpasswd) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-3/P4-BT-3.outcome.txt`
- `UND:P4-BT-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-3/UND:P4-BT-3.outcome.txt`
- `P4-BT-4` (P4) **undecided** [Q3]: a declaration file changed although the runner did not write it (QUESTIONS.md Q3) — `P4-BT-4/P4-BT-4.outcome.txt`
- `UND:P4-BT-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-4/UND:P4-BT-4.outcome.txt`
- `P4-BT-5` (P4) **undecided** [Q3, Q6, S8.1-8]: a declaration file changed although the runner did not write it (QUESTIONS.md Q3) | not counted (no change): `R: sudo -l -U person` held before the attempt too | note: breaking-candidate (QUESTIONS.md Q6): `install` into /etc/sudoers.d is file copying (S8.1-8) — `P4-BT-5/P4-BT-5.outcome.txt`
- `UND:P4-BT-5` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-5/UND:P4-BT-5.outcome.txt`
- `P4-BT-6` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (nft) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-6/P4-BT-6.outcome.txt`
- `UND:P4-BT-6` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-6/UND:P4-BT-6.outcome.txt`
- `P4-BT-7` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (ip) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-7/P4-BT-7.outcome.txt`
- `UND:P4-BT-7` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-7/UND:P4-BT-7.outcome.txt`
- `P4-BT-8` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (nmcli) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies; note: without NetworkManager the attempt cannot run; the outcome is then decided by the probe and CMP — `P4-BT-8/P4-BT-8.outcome.txt`
- `UND:P4-BT-8` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-8/UND:P4-BT-8.outcome.txt`
- `P4-BT-9` (P4) **undecided** [Q3]: a declaration file changed although the runner did not write it (QUESTIONS.md Q3) — `P4-BT-9/P4-BT-9.outcome.txt`
- `UND:P4-BT-9` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-9/UND:P4-BT-9.outcome.txt`
- `P4-BT-10` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (timedatectl) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-10/P4-BT-10.outcome.txt`
- `UND:P4-BT-10` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-10/UND:P4-BT-10.outcome.txt`
- `P4-BT-11` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (localectl) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-11/P4-BT-11.outcome.txt`
- `UND:P4-BT-11` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-11/UND:P4-BT-11.outcome.txt`
- `P4-BT-12` (P4) **undecided** [Q3]: a declaration file changed although the runner did not write it (QUESTIONS.md Q3) — `P4-BT-12/P4-BT-12.outcome.txt`
- `UND:P4-BT-12` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-12/UND:P4-BT-12.outcome.txt`
- `P4-BT-13` (P4) **undecided** [Q3]: a declaration file changed although the runner did not write it (QUESTIONS.md Q3) — `P4-BT-13/P4-BT-13.outcome.txt`
- `UND:P4-BT-13` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-13/UND:P4-BT-13.outcome.txt`
- `P4-BT-14` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (mount) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-14/P4-BT-14.outcome.txt`
- `UND:P4-BT-14` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-14/UND:P4-BT-14.outcome.txt`
- `P4-BT-15` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (systemctl set-property) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-15/P4-BT-15.outcome.txt`
- `UND:P4-BT-15` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-15/UND:P4-BT-15.outcome.txt`
- `P4-PIPE-1` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 7 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-PIPE-1/P4-PIPE-1.outcome.txt`
- `P1:P4-PIPE-1` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-PIPE-1/P1:P4-PIPE-1.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/cases-pipe.service (`P4-PIPE-1/inv-P4-PIPE-1/compare-p1.tsv`)
- `UND:P4-PIPE-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-PIPE-1/UND:P4-PIPE-1.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/cases-pipe.service (`P4-PIPE-1/inv-P4-PIPE-1/compare-und-reference.tsv`)
- `P4-PIPE-2` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 7 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-PIPE-2/P4-PIPE-2.outcome.txt`
- `P1:P4-PIPE-2` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-PIPE-2/P1:P4-PIPE-2.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/cases-pipe.service (`P4-PIPE-2/inv-P4-PIPE-2/compare-p1.tsv`)
- `UND:P4-PIPE-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-PIPE-2/UND:P4-PIPE-2.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/cases-pipe.service (`P4-PIPE-2/inv-P4-PIPE-2/compare-und-reference.tsv`)
- `P4-PIPE-3` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 6 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-PIPE-3/P4-PIPE-3.outcome.txt`
- `P1:P4-PIPE-3` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-PIPE-3/P1:P4-PIPE-3.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/cases-pipe.service (`P4-PIPE-3/inv-P4-PIPE-3/compare-p1.tsv`)
- `UND:P4-PIPE-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-PIPE-3/UND:P4-PIPE-3.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/cases-pipe.service (`P4-PIPE-3/inv-P4-PIPE-3/compare-und-reference.tsv`)
- `P4-S-054` (P4) **undecided** [Q11, Q12]: met under one reading only: Q11: an object that only a data route executes; Q12: an object that only an interpreter its form does not name accepts | 2 object(s) of attempt-effect.tsv concern these questions | 6 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 2 count against (attempt-effect.tsv) | note: a success of the search: search/routes-0.32.tsv, row  — `P4-S-054/P4-S-054.outcome.txt`
- `P1:P4-S-054` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 2}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-S-054/P1:P4-S-054.outcome.txt`
  - QUESTION `any-only` file /state/home/person/r/054/.pdbrc (`P4-S-054/inv-P4-S-054/compare-p1.tsv`)
  - QUESTION `data-only` file /state/home/person/r/054/t.py (`P4-S-054/inv-P4-S-054/compare-p1.tsv`)
- `UND:P4-S-054` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 2}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-S-054/UND:P4-S-054.outcome.txt`
  - QUESTION `any-only` file /state/home/person/r/054/.pdbrc (`P4-S-054/inv-P4-S-054/compare-und-reference.tsv`)
  - QUESTION `data-only` file /state/home/person/r/054/t.py (`P4-S-054/inv-P4-S-054/compare-und-reference.tsv`)
- `P4-S-056` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 5 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) | note: a success of the search: search/routes-0.32.tsv, row 056 (gyp); attempt from search/routes/056-gyp-co — `P4-S-056/P4-S-056.outcome.txt`
- `P1:P4-S-056` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-S-056/P1:P4-S-056.outcome.txt`
  - QUESTION `any-only` file /state/home/person/r/056/p.gyp (`P4-S-056/inv-P4-S-056/compare-p1.tsv`)
- `UND:P4-S-056` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-S-056/UND:P4-S-056.outcome.txt`
  - QUESTION `any-only` file /state/home/person/r/056/p.gyp (`P4-S-056/inv-P4-S-056/compare-und-reference.tsv`)
- `UND:P4-S-089` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-089/UND:P4-S-089.outcome.txt`
- `UND:P4-S-090` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-090/UND:P4-S-090.outcome.txt`
- `UND:P4-S-107` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-107/UND:P4-S-107.outcome.txt`
- `UND:P4-S-108` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-108/UND:P4-S-108.outcome.txt`
- `P4-S-111` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (apt-get) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies; note: a success of the search: search/routes-0.32.tsv, row 111 (apt-get (APT_CONFIG)); attempt from search/routes/111-apt-config-pre-invoke.sh — `P4-S-111/P4-S-111.outcome.txt`
- `UND:P4-S-111` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-111/UND:P4-S-111.outcome.txt`
- `UND:P4-S-135` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-135/UND:P4-S-135.outcome.txt`
- `UND:P4-S-136` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-136/UND:P4-S-136.outcome.txt`
- `P4-S-160` (P4) **undecided** [Q11]: met under one reading only: Q11: an object that only a data route executes | 1 object(s) of attempt-effect.tsv concern these questions | 43 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) | note: a success of the search: search/routes-0.32.tsv, row 160 (flatpak run (runtime python3)); attempt from search/routes/160-fla — `P4-S-160/P4-S-160.outcome.txt`
- `P1:P4-S-160` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-S-160/P1:P4-S-160.outcome.txt`
  - QUESTION `data-only` file /state/home/person/.var/app/io.mpv.Mpv/r160/c.py (`P4-S-160/inv-P4-S-160/compare-p1.tsv`)
- `UND:P4-S-160` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-S-160/UND:P4-S-160.outcome.txt`
  - QUESTION `data-only` file /state/home/person/.var/app/io.mpv.Mpv/r160/c.py (`P4-S-160/inv-P4-S-160/compare-und-reference.tsv`)
- `P4-S-161` (P4) **undecided** [Q11]: met under one reading only: Q11: an object that only a data route executes | 1 object(s) of attempt-effect.tsv concern these questions | 43 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) | note: a success of the search: search/routes-0.32.tsv, row 161 (flatpak run (runtime sh, stdin)); attempt from search/routes/161-f — `P4-S-161/P4-S-161.outcome.txt`
- `P1:P4-S-161` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-S-161/P1:P4-S-161.outcome.txt`
  - QUESTION `data-only` file /state/home/person/.var/app/io.mpv.Mpv/r161/c.sh (`P4-S-161/inv-P4-S-161/compare-p1.tsv`)
- `UND:P4-S-161` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-S-161/UND:P4-S-161.outcome.txt`
  - QUESTION `data-only` file /state/home/person/.var/app/io.mpv.Mpv/r161/c.sh (`P4-S-161/inv-P4-S-161/compare-und-reference.tsv`)
- `P4-S-162` (P4) **undecided** [Q11, Q12]: met under one reading only: Q11: an object that only a data route executes; Q12: an object that only an interpreter its form does not name accepts | 3 object(s) of attempt-effect.tsv concern these questions | 44 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 3 count against (attempt-effect.tsv) | note: a success of the search: search/routes-0.32.tsv, row — `P4-S-162/P4-S-162.outcome.txt`
- `P1:P4-S-162` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 3}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-S-162/P1:P4-S-162.outcome.txt`
  - QUESTION `data-only` file /state/home/person/.var/app/io.mpv.Mpv/r162/c.sh (`P4-S-162/inv-P4-S-162/compare-p1.tsv`)
  - QUESTION `any-only` file /state/home/person/r/162/out (`P4-S-162/inv-P4-S-162/compare-p1.tsv`)
  - QUESTION `data-only` vfile /tmp/c162.sh (`P4-S-162/inv-P4-S-162/compare-p1.tsv`)
- `UND:P4-S-162` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 3}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-S-162/UND:P4-S-162.outcome.txt`
  - QUESTION `data-only` file /state/home/person/.var/app/io.mpv.Mpv/r162/c.sh (`P4-S-162/inv-P4-S-162/compare-und-reference.tsv`)
  - QUESTION `any-only` file /state/home/person/r/162/out (`P4-S-162/inv-P4-S-162/compare-und-reference.tsv`)
  - QUESTION `data-only` vfile /tmp/c162.sh (`P4-S-162/inv-P4-S-162/compare-und-reference.tsv`)
- `P4-S-166` (P4) **undecided** [Q11]: met under one reading only: Q11: an object that only a data route executes | 1 object(s) of attempt-effect.tsv concern these questions | 43 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) | note: a success of the search: search/routes-0.32.tsv, row 166 (flatpak run (runtime sh, source)); attempt from search/routes/166- — `P4-S-166/P4-S-166.outcome.txt`
- `P1:P4-S-166` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-S-166/P1:P4-S-166.outcome.txt`
  - QUESTION `data-only` file /state/home/person/.var/app/io.mpv.Mpv/r166/c.sh (`P4-S-166/inv-P4-S-166/compare-p1.tsv`)
- `UND:P4-S-166` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-S-166/UND:P4-S-166.outcome.txt`
  - QUESTION `data-only` file /state/home/person/.var/app/io.mpv.Mpv/r166/c.sh (`P4-S-166/inv-P4-S-166/compare-und-reference.tsv`)
- `P4-S-167` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 45 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) | note: a success of the search: search/routes-0.32.tsv, row 167 (mpv (mpv.conf script= of the recorded Flat — `P4-S-167/P4-S-167.outcome.txt`
- `P1:P4-S-167` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-S-167/P1:P4-S-167.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.var/app/io.mpv.Mpv/config/mpv/mpv.conf (`P4-S-167/inv-P4-S-167/compare-p1.tsv`)
- `UND:P4-S-167` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-S-167/UND:P4-S-167.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.var/app/io.mpv.Mpv/config/mpv/mpv.conf (`P4-S-167/inv-P4-S-167/compare-und-reference.tsv`)
- `P4-S-202` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (apt-mark) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies; note: a success of the search: search/attempts-0.32.tsv, row 202 (apt-mark as root); attempt from search/attempts/202-apt-mark-hold-recorded.sh — `P4-S-202/P4-S-202.outcome.txt`
- `UND:P4-S-202` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-202/UND:P4-S-202.outcome.txt`
- `P4-S-234` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (crontab) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies; note: a success of the search: search/attempts-0.32.tsv, row 234 (crontab -u as root); attempt from search/attempts/234-root-crontab-for-account.sh — `P4-S-234/P4-S-234.outcome.txt`
- `UND:P4-S-234` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-234/UND:P4-S-234.outcome.txt`
- `P4-S-241` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 7 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) | note: a success of the search: search/attempts-0.32.tsv, row 241 (curl (~/.curlrc)); attempt from search/at — `P4-S-241/P4-S-241.outcome.txt`
- `P1:P4-S-241` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-S-241/P1:P4-S-241.outcome.txt`
  - QUESTION `any-only` file /state/home/person/r/241/pid (`P4-S-241/inv-P4-S-241/compare-p1.tsv`)
- `UND:P4-S-241` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-S-241/UND:P4-S-241.outcome.txt`
  - QUESTION `any-only` file /state/home/person/r/241/pid (`P4-S-241/inv-P4-S-241/compare-und-reference.tsv`)
- `P4-S-LO-1` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 2 object(s) of attempt-effect.tsv concern these questions | 106 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 2 count against (attempt-effect.tsv) | note: a success of the search: build/IMPOSSIBLE.md, row saved LibreOffice Basic profile libraries (libreo — `P4-S-LO-1/P4-S-LO-1.outcome.txt`
- `UND:P4-S-LO-1-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-LO-1/UND:P4-S-LO-1-apply-1.outcome.txt`
- `P1:P4-S-LO-1` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 193, 'QUESTION': 2}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-S-LO-1/P1:P4-S-LO-1.outcome.txt`
  - QUESTION `any-only` file /state/home/person/lo-profile-user-home/user/basic/Standard/script.xlb (`P4-S-LO-1/inv-P4-S-LO-1/compare-p1.tsv`)
  - QUESTION `any-only` file /state/home/person/lo-profile-user-home/user/basic/script.xlc (`P4-S-LO-1/inv-P4-S-LO-1/compare-p1.tsv`)
- `UND:P4-S-LO-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 2}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-S-LO-1/UND:P4-S-LO-1.outcome.txt`
  - QUESTION `any-only` file /state/home/person/lo-profile-user-home/user/basic/Standard/script.xlb (`P4-S-LO-1/inv-P4-S-LO-1/compare-und-reference.tsv`)
  - QUESTION `any-only` file /state/home/person/lo-profile-user-home/user/basic/script.xlc (`P4-S-LO-1/inv-P4-S-LO-1/compare-und-reference.tsv`)
- `P4-S-LO-2` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 2 object(s) of attempt-effect.tsv concern these questions | 106 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 2 count against (attempt-effect.tsv) | note: a success of the search: build/IMPOSSIBLE.md, row saved LibreOffice Basic profile libraries (libreo — `P4-S-LO-2/P4-S-LO-2.outcome.txt`
- `UND:P4-S-LO-2-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-S-LO-2/UND:P4-S-LO-2-apply-1.outcome.txt`
- `P1:P4-S-LO-2` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 193, 'QUESTION': 2}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-S-LO-2/P1:P4-S-LO-2.outcome.txt`
  - QUESTION `any-only` vfile /tmp/lo-profile-user-tmp/user/basic/Standard/script.xlb (`P4-S-LO-2/inv-P4-S-LO-2/compare-p1.tsv`)
  - QUESTION `any-only` vfile /tmp/lo-profile-user-tmp/user/basic/script.xlc (`P4-S-LO-2/inv-P4-S-LO-2/compare-p1.tsv`)
- `UND:P4-S-LO-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 2}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-S-LO-2/UND:P4-S-LO-2.outcome.txt`
  - QUESTION `any-only` vfile /tmp/lo-profile-user-tmp/user/basic/Standard/script.xlb (`P4-S-LO-2/inv-P4-S-LO-2/compare-und-reference.tsv`)
  - QUESTION `any-only` vfile /tmp/lo-profile-user-tmp/user/basic/script.xlc (`P4-S-LO-2/inv-P4-S-LO-2/compare-und-reference.tsv`)
- `UND:REM-1-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-1/UND:REM-1-apply-1.outcome.txt`
- `UND:REM-1-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-1/UND:REM-1-apply-2.outcome.txt`
- `UND:REM-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-1/UND:REM-1.outcome.txt`
- `UND:REM-2-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-2/UND:REM-2-apply-1.outcome.txt`
- `UND:REM-2-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-2/UND:REM-2-apply-2.outcome.txt`
- `UND:REM-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-2/UND:REM-2.outcome.txt`
- `UND:REM-3a-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-3a/UND:REM-3a-apply-1.outcome.txt`
- `UND:REM-3a-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-3a/UND:REM-3a-apply-2.outcome.txt`
- `UND:REM-3a` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-3a/UND:REM-3a.outcome.txt`
- `UND:REM-3b-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-3b/UND:REM-3b-apply-1.outcome.txt`
- `UND:REM-3b-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-3b/UND:REM-3b-apply-2.outcome.txt`
- `UND:REM-3b` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-3b/UND:REM-3b.outcome.txt`
- `UND:REM-4-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-4/UND:REM-4-apply-1.outcome.txt`
- `UND:REM-4-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-4/UND:REM-4-apply-2.outcome.txt`
- `UND:REM-4a` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-4/UND:REM-4a.outcome.txt`
- `UND:REM-4-apply-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-4/UND:REM-4-apply-3.outcome.txt`
- `UND:REM-4b` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REM-4/UND:REM-4b.outcome.txt`
- `UND:REPRO-1-a` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REPRO-1/UND:REPRO-1-a.outcome.txt`
- `UND:REPRO-1-b` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REPRO-1/UND:REPRO-1-b.outcome.txt`
- `UND:REPRO-2a-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REPRO-2a/UND:REPRO-2a-apply-1.outcome.txt`
- `UND:REPRO-2a-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REPRO-2a/UND:REPRO-2a-apply-2.outcome.txt`
- `UND:REPRO-2a-apply-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REPRO-2a/UND:REPRO-2a-apply-3.outcome.txt`
- `UND:REPRO-2a-apply-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REPRO-2a/UND:REPRO-2a-apply-4.outcome.txt`
- `UND:REPRO-2a-x` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REPRO-2a/UND:REPRO-2a-x.outcome.txt`
- `UND:REPRO-2a-y` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REPRO-2a/UND:REPRO-2a-y.outcome.txt`
- `REPRO-2b` (REPRO) **unobserved** [-]: unobserved: not expressible: account tcpdump groups=- shell=/usr/sbin/nologin: not expressible: the `account` kind requires the numeric UID and GID — `REPRO-2b/REPRO-2b.outcome.txt`
