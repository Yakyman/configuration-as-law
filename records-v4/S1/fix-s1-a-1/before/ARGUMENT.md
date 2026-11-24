STEP 1: Understanding 0; Reproducibility ?; Removal 1

# Consequences of the fixed properties

Recorded 2026-11-23 UTC. Argument-stage outcomes for `SUP1/step-1.md`; the separate RV-S1 review has not been performed here. Inputs: (not published: orchestration or scratch), `TEXT.md` Sections 8–9 and Appendix A, `SENTENCES.md`, `SUP1/step-1.md`, `OP/OPINION.md` F1/F10/F11, and the two named D1 comparison files. Input fingerprints are in `S1/raw/input-hashes.tsv`. F1, F10 and F11 were claims to test, not premises. No machine was started and no behavioural probe was run.

## 1. Sentence rules, without additional conditions

The following is the rule basis. The quoted sentences, rather than the inventory's kind names or classification decisions, govern the argument. The order in S8.2-6 is preserved. Sentence quotations are copied from `SENTENCES.md`; Section 8.4 and the other quoted passages are from `TEXT.md`.

### Declaration, installation units, tools and breaking

- S8.1-1: «**Declaration**—a text recording what the computer should be like: what is installed on it and how it is configured.»
- S8.1-2: «The computer is brought into conformity with this text, rather than the text being compiled from the computer.»
- S8.1-3: «The declaration consists of files that a person has designated as the primary description of the computer; there may be many files, and together they form one description.»
- S8.1-4: «**Installer**—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.»
- S8.1-5: «A general-purpose program with a built-in installer counts as an installer in that part of its functionality.»
- S8.1-6: «**Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.»
- S8.1-7: «**Built-in tool**—a program of the system whose purpose, according to its documentation, includes changing what is installed and settings: an installer, account and rights management, the service manager, network and access rule configuration.»
- S8.1-8: «General-purpose programs—an editor, file copying, link creation, the command shell—do not count as built-in tools, except in the part of their functionality that contains a built-in installer.»
- S8.1-13: «**Application of the declaration**—an action of the system that brings the computer into conformity with the declaration.»
- S8.1-14: «The declaration in force is the declaration of the last application that the system reported as successful [3, Section 3].»
- S8.1-15: «**Breaking**—a change to what is installed or settings, made past the declaration through the power of superuser privileges, outside the built-in tools: by writing directly to files, deleting, or disabling system mechanisms.»
- S8.1-16: «Breaking is a violation on the person’s part rather than a property of the system, and it refutes no property.»

### When recorded objects are in force and what a line requires

- S8.1-9: «**In force.** An installed object is in force if it is on the computer; a program, if it runs or can be started.»
- S8.1-10: «A setting is in force if it has its value.»
- S8.1-11: «A service is in force if it is enabled; an account, if it exists.»
- S8.1-12: «The required state of a recorded object is stated by its line.»

### Objects, mandatory recording and the ordered questions

- S8.2-1: «Everything that is installed and every setting must be recorded.»
- S8.2-2: «The rest need not be recorded.»
- S8.2-3: «The rule applies to objects that are on the computer.»
- S8.2-4: «A command that a person typed himself or herself is that person’s action, not an object.»
- S8.2-5: «What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.»
- S8.2-6: «What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.»
- S8.2-7: «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?»
- S8.2-8: «Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.»
- S8.2-9: «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»
- S8.2-10: «Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.»
- S8.2-11: «Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?»
- S8.2-12: «Then it is a **setting**, however it was entered and whatever file stores it.»
- S8.2-13: «Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.»
- S8.2-14: «A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.»
- S8.2-15: «Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.»

### Which line records the object

- S8.2-16: «What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.»
- S8.2-17: «A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.»
- S8.2-18: «A line may take a list from outside the declaration, for example accounts from an organisation’s server; in that case, what counts as recorded is the source named in the line.»
- S8.2-19: «What need not be recorded may also be recorded in the declaration.»

### Clarifications, without changing question order

- S8.2-20: «A file containing code that cannot be executed on this computer is not a program.»
- S8.2-21: «Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.»
- S8.2-22: «A program that runs as its own process on the computer, including in a container, is a program.»
- S8.2-23: «A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.»

### Property scope and P1, P2, P4

- S8.3-1: «The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.»
- S8.3-4: «**P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.»
- S8.3-5: «**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.»
- S8.3-6: «**P4. Law.** The system provides no ordinary path for changing what is installed and settings past the declaration.»
- S8.3-7: «Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.»
- S8.3-8: «What is installed and settings can be changed past the declaration only by breaking.»


Consequences under examination, Section 8.4:

- Understanding, quote: «The declaration alone, without inspecting the computer, shows what is installed on it and how it is configured. For a line that takes a list from outside the declaration, the declaration shows which source determines the list.»
- Reproducibility, quote: «The same declaration on another computer yields exactly the result described in it, provided the description is unambiguous. For a line that takes a list from outside the declaration, reproducibility is not claimed. Differences explained by hardware are excluded.»
- Removal, quote: «After application of a declaration from which a line has been removed, nothing the line contributed is in force unless it is recorded in the remaining lines.»

The explicit boundary in Section 8.5 is also retained: quote: «How to store, transfer and remove program records and material.» It is an exclusion, not a missing deletion requirement.

For the proofs, **required** refers to the installed/program and setting objects under examination; **covered** means recorded by a line through S8.2-16/17, or the named-source provision S8.2-18. These are abbreviations, not new rules. The non-executable and restricted-code clarifications S8.2-20/21 remain in the rule basis; no object of the pair relies on the restricted-code clarification. P1 requires coverage of required objects when in force; P2 requires fulfilment of each recorded requirement; P4 restricts ordinary changes. None of these abbreviations asserts that a covering line specifies a unique realized value. The only rule about what its line requires is S8.1-12, applied through S8.3-5.

## 2. First case: what installation itself creates

This first pass follows every classification branch an installation product can reach. It is not a claim that one real package creates every listed kind. Creation during installation alone does not classify an object and does not give every output blanket package coverage.

| Product or effect | Ordered decision and recording rule | Consequence for this step |
|---|---|---|
| Installed package, including an automatically installed dependency | S8.2-7/8, then S8.2-16 | Own line, or a genuine package/derivation line; automatic installation does not exempt it. |
| Unchanged received payload: code, fonts, icons, translations, tables, firmware, default files, dependency-only packages | S8.2-7/8 decides before questions 2–4; S8.2-16 | Package coverage; not reclassified as a record just because it contains no executable code. |
| Generated executable, compiled copy or executable generated list | If question 1 does not decide, S8.2-9/10 and S8.2-23; S8.2-16 | Needs an actual covering line; the fact that a recorded compiler exists is not by itself the fact that this output was built from its line. |
| Installation-created default account or other default setting | For a chosen account, S8.2-11/12/13; other settings also use S8.2-14 where applicable; S8.2-17 explicitly covers installation defaults | A package line can cover the generated default without a separate line containing its realized value. This is the distinguishing branch below. |
| Non-default setting chosen during installation | S8.2-11–14, then first clause of S8.2-17 | Requires its own line unless another expressly applicable provision, such as S8.2-18, applies. Mere generation is not an extra setting-coverage rule. |
| Generated non-code list, log, cache, history or working state that fails questions 1–3 | S8.2-15, then S8.2-2/19 | Program record, not automatically installed merely because S8.2-16 mentions a generated list. It can be recorded voluntarily. |
| Person-created or brought material, if questions 1–3 fail | S8.2-15, then S8.2-2/19 | Material. This branch concerns supplied material; the package's own output does not acquire person-created provenance merely by looking like a document. |
| Process, port, mount point or relationship existing only while running | S8.2-5 | Follow the creating program or setting; no separate object line is required by this sentence. |

These branches distinguish received defaults from created defaults, executable caches from non-code caches, and persistent settings from runtime manifestations. A missing fact about a particular product would be FACT_UNKNOWN, not a textual gap ((not published: orchestration or scratch)).

### Documented ordinary mechanism

The primary [sysusers.d manual, version 258](https://www.freedesktop.org/software/systemd/man/258/sysusers.d.html#ID), in Description, Type and ID, documents installation-time account/group creation, creation when absent, and automatic numeric allocation. Its exact short passages are: “at package installation or boot time”; “should they not exist yet”; “Specify "-" for automatic UID/GID allocation for the user or group”. These are 22 quoted words from that page. The documentation supports this mechanism; it does not specify the numerical selection algorithm constructed below, and it does not establish P1/P2/P4 for an existing distribution.

### One declaration, two states

The following three lines specify a logical system; they are not proposed additions to the hypothesis. The package identities denote fixed artifacts, not mutable repository names. This avoids relying on an undocumented resolver or changed package contents.

| Line | Complete requirement relevant to the pair |
|---|---|
| L0 | Install fixed base package B. Its fixed payload includes the installer, allocator, ordinary-access enforcement and supporting programs. Its base accounts and settings have fixed values, identical in both states. The allocator's permitted UID range is `{61000,61001}`; both are unused initially. When creating an account, choose the least unused UID in that range and thereafter retain it. The range is fixed; availability is evaluated at creation, not required to remain unused afterwards. |
| LP | Install fixed package P with its fixed payload. Request the system account `alpha`, with fixed name, group membership, shell, account directory and other fields; only its UID is allocated by L0's creation rule. Create it during P's installation and retain the allocation. No service is enabled and no other setting is changed. |
| LQ | Install fixed package Q with its fixed payload. Request the system account `beta`, with the analogous fixed fields and allocation requirement. Create it during Q's installation and retain the allocation. No service is enabled and no other setting is changed. |

All fixed base objects/settings are a common fixed block under L0; it covers neither `alpha` nor `beta` merely because it contains the allocator. Those accounts/defaults are covered by LP and LQ. No unspecified background settings, extra installed programs, external sources or hardware differences are used. Fixed account groups already belong to the common base. Thus only the two numeric UIDs distinguish the installed/configuration states.

The account names and fixed fields belong to the respective immutable package's installation defaults; requesting them accepts those defaults, without overriding them. The person explicitly chooses the two accounts through the package lines. Each line states a required account state: existence, fixed fields, valid distinct allocation by the stated rule, and retention. It does not require `alpha` to have a particular integer regardless of creation order. LP/LQ are package lines containing these requirements, not separate lines of the generated UIDs.

**D is byte-identical in both states: `[L0, LP, LQ]`.** Before either application, the person designates the file containing D as the primary description (S8.1-3). Its semantics is an unordered set of requirements, not an instruction to execute package installations in textual order. This is an explicit feature of this declaration, not a rule imposed on other declarations. The same installer permits either order after base setup. Both computers start their first application with identical fixed base conditions and the same two free UIDs; neither has an earlier completed application.

| | State A | State B |
|---|---|---|
| Declaration used throughout the first application | D | D |
| Allowed installation schedule after base setup | P, then Q | Q, then P |
| Created `alpha` UID | 61000 | 61001 |
| Created `beta` UID | 61001 | 61000 |
| Other installed objects and settings | The fixed common block and fixed P/Q payloads | Identical |
| Observation moment | After first successful completed application of D | After first successful completed application of D |
| Subsequent relevant state | Stable | Stable |

The exact numbers and least-unused rule are stipulated mathematical features, not claimed results of the documented tool. No fact about that tool's scheduling or a distribution's actual allocations is needed. Its precise numbers in any unobserved installation remain FACT_UNKNOWN.

### Checking every property in each state

| Obligation | State A | State B |
|---|---|---|
| Scope and no breaking | First application completed in conformity with D; D is the last successful declaration (S8.1-13/14, S8.3-1). No change bypassed the declaration through superuser direct writing (S8.1-15). | Same, with the other allowed installation order. |
| P1 | B/P/Q and unchanged payloads are installed and covered by their package lines (S8.2-7/8/16). Chosen accounts are settings (S8.2-11/12/13); their installation-created UID defaults are covered by LP/LQ (S8.2-17). All fixed base settings are recorded. Thus S8.3-4 holds. | Exactly the same coverage: LP covers `alpha` with 61001, LQ covers `beta` with 61000. Changing which default was generated does not remove S8.2-17 coverage; S8.3-4 holds. |
| P2 | Packages/payloads are present (S8.1-9), accounts exist (S8.1-11), fixed fields hold, and each UID was the least unused at its creation and is retained. Every stated requirement is fulfilled (S8.1-12, S8.3-5). | Q takes 61000 first; P then takes 61001. Both allocation requirements and all fixed fields hold. Neither LP nor LQ states a contrary fixed UID. S8.1-12 and S8.3-5 hold. |
| P4 | The first installer operates only from D's recorded requirements. Thereafter ordinary tools permit read-only use and unchanged reapplication; unsupported alterations are rejected. No ordinary write can change installed objects/settings, including through privileged built-in tools. Therefore no past-declaration ordinary path exists (S8.3-6); actual tool creations are recorded through LP/LQ and S8.2-17 (S8.3-7); bypass would require breaking (S8.3-8). | Identical available paths and enforcement. The alternate initial schedule is a permitted way to fulfil D, not a later UID edit. The same S8.3-6/7/8 checks hold. |

This restricted transition system specifies available ordinary paths, rather than inferring P4 merely from an absence of observed bypasses. It is not asserted to be an implemented general-purpose distribution. Useful ordinary work is a separate testbed question in Appendix A.4.3, not an extra premise of this step's implication. A system can reject unsupported alterations without violating these three properties.

The temporal quantifier is respected: no previous successful application exists during initialization; at first success all requirements hold; thereafter the installed/configuration state remains unchanged, even during unchanged reapplication. There is no intervening state under an old successful declaration to hide. S8.3-1 therefore holds at every relevant moment, without assuming atomic multi-object updates. The declaration is selected before creating the state, consistent with S8.1-2; it is not a retrospective inventory.

## 3. Understanding: 0

1. A and B satisfy the same D and P1/P2/P4 as just checked by S8.2-16/17 and S8.3-4–8.
2. They have different present numeric identities for the same chosen accounts. Accounts are expressly among settings (S8.2-13) and exist in both states (S8.1-11). Appendix A.4.4 specifically includes an account's numeric identifier in its comparison; this is configuration, not incidental log content.
3. D and all its stated requirements are identical. A function of D alone therefore cannot identify which of those two account configurations is present. It can identify the allocation requirement, not the realized UID.
4. The false words of Section 8.4 are **“The declaration alone, without inspecting the computer”** together with **“how it is configured”**: D alone does not show whether `alpha` is configured with UID 61000 or 61001. The external-list qualification does not apply.

### Strongest objection to the pair, and other attempted refutations

| Objection | Disposition by the fixed text |
|---|---|
| **S8.1-12 already demands one exact UID, invalidating LP/LQ.** | It demands the required state be stated. The lines explicitly state existence, fixed fields, allocation and retention. No sentence says every permitted requirement has exactly one realization or that an installation-created default must be replaced by a value-bearing own line; S8.2-17 expressly permits package coverage. The singleton demand is the missing premise, not a refutation from a sentence. This is the strongest attack on the pair; it fails on the stated rules. |
| **S8.3-7 requires generated numeric values to be appended to D.** | It requires recording changes. LP/LQ record the account creation and its requirement; S8.2-17 says the generated default is covered by that package line. No second definition of recording in S8.3-7 overrides that provision. The pair does not infer permission for arbitrary later edits just because a covering package remains. |
| **The UID was not personally chosen, so the account is a program record.** | The whole named account is expressly requested by the person and is a system account, meeting S8.2-11/13. Its default field is expressly covered by S8.2-17. Requiring personal selection of every scalar field adds a condition to those sentences. Splitting off the generated integer does not remove the chosen account or its configuration. The pair does not rely on classifying an unrequested incidental account. |
| **Different histories or order violate the same-declaration premise.** | D is identical from the start of the first application; only an allowed internal schedule differs. No sentence fixes execution order from line order, and the specified D does not do so. S8.1-13 requires conformity, which both endpoints have. |
| **The declaration shows the allocation policy, which is sufficient Understanding.** | It shows what is required, but not which present account configuration obtains. Section 8.4 says how the computer *is* configured and supplies only the named-source qualification. Replacing that claim with knowledge only of a permitted policy is a weaker statement, not a derivation of the published actual-configuration claim. |
| **A real distribution must first be shown to have all three properties.** | This step asks for an argument pair, not a new testbed. The pair explicitly supplies its state requirements and ordinary transition restrictions. Documentation is used only for the ordinary installation-default mechanism; no existing implementation is credited with the constructed properties. |

**Missing-premise finding:** exact Understanding needs all admissible states under the same declaration to agree on the installed/configuration information that it promises to show. Coverage, satisfaction of the specified requirement, and prevention of bypass do not supply that uniqueness. The pair demonstrates the missing implication; this is not a proposal to amend the text.

## 4. Reproducibility: ?

The account pair is reused as a logical comparison, not rerun or presented as a second case. Its declaration, states, P1/P2/P4 checks, and strongest S8.1-12/P4 objections are exactly those above.

The derivation that survives is narrower than equality of all realized fields:

1. Consider two completed applications of the same declaration with no breaking: S8.3-1 gives the scope, and S8.1-14 identifies their operative declaration.
2. Each line states its required state, S8.1-12.
3. P2 makes every recorded object in force as that line requires in each computer, S8.3-5. Therefore every stated requirement is fulfilled in both.
4. P1 excludes required in-force objects without valid coverage, S8.3-4 with S8.2-16/17/18. This supplies coverage, not additional values for a recorded requirement.
5. P4 restricts changes past the declaration, S8.3-6–8. It does not compare distinct applications or select a unique permitted realization.
6. **Conditional step:** if the described requirements uniquely determine the relevant result, step 3 entails that result on both computers. Uniqueness is not independently stated by a sentence of Sections 8.1–8.3. It could be the meaning of Section 8.4's explicit condition “provided the description is unambiguous”.

| Reading of Section 8.4 | Application to A/B | Result |
|---|---|---|
| “Unambiguous” requires one possible relevant realized result | D allows either allocation, so fails that antecedent. For declarations meeting it, P2 yields their determined result. | Pair is not a counterexample; conditional derivation holds. |
| “Unambiguous” means requirements have one clear meaning; “result described” means those stated requirements | D's allocator rule has a clear meaning; both states fulfil it. | P2 proves this satisfaction claim; different permitted UIDs do not falsify it. |
| “Unambiguous” means clear requirements, but “exactly the result described” requires identical realized covered fields | D qualifies, yet account identifiers differ without hardware or external lists. | The pair falsifies “yields exactly the result described in it” on this reading. |

**Strongest objection to using the pair as a reproducibility refutation:** the published condition can exclude D for admitting more than one result, or the published result can be only the stated allocation requirement. This objection holds under the first two readings. Unlike Understanding, Reproducibility expressly includes the “unambiguous” condition and refers to the result *described*. Choosing among these readings belongs to the author; the committed outcome rule therefore gives **?**, not an unconditional 0 or 1.

Appendix A.4.4 compares, quote: «every value the line states and, in addition, for a program, the checksums and permissions of its installed files; for a service, whether it is enabled and the checksum of its unit file; for an account, its name, numeric identifier, groups, shell, and home directory; for a rule, its effective text as reported by the system.» Those additional fields follow from P2 only when the description determines them. Their inclusion in the fixed check does not itself prove that S8.2-16/17 determines them. The oracle is retained, not rewritten.

The pair has identical hardware and no external list. Thus neither qualification explains its different UIDs. The broader hardware wording of Section 8.4 and the narrower driver/firmware/device-file rule in Appendix A.4.4 are a textual distinction, not an additional case attempted here.

**Missing-premise findings:** equality of covered fields needs unique realization of those fields; equal interpretation of a declaration on both computers is also needed for comparing its requirements. A promise that application succeeds on every other computer would additionally require existence/completion, whereas S8.3-1 only scopes the properties after completion. No counterexample based on failed application is attempted. The outcome depends on the first two wording choices, recorded in `S1/QUESTIONS.md`.

## 5. Removal: 1

Let D previously be in force, L be removed, and R be the remaining declaration. Consider an arbitrary object x contributed by L. The consequence is about being **in force**, using S8.1-9–11; it is not a claim that all historical bytes, program records or material must be erased (Section 8.5).

1. Choose a moment after a completed application of R without breaking. This is within S8.3-1. R is the operative declaration by S8.1-14; the removed line is not a remaining recording line.
2. For an object still installed/program or a setting, apply S8.2-6's ordered questions and S8.2-1. A running or startable program belongs to what is installed by S8.2-9/10; its runtime manifestations follow it by S8.2-5.
3. Evaluate coverage in **R** through S8.2-16/17, or S8.2-18 when applicable. Suppose no remaining line records x. This is precisely the exception condition in Section 8.4, not an assumption that every object has only one owner.
4. Suppose x nevertheless remains in force under S8.1-9, S8.1-10 or S8.1-11. P1, S8.3-4, then requires x to be recorded in R, contradicting step 3. Hence x is not in force.
5. Since x is arbitrary, no uncovered contribution in that domain remains in force. Where a remaining line records x, Section 8.4 explicitly permits it; P2, S8.3-5, may require its retained state.
6. P4, S8.3-6–8, forbids an ordinary path restoring an uncovered installed object or setting. P1 already applies at every relevant moment, not only the first observation. No deletion algorithm, unique provenance, deterministic default or unique result is needed for this implication.

### Attempts to break the derivation

| Attack | Why it fails, or the boundary it establishes |
|---|---|
| Retain the installation-created account but disable login | S8.1-11 makes an account in force when it exists. Without any remaining coverage under S8.2-17/18, P1 fails. This cannot be a state satisfying all premises. |
| Leave a program running after deleting its pathname, or retain a startable compiled copy | Running/startable meets S8.1-9; executable code meets S8.2-9/10; a runtime child follows its program under S8.2-5. Uncovered survival contradicts P1. S8.2-22 does not exempt a separate container process. |
| Keep a disabled service's file | The service itself is not thereby enabled (S8.1-11). Its file must be classified separately under S8.2-6–15; any still in-force installed object or setting needs coverage. Removal does not equate disabling every service with deleting every backing file. |
| A shared dependency or derived object remains after deleting one owner | Actual remaining coverage under S8.2-16 is the explicit exception. If the last covering line is gone, an installed in-force dependency contradicts P1. Keeping the installer alone does not establish that its line built or obtained this dependency. |
| **A non-code package remnant changes kind when its package is removed** | Strongest boundary attack. S8.2-7's “such a package” can raise a present-package versus historical-provenance question. Under either reading, if the residue is still installed or a setting, P1 gives the same conclusion. If it instead reaches record/material in S8.2-15, Section 8.5 excludes its removal and S8.1-9–11 supplies no separate force criterion for that kind. If provenance is unknown, its classification is not guessed. No admissible in-force uncovered installed/setting residue results. |
| A voluntarily recorded document remains after its line is removed | S8.2-19 permits its recording and P2 enforces a line while present. It does not say Section 8.5 ceases to exclude removal of material/records. Nor does P2 preserve the requirement of a removed line. Retained material is not manufactured into a refutation. |
| The removed external-source line's server still exists | S8.2-18 records its source through a line; a source outside R is not a remaining line. A local account with no other coverage is still in force if it exists (S8.1-11), so P1 forbids it. No freshness assumption is needed for that implication. |

No missing premise is needed for this no-uncovered-force derivation. A stronger erasure claim would need a preservation-of-kind or deletion premise absent from the text; that stronger claim is outside the stated record/material boundary. Questions about classifying a particular non-code remnant are recorded separately, without changing P1's implication or pretending its provenance is known.

## 6. Remaining indirect coverage modes, after the installation case

These are the remaining required examinations, once each. No extra observed state pair or undocumented ordinary-system behaviour is asserted.

| Mode | Sentences and what the line records | Understanding / Reproducibility | Removal |
|---|---|---|---|
| Object obtained as part of a package | S8.2-7/8 and package clause of S8.2-16; unchanged received content, including non-code kinds | An exactly fixed artifact fixes its payload; package coverage alone does not state that every package name identifies immutable bytes. No different fixed payload is claimed in A/B. P2 gives what the actual line requires. | Current installed in-force content without remaining coverage contradicts P1; reclassification boundary as above. |
| Compiled copy | Executable output is a program by S8.2-9/10; actual system derivation from a line is covered by S8.2-16 | Derivation coverage is not a uniqueness-of-bytes statement. A line that fixes the result gets that result through P2; merely naming the compiler is not proof of the necessary derivation facts. | Running/startable uncovered output fails P1. |
| Generated list | S8.2-16 permits derivation coverage for what is installed; first classify under S8.2-6–15 | Generation alone supplies neither installed status nor fixed membership/order. A setting list needs S8.2-17's setting rule. An external-source list uses the separate S8.2-18 provision and Section 8.4 exceptions. | P1 applies if installed/setting and in force. A record/material list does not acquire an erasure obligation. |
| Dependency package | Package under S8.2-7/8; originating recorded package line under S8.2-16 | Covered without its own line. Coverage alone does not fix the dependency artifact; a requirement that does fix it is enforced by P2. No actual resolver behaviour is assumed. | May remain under a genuine remaining covering line; otherwise an installed dependency violates P1. |
| Default value obtained with a package | Unchanged received default first meets S8.2-7/8 and S8.2-16; S8.2-17 also expressly provides default coverage | Fixed received content fixes that default. This differs from the installation-created default in A/B, so it supplies no independent differing-value pair with identical fixed bytes. | Any remaining in-force installed object or setting needs remaining coverage. |

## 7. Crosswalk to every D1 inventory kind

Source universe: `D1/compare/STATS.md`, table “By kind”: **45 kinds, 16,375 objects**. Each example ID below is an actual row of that kind in `D1/compare/joined.tsv`; `S1/raw/kind-examples.tsv` stores the extracted counts and IDs. The mapping is to **possible sentence routes**, not an adjudication of those rows. Neither classifier's decision is used as a premise. Kind labels alone do not prove membership, unchanged contents, derivation, default provenance, executable capability or lifetime.

- **P**: package-content route, S8.2-16, with the actual package-receipt facts and ordered classification; **G**: installed output genuinely built/obtained from a line, S8.2-16, including compiled code, generated installed lists and dependency packages.
- **D**: default-setting route through its package, S8.2-17. Ordinary non-default settings instead require their own line. Received unchanged defaults can reach P before the setting question.
- **R**: runtime-only manifestation, S8.2-5; follow its creating program/setting and that parent's recording route. This is not independent blanket P/G/D coverage of the runtime row.
- **N**: after failure of earlier questions, record/material under S8.2-15; S8.2-2/19 permits no mandatory line or voluntary recording. **Split**: the inventory kind may aggregate unlike members, so no single recording route follows from the directory/image label.

Every P/G/D entry below is conditional on its sentence's actual facts. If none applies to a required object, use its own line. The table does not infer that any cited example was produced during installation; that additional provenance may be FACT_UNKNOWN.

| D1 kind | Count | Real example ID | Applicable indirect route and necessary distinction |
|---|---:|---|---|
| L2:stored-ownership-unresolved | 3676 | `alma-632511e739337dc6b0644fd0` | Split: P/G/D if the corresponding provenance holds; otherwise N or own line. Ownership is not supplied by the kind. |
| L2:stored-outside-packages | 3174 | `microos-4e547bbfff8b6a90a75081b4` | Split: G for derived installed/code members; D for installation defaults; otherwise N or own line. Outside-package storage is not derivation proof. |
| L1:package | 2484 | `alma-d15afe8d066344657cce9f0e` | G for an installed dependency; P only if actually obtained within another package/image; otherwise own line. |
| L2:executable-code-outside-packages | 1874 | `microos-900b60a922695141d874da92` | G for actual derived executable output; otherwise own line. S8.2-9/10/20/23 determines executability. |
| L1:process | 1574 | `alma-9a469fe77b60b9eee6cbc515` | R: follow the creating program; no independent process line (S8.2-5). |
| L1:module-name | 610 | `alma-5af8cb1ac7d4e30d3d553dfd` | R if only a live module name; a stored module must separately meet P/G or its own-line rule. |
| L1:unit-file | 559 | `alma-b6d46ec30f2a5544c8f034eb` | P for unchanged received file; G only if installed derived output; D for an installation-default setting. S8.2-23 distinguishes code from values. |
| L1:polkit-action | 455 | `alma-14871a4e021248a0eb594cdd` | P for unchanged packaged policy; D for a default access setting; otherwise own line. |
| L1:service | 331 | `alma-85015779692fff0fbc940ccc` | D for installation-default enablement/parameters; P for an unchanged received setting; R for only its running manifestation. |
| L1:driver | 303 | `alma-93239e121b690d843ef6c96d` | R for a live binding; P/G for a separately identified installed driver program. |
| L1:firewall-rule | 206 | `alma-5d4851bac204d92d245f2971` | R for runtime-only manifestation; P/D for the actual unchanged packaged/default setting; otherwise own line. |
| L1:access-rule | 155 | `alma-6d0aa52e5b3df3c2be89cd1f` | P for unchanged received policy; D for installation-default access value; otherwise own line. |
| L1:group | 130 | `alma-baf86b8658c50b69d8d05108` | P if an unchanged received group record meets question 1; D for installation-default rights/account configuration; otherwise own line. |
| L1:firewall-chain | 127 | `alma-0c695f336bb265c216f7580d` | R for runtime-only chain; P/D for its actual persistent packaged/default setting; otherwise own line. |
| L1:user-unit-file | 121 | `alma-980ca635a3094dc22a3e5fe2` | P for unchanged received file; G only for installed derived output; D for a default launch setting; R if only runtime-generated manifestation. |
| L1:socket | 66 | `talos-d8c29fedf733e0a4a51ba28e` | R if it exists only while running; separately classify any saved socket/service configuration (P/D or own). |
| L1:account | 58 | `alma-1270901ac803f087770d4a03` | P if unchanged received account content meets question 1; D for the installation-created default account; otherwise own/source line. |
| L2:image | 48 | `alma-ccee8b9ad93a05d741a4a687` | Split: P/G for installed image or executable members; an image installed as a whole is a package (S8.1-6); otherwise classify contents. |
| L2:code-ownership-unresolved | 46 | `alma-6ab52ad29dde92c736eff4ca` | P/G conditional on receipt/derivation; own line for other executable code. Unknown ownership does not supply coverage. |
| L1:network-state | 42 | `talos-2f36d1463959ee3f8c73cb86` | R if live state only; P/D for actual packaged/default network setting; otherwise own line. |
| L1:firewall-ipv4 | 40 | `void-55d99c0ce07ba7097a94c507` | R for runtime entries; P/D for saved packaged/default rules; N if the row is only recorded report text. |
| L1:sudo-access | 36 | `alma-f6259a1b9fd662992dde8e5e` | P/D for actual packaged/default access policy; R for a live manifestation; N for a report that is not itself the policy. |
| L2:stored-ownership-unknown | 35 | `talos-d82085fcdfd8922534b0400b` | Split: P/G/D only with the missing facts; N or own line for other classified members. |
| L1:firewall-ipv6 | 29 | `void-53790aba31a820a2b8048e4c` | R for runtime entries; P/D for saved packaged/default rules; N if merely report text. |
| L1:timer | 19 | `alma-6f09e788229a52376c55f438` | R for a live timer; P/D for a received/default schedule setting; separately classify its stored unit. |
| L1:user-service | 18 | `alma-091c0495a609c53ca29b9022` | R for running manifestation; P/D for received/default launch setting; otherwise own line (S8.2-14/22). |
| L1:mount-resource | 18 | `talos-b02c86d496a85cd38e7e387d` | R if only a runtime mount resource; P/D for its persistent received/default filesystem setting. |
| L1:port | 17 | `alma-84d725a8c827746aa63fabfa` | R: the open port follows its creating program/setting, S8.2-5. |
| L1:runit-service | 15 | `void-59e0e7fd507094a2cd50772c` | P for unchanged received service content; D for installation-default service setting; R if runtime-only manifestation. |
| L1:container-image | 14 | `alma-38796fa980d637275ca18b36` | P/G if package content or installed derivation; otherwise own line for installed/executable content. Container naming is not an exemption. |
| L1:saved-network | 13 | `alma-c2ca5831f857c8ba99cdfc0e` | P for unchanged received value; D for installation default; other personally chosen saved networks need their own line. |
| L1:mount | 13 | `talos-a3c68f4b469259b6ad8f61a5` | R for runtime mount point; separately classify its saved filesystem configuration (P/D or own). |
| L1:network-configuration | 11 | `talos-6998c9d70456b15188cbe45a` | P/D for actual received/default setting; R if the row only represents runtime state; otherwise own line. |
| L2:opaque-directory | 11 | `talos-b2c1d35516b9bf6ae72ee042` | Split: member facts required; P/G/D for qualifying members, R for runtime-only members, N for remaining records/material. |
| L1:kernel-module | 10 | `talos-2786c8805d2d10a875f176ff` | R for live module manifestation; P/G or own line for separately identified installed module code. |
| L1:saved-network-file | 7 | `alma-514d98f76b08abf8d7841b6e` | P for unchanged received file; D for default setting; otherwise own setting line. Filename alone does not show provenance. |
| L2:code-ownership-unknown | 7 | `talos-0ef7f470fe09509cf8804594` | P/G only with receipt/derivation facts; R for runtime-only item; otherwise ordered capability/classification check. |
| L2:image-container-store | 6 | `alma-0c99474b7568b9110f088ac0` | Split: P/G for qualifying installed image/package/code members; D for defaults; N for remaining records/material. |
| L1:container | 4 | `alma-d425410a38af578ebda1ae31` | R for runtime instance; its own-process program remains subject to S8.2-22. Stored image/code uses P/G or own line; settings P/D or own. |
| L1:block-device | 4 | `talos-6ca7b1e2069941171bbdc3bd` | R if runtime-only device manifestation; separately classify persistent device/filesystem settings (P/D or own). |
| L1:user-timer | 3 | `alma-84d03e84c4dd242bf7cbcb83` | R for runtime timer; P/D for received/default launch/schedule setting; otherwise own line. |
| L1:firewall-table | 2 | `alma-29c00ab03689c5595ac65e00` | R if runtime-only; persistent received/default policy can use P/D, otherwise own line. |
| L2:snapshot | 2 | `microos-7498ba233df8431e0868598a` | Split: copying/snapshot naming alone proves no G relation; examine stored members for P/G/D, executable own-line duty, or N. |
| L1:docker-container | 1 | `void-6a88d609b57d2b7af3ba2aba` | R for runtime instance; separately apply S8.2-22 to its program and P/G/D or own-line rules to stored objects/settings. |
| L1:docker-image | 1 | `void-24ae24b13acd038977065c77` | Installed image/code requires P/G or own coverage when its facts meet those routes; the kind alone does not prove a package or derivation. |

This crosswalk includes every kind even where the only available route is through a runtime parent or where the label leaves the classification unresolved. It does not silently turn all directory members, generated lists, images or cached code into package-covered objects. Fonts/icons/translations/tables/firmware/default values have no separate D1 kind names: when present they occur within the package/payload or stored-object kinds, and S8.2-8 explicitly includes them. No invented example ID is supplied for an absent standalone kind.

## 8. Findings and questions

**Gaps in the idea.** The Understanding pair demonstrates a failure of the implication from recording and fulfilling a package's allocation requirement to knowing its realized account configuration. Exact cross-computer equality under a mere constraint interpretation likewise lacks uniqueness, but Reproducibility's wording prevents assigning that conditional failure an unconditional 0. No logical gap was established in Removal's P1 implication. These labels do not determine the outcomes.

**Gaps in the wording.** Reproducibility does not decide between one clear requirement and one possible result, or between satisfaction of the described requirement and equality of all covered fields. Appendix A.4.4's additional comparisons make that distinction consequential. “Such a package” in S8.2-7 leaves a boundary question about old non-code remnants; S8.2-19 alongside Section 8.5 raises an intended-scope question for voluntarily recorded material. Those latter questions do not create an in-force counterexample to the Removal proof. The ordered classification must also precede S8.2-16's generated-list example; the example alone is not a new classification rule.

The author-only alternatives are stated in plain words in `S1/QUESTIONS.md`. No rule was supplied to choose between them, and no change to the fixed text is proposed. F1's coverage-versus-value objection survives this constructed pair; F10 survives as the stated reading dependency; F11's no-uncovered-force claim is derived from P1. These are argument results awaiting RV-S1, not changes to earlier check outcomes.

Verification: the exact quote-check command and its output are saved in `S1/raw/quote-check.txt`; kind-count/ID and input-integrity checks are saved in `S1/raw/validation.txt`.
