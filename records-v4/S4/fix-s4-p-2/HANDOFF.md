# Observation handoff

2026-11-23 UTC. Before delivery, the operator makes a separate copy of each new observation using the committed neutralize.py and literal map. Original observations remain frozen. A copy preserves object/membership tables, levels, IDs, names, evidence paths, raw query outputs, bytes, hashes, numerical counters, failure statuses and unknown fields. Only enumerated collector-written labels change. This adds no fact, decision or rule to the published text.

The handoff uses these neutral terms:

| Table / field | Value and meaning |
|---|---|
| npm-archive-sources.tsv / status | `verified-archive:cache-identity-reference`: verified archive selected by cache identity. Other source types retain their existing labels. |
| old-package-member-integrity.tsv / status | `no-reference-found`: no reference entry was found by the implemented searches. Expected/actual fields remain as collected. |
| void-configuration-facts.tsv / historical_creator | `creator-field-empty`: this field contains no creator record. |
| alma-facts.tsv / status | `recorded-snapshot`, `recorded-directives`, `recorded-current-query`, `recorded-bounded-extract`, `recorded-script-text`: name the recorded source. The fact/value/evidence fields retain all data. |
| talos-fact-index.tsv / image_integrity | `image-reference-field-empty`: this field contains no original image reference comparison. |
| fact-summary.json / adapters | Two counter keys use `cache-identity-reference` and `no-reference-found`; their numeric values are unchanged. |

Only whole cells in the named columns and exact keys in the named JSON containers are mapped. A literal inside a path, object name, content field or raw source is never substituted. Files outside the map are byte-identical; tables with no replacement are byte-identical. Modified tables keep the same columns and rows. Missing system-specific tables in a partial observation remain missing. Unknown facts and failed reads retain their status; no absence becomes a positive fact. The copier rejects existing outputs, links, malformed mapped tables and counter-key collisions. A failed handoff is withheld, never repaired by recollecting an observation.

From the laboratory root, with S4_INPUTS pointing to the committed S4 directory, use new destinations and external audit paths (create D1b/handoff-audit first):

```sh
mkdir -p D1b/handoff-audit
python3 "$S4_INPUTS/fix-s4-p-2/neutralize.py" D1b/raw/alma D1b/handoff/alma --report D1b/handoff-audit/alma.json
python3 "$S4_INPUTS/fix-s4-p-2/neutralize.py" D1b/raw/void D1b/handoff/void --report D1b/handoff-audit/void.json
python3 "$S4_INPUTS/fix-s4-p-2/neutralize.py" D1b/raw/gentoo D1b/handoff/gentoo --report D1b/handoff-audit/gentoo.json
python3 "$S4_INPUTS/fix-s4-p-2/neutralize.py" D1b/raw/microos D1b/handoff/microos --report D1b/handoff-audit/microos.json
python3 "$S4_INPUTS/fix-s4-p-2/neutralize.py" D1b/raw/talos D1b/handoff/talos --report D1b/handoff-audit/talos.json
```

Each exit status is recorded. A successful audit gives original/copy hashes for every file, verifies the source did not change, and counts replacements. The matching party uses the unchanged match.py rule on objects.tsv; these bytes are identical in original and copy. Missing observations remain missing and are reported under the original procedure.

Deciding parties receive the handoff copy, unchanged matching output, and documents in CLASSIFICATION-INPUTS.list (including this document), alongside the fixed text/protocol required by the task. Withhold original unneutralized observations, literal-map source, operator audit, rehearsal outputs, readiness/status summaries, correction/review reports and all earlier decisions during their independent work. Preserve these withheld materials for publication as records. The map and copier are instrument inputs committed before observation, not classification guidance.
