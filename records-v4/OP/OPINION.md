OPINION: 2 ways not covered by the checks

Independent opinion, 2026-11-23 UTC. Evidence and source identities: [SOURCES.md](SOURCES.md). Paths below are relative to the night folder. No machines were started and no experiments were performed for this opinion.

The two counted ways are **F1, whether coverage actually gives Understanding**, and **F2, the meaning and continuing validity of an external-source line**. Neither has a discriminating check in the supplied plan and concrete build rounds. The number counts missing coverage, **not two established refutations**. Other ways below have at least deliberate partial coverage and are not included in that number. A general invitation to notice contradictions is not equivalent to checking a particular implication or behavior.

My judgement on **“checked completely” is ?**. This is not a replacement for the published checks' outcomes. I do not find a demonstrated impossibility of jointly satisfying P1, P2 and P4. I do find a substantive missing argument between recording an object and determining its actual state, unresolved ordinary classification cases, and a substantial difference between invariants at every moment and successful endpoint checks. More successful classifications alone would not close those matters.

## 1. What the hypothesis claims

The proposal defines a class of computers governed by a designated description: all relevant actual state is covered by it; its requirements are actually fulfilled; ordinary installation and configuration cannot escape it. It additionally claims three benefits follow. Calling something a definition does not establish that it is unambiguous, jointly satisfiable, useful for the stated ordinary work, or sufficient for those benefits. Conversely, an existing distribution lacking a property does not refute the definition.

These are separate propositions to examine, drawn from TEXT.md Sections 8.1–8.5 and the aims in Section 9/Appendix A. Their truth is not asserted by listing them. The final column maps each to the objections below; it also makes explicit where I have no separate counterexample.

| Claim | Independently assessable content | Main possible failures |
|---|---|---|
| C1. Primary description | There is an identifiable, designated declaration, and the direction of control is from it to the computer. A retrospective inventory is insufficient. | F8 |
| C2. Object decision | With the relevant facts known, the ordered questions and clarifications give one consistent answer about kind and recording duty for every real object. Runtime objects, restricted code and personal records fit that account. | F3–F5 |
| C3. Coverage | Own, package, derivation and default coverage identify which line records an object without silently treating arbitrary outputs as already described. | F1, F4, F5 |
| C4. External lists | Naming an external source is a coherent substitute for enumerating its objects; it remains compatible with the properties. Understanding and reproducibility have the stated exceptions. | F2 |
| C5. Actual state and time | Presence, startability, enabled services, existing accounts, line requirements and the last successful application give usable truth conditions throughout the stated time interval. | F6, F7 |
| C6. P1 | At every relevant moment, every in-force installed object and setting is recorded. | F3–F8 |
| C7. P2 | At every relevant moment, each recorded requirement is fulfilled. | F1, F2, F6, F7 |
| C8. P4 | Every ordinary route obeys the declaration, and installation/configuration tools record their changes, including when privileged. The breaking exception has an identifiable boundary. | F4, F8 |
| C9. Joint realizability and ordinary work | One nontrivial system can maintain all three together while performing the ordinary work specified for check 2. This is an explicit aim of Appendix A.4.3, not a theorem obtained by defining the properties. | F6, F9 |
| C10. Understanding | From the declaration alone one can know what is installed and how the computer is configured, with the named-source qualification. | F1, F2 |
| C11. Reproducibility | An unambiguous declaration yields exactly its described result on another computer, subject to the external-list and hardware qualifications. | F1, F10 |
| C12. Removal | A removed line leaves no contribution in force that the remaining lines do not record. | F11 |
| C13. Applicability | Existing systems can be assessed against each property using the definitions and adequate facts. This is check 4's aim; it is distinct from existence of a system with all three. | F3/F8 could obstruct a different assessment; no such obstruction was established in the six supplied cases. |

The operative property statements are:

- **S8.3-4:** “**P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.”
- **S8.3-5:** “**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.”
- **S8.3-6:** “**P4. Law.** The system provides no ordinary path for changing what is installed and settings past the declaration.”
- **S8.3-7:** “Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.”
- **S8.3-8:** “What is installed and settings can be changed past the declaration only by breaking.”

Section 8.5 makes representation, protection mechanisms, authority, rollback and handling of material design choices. Their absence from the definition is not a hole. A chosen mechanism must nevertheless fulfill the properties. Section 9.6 expressly leaves long-term work with all one's programs unchecked; that broader usability claim must not be imported into C9, or presented as already established.

## 2. Concrete ways the claims could fail, and whether the checks would notice

“Strong” means a direct logical argument or a documented mechanism; it does not turn an unrun situation into an observed failure. “Medium” identifies a consequential unresolved boundary with an ordinary witness. “Open” means there is a legitimate obligation to check but no demonstrated contradiction. These are argument-strength descriptions, not weights under PROTOCOL.md.

### F1. A line can cover a default without identifying its actual value

**Claims:** C3, C7, C10, C11. **Strength:** strong objection to the inference of exact Understanding; conditional objection to reproducibility, depending on what “unambiguous” requires.

**S8.2-17:** “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”

**S8.1-12:** “The required state of a recorded object is stated by its line.”

Consider two ordinary packages that create service accounts with automatically allocated numeric identifiers. Install the packages in opposite orders, eventually retaining the same package declaration. Automatic allocation and creation only when an account is absent are ordinary documented operations, not a malicious program: see the [sysusers.d manual](https://www.freedesktop.org/software/systemd/man/258/sysusers.d.html#ID) and the saved excerpt in SOURCES.md. A concrete pair of different allocations has not been measured here.

The logical countermodel is simpler than a claim about a particular distribution. Let a package's requirement be to create its named account using a free identifier, without requiring a particular identifier. Consider two states using different identifiers, both satisfying that requirement. Default coverage records the accounts under the package lines. P2 requires the chosen allocation policy, not a number absent from the requirement. P4 can mediate all changes in both states. Thus the three properties do not by themselves select one numeric configuration. There is no external-list line in this example. Account identifiers are not an invented diagnostic detail: Appendix A.4.4 explicitly compares them.

This gives a precise fork. If Understanding promises the actual configuration, its derivation needs a condition not supplied by mere coverage. If it promises only knowledge of the allocation policy, that weaker statement is consistent with the example, but exact equality of the resulting account identifiers is not thereby a consequence. I would not resolve that fork by quietly adding exact generated values to every declaration: that is an implementation choice stronger than the stated package-default rule. Nor am I claiming that either existing account allocator satisfies all three properties; the argument is about what the premises require.

**Detection: NO for this implication.** Check 1 can correctly classify both accounts as covered defaults and pass. Check 4 can correctly assess its six cases and pass. A2's stated sentence work ends at Section 8.3, before Understanding. Check 3 provides **related partial evidence**, but compares two clean executions of one declaration; B2's present account format requires explicit numeric identifiers. That can establish equality for the stronger fixture while avoiding this countermodel. No supplied step asks whether every permitted coverage relation determines what Understanding promises. This is the first counted omission.

### F2. Naming an external source does not by itself specify which time's list is in force

**Claims:** C4, C7, C10, C11. **Strength:** medium; an ordinary missing test and possible semantic gap, not an impossibility proof.

**S8.2-18:** “A line may take a list from outside the declaration, for example accounts from an organisation’s server; in that case, what counts as recorded is the source named in the line.”

An ordinary laptop uses directory accounts, loses its connection, and continues with cached identity information. The directory then removes a user or changes a group. Cached offline identity/authentication is documented in [SSSD's own troubleshooting guide](https://sssd.io/troubleshooting/basics.html#troubleshooting-identity-information); no particular product's revocation delay is assumed here.

For a line naming that source, what must P2 match: the list read at application, the latest successful refresh, or the current remote list? Those choices produce different decisions about the same local account. Removal of the source line also raises a concrete question about still-effective cached accounts and group access. The reproducibility exception does not expressly suspend P1, P2 or Removal.

This is not a demand for instantaneous remote knowledge. A line can state a snapshot or caching policy, and S8.1-12 permits line-specific requirements. A system with that explicit policy may be entirely coherent. The question is whether the source-only form the text permits has an unambiguous required state, and whether the chosen policy stays enforced through refresh, disconnection and removal. If an unspecified time is needed to decide the case, the answer is not obtained merely by identifying the source. I do not choose a freshness rule for the author.

**Detection: NO.** The named inputs/results contain no explicit external-source lifecycle test. D4 deliberately establishes its account counterexamples without such a source. B2 has finite local account tuples but no supplied external-list fixture, refresh contract or source-removal case. General account tests and local crash tests do not exercise this distinction. This is the second counted omission.

### F3. Restricted installed code can receive conflicting recording duties

**Claims:** C2, C6, C13. **Strength:** strong textual candidate; the specific witness's capabilities still matter.

**S8.2-1:** “Everything that is installed and every setting must be recorded.”

**S8.2-6:** “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

**S8.2-21:** “Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.”

An installed browser extension is the ordinary proposed witness in A2/VERIFY.md, candidate N1. If Q1 makes it an installed object and its actual confinement satisfies S8.2-21, one rule requires recording and another permits omission. Choosing Q1 first fixes its kind; it does not plainly say which of those recording duties prevails. Treating every clarification as an overriding exception is also a priority rule that the fixed text does not expressly supply. Section 8.6 expects an extension to be recorded, which makes dismissing the conflict by an assumed exception especially unsatisfactory.

I would retain this candidate. I would not treat absence of several named extension permissions, by itself, as a proof that no route can launch a host program or change a relevant setting. The concrete capabilities must satisfy the whole exemption. W0's extension dispute has a different emphasis—whether the installer/program definitions determine package status—and does not automatically prove the same argument. These are questions to adjudicate, not two independently confirmed holes merely because both reports mention an extension.

**Detection: YES as a search route, not yet a settled outcome.** A2 verification and W0 already found the issue; extension actions are in check 1, and B2 rounds 1–2 cover related code. It is not an uncovered way. The danger is losing it because the A2 headline says zero cards, or importing an implementation's preferred reading as the adjudication.

### F4. Saved code and derived output can be covered too broadly or classified at the wrong operation

**Claims:** C2, C3, C6, C8. **Strength:** medium for the remaining semantic boundary; strong that a recorder must distinguish these cases.

**S8.2-9:** “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”

**S8.2-23:** “A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.”

**S8.2-16:** “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

First, a shell or language history contains retained executable statements but is initially read as history data. B1/fix-b1-1/GAPS.md identifies the competing decisions. The relevant object and capability must be specified: reading a file as values once does not prove it can never supply executable statements; conversely, an arbitrary history file is not necessarily a valid script as a whole. A decision that changes only because one classifier considered the file and the other its entries is not yet a contradiction for the same object.

Second, a recorded compiler, interpreter or application builds or downloads new code using mutable project/input files. Causal descent from a recorded program is weaker than being built **from a declaration line** specifying the relevant input. If the compiler's own line covers every possible output without recording the distinguishing inputs, much of P1 becomes an ancestry assertion and F1 returns. If an actual source/derivation line is required, that broad loophole closes. The text and the observed derivation must decide which applies; I do not assume that merely naming the compiler is enough. W0/RESULT.md records the open question about “the system itself built”, and B2/STAND.md expressly identifies its stricter saved-input treatment as an engineering reading.

**Detection: PARTLY.** B1 has the history cases; check 2 includes interpreters and builds; B2 round 2 requires actual provenance and rejects coverage inferred from an interpreter name. These are valuable. A pass under that stricter implementation does not by itself establish that the text requires its coverage rule. One needs a text-based decision about the derivation, not only a successful execution guard.

### F5. A file inventory can miss the real object or its decisive fact

**Claims:** C2, C3, C6. **Strength:** strong limitation of inference from the inventory; medium as a source of new textual gaps.

**S8.2-14:** “A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.”

An application profile or database can hold ordinary records, an autostart choice and stored executable content together. Deciding a containing path as a record does not decide each of those objects. A composite row is not itself proof that the definition gives two answers for one indivisible object. Conversely, finding no offending file is insufficient if the offending setting is a database entry or access decision. Changed package files and unknown installation defaults pose a second problem: the facts that decide the first question may be missing even when the path and package name are known.

B1's home-page case is a real language boundary, but a weaker candidate for a hole in the idea: whether “launches something” includes opening a page affects one recording duty; it does not show that recording the intended launch/access settings is impossible. I would give it less priority than F1, F3 or F6. I would retain the two readings rather than turn an ordinary page navigation into an invented host-program execution.

**Detection: PARTLY.** D1/A3 deliberately collect provenance and code, and their MIXED/UNKNOWN dispositions expose the issue. B2 includes executable serialized input and settings readers. But file/directory counts, a whole-file label, or subtraction of base-equal inventory rows cannot prove value-level coverage. Any reduction is safe only to the extent that equality includes the facts relevant to the definition. The supplied READY files disclose substantial unknown ownership/integrity facts; these cannot be silently converted into either coverage or gaps.

### F6. Endpoint correctness can conceal violation during an ordinary change

**Claims:** C5–C9. **Strength:** strong test obligation; no general impossibility established.

**S8.3-1:** “The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.”

**S8.1-14:** “The declaration in force is the declaration of the last application that the system reported as successful [3, Section 3].”

After a successful application, make an ordinary update that changes a service account and an access rule. A later update is still within the time following the earlier completed application. If one live value changes before the new success report, the old declaration may already be false. If success is reported first, the new one may still be false. A failed update that restores the old state several seconds later does not erase the intervening violation. A second administrator, a timer or an existing process makes this an ordinary observable situation, not merely an argument about an invisible machine instruction.

B2's shell-admission barrier and freezer address interference, but pausing observers does not by itself make an actual changed account, rule or device state equal to the old requirement. Conversely, an architecture could make effective state and the active description change together. The argument defeats a sequential partial-activation scheme, not every possible system. If the only defense is to reinterpret “at any moment” as “after recovery”, that would change the hypothesis.

**Detection: PARTLY.** Appendix A.4.3 checks readback after application and cuts immediately after success. B2 round 3 adds valuable failed-operation, supervisor and recovery cases, including multi-resource effects. The supplied procedure still needs a trace/invariant argument about intermediate state, not merely a final statement that no partial state survives. Round 4's combined work does not supply that argument automatically.

The special unsaved download/execute case in Section 9.3 also observes a post-reboot condition. Its clean reboot does not establish that settings changed during execution were recorded while in force. B2/ROUNDS.md correctly states that a setting need not survive reboot to require coverage; that distinction must survive into the acceptance evidence.

### F7. A checker can use the wrong meaning of “in force”

**Claims:** C5–C7. **Strength:** strong, mostly already recognized in the plan.

**S8.1-9:** “**In force.** An installed object is in force if it is on the computer; a program, if it runs or can be started.”

**S8.1-11:** “A service is in force if it is enabled; an account, if it exists.”

**S8.2-5:** “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”

Ordinary counterexamples include an unrecorded installed font that has no process, a startable saved program that is not currently running, an account whose login is unused, and an enabled service whose process happens to be stopped. P1 can fail in the first three despite an empty process list. A stopped service does not violate a line requiring only enablement; a line that explicitly requires running state has a stronger requirement. Package membership, executable capability and a current process must not be interchanged for convenience. Runtime objects must be traced to the creating program or setting, not automatically required to have their own separate lines; voluntarily recorded runtime requirements still incur P2.

**Detection: YES for the named mechanisms; PARTLY for completeness.** Check 1 has two inventory levels; check 2 includes saved execution and removal; B2 round 2 explicitly addresses non-code package contents and defaults. B2/STAND.md distinguishes optional active-state requirements. This is not a new omitted family, but a process-only or declared-lines-only observer would still miss it.

### F8. A bypass can be excused as breaking, or a retrospective record accepted as a declaration

**Claims:** C1, C6, C8, C13. **Strength:** strong, with concrete implementation failures already reported.

**S8.1-2:** “The computer is brought into conformity with this text, rather than the text being compiled from the computer.”

**S8.1-3:** “The declaration consists of files that a person has designated as the primary description of the computer; there may be many files, and together they form one description.”

**S8.1-15:** “**Breaking**—a change to what is installed or settings, made past the declaration through the power of superuser privileges, outside the built-in tools: by writing directly to files, deleting, or disabling system mechanisms.”

An ordinary native account tool or package-manager API must not escape merely because a wrapped command records changes. Root use of a built-in tool is not breaking. Unprivileged editing of a setting is not breaking either. Relabelling these paths would make P4 easier than the text. B2/STAND.md correctly retains the native root account-tool bypass as a failure of that prototype.

A different false pass would occur if a tool first changes the system and later incorporates the observed result into a designated manifest, with no declaration-directed application. Exact agreement at the final readback would not establish C1 or continuous P1/P2. This is a warning about the acceptance method, not an accusation that adopting an initial inventory as a future declaration is forbidden. Initial capture and ongoing retrospective governance are different facts.

B1's compiler/build-tool dispute belongs here too. Its five rows change the tool-specific recording obligation, while both readings still forbid unrecorded executable output through an ordinary route. That is materially narrower than five separate impossibility results.

**Detection: YES for the principal bypasses, PARTLY for direction and integration.** D4 has actual/documented built-in account operations; check 2 explicitly includes privileged built-in tools; B2 round 1 has positive broker tests, direct routes and APIs. The remaining acceptance question is whether the designated primary description controls the whole transition, including its native backends, rather than merely matching the final inventory.

### F9. Safe refusal can satisfy the negative tests while avoiding useful coexistence

**Claims:** C9 and the practical significance of C6–C8. **Strength:** strong test-design risk; open as an incompatibility claim.

A prototype can block an unrecorded script, then also fail to support the corresponding recorded build or editor workflow. It can satisfy each feature separately in configurations that cannot coexist. Or it can repeatedly refuse changes without falsifying any requirement after a successful application. Such results do not supply the constructive witness promised by check 2's aim.

On the other hand, no logical impossibility follows merely from allowing an interpreter or from difficulty recognizing arbitrary code. **S8.2-19:** “What need not be recorded may also be recorded in the declaration.” Conservative recording, mediation, or a restricted declaration language remain possible choices. Section 8.5's permission for an algorithmic declaration does not require every implementation to decide or terminate every possible algorithm. An abstract undecidability slogan would not refute this text. In particular, B2's open M5.02 requirement for unrestricted algorithmic semantics is a declared construction ambition; inability to close that ambition is not by itself failure to implement the definition in an allowed finite form.

**Detection: PARTLY, deliberately planned.** Appendix A.4.3 has positive ordinary work; B2 rounds 1 and 4 explicitly reject refusal-only evidence and require coexistence, real Wi-Fi and Bluetooth, browser work, documents and an ordinary shell. This is substantially better than counting blocked bypasses. It is still a finite useful witness, not long-term compatibility with all programs. The presently unsupported formats and missing hardware are testbed limitations yielding ?, unless a separate argument establishes a contradiction in the requirements themselves.

### F10. Reproducibility can be tested at the wrong strength or on an uninformative fixture

**Claims:** C11, with implications for C3 and C7. **Strength:** strong distinction between the claim and its oracle; conditional counterexamples.

Section 8.4 claims exactly the result described in an unambiguous declaration. If a description uniquely fixes the relevant result, P2 already gives that result on either successful application; proving the consequence then largely requires proving uniqueness and the common interpretation. If a description merely imposes unambiguous constraints with several valid realizations, equality of all realizations does not follow. F1 is an ordinary example of that distinction.

Check 3 compares additional hashes, permissions and account fields beyond explicitly stated values. That is justified only if those fields are determined by the declaration's semantics, including its coverage/default rules. An unexplained difference in a required value is adverse evidence; a difference in an unspecified value is not automatically a refutation of the stated consequence. Rejecting every troublesome input as “ambiguous” only after its results differ would make the test circular.

There is also an explicit scope mismatch to resolve in the record: Section 8.4 excludes differences explained by hardware, whereas A.4.4 accepts that explanation only for drivers, firmware and device files of differently present hardware. A declared ordinary application build using `-march=native` may produce hardware-dependent application code, as the [GCC manual](https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html) documents. Such a binary is not necessarily a driver, firmware or device file. A failed equality comparison could therefore obey the narrow published check while failing to refute the broader consequence. This is a mechanism, not a claim that the two current testbed machines have different CPUs or different binaries.

**Detection: PARTLY.** Check 3 and B2 round 4 test exact comparisons, and B2 admits that finite formats do not prove arbitrary algorithmic requirements. Identical pinned builds are useful but can avoid default allocation, history dependence, mutable derivation inputs and the hardware mismatch. The semantic obligation and the equality oracle must be assessed before running; existing fixed outcomes must not be silently redefined afterward.

### F11. Removal depends on a correct coverage relation and complete observation

**Claims:** C12, C3, C6. **Strength:** strong as an implementation/test obligation; no independent logical counterexample established within the stated domain.

Ordinary failures include a removed program still running through a child, a saved executable copy still startable, a job recreated by a timer, a container restarted from retained state, or a derived object surviving with no remaining covering line. Shared contributions are the essential control: remove one owner while another valid owner remains, then remove the last owner. Testing only the first case could wrongly demand deletion; testing only unique owners could miss a faulty contribution graph.

For objects still subject to mandatory recording, Removal follows from P1 if the remaining declaration genuinely provides no coverage: a surviving in-force unrecorded object would violate P1. That is a useful short derivation, not a new empirical law independent of P1. It depends on F3–F5 being resolved. Material and program-record deletion are outside the definition; I would not manufacture a refutation by demanding that a removed application erase the user's documents.

**Detection: YES for these families, PARTLY for actual scope.** Appendix A.4.3 supplies program/service/rule removal; B2 rounds 2–3 extend it to non-code package content, descendants, retained copies, activators and shared ownership. These are well-targeted. Their success will establish only the observed kinds and the proved coverage semantics, not an exhaustive absence of every possible residual object.

## 3. What the supplied results establish now

| Evidence | What I accept from the named files | What it does not establish |
|---|---|---|
| `A2/CARDS.md`, `A2/VERIFY.md` | Zero original cards; verification finds candidate N1. The pair table has 741 pairs of 39 sentences, uses 14 witnesses, and uses the unchanged gawk package in 399 rows. Verification says the protocol-wide scope additionally has 340 pairs involving Section 8.3 absent from that table. | Neither all semantic combinations nor absence of contradiction. A consistent pair on one witness is not universally consistent; pairwise checks also do not prove joint satisfiability. No Section 8.4 implication is established. |
| `B1/RESULT.md`, revised `GAPS.md` | 53 decided, 8 two-ways and 27 fact-unknown rows; the eight disputed rows comprise three families. Revision acceptance is pending in the report. | Eight independent holes in the idea, or actual enforcement of 88 channels. The classifications are explicitly unweighted and are not the four checks' outcomes. |
| `D4/RESULT.md` | Check 4 reports 1 for six determinate negative property assessments on its concrete inputs. | Existence, compatibility, useful implementation, or the consequences. An inconsistent conjunction could still have easily assessed negative cases. |
| `D1/in/READY.md`, `compare/STATS.md` | Four inventories, none from Gentoo; 16,375 rows; 7,708 rows sent to adjudication; 52.99% matching decisions. Talos' second level is explicitly incomplete; package provenance/integrity is not uniformly known. | A complete five-machine check, an outcome inferred from agreement, or a gap wherever facts are unknown. “L2 rows exist” is weaker than complete second-level coverage. |
| `A3/in/READY.md`, `compare/STATS.md` | Three lived/base pairs; 24,249 retained rows; 21,251 for adjudication; 12.40% agreement. In 14,918 matrix entries one side says UNKNOWN and the other GAP-TWO. A gaming download failed. | 21,251 textual holes, long-term lived experience, or independence of each row as a new conceptual challenge. Scripted activity plus one restart is the actual scope. |
| `B2/STAND.md`, `ROUNDS.md` | Partial stand; 2 of 88 variants closed in the reported rebuilt round; documented saved-input and native root-tool failures; substantive future coverage, including positive work and lifecycle tests. | A completed property check or completed reproducibility check. Builder self-tests are not the published checks. Historical closures and a successful pinned example do not close the current open variants. |
| `W0/RESULT.md` | Calibration reports failure in 2 of 8 cases. It explains that missing answers to the meaning question produced “idea” weights. | Evidence that every such case is a disagreement about the idea or an impossibility. Under PROTOCOL.md, weighting must not begin after failed calibration. |

The missing Gentoo run and incomplete inventories prevent an all-clear where the published rules require adequate observations. They are not evidence that the hypothesis is false. Conversely, an unresolved textual counterexample must not disappear merely because the run is already incomplete.

## 4. How a false hypothesis could pass, or a true one appear to fail

The published 1/0/? rules already prevent several mistaken failures if followed. The table names mechanisms to guard against, not allegations that every mistake occurred.

| Check or procedure | How a false claim can appear to pass | How a true idea can appear to fail for another reason |
|---|---|---|
| A2 sentence review | Reuse a witness to which one sentence is irrelevant; mistake coverage of pairs for coverage of meanings; omit higher-order interactions and Section 8.4. | Require an unnatural reading instead of the operative ordinary case, or infer incompatibility from harmless overlap when the ordered questions actually resolve it. |
| Check 1 / D1 and lived inventories / A3 | Both classifiers share the collector's omissions; agree on a directory label while missing a setting inside it; adjudicate only disagreements and never challenge shared errors. Numerous repeated files inflate apparent breadth. | Treat unknown provenance as a textual gap; mistake a composite object for contradictory classification; treat failed startup/download/collection as a refutation. The correct response to insufficient facts is ?. |
| B1 channel review | A documented route name stands in for every entry point or output; one preferred interpretation of a build tool or saved input is silently baked into later tests. | Missing documentation becomes a gap; differently counted branches are mistaken for contradictory obligations; many rows of one semantic dispute become many independent failures. |
| Check 4 / D4 | Negative membership decisions are presented as positive evidence for a nonempty, coherent, useful class of systems. | Failure of a particular installed configuration to have a property is labelled failure of the definition. The protocol correctly says it is a successful assessment. |
| Check 2 / B2 | Test only the declared-line enumerator, block every attempted workflow, use a narrower finite schema to certify the whole text, or inspect only successful endpoints. A wrapper succeeds while a native tool bypasses it. | An unsupported format, unavailable radio adapter, faulty guard or recovery bug is called a contradiction of the idea. Superuser use of a built-in tool is incorrectly excluded as breaking, which creates the opposite error. |
| Check 3 | Choose only exact, pinned requirements and identical environments, then generalize to all allowed declarations and histories. Decide “unambiguous” from whether outputs happened to match. | Compare values not required by the declaration, apply the narrower hardware exclusion as if it were the consequence itself, or call an ordinary build defect a definition-only failure. F10 gives concrete mechanisms. |
| Weighting / W0 | Exclude a logical countermodel because it is not an inventory row; call a gap merely wording because two readers agree while feasibility is only asserted. This cannot close all of Section 8. | Call missing meaning answers disagreement about meaning. W0 explicitly records this mechanism in cases 3 and 8. Calibration expectations are themselves propositions to check, not evidence that an unexpected answer must be wrong. |

In particular, the protocol's real-inventory gate is appropriate for its object-weighting procedure, but cannot be the admission rule for every logical objection to the hypothesis. A proof that a consequence does not follow need not first manifest as an inventory anomaly. The beyond-plan report can contain it without changing any existing check's outcome or weighting rules.

The testbed failure rule is also sensible: one broken implementation does not refute existence of a working one. Its price is that endlessly repairing implementations cannot establish the missing logical implication or prove impossibility. Positive evidence and a written argument must have separate jobs.

## 5. Proposed order of the remaining checks

This queue preserves the published work and its outcome rules. New fixtures, readings to be compared, observations and failure conditions belong in a separately preregistered supplement; they must not be inserted retrospectively into the four checks. Any new wording belongs to a new version. “Against” below distinguishes a textual counterexample from an implementation failure, for which Appendix A.4.1 still applies.

1. **Prove or refute the consequences from the actual coverage rules.** Write the predicates for required objects, covered objects, line requirements and admissible states. Work through package-created account defaults and generated code before abstract examples. Try to exhibit two admissible actual configurations for the same declaration, and check whether Understanding distinguishes them. Derive Removal on its proper domain; state exactly what uniqueness is needed for reproducibility. **Against:** a state satisfying the premises while falsifying a claimed consequence, or an indispensable premise absent from the text. **Needs:** the fixed text, exact package/derivation semantics, the documented default example, and independent review of the argument. No new machine is necessary until a disputed behavioral fact remains. This is first because it attacks a substantive inference that the large object counts do not test.

2. **Resolve representative ordinary semantic conflicts with all deciding facts present.** Finish the ongoing adjudications, starting with restricted installed extensions, retained history/code, actual derivation inputs, and the boundary of built-in build functionality. Fix the object granularity and actual capabilities before deciding. Challenge a sample of agreements as well as disagreements. Group repeated rows for analysis while retaining every required per-object disposition. **Against:** the same fully specified object still receives incompatible obligations, or no sentence decides it without an added rule. **Needs:** the existing raw records and independent adjudication; narrowly targeted fact collection only where documentation and existing records cannot decide. Keep wording/idea weight separate; do not resume failed calibration by fiat.

3. **Check continuous state through ordinary transitions, including external-source changes.** First write the exact expected active declaration and actual-state invariant at each event. Cover a multi-resource update, an interrupted update, an overlapping ordinary change, and an external account list with refresh, offline cache, revocation and removal of its source line. Use one declared freshness policy per concrete fixture; separately expose any source-only form for which the text gives no policy. **Against:** an undecidable required state, an observable interval violating the active declaration, or a reviewed argument that the requirements cannot coexist. A prototype-only violation remains ?. **Needs:** the semantic decisions from steps 1–2, event/readback evidence independent of the mutator, and a disposable client/source pair for any genuinely unanswered external-source behavior. Pausing the shell and checking eventual recovery alone are insufficient.

4. **Close the factual and object-boundary gaps in the existing classifications.** Recover decisive provenance, integrity, contained-value and capability facts; explicitly account for missing Gentoo and incomplete second-level coverage. Audit whether the collector and base subtraction can hide changed values or executable content inside aggregates. Preserve failed original attempts and give any new observations a new identity. **Against:** a fully known ordinary object the text cannot decide. Missing facts alone are insufficient, not adverse. **Needs:** adjudication's precise fact requests and the existing collector specifications; new observations only when permitted in a supplemental run. Broadly repeating successful package-file inventories is lower value.

5. **Build one joint positive witness using representative difficult work.** Finish the authorized property work, but prioritize an ordinary shell, a recorded changing project/script, package/account administration including native privileged tools, real network/device work, browser use and document editing in the same system. Pair each denied bypass with the corresponding permitted declared operation. Require the declaration to govern the transition. **Against:** an ordinary action on the required list is impossible for reasons deduced from the definitions, or the properties require incompatible states. A missing feature or bad guard only rejects this witness. **Needs:** a stable semantic contract, the relevant hardware, a testbed and separate review. Do not make polishing every wrapper a prerequisite to asking the logical questions in steps 1–3.

6. **Complete the planned reproducibility and removal checks, then test the unrepresented distinctions separately.** Keep exact declared inputs and verify each stated value plus a genuinely independent census of extra state. For the supplement, contrast clean application with convergence after different ordinary installation histories, and separate unique requirements from defaults permitting several outcomes. On removal, test copied/loaded code, generated content, activation edges and shared ownership through removal of the final owner. Assess the hardware-oracle mismatch before interpreting a difference. **Against:** a remaining in-force uncovered object, a missing requirement, or different results that the same unambiguous description actually requires to be equal; apply the definition-only rule before assigning 0 to the hypothesis. **Needs:** steps 1–5, independently prepared installations, exact ownership/derivation evidence and a predeclared comparison oracle.

7. **Evaluate the evaluators and the final coverage argument.** Reconcile the failed weighting calibration without rewriting its historical outcome. Separate unavailable answers from actual disagreement; justify the feasibility sign rather than infer it from agreement. Use known-invalid and known-valid cases to check that the acceptance process can reject and accept for the right reasons, and audit untouched agreements. Map every claim above to a logical argument or appropriately bounded observation. **Against:** a false case passes the acceptance method, a valid case is rejected by an unstated requirement, or a claimed implication still has no argument. **Needs:** independent review, preserved expectations and all earlier evidence. Failures here reject the checking method's inference; they do not automatically refute the idea.

8. **Only then broaden ordinary-work duration and diversity.** Run modest, purposeful histories of updates, development, games, application changes, disconnections and removals, selected for mechanisms absent above. Prefer a new mechanism to another distribution containing thousands of the same kind of file. **Against:** a new real object gap or a definition-level incompatibility in ordinary work; otherwise retain implementation failures with their proper status. **Needs:** a credible working candidate and supplemental inputs fixed in advance. This extends evidence toward the deliberately unchecked long-term claim; it cannot turn a finite sample into a universal proof.

**Work of lower marginal value for the author's goal:** more A2 rows using the same harmless witness; treating every repeated UNKNOWN/GAP disagreement as a new intellectual problem; more check-4 demonstrations of already established account bypasses; and prolonged repair of variants that share an unresolved semantic boundary. I would finish the required records rather than discard inconvenient cases, but spend the remaining investigative effort on deciding distinct mechanisms. The useful parts of the existing work are the real witnesses, explicit unknowns, independent adjudication and the positive/coexistence tests already in B2's plan.

## 6. When “checked completely” would be justified

I would accept “checked completely” only as an explicitly bounded statement about this fixed text and the declared domain of ordinary work: every separate claim has been examined, every known ordinary counterexample has a fact-complete text-based disposition, the properties have a joint constructive witness with positive work, their temporal and coverage obligations have an argument beyond sampled endpoints, the three consequences have valid derivations, and the required checks contain no unresolved ? or silently omitted scope. A confirmed gap means this version fails; repairing it starts a different version. Even then I would not claim that every possible computer, future program, execution history or implementation is covered by empirical proof, that the search found all possible counterexamples, or that the properties ensure security, availability, convenience or long-term compatibility beyond what was actually stated and checked. The unqualified universal reading of “no holes remain anywhere” is never licensed by a finite set of runs.

## Short list excluded from the main objections

- Reading “a setting is in force if it has its value” as making every possible value simultaneously true. S8.1-12 supplies the line's required state; the strained reading adds no ordinary counterexample.
- Arguing that every file is a program because an imagined interpreter could execute its bytes. Use the computer's actual execution mechanisms and rights, not a hypothetical universal decoder.
- Treating failure of a disabled or merely enabled service to be running as an automatic P2 failure, demanding deletion of user documents, or calling all privileged operations breaking. The relevant scope and line requirements already distinguish these.
- Calling P2 wholly unfalsifiable solely because **S8.1-13** says “**Application of the declaration**—an action of the system that brings the computer into conformity with the declaration.” In isolation that wording invites a circular success definition, but S8.1-14 and the explicit success-report/readback procedure provide a practical failure observation. Excluding a false success report by definition would be a bad reading of the check, not a convincing new ordinary hole.
- Treating an algorithmic declaration as a promise to solve arbitrary program termination, or treating “provided there was no breaking” as permanent immunity after any privileged edit in a machine's entire past. Neither is needed to describe an ordinary counterexample to the intended claim.
