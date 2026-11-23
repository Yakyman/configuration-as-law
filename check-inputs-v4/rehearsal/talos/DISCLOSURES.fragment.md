# Talos diagnostic disclosures

- `rehearsal/talos/diagnostics/fx1/collector.stderr`: read; empty, no machine facts disclosed.
- `rehearsal/talos/diagnostics/fx1/coverage.tsv`: first four query rows read; redacted configuration query succeeded but produced no matching image; block mount API returned 17 resource rows. No resource content read.
- `rehearsal/talos/diagnostics/fx2/collector.stderr`: read; the instrument matched one configured image and no readonly image mount under its initial narrow filesystem criterion. No names or raw query contents read.
- `rehearsal/talos/diagnostics/fx4/collector.stderr`: read; the repaired instrument matched one configured image and no API-proven readonly root mapping. No resource names, files or raw query contents read.

All four fresh-clone rounds (11–14) had collector status0, every query status0 and transport20/20. Final round14: collector10.296s, whole run42.599s, L2 rows53, reason known1/1, packaged regular files95, integrity known0/95. Each clone was destroyed with status0. Inventory outputs, raw query stdout and member lists were deleted unread. Only numeric reductions and the explicitly listed diagnostics were read.

A synthetic fixture ran locally with no machine access, after the task coordinator explicitly permitted offline parser fixtures; its output is fixture.json. The first unit-launch attempt omitted its working directory and exited before invoking the harness, leaving no clone; the corrected launch used the lab working directory.

After round 14, source review added symlinks with unknown integrity and prevented image/file integrity from being inferred without complete covering-mount or verification evidence. No fifth rehearsal ran. The published 0/95 integrity count describes the 95 regular files in round 14, not an unmeasured final-source symlink denominator.
