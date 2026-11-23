# Questions recorded by assessment c2 (not decided here)

1. Time scope of the properties (author question). S2.3-1: "The properties concern the computer after a completed
   application of the declaration, provided there was no breaking." Reading A (used by c2, literal): any moment after
   the last completed application while its declaration is in force (S3-3), so a later change by a built-in tool
   counts against P1 and P2. Reading B: only the state produced by the application itself (at the success report and,
   by S3-5, after an immediate power cut). Under B, NixOS × P2 and Guix × P2 would rest on records N1 and G1 alone, and
   Guix × P1 would need a fact c2 did not establish (whether per-user packages stay in force across a later
   `guix system reconfigure`). NixOS × P1 and both P4 cases do not depend on the reading.
2. Instrument: the selected Guix declaration adds an agetty on ttyS0 while `%base-services` already runs one on the
   kernel console ttyS0, so the serial runner meets two readers; `new` failed twice for c2 (`raw/instrument-guix-serial.md`).
3. Not examined: whether `nix-channel` / `guix pull` (changing the package source used by the next application without
   editing the declaration) is a path of the kind P4 excludes.
4. On the clean Guix installation, `guix system reconfigure /etc/config.scm` with the unchanged declaration failed
   (exit 1: refused a downgrade; D-G1 recommends `guix pull` before the first reconfigure). So c2 has no record of a
   reconfigure that reported success; under reading B of item 1, Guix × P2 would rest only on the installation as the
   last completed application.
