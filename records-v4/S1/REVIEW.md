VERDICT: DISAGREE

# Review RV-S1 of supplement 1, step 1 (`S1/ARGUMENT.md`)

Recorded 2026-11-23 UTC. Inputs read: (not published: orchestration or scratch), `TEXT.md` Sections 8–9 and Appendix A, `SENTENCES.md`,
`SUP1/step-1.md`, `S1/ARGUMENT.md`, `S1/QUESTIONS.md`, `S1/raw/*.txt|tsv`, the "By kind" table of
`D1/compare/STATS.md`, `D1/compare/joined.tsv` (kind and id columns only), and the performer's run log (command lines
only). The disagreement is with one outcome: Removal is given 1, but its derivation needs a reading of S8.2-11 that the
argument does not record (finding 4). Understanding 0 and Reproducibility ? stand. Findings 1–3 note defects in how the
argument supports them; fixing these defects does not change either outcome.

1. **Pair A/B against Understanding: survives. Its P4 justification decides a reading.**
   *Where:* `S1/ARGUMENT.md` lines 141 and 143 ("unsupported alterations are rejected"; "A system can reject unsupported
   alterations without violating these three properties").
   *Evidence:* I tried to refute the pair using the literal sentences:
   - P1 holds in both states. `alpha` and `beta` are named in LP and LQ, so they are recorded whether through S8.2-17
     or as their own line.
   - P2 holds. Each line requires the least unused UID at creation, and both schedules satisfy that (S8.1-12, S8.3-5).
   - The difference between the states is not required by any line. Line order is declared not to fix execution.
   - The words "The declaration alone, without inspecting the computer, shows … how it is configured" are false. An
     account is a setting (S8.2-13), and its numeric identifier differs between the states. Reading "configured" as
     "what the lines state" adds words. Section 8.4 qualifies only lists taken from outside.

   The weak point is P4. S8.3-7 says "an installer does not install a program past the declaration but adds it to the
   declaration". One reading makes this a requirement that an installer adds what it is asked to install. Under that
   reading, a system whose tools reject every alteration lacks P4. The argument settles this silently in its own favour.
   The pair does not depend on it: an installer that records each request as a new line of D leaves states A and B
   unchanged at the observation moment.
   *Minimal fix:* make the P4 stipulation "an installer request adds a line to D (S8.3-7); the observation moments
   precede any such request", and drop the sentence on line 143.

2. **The pair says two different things about how `alpha` is chosen.**
   *Where:* line 118 says "The account names and fixed fields belong to the respective immutable package's installation
   defaults; requesting them accepts those defaults". The same line also says "The person explicitly chooses the two
   accounts through the package lines". Line 94 calls the S8.2-17 default route "the distinguishing branch".
   *Evidence:* Under S8.2-11 an object is a setting only if it is "a value chosen by a person". The pair survives only
   because LP explicitly requests `alpha`, and LP therefore records it as its own line. The failure comes from a line
   whose stated requirement allows two outcomes (S8.1-12 permits such a line). It does not depend on S8.2-17's coverage
   of installation-created defaults. Line 160 shows the argument avoided the other route on purpose: "The pair does not
   rely on classifying an unrequested incidental account."
   *Minimal fix:* say that `alpha` and `beta` are settings because LP and LQ request them, and that the pair does not
   rest on S8.2-17. The outcome is unchanged.

3. **The Reproducibility derivation and the use of the pair: survives as "?".**
   *Where:* §4, lines 167–192; `S1/QUESTIONS.md` items 1–2.
   *Evidence:* Steps 1–5 follow from S8.3-1, S8.1-12, S8.1-14 and S8.3-4/5. Step 6 depends on a premise and says so.
   The choice between readings is anchored in the published text itself. Section 8.4 says "the result described in it",
   while Section 9.4 → A.4.4 also compares an account's "numeric identifier" and file checksums that no line need state.
   `SUP1/step-1.md` says that a consequence depending on such a choice gives "?". The missing premise that application
   completes on another computer is recorded as a finding, not as a pair. That is correct: S8.3-1 rules out any pair
   at a moment without a completed application.
   *Minimal fix:* none.

4. **The Removal derivation does not survive. The outcome should be "?", not 1.**
   *Where:* line 201, step 4 ("Suppose x nevertheless remains in force under S8.1-9, S8.1-10 or S8.1-11. P1, S8.3-4,
   then requires x to be recorded"). Line 209 is the attack row "Retain the installation-created account".
   *Evidence:* S8.1-11 makes an account or a service in force by its type ("an account, if it exists"), not by its
   kind. P1 (S8.3-4) covers only "Everything that is installed and every setting". Take an account `svc` that a
   package's installation creates by itself, which the person never requested. Under S8.2-6 it is not received content
   (Q1), not code (Q2), and a setting under Q3 only if "a value chosen by a person" includes a choice made by the
   package's author, or the person's choice of the package. Those are two readings:
   - **Narrow reading:** only a choice by the person of this computer counts. Then `svc` is a program record (S8.2-15:
     "a program recorded the object as it ran"), and S8.2-2 says it need not be recorded. Take the declaration
     [L0, LS], where LS installs package S, then remove LS and apply [L0]. State A: `svc` is deleted. State B: `svc` is
     retained. In both states P1 holds (`svc` is neither installed nor a setting), P2 holds (L0 is fulfilled), and P4
     holds (keeping a program record changes nothing installed and no setting). In B, `svc` exists, so it is in force
     (S8.1-11). Then "nothing the line contributed is in force unless it is recorded in the remaining lines" is false.
     A service enabled by a package's own preset gives the same result through "a service is in force if it is
     enabled".
   - **Wide reading:** `svc` is a setting, S8.2-17 covers it, and P1 rules out B. On this reading the derivation holds.

   The argument applies the wide reading without recording it. At line 209 it treats the account as covered by S8.2-17,
   while line 160 avoids classifying exactly such an account. Whether Section 8.5 ("How to store, transfer and remove
   program records") takes B out of Removal's scope is the same question as `S1/QUESTIONS.md` item 4. That question
   cannot be dismissed here, because B involves an object that is in force.
   *Minimal fix:* add this reading as a question in `S1/QUESTIONS.md`. Change the first line to
   `STEP 1: Understanding 0; Reproducibility ?; Removal ?`. Limit the Removal derivation to "installed objects and
   settings", and state that its full scope depends on the question.

5. **A wrong statement about the text supports Removal.**
   *Where:* line 213 says that for record or material, "S8.1-9–11 supplies no separate force criterion for that kind".
   `S1/QUESTIONS.md` item 4 and its final paragraph ("do not defeat the P1 implication") rest on this statement.
   *Evidence:* S8.1-11 gives force criteria to services and accounts whatever kind the ordered questions assign them.
   The statement holds for documents and non-account records, but not for an account or service that classifies as a
   program record.
   *Minimal fix:* correct line 213 and the last paragraph of `S1/QUESTIONS.md` to match finding 4.

6. **The other Removal attack rows survive.**
   *Where:* lines 210–215.
   *Evidence:* These cases are all either installed objects or programs. In each case, being in force while uncovered
   contradicts P1:
   - a running or startable program (S8.1-9, S8.2-9/10, S8.2-5);
   - a shared dependency whose last covering line is removed (S8.2-16);
   - a non-code package remnant under either reading of S8.2-7 (as an installed object it is in force and uncovered;
     otherwise it is not an account or service, so no force criterion applies);
   - an external-source account (S8.2-18 together with S8.1-11, where the account is a setting under S8.2-13 because
     the line requests it).

   The derivation uses a moment "after a completed application … without breaking". That is narrower than Section 8.4's
   "After application", but `SUP1/step-1.md` requires this scope for pairs, so it is not an error.
   *Minimal fix:* none.

7. **The crosswalk inherits the unrecorded reading.**
   *Where:* line 260 (`L1:account`: "D for the installation-created default account"). The `L1:service`, `L1:group`
   and other "D" rows make the same assumption.
   *Evidence:* The D route (S8.2-17) applies only after Q3 has made the object a setting. For defaults that the person
   did not request, that depends on the reading in finding 4.
   *Minimal fix:* make the D route conditional on that question. The counts and IDs are unaffected.

8. **The numbers match the data files.**
   *Where:* §7 table; `S1/raw/kind-examples.tsv`, `validation.txt`, `input-hashes.tsv`.
   *Evidence:* Recounted with awk:
   - `D1/compare/joined.tsv` has 16,375 rows in 45 kinds.
   - Every count equals the "By kind" table of `D1/compare/STATS.md`.
   - Every example ID exists with the stated kind.
   - The §7 table is identical to `kind-examples.tsv`.
   - All 7 SHA-256 fingerprints match the current files, including `SUP1/step-1.md`.
   *Minimal fix:* none.

9. **Sample of cited evidence (8 claims): 6 hold and 2 fail.**
   *Evidence:* The six that hold:
   - (a) The quote check reruns with "quotes checked: 50; not found in TEXT.md: 0".
   - (b) The A.4.4 quotation is exact.
   - (c, d) The kind counts and IDs match (finding 8).
   - (e) The three sysusers.d passages occur word for word in the host's installed sysusers.d(5) manual: "at package
     installation or boot time", "should they not exist yet", and "Specify "-" for automatic UID/GID allocation for
     the user or group". They total 22 words, as line 104 states. `S1/raw/reproducibility.md` says 24, but that is a
     raw file, not the result.
   - (f) "No machine was started and no behavioural probe was run" is confirmed by the command lines in the run log.

   The two that fail:
   - (g) Line 209: "Without any remaining coverage under S8.2-17/18, P1 fails" holds only under one reading (finding 4).
   - (h) Line 213: the force-criterion statement is wrong (finding 5).

   *Minimal fix:* as in findings 4 and 5.

10. **The work stayed inside its task.**
    *Evidence:* From the run log, the performer:
    - read only the named inputs ((not published: orchestration or scratch), `TEXT.md`, `SENTENCES.md`, `SUP1/step-1.md`, `OP/OPINION.md`,
      `D1/compare/STATS.md`, `D1/compare/joined.tsv`, (not published: orchestration or scratch));
    - made one search of public documentation;
    - wrote only under `S1/`.

    One file-name listing across the night folder, and a check for instruction files above it, showed names from other
    task folders but read none of their contents. Other task folders appear in the argument only through `OP/OPINION.md`,
    which the task named. No machine, probe or classification decision was used as a premise.
    *Minimal fix:* none.
