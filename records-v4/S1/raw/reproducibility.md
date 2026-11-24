# Reproducibility argument fragment

Recorded 2026-11-23 UTC. Outcome: **?**. This is a reasoning result, not a machine observation or an acceptance of the earlier opinion. Inputs: (not published: orchestration or scratch), `TEXT.md` Sections 8–9 and Appendix A, `SENTENCES.md`, `SUP1/step-1.md`, `OP/OPINION.md` F1 and F10. No probe was needed or run.

## What is actually derivable

1. S8.1-12: “The required state of a recorded object is stated by its line.” This gives a line a required state; it does not expressly say that every field of every object covered by the line has exactly one possible value.
2. S8.3-1: “The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.” Choose two such moments on two computers and the same declaration. This supplies the scope, not a promise that an application will terminate or succeed on every possible computer.
3. S8.3-5: “**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.” Consequently, each required state stated by each line holds in each chosen computer. This is the entire direct derivation of satisfaction of the described requirements.
4. S8.3-4: “**P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.” Thus there is no in-force installed object or setting outside the coverage permitted by S8.2-16–18. P1 restricts coverage; it does not add a numeric value to an account requirement or a checksum to a program requirement.
5. S8.3-6: “**P4. Law.** The system provides no ordinary path for changing what is installed and settings past the declaration.” This restricts transitions. It does not state equality of outcomes of two different applications of the same description.
6. If the declaration's required states determine exactly one relevant result, step 3 gives that result on each computer. This is a conditional inference: the uniqueness premise is not another sentence of Sections 8.1–8.3. It may be the intended content of Section 8.4's condition, “provided the description is unambiguous.” If that condition instead means only that the requirements have one clear meaning, step 3 gives satisfaction, not a unique realization.

Section 8.4 says: “The same declaration on another computer yields exactly the result described in it, provided the description is unambiguous.” A predicate such as account-name-is-fixed-and-ID-is-a-free-valid-ID can have one clear meaning and multiple satisfying states. If “result described” is precisely that predicate, both states deliver exactly it. If it includes a particular numeric ID or equality of every covered field, the states below disagree. Neither reading is silently selected here.

## First attempted case: defaults created during installation

### Documentation and limits of its evidence

Primary documentation: [sysusers.d, version 258](https://www.freedesktop.org/software/systemd/man/258/sysusers.d.html#ID). The exact excerpts and factual limits are consolidated in `S1/ARGUMENT.md`, Section 2. The countermodel does not assert that this ordinary tool implements P1/P2/P4.

### One conditional pair, not two alternative experiments

Declaration D contains these lines, stated as their complete *requirements*, not as commands in a proposed language:

- L0: the fixed common base, its installation/configuration tools and their fixed configuration are present. The allocator uses the fixed pool `{61000, 61001}`, and on first account creation selects its smallest free identifier. These integers and the selection rule define the conceptual pair, not observations of a real allocator.
- LP: fixed package P is present unchanged, with its installation procedure: create the explicitly chosen service account `alpha` and its same-name group if absent, allocating the smallest free identifier from the fixed pool; retain the resulting account/group as package defaults while P remains. The line requires those defaults and that policy, without naming the allocated integer.
- LQ: fixed package Q is present unchanged, with the analogous procedure for `beta`.

Both packages and their fixed contents are identical in both states. All other mandatory objects have identical fixed coverage and values under L0, LP or LQ. There are no external-list lines, hardware differences, ordinary changes to the resulting account values, or breaking. This is a logical candidate system: ordinary installation/configuration tools always operate through declaration changes and application; no ordinary bypass exists. No empirical claim about a real enforcement implementation is needed for the logical comparison.

State A: the first application of D installs P before Q and reports success only after both installations complete. At the observation D is in force; `alpha` has ID `61000` and `beta` has ID `61001`.

State B: the first application of the same D installs Q before P and reports success only after both installations complete. At the observation `beta` has ID `61000` and `alpha` has ID `61001`. D has the same lines in the same written order on both computers; the conceptual application mechanism does not prescribe installation order. Before these applications there was no successful application; no intermediate state governed by an earlier successful declaration is used. After completion, both states remain stable and ordinary changes are mediated by the declaration. This does not claim that two clean applications of a real allocator produce different numbers.

In each state:

- Scope: final application completed successfully and no breaking occurred (S8.3-1, S8.1-13–16).
- Classification: packages and unchanged package contents meet S8.2-7–8 first; the fixed installation code is covered content. Accounts/groups/default identifier settings are the installation defaults expressly covered by S8.2-17. If the absence of a personally selected numeric ID prevents question 3 from classifying that field as a setting, S8.2-17 still expressly covers the default value; that classification issue is not repaired here by adding “chosen automatically” to S8.2-11.
- P1: every installed object has L0/LP/LQ coverage under S8.2-16, and every default setting has its package line under S8.2-17; therefore S8.3-4 holds. S8.2-17: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”
- P2: each fixed package is present; its account and group exist; each ID is a distinct free valid allocation created at installation and retained as its line requires. S8.1-11: “A service is in force if it is enabled; an account, if it exists.” S8.1-12 and S8.3-5 require no specific integer **under the predicate reading of required state**.
- P4: each installation occurred during the first application of D, with its package line already present, and resulting defaults are recorded by that package line, using the express coverage rule. No subsequent ordinary operation changes these defaults behind D; other ordinary configuration/install operations likewise change D. S8.3-7: “Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.” S8.3-8: “What is installed and settings can be changed past the declaration only by breaking.” Different permitted installation schedules during first application are not later ordinary changes behind D.

### Attempted refutation and disposition

The strongest objection is that “unambiguous” in Section 8.4 may exclude D because its realization is not unique. That objection **holds under the unique-result reading** and is not answered by citing coverage alone. Under that reading the pair is outside the reproducibility antecedent. A separate objection invokes S8.1-12, requiring the line to state the required state. LP and LQ do state it: a named account with its automatically allocated valid ID. S8.1-12 does not expressly require a singleton numeric result, so the mere singular word “state” does not defeat this predicate requirement.

Under the clear-predicate reading, P2 is satisfied by both states and P4 does not compare distinct permitted first-application schedules. But then the pair falsifies Section 8.4's words “yields exactly the result described in it” only if those words promise equality of the realized identifiers in addition to satisfaction of the stated policy. If they promise only the stated policy, the pair does not falsify them. These are author questions, not a demonstrated unconditional 0.

The objection that P4 requires literal numeric additions for each generated default would remove the pair too, but S8.2-17 explicitly supplies recording through the package line. No sentence explicitly strengthens P4's recording requirement to a distinct value-bearing line for every such default. Conversely, the fragment does not assert that P4 permits arbitrary later changes of covered defaults merely because their package remains recorded.

The objection that both independent machines must be clean confuses the Section 8.4 consequence and the particular check. The pair meets the step's specified postapplication-state condition; it does not claim to instantiate Appendix A.4.4's clean-install procedure. Hardware and external-list exemptions are immaterial to the pair.

## Remaining required coverage families: each assessed once

These are examinations of the coverage rule's logical strength, not new observed pairs or invented facts about actual package builds.

| Family, in the required order after installation defaults | Coverage and what follows | What does not follow without an additional premise |
|---|---|---|
| Object obtained as part of a package | S8.2-7–8 classifies unchanged received content as installed; S8.2-16 records it through the package. P2 yields whatever exact package/content state its line requires. | Equal package names alone are not stated to designate equal complete contents. If the line fixes the complete artifact, then equal content follows from that requirement; coverage alone supplies no independent checksum equality. |
| Compiled copy | Express example in S8.2-16. The output must be in force as the source line requires (S8.1-12, S8.3-5). | Uniqueness of output bytes is not stated by the coverage relation. Claiming an ordinary compiler's nondeterminism would need documentation; no such claim is used here. |
| Generated list | Express example in S8.2-16; if the line fixes the list, P2 yields it. | Coverage through generation does not independently fix all generation inputs or the resulting membership/order. A line taking an external list is separately exempt from reproducibility by Section 8.4; it cannot serve as a refutation. |
| Dependency package | Express example in S8.2-16; if the line fixes the dependency artifact and required state, P2 yields them. | A uniquely determined dependency version or artifact is not supplied by the fact that a dependency is covered. No claim about a particular package resolver is made. |
| Default obtained with a package | S8.2-7–8 and S8.2-16 cover unchanged received content; S8.2-17 expressly covers the default value. | If the package artifact and its values are fixed, the default is fixed. Merely satisfying package-line coverage does not supply those pins. Unlike the installation-allocation case, no variation is asserted for the same fixed received bytes. |

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

## Appendix A.4.4 comparison

A.4.4 compares “every value the line states and, in addition” hashes/permissions of installed program files, enabled state/unit checksum, account name/numeric identifier/groups/shell/home directory, and effective rule text. These additional observations are justified as a test of Section 8.4 only to the extent that the line's described result determines them or that “unambiguous” expressly requires their uniqueness. P2 by itself does not make an unspecified additional value equal. The fixed oracle must not be silently weakened: this is a finding about the implication from premises to its equality expectation, not a proposal to change the test.

A.4.4's hardware explanation is expressly limited to drivers, firmware and device files for differently present hardware, whereas Section 8.4 says generally “Differences explained by hardware are excluded.” That textual difference is real but not exercised here; the candidate pair uses identical hardware. No ordinary-system hardware claim or additional case is introduced.

## Findings: missing premises, not proposed changes

- Uniqueness of every compared required field is not independently stated by S8.2-16 or S8.2-17. The predicate requirement explicitly stated in the pair meets S8.1-12; no sentence adds a unique numeric result to it.
- One clear meaning of a requirement does not logically imply one satisfying realization. Reproducibility as satisfaction follows from P2; reproducibility as equality of realizations needs the latter.
- Equality of additional A.4.4 observations needs them to be determined by the description, beyond their coverage. Their inclusion in the check is not a derivation of determination from Sections 8.1–8.3.
- The consequence as a promise of successful application on every other computer would need an existence/success premise. S8.3-1 scopes properties after completion. This is only a scope finding; no additional counterexample is attempted.

Wording gaps: meaning of “unambiguous”; scope of “exactly the result described in it”. Idea gaps: no unconditional failure established by this fragment; exact equality under a mere predicate reading lacks a uniqueness premise. These lists do not determine the outcome.

## Plain author questions for the assembled QUESTIONS.md

1. Does “unambiguous” mean that a requirement has one clear meaning, or that every relevant value has only one permitted result? For example, is “create this account with a free identifier” unambiguous when several identifiers are free?
2. Does “exactly the result described in it” require only the stated requirements to hold, or also identical values for all objects covered by those requirements, including values the line does not state?
3. Are the additional fields compared in A.4.4 necessarily part of every unambiguous description, even if the description does not state them? If not, how does their inequality bear on the stated consequence? This asks which existing meaning is intended, not for a changed oracle.

Recommended final consequence sentence: Reproducibility follows for the requirements stated by each line, but equality of covered values depends on the unresolved meaning of “unambiguous.”
