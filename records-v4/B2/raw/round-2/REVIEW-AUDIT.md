# Offline audit transport review

Reviewed 2026-11-23 UTC. Scope: `audit.py`, `AUDIT-TRANSPORT.md`, the frozen `round3-driver.py`, and the prior/current saved `boot-order.jsonl` outputs.

Accepted as a narrow evidence-parser correction. The frozen driver obtains `After` and `Requires` with `systemctl show` for four named units, writes the property listing, and asserts only that each listing contains `stand-replay.service`. It does not create an execution-order assertion from the order of dependency tokens.

The two saved outputs have the same first JSON assertion schema and pass verdict. They retain the same four units, property framing, blank separators, dependency-token spelling, and token multiplicities. The token order inside each `Requires=` or `After=` listing differs. Treating that enumeration order as an execution order would reject equivalent evidence.

The revised parser remains strict where the test has evidence: it requires exactly twelve transport lines after the JSON assertion; the four expected unit names in order; exact `Requires=` and `After=` framing; each blank separator; a nonempty token list with `stand-replay.service`; and equality of separately sorted token lists. Sorting preserves duplicate token counts, and does not remove or rename a token. The JSON assertion still undergoes its existing schema/signature comparison and false-verdict collection.

The relative-path correction is also narrow. Resolving `--final` and `--combined-declaration` before relative-path reporting repairs the observed distinction between a missing input and an invalid relative path. A relative `--final B2/raw/round-2/final-1` recheck now has zero invalid sections and four incomplete sections, as expected for the partial evidence; it does not treat the incomplete sections as successful.

I found no evidence weakening or false acceptance in this correction. This review accepts neither the complete suite nor any Round 2 variant; the audit remains a finite saved-evidence consistency check.
