# Understanding: independent argument

Date: 2026-11-23 UTC. Proposed outcome: **0**, subject to the independent review of this argument. This is a logical pair, not an observation of any existing distribution and not an assertion that an existing account tool has P1, P2 or P4. No probe was run. The earlier F1 opinion is a candidate tested here, not evidence of the conclusion.

## Sentence basis

- S8.1-1: “**Declaration**—a text recording what the computer should be like: what is installed on it and how it is configured.”
- S8.1-2: “The computer is brought into conformity with this text, rather than the text being compiled from the computer.”
- S8.1-9: “**In force.** An installed object is in force if it is on the computer; a program, if it runs or can be started.”
- S8.1-10: “A setting is in force if it has its value.”
- S8.1-11: “A service is in force if it is enabled; an account, if it exists.”
- S8.1-12: “The required state of a recorded object is stated by its line.”
- S8.1-13: “**Application of the declaration**—an action of the system that brings the computer into conformity with the declaration.”
- S8.1-14: “The declaration in force is the declaration of the last application that the system reported as successful [3, Section 3].”
- S8.2-1: “Everything that is installed and every setting must be recorded.”
- S8.2-2: “The rest need not be recorded.”
- S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”
- S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”
- S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”
- S8.2-8: “Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.”
- S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”
- S8.2-10: “Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.”
- S8.2-11: “Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?”
- S8.2-12: “Then it is a **setting**, however it was entered and whatever file stores it.”
- S8.2-13: “Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.”
- S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”
- S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”
- S8.2-17: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”
- S8.3-1: “The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.”
- S8.3-4: “**P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.”
- S8.3-5: “**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.”
- S8.3-6: “**P4. Law.** The system provides no ordinary path for changing what is installed and settings past the declaration.”
- S8.3-7: “Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.”
- S8.3-8: “What is installed and settings can be changed past the declaration only by breaking.”

## First case: everything created during package installation

The order of this analysis is the committed order: installation effects first, then the remaining indirect coverage modes. These are classification branches of one installation case, not empirical observations of unspecified packages.

| Installation effect | Decision and coverage | Relevance to Understanding |
|---|---|---|
| An installed package, including a dependency package | Q1, S8.2-7–8; own package line or the line that obtained it under S8.2-16 | Naming a package records it; this alone says nothing about whether its identity is immutable. The pair below fixes identity to avoid that distraction. |
| A payload object still as received, including non-code resources and default files | Q1, S8.2-7–8, before later questions; package line under S8.2-16 | Fixed payloads in the pair are identical. There is no counterexample from pretending their coverage is missing. |
| Generated executable code or a compiled copy | If not Q1, Q2, S8.2-9–10; the actual declaration line from which the system built it under S8.2-16 | Generated code is not exempt merely because installation created it. A compiler package line alone does not establish the required derivation relation. |
| Generated account and generated default UID | The chosen account is an account setting under S8.2-11–13; its installation-created default is expressly covered by S8.2-17 | This is the distinguishing effect below. The package line states the allocation rule; it does not state the resulting integer. |
| Other generated default settings, such as service or network defaults | A value satisfying Q3 is a setting under S8.2-11–14; the default is covered under S8.2-17 | Coverage is explicit even when a separate value line is absent. Whether a particular value was chosen by a person is a required fact, not something to assume from its filename. |
| Installation logs, caches and other generated non-code state that fail Q1–Q3 | Program records under S8.2-15; need not be recorded under S8.2-2 | They cannot establish an Understanding failure about installed objects or configuration merely because their bytes differ. |
| Material supplied by a person | Only the person-created/brought branch of S8.2-15, after Q1–Q3 fail | A package's own generated output is not material just because it looks like a document. Person-supplied material is outside this package-created branch. |
| Processes, open ports, mount points and service relationships existing only while running | S8.2-5 assigns them to their creating program or setting | They do not supply an independent unrecorded-object counterexample. |

### Ordinary factual anchor

Primary documentation: [sysusers.d, version 258](https://www.freedesktop.org/software/systemd/man/258/sysusers.d.html#ID). The exact excerpts and factual limits are consolidated in `S1/ARGUMENT.md`, Section 2. The numeric pair and allowed scheduling below are stipulated features of the logical construction, not observations of this tool.

### The declaration and its lines

Use the same computer hardware in both states. The following is a specification of an abstract system and its declarations, not an added requirement for all systems. Package names and account names are schematic.

- **L0:** Install one fixed, immutable base package B. Its fixed contents include the installer, account allocator, enforcement mechanism and all supporting programs; all base accounts and settings have exact fixed values. The allocator's permitted ID range is exactly `{61000,61001}`; both IDs are unused initially, and availability is evaluated only when an account is created. On account creation it selects the least unused ID in this pool. It preserves an existing account's allocation. There are no external-source lines.
- **LP:** Install fixed immutable package P with its fixed payload; request account `alpha`, with all fields fixed except its numeric UID. During installation create `alpha` using B's default allocation rule, and retain that UID while the account exists. No service is enabled and no other setting is changed.
- **LQ:** Install fixed immutable package Q with its fixed payload; request account `beta`, with all fields fixed except its numeric UID. During installation create `beta` using B's default allocation rule, and retain that UID while the account exists. No service is enabled and no other setting is changed.

Here `alpha` and `beta` are accounts expressly requested by the person in LP and LQ, not accounts whose existence is silently guessed from a package name. The line states the required account state: named account exists, specified fixed fields hold, UID comes from the designated unused pool according to the creation rule, and the resulting allocation is retained. It does not require one particular integer independently of creation history. LP and LQ are the package lines, not separate generated-UID lines. The package's creation operation supplies the default; S8.2-17 covers it.

The declaration **D = [L0, LP, LQ]** is byte-identical in both states, in the same textual order. It specifies an unordered set of installation requirements: the order of the lines is not an execution sequence, and no line requires P to be installed before Q. No line selects an external list. Both runs start before any successful application, on identical clean hardware with the same initially unused ID range.

### States after the first successful applications

| | State A | State B |
|---|---|---|
| Declaration throughout first application | D | D |
| First package creation after base setup | P creates `alpha` UID 61000 | Q creates `beta` UID 61000 |
| Second package creation | Q creates `beta` UID 61001 | P creates `alpha` UID 61001 |
| Current accounts after first successful application of D | `alpha` 61000; `beta` 61001 | `alpha` 61001; `beta` 61000 |
| All other installed objects and settings | Identical fixed base and payload objects | Identical fixed base and payload objects |

The same allocator operates in both runs; only the allowed package scheduling differs. Both completed applications conform to every line. Neither run contains breaking. These are the two endpoints of the single attempted package-default case; no different earlier successful declarations or archived histories are needed. S8.1-13 requires conformity, not a fixed installation order, and S8.1-14 makes D current in both states. The relevant state remains stable afterwards.

### P1, P2 and P4 in each state

**P1 in A.** B, P and Q exist and their payloads are covered under S8.2-7–8 and S8.2-16. The chosen accounts exist (S8.1-11), and their default UID values 61000 and 61001 are covered by LP and LQ under S8.2-17. Base settings have their fixed values (S8.1-10) and are covered by L0. There are no other installed objects or settings. Therefore every in-force installed object and setting is recorded as S8.3-4 requires.

**P1 in B.** The package/payload/base inventory is identical. Account `beta`'s default UID 61000 is covered by LQ and `alpha`'s default UID 61001 by LP, by the same S8.2-17. The different allocation does not remove coverage. Thus S8.3-4 also holds in B.

**P2 in A.** L0's fixed requirements hold; P and Q and their payloads are installed (S8.1-9); accounts `alpha` and `beta` exist (S8.1-11) with all fixed fields. Each UID was allocated by the stated least-unused rule when its account was created and retained. Every line's required state is fulfilled under S8.1-12 and S8.3-5.

**P2 in B.** The same checks hold, with the opposite creation order. LQ's first allocation and LP's second allocation both fulfill their stated rules. No line requires `alpha` specifically to have 61000, so its 61001 does not violate S8.3-5. This is a positive satisfaction check, not reliance on an unspecified line requirement.

**P4 in A.** The abstract system's first installer carries out only D's package/account requirements; the package lines record the creations and cover their defaults under S8.2-16–17. After the first success, its ordinary tools allow an unchanged reapplication and reject every request to alter installed objects or settings outside a new declaration-mediated application. For this witness, no further altering application occurs, and the system may reject unsupported alterations altogether. Ordinary writes cannot alter effective installed objects or settings. Thus there is no past-declaration path (S8.3-6), tool changes are recorded (S8.3-7), and bypass requires breaking (S8.3-8).

**P4 in B.** The identical enforcement and recorded operations apply, with Q created before P. There is no UID edit after creation, and no ordinary route for an unrecorded alteration. S8.3-6–8 hold for the same reasons as in A. This is an explicit restricted logical system, not a claim of an implemented general-purpose system; the implication from the three properties does not require general-purpose usability as an extra premise.

**Temporal requirement in both.** Before the first completed application there is no prior successful application to which S8.3-1 applies. At first success, every requirement has been satisfied. At every later moment the installed/configuration state is unchanged, including during no-op reapplication; rejected mutations change nothing. Therefore S8.3-1 holds at all required times, without assuming atomic multi-object modifications under an earlier active declaration. P4 quantifies over the available ordinary paths, all of which have been specified above, rather than merely over which paths happen to have been used.

### What Understanding fails to show

Section 8.4 says the declaration alone “shows what is installed on it and how it is configured.” The exact false part is **“how it is configured”**, with **“The declaration alone, without inspecting the computer”** as the information restriction. D cannot tell whether the account `alpha` has UID 61000 or 61001. These are two different effective account configurations under the same D. Appendix A.4.4 explicitly includes the numeric identifier in account comparison; the distinction is not invented file noise. There is no external-source exception to invoke.

## Strongest objections and disposition

1. **S8.1-12 demands the actual UID, so the proposed lines are invalid.** The sentence demands a *required state*. LP and LQ state one: account existence, exact fixed fields, the designated allocation rule and retention. It does not say every property must be a uniquely named constant, that all conforming states must be identical, or that actual generated defaults must be inserted in their own lines. S8.2-17 expressly permits the package line to cover installation-created defaults. Requiring a singleton value adds the very uniqueness premise whose derivation is at issue. On that exact-value demand the pair fails, but no cited sentence states that demand; treating it as automatically mandatory would assume the conclusion. This is the strongest objection to the logical pair.

2. **P4 says to record changes, not merely packages.** LP/LQ record both the requested account creation and its allocation requirement; S8.2-17 defines the default as covered by that package line. No sentence supplies a second, stronger meaning of “record” in S8.3-7 requiring the resulting integer to be appended despite that coverage. The pair would fail if either created account/default had no covering line; it does not. Recording a line before effecting its creation also respects S8.1-2.

3. **The histories differ, or the textual line order requires P first.** Only the internal scheduling of the same first application differs. Both runs have identical D and no prior successful application. D specifies installation requirements, not sequential execution; neither the line requirements nor a numbered sentence imposes an execution order. Understanding has no equal-scheduling qualification. Requiring installation order to be uniquely determined would add a premise absent from the sentence rules.

4. **A generated UID was not chosen by a person, so Q3 fails.** The chosen account is expressly requested in LP/LQ and is a setting under S8.2-11–13; its generated default is covered by S8.2-17. It is unnecessary to claim that a person personally chose 61000 rather than 61001. If instead the analysis splits off each generated UID as an entirely separate object and applies Q3 to that scalar, it can fall through to S8.2-15. That does not make the chosen account cease being an account, and does not make its effective numeric identity cease part of its configuration. The account itself is expressly chosen, and S8.2-13 expressly names accounts. Requiring every field of a chosen account to be individually selected before the account counts as a setting adds a condition not stated in S8.2-11–13. Treating the whole chosen account as program state on that basis is therefore rejected here; it is not a remaining author-choice dependency. An unrequested incidental account would require a different analysis and is not asserted to settle this case.

5. **Knowing the allocation policy is already Understanding.** It shows the requirement, but cannot distinguish the two present account configurations. Section 8.4 says “how it is configured”, not only how it is required to be configured. A policy-only statement would be weaker than these words. No sentence makes that substitution or limits Understanding to the stated requirements; the only express exception concerns external lists, absent here. Therefore this objection is rejected as a narrowing of the consequence, not retained as an equally supported reading on which this outcome depends.

6. **The pair must be an observed ordinary distribution.** The task calls for a reasoning pair, and the known implementation fact has a primary source. No existing distribution is credited with the abstract enforcement. Those are constructed states and transitions checking the logical implication. No machine, runtime probe or undocumented allocator fact is needed.

## The remaining indirect coverage modes, in committed order

| Mode | Once-only examination | Result for this argument |
|---|---|---|
| Object obtained as part of a package | S8.2-7–8 and S8.2-16 cover a fixed unchanged payload; P2 enforces its line requirement. | A fixed payload gives no independent distinguishing pair; mutable package identity is not silently assumed. The package line still need not enumerate payload objects. |
| Compiled copy | Q2 makes executable output a program; the actual source/build line can cover it through S8.2-16. | Coverage is not an assertion that compilation has only one permitted output. A stronger byte-uniqueness proof would need its own premise. No additional pair is claimed here. |
| Generated list | S8.2-16 describes coverage of what is installed; it does not turn every generated non-code list into an installed object. First classify by S8.2-6–15. | A program record list falls outside mandatory recording. A list genuinely belonging to installed state is covered by its actual derivation line. No blanket exemption or blanket installed classification is available. |
| Dependency package | Q1 makes it an installed object, and S8.2-16 allows the originating package line to cover it. | Coverage records the dependency without its own line; uniqueness of dependency selection is not stated. The account pair fixes package identities, so mutable resolution is unnecessary. |
| Default value obtained with a package | Q1 decides an unchanged payload default as an installed object; S8.2-17 also describes package coverage for a default setting. | With fixed package content the value is fixed, so no independent failure arises here. Do not skip Q1 to manufacture Q3 disagreement. |

## Findings, with no proposed repair

**Gaps in the idea.** Coverage plus satisfaction of a stated allocation requirement is weaker than identification of the realized configuration from current declaration text. A derivation of exact Understanding needs the missing premise that all states satisfying the same declaration agree in all installed/configuration information that Understanding promises to show. Neither S8.1-12, P1, P2 nor P4 states that premise. The account pair realizes the difference without changing payload versions, hardware or external lists.

**Gaps in the wording.** None is needed to sustain this Understanding pair. The proposed field-by-field personal-choice condition and policy-only consequence are rejected above because they add or substitute requirements. This finding is limited to expressly chosen named accounts; it does not settle the classification of every incidental account an installer may create.

**Questions for the author.** No unresolved two-reading dependency remains for this Understanding argument. Asking whether a weaker, policy-only consequence was intended would concern a change of scope rather than a choice compelled by two equally supported readings of the present sentence. No wording change is proposed. The separate Reproducibility phrase “provided the description is unambiguous” has its own interpretive issue and is not decided here.

No missing ordinary-system fact is used as a textual gap. The exact numeric result of the ordinary documented tool for any particular distribution remains **FACT_UNKNOWN** and is not asserted; only the abstract construction has the stipulated numbers.
