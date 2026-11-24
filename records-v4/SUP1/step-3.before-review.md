# Supplement 1, step 3: the properties “at any moment”, and a line that takes a list from outside

Recorded before the work on this step begins.

**Question.** The text says that the properties concern the computer at any moment after a completed application of
the declaration. (a) During an ordinary change of the declaration and its application, does the text determine, for
every moment, which declaration is in force and what must be true on the computer? (b) For a line that takes a list
from outside the declaration, does the text determine which state of the list must be in force: when the list changes
at its source, when the computer has no network, when an entry is withdrawn, when the line is removed?

**What is done.** One party works by reasoning on the fixed text. For each ordinary event it writes the sequence of
moments and, for each moment, the sentence that determines the declaration in force and the required state, or records
that no sentence does. The events for (a): an update that changes several objects; an update interrupted before its
success report; two changes made at the same time. The events for (b): the four named in the question. A fact about
the behaviour of real systems is taken from documentation. Another party then tries to refute each recorded
undetermined moment, and each argument of incompatibility, with the text read literally.

**Expected result, written before the work.** (a) The text determines the declaration in force at every moment (the
last application reported as successful), and during a change that is not made as one indivisible step there is at
least one moment at which the state required by that declaration does not hold. Whether a system can make every change
indivisible is a design matter outside the definition; such a moment therefore gives “?”, not 0. (b) No sentence
determines which state of an outside list is in force: at least two of the four events are undetermined.

**What counts against the hypothesis.** A moment for which the text does not determine what must be true, surviving
refutation; or a written argument, surviving refutation, that P1, P2 and P4 cannot hold together at some moment of an
ordinary change whatever the system does. A violation that only a particular implementation would show gives “?”.

**Outcome.** For (a) and for (b) separately: 1, 0 or “?”.
