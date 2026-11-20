VERDICT: AGREED

Review of X9 (where 25 programs keep their state), 2026-11-19. Read: the shared rules of the checks, PAPER.html §5 and §9, X9-STATE.md, X9-PROTOCOL.md, plus the data X9 cites (analysis.json, validation.json, shared.txt, X9-paths.tsv, RUNLOG, REVIEW excerpts). My own recomputation is in `raw-REVIEW-X9/recompute.py` and its output in `recompute.out`.

The checks I ran:
- **(1) Outcomes.** O1, O2, P6 and the hypothesis are all `?`, and the collection status is also `?`. This follows the fixed rules:
  - §9.1 and the protocol say unresolved trace attribution gives `?`.
  - The §9.2 census condition and the §9.5 P6 condition are never exercised: X9 does no classification and no generation or archive transition.
  - No `0` was claimed from a stand defect.
- **(2) Numbers.** I recomputed every headline metric and all 25 table rows independently from `X9-paths.tsv` (primary_run=1). They all match:
  - 2,058 created paths; creators 2,053/5/0; mutators 2,051/5/2.
  - Shared paths 2/3/1; outside 1,635 and 1,645.
  - Per-program attributed, outside and C/Ch/D counts.
  - These also match `analysis.json`.
  - Protocol sha256 = `8a18a0e2…` equals the preregistered hash. The protocol mtime is 08:44 UTC, before the first run at 08:53 UTC.
  - All 25 primaries are from guest-b. Inventory errors in the primary runs: 0. Runtime checks: 24.
  - The 3 unverified attempts have rc 1, 1 and 125, as stated.
- **(3) No invented classification rule.** No path is assigned to derivative or data. caller_directed is defined in the protocol and is explicitly not used as a class. Candidate holes are listed as open.
- **(4) Sample of 5 claims, each checked against the cited evidence:**
  - Firefox `trace.log:83271` is the literal `???() = ?`, syscall number 9.
  - GnuPG `trace.log:643–657` shows the existing agent socket and IPC writes.
  - Podman `trace_stats` has 86 unresolved namespace paths, 21 unresolved dirfds and 10 unsupported mount mappings.
  - shared.txt was written by Vim (`02-vim-a3/trace.log:612–615`) and by Emacs (`03-emacs-a3/trace.log:2896–2903`).
  - Firefox paths under `~/.config/mozilla` are real. Debian ships firefox-esr 153.7.0esr per packages.tsv, and the path appears in the trace (line 2066).

Findings (none changes an outcome):

1. **"Frozen" selection rule that is not in the frozen protocol.**
   - *Where:* X9-REVIEW.md lines 370 and 406, and the RUNLOG campaign-B entry.
   - *Problem:* They call "highest verified complete attempt per family" the *frozen* rule. X9-PROTOCOL.md contains no attempt-selection rule (grep `highest|supersed` gives 0 hits).
   - *Why the effect is nil:* Every label has exactly one guest-b run, and the B run supersedes A by construction.
   - *Minimal fix:* Call it an implementation selection rule set in the RUNLOG after campaign A, not a frozen rule.

2. **Wording that names a creator X9 says it does not know.**
   - *Where:* X9-STATE.md, the GnuPG paragraph.
   - *Problem:* "GnuPG also created two persistent paths without a traced creator" names a creator. The cited lines 643–657 show only IPC to gpg-agent, not writes to those paths.
   - *Minimal fix:* "Two persistent paths appeared during the GnuPG run without a traced creator."

3. **What "verified" means for 12 of the 25 runs is not said in STATE.**
   - *Where:* X9-STATE.md, the claim "25/25 verified scripted use".
   - *Problem:* 12 runs have `expected_output = null` in analysis.json. Their verification comes from other sources:
     - for 6 GUI programs, the X9-gui.py window-title match plus rc 0;
     - for the CLI programs, the `grep`/`test`/`cmp` lines under `set -e`.
   - *Why it still meets the protocol:* For "open local web/mail/document/media" this is enough.
   - *Minimal fix:* Add one line to STATE saying how the GUI runs were verified.
