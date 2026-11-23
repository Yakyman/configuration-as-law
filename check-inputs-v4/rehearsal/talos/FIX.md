# Talos repair result

NOT READY after four new fresh-clone rounds (11–14). No hypothesis outcome is assigned.

| Round | Collector | All query statuses | Transport | L2 rows | Known reason | Known packaged-file integrity | Whole run | Cleanup |
|---|---|---|---|---|---|---|---|---|
| 11 | 0, 4.458 s | 0 | 20/20 | 48 | 0/1 | 0/0, not a passing ratio | 30.691 s | destroy0 |
| 12 | 0, 7.903 s | 0 | 20/20 | 48 | 1/1 | 0/0, not a passing ratio | 34.676 s | destroy0 |
| 13 | 0, 8.227 s | 0 | 20/20 | 48 | 1/1 | 0/0, not a passing ratio | 46.058 s | destroy0 |
| 14 | 0, 10.296 s | 0 | 20/20 | 53 | 1/1 | 0/95 | 42.599 s | destroy0 |

Evidence: status.tsv, counts.tsv, diagnostics/fx1/coverage.tsv, diagnostics/fx2/collector.stderr, diagnostics/fx4/collector.stderr. Diagnostic reads are enumerated in DISCLOSURES.fragment.md. No actions apply to this immutable system.

What was wrong and repaired:

- Image facts were an opaque semicolon string, which numeric reduction could not interpret. They are now structured fields on exactly one package-like image object.
- The collector did not inspect the configured install image. A host-side standard-library filter now retains only that field from the active config, including the v1.14 installer.image nesting; credentials never enter retained raw output. Reason is explicit1/1.
- Legacy runtime mount records omit populated flags. The collector now queries block mount status and disk readonly state and joins the actual root mount source to a readonly disk. All four mapping queries must succeed and parse. An overlay with readonly lower devices is not silently treated as readonly.
- Installed /usr namespace was excluded as if it were a stored image artifact. Bounded API listings now supply real packaged regular-file facts, while keeping one image package and excluding actual images, container stores, snapshots and pseudo-filesystems. The final run obtained 95 packaged files.
- Offline synthetic fixtures verify the readonly-source join, rejection of overlay inference, nested-mount masking, bounded listing and failure continuation (fixture.json).

What remains: the collected API mappings do not certify readonly state for the complete running image namespace, including every covering mount. All 95 listed package-file integrities correctly remain unknown. Public version-specific boot source constructs a readonly root, but this design fact was not relabeled as measured current mount state. Complete image manifest, full namespace/mount coverage and complete second-level inventory remain unavailable through the implemented bounded API interface. TALOS-COLLECT.md and COLLECT.fragment.md state the exact limitations and Section9.2 reporting rule. No fifth round was run.

Related review findings: the prior package-fact limitation is repaired for reason but not integrity. Review finding 8's unstated metal-amd64 variant is a frozen choice/documentation issue; this system worker did not change CHOICES.md. Shared release evidence, final manifests, publication paths and cross-system records are handled by the coordinating task.

Post-round source review: final file-fact emission includes symlinks with unknown integrity; round 14 tested only 95 regular files. The final source requires certified complete covering-mount mapping for any file-integrity attribution, which these APIs cannot provide, so file integrity stays unknown even if root backing is readonly. Image-level integrity is also unknown rather than inferred from backing evidence. These conservative changes were not run as a fifth rehearsal and do not change the recorded round-14 counts.
