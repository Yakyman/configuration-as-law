# YaST DVD installation recipe

Image: `openSUSE-Tumbleweed-DVD-x86_64-Snapshot20261120-Media.iso`.
Verification: `raw/checksum-status.txt`, `raw/signature-status.txt` and the original published checksum/signature alongside them.

The complete system role “Desktop with KDE Plasma”, first in the YaST list, is a choice of this check under TASK-C1, not an installer default. All other installer proposals are accepted; no extra software selection is made. The ordinary account is `user`, with the disposable laboratory password `cal-test`.

`launch.sh` boots the verified DVD's kernel and initramfs in text mode, on one 40 GiB disk, 4096 MiB RAM and two virtual CPUs, under one available slot lock. The launcher is run under a persistent user service with output discarded. `terminal.py` holds the installer terminal in memory; `ui.py` sends recorded key inputs. Installer output is not stored as a transcript. The event log retains only UTC timestamps and the exact input bytes. No inventory commands are issued.

`verify-start.sh` verifies the download and launches the installer. It runs from the laboratory root with `LAB_ROOT` set to that root. The temporary parser dependency is `pyte`; it is installed only under the new installation directory and removed after installation.

Installer VM completed with exit status zero. The resulting disk is retained read-only; all boot/login and ordinary-action commands run on disposable overlays.

Sequence executed through the terminal:
1. At Language, Keyboard and License Agreement, F10 accepts English (US) and its default keyboard.
2. At “Activate online repositories now?”, F10 accepts Yes. At the repository selection, F10 retains the three preselected repositories.
3. At System Role, Space explicitly selects the first entry, “Desktop with KDE Plasma”; F10 applies it.
4. At Suggested Partitioning, F10 accepts the default guided proposal on the empty disk.
5. At Clock and Time Zone, F10 retains the default. All external records use UTC independently of the guest timezone.
6. At Local User, send `user<Tab><Tab>cal-test<Tab>cal-test`; the full name and generated username are `user`. Retain “Use this password for system administrator” and “Automatic Login”; F10 continues.
7. At Installation Settings, F10 opens confirmation; F9 confirms Install. No software selection is changed.

The terminal control sequences are F10=`ESC [ 21 ~`, F9=`ESC [ 20 ~`; exact bytes and timing are retained in `raw/input-events.jsonl`.

Command transport uses passive boot-time login detection and an openSUSE-specific anchored shell-prompt match in `C1/fix-c1-1/lab.sh`. These are host instrument corrections; the installed system is not edited to enable additional services or alter its boot declaration. The first failed transport attempt and idle-boot diagnostic are retained in `raw/boot-transport-diagnostic.txt`.

After the original ACPI request timed out, only the host runner shutdown path changed: root transport runs `systemctl --check-inhibitors=no poweroff --no-block` and waits for VM exit. `raw/lifecycle-status.txt` records successful new/user/root/stop/destroy with the final runner; `raw/lifecycle-runner.sha256` fixes its bytes. No guest services or defaults were changed for transport. All disposable overlays are removed, and the installed backing remains mode 444.
