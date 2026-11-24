# Supplement 1, step 7: a check of the checks themselves

Recorded before the work on this step begins. The other paths are those of the records of the checks, relative to the
folder of those records.

**Question.** Supplement 1 asks that the way of telling a real gap from a far-fetched one be tried on cases known to
be right and cases known to be wrong. Supplement 1 does not name the way. This step reads it as the weighting of
Section 2 of `PROTOCOL.md`; the other reading is the procedure of Section 3 (a gap stands only if a second party,
deciding the object by the text, names no sentence that decides it). The choice between the two readings is the
author's; this step runs under the first reading, and its outcome holds only for it. Under the first reading: a gap is
a gap in the wording when two parties, asked separately “must this be in the declaration, if the declaration describes
everything installed and every setting”, give the same answer, and a system can meet this requirement without
forbidding any ordinary action from the list in Section 9.2; everything else is a gap in the idea. On cases whose
answer is known, does this way give the known answer?

**The cases with a known answer.** The ten gaps of Part I named in the table of Section 8.6 of the fourth paper. For
each, the table states how version 4 resolves it; that resolution is the known answer to the first question. The
cases as the parties see them are in `step-7-inputs/CASES.md`; the known answers and their opposites are fixed in the
script `step-7-inputs/s7_pairs.py`, which also fixes the order of the pairs (seed 20261123), and in
`step-7-inputs/key/KEY.tsv`.

| No. | Case (Section 8.6) | Known answer (Section 8.6) | Opposite answer |
|---|---|---|---|
| 1 | Shared content or capability (fonts, translations, themes) | recorded: by a line of its own or as a dependency of a recorded package | need not be recorded |
| 2 | Lookup tables | the same | need not be recorded |
| 3 | Packages containing only dependencies | recorded: an installed object | need not be recorded |
| 4 | Support for absent hardware | recorded: an installed object, obtained as part of a package or image | need not be recorded |
| 5 | Objects that the system recreates | no line of its own: exists only while the computer runs, or is built by the system from what is recorded | a line of its own |
| 6 | A system service setting | recorded: a setting | need not be recorded |
| 7 | A compiled copy of code | recorded: covered by the line of the original package | need not be recorded |
| 8 | A program's history that the program executes as code | recorded: a line of its own | need not be recorded |
| 9 | A record that a service was enabled in the past | need not be recorded: a program record | a line of its own |
| 10 | A browser extension | recorded: an installed object | need not be recorded |

**What is known before the work.** The calibration of Section 4 of `PROTOCOL.md` did not pass: two of its eight cases
received a different decision (`W0/RESULT.md`). The weighting done afterwards, outside the published order, put two of
its gaps (G1 and G2) among the gaps in the idea because the answers of the two parties differed on two objects of ten
and on two objects of nine; in no gap did a party answer that an ordinary action would have to be forbidden
(`W1/RESULT.md`).

**What is done.**

1. Two parties, separately, are given Sections 8.1–8.5 of the fourth paper without Section 8.6
   (`step-7-inputs/TEXT-8.1-8.5.md`), the ten cases (`step-7-inputs/CASES.md`) and the list of ordinary actions of
   Section 9.2 (`step-7-inputs/ACTIONS-9.2.md`). For each case each party answers the two questions of Section 2 of
   `PROTOCOL.md`: the first with “yes, by a line of its own”, “yes, covered by another line” (naming it) or “no”; the
   second with “yes” or “no” (naming the action). Neither sees the other's answers, Section 8.6, this file,
   `step-7-inputs/PAIRS.tsv`, `step-7-inputs/s7_pairs.py`, `step-7-inputs/key/`, or any earlier record about these
   cases.
2. A third party, which sees neither Section 8.6, nor this file, nor `step-7-inputs/s7_pairs.py`, nor
   `step-7-inputs/key/`, nor the answers of part 1, is given the same sections and cases and the twenty pairs of a case
   and an answer (`step-7-inputs/PAIRS.tsv`): the ten known answers and the ten opposite ones, in the fixed order and
   without their labels. For each pair it says whether the answer is what the definition of Sections 8.1–8.5 means for
   that case.

A party's answer to the first question equals the known answer when its yes or no is that of the table and, for yes,
the line it names is one that the resolution of the table allows; where the resolution names no line (cases 3, 4, 6
and 10), any yes equals the known answer; in case 5, when it requires no line of its own.

**Expected result, written before the work.** It is expected that in part 1 the two parties will give the same answer
in at least eight cases of ten, and that in at least seven this answer will be the known one; and that in part 2 the
third party will accept at least eight of the ten known answers and reject at least eight of the ten opposite ones.
This expectation decides no outcome and is not a threshold.

**What counts against the way.** In part 1: a case in which the two parties give the same answer and it is not the
known one — the first sign is then established for an answer the author does not hold; or a case in which they give
different answers (a case for which a party gives no answer is not counted as different answers) — the way then sorts
into the gaps in the idea a case whose answer is known. Part 2 is not the way of Section 2 of `PROTOCOL.md` (one party
judges given answers), so nothing in it counts for or against the way; its numbers are reported as they are. The
published text names no case known to be wrong for this way; that half of step 7 is not attempted here and is reported
as not attempted. What counts here counts against the way of sorting, not against the hypothesis; no outcome of a
check or of another step changes.

**Rules of Supplement 1.** Each case is attempted once by each party. The work of each party is checked by another
party. No gap is put into a list of gaps in the wording or gaps in the idea in this step.

**Outcome.** For the way of sorting: 0 if something counts against it in part 1, with the cases; otherwise 1 if both
parties answered every case, and “?” if not, with the cases left without an answer.
