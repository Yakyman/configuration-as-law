# Removal: independent argument for assembly

Recorded: 2026-11-23 (UTC). Input: (not published: orchestration or scratch), `TEXT.md` Sections 8 and 9 and Appendix A, `SENTENCES.md`, `SUP1/step-1.md`, and objection F11 of `OP/OPINION.md`. No machine, installation, or probe was run. This is a reasoning result, not acceptance by the later review.

**Recommended outcome: 1 for Removal in the definition's domain of objects that can be in force.** P1 is already the required exclusion of in-force uncovered installed objects and settings. The proof does not establish deletion of every physical trace or of program records and material. Those are not additional obligations silently supplied here. The only unresolved scope question below concerns whether voluntary recording changes the explicit exclusion of program records and material; it does not supply a counterexample.

## Sentences used

- S8.1-6: «**Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.»
- S8.1-9: «**In force.** An installed object is in force if it is on the computer; a program, if it runs or can be started.»
- S8.1-10: «A setting is in force if it has its value.»
- S8.1-11: «A service is in force if it is enabled; an account, if it exists.»
- S8.1-12: «The required state of a recorded object is stated by its line.»
- S8.1-14: «The declaration in force is the declaration of the last application that the system reported as successful [3, Section 3].»
- S8.2-1: «Everything that is installed and every setting must be recorded.»
- S8.2-2: «The rest need not be recorded.»
- S8.2-3: «The rule applies to objects that are on the computer.»
- S8.2-5: «What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.»
- S8.2-6: «What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.»
- S8.2-7: «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?»
- S8.2-8: «Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.»
- S8.2-9: «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»
- S8.2-10: «Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.»
- S8.2-13: «Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.»
- S8.2-15: «Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.»
- S8.2-16: «What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.»
- S8.2-17: «A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.»
- S8.2-18: «A line may take a list from outside the declaration, for example accounts from an organisation’s server; in that case, what counts as recorded is the source named in the line.»
- S8.2-19: «What need not be recorded may also be recorded in the declaration.»
- S8.2-20: «A file containing code that cannot be executed on this computer is not a program.»
- S8.2-22: «A program that runs as its own process on the computer, including in a container, is a program.»
- S8.3-1: «The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.»
- S8.3-4: «**P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.»
- S8.3-5: «**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.»
- S8.3-6: «**P4. Law.** The system provides no ordinary path for changing what is installed and settings past the declaration.»
- S8.3-7: «Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.»
- S8.3-8: «What is installed and settings can be changed past the declaration only by breaking.»

Section 8.4, quote: «**Removal.** After application of a declaration from which a line has been removed, nothing the line contributed is in force unless it is recorded in the remaining lines.»

Section 8.5, quote: «How to store, transfer and remove program records and material.»

## First case: objects created during installation

The starting point is a package line, not a separate explicit account line. Examine each created object's classification first (S8.2-6), then its coverage. A package line is not a blanket waiver for everything its installation happens to touch. S8.2-16 covers installed things obtained as part of the package or built/obtained from a line; S8.2-17 expressly covers default settings created during installation.

A documented example establishes that account creation at installation is an ordinary mechanism. The `sysusers.d` manual describes creation of system users/groups during package installation or boot, and its `u` type creates an account initially unable to log in. Source: https://www.freedesktop.org/software/systemd/man/258/sysusers.d.html, Description and Type sections. The documented creation timing and initial login restriction are paraphrased here; the assembled argument supplies the shared source quotation. No claim is made that this ordinary tool itself implements P1/P2/P4.

For a stipulated created default account that is a setting, S8.2-17 covers it through the package line, and S8.1-11 makes it in force whenever it exists, including when login is disabled. If the package line is removed and no remaining line covers that account, a surviving account is an in-force setting not recorded. S8.3-4 rejects it. A state in which the account remains with no remaining coverage therefore cannot be one half of a valid counterexample pair. The proof needs neither a fixed numeric identifier nor the declaration's disclosure of it.

Other installation outputs follow the same first-pass analysis:

| Installation creates | Classification/coverage and Removal disposition |
|---|---|
| Installed package and unchanged package payload | S8.2-7/8, covered S8.2-16. In-force uncovered objects fail P1; payload classification must be evaluated again if its package ceases to be installed. |
| Default account, service parameter, access rule or other setting | S8.2-17 covers installation defaults; S8.1-10/11 supplies force. Remaining account existence, service enablement or setting value requires coverage. |
| Generated executable code | If question 1 does not decide, S8.2-9/10 decides; S8.2-16 permits genuine system derivation from a line. Runnable or running residue is subject to P1. |
| Generated non-code list | A list is not automatically installed merely because S8.2-16 gives it as an example of coverage. Its classification must first follow S8.2-6. If installed/setting, P1 applies; if record/material, Section 8.5 excludes its removal from the definition. |
| Installation log, cache or working-state object reaching question 4 | S8.2-15, S8.2-2 and Section 8.5. Retention is not a Removal refutation. If it is executable or a setting, an earlier question takes precedence. |
| Process, open port, mount point or service relationship existing only at runtime | S8.2-5: no separate object; follow the creating program/setting. This rule does not supply arbitrary other coverage merely because another program remains installed. |

This table is exhaustive by classification alternatives for installation outputs; it is not an empirical inventory of all package side effects.

## Derivation

Let D be the last successfully applied declaration, let L be one of its lines, and let R be D with L removed. Consider a moment after a completed application of R and no breaking. Let x be an object contributed by L, still within the installed/setting domain, and suppose no remaining line records x.

1. The chosen moment is in the properties' scope by S8.3-1. By S8.1-14 the operative declaration is R, not the previous D. The old removed line cannot itself satisfy present recording.
2. Determine x using the ordered questions, S8.2-6. Installed objects/programs and settings are subject to S8.2-1; program membership follows S8.2-10. This step prevents deriving deletion obligations for a record/material just by calling it a contribution.
3. Determine recording in R using S8.2-16 for installed objects and S8.2-17 for settings, with the source exception S8.2-18 where relevant. By hypothesis none of those remaining lines covers x. The hypothesis is exactly the exception condition of Section 8.4; it is not a uniqueness-of-owner assumption.
4. Assume x remains in force according to S8.1-9, S8.1-10 or S8.1-11. S8.3-4 then says x is recorded in R. This contradicts step 3. Hence x is not in force.
5. Since x was arbitrary, no contributed installed object or setting lacking remaining coverage is in force after the removal application. If another remaining line records x, Section 8.4 expressly permits its survival; S8.3-5 may require it to remain as that line requires.
6. S8.3-6/7/8 do not add a history-preserving ownership rule or a deletion algorithm. They rule out an ordinary bypass that restores an uncovered installed object or setting. In particular, no ordinary post-application action can produce the proposed uncovered in-force residue while P4 holds. P1 already rejects it at every relevant moment.

Thus P1 is sufficient for Removal over its defined installed/setting domain. P2 explains retained shared requirements; P4 maintains the same boundary through ordinary paths. All three can hold, but the derivation does not need every property as a separate premise.

## Every other indirect mode, examined after installation creation

| Mode authorized by the text | Attempted survival after removal of its covering line | Result |
|---|---|---|
| Object obtained as part of a package, S8.2-16 | Unchanged installed non-code payload remains on the computer without remaining coverage. | S8.1-9 and S8.3-4 reject it if it is still installed; see the reclassification boundary below. |
| Compiled copy built from a line, S8.2-16 | The executable copy can still run, but neither its own line nor any package/derivation line covers it. | S8.2-9/10 and S8.1-9 make it installed and in force; P1 rejects it. Failure to run on this computer is S8.2-20, not permission to claim the executable still is in force. |
| Generated list built from a line, S8.2-16 | A list survives. | Its title does not decide its kind. If a setting/installed object, P1 rejects uncovered force; if a record/material, retention is outside Section 8.5. No universal list-deletion conclusion follows. |
| Package installed as dependency of a recorded package, S8.2-16 | Its former explicit parent line is gone; another line genuinely obtains the dependency. | Recorded survival is allowed by Section 8.4. If no line covers the still-installed package, P1 rejects it even if the original installation was automatic. |
| Default value obtained with a package, S8.2-17 | A setting remains after its last covering line is removed. | P1 rejects an in-force uncovered setting. If the object remains unchanged package content, question 1 has priority and the installed-object branch yields the same rejection. |

## Strongest attempts to break the proof

**Shared ownership is not a counterexample.** S8.2-16 admits coverage through a package and through system building/obtaining; it does not require a single unique causal parent. Removing one line while another genuinely covers the contribution is the explicit exception in Section 8.4. Removing the last covering line invokes step 4. It is insufficient to assert that the remaining base line covers everything merely because the base contains the installer: S8.2-16 requires that the object was actually obtained as part of that package or built/obtained from that line. Mere capability is not that fact.

**A locked account can remain because it cannot log in.** Rejected. The documented installation example can create an account with login disabled. S8.1-11 uses existence for an account, not permission to log in. A retained account without coverage violates P1 if it is a setting.

**A disabled service can remain on disk.** This does not refute Removal. S8.1-11 makes the service in force when enabled; the consequence does not demand deletion of a disabled service as such. Its backing unit file is a separate classification question. If that file is installed package content, executable code or a setting still in force, its own classification invokes P1. Merely disabling a service does not excuse a separately in-force uncovered file or account.

**Deleting the executable file may leave a running process.** This would refute a defective implementation, not the implication. S8.2-5 makes the process belong to its creating program and S8.1-9 says the program is in force if it runs. The program remains uncovered and P1 fails. S8.2-22 specifically does not exempt a separate process in a container. Nothing in the proof treats a deleted pathname as sufficient evidence of not being in force.

**A surviving copy is no longer the original package's object.** If it can execute, S8.2-9/10 still classify it as a program. It cannot escape P1 by changing its provenance. A genuine remaining derivation line covers it, but then the explicit exception applies. Whether an actual retained copy was built/obtained from a remaining line requires its provenance; missing provenance is FACT_UNKNOWN, not new coverage.

**A non-code package remnant changes kind when the package disappears.** This is the strongest boundary objection. S8.2-7 says "such a package" after "a package installed on the computer". On a present-package reading, residue after removal may no longer pass question 1; on a historical-provenance reading it can still pass if unchanged. The present-package reading does not by itself prove a counterexample: one must classify the residue through the remaining questions and show that it is in force. If it is a program or setting, P1 still applies. If it becomes a program record or material, Section 8.5 excludes its removal, and S8.1-9/10/11 provides no independent in-force criterion for that kind. If neither question 4 provenance alternative is established, the residue's classification is unresolved, not established material. The proof does not assert that all old non-code package bytes must physically disappear.

**Voluntarily recorded material retains a requirement after its line disappears.** S8.2-19 permits recording it and S8.3-5 requires a surviving line to be fulfilled. Neither says that the removed line's requirements survive removal. Section 8.5 explicitly excludes removal of records/material. A constructed pair differing only in retained documents would therefore impose an unlicensed deletion requirement. If the author intends voluntary recording to override that exclusion and assign a persistent force notion to such objects, that is a choice of scope, recorded below; it is not selected here.

**The source still exists outside the declaration.** S8.2-18 counts the named source as recorded only through its remaining line. If the source line is removed and its account members have no other coverage, the exception cannot be invoked merely because a remote source still exists. Accounts on the computer are in force if they exist (S8.1-11); P1 rejects them if uncovered. No fact about freshness of an actual source is needed for this implication.

## Missing-premise findings; no proposals

1. No new premise is needed for the P1 implication on current installed objects and settings. In particular, uniqueness of contribution, fixed derivation results, static account identifiers, bytewise equality between machines, and a particular deletion mechanism are not used.
2. The stronger claim that every byte or artifact ever caused by the removed line must disappear needs a domain-preservation/deletion premise absent from the text. It is not the proved claim. Program records and material are explicitly outside Section 8.5.
3. Establishing a concrete remaining-coverage relation requires facts about package membership, derivation and installation defaults. The text states the permitted relations but supplies no concrete object's provenance. A concrete missing provenance is FACT_UNKNOWN; it is not a premise that the implication covertly assumes true.
4. The text does not expressly define historical contribution identity across reclassification. The proof quantifies over any contributed object that is presently an in-force installed object or setting and therefore does not need such identity to be uniquely reconstructible from the declaration.

## Wording gaps and idea gaps

Wording: possible author choices about present versus historical package provenance and about voluntary recording versus the excluded record/material removal domain are listed below. These do not establish a counterexample pair and are not silently filled by a new rule.

Idea: no separate logical gap established for Removal in the stated installed/setting domain. A practical failure to observe a running copy, classify a residual object or find its remaining coverage is not an independent logical failure of the implication.

## Questions only the author can decide

1. After a package has been removed, does an unchanged non-code file previously obtained in that package still count as an installed object, or does the first question require the package to be installed now? The first reading keeps package provenance decisive; the second sends the remaining file through the later questions. This affects physical residue classification, although P1 still proves Removal for anything that remains installed or a setting.
2. If a person voluntarily records a document or program record, does Section 8.5 still exclude what happens to it when its line is removed, or does recording it bring that removal under "nothing the line contributed"? S8.2-19 permits recording; the text does not expressly say it overrides the Section 8.5 exclusion. No deletion demand for such objects has been used in the outcome.

## Relation to earlier opinion

F11's claim is sustained only to this extent: after remaining coverage and present installed/setting status are established, P1 proves the no-uncovered-force implication. Its observations about an implementation's coverage graph and complete observation are obligations of a testbed check, not extra logical axioms of the proof. No earlier claim was treated as a premise.
