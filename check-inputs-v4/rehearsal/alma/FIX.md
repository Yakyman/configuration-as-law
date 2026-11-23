# Alma repair record

2026-11-23 UTC. The historical failure was instrument readiness, not a
hypothesis result. FX rounds 11–14 are fresh clones separate from the earlier
rounds. All four FX rounds are complete. Alma is not ready: known package reasons remain below the required threshold.

Repaired:
- RPM file modes distinguish directory ownership from packaged-file integrity.
  Directory ownership is retained. Symlinks compare the installed target with
  RPM FILELINKTOS instead of being uniformly unknown.
- RPM file digests are validated against algorithm-specific hexadecimal length;
  absent/zero algorithm uses the documented MD5 default.
- Shared package reconciliation propagates an unambiguous native reason through
  exact native metadata ownership, without directory-containment assumptions.
- A new helper stderr diagnostic identified root's denied traversal of the
  runtime document portal. The shared helper now represents that documented
  virtual alias boundary without claiming an empty directory.

Preserved limitations:
- DNF's native GROUP reason is distinct from USER and DEPENDENCY. Positive
  selected-group/environment records are retained as provenance but do not
  establish each member's individual historical selection. Independent review
  rejected a proposed binary conversion before the FX3 collector began.
- Missing OpenRC/Docker interfaces, unavailable user buses and inaccessible
  user Flatpak scopes are diagnosed and explicitly not collected.

No Alma action was replaced. All nine original actions have passed in all
four FX rounds. No inventory, raw query stdout, or member list was read.
Every diagnostic actually read is listed in `DISCLOSURES-FRAGMENT.md`.

| FX round | Actions | Collector | Whole run | L2 rows | Known package reason | Known packaged-file integrity | Cleanup |
|---|---|---|---|---|---|---|---|
| 11 | 9/9 zero | 2; 173.721 s | 280.153 s | 1689 | 1241/1561 | 120520/121931 | 0 |
| 12 | 9/9 zero | 2; 107.999 s | 231.291 s | 1689 | 1241/1561 | 120520/121931 | 0 |
| 13 | 9/9 zero | 0; 96.686 s | 202.641 s | not retained | not retained | not retained | 0 |
| 14 | 9/9 zero | 0; 76.862 s | 180.137 s | 1692 | 1238/1561 | 120520/121931 | 0 |

All four rounds passed 20/20 transport calls. Evidence: `status.tsv`, `counts.tsv`,
`diagnostics/fx1/coverage.tsv`, and `diagnostics/fx2/filesystem-live.stderr`.


Final round 14 has complete filesystem/in-memory reduction flags, collector
status zero, and 98.84% known packaged-file integrity. Known package reasons
are 79.31%; 261 native GROUP records plus one unknown RPM reason, 41 npm and
20 Python unknown reasons remain. The group reason is not recoded to satisfy
the threshold. The remaining nine nonzero queries have the same diagnosed
missing-interface, inaccessible-scope and missing-user-bus limitations, named
in `COLLECT-FRAGMENT.md` for integration into `COLLECT.md`.

Round 13 counters were lost during a concurrent transition of the shared
reduction implementation. No raw inventory was reopened to reconstruct them;
round 14 verifies the synchronized in-memory counter path. Its source hashes
matched before launch (`fx4-local.sha256`, `fx4-deployed.sha256`).

`CLEANUP.tsv` confirms that all four FX clones and all four transient raw-output
folders are absent. No Alma action replacements were necessary. Source review
of the selected-group conversion was independent; it rejected that conversion,
which was removed before any collector using it started.

Review finding 2, Alma portion: the historical round 3 was recovered into the
status/count tables by the coordinating task. New runs are complete and cleaned
before final records are regenerated. Other global input-review findings are
outside this system-specific work; the coordinating task tracks them.
