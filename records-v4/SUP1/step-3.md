# Supplement 1, step 3: the properties “at any moment”, and a line that takes a list from outside

Recorded before the work on this step begins. Sentence numbers refer to `SENTENCES.md` in this folder.

**Question.** The text says (S8.3-1): “The properties concern the computer at any moment after a completed application
of the declaration, provided there was no breaking.” (a) At each point of an ordinary update, does the text determine
which declaration is in force and what must be true on the computer? (b) For a line that takes a list from a server
outside the declaration, does the text determine which state of the list must be in force when the computer has no
network?

**What is done.** One party works by reasoning on the fixed text. For each event it writes the sequence of moments
and, for each moment, the sentence that determines the declaration in force and the required state, or records that no
sentence does. The events for (a): an update that changes several objects; the same update interrupted before the
system reports it as successful. The event for (b): the computer has no network at a moment after a completed
application. A fact about the behaviour of real systems is taken from documentation. Another party then tries to
refute each recorded undetermined moment, and each argument of incompatibility, with the text read literally.

**Expected result, written before the work.** (a) The text determines the declaration in force at every moment (the
declaration of the last application that the system reported as successful, S8.1-14), and during a change that is not
made as one indivisible step there is at least one moment at which the state required by that declaration does not
hold. Whether such a moment gives 0 or “?” is not settled here; it is decided by the rules under “What counts against
the hypothesis”. (b) No sentence determines which state of an outside list is in force when the computer has no
network: the event is undetermined.

**What counts against the hypothesis.** A moment for which the text does not determine what must be true, surviving
refutation; or a written argument, surviving refutation, that P1, P2 and P4 cannot hold together at some moment of an
ordinary update whatever the system does. A violation that only a particular implementation would show gives “?”.
Where whether a moment is determined depends on a choice between two readings of a sentence, the readings are recorded
as a question for the author and that moment gives “?”.

**Rules of Supplement 1.** Each case is attempted once. Every gap found is reported in one of two separate lists, gaps
in the wording and gaps in the idea; the list does not affect the outcome.

**Outcome.** For (a) and for (b) separately: 1, 0 or “?”.
