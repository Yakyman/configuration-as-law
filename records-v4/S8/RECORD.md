STEP 8: updates ?; development ?; game ?; network ?; the step ?

# S8 — supplement 1, step 8: the second party's single performance of the four histories

Performed 2026-11-23, 18:36–19:04 UTC, by the second party (it did not prepare the histories); offline reading of the
saved observations until 19:09 UTC (last write of the first record, `QUESTIONS.md`, 19:09:08 UTC). Review RV-S8-O
(`REVIEW.md`) disagreed; this text is corrected by FX-S8-O-1 (`FIX-S8-O-1.md`) from the raw files that already existed;
the earlier text is `RECORD.before-fix-1.md`. No history was performed again and no raw file of the performance was
changed; the corrections' derived outputs are new files under `raw/fix-1/`, made with `tools/fix-1/`.
Criteria: `SUP1/step-8.md` (unchanged); sentences: `SUP1/SENTENCES.md` / `SENTENCES.md`. Paths below without a
prefix are under `S8/`. Log with the expectations written before each run: `LOG.md`. Questions: `QUESTIONS.md`.

## Before the first history

- Checksums named by (not published: orchestration or scratch) and at the top of `check-inputs-v4/supplement-1/step-8-cases/B2/CASES-8.md` all match: CASES-8.md `72f8a2f2…`,
  OBSERVE-8.md `29b0c7f2…`, image `1b581030…ca980eca`, initial declaration `2e6946a8…cd79b4a`; the public `main` is the
  gate commit `7cda0636…`; all 41 committed files equal the local and server copies; 198 sealed files, 0 mismatches
  (`raw/checksums/`). Publication receipt written on the server after that check (`raw/h1/publication.json`).
- Each history ran once, sequentially, on a fresh guest `s8-second-hN`. What the saved evidence shows: `raw/hN-launch.txt`
  holds the `sha256sum` output of the image, the declaration and the input seal, the UTC launch time and the
  `systemd-run` reply “Running as unit: s8-second-hN.service” (the unit name of the CASES-8.md command); `raw/hN/started.json`
  holds the history name and the seal; `raw/hN/commands.json` holds the exact argv, stdin SHA-256 and UTC boundaries of
  every guest session, beginning with `create`. The `systemd-run` command line itself was **not saved**; that the
  invocation was exactly the CASES-8.md command is therefore stated by the performer and corroborated by the unit names,
  `started.json` and `commands.json`, not shown by a saved argv. Every service ended
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

Facts the committed query cannot establish, present at every point (U1, U2, U4, U5 identical at every point; U3 counted
per point below):
U1 compiled AppArmor cache `/var/cache/apparmor/979b3ac6.0/{stand-build,stand-format-parser}` rewritten at every boot —
whether its bytes encode exactly the recorded policy sources; U2 the `boot` line (host order/firmware) and the prose
`code-boundary` line are unproved obligations of P2 (`p2_machine_unproved`); U3 image entries without an own claim and
not changed since the guest was created (dpkg database, AppArmor cache of 100 profiles, two Python bytecode files, …),
whose receipt/derivation provenance is not established; U4 the collector's stated limits (`limits` field); U5 the
failed native queries below. The U3 counts per point, from the summary fields `unclaimed_unchanged_by_kind.directory`
and the length of `unclaimed_unchanged_non_directories` (`raw/fix-1/u3-per-point.txt`):

| Point | directories | non-directories | note |
|---|---|---|---|
| h1 after restart 1 | 3,469 | 2,913 | |
| h1 after restart 2 | 3,441 | 2,876 | |
| h1 end | 3,441 | 2,876 | |
| h2 end | 3,471 | 2,912 | |
| h3 end | 6,719 | 33,996 | at this point the copies under `/var/lib/stand/code-root` fell on the unchanged side: 31,116 of the non-directories are under it, 2,880 are outside it |
| h4 install, disconnected | 3,474 | 2,917 | |

(The earlier “~3,170 directories” was `code_root_copies.no_declared_counterpart_directory`, a different quantity:
3,171 at the three h1 points, 3,174 at h2, 3,167 at h3 and h4.)

**U5 — native queries that failed at every point** (7 per point, identical argv/exit/stderr at all six collected points,
`query_failures` in each `raw/analysis/*.summary.json` (some matches not published: direct evidence at least 2 MB) (some matches not published: direct evidence at least 2 MB); extract `raw/fix-1/query-failures-and-mismatches.txt`). OBSERVE-8:
“a failed query is not an empty inventory”. What each leaves unseen is **not counted as recorded and not counted as
absent**:

| Failed query | Failure | Left unseen by native query |
|---|---|---|
| `bluetoothctl show` | `TimeoutExpired`, no exit | Bluetooth controller state (devices, S8.2-13) |
| `bluetoothctl devices` | `TimeoutExpired`, no exit | known/paired Bluetooth devices (devices, S8.2-13) |
| `busctl … call org.freedesktop.timedate1 … GetAll` | exit 1, `Name "org.freedesktop.timedate1" does not exist` | the effective time settings as the time service reports them (time, S8.2-13); the collector does not start inactive services; the time configuration files and `/etc/localtime` are in the file census |
| `busctl … call org.freedesktop.locale1 … GetAll` | exit 1, `Name "org.freedesktop.locale1" does not exist` | the effective language settings as the locale service reports them (language, S8.2-13); the language configuration files are in the file census |
| `systemctl show autovt@.service` | exit 1, “neither a valid invocation ID nor unit name” | the full effective `show` properties of the enabled template unit (services and their parameters, S8.2-13); its unit file is in the file census |
| `systemctl show getty@.service` | exit 1, same message | same, for `getty@.service` |
| `systemctl show sshd-unix-local@.service` | exit 1, same message | same, for `sshd-unix-local@.service` |

Runtime entries under `/run` (S8.2-5), logs/journals/state files (program records, question 4 of Section 8.2) and the
declaration machinery's own generations/receipts were classified as not separately required. Copies under
`/var/lib/stand/code-root` with the same bytes as their declared originals (`code_root_copies.same_as_declared_original`):
31,245 (h1 points), 31,244 (h2), 31,240 (h3), 31,241 (h4); copies that differ or have no declared counterpart and are not
directories are listed in `code_root_copies_not_matching` and named per history below (`/var/lib/stand/code-root/dev/null`,
a special file without a declared counterpart, at every point). None of the changed entries named in column (a) below is
registered in the installer ledger `/var/lib/stand/objects.json` saved at the same point (27,913 objects at h1, 27,911 at
h4; `raw/fix-1/ledger-*.txt`). Collector defect:
after any application that rewrote the machine declaration without `base-files.json`, its machine-authority step
raised `FileNotFoundError`; the generation identity was recomputed offline from the saved bytes and equals the success
report at every such point (`authority.machine_identity_matches_receipt_offline`).

## History 1 — updates (outcome ?)

Commands (root): `h1/update-1.sh` (`apt-get upgrade --stand-catalog ed`), `systemctl reboot`, `h1/update-2.sh`
(fetch ed 1.22.5-1, `/usr/bin/dpkg --install`), `systemctl reboot`; observations with `check-inputs-v4/supplement-1/step-8-cases/B2/cases-8/observe.py` (stdin sha256
`3aa84d89…`) after each restart and at the end (`raw/h1/commands.json`).

Entries caused by the history (changed after the guest was created, without an own claim, and not changed at the points
of histories 2 and 4 on fresh copies of the same image — `raw/fix-1/changed-unclaimed-differences.txt`; full list with
times `raw/fix-1/changed-unclaimed-entries.txt`):

- **E1** (from restart 1 on) directories `/usr/bin`, `/usr/share/doc/ed`, `/usr/share/info`, `/usr/share/man/man1`,
  `/var/lib/dpkg`, `/var/lib/dpkg/info`: mtime 18:40:52Z, during the boot after restart 1 (request 18:40:42Z, boot ID
  changed by 18:41:24Z, `raw/h1/restart-1.json`); at restart 2/end mtime 18:43:27Z, during the boot after restart 2
  (request 18:43:18Z). Members of dpkg packages (`ed` among the owners of the first four; `dpkg`, `base-files` of the
  last two). Decision: question 1 (S8.2-7) asks whether each was obtained as part of an installed package **and remains
  as received**; the inventory holds no record of the directory state as received (dpkg records none; OBSERVE-8:
  “Package membership alone does not establish unchanged receipt”) → **FACT_UNKNOWN**, missing fact: the state of each
  directory as received with its package. The later questions are not asked (S8.2-6). Which program wrote them at boot is
  not shown by the saved output.
- **E2** (from restart 1 on) `/var/lib/NetworkManager/NetworkManager.state`, `/var/lib/NetworkManager/seen-bssids`
  (empty), written 18:40:44Z and 18:43:19Z, at the shutdowns of the restarts; no dpkg membership, no ledger registration.
  Decision: **FACT_UNKNOWN**, missing fact: the content of `NetworkManager.state` (the summary keeps only its hash), which
  question 3 (a value chosen by a person that the computer obeys, S8.2-11) or question 4 (working state, S8.2-15) needs.
- **E3** (after restart 2 and end) left by update 2 (18:43:17–18:43:18Z, `raw/h1/h1-update-2.stdout`):
  `/var/lib/dpkg/info/ed.postinst` and `ed.prerm` (mode 0755; bytes equal the control members of both committed ed
  packages; last written 18:43:17Z, before the restart-2 request; mtime 1777275000 instead of 1673853117 at restart 1;
  `raw/analysis/h1-ed-maintainer-scripts.json`). Decision: question 1 — they carry the bytes and mode of the control
  members of the installed `ed` 1.21.1-1 but were written by the installation of 1.22.5-1, which the restart replay
  removed; whether they “remain as received” from the installed package needs a receipt record for control files, which
  the inventory does not hold → **FACT_UNKNOWN**, missing fact: the receipt record of these control files.
- **E4** (after restart 2 and end) `/var/lib/dpkg/alternatives/editor`: same bytes as at restart 1 (`60e3ad56…`), rewritten
  18:43:17Z; no dpkg membership, no ledger registration; on the image it is a U3 entry. Decision: **FACT_UNKNOWN**,
  missing fact: derivation evidence linking these bytes to the installation of a recorded package (S8.2-16, third line
  type), the same fact as for the image.
- **E5** (after restart 2 and end) directories `/var/lib/dpkg/alternatives`, `/var/lib/dpkg/updates`, `/var/cache/man`
  (dpkg members of `dpkg`, `man-db`). Decision as E1: **FACT_UNKNOWN** (state as received).
- **E6** (after restart 2 and end) man cache `/var/cache/man/index.db`, `/var/cache/man/CACHEDIR.TAG` and 25 language
  subdirectories with their `CACHEDIR.TAG` (written 18:43:17–18:43:18Z, “Processing triggers for man-db”,
  `raw/h1/h1-update-2.stdout`): no dpkg membership, no ledger registration (question 1: no); index database and tag files,
  no execute bit (question 2: not code, S8.2-20/S8.2-23); not a value chosen by a person (question 3: no); written by
  man-db as it ran → **program record** (cache, S8.2-15), need not be recorded (S8.2-2).
- **E7** (after restart 2 and end) dpkg working state and logs: `/var/lib/dpkg/lock`, `lock-frontend`, `status-old`,
  `triggers/Lock`, `/var/log/dpkg.log`, `/var/log/alternatives.log`: no dpkg membership, no ledger registration, not
  code, not chosen by a person; written by dpkg as it ran → **program record** (S8.2-15).

| Point | (a) in force, not recorded | (b) lines not fulfilled | (c) actions not done | Evidence |
|---|---|---|---|---|
| after restart 1 (boot `21b47d79`) | caused by the history: E1, E2 (FACT_UNKNOWN); U1–U5 | 0 of 560 machine lines, 0 of 1362 fs paths, 0 of 93 account rows; U2 | update-2, restart-2 not yet reached | `raw/analysis/h1-after-restart-1.summary.json`, `actions-h1-after-restart-1.json` |
| after restart 2 (boot `4d7f41f8`) | caused by the history: E1, E2, E3, E4, E5 (FACT_UNKNOWN); E6, E7 (program records); U1–U5 | 0 of 560, 0 of 1363, 0 of 93; U2 | none | `h1-after-restart-2.summary.json`, `actions-h1-after-restart-2.json` |
| end | same as after restart 2 | same (0/560, 0/1363, 0/93) | none | `h1-end.summary.json`, `actions-h1-end.json` |

- Update 1: exit 0, `SUCCESS 6dc280d6…`, ed 1.21.1-1 (`raw/h1/h1-update-1.stdout`); restart 1 changed boot ID
  (`raw/h1/restart-1.json`).
- Update 2: exit 0, read back `ed 1.22.5-1 installed` immediately, **no success report** (`raw/h1/h1-update-2.stdout`);
  the machine declaration in force is the same generation `6dc280d6…` (report 18:40:41Z) before and after
  (`raw/analysis/h1-diff-r1-to-r2.json`: no machine change; line `package:ed` requires 1.21.1-1). After restart 2 the
  system's replay restored ed 1.21.1-1 (`raw/h1/h1-after-restart-2-package.stdout`). The downloaded `.deb` in `/tmp` was
  recorded (`tmp:/ed_1.22.5-1_amd64.deb`).
- Declaration entries: 2010 before → 2016 after (machine 559→560: `system:base-state` added, `base` and `package:ed`
  changed; tmp 7→10, vartmp 4→6) (`h1-diff-initial-to-r1.json`, `h1-end.summary.json`).
- **Observation against:** a built-in tool with superuser privileges (`dpkg`, “the system package manager”, S8.1-4;
  “an installer” is a built-in tool, S8.1-7; so not breaking, S8.1-15) changed an installed package past the declaration (P4); between update 2
  and restart 2 the package was in force unrecorded (P1) and line `package:ed` unfulfilled (P2). Seen by the history's
  own readback; no committed observation point lies in that interval (question 2). The second update did not persist
  after restart (ordinary work, question 3). E1–E5 are undecided for a missing fact (FACT_UNKNOWN), not for the text.
- No written argument exists, from Section 8 alone, that any system having P1, P2 and P4 would fail this history; such a
  system's installer adds the change to the declaration (S8.3-7). Absent → testbed defect → **?**.

## History 2 — development (outcome ?)

Command (ordinary shell): `h2/history.sh` (stdin `b4c08e80…`): 3 fetches, 3 one-line edits, 6 source admissions/builds/
result admissions, 6 runs; observation at the end.

| Point | (a) | (b) | (c) | Evidence |
|---|---|---|---|---|
| end (boot `a1988efd`) | none caused by the history outside runtime, logs and the declaration machinery (below); U1–U5 | 0 of 561 machine lines, 0 of 1373 fs paths, 0 of 93 account rows; U2 | all 18 done | `raw/analysis/h2-end.summary.json`, `h2-end.units.json`, `actions-h2-end.json` |

- All three fetches checksum-verified, three `ONE_SOURCE_LINE_CHANGED`, six `OUTPUT_VERIFIED`, twelve `SUCCESS`
  applications, `H2_COMMANDS_COMPLETE` (`raw/h2/h2-development.stdout`); declaration in force `cf6065f6…` (18:54:37Z).
- Declaration entries: 2010 → 2027 (machine +2: `source:h2-hello`, `import:h2-hello-built`; home 4→15: `step8-h2/`,
  `hello.c`, `source.json`, six outputs, `h2-hello.built{,.json}`; tmp/vartmp +2 each) (`h2-diff-initial-to-end.json`).
- Unrecorded new entries were directories `/opt/stand/pkgs`, `/opt/stand/pkgs/h2-hello{,/src}`,
  `/opt/stand/pkgs/h2-hello-built{,/bin}` created by the system for recorded lines, runtime, logs and machinery
  (`raw/fix-1/changed-unclaimed-entries.txt`). No observation against.
- Outcome depends on whether the unresolved facts U1–U5 leave “nothing counts against” established (question 1);
  under the step-8 rule for two readings → **?**.

## History 3 — game (outcome ?; not performable)

Commands: root `h3/prerequisites.sh` (stdin `fb41a0aa…`): 15 checksum-verified packages, one `/usr/bin/dpkg --install`,
readback; ordinary `h3/history.sh` (stdin `927812e2…`).

| Point | (a) | (b) | (c) | Evidence |
|---|---|---|---|---|
| end (boot `72737801`) | 15 installed packages without any line (bc, bsdmainutils, bzip2, distro-info, jq, lib32gcc-s1, lib32stdc++6, libc6-i386, libevent-core-2.1-7t64, libjq1, libonig5, ncal, pigz, tmux, unzip) and their files, e.g. `/usr/bin/jq`, `/usr/bin/tmux`, `/usr/lib32/libc.so.6`; code-root copies `/var/lib/stand/code-root/etc/{ld.so.cache,shells}` differ from their declared originals (`code_root_copies_not_matching`); U1–U5 | line `base`: `/etc/ld.so.cache` and `/etc/shells` sha256 differ (rewritten by dpkg triggers; the `/etc` filesystem declaration recorded the new bytes); other 558 machine lines, 1415 fs paths, 93 account rows: 0; U2 | game install and the 7 later actions not done | (not published: direct evidence at least 2 MB), `h3-diff-initial-to-end.json`, `actions-h3-end.json` |

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

Entries caused by the history at the disconnected point (`raw/fix-1/changed-unclaimed-differences.txt`,
`raw/fix-1/changed-unclaimed-entries.txt`, `raw/fix-1/ledger-h4-install-disconnected.txt`):

- **F1** directory `/opt/stand/pkgs` (changed, mtime 19:00:53Z) and the new directories `/opt/stand/pkgs/dev-worker` (19:00:53Z) and `/opt/stand/pkgs/dev-worker/bin`
  (19:01:21Z), created during the interrupted install (19:00:50–19:01:46Z); the census holds no entry below them.
  Question 1: no — the installer reported `FAILED`, the machine declaration in force has no `dev-worker` line, no dpkg
  membership, and the installer ledger at this point (27,911 objects) registers nothing named `dev-worker`
  (`raw/fix-1/h4-ledger-dev-worker.txt`); question 2: no — empty directories hold no code; question 3: no — not a value
  chosen by a person; question 4: created by the installer as it ran → **program record** (working state, S8.2-15), need
  not be recorded (S8.2-2).
- **F2** `/var/lib/stand/code-root/etc/stand/read-closure` (written 19:01:26Z) differs from its declared original
  (`code_root_copies.differs_from_declared_original` = 1). It was compared while the `/etc` declaration changed during
  collection (below), and its original `/etc/stand/read-closure` is one of the five `/etc` paths whose census entry did
  not match its claim at comparison (`claimed_but_no_matching_claim`). **Unresolved, unstable reading** — not counted as
  matching; FACT_UNKNOWN, missing fact: a stable `/etc` declaration during collection against which to compare the copy.
- `/var/lib/stand/pending.json` (candidate `8824e9eb…`, declaration machinery) and
  `/var/log/journal/…/user-1000.journal` (log, program record): as classified above.

| Point | (a) | (b) | (c) | Evidence |
|---|---|---|---|---|
| install, disconnected (boot `904bdb6d`) | caused by the history: F1 (program record), F2 (unresolved, unstable); five `/etc` paths whose census entry did not match their claim at comparison (`/etc/apparmor.d/abstractions/stand-map`, `/etc/ssh/sshd_config.d/00-stand.conf`, `/etc/stand/launch.tsv`, `/etc/stand/read-closure`, `/etc/stand/stand-profiles`; all and only timestamp fields changed against the initial declaration, `raw/analysis/h4-diff-initial-to-disconnected.json`) — unstable reading; U1–U5 | `port:udp:1` (`10.0.2.15%ens3:68`, listening) not listening; 558 other machine lines 0; the `/etc` filesystem declaration had three distinct identities during collection (two changes: success reports `170b86d2…` generation 237 before, `5bc3280d…` generation 381 at comparison, `018d47b2…` generation 386 after; `declaration_stable=false`), so the one timestamp-only difference found at comparison (1 path, `etc:/ssh/sshd_config.d/00-stand.conf`, 3 fields: atime, ctime, mtime) is not a stable reading; 1361 other fs paths, 93 account rows: 0 | install not done (exit 1) | (not published: direct evidence at least 2 MB) (`disconnected_observation.identity_before`, `identity_at_comparison`, `identity_after`), `raw/analysis/h4-install-disconnected.summary.json`, `actions-h4-install-disconnected.json`, `raw/fix-1/h4-identities-and-cut.txt` |
| restored | unavailable: session exit 255 | unavailable | retry not yet reached | `raw/h4/h4-install-restored.*`, `actions-h4-install-restored.json` |
| after restored retry | unavailable (255) | unavailable | retry unavailable (255) | `raw/h4/install-restored-retry.*`, `actions-h4-install-after-restored-retry.json` |
| end | unavailable (255) | unavailable | worker run, development prefix/cut/suffix not done | `raw/h4/h4-end.*`, `actions-h4-end.json` |

- Cut valid: installer process active at carrier 0 (`valid_cut: true`, `active_at_cut`: `stand-pkg install …` pid 1382,
  `carrier_at_cut {"ens3":"0"}` in (not published: direct evidence at least 2 MB); `valid_cut` also in `raw/h4/observation-points.json`;
  the QMP requests, replies and times are in `raw/h4/install/host-events.json`). Installer output (exit 1):
  `FAILED recovery incomplete: readback mismatch: port:udp:1; restoration mismatch: port:udp:1`.
- During and after the disconnected observation `/run/stand-ready` was absent and `pending.json` held candidate
  `8824e9eb…` (`identity_before`/`identity_after`). The image requires that file for every login
  (`B2/build/install-transactions.py:27`, `account requisite pam_exec.so quiet /usr/bin/test -f /run/stand-ready` in
  `/etc/pam.d/common-account`; `B2/build/transactions.py` removes it in recovery). The link was restored at 19:03:39Z and
  the buffered output arrived over the existing session (19:03:41Z); every new session 19:03:41–19:03:42Z exited 255 with
  empty stderr. Established: gate file absent; new sessions refused. Not established by output: that the gate, and not
  something else, refused them (no further probe; the history is not repeated).
- Declaration entries: 2010 → 2014 at the disconnected point (tmp +2, vartmp +2); after the history: unavailable.
- **Observations against:**
  1. Line `port:udp:1` unfulfilled after the last completed application (P2).
  2. The installation failed **while disconnected** (exit 1, `readback mismatch: port:udp:1`). The committed inputs state
     that this installation is a local-input operation that “need[s] not fail merely because the link is down”
     (`check-inputs-v4/supplement-1/step-8-cases/B2/CASES-8.md`, History 4). If it is therefore not “an action that needs the network” (`SUP1/step-8.md`), its
     failure is an observation against ordinary work (A.4.3) in its own right, before any restoration. The output also
     shows that the failing readback is of the port line bound to the disconnected interface; whether an action that
     fails only for that reason “needs the network” is a choice between two readings, recorded as question 4.
  3. The single prescribed retry after the network was restored, and every later action, could not be performed: every
     new session exited 255. This is the separate reason the history is not performable.
  No argument from the definitions alone that any P1/P2/P4 system fails this history (an open port is not a separate
  object, S8.2-5, and “may also be recorded”, S8.2-19); history not performable, and item 2 depends on a choice between
  two readings → **?**.

## Breaking, counterexamples, lists

- Breaking: none. Root was used for the built-in installer (`dpkg`), the service manager (`systemctl reboot`), fetching
  files to `/tmp` and read-only queries.
- Counterexample (an object the text of 8.1–8.2 cannot decide): none found; undecided cases above are FACT_UNKNOWN, each
  with its missing fact named, or unstable readings.
- Gaps were not put into either list of Supplement 1 (`step-2.md` question still open).

## Comparison with the expected result of `SUP1/step-8.md`

| Expected | Result |
|---|---|
| In the performable histories nothing in force found unrecorded and every line fulfilled | **not met**. Histories 3 and 4 were judged not performable and are excluded from this row. History 1 — ed 1.22.5-1 in force unrecorded after update 2 (own readback); entries E1–E5 left by the history undecided (FACT_UNKNOWN). History 2 — no unrecorded object found and no line found unfulfilled, but coverage is not established (U1–U5: the unresolved facts, the two unproved lines and the seven failed queries) |
| The game history not performable | **met** |
| The declaration grows with every file a history saves | **not met**: files saved in the mediated trees were recorded (h1, h2, h3), but the files written by `dpkg` under `/usr` in histories 1 and 3 were not; history 4 not assessable |
