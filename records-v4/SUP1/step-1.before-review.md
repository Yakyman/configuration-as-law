# Supplement 1, step 1: whether the consequences follow from the properties

Recorded before the work on this step begins.

**Question.** Section 8.4 of the fourth paper names three consequences of the properties P1, P2 and P4:
Understanding, Reproducibility and Removal. Does each of them follow from the three properties and the rules of
Section 8.2?

**What is done.** One party works by reasoning on the fixed text, with no machine. From the sentences of Sections
8.1–8.3 it writes out when an object must be recorded, which line covers it, and what a line requires. For each
consequence it either derives the consequence from these, or constructs two states of a computer under one
declaration, both satisfying P1, P2 and P4, in which the consequence as worded in Section 8.4 is false. The first case
examined is what a package creates by itself during installation: a default value covered by the line of the package.
After it, every other kind of object that the rules let a line cover without stating its value. A fact about the
behaviour of an ordinary system is taken from its documentation; only a fact that documentation does not settle is
observed, once, with the expected result written first.

Another party then tries to refute each constructed pair of states with the sentences of the text read literally, and
to break each derivation.

**Expected result, written before the work.** Understanding does not follow for default values created during
installation: at least one pair of states is constructed and survives refutation. Removal follows from P1 wherever the
remaining lines cover nothing of what the removed line contributed. Reproducibility holds for what a line determines;
whether that is all Section 8.4 claims depends on the reading of “unambiguous” and becomes a question for the author.

**What counts against the hypothesis.** Two states that satisfy P1, P2 and P4 under one declaration, survive
refutation, and in which a consequence as worded in Section 8.4 is false; or a consequence whose derivation needs a
premise that the text does not contain. A dispute about the reading of a sentence is recorded as a question for the
author and gives “?”.

**Outcome.** For each of the three consequences: 1 (it follows), 0 (it does not follow), or “?” (it depends on a
reading that only the author can choose).
