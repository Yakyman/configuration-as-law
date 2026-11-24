# Optional systemd radio lifecycle repair (private derivative)

This supersedes the unresolved lifecycle proposal in RADIO-040-DOCUMENTATION.md.
No numbered 0.40 image was built or tested by this work.

## Change

- `radio_systemd.py` generates an immutable Type=notify native service. PID1 owns
  the supervisor and its child cgroup; KillMode=control-group stops native children.
- `radio_runtime.py` notifies PID1 only after native verification and publication
  of the exact plan readiness record. Native child environments omit NOTIFY_SOCKET.
- Ready and user-manager units have BindsTo+After dependencies. Radio death stops
  them. StopPost removes both readiness files; ready's own StopPost handles the
  race in which its running startup operation could publish global readiness late.
- Normal PID1 retains its bootstrap/monitor path. Optional systemd skips that
  bootstrap, starts the service itself, and waits for its notification.
- `/run/confos-radio.pid` is an additional volatile runtime identifier; it is only
  used by trusted test fault injection, never as configuration or readiness input.
- Shared AppArmor session and Flatpak denial fragments are unchanged. Flatpak
  application-context integration still needs the canonical reader39 fixture.

## Evidence so far

| Command | Observed result |
|---|---|
| `python3 test-radio-lifecycle.py` | 2 pure checks passed; real Unix notify datagram and generated dependencies; `radio-lifecycle-tests.log`. |
| `python3 test-radio-runtime-draft.py` | Existing 5 pure checks passed. |
| `bash radio-lifecycle-private.sh` | Private current38 source derivative boots systemd; WPA2 AP traffic and authenticated bidirectional Bluetooth observed; native user-unit, ordinary and sudo control probes pass. |
| Same first native attempt, trusted SIGKILL | Serial confirms actual supervisor death and `confos-ready.service: Deactivated successfully`; SSH shuts down. Harness wrongly attempted a second SSH observation and exited nonzero. This is not a full lifecycle pass. |

Initial preparation also failed before build because draft module files had not
been copied to worker root; corrected by copying the explicitly listed drafts.
Native logs: `logs/radio-lifecycle-private-second.log` and `.serial`; initial
missing-file trace: `logs/radio-lifecycle-private-first.log`.

A bounded second run fixed only the private observation hook and **passed**:
`bash radio-lifecycle-retry.sh` rebuilt that private runtime and disk, then printed
`PRIVATE SYSTEMD RADIO READY AND CONTROLS PASS` and
`PRIVATE SYSTEMD RADIO DEATH REVOKES READY PASS`. The worker unit exited0.
`logs/radio-lifecycle-private.serial` contains `RADIO TRUSTED READINESS FILES REVOKED`
after the actual SIGKILL; the trusted hook requires all three files (global ready,
radio ready, runtime PID) to be absent. Final log: `logs/radio-lifecycle-private.log`;
rebuild log: `logs/radio-lifecycle-retry-build.log`. The canonical fault builder
uses the same observation for both readiness files. A failed SSH command alone
is not evidence that readiness was revoked. This tests the optional-systemd
lifecycle on a private38 derivative, not production40 or canonical power cuts.

Disposable derivative source/disk were removed after logs and exact private
runtime-init were saved. Final worker tree usage32G; no lifecycle guest remains.

## Exact integration order

1. Seal and hand over 0.39 first. Run `python3 advance-radio-release-040.py` only
   against its sealed source; existing archive/source checks remain mandatory.
2. Use `bash sync-radio-lifecycle-040.sh` instead of the earlier sync script so
   `radio_systemd.py` and the revised private fault recipe also reach the worker.
3. Run `prepare-radio-040.sh` in a persistent bounded worker unit. It now calls
   `build-radio-lifecycle-fault-040.py`, which keeps original private build isolation
   but injects via PID file before either PID1 path. No production fault hook.
4. Complete both canonical paths: clean boot, reboot, controls, actual changes,
   three cuts each, removal/restoration, and confirmed readiness revocation.
   Run Flatpak reader39 radio-control probes before claiming that context verified.
5. Incorporate declaration/inventory documentation from RADIO-040-DOCUMENTATION.md
   plus the PID identifier above; independent case party owns acceptance.
