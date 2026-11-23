# Supplement 1, step 5: one system in which the properties and ordinary work hold together

Recorded before the work on this step begins, except for the build of the check 2 testbed, which began during the
first night and was running when Supplement 1 was published. Sentence numbers refer to `SENTENCES.md` in this folder;
the other paths are those of the records of the checks, relative to the folder of those records.

**Question.** Can one system keep P1, P2 and P4 and at the same time let a person do the ordinary work that step 5
of Supplement 1 names, taken from the list of check 2 (Appendix A.4.3 of the fourth paper with the additions of
Section 9.3): a command shell with commands typed freely, one's own script recorded in the declaration, packages, a
network, a browser, documents? Updating the system, connecting to a Wi-Fi network on real hardware and pairing a
Bluetooth device, which Appendix A.4.3 also lists, are not part of this step.

**What is known before the work.** The first build round of the check 2 testbed closed 2 of the 65 ways past the
declaration assigned to it (`B2/BUILD-1.md`). In fifteen of its observations, saved code that the declaration does
not cover still executed; the record of the round names these “saved uncovered script, sourced, piped, imported,
serialized, startup, editor, JIT and custom-dispatch inputs” (`B2/BUILD-1.md`). In the list `all_false_observations`
of `B2/raw/round-1/metrics.json` they are named SAVED-SCRIPT, SAVED-PIPE, SAVED-SOURCE, STARTUP-ENV, PYTHON-IMPORT,
PICKLE-CODE, DIRECT-REDIRECT-STDIN, DIRECT-PROC-FD, DIRECT-READ-EXEC, DIRECT-AWK-FILE, DIRECT-SCRIPT-HELPER,
RC-STARTUP, EDITOR-SAVED-COMMANDS, JIT-SAVED-INPUT and DISPATCHER-SAVED. In one further observation,
root-native-account-bypass, the system's own account administration, run with superuser privileges, bypassed the
declaration (`B2/BUILD-1.md`: “Canonical native root account administration also bypasses the declaration”).

**What is done.** One party brings the testbed to a single image on which three things are observed together.

1. Each of the fifteen ways and the account tool is tried again on a fresh copy of the image, by the same commands as
   in the first build round.
2. For each way, the corresponding permitted action is performed: the same code, recorded in the declaration, is run
   in the same way; for the account tool, the same change made through the tool is written into the declaration and
   applied.
3. The ordinary work is done on the same image in one session: free commands in the shell with a pipeline and a
   redirection; running one's own script recorded in the declaration; installing a program with the package manager;
   connecting to a network; opening a page in the browser; creating and editing a document.

A way together with its permitted action is one case; the ordinary work is one more case: seventeen cases. A second
party, which did not build the image, performs every case once on a fresh copy; another party reviews the record. For
a way that the image does not refuse, the building party writes either the mechanism by which another system having
P1, P2 and P4 could keep the way from launching what is not recorded while leaving its permitted action and the
ordinary work possible, or an argument, from the definitions of Section 8 alone, that no system having P1, P2 and P4
can leave them possible. Before the second party's first attempt, the image (SHA-256), its declaration (SHA-256) and
the exact commands of every way, every permitted action and every ordinary action are committed to the records of the
checks; the commands of the ways are those of `B2/raw/round-1/final-2/shell.jsonl`,
`B2/raw/round-1/final-2/tools.jsonl`, `B2/raw/round-1/final-2/supplement/direct.jsonl` and
`B2/raw/round-1/final-2/supplement/extra.jsonl`. None of them changes after that.

This step observes P1, P2 and P4 only in these sixteen ways; its outcome states nothing about any other way of
check 2.

**Expected result, written before the work.** It is expected that the ways in which a saved file is started as a
program, sourced or used as a startup file will be refused while the recorded script runs; and that for at least one
way in which a typed command makes a recorded interpreter read saved text and evaluate it, no mechanism will be found
that refuses it and leaves free commands in the shell possible, so that the step ends with a written argument about
that way. This expectation decides no outcome and is not a threshold.

**What counts against the hypothesis.** A case in which its permitted action or an ordinary action of the list is
impossible in any system having P1, P2 and P4, so that any such system would fail the same case, shown by a written
argument from the definitions of Section 8 alone and checked by a separate review, yields 0 (Appendix A.4.1). A way
that this image fails to refuse, a permitted action that fails on it, or an ordinary action that it fails to allow,
without such an argument, is a defect of the testbed and yields “?”. Where the argument depends on a choice between
two readings of a sentence — in particular, of what “saving and running a file” in Section 9.3 covers when a person
types the command each time — the readings are recorded as a question for the author and the case gives “?”.

**Rules of Supplement 1.** Each case is attempted once: by the second party, on the final image; the building party's
own trials during the build are not attempts of the case. Every gap found is reported together with the argument or
the readings; whether gaps are put into the two lists required by Supplement 1 is the question for the author
recorded in `step-2.md`, and until the author answers no gap is put into either list. The lists do not affect the
outcome.

**Outcome.** For the case of a way: 1 if the way launches nothing that must be recorded and is not recorded (it is
refused, or what it leaves is recorded in the declaration) and its permitted action succeeds; for the case of the
ordinary work: 1 if every action of item 3 succeeds on the same image; otherwise 0 or “?” as stated under “What
counts against the hypothesis”. For the step: 0 if any case yields 0; otherwise “?” if any case yields “?”; otherwise
1.
