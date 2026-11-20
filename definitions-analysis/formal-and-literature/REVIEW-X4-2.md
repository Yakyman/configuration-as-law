VERDICT: AGREED

# Review of X4 after fix round 1 (FX-X4-1)

2026-11-19. Reviewer: independent of the X4 executor and of the FX-X4-1 acceptance reviewer.
Read: the shared rules of the checks, PAPER §5 and §9 (plus O1–O9 in §8, which the outcomes cite), X/X4-FORMAL.md, X/FIX-X4-1.md,
X/REVIEW-X4.md, the frozen-outcome section of X/X4-PROTOCOL.md (lines 52–79), and the data files listed below.
I changed no file except this one.

## Were the previous findings handled?

| REVIEW-X4 finding | Status | Evidence |
|---|---|---|
| 1. P3/P4 effective bypass never searched; a sentence with no source dismissed it | Handled | `X4-model.py:107` `physical.launched_present`, `:126` `P4.permitted_launch_effective`. `canonical-permitted-bypass-no-class-left` SAT (present=0, launch_effective=0). `-right` SAT (present=1, launch_effective=1, change_allowed=1). `-joint` UNSAT; its `unsat_core` contains `P3.remainder`, `P4.permitted_launch_effective` and `physical.launched_present`. `control-omitted-launch-effect` SAT. The sentence "bypass is a change, not a fourth class" is gone from FORMAL (grep finds no match) and is withdrawn there explicitly. Strict outcome recomputed: "?" with the hole named (O5, line 204, quoted). |
| 2. Classification 0 reused Check 1 evidence | Handled | The FORMAL headline uses the requested wording word for word. `summary.json` `class_conflicts`: derivative/data is UNSAT in both profiles. No new census is claimed. |
| 3. C4 temporal hole not registered | Handled | FORMAL registers "H-X4-temporal" outside O1–O9 and cites lines 133, 142 and 145. It chooses neither reading. `canonical-historic-archive-joint` is UNSAT (current-only reading) and `canonical-historic-archive-historical-scope` is SAT (historical reading). |

## (1) Outcomes against the fixed failure conditions

- **Classification: 0.** This follows the §9.2 disagreement branch (PAPER line 220) and the frozen protocol (lines 54–60).
  It uses the same witness as Check 1 and is now labelled "not counted separately". ✓
- **Strict contradiction: ?** Protocol lines 62–66: a contradiction is 0 only "without adding a rule at an open
  boundary". Each of C1–C6 depends on such a boundary:
  - C1: O3, plus lifecycle priority after P5.
  - C2: execution scope vs admission scope of P7.
  - C3: O4.
  - C4: H-X4-temporal.
  - C5: O5. A bypass-launched program counts as "neither derivative nor data" only if O5 says that a program launched
    by a shell is not the shell's derivative. Line 133 ("Code executed within a program is its derivative") leaves this
    open.
  - C6: the queried state puts the launch and the completed deletion in the same moment. This is a projection choice
    of the stand, and the paper does not require it. Protocol line 69 gives "?" for unresolved semantics.

  So "?" is the protocol's prescribed outcome, not a softened 0. ✓
- Pair UNSAT results are reported as "1 only within the stated partial encoding and bound" (protocol lines 67–68). ✓

## (2) Numbers checked against the data files

- `run-006/summary.json` and `results.jsonl`: 226 calls, 104 SAT, 122 UNSAT, 0 unknown.
  `failed_controls` = [] and no row has `expected` ≠ `status`. ✓
- `queries/`: 226 `.smt2` files and 226 `.json` files. ✓
- 105 pair entries, 19 SAT: P3/P4 ×5, P3/P6 ×5, P4/P6 ×5, P4/P7 ×2, P2/P6 ×1, P5/P7 ×1.
  This leaves 15 pairs UNSAT in all profiles. It matches `pair-matrix.md`. ✓
- `pair-delta.json`: exactly 10 entries, P3/P4 and P4/P6 in each of the 5 profiles, all changed from unsat to sat. ✓
- Searches: 3 overlap, 6 class-conflict (plus left/right/joint replay), 1 no-class, 2 epistemic. ✓
- Protocol hash `c234983d…608d` matches `raw-X4/protocol.sha256`. `raw-X4/PAPER.html` is identical to `../PAPER.html`
  (cmp). ✓

## (3) Invented rules

None found. Every place where the paper does not decide a case is left open and named:
- O3, O4, O5, O6;
- H-X4-temporal;
- shared-needer eligibility (reported as both SAT and UNSAT, with neither chosen);
- P7 scope.

C5 does not use O4 as an exception to P3, and it adds no "bypass class".

## (4) Sample of claims (5)

1. C5 left, right and joint statuses and the joint core: as in the table above. ✓
2. C4 historical-scope query: SAT, with `historical_owner_eligibility=True`, `archive_keep` and `present=1`. ✓
3. C6 joint: UNSAT. Its core contains `P4.permitted_launch_effective`, `P6.completed_delete_setting`,
   `physical.deleted_absent` and `physical.launched_present`. ✓
4. E4 claim, `B/raw/fb1/check-authority.jsonl`. The file's sha256 `6d04eb40…` equals the manifest entry.
   - line 2: alice records `hello`;
   - line 5: `cp /usr/bin/hello /home/alice/downloaded`;
   - line 6: running it gives "Permission denied", rc 126;
   - line 7: `allow_channels {"alice":["download"]}`;
   - line 8: the same file prints "Hello, world!", rc 0.
   ✓
5. Fresh replay: `review/run-006-replay.json` records 226 queries, each replayed with a fresh solver. This agrees with
   `X4-FIX-1-REVIEW.md` (ACCEPT, 0 mismatches). ✓

## Findings (minor; none changes an outcome)

1. **The withdrawn sentence still stands, unmarked, in the evidence file.**
   - Where: `X/X4-EVIDENCE.md:9`, E3 row: "A bypass is a change, not a fourth P3 class."
   - FORMAL withdraws it, but someone who reads only X4-EVIDENCE sees it with no note.
   - Minimal fix: append a dated line at the end of X4-EVIDENCE.md, without editing row 9: "2026-11-19 FX-X4-1: the
     sentence in E3 'A bypass is a change, not a fourth P3 class' is withdrawn; see X4-FORMAL C5."
2. **E4's "not data" gap is not tied to O2.**
   - Where: FIX-X4-1 "Closest existing object" and FORMAL C5.
   - Both list E4's unresolved data-provenance question, a person-copied executable, but name only O5 as the open
     boundary. For the "is it data?" part of the same object, the matching open problem is O2 (line 201). This does not
     affect the synthetic C5 "?", which rests on O5.
   - Minimal fix: one clause, "E4's data-vs-derivative status also touches O2 (line 201)".
