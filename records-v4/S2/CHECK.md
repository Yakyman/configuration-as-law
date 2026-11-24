# Facts assembly checks

Completed 2026-11-23 UTC. This records assembly checks; the subsequent decisions and step review are separate.

- Coverage: 105 objects across all 15 fixed family titles: 72 explicitly listed inventory IDs, 12 further objects
  named in card prose, and 21 disk artifacts specified by the eight named B1 channels.
- Structure: exact seven-column header, 27,631 fact rows, unique family/object/fact keys, nonempty fields,
  consistent object identities, and 770 unknown rows. The summary count is recomputed from the data.
- Evidence: 135 local source paths exist; 16,050 filesystem attributes and 7,483 member attributes were compared
  against retained raw inventories without a mismatch. Sources for behavioral statements include quoted primary
  documentation and distinguish documented behavior from a historical observation.
- Content recovery: complete retained hashes support the Git hook/template comparison, the two recovered Alma
  service files, and four Void runit script/configuration files. A matching extension size and prefix does not
  establish complete historical bytes, version or permissions; those remain unknown.
- Boundary: no decision, verdict, card argument or sentence selection was imported. B1 channel evidence is exposed
  through column-only factual extracts. Directory examples preserve their original immediate-child scope.
- No fresh-machine probe was required for documented semantics. Unrecoverable historical details and unspecified
  B1 instances remain explicitly unknown. No machine or downloaded package/archive remains from this task.

Reproducible structural assembly: `python (not published: orchestration or scratch)`.
Source-attribute checking: `python (not published: orchestration or scratch)`.
Saved reports: `S2/raw/structure-check.json`, `S2/raw/source-check.json`,
`S2/raw/scope-and-recovery-check.json`, `S2/raw/runit-source-check.json`, and `S2/raw/digests.json`.
The per-object unknown facts and reasons are in `S2/FACTS.md`; their individual source pointers are in (not published: direct evidence at least 2 MB).
