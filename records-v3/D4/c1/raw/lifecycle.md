# Lifecycle and invocation record

Date: 2026-11-22 UTC. All guest commands use the pinned runner on the server;
script files are supplied on standard input from the laptop. Runner paths below
are relative to the server laboratory root. The connection explicitly uses the
existing user SSH configuration to bypass a local system-configuration permission
error; no host file was modified.

| Runner invocation | Record | Exit status |
|---|---|---|
| `./lab-fx-c1-1.sh new d4c1-nixos nixos` | `new-nixos.txt` | 0 |
| `./lab-fx-c1-1.sh new d4c1-guix guix` | `new-guix.txt` | 1 (boot/login timeout; VM retained) |
| `./lab-fx-c1-1.sh run d4c1-nixos < inspect-nixos.sh` | `inspect-nixos.txt` | 0 |
| `./lab-fx-c1-1.sh run d4c1-nixos --root < p2-nixos.sh` | `p2-nixos.txt` | 0 |
| `./lab-fx-c1-1.sh destroy d4c1-nixos` | `destroy-nixos.txt` | 0 |

The runner itself acquires shared VM-slot locks and launches persistent,
memory-bounded user service units. No other VM was inspected. After the Guix
startup timeout, its own QEMU log was empty. A normal `run` invocation was tried
on that retained clone, without restarting or replacing it; no Guix property
probe had yet run. This is an attempt to resolve transport access, not a repeated
property experiment. Its result is recorded separately.

| Remaining runner invocation | Record | Exit status |
|---|---|---|
| `./lab-fx-c1-1.sh run d4c1-guix < inspect-guix.sh` | `inspect-guix.txt` | 1 (wrapper syntax error; script not delivered) |
| `./lab-fx-c1-1.sh run d4c1-guix --root < p2-guix.sh` | `p2-guix.txt` | 1 (serial login timeout; script not delivered) |
| `./lab-fx-c1-1.sh destroy d4c1-guix` | `destroy-guix.txt` | 1 (graceful shutdown timeout) |
| `./lab-fx-c1-1.sh kill d4c1-guix` | `kill-guix.txt` | 0 |
| `./lab-fx-c1-1.sh destroy d4c1-guix` | `cleanup.txt` | 0 |

Final `test ! -e` checks of both owned VM directories succeeded; output is
`both_vm_directories_absent` in `cleanup.txt`. Both disposable disks are removed.
The forced shutdown is cleanup after failed transport, not a power-cut P2 probe.
No Guix script made a guest mutation, and no property experiment was repeated.
The Guix behavioral decisions use official documentation and versioned primary
sources only. The unattained exact guest transcript is explicitly not evidence.

The two task-owned lifecycle lock files were then removed after verifying both
VM directories absent; see lock-cleanup.txt. Shared slot locks were retained.
