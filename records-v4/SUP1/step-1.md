# Supplement 1, step 1: whether the consequences follow from the properties

Recorded before the work on this step begins. Sentence numbers refer to `SENTENCES.md` in this folder.

**Question.** Section 8.4 of the fourth paper names three consequences: Understanding, Reproducibility and Removal.
Does each of them follow from the properties P1, P2 and P4 and the rules of Sections 8.1 and 8.2?

**What is done.** One party works by reasoning on the fixed text; no machine is used except for the single
observation of a fact allowed at the end of this paragraph. From the sentences of Sections 8.1–8.3 it writes out when
an object must be recorded, which line covers it, and what a line requires. For each consequence it either derives
the consequence from these, or constructs two different states of a computer under one declaration, each at a moment
after a completed application of that declaration with no breaking (S8.3-1) and each satisfying P1, P2 and P4, in
which the consequence as worded in Section 8.4 is false. The first case examined is what a package creates by itself
during installation: every kind of object its installation creates, including a default value created during
installation, which S8.2-17 covers by the line of the package. After it, every other kind of object that S8.2-16 and
S8.2-17 let a line record other than a line of its own: an object obtained as part of a package; a compiled copy, a
generated list, and a package installed as a dependency of a recorded package; a default value obtained with a
package. A fact about the behaviour of an ordinary system is taken from its documentation; only a fact that
documentation does not settle is observed, once, with the expected result written first.

Another party then tries to refute each constructed pair of states with the sentences of the text read literally, and
to break each derivation.

**Expected result, written before the work.** Understanding does not follow for default values created during
installation: at least one pair of states is constructed and survives refutation. Removal follows from P1 wherever the
remaining lines cover nothing of what the removed line contributed. Reproducibility holds for what a line determines;
whether that is all Section 8.4 claims depends on the reading of “unambiguous” and becomes a question for the author.

**What counts against the hypothesis.** Two states as described under “What is done”, that survive refutation and in
which a consequence as worded in Section 8.4 is false. A premise that a derivation needs and the text does not contain
is recorded as a finding; it counts against the hypothesis only through such a pair of states. Where whether a
consequence follows depends on a choice between two readings of a sentence, the readings are recorded as a question
for the author and the consequence gives “?”.

**Rules of Supplement 1.** Each case is attempted once. Every gap found is reported in one of two separate lists, gaps
in the wording and gaps in the idea; the list does not affect the outcome.

**Outcome.** For each of the three consequences: 1 (a derivation survives the attempt to break it), 0 (a pair of
states counting against the hypothesis survives refutation), or “?” (neither; or it depends on a reading that only the
author can choose).
