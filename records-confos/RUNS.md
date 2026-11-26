# Complete runs of the check (plan, Sections 9.4 and 9.5; at most eight)

Development runs (dev-1 … dev-13b) are not counted and are not observations of the check.

| Run | Release | Source archive SHA256 | Commit of the inputs (repository of records) | Ordered (UTC) | Ended (UTC) | Programs | Departures | Result |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.32 | `61d290744606b4804b298217d340df5445cf276ea2b3ad69cc024e9457261001` | `425609f9fbf119dcf83a2c71d2a2912818a3be49`, 2026-11-24 16:27:01 | 2026-11-24 16:28 | 2026-11-24 19:56 | fourth freeze (`cases/READY.md` of 16:24) | one pinned component not the latest of the commit day: `linux-image-amd64` 6.12.117-1 against 6.12.118-1 | 388 rows; no row fails because of the implementation. Written: pass 184, undecided 194, unobserved 9, fail 1. After the review (R3–R6), by the text: OW 9 met and 2 not performed (real hardware); P1 124 met; P2 38 of 38; P4 70 met; REM 5 of 5; REPRO 1 met, 1 not expressible; UND 125 met (under the plan's Table 9: 1 met, 124 undecided, D1–D6). Seven rows are the case party's own defects (REPRO-2a `fail`; P4-C9-1, P4-C9-2 with their P1 and UND rows `unobserved`); six rows of the inventories before the restart are records (R6). Summary `cases/RUN-1.md`; table `bin/apply-review.py … --questions-met --instrument runs/run-1.instrument.txt`. Not in this run: S8.3-7 (no installer of 0.32 records), Wi-Fi and Bluetooth. The catalogue of the search on 0.32: 14 of 173 direct routes and 4 of 58 attempts ran (`search/REQUESTS.md` 1) — defects for the builder; a second complete run is needed. |

| 2 | 0.49 | `0f71e751f85a05fba1a8f8c726c823109a6dec6feaa1d27e210e5c729d9ef4db` | `9e99accd47d9e29dbaef4532842c7b6f015556c5`, 2026-11-24 23:02:07 | 2026-11-24 23:05 | 2026-11-25 01:34 (started 23:12) | fifth freeze (`cases/READY.md` of 22:55; `run` only changed: REPRO-2 account lines, routes that start a background process, the inventories before the restart as records) | (1) one pinned component not the latest of the commit day: `libzstd1` 1.5.7+dfsg-1 against 1.5.7+dfsg-1+deb13u1 (the kernel departure of run 1 is gone); (2) the successes of the search after run 1 (14 routes, attempts 202, 234, 241 on 0.32) were not yet cases of this run, against Section 9.5 — an omission of the party that directed the work; the catalogue performed them on 0.49 outside the run, all refused (`REVIEW.md`, after R8) | 385 rows. **Three rows fail because of the implementation, all in the ordinary work**: OW-2, OW-3 (the declaration of the first update does not build: the guarded `curl` is bound to one release — repaired in 0.52) and OW-8 (the apply of the game update runs out of space on the 12 GiB disk). Written: pass 184, undecided 195, fail 3, unobserved 3. After the review, by the text: OW 6 met, 3 fail, 2 not performed (real hardware); P1 127 of 127; P2 39 of 39; P4 72 of 72; REM 5 of 5; REPRO 2 met and REPRO-2b not expressible (an `account` line must name its numeric identifiers); UND 128 of 128. Under the plan: P4 64 met and 8 `?` (R8: the tool the person ran recorded the request as a line — the plan's own condition on a program written for the implementation); UND 1 met and 127 `?` (Table 9, D1–D6). No row is a defect of the case party's programs. The QUESTION objects: 72 entries, every direct route of their form refused; accepted only by data routes (R4), and two `times.json` of a browser by `node` (R5). First complete run in which the built-in tools record (S8.3-7): 8 rows of P4, each with its P1 row `pass`. Table: `bin/apply-review.py <copy> --questions-met --recorded runs/run-2.recorded.txt --rows`. The catalogue of the search on 0.49: none of 182 direct routes and none of 58 attempts ran (attempt 256 is a refusal, R7). A third complete run is needed: the three failing rows, and the cases that Section 9.5 adds. |

| 3 | 0.55 | `eb901118dc725dfbadfc46ee56069f4fa631903fdb08eec25bf763f6a12acdd1` | `39533ee3b74d845f5ff434688d0fbc4c37ff9fe9`, 2026-11-25 04:59:45 (the seventh freeze; before it `98a32e7406cdd1a57083b9bc140795b1102ca79f`, 04:02:54, the sixth freeze, followed by no run) | 2026-11-25 05:01 | 2026-11-25 07:14 (started 05:01) | seventh freeze (`cases/READY.md` of 04:56): the 19 new cases `P4-S-*` of the sixth freeze — 17 successes of the search on 0.32 and 2 for the saved macro libraries — and the correction [f7] of `inventory` and `compare` (a process is placed by the file it executes, `REVIEW.md` R9); for the first time the second set (`confos-check-extra/`: the cases beyond the plan), performed after the run | (1) one pinned component not the latest of the commit day: `libzstd1` 1.5.7+dfsg-1 against 1.5.7+dfsg-1+deb13u1, as in run 2 (lock check read at 06:31 UTC with every index 200; before that the two newest security states answered 404, `cases/QUESTIONS.md` Q15); (2) the commit of the sixth freeze (04:02:54) was followed by no complete run (paragraph below) | 458 rows, 124 cases. **No row fails.** Written: pass 212, undecided 243, unobserved 3, fail 0. After the review, by the text: OW 9 met (OW-2, OW-3, OW-8 of run 2 repaired) and 2 not performed (real hardware); P1 152 of 152; P2 43 of 43; P4 91 of 91; REM 5 of 5; REPRO 2 met and REPRO-2b not expressible; UND 153 of 153. Under the plan: P4 81 met and 10 `?` (R8; the 8 rows of run 2 and P4-BT-4 `groupadd`, P4-BT-12 `modprobe`, which record since 0.50); UND 1 met and 152 `?` (Table 9, D1–D6). No row is a defect of the case party's programs. The 19 new cases: 6 `pass`; 13 `undecided` as written — 3 by a refusing tool (R3), 10 by objects that only a typed command hands to an interpreter (R4) — all met after the review. The QUESTION objects: 102 entries in 9 groups (`bin/question-rows.py`), every direct route of their form refused; accepted only by data routes (R4), and two `times.json` of a browser also by `node` (R5). Read by hand: the ten recorded rows (the declaration differs by the request line only, the state queried before and after the tool is the same, the `P1:` row of each `pass`; `runs/run-3.recorded.txt`), and P4-S-LO-1 (the saved Basic library called by `macro:///Standard.Module1.Main`: exit 0, neither marker exists). Table: `bin/apply-review.py <copy> --questions-met --recorded runs/run-3.recorded.txt --rows`. |

Before run 3 the order asks for two checks on 0.55 that are not part of the run: the specificity test, and a
development run of the three cases that failed on 0.52 and 0.54 (P4-S-135, -136, -167). The run starts only if both
are clean (order 6 of the party that directed the work).

**04:19 UTC: run 3 was not started.** The specificity test passed (20 of 20), but `dev-18` failed in all 9 rows:
the frozen `inventory` and `compare` cannot place a process whose executable is reported with a path of another
mount namespace (`REVIEW.md` R9). The programs are being corrected (order 7, seventh freeze). The commit of the row
above (sixth freeze) was followed by no complete run; row 3 will name the commit of the seventh freeze, and this
paragraph stays as the record of why.

**The search after run 3 (plan, Section 9.5), on the same release 0.55.** The catalogue was performed once more
after the run had ended, 07:15–08:29 UTC, one stream (`search/REQUESTS.md`, entry 4; the performance before the run
is kept as `search/routes-0.55-before-run.tsv`, `attempts-0.55-before-run.tsv`, `evidence/0.55-before-run`): of 182
direct routes none ran; of 58 attempts the script counts one as `RAN`, attempt 256, whose recorded output is
`nsenter: reassociate to namespaces failed: Operation not permitted` — a refusal (`REVIEW.md`, R7; read by the
review after this performance too). The control ran, and 12 of 14 data routes ran (R4). Per channel the catalogue
has at least three attempts that are not fixed cases (C1 5, C2 4, C3 4, C4 4, C5 3, C6 4, C7 4, C8 6, C9 4, C10 3,
C11 4, built-in tools 10; attempts 202, 234 and 241 are cases since the sixth freeze and are not counted). The
attempts are those written on 2026-11-24; none was added for 0.49 or 0.55 (sixth paper, Table 4).
**With it the work ends: complete run 3 left no row failing, and the search on the same release found nothing.**
Under Section 9.4 the outcome of each part under the plan is `?` and not 1: the ordinary work on real hardware
(OW-10, OW-11) was not performed; 10 cases of P4 yield `?` by the plan's condition on a program written for the
implementation (R8), and 152 comparisons of Understanding by Table 9 (D1–D6). By the text of the hypothesis every
part is met in every row performed.

**The second set after run 3 (not observations of the check; `cases/RUN-3-EXTRA.md`).** On 0.55, 07:14–08:13 UTC,
from `confos-check-extra/` as committed: 17 cases of recording tools, X-WIFI and X-BT on simulated radios. Every one
of the 17 requests was recorded as exactly its line, nothing of it was in force before `confos apply`, the
application brought it in force, and the removal request likewise. Written: 14 `pass`; X-REC-SYSCTL and X-REC-MODULE
`fail` only through P2 rows of the frozen `inventory`, which takes no kernel parameter and no loaded module as a
setting in force (the probes show the values; X-REC-SYSCTL read by hand: 0, 0 after the request, 1 after the
application, 1 after the removal request, 0 after its application); X-REC-PODMAN `unobserved` by two files under
`/run/user/1000` whose routes the frozen program did not try. X-WIFI and X-BT `pass` (a new clean installation from
the same declaration was connected, and paired, with nothing typed); their P2 rows fail on kinds that the frozen
`inventory` does not observe. No row fails because of the implementation. Not built in 0.55 (`build/STATE.md`,
“Open after 0.55”): the recorders of `localectl set-locale`, `loginctl enable-linger` and `dpkg -i FILE.deb`, and a
pairing tool for Bluetooth (a pairing is recorded by lines written by hand); the second set names the first two
as cases not performed.

Published copies: from run 2 on, `confos/` holds the text files of the implementation only; the third-party inputs
(`interpreter-inputs/`) and the builder's working files (raw logs of drafts and helper scripts) are
listed in `confos/BINARIES.tsv` by checksum (`bin/publish-step4.py`, `WORKING`). The source archive of 0.49 contains
unpacked third-party dependencies and working files of the builder; none of that is published.

After each run: `python3 -I bin/apply-review.py <copy of runs/run-N> --rows` gives the rows as written, under the plan
after the review (R3, R4), and by the text of the hypothesis.
