# Complete run 1

Written by the case party. Times in UTC.

## Departure from the plan, stated before the results

One pinned component of release 0.32 is not the latest of the day of the commit of the inputs (2026-11-24
16:27:01 UTC): `linux-image-amd64` is pinned at 6.12.117-1; the security archive has 6.12.118-1. Checked with
`python3 -I tools/lock-check.py --source confos-0.32-source.tar.gz --lock components/20261123T000000Z.txt --at
20261124T162701Z` (output `ready/lock-check-0.32.tsv`): of 113 components, 108 are the same as the newest archive
states at that time (debian `20261124T150911Z`, debian-security `20261124T152313Z`), 4 are the implementation's own
components, and 1 is newer in the archive — this one.

## The run

- Inputs: commit `425609f9fbf119dcf83a2c71d2a2912818a3be49` of the repository of records (folders `confos/`, release
  0.32, and `confos-check/`, the fourth freeze of the programs).
- Release 0.32 source archive SHA256 `61d290744606b4804b298217d340df5445cf276ea2b3ad69cc024e9457261001`, checked on the
  server before the run.
- Programs: the fourth freeze (`run/src10`); `sha256sum -c src10.sha256` before the run: every file OK; no program
  changed while the run was going.
- Command: `run --source confos-0.32-source.tar.gz --name run-1 --max-vms 3` (every case of `CASES.md`, nothing
  skipped), with `CASES_SLOT_WAIT=14400`.
- Time: 2026-11-24 16:28:41 – 19:56:38 UTC; at most 3 machines at once; every machine stopped and the work folder
  removed at the end (no machine of the run was left running; checked with `pgrep -af qemu` at 19:57 UTC).
- Results: `runs/run-1/results.tsv` on the server (388 rows); every evidence path below is relative to `runs/run-1/`.
- The list for the builder (case ID, command, output of every row that did not pass): `REQUESTS.md`, entry 12.

## Rows by part and outcome

| part | pass | fail | unobserved | undecided | all |
|---|---|---|---|---|---|
| OW | 9 | 0 | 2 | 0 | 11 |
| P1 | 112 | 0 | 2 | 15 | 129 |
| P2 | 38 | 0 | 0 | 0 | 38 |
| P4 | 18 | 0 | 2 | 52 | 72 |
| REM | 5 | 0 | 0 | 0 | 5 |
| REPRO | 1 | 1 | 1 | 0 | 3 |
| UND | 1 | 0 | 2 | 127 | 130 |
| all | 184 | 1 | 9 | 194 | 388 |

## Rows that are not `pass` because of a program of the case party

As the order says, none was repaired during the run.

1. **`REPRO-2a` `fail`: the declaration line written by `run`, not the implementation.** `run` (lines 1679–1680)
   declares the two package accounts with `home=/nonexistent`. On the first machine, `confos apply` refused that
   text before a reboot (`REPRO-2a/0040.err`: `ValueError: account home must be an immediate child of /home`,
   `assemble.py` line 96, `validate_accounts`). The implementation documents this rule (`build/DECLARATION.md`:
   “Source 0.7 requires account homes immediately below /home”). The value was `home=/home/tcpdump` up to the copy
   `run/src3` and became `/nonexistent` on 2026-11-24 at about 14:40 UTC, in the cleaning of invented home paths
   before publication (`run/src4` … `run/src10`). With the earlier value, REPRO-2a was `pass` on 0.22 (development
   run dev-11, `runs/dev-11/REPRO-2a/REPRO-2a.outcome.txt`). No run after that change reached REPRO-2a (`READY.md`,
   section 4: “REPRO-1, REPRO-2a, REPRO-2b: … not exercised”). So this row says nothing about the implementation.
2. **`P4-C9-1`, `P1:P4-C9-1`, `UND:P4-C9-1`, `P4-C9-2`, `P1:P4-C9-2`, `UND:P4-C9-2` `unobserved`: the routes of
   `run`.** The object that decides each row is the attempt's file in `/tmp` (`/tmp/f.sh`, `/tmp/f.py`). It is
   `UNROUTED`: no route line was written for it (`P4-C9-1/attempt-effect.tsv`: `attempt:UNRECORDED UNROUTED vfile
   /tmp/f.sh code in form (suffix) and no direct route was tried`; `inv-P4-C9-1/routes.tsv` has lines for
   `/dev/shm/f.sh` and `/home/person/f.sh` only). Both calls of the routes timed out over SSH
   (`P4-C9-1/log.txt`: inventory done 18:00:09; routes of 3 files until 18:24:09, which is 2 × 720 s, the timeout
   `600 + 40 × 3` for the person and for root; routes of 35 files 18:24:11 – 19:30:51, about 2 × 2000 s;
   `P4-C9-2/log.txt`: 18:00:48 – 18:24:51 and until 19:31:33). The cause, shown by an experiment after the run (below): a route that runs the
   file starts its background process (`sleep 86413 &`), which keeps the pipe of the route's `$(…)` open, so the
   routes script never ends and the file gets no route line. The routes of `/home/person/f.sh` and `/dev/shm/f.sh`
   are `refused`; in P4-C9-3 (`perl`) both calls of the routes ended by 18:01:26, within a minute of its inventory.

   **Experiment** (`ready/run-1/c9probe.sh` with the frozen routes script copied to `ready/run-1/routes.sh`, not part of any run; output `ready/run-1/c9probe-output.txt`): the clean
   D-test installation that run-1 built from 0.32 (`APPLIED b67c320b…`), a file of the form of P4-C9-1 (`sleep 86413 &`) written to `/tmp/f.sh`
   as the person, and the frozen routes script given that one file under `bash -x` with an outer `timeout 120`:
   the same then for `/tmp/f.py` of the form of P4-C9-2 (`subprocess.Popen(["sleep", "86414"], start_new_session=True)`), each first as the person, then as root (19:57–20:05 UTC).

   | File | Direct routes (path, loader, bash, sh, bash-stdin, source, python3, perl, awk, make, node) | The data route that ran it | After the route |
   |---|---|---|---|
   | `/tmp/f.sh` | none executed it, as the person or as root (`ConfOS: Permission denied for saved code input`; the loader: not an ELF file; awk, make: nothing to execute) | `cat /tmp/f.sh \| timeout 10 bash` (`cat-pipe-bash`) | `sleep 86413` running, parent PID 1 (PID 497 after the person's routes, 745 after root's); the routes script did not end within 120 s |
   | `/tmp/f.py` | none executed it, as the person or as root | `python3 -c 'import sys; exec(open(sys.argv[1], "rb").read())' /tmp/f.py` (`python3-exec`) | `sleep 86414` running, parent PID 1 (PID 634, 874); the routes script did not end within 120 s |

   The last traced command of each hung call is that data route. Under the rule of `run` (`try_routes`), a file whose
   every direct route is refused and that a data route runs is `data-only` (Q11), and `compare` makes such an object
   `QUESTION`. The run did not reach that because the route did not return. That a typed data route runs these two
   files is an observation on 0.32; that their rows say `unobserved` instead is the defect of `run`.
3. **The reason text of `UND:P4-PIPE-1-before`, `UND:P4-PIPE-2-before`, `UND:P4-PIPE-3-before`** says “met under one
   reading only: undecided (D1, D3, D4, D5, D6)”, but both readings are `fail` there. The outcome `undecided` comes from
   Q4 (`run`, `p1_und_rows`: an inventory `-before` of a P4-PIPE case that would fail is `undecided`, as its P1 row
   is). The outcome is the one the code intends; only its reason text names the wrong questions. The lines below
   give Q4.

## Rows that are not `pass` because of the plan or the implementation

- `OW-10`, `OW-11`: not performed in this run: real hardware (plan, Section 9.3; the rules of the work, item 6).
- `REPRO-2b` `unobserved`: the case asks for account lines without the numeric identifiers. The implementation's
  `account` kind requires them (`build/DECLARATION.md`: `account NAME UID GID GROUPS SHELL HOME`), so the case is
  “not expressible” (`CASES.md`, REPRO-2b: “if the format does not admit a line without the identifier →
  `unobserved: not expressible`”).
- 52 P4 rows `undecided`. 42 of them depend on S8.3-7: a built-in tool refused, and nothing of the attempt is in
  force. That meets reading A and not reading B, under which the tool adds the change to the declaration. R3 of the
  review applies (P4-BT-5 also carries a note of Q6). 9 depend on Q11 or Q12 (an object that only a data route, or only an interpreter
  its form does not name, executes).
- 15 P1 rows `undecided`. 12 are undecided by `QUESTION` objects (Q11, Q12), listed with their kind and path. 3 are
  undecided by Q4 (the `-before` inventories of P4-PIPE-1 … 3: the person's user unit
  `~/.config/systemd/user/cases-pipe.service` was in force before the restart).
- 127 UND rows `undecided`. 112 are met against the reference installation and not under the derivation from the
  declaration alone (D1, D3–D6). 12 are the same, and the reading against the reference installation is itself
  undecided by `QUESTION` objects (listed). 3 are Q4 (the `-before` inventories).

## Every row that is not `pass`

Form: row, part, outcome, the questions its outcome text names, one sentence, the evidence file. Under each P1 or
UND row that is `undecided` because of `QUESTION` objects: each object with its kind from the routes of its
comparison (`data-only`: only a data route executed it, Q11; `any-only`: only an interpreter that its form does
not name accepted it, Q12), its path and the comparison table. Under each Q4 row, the object that would count
under reading B.

- `UND:OW-1-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-1/UND:OW-1-apply-1.outcome.txt`
- `UND:OW-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-1/UND:OW-1.outcome.txt`
- `UND:OW-2-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-2/UND:OW-2-apply-1.outcome.txt`
- `UND:OW-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-2/UND:OW-2.outcome.txt`
- `UND:OW-2-apply-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-2/UND:OW-2-apply-2.outcome.txt`
- `UND:OW-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-2/UND:OW-3.outcome.txt`
- `UND:OW-4-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `OW-4/UND:OW-4-apply-1.outcome.txt`
- `P1:OW-4` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 193, 'QUESTION': 2}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `OW-4/P1:OW-4.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/0hf6166t.default/times.json (`OW-4/inv-OW-4/compare-p1.tsv`)
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/9kvhd2yj.default-esr/times.json (`OW-4/inv-OW-4/compare-p1.tsv`)
- `UND:OW-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 2}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `OW-4/UND:OW-4.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/0hf6166t.default/times.json (`OW-4/inv-OW-4/compare-und-reference.tsv`)
  - QUESTION `any-only` file /state/home/person/.config/mozilla/firefox/9kvhd2yj.default-esr/times.json (`OW-4/inv-OW-4/compare-und-reference.tsv`)
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
- `P4-C1-2` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (apt-get) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C1-2/P4-C1-2.outcome.txt`
- `UND:P4-C1-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-2/UND:P4-C1-2.outcome.txt`
- `P4-C1-3` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (dpkg) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C1-3/P4-C1-3.outcome.txt`
- `UND:P4-C1-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-3/UND:P4-C1-3.outcome.txt`
- `P4-C1-4` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (apt-get) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C1-4/P4-C1-4.outcome.txt`
- `UND:P4-C1-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-4/UND:P4-C1-4.outcome.txt`
- `P4-C1-5` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (dpkg) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C1-5/P4-C1-5.outcome.txt`
- `UND:P4-C1-5` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-5/UND:P4-C1-5.outcome.txt`
- `P4-C1-6` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (dpkg-deb) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C1-6/P4-C1-6.outcome.txt`
- `UND:P4-C1-6` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C1-6/UND:P4-C1-6.outcome.txt`
- `P4-C2-1` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (pip) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C2-1/P4-C2-1.outcome.txt`
- `UND:P4-C2-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C2-1/UND:P4-C2-1.outcome.txt`
- `P4-C2-2` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (venv, pip) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C2-2/P4-C2-2.outcome.txt`
- `UND:P4-C2-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C2-2/UND:P4-C2-2.outcome.txt`
- `P4-C2-3` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (pip) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C2-3/P4-C2-3.outcome.txt`
- `UND:P4-C2-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C2-3/UND:P4-C2-3.outcome.txt`
- `P4-C2-4` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (pip) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C2-4/P4-C2-4.outcome.txt`
- `UND:P4-C2-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C2-4/UND:P4-C2-4.outcome.txt`
- `P4-C3-1` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (npm) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C3-1/P4-C3-1.outcome.txt`
- `UND:P4-C3-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C3-1/UND:P4-C3-1.outcome.txt`
- `P4-C3-2` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (npm) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C3-2/P4-C3-2.outcome.txt`
- `UND:P4-C3-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C3-2/UND:P4-C3-2.outcome.txt`
- `P4-C3-3` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (npx) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C3-3/P4-C3-3.outcome.txt`
- `UND:P4-C3-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-C3-3/UND:P4-C3-3.outcome.txt`
- `P4-C3-4` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (npm) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-C3-4/P4-C3-4.outcome.txt`
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
- `P4-C8-1` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 5 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-C8-1/P4-C8-1.outcome.txt`
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
- `P4-C9-1` (P4) **unobserved** [-]: 1 object(s) changed by the attempt could count against, but the route or probe that decides them was not taken (UNROUTED, UNPROBED in attempt-effect.tsv) | 3 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-C9-1/P4-C9-1.outcome.txt`
- `P1:P4-C9-1` (P1) **unobserved** [Q2, Q11, Q12]: objects that equal neither the derivation nor the reference installation, after the four questions: {'UNDERIVED': 171, 'UNROUTED': 2} — `P4-C9-1/P1:P4-C9-1.outcome.txt`
- `UND:P4-C9-1` (UND) **unobserved** [D1, D3, D6]: harder reading (derivation from the declaration alone, D1, D3–D6 as followed in QUESTIONS-derive.md): fail, counts {'UNRECORDED': 81118, 'UNDERIVED': 171, 'UNROUTED': 29, 'UNPROBED': 6} | easier reading (what the published source gives for the declaration: the reference installation): unobserved, counts {'UNROUTED': 2} | outcome unobserved — `P4-C9-1/UND:P4-C9-1.outcome.txt`
- `P4-C9-2` (P4) **unobserved** [-]: 1 object(s) changed by the attempt could count against, but the route or probe that decides them was not taken (UNROUTED, UNPROBED in attempt-effect.tsv) | 3 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-C9-2/P4-C9-2.outcome.txt`
- `P1:P4-C9-2` (P1) **unobserved** [Q2, Q11, Q12]: objects that equal neither the derivation nor the reference installation, after the four questions: {'UNDERIVED': 171, 'UNROUTED': 2} — `P4-C9-2/P1:P4-C9-2.outcome.txt`
- `UND:P4-C9-2` (UND) **unobserved** [D1, D3, D6]: harder reading (derivation from the declaration alone, D1, D3–D6 as followed in QUESTIONS-derive.md): fail, counts {'UNRECORDED': 81118, 'UNDERIVED': 171, 'UNROUTED': 29, 'UNPROBED': 6} | easier reading (what the published source gives for the declaration: the reference installation): unobserved, counts {'UNROUTED': 2} | outcome unobserved — `P4-C9-2/UND:P4-C9-2.outcome.txt`
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
- `P4-C10-7` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 2 object(s) of attempt-effect.tsv concern these questions | 2 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 2 count against (attempt-effect.tsv) — `P4-C10-7/P4-C10-7.outcome.txt`
- `P1:P4-C10-7` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 2}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-C10-7/P1:P4-C10-7.outcome.txt`
  - QUESTION `any-only` file /state/home/person/k (`P4-C10-7/inv-P4-C10-7/compare-p1.tsv`)
  - QUESTION `any-only` file /state/home/person/k.pub (`P4-C10-7/inv-P4-C10-7/compare-p1.tsv`)
- `UND:P4-C10-7` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 2}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-C10-7/UND:P4-C10-7.outcome.txt`
  - QUESTION `any-only` file /state/home/person/k (`P4-C10-7/inv-P4-C10-7/compare-und-reference.tsv`)
  - QUESTION `any-only` file /state/home/person/k.pub (`P4-C10-7/inv-P4-C10-7/compare-und-reference.tsv`)
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
- `P4-BT-1` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (useradd) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-1/P4-BT-1.outcome.txt`
- `UND:P4-BT-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-1/UND:P4-BT-1.outcome.txt`
- `P4-BT-2` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (usermod) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-2/P4-BT-2.outcome.txt`
- `UND:P4-BT-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-2/UND:P4-BT-2.outcome.txt`
- `P4-BT-3` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (chpasswd) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-3/P4-BT-3.outcome.txt`
- `UND:P4-BT-3` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-3/UND:P4-BT-3.outcome.txt`
- `P4-BT-4` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (groupadd) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-4/P4-BT-4.outcome.txt`
- `UND:P4-BT-4` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-4/UND:P4-BT-4.outcome.txt`
- `P4-BT-5` (P4) **undecided** [S8.3-7, Q6, S8.1-8]: S8.3-7: the built-in tool (visudo) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies; note: breaking-candidate (QUESTIONS.md Q6): `install` into /etc/sudoers.d is file copying (S8.1-8) — `P4-BT-5/P4-BT-5.outcome.txt`
- `UND:P4-BT-5` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-5/UND:P4-BT-5.outcome.txt`
- `P4-BT-6` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (nft) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-6/P4-BT-6.outcome.txt`
- `UND:P4-BT-6` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-6/UND:P4-BT-6.outcome.txt`
- `P4-BT-7` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (ip) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-7/P4-BT-7.outcome.txt`
- `UND:P4-BT-7` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-7/UND:P4-BT-7.outcome.txt`
- `P4-BT-8` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (nmcli) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies; note: without NetworkManager the attempt cannot run; the outcome is then decided by the probe and CMP — `P4-BT-8/P4-BT-8.outcome.txt`
- `UND:P4-BT-8` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-8/UND:P4-BT-8.outcome.txt`
- `P4-BT-9` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (hostnamectl) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-9/P4-BT-9.outcome.txt`
- `UND:P4-BT-9` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-9/UND:P4-BT-9.outcome.txt`
- `P4-BT-10` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (timedatectl) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-10/P4-BT-10.outcome.txt`
- `UND:P4-BT-10` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-10/UND:P4-BT-10.outcome.txt`
- `P4-BT-11` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (localectl) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-11/P4-BT-11.outcome.txt`
- `UND:P4-BT-11` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-11/UND:P4-BT-11.outcome.txt`
- `P4-BT-12` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (modprobe) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-12/P4-BT-12.outcome.txt`
- `UND:P4-BT-12` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-12/UND:P4-BT-12.outcome.txt`
- `P4-BT-13` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (sysctl) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-13/P4-BT-13.outcome.txt`
- `UND:P4-BT-13` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-13/UND:P4-BT-13.outcome.txt`
- `P4-BT-14` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (mount) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-14/P4-BT-14.outcome.txt`
- `UND:P4-BT-14` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-14/UND:P4-BT-14.outcome.txt`
- `P4-BT-15` (P4) **undecided** [S8.3-7]: S8.3-7: the built-in tool (systemctl set-property) refused and nothing of the attempt is in force (met under reading A); it did not add the change to the declaration (not met under reading B); R3 of the review applies — `P4-BT-15/P4-BT-15.outcome.txt`
- `UND:P4-BT-15` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `P4-BT-15/UND:P4-BT-15.outcome.txt`
- `P4-PIPE-1` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 6 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-PIPE-1/P4-PIPE-1.outcome.txt`
- `P1:P4-PIPE-1-before` (P1) **undecided** [Q2, Q11, Q12, Q4]: Q4: the state before the restart, {'UNDERIVED': 171, 'UNRECORDED': 1}: counts under reading B of Q4, is not judged under reading A — `P4-PIPE-1/P1:P4-PIPE-1-before.outcome.txt`
  - UNRECORDED file /state/home/person/.config/systemd/user/cases-pipe.service: a setting obeyed: a probe of the case showed it in force;  (`P4-PIPE-1/inv-P4-PIPE-1-before/compare-p1.tsv`)
- `UND:P4-PIPE-1-before` (UND) **undecided** [D1, D3, D6, D4, D5]: Q4: the state before the restart, {'UNRECORDED': 1} against the reference installation: counts under reading B of Q4, is not judged under reading A; the runner's reason text names D1–D6 here, the outcome comes from Q4 (run, p1_und_rows) — `P4-PIPE-1/UND:P4-PIPE-1-before.outcome.txt`
  - UNRECORDED file /state/home/person/.config/systemd/user/cases-pipe.service: a setting obeyed: a probe of the case showed it in force;  (`P4-PIPE-1/inv-P4-PIPE-1-before/compare-und-reference.tsv`)
- `P1:P4-PIPE-1` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-PIPE-1/P1:P4-PIPE-1.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/cases-pipe.service (`P4-PIPE-1/inv-P4-PIPE-1/compare-p1.tsv`)
- `UND:P4-PIPE-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-PIPE-1/UND:P4-PIPE-1.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/cases-pipe.service (`P4-PIPE-1/inv-P4-PIPE-1/compare-und-reference.tsv`)
- `P4-PIPE-2` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 6 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-PIPE-2/P4-PIPE-2.outcome.txt`
- `P1:P4-PIPE-2-before` (P1) **undecided** [Q2, Q11, Q12, Q4]: Q4: the state before the restart, {'UNDERIVED': 171, 'UNRECORDED': 1}: counts under reading B of Q4, is not judged under reading A — `P4-PIPE-2/P1:P4-PIPE-2-before.outcome.txt`
  - UNRECORDED file /state/home/person/.config/systemd/user/cases-pipe.service: a setting obeyed: a probe of the case showed it in force;  (`P4-PIPE-2/inv-P4-PIPE-2-before/compare-p1.tsv`)
- `UND:P4-PIPE-2-before` (UND) **undecided** [D1, D3, D6, D4, D5]: Q4: the state before the restart, {'UNRECORDED': 1} against the reference installation: counts under reading B of Q4, is not judged under reading A; the runner's reason text names D1–D6 here, the outcome comes from Q4 (run, p1_und_rows) — `P4-PIPE-2/UND:P4-PIPE-2-before.outcome.txt`
  - UNRECORDED file /state/home/person/.config/systemd/user/cases-pipe.service: a setting obeyed: a probe of the case showed it in force;  (`P4-PIPE-2/inv-P4-PIPE-2-before/compare-und-reference.tsv`)
- `P1:P4-PIPE-2` (P1) **undecided** [Q2, Q11, Q12]: after the four questions, objects that equal neither the derivation nor the reference installation: {'UNDERIVED': 171, 'QUESTION': 1}; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below — `P4-PIPE-2/P1:P4-PIPE-2.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/cases-pipe.service (`P4-PIPE-2/inv-P4-PIPE-2/compare-p1.tsv`)
- `UND:P4-PIPE-2` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: undecided, {'QUESTION': 1}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below — `P4-PIPE-2/UND:P4-PIPE-2.outcome.txt`
  - QUESTION `any-only` file /state/home/person/.config/systemd/user/cases-pipe.service (`P4-PIPE-2/inv-P4-PIPE-2/compare-und-reference.tsv`)
- `P4-PIPE-3` (P4) **undecided** [Q12]: met under one reading only: Q12: an object that only an interpreter its form does not name accepts | 1 object(s) of attempt-effect.tsv concern these questions | 5 object(s) differ between the inventories before and after the attempt (attempt-delta.tsv); 1 count against (attempt-effect.tsv) — `P4-PIPE-3/P4-PIPE-3.outcome.txt`
- `P1:P4-PIPE-3-before` (P1) **undecided** [Q2, Q11, Q12, Q4]: Q4: the state before the restart, {'UNDERIVED': 171, 'UNRECORDED': 1}: counts under reading B of Q4, is not judged under reading A — `P4-PIPE-3/P1:P4-PIPE-3-before.outcome.txt`
  - UNRECORDED file /state/home/person/.config/systemd/user/cases-pipe.service: a setting obeyed: a probe of the case showed it in force;  (`P4-PIPE-3/inv-P4-PIPE-3-before/compare-p1.tsv`)
- `UND:P4-PIPE-3-before` (UND) **undecided** [D1, D3, D6, D4, D5]: Q4: the state before the restart, {'UNRECORDED': 1} against the reference installation: counts under reading B of Q4, is not judged under reading A; the runner's reason text names D1–D6 here, the outcome comes from Q4 (run, p1_und_rows) — `P4-PIPE-3/UND:P4-PIPE-3-before.outcome.txt`
  - UNRECORDED file /state/home/person/.config/systemd/user/cases-pipe.service: a setting obeyed: a probe of the case showed it in force;  (`P4-PIPE-3/inv-P4-PIPE-3-before/compare-und-reference.tsv`)
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
- `REPRO-2a` (REPRO) **fail** [-]: x: the application did not report success: confos apply exited 1 before a reboot — `REPRO-2a/REPRO-2a.outcome.txt`
- `UND:REPRO-2a-apply-1` (UND) **undecided** [D1, D3, D6, D4, D5]: met against the reference installation (easier reading: pass, {}), not under the derivation from the declaration alone (harder reading: fail); D1, D3–D6 — `REPRO-2a/UND:REPRO-2a-apply-1.outcome.txt`
- `REPRO-2b` (REPRO) **unobserved** [-]: unobserved: not expressible: account tcpdump groups=- shell=/usr/sbin/nologin home=/nonexistent: not expressible: the `account` kind requires the numeric UID and GID — `REPRO-2b/REPRO-2b.outcome.txt`
