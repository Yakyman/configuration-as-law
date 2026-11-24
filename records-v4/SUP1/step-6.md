# Supplement 1, step 6: reproducibility and removal, with additions

Recorded before the work on this step begins. Sentence numbers refer to `SENTENCES.md` in this folder; the other paths
are those of the records of the checks, relative to the folder of those records.

**Question.** On the testbed image of step 5: (a) does the same declaration give the same result on two independent
clean installations (check 3, Appendix A.4.4), also when two packages are installed in a different order; (b) after a
line is removed and the declaration is applied, is nothing that the line contributed in force unless the remaining
lines record it (the Removal part of check 2, Appendix A.4.3), also for an object contributed by two lines when the
last of them is removed?

**What is known before the work.** The record of the check 2 testbed gives its status as “partial” (`B2/STAND.md`). Step 1 of this supplement gave, by reasoning on the text: Understanding 0, Reproducibility “?”,
Removal “?” (`S1/ARGUMENT.md`). Step 5 fixed one final image and its complete declaration by their SHA-256 (`check-inputs-v4/supplement-1/step-5-cases/CASES-5.md`).

**What is done.** One party prepares, on the image of step 5, what the four cases below need — the packages, the
declaration lines and the exact commands — and the comparison of Appendix A.4.4 as a list of exact queries. Its own
trials are not attempts of a case. Before the second party's first attempt, the image (SHA-256), the declarations (full text and SHA-256), the packages chosen for each case and the lines removed in cases 3 and 4, the exact commands of every case and the list of comparison queries are committed to the records of the
checks. None of them changes after that. A second party, which did not prepare them, performs every case once on
fresh copies; another party reviews the record.

1. Reproducibility as Appendix A.4.4 states it: the same declaration, all of whose lines are unambiguous, is applied to two independent clean installations of the image on different virtual machines; what is in force under
   each line is compared as A.4.4 lists.
2. A different order. The same declaration contains two packages, each of which creates an account. It is applied to two independent clean installations of the image on different virtual machines with the two packages installed in opposite orders; the declaration last applied is byte-identical (same SHA-256) on both, and the way the order is produced is part of the committed commands, and the two accounts are compared as
   A.4.4 lists for an account. Twice: (2a) the lines state the numeric identifiers of the accounts; (2b) the lines do
   not state them. If the declaration format of the testbed does not admit a line without the identifier, 2b is
   recorded as not expressible on this testbed.
3. Removal as Appendix A.4.3 states it: the line of a program, of a service and of a rule is removed from the
   declaration; after application it is observed whether anything those lines contributed is in force, including whether the program’s former process runs and whether its executable can be started (Appendix A.4.3).
4. The last owner. One object is contributed by two lines (a package that two recorded packages require). The first
   of the two lines is removed and the declaration applied; then the second.

**Expected result, written before the work.** It is expected that case 1 and case 2a will show no difference; that in
case 2b the numeric identifiers of the two accounts will differ between the two installations, or the line will not
be expressible; that in case 3 nothing the removed lines contributed will be in force; and that in case 4 the object
will stay in force after the first removal, covered by the remaining line, and will not be in force after the second.
This expectation decides no outcome and is not a threshold.

**What counts against the hypothesis.** In cases 1, 2a and 2b: what is in force under the lines of the declaration
differs between the two installations and the difference is not explained by hardware (Appendix A.4.4). In cases 3
and 4: after application, something that a removed line contributed and that the remaining lines do not cover is in force (Appendix A.4.3). In case 4, after the first removal: the line of the remaining package is not in force as it requires, or the shared object it covers is not in force (P2, Appendix A.4.3). Such an observation yields 0 only with a written argument, from the definitions of Section 8
alone and checked by a separate review, that any system having P1, P2 and P4 would fail the same case; otherwise it is
a defect of the testbed and yields “?” (Appendix A.4.1). In case 2b a difference only in the numeric identifiers of the two accounts depends on what “unambiguous” in Section 8.4 requires of a line that does not state the identifier: the choice between the readings is recorded as a question for the author, and the case gives “?”; any other difference in case 2b counts as in cases 1 and 2a. A case that cannot be expressed or performed gives “?”.

**Rules of Supplement 1.** Each case is attempted once: by the second party; the preparing party's own trials are not
attempts of the case. Every gap found is reported together with the argument or the readings; whether gaps are put
into the two lists required by Supplement 1 is the question for the author recorded in `step-2.md`, and until the
author answers no gap is put into either list. The lists do not affect the outcome.

**Outcome.** For each case: 1 (nothing counts against the hypothesis in it), 0 or “?” as stated above. For the step: 0
if any case yields 0; otherwise “?” if any case yields “?”; otherwise 1. This step observes reproducibility and
removal only in these cases; its outcome is not the outcome of check 2 or of check 3.
