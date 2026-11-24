# Void finding 4 rehearsal

2026-11-23 UTC. V03, V07 and V09 each reached the three-distinct-failed-attempt
endpoint. Each is **not-obtainable from the attempted surviving sources and
snapshots**. This is not a claim of universal query impossibility. No complete
missing fact was obtained, no object decision was taken and no hypothesis
outcome is assigned.

`diagnostics/status.tsv`: fresh clone boot exit 0, 16.225 seconds; unchanged
ordinary actions exit 0, 292.849 seconds; all twelve action/substep rows in
`diagnostics/actions.tsv` exit 0. Five distinct targeted query methods each
exit 0 (0.197, 0.197, 0.653, 0.196, 0.197 seconds respectively). A successful
query exit is not successful acquisition of the full missing fact. The
unchanged full collector was not rerun; its last exit-0 evidence remains
`S4/rehearsal/void/round3/status.tsv`.

| Fact | Attempted methods | Evidence and why the full fact was not obtained |
|---|---|---|
| V03 | 01 retained event logs; 02 command histories; 03 installation artifacts/package metadata | 01: all eight specified log roots absent. 02: none of the four specified history types exists under the searched account homes. 03: four specified installer-record locations absent; two account backups present, 331 metadata records parsed, zero `install-script`/`remove-script` fields. A backup supplies a state, not an executed choice event or default-versus-later-selection record. These three independent source routes did not provide account/sudo creation or choice events. |
| V07 | 01 retained event logs; 02 command histories; 03 installation artifacts/package metadata | Same acquired sources, searched for the five configuration/key/mount targets. No retained event or history source was available; source/default metadata and account backups do not establish the historical creator of live.conf, module configuration, the wheel rule, mount contents or trust keys. No chooser is inferred from present values. |
| V09 | 01 retained event logs; 02 command histories; 04 live descriptor/mapping snapshot; 05 running-process overrides/current policy | No searched event/history source was available. 04: 126 processes, 430 descriptor links, 126 map reads; zero certificate-path descriptor links or mappings; 25 TLS-library mapping lines; one descriptor read error. Library mappings do not establish certificate use, and a closed earlier read is invisible. 05: 126 process environments/command lines; zero matching trust-path overrides/references; two policy files with 258 nonblank noncomment directives. Policy content does not identify actual use or a chooser. The required endpoint was reached after routes 01, 02 and 04 failed to obtain complete trust-choice and actual-use facts. Route 04 is the third distinct attempt and includes actual current-consumer queries within its stated snapshot limits. Route 05 is supplementary after that endpoint. |

Exact scripts: `probes/01-retained-event-logs.py` through
`probes/05-trust-process-overrides.py`. Their JSON diagnostic reductions are
under `diagnostics/` with matching basenames. `attempts.tsv` joins each fact to
its methods, status and evidence. `expectations.md` gives primary-source URLs,
quoted passages, and expectations written before the queries.

Coverage limits remain explicit: log files are capped at 16 MiB each, histories
at 4 MiB, parsed package metadata at 16 MiB. The diagnostics report zero size
exclusions and zero read/parse errors for routes 01–03. The process snapshots
cover the guest process namespace at their respective instant,
not prior use or every namespace. Route 04 records one read error, rather than
silently calling its scan complete. Pattern searches are only candidate
finders; a zero pattern count is not proof of absence of all possible event
encodings. Here routes 01–02 have zero files to search, so their failure is
absence of those searched sources, not absence of an English phrase. Route 03
checks the named locations and metadata fields only, not all possible installer
or package-cache representations. No inference of complete history is made.

No complete new fact qualifies as recordable, so no new collector module or
factual field is proposed. The published collector continues to preserve
unknown historical fields; the rehearsal probes are retained as method evidence,
not substituted for object facts at observation. The source state, policy and
library counts do not turn any group into recordable.

Cleanup: destroy exit 0, 3.842 seconds. `diagnostics/cleanup.json` verifies clone
absence and that no inventory was written. The isolated server runner was then
removed and its absence verified with exit 0; `cleanup-final.json` records this.
Only diagnostic aggregates, command sources, action status/stderr, and input
hashes remain here. `deployed-inputs.tsv` verifies all 23 staged source files
against local inputs; `preservation.json` verifies 24 snapshotted inputs still
match. Read-only bases and earlier records were not modified. Independent
acceptance remains with the assigned review.

Procedure deviation: route 05 was a redundant fourth V09 query, run after the three distinct failed attempts in routes 01, 02 and 04 had already reached the required stopping endpoint. It exceeded the requested endpoint and was not necessary to establish the terminal status. Its evidence is retained for transparency and its `attempts.tsv` status is `supplementary-after-endpoint`. No further probe was run for this documentation correction.
