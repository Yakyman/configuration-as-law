VERDICT: DISAGREE

Review of `SUP1/step-8.md` (inputs of step 8 of Supplement 1, before publication). Sources read: (not published: orchestration or scratch),
`TEXT.md` Sections 8, 9 and Appendix A, `SENTENCES.md`, `PROTOCOL.md`, `SUP1/SUPPLEMENT-1.md`, `SUP1/step-5.md`,
`SUP1/step-6.md`, the first 14 lines of `S5/RECORD.md` and the first 3 lines of `check-inputs-v4/supplement-1/step-6-cases/B2/CASES-6.md`. No personal name,
host name, home path or name of a performer other than “party” was found in `SUP1/step-8.md`. The expected result is
worded as an expectation and decides no outcome. The combination of outcomes follows Appendix A.4.1.

1. **“What is known”: P1, P2 and P4 were not observed in the ordinary work.**
   Where: `SUP1/step-8.md` line 10. Evidence: `SUP1/step-5.md` line 45: “This step observes P1, P2 and P4 only in these
   sixteen ways”; the ordinary work is a separate case judged only on whether its actions succeed (line 70). The file
   says P1, P2 and P4 were observed “only in sixteen ways and in the ordinary work of one session”, which is stronger.
   Fix: replace “Step 5 observed P1, P2 and P4 on its image only in sixteen ways and in the ordinary work of one session
   (`SUP1/step-5.md`);” with “Step 5 observed P1, P2 and P4 on its image only in sixteen ways, and ordinary work only in
   one session (`SUP1/step-5.md`);”.

2. **“What is known”: “no command was refused” is not in the record.**
   Where: line 11. Evidence: `S5/RECORD.md` lines 10–11 say “Every case exited 0.” and “No way was refused.”; the first
   14 lines say nothing about every command. Fix: replace “in its record no command was refused,” with “in its record no
   way was refused and every case exited 0,”.

3. **“What is known”: “what a way saved” misstates the record.**
   Where: lines 11–12. Evidence: `S5/RECORD.md` lines 11–13: “the saved source was in the designated filesystem
   declaration, under a matching success report, before the way read it (cases 01, 05, 06: written by the way itself;
   other cases: written earlier by the ordinary account when the controller set up the fixture)”. In most cases the way
   saved nothing. Fix: replace “and what a way saved was found in the declaration before the way read it
   (`S5/RECORD.md`).” with “and the saved source that each way read was in the designated filesystem declaration,
   under a matching success report, before the way read it; only in cases 01, 05 and 06 had the way itself written it
   (`S5/RECORD.md`).”.

4. **“What is known”: the question for the author is not shown by the cited sources.**
   Where: lines 12–14. Evidence: neither `SUP1/step-5.md` (its only reading named is that of “saving and running a
   file”, line 59–60) nor the first 14 lines of `S5/RECORD.md` record a question on whether a declaration the system
   fills in is the primary description of Section 8.1 (S8.1-3); the record only names the file of questions (line 6).
   Fix: replace “Whether a declaration that the system itself fills in this way is the primary description of Section
   8.1 is a question recorded for the author in step 5; this step does not decide it.” with “Step 5 recorded questions
   for the author (`S5/RECORD.md`: “Questions for the author: `S5/QUESTIONS.md`”); this step decides none of them.”.

5. **Committed inputs omit the test declaration and the programs chosen.**
   Where: lines 17–19. Evidence: Appendix A.4.1: “Before the first observation of a check, its concrete inputs—the
   release numbers, the test declaration, the program chosen for each channel, and the ordinary actions with their exact
   commands—are committed”; `SUP1/step-6.md` line 17 and `SUP1/step-5.md` line 39 commit the declaration with its
   SHA-256. Step 8 commits neither the starting declaration nor the project, game, launcher and package used. Fix:
   replace “the image (SHA-256), the exact commands of every history and the observation queries are committed” with
   “the image (SHA-256), its declaration (full text and SHA-256), the project of history 2, the game and launcher of
   history 3, the package installed in history 4, the exact commands of every history and the observation queries are
   committed”.

6. **History 3 can be dropped without an attempt.**
   Where: lines 25–26. Evidence: Supplement 1 rules: “each case is attempted once”; the file does not say who finds
   that “no such launcher can run” or on what record, and the expected result (line 36) already anticipates that
   finding, so the preparing party could record the history as not performable without the second party's attempt.
   Fix: replace “If no such launcher can run on the image, the history is recorded as not performable.” with “Whether
   the committed launcher runs on the image is decided by the second party's single attempt with the committed
   commands; if it does not run, the history is recorded as not performable, with the output of that attempt.”.

7. **The way the network is lost is not fixed, and history 4 overlaps history 2.**
   Where: lines 27–28. Evidence: a network is a setting (S8.2-13); a disconnection made on the machine with a built-in
   tool is itself a change of a setting that must be recorded (S8.3-6, S8.3-7) or is breaking (S8.1-15), so the
   history would count against or be excluded by its own method. “During the development history” does not say whether
   history 2 itself is interrupted. Fix: replace item 4 with “4. Loss of network. The network is disconnected from
   outside the machine, without changing any setting on it, during an installation with the built-in tool and during a
   run of the development commands of history 2 within this history, and then restored the same way.”.

8. **Observations miss the moment of the loss of network.**
   Where: lines 30–31. Evidence: S8.3-1: “The properties concern the computer at any moment after a completed
   application of the declaration”; history 4 has no restart, so it is observed only at its end, after the network is
   back, and a state left by the interrupted installation that the restored network later completes or removes is never
   observed. Fix: replace “At the end of each history, and after each restart within it,” with “At the end of each
   history, after each restart within it, and in history 4 after each interrupted action and again after the network
   is restored,”.

9. **The P4 clause of the failure condition of Appendix A.4.3 is missing.**
   Where: lines 40–42. Evidence: Appendix A.4.3, failure condition for the properties: “a built-in tool, including
   with superuser privileges, changes such a thing past the declaration (P4)”. Histories 1 and 4 use the built-in tool;
   step 8 lists only what is in force at an observation. Fix: replace “is not recorded, and this is not breaking (P1,
   P4); a line” with “is not recorded, and this is not breaking (P1, P4); a built-in tool, including with superuser
   privileges, changes such a thing past the declaration (P4); a line”.

10. **The ordinary-work condition is not that of Appendix A.4.3, and counts the network loss itself.**
    Where: line 42. Evidence: Appendix A.4.3, failure condition for ordinary work: “An ordinary action from the list
    above cannot be performed through the declaration and its built-in tools.” Step 8 says “is impossible”; and in
    history 4 an installation that needs the network necessarily fails while it is disconnected, which by line 42 would
    count against the hypothesis. Fix: replace “or an ordinary action of a history is impossible.” with “or an ordinary
    action of a history cannot be performed through the declaration and its built-in tools (Appendix A.4.3); in history
    4, an action that needs the network counts only if it cannot be performed after the network is restored.”.

11. **No rule for an undecidable object or for a choice between two readings.**
    Where: lines 40–45. Evidence: Appendix A.4.1: “A counterexample to the definitions—an object for which the
    definitions do not allow deciding whether it must be recorded …—yields 0.” The first observation (line 31) decides
    every object in force; `SUP1/step-5.md` lines 58–60 and (not published: orchestration or scratch) give a choice between two readings to the author.
    Step 8 has neither rule. Fix: after “A history that cannot be performed gives “?”.” add “An object observed in force
    for which the text of Sections 8.1 and 8.2 does not allow deciding whether it must be recorded is a counterexample
    and yields 0 (Appendix A.4.1). Where a decision depends on a choice between two readings of a sentence, the readings
    are recorded as a question for the author and the history gives “?”.”.

12. **Breaking events are not set aside as Appendix A.4.1 requires.**
    Where: lines 40–45 and 52–54. Evidence: Appendix A.4.1: “Events recognized as breaking are excluded from the outcome
    and listed separately.” Step 8 uses “not breaking” but does not say breaking events are listed. Fix: before “This
    step observes four histories on one image;” add “Events recognized as breaking are excluded from the outcome and
    listed separately (Appendix A.4.1).”.
