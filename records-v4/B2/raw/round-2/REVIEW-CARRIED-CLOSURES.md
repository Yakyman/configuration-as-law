# Carried-closure regression review

Reviewed 2026-11-23 UTC from the saved Round 2 tools lane, its frozen `v4-tools-selftest.py`, `tools-verify.log`, and the accepted Round 1 review. This is a bounded rerun review only; complete-controller, peer, regression-chain, and combined evidence remain pending.

The fresh Round 2 tools lane has 85 passing required tool assertions and no required assertion failure. Its 553-row readback log has exactly four tab-separated fields per row and every row is `OK`. The one native root account-tool bypass is preserved as a boundary observation for C10.1, with cleanup; it is not counted as a passing required assertion.

C5.4 is preserved subject to the pending complete-suite checks. `recorded-native-overwrite` again attempts an ordinary copy over the recorded native worker. It fails with a permission error, while the saved exact file state, covering declaration row, and successful application identity remain unchanged. This repeats the accepted bounded mechanism: declared native bytes are protected and remain usable through declared application. It does not enlarge the earlier closure beyond recorded native files.

C10.4 is preserved subject to the pending complete-suite checks. The frozen tool self-test again exercises the supplied general editor under both ordinary and root identities: arbitrary document write, append, and read; documented package installation; installed-program execution; removal; and bad-artifact refusal. The successful package operations use the editor's documented package subcommands, and the bad-artifact path refuses with no declaration/report change. Direct root editing remains separately classified as breaking. The native account-tool bypass concerns C10.1 and does not contradict this editor-specific result.

No new Round 2 closure follows from these observations. Final preservation of the two historical closures still depends on the complete controller, carried and regression-chain completion, peer comparison, cleanup, and combined replay evidence.
