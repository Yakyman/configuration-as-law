# Supplement 1, step 2: disputed cases with complete facts

Recorded before the work on this step begins. Sentence numbers refer to `SENTENCES.md` in this folder; the other
paths are those of the records of the checks, relative to the folder of those records.

**Question.** For each family of disagreements found during the first night: when every fact on which the decision
depends is known, does the text of Sections 8.1 and 8.2 give the objects of the family one decision — what the object
is and whether it must be recorded? And do the decisions on which the two classifications of the first night agreed
follow from the text?

**The families.** Fifteen, fixed here.

From check 1, the five cards of its adjudication: (1) a default value created during installation that no person of
the computer chose; (2) a list the system generated from installed packages; (3) files left from an earlier version of
a package that is still installed; (4) a stored archive whose contents are executed; (5) a package of a program's
built-in installer whose code runs only inside that program.

From the lived-in machines, the seven cards of their adjudication: (6) files that a self-managing client installs and
deletes for itself; (7) repository history fetched at a person's command; (8) container images and containers; (9)
package contents held in an installer's cache; (10) code that an installed program copies or generates as it runs;
(11) values the computer obeys that a program generated rather than a person chose; (12) value files whose entries
include commands that are run.

From the channels, the three families of the revised gap analysis: (13) a browser's home page and “launches
something”; (14) a compiler or a build tool as a built-in tool or as general-purpose work; (15) saved history as
values read or as executable statements.

**What is done.**

1. Facts. For each family one party takes every example object named in the card of that family
   (`D1/adjudication/HOLES.md` cards 1–5, `A3/adjudication/HOLES.md` cards 1–7, the three sections of
   `B1/fix-b1-1/GAPS.md`) and collects every fact that the four questions and the clarifications of Section 8.2 ask
   about. Facts come from the first night's inventories and logs and from documentation. A fact that none of them
   holds is observed once on a fresh machine of the same committed installation, with the expected result written
   first; such an observation receives a new name, and the earlier records are not changed. The facts are written
   without any decision, reading or sentence that the first night's records assign to the object.
2. Decisions. Two parties, separately, without seeing each other's work or any decision of the first night, decide
   each example object from the facts: the first question answered “yes” (or S8.2-4 or S8.2-5 where it decides before
   the questions), the sentence that decides, and whether the object must be recorded; or that no sentence decides; or
   that two sentences decide differently. Each party then answers for each example object, also separately, the two
   questions by which Section 2 of `PROTOCOL.md` defines a gap in the wording: “must this be in the declaration, if
   the declaration describes everything installed and every setting”, and whether a system can meet this requirement
   without forbidding any ordinary action from the list in Section 9.2.
3. A third party adjudicates every difference between the two.
4. Agreements. A sample of 300 objects of check 1 and 300 objects of the lived-in machines on which the two
   classifications of the first night gave the same decision (not a gap, a mixed group or an unknown fact), drawn by
   the script `s2_sample.py` published with this file (seed 20261123, in proportion to the kinds of objects), run with
   Python 3.14.10 on the comparison tables of the first night `D1/compare/joined.tsv` (check 1; SHA-256
   a0921b413f92a0f5163aa94434ab7711f94905d63de7e7ecbb2490ca09e0216d) and `A3/compare/joined.tsv` (the lived-in
   machines; SHA-256 b23d7175dcd25a9f41ac070cd3eba95347d96da6bd76e43ec1aec7e29ba405c4). Two parties, separately, state
   for each sampled object whether the agreed decision follows from a sentence of the text read literally. A third
   party adjudicates every sampled agreement that either party finds not to follow from a sentence. For each sampled
   agreement that goes to adjudication, each party also answers, separately, the two questions of part 2.

**Expected result, written before the work on this step and after the outcome of check 1 was known.** It is
expected that, with complete facts, families 2, 3, 4, 5, 11 and 12 will still receive two decisions or none; that
family 1 will receive one decision; that family 7 will receive two decisions under which the declaration is the same;
and that at most 20 of the 600 sampled agreements will not follow from a sentence. This expectation decides no outcome
and is not a threshold.

**What counts against the hypothesis.** An example object whose deciding facts are all known and which receives two
decisions or none, from both parties or after adjudication of their difference. A sampled agreement that either party
finds not to follow from any sentence is adjudicated, and counted in the same way. An object for which a deciding fact
remains unknown gives “?”. Where the decision depends on a choice between two readings of a sentence, the readings are
recorded as a question for the author, and the object counts as receiving two decisions.

**Rules of Supplement 1.** Each case is attempted once. Every gap found is reported together with both parties'
answers to the two questions of part 2, and the answers are published. Section 4 of `PROTOCOL.md` says that weighting
does not begin if one of its cases receives a different decision, and its calibration did not pass (two of the eight
cases received a different decision). Whether the two lists required by Supplement 1, gaps in the wording and gaps in
the idea, are nevertheless made by the signs of Section 2 of `PROTOCOL.md` is recorded before the work as a question
for the author. Until the author answers, no gap is put into either list. The lists do not affect the outcome.

**Outcome.** For each family: 1 (every example object receives one decision), 0 (an example object with all deciding
facts known receives two decisions or none), or “?” (otherwise). For the sample: 1, 0 or “?” by the same rule, applied
to the sampled agreements; and the number of agreements that do not follow from a sentence, and the families they
form.
