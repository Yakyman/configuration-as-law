# Supplement 1, step 4: the facts missing after the first night

Recorded before the work on this step begins. Sentence numbers refer to `SENTENCES.md` in this folder; the other paths
are those of the records of the checks, relative to the folder of those records.

**Question.** With the facts that the inventories of the first night did not hold, does the text of Sections 8.1 and
8.2 decide the objects whose decision depended on those facts, and the objects of Gentoo, from which no inventory was
obtained?

**What is known before the work.** Check 1 gave 0 for AlmaLinux, Void Linux and openSUSE MicroOS and “?” for Gentoo
and Talos Linux (`D1/RESULT.md`). The Gentoo machine did not start, and nothing was observed on it
(`D1/in/READY.md`). On the four other machines 937 objects were left with an unknown deciding fact — AlmaLinux 65,
Void Linux 75, openSUSE MicroOS 754, Talos Linux 43 (`D1/review/unknown-rows.tsv`) — 1,069 further objects of Void
Linux depend on facts about files left from an earlier version of a package, and one further object of AlmaLinux on
the contents and use of compiled values; 2,007 objects in all (`D1/RESULT.md`).

**What is done.**

1. One party lists every missing deciding fact that the result of check 1 names, grouped by what kept the collector
   from recording it, and extends the collector of check 1 so that it records these facts. The extended collector is
   rehearsed on throwaway copies of the machines; the output of a rehearsal is not an observation, and no decision
   about an object is taken from it.
2. Before the first observation, the extended collector, its exact commands, the list of facts it is to record and
   the rule by which an object of a new inventory is matched to an object that the first night left with an unknown
   fact are committed to the records of the checks. None of them changes after that.
3. On fresh machines of the same committed installations as in check 1 — the five systems, after the same ordinary
   actions with the same commands — the extended collector is run once per machine. The new inventories receive the
   name `D1b`; the inventories, decisions and outcomes of the first night are not changed. For Gentoo this is its
   first inventory. The matching rule is applied by a party that does not decide; an object of the first night with no
   match in its new inventory is listed by its id, receives no decision in this step, and is reported with the
   outcome.
4. Two parties, separately and without seeing each other's work, the output of a rehearsal, or any earlier decision
   about the same objects, of the first night or of another step of this supplement, and without taking part in parts
   1–3, decide every object of the new inventories for which the first night left an unknown fact, and every object of
   Gentoo: the first question answered “yes” (or S8.2-4 or S8.2-5 where it decides before the questions), the sentence
   that decides, whether the object must be recorded and by which line; or that no sentence decides; or that two
   sentences decide differently. A third party adjudicates every difference between the two. For each object that a
   party finds to receive two decisions or none, that party also answers, separately, the two questions by which
   Section 2 of `PROTOCOL.md` defines a gap in the wording.

**Expected result, written before the work.** It is expected that an inventory of Gentoo will be obtained; that at
least half of the 937 objects will receive a decision once their fact is known; and that at least one kind of object
not met in the first night — among what a system that builds its programs from source leaves on the disk — will
receive two decisions or none. This expectation decides no outcome and is not a threshold.

**What counts against the hypothesis.** An object of a new inventory whose deciding facts are all known and which
receives two decisions or none from both parties; or an object on which the two parties decided differently and the
adjudication finds no sentence of the text that resolves the difference (Section 9.2; Appendix A.4.1). Otherwise, an
object for which a deciding fact is still unknown gives “?” (Section 9.6). A machine whose second-level inventory is
not obtained cannot give 1: it gives 0 if an object that counts against the hypothesis is found on it, and “?”
otherwise (Section 9.2); where the second level is obtained only in part, the outcome is reported under both readings
A and B recorded in `C1/QUESTIONS.md`. Where the decision depends on a choice between two readings of a sentence, the
readings are recorded as a question for the author, and the object counts as receiving two decisions.

**Rules of Supplement 1.** Each case is attempted once: each machine is started once for its new inventory, and a
command that fails is recorded and not repaired. Every gap found is reported together with the sentences, the readings
and both parties' answers to these two questions, and the answers are published; whether gaps are put into the two
lists required by Supplement 1 is the question for the author recorded in `step-2.md`, and until the author answers no
gap is put into either list. The lists do not affect the outcome. The work of each of parts 1–3 is checked by a party
that did not perform it.

**Outcome.** For each of the five machines, under the name `D1b`, for the objects decided in this step: 1 (every such
object receives one decision), 0 (an object meets the condition above that counts against the hypothesis), or “?”
(otherwise); the five are combined by the rule of Appendix A.4.1. For AlmaLinux, Void Linux, openSUSE MicroOS and
Talos Linux this outcome does not cover the objects of the new inventories that are not decided in this step. These
outcomes are reported separately; the outcome of check 1 remains the one obtained in the first night.
