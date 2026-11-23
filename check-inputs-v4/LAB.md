# Laboratory runner

Prepared 2026-11-23 UTC. The laboratory root contains `lab.sh`, `keys/lab`,
`images/`, `install/`, `C1/base/`, `C1/vms/`, and twelve shared
`slots/slot-N.lock` files. The private key remains on the host and is never
included in the records. `lab.sh` is derived from the preceding laboratory runner.

Commands (run from the laboratory root):

```
./lab.sh new NAME SYSTEM
./lab.sh run NAME [--root] [--timeout N] < script.sh
./lab.sh copy-out NAME GUEST_PATH DESTINATION
./lab.sh stop NAME
./lab.sh start NAME
./lab.sh kill NAME
./lab.sh destroy NAME
./lab.sh list
```

`new` creates a disposable qcow2 overlay over a read-only base and boots it.
Supported system identifiers are `alma`, `void`, `gentoo`, `microos`, `talos`,
`nixos`, `guix`, `debian`, `fedora`, `mint`, and `debian-server`. Availability is
reported separately in `KIT-READY.md`; accepting an identifier does not certify a base.
`stop` requests graceful poweroff; `kill` cuts power; `destroy` stops and removes
only the named disposable machine. `list` reads host registry metadata only.
Talos stops through its API, Guix through its documented Shepherd command, and
Gentoo through privileged SSH `poweroff`; other systems use the virtual ACPI
power button. Explicit Gentoo shutdown avoids adding an ACPI daemon merely for
the instrument. Transport disconnects during shutdown are tolerated, but success
still requires the host QEMU process to exit.

SSH forwards a host loopback port to guest port 22 and uses the laboratory key.
`run` takes a script from standard input, preserving it across the shell/Python
wrapper, emits stdout and exits with its status. With `LAB_SEPARATE_STDERR=1`, SSH and Talos preserve stderr separately; serial retains combined framing and is limited to the fixed check-4 status calls during these rehearsals. A script
shebang selects its interpreter; absent a shebang, `sh` is used. `--root` uses
passwordless sudo. The default run limit is 300 seconds; `--timeout N` overrides
it, including waiting for the per-machine run lock and reading standard input.
Timeout is status 124; SSH failures normally return 255. A script may itself use
those statuses, so callers should also retain runner diagnostics. SSH interruption
bounds the host call; it does not guarantee termination of detached guest children.
Outer SSH invokes this same interface with the script redirected to its standard input.

Talos has no shell. Its scripts run on the host with the machine's TALOSCONFIG,
endpoint, node and an executable `talosctl` wrapper configured first on PATH.
The declared shebang is honored on the host as it is over SSH; no shebang means
`sh`. `--root` uses the same administrative Talos API credentials, without host
privilege escalation. Serial-console transport is
retained only for explicitly documented bootstrap/fallback access. Serial errors
retain no console tails or frames. Routine SSH execution avoids serial login.

VMs run in durable user service units and acquire nonblocking `flock` locks on the
shared numbered slots before QEMU starts. A slot supplies 4 GiB RAM / 2 vCPU;
`debian-server` holds two, with a 40 GiB disk; the Gentoo compiler holds four.
QEMU inherits the locks. Host memory limits bound each unit. Unit console output
is discarded. No guest inventory is part of lifecycle operations.

## Validation boundary

Only Debian is used for instrument output, copy-out, timeout and error-path tests.
Check-system smoke tests redirect all stdout/stderr to `/dev/null` and retain
exit statuses only: boot/login, `exit 0`, and a selected nonzero `exit` value.
Do not use `copy-out` on a check machine during preparation. Release documents,
published checksum/signature verification and host-authored inputs are not guest
observations. Concrete check inputs still require a repository commit before
any subsequent check observation.

SSH and Talos `run` streams output directly, so the host runner does not retain an
entire command transcript in RAM. Internal lifecycle checks discard output;
`copy-out` captures its command result for decoding/extraction. Serial
fallback preserves the earlier framed transport and buffers its command result.
Lifecycle commands `new/start/stop/kill/destroy` use the same per-machine lock.
The supplement in `raw/debian/timeout-supplement.json` confirms timeout handling
before stdin arrives and while waiting for the command lock, without starting a VM.

## Late-system supplement

See [KIT2-READY.md](KIT2-READY.md) for the later MicroOS and Guix preparation.
Guix retains the unchanged previous installation and its serial login credentials
from the host-authored recipe. Its base metadata sets `passive_boot_login: true`:
startup waits for the login prompt within the existing boot deadline without
sending an interrupt. Subsequent `run` calls retain the existing framed serial
transport and their explicit time limits. This restores the prior working boot
access method; it does not apply the unsuccessful SSH declaration.
The KIT2 Guix smoke test passed boot/login and script statuses, but native
`stop` returned 1 when QEMU did not exit within the bound. The subsequent
`kill` and `destroy` returned 0. Until separately resolved, callers must allow
this documented shutdown fallback; see `raw/guix-kit2/status.txt`.

MicroOS uses the verified same-release plain KVM/XEN image and the documented
Combustion first-boot recipe. Preparation mounts `/home` before creating user
access and uses the same two virtual NICs and MAC addresses as the runner.
Its base metadata selects SSH with the lab key, q35 and UEFI. The exact selected
recipe is `install/microos/kit2/attempt-6/`; the preparation history remains
under `parts/microos-kit2.md`.

## FX rehearsal runner

`rehearsal/fx-run.py SYSTEM ROUND` creates a fresh throwaway clone for repair
round1–4, recorded under numeric keys11–14. It refuses an existing clone or a
repeated round. Actions run in a detached guest session with separate logs. A
batch timeout triggers bounded termination and a privileged session-absence
check that distinguishes pgrep absence from privilege or execution errors.
Uncertified termination refuses collection. Completed action statuses and stderr
are preserved; stdout is deleted unread. The collector emits aggregate counts
from memory and raw object/query/member files are deleted without being opened
by the rehearsal harness. Collector stderr and coverage are retained under
`rehearsal/SYSTEM/diagnostics/`. Every diagnostic read is disclosed.

Whole-run duration includes clone creation, twenty transports, all assigned
actions, collection and destruction. Each system must pass all criteria or
exhaust four repair rounds before finalization. A later source repair cannot
convert an exhausted system's old numerical evidence into a successful fresh run.

## FX serial transport repair

A candidate shell prompt first requires a unique exact printf SYNC response. Serial input is paced one byte every 10 ms; fixed transport calls send about 2700 bytes including protocol shell syntax (about 27 s nominal transmission). The serial transport disables echo with an acknowledged short command, stages its receiver in 128-character base64 chunks, checks the complete encoded receiver SHA-256 and decoder success, then evaluates it. The payload independently checks SHA-256 and decoder success before execution; a sentinel preserves trailing newlines. A unique exact ACK and successful terminal-echo restoration gate the final CLOSED frame. Output frames check sequence and encoded length. The guest requires its existing shell, base64, sha256sum, awk and stty; no tool is installed. Fixed-command synthetic PTY cases cover successful and nonzero exit statuses, corrupt receiver, corrupt payload, wrong ACK and initial stty failure. Synthetic tests establish protocol behavior, not guest readiness; fresh 20-call rehearsal establishes readiness.

The four fresh Guix repair rounds did not establish reliable live login and command delivery. The final round failed boot readiness after shell-SYNC and wrapper-chunk timeouts; native shutdown failed and the kill/destroy fallback removed the clone. The synthetic protocol tests do not establish guest readiness. See `rehearsal/guix/FIX.md` and `READY.md`. NixOS passed its fresh twenty-call sequence.
