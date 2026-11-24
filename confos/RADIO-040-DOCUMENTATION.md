# Guarded 0.40 integration — prepared, not run

Historical planning note. The lifecycle defect described below was subsequently
repaired and privately exercised (RADIO-LIFECYCLE-RESULTS.md); the canonical40
pipeline now includes Flatpak controls (RADIO-FLATPAK-040.md), fixed native
inspection and independent clean replay. STATE.md and versioned canonical logs
give the current status; the original future-tense paragraphs below are not
current pending instructions.

Parent order: seal 0.39, review these scripts, run `python3 advance-radio-release-040.py`, sync, then launch `prepare-radio-040.sh` in a persistent worker unit. Build limit MemoryMax8G/CPUQuota100%; probe guest 3GiB, one reserved slot. No script seals a release or modifies numbered source archives. The advance refuses raw source differing from sealed39; archive recipe uses `releases/source-0.39.sha256` because historical archives omit that recipe. All source anchors are checked before writes. Configuration38 native helper and Flatpak39 reader hooks stay intact. New runtime is explicitly rebuilt, avoiding the existing-package cache trap. Reader40 inherits the complete sealed39 reader payload; only package version changes.

Existing proof: `RADIO-PRIVATE36-RESULTS.md`, evidence archive SHA256 `ce685f026515cf52abf73d16559b8224cf376869619b8593a4353c681dd74830`. These new scripts have syntax checks only; they have not built or booted 0.40.

## Declaration table for DECLARATION.md

| Kind | Syntax | Section 8.2 | Meaning |
|---|---|---|---|
| Simulated fixture | `radio-fixture NAME SHA256 RELATIVE_JSON` | S8.2-11–13; S8.2-5 | Exact AP configuration, two fixed virtual controller identities; fixture remains without client/bond rows. |
| Saved Wi-Fi | `network NAME SHA256 RELATIVE_JSON` | S8.2-11–13 | Exact SSID bytes, WPA2-PSK key, IPv4 address and fixture association. Automatic native association and AP traffic before READY. |
| Saved pairing | `bluetooth-pair ADAPTER PEER SHA256 RELATIVE_INFO` | S8.2-11–14 | Exact native BlueZ authenticated type5 BR/EDR bond, including chosen key/metadata. Both directions needed for mutual authenticated traffic. |

Complete examples and public inputs: `radio-public-fixture/radio-draft.conf`. Public test keys are intentionally non-secret. No pairing/key creation occurs on startup. One fixture/client supported; exact resolved packages enforced; JSON keys, canonical addresses, allowed native metadata, input checksum/path/symlink constraints are strict. Hardware radio support is not claimed. These new kinds currently require manual text editing; no built-in radio recorder exists yet.

## UNDERIVED additions / complete native input inventory

All four native BlueZ input files below are immutable generated root0600 output and copied byte-for-byte into a private writable volatile store. They are derived; list them explicitly so neither controller settings file is mistaken for unrecorded state. A=00:AA:01:00:00:00; B=00:AA:01:01:00:01. Prefix `/usr/lib/confos/radio/bluez/`.

| File | SHA256 in public fixture | Source |
|---|---|---|
| A/B/info | d64093eaddc1a6d392b4f9707b7bbaaa64af072df3a96cdba305fc472931108b | First bluetooth-pair input |
| B/A/info | 0dd10ad01633603b9c537ae709020274d9eb0ba3b4d137f48992730e6f1e83d4 | Second bluetooth-pair input |
| A/settings | 62336834a96837682ce87342a40a8dda7e84640b221ffe87db0a01575a34db0e | Fixture renderer, `[General]\nDiscoverable=false\n` |
| B/settings | 62336834a96837682ce87342a40a8dda7e84640b221ffe87db0a01575a34db0e | Same deterministic renderer |

| Runtime object | Derivation/status and reason |
|---|---|
| Private `/run/confos-radio/bluez/{A,B}/settings` and peer `/info` | Exact four copies above; info membership and bytes rechecked every10s. Removing pair rows omits corresponding info. |
| Private BlueZ `A/cache/B` and `B/cache/A` | Native cache observed at replay,26bytes `[General]\nName=BlueZ 5.82\n`, SHA e01aace499baa68671acf55628f2d0cab847bdb13ff29790d708271e28dbe305. Not generated as immutable output; list under UNDERIVED until outside inventory decides. No saved access/key is kept in cache. |
| `/run/confos-radio/machine-id` bound privately over `/var/lib/dbus/machine-id` | Deterministic first32 hex SHA256 of literal `ConfOS simulated radio fixture bus`, newline. Derived from runtime package; underlying empty mount target may be created at boot. |
| Private `bus.conf` | Exact deterministic runtime-generated XML; root-only native bus policy. Derived from runtime package. |
| Private `bus` socket; D-Bus unique names/server GUID, message IDs | Runtime-only native identifiers, may vary; belong to declared fixture bus. No persisted keys. |
| Private `wpa/` directory and `wpa/wlan1` control socket | Native supplicant control endpoint, runtime-only. Exact immutable wpa.conf has update_config=0. |
| `/run/netns/confos-radio-ap`; private tmpfs and BlueZ/machine-id bind mounts | Volatile control mounts; belong to fixture; S8.2-5. |
| Private `hostapd.log`, `supplicant.log`, `dbus.log`, `btvirt.log`, `bluetoothd.log` | Native diagnostics with variable times/event sequence; not claimed checksum-derived. Exact names follow launch() calls; no persistent log disk. |
| `/run/confos-radio-ready.json`, temporary `.pending` | Runtime status and immutable plan digest; protected from sessions. Not installation input. |
| hwsim PHY/interfaces/MACs, HCI controller IDs/addresses, sockets/processes, packet counters, association/authentication session state | Volatile native objects governed by fixture/client/bond rows and runtime implementation; S8.2-5. No random saved bond generation. |
| Empty `/run/confos-radio` outside private namespace | Mount point visible to sessions; actual controls are in private tmpfs. |

Immutable plan.json, hostapd.conf, wpa.conf and the four native inputs follow renderer checksums. Runtime cache/identifier/log output above must be included in whole-machine inventory; private mounts need trusted namespace-aware collection. Local UNDERIVED document additions are proposed here, not silently applied.

## Canonical test phases and remaining gate

`probe-radio-040.sh` prepares ordinary and optional systemd PID1 paths. The second fixture declares an enabled native user-unit that executes the mutation probe; it must finish successfully. Each path checks actual native traffic before READY, ordinary/sudo controls, reboot, three cuts each following real client-address changes, removal of client/both bonds while fixture remains, and restoration. Exact declaration digest is required each time. Assertions use strict shell or Python assertions. Cuts are after observed APPLIED, matching the existing builder durability harness; they are not claimed to hit the earliest internal commit instruction.

Private fault derivative: `build-radio-fault-fixture-040.py` copies source and symlinks existing package inputs, builds its own runtime package, and injects a trusted boot-only signal trigger. Canonical runtime stays untouched. Trigger files exist only as a test entry in this derivative. Probe requires serial confirmation of actual SIGKILL injection, then requires `confos status` to stop reporting success. Ordinary sudo cannot legitimately signal the distinct radio label, so using sudo pkill as the fault injector would be a false test.

**Expected unresolved lifecycle gate:** bootstrap radio runs before optional `exec systemd`, retaining its private mount namespace and label, but the normal runtime-init monitoring loop is replaced by systemd. Thus forced supervisor death may leave global READY stale in the optional path. The pipeline deliberately fails here; do not seal40 until repaired and rerun. Proposed repair: systemd owns a Type=notify radio service, KillMode=control-group, readiness dependency before confos-ready/user managers, and trusted ExecStopPost revoking global READY; runtime notifies only after native traffic. This is not implemented or tested by these draft scripts. Boot/reboot privacy itself also remains untested under systemd.

Private36 also tested real root confos-flatpak controls via a trusted boot fixture hook. The canonical40 pipeline here tests ordinary/sudo plus native user-unit contexts; canonical Flatpak app-context radio probes must be added using the reader39 fixture before claiming that new integration validated that context. Do not add the old trusted probe hook to production runtime-init.

After evidence collection remove disposable `images/radio-040-*` disks/work trees and `radio-040-fault-source`; retain declarations, inputs, all failure/success logs, and diff of trusted fault hook. Preserve current/previous numbered release images only.
