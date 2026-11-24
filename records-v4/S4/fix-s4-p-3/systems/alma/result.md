# Alma historical fact rehearsals

2026-11-23 UTC. This is instrument preparation, not an observation or an object decision. Results apply to the retained sources and query routes actually attempted, not to every conceivable source.

(not published: orchestration or scratch) records primary-source passages and the expectation before the first run. `probe.py` contains the new fact-specific queries and diagnostic reducer; `run.py` stages unchanged ordinary actions on a new copy, runs the targeted extension, then destroys the copy. The original collector and earlier rounds were not changed. Only the changed historical queries were rerun; the unchanged full collector's prior successful run remains `S4/rehearsal/alma/round3/status.tsv`.

First fresh copy: boot exit 0 in 16.428 s; ordinary actions exit 0 in 132.811 s (nine individual exits 0); targeted probe exit 0 in 0.994 s; destroy exit 0 in 2.273 s. See `raw/status.tsv` and `raw/actions.tsv`. Poll status 1 means the action completion marker had not yet appeared; it is not an action failure.

The first run acquired the accessible journal once (2,131 message lines, exit 0), then reused it for the five target predicates. Every target had zero journal matches. Audit queries use the actual target paths, selected executables and the MAC_CONFIG_CHANGE record type; every audit query returned 1 with the no-matches diagnostic. The separate application/installer route reads regular matching log files once, reusing their bytes across fact predicates. Every log read returned 0, none reached the 32 MiB per-file cap. Detailed commands, file lists, statuses, times, counts and path coverage are in `raw/fact-diagnostics.jsonl`. Source text was held only in the guest process and never saved or opened as an inventory.

| Fact | Journal route | Audit route | Application/installer route | Terminal status |
|---|---|---|---|---|
| A03 | 0 matching target messages | 6 path queries; all no matches | 28 target mentions, 2 operation-pattern mentions; no target-path coverage for boot/grubenv, boot entries, firewall zones or kernel values. Neither complete eight-row coverage nor the installation-choice/default/later-change distinction is established. | not-obtainable after three different failed routes |
| A04 | 0 matching unit messages | 2 unit-link paths and systemctl executable; all no matches | 4 unit mentions; 0 disable/preset/unlink/remove operation matches. A unit mention does not identify a historical disablement event. | not-obtainable after three different failed routes |
| A07 | 0 matching key messages | 2 RPM database paths and rpm executable; all no matches | Exact-key import context exists, but the preceding command is linked only by position in a log segment, without PID/transaction correlation. Full original acquisition reason remains unknown. | not-obtainable after three different failed routes; partial event fields retained |
| A09 | 0 ALSA target messages | stored-value path and alsactl executable; both no matches | 0 ALSA path/value/tool mentions. No stored-value creation record returned. | not-obtainable after three different failed routes |
| A11 | 0 boolean target messages | persistent-value path and MAC_CONFIG_CHANGE; both no matches | 16 generic tool mentions. The distinct follow-up finds 0 persistent setsebool commands, 0 semanage boolean modifications, 0 booleans.local references and 0 boolean audit events. | not-obtainable after three different failed routes |

The first application scan found one generic key import-operation candidate and 16 boolean-tool mentions. These were not discarded as irrelevant without examination: `CANDIDATE-(not published: orchestration)` describes the distinct exact-key/persistent-operation verification query on a second fresh copy. It retains only diagnostic counts. Zero lexical matches establishes failure of the specified search, not universal absence of a historical event. Matching words alone do not establish a complete fact.

Cleanup for the first copy is recorded in `raw/cleanup.json`: the clone is absent; no inventory was created and no event payload was saved. No record in this folder assigns a decision to an object. The future collector retains its explicit unknowns; no current file, script text or present policy is converted into a historical claim.


## Candidate and structured follow-ups

`raw2/fact-diagnostics.jsonl` records the distinct candidate verification. Every log read succeeded without reaching the cap. For A07 it found one exact-key import message in the DNF log; the absence of a same-line English reason token was **not** treated as proof of absence of the requested fact. A further structured parser was built, with expectation and primary-source references in `KEY-(not published: orchestration)`. Its fresh rehearsal (`raw3/fact-diagnostics.jsonl`) records one target event, one complete set of measured command/fingerprint/source/success fields, and zero commands rejected by the safe grammar. No raw event row was read or retained.

The primary implementation sources are https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/base.py (`_get_key_for_package`, repository key URLs, import operation and success log), https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/crypto.py (`log_key_import`, fingerprint and source fields), and https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/cli/cli.py (`_log_essentials`, command logging). In the first source, the function is described as “Retrieve a key for a package”; “Key imported successfully” follows a zero return from the import operation. These passages explain the logged fields. They do not add a missing concrete PID or transaction correlation. The adapter therefore retains measured event context only and does not emit an explicit/dependent reason. **A07 remains not-obtainable for its full original reason after the three attempted routes; this partial context does not increase the recordable numerator.** The standalone structured success is not a claim that the full missing fact was recovered.

All five assigned groups have reached the task's failed-three-routes stopping condition. This status describes these attempts, not impossibility of any future query. `fact-status.tsv` has the requested five-column schema and one row per group. No first-night row is assigned a decision.

## Assembled check

The initial full-collector launch completed the ordinary actions but was rejected before any query because its clone name lacked the required `reh-` prefix. `LAUNCH-CORRECTION.md` records the failure and the corrected fresh rehearsal; it is not counted as a fact attempt. The byte-identical publication layout and schema are documented in `INTEGRATION.md`. The adapter is useful as partial measured evidence only; it does not change the five terminal full-fact statuses.


| Fresh run | Boot seconds | Actions seconds | Targeted query / collector seconds | Exit | Destroy seconds |
|---|---:|---:|---:|---:|---:|
| targeted routes (`raw/status.tsv`) | 16.428 | 132.811 | 0.994 | 0 | 2.273 |
| candidate verification (`raw2/status.tsv`) | 16.425 | 122.595 | 1.251 | 0 | 2.583 |
| structured key fields (`raw3/status.tsv`) | 16.421 | 102.211 | 0.194 | 0 | 2.285 |
| rejected full launch (`raw4/status.tsv`) | 16.425 | 122.541 | 0.033 | 1 | 2.286 |
| final assembled collector (`raw5/status.tsv`) | 16.428 | 112.403 | 114.397 | 0 | 2.856 |

The final assembled collector completed with exit 0 in 114.397 s. `raw5/fact-summary.json` records one joined key-event row, one complete measured-field row, and query exit 0. This does not establish the full A07 reason. `raw5/coverage.tsv` records the new query's transport status and timing; all event payloads, inventories and query stdout were deleted unread. Nine of nine ordinary actions returned zero on each of the five fresh copies; there are no action failures to carry forward. The full launch validation failure was preserved rather than hidden.

Final tested files: wrapper SHA-256 `d617cd228e069927b2f04e1cb4f64bcb52fcb0874b14b19119b6bd33b42c84e2`; adapter SHA-256 `f260c683630165f415fb711c4372232ef075fe630e85d6ce295c2a447a4eebb8`. The final adapter uses byte-bounded reads and explicitly marks retained partial stdout from a nonzero query as unknown; seven synthetic tests passed. Exact integration/schema are in `INTEGRATION.md`.

## Cleanup and preservation

Every run's `cleanup.json` confirms its clone is absent. The final collector inventory is removed (`raw5/cleanup.json`). `raw/server-cleanup.json` verifies zero remaining clone directories, zero active owned QEMU processes, a read-only base, and complete removal of the server task root, including copied sources and bytecode caches. The task runner remained byte-identical to the original. The 52 staged core/action/adapter files matched their local counterparts (`raw/staged-inputs-check.json`); original action files and the original Alma extension match their before/after hashes (`raw/source-preservation.json`). No earlier-round output or original collector file was modified. Rehearsal diagnostic summaries only remain here; no object decision or hypothesis outcome is taken from them.
