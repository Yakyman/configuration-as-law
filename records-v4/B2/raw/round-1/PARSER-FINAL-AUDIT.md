# Final saved-evidence parser audit

Recorded 2026-11-23T12:26:18Z. Host-only validation of existing evidence; no guest, build, or experiment was run. Only `B2/tools/summarize-round1.py` was changed. This record makes no closure decision.

## Original failure and provenance

The complete exported tree first failed strict validation with:

```text
evidence validation failed: B2/raw/round-1/final-2/carried-suite/events.jsonl: missing, duplicate, reordered, unknown, or schema/phase-changed record
```

The original message is quoted above. `metrics-validation.log` now records the
subsequent successful final validation.
The previously frozen parser SHA-256 in `B2/raw/round-1/host-tools-sha256.json` is `f40b38dd4b32a8bea6dbb8c658883987593e33985667dbdbfb891ce784fed0b5`. Reversing this bounded change reproduced that exact digest; the original source identity was not inferred from target evidence.

Both event logs contain 36 records. The only differing contract identities were these four expected cleanup IDs:

| Pinned baseline ID | Required final-2 ID |
|---|---|
| CLEANUP-bc4-baseline-language | CLEANUP-bc4-final-2-language |
| CLEANUP-bc4-baseline-applications | CLEANUP-bc4-final-2-applications |
| CLEANUP-bc4-baseline-system | CLEANUP-bc4-final-2-system |
| CLEANUP-bc4-baseline-ordinary | CLEANUP-bc4-final-2-ordinary |

`B2/build/round4-driver.py` constructs guest names from `bc4-` plus the supplied phase and suite label, then prefixes that name with `CLEANUP-` for the expected cleanup event. Its reviewed SHA-256 is `bd79bfbed47a7d4ee5327c52eea5b940e944ea37b2906c7d86449b6182e087af`. The parser now pins that source and maps only these four exact expected identities. Existing exact record order, keys, result IDs, file inventories, source hashes, marker payloads and summary checks remain mandatory. Unknown phase names are not normalized or accepted.

## Local validation

`python3 B2/tools/summarize-round1.py --check-only` completed successfully against the full actual final-2 export. No metrics file was written by this check. There were no subsequent contract mismatches. The validated controller has 22 successful steps and no retained guest or peer; exact carried and combined file inventories contain 123 and 50 files respectively.

| New/supplement log | Result rows | Boolean assertions | False assertions |
|---|---:|---:|---:|
| gate.jsonl | 9 | 9 | 0 |
| shell-reboot.jsonl | 1 | 1 | 0 |
| shell.jsonl | 28 | 28 | 6 |
| supplement/direct.jsonl | 17 | 17 | 5 |
| supplement/extra.jsonl | 21 | 16 | 4 |
| tools.jsonl | 86 | 86 | 1 |

There are 157 Boolean assertions, 141 true and 16 false. The extra suite additionally contains five null-verdict observations; these are neither passes nor failures. All 16 real failures remain in the aggregate: six shell saved-input failures, one native-root account bypass, five direct saved-input failures and four extra saved-input failures. The earlier FFI detector error is not reintroduced.

The eight carried assertion suites retain 79 language, 131 application, 32 system, 59 ordinary, 166 authority, 133 code/lifecycle, 35 transaction and nine power-cut assertions, with no false assertion. Exact ordinary-shell routing markers retain counts 55 language, 59 application, 16 system and 46 ordinary. The source-defined dynamic DOWNLOAD loopback port remains bounded and recorded. Full combined and supplementary readback/summary validation completed within the same strict check.

Three host-only altered in-memory copies of the carried event log were rejected: a cleanup ID using `final-3`, an omitted cleanup expectation, and a duplicate cleanup expectation. No evidence file was altered. Earlier malformed/unknown/duplicate/transport checks are unchanged.

The corrected parser SHA-256 is `df131f96cae4dc61cf4c10b6ddf196472051fdedd51cc10478fd353efbdcc9a4`. The unaccepted publication's old host-tool manifest must be replaced and independently reviewed before final metrics/publication acceptance. Frozen installed recipe bytes, images, payloads and guest evidence do not change.
