# Independent verification of D1/RESULT.md

Verified against (not published: orchestration or scratch), (not published: orchestration or scratch), Sections 8 and 9 and Appendix A.4.1 of `TEXT.md`, `SENTENCES.md`, the comparison and adjudication tables, the two sample records, and the reproducible review outputs.

- The reported result is consistent: 0 confirmed gaps, with outcome `?` under both readings A and B because fact-limited cases remain and Gentoo has no inventory.
- Counts reproduce: 16,375 objects; 8,677 matching decisions (52.99%); kappa 0.45940; 7,708 adjudicated rows; and the stated per-verdict and per-machine totals.
- The original unresolved set has 937 distinct rows. The 1,070 non-overlapping additions contain 1,069 old-kernel rows and one dconf row, giving an identified union of 2,007 rows.
- The revised card 2 analysis applies Q3 before Q4, retains the dconf row as FACT_UNKNOWN, and no longer assigns a blanket RECORD verdict to generated non-code data. Its refutation of the asserted S8.2-16 conflict remains valid.
- Cards 4 and 5 consistently distinguish an archive or installed package from executable code contained inside it. Their stated dispositions do not transfer a member-code decision to the enclosing object.
- Both seeded samples, the whole-table candidate extents, and all required report sections are present. Quote validation reports 20 checked and 0 missing.

No remaining blocking finding.
