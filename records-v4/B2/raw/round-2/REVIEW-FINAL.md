# Independent Round 2 final evidence review

Reviewed 2026-11-23 UTC from saved evidence only. No source, guest, build, probe, or remote state was changed by this review.

## Evidence acceptance

The offline audit was rerun against the completed `final-1` tree and exited zero. It validates all eight sections: frozen inputs, object suite, independent censuses, fixed whole-suite inventories, object exports, native regressions and ancillary evidence, combined replay, and controller lanes/cleanup. The saved final audit has the same result: zero invalid and zero missing sections. Its scope remains finite saved-evidence consistency, rather than a claim that controller success closes a variant.

The frozen-input validation binds the run to the frozen manifest and the copied recipe/controller inputs. The adoption record reports 82 source files unchanged, an immutable image mode, successful inactive service state, and no remaining machine or peer. The controller summary records 40 successful steps, all three lanes exiting zero, no remaining machines, and no remaining peer.

The object lane retains its complete fixed inventory: 52 machine-result rows with 49 passing and three boundary failures, 37 passing pure cases, and two passing post-reboot rows. Its five independent censuses remain incomplete by design, each with `complete: false`, `observed_coverage: failed`, and roughly 65 thousand `FACT_UNKNOWN` observations. Native package-file receipt is therefore not treated as proved.

The carried suites and regression chain validate their fixed inventories and completed results. The combined replay accepts the 578-row declaration on both independently built sides, with complete snapshots and complete post-reboot snapshots on both sides; its summary has zero exit and no owned machines remaining. The audit also validates exact carried and combined evidence inventories rather than relying only on their summaries.

Nineteen genuine false observations are retained: three object boundaries, six saved-shell-input cases, the native root account-tool bypass, five direct saved-input cases, and four supplemental saved-input cases. Thirteen unavailable or untested observations also remain explicit, including the capability record that covers the unavailable browser and foreign-runtime families. None is converted into a passing assertion.

## Variant disposition

All nine Round 2 owners remain **NOT CLOSED**: C1.3, C6.5, C7.18, C7.19, C7.21, C7.25, C8.08, M5.01, and M5.02. The actual alternate-root native installation, extracted/unrecorded executable paths, incomplete provenance census, runtime diagnostic limits, unavailable capabilities, and finite fixture scope prevent a general closure.

C5.4 and C10.4 remain **CLOSED** on their previously accepted bounded mechanisms. The fresh-image tools lane repeats the recorded-native overwrite denial with exact state and report unchanged for C5.4. It also repeats the supplied editor's documented installer path under ordinary and root execution, including bad-artifact refusal and cleanup for C10.4. The retained native account-tool bypass concerns C10.1 and does not broaden or negate the editor-specific closure.

The evidence supports exactly two closed variants of 88 and an overall hypothesis outcome of `?`.

## Final document consistency

Reviewed 2026-11-23 UTC after the final evidence review. `BUILD-2.md` begins with the required `0 variants closed in this round, 2 of 88 closed in all` line. `STAND.md`, `SELFTEST.md`, `HOWTO.md`, and the Round 2 coverage map consistently retain all nine Round 2 owners as NOT CLOSED, retain C5.4 and C10.4 as the two historical bounded closures, distinguish historical evidence from the current rebuilt run, and keep the outcome `?`.

The documents agree with the accepted evidence on 40 successful controller steps and cleanup, the 553-row factory and final readbacks, the 578-row two-side combined replay/reboot, and preservation of 19 false and 13 unavailable/untested observations. The coverage map and build report describe finite fixtures and refusals as bounded observations; they do not turn them into universal closures. The transport note identifies its earlier partial snapshots and its completed final audit separately. No document consistency issue blocks this Round 2 record.
