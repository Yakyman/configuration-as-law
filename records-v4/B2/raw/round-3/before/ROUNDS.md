# Version 4 build rounds

Recorded 2026-11-23 UTC. These are four future build rounds, not work performed in this carry task. Round 0 is the separately recorded unchanged baseline in [SELFTEST.md](SELFTEST.md). The builder implements; a separate review evaluates evidence before any closure is claimed. There is no supplied clock deadline. Exact fixtures and expected results must be fixed before each builder run; the eventual published checks additionally require their inputs committed before the first observation (TEXT.md §9.1 and A.4.1).

The previous night ended with 78 closed and 10 not closed variants, within its bounded version 3 interface. All 88 require version 4 validation; a successful unchanged baseline establishes continuity only. [STAND.md](STAND.md) assigns every variant an owning round. Round 4 additionally checks their coexistence. A failed implementation yields `?` unless a separately reviewed argument derives failure from the definitions alone. Breaking is listed separately and excluded (S8.1-15–16; A.4.1).

## Round 1 — Ordinary shell and declaration-writing mutation boundary

**One scope:** replace the fixed request-only ordinary interface with a command shell whose boundary concerns installed objects and settings left by commands, and connect installation/configuration functionality to declaration application.

**Variants:** C1.1–C1.2, C1.4–C1.5; C2.1–C2.6; C3.1–C3.5; C4.1–C4.5; C5.1–C5.5; C6.1–C6.4; C7.01–C7.17, C7.20, C7.22–C7.24; C8.01–C8.07; C9.1–C9.5; C10.1–C10.2, C10.4. Previously open owners: C1.1, C10.4.

**Requirements:** §9.3 requires ordinary commands and a recorded personal script in the shell. S8.2-4 says: “A command that a person typed himself or herself is that person’s action, not an object.” A setting need not survive reboot to require coverage while in force. Stored executable files, enabled jobs/autostarts, and changed settings remain governed by S8.1-9–12, S8.2-7–14 and P1/P4. S8.1-5 says: “A general-purpose program with a built-in installer counts as an installer in that part of its functionality.” S8.3-7 says: “Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.” Root outside built-in tools is governed separately by S8.1-15–16, not by a requirement to contain deliberate breaking.

**Intended mechanism:** a real recorded shell with ordinary command parsing and pipelines; reuse exact executable/mapping admission and protected configuration stores where compatible. Move admission to saved code, its execution/import, and effective job/configuration writes. Existing broker transactions must write the designated primary declaration and apply it before reporting a supported mutation successful. Route package/language/application managers, account/rights/service/network/access tools and the installer part of a general-purpose program through that path, including genuinely privileged invocations. A refusal-only wrapper or denying the root shell is insufficient evidence of positive tool behavior. No shell input log becomes an automatic declaration merely because a command was typed. The saved-file and custom-interpreter input boundary is an unresolved engineering dependency, not an already implemented solution.

**Self-tests that establish this scope:**

- An ordinary login accepts free commands with quoting, arguments, a pipeline and redirection; it performs document/browser work and runs a personal script whose exact bytes/interpreter are recorded. The old `TYPED` refusal is no longer a positive v4 assertion.
- For each affected variant, observe the concrete object/effect, not just command exit: a saved/extracted/built file cannot become an unrecorded program; a service/timer/autostart cannot become unrecorded enabled state; a setting change either remains unapplied or has a covering declaration line and exact readback. Exercise the same outcome through direct paths, interpreter reads, inherited inputs, helper launches and API entry where that variant specifies them. Harmless material stays writable without a mandatory line.
- Through ordinary and actual superuser execution of each supplied built-in tool, perform a supported change, check the declaration diff, successful application identity and actual required state; then remove it through the tool. Include the documented installer functionality of a general-purpose program (C10.4), while a direct privileged edit is recorded separately as breaking. An unavailable installer is not a positive installation test.
- Run the §9.3 download-and-execute-without-saving case, preserve evidence that the executed payload was not saved, reboot, and inspect that none of its executed contribution remains in force. Saving code or registering a job/setting during that command instead invokes the corresponding object/setting boundary. A rejection before execution is not evidence of the required post-reboot condition.
- For memfd, anonymous/JIT memory and process-memory injection, distinguish runtime-only state following its creator under S8.2-5 from saved executable source/payloads and access settings. Do not demand a separate declaration line for transient memory bytes. Apply the unsaved-execution/reboot condition where applicable; check saved objects and settings under their own rules.
- Preserve original expectations in Round 0; create a separately identified v4 suite for changed requirements. Rerun compatible refusal, positive install/update/remove and declared-script checks through the real shell. Record any conflict that the fixed text does not settle as a GAP, without choosing an author reading.

## Round 2 — Complete recorded-object coverage

**One scope:** make declaration coverage and the independent inventory follow the ordered version 4 object rules.

**Variants:** C1.3, C6.5, C7.18–C7.19, C7.21, C7.25, C8.08, M5.01–M5.02. Previously open owners: C1.3, C6.5, M5.01, M5.02.

**Requirements:** S8.2-1 says: “Everything that is installed and every setting must be recorded.” S8.2-6 fixes first-affirmative ordering. Package content, including packages without programs and untouched defaults, is assessed first (S8.2-7–8); installed objects are in force when present (S8.1-9). S8.2-16 permits own/package/derived coverage; S8.2-17 says: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.” Program records/material need no line after the earlier questions fail (S8.2-2, S8.2-15). Runtime-only objects follow their creating program/setting (S8.2-5). Apply S8.2-20–23 after the ordered questions; do not silently revive a v3 cache or partial-confinement reading.

**Intended mechanism:** extend finite typed rows, package manifests and provenance edges so the inventory can name the exact own/package/derived line and required state. Preserve a census independent of the declaration's enumerator. Add setting readers for chosen values and launch/access effects; trace generated units and code to their real source lines. Remove mandatory standalone runtime-port/mount/process rows from the *criterion*, retaining optional diagnostic rows only as explicit design choices. Do not infer coverage merely from a matching path, an interpreter line or a dependency name.

**Self-tests that establish this scope:** census the concrete supported objects before matching; show coverage of installed packages without executable code, dependency-only packages, untouched package defaults, edited settings, installed/extracted code and generated units. Confirm that program records and material require no extra line only after the earlier questions fail. Remove an owning line and check residual package/derived contributions, including non-executable installed content; distinguish surviving package membership from an inert loose copy. Match each required value and file checksum/permission, report absent facts as `FACT_UNKNOWN`, and never turn unknowns into coverage. Reassess executable bytecode, sandboxed modules and listeners using their actual provenance/capabilities and the v4 rules. M5.02's unrestricted algorithm support is not implemented: exercise the chosen finite format and record any unsupported algorithmic requirement explicitly; neither finite tests nor §8.5 establish universal validation. A remaining unsupported case keeps that variant open.

## Round 3 — Transactional realization and removal

**One scope:** complete the apply/report/recover/remove lifecycle for the state admitted by the first two rounds.

**Variants:** C1.6, C6.6, C9.6, C10.3; M1.01–M1.02, M2.01–M2.02, M3.01–M3.02, M4.01–M4.04. Previously open owners: C10.3, M1.02, M2.02, M3.02.

**Requirements:** S8.1-13–14 define application and the declaration in force; S8.3-1, S8.3-4–8 require actual recorded state after successful application without breaking. §8.4 supplies Removal. A.4.3 requires every-line readback and three success-triggered power cuts for each of add/change/remove. The carried one-hour recovery duration remains an engineering/self-test bound, not a version 4 hypothesis condition; a timer value alone cannot establish restoration.

**Intended mechanism:** extend the existing journal, durable success report, serialized writer, boot admission, contribution graph and revocation to every supported state added in Rounds 1–2. Include real supported device effects in reconciliation/readback. Stop activation edges and living descendants before withdrawing their authority; retain only contributions covered by remaining lines. Bound recovery itself as well as its worker, and report failure honestly when restoration cannot be established. Superuser raw-file disabling of these mechanisms remains breaking, not a required denial path.

**Self-tests that establish this scope:** inject the carried failures/stalls/supervisor death into the extended state transitions; compare exact previous report and actual state, not just the selected link. Verify no partially changed object survives a failed operation. Perform the nine required add/change/remove cuts and inspect complete post-reboot state and admission timing. Exercise running processes and descendants, saved code/copies, installed non-code package content, service/timer/socket/autostart/container activators, accounts, rules and shared ownership on removal. For device recovery, use actual adapter state and readback; prepared profiles alone cannot close M1.02/M2.02. If recovery can still stall or any affected state is unreadable, keep M3.02/the affected variant open. Finite successes support only the supplied scope, not every possible device or effect.

## Round 4 — Integrated ordinary work and reproducibility

**One scope:** validate the completed candidate as one working testbed with one complete declaration on two independent clean installations.

**Variants:** all 88, as the common coexistence/validation gate after their owning rounds. No historical open row is deferred solely to this gate.

**Requirements:** §9.3 ordinary shell and recorded personal script; A.4.3 installation, system update, real Wi-Fi connection, real Bluetooth pairing, browser and document editing; §9.4/A.4.4 same unambiguous declaration and comparison of every stated value, program hashes/permissions, enabled service state/unit hash, account tuple and effective rule text. Hardware exclusions are limited to A.4.4, not a general excuse for different declarations.

**Intended mechanism:** reuse the independent full recipe builds, exact export assembly and actual-state comparison tools, extending their inputs/readers to the new supported rows. Supply an adapter to the VM or a separate permitted computer for the required radio work. Hardware availability is currently unknown; arranging it is a prerequisite to a complete result, not replaced by saved-profile assertions.

**Self-tests that establish this scope:** freeze the complete version 4 builder declaration and ordinary commands before observing them; rebuild two independent images from identical pinned inputs; apply identical declaration bytes, perform all required ordinary work and per-channel positive/negative cases, reboot and compare complete actual observations. Compare both per-line values and independent extra-object inventory. Preserve failures and distinguish source nondeterminism from allowed hardware differences. Require cleanup, a separate review and no unsupported/open variant before describing the testbed as complete. These builder tests do not themselves constitute the published checks; those checks retain their separately fixed inputs and outcome rules.

## Coverage of the ten inherited open variants

| Owning round | Previously not closed |
|---|---|
| 1 | C1.1, C10.4 |
| 2 | C1.3, C6.5, M5.01, M5.02 |
| 3 | C10.3, M1.02, M2.02, M3.02 |
| 4 | Cross-checks all preceding scopes; no unassigned inherited variant |

Implementation restrictions and unavailable hardware are limitations of this testbed. They do not become amendments to the definition or definition-only impossibility arguments.
