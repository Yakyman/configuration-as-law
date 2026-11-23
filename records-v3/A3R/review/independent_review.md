# Independent review

Scope: the fixed text, the numbered sentences, the three review analyses, both fixed samples, and the consolidated result. No new cases or probes were added.

## Accepted reasoning

- Card 1 establishes a literal collision between S2.2-5 and S2.2-10 for executable caches with a demonstrated source fallback. The narrowed extent is 115 represented rows. This count is acceptable only with the stated qualification: a source/compiled pair establishes an operation that can start the cached code and fall back to the source; it does not establish that every module ran during inventory. Unpaired compiled objects and objects without fallback remain unknown rather than additional holes.
- Card 7 establishes the analogous collision between S2.2-6 and S2.2-10 for saved history restored by executing editor code. Its seven rows are represented ancestor/subtree rows for two concrete saved-code families, not seven independent mechanisms. S2.5-1 does not remove the simultaneous obligations created by the explicit history exemption and code rule.
- Cards 2, 3, 4, 5 and 8 are refuted by the positive removal/code rules or by the qualifications within the asserted exemptions. Card 6 is not demonstrated by the available certificate evidence and therefore yields `?` under S3-2 rather than a confirmed redundancy hole.
- In the agreed sample, 59 of 60 rows are supported on the recorded facts. The Go and Mesa cache rows do not demonstrate unrestricted execution and therefore do not reproduce card 1. Agreed sample 7 is program state outside the definition under S2.5-1, so the two matching `MUST` decisions do not make that row correct.

## Findings and limits

- The resolved sample supports 26 adjudications as written, subject to quotation corrections below. Nine mixed plugin rows have an incomplete resolving citation: S2.2-10 supports their `MUST` members, while their `NOT` members require S2.2-4 and/or S2.2-7. These records do not satisfy the requirement to quote the sentence that resolves the whole dispute.
- Four resolved rows lack enough functional evidence: samples 4, 15 and 16 establish unavailable package metadata, but no non-content operation depending on those particular files; sample 12 does not establish whether the manifest merely describes files or governs updater/uninstaller effects. S3-2 decides these members as `?`.
- Resolved sample 38 is factually wrong: the saved sources distinguish a value-parsed Fontmap from a cidfmap path that is converted and executed. S2.2-13 resolves the distinction; the categorical values-only `NOT` rationale cannot stand.
- Fifteen of 40 resolved-sample quote fields are not exact full sentences: 2, 7, 8, 9, 13, 14, 19, 22, 23, 25, 26, 29, 31, 37 and 39. Nine are the mixed-row coverage defect above. The other six contain missing terminal text or punctuation, and samples 9 and 29 substitute an ellipsis. The immutable input remains unchanged; `sample_audit.tsv` supplies the exact full sentences and `../RESULT.md` records all 15 defects.
- The 115-row card-1 extent must not be described as 115 independent executable files or observed executions. It counts inventory rows, including ancestors that share witnesses. Card 7 has seven rows, six overlapping card 1, for 116 distinct rows across the two cards.

## Review verdict

The evidence supports two confirmed definition collisions, cards 1 and 7, and no other confirmed card. `../RESULT.md` incorporates the reviewed sample corrections, reports 115 card-1 rows plus seven card-7 rows with six overlaps, and preserves the extent qualifications. Its outcome `0` and its consolidated counts are accepted.
