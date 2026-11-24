# Supplement 1, step 2: disputed cases with complete facts

Recorded before the work on this step begins. Sentence numbers refer to `SENTENCES.md` in this folder.

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

1. Facts. For each family one party takes every example object named in the first night's records of that family and
   collects every fact that the four questions and the clarifications of Section 8.2 ask about. Facts come from the
   first night's inventories and logs and from documentation. A fact that none of them holds is observed once on a
   fresh machine of the same committed installation, with the expected result written first; such an observation
   receives a new name, and the earlier records are not changed.
2. Decisions. Two parties, separately, without seeing each other's work or any decision of the first night, decide
   each example object from the facts: the first question answered “yes”, the sentence that decides, and whether the
   object must be recorded; or that no sentence decides; or that two sentences decide differently.
3. A third party adjudicates every difference between the two.
4. Agreements. A sample of 300 objects of check 1 and 300 objects of the lived-in machines on which the two
   classifications of the first night gave the same decision (not a gap, a mixed group or an unknown fact), drawn by the script (not published: orchestration or scratch) in this folder (seed
   20261123, in proportion to the kinds of objects). Two parties, separately, state for each sampled object whether
   the agreed decision follows from a sentence of the text read literally.

**Expected result, written before the work.** With complete facts, families 1, 3, 5 and 11 still receive two
decisions or none. Families 7, 9 and 13 receive two decisions under which the declaration is the same. At most 20 of
the 600 sampled agreements do not follow from a sentence.

**What counts against the hypothesis.** An example object whose deciding facts are all known and which, after
adjudication, receives two decisions or none. A sampled agreement that both parties find not to follow from any
sentence is adjudicated and counted in the same way. An object for which a deciding fact remains unknown gives “?”.
Where the decision depends on a choice between two readings of a sentence, the readings are recorded as a question for
the author, and the object counts as receiving two decisions.

**Rules of Supplement 1.** Each case is attempted once. Every gap found is reported in one of two separate lists, gaps
in the wording and gaps in the idea; the list does not affect the outcome.

**Outcome.** For each family: 1 (every example object receives one decision), 0 (an example object with all deciding
facts known receives two decisions or none), or “?” (otherwise). For the sample: the number of agreements that do not
follow from a sentence, and the families they form.
