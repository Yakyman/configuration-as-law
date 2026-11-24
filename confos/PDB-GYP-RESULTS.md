# Private39 native pdb/gyp candidate — 17 checks passed

Supersedes the preparation-only status in PDB-GYP-DRAFT.md. No production40/41
files or packages changed; this is a private candidate for a later release.

`pdb-gyp-private-run.sh` completed with exit0 and
`PDB GYP PRIVATE NATIVE MATRIX PASS 17`, `PDB GYP PRIVATE PIPELINE PASS`.
Full outputs: `pdb-gyp-private.log`; boot log: `pdb-gyp-private.serial`.

| Checks | Native result |
|---|---|
| Unrecorded home/cwd pdb rc, symlink and inherited-fd aliases | Four RC1 PermissionError refusals; attempted markers absent. Main script was recorded, so refusal is specifically rc loading. |
| Recorded cwd/home rc and main; missing rc; typed debugger command | Four RC0 positives; recorded/typed markers and main output present. |
| Unrecorded gyp main, symlink/fd aliases, recursive/explicit includes | Five RC1 PermissionError refusals before command expansion; attempted markers absent. |
| Recorded gyp main and include | Two RC0 generator executions; expected expansion markers present. |
| Explicit Python data read/exec and piped typed Python | Two RC0 markers; R4 data routes preserved. |

All four gyp binary/source archives matched hashes in PDB-GYP-DRAFT.md. Debian
source extraction (including remove-old-pkg_resources.patch) and binary package
input.py had identical SHA256. dpkg-source reported no acceptable signature in the
worker keyring; pinned archive SHA256 checks independently passed.

The private reader component inherited sealed39 bytes and extended only its
optional-reader manifest plus two compressed payloads. Gyp override is active
only when the gyp package is selected. Assembly confirmed exact patched module
hashes and absence of stale pdb/input bytecode before boot. Whole-component
checksum, complete optional manifest, payloads, fixtures, source archives and
licences are retained in the evidence archive. Original failure evidence remains
unchanged in `records/search-followup-0.39.log` and search request1.

Evidence: `pdb-gyp-evidence.tar.gz`, SHA256
`58eb67c7cea6ac2cad860994017e7619aca58f10f189e3b8ebd6a6d8c5e0d8a5`.
The disposable guest was stopped and its3.3G tree deleted after collection;
worker usage then35G. Scripts reproduce from sealed39 without touching main
packages/images. Integrating a later release still needs exact-original module
hash guards when optional overrides apply, updated declaration requirements,
source/component packaging and independent case-party checks. This experiment
does not claim unknown gyp versions, node-gyp copies or Flatpak pdb are guarded.
