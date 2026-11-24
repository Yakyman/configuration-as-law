VERDICT: DISAGREE

Review of `SUP1/step-4.md` (inputs of step 4 of Supplement 1, recorded before the work), read against `SUP1/SUPPLEMENT-1.md` (step 4 and the rules line), `SUP1/step-2.md` ("Rules of Supplement 1"), `TEXT.md` Sections 8, 9.2, 9.6 and Appendix A.4.1–A.4.2, `SENTENCES.md` (identical to `SUP1/SENTENCES.md`), `PROTOCOL.md`, the first 100 lines of `D1/RESULT.md`, the first 25 lines of `D1/in/READY.md`, and the row count per machine of `D1/review/unknown-rows.tsv`. Paths below are relative to the night folder.

Verified true, no change needed: check 1 gave 0 for AlmaLinux, Void Linux and openSUSE MicroOS and "?" for Gentoo and Talos Linux under both readings (`D1/RESULT.md` lines 13–18); the Gentoo machine did not start and actions and collection were not attempted (`D1/in/READY.md` line 19); `D1/review/unknown-rows.tsv` has 937 data rows, by machine column and by id prefix alike AlmaLinux 65, Void Linux 75, openSUSE MicroOS 754, Talos Linux 43 (`D1/RESULT.md` line 66 gives 937); the 1,069 Void Linux rows of card 3 (`D1/RESULT.md` line 91). The expected result is worded as an expectation and states that it decides no outcome. Performers are named only as "party"; no personal name, host name or home path appears. S8.2-4 and S8.2-5 are cited correctly.

1. **The outcome claims more than the step decides.**
   Where: `SUP1/step-4.md` lines 50–52.
   Evidence: part 4 (lines 28–29) decides only the objects for which the first night left an unknown fact, plus every Gentoo object. Section 9.2 gives a machine its outcome by the objects found on it, and each object is decided twice. So a 1 "by the failure condition of Section 9.2" for AlmaLinux, Void Linux, MicroOS or Talos Linux would cover objects nobody decided in this step. That includes the confirmed generated-list, archive and contained-code gaps (`D1/RESULT.md` lines 55–57). The same kinds of object are expected again on fresh machines of the same installations. The combination by Appendix A.4.1 carries the same overstatement into the result for the five machines together.
   Fix: replace lines 50–52 with:
   "**Outcome.** For each of the five machines, under the name `D1b`, for the objects decided in this step: 1 (every such object receives one decision), 0 (an object meets the condition above that counts against the hypothesis), or “?” (otherwise); the five are combined by the rule of Appendix A.4.1. For AlmaLinux, Void Linux, openSUSE MicroOS and Talos Linux this outcome does not cover the objects of the new inventories that are not decided in this step. These outcomes are reported separately; the outcome of check 1 remains the one obtained in the first night."

2. **The condition that counts against narrows Section 9.2, cites the wrong section and leaves the partial second level open.**
   Where: lines 39–43.
   Evidence:
   - Section 9.2 has two failure clauses. The second one ("or the two classifications decided differently and the adjudication finds no sentence of the text that resolves the dispute") and Appendix A.4.1 ("if no sentence resolves it, the case yields 0") are not conditional on all facts being known. Line 39 makes both clauses conditional on "whose deciding facts are all known". `D1/RESULT.md` line 13 applies the text as "Missing facts do not override a failure".
   - The rule that an object with an unknown fact gives "?" comes from Section 9.6, not Section 9.2.
   - Section 9.2 gives a machine without a second-level inventory "0 if an object meeting the failure condition below is found on it, and ? otherwise". Line 42 says only "cannot give 1".
   - Two of the machines had a partial second level, and check 1 reported its outcome under readings A and B (`D1/RESULT.md` lines 3, 9). The step-4 file says nothing about which reading applies, which leaves the choice of reading to the performer.
   Fix: replace lines 39–43 with:
   "**What counts against the hypothesis.** An object of a new inventory whose deciding facts are all known and which receives two decisions or none from both parties; or an object on which the two parties decided differently and the adjudication finds no sentence of the text that resolves the difference (Section 9.2; Appendix A.4.1). Otherwise, an object for which a deciding fact is still unknown gives “?” (Section 9.6). A machine whose second-level inventory is not obtained cannot give 1: it gives 0 if an object that counts against the hypothesis is found on it, and “?” otherwise (Section 9.2); where the second level is obtained only in part, the outcome is reported under both readings A and B recorded in `check-inputs-v4/QUESTIONS.md`. Where the decision depends on a choice between two readings of a sentence, the readings are recorded as a question for the author, and the object counts as receiving two decisions."

3. **The decision leaves out "by which line".**
   Where: lines 30–31.
   Evidence: Section 9.2, Procedure: "whether the object must be recorded and by which line". Card 2, one of the confirmed gaps of check 1, concerns exactly the line (S8.2-16; `D1/RESULT.md` lines 95–99). Part 4 asks only "whether the object must be recorded". That is weaker than the procedure the outcome invokes.
   Fix: in line 31, replace "and whether the object must be recorded;" with "whether the object must be recorded and by which line;".

4. **Independence is weaker than the common rules.**
   Where: line 28.
   Evidence: the common rules state that "a classification never reads the other classification, an adjudication or any earlier classification of the same objects". The Void card-3 objects are also the example objects of family 3 of step 2 (`SUP1/step-2.md` line 14), so a step-2 decision would be an earlier classification of the same objects. Line 28 excludes only "the decisions of the first night". Nothing in the file stops a party of part 4 from taking part in part 1. In part 1 the party reads the result of check 1, whose missing-fact entries carry first-night readings (`D1/review/unknown-rows.tsv`, column `missing_facts`, e.g. "Listed as an installed package (Q1)"). Nothing stops a deciding party from seeing rehearsal output either.
   Fix: in line 28, replace "without seeing each other's work or the decisions of the first night," with "without seeing each other's work, the output of a rehearsal, or any earlier decision about the same objects, of the first night or of another step of this supplement, and without taking part in parts 1–3,".

5. **The selection of the objects to decide is not fixed before the observation.**
   Where: lines 22–23 and 28–29.
   Evidence: the rules line of Supplement 1 says "the inputs and the expected result are recorded before the first observation". The objects to decide are "every object of the new inventories for which the first night left an unknown fact". They lie on fresh machines, and the deciding parties may not see the first night's decisions. The file does not say how a new object is matched to a first-night object, who applies the match, or what happens to a first-night object that has no match.
   Fix: in line 22, replace "the extended collector, its exact commands and the list of facts it is to record are" with "the extended collector, its exact commands, the list of facts it is to record and the rule by which an object of a new inventory is matched to an object that the first night left with an unknown fact are". After "For Gentoo this is its first inventory." (line 27), add: "The matching rule is applied by a party that does not decide; an object of the first night with no match in its new inventory is listed by its id, receives no decision in this step, and is reported with the outcome."

6. **No check of a performer's work by another party for parts 1–3.**
   Where: lines 45–48.
   Evidence: the rules line of `SUP1/SUPPLEMENT-1.md` (line 33) says "the work of a performer is checked by another party". Part 4 gives the decisions an adjudication. Nothing provides a check of the fact list, the collector extension or the runs.
   Fix: at the end of line 48, after "The lists do not affect the outcome.", add: "The work of each of parts 1–3 is checked by a party that did not perform it."

7. **The answers needed for the two lists are not collected.**
   Where: lines 28–32 and 46–48.
   Evidence: in `SUP1/step-2.md` (lines 40–43, 67–68), each party answers separately the two questions of Section 2 of `PROTOCOL.md`, and every gap is reported with those answers. That keeps the two lists possible if the author answers the recorded question with "yes". Step 4 collects no answers. A later "yes" could not be applied to its gaps, because `PROTOCOL.md` Section 3 requires answers given separately. This is weaker than the rules line, under which gaps "are reported in two separate lists".
   Fix: at the end of part 4 (line 32), add: "For each object that a party finds to receive two decisions or none, that party also answers, separately, the two questions by which Section 2 of `PROTOCOL.md` defines a gap in the wording." In line 46, replace "Every gap found is reported together with the sentences and the readings;" with "Every gap found is reported together with the sentences, the readings and both parties' answers to these two questions, and the answers are published;".

8. **"What is known" leaves out one object with an unknown fact.**
   Where: lines 13–14.
   Evidence: `D1/RESULT.md` line 91 also adds one AlmaLinux row, `alma-caff428f8364f0a663721a85`, whose compiled values' "contents and use are needed". It gives the union as "2,007 rows". Part 1 lists "every missing deciding fact that the result of check 1 names", so this object is in scope, but the record of what is known leaves it out.
   Fix: replace "— and 1,069 further objects of Void Linux depend on facts about files left from an earlier version of a package (`D1/RESULT.md`)." with "— 1,069 further objects of Void Linux depend on facts about files left from an earlier version of a package, and one further object of AlmaLinux on the contents and use of compiled values; 2,007 objects in all (`D1/RESULT.md`)."
