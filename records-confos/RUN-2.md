# Complete run 2

Written by the case party. Times in UTC.

## Departures from the plan, stated before the results

1. **One pinned component of release 0.49 is not the latest at the time of the commit of the inputs**
   (2026-11-24 23:02:07 UTC): `libzstd1` is pinned at 1.5.7+dfsg-1; the archive has 1.5.7+dfsg-1+deb13u1. Checked
   with `python3 -I tools/lock-check.py` on the 0.49 source at `20261124T230207Z`, lock
   `components/20261123T000000Z.txt` (output `ready/lock-check-0.49.tsv`): of 113 components, 108 are the same as
   the newest archive states at that time (debian `20261124T202946Z`, debian-security `20261124T215723Z`), 4 are
   the implementation's own components, and 1 is newer in the archive — this one. The departure of run 1
   (`linux-image-amd64` 6.12.117-1 against 6.12.118-1) is gone: on 0.49 that component is the same as the archive.
2. **The successes of the search after run 1 were not yet cases of this run** (an omission of the party that directed the work, order 4 of
   2026-11-25 00:38 UTC). Plan, Section 9.5: “Each success becomes a new case, committed before the next complete
   run.” The search of release 0.32 (`search/routes-0.32.tsv`, `search/attempts-0.32.tsv`, 18:20 UTC) had 14 direct
   routes and 3 attempts that ran; none of them is a case of `CASES.md` of the fifth freeze, so this run did not
   perform them. They become cases in the sixth freeze (`CASES.md`, section P4-S), before complete run 3.

## The run

- Inputs: commit `9e99accd47d9e29dbaef4532842c7b6f015556c5` of the repository of records, 2026-11-24 23:02:07 UTC
  (folders `confos/`, release 0.49, and `confos-check/`, the fifth freeze of the programs).
- Release 0.49 source archive SHA256 `0f71e751f85a05fba1a8f8c726c823109a6dec6feaa1d27e210e5c729d9ef4db`, checked on the
  server before the run.
- Before the run, the specificity test of the fifth freeze on 0.49: `SPECIFICITY TEST PASS 20/20` (23:03:22 –
  23:11:51 UTC; `D-test` built; output `scraps/f6/specificity-0.49.txt`).
- Programs: the fifth freeze (`run/src11`); `sha256sum -c src11.sha256` before the run: every file OK; no program
  changed while the run was going.
- Command: `run --source confos-0.49-source.tar.gz --name run-2 --max-vms 5` (every case of `CASES.md` of the fifth
  freeze, nothing skipped), with `CASES_SLOT_WAIT=14400`.
- Time: 2026-11-24 23:12:43 – 2026-11-25 01:34:40 UTC; at most 5 machines at once; every machine stopped and the work
  folder removed at the end (no machine of the run was left running; checked with `pgrep -af qemu` at 01:35 UTC).
- Results: `runs/run-2/results.tsv` on the server (385 rows); every evidence path below is relative to `runs/run-2/`.
- The list for the builder (case ID, command, output of every row that did not pass): `REQUESTS.md`, entry 14.
- Evidence lost after run 1: the folder `runs/dev-11` was deleted on the server at 2026-11-24 23:21 UTC to stay within
  the disk limit, without a copy; `RUN-1.md`, item 1, cites `runs/dev-11/REPRO-2a/REPRO-2a.outcome.txt` from it. The
  repaired REPRO-2a is `pass` in this run (below).

## Rows by part and outcome

| part | pass | fail | unobserved | undecided | all |
|---|---|---|---|---|---|
| OW | 6 | 3 | 2 | 0 | 11 |
| P1 | 113 | 0 | 0 | 14 | 127 |
| P2 | 39 | 0 | 0 | 0 | 39 |
| P4 | 18 | 0 | 0 | 54 | 72 |
| REM | 5 | 0 | 0 | 0 | 5 |
| REPRO | 2 | 0 | 1 | 0 | 3 |
| UND | 1 | 0 | 0 | 127 | 128 |
| all | 184 | 3 | 3 | 195 | 385 |

## Rows that are not `pass` because of a program of the case party

None. The three defects of run 1 that were the case party's are repaired in the fifth freeze (`CORRECTIONS.md`,
[f5]), and their rows here are: `REPRO-2a` `pass`; `P4-C9-1`, `P4-C9-2` and their `P1:` and `UND:` rows decided
(`undecided` by Q11, every route line written, no `UNROUTED` object); the inventories `P4-PIPE-n-before` are records
(`P1:P4-PIPE-n-before.record.txt`, `UND:P4-PIPE-n-before.record.txt`) and no rows (R6).

## Rows that are not `pass` because of the plan or the implementation

- `OW-2`, `OW-3` `fail`: release 0.49 does not build the clean installation of the declaration of the first update
  (snapshot `20260801T000000Z`): `build.sh` exit 1, `ValueError: reader override original checksum mismatch:
  /usr/bin/curl` (`OW-2/0001.err`; `optional_readers.py` line 34). OW-3 is the second update of the same case.
- `OW-8` `fail`: the application of the game's update 26.6.0 did not report success: `confos apply` exited 1 before
  a reboot, `OSError: [Errno 28] No space left on device: '/state/staging/initramfs'` (`OW-8/0446.err`; the disk of
  a clean installation is 12 GiB, `assemble.py` line 676, `qemu-img create -f qcow2 output 12G`). The person's own
  launcher outside the declaration was refused (exit 126, `OW-8/direct.json`; REVIEW.md R2).
- `OW-10`, `OW-11` `unobserved`: not performed in this run: real hardware (plan, Section 9.3; the rules of the work, item 6).
- `REPRO-2b` `unobserved`: the case asks for account lines without the numeric identifiers; the implementation's
  `account` kind requires them (`build/DECLARATION.md`), so the case is “not expressible” (`CASES.md`, REPRO-2b).
- 54 P4 rows `undecided`. 35 depend on S8.3-7 only: a built-in tool refused, and nothing of the attempt is in force
  (reading A met, reading B not; R3 of the review applies). 8 are `undecided` by Q3: a declaration
  file changed although the runner did not write it — the built-in tool recorded the request in the declaration
  (`build/CHOICES.md`; how the plan counts a line written by a tool of the implementation is applied by the review,
  the rules of the work, item 1); P4-BT-5 also carries Q6. The change of each, the declaration read from the disk after the
  attempt against `D-test` (`scraps/f7/q3-diff.sh`, files `CASE/decl-CASE/state-declaration.conf`): P4-C1-2 adds
  `package hello 2.10-5`; P4-C1-4 removes `package ed 1.21.1-1`; P4-C2-3 adds `pip pyjokes 0.8.3 …`; P4-C3-4 adds
  `npm semver 7.6.3 …`; P4-BT-1 adds `account p4user 1001 1001 - /bin/bash /home/p4user`; P4-BT-5 adds `file
  /etc/sudoers.d/confos-local 0440 0:0 …`; P4-BT-9 changes `setting hostname confos-test` to `setting hostname
  p4host`; P4-BT-13 adds `setting sysctl:net.ipv4.ip_forward 1`. 11 depend on Q11 or Q12 (an object that only a data route, or only
  an interpreter its form does not name, executes).
- 14 P1 rows `undecided`, all by `QUESTION` objects (Q11, Q12) or `BOTHWAYS` (Q2), listed with their kind and path.
- 127 UND rows `undecided`: met against the reference installation and not under the derivation from the
  declaration alone (D1, D3–D6); those whose reading against the reference installation is itself undecided by
  `QUESTION` objects list them.

## Every row that is not `pass`

Form: row, part, outcome, the questions its outcome text names, one sentence, the evidence file. Under each P1 or
UND row that is `undecided` because of `QUESTION` objects: each object with its kind from the routes of its
comparison (`data-only`: only a data route executed it, Q11; `any-only`: only an interpreter that its form does
not name accepted it, Q12), its path and the comparison table.

- `UND:OW-1-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-1/UND:OW-1-apply-1.outcome.txt`
- `UND:OW-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-1/UND:OW-1.outcome.txt`
- `OW-2` (OW) **fail** [-]: StepFailed: the clean build failed (exit 1) — `OW-2/OW-2.outcome.txt`
- `OW-3` (OW) **fail** [-]: StepFailed: the clean build failed (exit 1) — `OW-2/OW-3.outcome.txt`
- `UND:OW-4-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-4/UND:OW-4-apply-1.outcome.txt`
- `P1:OW-4` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 193, 'QUESTION': 2}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `OW-4/P1:OW-4.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/qtjwz0hu.default/times.json (`OW-4/inv-OW-4/compare-p1.tsv`)
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/sffqqpw5.default-esr/times.json (`OW-4/inv-OW-4/compare-p1.tsv`)
- `UND:OW-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 2}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `OW-4/UND:OW-4.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/qtjwz0hu.default/times.json (`OW-4/inv-OW-4/compare-und-reference.tsv`)
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/sffqqpw5.default-esr/times.json (`OW-4/inv-OW-4/compare-und-reference.tsv`)
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
- `OW-8` (OW) **fail** [R2]: 26.6.0: the application did not report success: confos apply exited 1 before a reboot | through the lines of the declaration and confos apply (REVIEW.md R2); the person's own launcher: `mkdir -p ~/game-direct && cd ~/game-direct && curl -fsSLo li` exit 0; `cd ~/game-direct && bash linuxgsm.sh wetserver` exit 126 (direct.json) — `OW-8/OW-8.outcome.txt`
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
- `P4-BT-4` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (groupadd) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-4/P4-BT-4.outcome.txt`
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
- `P4-BT-12` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (modprobe) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-12/P4-BT-12.outcome.txt`
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
