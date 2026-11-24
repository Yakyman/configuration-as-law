# Cases of the ConfOS check

Written by the case party from Paper 4, Section 8 (`spec/HYPOTHESIS.md`, sentences `spec/SENTENCES.md`), the plan
(`spec/PAPER5.md`, Section 9) and Paper 3, Sections 4.3–4.4 (`spec/PAPER3.md`). Programs and packages: `PROGRAMS.md`.
Data formats: `FORMATS.md`. Questions: `QUESTIONS.md`. The runner `run` performs every case below in this order and
writes `runs/<name>/results.tsv`.

## Notation

| Step | Meaning |
|---|---|
| `FRESH NAME` | a fresh clean installation: an overlay of a disk built by the builder's documented command from the published source and the test declaration `D-test`; booted with the builder's documented script, a slot of `COMMON.md`, a serial log and a QMP socket. `FRESH-BUILD NAME` builds a new independent installation instead of an overlay |
| `L+ SPEC` / `L~ SPEC` / `L- SPEC` | the person adds / changes / removes a line; SPEC is a semantic line (below) that `adapter.py` writes in the builder's format (`build/DECLARATION.md`) |
| `APPLY` | the documented application (`build/INTERFACE.md` revision 1: `sudo confos apply`, the reboot it makes, reconnect, `confos status`); result: `applied` when `confos status` prints `APPLIED SHA256` with the sha256 of the declaration just written, else `not-applied` |
| `U: CMD` / `R: CMD` | CMD in the guest over SSH as the ordinary account / as root by the documented means |
| `H: CMD` | CMD on the host |
| `RESTART` | `R: systemctl reboot`; if the system has no systemctl, `R: reboot`; if no command restarts the machine as root (refused, or no new boot within 60 s), `R: sync` and the reset of the machine from the host (QMP `system_reset`), noted in the evidence; then wait for SSH and require a new boot id (`/proc/sys/kernel/random/boot_id`) |
| `CUT` | power cut: `kill -9` of the QEMU process the instant the report of success is read, then boot the same disk |
| `LINK down` / `LINK up` | QMP `set_link` of the guest's network device, from the host; no setting of the guest changes |
| `INV TAG` | `inventory` of the whole machine: the force level over SSH (including every file on a volatile filesystem — tmpfs, ramfs — which exists only while the machine runs), then `R: sync` and the stored level read from the disk image with libguestfs opened read-only (`--ro`) while the machine runs; the machine is not restarted for an inventory. The stored level includes the contents of every filesystem image found on the disk (for example a squashfs root image) |
| `DER` | `derive` from the declaration in force (files read from the disk from outside, identity checked against `confos status`) |
| `CMP TAG` | `compare` of `INV TAG` with `DER` and the declaration → `compare.tsv` |
| `DECL?` | sha256 of every declaration file, read from outside; `DECL-CHANGED` = differs from what the person (the runner) last wrote |

Semantic line specs (the builder's format is filled in by `adapter.py`): `package NAME[=VERSION]`,
`pip NAME==VERSION`, `npm NAME@VERSION`, `flatpak APP-ID [REMOTE]`, `appimage PATH URL SHA256`,
`download PATH URL SHA256 [unpack]`, `built PATH SOURCE-PATH BUILD-CMD`, `script PATH SHA256`,
`user-unit ACCOUNT NAME TEXT [enabled]`, `service NAME TEXT [enabled]`, `firewall RULE`, `sudo RULE`,
`account NAME [uid=N] [groups=…] [shell=…] [home=…]`, `container-image REF@DIGEST`, `shell-startup ACCOUNT FILE TEXT`,
`git-config ACCOUNT KEY VALUE`, `archive-state T`.

`D-test` is the builder's base declaration plus one line for the recorded program of each channel (`PROGRAMS.md`,
column “Recorded program”) and the account `person` with its SSH key: Paper 3, Section 4.3, “The test declaration
names everything it permits: the base system and, for each channel below, one program installed through that
channel.”

## Decisions common to all cases

(Revised 2026-11-24 from 11:45 UTC: the repairs below are marked [n2-1] … [n2-7], [n3-A] … [n3-D], [f2], [f3];
CORRECTIONS.md records each with its time and its test.)

- **Every application** in any case is followed by `CMP`. Each such check is one row `P2-1:<case>:<n>` (part P2).
  Source: Table 9, P2, “After each completed application, every line is compared with the state it requires.” Counts
  against: “At least one line is not fulfilled”. Each line is compared with the state that this line requires: the
  account exists with the fields its line states, the hostname is the stated one, the package is installed in the
  stated version with its files as received, the service runs, the rule is in force. A file whose content an account
  or setting line determines (`/etc/passwd`, `/etc/shadow`, `/etc/group`, `/etc/gshadow`, `/etc/subuid`,
  `/etc/subgid` under an `account` line; `/etc/hostname`, `/etc/hosts` under `setting hostname`; `/etc/localtime`,
  `/etc/timezone` under `setting timezone`) is not compared with the default of the base: `derive` gives it as
  underived with the package default kept (S8.2-17; D4) [n2-2]. `fail` on any `MISSING` or `DIFFERS` line;
  `undecided` when the only differences are rules in force with an added comment (Q7, both readings) [n2-6];
  `unobserved` on `UNVERIFIED` only (Q8) or if the inventory could not be taken; else `pass`. An application that does
  not report success leaves the earlier declaration in force (S8.1-14) and it is that declaration that is compared.
- **Every inventory** is also an inventory under P1 and under Understanding: rows `P1:<TAG>` and `UND:<TAG>`. Source:
  Table 9, P1, “After the ordinary work and after every attempt of the cases of P4, an inventory of the whole machine
  is taken at both levels of [3], Section 4.2”; Understanding, “The comparison is made with every inventory taken
  under P1”. Counts against: P1 “An installed object or a setting is in force and no line records it, and this is not
  breaking”; Understanding “An installed object or a value of a setting on the machine differs from what was derived
  from the declaration”.
  - `REF` [n2-1]: the reference installation of the declaration in force — a clean installation built by the case
    party from the published source and that declaration (`build.sh`), booted once until `confos status` prints
    `APPLIED`, its inventory taken from outside, then stopped and deleted (one per declaration per run,
    `runs/<name>/_reference/`). Plan Section 9.3, “How objects are decided”: “The implementation may name the line
    from which it built an object; this is accepted only if the checksum of the object equals the one that follows
    from that line. Every other object is decided under [4], Section 8.2”; the checksum that follows from a line is
    computed from the package the line names and its dependencies in the archive state of the `snapshot` line
    (`derive`), and for what the system builds from lines, from the published source run in a clean environment
    (`REF`), never on the machine under test.
  - P1: `compare --reference` — an object of the machine that equals the derivation or the object of `REF` is
    recorded by the lines; every other object is taken through the four questions of S8.2-6 in their order
    (`decide.tsv`, the case's list of what the person made, the routes) [n2-1, n2-3, n2-4]. `fail` on any
    `UNRECORDED` object, or a stored object that differs from its line and from `REF` (a file of a package that no
    longer remains as received, S8.2-7); `undecided` when the only such objects are decided both ways (Q2, `BOTHWAYS`)
    or executed only by a data route or by a program that reads almost any text (Q11, Q12, `QUESTION`); else `pass`.
  - UND, under both readings of D1, D3, D4, D5, D6 [n2-6]: the harder reading is the comparison with the derivation
    by `derive` (`fail` on `UNRECORDED`, `DIFFERS`, `MISSING`, `UNDERIVED`); the easier reading is the comparison with
    `REF`, what the published source gives for the declaration (`compare --baseline REF`, with `decide.tsv`; `fail` on
    `UNRECORDED`, `DIFFERS`, `MISSING`). Met under both: `pass`; not met under the easier: `fail`; met under the easier
    only: `undecided`. The evidence keeps both outcomes with their counts.
  - Q4: the rows of the inventory before the restart in P4-PIPE-* exist under the harder reading only; a `fail` there
    is `undecided` [n2-6].
- **What the person made** [n2-3]. S8.2-15: “if a person created or brought the object, it is material—documents,
  photographs, projects, downloaded files, private keys and passwords for logging in to other machines”; S8.2-4: “A
  command that a person typed himself or herself is that person’s action, not an object.” Each case lists the objects
  that the person's own typed commands create or bring (`casedefs.MADE`: `mkdir`, a shell redirection, `curl -o`,
  `cp`, `tar x`, `git init`, `ssh-keygen`, a compiler at the person's command) — never what a channel's installer
  installs. Such an object that follows from no line is taken through the four questions: it was obtained with no
  package (S8.2-7); it is code only if a direct route executes it (S8.2-9, review decision R1, below); a startup
  file, unit file, hook or alias is a setting only if something obeys it — a probe of the case shows it in force since
  the last restart (S8.2-11 … S8.2-14; [n2-4]); otherwise it is material: it need not be recorded
  (S8.2-2) and counts against neither P1 nor P4. A recorded object that the person changed is never material: it is a
  recorded thing changed past the declaration.
- **Routes** [n2-4] (review decision R1). After each inventory of a case that lists what the person made, every such
  file, and every file with an execute flag that a rule of `decide.tsv` would decide, is given to every direct route —
  launched by its path (with `chmod u+x` if the person owns it and it is not executable), the loader, `bash F`,
  `sh F`, `bash < F`, `. F`, `python3 F`, `perl F`, `awk -f F`, `make -f F`, `node F`, the interpreter its `#!` line
  names — and to every data route — `cat F | bash`, `bash -c "$(cat F)"`, `python3 -c "exec(open(F).read())"` — as
  the person and as root, each under `timeout 10` with standard input from `/dev/null`, after the inventory so that
  nothing it does enters it. A route is refused on exit 126 or 127 or a message of refusal or of a file that is not a
  program in that language (`run`: `REFUSAL`); exit 0, a timeout, or another exit without such a message means it
  executed; only the routes that the file's own form names count as executing it (its `#!` line, suffix or startup-file name;
  the path and the loader for every form; QUESTIONS.md Q12). `routes.tsv`: `executes` (a direct route of its form executed it: the file is code, a program no line records), `refused`
  (every route refused: not code, R1), `data-only` (every direct route refused, a data route ran it: Q11), `any-only`
  (only an interpreter that its form does not name accepted it: Q12; for an object a rule decides this does not count). A file with
  NUL bytes is given only to the path and the loader. `awk -f F` counts only if F contains an action (`{`) and `make -f F`
  only if `make -n -f F` prints a command: otherwise that program executes nothing of F. An empty file
  contains no code and is given to no route. `routes-raw.tsv` keeps every route with its exit and error output.
- **The four questions for every object of the writable area** [n3-A] (S8.2-6, “What an object
  is is determined by four questions asked in order; the first affirmative answer decides”; S8.2-15, “Otherwise: if
  a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person
  created or brought the object, it is material”). Every comparison of an installation (`compare --questions`)
  takes every object outside the stored, read-only system part that equals neither the derivation nor `REF`,
  whoever made it, through: (1) is it in a package manager's store (`store` rules of `decide.tsv`: pip, npm,
  Flatpak, the container store, an unpacked AppImage, the dpkg database) — counts; (2) is it code in form — the
  routes are tried on it as on the person's own files (above): a direct route of its form executes it — counts;
  (3) is it a carrier of a setting (`carrier/…` rules: units, cron tables, authorized keys, startup files, hooks,
  saved networks, access rules) and does its probe show it in force — counts; (4) otherwise a program record or
  material: not counted, written to the excluded list with the reason “S8.2-15: none of the first three questions is
  answered yes”. Every counted object carries the question and the evidence. In the stored, read-only system part,
  everything that equals neither the derivation nor `REF` counts. Format: FORMATS.md, “Additions of 2026-11-24,
  13:55–15:50 UTC”.
- **A row whose deciding observation was not made is `unobserved`** [n3-B] (COMMON.md: `fail`
  means the requirement is not met). An object that is code in form and that no direct route was tried on is
  `UNROUTED`; a carrier of a setting whose probe was not made is `UNPROBED`. A P1, UND, P4 or REM row is `fail` if one
  object counts against it with its observation made; otherwise `unobserved` if such objects remain; otherwise
  `undecided` on `BOTHWAYS` or `QUESTION`; otherwise `pass`.
- **A line written by a program.** If `DECL-CHANGED` after an attempt (a line the runner did not write appeared), the
  case is `undecided` with the evidence naming the program that wrote it (Q3; plan Section 9.3, “For each case that
  is met because a program recorded the change in the declaration as part of its own operation, the review checks
  which program recorded the change and whether it is such a tool; if the review does not confirm that it is, the
  case yields ?”).
- **`unobserved`** is given only when a step outside the implementation failed: an external download answered other
  than 200 or its checksum differed, the host ran out of a slot, the runner itself raised an error, or the reference
  installation could not be made. A machine of ConfOS that does not boot, does not answer, or refuses an ordinary
  action is `fail`, not `unobserved`.
- No event of these cases is breaking (S8.1-15) except the two breaking candidates of Q6 (P4-C6-5, the first attempt
  of P4-BT-5), whose rows are evaluated under both readings of Q6 [n2-6].
- `FRESH` waits until `confos status` prints `APPLIED` (at most 900 s, noted in the evidence) before the case goes on:
  the person starts once the system reports the declaration in force, as the reference installation does.

## Ordinary work (OW)

Source: plan Section 9.3, “Ordinary work is a condition of the whole check … It counts against the hypothesis when an
ordinary action cannot be performed through the declaration and its built-in tools.” Counts against: quoted. Each OW
case: `pass` if every step exits 0 and every check holds; `fail` if a step of the action cannot be performed through
the declaration and its built-in tools; then `INV OW-n` (rows `P1:OW-n`, `UND:OW-n`).

| ID | Source | Steps | Observed by | pass when |
|---|---|---|---|---|
| OW-1 | “installing a program” | `FRESH ow1`; `L+ package tree`; `APPLY`; `U: tree --version`; `U: tree -L 1 ~` | exit codes; `U: dpkg-query -W tree` | applied, both commands exit 0, version 2.2.1-1 |
| OW-2 | “two updates with a restart after each” | `FRESH ow2` built at archive state T0 (Q1); `L~ archive-state T1`; `APPLY`; `RESTART`; `U: dpkg-query -W` | versions vs `Packages` of T1 for every package of `D-test` | applied, new boot id, every listed package at its T1 version, `INV OW-2` taken |
| OW-3 | same | after OW-2: `L~ archive-state T2`; `APPLY`; `RESTART` | versions vs `Packages` of T2 | as OW-2 for T2 |
| OW-4 | “working in a browser” | `FRESH ow4`; `L+ package firefox-esr`; `APPLY`; `H:` serve `page.html`; `U: firefox-esr --headless --screenshot ~/shot.png http://10.0.2.2:PORT/page.html`; `U: firefox-esr --headless --screenshot ~/local.png file:///usr/share/doc/firefox-esr/copyright` | `U: test -s ~/shot.png && file ~/shot.png` | both PNG non-empty |
| OW-5 | “editing documents” | `FRESH ow5`; `L+ package libreoffice-writer`; `APPLY`; `U: printf 'First line\n' > ~/doc.txt`; `U: soffice --headless --convert-to odt --outdir ~ ~/doc.txt`; `U: printf 'First line\nSecond line\n' > ~/doc.txt`; convert again; `U: soffice --headless --cat ~/doc.odt` | output of `--cat` | contains both lines |
| OW-6 | “running ordinary commands and one's own recorded script” [4, 9.3] | `FRESH ow6` (the script `~/bin/cases-report.sh` is in `D-test`); `U: ls -la ~ && cp /etc/hostname ~/h && grep -c . ~/h && sort /etc/shells && printf '1p\nq\n' \| ed -s ~/h`; `U: ~/bin/cases-report.sh` | exit codes; script output `cases-report ok` | all exit 0 |
| OW-7 | “fetching, building, changing and rebuilding a small program” | `FRESH ow7`; three rounds: `U: curl -fsSo ~/src/hello.c URL` (sha256 `cb95a0ed…`); the person records the program by a line of its own, `L+ compile-from ~/bin/hello ~/src/hello.c -O2` (rendered as `compile PATH 0755 SHA256 files/hello.c -O2` of `build/DECLARATION.md`, the source being the person's current file); `APPLY`; `U: ~/bin/hello` (output sha256 as step 8 `h2/inputs.json`); change the greeting line (`sed`); `L~` the line; `APPLY`; run. After each run, the person's own direct build `U: gcc -O2 -o ~/bin/hello-direct ~/src/hello.c && ~/bin/hello-direct`, kept in `direct.json` (REVIEW.md R2: it does not decide) | output checksums of step 8 `h2/expected-*.txt` | six runs of the program of the line print the expected outputs |
| OW-8 | “installing and starting a game through a launcher that downloads it” | `FRESH ow8`; `L+ package NAME=VERSION` for each prerequisite that the release's `game-packages.conf` lists and D-test does not record; `L+ linuxgsm person /home/person/game 26.5.0` (rendered `linuxgsm USER PATH RELEASE SHA256 BUNDLE`, the bundle made by `tools/make-inputs.sh game` from the upstream LinuxGSM sources of v26.5.0 and v26.6.0, the ET 2.60b server archive and the two defaults of the published release); `APPLY`; `U: bash ~/game/wetserver start`; check `etded` in `/proc/*/exe`; `U: bash ~/game/wetserver stop`; the launcher's update: `L~ linuxgsm person /home/person/game 26.6.0`; `APPLY`; start/check/stop again. The person's own launcher in `~/game-direct` (`curl` LinuxGSM v26.5.0, sha256 `3063de7f…`; `bash linuxgsm.sh wetserver`; `./wetserver auto-install`) is performed too and kept in `direct.json` (R2: it does not decide) | `R: ls -l /proc/*/exe \| grep etded` | the game server process ran both times |
| OW-9 | “an installation during which the network is lost and then restored” | `FRESH ow9`; `L+ package fonts-noto-cjk`; `APPLY` in the background; `LINK down` when the guest has received ≥ 5 MB more than before the application (read from the guest's `/sys/class/net/DEV/statistics/rx_bytes` over SSH every 0.2 s); wait for the application to end; `CMP`; `LINK up`; `APPLY`; `CMP` | `dpkg-query -W fonts-noto-cjk`; report of success | after `LINK up` the second application is applied and the package is installed |
| OW-10 | “connecting to a Wi-Fi network … on real hardware” | not performed in this run: real hardware (`nmcli device wifi connect SSID password …` with a line for the saved network) | — | `unobserved` |
| OW-11 | “pairing a Bluetooth device on real hardware” | not performed in this run: real hardware (`bluetoothctl pair ADDR` with a line for the pairing) | — | `unobserved` |

## P1 — Completeness

Rows `P1:<TAG>` come from every inventory of OW and P4 (above). In addition:

| ID | Source | Steps | Counts against | pass/fail |
|---|---|---|---|---|
| P1-0 | Table 9, P1, “an inventory of the whole machine … every object is decided” | `FRESH p1`; `INV P1-0` once `confos status` prints `APPLIED`, no action | “An installed object or a setting is in force and no line records it, and this is not breaking” | as every `P1:<TAG>` row (Decisions common to all cases): against `REF` and the four questions |

## P2 — Guarantee

| ID | Source | Steps | Observed by | pass/fail |
|---|---|---|---|---|
| P2-1:* | “After each completed application, every line is compared with the state it requires” | every `APPLY` of the run | `CMP` | as “Decisions common to all cases” |
| P2-ADD-1, -2, -3 | “A power cut right after the report of success, three times for each kind of application: adding, changing and removing a line” | `FRESH p2a-k`; `L+ package tree` (k=1), `L+ package sl` (k=2), `L+ user-unit person cases-cut.service …` (k=3); `APPLY` streaming; `CUT` the instant `APPLIED` is read; boot; `R: confos status`; `INV P2-ADD-k`; `CMP` | identity in force = identity of the declaration just applied; `CMP` | `pass` if the declaration in force is the one reported as applied and `compare.tsv` has no `MISSING`/`DIFFERS`; `fail` otherwise (also when the declaration in force is the earlier one: the report of success named the new one, S8.1-14) |
| P2-CHG-1, -2, -3 | same | `FRESH p2c-k`; k=1 `L~ setting hostname` from the value of `D-test` to `cases-chg`; k=2 `L~ firewall` rule port 8081→8082; k=3 `L~ account person shell=/bin/sh`; `APPLY`; `CUT`; boot; check as above | same | same |
| P2-REM-1, -2, -3 | same | `FRESH p2r-k`; k=1 `L- package ed`; k=2 `L- firewall` rule; k=3 `L- user-unit person cases-tick.timer`; `APPLY`; `CUT`; boot; check as above, and the removed object is not in force | same, and `U: command -v ed` / `nft list ruleset` / `systemctl --user is-enabled` | same; and `fail` if what the removed line contributed is in force |
| P2-NET-1 | “An installation interrupted by a loss of network” | `FRESH p2n`; `L+ package fonts-noto-cjk`; `APPLY`; `LINK down` during the download (as OW-9); wait for the application to end; `R: confos status`; `INV P2-NET-1`; `CMP`; `LINK up` | report of success, identity in force, `CMP` | `pass` if either (the application did not report success, the earlier declaration is in force and all its lines are fulfilled) or (it reported success and every line including `fonts-noto-cjk` is fulfilled); `fail` otherwise |

## P4 — Law

Source of every P4 case: Table 9, P4, “Through every channel of [3], Section 4.3, an attempt is made to install,
launch or change what is not recorded; the built-in tools, including the system’s own package installer, are also
tried directly with superuser privileges.” Counts against: “A channel installs, launches or changes such a thing
although it is not recorded, and this is not breaking; a built-in tool changes it past the declaration”.

Every P4 case: `FRESH p4-<id>` (one fresh overlay per case); `INV <ID>-pre` (no rows of its own); every probe of the
case, taken before the attempt [n2-5]; the attempt; the probes; `DECL?`; `INV <ID>`; the routes; `CMP <ID>`; then
`compare --baseline` of `INV <ID>` against `INV <ID>-pre` (`attempt-delta.tsv`: every object new, gone or different
after the attempt). The effect of the attempt (`attempt-effect.tsv`) is every object of the delta that `CMP <ID>`
reports as following from no line (`UNRECORDED`, `BOTHWAYS`, `QUESTION`) or as different from its line (`DIFFERS`),
and every `MISSING`/`DIFFERS`/`UNVERIFIED` line of `CMP <ID>` that was not in the comparison of `INV <ID>-pre` (a
recorded thing changed past the declaration). What the person made and is material is not in `CMP <ID>` (above).

A probe counts against only if it holds after the attempt and did not hold before it (`pre-probes.json`): a probe
that already holds reads a state the declaration itself gives ([n2-5]; P4-BT-5 in dev-11). A probe
that would itself perform the attempt (`npx --yes`, `podman run` of an image not yet pulled) is not taken before,
and the row says so. A probe's regex is matched on stdout and stderr (`re:`) or on stdout after exit 0 (`out:`).

Decision, under both readings of every open question that changes it [n2-6] (`run`: `p4_decide`):
`undecided` if `DECL-CHANGED` (Q3); `fail` if a probe counts against or the effect is not empty under every reading
(a step of the case failing, for example the restart, is also `fail`); `undecided` if what counts is only the
breaking candidate's write (Q6), or objects decided both ways (Q2) or executed only by a data route or a program that
reads almost any text (Q11, Q12); `unobserved` if either inventory could not be taken; otherwise the case is met
under reading A of S8.3-7 (the built-in tool refused) and, when its attempt uses a built-in tool (S8.1-7;
`casedefs.TOOL` names it), not under reading B (the tool must add the change to the declaration; build/QUESTIONS.md
1, not decided by the review, QUESTIONS.md Q13): `undecided`; a case whose attempt uses no built-in tool (a download,
an archive, a compiler, an interpreter, a startup file, a hook, a key) is `pass`.
Objects that were on the machine before the attempt and follow from no line are not the channel's doing: they count
under P1, in the rows `P1:<ID>` (and `P1-0`), not under P4. (Until 2026-11-24 05:30 UTC the rule was “or `CMP` shows
any `UNRECORDED` object”, which made every P4 case fail on the objects of the fresh installation alone — dev-8.)
Rows `P1:<ID>` and `UND:<ID>` follow.
“Startable” is tested by running it: a file that exists but whose run is refused (exit 126/127 or `Permission
denied`/`Operation not permitted`) is not startable; it is still an object on the computer, and the routes decide
whether it is code (R1).

| ID | Channel | Attempt (commands) | Probe |
|---|---|---|---|
| P4-C1-1 | system package manager, user | `U: apt-get download hello; apt-get install -y hello` | `U: hello --version; dpkg-query -W hello` |
| P4-C1-2 | system package manager, root | `R: apt-get update; apt-get install -y hello` | same |
| P4-C1-3 | system package manager, root, direct | `R: apt-get download hello && dpkg -i hello_2.10-5_amd64.deb` | same |
| P4-C1-4 | change past the declaration, root | `R: apt-get remove -y ed` | `U: ed --version`; `dpkg-query -W ed` (the recorded `ed` must stay in force) |
| P4-C1-5 | change past the declaration, root | `R: dpkg --purge --force-depends ed` | same |
| P4-C1-6 | unpacked package, user | `U: apt-get download hello && dpkg-deb -x hello_*.deb ~/x && ~/x/usr/bin/hello` | the run's exit and output |
| P4-C2-1 | pip, user | `U: pip install --user --break-system-packages pyjokes==0.8.3 && ~/.local/bin/pyjoke` | run; `U: python3 -m pip list --user` |
| P4-C2-2 | pip, venv | `U: python3 -m venv ~/venv && ~/venv/bin/pip install pyjokes==0.8.3 && ~/venv/bin/pyjoke` | run |
| P4-C2-3 | pip, root | `R: pip install --break-system-packages pyjokes==0.8.3 && pyjoke` | run; `R: pip list` |
| P4-C2-4 | pip, wheel file | `U: pip download pyjokes==0.8.3 -d ~/w && pip install --user --break-system-packages --no-index ~/w/*.whl && ~/.local/bin/pyjoke` | run |
| P4-C3-1 | npm, user prefix | `U: npm install -g --prefix ~/.npm-global semver@7.6.3 && ~/.npm-global/bin/semver 1.2.3` | run |
| P4-C3-2 | npm, project | `U: mkdir ~/p && cd ~/p && npm install semver@7.6.3 && ./node_modules/.bin/semver 1.2.3` | run |
| P4-C3-3 | npx | `U: npx --yes semver@7.6.3 1.2.3` | run; `U: ls ~/.npm/_npx` |
| P4-C3-4 | npm, root | `R: npm install -g semver@7.6.3 && semver 1.2.3` | run |
| P4-C4-1 | Flatpak, user | `U: flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo && flatpak install --user -y flathub net.sourceforge.ExtremeTuxRacer` | `U: flatpak list --user`; `U: flatpak run --command=true net.sourceforge.ExtremeTuxRacer` |
| P4-C4-2 | Flatpak, root | `R: flatpak install --system -y flathub net.sourceforge.ExtremeTuxRacer` | `R: flatpak list --system`; run |
| P4-C4-3 | Flatpak, a new remote | `U: flatpak remote-add --user cases-extra https://dl.flathub.org/beta-repo/flathub-beta.flatpakrepo` | `U: flatpak remotes --user` (a remote is a setting of the installer: S8.2-11) |
| P4-C5-1 | AppImage | `U: curl -fsSLo ~/nvim.appimage URL-0.9.5 && chmod +x ~/nvim.appimage && ~/nvim.appimage --version` | run |
| P4-C5-2 | AppImage, extract | `U: ~/nvim.appimage --appimage-extract-and-run --version; ~/nvim.appimage --appimage-extract && ~/squashfs-root/AppRun --version` | run |
| P4-C6-1..4 | direct download | `U: curl -fsSLo DIR/jq URL && chmod +x DIR/jq && DIR/jq --version` for DIR = `~`, `/tmp`, `/dev/shm`, `/var/tmp` | run |
| P4-C6-5 | direct download, root | `R: curl -fsSLo /usr/local/bin/jq URL && chmod +x /usr/local/bin/jq && jq --version` — note: writing into `/usr/local/bin` with `curl -o` is a direct write by root outside the built-in tools, a breaking candidate under S8.1-15 (Q6): it is performed and counts until the review recognises it as breaking | run |
| P4-C6-6 | archive | `U: curl -fsSLo ~/rg.tgz URL-ripgrep && tar xf ~/rg.tgz -C ~ && ~/ripgrep-14.1.1-x86_64-unknown-linux-musl/rg --version` (ripgrep unpacked outside its recorded line) | run |
| P4-C7-1 | build from source | `U: curl -fsSLo ~/h.tgz URL-gnu-hello && tar xf ~/h.tgz -C ~ && cd ~/hello-2.12.1 && ./configure --prefix=$HOME/.local && make && make install && ~/.local/bin/hello` | run |
| P4-C7-2 | one-file compile | `U: printf 'int main(){return 42;}' > ~/t.c && gcc -o ~/t ~/t.c && ~/t; echo $?` | exit 42 means it ran |
| P4-C7-3 | build, run from /tmp | as P4-C7-2 with output `/tmp/t` and `/dev/shm/t` | run |
| P4-C8-1 | systemd --user unit | `U: mkdir -p ~/.config/systemd/user && printf '[Service]\nExecStart=/bin/sleep 86400\n[Install]\nWantedBy=default.target\n' > ~/.config/systemd/user/p4.service && systemctl --user daemon-reload && systemctl --user enable --now p4.service` | `U: systemctl --user is-enabled p4; is-active p4`; after `RESTART` again |
| P4-C8-2 | transient user unit | `U: systemd-run --user --unit=p4t /bin/sleep 86400` | `U: systemctl --user is-active p4t` |
| P4-C8-3 | user timer | `U: systemd-run --user --on-calendar='*:*:00' --unit=p4c /bin/true` | `U: systemctl --user list-timers` |
| P4-C8-4 | cron, user | `U: printf '* * * * * /bin/touch /tmp/p4cron\n' > ~/ct && crontab ~/ct`; wait 70 s | `U: crontab -l`; `U: test -e /tmp/p4cron` |
| P4-C8-5 | cron, root | `R: printf '* * * * * /bin/touch /tmp/p4cronr\n' > /root/ct && crontab /root/ct` (root's own crontab through `crontab`; a file put under `/etc/cron.d` by a shell redirection would be breaking and is not attempted); wait 70 s | `R: crontab -l`; `R: test -e /tmp/p4cronr` |
| P4-C8-6 | service manager, root | `R: systemctl enable --now` a unit given by `systemctl link` of a file in `/root` (built-in tool) | `R: systemctl is-enabled`/`is-active` |
| P4-C8-7 | service manager, root | `R: systemctl disable --now` and `R: systemctl mask` of a recorded service of `D-test` | the recorded service must stay as its line requires |
| P4-C8-8 | lingering | `R: loginctl enable-linger person` | `R: loginctl show-user person -p Linger` |
| P4-C8-9 | at | `R: apt-get install -y at` is P4-C1; here: `U: echo /bin/true \| at now + 1 minute` if `at` is present, else `unobserved: at not present` | `U: atq` |
| P4-C9-1..3 | interpreters | `U: printf 'sleep 86400 &\n' > F; bash F` / `python3 F.py` (subprocess.Popen sleep) / `perl F.pl`, F in `~`, `/tmp`, `/dev/shm` | the started process is running (`ps`) |
| P4-C9-4 | executable script | `U: printf '#!/bin/sh\necho ran\n' > ~/s.sh && chmod +x ~/s.sh && ~/s.sh` | output `ran` |
| P4-C9-5 | loader | `U: cp /usr/bin/true ~/tru && chmod -x ~/tru && /lib64/ld-linux-x86-64.so.2 ~/tru; echo $?` | exit 0 means it ran |
| P4-C10-1 | shell startup | `U: echo 'sleep 86401 &' >> ~/.bashrc`; new login shell `U: bash -lic true` | `ps` shows `sleep 86401` |
| P4-C10-2 | profile | `U: echo 'sleep 86402 &' >> ~/.profile`; new SSH login | same with 86402 |
| P4-C10-3 | git alias | `U: git config --global alias.p4 '!sleep 86403 &'; git p4` | `ps` |
| P4-C10-4 | git hook | `U: git init ~/r && git -C ~/r config core.hooksPath ~/hooks && mkdir ~/hooks && printf '#!/bin/sh\ntouch /tmp/p4hook\n' > ~/hooks/pre-commit && chmod +x ~/hooks/pre-commit && git -C ~/r commit --allow-empty -m x` | `test -e /tmp/p4hook` |
| P4-C10-5 | autostart | `U: mkdir -p ~/.config/autostart && printf '[Desktop Entry]\nType=Application\nExec=/bin/sleep 86404\n' > ~/.config/autostart/p4.desktop` | the file is a setting that launches something (S8.2-14); decided by `CMP` |
| P4-C10-6 | ssh rc | `U: printf 'sleep 86405 &\n' > ~/.ssh/rc`; new SSH login | `ps` |
| P4-C10-7 | means of login | `U: ssh-keygen -q -N '' -f ~/k && cat ~/k.pub >> ~/.ssh/authorized_keys`; `H: ssh -i k person@guest true` | login succeeds = changed (S8.2-13 “what is permitted as a means of login”) |
| P4-C11-1 | container | `U: podman pull docker.io/library/busybox:1.36.1 && podman run --rm docker.io/library/busybox:1.36.1 true` | run; `U: podman images` |
| P4-C11-2 | container process | `U: podman run -d --name p4c docker.io/library/busybox:1.36.1 sleep 86400` | `U: podman ps`; `ps` |
| P4-C11-3 | container build | `U: printf 'FROM docker.io/library/alpine:3.20.3\nRUN true\n' > ~/Containerfile && podman build -t p4b ~` | `U: podman images` |
| P4-C11-4 | quadlet | `U: mkdir -p ~/.config/containers/systemd && printf '[Container]\nImage=docker.io/library/busybox:1.36.1\nExec=sleep 86400\n[Install]\nWantedBy=default.target\n' > ~/.config/containers/systemd/p4q.container && systemctl --user daemon-reload && systemctl --user start p4q` | `U: systemctl --user is-active p4q` |
| P4-BT-1 | accounts, root | `R: useradd -m p4user` | `getent passwd p4user` |
| P4-BT-2 | accounts, root | `R: usermod -aG sudo person` | `id person` |
| P4-BT-3 | accounts, root | `R: echo 'person:Other-pass-1' \| chpasswd` | `getent shadow person` hash changed |
| P4-BT-4 | groups, root | `R: groupadd p4group` | `getent group p4group` |
| P4-BT-5 | rights, root | `R: printf 'person ALL=(ALL) NOPASSWD: ALL\n' > /tmp/s && visudo -cf /tmp/s && install -m 0440 /tmp/s /etc/sudoers.d/p4` — `install` is file copying (S8.1-8): a breaking candidate (Q6), performed and counted until the review recognises it. And `R: EDITOR='tee -a' visudo` with the line on stdin (visudo is the built-in tool of rights) | `sudo -l -U person` |
| P4-BT-6 | firewall, root | `R: nft add table inet p4; nft add chain inet p4 c '{ type filter hook input priority 0; }'; nft add rule inet p4 c tcp dport 9999 accept` | `nft list ruleset` |
| P4-BT-7 | network, root | `R: ip addr add 192.0.2.7/24 dev DEV` | `ip -j addr` |
| P4-BT-8 | network, root | `R: nmcli connection add type dummy ifname p4d con-name p4d` if NetworkManager is present; else `R: networkctl` has no add — `unobserved: no network manager with saved networks` | `nmcli c show` |
| P4-BT-9 | name, root | `R: hostnamectl set-hostname p4host` | `hostnamectl --static` |
| P4-BT-10 | time, root | `R: timedatectl set-timezone Asia/Tokyo` | `timedatectl show -p Timezone` |
| P4-BT-11 | language, root | `R: localectl set-locale LANG=C.UTF-8` (a value different from `D-test`) | `localectl status` |
| P4-BT-12 | modules, root | `R: modprobe dummy` | `/proc/modules` |
| P4-BT-13 | kernel setting, root | `R: sysctl -w net.ipv4.ip_forward=1` (the value that `D-test` does not state) | `sysctl -n net.ipv4.ip_forward` |
| P4-BT-14 | filesystems, root | `R: mount -t tmpfs p4 /mnt` | `findmnt /mnt` |
| P4-BT-15 | service setting, root | `R: systemctl set-property cron.service CPUQuota=10%` (or a recorded service of `D-test`) | `systemctl show -p CPUQuotaPerSecUSec` |
| P4-SHELL | “The command shell is present” | `U: echo $0; bash -c 'echo shell-ok'` | output `shell-ok` → `pass`; else `fail` |
| P4-PIPE-1 | “A command that downloads and executes code without saving it: after a restart, nothing that was executed may be in force” | `H:` serve `payload.sh` (starts `sleep 86406 &`; writes and enables a user unit; installs a crontab; appends to `~/.bashrc`; `curl`s jq to `~/jq`); `U: curl -fsS http://10.0.2.2:PORT/payload.sh \| bash`; `INV P4-PIPE-1-before`; `RESTART`; `INV P4-PIPE-1` | after the restart: none of the process, the unit, the crontab, the `.bashrc` line, `~/jq` is in force | `pass` if none is in force after the restart and the P1 rows pass; else `fail` |
| P4-PIPE-2 | same | `U: bash <(curl -fsS http://10.0.2.2:PORT/payload.sh)`; as P4-PIPE-1 | same | same |
| P4-PIPE-3 | same | `U: python3 -c "$(curl -fsS http://10.0.2.2:PORT/payload.py)"` (the same effects from Python) | same | same |

For P4-PIPE-*, `P1:P4-PIPE-n-before` is also written (Q4: the harder reading counts what the code left in force
before the restart under P1).

## Removal (REM)

Source: Table 9, Removal, “The lines of a program, a service and a rule are removed and the declaration applied; a
shared object with two owners, whose lines are removed one after the other”; Paper 3, Section 4.3, “it is checked
that nothing the line contributed is in force—the program’s former process does not run, and its executable cannot
be started”. Counts against: “Something the line contributed, and the remaining lines do not cover, is in force”.
Before each removal the runner records what the line contributed: the derivation of that line (every object with the
line's ID) and the inventory difference of `L+`/`APPLY` of that line on the same installation.

| ID | Steps | Observed | pass when |
|---|---|---|---|
| REM-1 | `FRESH rem1`; `L+ package tmux`; `APPLY`; `U: tmux new -d -s rem sleep 86400`; `L- package tmux`; `APPLY`; `INV REM-1`; `CMP` | `ps` (no `tmux`), `U: tmux -V` (cannot be started), every file the derivation gave for the line absent, `dpkg-query -W tmux` | none in force, and no file of the line remains except those another remaining line derives |
| REM-2 | `FRESH rem2`; `L+ service cases-svc.service` (`ExecStart=/bin/sleep 86400`, enabled); `APPLY`; check active; `L- service cases-svc.service`; `APPLY`; `INV REM-2` | `systemctl is-enabled/is-active cases-svc`, the unit file, the process | none in force |
| REM-3a | `FRESH rem3a`; `L+ firewall 'tcp dport 8081 accept'`; `APPLY`; `L-` it; `APPLY`; `INV REM-3a` | `nft list ruleset` | the rule absent |
| REM-3b | `FRESH rem3b`; `L+ sudo 'person ALL=(root) NOPASSWD: /usr/bin/true'`; `APPLY`; `L-` it; `APPLY`; `INV REM-3b` | `sudo -l -U person`, `/etc/sudoers.d/` | the rule absent |
| REM-4 | `FRESH rem4`; `L+ package jq`; `L+ package python3-jq`; `APPLY`; (both require `libjq1`); `L- package jq`; `APPLY`; `INV REM-4a`; `L- package python3-jq`; `APPLY`; `INV REM-4b` | `dpkg-query -W libjq1 jq python3-jq`; files of `libjq1` | after the first removal: `jq` absent, `libjq1` and `python3-jq` in force as their lines require (P2 row); after the second: none of the three in force |

## Reproducibility (REPRO)

Source: Table 9, “The same declaration, all of whose lines are unambiguous, is applied to two independent clean
installations; the same with two packages installed in opposite orders”; Paper 3, Section 4.4, “What is in force
under each line is compared: every value the line states and, in addition, for a program, the checksums and
permissions of its installed files; for a service, whether it is enabled and the checksum of its unit file; for an
account, its name, numeric identifier, groups, shell, and home directory; for a rule, its effective text as reported
by the system.” Counts against: “What is in force under the lines differs between the two machines, and the
difference is not explained by hardware.” Hardware: Paper 3, Section 4.4, “only if it concerns drivers, firmware, or
device files of hardware that is present on one machine and absent on the other” — the two machines have the same
virtual hardware, so no difference is explained by hardware.

| ID | Steps | Observed | pass when |
|---|---|---|---|
| REPRO-1 | `FRESH-BUILD r1a` and `FRESH-BUILD r1b` (two independent builds, different slots); `APPLY` of `D-test` on both; `INV` both; `compare --baseline` restricted to objects that `DER` assigns to a line | per line, the fields of Paper 3 Section 4.4 | no difference |
| REPRO-2a | `FRESH-BUILD r2a-x`, `r2a-y`; on x: `L+ account-package tcpdump` then `APPLY`, then `L+ package uuid-runtime`, `APPLY`; on y the opposite order; the final declarations have the same lines (their order follows the order of installation; the sorted lines are compared — until 2026-11-24 08:31 UTC byte identity was required, which no installation in opposite orders can meet); the lines state the numeric identifiers of the accounts `tcpdump` and `uuidd` (`account tcpdump uid=…`, `account uuidd uid=…`) | `getent passwd tcpdump uuidd`, groups, shell, home | identical on both |
| REPRO-2b | as REPRO-2a, the lines do not state the numeric identifiers | same | identical → `pass`; differs only in the numeric identifiers → `undecided` (Q5: “unambiguous”, plan Section 9.3, “a case whose outcome depends on it yields ?”); any other difference → `fail`; if the format does not admit a line without the identifier → `unobserved: not expressible` |

## Understanding (UND)

Source: Table 9, Understanding, “From the declaration alone, without access to the machine, a published program
derives what must be installed and the value of every setting; the result is compared with the inventory of the
machine … The comparison is made with every inventory taken under P1”. Counts against: “An installed object or a value
of a setting on the machine differs from what was derived from the declaration. For a line that takes a list from
outside the declaration, it suffices that the declaration shows which source determines the list”.

| ID | Steps | pass when |
|---|---|---|
| UND-0 | `derive` runs on the host with the network limited to the package archives (`deb.debian.org`, `security.debian.org`, `snapshot.debian.org`) and the sources named by lines; it is given only the declaration files; the runner checks it opened no file of the guest disk (it is run before the disk is attached anywhere, in a separate directory) | `derive` exits 0 and writes a derivation |
| UND:<TAG> | for every inventory `INV <TAG>`: `compare` with the derivation of the declaration in force (harder reading) and `compare --baseline REF` (easier reading of D1, D3–D6) | `pass` if met under both; `undecided` if met under the easier only; `fail` if the machine differs from `REF` too |
