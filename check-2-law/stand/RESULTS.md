# B1 results — 2026-11-19

Executor's results, revised in FB1 after REVIEW-1.md returned DISAGREE. Dispositions: FIX-1.md. Fixed rules: PROTOCOL.md, paper §§9.1, 9.3–9.6. Mechanisms and gaps: STAND.md. Source and failure-condition hashes were saved before test results in `raw/protocol.sha256`.

| Check | Outcome | Finding |
|---|---:|---|
| 2 — law | **?** | Tested prohibited channels were blocked. Download and now build exceptions work; revocation blocks the compiled artifact. O5, unmanaged root programs, absent radios and everyday-use gaps remain. |
| 3 — reproducibility | **?** | Prepared-image clones match except kernel-worker identities. Most inventories are inherited; independent clean bootstraps and declaration-driven base reconstruction remain untested even if process granularity is resolved. |
| 4 — lifecycle | **?** | Original alpha/beta fixture passes. Broader Chromium test exposes untracked home state and an unresolved base-versus-catalog owner boundary; assigned state archives correctly. |
| 5 — authority | **?** | No-list Unix execution is denied; same-file exception succeeds. P7 default Unix permissions vs P1/P4 for executing undeclared user files remains a hole. Other catalog authority scenarios pass. |

All overall outcomes are now `?`. Earlier fixture successes remain evidence, not complete passes. Check 5 contains an observed Unix-execution failure; whether this is a stand defect or a requirement contradiction under §9.1 remains unresolved for the author. No `0` is asserted without that attribution; no failure condition has been narrowed or changed.

## Check 2 — law (§9.3)

Original full run (retained): [raw/law-v2/rows.json](raw/law-v2/rows.json), 39 recorded rows, 33 checked expectations met and none unexpectedly failed; six rows are deliberately non-binary (two O5 cases, unmanaged root, two absent radios, audit evidence). The first full run is retained in `raw/evidence/stand-a/law/`. Each ordinary attempt ran through `runuser -u alice -- /usr/local/bin/cal-login -c COMMAND`; the identity row verifies UID 1000 and `cal-alice (enforce)`. Admin/setup rows explicitly say root. All exact commands, return codes, stdout/stderr, declaration hashes and timestamps are in the linked JSON files.

| Channel / attempt | Command | Expected | Observed | Evidence |
|---|---|---|---|---|
| declaration apply (root) | `calctl apply` | Succeeds | Succeeded; rc 0 | [00-reset](raw/law-v2/00-reset.json) |
| identity | `id; cat /proc/self/attr/current` | Succeeds | UID 1000; enforcing profile | [01-identity](raw/law-v2/01-identity.json) |
| system package manager | `apt-get install -y hello` | Blocked | Blocked; rc 126 | [02-system-package](raw/law-v2/02-system-package.json) |
| pip global | `pip3 install --break-system-packages /srv/cal-web/python-package` | Blocked | Blocked; rc 126 | [03-pip-global](raw/law-v2/03-pip-global.json) |
| pip user | `pip3 install --user --break-system-packages /srv/cal-web/python-package` | Blocked | Blocked; rc 126 | [04-pip-user](raw/law-v2/04-pip-user.json) |
| npm global | `npm install --global /srv/cal-web/node-package` | Blocked | Blocked; rc 126 | [05-npm-global](raw/law-v2/05-npm-global.json) |
| npm user | `npm install --prefix "$HOME/local-node" /srv/cal-web/node-package` | Blocked | Blocked; rc 126 | [06-npm-user](raw/law-v2/06-npm-user.json) |
| Flatpak system | `flatpak install --system --noninteractive /srv/cal-web/probe.flatpak` | Blocked | Blocked; rc 126 | [07-flatpak-system](raw/law-v2/07-flatpak-system.json) |
| Flatpak user | `flatpak install --user --noninteractive /srv/cal-web/probe.flatpak` | Blocked | Blocked; rc 126 | [08-flatpak-user](raw/law-v2/08-flatpak-user.json) |
| AppImage | `curl -fsS http://127.0.0.1:8080/probe.AppImage -o "$HOME/probe.AppImage" && chmod +x "$HOME/probe.AppImage" && "$HOME/probe.AppImage" --appimage-extract-and-run` | Blocked | Blocked; rc 126 | [09-appimage](raw/law-v2/09-appimage.json) |
| download into home | `curl -fsS http://127.0.0.1:8080/downloaded -o "$HOME/downloaded" && chmod +x "$HOME/downloaded" && "$HOME/downloaded"` | Blocked | Blocked; rc 126 | [10-download-home](raw/law-v2/10-download-home.json) |
| download into tmp | `curl -fsS http://127.0.0.1:8080/downloaded -o /tmp/downloaded && chmod +x /tmp/downloaded && /tmp/downloaded` | Blocked | Blocked; rc 126 | [11-download-tmp](raw/law-v2/11-download-tmp.json) |
| archive download/extract | `mkdir -p "$HOME/unpacked" && curl -fsS http://127.0.0.1:8080/program.tar.gz -o "$HOME/program.tar.gz" && tar -xzf "$HOME/program.tar.gz" -C "$HOME/unpacked" && "$HOME/unpacked/downloaded"` | Blocked | Blocked; rc 126 | [12-archive](raw/law-v2/12-archive.json) |
| build in home | `printf '#include <stdio.h>\nint main(){puts("source program");}\n' >"$HOME/probe.c"; gcc "$HOME/probe.c" -o "$HOME/built" && "$HOME/built"` | Blocked | Compiler exec denied; no binary produced by this attempt; rc 126 | [13-build](raw/law-v2/13-build.json) |
| systemd user unit | `mkdir -p "$HOME/.config/systemd/user"; printf '[Service]\nExecStart=/home/alice/downloaded\n' >"$HOME/.config/systemd/user/probe.service"; systemctl --user daemon-reload && systemctl --user start probe.service` | Blocked | Blocked; rc 126 | [14-user-service](raw/law-v2/14-user-service.json) |
| systemd user timer | `systemd-run --user --on-active=1 /home/alice/downloaded` | Blocked | Blocked; rc 126 | [15-user-timer](raw/law-v2/15-user-timer.json) |
| cron | `printf '* * * * * /home/alice/downloaded\n' \| crontab -` | Blocked | Blocked; rc 126 | [16-cron](raw/law-v2/16-cron.json) |
| interpreter Python | `printf 'print("USER_SCRIPT")\n' >"$HOME/probe.py"; python3 "$HOME/probe.py"` | ? under O5 | Blocked, rc 126; interpretation remains ? | [17-python-script](raw/law-v2/17-python-script.json) |
| interpreter shell | `printf 'echo USER_SCRIPT\n' >"$HOME/probe.sh"; bash "$HOME/probe.sh"` | ? under O5 | USER_SCRIPT executes, rc 0; interpretation remains ? | [18-shell-script](raw/law-v2/18-shell-script.json) |
| system tree | `printf forbidden >/usr/local/forbidden` | Blocked | Blocked; rc 1 | [19-system-write](raw/law-v2/19-system-write.json) |
| direct dynamic loader | `/lib64/ld-linux-x86-64.so.2 "$HOME/downloaded"` | Blocked | Blocked; rc 126 | [20-loader](raw/law-v2/20-loader.json) |
| declaration apply (root) | `calctl apply` | Succeeds | Succeeded; rc 0 | [21-allow-apply](raw/law-v2/21-allow-apply.json) |
| explicit allow line home | `"$HOME/downloaded"` | Succeeds | Hello, world!; rc 0 | [22-allow-home](raw/law-v2/22-allow-home.json) |
| explicit allow line tmp | `/tmp/downloaded` | Succeeds | Hello, world!; rc 0 | [23-allow-tmp](raw/law-v2/23-allow-tmp.json) |
| declaration apply (root) | `calctl apply` | Succeeds | Succeeded; rc 0 | [24-revoke-apply](raw/law-v2/24-revoke-apply.json) |
| allow line revoked | `"$HOME/downloaded"` | Blocked | Blocked; rc 126 | [25-revoked](raw/law-v2/25-revoked.json) |
| ordinary declaration install | `printf '%s\n' '{"programs":{"hello":{"version":"1"}}}' >"$HOME/declaration.json" && calctl apply && /usr/bin/hello` | Succeeds | dpkg installs hello; user runs it | [26-install](raw/law-v2/26-install.json) |
| ordinary network | `curl -fsS http://127.0.0.1:8080/; curl -I -sS --max-time 20 https://www.debian.org/` | Succeeds | Local HTTP page and external HTTPS succeed | [27-network](raw/law-v2/27-network.json) |
| declaration apply (root) | `calctl apply` | Succeeds | apt update/upgrade through apply; 0 packages needed upgrade | [28-update](raw/law-v2/28-update.json) |
| ordinary update evidence (root) | `dpkg-query -W -f='${Package} ${Version}\n' \| sort` | Succeeds | Succeeded; rc 0 | [29-update-packages](raw/law-v2/29-update-packages.json) |
| ordinary browser declare | `printf '%s\n' '{"programs":{"hello":{"version":"1"},"browser":{"version":"1"}}}' >"$HOME/declaration.json" && calctl apply` | Succeeds | User declaration applied | [30-browser-declare](raw/law-v2/30-browser-declare.json) |
| ordinary browser | `/usr/lib/chromium/chromium --headless --no-sandbox --disable-dev-shm-usage --disable-gpu --no-first-run --no-default-browser-check --user-data-dir=/var/lib/cal/active/browser --dump-dom http://127.0.0.1:8080/` | Succeeds | Headless Chromium renders fixture DOM | [31-browser](raw/law-v2/31-browser.json) |
| browser extension derivative | `mkdir -p "$HOME/extension"; printf '%s' '{"manifest_version":3,"name":"CAL extension fixture","version":"1.0","content_scripts":[{"matches":["http://127.0.0.1/*"],"js":["content.js"]}]}' >"$HOME/extension/manifest.json"; printf '%s' 'document.body.append("EXTENSION_EXECUTED");' >"$HOME/extension/content.js"` | Succeeds | Extension files created | [32-extension-prepare](raw/law-v2/32-extension-prepare.json) |
| extension within declared browser | `/usr/lib/chromium/chromium --headless --no-sandbox --disable-dev-shm-usage --disable-gpu --no-first-run --no-default-browser-check --user-data-dir=/var/lib/cal/active/browser --load-extension=/home/alice/extension --disable-extensions-except=/home/alice/extension --virtual-time-budget=3000 --dump-dom http://127.0.0.1:8080/` | Succeeds | EXTENSION_EXECUTED appears in DOM | [33-extension](raw/law-v2/33-extension.json) |
| managed root program write (root) | `/usr/local/lib/cal/worker --probe` | Blocked | Confined UID-0 worker denied, rc 13 | [34-root-managed](raw/law-v2/34-root-managed.json) |
| unmanaged root program write (root) | `/bin/sh -c 'printf ROOT_PROGRAM_UNCONFINED >/usr/local/root-program-probe'; cat /usr/local/root-program-probe` | Full P4 would constrain a root program | Root program writes system tree, rc 0 | [35-root-unconfined](raw/law-v2/35-root-unconfined.json) |
| Wi-Fi (root) | `ls -l /sys/class/ieee80211 /sys/class/bluetooth` | ?; hardware absent | No wireless interface class/device | [36-wifi](raw/law-v2/36-wifi.json) |
| Bluetooth (root) | `ls -l /sys/class/ieee80211 /sys/class/bluetooth` | ?; hardware absent | No Bluetooth class/device | [37-bluetooth](raw/law-v2/37-bluetooth.json) |
| AppArmor audit (root) | `journalctl -k --no-pager \| grep -E 'apparmor=\|DENIED'` | Capture evidence | Kernel denial records; audit rate limiting also recorded | [38-audit](raw/law-v2/38-audit.json) |

The AppImage is real: upstream type-2 runtime plus a hello payload, successfully exercised before confinement (`raw/appimage-fixture.log`). Flatpak is an exported local bundle; pip/npm have local package fixtures. The recorded rc-126 denials occur at the attempted executable. In the original build row, that executable is gcc: no compilation or resulting-binary launch occurred; rows 10–12 cover downloaded/unpacked files only. The FB1 supplement below separately covers a genuinely compiled artifact. Browser extension execution is permitted as a derivative under §9.3, not counted as bypass. Chromium was tested headless with its internal sandbox disabled while AppArmor remained enforcing; a full graphical day of use was not tested. System update exercised the declaration path but was a no-op; an actual version-changing OS upgrade remains untested.

Failure/uncertainty attribution:

| Observation | §9.1 attribution |
|---|---|
| Unconfined root program can change the system | **Stand defect / O4 coverage gap**, not proved inherent. Only selected managed root programs are confined. Do not relabel this automated program as a human-root exception. |
| Bash executes a user's script; Python execution is denied | **? explicitly required by §9.3/O5** where definitions do not decide. A denied path alone does not resolve script classification. |
| Wi-Fi and Bluetooth cannot be exercised | **Missing VM hardware**, not a demonstrated impossibility of P4. |
| Other exception channels have only partial dependency/daemon support | **Known untested stand gaps**; download and build are now exercised; other named exceptions remain unverified. |

### FB1 build-channel supplement

[raw/fb1/check-build.jsonl](raw/fb1/check-build.jsonl), source [src/check-build-fb1.py](src/check-build-fb1.py): nine command events; all mechanism assertions pass. Each row records command, UID route, declaration, artifact mode/owner/inode/hash, stdout/stderr and return code. These observations extend coverage without resolving the remaining Check 2 holes.

| Channel / command (Alice unless noted) | Expected | Observed | Evidence event |
|---|---|---|---|
| `gcc "$HOME/probe.c" -o "$HOME/built"`, no exception | Compiler denied; no artifact | rc 126; file absent | `compiler-denied-no-artifact` |
| Root applies `allow_channels: {"alice": ["build"]}` | Permission takes effect | rc 0 | `allow-build` |
| `gcc "$HOME/probe.c" -o "$HOME/built"; "$HOME/built"` under `set -e` | Compilation and launch | rc 0; `BUILT_BY_ALICE`; binary owned by Alice | `allowed-compile-and-launch` |
| Root removes build exception; `"$HOME/built"` | Resulting executable denied | rc 126; same bytes/mode/owner/inode | `revoke-build`, `compiled-artifact-launch-denied` |
| `gcc "$HOME/probe.c" -o "$HOME/built-again"` | Compiler denied again | rc 126; no second artifact | `compiler-denied-after-revocation` |

## Check 3 — reproducibility (§9.4)

Final pair: `clean-a` and `clean-b`, separate fresh overlays of the same stopped, empty test instrument, identical virtual hardware. Both start with `{current: {}, generations: [], active: [], archive: []}`: A pristine, B pristine. Different fresh machine IDs are recorded. Both apply the exact [declaration](src/repro-root.json), SHA-256 `e2de2505c2de4e84b86ad9d3a6fd3660b7135e06b13753f0aa1d302463068278`, whose `allow_channels` is empty. Apply outputs: A, B.

| Compared observation | A / B | Result |
|---|---|---|
| Package database | 1101 records each; 1100 installed | Identical names, versions, architectures, statuses |
| Accounts | 31 each | Identical UID/GID/home/shell |
| Groups, generated AppArmor and declarations | Exact `rules.txt` bytes | Identical |
| Active services/timers | 38 each | Identical |
| Service/timer unit-file states | 138 each | Identical |
| Kernel and loaded modules | Same kernel; 51 modules | Identical compared fields |
| PCI devices/drivers | 7 each | Identical |
| Userspace process records | 18 each | Identical executable, UID, argv, comm and multiplicity |
| Full process records | 86 each | Kernel `kworker` names/workqueue labels differ |

Full unchanged diff: raw/repro-comparison-v2.txt. Supporting projection and every differing record: raw/repro-summary.json. Raw collector outputs and all normalization rules remain under each pair directory. Rules: A, B. Initial pair/diff remain in `raw/evidence/stand-{a,b}/` and `raw/repro-comparison.txt`.

The raw difference is **not explained by hardware**. It does not identify a different executable, package, service or driver; it concerns internal kernel tasks. §5.1 names users/rules, programs, drivers and services, but does not state whether these changing thread/workqueue identities count separately. We retain this boundary as **? (definition/measurement granularity, related to O9)** instead of silently dropping the differing records or declaring a property-level counterexample. The clean pair uses one prepared instrument; independent OS bootstrap and cross-hardware reproduction were not established. **Even if the kworker granularity hole is resolved, this pair cannot support `1` without independent clean bootstraps.** Most package/account/unit equality is inherited from the common prepared disk. Moreover, `base-*` files are descriptive snapshots: the controller/hook do not reconstruct those inventories from them. Repeating setup independently would improve bootstrap evidence but would not alone establish full declaration-driven reconstruction. Source/evidence audit: raw/fb1-independent-audit.md. This round adds no new Check 3 VM pair and claims no new comparison result.

## Check 4 — lifecycle (§9.5)

Original fixture evidence: [raw/check-lifecycle-v2.jsonl](raw/check-lifecycle-v2.jsonl); 102 assertions passed, including command success/preconditions. The first run is preserved in `raw/evidence/stand-a/check-lifecycle.jsonl`. Each run records declaration commands, full generation documents before GC, directory inode/mode, cache bytes (base64) and shared-consumer output. Alpha and beta are separate installed fixture executables with a common implementation; ownership is supplied by the declaration, not inferred from intent.

| Procedure step, repeated for keep and delete | Observed |
|---|---|
| Declare alpha + beta and shared cache | Each program has its own state; both consume shared bytes |
| Remove alpha with its saved generation retained | Alpha state renamed into archive; cache bytes preserved |
| Leave beta current | Shared directory keeps its inode and remains readable by beta |
| Roll back to initial saved generation | Same state directories return; original cache prefixes remain |
| Remove alpha, then beta | Program and shared state move to archive; no ownerless active directory |
| Before deleting saved generations | All three caches still exist in archive in both settings |
| Delete every noncurrent saved generation | Keep retains all three archives; delete removes all three |

Original fixture result remains **1** within that recorded coverage. **Overall Check 4 is now `?`** after extending the test to actual Chromium-generated files: [raw/fb1/check-browser-lifecycle.jsonl](raw/fb1/check-browser-lifecycle.jsonl), source [src/check-browser-lifecycle-fb1.py](src/check-browser-lifecycle-fb1.py).

| FB1 browser procedure, repeated for keep/delete | Observed |
|---|---|
| Declare browser for Alice; render the local page | Chromium succeeds; creates assigned profile files plus a new 40-byte `~/.config/chromium/Crash Reports/settings.dat` |
| Remove catalog browser, retaining saved generation | Assigned profile moves to archive with identical content hashes; home file remains unchanged at its original location |
| Delete all noncurrent saved generations | Assigned profile retained for keep, removed for delete; home file still remains under both settings |

The summary records two **catalog archival coverage failures**, one per setting. These are evidence of the stand's untracked browser-associated home state, not proof of property-inherent failure. Chromium also remains installed and listed in the fixed `base-packages.tsv`: removing the mutable catalog entry does not prove absence of every owner under the full declaration. The `browser-owner-scope` events preserve this boundary; no new rule decides whether base presence or catalog removal controls this case. Therefore we do **not** assert that §9.5's no-owner clause conclusively fired. Automatic ownership/discovery (O1), base-versus-catalog presence, open descriptors, simultaneous users and crash consistency remain unresolved coverage.

The initial supplemental log raw/fb1/check-browser-lifecycle-initial.jsonl is retained. Its assertion label prematurely assumed owner absence; the final harness makes this qualification explicit and was rerun with the same keep/delete procedure. Neither label is a change to the fixed failure condition.

## Check 5 — authority (§9.6)

FB1 evidence: [raw/fb1/check-authority.jsonl](raw/fb1/check-authority.jsonl), **32 command events, one failed assertion**, exit 1. The failed assertion is deliberately retained: no-list execution expected success under the unmodified §9.6 Unix-permissions condition but returned 126. The earlier v2 run and figlet repair remain historical evidence; they did not cover execution of a user's own file.

| Attempt | Observed | FB1 event / line |
|---|---|---|
| No lists: user adds and runs hello | Accepted; real package installed and runs | lines 2–3 |
| Normal file creation/read/rename/chmod/remove | Succeeds | line 4 |
| Copy hello to own file; chmod 0755; execute, no lists | UID 1000, enforcing profile, file hash/mode recorded; execution denied rc 126 | `no-lists-prepare-own-executable`, `no-lists-unix-execute-own-file`, lines 5–6 |
| Add only download exception; rerun same file | rc 0; bytes, mode, UID/GID and inode unchanged; lists remain empty | lines 7–8; exception revoked line 9 |
| Write Bob's or root's declaration | Rejected; bytes unchanged | lines 10–11 |
| Personal hello v2 contradicts root hello v1 | Rejected; generations unchanged | line 14 |
| Override archive/policies or request system scope | Rejected; generations unchanged | lines 15–17 |
| Root allowlist containing hello | Hello allowed/runs; figlet rejected | lines 20–22 |
| Root denylist containing hello | Hello rejected; figlet allowed/runs | lines 25–27 |
| Root direct write, chmod 000 then read | Succeeds | line 28 |
| Root edits personal declaration and applies | Succeeds | lines 29–30 |

**Hole: P7 default Unix permissions vs P1/P4 for executing undeclared user files.** Empty lists do not restore ordinary Unix execution in the stand. The paired execution proves that the additional policy, rather than a change in DAC or file content, controls this case. Restricting the authority check to catalog entries or non-execution file operations would narrow the fixed condition and is not allowed. The evidence establishes the stand-level failure; whether the requirements necessarily contradict each other (§9.1 `0`) or the implementation is inadequate (`?`) is unresolved for the author. Current outcome: **?**, not a clean pass.

Initial unrelated defect: valid figlet could not execute because the profile missed its resolved Debian alternative target. Original failure: `raw/evidence/stand-a/check-authority.jsonl`; fix: FIX-B1.md, diagnosis `raw/figlet-diagnosis.txt`. Both v2 and FB1 pass that case. No runtime enforcement rule was relaxed in FB1.

## Reuse, review and cleanup

VM resources and checksums: `raw/infrastructure.txt`, `raw/infrastructure/`, `raw/launch-final-clean-pair.log`. All four test VMs were powered off after evidence collection. The clean, patched stand was retained stopped for the later channel experiment (D) and the review/fix rounds; redundant disposable disks are removed as recorded in `raw/cleanup.txt`. Review 1 returned DISAGREE; FB1 addresses it. FB1 ran on a separate disposable overlay of stopped clean-a, leaving the D1 disk unchanged. Launch/resource, cleanup and checksum records are under `raw/fb1/`; details in FIX-1.md.
