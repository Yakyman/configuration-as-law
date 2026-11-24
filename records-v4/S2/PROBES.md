# Probe record

Recorded 2026-11-23 UTC.

No fresh-machine probe was run. Inventories were checked first, followed by ordinary-action records and primary
documentation. Missing historical transactions, complete old bytes, personal choices, and designated description
files cannot be reconstructed by observing a new object. The per-object reasons are in `FACTS.md` and (not published: direct evidence at least 2 MB).
The B1 descriptions identify no observed installation or artifact instance to reproduce.

Four further source checks were completed before treating missing content as unrecoverable:

- The Git sample hook and its installed template have matching hashes covering all 482 bytes; the template also
  has an unchanged native package digest. The equality and its limits are in family 10.
- The two Alma service files were recovered from official packages of the recorded versions. Their complete
  digests match the retained package manifests, and the inventory reports the original files unchanged.
  `parts/d1/raw/service-content-recovery.json` records the sources and digest comparison.
- One authoritative extension archive candidate matches the saved size and first-4096-byte digest. Its manifest
  lies outside that range; version, permission and full-file integrity facts remain unknown.
  `parts/d1/raw/amo-prefix-check.json` records the boundary.

- The Void runit stage-2 script, acpid run script, agetty run script and its configuration
  match complete retained hashes. Their launch commands and configured credential inheritance are recorded
  with the distinction between a configured launch context and a sampled live process.
  `raw/runit-source-check.json` records the full-byte comparisons.

These were source retrieval/comparison operations, not guest executions, installations, or repetitions of ordinary
actions. No virtual machine, disposable disk, server process, downloaded package archive, or extension archive
remains from this task. There is no runtime observation for which a preregistered expected result is required.
