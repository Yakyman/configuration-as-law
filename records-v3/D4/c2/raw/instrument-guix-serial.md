# Guix serial transport: instrument defect and workaround (c2)

Times UTC, 2026-11-22.

- 06:33–06:37 `new d4c2-guix guix` failed: "Boot/login timed out; VM retained" (`vm-new-guix.txt`).
  Two later `run` calls failed with "Serial timeout", console tail ending in a bash continuation prompt `> `.
- 06:38 the clone was killed and destroyed (`kill`, `destroy`, both exit 0) and created again; `new` failed the same
  way at 06:42.
- Cause, from documentation: the Guix 1.5.0 manual, Base Services, `agetty-configuration` field `tty`: "This argument
  is optional, it will default to a reasonable default serial port used by the kernel Linux. ... If not and if there
  is a value for an option console with a tty in the Linux command line, agetty will extract the device name of the
  serial port from it and use that." (https://guix.gnu.org/manual/1.5.0/en/html_node/Base-Services.html). The
  installed declaration adds `console=ttyS0,115200n8` and a second `agetty-service-type` on `ttyS0`, so two login
  programs read ttyS0. The runner sends its payload in paced 8-byte chunks; with two readers the bytes are split
  between them (raw console output with interleaved characters was observed with `tools/` peek scripts).
- Workaround (no runner change, no service change): on the virtual console tty1, through QMP `send-key`
  (`../tools/qmpkeys.py`, screen read with QMP `screendump`, `../tools/ppm2png.py`), the ordinary user logged in and listed
  the processes holding ttyS0 open: agetty pid 316 (root) and a leftover user login shell `bash` pid 317. The user
  sent SIGSTOP to its own pid 317 (`kill -STOP 317`), logged out of tty1. After that, `run` and `run --root`
  succeeded (exit 0).
- Effects on the guest retained as instrumentation: one tty1 login of the ordinary user; a stopped user `bash`
  process; shell history of tty1. No package, service, account or file of the declaration was changed by this.
- No property was assessed from these observations.
- Diagnosis scripts (raw console peeks over the serial socket: Ctrl-C, Enter, one echo line; then a Ctrl-D plus
  `exec sleep 1e9` attempt that did not leave a single reader) were temporary files on the laptop and in the VM's host
  directory; they were removed with the VM. The QMP keyboard and screen tools are kept under `tools/`.
- 07:02–07:04: after the power cut and new boot of G1, the two-reader state came back (two root agettys, pids 356 and
  357, `d4c2-s4.png`). The ordinary user logged in on tty1 and stopped pid 357 with `sudo kill -STOP 357`; after
  that `run --root` succeeded.
