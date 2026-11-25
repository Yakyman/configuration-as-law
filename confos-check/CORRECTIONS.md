# Corrections of the checking programs

The record of every repair of the programs of the check (`inventory`, `derive`, `compare`, `run`, `adapter.py`,
`casedefs.py`, `decide.tsv`, `lib/`) found by development runs, with the tag that the programs and `CASES.md` use for
it (plan, Section 9.5: “each repair is recorded and published with the outcomes”). Times are UTC, 2026-11-24.
Development runs are not observations of the check; their rows are named only as the evidence that found a defect.

Each entry: when, what was wrong, what the program does now, and the test that shows it. Self-test commands are those
of `READY.md`.

## [n2-1] P1 counted as unrecorded what S8.2-16 records — repaired 11:45–12:26, tested 12:55

- Wrong: `compare` called `UNRECORDED` every object that `derive` did not produce, and `run` gave P1 `fail` on any
  `UNRECORDED`. On a fresh installation with nothing done (dev-11, P1-0) 82,712 objects of the base, the packages and
  the accounts were unrecorded, so every P1 row failed on any system whatever.
- Now: for every declaration in force, `run` builds a second clean installation from the published source and the
  same declaration (`Run.reference`, `runs/NAME/_reference/`), boots it until the report of success, takes its
  inventory from outside and deletes it. `compare --reference` writes `compare-p1.tsv`: an object of the machine
  equal to the object of that installation is recorded by the lines (plan, Section 9.3); every other object is
  decided by the four questions of S8.2-6 ([n3-A]). Fields that are random by construction (UUIDs, GUIDs) are
  compared by pattern rules `~REGEX`.
- Test: `selftest/specificity/test.sh` (no P1 row of a correct state is `fail`), PASS 12:55 on release 0.26; the
  re-decision of dev-11 from its stored inventories (`tools/redecide.py`): unrecorded objects of the fresh installation
  82,712 → 1.

## [n2-2] P2 failed on files that account and setting lines determine — repaired 11:45–12:26, tested 12:30

- Wrong: `derive` gave `/etc/group`, `/etc/hostname`, `/etc/hosts`, `/etc/passwd`, `/etc/shadow` the bytes of the
  base; the machine held them as the `account` and `setting hostname` lines require, so every P2 row failed on them.
- Now: `derive` marks the files whose content a line of another kind determines as underived (`line_determined`);
  P2 compares each line with the state that line requires (the account with its fields, the hostname, …).
- Test: `selftest/derive/run.sh` → `SELFTEST derive: PASS` 12:30 on 0.26, 14:27 on 0.29.

## [n2-3] No object was ever decided as material — repaired 11:45–12:26, tested 12:55

- Wrong: `decide.tsv` had the classes `runtime` and `program-record` only; a directory made by `mkdir`, a downloaded
  archive and a text file of the person made P4 rows fail (dev-11: P4-C3-2, P4-C7-1, P4-C11-3).
- Now: `casedefs.MADE` names per case what the person creates or brings; `compare --made` takes such objects through
  the four questions of S8.2-6; one that is not a package, not code that a route executes and not a setting in force
  is material (S8.2-15) and counts against neither P1 nor P4.
- Test: `selftest/specificity/test.sh` (`mkdir ~/p`, a saved text document, a downloaded archive of sources: no row
  `fail`), PASS 12:55 on 0.26; dev-11 re-decided: P4-C3-2 and P4-C7-1 no longer fail.

## [n2-4] Saved code whose launch the system refuses was counted as code — repaired 11:45–12:26, tested 13:00

- Wrong: a saved file (`~/nvim.appimage`, `~/jq`) made its row `fail` although its launch was refused (exit 126).
- Now: `run` tries the direct routes of the file's form (`./F`, the loader, `bash F`, `source F`, `python3 F`, a unit
  or startup file that names it, …) and the data routes (`cat F | bash`, `bash -c "$(cat F)"`, …) separately
  (`ROUTES_SH`, `routes.tsv`); a direct route that executes makes the row `fail` (review decision R1); only a data
  route executing gives `undecided` (Q11); every route refused: the object is not code in force. Only interpreters
  that the file's form names count.
- Test: `selftest/run/form-routes.py` → `RESULT: PASS`; `selftest/specificity/test.sh`: P4-T-CODE is `fail` exactly
  when a direct route executes the saved file.

## [n2-5] A probe read a state the declaration itself gives — repaired 11:45–12:26, tested 12:55

- Wrong: P4-BT-5 failed on `sudo -l -U person` showing `(ALL) NOPASSWD: ALL`, a right the test declaration gives;
  both attempts had been refused.
- Now: every probe of a P4 case is taken once before the attempt too (`pre-probes.json`), and only a probe that
  changed counts; probes that would themselves perform the attempt are not taken before (`NOPRE_SELF`).
- Test: `selftest/specificity/test.sh` performs the two refused attempts of P4-BT-5: no row `fail`, PASS 12:55;
  dev-11 re-decided: P4-BT-5 no longer fails.

## [n2-6] A row met under one reading only was `fail` — repaired 11:45–12:26

- Wrong: rows were `fail` under the harder reading of D1–D6 alone.
- Now: for every question of `QUESTIONS.md` and `QUESTIONS-derive.md` that changes a row, the row is evaluated under
  both readings (`p4_decide`, `p2_outcome`, the Understanding rows against the reference installation of [n2-1] as the
  easier reading); met under both `pass`, neither `fail`, one only `undecided` with the question ID; the evidence
  file keeps the outcome and counts under each reading.
- Test: the re-decision of dev-11 and the rows of dev-12 and dev-13 (`undecided` rows carry the question ID and both
  counts in their evidence files); no separate self-test.

## [n2-7] Nothing showed that a correct state is left alone — added 11:45–12:26, first PASS 12:55

- Now: `selftest/specificity/test.sh` with `check.py`: on a clean installation of a release with the test
  declaration, ordinary objects of the person and two refused attempts make no row of P1, P2 or P4 `fail`, while the
  planted objects ([n3-A]) still make theirs `fail`.
- Test: the test itself; PASS 12:55 on 0.26, 15:27 on 0.29 (20 of 20 checks).

## [n3-A] An object that no rule names was counted as unrecorded — repaired 13:55–14:40, tested 14:51–15:27

- Wrong: in the writable area, an object that equalled neither the derivation nor the reference installation was
  `UNRECORDED` with an empty reason (dev-12, OW-4: 103 objects of the browser's profile and cache).
- Now: `compare --questions` asks the four questions of S8.2-6 in order for every such object: question 1 by the
  `store` rules of `decide.tsv` (package managers' stores), question 2 by the routes ([n2-4]), question 3 by the
  `carrier/...` rules and a probe that shows the carrier in force, otherwise S8.2-15 (not counted, written to the
  excluded list with that reason). An `UNRECORDED` line always carries the question and the evidence. The stored,
  read-only system part is not changed by this: there everything equal to neither stays `UNRECORDED`. The earlier
  rules that only named the working state of one program were removed.
- Test: `selftest/specificity/test.sh` PASS 15:27 on 0.29: a module planted in the pip store fails by question 1, a
  saved script that a direct route executes fails, a file of a recorded program in its working folder under the home
  directory does not fail; `selftest/inventory/test.sh` step 4 on a stock image: a unit that the person put in force
  is reported by question 3 (RESULT: PASS 14:44 and 15:15). The offline re-comparison of dev-12 OW-4: 103
  `UNRECORDED` → 0.

## [n3-B] A row whose deciding observation was not made was `fail` — repaired 13:55–14:40, tested 14:51–15:27

- Wrong: rows failed on “code in form … and no route was tried”, which says nothing about the system.
- Now: `compare` gives such objects the verdicts `UNROUTED` and `UNPROBED`; `run` tries the routes of
  `compare-routes-wanted.txt` while the machine runs and compares again; a row whose only objects counting against it
  still need a route or probe that was not taken is `unobserved` with that reason.
- Test: `selftest/specificity/test.sh` PASS 15:27 on 0.29; in dev-13 every `unobserved` row names the missing
  observation in its evidence file.

## [n3-C] The published set — 14:40

- Not a change of behaviour: `PUBLISH.txt` lists the files of the published check; working files moved out of it;
  `local.env.example` with invented values; the self-tests use invented accounts and homes.
- Test: `python3 -I ../bin/scan-public.py <copy of the published set> --all` — no hit of a blocking category.

## [n3-D] Are the pinned components the latest on the day of the commit — by 14:40

- Now: `tools/lock-check.py` compares the lock of a release with the newest archive states of the day.
- Test: its output `ready/lock-check-0.28.tsv`, `ready/lock-check-0.29.tsv` (113 components: 108 the same, 4 the
  implementation's own, 1 newer: `linux-image-amd64` 6.12.117-1 → 6.12.118-1).

## [f2] `derive` stopped on a kind of line it did not know — repaired 15:36–15:40, tested 16:08 (0.32)

- Wrong: dev-13 OW-8 rows were `unobserved` with “derive did not exit 0”: `derive: ERROR … unknown kind 'linuxgsm'`
  (a kind of line added by revision 18 of the implementation's declaration format, used only by OW-8).
- Now: `derive` handles `linuxgsm USER PATH RELEASE SHA256 BUNDLE` (the bundle checksum is checked; a `dir` object
  PATH with underived owner and mode, an underived `PATH/**`; FORMATS.md).
- Test: `selftest/derive/run.sh` step 8 has a `linuxgsm` line → `SELFTEST derive: PASS`; the repaired `derive` gives
  byte-identical `derived.jsonl` for dev-13 OW-1 and OW-4 (`cmp`), so no other row changes. Second freeze.

## [f3] Rows written after a stop signal carried the damage of the stop — repaired 15:54–15:56

- Wrong: when dev-13 was stopped (15:54:12), rows decided while its machines and programs were being killed came
  out `fail` or `unobserved` with that damage as the reason (12 rows, among them OW-9 and P2-ADD-1 `fail`).
- Now: after a stop signal every row that `run` writes is `unobserved` with the reason “the run was stopped (signal
  N at T) before this row was decided; the observation was not completed”, and the outcome the interrupted steps
  gave is kept in the evidence, not used (`Ctx.row`). Third freeze.
- Test: `selftest/run/check-stop-row.py` (step 3b of `selftest/run/selftest.sh`) calls `Ctx.row` of the frozen `run`
  with a stop signal noted and without: `unobserved` naming the stop, and the outcome kept, respectively; against the
  `run` of the first freeze it fails (`CHECK row-after-stop-is-unobserved FAIL outcome fail`), against the third and
  fourth it passes. The live part of step 3b stops a run on a stock image during P4-PIPE-1 (a case that runs guest
  commands there) and checks that the signal is noted, that every row written after it is `unobserved`, and that no
  machine or disk of the stopped run is left. A live stop cannot be made to write a row after the signal on purpose:
  the runner cleans up and exits at once (16:15: none was written); in dev-13 rows after the signal arose because
  cleaning up several machines took long.
- Repairs of this test (it is not one of the frozen programs): its first form (15:56) stopped OW-1, which ends at
  once on the stock image, so the signal never reached a case in progress; from 16:09 it stops P4-PIPE-1 and fails
  if the runner ends before the signal; from 16:17 the in-process check was added and a live stop with no row
  after the signal is reported, not failed.

## [c1] References to the organisation of the work removed from comments and text — 16:00–16:05

- Not a change of behaviour: comments, documentation text and message strings that named internal notes or work
  sessions now carry the tags of this file or the date and time. Fourth freeze.
- Test: `tools/text-only-diff.py OLD NEW` on copies of the published set before and after: for every Python file the token streams without comments
  are equal except for string tokens, and every other changed line is a comment or documentation
  (`READY.md` gives the command and its output); the quick self-tests rerun on the fourth freeze.

## Repairs before the first freeze, found by the development runs

These were found and repaired while the programs were written, before the programs were first frozen (14:45); each
was followed by the self-tests then in force.

- 12:58 `inventory` wrote names that are not UTF-8 as `\xHH` escapes (found by the specificity test: the stored level
  could not be written). Test: `selftest/inventory/test.sh` PASS 12:58.
- By 13:05 `run`: rows of test-only cases were not written to `results.tsv`; the probes before an attempt ran before an
  `APPLY` step; interpreters not named by a file's form counted as executing it; the container-store rule covered the
  image's own files. Test: `selftest/specificity/test.sh` PASS 13:05.
- After 13:05 `adapter.py`: the content file of a `compile-from` line was named `files/hello.c`, the name of the test
  declaration's own source (dev-12 OW-7); now `files/compile_<target>.c`. Test: dev-12-ow7, OW-7 `pass`.
- 14:16 `inventory`: a variable renamed for the published set was left under its old name at one place (NameError);
  `derive` kept a package's hard link where a component ships a symlink for the same path: stored kinds are merged per
  path, `Replaces` decides. Test: `selftest/inventory/test.sh` PASS 14:44; `selftest/derive/run.sh` PASS 14:27.
- 14:29 `compare`: question 3 is asked also while question 2 is open or not observed; routes that only a data route
  offers do not count for an object that a rule decides (Q12). Test: `selftest/specificity/test.sh` PASS 15:27.

## [r1] Tools of the report of complete run 1 — 2026-11-24 20:00–20:10 UTC (no program of the check changed)

- `tools/failing-list.py`: its first line called every run a development run; for a run named `run-N` it now says
  “Complete run `run-N` of the check”. Nothing else changed. It reads only what a run wrote.
- `tools/run-report.py` (new): the body of `RUN-1.md`, i.e. the counts by part and outcome, one line per row that is not
  `pass`, and the `QUESTION` objects with their kind and path. It reads only what a run wrote and uses
  `tools/ready-summary.py`.
- Found by complete run 1 in the frozen `run`, NOT repaired (the order of the run): the routes hang on a file that a
  route runs and that leaves a background process (P4-C9-1, P4-C9-2), and the REPRO-2 account lines state a home that
  the implementation refuses (REPRO-2a). See `RUN-1.md`.

## [f5] Three defects found by complete run 1 — repaired 2026-11-24 20:12–20:20 UTC, fifth freeze (`run` only)

Each repair has a test that fails on the fourth freeze and passes on the fifth (commands below; both outputs of
20:20 UTC are in `READY.md`, section 2). They are step 5 of the runner self-test (`selftest/run/selftest.sh`).

- **[f5-a] REPRO-2: account lines that the implementation refuses.** Wrong: `run` (`fam_repro2`) declared the two
  package accounts with `home=/nonexistent`; the implementation documents homes immediately below `/home`
  (`build/DECLARATION.md`), and `confos apply` refused the text in complete run 1 (`REPRO-2a` `fail`, `RUN-1.md`). The
  value had been a home below `/home` until the cleaning of home paths before publication. Now: the lines state no
  `home=`, and `adapter.py` gives the documented default `/home/NAME`. Test: `selftest/run/check-repro2-accounts.py
  RUN RELEASE-DIR` calls `fam_repro2` with stubs that only record the lines it adds, renders them with `adapter.py`
  and gives them to `validate_accounts` of the release's own `assemble.py` (fourth freeze: “account home must be an
  immediate child of /home”; fifth: accepted).
- **[f5-b] The routes never ended when a route started a background process.** Wrong: the routes script captured
  the standard error of each route with `e=$(… 2>&1 >/dev/null)`; a file that a route ran started a background
  process (`sleep 86413 &` in P4-C9-1, `subprocess.Popen(…)` in P4-C9-2), which kept that pipe open, so the script
  never ended, the call of the routes timed out over SSH and the file got no route line (`UNROUTED`: six rows
  `unobserved` in complete run 1). Now: the standard error of each route goes to a file of its own in a temporary
  folder of the guest (removed when the script ends); the route is over when its own program has ended or `timeout`
  ended it, and its line is written with its exit status. What the route left running stays running, as before.
  Test: `selftest/run/check-routes-background.sh RUN` gives the routes script of RUN the two files of the forms of
  P4-C9-1 and P4-C9-2 under `timeout 120` (fourth freeze: ended by the timeout, no line for `cat-pipe-bash` or
  `python3-exec`; fifth: ends at once with every route line), and stops the background processes afterwards.
- **[f5-c] The inventory before the restart of P4-PIPE was a row.** Wrong: the P1 and Understanding comparisons of
  `P4-PIPE-n-before` were rows, `undecided` by Q4, and the reason text of the Understanding row named D1–D6 instead
  of Q4. The review decided Q4 (`REVIEW.md`, R6: the case is judged after the restart; the rows before it are
  records). Now: `Ctx.row` writes them as `P1:P4-PIPE-n-before.record.txt` and `UND:P4-PIPE-n-before.record.txt` in
  the evidence, with what the comparison gave and R6, and writes no row; the inventory and both comparisons are still
  made. Every other row is unchanged. Test: `selftest/run/check-before-record.py RUN` (fourth freeze: the two rows are
  written; fifth: two records, no row, the rows after the restart and of other cases unchanged).

Under R3–R5 nothing else changed: the rows keep their outcome and question; the decisions of the review are applied when the outcomes are assigned.
Fifth freeze: `run/src11` (`run` `c5f856085f5549bbd9ed6bef18f22e310b15a596db906d0baee8c4bb498e324e`; the other eleven
program files are byte-identical to the fourth freeze).

## [f6] New cases from the successes of the search — added 2026-11-25 00:45–01:43 UTC, sixth freeze

Plan, Section 9.5: “Each success becomes a new case, committed before the next complete run … Cases are only added in
this way, never removed or weakened.” No case was removed or changed.

- **Added: 19 cases of P4, `P4-S-*` (`CASES.md`, section P4-S).** 14 are the direct routes of the search that ran on
  release 0.32 (`search/routes-0.32.tsv`, group `direct`, result `RAN`), 3 are the attempts 202, 234 and 241 of
  `search/attempts-0.32.tsv`, 2 are the builder's finding that saved Basic macro libraries run
  (`build/IMPOSSIBLE.md`). Attempt 256 has no case: its recorded output is the refusal. The cases are written by
  `tools/make-search-cases.py` into `casedefs_search.py`, which `casedefs.py` reads; the attempt of a route case is
  the route's own script, its probe is the condition of that script's `RESULT RAN` line. Test: the development runs
  `dev-16-old` (the route cases on 0.32, where each route ran, and the macro cases on 0.52, where the builder says
  they run: every case must be `fail`) and `dev-16-new` (all 19 on 0.52): `dev-16-old` on 0.32 (00:53–01:19 UTC): 17
  of 17 route cases `fail`, each by its probe, which did not hold before the attempt; the two macro cases on 0.52
  are `fail` by both probes (in `dev-16-new`: their separate run `dev-16-old-lo` on the same release was stopped as
  a twin and removed); `dev-16-new` on 0.52 (00:53–01:37 UTC): P4-S-089, -090, -107, -108 `pass`; P4-S-054, -056,
  -111, -160, -161, -162, -166, -202, -234, -241 `undecided` (Q11, Q12, S8.3-7); P4-S-LO-1, -LO-2 `fail` by their
  probes; P4-S-135, -136, -167 `fail` by the process of the recorded mpv that remains after the refused route and
  whose executable root cannot read (`[exe-unreadable]`, `REQUESTS.md` entry 15). Also
  `selftest/run/check-search-cases.sh` (the cases are the program's output; the rows are in `CASES.md`; `run --list`
  equals `CASES.md`): `RESULT: PASS`.
- **The cases beyond the plan** (not part of `CASES.md` or of a complete run): `X-REC-GROUP` and `X-REC-MODULE` are
  performed from release 0.50, where `build/CHOICES.md` names `groupadd` and `modprobe` as recording.
Sixth freeze: `run/src13` (`casedefs.py` `8e153000e03d9e78ff57fd72e9015ebb2ed1d5eb0289747f05ae0ee687693bf5`, new
`casedefs_search.py` `59f41c31d2582e9b3d42cdcf42c516e5a57195312ed6e0868edb019b3e084298`; the other eleven program files
are byte-identical to the fifth freeze). No row of complete run 2 is `fail` or `unobserved` because of a program of
the case party (`RUN-2.md`), so nothing was repaired.

## [f7] A process whose executable lies in another mount namespace — repaired 2026-11-25 04:24–04:41 UTC, seventh freeze

Found by the development run `dev-18` (P4-S-135, P4-S-136, P4-S-167 on release 0.55 from the sixth freeze,
2026-11-25 04:06–04:14 UTC): all nine rows `fail` by one object, `UNRECORDED process /app/bin/mpv  creator
/app/bin/mpv not in the inventory`. On 0.55 root's `readlink /proc/PID/exe` answers for the process of the recorded
Flatpak application, and the path it prints, `/app/bin/mpv`, is one of the application's own mount namespace.
`inventory` knew a process only by that path, and `compare` placed a process only by looking that path up among the
stored paths of the machine. The file the process executes was not read. The defect went both ways: a process in
another mount namespace whose path there equals a stored path of the machine was placed by that path, whatever file
it executed.

What decides whether a process is past the declaration is the file it executes, not the name that file has in some
namespace. The repair:

- **`inventory`** records for every process, read as root, the SHA-256 of the file it executes, read through
  `/proc/PID/root` and the path that `readlink /proc/PID/exe` prints (`value.exe`, `value.exe_sha256`). When that
  path no longer leads to the file — the process changed its root after it started, as the sandbox's own `bwrap`
  process does (seen at 04:38 UTC in the first development run after the repair, `dev-18-f7`: `/proc/435/root/usr/bin/
  bwrap: No such file or directory`), or the file was deleted — the file is read through `/proc/PID/exe` itself;
  `value.exe_read` says which way (`root-path`, `exe-link`, `unreadable`). Processes with the same path whose files
  differ are separate objects, with the id `PATH#sha256=HEX` (`PATH#sha256=unreadable`); when all processes of a path
  execute the same file, the id stays `PATH`. Ports (`value.exe`) and the members of transient units name their
  processes by these ids.
- **`compare`** places a process (and a port or a transient unit through its processes) by that checksum: if the
  stored object at the path has the same content, by that object, as before; otherwise the path does not place it,
  and it is placed by a stored file with that content that follows from a line (decision `ok`); a process whose file
  is no stored object is past the declaration, as before. A process whose file cannot be read either way, or whose
  executable was deleted, is not placed by its path: like `[exe-unreadable]` (unchanged), it is accepted only if the
  reference installation has an equal object. A `service` line does not match a process at its path whose file
  differs from the stored file there, and gives `UNVERIFIED` (never `ok`) for a process whose file is not known, as it
  does for `[exe-unreadable]`. No other rule changed; nothing is taken from the implementation's own records.

The first form of the repair (04:24–04:27 UTC, tree `run/src15`) read only through `/proc/PID/root` and placed a
process whose file it could not read by its path; `dev-18-f7` on 0.55 passed with it, but the sandbox's inner `bwrap`
was placed by its path without its file having been read. The second form (04:38–04:41 UTC, `run/src16`) is the one
frozen. Every test below was made with the second form.

Tests, each failing on the sixth freeze where it should and passing after the repair:

- **Fixture test of `compare`** (new, `selftest/compare-process/test.sh`: `make.py` writes two inventories and a
  derivation, `check.py` decides): 13 checks — (a) the process `/app/bin/mpv` whose file is stored only under the
  application's tree is placed by the checksum; (b1) a process whose file is no stored object is reported; (b2) a
  process at a stored path (`/usr/bin/tail`) whose file differs is not placed by the path; an unreadable file and a
  deleted executable are not placed; a split object, a port and a login scope follow the placement of their
  processes; `service` lines: matched, MISSING, UNVERIFIED. Repaired: `RESULT: PASS`
  (`ready/f10/compare-process-after.txt`); sixth freeze (`test.sh <sixth-freeze compare>`): `RESULT: FAIL`, 9 of 13
  fail; (b1), the deleted executable, the process placed by its own path and the matched `service` line pass on both (`ready/f10/compare-process-sixth-freeze.txt`). The fixture
  test `selftest/compare-alias` still passes.
- **Planted-object test of `inventory`** (`selftest/inventory/test.sh`; `test.py` has four new planted processes
  on the stock Debian 13 image, each started by root in a private mount namespace): a stored file under a path that
  exists only in the namespace (must not be reported, its checksum equal to the stored `/usr/bin/sleep`); a file
  that is no stored object (must be reported); a changed file at the stored path `/usr/bin/tail` (must be
  reported); a process that changed its root after it started (read through `/proc/PID/exe`, placed). Repaired
  (04:42:37–04:48:28 UTC): `RESULT: PASS`, 21 checks (`ready/f10/planted-after.txt`); sixth freeze
  (`TEST_TAG=f6 INVENTORY_PROG=… COMPARE_PROG=… test.sh`, 04:48:30–04:54:13 UTC): `RESULT: FAIL`, the first,
  third and fourth of the new checks fail and one line is reported that was not planted; the second passes on both
  (`ready/f10/planted-sixth-freeze.txt`).
- **`dev-18` again on 0.55** (`dev-18-f7b`, P4-S-135, -136, -167 from `run/src16`, 04:42–04:51 UTC): no row
  `fail` or `unobserved` (P4-S-135 and -136: P4 `pass`, P1 `pass`, UND `undecided` by D1–D6; P4-S-167: P4, P1, UND
  `undecided`, Q12, `mpv.conf`). `/app/bin/mpv` is `placed by the checksum of the file it executes` with the
  application's file in the system generation; both `bwrap` processes are one object (`exe_read` `exe-link`,
  `root-path`) placed with `/usr/bin/bwrap`. On the sixth freeze the same nine rows were `fail` (`dev-18`).
- **The runner self-test** (`SELFTEST PASS`, 04:42:27–04:47:05 UTC) and **the specificity test on 0.55**
  (`SPECIFICITY TEST PASS`, 20 of 20, 04:42:22–04:55:45 UTC) from `run/src16`.

Seventh freeze: `run/src16` (`inventory` `93d47964b38098d550bb06496978282805390a3ec87384d1e3a4fcb0a5b5bcd7`,
`compare` `5da383452b8f2eaa3b2c8e0771b33fd5cf5218136c0a101d5c90a3c627b97087`; the other eleven program files are
byte-identical to the sixth freeze).
