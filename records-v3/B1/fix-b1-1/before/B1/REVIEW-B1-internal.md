# Independent review

Review time: 2026-11-22T04:37:49Z. Role: review.

## Scope and status

Reviewed (not published: orchestration and working notes), Sections 2, 3, 4.1, and 4.3 of `../TEXT.md`, `../SENTENCES.md`, the three B1 research reports, and their raw source ledgers. Review ran no experiment. This paragraph records the source-research pass performed before `CHANNELS.md`, `DESIGN-INPUT.md`, and the later P01 bundle existed.

## Objection requiring correction

The C10.4 card does not establish `TEXT-OPEN`. S3-7 expressly says that an editor is not a built-in tool and that changing a required object with it through superuser privileges is breaking. That sentence directly classifies the root-editor case even when the editor documents a package-install command. S3-6 states the general purpose-based indicator, but S3-7 then supplies the explicit editor classification; S3-8 applies only if the indicator still does not decide. The current argument therefore cannot support a definition counterexample. Classify the stated root-editor operation as excluded breaking, or supply a distinct object for which S3-7 does not decide the program class.

## Findings that survive review

1. The executable-cache card is a valid conditional `TEXT-OPEN` case. An executable cache can meet S2.2-5 exactly when removing it changes only speed, while the same bytes can meet S2.2-10 when executed with the program's own rights. The text gives no priority between “need not be recorded” and “must be recorded.” The premise must remain limited to a genuinely regenerable performance-only cache.
2. The browser-extension card is valid only under its stated dual predicate. S2.2-7 expressly names browser extensions, while S2.2-10 and S2.2-13 cover code executed with the program's own rights. Evidence for an ordinary permission-limited extension does not establish the same-rights predicate. A synthesis must not generalize this card to all browser extensions.
3. No research report supplies a universal `NOT-CLOSABLE` proof. The reports correctly distinguish a missing stock primitive or an unverified composition from an impossibility that follows from the definitions for every possible system.
4. The partial-sandbox boundary remains a candidate textual hole, not a settled result. S2.2-11 does not define when limited host APIs cease to be confinement “to its own interface.” S2.5 does not assign this classification boundary to system design. A final claim needs one concrete object and documented rights showing that S2.2-10 does not decide it and that the S2.2-11 boundary controls the answer.

## Quantifier controls for synthesis

Q1 must be conditional: when accessible material can be executed as own-rights code and is not covered by a declaration line, P1 fails and an unmediated introduction path fails P4. This does not make data-to-code conversion universally impossible; a system may deny conversion or mediate declaration admission first.

Q2 cannot support a universal failure. An algorithmic declaration may be pure, may operate only on recorded inputs, or may include its expansion in the designated declaration files. An algorithm that consults mutable external state can fail the declaration-alone or same-declaration consequences under a concrete-object reading, but that rejects that design; it does not contradict every system allowed by S2.5-3. Treatment of data and program state is also assigned design latitude by S2.5-1, so the synthesis must separate a bad design choice from a definition-level hole.

## Research-evidence limits

The primary sources establish individual mechanisms and bypasses, not a composed M1–M5 implementation. `CLOSABLE` is supportable only as an existence claim for the bounded variant with all stated restrictions. It must not be rewritten as evidence that a stock distribution, one mandatory-access policy, one immutable tree, or one wrapper closes a complete channel. In particular, live account, network, firewall, device, report/commit, and loaded-code state remain integration obligations.

## Final synthesis review

Final pass time: 2026-11-22T04:47:14Z.

The table arithmetic is correct: 85 counted rows comprise 74 `CLOSABLE`, 3 `TEXT-OPEN`, and 8 `UNKNOWN`; there are no `CLOSABLE-ONLY-BY-REMOVAL` or `NOT-CLOSABLE` rows. The explicit root-editor operation is now correctly excluded from the count as breaking under S3-7. The direct quotations from the fixed text match `../SENTENCES.md`.

The three remaining `TEXT-OPEN` cards are sufficiently bounded for referral rather than acceptance as universal failures. C7.18 requires a cache that actually changes only speed. C8.07 uses a privileged extension implementation documented as full-chrome-privilege code packaged in an extension and does not generalize to ordinary extensions. C7.21 uses a WASI module with a selected preopened host directory and known lesser authority than its runtime; the unresolved issue is the textual extent of “own interface,” not unknown object behavior.

The synthesis preserves the required quantifiers. Q1 is a conditional failure when uncovered own-rights code remains executable; it does not claim every system permits that premise. Q2 rejects only the external-state-dependent arrangement and does not turn algorithmic declarations into a general hole. `DESIGN-INPUT.md` retains `?` for whole-system existence and carries all eight engineering unknowns and all three text questions forward. It does not treat individual primitives as proof of a composed transaction or completed Check 2.

The requested source-record and terminology corrections were applied: E17 records the Linux 7.3 documentation, E18 records the 7.3.4 `set-exec` source, and C7.07 uses mechanism shorthand `D`.

## P01 review and final finding

Final evidence pass: 2026-11-22 UTC.

P01 asks one bounded runtime question that the preceding source inspection did not answer: whether the selected downstream Python binary cooperates with the locked interactive-denial securebit for argument code. The question, expected result, exact guest target, one-invocation rule, and cleanup requirement were recorded before the invocation. The unprivileged-child refinement was also timestamped before invocation and did not change the question.

The raw result supports the stated conclusion. The wrapper set and reread mask `0xf00`; after dropping supplementary groups and changing to uid/gid 65534, a fresh `python3 -I -S -c` child reread `0xf00`, printed `PYTHON_CODE_RAN`, and exited 0. Version records identify Debian 13.8, kernel `7.3.4+deb13-amd64` from package `7.3.4-1~bpo13+1`, Python 3.13.5 from `python3.13` package `3.13.5-2+deb13u5`, and systemd `257.13-1~deb13u1`. Setup dependency correction and the setup reboot occurred before the sole test invocation and are not test retries.

The inference is correctly limited to that binary and the `-c` route. It does not establish file/import/eval behavior, general interpreter adoption, or universal impossibility. C7.03 therefore remains `CLOSABLE` through a cooperating implementation, while the selected stock Python cannot serve as that implementation on this route merely by setting the securebits. The probe does not alter the 85-row counts or the whole-system outcome `?`.

Cleanup evidence records the VM inactive, slot 2 unlockable, and the disposable task directory removed. Final deliverables no longer assert that B1 ran zero probes; statements that no probe was run remain only in separately scoped research reports for channels that P01 did not test. No additional material objection remains. This is review acceptance of the bounded research synthesis and P01 record, not acceptance of an implemented whole system or Check 2.
