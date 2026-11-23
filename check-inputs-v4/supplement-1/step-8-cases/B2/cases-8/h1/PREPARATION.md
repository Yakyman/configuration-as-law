# History 1 preparation: two updates

Preparation only, 2026-11-23 UTC. Recommended committed sequence: **performable candidate with two distinct real upgrades**, first through the declaration-writing catalog updater and second through the retained native built-in installer. There is only one declaration-writing base transition; the second native upgrade is expected to be restored to that recorded state during restart. Actual availability and every observation belong to the second party, not this source assessment. The separate native-first preparation trial was unsuccessful and is retained below without changing its identity.

## Fixed input identity

Use only the final step-6 image SHA-256 `1b581030629256ccc975950a2254572217e01a2474d2a07808a8e477ca980eca`. The complete unbooted declaration SHA-256 is `2e6946a893a04b121ef4687d82bc34fde2577e983ac0bfdc2ecf3ad4cdd79b4a`. Source binding and the exact factory `package:ed` row are retained in `B2/raw/step-8-prep/h1/source-evidence.json`.

| Input | Source | SHA-256 |
|---|---|---|
| First newer package, Debian ed 1.21.1-1 amd64 | https://deb.debian.org/debian/pool/main/e/ed/ed_1.21.1-1_amd64.deb | `b5498068d8ac54ad004bacbde2223a348fee781f9bb94328b01d8bfcbd179b48` |
| Second newer package, Debian ed 1.22.5-1 amd64 | https://deb.debian.org/debian/pool/main/e/ed/ed_1.22.5-1_amd64.deb | `593a7915c2ec0e3c87f824c2b11b4f72d3d74d654183c6833a18c4320e5df6a0` |

`sources.json` preserves independently fetched package metadata. The first requires libc6 >=2.34, the second >=2.38; the frozen image has libc6 2.41-12+deb13u5 and ed 1.19-1 (`initial.stdout`). The package sets are fixed deltas consisting of one real distribution package each; all other packages are retained. No fabricated worker version or repeated unchanged state is called a system update.

## Source determination

`B2/build/system_channels.py` begins: “Only catalog exact payloads may modify root paths. Catalog generation is an image-build operation; ordinary tools only select a recorded complete state.” Its `prepare` accepts only `apt[-get] install PACKAGE=VERSION` from the finite install catalog, or `upgrade --stand-catalog KEY` from the finite update catalog. `validate` requires exact equality to the catalog row.

`B2/build/system-fixtures.py:build` writes `updates={'ed': ...}` from the real transition ed 1.19-1 → 1.21.1-1. The one supported command is:

```sh
/usr/local/bin/apt-get upgrade --stand-catalog ed
```

The same command after restart selects the same new state; it does not upgrade any package a second time. `remove system:base-state` followed by upgrade restores the old package then repeats the same transition; it is not two successive newer package sets. The ordinary artifact path cannot replace the factory line: `B2/build/guard.py:validate` refuses a changed factory row, and managed payload paths are confined to the package tree except for exact trusted system updates. Neither changing the catalog nor rebuilding the image is allowed by this task.

Native tools are retained and root-only (`B2/build/install-guard.py`, `install-v4-tools.py`), so source review also considered the real pinned second package rather than inferring that no newer Debian package exists. Root `dpkg --install` is a built-in installation operation, not a general-purpose direct edit. S8.3-7: “Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.” No root installer invocation is relabelled as breaking merely because it is privileged.

`B2/build/install-transactions.py` installs an account prerequisite for all login sessions: `account requisite pam_exec.so quiet /usr/bin/test -f /run/stand-ready`. `B2/build/transactions.py:recovery` removes that readiness file, applies the selected rows, verifies them, and raises on a mismatch before publishing readiness. A native package replacement does not replace the immutable factory requirement. The native route therefore risks losing both ordinary sessions and the root observation transport at restart; the trial below investigated exactly that uncertainty.

## Final committed sequence: catalog update, then native update

Run as actual root on a fresh disposable copy through the existing laboratory observation credential, without changing guest permissions, PAM, replay or policy. Record each command's UTC, exact stdin, stdout, stderr and status separately on the host. Do not run this block in addition to another history attempt. The builder's trial is not an attempt.

The first command selects the image's preinstalled exact catalog payload ed 1.21.1-1. Record native package state before and after; its source/checksum are in the fixed-input table. No new package is installed merely to provide an updater.

```sh
/usr/bin/dpkg-query -W '-f=${Package} ${Version} ${db:Status-Status}\n' ed
/usr/local/bin/apt-get upgrade --stand-catalog ed
/usr/bin/dpkg-query -W '-f=${Package} ${Version} ${db:Status-Status}\n' ed
cat /proc/sys/kernel/random/boot_id
/usr/bin/systemctl reboot
```

After the machine restarts, record the changed boot ID and perform all three observations defined by `B2/OBSERVE-8.md` at `h1-after-restart-1`. A missing observation transport is an unavailable observation, never a pass. Do not disable the readiness gate to obtain it. If the dependent next session cannot be established, retain the failure and stop the dependent sequence; the second update and its observation points remain unperformed.

```sh
python3 - <<'PY'
import hashlib,pathlib,urllib.request
u='https://deb.debian.org/debian/pool/main/e/ed/ed_1.22.5-1_amd64.deb'
b=urllib.request.urlopen(u,timeout=60).read()
assert hashlib.sha256(b).hexdigest()=='593a7915c2ec0e3c87f824c2b11b4f72d3d74d654183c6833a18c4320e5df6a0'
pathlib.Path('/tmp/ed_1.22.5-1_amd64.deb').write_bytes(b)
PY
/usr/bin/dpkg --install /tmp/ed_1.22.5-1_amd64.deb
/usr/bin/dpkg-query -W '-f=${Package} ${Version} ${db:Status-Status}\n' ed
cat /proc/sys/kernel/random/boot_id
/usr/bin/systemctl reboot
```

After restart 2, record boot ID and perform all three observations at `h1-after-restart-2-and-end`. Each update is done only if the installer succeeds and immediate native package readback reports its requested newer version installed; each restart requires a different boot ID and restored observation access. Also report separately whether the requested version persists after restart. The second update may be completed and then reverted by replay; do not conceal that fact as either two persistent updates or an unchanged successful final package set. Declaration fulfillment remains a separate observation. No missing update or restart counts as done because an earlier command returned zero.

## Why this final sequence differs from the unsuccessful trial

`system_channels.activate` chooses `entry['after']` whenever the selected declaration includes the catalog system-update row, and rewrites every captured package/database path before readback. Therefore, after the first supported update and reboot, the second native upgrade has a different recovery path than native-first: on its restart the selected ed 1.21.1-1 catalog state is restored. A return to ed 1.21.1-1 is the expected source consequence, not a trial observation. That difference means the native-first trial alone cannot justify declaring the final sequence impossible. No second trial is needed to inspect this explicit source behavior.

The candidate does not assert that the second native update records its new version correctly; determining declaration completeness and ordinary work is precisely the purpose of the prescribed observations. There is no combination of default broker operations that supplies two successive newer base states: the sole update key remains `ed`, trusted row equality is mandatory, the install catalog only contains hello, and generic artifacts cannot replace a factory row or arbitrary root paths. The final sequence uses retained native installation functionality rather than altering those constraints.

## Preparation evidence, not outcomes

`B2/raw/step-8-prep/h1/expected.json` and `before-trial.utc` preceded the trial. One native ed 1.21.1-1 installation returned 0, native readback reported that version, and the restart request returned 0. The existing root observation transport did not return within the fixed 120-second readiness interval. No second update, second restart, or post-restart declaration observation was executed. `commands.json`, `upgrade-1.stdout`, `version-1.stdout`, `trial-failure.json` and `console-replay-excerpt.txt` retain those facts. The timeout is bounded availability evidence; the source argument above identifies the independent mechanism and does not treat the timeout as a proof about every conceivable route.

An early controller invocation preceded completion of VM startup: its two SSH commands returned 255 without executing in the guest. Those transport-only records are preserved under `premature-transport/`; they were not package-update probes and are not hidden or counted as updates. The actual compatibility trial started only after `lab.py new` completed.

The owned guest and disposable disk are removed; `cleanup.json` records that removal. No base image, recipe, catalog, guest gate or shared laboratory file was modified. All checks of the hypothesis and the required separate review remain unperformed.
