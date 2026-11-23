# Independent correction review

Role: review  
Date: 2026-11-22 UTC  
Verdict: **ACCEPT**

The correction addresses all five substantive findings without changing a failure condition or adding a rule to the published text.

1. The inconsistent S2.5-1 treatment is removed. `QUESTIONS.md` states both readings of the program-state scope question and explicitly chooses neither. The corrected audit does not use S2.5-1 as a blanket recording exemption; it follows S3-1 into Section 2.2 for the established functions and leaves the broader reading for the author.
2. Card 7 now contains only the four recentf/savehist rows. The three Neovim-session memberships are removed, three of the four retained rows overlap card 1, and the card-1/card-7 union remains 116.
3. Card 6 and all fact-insufficient sampled candidates are reported as `?` under S3-2 rather than REFUTED. The resolved-sample dispositions independently total 22 SUPPORTED, 9 REFUTED, 7 UNKNOWN, 1 FACT-WRONG and 1 CONFIRMED.
4. `../RESULT.md` assigns no published-check outcome to this additional run.
5. `RESOLVED:MIXED` is identified as an emitted label outside the specified verdict set. The frozen resolved sample contains 12 such rows, not the review's stated 11: 9 have partial citations, 2 are supported after full member review, and 1 remains UNKNOWN. `mixed-sample.tsv` preserves all 12 IDs.

Card 9 is supported without an invented rule. The installed `init-system-helpers` version is `1.69~deb13u1`; the preserved exact-version source at `raw/helper-source.txt` lines 354–375 maps an active link to its marker, skips link creation when that marker exists, and describes the marker as storing the fact that enable previously ran. This establishes both sides of the reported collision: a record of the past under S2.2-6 and behavioural dependence under S2.2-1. The frozen inventory contains all 56 cited regular-file markers: 49 under `*.wants` directories and 7 root-level alias markers.

An independent whole-table membership scan reproduces 21 card-9 rows. Independent ledger counts reproduce card 1 = 115, card 7 = 4, card 9 = 21, card-1/card-7 overlap = 3, no card-9 overlap, and 137 distinct rows overall. The agreed sample independently totals 60 SUPPORTED.

All 149 sentence references in the 100 corrected sample-audit rows match their named canonical sentences in `../../SENTENCES.md`; all 14 quotations in `../RESULT.md` are exact. Independent SHA-256 verification matches all 1,042 recorded frozen-input digests. The correction's local evidence links resolve.
