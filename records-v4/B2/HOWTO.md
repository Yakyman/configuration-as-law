# Round 4 operating handoff: supplement 1, step 6 preparation

Use (not published: record outside this collection) for the exact image/declaration hashes, publication gate, fresh-copy procedure, opposite installation orders, removal commands and cleanup. (not published: record outside this collection) fixes the native queries. The builder has not executed the second-party runner. Current `base/stand.qcow2` is the BC4 image; the previous step-5 image is retained as `base/stand-step5.qcow2`. Follow each document's image identity rather than treating historical commands below as current case instructions.

The final recipe is `build/build.py`. For an explicitly planned later rebuild in a separate laboratory copy with the same pinned input caches, `python3 build/bc4-build.py final-2` performs a scratch build under an unused output name; run long work through a user service. This command is not a reason to overwrite the sealed candidate before independent attempts. Complete bundle application is `python3 -B /usr/local/lib/stand/bc4_bundle.py apply DIRECTORY`, where DIRECTORY supplies exact `declaration.json` and `blobs.json`; it is a general root application interface for the existing complete format. Its limitations are in BUILD-4.

# Round 3 operating instructions: supplement 1, step 5

The current image implements the seventeen committed cases in
(not published: record outside this collection). That document fixes the image and complete declaration
identities, the exact original commands, fixtures, observations and the
second-party procedure: one fresh copy per case. Follow its publication gate
before starting independent attempts. The builder's results are in
[BUILD-3.md](BUILD-3.md); the older instructions below describe earlier rounds.

The shell is still ordinary Bash. Saving a file in `/home/stand`, `/tmp`,
`/var/tmp`, `/dev/shm` or `/etc` now requests a declaration transaction in the
filesystem service. The service records intended bytes and metadata and publishes
the successful generation before a reader can obtain those bytes. It does this
for documents as well as code; recording optional material does not reclassify
it as a mandatory installed program. The fifteen saved-code commands therefore
can execute successfully through automatic recording. Native `/usr/sbin/useradd`
is unchanged; its writes to the mediated account databases also produce own
account/group/setting requirements.

## Complete declaration and readback

`/etc/stand/bc3-primary.json` designates one description composed of the original
`/var/lib/stand/current/machine.jsonl` and five filesystem declarations at
`/var/lib/stand-fs/{home,tmp,vartmp,shm,etc}/current/declaration.json`.
Each filesystem generation has a matching `success.json`; `audit.jsonl` records
its mutation identity. These audits are evidence, not substitutes for the primary
declaration. `base-files.json` is the original declaration's referenced manifest.

Inside a disposable guest, export and verify the description with:

```sh
python3 -B /usr/local/lib/stand/bc3-state.py export
python3 -B /usr/local/lib/stand/bc3-state.py verify
stand-verify
```

The filesystem verifier reads declared path bytes, modes, owners/groups and
symlink targets and checks successful-generation identities. It reports a
concurrent generation change as inconclusive failure. It does not establish a
complete object census, verify every orphan/backing blob, or independently
recompute account semantics. `stand-verify` separately checks the original
machine declaration. Neither command alone establishes whole-system P1/P2/P4.

## Rebuild and run the whole builder suite

All commands run on the server from `VMs/cal-1123/stand/`, relative to the server
account's initial directory. Preserve the frozen final image for independent
attempts; rebuilds belong in a separate laboratory directory prepared with the
same recipe and retained input cache. The full recipe is `build/build.py` with
the sources in `build/`; the actual binary-input checksums are retained in
`downloads/packages.sha256` and exported with the Round 3 evidence. The two new
fixed FUSE package inputs and their official download URLs are specified by
`tools/bc3-inputs.py`. Run it before reusing an earlier-round package cache.

The following is the reproducible builder sequence. Use an unused phase name
accepted by the controllers, wait for each service's completion and inspect its
exit status before starting the next. Each controller refuses an existing phase
directory. Use the network fixture from CASES-5 during validation.

```sh
python3 tools/bc3-inputs.py
systemd-run --user --unit=bc3-build-replay --property=WorkingDirectory="$PWD" --setenv=PYTHONDONTWRITEBYTECODE=1 python3 tools/bc3-build.py final-2
# After the build service succeeds:
systemd-run --user --unit=bc3-validate-replay --property=WorkingDirectory="$PWD" --setenv=PYTHONDONTWRITEBYTECODE=1 python3 tools/bc3-validation.py final-2
# Read-only export of the frozen image; it does not boot or mutate the base:
systemd-run --user --unit=bc3-export-replay --property=WorkingDirectory="$PWD" --setenv=PYTHONDONTWRITEBYTECODE=1 python3 tools/bc3-export-image.py final-2
```

The validation builds an independent temporary peer, runs all seventeen current
cases plus the complete carried component/channel/transaction/reboot suites,
then replays the combined example on both builds. It retains raw false and
unavailable observations. The older saved-code checks inspect only the original
machine declaration and expect marker suppression; they do not recognize the
new automatically recorded filesystem declarations. Read their raw findings
alongside the scoped seventeen-case evidence rather than treating an exit code
as a closure count. Every VM holds the shared slot lock, and owned overlays and
the temporary peer are destroyed at completion.

The recorded final full-suite invocation fails in the carried code/lifecycle
scenario when its fixture calls `mkfifo` in the mediated home directory. The
filesystem does not implement named special nodes. The unchanged original log
contains 73 observations and then the setup exception; it is not a complete pass.
A separately recorded continuation executes the 59 still-available suffix
observations with unchanged commands, explicitly retaining the unavailable FIFO
case. Its plan, source and results are linked from SELFTEST. This continuation is
builder evidence and does not change the seventeen commands in CASES-5.

The filesystem implementation does not support every Linux filesystem operation;
in particular shared writable mappings, special nodes and full ACL handling are
outside this bounded claim. Retained backing-version coverage and publication
ordering limits are discussed in [ARGUMENT-5.md](ARGUMENT-5.md). Reading choices
are preserved in [QUESTIONS-5.md](QUESTIONS-5.md), without selecting an authorial
interpretation.

# Historical Round 2 operating instructions

Recorded 2026-11-23 UTC. Round 2 extends the finite format and supplies a separate
ordered version 4 inventory. Results and exact retained-image identity are in
[BUILD-2.md](BUILD-2.md) and [SELFTEST.md](SELFTEST.md). The complete recipe remains
in `build/`. The operations below run inside disposable server guests; host
commands run from `VMs/cal-1123/stand/` relative to the account's initial directory.

The round 2 exports are (not published: record outside selected evidence) and
(not published: record outside selected evidence). The factory has 553 rows; the combined
candidate has 578 rows, including the six new rows listed in
[the assembly record](raw/round-2/final-1/complete-example.json). Use the full
combined directory, including its manifest, for replay. Individual channel
exports do not include every round 2 row and are not the complete example.

## Ordered object census

```sh
python3 lab.py new object-check stand
printf 'stand-inventory --v4\n' | python3 lab.py run object-check
```

The command first enumerates actual files, native installed package identities,
accounts, groups, enabled system units, the supported kernel setting and runtime
observations. It then matches declaration requirements. `FACT_UNKNOWN` means
the required semantic/provenance fact was not obtained; it never means covered.
Runtime objects are diagnostic, with creator coverage where established.
Exit 1 means uncovered/mismatching required objects were observed; exit 2 means
an incomplete census without such a mismatch; neither is a hypothesis outcome 0.
The historical `stand-inventory` entry retains its original criterion for the
unchanged regression fixture; use `--v4` for version 4 decisions.

## Exact package and generated-object rows

Existing `program`/`code` rows optionally carry `package_identity` with backend,
name and version. Factory native identities additionally include architecture.
The finite `stand` installer supports packages without files and exact package
dependencies via `package_dependencies`. Its protected registration database is
`/var/lib/stand/objects.json`. Native package state is read from the native
installer independently. Native file delivery receipts are not established by
the factory capture, so their first-question classification remains unknown.

`derivations` names a source path, output path and `copy` or `python-bytecode`
algorithm. Both files have exact required bytes and metadata. Admission checks
the source/output relationship; application actually runs the producer; inventory
matches the saved provenance against the single census snapshot. A generated
unit uses `derived_from` with source line, source path and `algorithm: copy`.
Its own service row still records the chosen enabled/active state.

The installed helper prints complete fixture rows using the guest's recorded
interpreter, so generated bytecode corresponds to that exact Python version:

```sh
printf 'python3 -B /usr/local/lib/stand/v4-object-fixtures.py\n' | python3 lab.py run object-check --root
```

Do not treat the printed array as a complete machine declaration. Install a
selected row through `stand-line add ROW.json`, or include the exact rows in a
complete candidate. The complete example exported for round 2 adds those rows
to the assembled complete declaration before replay on both independent builds.

## Chosen system value

One additional finite setting reader is implemented:

```json
{"id":"example:printk","type":"setting","managed":true,"reader":"sysctl","name":"kernel.printk","value":"4 4 1 7"}
```

`stand-line add` applies the value and `stand-verify` reads the actual kernel
interface. Unsupported names/value shapes refuse. Removal retains a visible
residual provenance record; it does not invent a restore value. The round 2
fixture explicitly restores its original value before removing the line.

## Rebuild and test this round

`tools/round2.py` accepts single-use development/final phase names and refuses an
existing output directory. It freezes the recipe/controller inputs, rebuilds
from scratch, runs the object suite and reboot/readback, and for final phases
runs the complete carried and version 4 suites plus independent-build replay.
The final controller schedules at most three independent guest branches at once;
all guests still hold the shared nonblocking slot locks. Run long jobs under a
user service using the pattern below with an unused phase name:

```sh
systemd-run --user --unit=cal-1123-stand-bc2-final-3 \
  --property=WorkingDirectory="$PWD" \
  --property=StandardOutput=append:"$PWD/raw/round-2/final-3-controller.log" \
  --property=StandardError=append:"$PWD/raw/round-2/final-3-controller.log" \
  --setenv=PYTHONDONTWRITEBYTECODE=1 python3 tools/round2.py final-3
```

The new suite lives at `/usr/local/lib/stand/v4-objects-selftest.py`. Its raw
censuses and exact fixture rows are exported from `/var/lib/stand/round2-evidence`.
Read assertion records as well as controller exits: boundary failures remain
failures even when the fixture continues observing later cases. Browser/WASI
capability cases without supplied executable fixtures are UNTESTED, not refusals.
Destroy the example guest when finished: `python3 lab.py destroy object-check`.

The saved final run is `raw/round-2/final-1/`; its recipe/controller snapshots
and hashes fix the tested inputs. After exporting the final logs and example,
run the offline audit from the night workspace:

```sh
python3 -B B2/raw/round-2/audit.py --output B2/raw/round-2/audit-final-1.json
```

Audit exit 0 means that the required saved evidence is complete and consistent.
It does not turn retained false or UNTESTED observations into passes. Exit 1
means inconsistent evidence; exit 2 means required evidence is missing. The
[transport correction](raw/round-2/AUDIT-TRANSPORT.md) and its
[review](raw/round-2/REVIEW-AUDIT.md) document comparison of systemd dependency
tokens without imposing an execution order on their printed enumeration.

## Retained round 1 interface instructions

Recorded 2026-11-23 UTC. The testbed supplies an ordinary Bash shell and
additional declaration-writing tools. The final recipe was rebuilt from scratch
and tested on fresh guests. Component checks, the whole carried suite and
independent-build comparison completed; the final combined replay is recorded
in [SELFTEST.md](SELFTEST.md). Saved-code and privileged native-tool failures
remain explicit. This is a partial testbed; hypothesis outcome: `?`.

## Work directory and disposable machines

Run VM and build commands on the server only, from `VMs/cal-1123/stand/` relative
to its account's initial directory. The local source and exported evidence are
under `B2/`. Do not run these commands in the previous night's directory. No
host sudo is required.

```sh
cd VMs/cal-1123/stand
python3 lab.py new example stand
cat <<'GUEST' | python3 lab.py run example
message="two words"
printf '%s\n' "$message" | tr a-z A-Z > document.txt
cat document.txt
GUEST
printf 'stand-verify\n' | python3 lab.py run example
python3 lab.py stop example
python3 lab.py start example
python3 lab.py destroy example
python3 lab.py list
```

By default `lab.py run` sends ordinary command text to the guest's login shell.
The ordinary `stand-shell` entry runs Bash with quoting, pipelines, redirections,
functions and arguments. It is no longer the tab-separated request protocol.
QEMU uses a shared nonblocking slot lock, a user service, 4 GiB memory and two
virtual CPUs. Destroy disposable guests when finished.

`lab.py run example --root` uses the separate laboratory credential and sends a
root shell script. This is actual privileged execution; it is not evidence that
the ordinary user has unrestricted sudo. Ordinary public mutation frontends
internally request their specifically authorized broker command.

Explicit legacy compatibility remains available for old suites. If the guest
from the first example was destroyed, create a fresh guest before this command:

```sh
python3 lab.py new example stand
printf 'broker\tstand-verify\n' | STAND_LEGACY=1 python3 lab.py run example
```

Set `STAND_LEGACY=1` only for intentionally preserved structured inputs. In
`v4-suite-adapter.py`, old broker requests become Bash commands, while old `run`
requests remain sealed `stand-session` launches inside Bash. Such launch refusals
must not be described as proof about arbitrary Bash interpreter inputs.

## Install, update and remove exact artifacts

After creating a fresh guest:

```sh
cat <<'GUEST' | python3 lab.py run example
stand-pkg install /usr/local/share/stand/dev/worker-1.json
/opt/stand/pkgs/dev-worker/bin/worker
stand-pkg update /usr/local/share/stand/dev/worker-3.json
stand-pkg downgrade /usr/local/share/stand/dev/worker-1.json
stand-pkg reinstall /usr/local/share/stand/dev/worker-1.json
stand-compare --snapshot -
stand-pkg remove dev-worker
GUEST
```

`reinstall` and `downgrade` are exact desired-state selection aliases for
`install` on `stand-pkg`, `apt` and `apt-get`. They require a supported artifact;
apt variants also accept exact catalog package/version selection. They do not
make arbitrary versions or native package-manager flags supported. The complete
candidate is applied before `SUCCESS <generation>`; `/var/lib/stand/current`
selects the declaration and `/var/lib/stand/last-success.json` identifies the
last durable successful application. Use `stand-verify` for every-line readback.

The shell suite demonstrates an exact recorded personal Bash script with an
explicit interpreter entry and arguments. Command text itself is not recorded
as a declaration line. Ordinary documents do not acquire a mandatory line just
because they were written through the shell.

## Record and run a personal script

This uses the same exact script/interpreter row exercised by the shell suite.
The ordinary command creates the declaration input, then the installer applies
it before the script is started:

```sh
cat <<'GUEST' | python3 lab.py run example
python3 -B - <<'PYTHON'
import base64, hashlib, json, pathlib
payload = b'#!/usr/bin/bash\nprintf "Hello, %s\\n" "$1"\n'
entry = '/opt/stand/pkgs/personal-example/bin/hello'
row = {'id':'personal-example', 'type':'code', 'managed':True,
       'version':'1', 'source':'user:personal-script',
       'entrypoints':[{'path':entry, 'interpreter':'/usr/bin/bash'}],
       'files':[{'path':entry, 'kind':'file', 'mode':493, 'uid':0, 'gid':0,
                 'sha256':hashlib.sha256(payload).hexdigest(),
                 'content_b64':base64.b64encode(payload).decode()}]}
pathlib.Path('personal.json').write_text(json.dumps(row)+'\n')
PYTHON
stand-pkg install personal.json
/opt/stand/pkgs/personal-example/bin/hello 'ordinary argument'
stand-pkg remove personal-example
GUEST
```

## Typed configuration tools

The public APIs use `TOOL add ROW.json` and `TOOL remove ID`:

| Tool | Supported row kinds |
|---|---|
| useradd, usermod | account |
| userdel | account removal only |
| groupadd | independent group |
| groupdel | independent group removal only |
| systemctl | service, timer, socket |
| systemd-run | service, timer |
| crontab, at | timer |
| nft | rule |
| nmcli | wifi |
| bluetoothctl | bluetooth |

Rows must be managed, validate against the finite schema, and preserve factory
requirements. Removal requires an existing managed row of the correct kind.
Account rows continue to include their own primary group. Independent group
rows require a supported name, GID 1100–60000 and empty `members`; they cannot
conflict with an account's group. These are finite typed interfaces, not full
native CLI compatibility.

```sh
cat <<'GUEST' | python3 lab.py run example
useradd add /usr/local/share/stand/dev/account.json
stand-verify
userdel remove dev-account
nft add /usr/local/share/stand/dev/rule.json
nft remove dev-rule
GUEST
```

For jobs, declare the executable first, then the service, then its timer or
socket. Remove the timer/socket before removing its service. The existing
`crontab add` schedule specification, `systemctl --user add`, and
`systemd-run --user add-timer` interfaces remain available. Saved Wi-Fi and
prepared Bluetooth rows demonstrate profile state, not connection or pairing.

## Document editing and integrated installation

```sh
cat <<'GUEST' | python3 lab.py run example
printf 'First line\n' | v4-editor write document.txt
printf 'Second line\n' | v4-editor append document.txt
v4-editor read document.txt
v4-editor package-install /usr/local/share/stand/dev/worker-1.json
/opt/stand/pkgs/dev-worker/bin/worker
v4-editor package-remove dev-worker
GUEST
```

Document operations retain the invoking identity. `package-install` and
`package-remove` use the common `stand-pkg` broker, including when the editor is
invoked as actual root. Document editing receives no extra sudo grant. The
ordinary Bash shell also permits normal `ed` editing and passive `w3m` browser
work demonstrated in the shell suite.

## Application pause and caller restoration

The current transaction gate uses cgroup v2 freezing rather than job-control
stop signals. It journals each original cgroup and its private `.stand-freeze`
child in `/run/stand-shell-paused.json`, waits for kernel `frozen=1`
acknowledgement, and restores surviving tasks to their original cgroups after
successful publication or successful rollback. The private children and journal
are removed. Ordinary Python callers may retain `subprocess.run()` while their
broker child applies a declaration; the unchanged editor uses this same path.

The final-2 gate tests verify a frozen heartbeat, refusal of new entry while
pending, exact readback, and nested broker/editor caller restoration. These
finite successes do not establish every process race or cgroup topology. The
prior final-1 SIGSTOP caller stall remains in the evidence; it is not the current
mechanism and is not represented as a successful full run.

## Rebuild and validation

The complete recipe includes the shell launcher/policy, typed adapters, editor,
and new test suites. A planned rebuild uses:

```sh
python3 build/build.py --server --replace
```

`--replace` explicitly replaces the retained candidate image. It is appropriate
for a planned new build phase, not for overwriting completed evidence. Freeze
source inputs and expectations before each such phase. The controller
`tools/round1.py` currently accepts only `development-1`, `final-1`, `final-2`,
and `final-3`, refuses an existing output directory, and runs the full build,
new suites, independent peer build, carried regression suite and combined replay.
Never re-run a consumed phase name or delete its evidence to permit a repeat.

Long validation jobs run under a user service so they survive the initiating
terminal. For a newly authorized build phase with unused output names:

```sh
systemd-run --user --unit=cal-1123-stand-bc1-final-3 \
  --property=WorkingDirectory="$PWD" \
  --property=StandardOutput=append:"$PWD/raw/round-1/final-3-controller.log" \
  --property=StandardError=append:"$PWD/raw/round-1/final-3-controller.log" \
  --setenv=PYTHONDONTWRITEBYTECODE=1 \
  python3 tools/round1.py final-3
```

For a fresh disposable guest, the new guest suites can be invoked individually:

```sh
python3 lab.py new shell-check stand
printf 'python3 -B /usr/local/lib/stand/v4-shell-selftest.py\n' | python3 lab.py run shell-check --root
python3 lab.py stop shell-check
python3 lab.py start shell-check
printf 'python3 -B /usr/local/lib/stand/v4-shell-selftest.py --after\n' | python3 lab.py run shell-check --root
python3 lab.py destroy shell-check
python3 lab.py new tools-check stand
printf 'python3 -B /usr/local/lib/stand/v4-tools-selftest.py\n' | python3 lab.py run tools-check --root
python3 lab.py destroy tools-check
python3 lab.py new gate-check stand
printf 'python3 -B /usr/local/lib/stand/v4-gate-selftest.py\n' | python3 lab.py run gate-check --root
python3 lab.py destroy gate-check
```

Capture stdout/stderr in the preselected fresh evidence directory; the controller
already does this. These individual commands are the mechanics, not a reason to
repeat an answered experiment. The shell's post-reboot phase is mandatory for its
unsaved-execution test. Complete validation also requires the carried channel
suite and combined declaration replay; the new component suites do not replace
those stages. Controller evidence is under `raw/round-1/PHASE/`, including source
hashes, image identities, expected commands, exits, shell/tools/gate logs,
`carried-suite/`, `combined/` and `summary.json` when the stages complete.

The separate supplementary probes use host-controlled Python payloads, not
new installed components. The final-2 executed originals and hashes are retained in
`raw/round-1/final-2-supplement-inputs/`; the earlier final-1 payloads remain
in `raw/round-1/supplement-inputs/`. The current extra payload has a corrected
output-marker detector. To include these probes in a new planned validation:

```sh
python3 lab.py new extra-check stand
cat tools/v4-direct-selftest.py | python3 lab.py run extra-check --root
cat tools/v4-extra-selftest.py | python3 lab.py run extra-check --root
printf 'stand-verify\ncat /var/lib/stand/last-success.json\n' | python3 lab.py run extra-check --root
python3 lab.py stop extra-check
python3 lab.py start extra-check
printf 'stand-verify\ncat /var/lib/stand/last-success.json\n' | python3 lab.py run extra-check --root
python3 lab.py destroy extra-check
```

Save and compare both readback/report outputs. The one-shot `supplement1.py`
controller accepts an unused phase argument, for example
`python3 tools/supplement1.py final-3`, after that phase's rebuilt image is
ready. It records frozen inputs, separate before/after logs and byte comparison.
Consumed output names cannot be reused. The supplementary controller's zero exit denotes completed observation;
failed property rows and unavailable routes remain explicit.

## Completed component evidence and frozen supplemental inputs

Historical Round 1 component evidence is under `raw/round-1/final-2/`: `shell.jsonl`,
`shell-reboot.jsonl`, `gate.jsonl`, `tools.jsonl` and their verification files.
The tool log contains 85 successful implementation rows and one separately
failed `root-native-account-bypass`; the gate log contains nine passing rows.
Both end with 553 clean final readback rows.

The executed final-2 host-controlled payloads are retained in
`raw/round-1/final-2-supplement-inputs/`. Their source hashes are in
`raw/round-1/final-2-supplement-source-sha256.json` and match
`raw/round-1/final-2/supplement/input-sha256.json`. The installed image recipe
is unchanged by these external test payloads. The supplement controller runs
those recorded payloads through actual ordinary Bash on a fresh overlay:

```sh
python3 tools/supplement1.py final-2
```

That phase has already completed; the command documents the recorded invocation,
not a request to repeat it. Run a long planned controller through a user service
so it survives the initiating terminal. Both main and supplemental controllers
refuse an existing output directory. For a later authorized validation phase,
freeze its source bytes and use its own unused phase name; do not overwrite or
silently substitute payloads in the recorded final-2 evidence.

The final-2 supplement has five direct-shell and four extra-suite saved-input
failures. Its before/after reboot verification files contain the same 553 `OK`
rows and are byte-identical; successful report bytes also match. Its owned guest
was destroyed. Those facts establish finite continuity and cleanup, not closure.

The historical `supplement-marker-audit.json` concerns final-1: a substring
matcher falsely called a denied FFI mapping an execution because a traceback
echoed source text. The offline audit reran no command. The corrected detector
was later frozen in the mandatory final-2 rebuilt-image validation after the
general freezer change; this was not a repeat solely for detector correction.
Final-2 correctly records `SAVED-FFI` as denied with no executed marker.

Round 1 closure decisions and their separate review are recorded in
[BUILD-1.md](BUILD-1.md) and [STAND.md](STAND.md). Component counts alone do not
establish whole-testbed closure.

## Reading partial results honestly

A zero implementation-check exit does not mean the v4 boundary is complete.
Saved script, saved pipe, source, startup, import and serialized-code probes are
separately retained boundary observations. The Bash shell can read material and
therefore still has unresolved ways to evaluate saved unrecorded instructions.
Native executable and mapping restrictions alone do not solve that distinction.

Canonical privileged native tools remain available. The native root `useradd`
probe records an actual account without a declaration change, then removes it.
That is a built-in-tool bypass, not breaking. The typed public adapter's positive
behavior does not close the native bypass. By contrast, root general-purpose
editing around built-in tools is classified separately as breaking; the editor
suite immediately removes its temporary marker.

Inspect each `boundary_result`, boundary-failure list, concrete readback and
independent review alongside exit statuses. The final row-by-row disposition
is in [STAND.md](STAND.md), with [independent review](raw/round-2/REVIEW-FINAL.md);
the testbed remains partial.
