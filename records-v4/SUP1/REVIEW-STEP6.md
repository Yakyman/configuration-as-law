VERDICT: DISAGREE

Review of `SUP1/step-6.md` (inputs of Supplement 1, step 6) against `SUP1/SUPPLEMENT-1.md` (step 6 and the rules
line), the paragraphs “Rules of Supplement 1” of `SUP1/step-5.md` and `SUP1/step-2.md`, `TEXT.md` Section 8.4,
Sections 9.3–9.4 and Appendix A.4.1, A.4.3, A.4.4, `SENTENCES.md` and `PROTOCOL.md`. Data read: only the first line of
`S1/ARGUMENT.md`, the first 12 lines of `B2/STAND.md` and the first 5 lines of `check-inputs-v4/supplement-1/step-5-cases/CASES-5.md`. Paths below are
relative to the night folder. Checked and found in order: the four cases are A.4.4 (case 1), A.4.3 Removal (case 3)
and exactly the two additions the supplement names (case 2, different order; case 4, last owner); the expected result
is worded as an expectation and states that it decides no outcome; the rules paragraph agrees with those of steps 5
and 2; the outcome combination follows A.4.1; performers are named only as “party”; no personal name, host name or home
path; no personal provenance is included; the file contains no result numbers to check against data.

1. **“What is known”: two statements not shown by `B2/STAND.md`.** Where: `SUP1/step-6.md` line 12–13. Evidence: the
   first 12 lines of `B2/STAND.md` say “STAND: partial” (line 1) and “Public commitment and separate replay/review remain
   pending; the hypothesis/step outcome is `?`” (line 7); they do not say that the testbed “was not accepted” and say
   nothing about check 3 or about checks 2 and 3 not having been conducted. Minimal fix: replace
   “Checks 2 and 3 of the plan have not been conducted: the testbed was not accepted (`B2/STAND.md`).” with
   “The record of the check 2 testbed gives its status as “partial” (`B2/STAND.md`).”

2. **“What is known”: a statement about step 1 not shown by `S1/ARGUMENT.md`.** Where: line 14–15. Evidence: the first
   line of `S1/ARGUMENT.md` is “STEP 1: Understanding 0; Reproducibility ?; Removal ?”; it says nothing about a pair of
   states, accounts, numeric identifiers or installation order. Minimal fix: delete
   “; its pair of states differs in the numeric identifiers of two accounts created by two packages installed in a
   different order” so that the sentence ends “… Removal “?” (`S1/ARGUMENT.md`).”

3. **“What is known”: “sealed” is not the word of the source.** Where: line 15. Evidence: `check-inputs-v4/supplement-1/step-5-cases/CASES-5.md` lines 1–4:
   “frozen second-party cases”, “Final image SHA-256: …”, “Final complete declaration SHA-256: …”; “sealed” does not
   occur. Minimal fix: replace “Step 5 produced one sealed image (`check-inputs-v4/supplement-1/step-5-cases/CASES-5.md`).” with
   “Step 5 fixed one final image and its complete declaration by their SHA-256 (`check-inputs-v4/supplement-1/step-5-cases/CASES-5.md`).”

4. **Case 1 replaces the condition of A.4.4 with a different one.** Where: line 24. Evidence: A.4.4 applies “the same
   declaration, all of whose lines are unambiguous”; Section 8.4 claims reproducibility “provided the description is
   unambiguous”. The file substitutes “every line of which states its values”, which decides by itself what
   “unambiguous” requires — the very reading the file elsewhere (line 48–50) leaves to the author. Minimal fix: replace
   “the same declaration, every line of which states its values, is applied” with
   “the same declaration, all of whose lines are unambiguous, is applied”.

5. **Case 2 does not fix independence and leaves open whether the declaration stays the same.** Where: lines 27–29.
   Evidence: A.4.4 requires “two independent clean installations … on different virtual machines”; case 2 says only
   “two clean installations”. It also does not say how the opposite order is produced; if it is produced by reordering
   lines, the two installations no longer receive “the same declaration” (A.4.4, Section 8.4). Minimal fix: replace
   “It is applied to two clean installations with the two packages installed in opposite orders” with
   “It is applied to two independent clean installations of the image on different virtual machines with the two
   packages installed in opposite orders; the declaration last applied is byte-identical (same SHA-256) on both, and
   the way the order is produced is part of the committed commands”.

6. **Case 3 is weaker than A.4.3.** Where: lines 32–33. Evidence: A.4.3 Removal: “it is checked that nothing the line
   contributed is in force—the program’s former process does not run, and its executable cannot be started.” The file
   omits both named checks. Minimal fix: replace
   “after application it is observed whether anything those lines contributed is in force.” with
   “after application it is observed whether anything those lines contributed is in force, including whether the
   program’s former process runs and whether its executable can be started (Appendix A.4.3).”

7. **Case 4: what counts against omits the P2 comparison of A.4.3, so the first half of the case cannot count.** Where:
   lines 34–35 and 45–46. Evidence: A.4.3 Procedure: “After each completed application, every line of the declaration
   is compared with the state it requires”; failure condition: “after a completed application, at least one line is
   not fulfilled (P2)”. S8.2-16 makes the remaining recorded package’s line cover the shared dependency. As written,
   if the shared object disappears after the first removal, nothing counts against, although the file itself expects it
   to stay (line 39–40). Minimal fix: after “is in force (Appendix A.4.3).” insert
   “In case 4, after the first removal: the line of the remaining package is not in force as it requires, or the shared
   object it covers is not in force (P2, Appendix A.4.3).”

8. **Case 2b: the “?” rule is broader than the reading question it rests on, and rests on a record not verified.**
   Where: lines 48–50. Evidence: the reading of “unambiguous” (Section 8.4) concerns only a line that does not state the
   identifier, yet the sentence gives “?” for any difference in 2b — including differences in groups, shell or home
   directory, which A.4.4 compares and which do not depend on that reading. The claim that the readings “are those
   recorded as a question for the author in step 1” is not shown by the first line of `S1/ARGUMENT.md`; `SUP1/step-1.md`
   records it only as an expectation (“becomes a question for the author”). Minimal fix: replace
   “In case 2b a difference depends on what “unambiguous” in Section 8.4 requires of a line that does not state the
   identifier: the two readings are those recorded as a question for the author in step 1, and the case gives “?”.” with
   “In case 2b a difference only in the numeric identifiers of the two accounts depends on what “unambiguous” in
   Section 8.4 requires of a line that does not state the identifier: the choice between the readings is recorded as a
   question for the author, and the case gives “?”; any other difference in case 2b counts as in cases 1 and 2a.”

9. **Committed inputs: the declarations are committed only as checksums.** Where: line 19–20. Evidence: A.4.1:
   “its concrete inputs—the release numbers, the test declaration, the program chosen for each channel, and the
   ordinary actions with their exact commands—are committed to the repository of check records.” “the declarations
   (SHA-256)” can be read as committing only their checksums, and the chosen packages and removed lines are not named
   as inputs. Minimal fix: replace “the declarations (SHA-256),” with
   “the declarations (full text and SHA-256), the packages chosen for each case and the lines removed in cases 3 and 4,”.
