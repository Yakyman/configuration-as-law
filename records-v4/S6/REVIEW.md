VERDICT: AGREED

# Review RV-S6-O of `S6/RECORD.md` (supplement 1, step 6)

Reviewed 2026-11-23 UTC by a party that took no part in preparing or performing step 6. Inputs read: (not published: orchestration or scratch),
`TEXT.md` Sections 8, 9.3, 9.4 and Appendix A.4.1, A.4.3, A.4.4, `SENTENCES.md`, `SUP1/step-6.md`, `B2/BUILD-4.md`,
`check-inputs-v4/supplement-1/step-6-cases/B2/CASES-6.md`, `check-inputs-v4/supplement-1/step-6-cases/B2/COMPARE-6.md`, (not published: orchestration or scratch), (not published: orchestration or scratch), `S6/RECORD.md`, `S6/LOG.md`,
`S6/QUESTIONS.md`. Paths are relative to the night folder. Raw evidence was read only for the sample in finding 5.

The recorded outcomes (case 1: 1; 2a: 1; 2b: ?; 3: 1; 4: 1; the step: ?) follow `SUP1/step-6.md` and Appendix A.4.1.
No rule was invented and no sentence of the text was reinterpreted. The numbers checked match the data files. The
findings below are corrections to how the record states things. None of them changes an outcome.

1. **The publication gate of CASES-6 was only partly met, and §0 presents this as a question instead of a fact.**
   *Where:* `S6/RECORD.md` §0; `S6/QUESTIONS.md` item 2. *Evidence:* `check-inputs-v4/supplement-1/step-6-cases/B2/CASES-6.md` (“Publication gate”) requires the
   records operator to “commit and publish **the unchanged sealed inputs**”, and says that the seal binds “the
   executable runner and the recipe”. `S6/raw/verify/published-vs-seal.txt` shows that 89 sealed files were published
   and 92 were not, among them `build/bc4-run-case.py`, `build/bc4-compare.py` (which COMPARE-6 calls “the executable
   query list”), `lab.py`, and the seal itself. The seal's SHA-256 `42317d32…7840124` appears in no committed file
   (`B2/*.md` (some matches not published: orchestration or scratch) (some matches not published: orchestration or scratch), (not published: record outside selected evidence), `SUP1/`). So no public hash bound those bytes before 18:03:03Z. CASES-6 gives the records
   operator the job of writing the publication record. Here the second party wrote it (§0). Its content is factual: the
   commit and URL match `S6/raw/verify/public-fetch.txt`. *Why the outcomes stand:* what A.4.1 and step-6.md require to
   be committed was committed before the first attempt. That is the image hash, the seven declarations, the packages,
   the removed lines, the exact commands (CASES-6) and the list of queries (COMPARE-6, which gives each exact query).
   The commands that ran in the guests match the committed text (finding 2). Today the local runner and collector equal
   their seal entries (`ead2f4e2…`, `dd1af84f…`). *Minimal fix:* in §0, say plainly that the CASES-6 precondition was not
   met for 92 of the 181 sealed files, and that the second party, not the records operator, wrote the publication
   record. The records operator publishes the 92 files with a dated note that they were published after the attempts.

2. **The commands executed match the committed commands. No defect.** *Where:* RECORD “Commands” in every case.
   *Evidence:* `S6/raw/case-{1,2a,3,4}/commands.json` compared line by line with the guest sequence in `check-inputs-v4/supplement-1/step-6-cases/B2/CASES-6.md`.
   They match, including the opposite install orders (left: alpha then beta; right: beta then alpha), the ordinary
   (non-root) worker launches in case 3, and the case-4 stage order (both → one → none). The only extra steps are the
   ones CASES-6 itself describes: staging the inputs, `sha256sum` source identities, the final read-only report export,
   and destroy. In case 4 the three `package` queries and `cat objects.json` run in one `set -e` invocation. This
   changes no query. Each case ran once on new guests (`lab.py new` per case; `cleanup.json`: `remaining_owned_guests: []`).

3. **Case 3: “its executable” was not observed independently after removal, and the outcome line leaves this out.**
   *Where:* RECORD case 3, “Limit” and “Outcome: 1”; the comparison table row for case 3. *Evidence:*
   `S6/raw/case-3/before-processes.stdout`. The former process 1538 ran
   `exe=/var/lib/stand/code-root/opt/stand/pkgs/dev-worker/bin/worker`, not the `/opt/...` path that COMPARE-6 names as
   “the worker service's executable”. The committed queries after removal test only the `/opt` path: `stat` exit 1,
   launch exit 127, no path holder. The code-root view is covered only by the testbed's own verifier
   (`B2/build/codeboundary.py` lines 154–157 and 207–208, checked: exact membership of the input root). Outcome 1 still
   follows step-6.md. Step-6.md gives 1 when nothing counts against the hypothesis. No observation counts against it.
   The system's own report says the view no longer holds the worker. The record discloses the limit. *Minimal fix:* add
   the qualifier to the Outcome line and to the comparison row: “code-root view after removal observed only through the
   testbed's own verifier”.

4. **Cases 1 and 2a: the outcome sentence claims more than was observed for the `boot` line.** *Where:* RECORD case 1
   “Outcome: 1” (“what is in force under the lines does not differ”). *Evidence:* `S6/raw/case-3/judge-after-fulfil.json`
   and the case-1 judge files list `boot` and `code-boundary` as not decidable from inside a guest. The two guests' host
   VM argv differ only in per-guest paths and the forwarded port. There is one `-drive` and no boot, bios or pflash
   option (`S6/raw/case-1/{left,right}-qemu-argv.json`, checked). The stated value `guest_can_change: false` was not
   observed on either guest. *Minimal fix:* change it to “no observed difference; `guest_can_change` cannot be observed
   from a guest and was compared only through the identical host launch arguments”. The outcome stays 1: A.4.4 fails a
   case only when a difference is found.

5. **Sample of 8 claims checked against the cited evidence. All hold.**
   (a) Case 1, both guests: `COMPLETE SUCCESS 8a98779d…`, `filesystem_paths_checked: 1370` (`case-1/{left,right}-apply.stdout`).
   (b) Each pair diff has 8 entries. In `/evidence/commands` only `ss` outputs differ: 11 in case 1, 6 in case 2a.
   Their argv, exit and stderr are equal, and the sorted stdout is equal. `last_success` and the five `success_report`
   entries are equal once `time_utc`/`utc_epoch` is removed. Kernel profiles hold the same set in a different order:
   119 lines in case 1, 117 in case 2a (`case-{1,2a}/pair-diff.stdout`).
   (c) Case 2a, before the final application: left and right are byte-identical, 2201/2201 and 2202/2202, own group
   only, nologin, `/home/NAME`, stated GECOS (`case-2a/*-accounts-before-final.stdout`). The last-applied hash is
   `fdf0bc71…` on both guests.
   (d) Case 2b: `B2/build/stand.py` line 94 (managed account UID range check), line 118 (`expected_account` requires
   `uid`, `gid`), and `B2/build/bc3_account_rows.py` lines 61–72 (numeric UID/GID emitted). This is as stated.
   `case-2b/not-expressible.json` exists.
   (e) Case 3 before: MainPID 1534, active and enabled. The holder is PID 1538 with argv `… --wait`. The ordinary launch
   exits 0 and prints `development-version-1`.
   (f) Case 3 after: `exists: false` for 1538/5173, `holders: []`, `is-enabled` gives `not-found` (exit 4), the launch
   exits 127, and the nft table holds only the `input` chain with policy accept.
   (g) Case 4: the stages hold exactly as in the RECORD table: both origins → only `bc4:owner-b` → no registration of
   `bc4-shared`, `bc4-owner-a` or `bc4-owner-b` (`case-4/{both,one,none}-packages.stdout.zst`).
   (h) §0: seal of 181 files with no mismatches. Image `1b581030…` has mode 0444. Local and public CASES-6 and COMPARE-6
   equal the gate hashes. The seven declaration hashes equal both the seal entries and `B2/cases-6/*/declaration.json`.
   `SUP1/step-6.md` equals `check-inputs-v4/supplement-1/step-6-cases/B2/cases-6/criteria/step-6.md` (`3d490b8c…`).

6. **The other numbers in the record match the data files.** 89 published + 92 unpublished = 181 sealed files. There
   are 22 `.zst` files and 22 lines in `S6/raw/LARGE-ORIGINALS.sha256`. Five `publication.json` copies have one
   recorded original hash. Times in RECORD and LOG match `commands.json` and `completed.json` (case 1 18:03:03–18:06:21Z;
   2a 18:08:01–18:13:43Z; 2b 18:14:37Z; 3 18:14:51–18:17:28Z; 4 18:18:53–18:22:22Z).

7. **Service statuses were captured once at the end, not after each service.** *Where:* LOG, “(service exit 0,
   Result=success)” for each case. *Evidence:* CASES-6 says to “save its status before starting the next”. The only
   saved status is `S6/raw/cleanup-final.txt` (18:23:06Z), which shows all four services. The services did run one
   after another without overlap: the times in finding 6 show this. *Minimal fix:* cite the `completed.json` times as
   the evidence of sequential runs, and say that the statuses were saved once at the end.

8. **Outcomes and their combination: correct.** Cases 1, 2a, 3 and 4 each get 1 because no observation counts against
   the hypothesis under the failure conditions of step-6.md, A.4.3 and A.4.4. No argument for 0 was needed, and the
   record notes that none was written. Case 2b gives “?” under step-6.md (“If the declaration format of the testbed does
   not admit a line without the identifier, 2b is recorded as not expressible on this testbed.”; “A case that cannot be
   expressed or performed gives “?”.”). The question on the readings of “unambiguous” stays open for the author
   (`S6/QUESTIONS.md` item 1) and is not decided. The step is “?” by the combination rule of A.4.1. The comparison with
   the expected result is honest: the 8 order and time differences in cases 1 and 2a are listed, and the case-3 row is
   qualified (“by every committed query”). No gap was put into a list.

9. **The work stayed inside its task. No defect.** No probe was added. No case was repeated or repaired. The first
   offline reading of case 1 had an error: a multi-arch name qualifier gave 204 false package mismatches. It was
   corrected offline on the same saved files, and this is disclosed. The tools in `S6/tools/` only read saved outputs, a
   clone of the public record, and `B2/build/` sources that BUILD-4 links. No folder of another task was read. The
   publication record was written inside the server's `VMs/cal-1123/` tree, which (not published: orchestration or scratch) permits (see finding 1 for
   the role question). The S6 files contain no personal names, host names, home paths or mentions of the system that
   prepared them. All guests were destroyed (`S6/raw/cleanup-final.txt`).
