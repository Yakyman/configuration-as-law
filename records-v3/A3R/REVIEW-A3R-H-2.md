VERDICT: DISAGREE

Review of `RESULT.md` after fix round 1, 2026-11-22 UTC. Read: (not published: outside selected checks and direct evidence), `../TEXT.md` Sections 2–4,
`../SENTENCES.md`, (not published: orchestration and working notes), (not published: orchestration and working notes), `RESULT.md`, `FIX-A3R-H-1.md`, `REVIEW.md`,
the files under `A3R/fix-a3r-h-1/`, `compare/STATS.md`, `adjudication/rows.tsv`, (not published: outside selected checks and direct evidence)
(selected rows), `review/resolved_sample.json`, and selected lines of `A3R/in/raw/lived/raw/003-…` and `160-…`.
The disagreement rests on finding 1: one confirmed-hole extent and the total of distinct rows do not match the
full-table search that the task requires.

## Findings

1. **The card-9 extent leaves out the user-instance markers of the same helper.** Where: `RESULT.md`, "Confirmed
   hole 3" ("Extent: 21 stored-outside-packages rows") and the total of 137 distinct rows; `fix-a3r-h-1/code_extent.tsv`
   (card 9); `fix-a3r-h-1/helper-search.tsv`; `fix-a3r-h-1/recount.py` lines 40 and 57, which search only the prefix
   `/var/lib/systemd/deb-systemd-helper-enabled/` and the name substring `deb-systemd-helper`. Evidence: the exact
   installed source (`init-system-helpers 1.69~deb13u1`, same URL as (not published: external working record), lines 100–105) defines
   `USER_INSTANCE_ENABLED_STATE_DIR => '/var/lib/systemd/deb-systemd-user-helper-enabled'`; saved excerpt lines
   576–580 switch `$enabled_state_dir` to it for user units, and the same `make_systemd_links` branch (lines 354–377)
   then checks and touches markers there. `160-filesystem.out` lists regular-file markers in that directory, e.g.
   `…/deb-systemd-user-helper-enabled/default.target.wants/pulseaudio.service f`,
   `…/graphical-session.target.wants/hyprpolkitagent.service f`, `…/sockets.target.wants/dirmngr.socket f`.
   `joined.tsv` has five rows for them, none in `code_extent.tsv`: `44ecaacc91e376e873a2b925`
   (`/var/lib/systemd/deb-systemd-user-helper-enabled`), `60af4555f895a621f8fdd8b5` (`…/default.target.wants`),
   `296089dc9d4776765bdfe6b3` (`…/graphical-session-pre.target.wants`), `4c799fa72ea8014675516c7b`
   (`…/graphical-session.target.wants`), `3dbad18363c3236ada19e5bb` (`…/sockets.target.wants`). Minimal fix: add
   the user-instance marker directory to the witness search, save the constant line with the source excerpt,
   and recount (on this evidence card 9 becomes 26 rows and the distinct total 142), or state with evidence why these
   markers differ.

2. **S2.5-1 is listed among the sentences that "support the refutations".** Where: `RESULT.md`, "Cards that did not
   survive", first paragraph. Evidence: the same file says "S2.5-1 is not used as a recording exemption anywhere",
   and the linked reviews (`review/code_cards.md` lines 15 and 37, `review/settings_cards.md` line 93,
   `review/cache_redundancy.md` line 44) use it only to reject OUTSIDE. Minimal fix: say that S2.5-1 is quoted
   only to show why the cards are not OUTSIDE.

## Handling of the previous review (`REVIEW.md`)

- Finding 1 (inconsistent S2.5-1 use): handled. The four S2.5-only NOT rows and the udev OUTSIDE decision are
  withdrawn (`fix-a3r-h-1/scope-review.md`); both readings go to `fix-a3r-h-1/QUESTIONS.md` as an author question,
  with neither adopted. The four rows were treated as step-1 candidates: three ? under S3-2, one confirmed (card 9).
  The udev row's MUST rests on the c1 record in `joined.tsv` ("Removing arbitration entries changes which device can
  hold the shared symlink").
- Finding 2 (session file as history): handled. Card 7 is the four recentf/savehist rows; the three removed
  memberships are in `fix-a3r-h-1/removed-history-memberships.tsv`.
- Finding 3 (missing facts labelled REFUTED): handled. Card 6 and the sample rows carry "? under S3-2" and are not
  counted as refuted.
- Finding 4 (outcome for an extra run): handled. The result states that it carries no published-check outcome.
- Finding 5 (RESOLVED:MIXED): handled. The rejected denominator is right: the 40 sampled IDs in
  `review/resolved_sample.json` have 12 RESOLVED:MIXED, 18 RESOLVED:MUST and 10 RESOLVED:NOT in `adjudication/rows.tsv`, and
  the 12 match `fix-a3r-h-1/mixed-sample.tsv` (9 REFUTED, 2 SUPPORTED, 1 UNKNOWN).

## Checked without finding

- Numbers: STATS (5,212; 3,854 = 73.94 %; kappa 0.55445; 2,010) and verdict counts 681/226/441/621/41 match.
  `code_extent.tsv`: card 1 has 115 rows (69 + 45 + 1), card 7 has 4, 3 overlap, 116 distinct; card 9 has 21 rows
  with no overlap. `sample_audit.tsv`: resolved 22 supported, 18 candidates (9 REFUTED, 7 UNKNOWN, 1 FACT-WRONG,
  1 CONFIRMED), 15 quotes that are not full sentences; agreed 60 supported. All of these match `counts.json`.
- Sampled evidence holds: `in/raw/lived/raw/003-packages-root-dpkg-query.out` line 227 reads `init-system-helpers 1.69~deb13u1 ii`;
  the source excerpt shows `next if -e $statefile;` before link creation, and the comment "Store the fact that we ran
  enable … so that we can skip enable the next time"; `fix-a3r-h-1/raw/scope-inventory.tsv` has 34 regular files under the
  journal streams directory and the staged os-release entry; `/var/lib/systemd` (`9a8b54a65f2c0b01ccabcf0e`) lists
  the helper directory among its members.
- Card 9 reads S2.2-6 literally: the source's own comment describes each marker as a stored record of a past enable
  action, and no sentence sets S2.2-1 or S2.2-6 above the other. No rule was added.
- `bin/check_quotes.py A3R/RESULT.md`: 14 quotes checked, 0 missing. No proposal to change the text. The fix ran no
  probe, VM or new classification, read no other task folders, and the files contain no host names, home paths of
  the host or private tooling labels.
