VERDICT: DISAGREE

Review of `SUP1/step-5.md` (inputs of step 5 of Supplement 1, before the work begins), checked against
`SUP1/SUPPLEMENT-1.md`, `SUP1/step-2.md`, `TEXT.md` Sections 8–9 and Appendix A, `SENTENCES.md`, `PROTOCOL.md`,
`B2/BUILD-1.md` and the list `all_false_observations` in `B2/raw/round-1/metrics.json`. Verified as correct and not
listed below: the sixteen identifiers and their order (the list has 16 entries: the fifteen named saved-code
observations and `root-native-account-bypass`; per `B2/BUILD-1.md` six + five + four saved-code failures and one
account bypass, 16 of 157); “2 of the 65” (`B2/BUILD-1.md`: “Scope: exactly Round 1's 65 variants”, “C5.4 and C10.4
are CLOSED”); seventeen cases (16 + 1); the expected result is worded as an expectation and decides no outcome; the
step combination rule matches Appendix A.4.1; the “Rules of Supplement 1” paragraph agrees with that of `step-2.md`;
every performer is named only as a “party”; no personal name, host name or home path.

1. **Ordinary-work list goes beyond Appendix A.4.3 and Section 9.3, and leaves out the recorded script.**
   Where: “What is done”, item 3. Evidence: A.4.3 lists “installing a program, updating the system, connecting to a
   Wi-Fi network, pairing a Bluetooth device, working in a browser, editing documents”; Section 9.3 adds “running
   ordinary commands and one’s own script, recorded in the declaration, in the command shell”. “Running a container”
   and “removing a program” are in neither list (containers appear only as a channel in A.4.3 and as an action before
   the inventory in A.4.2/9.2), nor in step 5 of `SUPPLEMENT-1.md`; one’s own recorded script, named by both 9.3 and
   the supplement, is missing. Fix: replace item 3 with
   “3. The ordinary work is done on the same image in one session: free commands in the shell with a pipeline and a
   redirection; running one's own script recorded in the declaration; installing a program with the package manager;
   connecting to a network; opening a page in the browser; creating and editing a document.”

2. **The question attributes the supplement’s shorter list to check 2.** Where: “Question”. Evidence: check 2
   (A.4.3) also names updating the system, a Wi-Fi network on real hardware and pairing a Bluetooth device; the six
   items quoted are those of step 5 of `SUPPLEMENT-1.md`. Fix: replace the paragraph with
   “**Question.** Can one system keep P1, P2 and P4 and at the same time let a person do the ordinary work that step 5
   of Supplement 1 names, taken from the list of check 2 (Appendix A.4.3 of the fourth paper with the additions of
   Section 9.3): a command shell with commands typed freely, one's own script recorded in the declaration, packages, a
   network, a browser, documents? Updating the system, connecting to a Wi-Fi network on real hardware and pairing a
   Bluetooth device, which Appendix A.4.3 also lists, are not part of this step.”

3. **The condition for 0 is reinterpreted.** Where: “What counts against the hypothesis”, first two sentences.
   Evidence: A.4.1: a testbed failure yields 0 only if the argument shows “that any system having the property would
   fail the same case; a separate review checks the argument”. The file quantifies over “every system that refuses
   the way” instead of every system having the properties (S8.3-7 lets a system keep P4 by recording a change in the
   declaration, not only by refusing it), and replaces the separate review by “the attempt of another party to refute
   it”. A failed permitted action (P2, S8.3-5) is not covered. Fix: replace the two sentences with
   “A case in which its permitted action or an ordinary action of the list is impossible in any system having P1, P2
   and P4, so that any such system would fail the same case, shown by a written argument from the definitions of
   Section 8 alone and checked by a separate review, yields 0 (Appendix A.4.1). A way that this image fails to refuse,
   a permitted action that fails on it, or an ordinary action that it fails to allow, without such an argument, is a
   defect of the testbed and yields “?”.”

4. **The mechanism-or-argument requirement uses the same narrowed quantifier.** Where: “What is done”, last sentence.
   Evidence: as in finding 3 (A.4.1, S8.3-7). Fix: replace with
   “For a way that the image does not refuse, the building party writes either the mechanism by which another system
   having P1, P2 and P4 could keep the way from launching what is not recorded while leaving its permitted action and
   the ordinary work possible, or an argument, from the definitions of Section 8 alone, that no system having P1, P2
   and P4 can leave them possible.”

5. **The outcome rule is stronger than the failure condition and does not fit the ordinary-work case.** Where:
   “Outcome”, first sentence. Evidence: A.4.3’s failure condition is that a channel “installs, launches, or changes
   something that must be recorded although it is not recorded”; “the way is refused” excludes recording (S8.3-7). The
   condition “the way is refused, its permitted action succeeds” has no meaning for case 17, and 0 and “?” are not
   tied to their conditions. Fix: replace the first sentence with
   “**Outcome.** For the case of a way: 1 if the way launches nothing that must be recorded and is not recorded (it is
   refused, or what it leaves is recorded in the declaration) and its permitted action succeeds; for the case of the
   ordinary work: 1 if every action of item 3 succeeds on the same image; otherwise 0 or “?” as stated under “What
   counts against the hypothesis”.”

6. **Concrete inputs are not fixed before the first observation.** Where: “What is done”. Evidence: A.4.1: “Before
   the first observation of a check, its concrete inputs—… the test declaration, … and the ordinary actions with their
   exact commands—are committed”; `SUPPLEMENT-1.md`: “the inputs and the expected result are recorded before the first
   observation”. The image and its declaration do not exist yet, and “the same commands as in the first build round”
   are not located. Fix: append to the paragraph after item 3
   “Before the second party's first attempt, the image (SHA-256), its declaration (SHA-256) and the exact commands of
   every way, every permitted action and every ordinary action are committed to the records of the checks; the
   commands of the ways are those of `B2/raw/round-1/final-2/shell.jsonl`, (not published: direct evidence at least 2 MB),
   `B2/raw/round-1/final-2/supplement/direct.jsonl` and `B2/raw/round-1/final-2/supplement/extra.jsonl`. None of
   them changes after that.”

7. **Parts of “What is known” are not shown by the two sources and the build record is not cited.** Where: “What is
   known before the work”. Evidence: `B2/BUILD-1.md` says only “Saved uncovered script, sourced, piped, imported,
   serialized, startup, editor, JIT and custom-dispatch inputs can still execute” and “Canonical native root account
   administration also bypasses the declaration”; the list holds only identifiers, files and `false_fields`. “Redirected
   into an interpreter”, “loaded by a recorded program” and “read and evaluated at a typed command” are read from the
   identifiers, not stated by either source; “closed 2 of the 65” has no citation. Fix: replace the paragraph with
   “**What is known before the work.** The first build round of the check 2 testbed closed 2 of the 65 ways past the
   declaration assigned to it (`B2/BUILD-1.md`). In fifteen of its observations, saved code that the declaration does
   not cover still executed; the record of the round names these “saved uncovered script, sourced, piped, imported,
   serialized, startup, editor, JIT and custom-dispatch inputs” (`B2/BUILD-1.md`). In the list `all_false_observations`
   of `B2/raw/round-1/metrics.json` they are named SAVED-SCRIPT, SAVED-PIPE, SAVED-SOURCE, STARTUP-ENV, PYTHON-IMPORT,
   PICKLE-CODE, DIRECT-REDIRECT-STDIN, DIRECT-PROC-FD, DIRECT-READ-EXEC, DIRECT-AWK-FILE, DIRECT-SCRIPT-HELPER,
   RC-STARTUP, EDITOR-SAVED-COMMANDS, JIT-SAVED-INPUT and DISPATCHER-SAVED. In one further observation,
   root-native-account-bypass, the system's own account administration, run with superuser privileges, bypassed the
   declaration (`B2/BUILD-1.md`: “Canonical native root account administration also bypasses the declaration”).”

8. **The question claims more than the cases observe.** Where: “Question” and “What is done”. Evidence: the cases
   observe P1, P2 and P4 only in the sixteen ways of the list; `B2/BUILD-1.md` leaves 86 of 88 variants not closed,
   and checking them all is check 2 (Section 9.3, A.4.3), not this step. Without a limit, outcome 1 would read as “one
   system keeps P1, P2 and P4”. Fix: append to “What is done”, after the paragraph on the seventeen cases,
   “This step observes P1, P2 and P4 only in these sixteen ways; its outcome states nothing about any other way of
   check 2.”
