STEP 8 CASES: 3 of 4 histories performable

Final step-6 image SHA-256: `1b581030629256ccc975950a2254572217e01a2474d2a07808a8e477ca980eca`.
Complete initial declaration SHA-256: `2e6946a893a04b121ef4687d82bc34fde2577e983ac0bfdc2ecf3ad4cdd79b4a`; full unchanged text: [cases-8/declaration.json](cases-8/declaration.json).

Prepared 2026-11-23 UTC. **Preparation only; public commitment pending; no second-party history attempted.** The first line is the preparation assessment: histories 1, 2 and 4 have supported candidate procedures; the selected game history has a documented expected execution blocker. It is not four measured outcomes. **History 3 must still be attempted once with its committed launcher and commands; only that attempt decides whether it runs.** Preparation trials are not history attempts and establish no `1`, `0` or `?`.

The only image is `VMs/cal-1123/stand/base/stand.qcow2`, relative to the server account's initial directory, mode `0444`, exactly the final image named in [CASES-6.md](CASES-6.md). No rebuild, recipe modification, catalog extension or guest-policy repair is permitted. The declaration is the complete eight-file export extracted read-only from that image in step 6, not a case-1 fixture or a new description reconstructed after boot. Its source identity is [raw/round-4-prep/final-1/offline-declaration/identity.json](raw/round-4-prep/final-1/offline-declaration/identity.json). Startup and ordinary writes may subsequently select other declarations; observe their actual success identities.

## Chosen inputs

| History/input | Fixed source | SHA-256 |
|---|---|---|
| 1, first newer package set: ed 1.21.1-1 amd64, all other packages retained | [Debian package](https://deb.debian.org/debian/pool/main/e/ed/ed_1.21.1-1_amd64.deb); exact payload already in the image's `ed` update catalog | `b5498068d8ac54ad004bacbde2223a348fee781f9bb94328b01d8bfcbd179b48` |
| 1, second newer package set: ed 1.22.5-1 amd64, all other packages retained | [Debian package](https://deb.debian.org/debian/pool/main/e/ed/ed_1.22.5-1_amd64.deb) | `593a7915c2ec0e3c87f824c2b11b4f72d3d74d654183c6833a18c4320e5df6a0` |
| 2, public native C project | [docker-library/hello-world, hello.c](https://raw.githubusercontent.com/docker-library/hello-world/522bcd2faf422c60b9d20e64d7cd6d56600aec97/hello.c), commit `522bcd2faf422c60b9d20e64d7cd6d56600aec97`; retained [hello.c](cases-8/h2/hello.c) | `cb95a0ed950c272471e7eb2a6b4261d857174bc3750874f538ac60e20af16d34` |
| 3, launcher before self-update | [LinuxGSM v26.5.0 linuxgsm.sh](https://raw.githubusercontent.com/GameServerManagers/LinuxGSM/50dc4e551b661b9d1fa39c291068a16a66056aff/linuxgsm.sh), commit `50dc4e551b661b9d1fa39c291068a16a66056aff` | `3063de7f3bf025976dcd11693af84bbe78b43564c3174129d524c7b3c16f5707` |
| 3, launcher after its own `update-lgsm` command | [LinuxGSM v26.6.0 linuxgsm.sh](https://raw.githubusercontent.com/GameServerManagers/LinuxGSM/9ca2e951c6e15d4db7184a60e1fd8a831b2cdb0f/linuxgsm.sh), commit `9ca2e951c6e15d4db7184a60e1fd8a831b2cdb0f` | `f0fa0f6e60c6d8fb296f4e50fe88ab441d7dd5ff930abaf1487a055961411f6e` |
| 3, game | [Wolfenstein: Enemy Territory dedicated game server 2.60b](https://linuxgsm.download/WolfensteinEnemyTerritory/wet-2.60b-linux-i386-linuxgsm-20261101.tar.xz), packaging revision `linuxgsm-20261101`, 263,915,952 bytes | `ac359aebe0bf8fd568341876e3a8992d7c562ee6fdc4a8906bdbab47eae66cf3` |
| 4, installed package | `dev-worker` version 1, source `builder-source:development-worker`, exact existing recipe [build/dev-inputs.py](build/dev-inputs.py); installable input `/usr/local/share/stand/dev/worker-1.json`; retained [worker-1.json](cases-8/h4/worker-1.json) | artifact `cc7a77f4e8cb92e2db65c112f17cce425bf966980ff239772bf500599d1ff2ba`; recipe `590b8c051a3be3222b415e4d937c89909da389f1d6fcdb02e269f1f14620938e` |

Additional fixed identities: [h1/sources.json](cases-8/h1/sources.json) (package metadata), [h2/inputs.json](cases-8/h2/inputs.json) (all three edited source and four expected output hashes), [h3/launcher-sources.json](cases-8/h3/launcher-sources.json) (launcher modules, game configuration and startup evidence sources), [h3/game.json](cases-8/h3/game.json), [h3/prerequisites.json](cases-8/h3/prerequisites.json) (all 15 missing native prerequisite/dependency packages with individual URL/version/SHA-256), and [h4/inputs.json](cases-8/h4/inputs.json) (artifact and installed worker payload). Every fetched input is checksum-checked; a mismatch stops its dependent actions, with no replacement version. Package repositories are not refreshed to choose a different version during performance.

History 2 builds the public single-file executable natively, using the image's compiler and C library. Its container packaging is irrelevant; the original output's container references are fixed source text, not an observed container. History 3 is explicitly a **dedicated game-server process**, started and stopped by a console launcher; it makes no claim about local graphical gameplay. It needs no account, display server or hardware beyond the existing guest.

## Fixed criteria and publication gate

The question, four histories, three observations, expected result, failure conditions, author-reading exception and outcome combination remain exactly [SUP1/step-8.md](cases-8/criteria/step-8.md). The unchanged Section 8/9.3/Appendix text and numbered sentences are in [criteria/](cases-8/criteria/). This preparation applies no weighting protocol and resolves no author question.

Expected result, copied from the committed step: “It is expected that in the histories that can be performed nothing in force will be found unrecorded and every line will be fulfilled; that the game history will not be performable on the image; and that the declaration will grow with every file a history saves.” This expectation decides no outcome and is not a threshold. The preparation findings below do not revise it.

[cases-8/inputs-seal.json](cases-8/inputs-seal.json) binds this document, [OBSERVE-8.md](OBSERVE-8.md), the complete initial declaration, every history script/input, controller, criteria, supporting preparation evidence and unchanged recipe. Local sealing is **not publication**. The working copy's repository metadata is empty/read-only and no public destination is supplied; `COMMON.md` forbids public writes in this task. Therefore the records operator must publish the unchanged sealed package, with the actual image identity, before the second party's first attempt. No placeholder publication record is supplied and the builder has not invoked the performance controller.

After independently checking the public bytes, the performer supplies `cases-8/publication.json` with the actual `public_record_url`, actual `commit`, `inputs_seal_sha256`, and `operator_verified_published_bytes: true`. This is an external receipt, excluded from the input seal. The controller rejects a missing/mismatching receipt or any changed sealed file. A supplied string alone is not proof of publication: the performer must inspect the public record. Inputs and commands must not change after publication or the first attempt. Later results go in new output files, never by editing these inputs.

## Exact host execution and recording

The server laboratory contains `lab.py`, existing laboratory credentials and the immutable image. Copy the sealed `cases-8/`, these two documents and preparation evidence there without changing the existing recipe or image; the seal checks their required bytes. Work only inside `VMs/cal-1123/stand/`. Check the fixed image and seal, then run **one history at a time**, waiting for its service to finish before starting the next:

```sh
cd VMs/cal-1123/stand
sha256sum base/stand.qcow2 cases-8/declaration.json cases-8/inputs-seal.json
python3 lab.py list
mkdir -p raw/step-8-second-party

systemd-run --user --unit=s8-second-h1 --property=WorkingDirectory="$PWD" --property=StandardOutput=append:"$PWD/raw/step-8-second-party/h1-controller.log" --property=StandardError=append:"$PWD/raw/step-8-second-party/h1-controller.log" python3 cases-8/run.py h1 --publication cases-8/publication.json
systemctl --user show s8-second-h1.service -p ActiveState -p ExecMainStatus

systemd-run --user --unit=s8-second-h2 --property=WorkingDirectory="$PWD" --property=StandardOutput=append:"$PWD/raw/step-8-second-party/h2-controller.log" --property=StandardError=append:"$PWD/raw/step-8-second-party/h2-controller.log" python3 cases-8/run.py h2 --publication cases-8/publication.json
systemctl --user show s8-second-h2.service -p ActiveState -p ExecMainStatus

systemd-run --user --unit=s8-second-h3 --property=WorkingDirectory="$PWD" --property=StandardOutput=append:"$PWD/raw/step-8-second-party/h3-controller.log" --property=StandardError=append:"$PWD/raw/step-8-second-party/h3-controller.log" python3 cases-8/run.py h3 --publication cases-8/publication.json
systemctl --user show s8-second-h3.service -p ActiveState -p ExecMainStatus

systemd-run --user --unit=s8-second-h4 --property=WorkingDirectory="$PWD" --property=StandardOutput=append:"$PWD/raw/step-8-second-party/h4-controller.log" --property=StandardError=append:"$PWD/raw/step-8-second-party/h4-controller.log" python3 cases-8/run.py h4 --publication cases-8/publication.json
systemctl --user show s8-second-h4.service -p ActiveState -p ExecMainStatus
```

These are four sequential invocations, not a concurrent shell batch. Save each final service status with its history. The script is the exact executable sequence, not a suggested implementation. It creates fresh guests `s8-second-h1` through `s8-second-h4`, using the existing `lab.py new NAME stand` and its systemd-owned QEMU process, nonblocking shared slot lock, 4 GiB memory and two vCPUs. It checks the image hash first, refuses existing guest/output names and never reuses another history's state. No installation is performed on the base image. Missing prerequisites are installed **within the history** using native built-in tools, not added to the image beforehand.

All guest scripts are passed as command text through the existing shell; no test helper is installed in the guest. The root credential is used only where stated (native built-in package operations, reboot and read-only observations). General-purpose privileged state edits, policy exceptions and manual declaration repairs are not part of a history. Root `dpkg` is a built-in installer, not breaking by virtue of its privilege: S8.3-7 explicitly includes tools running with superuser privileges.

The controller saves exact stdin and argv, SHA-256, UTC boundaries, separate stdout/stderr and exit for every guest session. Bash traces add command-level epoch times and line numbers. Native observations and success reports are host files. For each mandatory point, complete the cumulative ordinary-action table specified in [OBSERVE-8.md](OBSERVE-8.md), including all not-reached actions from [actions-plan.json](cases-8/actions-plan.json). Record every query failure and instability; collection success is not property fulfillment.

## History 1: two updates, two restarts

Full source assessment and the separate native-first trial are in [h1/PREPARATION.md](cases-8/h1/PREPARATION.md). The final once-only sequence is:

1. Root executes exact [h1/update-1.sh](cases-8/h1/update-1.sh): query native ed state, `/usr/local/bin/apt-get upgrade --stand-catalog ed`, require immediate installed ed `1.21.1-1`, retain native state. This uses the real newer package already pinned in the image.
2. Save boot ID; root executes `/usr/bin/systemctl reboot`. Wait at most the existing laboratory readiness limit of 180 seconds. Require a different boot ID. **Observe at `h1-after-restart-1`**, including failure to regain access, then retain native ed version.
3. Root executes exact [h1/update-2.sh](cases-8/h1/update-2.sh): fetch/check the pinned ed `1.22.5-1` package to `/tmp`, `/usr/bin/dpkg --install /tmp/ed_1.22.5-1_amd64.deb`, require immediate installed ed `1.22.5-1`, retain native state.
4. Save boot ID, perform the second identical reboot command, require a different boot ID and **observe at `h1-after-restart-2`**. Retain native ed version, then **observe at `h1-end`**.

The scripts preserve every literal command, argument and checksum. Two repeated selections of the same catalog state would not be two updates. The image has only one declaration-writing update entry (`ed`); the second genuine newer package is obtained with fixed inputs through its retained native installer. No catalog edit, downgrade-and-repeat substitute or fabricated program update is used. Source inspection predicts that replay may restore the second native upgrade to the first recorded package version. Report immediate installation and post-restart persistence separately; neither is inferred from a wrapper exit. If an update fails or login is unavailable after a restart, stop dependent actions, retain their not-done status, and attempt the required end query without repairing the guest.

## History 2: three development rounds

Execute [h2/history.sh](cases-8/h2/history.sh) once through the ordinary shell, with no root flag. All tools are already installed. Each of three consecutive rounds on the same copy performs:

1. Fetch the same pinned public `hello.c`, verify its checksum and save it.
2. Write its exact import specification; `stand-import source /home/stand/step8-h2/source.json`; `stand-build build source:h2-hello`; `stand-import install /home/stand/h2-hello.built.json`.
3. Run `/opt/stand/pkgs/h2-hello-built/bin/program`, retain output and verify the original output checksum.
4. Change exactly the one greeting source line to the round-specific greeting, assert that exactly one source line changed, and repeat source admission, build, result admission and launch; verify the corresponding edited output checksum.

There are three fetches/edits and six builds/launches, not three independent copies or only three total builds. The compiler is the image's native fixed GCC tool; the result's ordinary admission is part of its supported workflow. Full source, source specifications, expected output bytes, checksums and exact loop expansion are fixed by [h2/README.md](cases-8/h2/README.md) and [h2/inputs.json](cases-8/h2/inputs.json). Stop at the first failed command, preserve remaining actions as not done, and **observe at `h2-end`**. No restart is prescribed.

## History 3: fixed console game launcher

First execute [h3/prerequisites.sh](cases-8/h3/prerequisites.sh) as root: fetch and verify the 15 pinned missing native packages, install them in one ordinary `/usr/bin/dpkg --install` invocation without bypass flags, and read the package database. Their dependency check against the frozen image is [dependency-check.json](raw/step-8-prep/h3/dependency-check.json). The image is not changed in advance. If this prerequisite action fails, preserve it and mark subsequent launcher actions not done.

If it succeeds, execute [h3/history.sh](cases-8/h3/history.sh) once through the ordinary shell:

1. Fetch/check LinuxGSM at the pinned first commit; set its documented branch selector to that commit; `bash linuxgsm.sh wetserver`.
2. `bash wetserver auto-install`; verify the fixed game archive and server configuration before first start.
3. `bash wetserver start`; verify an actual live `etded` executable and exact argv through `/proc`; retain `bash wetserver details`; `bash wetserver stop`; require the game initialization marker in its log.
4. Set the branch selector to the pinned second commit; `bash wetserver update-lgsm`; retain the actual changed launcher hash and verify the pinned source bytes after reversing only the launcher's own documented identity-field substitutions in memory.
5. Start/read back/retain details/stop the game again using the same commands and process/log checks. **Observe at `h3-end`**, also on any early failure. No restart is prescribed.

The launcher downloads the game and updates itself; the controller does not replace it with a newly downloaded executable to pretend self-update happened. No account, graphical client or additional display session is used. The chosen launcher/game do not change if they fail.

**Preparation reason for excluding history 3 from the first-line count:** native prerequisite installation has no hook admitting the newly installed executables/libraries into the ordinary shell's recorded execution policy; independently, LinuxGSM's downloaded game executable is placed under the image's `noexec` home filesystem. This is a source-based prediction of failure of the committed ordinary launch path, not an observed outcome or a universal impossibility argument. Sources and exact limitations are [preparation.md](raw/step-8-prep/h3/preparation.md), `build/codeboundary.py:inputs`, `build/shell_boundary.py:generate`, `build/import_channels.py` and `build/bc3_filesystem.py`. The second party must nevertheless run this exact history once and decides performability from its output, as step 8 requires. No extra admission scheme or launcher-specific image change is added.

## History 4: loss and restoration of the external virtual link

The full exact ordered host/guest sequence and frozen development fragments are in [h4/README.md](cases-8/h4/README.md); [h4/cut-action.py](cases-8/h4/cut-action.py) implements the barriers. The common controller runs it, so do not run those commands a second time.

1. Verify the committed worker artifact. Start the ordinary `stand-pkg install /usr/local/share/stand/dev/worker-1.json`. When the guest has observed the actual installer process and emitted its serial `CUT_READY` marker, the host sends QMP `set_link` with `{"name":"net0","up":false}` to that guest's existing `qmp.sock`. The guest records whether the actual installer is still active when carrier becomes zero.
2. When that action finishes, **observe while disconnected**, before any network restoration. The in-memory collector signals `OBSERVATION_DONE` on the serial console. Only then the host sends `set_link` with `{"name":"net0","up":true}`. **Observe immediately after restoration.** If installation failed, retry precisely the same command once with the restored link, retain its result, and observe again. If installed, run the worker once.
3. Execute [development-prefix.sh](cases-8/h4/development-prefix.sh): exactly history 2's first fetch, source specification and source admission. If it succeeds, apply the same host cut procedure during precisely `stand-build build source:h2-hello`. **Observe immediately after that individual build finishes while disconnected**, then restore through QMP and **observe immediately after restoration**.
4. Only if that build failed, retry precisely the same build once with the link restored, retaining its result and another observation. On successful build, execute [development-suffix.sh](cases-8/h4/development-suffix.sh): first binary admission/run, first edit/build/run, then full rounds 2 and 3. No already successful development action is repeated. **Observe at `h4-end`**, including after any unavailable part.

Both cut and restoration occur at the host virtual device; no guest network setting is edited. The exact installation artifact and the interrupted compiler are local-input operations: they need not fail merely because the link is down. This is not misreported as a download interruption. The prescribed development sequence still contains its actual public source fetches. A missed process interval, missing carrier transition or failed barrier is retained as an incomplete interruption, not silently retried. Source: [QEMU set_link](https://www.qemu.org/docs/master/interop/qemu-qmp-ref.html#command-net.set_link), “Sets the link status of a virtual network adapter.”

## Cleanup, trials and later judgments

After final collection the controller preserves the console and stops/destroys only its own guest. If graceful shutdown fails, it records that failure, force-stops the owned disposable process and deletes its overlay; this cleanup power-off occurs after observation and is not another history restart. It retains `cleanup.json`, an unchanged base hash and the remaining-guest listing. A cleanup failure must be resolved for that named owned guest only. Never delete an existing output or another party's guest to permit a repeat.

Preparation evidence is in [raw/step-8-prep/](raw/step-8-prep/). History 1 has one unsuccessful **native-first** compatibility trial, different from the final supported-first sequence; both initial transport-only failures and the actual trial are retained. History 4 has one external-cut/barrier trial and its prescribed restored-network recovery action. History 2 and history 3 have source/input checks and no VM trial. A separate [collector integration check](raw/step-8-prep/OBSERVER.md) executed no history: it detected observer-induced D-Bus service activation, retained the unstable readback, and prompted a documentation-backed query correction before commitment, without repeating the probe. All owned preparation guests and copies were removed; the final [handoff audit](raw/step-8-prep/handoff-audit.json) binds the unchanged base, full declaration, frozen files and cleanup. Source checks and trial results are preparation evidence only; the final full histories and common collector were not executed as second-party attempts.

The performer records every history as `1`, `0` or `?` under the unchanged step-8 criteria. A testbed failure yields `0` only with a written argument from Section 8 alone, checked by the separate reviewer, that any system with P1/P2/P4 would fail the same history; otherwise it is `?`. A not-performable history is `?`. A definition counterexample and a choice between readings receive the distinct treatment fixed in step 8. Breaking is excluded and listed separately. For the step: any `0` gives `0`; otherwise any `?` gives `?`; otherwise `1`. The preparation header, code checks, matched hashes and controller exits are none of those outcomes.
