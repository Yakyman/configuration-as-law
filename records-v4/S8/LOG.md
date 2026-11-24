# S8 log — supplement 1, step 8, second party (performer)

All times UTC. Paths relative to the night folder unless stated; server paths relative to the laboratory
`VMs/cal-1123/stand/` of the server account.

## 18:36–18:39 checksums before the first history

- Gate (not published: orchestration or scratch): commit `7cda06364e14…`, CASES-8.md `72f8a2f2…df446`, OBSERVE-8.md `29b0c7f2…f0af7`.
- Public remote `main` = `7cda06364e1428e9c75eac62a25531aee710131c` (`S8/raw/checksums/public-remote-main.txt`).
- Public bytes fetched from the public record at that commit: CASES-8.md, OBSERVE-8.md, inputs-seal.json, run.py,
  observe.py hash as committed (`S8/raw/checksums/public-raw-fetch.txt`).
- All 41 committed files: public commit = local `B2/` copy = server copy (`S8/raw/checksums/committed-41-files.txt`).
- Server: image `base/stand.qcow2` = `1b581030…ca980eca` (named at the top of CASES-8.md), declaration
  `2e6946a8…cd79b4a`, CASES-8.md and OBSERVE-8.md as in the gate (`S8/raw/checksums/server-image-and-documents.sha256`);
  198 sealed files, 0 mismatches; image mode 0444.
- Result: no checksum differs. Histories may run.
- `raw/step-8-second-party/` did not exist on the server before (no earlier attempt); no guest `s8-second-*` existed.

## Publication receipt

`cases-8/publication.json` written on the server (outside the seal, as CASES-8.md requires) after the checks above:
public record URL of the step-8 folder at commit `7cda063…`, that commit, inputs seal SHA-256 `68d5a18c…12c0ed`,
`operator_verified_published_bytes: true`.

## History 1 — expected observation, written before the run (18:39, appended immediately before the launch at 18:39:08)

Sources: committed expectation of `SUP1/step-8.md`; `check-inputs-v4/supplement-1/step-8-cases/B2/cases-8/h1/PREPARATION.md` (source assessment of the builder).
- Update 1 (`apt-get upgrade --stand-catalog ed`): exit 0, ed 1.21.1-1 immediately; restart 1 changes boot ID and access
  returns; at `h1-after-restart-1` ed 1.21.1-1, nothing in force unrecorded, every line fulfilled (step-8 expectation).
- Update 2 (root `dpkg --install` ed 1.22.5-1): exit 0 and ed 1.22.5-1 immediately; PREPARATION.md predicts from
  source (`system_channels.activate`) that the restart replay restores ed 1.21.1-1, so at `h1-after-restart-2` and
  `h1-end` ed 1.21.1-1, and the second update is done immediately but does not persist. Whether the native install
  wrote the declaration between update 2 and restart 2 is not observed by any committed point (none is prescribed there).
- Declaration lines: grows by the catalog update's state change (step-8 expectation: “the declaration will grow with
  every file a history saves”); no other expected count is sourced.
- 18:39:08 launched `s8-second-h1` with the exact CASES-8.md commands (`S8/raw/h1-launch.txt`).

## History 2 — expected observation, written before its run (18:45, while history 1 runs)

Sources: committed expectation of `SUP1/step-8.md`; `check-inputs-v4/supplement-1/step-8-cases/B2/cases-8/h2/README.md` (tools are recipe components; no
prerequisite installation). Expected: all 18 actions done (3 fetches, 3 one-line edits, 6 builds, 6 runs, each output
checksum as committed); at `h2-end` nothing in force unrecorded and every line fulfilled; the declaration grows with
every saved file (home filesystem declaration: `step8-h2/hello.c`, `source.json`, `output-*.txt`, `h2-hello.built.json`;
machine declaration: the admitted source/result line(s) of `h2-hello`). No exact count is sourced.

## History 3 — expected observation, written before its run (18:47, while history 1 runs)

Sources: committed expectation of `SUP1/step-8.md` (“the game history will not be performable on the image”);
`B2/raw/step-8-prep/h3/preparation.md` (source prediction: native `dpkg --install` of the 15 prerequisites is not
admitted into the ordinary shell's execution policy, `B2/build/codeboundary.py`, `B2/build/shell_boundary.py`; the
downloaded `etded` lands on the `noexec` home filesystem, `B2/build/bc3_filesystem.py`, `B2/build/noexec.py`).
Expected: prerequisites fetch/install/readback done as root (exit 0); then the first launcher command that executes a
newly installed native program (e.g. `tmux`, `jq`, `bzip2`) or the game executable is refused; game not installed and/or
not started; history not performable → “?”. Whether root `dpkg --install` of 15 packages records them in the
declaration is exactly what the end observation shows; the step-8 expectation is “nothing in force unrecorded”.

## History 4 — expected observation, written before its run (18:48, while history 1 runs)

Sources: committed expectation of `SUP1/step-8.md`; `check-inputs-v4/supplement-1/step-8-cases/B2/cases-8/h4/README.md` (install artifact carries its bytes;
`stand-build` is a local compiler invocation, “they need not fail merely because the link is down”).
Expected: artifact checksum verified; cut lands while `stand-pkg install` is active (`valid_cut` true); install exits 0
while disconnected; disconnected observation collected; restore; worker runs; development prefix (fetch with network
up) done; cut during `stand-build`, build exits 0 while disconnected; observation; restore; suffix completes all
remaining h2 actions. At every point nothing in force unrecorded and every line fulfilled; declaration grows
(dev-worker line, h2-hello lines, home files). No exact count is sourced.
- 18:48 history 1 finished (service inactive, ExecMainStatus=0); history 2 launched with the exact CASES-8.md command (`S8/raw/h2-launch.txt`).
- 18:56 history 2 finished (inactive, ExecMainStatus=0); history 3 launched with the exact CASES-8.md command (`S8/raw/h3-launch.txt`).
- 19:00 history 3 finished (inactive, ExecMainStatus=0); history 4 launched with the exact CASES-8.md command (`S8/raw/h4-launch.txt`).

## Results as observed (after each run; see RECORD.md)

- 18:47 History 1: update 1 exit 0 with SUCCESS; restart 1 new boot ID; update 2 (root dpkg) exit 0, ed 1.22.5-1 read
  back, no SUCCESS; restart 2 new boot ID; after restart 2 ed 1.21.1-1 again; three observations collected, stable.
  Differs from the expectation: the second update did not persist (as the builder's source prediction said) and was not
  recorded while in force.
- 18:56 History 2: all 18 actions done, 12 SUCCESS applications; end observation collected, stable. As expected.
- 18:59 History 3: prerequisites installed by root dpkg (exit 0), not recorded in the machine declaration; launcher
  `auto-install` failed with `/usr/bin/jq: Permission denied`; game not installed. Not performable, as expected.
  Unexpected: line `base` no longer fulfilled for `/etc/ld.so.cache` and `/etc/shells`.
- 19:03 History 4: valid cut during `stand-pkg install`; install exit 1 (`readback mismatch: port:udp:1`); disconnected
  observation collected but the `/etc` declaration changed during it; after restoration every new session exited 255
  (`/run/stand-ready` absent); retry, worker, development not performed. Differs from the expectation (install expected
  to succeed offline).
- 19:04–19:10 Offline reading of the saved observations with `S8/tools/` (no further guest, no repeated history).
  Server: no guest, no unit left; my helper files removed; the controller's outputs stay under the laboratory's
  `raw/step-8-second-party/`.

## Correction FX-S8-O-1 (appended; the lines above are unchanged)

- The end time “19:10” above is wrong: the last writes of the first record were `RECORD.md` 19:08:36, `LOG.md` 19:08:55
  and `QUESTIONS.md` 19:09:08 UTC (file modification times); the offline reading ended by 19:09 UTC.
- The record was corrected from the existing raw files after review RV-S8-O (`REVIEW.md`); see `FIX-S8-O-1.md`. No
  history was performed again and no machine was started.
