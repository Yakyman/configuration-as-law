# Object evidence review

Reviewed 2026-11-23 UTC from `final-1` saved evidence only. This is a review of the object lane, not acceptance of the still-running complete suite.

The object lane is internally consistent. `objects.jsonl` has the fixed ordered set of 52 result rows. It reports 49 passing required supported-operation assertions and three non-required boundary failures: `UNRECORDED-BYTECODE`, `EXTRACTED-CODE`, and `ALTERNATE-DATABASE`. One availability record is explicit as `UNTESTED`; it covers the two unavailable capability families C7.19 and C7.21. The summary has no failure of a required supported-operation assertion and keeps hypothesis outcome `?`. All 37 pure rule cases pass, and the two post-reboot rows pass. The offline auditor reports no invalid section for the available object evidence; missing complete-suite sections remain incomplete, as expected while the other lanes run.

The three failed boundaries are real testbed implementation boundary failures, although they are not failures of the required supported-operation assertions. An unrecorded bytecode file runs; extracted code runs; and the native installer succeeds against the alternate root and database, leaves the package and file readable, and leaves the declaration report unchanged. These results support keeping C1.3 and C7.18 open. They do not establish a general mechanism for arbitrary privileged paths.

The recorded positive examples are evidenced narrowly. `BYTECODE-RUN` exits zero and prints both `RECORDED-BYTECODE` and `DEFAULT-LANGUAGE:en`; the saved fixture shows that the recorded source reads the received default value. `FALSE-DERIVATION` exits nonzero with the stated derived-output mismatch, so the false derivation is refused. The installed census covers the selected `kernel.printk` value with exact line `v4:printk`; a direct system-value write is refused and reports unchanged readback.

Removal evidence is also consistent. The recorded package rows, generated unit, bytecode, and chosen-setting declaration row are removed, `final-verify` has no failed rows, and both post-reboot verification rows pass. The saved residual-setting observation records the restored effective value `7 4 1 7` as unrecorded with no coverage, which is the required positive residual-state check after the declaration row is removed.

The independent censuses remain deliberately incomplete: each reports `complete: false`, `observed_coverage: failed`, and approximately 65 thousand `FACT_UNKNOWN` rows. In particular, native package-member files retain an unknown receipt state. This prevents treating the finite fixtures as closure of M5.01 or M5.02, and leaves all nine Round 2 owners open.

No object-lane evidence issue requires a source change. Full-suite, carried-suite, regression, combined-example, and controller-cleanup evidence still require separate review after they are saved.
