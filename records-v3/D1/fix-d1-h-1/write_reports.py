from pathlib import Path
import csv,json,re
P=Path('D1/fix-d1-h-1');s=json.loads((P/'summary.json').read_text());old=(P/'RESULT.before.md').read_text()
quotes={}
for line in Path('SENTENCES.md').read_text().splitlines():
 m=re.match(r'- \*\*(S[\d.]+-\d+)\*\* (.*)',line)
 if m:quotes[m[1]]=m[2]
def q(id):return id+': “'+quotes[id]+'”'
result='''CHECK 1: 4 confirmed holes
OUTCOME: 0

Recorded 2026-11-22 UTC. Fix round 1; the published definitions and failure conditions are unchanged.

The Section 4.1 adjudication record yields 0 on Fedora, Tumbleweed, Mint and Flatcar; Talos has no inventory and yields ?. The verification below is a separately labelled audit of those records, not a replacement adjudication or a new outcome rule. It confirms four kinds of gap. The source adjudication still contains eight cards and 924 HOLE rows; its files are frozen.

## Inventory, agreement and recorded case outcomes

Unchanged metrics: `D1/compare/STATS.md`, `D1/review/statistics.json`. The outcome column now preserves the adjudication cases. The verification column is a separate enumeration from `D1/fix-d1-h-1/confirmed-rows.tsv`; it includes matching objects found outside adjudicated rows and counts root/user inventory rows separately.

| Machine | Objects | Matching | Matching share | Cohen’s kappa | Adjudicated | Verification confirmed rows | Outcome |
|---|---:|---:|---:|---:|---:|---:|:---:|
| fedora | 5887 | 5444 | 92.47% | 0.54997 | 455 | 496 | 0 |
| tumbleweed | 6779 | 6542 | 96.50% | 0.78126 | 490 | 314 | 0 |
| mint | 2031 | 1816 | 89.41% | 0.44824 | 250 | 132 | 0 |
| flatcar | 1827 | 1223 | 66.94% | 0.30104 | 648 | 193 | 0 |
| talos | 0 | 0 | — | — | 0 | 0 | ? |
| TOTAL | 16524 | 15025 | 90.93% | 0.55586 | 1843 | 1135 | 0 |

Original adjudication counts, unchanged:

'''
start=old.index('| Machine | RESOLVED:MUST');end=old.index('\nThe resolved sample adds')
result+=old[start:end]+'\n\n'
result+='''The revised explicit UNKNOWN set has 97 rows: Fedora 11, Tumbleweed 5, Mint 13, Flatcar 68. Kinds: 67 stored-object groups, 13 dpkg packages, 12 RPM packages, three Flatpak packages, two processes. `D1/fix-d1-h-1/final-unknown.tsv` lists each id and reason. Compared with 114: remove two alsa-sof-firmware rows whose uncertainty is textual, remove 19 Mint rows whose supposed missing fact was only the discarded metadata criterion, and add four QML package rows whose actual execution privileges remain unestablished after discarding that criterion. Keep the original 89 UNKNOWNs, three failed sample factual premises and the genuinely incomplete `/etc/udev` contents. Broad search membership uncertainty is not automatically an object UNKNOWN.

'''+q('S3-2')+'''

## Verification: confirmed holes

The four gaps below are missing distinctions, not claims that two unconditional sentences always collide. Sentences used in the gap analyses are quoted exactly here:

'''+ '\n\n'.join(q(i) for i in ['S2.2-1','S2.2-2','S2.2-4','S2.2-7','S2.2-13','S2.2-16'])+'''

### 1. Shared presentation content versus loss of capability

Removing a shared font, translation or theme can mean losing particular presentation content or losing a rendering capability. S2.2-2, S2.2-4, S2.2-7 and S2.2-13 do not specify that boundary for these shared values.

Examples: `mint-854622d42bc8ca5d899db0ff` — root:fonts-noto-color-emoji; `tumbleweed-25d4e59fef6a08262890c4c4` — root:google-roboto-fonts; `fedora-e94d6040fe6b71468614c285` — user:adwaita-icon-theme-legacy. The first package's exact-version empty controls remain evidence (`D1/review/cards14-raw/mint-fonts-noto-color-emoji-control.json`); the other two are no longer rejected solely for Requires fields. Established extent: **410 rows**, all from original card 1 (Fedora 196, Tumbleweed 166, Mint 48). Three original rows with actual maintainer-script evidence are excluded by S2.2-10. A requirement for a shell is not itself evidence of a shell script.

### 2. Descriptive lookup content versus loss of capability

Removing a descriptive reference table can be described as losing particular answers or losing the ability to perform those lookups. S2.2-2 and the full condition of S2.2-4 do not distinguish these descriptions for the established data-only examples.

Examples: `mint-cef67297df4b26083898d0be` — root:libdrm-common, GPU names; `tumbleweed-856378d1c349da9571edbf48` — root:poppler-data, character mappings; `fedora-1616320aeaca00e35b428e9b` — user:ncurses-base, terminal descriptions. This does **not** interpret S2.2-4 as an unconditional exemption for every database. Known trust and transport policies are separately decided from their operational function. Established extent: **151 rows** (Fedora 48, Tumbleweed 54, Mint 49): 145 original card-2 rows plus six additional locale, braille, dictionary and rendering-data rows. Of the 161 original rows, 15 have independent trust/transport or actual-script grounds and one (`/etc/udev`) has incomplete payload facts.

### 3. Dependency metadata and the scope of the removal test

Removing a dependency-only package leaves its selected programs available while changing what a later package transaction selects or retains. S2.2-1 and S2.2-2 do not settle whether that later selection change, including a relaxation of constraints, is the required loss of behaviour or capability.

Examples: `tumbleweed-8ffe304c89c8c7e36f097d58` — root:patterns-fonts-fonts; `fedora-acb86505aa1316e17254882c` — user:passwdqc; `fedora-fe662177103b7d48f6e25461` — user:default-fonts-syr. Both immediate-payload and later-transaction readings remain recorded, without selecting either. Established extent: **319 rows** (Fedora 196, Tumbleweed 88, Mint 35): all 127 original card-3 rows and 192 additional rows supported by the affected samples, their duplicate installed-package rows, or the two recorded factual accounts identifying dependency-only packages. This includes packages with exempt documentation or program-local values whose only proposed independent MUST ground was metadata.

### 5. Absent hardware and alternative execution environments

Support files for absent devices or another boot environment are inert with the observed environment held fixed but support operations if that environment changes. S2.2-2 and S2.2-16 do not say which environment belongs in the removal comparison.

Examples: `fedora-eaecd855d3b238f815d51e72` and `fedora-369a1218fca1b15b045403ef` — root/user:alsa-sof-firmware; `flatcar-148193fc319dd99b4186c9e5` — /boot/boot; `flatcar-2a8ca562df17fe66a53a012d` — /boot/flatcar/grub/x86_64-xen/macbless.mod. The first two rows' firmware role and absence of sound hardware are established in `D1/adjudication/rows.tsv`; the question is textual, so S3-2 cannot dispose of it. The same gap applies to platform-specific boot support and CPU microcode, not just attachable peripherals. Established extent: **255 rows** (Fedora 56, Tumbleweed 6, Flatcar 193): 58 original card-5 rows, four CPU-microcode package rows, 192 Xen-directory/module rows and `/boot/boot`. There is no new hardware experiment or new inventory object.

### Extent evidence and limits

`D1/fix-d1-h-1/recompute.py` searches the entire frozen joined table by kind and name for all four confirmed cards. `confirmed-rows.tsv` enumerates 1,135 distinct established rows with facts and evidence; `extent-search.tsv` retains every match and exclusion, including matches beyond the original adjudication. The four established sets are disjoint in this enumeration. There are also 920 unresolved **row/card search memberships**, not 920 additional confirmed holes or UNKNOWN objects: a name match alone supplies neither payload facts nor a deciding sentence. Thus 1,135 is the exact enumerated established extent, not an assertion that all other objects are outside the gaps. The broader search is intentionally retained instead of claiming complete negative knowledge from names.

The original card facts in `D1/adjudication/rows.tsv` are used as recorded evidence. This fix does not repeat all earlier package-file investigations. Missing exact dependency metadata no longer overturns an established payload fact. Direct maintainer-script evidence remains independently usable under S2.2-10; outgoing requirements, recommendations, reverse requirements, Supplements, and Essential fields are no longer treated as a blanket deciding rule.

## Other original cards

Original-card verification dispositions: **four CONFIRMED, two REFUTED, two FACT-WRONG, zero OUTSIDE**. `D1/fix-d1-h-1/card-audit.md` gives the renewed challenges; the unchanged factual portions of `D1/review/cards-1-4.md` and `cards-5-8.md` remain evidence, subject to the procedural deviation below. Their superseded metadata conclusions and old extents are not current results.

- Card 4 — REFUTED: S2.2-7 says in force only inside one program, not merely read by one program; established login-session, subprocess and installed-file-label effects satisfy S2.2-1. Original examples remain individually explained in `D1/review/cards-1-4.md`.
- Card 6 — REFUTED: the examples are established operational inputs under S2.2-1; automatic regeneration supplies no exemption. S2.5-3 separately leaves declaration form to design. Each original example is retained in `D1/review/cards-5-8.md`.
- Card 7 — FACT-WRONG as the asserted universal collision: the browser/bridge separation, restricted XSLT operations and lens primitives do not establish the same program's unrestricted rights plus confinement. Saved primary sources are `D1/review/raw/cockpit-development.html`, `libreoffice-xslt.cxx`, `augeas-lenses.html` and `qt-untrusted.html`, with URLs in `sources.json`. Withdraw the independent MUST claim for all 14 packages; four QML package rows remain UNKNOWN because generic QML documentation does not establish actual installed scripts' privileges. This factual rejection is not a blanket package classification.
- Card 8 — FACT-WRONG for the code-only premise of descriptor-bearing packages; the guest-code collision is REFUTED by the explicit S2.2-11/12 exemption. SeaBIOS/OVMF host-read descriptors remain a separate operational function, as recorded in `D1/review/cards-5-8.md`. For ipxe-roms-qemu and seavgabios-bin, guest-only code remains exempt; no reverse-dependency MUST rule is applied. Finding 6's inconsistency is removed by dropping that ground everywhere, not by selectively ignoring these two dependencies.

'''+ '\n\n'.join(q(i) for i in ['S2.2-10','S2.2-11','S2.2-12','S2.5-3'])+'''

## Seeded samples: revised verification

The samples and ordered ids are unchanged: Python `random.Random(seed).sample`, source-order populations, tab delimiter with `csv.QUOTE_NONE`. The fix changes the assessments only. New per-row records are `D1/fix-d1-h-1/resolved-sample.tsv` and `agreed-sample.tsv`; reasons are in `sample-audit.md`. Original citations and factual records remain in the corresponding `D1/review/` sample files.

| Sample | Population | Seed | Drawn | Upheld | Confirmed candidates in existing cards | OUTSIDE | UNKNOWN | New gap types |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RESOLVED:* | 888 | 2026112201 | 40 | 10 | 20 | 7 | 3 | 0 |
| Agreed, not adjudicated | 14681 | 2026112202 | 60 | 57 | 3 | 0 | 0 | 0 |

The resolved sample's nine metadata-based corrections now join card 3; ten Xen/menu rows and microcode_ctl join card 5. This applies the finding to every sampled row with the same reasoning, not only the three Xen rows named by review. The three formerly corrected agreed packages join card 3. No drawing or inventory attempt was repeated. Per-machine sample sizes remain Fedora 6/26, Tumbleweed 6/24, Mint 7/7, Flatcar 21/3, Talos 0/0 (resolved/agreed).

Seven OUTSIDE candidates concern program-state bookkeeping or a private temporary directory; this is not a universal NOT-recorded rule. The merged process record and two unestablished SELinux consumers remain factual UNKNOWN. The unchanged firewall correction still uses the existing jump target as the deciding fact.

'''+q('S2.5-1')+'''

## Procedure and evidence deviations

The earlier verification read and relied on `D1/adjudication/work/`, although the task named only its public hole/row outputs and the inventory. This breached the folder restriction in `COMMON.md`; it is recorded here rather than silently relabelling those reads as authorized. Prior reports preserve the affected references (dependency extracts, file lists, package indexes and a decision script). This round did not read that work folder, did not read c1/c2 folders, and did not claim an independent new fetch of those facts. Retained descriptor and unchanged payload evidence from the earlier reports carries this provenance limitation. This is the deviation-recording alternative requested in review finding 7.

The previous result is retained at `D1/fix-d1-h-1/RESULT.before.md`. New outputs are under `D1/fix-d1-h-1/`; `input-sha256.json` and `raw/recompute.txt` verify that 1,668 frozen files remained unchanged. Only affected assessments, extents, UNKNOWN membership and outcome reporting were recomputed. No VM, build, installation, inventory, removal probe, public upload or failure-condition change was performed. Independent acceptance belongs to the subsequent review; these consistency checks are not acceptance of the fix.

'''
# Preserve unchanged committed-input/coverage disclosure from the previous result.
tail=old[old.index('## Inventory limits and committed-input deviations'):]
tail=tail[:tail.index('\nQuote validation:')]
result+=tail+'''\n\nQuote validation: `/usr/bin/python3 -I bin/check_quotes.py D1/RESULT.md`; output is in `D1/fix-d1-h-1/raw/quotes-result.txt`. Corrected counts and unchanged ordered samples are in `raw/recompute.txt`.\n'''
Path('D1/RESULT.md').write_text(result)
fix='''# FX-D1-H-1 — response to review

Recorded 2026-11-22 UTC. Result: **CHECK 1: 4 confirmed holes; OUTCOME: 0**. Execution and consistency checks are complete; subsequent independent review performs acceptance.

| Finding | Disposition | Correction or evidence |
|---|---|---|
| 1 — adjudication outcomes | FIXED | The result now reports Fedora/Tumbleweed/Mint/Flatcar 0 and Talos ?. The eight-card/924-row original adjudication is preserved and the four-card verification is separately labelled. No new override stage or failure condition is asserted. |
| 2 — metadata decides MUST | FIXED | Removed the blanket ground everywhere, including cards 1/2/5/7 and both samples. A dependency field does not establish the actual removal loss or executable script. Recomputed all four confirmed-card extents, retaining direct script/trust evidence separately. `confirmed-rows.tsv`, `extent-search.tsv`, `card-audit.md`. The review's universal assertion that dependency removal stops nothing is not adopted as a NOT rule either; the text's scope remains unresolved. |
| 3 — card 3 refutation | FIXED | Card 3 CONFIRMED: S2.2-1/S2.2-2 do not decide between runtime removal and later transaction selection. 319 established rows, including all 127 original rows. No immediate-only or later-run rule is added. |
| 4 — hardware ambiguity called UNKNOWN | FIXED | Card 5 CONFIRMED. Both alsa-sof-firmware rows leave UNKNOWN, as their roles and device absence are in the allowed adjudication notes. Applying the same correction to metadata-only UNKNOWNs and QML facts gives 97, not merely 112: 114 − 2 − 19 + 4. `final-unknown.tsv` identifies every retained/additional case. |
| 5 — Xen sample | FIXED | All ten Xen/menu sample rows plus microcode_ctl are CONFIRMED card-5 candidates. Resolved sample now 10 upheld, 20 confirmed candidates, 7 outside, 3 UNKNOWN. Seeds and ordered ids unchanged. `sample-audit.md`, `resolved-sample.tsv`. |
| 6 — guest-ROM dependency inconsistency | FIXED via the offered alternative | Drop metadata MUST everywhere. Do not add card 8 as a confirmed collision merely from those reverse dependencies: S2.2-11 and S2.2-12 explicitly call guest-confined code an exemption. Host-read descriptors remain a distinct package fact. The finding correctly identifies inconsistency; its first suggested remedy is unnecessary after its second remedy is applied. `card-audit.md` and RESULT's Card 8 discussion. |
| 7 — out-of-scope folder reads | FIXED disclosure; historical deviation cannot be undone | RESULT explicitly records the earlier reads of the adjudication work folder and the provenance limitation of retained evidence. No such folder was read this round, and no replacement public fetch is claimed. This uses the review's requested deviation-recording alternative. |
| 8 — headline count | FIXED | Four confirmed cards: 1, 2, 3, 5; two refuted: 4, 6; two fact-wrong: 7, 8. 1,135 established rows enumerated; broad unresolved search memberships kept separate. Overall outcome remains 0. |
| 9 — verified figures and claims | NOT CHANGED where unaffected | Inventory/decision metrics, ordinary-action counts, missing Talos data, emoji package version, process merge and saved factual evidence remain as verified. Old 114-row UNKNOWN and old sample disposition totals described the previous files correctly but are superseded by the corrections above. `RESULT.before.md` preserves that version. |

All paths in this table without a prefix resolve under `D1/fix-d1-h-1/`. The full revised result is `D1/RESULT.md`.

## What was rerun

Only the changed verification derivations: `recompute.py` generates revised sample decisions, whole-table extent searches, established membership, UNKNOWN ids and summaries into this new directory. The same ordered draws are checked, never replaced. Original metrics are retained from the already verified statistics; no VM or removal/inventory probe was run.

`input-sha256.json` covers 1,668 frozen input/evidence files. `raw/recompute.txt` records the counts and successful unchanged-hash check. Exact quote validation of the updated result and this response is saved in `raw/quotes-result.txt` and `raw/quotes-fix.txt`.

## Limits retained rather than repaired

The established extent is an enumerated set, not a claim that all broad kind/name matches are proved negative. `extent-search.tsv` has 920 unresolved row/card search memberships; these are neither extra confirmed rows nor automatically UNKNOWN objects. Existing factual accounts, rather than new package investigations, supply the unaffected payload evidence. The text alone must decide the four remaining gaps; no wording or rule has been added to it.

The prior verification's procedural breach remains in the record. The correction records it and does not certify the old evidence as newly obtained within scope. Independent acceptance remains with the next review.
'''
Path('D1/FIX-D1-H-1.md').write_text(fix)
# Preserve unresolved readings as questions, with no proposed wording changes.
(P/'QUESTIONS.md').write_text('''# Textual readings left undecided\n\nRecorded 2026-11-22 UTC. These are recorded questions, not decisions or proposed amendments.\n\n- Does losing particular shared presentation or lookup values count as losing content or losing capability? Cards 1 and 2 retain both readings.\n- Does changed later package selection satisfy the removal test when the payload capabilities remain? Card 3 retains both readings.\n- Does the removal comparison keep the observed hardware/platform fixed or admit another supported environment? Card 5 retains both readings.\n''')
print('Wrote RESULT.md, FIX-D1-H-1.md and question record.')
