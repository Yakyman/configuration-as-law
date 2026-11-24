VERDICT: DISAGREE

Review of `SUP1/SUPPLEMENT-1.md` as a translation of `SUP1/supplement-1-ru.md`, sentence by sentence, against `TEXT.md` Sections 8–9 and Appendix A, `SENTENCES.md` and `PROTOCOL.md`. Reviewed 2026-11-23 UTC.

Checked without finding: every Russian sentence has an English counterpart and no English sentence lacks a Russian source (title, two paragraphs, steps 1–8, the rules line); the numbers (Supplement 1, version 4, four checks, three properties, eight steps, outcomes 1, 0, ?) match the Russian text and `TEXT.md` S8.3-2; “consequences” (step 1) and “Reproducibility and removal” (step 6) are the terms of Section 8.4; “adjudicates”, “parties”, “in force”, “each case is attempted once” follow Section 9, Appendix A.4.1 and `PROTOCOL.md` Section 3; no sentence contradicts `PROTOCOL.md` or Section 9; `PROTOCOL.md` was last modified 2026-11-23 05:37 UTC, before the first task of the night started (05:45 UTC, (not published: orchestration or scratch) job `SN`), so the framing claim that it is not changed is true. The work wrote only the two files in `SUP1/`.

1. **Framing sentence: “before the work on any step named here begins” and “after the first night of checks” are not established as true.**
   Where: `SUP1/SUPPLEMENT-1.md` line 3.
   Evidence: (not published: orchestration or scratch) shows job `BC2` (testbed, build round 2 of 4) `running` since 12:36:51 UTC and the night report `"pending"`; (not published: orchestration or scratch) shows two reviews of the night started at 13:01:01 and 13:02:31 UTC and still running. `B2/ROUNDS.md` Round 1 self-test: “it performs document/browser work and runs a personal script whose exact bytes/interpreter are recorded”; Round 4 is “Integrated ordinary work and reproducibility”. This is the system that step 5 names (“command shell, one’s own recorded script, packages, a network, a browser, documents”), and its build has begun and is running.
   Minimal fix: replace lines 3–4 with: “Published on 23 November 2026. It does not change `PROTOCOL.md`. At publication, the build of the check 2 testbed, begun during the first night, was still running; no other work on the steps named here had begun.”

2. **“we” names who performs the work (step 1).**
   Where: `SUP1/SUPPLEMENT-1.md` line 10.
   Evidence: the task allows only “party” or “performer” for who performs the work; step 2 of the same page already renders the same Russian first-person verb form (“собираем”) in the passive.
   Minimal fix: “By reasoning, we look for two different states of a computer under one declaration, in each of which the three properties hold.” → “By reasoning, two different states of a computer under one declaration are sought, in each of which the three properties hold.”

3. **“We” names who performs the work (step 3).**
   Where: `SUP1/SUPPLEMENT-1.md` line 16.
   Evidence: as in finding 2; Russian “Записываем”.
   Minimal fix: “We write down what must be true at each point of an ordinary update, and what is in force for a list taken from a server when there is no network.” → “What must be true at each point of an ordinary update is written down, and what is in force for a list taken from a server when there is no network.”

4. **“An unfinished testbed” narrows the Russian “недоделка стенда” and departs from the term of Appendix A.4.1.**
   Where: `SUP1/SUPPLEMENT-1.md` line 23.
   Evidence: “недоделка” is a shortcoming or defect of the testbed, not a testbed that is unfinished as a whole; Appendix A.4.1: “Otherwise it is a defect of the testbed, and the case yields ?.” As written, a finished testbed with a defect would not be covered.
   Minimal fix: “An unfinished testbed gives “?”.” → “A defect of the testbed yields “?”.”

5. **“did not hold” is not the outcome term of the text.**
   Where: `SUP1/SUPPLEMENT-1.md` line 8.
   Evidence: Russian “не выдержала”; Appendix A.4.1: “1 (the hypothesis withstood the check), 0 (it did not)”. “Hold” is used on the same page for properties (“the three properties hold”), so the outcome and the property read alike.
   Minimal fix: “a confirmed gap means that version 4 did not hold” → “a confirmed gap means that version 4 did not withstand the checks”.
