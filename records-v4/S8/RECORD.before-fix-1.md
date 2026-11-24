STEP 8: updates ?; development ?; game ?; network ?; the step ?

# S8 — supplement 1, step 8: the second party's single performance of the four histories

Performed 2026-11-23, 18:36–19:04 UTC, by the second party (it did not prepare the histories). Reviewed by RV-S8-O.
Criteria: `SUP1/step-8.md` (unchanged); sentences: `SUP1/SENTENCES.md` / `SENTENCES.md`. Paths below without a
prefix are under `S8/`. Log with the expectations written before each run: `LOG.md`. Questions: `QUESTIONS.md`.

## Before the first history

- Checksums named by (not published: orchestration or scratch) and at the top of `check-inputs-v4/supplement-1/step-8-cases/B2/CASES-8.md` all match: CASES-8.md `72f8a2f2…`,
  OBSERVE-8.md `29b0c7f2…`, image `1b581030…ca980eca`, initial declaration `2e6946a8…cd79b4a`; the public `main` is the
  gate commit `7cda0636…`; all 41 committed files equal the local and server copies; 198 sealed files, 0 mismatches
  (`raw/checksums/`). Publication receipt written on the server after that check (`raw/h1/publication.json`).
- Each history ran once, sequentially, with the exact `systemd-run … python3 cases-8/run.py hN --publication …`
  command of CASES-8.md, on a fresh guest `s8-second-hN` (`raw/hN-launch.txt`). Every service ended
  `ActiveState=inactive, ExecMainStatus=0` (`raw/hN/hN-final-service-status.txt`); the controller exit is not an
  outcome. Every guest was destroyed, base image hash unchanged, no guest left (`raw/hN/cleanup.json`,
  `raw/hN/remaining-guests.stdout`). No history was repeated; nothing was repaired.

## How the observations were read

The committed collector's raw JSON for every point is kept compressed ((not published: direct evidence at least 2 MB), (not published: direct evidence at least 2 MB),
(not published: direct evidence at least 2 MB), (not published: direct evidence at least 2 MB) → `disconnected_observation`). The collector computes no
verdict; I read each with offline tools kept in `tools/` (`analyze.py`, `decldiff.py`, `units.py`, `actions.py`,
`h4actions.py`) and saved the summaries in `raw/analysis/`. Per point:
(a) every census entry without an own claim, split into entries changed after the guest was created and unchanged
image entries; installed packages without an own line; accounts/groups without a row; enabled units without a unit
row (their enablement links checked against own claims, `*.units.json`); (b) every machine line and every filesystem
path/account row compared field by field with the collector's native readback; (c) the cumulative action table
(`raw/analysis/actions-POINT.json`).
“Declaration entries” = machine lines + filesystem path entries + filesystem account rows of the declaration in force.
The initial declaration has 2010 (559 + 1358 + 93).

Facts the committed query cannot establish, present at every point and **not** caused by any history (named once):
U1 compiled AppArmor cache `/var/cache/apparmor/979b3ac6.0/{stand-build,stand-format-parser}` rewritten at every boot —
whether its bytes encode exactly the recorded policy sources; U2 the `boot` line (host order/firmware) and the prose
`code-boundary` line are unproved obligations of P2 (the reader says so); U3 ~3,170 directories and 2,913 unchanged
non-directory image entries without an own claim (dpkg database, AppArmor cache of 100 profiles, two Python bytecode
files, …), whose receipt/derivation provenance is not established; U4 the collector's stated limits (`limits` field).
Runtime entries under `/run` (S8.2-5), logs/journals/state files (program records, question 4 of Section 8.2) and the declaration
machinery's own generations/receipts were classified as not separately required. 31,240+ entries under
`/var/lib/stand/code-root` have the same bytes as their declared originals (`code_root_copies`). Collector defect:
after any application that rewrote the machine declaration without `base-files.json`, its machine-authority step
raised `FileNotFoundError`; the generation identity was recomputed offline from the saved bytes and equals the success
report at every such point (`authority.machine_identity_matches_receipt_offline`).

## History 1 — updates (outcome ?)

Commands (root): `h1/update-1.sh` (`apt-get upgrade --stand-catalog ed`), `systemctl reboot`, `h1/update-2.sh`
(fetch ed 1.22.5-1, `/usr/bin/dpkg --install`), `systemctl reboot`; observations with `check-inputs-v4/supplement-1/step-8-cases/B2/cases-8/observe.py` (stdin sha256
`3aa84d89…`) after each restart and at the end (`raw/h1/commands.json`).

| Point | (a) in force, not recorded | (b) lines not fulfilled | (c) actions not done | Evidence |
|---|---|---|---|---|
| after restart 1 (boot `21b47d79`) | none caused by the history; U1–U4 | 0 of 560 machine lines, 0 of 1362 fs paths, 0 of 93 account rows; U2 | update-2, restart-2 not yet reached | `raw/analysis/h1-after-restart-1.summary.json`, `actions-h1-after-restart-1.json` |
| after restart 2 (boot `4d7f41f8`) | same | same (0/560, 0/1363, 0/93) | none | `h1-after-restart-2.summary.json`, `actions-h1-after-restart-2.json` |
| end | same | same | none | `h1-end.summary.json`, `actions-h1-end.json` |

- Update 1: exit 0, `SUCCESS 6dc280d6…`, ed 1.21.1-1 (`raw/h1/h1-update-1.stdout`); restart 1 changed boot ID
  (`raw/h1/restart-1.json`).
- Update 2: exit 0, read back `ed 1.22.5-1 installed` immediately, **no success report** (`raw/h1/h1-update-2.stdout`);
  the machine declaration in force is the same generation `6dc280d6…` (report 18:40:41Z) before and after
  (`raw/analysis/h1-diff-r1-to-r2.json`: no machine change; line `package:ed` requires 1.21.1-1). After restart 2 the
  system's replay restored ed 1.21.1-1 (`raw/h1/h1-after-restart-2-package.stdout`). The downloaded `.deb` in `/tmp` was
  recorded (`tmp:/ed_1.22.5-1_amd64.deb`).
- Entries left by update 2 at the later points (`tools/residual.py` on the summaries): dpkg database files, man cache,
  dpkg/alternatives logs. The executable `/var/lib/dpkg/info/ed.{postinst,prerm}` and `dpkg/alternatives/editor` were
  only rewritten: same bytes as on the image and as in the control archives of both committed ed packages, new mtime
  (`raw/analysis/h1-ed-maintainer-scripts.json`); dpkg maintainer scripts are unclaimed on the whole image (U3).
- Declaration entries: 2010 before → 2016 after (machine 559→560: `system:base-state` added, `base` and `package:ed`
  changed; tmp 7→10, vartmp 4→6) (`h1-diff-initial-to-r1.json`, `h1-end.summary.json`).
- **Observation against:** a built-in tool with superuser privileges (`dpkg`, “the system package manager”, S8.1-4;
  “an installer” is a built-in tool, S8.1-7; so not breaking, S8.1-15) changed an installed package past the declaration (P4); between update 2
  and restart 2 the package was in force unrecorded (P1) and line `package:ed` unfulfilled (P2). Seen by the history's
  own readback; no committed observation point lies in that interval (question 2). The second update did not persist
  after restart (ordinary work, question 3).
- No written argument exists, from Section 8 alone, that any system having P1, P2 and P4 would fail this history; such a
  system's installer adds the change to the declaration (S8.3-7). Absent → testbed defect → **?**.

## History 2 — development (outcome ?)

Command (ordinary shell): `h2/history.sh` (stdin `b4c08e80…`): 3 fetches, 3 one-line edits, 6 source admissions/builds/
result admissions, 6 runs; observation at the end.

| Point | (a) | (b) | (c) | Evidence |
|---|---|---|---|---|
| end (boot `a1988efd`) | none caused by the history; U1–U4 | 0 of 561 machine lines, 0 of 1373 fs paths, 0 of 93 account rows; U2 | all 18 done | `raw/analysis/h2-end.summary.json`, `h2-end.units.json`, `actions-h2-end.json` |

- All three fetches checksum-verified, three `ONE_SOURCE_LINE_CHANGED`, six `OUTPUT_VERIFIED`, twelve `SUCCESS`
  applications, `H2_COMMANDS_COMPLETE` (`raw/h2/h2-development.stdout`); declaration in force `cf6065f6…` (18:54:37Z).
- Declaration entries: 2010 → 2027 (machine +2: `source:h2-hello`, `import:h2-hello-built`; home 4→15: `step8-h2/`,
  `hello.c`, `source.json`, six outputs, `h2-hello.built{,.json}`; tmp/vartmp +2 each) (`h2-diff-initial-to-end.json`).
- Unrecorded new entries were directories `/opt/stand/pkgs/h2-hello*` created by the system for recorded lines,
  runtime, logs and machinery. No observation against.
- Outcome depends on whether the unresolved facts U1–U4 leave “nothing counts against” established (question 1);
  under the step-8 rule for two readings → **?**.

## History 3 — game (outcome ?; not performable)

Commands: root `h3/prerequisites.sh` (stdin `fb41a0aa…`): 15 checksum-verified packages, one `/usr/bin/dpkg --install`,
readback; ordinary `h3/history.sh` (stdin `927812e2…`).

| Point | (a) | (b) | (c) | Evidence |
|---|---|---|---|---|
| end (boot `72737801`) | 15 installed packages without any line (bc, bsdmainutils, bzip2, distro-info, jq, lib32gcc-s1, lib32stdc++6, libc6-i386, libevent-core-2.1-7t64, libjq1, libonig5, ncal, pigz, tmux, unzip) and their files, e.g. `/usr/bin/jq`, `/usr/bin/tmux`, `/usr/lib32/libc.so.6`; U1–U4 | line `base`: `/etc/ld.so.cache` and `/etc/shells` sha256 differ (rewritten by dpkg triggers; the `/etc` filesystem declaration recorded the new bytes); other 558 machine lines, 1415 fs paths, 93 account rows: 0; U2 | game install and the 7 later actions not done | (not published: direct evidence at least 2 MB), `h3-diff-initial-to-end.json`, `actions-h3-end.json` |

- Prerequisites: exit 0, all 15 `installed` (`raw/h3/h3-prerequisites.stdout`); machine declaration unchanged — still the
  image generation `0e9590be…` (17:39:52Z).
- Launcher fetched, checksum OK, `bash linuxgsm.sh wetserver` done; `bash wetserver auto-install` failed:
  `/usr/bin/jq: Permission denied`, `[ FAIL ] Installing wetserver: Failed to resolve permissions issues`; the game
  archive was never downloaded; `ACTION_FAILED h3 line=38` (`raw/h3/h3-launcher.stdout`, `.stderr`). History not
  performable with the committed launcher.
- Declaration entries: 2010 → 2067 (machine unchanged; etc +1 `ld.so.conf.d/zz_i386-biarch-compat.conf`; home +36
  launcher files; tmp +18 incl. the 15 `.deb`; vartmp +2).
- **Observations against:** root `dpkg` installed 15 packages past the declaration (P1, P4); line `base` not fulfilled
  for two paths (P2); installing and starting the game could not be performed (A.4.3). No argument from the
  definitions alone that any P1/P2/P4 system fails this history; not performable → **?**.

## History 4 — loss of network (outcome ?; not performable after the first interruption)

Commands: artifact check (exit 0); `cut-action.py … install 'stand-pkg install /usr/local/share/stand/dev/worker-1.json'`
with QMP `set_link net0 false/true`; then the restored observation, retry, prefix, end — as fixed in `run.py`.

| Point | (a) | (b) | (c) | Evidence |
|---|---|---|---|---|
| install, disconnected (boot `904bdb6d`) | none caused by the history (empty `/opt/stand/pkgs/dev-worker/bin` directories left); U1–U4 | `port:udp:1` (`10.0.2.15%ens3:68`, listening) not listening; 558 other machine lines 0; `/etc` declaration changed three times during collection (`declaration_stable=false`), so 4 `/etc` timestamp differences are not a stable reading | install not done (exit 1) | (not published: direct evidence at least 2 MB), `raw/analysis/h4-install-disconnected.summary.json`, `actions-h4-install-disconnected.json` |
| restored | unavailable: session exit 255 | unavailable | retry not yet reached | `raw/h4/h4-install-restored.*`, `actions-h4-install-restored.json` |
| after restored retry | unavailable (255) | unavailable | retry unavailable (255) | `raw/h4/install-restored-retry.*`, `actions-h4-install-after-restored-retry.json` |
| end | unavailable (255) | unavailable | worker run, development prefix/cut/suffix not done | `raw/h4/h4-end.*`, `actions-h4-end.json` |

- Cut valid: installer process active at carrier 0 (`valid_cut: true`, `raw/h4/install/host-events.json`). Installer
  output: `FAILED recovery incomplete: readback mismatch: port:udp:1; restoration mismatch: port:udp:1`.
- During and after the disconnected observation `/run/stand-ready` was absent and `pending.json` held candidate
  `8824e9eb…` (`identity_before`/`identity_after`). The image requires that file for every login
  (`B2/build/install-transactions.py:27`, `account requisite pam_exec.so quiet /usr/bin/test -f /run/stand-ready` in
  `/etc/pam.d/common-account`; `B2/build/transactions.py` removes it in recovery). The link was restored at 19:03:39Z and
  the buffered output arrived over the existing session (19:03:41Z); every new session 19:03:41–19:03:42Z exited 255 with
  empty stderr. Established: gate file absent; new sessions refused. Not established by output: that the gate, and not
  something else, refused them (no further probe; the history is not repeated).
- Declaration entries: 2010 → 2014 at the disconnected point (tmp +2, vartmp +2); after the history: unavailable.
- **Observations against:** line `port:udp:1` unfulfilled after the last completed application (P2); the installation
  could not be performed after the network was restored, nor any later action (A.4.3, the step-8 network rule). No
  argument from the definitions alone that any P1/P2/P4 system fails this history (an open port is not a separate object, S8.2-5, and
  “may also be recorded”, S8.2-19); history not performable → **?**.

## Breaking, counterexamples, lists

- Breaking: none. Root was used for the built-in installer (`dpkg`), the service manager (`systemctl reboot`), fetching
  files to `/tmp` and read-only queries.
- Counterexample (an object the text of 8.1–8.2 cannot decide): none found; undecided cases above are FACT_UNKNOWN.
- Gaps were not put into either list of Supplement 1 (`step-2.md` question still open).

## Comparison with the expected result of `SUP1/step-8.md`

| Expected | Result |
|---|---|
| In the performable histories nothing in force found unrecorded and every line fulfilled | **not met**: history 1 — ed 1.22.5-1 in force unrecorded after update 2 (own readback); history 2 — met (2 lines unproved, U2) |
| The game history not performable | **met** |
| The declaration grows with every file a history saves | **not met**: files saved in the mediated trees were recorded (h1, h2, h3), but the files written by `dpkg` under `/usr` in histories 1 and 3 were not; history 4 not assessable |
