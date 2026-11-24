# Supplement 1, step 8: wider and longer ordinary work

Recorded before the work on this step begins. Sentence numbers refer to `SENTENCES.md` in this folder; the other paths
are those of the records of the checks, relative to the folder of those records.

**Question.** On the final image of step 6, during ordinary work that lasts longer than one session — updates,
development, games, loss of network — does anything come to be in force that must be recorded and is not recorded,
does every line of the declaration stay fulfilled, and does the work stay possible?

**What is known before the work.** Step 5 observed P1, P2 and P4 on its image only in sixteen ways, and ordinary work only in one session (`SUP1/step-5.md`); in its record no way was refused and every case exited 0, and the saved source that each way read was in the designated filesystem declaration, under a matching success report, before the way read it; only in cases 01, 05 and 06 had the way itself written it (`S5/RECORD.md`). Step 5 recorded questions for the author (`S5/RECORD.md`: “Questions for the author: `S5/QUESTIONS.md`”); this step decides none of them. Step 6 fixed one final image by its SHA-256 (`check-inputs-v4/supplement-1/step-6-cases/B2/CASES-6.md`).

**What is done.** One party prepares, on the final image of step 6, four histories with their exact commands, and the
queries of the observations below. Its own trials are not attempts of a history. Before the second party's first
attempt, the image (SHA-256), its declaration (full text and SHA-256), the project of history 2, the game and launcher of history 3, the package installed in history 4, the exact commands of every history and the observation queries are committed to the
records of the checks. None of them changes after that. A second party, which did not prepare them, performs every
history once on a fresh copy; another party reviews the record.

1. Updates. The system is updated twice with its built-in tool, with a restart after each update.
2. Development. A project is fetched, built and run; its source is changed, and it is built and run again; three
   times in a row.
3. A game. A game is installed and started by a launcher that downloads the game and updates itself. Whether the committed launcher runs on the image is decided by the second party's single attempt with the committed commands; if it does not run, the history is recorded as not performable, with the output of that attempt.
4. Loss of network. The network is disconnected from outside the machine, without changing any setting on it, during an installation with the built-in tool and during a run of the development commands of history 2 within this history, and then restored the same way.

At the end of each history, after each restart within it, and in history 4 after each interrupted action and again after the network is restored, three observations are made with the committed
queries: every installed object and every setting in force is compared with the declaration in force; every line of
the declaration is compared with the state it requires; and each ordinary action of the history is recorded as done
or not done.

**Expected result, written before the work.** It is expected that in the histories that can be performed nothing in
force will be found unrecorded and every line will be fulfilled; that the game history will not be performable on
the image; and that the declaration will grow with every file a history saves. This expectation decides no outcome
and is not a threshold.

**What counts against the hypothesis.** After a completed application: something installed or a setting is in force,
must be recorded, is not recorded, and this is not breaking (P1, P4); a built-in tool, including with superuser privileges, changes such a thing past the declaration (P4); a line of the declaration is not fulfilled
(P2); or an ordinary action of a history cannot be performed through the declaration and its built-in tools (Appendix A.4.3); in history 4, an action that needs the network counts only if it cannot be performed after the network is restored. Such an observation yields 0 only with a written argument,
from the definitions of Section 8 alone and checked by a separate review, that any system having P1, P2 and P4 would
fail the same history; otherwise it is a defect of the testbed and yields “?” (Appendix A.4.1). A history that cannot be performed gives “?”. An object observed in force for which the text of Sections 8.1 and 8.2 does not allow deciding whether it must be recorded is a counterexample and yields 0 (Appendix A.4.1). Where a decision depends on a choice between two readings of a sentence, the readings are recorded as a question for the author and the history gives “?”.

**Rules of Supplement 1.** Each history is attempted once: by the second party; the preparing party's own trials are
not attempts. Every gap found is reported together with the argument or the readings; whether gaps are put into the
two lists required by Supplement 1 is the question for the author recorded in `step-2.md`, and until the author
answers no gap is put into either list. The lists do not affect the outcome.

**Outcome.** For each history: 1 (nothing counts against the hypothesis in it), 0 or “?” as stated above. For the
step: 0 if any history yields 0; otherwise “?” if any history yields “?”; otherwise 1. Events recognized as breaking are excluded from the outcome and listed separately (Appendix A.4.1). This step observes four histories on one image; its outcome states nothing about other work, other systems, or longer use.
