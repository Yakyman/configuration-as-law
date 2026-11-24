"""Apply round-2 report corrections to the saved round-1 result."""
from pathlib import Path
p=Path('D1/RESULT.md')
s=Path('D1/fix-d1-h-2/raw/RESULT.before.md').read_text()
s=s.replace('CHECK 1: 1 confirmed gaps','CHECK 1: 3 confirmed gaps',1)
s=s.replace('corrected by FX-D1-H-1','corrected by FX-D1-H-2',1)
s=s.replace('the archive-of-code gap also survives verification.','three gap kinds survive verification: generated lists, executable-content archives, and installed contained-code packages.',1)
s=s.replace('Corrections and changed checks are in `D1/fix-d1-h-1/`; the earlier report is preserved as `raw/RESULT.before.md` there. `D1/FIX-D1-H-1.md` answers each review finding.', 'Round-1 records remain in `D1/fix-d1-h-1/`. Round-2 corrections and changed checks are in `D1/fix-d1-h-2/`; its `raw/RESULT.before.md` preserves the preceding report. `D1/FIX-D1-H-2.md` answers every round-2 review finding. New scripts `scan.py` and `build-extents.py` use saved inputs, with no probes, machine runs or resampling. The new `raw/whole-table-search.tsv` records all 16,375 kind/name searches; `raw/candidates.tsv` retains broad matches. Confirmed extents are separated from unresolved extent candidates; an opaque inventory cannot establish that no other affected objects exist.')
s=s.replace('**3 REFUTED cards, 1 FACT_UNKNOWN card, 0 FACT-WRONG, 0 OUTSIDE, 1 CONFIRMED**','**1 REFUTED card, 1 FACT_UNKNOWN card, 0 FACT-WRONG, 0 OUTSIDE, 3 CONFIRMED**')
a=s.index('`D1/fix-d1-h-1/raw/gap-row-dispositions.tsv` gives');b=s.index('### UNKNOWN rows',a)
s=s[:a]+'''`D1/fix-d1-h-2/raw/gap-row-dispositions.tsv` gives every one of the 1,364 original GAP ids exactly one status. These are row dispositions after verification, not edits to the adjudication.

| Status after correction | Rows | Scope |
|---|---:|---|
| CONFIRMED generated-list gap | 64 | 63 original card-2 rows and Void `/etc` from card 1, specifically its `ld.so.cache` member. |
| CONFIRMED archive gap | 9 | Card 4; Void `/boot` also has fact-limited old-package members. |
| CONFIRMED installed contained-code gap | 2 | Both installed XPI rows of card 5. |
| FACT_UNKNOWN without a confirmed gap | 1,069 | Card 3's 1,068 rows and card 2's dconf row. |
| UNDECIDED:row-audit | 220 | 213 card-1 rows and 7 card-2 certificate/policy rows; no final aggregate verdict is claimed. |
| **Total** | **1,364** | Every original GAP row retained. |

The whole-table generated-list search also confirms 36 rows outside the original GAP population. Together with the 75 confirmed rows in this ledger, the three cards cover **111 distinct confirmed rows**. `raw/changed-counts.json` records the counts; `raw/card2-original-rows.tsv` explains all 71 original card-2 rows. Card-level confirmation does not certify all original members, and an unfinished row audit is not automatically factual uncertainty. The earlier identified fact-limited total of 2,007 and its one-row overlap with card 4 remain historical counts; additional extent fact limits found in this round are reported separately below, not silently merged into that total.

''' +s[b:]
a=s.index('## Confirmed gaps');b=s.index('## Card dispositions',a)
s=s[:a]+'''## Confirmed gaps

### Card 2 — A list the system generated from installed packages

Q4 calls the generated non-code cache a program record that need not be recorded, while S8.2-16 names a generated list among what is installed and recorded through a source line. Reading S8.2-16 as only supplying a line after classification avoids that conflict, but the text does not select that reading over the reading that its own example is installed.

**Type:** two sentences collide, S8.2-15 and S8.2-16, with opposite recording obligations under S8.2-2 and S8.2-1. Exact quotes appear below. S8.2-6 orders the four questions; it does not expressly rank the separate recording-line paragraph against Q4. The refutation is withdrawn without adopting either reading; both are in `D1/QUESTIONS.md`.

**Competing decisions:** RECORD permits omission. INSTALLED-DERIVED requires representation through a line from which the system built or obtained the list; the line specifies the required state. This does not add the original card's stronger requirement that every generated artifact must exist whenever any source package exists.

**Established extent:** **100 rows: AlmaLinux 38, Void 28, MicroOS 34, Talos 0; Gentoo no inventory.** All ids, names, affected members and evidence are in `D1/fix-d1-h-2/raw/card2-extent.tsv`. Of these, 63 belong to the original card-2 set; 37 are outside it: 30 AlmaLinux manual-page index buckets, 3 GRUB list buckets, MicroOS's loader-cache bucket and active RPM database, and Void's `/etc` and XBPS database buckets. The search is independent of adjudication status and includes agreements. Mixed rows are counted once when they contain an affected member.

Examples: `alma-889f8cd2dae65a248533322a`, `/usr/lib/modules/6.12.0-264.16.1.el10_3.x86_64` (the ten depmod lists, not its unchanged package members); `microos-a1f877f4c02acd2a5f9a0d97`, `/usr/share/mime`; `void-4ab73c90e99c24b1fb10c341`, `/usr/share/mime/application`; `alma-3827efd6d880bbf3bcd0736f`, `/var/cache/man/id` (the existing agreement sample).

**Extent limits:** the original dconf row remains FACT_UNKNOWN; four certificate and three policy rows remain without a completed aggregate verdict. Five further extent candidates have missing source/content facts: the inactive MicroOS RPM database, three fontconfig buckets and MicroOS's `@System` solver cache (`generated/dispositions.tsv` and `generated/assessment.md`). These are not counted as confirmed conflicts. The inactive RPM row was in the resolved sample and is now FACT_UNKNOWN there. Neither a cache filename nor the confirmed card permits guessing the missing source facts. The evidence-supported extent is enumerated; unresolved candidates prevent a claim of a closed census of every possible generated list.

### Card 4 — A stored archive whose contents are executed

The computer extracts a generated initramfs archive and executes its contents, but Sections 8.1–8.2 do not decide whether the stored archive itself is code executed through another program. Separating extraction from execution supports the record reading, while treating the stored executable contents as code supports the program reading; the text supplies no boundary that selects one.

**Type:** missing distinction in S8.2-9/23, not a new fact and not a design question under Section 8.5. S8.2-15 supplies the record branch if Q2 is negative; S8.2-10/16 supply the program and its source-line recording if Q2 is positive. The fixed order S8.2-6 cannot decide whether Q2 is affirmative for this representation. Exact quotes appear below.

**Competing decisions:** PROGRAM-DERIVED requires recording through the line from which it was built, with its required state specified by that line; RECORD permits omission under S8.2-2/15.

**Established boot-archive extent:** **9 rows: AlmaLinux 4, Void 4, MicroOS 1, Talos 0; Gentoo no inventory.** Exact ids and members are in `D1/fix-d1-h-2/raw/card4-boot-extent.tsv`. The boot pattern is limited to `initramfs-*.img` and `initrd-*` names under `/boot`, including snapshot paths; it excludes symlinks. The new script has no equality-to-original-ids assertion. Its unconstrained result happens to equal the nine original rows.

The broader kind/name/member search found 265 archive-family candidates, discussed in `D1/fix-d1-h-2/archive/assessment.md`. The two installed XPI rows share this archive/content boundary and are counted separately under card 5 because their recording conflict differs. Two downloaded XPI copies do not add the mandatory-versus-optional conflict: the material reading permits omission, as does the qualifying contained-code reading under S8.2-21. Logical container images and opaque stores do not establish a stored archive's representation or complete contents. The report therefore claims nine confirmed boot rows, not an exhaustive census of all stored executable archives; missing representation/contents remain factual limits.

### Card 5 — An installed package whose code runs only inside its program

Q1 classifies the permanently installed XPI as an installed package, for which S8.2-1 requires recording. If its contained executable code makes the archive itself qualifying code under S8.2-21, that sentence permits omission, and the text does not settle the archive/content boundary or the resulting recording conflict.

**Type:** collision between S8.2-1 and S8.2-21, dependent on the missing boundary in card 4. S8.1-5/6 and S8.2-7/8 establish the package branch; S8.2-6 fixes classification order but does not resolve this recording obligation. Exact quotes appear below. This is a separate recording conflict, not a second count of the nine initramfs rows.

**Competing decisions:** INSTALLED-OWN requires recording the installed package, with an own line available under S8.2-16; the qualifying contained-code reading permits omission under S8.2-21. No assertion that the extension can launch a native program is needed.

**Established extent:** **2 rows: AlmaLinux 1, Void 1, MicroOS 0, Talos 0; Gentoo no inventory.** `alma-2ea4b9f74eb9ce06f9d317ff` and `void-61a9a88ad2b852b6cf106db6`, both named `/home/user/.mozilla/firefox/cal-check/extensions`, contain the permanently installed XPI. Evidence and excluded downloaded copies: `D1/fix-d1-h-2/raw/card5-extent.tsv`, `raw/xpi-search.tsv`, `archive/assessment.md`, and the unchanged `D1/review/extension-evidence.json`.

''' +s[b:]
s=s.replace('- **Card 2 — REFUTED:** S8.2-16 selects a line for what is already installed; it cannot create the asserted INSTALLED-DERIVED alternative. Q3 still decides settings before Q4 decides caches, with missing contents/use facts retained as unknown.','- **Card 2 — CONFIRMED:** the former refutation selected one reading of S8.2-16; the generated-list/record collision remains, with row-specific factual limits.')
s=s.replace("- **Card 5 — REFUTED:** the permanently installed XPI is a package under S8.1-5/6 and Q1; S8.2-21's exemption for qualifying code does not exempt the enclosing installed package.",'- **Card 5 — CONFIRMED:** Q1 establishes installed-package classification but does not settle the S8.2-1/21 recording conflict under the unresolved archive/content reading.')
a=s.index('### Card 2: refutation');b=s.index('### Card 3:',a)
s=s[:a]+'''### Card 2: corrected named-example reasoning

The former categorical refutation is withdrawn. The heading `Which line records an object.` supports the prior reading of S8.2-16, but does not eliminate the competing reading of its generated-list example. S8.2-6 does not supply an explicit priority between that paragraph and Q4. This is treated consistently with card 4: record the unresolved readings without choosing one.

| Named example | Corrected disposition |
|---|---|
| `microos-a1f877f4c02acd2a5f9a0d97`, `/usr/share/mime` | CONFIRMED for the generated database members: record versus installed generated list. |
| `void-4ab73c90e99c24b1fb10c341`, `/usr/share/mime/application` | CONFIRMED for the 505 generated MIME data files. |
| `void-f2e5d5edfa5902c8aee7bace`, `/etc/ssl/certs` | No definitive replacement of the withdrawn trust-setting claim. Generation does not establish Q3's facts or an optional-record branch for all trust values; row audit remains undecided. |
| `microos-dcce813055fa256ed012c87a`, `/var/lib/ca-certificates/openssl` | Same certificate limitation; no blanket confirmation or setting verdict. |
| `microos-c111706edb49a56b42b0ff18`, snapshot `/etc` | CONFIRMED for generated `ld.so.cache`; other members keep their separate facts/classes. |
| `alma-889f8cd2dae65a248533322a`, kernel module directory | CONFIRMED for 10 depmod-generated `modules.*` lists. The 19 unchanged package members retain Q1. |
| `void-982c71cf468c85befb1aa508`, `/var/cache/ldconfig` | CONFIRMED for the generated auxiliary cache. |
| `alma-caff428f8364f0a663721a85`, `/etc/dconf/db` | FACT_UNKNOWN: the compiled values' contents/use are still needed for system/launch/access settings versus personal-program records. |
| `microos-2ce40b9afb2194333071f853`, snapshot SELinux active store | Known access-policy values meet S8.2-13; the aggregate row and ancillary representations are not certified as optional records. Retain the row-audit limitation. |

Evidence: named member inventories, `D1/adjudication/raw/l2o_member_classes.tsv`, `D1/adjudication/rows.tsv` notes and `D1/adjudication/parts/{l1-microos,l2-other}.facts.md`. New `raw/card2-original-rows.tsv` covers every original row, including the other certificate/policy limitations. The whole-table search adds the confirmed members listed in `raw/card2-extent.tsv`; the eight-row database/font-cache assessment is in `generated/assessment.md`. No certificate setting classification is restored, and no new rule makes all generated bytes installed.

''' +s[b:]
s=s.replace('S8.2-16 cannot itself make the archive code: it selects a line if the program reading is adopted.','Under the program reading, S8.2-16 provides the source-line option; it does not resolve the code/archive boundary.')
s=s.replace('member inventories named in `card4-extent.tsv`','member inventories named in `D1/fix-d1-h-2/raw/card4-boot-extent.tsv`')
a=s.index('The strongest contrary reading applies');b=s.index("The card's permissions premise",a)
s=s[:a]+'''The previous refutation separated the installed archive from its contained code, although that boundary remains undecided for card 4. Q1 does decide the installed package's class; it does not resolve whether S8.2-21 also applies to that same stored object under the other boundary reading. Neither S8.2-6 nor the recording sentences supply a priority that closes this conflict. Both rows therefore return to CONFIRMED gap status. The refutation attempt and its failure are recorded without choosing either boundary.

''' +s[b:]
s=s.replace('both classifications', 'both classifications')
s=s.replace('38 supported verdicts; 2 incorrect homogeneous bucket verdicts, both REFUTED as gap candidates; 0 confirmed gaps; 0 FACT_UNKNOWN.','37 supported verdicts; 2 incorrect homogeneous bucket verdicts, both REFUTED as gap candidates; 1 FACT_UNKNOWN after the generated-list extent check; 0 confirmed gaps.')
s=s.replace('58 supported definite decisions; 2 FACT_UNKNOWN agreements retained; 1 of the 58 challenged as a generated-list candidate and REFUTED; 0 confirmed gaps.','57 supported definite decisions; 2 FACT_UNKNOWN agreements retained; 1 CONFIRMED generated-list gap (already counted under card 2).')
s=s.replace('The samples were not replaced after seeing their findings.', 'The samples were not replaced after seeing their findings. Those original audits remain frozen; corrected row checks, in the same draw order with the same ids, are `D1/fix-d1-h-2/raw/resolved-sample.tsv` and `raw/agreed-sample.tsv`. Only the two affected checks changed.')
s=s.replace('- **REFUTED sample candidate:** `alma-3827efd6d880bbf3bcd0736f`, `/var/cache/man/id`: both RECORD decisions are supported by Q4; the presence of generated `index.db` does not reverse S8.2-16. This tests card 2 beyond its adjudicated rows.', '- **CONFIRMED sample candidate:** `alma-3827efd6d880bbf3bcd0736f`, `/var/cache/man/id`: generated `index.db` supports the competing S8.2-15/2 and S8.2-16/1 readings. The old refutation is withdrawn; this row is included in card 2.\n- **New FACT_UNKNOWN sample check:** `microos-230864c607d1cffde69583f3`, inactive snapshot RPM database: full contents/source package set are not established by matching size and prefix digest. The former RESOLVED:RECORD support cannot exclude the generated-list conflict; see `D1/fix-d1-h-2/generated/assessment.md`.')
s=s.replace('output in `D1/fix-d1-h-1/raw/quotes-result.log`','output in `D1/fix-d1-h-2/raw/quotes-result.log`')
p.write_text(s)
