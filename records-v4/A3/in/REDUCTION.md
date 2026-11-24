# Base-inventory subtraction

This inventory is beyond the published four-check plan (PROTOCOL.md Section 5); it supplies no hypothesis outcome or classification.

Run `python3 A3/in/reduce.py developer gaming server` from the night folder. For each machine, the inputs are the complete collector output directories `raw/MACHINE/` and `raw/MACHINE-base/`. The latter comes from an untouched disposable clone of the same clean base, using the same committed collector.

An object is removed only when a base object has the same level, kind, name and recorded facts. Facts comprise the entire JSON `members` value, complete referenced member-table rows, and the package object's rows from `package-files.tsv` (path, integrity and rule). JSON key order and table row order are not facts; duplicate rows are retained. Every timestamp, signature, mode, owner, runtime value, unknown marker and completeness flag is compared exactly. No volatile facts are discarded and no missing facts are supplied.

Two locator normalizations allow comparison across inventories: member-file references are resolved to their complete TSV contents, and the documented `native_package_ids` field is resolved to referenced level/kind/name identities. The package-file object ID joins rows to the source object; it is not compared as a fact. Evidence filenames and object IDs are locators, not facts; their bytes differ with machine names or query sequence and are not compared. A missing referenced file or object fails the reduction instead of silently treating it as empty.

All other fields remain unchanged. A match means the recorded facts match, including any explicit unknown values; it does not prove an unknown real-world fact. This exact subtraction can retain objects changed by ordinary boot, elapsed time, collection, or instrument staging. It does not claim every retained object was caused by an action. It never removes such rows using a causal guess.

Each retained source row appears once, in its original order, without merging. The output header is exactly `id\tpart\tmachine\tkind\tname\tmembers\tevidence`. IDs are prefixed `MACHINE-`, part is `A3`, and kind is `LEVEL:KIND`. Names and members are copied verbatim. Evidence identifies the source object row and inventory root; original relative member and query references resolve inside that root. Complete raw inventories remain unchanged.

`reduction-MACHINE.tsv` records keep/drop, every matching base ID, and SHA-256 of the canonical identity/facts comparison value. `counts-MACHINE.json` records base counts and lived-in counts before/after, overall and by level/kind. READY.md reports these counts and collection limitations. No object is omitted because an action failed or a collector query was incomplete.
