# Prepared Flatpak radio composition gate

First canonical run exposed an incorrect errno expectation; retained in
records/radio-flatpak-0.40-first.log and .serial. Native authenticated Bluetooth
worked, but the sandbox returned EAFNOSUPPORT instead of EACCES/EPERM.
Flatpak1.16.6 common/flatpak-run.c, socket_family_allowlist and setup_seccomp,
explicitly filters AF_BLUETOOTH unless its feature flag is enabled and returns
EAFNOSUPPORT for excluded families:
https://github.com/flatpak/flatpak/blob/1.16.6/common/flatpak-run.c#L1833-L1982
The corrected gate requires native traffic, actual Flatpak context and active
seccomp filtering; it reports that mechanism separately from access denial.
No production policy change was needed. Final success requires the marker below.

After `build-radio-fixture-040.py`, run `python3 build-radio-flatpak-fixture-040.py`
then `bash probe-radio-flatpak-040.sh` in the same bounded persistent worker job.
The first creates its own fixture directory and disk, combining normal radio rows
with the exact39 runtime/mpv refs and commits and recorded home-path probe scripts.
It verifies refs/commits against the sealed39 fixture recipe; native installer
validates each bundle's actual commit and the inherited reader component validates
the runtime bundle hash. Existing bundle files are reused without modification.
No shared example or production source file is edited.

The guest gate requires all of:

- Native Wi-Fi traffic and authenticated bidirectional Bluetooth before probing.
- Host recorded native radio probe succeeds; control mechanisms really exist.
- Actual Flatpak sandbox and exact `confos-flatpak (enforce)` context, ordinary UID.
- Native mpv starts (`--version`), recorded Python executes, recorded Bash executes
  the recorded Python mutation probe; libc and ordinary sockets work positively.
- Native libc HCI/raw and L2CAP/seqpacket sockets fail with EACCES/EPERM or the
  documented seccomp-family-filter EAFNOSUPPORT. Missing libraries/tools fail;
  missing host Bluetooth fails the required native traffic positive control.
- Unix/device/namespace routes either deny access or are explicitly reported as
  UNEXPOSED when absent from the sandbox. Absence is never counted as a denial.
- A subsequent supervisor verification occurs and exact declaration APPLIED
  remains. The runtime continuously monitors association and rechecks bond bytes.

This gate does not claim that Flatpak includes host `wpa_cli`, `btmgmt` or D-Bus
tools; it uses direct native socket/device operations, with positive primitives.
It also does not claim proc-root alias denial when the app's PID namespace hides
the supervisor. Existing host probe covers those visible host aliases.

Outputs: `logs/radio-flatpak-0.40.log`, `.serial`,
`logs/radio-flatpak-controls-0.40.log`, `logs/radio-flatpak-mpv-0.40.log`.
Completion marker: `CANONICAL40 FLATPAK RADIO CONTROLS PASS`.
Cleanup after evidence: `images/radio-040-flatpak.qcow2`, corresponding work tree,
`radio-040-flatpak-fixture/` (large bundle copies). Preserve declaration and probe
inputs/hashes before cleanup; original flatpak-inputs stay intact.

Rebuild provenance: preparation helpers require the sealed39 source archive
alongside the40 tree to verify inherited bytes/fixture recipe. Do not duplicate
that large archive inside40. A normal clean installation uses the already sealed
40 packages and `build.sh`; it does not rerun component preparation.
