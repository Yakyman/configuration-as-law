VERDICT: DISAGREE

Review of `SUP1/step-1.md` and `SUP1/step-3.md` against `SUP1/SUPPLEMENT-1.md` (steps 1 and 3 and the rules line), `TEXT.md` Sections 8–9 with Appendix A, `SENTENCES.md` and `PROTOCOL.md`. Reviewed 2026-11-23 UTC.

Checked without finding: both files are recorded before the work on their step (no `S1/` or `S3/` folder exists and (not published: orchestration or scratch) holds no job of either step); the numbers (three consequences, three properties P1, P2, P4, four events of (b), outcomes 1, 0, ?) agree within each file and with `TEXT.md`; “Understanding”, “Reproducibility”, “Removal”, “covered by the line of the package”, “declaration in force”, “reported as successful”, “takes a list from outside the declaration” are quoted correctly (S8.2-17, S8.1-14, S8.2-18, Section 8.4); the second failure route of step 3 (“P1, P2 and P4 cannot hold together … whatever the system does”) and its “?” for a particular implementation agree with Appendix A.4.1 (“a requirement that contradicts another requirement—yields 0”; “Otherwise it is a defect of the testbed, and the case yields ?”); who performs the work is named only as “party”; every expected result except the one in finding 1 is worded as an expectation.

1. **Step 3: the expected result decides the outcome of (a) in advance and attributes to Section 8.5 what it does not say.**
   Where: `SUP1/step-3.md`, “Expected result”, (a).
   Evidence: “Whether a system can make every change indivisible is a design matter outside the definition; such a moment therefore gives “?”, not 0.” Section 8.5 lists program records and material, the mechanism preventing execution, adding what a downloading program installed, “User authority, generations and rollback, protection of the declaration itself and secrets, when an edit takes effect. The form of the declaration”; an indivisible change is not among them. The same file makes 0 depend on whether the properties fail “whatever the system does” — the very question this sentence answers before the work.
   Minimal fix: replace “(a) The text determines the declaration in force at every moment (the last application reported as successful), and during a change that is not made as one indivisible step there is at least one moment at which the state required by that declaration does not hold. Whether a system can make every change indivisible is a design matter outside the definition; such a moment therefore gives “?”, not 0.” with “(a) The text determines the declaration in force at every moment (the declaration of the last application that the system reported as successful, S8.1-14), and during a change that is not made as one indivisible step there is at least one moment at which the state required by that declaration does not hold. Whether such a moment gives 0 or “?” is not settled here; it is decided by the rules under “What counts against the hypothesis”.”

2. **Step 1: a second failure route not in the supplement, and an outcome rule that leaves a case undecided.**
   Where: `SUP1/step-1.md`, “What counts against the hypothesis” and “Outcome”.
   Evidence: `SUPPLEMENT-1.md` step 1: “Against the hypothesis: such states are found.” The file adds “or a consequence whose derivation needs a premise that the text does not contain”, a new way to 0. Its “Outcome” gives “?” only for a reading, so a consequence with neither a surviving derivation nor a surviving pair has no outcome. “A dispute about the reading of a sentence … gives “?”” also turns into “?” a consequence that is false under every reading.
   Minimal fix: replace the paragraph “What counts against the hypothesis” with “**What counts against the hypothesis.** Two states as described under “What is done”, that survive refutation and in which a consequence as worded in Section 8.4 is false. A premise that a derivation needs and the text does not contain is recorded as a finding; it counts against the hypothesis only through such a pair of states. Where whether a consequence follows depends on a choice between two readings of a sentence, the readings are recorded as a question for the author and the consequence gives “?”.”; and replace the paragraph “Outcome” with “**Outcome.** For each of the three consequences: 1 (a derivation survives the attempt to break it), 0 (a pair of states counting against the hypothesis survives refutation), or “?” (neither; or it depends on a reading that only the author can choose).”

3. **Step 1: the cases after the first presuppose a reading against S8.1-12 and are not fixed before the work.**
   Where: `SUP1/step-1.md`, “What is done”, “After it, every other kind of object that the rules let a line cover without stating its value.”
   Evidence: S8.1-12: “The required state of a recorded object is stated by its line.” Whether a covering line states the value is what the step tests; the sentence assumes the answer. The kinds are left to be chosen during the work, while the rules line of the supplement requires the inputs to be recorded before the first observation. S8.2-16 and S8.2-17 give the list.
   Minimal fix: replace with “After it, every other kind of object that S8.2-16 and S8.2-17 let a line record other than a line of its own: an object obtained as part of a package; a compiled copy, a generated list, and a package installed as a dependency of a recorded package; a default value obtained with a package.”

4. **Step 1: the first case is narrower than the supplement's.**
   Where: `SUP1/step-1.md`, “What is done”, “The first case examined is what a package creates by itself during installation: a default value covered by the line of the package.”
   Evidence: `SUPPLEMENT-1.md` step 1: “The first case: what a package creates by itself during installation.” A package's installation can create objects other than default values; the colon restricts the case to one kind.
   Minimal fix: replace with “The first case examined is what a package creates by itself during installation: every kind of object its installation creates, including a default value created during installation, which S8.2-17 covers by the line of the package.”

5. **Step 1: the two states are not tied to the moments to which the properties apply.**
   Where: `SUP1/step-1.md`, “What is done”, “or constructs two states of a computer under one declaration, both satisfying P1, P2 and P4,”.
   Evidence: S8.3-1: “The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.” `SUPPLEMENT-1.md`: “two different states”.
   Minimal fix: replace with “or constructs two different states of a computer under one declaration, each at a moment after a completed application of that declaration with no breaking (S8.3-1) and each satisfying P1, P2 and P4,”.

6. **Step 1: “with no machine” contradicts the observation the same paragraph allows.**
   Where: `SUP1/step-1.md`, “What is done”, first and last sentences.
   Evidence: “One party works by reasoning on the fixed text, with no machine.” and “only a fact that documentation does not settle is observed, once, with the expected result written first.”
   Minimal fix: replace “One party works by reasoning on the fixed text, with no machine.” with “One party works by reasoning on the fixed text; no machine is used except for the single observation of a fact allowed at the end of this paragraph.”

7. **Step 1: the question attributes to Section 8.4 what it does not say and names a narrower basis than “What is done”.**
   Where: `SUP1/step-1.md`, “Question”.
   Evidence: Section 8.4 lists the three consequences without naming P1, P2 or P4; “What is done” works from “the sentences of Sections 8.1–8.3”, the question from “the rules of Section 8.2”.
   Minimal fix: replace “Section 8.4 of the fourth paper names three consequences of the properties P1, P2 and P4: Understanding, Reproducibility and Removal. Does each of them follow from the three properties and the rules of Section 8.2?” with “Section 8.4 of the fourth paper names three consequences: Understanding, Reproducibility and Removal. Does each of them follow from the properties P1, P2 and P4 and the rules of Sections 8.1 and 8.2?”

8. **Both files: two rules of the supplement's rules line are missing.**
   Where: `SUP1/step-1.md` and `SUP1/step-3.md`, whole file.
   Evidence: `SUPPLEMENT-1.md`: “each case is attempted once; … gaps in the wording and gaps in the idea are reported in two separate lists.” Neither file says either; `PROTOCOL.md` Section 2: “The weight does not affect the outcome of a check.”
   Minimal fix: in each file, insert before “**Outcome.**” the paragraph “**Rules of Supplement 1.** Each case is attempted once. Every gap found is reported in one of two separate lists, gaps in the wording and gaps in the idea; the list does not affect the outcome.”

9. **Step 3: part (b) adds three events the supplement does not name.**
   Where: `SUP1/step-3.md`, “Question” (b), “What is done”, “Expected result” (b).
   Evidence: `SUPPLEMENT-1.md` step 3: “what is in force for a list taken from a server when there is no network.” The file adds “when the list changes at its source”, “when an entry is withdrawn”, “when the line is removed”, and its expectation counts “at least two of the four events”.
   Minimal fix: replace (b) of “Question” with “(b) For a line that takes a list from a server outside the declaration, does the text determine which state of the list must be in force when the computer has no network?”; replace “The events for (b): the four named in the question.” with “The event for (b): the computer has no network at a moment after a completed application.”; replace “(b) No sentence determines which state of an outside list is in force: at least two of the four events are undetermined.” with “(b) No sentence determines which state of an outside list is in force when the computer has no network: the event is undetermined.”

10. **Step 3: part (a) adds a case beyond “an ordinary update”.**
    Where: `SUP1/step-3.md`, “Question” (a) and “What is done”.
    Evidence: `SUPPLEMENT-1.md` step 3: “What must be true at each point of an ordinary update is written down”. The file widens this to “an ordinary change of the declaration and its application” and adds “two changes made at the same time”, which is not a point of one update. “success report” departs from S8.1-14 “reported as successful”.
    Minimal fix: replace “(a) During an ordinary change of the declaration and its application, does the text determine, for every moment, which declaration is in force and what must be true on the computer?” with “(a) At each point of an ordinary update, does the text determine which declaration is in force and what must be true on the computer?”; replace “The events for (a): an update that changes several objects; an update interrupted before its success report; two changes made at the same time.” with “The events for (a): an update that changes several objects; the same update interrupted before the system reports it as successful.”

11. **Step 3: no rule for a choice between two readings.**
    Where: `SUP1/step-3.md`, “What counts against the hypothesis”.
    Evidence: the task rule (Appendix A.4.1 as applied here): a choice between two readings belongs to the author. Step 1 records such a choice as a question for the author; step 3 says nothing, so the performing party would choose the reading that decides a moment.
    Minimal fix: after “A violation that only a particular implementation would show gives “?”.” add “Where whether a moment is determined depends on a choice between two readings of a sentence, the readings are recorded as a question for the author and that moment gives “?”.”

12. **Step 3: the quotation of S8.3-1 drops its condition.**
    Where: `SUP1/step-3.md`, “Question”, first sentence.
    Evidence: S8.3-1 ends “, provided there was no breaking.”; the file stops before it.
    Minimal fix: replace “The text says that the properties concern the computer at any moment after a completed application of the declaration.” with “The text says (S8.3-1): “The properties concern the computer at any moment after a completed application of the declaration, provided there was no breaking.””
