VERDICT: DISAGREE

Review of B1 after fix round 1, 2026-11-22T05:17Z UTC. Role: review; took no part in B1 or FX-B1-1. Read: (not published: outside selected checks and direct evidence); `../TEXT.md` Sections 2–4; `../SENTENCES.md`; (not published: orchestration and working notes); (not published: orchestration and working notes); `REVIEW.md`; `FIX-B1-1.md`; `CHANNELS.md`; `DESIGN-INPUT.md`; `B1/fix-b1-1/` (control-audit, text-audit, evidence-addendum, PROBE-DISPOSITION, validation, input-manifest, timestamp-evidence, WORKLOG); the frozen copy `fix-b1-1/before/B1/CHANNELS.md`, used only to compare verdicts. No experiment was run.

1. **D rows rest on an unevidenced component that imposes D, which breaks the standard the fix itself applied under REVIEW finding 9.**
   - Where: CLOSABLE rows that depend on D for their verdict: C2.6, C4.4, C7.01, C7.07, C7.08, C7.09, C7.24, C8.01, C8.02. Also DESIGN-INPUT item 1 ("bounded evidenced controls").
   - Evidence:
     - The only cited source for D is `raw/c7-sources.md` E12: "Landlock empowers any process, including unprivileged ones, to securely restrict themselves." The Linux 6.12 Landlock page (checked) also says "The current thread is now ready to sandbox itself with the ruleset". It describes no way for the system to impose a ruleset on a process. A process enters a domain only by restricting itself or by inheriting a domain from its parent.
     - CHANNELS line 102 itself says D is "not an evidenced complete launcher".
     - The fix moved 27 rows to UNKNOWN because "General denial capability does not evidence … a policy covering all backend APIs" (`fix-b1-1/control-audit.md`). The component that puts every start of a recorded own-rights interpreter into the D domain is unbuilt and has no source in the same way.
   - Concrete bypass, inside C7 and without superuser: from an interactive shell that is not in a D domain (C7.17 is UNKNOWN), run `python3 ./x.py` on an unrecorded file. If instead the whole session runs under D, the shell and everything started from it lose reads of unrecorded files. The cost columns of C8.01/C8.02 and Q3 item 6 do not state that loss.
   - Minimal fix: for these rows, either cite a primary source for a mandatory mechanism that places every execution of each recorded own-rights interpreter in a restricted read domain, and state its cost, or set them to UNKNOWN on the finding-9 standard. Then regenerate the first line and the DESIGN-INPUT list. C7.02 and C7.12 are not affected: they stand on N, because the unrecorded script is reached only through execve.

2. **Requirement column and verdict disagree for the runtime-port change.**
   - Where: CHANNELS line 100 says R in every row includes S2.2-15: "Thus every row includes P2, Removal and changes to required accounts/rights/rules/ports". Many rows built on R are still CLOSABLE, for example C2.3, C2.4, C3.4, C5.1, C5.3, C5.4 and C7.01. Meanwhile C7.25, the runtime-listener route of these same channels, is UNKNOWN.
   - Evidence: the fix's own `fix-b1-1/evidence-addendum.md` says: "Do not label an entire affected row CLOSABLE solely because code admission or explicit bind filtering is evidenced. If the inventory's rows include this runtime-change obligation, their full verdict must retain this UNKNOWN until complementary closure is evidenced." CHANNELS line 96 and control-audit instead redefine CLOSABLE as "the named bounded route". Nothing in TASK-B1 defines CLOSABLE that way: it is a verdict on the variant against its stated requirement.
   - Minimal fix: use one consistent form. Either limit the requirement column of each bounded row to what its verdict covers, and point to C7.25 and the M rows for the rest of R. Or let the verdict follow the full R.

3. **The custom-dispatch failure (REVIEW finding 5) is closed only for file opens, but the row and Q1 present it as closed.**
   - Where: C7.24; Q1 ("For C7.07/08/24, D blocks …; No system-wide NOT-CLOSABLE result follows because systems need not retain both capabilities"); Q3 items 7–8.
   - Evidence:
     - Q1's premise requires only that recorded M can receive the unrecorded instructions F after application. Nothing in it limits the route to a file open.
     - CHANNELS line 102 states that D "does not filter argv/environment or revoke already-open FDs, terminal/stdin or IPC".
     - Bypasses inside C7 without superuser: `cat F | M`, or M reading its command stream from a socket. No row gives either of these a verdict.
   - Minimal fix:
     - Name C7.24 explicitly as the file-open route.
     - Add the non-file input route for admitted custom dispatchers as UNKNOWN, either as its own row or inside C7.24.
     - Correct the Q1 sentence and Q3 items 7–8: under D, scripts still receive unrecorded bytes through stdin, argv and IPC.

4. **C7.05 does not cite the evidence the disposition says it cites.**
   - Where: CHANNELS C7.05 cites only "T ledger: E1,E2,E16" (the execution-check API and sample). FIX-B1-1 finding 3 says "the path-open part of C7.05 cite[s] D/E12", and REVIEW finding 3 asked for E12.
   - Minimal fix: add `raw/c7-sources.md` E12 to the C7.05 evidence column.

5. **The other REVIEW.md findings were handled correctly. No fix is needed.**
   - Finding 1: C10.4 is restored as TEXT-OPEN with card T4. S3-6, S3-7 and S3-8 are quoted exactly, no rule is added, and both readings are kept.
   - Finding 2: C8.07 is a requirement row (S2.2-10/13) with verdict UNKNOWN. The T2 card is withdrawn.
   - Finding 4: C7.17 is UNKNOWN, an option the review allowed.
   - Finding 6: Q3 items 7–8 state the lost data reads, subject to finding 3 above.
   - Finding 7: Q2 keeps both reading choices, selects neither, and "not a fourth hole" is removed from both files.
   - Finding 10: C7.20 cites S2.2-13 as the deciding sentence.
   - Finding 11: the source-package omission is acknowledged. The refinement time is corrected to "no later than 2026-11-22T04:50:40.622Z", which matches `fix-b1-1/timestamp-evidence.txt`, and the original raw files are unchanged.
   - Finding 12: see item 6.
   - Findings 3, 5, 8 and 9: their row changes are as stated, except the gaps in items 1–4.
   - No failure condition or published sentence was changed. Where holes are said to yield 0, this rests on Section 4.1 and S3-8, not on a new rule.

6. **Numbers match the data files. No fix is needed.**
   - The table has 88 rows: 39 CLOSABLE, 3 TEXT-OPEN, 46 UNKNOWN. This equals the first line and `fix-b1-1/validation.json`.
   - Comparing verdicts with the frozen copy gives exactly the changes FIX-B1-1 lists:
     - 27 rows moved to UNKNOWN under the broker standard (11 named in REVIEW finding 9, plus 16 more);
     - 10 F/I-dependent rows moved to UNKNOWN (C7.03/04/05/06/11/17, C8.03/05/06, C4.5);
     - C7.08 moved UNKNOWN to CLOSABLE, and C8.07 moved TEXT-OPEN to UNKNOWN;
     - three rows were added: C7.24 (CLOSABLE), C7.25 (UNKNOWN), C10.4 (TEXT-OPEN).
   - The DESIGN-INPUT "cannot certify" list is exactly the 49 non-CLOSABLE rows.
   - In `fix-b1-1/input-manifest.json`, 36 of 38 frozen hashes still match. Only CHANNELS.md and DESIGN-INPUT.md changed.

7. **Sampled evidence, 8 claims. Seven are confirmed and one is not.**
   - Confirmed, quoted exactly at the cited source:
     - (a) `raw/python-securebits-output.txt` shows `bits=0xf00` and `PYTHON_CODE_RAN` (C7.03).
     - (b) The v6.14 `samples/check-exec/inc.c` header names only the two counter commands (control-audit).
     - (c) Linux 6.12 Landlock: "Files or directories opened before the sandboxing are not subject to these restrictions." (D limits).
     - (d) The same page: "requesting to bind on port 0 is allowed" (E-FX8a).
     - (e) v7.3 `security/landlock/net.c` hooks only `socket_bind`, `socket_connect` and `socket_sendmsg`, with no listen hook (E-FX8b).
     - (f) listen(2) EADDRINUSE describes binding "to an ephemeral port" for a socket that was not bound before (E-FX8c).
     - (g) Firefox source docs: "implementation of a WebExtensions API runs with full chrome privileges" (C8.07).
   - Not confirmed: (h) T E12 shows only self-restriction. It does not show that D denies the opens for every interpreter start, which is what the D rows claim (item 1).

8. **Scope was kept. No fix is needed.**
   - No VM, probe or testbed was run in the fix round.
   - The added rows are inside C7/C10 and were requested by the review. No channel was added to the list in Section 4.3.
   - Writes stayed inside `B1/`.
   - The new files reference no other task folder.
   - No personal names, host names, home paths, or mentions of any automated system were found in the new or changed files.
