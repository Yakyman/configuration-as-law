VERDICT: DISAGREE

Review of `RESULT.md` (lived-in machine, table reduced to subtrees, beyond the published plan), 2026-11-22 UTC.
Read: (not published: outside selected checks and direct evidence), `../TEXT.md` Sections 2–4, `../SENTENCES.md`, (not published: orchestration and working notes), (not published: orchestration and working notes), `RESULT.md`,
`compare/STATS.md`, `adjudication/HOLES.md`, `A3R/adjudication/DONE`, `adjudication/rows.tsv`,
(not published: outside selected checks and direct evidence), the review files cited by the result, and eight sampled lines of `A3R/in/raw/lived/raw/`.
The disagreement is about findings 1 and 2: they change a confirmed-hole extent and the sample counts, and they
rest on a choice between two readings of S2.5-1 that the text does not make.

## Findings

1. **S2.5-1 is used to decide some objects and not others.** Where: `RESULT.md`, "Agreed sample" and "Resolved
   sample"; `review/sample_audit.tsv` (agreed order 7, `e2107a3dd8d91a0eef56dac4`; the four resolved rows coded
   with S2.5-1: `852fec2bc63d3ac71655249a`, `lived-tec6e90176f`, `4223394cc494d974882ce847`,
   `e6c7b500df6175d8c883f1e4`); `review/code_cards.md` (cards 1 and 7); `review/settings_cards.md` ("S2.5 does not
   replace the coverage decision"). Evidence: both classifications decided `e2107…` MUST under S2.2-1/S2.2-2, on a
   recorded removal effect ("Removing arbitration entries changes which device can hold the shared symlink",
   `joined.tsv`). The review still calls the row OUTSIDE because it is "program state", and it accepts four NOT
   rows whose only deciding sentence is S2.5-1. For cards 1 and 7 the same review says S2.5-1 "does not decide the
   simultaneous recording obligations" once a rule of Section 2.2 applies. S2.5-1 says that how to *treat* program
   state is a design question. It does not say that program state need not be recorded. Treating it as an
   exemption is one reading; treating it as a scope remark is the other. (not published: outside selected checks and direct evidence) reserves that choice for the
   author. Minimal fix: apply one reading everywhere, or record the S2.5-1 coverage question as an author question
   with both readings. Then recount: with the card-7 reading, the agreed sample is 60/60 supported and the four
   S2.5-1 rows become hole candidates under step 1. With the e2107 reading, finding 2 gets worse.

2. **The card-7 extent counts an nvim session file as "history".** Where: `RESULT.md`, "Confirmed hole 2", extent
   of 7 rows; `review/code_extent.tsv`, card 7. Evidence: three of the seven rows qualify only through
   `/home/user/.local/state/nvim/sessions/%home%user%Projects%flask.vim`: `7eb4c3828a8c64d587f79a56`
   `/home/user/.local`, `00be4be3f78767b555ebdc00` `/home/user/.local/state`, and `lived-tbba8c81784`
   `/home/user/.local/state/nvim`. The adjudication calls this file "editor state" (`adjudication/HOLES.md`, card 7) and
   "sourced state" (`adjudication/rows.tsv`, `lived-tbba8c81784`). A saved session is not a record of the past. It fits S2.2-6
   ("records of the past—logs, history;") only if a word is added, which (not published: outside selected checks and direct evidence) forbids. Under the review's
   own reasoning for `e2107…` (finding 1), it would be program state under S2.5-1. Minimal fix: limit card 7 to the
   recentf/savehist witnesses (`/home`, `/home/user`, `/home/user/.emacs.d`, `/home/user/.emacs.d/savefile`: 4
   rows, 3 overlapping card 1), or cite a source showing that the session file is history. The 116 distinct rows
   do not change, because the three session rows are already in card 1.

3. **Card 6 and four sample rows are labelled REFUTED, but no sentence decides whether they must be recorded.**
   Where: `RESULT.md`, card 6 and the resolved sample ("four rows … are REFUTED as demonstrated holes by S3-2");
   `review/cache_redundancy.md`. Evidence: (not published: orchestration and working notes) defines REFUTED as "a sentence of Sections 2–3, read
   literally, decides the example objects". S3-2 assigns the outcome ? to an object whose function is unknown. It
   does not decide whether the object must be recorded, and the result itself says the redundancy question is not
   disproved. No evidence shows the fact to be wrong, so FACT-WRONG does not apply either. Minimal fix: report
   these as a separate disposition, "? under S3-2 (facts not established)", and do not count them among the
   refuted cards or candidates.

4. **The result states an outcome for a run outside the published checks.** Where: `RESULT.md`, paragraph 1 ("Its
   outcome is **0**"). Evidence: `../TEXT.md` Section 4.1 assigns outcomes to checks, and Section 4.2 names the Check 1
   machines (Fedora Workstation, openSUSE Tumbleweed, Linux Mint, Flatcar, Talos). This machine is not one of
   them, and Section 4.1 adds "no cases are added after the checks begin". (not published: orchestration and working notes) asks for no outcome.
   Minimal fix: delete the sentence, or say that the confirmed holes would meet the Check 1 failure condition and
   that this run carries no check outcome.

5. **441 rows are reported as "RESOLVED:MIXED" without noting that this is not an adjudication verdict.** Where:
   `RESULT.md`, verdict table. Evidence: (not published: orchestration and working notes) allows only `RESOLVED:MUST`, `RESOLVED:NOT`, `UNKNOWN` and
   `HOLE`. Section 4.1 requires the quoted sentence to resolve the case. The review's own sample found 9 of the 11
   sampled MIXED rows quoting a sentence that decides only some members (`sample_audit.tsv`). Minimal fix: one line
   saying that RESOLVED:MIXED lies outside the adjudication's verdict set, and that its quote covered only part of
   the members in 9 of the 11 sampled rows.

## Checked without finding

- All numbers match the data. STATS (5,212 objects; 3,854 matching = 73.94 %; kappa 0.55445; 2,010 adjudicated),
  verdict counts (681/226/441/621/41) and UNKNOWN composition (22 process, 18 package-environment-evidence,
  1 stored subtree `lived-tbc8fc72e18`; 5 unadjudicated both-UNKNOWN rows, all stored-outside-packages) match
  `adjudication/rows.tsv` and `joined.tsv`.
- Both seeded samples reproduce exactly with `random.Random(seed).sample` on the sorted populations (1,348 resolved;
  3,202 agreed unadjudicated). Sample counts match `sample_audit.tsv`: 26/14, 59/1, and 15 incomplete quotes.
- The card-1 ledger has 115 rows (69 + 45 + 1), card 7 has 7 rows, 6 overlap, 116 distinct. 113 of the original
  132 rows plus 2 added rows; 19 original rows and 1 added row are uncertain.
- Sampled evidence checks out: `savehist` and `recentf` exist under `/home/user/.emacs.d/savefile/`; the Lua source
  for the cited mason.nvim luac witness exists; (not published: external working record) and its `__pycache__` bytecode exist in the
  Flatpak runtime; `in/raw/lived/raw/085-ssh-access.out` lines 5, 9 and 45 read `usepam yes`, `maxauthtries 6` and
  `allowtcpforwarding yes`.
- `bin/check_quotes.py A3R/RESULT.md` passes: 11 quotes checked, 0 missing. No proposals to change the text were
  found. The review files read no classification or adjudication working folders (references to (not published: outside selected checks and direct evidence)
  occur only inside copied `members` fields).
