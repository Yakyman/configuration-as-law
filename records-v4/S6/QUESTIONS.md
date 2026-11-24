# Questions from S6-O (for the author and for the review)

1. **For the author — case 2b was never reached.** The testbed's declaration format requires a numeric identifier on
   every account line, so a line without one could not be written. The question in `SUP1/step-6.md` therefore stays
   open: when a line says “create this account” but does not say its number, is that line “unambiguous” in the sense of
   Section 8.4? Reading A: yes — the line states everything the person chose, and a number the system picks is not part
   of the required state; then two machines giving different numbers would count against reproducibility. Reading B:
   no — a line that leaves the number to the system is ambiguous, so reproducibility is not claimed for it and different
   numbers count against nothing. On this testbed the case cannot answer it either way; only a testbed that admits such
   a line could.

2. **For the review — what was public before the attempts.** The public commit `c0de5e63` holds CASES-6.md,
   COMPARE-6.md and the full declarations, packages and removed lines (89 files, all equal to the sealed bytes). The
   scripts that actually ran the cases and the queries (`build/bc4-run-case.py`, `build/bc4-compare.py`, `lab.py`) and the
   seal file itself were sealed on the laboratory but not published. The commands and queries are published as text.
   Is the text enough to count as “the exact commands … committed” (Appendix A.4.1, step-6.md), or should the scripts
   have been in the public commit too?

3. **For the review — one place the committed queries do not look (case 3).** The worker ran from a copy-view of the
   installed files, `/var/lib/stand/code-root/…`. After removal, the committed queries checked the ordinary path, the
   process, the service, the rule and the kernel profiles, but did not read that view. Only the testbed's own verifier
   says the view no longer holds the worker. Nothing was added here (no extra probe); noted for whoever plans the next
   step.

4. **For the review — two lines no readback can settle (all cases).** The `boot` line's `guest_can_change: false` and the
   prose of the `code-boundary` line are not observable from inside a guest; their observable implementation (host VM
   arguments, loaded kernel policy bytes) was identical on both machines in cases 1 and 2a. Recorded as limits, not as
   differences.
