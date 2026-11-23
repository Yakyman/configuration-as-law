VERDICT: DISAGREE

Review of B1 after fix round 2, recorded 2026-11-22 UTC. Role: review. I took no part in B1, FX-B1-1 or FX-B1-2. Read: (not published: outside selected checks and direct evidence); `../TEXT.md` Sections 2–4; `../SENTENCES.md`; (not published: orchestration and working notes); (not published: orchestration and working notes); `REVIEW-B1-2.md`; `FIX-B1-2.md`; `CHANNELS.md`; `DESIGN-INPUT.md`; `B1/fix-b1-2/` (evidence-audit, row-changes, variant-inventory, validation, input-manifest, WORKLOG, REVIEW, validate.py, revise.py, `before/`); the cited ledgers `raw/c7-sources.md`, `raw/install-sources.md` and `raw/mechanics-sources.md`; and line 29 of `fix-b1-1/control-audit.md`. I ran no experiment. I checked only the three primary pages in the sample (item 8).

1. **M4.01 and M4.02 are CLOSABLE for "All C1–C10". For interpreted code, that verdict depends on interpreter-route closure, and the report itself rates that closure UNKNOWN.**
   - Where:
     - CHANNELS M4.01 (line 87): "Revoke every launch authority".
     - CHANNELS M4.02 (line 88): "Current-declaration membership authorizes execution, not old signature or surviving pathname". Its cost cell says "Retained bytes permitted only as inert content".
   - Evidence:
     - S2.4-4 requires that the removed contribution "cannot be started". S2.1-3 puts code that "can be started" in force.
     - Take a recorded own-rights script (S2.2-10) whose line is removed. Its retained bytes are started with `python3 <file>`, or through stdin or `exec(open(...))`. Those routes are C7.01, C7.05, C7.08 and C7.24, and all four are UNKNOWN because "mandatory placement of every interpreter start in D is not evidenced" (lines 38, 42, 45, 61).
     - The evidence cited for M4.02 does not close those routes:
       - the limit of `raw/install-sources.md` E3 says MS_NOEXEC "does not describe interpreter read semantics";
       - the limit of E10 says "stock targeted policy leaves many user processes unconfined";
       - M7 (unlink) and M8 (mmap) show only that bytes survive.
     - This is the standard REVIEW-B1-2 finding 1 applied to the D rows: an unevidenced mandatory component cannot carry CLOSABLE.
     - The M rows are byte-identical to the frozen copy `fix-b1-2/before/B1/CHANNELS.md`, so this round did not check them against that standard.
   - Minimal fix: choose one of the following, then regenerate the first line, `variant-inventory.json`, `validation.json` and the DESIGN-INPUT list.
     - Limit M4.01 and M4.02, in both the variant name and the requirement cell, to native executables and mappings under N, and point to C7.01/05/08/24 for interpreted code.
     - Or set both rows to UNKNOWN.

2. **The M4.03 mechanism cell rests on the unbuilt broker.**
   - Where: CHANNELS M4.03 (line 89): "prevent reactivation through broker policy".
   - Evidence:
     - The report rates the broker as unevidenced in three places:
       - C1.1 and C6.2/C6.3: "no evidenced complete declaration-only integration";
       - DESIGN-INPUT item 2: "Declaration mutation authority — candidate, UNKNOWN".
     - The cited I16 and I17 limits describe the bypass, not a closure: "Transient APIs bypass persistent-file-only management" and "independent mutation".
     - `fix-b1-1/control-audit.md` line 29 limits M4.03 to "the bounded withdrawal obligation for a fixed controlled activation graph". The row itself does not say so.
   - Minimal fix: replace "through broker policy" with the bounded scope (withdrawal of the edges of a fixed activation graph; re-creation stays with C6.2/C6.3), or set the row to UNKNOWN.

3. **REVIEW-B1-2 finding 2 (requirement column versus verdict) is handled for the C rows only. The M rows keep the same inconsistency.**
   - Where:
     - CHANNELS line 94: "Each verdict covers its row's entire stated requirement".
     - `fix-b1-2/evidence-audit.md` E2-2: "Each retains its individually bounded stated requirement".
     - DESIGN-INPUT: "explicitly narrower requirements".
   - Evidence: the requirement cells cite whole property sentences:
     - M1.01: "S2.1-5; S2.3-4–7; S3-3", which is all of P1, P2 and P4;
     - M3.01 and M5.01: S2.3-4,5;
     - M4.01: "S2.1-3; S2.3-4,6; S2.4-4".
     A CLOSABLE verdict cannot cover all of S2.3-4 to S2.3-7 while 77 rows are UNKNOWN. Saying that a row "has no R" does not make these cells narrower.
   - Minimal fix: write the bounded obligation into each M requirement cell, for example M1.01: "S3-3: preparation success is not reported as application success". Or reword line 94, E2-2 and DESIGN-INPUT to say that for M rows the sentence IDs are sources, and that the obligation is limited to the variant name.

4. **Publication rule broken in a new file.**
   - Where: `fix-b1-2/validate.py` line 70.
   - Evidence: the hygiene regex literally contains a personal name, a host name and names of automated systems and vendors. COMMON.md, Records, forbids each of these "in every file you write". The file is new in this round; `fix-b1-1/validate.py` contains none of them.
   - Minimal fix: keep the forbidden-string list outside the published records (or compare hashes of the strings), then rerun the validation into a new output.

5. **Mechanics ledger labels cannot be traced (minor; already present before this round).**
   - Where:
     - CHANNELS cites M1–4, M5–8 and M9–11.
     - DESIGN-INPUT cites `raw/mechanics-sources.md` "E5,E6" and "E1–12".
     - CHANNELS line 100: "Each ledger gives a primary URL, a short exact quotation, and its limit".
   - Evidence: `raw/mechanics-sources.md` is 14 unnumbered bullets with no limit field. The labels only work if the reader counts bullets by position.
   - Minimal fix: add the position-to-label mapping in a new addendum, without editing the frozen raw file, or correct the line 100 sentence.

6. **REVIEW-B1-2 findings 1, 3 and 4 were handled, apart from items 1–3 above.**
   - Finding 1: C2.6, C4.4, C7.01/07/08/09/24, C8.01/02 and also C7.23 are now UNKNOWN. D is described as conditional, and the cost of whole-session inheritance (lost document reads) is stated in C8.01/02, in Q3 items 6–8 and in DESIGN-INPUT item 1.
   - Finding 3: C7.24 names both the file-open route and the non-file route (stdin, argv/environment, inherited descriptors, socket/IPC) as UNKNOWN. Q1 and Q3 items 7–8 were corrected accordingly.
   - Finding 4: C7.05 now cites E12 (`fix-b1-2/row-changes.json`, C7.05 after).

7. **REVIEW-B1-2 findings 5–8 were dispositioned correctly. No published sentence or failure condition was changed.**
   - C7.18, C7.21 and C10.4 remain TEXT-OPEN, and Q2 keeps both readings unselected.
   - Where holes are said to yield 0, this rests on Section 4.1. No new rule is added.
   - The full-R remedy was one of the two options the review offered. The fact that C8.08 (values only) becomes UNKNOWN follows from that choice and does not reclassify its content.

8. **Numbers match the data files.**
   - The table has 88 rows: 8 CLOSABLE, 0, 0, 3 TEXT-OPEN, 77 UNKNOWN. This equals the first line, `validation.json` and `variant-inventory.json`.
   - The 31 verdict changes are exactly the 31 C rows that were CLOSABLE in the frozen copy. The eight M rows are the only CLOSABLE rows left.
   - 32 rows changed: the 31 above plus C7.05, which changed in evidence only.
   - Every requirement cell is identical to the frozen copy. Every C row carries R.
   - The DESIGN-INPUT list has 80 entries and equals the non-CLOSABLE rows exactly.
   - `fix-b1-2/input-manifest.json`: 90 of 92 hashes still match. Only CHANNELS.md and DESIGN-INPUT.md changed, and the hashes of the `before/` copies equal the manifest. Timestamps are consistent UTC.

9. **Evidence sample: 8 claims, 5 confirmed, 2 not confirmed, 1 confirmed only in part.**
   - Confirmed:
     - (a) The Linux 6.12 Landlock page contains "ready to sandbox itself with the ruleset" and "Every new thread resulting from a clone(2) inherits Landlock domain restrictions from its parent" (E2-1).
     - (b) C7.05 cites E12.
     - (c) Hash preservation (item 8).
     - (d) fsync(2): "explicit fsync() on a file descriptor for the directory is also needed" (M2.01).
     - (e) Linux 6.12 cgroup-v2: "Killing a cgroup tree will deal with concurrent forks appropriately and is protected against migrations" (M4.01, termination part only).
   - Not confirmed:
     - (f) The M4.02 closure for retained interpreted code (item 1).
     - (h) The DESIGN-INPUT labels "E5,E6" match positions 5–6 in content (cgroup.kill, systemd.kill), but the labels do not exist in the ledger (item 5).
   - Confirmed only in part: (g) M4.03. Withdrawal through the service manager is supported. The broker clause is not (item 2).

10. **The work stayed inside its scope.**
    - No VM, probe or testbed was run.
    - No channel or case was added. The C7.24 refinement stays inside the existing row, as finding 3 requested.
    - Writes stayed inside `B1/`. The new files reference only (not published: external working record) and (not published: external working record) outside B1.
    - Publication hygiene is clean except item 4.
