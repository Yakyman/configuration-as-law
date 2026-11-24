VERDICT: DISAGREE

Review of the inputs of step 7 of Supplement 1: `SUP1/step-7.md` with `S7/CASES.md`, `S7/PAIRS.tsv`, (not published: record outside selected evidence),
(not published: record outside selected evidence), `S7/TEXT-8.1-8.5.md`, `S7/ACTIONS-9.2.md`. Read against `SUP1/SUPPLEMENT-1.md` (step 7 and the rules
line), `PROTOCOL.md` Sections 2–4, `TEXT.md` Section 8 (table of 8.6) and Section 9.2 with `SENTENCES.md`, the first
line of `W0/RESULT.md`, the first 45 lines of `W1/RESULT.md`, and the descriptions of the gaps in Part I of the fourth
paper (Section 3, Section 4.1 items 1–5, Section 4.5).

Checked and found correct, no change needed:
- (not published: record outside selected evidence) run twice into two empty folders: the two outputs are byte-identical, and identical to `S7/CASES.md`,
  `S7/PAIRS.tsv`, (not published: record outside selected evidence). (not published: orchestration or scratch) is byte-identical to (not published: record outside selected evidence). The temporary folders
  were deleted.
- `S7/TEXT-8.1-8.5.md` is byte-identical to lines 5–109 of `TEXT.md` (Section 8 heading through the end of 8.5) and
  contains nothing of Section 8.6.
- `S7/ACTIONS-9.2.md`: the quotation equals the list of ordinary actions of `TEXT.md` Section 9.2 word for word.
- `SUP1/step-7.md`, lines 8–10: the quotation of the two signs equals `PROTOCOL.md` Section 2 word for word.
- "What is known before the work": "two of its eight cases" matches `W0/RESULT.md` line 1 ("CALIBRATION: FAILED 2 of
  8"); "differed on two objects of ten and on two objects of nine" matches `W1/RESULT.md` (G1 "same on 8, different on
  2" of 10; G2 "same on 7, different on 2" of 9) and the columns m1_meaning/m2_meaning of `W1/j/compare.tsv`; "in no
  gap did a party answer that an ordinary action would have to be forbidden" matches the column "Both said: can be
  met" (yes in every gap) and m1_achievable/m2_achievable (all "yes" for G1, G2).
- The step-7 table: the known answers of cases 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 agree with the rows of the table of
  Section 8.6; every opposite answer is the opposite about recording.
- The pairs of (not published: record outside selected evidence) give each case exactly one known and one opposite pair; pairs 1, 2, 7, 8, 9, 10, 11,
  12, 14, 16, 17, 18, 19, 20 carry the answers of the step-7 table.
- The expected result is worded as an expectation and says it decides no outcome. No personal name, host name, home
  path or name of a performer other than "party" occurs in the seven files.

## Findings

1. **The way is fixed by a reading the published text does not make.**
   Where: `SUP1/step-7.md`, line 7 ("The way is that of Section 2 of `PROTOCOL.md`: …").
   Evidence: `SUP1/SUPPLEMENT-1.md` step 7 says only "the way of telling a real gap from a far-fetched one" and names
   no section. `PROTOCOL.md` holds two candidates: Section 2 (weight: gap in the wording or gap in the idea — both are
   gaps) and Section 3 (whether a gap stands at all: "If a sentence is named and it decides the object unambiguously,
   there is no gap"), which Section 4 already tries on cases with a known decision. (not published: orchestration or scratch): "any choice between two
   readings of it … is never decided by you: write it down in plain words with the readings".
   Minimal fix: replace "The way is that of Section 2 of `PROTOCOL.md`:" with "Supplement 1 does not name the way. This
   step reads it as the weighting of Section 2 of `PROTOCOL.md`; the other reading is the procedure of Section 3 (a gap
   stands only if a second party, deciding the object by the text, names no sentence that decides it). The choice
   between the two readings is the author's; this step runs under the first reading, and its outcome holds only for it.
   Under the first reading:".

2. **`S7/CASES.md` states the resolutions of Section 8.6 for eight of the ten cases.**
   Where: `S7/CASES.md` items 1, 2, 4, 6, 7, 8, 9, 10, and the same strings in the list `CASES` of (not published: record outside selected evidence).
   Evidence: neither the left column of 8.6 nor Part I says these words; the right column of 8.6 and the questions of
   8.2 do. "obtained with a package" (1, 2) and "obtained as part of a package or of an image" (4) are question 1
   (S8.2-7) and the resolution "Obtained as part of a package or image"; "chosen by a person, that the computer as a
   whole obeys" (6) is question 3 (S8.2-11) and the resolution of row 6; "that the system built from an installed
   package" (7) is the resolution "A program that the system built from what is recorded" (Part I says "a compiled copy
   of code that a program recreates itself"); "the system did not build it from anything recorded" (8) is the
   resolution "it was not built from what is recorded"; "written by a program as it ran" (9) is question 4 (S8.2-15)
   and the resolution "Recorded by a program as it ran"; "with the installer built into the browser" (10) is the
   resolution "An installer built into the browser installs and removes it".
   Minimal fix: in (not published: record outside selected evidence) set the descriptions to the following and regenerate (the order of the pairs does
   not depend on the descriptions):
   1 "A font, a translation or a theme shared by many programs."
   2 "Terminal descriptions and character tables."
   4 "Firmware for a device that is absent and boot files for another hypervisor."
   6 "A setting of a system service."
   7 "A compiled copy of code that a program recreates itself."
   8 "A history file of a program that the program executes as code."
   9 "A record that a service was enabled at some time in the past."
   10 "A browser extension that a person installed."
   Cases 3 and 5 stay as they are.

3. **Four known answers in `S7/PAIRS.tsv` say more than the table.**
   Where: `S7/PAIRS.tsv` pairs 3 (case 3), 13 (case 4), 5 (case 6), 15 (case 5); (not published: record outside selected evidence) list `CASES`.
   Evidence: step-7 table and Section 8.6 name no line for cases 3 ("recorded: an installed object"), 4 ("recorded: an
   installed object, obtained as part of a package or image") and 6 ("recorded: a setting"), but the pairs name lines
   ("by a line of its own, or as a dependency of a recorded package"; "covered by the line of the package or image it
   was obtained with"; "by a line of its own"). For case 5 the table says "no line of its own"; the pair adds "and the
   line it is built from covers it" and restates the 8.6 resolution, which `S7/CASES.md` withholds.
   Minimal fix: in (not published: record outside selected evidence) set the known answer of case 3, case 4 and case 6 to "It must be recorded." and of
   case 5 to "It needs no line of its own."; regenerate.

4. **The rule for comparing a named line is undefined where the table names no line.**
   Where: `SUP1/step-7.md` line 56.
   Evidence: "for yes, the line it names is one that the resolution of the table allows" — the resolutions of cases 3,
   4, 6 and 10 name no line, so whether "yes, by a line of its own" or "yes, covered by another line" equals the known
   answer would be decided after the answers are seen.
   Minimal fix: after "one that the resolution of the table allows;" insert "where the resolution names no line (cases
   3, 4, 6 and 10), any yes equals the known answer;".

5. **The parties are not barred from the files that hold the known answers and the labels.**
   Where: `SUP1/step-7.md`, part 1 (lines 41–45) and part 2 (line 46).
   Evidence: `step-7-inputs/s7_pairs.py` and `step-7-inputs/PAIRS.tsv` contain all known answers; `key/KEY.tsv` and the
   script contain the labels; all are published in the same folder as the inputs. Part 1 bars only "the other's
   answers, Section 8.6, this file, or any earlier record"; part 2 bars only "Section 8.6, … this file, … the answers of
   part 1". Part 1 also does not name the file of ordinary actions.
   Minimal fix: part 1 — "the list of ordinary actions of Section 9.2 (`step-7-inputs/ACTIONS-9.2.md`)" and "Neither sees
   the other's answers, Section 8.6, this file, `step-7-inputs/PAIRS.tsv`, `step-7-inputs/s7_pairs.py`,
   `step-7-inputs/key/`, or any earlier record about these cases."; part 2 — "which sees neither Section 8.6, nor this
   file, nor `step-7-inputs/s7_pairs.py`, nor `step-7-inputs/key/`, nor the answers of part 1".

6. **Part 2 does not apply the way, yet its results count against the way.**
   Where: `SUP1/step-7.md`, "What counts against the way" (line 67–68) and "Outcome" (line 74).
   Evidence: the way that line 7 names needs two parties answering separately and compares their answers (`PROTOCOL.md`
   Section 2). In part 2 one party judges given answers; neither Supplement 1 nor `PROTOCOL.md` makes such a judgement
   part of the way. Counting "an opposite answer accepted, or a known answer rejected" against the way is a rule not in
   the text. The ten cases of 8.6 are all cases whose answer is known to be right; the published text names no case
   known to be wrong for this way, and the step does not say so.
   Minimal fix: replace "In part 2: an opposite answer accepted, or a known answer rejected." with "Part 2 is not the way
   of Section 2 of `PROTOCOL.md` (one party judges given answers), so nothing in it counts for or against the way; its
   numbers are reported as they are. The published text names no case known to be wrong for this way; that half of step
   7 is not attempted here and is reported as not attempted."; in "Outcome" replace "in parts 1 and 2" with "in part 1".

7. **Part 3 is outside step 7 and counts alternative rules for the first sign.**
   Where: `SUP1/step-7.md`, "What is done" item 3 (lines 50–54), the last clause of the expected result (lines 61–63),
   "Part 3 is a count, and nothing in it counts for or against." (line 68), "The numbers of part 3 are reported as they
   are." (line 75).
   Evidence: step 7 of Supplement 1 tries the way on cases with a known answer; the gaps of `W1/`, `W2/`, `S2/` are not
   such cases. Counting how the sorting changes under two other ways of counting is a trial of rules that are not
   published; `PROTOCOL.md` Section 6: "the procedure of Section 3 [is] not changed after publication"; (not published: orchestration or scratch): "Do
   not add experiments" and "do not propose a fix".
   Minimal fix: delete item 3 and the three sentences named above; end the expected result with "… reject at least eight
   of the ten opposite ones. This expectation decides no outcome and is not a threshold."

8. **No "?" is defined: a missing answer would count as 0.**
   Where: `SUP1/step-7.md`, "What counts against the way" and "Outcome".
   Evidence: `SUP1/SUPPLEMENT-1.md` rules line: "the outcome is 1, 0 or “?”"; (not published: orchestration or scratch): "? (data insufficient)". As
   written, a case for which a party gives no answer is "a case in which they give different answers" and yields 0.
   Minimal fix: after "or a case in which they give different answers" insert "(a case for which a party gives no answer
   is not counted as different answers)"; replace the outcome sentence with "For the way of sorting: 0 if something
   counts against it in part 1, with the cases; otherwise 1 if both parties answered every case, and “?” if not, with
   the cases left without an answer."

9. **"Two gaps of check 1" is not stated by the cited result files.**
   Where: `SUP1/step-7.md` line 34.
   Evidence: the first 45 lines of `W1/RESULT.md` name the two gaps G1 and G2 by their sources (`D1/RESULT.md`, cards 2
   and 4) and never say "check 1" of them; `W0/RESULT.md` line 1 says nothing about them.
   Minimal fix: replace "put two gaps of check 1 among the gaps in the idea" with "put two of its gaps (G1 and G2) among
   the gaps in the idea".
