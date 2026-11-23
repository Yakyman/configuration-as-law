# Review of cards 5 and 6

Scope: (not published: outside selected checks and direct evidence), `../../TEXT.md` Sections 2–5, `../../SENTENCES.md`, `../compare/STATS.md`, `../adjudication/HOLES.md`, `../adjudication/rows.tsv`, all 5212 rows of (not published: outside selected checks and direct evidence), and available inventory under `A3R/in/raw/`. No new experiment was performed.

## Card 5 — REFUTED

The exemptions describe the object's removal behaviour, not merely the word used in a filename or documentation. Accepting this card's own stated facts that removal disables functions, its examples satisfy the positive removal test and fail the qualifications of both proposed exemptions.

- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”

Each example is decided for its disputed index/database member, not indiscriminately for every sibling in its grouped directory. Function claims below are those recorded in the card and the corresponding `joined.tsv` and `../adjudication/rows.tsv` entries; this refutation does not independently establish every removal effect.

| Example ID | Name | Application of S2.2-2 |
|---|---|---|
| 1690bef9f5dd9343f83fb23d | /usr/lib/udev | If removal of hwdb.bin disables device-property/keymap/quirk lookups as stated, it MUST be recorded. |
| c6b3dd48abb80159fee9f231 | /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0 | If removal of loaders.cache prevents the installed image loaders being found as stated, it MUST be recorded. |
| d58e9992edcefd52310ad71a | /usr/lib/x86_64-linux-gnu/gtk-3.0/3.0.0 | If removal of immodules.cache disables module input methods as stated, it MUST be recorded. |
| 1ce57ed0757b9e9232133b56 | /usr/share/applications | If removal of mimeinfo.cache disables MIME-handler discovery as stated, it MUST be recorded. |
| a4de6292d1e78167decc7081 | /usr/share/mime | If removal of the shared MIME-info database disables file-type detection as stated, the operative database MUST be recorded. |
| 4510afc64020ce965c69c93a | /var/cache/man | If removal of index.db disables apropos and whatis as stated, those indexes MUST be recorded; this does not classify formatted-page caches identically. |
| 3c4a5ca44a8a5ebbd1c4566e | /run | If removal of udev/data strips device properties/tags needed for device operations as stated, that operative database MUST be recorded; unrelated runtime members are separate. |
| lived-t50ddcd97a8 | /usr/share/fonts/X11 | If removal of font indexes/alias maps prevents font lookup as stated, those indexes/maps MUST be recorded. |

Regeneration later does not make the stated immediate loss of function a mere slowdown. Conversely, if factual investigation showed a particular implementation continues the same operations more slowly, S2.2-5 supplies its exemption. No precedence rule between a mere name and behaviour is missing.

## Card 6 — REFUTED as a demonstrated hole; examples yield ?

The suggested logical contradiction is not present: S2.2-2 is a sufficient positive test, not a biconditional. Failure to observe a change on removal does not itself decide NOT, while asserting that behaviour depends equally on a redundant individual copy is not established merely by identifying it as a trust input.

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S3-2: “If what the object does remains unknown, the case yields ?.”

An operative duplicate trust input could expose a missing classification if individual removal leaves all functions unchanged and neither another positive rule nor an exemption decides it. The supplied records do not establish those facts for this certificate; this conditional observation is not counted as a demonstrated hole.

The five examples in `redundancy_unknown.tsv` are exactly the five rows that explicitly contain the claimed local certificate or its trust-store link, directly or through their listed directory members. `redundancy_raw.tsv` extracts every matching ISRG path from the six-field, NUL-delimited filesystem inventory. It shows the local certificate, the local PEM symlink, the distribution certificate, and the distribution certificate's PEM/hash links. It does not contain certificate bytes, fingerprints, effective trust-store queries, or a rehash transcript proving that the local certificate was skipped as a duplicate. The absence of 4042bcee.1 alone cannot prove identical certificates or identical trust effect.

The statement about rehash skipping a duplicate occurs in `../adjudication/rows.tsv`; it is not supported by an included raw command result. A search of every available raw output for certificate PEM blocks, 4042bcee, the local certificate name, and a duplicate-skipping message found only the filesystem inventory. Therefore S3-2 literally decides each supplied example as ? (UNKNOWN): for f1dd4152b042e843dfb15c5c, the local certificate’s operative duplication is not established; for 4ea154d98eaad2618e7296f8, the local PEM link points to that same unverified certificate; for df8029550d37b2b3e98149c3, df85b130531509e4f79cd4b1, and 2f41a4b31ef3629ad27efa7b, the disputed member is that same certificate nested inside the listed directory members. Card 6 is REFUTED as a demonstrated hole in these supplied examples because the text supplies this procedural decision. This does not refute a hypothetical redundancy problem, prove NOT for the certificate, or assert any fact about the certificate’s contents to be false.

Whole-table search: every row's kind, name, and both reasons was searched for certificate/trust/SSL/redundancy/duplication terms; matches are recorded in `redundancy_search.tsv`. Additional name searches included backup/copy suffixes and all ancestor directory names. The table has no separate stored row for the packaged ISRG certificate; `/etc` does not list `/etc/ssl` as a member, and `/` does not list `/usr` or `/etc` as members. These broad directory names therefore do not add rows. The five candidate memberships are 2 differing decisions and 3 matching MIXED decisions; all five were adjudicated. Other TLS/PKI/key rows have no evidence of redundant trust and are not added to this card; ordinary duplicate programs are directly covered by the program/code rules, and stored historical backups have an explicit history exemption.

This question concerns whether an object must be recorded, not the design of state handling, rollback or declaration syntax. S2.5 does not settle that classification. There is no confirmed redundancy extent file: `redundancy_unknown.tsv` explicitly separates the five unverified candidates from confirmed holes.
