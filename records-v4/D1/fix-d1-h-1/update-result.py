"""Apply the documented fix to the preserved D1-H report, not to frozen inputs."""
from pathlib import Path

p = Path('D1/RESULT.md')
s = Path('D1/fix-d1-h-1/raw/RESULT.before.md').read_text()

def replace(old, new):
    global s
    assert old in s, old[:100]
    s = s.replace(old, new)

replace('CHECK 1: 0 confirmed gaps', 'CHECK 1: 1 confirmed gaps')
replace('Review of D1-H, recorded 2026-11-23 UTC. The outcome is **? under both readings A and B** in `C1/QUESTIONS.md`. Zero confirmed gaps is not an outcome of 1: missing inventory facts remain on every inventoried machine, and Gentoo supplied no inventory.', 'Verification D1-H, corrected by FX-D1-H-1 on 2026-11-23 UTC. The outcome is **0 under both readings A and B** in `C1/QUESTIONS.md`. The frozen adjudication satisfies the separate disagreement failure condition; the archive-of-code gap also survives verification. Missing facts remain, and Gentoo supplied no inventory.')
replace('The review used', 'The verification used')
replace('Original classifications and adjudication records were not changed.', 'Original classifications, adjudication and `D1/review/` outputs were not changed. Corrections and changed checks are in `D1/fix-d1-h-1/`; the earlier report is preserved as `raw/RESULT.before.md` there. `D1/FIX-D1-H-1.md` answers each review finding. The old `D1/review/verification.md` is an unsupported self-check, not evidence of independent acceptance; its corrected label and status are in `D1/fix-d1-h-1/verification.md`.')
replace('| ? | ? | No confirmed counterexample; 65 retained UNKNOWN rows plus one fact-limited dconf row identified during review. |', '| 0 | 0 | 179 disagreeing GAP adjudications; confirmed archive gap on 4 rows. Missing facts do not override a failure. |')
replace('| ? | ? | No confirmed counterexample; 75 retained UNKNOWN rows and 1,069 additional rows affected by unproved old-package provenance/integrity. |', '| 0 | 0 | 1,126 disagreeing GAP adjudications; confirmed archive gap on 4 rows, including a bucket also containing fact-limited old files. |')
replace('| ? | ? | No confirmed counterexample; 754 retained UNKNOWN rows, including active unit definitions and snapshot-file integrity. |', '| 0 | 0 | 57 disagreeing GAP adjudications; confirmed archive gap on 1 row. Partial L2 does not prevent 0. |')
replace('| **?** | **?** | No case establishes 0; cases with insufficient data remain. |', '| **0** | **0** | Three machines yield 0; Appendix A.4.1 combines them as 0. |')
replace('Reading B independently prevents 1 where coverage is partial; reading A does not cure the missing classification facts. Neither reading changes these outcomes.', 'Reading B independently prevents 1 where coverage is partial; reading A does not cure missing facts. Neither reading prevents 0 when the failure condition holds. Changed accounting: `D1/fix-d1-h-1/raw/failure-condition-rows.tsv` and `changed-counts.json`.')
marker = '## Counts\n'
replace(marker, '''Section 9.2, quote: “or the two classifications decided differently and the adjudication finds no sentence of the text that resolves the dispute.” Appendix A.4.1, quote: “if no sentence resolves it, the case yields 0.” The 1,362 disagreeing rows with frozen GAP verdicts meet this condition (179 AlmaLinux, 1,126 Void, 57 MicroOS); two further GAP rows have matching MIXED decisions and are not counted under this clause. D1-H's later refutations do not erase these recorded adjudication findings. Even under a reading that permits later verification to replace an adjudication finding, the confirmed archive gap independently gives the same machine and whole-check outcomes. No additional procedural rule is adopted, and neither the published text nor the failure condition is changed.

## Counts
''')
replace('not counts of confirmed gaps after review', 'not counts of confirmed gaps after verification')
replace('Review dispositions are **4 REFUTED cards, 1 FACT_UNKNOWN card, 0 FACT-WRONG, 0 OUTSIDE, 0 CONFIRMED**.', 'Verification dispositions are **3 REFUTED cards, 1 FACT_UNKNOWN card, 0 FACT-WRONG, 0 OUTSIDE, 1 CONFIRMED**.')
replace('### UNKNOWN rows and missing facts', '''### Accounting for every original GAP row

`D1/fix-d1-h-1/raw/gap-row-dispositions.tsv` gives every one of the 1,364 ids a status. Card refutations are not wholesale row resolutions. The exclusive accounting is:

| Status after correction | Rows | Scope |
|---|---:|---|
| CONFIRMED archive gap | 9 | Card 4; includes Void `/boot`, which also has fact-limited old-package members. |
| FACT_UNKNOWN without the confirmed archive gap | 1,069 | Card 3's 1,068 rows and card 2's dconf row. |
| RESOLVED:INSTALLED-OWN | 2 | Both card 5 installed-XPI rows. |
| UNDECIDED:row-audit | 284 | All 214 card 1 rows and the other 70 card 2 rows; no complete final row verdict is claimed. |
| **Total** | **1,364** | All original GAP rows retained. |

Of the review's 294 formerly unaccounted rows, 8 now have the confirmed archive gap and 2 the installed-XPI decision; **284 explicitly remain undecided at row level**. The named-example reasoning below applies only to the specified members or facts and does not close those 284 aggregate rows. This is an audit limitation, not a new classification or a replacement of their frozen GAP verdicts. Missing facts are not inferred merely from an unfinished audit. The separate fact-limited total remains 2,007, with a one-row overlap with the confirmed gap; these counts must not be added as disjoint populations.

### UNKNOWN rows and missing facts''')
replace('**None.** Consequently there are no confirmed titles, competing declarations, per-machine confirmed extents, or missing/colliding-sentence cases to report.', '''### Card 4 — A stored archive whose contents are executed

The computer extracts a generated initramfs archive and executes its contents, but Sections 8.1–8.2 do not decide whether the stored archive itself is code executed through another program. Separating extraction from execution supports the record reading, while treating the stored executable contents as code supports the program reading; the text supplies no boundary that selects one.

**Type:** missing distinction in S8.2-9/23, not a newly discovered fact and not a design question under Section 8.5. S8.2-15 supplies the record branch if Q2 is negative; S8.2-10/16 supply the program and its source-line recording if Q2 is positive. Their exact sentences are quoted below. The fixed order S8.2-6 cannot decide whether Q2 is affirmative for this representation.

**Competing decisions:** PROGRAM-DERIVED requires recording the generated program through the line from which it was built (S8.2-16), with that line specifying its required state; RECORD permits omission of the archive from the declaration (S8.2-2/15). Generation alone is not the reason for installed status. The difference is whether the archive must be represented, not a rule requiring every generated artifact whenever any source package is present.

**Extent:** 9 rows: AlmaLinux 4, Void 4, MicroOS 1, Talos 0, Gentoo no inventory. Every id, inventory name and matching archive path is in `D1/fix-d1-h-1/raw/card4-extent.tsv`. The search inspected kind/name for all 16,375 rows and all available L2 member paths, not just adjudicated rows (`card4-search.tsv`). These are the inventoried generated boot archives; unrelated boot-loader `.img` executables are not selected merely by suffix. Counts are rows, not unique archives: bucket and individual-image rows can refer to the same file. All six original examples and the other three rows are listed in the card 4 section below. No unsurveyed contents are presumed absent.''')
replace('- **Card 4 — REFUTED:** the dracut archive is unpacked as data, while extracted member programs execute; S8.2-23/15 decide the archive as a program record without assigning that decision to its executable members.', '- **Card 4 — CONFIRMED:** the extraction/execution facts do not supply the missing textual boundary between the archive and its executable contents; the previous refutation selected one reading of S8.2-9/23.')
replace('### Card 2: application to every named example', '### Card 2: refutation of the claimed collision and named-example limits')
replace('The alleged INSTALLED-DERIVED alternative reads S8.2-16 backwards.', 'Finding 2 is not accepted as a reason to change this card to a confirmed gap. S8.2-6 explicitly says classification is determined by the four questions, and S8.2-16 appears under the heading `Which line records an object.` The alleged INSTALLED-DERIVED alternative reads S8.2-16 backwards.')
replace('This refutes the claimed textual collision without certifying every associated row\'s final class.', 'The examples in S8.2-16 do not say that every generated list is installed, or that the four questions cease to determine its class. The absence of an applicable generated-list example in a restricted subclass of non-code, non-package records does not entail a contradictory classification. This uses the explicit S8.2-6 rule, not a new priority between conflicting requirements. It refutes the claimed collision; it does not certify all 70 rows whose final aggregate verdict remains undecided.')
replace('The package-selected trust values are access settings under S8.2-11/13, however stored (S8.2-12), with package-default coverage under S8.2-17; generated lookup/hash links carrying no separate choice reach Q4. Neither is made INSTALLED-DERIVED by S8.2-16.', 'The previous SETTING claim is withdrawn: the cited evidence does not establish S8.2-11/13 for the trust set. No third definitive classification replaces the disputed decisions. This row remains UNDECIDED:row-audit; generation alone supplies no affirmative Q1 or Q2 answer.')
replace('The same distinction applies to the supplied trust set and its generated lookup representation: Q3 for the access values, Q4 for index records, not automatic installed status.', 'The previous Q3 access-setting claim is withdrawn for the same reason. UNDECIDED:row-audit; the card-level argument about S8.2-16 does not settle the trust values or all their representations.')
start = s.index('### Card 4: application to every named example')
end = s.index('### Card 5: application to both examples')
s = s[:start] + '''### Card 4: failed refutation and all affected rows

The [kernel documentation](https://docs.kernel.org/filesystems/ramfs-rootfs-initramfs.html) establishes extraction followed by execution; it does not interpret S8.2-9/23. The short passage and inference limit are retained in `D1/fix-d1-h-1/raw/kernel-documentation.md`. The earlier argument established two technical stages, then assumed without a deciding sentence that the stored archive is only values for purposes of the definition. That assumption is withdrawn. The alternative reading treats the stored executable contents as code the computer can execute through the extraction/boot path. S8.2-23 does not state whether that path counts; both readings remain recorded in `D1/QUESTIONS.md`. S8.2-16 cannot itself make the archive code: it selects a line if the program reading is adopted.

| Example id | Inventory name / affected member | Disposition |
|---|---|---|
| `alma-c4a7c6d6eb439eb9d680a65e` | `/boot/initramfs-6.12.0-264.16.1.el10_3.x86_64.img` | CONFIRMED |
| `alma-2c25c1a886c5db421b08087b` | `/boot/initramfs-0-rescue-8ef0d28cd1cb4a80b9baa123cb63ef20.img` | CONFIRMED |
| `alma-9ba0bbb217552126cc411cf7` | `/boot/initramfs-6.12.0-264.16.1.el10_3.x86_64kdump.img` | CONFIRMED |
| `alma-632511e739337dc6b0644fd0` | `/boot`, containing rescue and kdump archives | CONFIRMED for those members |
| `void-0d4bff48fce03ced27aa83a4` | `/boot/initramfs-6.12.118_1.img` | CONFIRMED |
| `void-a6e5bb36a961f99d2e09e83e` | `/boot/initramfs-6.18.64_1.img` | CONFIRMED |
| `void-86ecf4dcf8ddad2c3dbf136e` | `/boot/initramfs-6.12.11_1.img` | CONFIRMED |
| `void-386e90812bdecbec21d0785c` | `/boot`, containing the three Void archives | CONFIRMED for archives; old config/kernel members separately FACT_UNKNOWN |
| `microos-62ccb03ff56e2af8ff91ff68` | `/.snapshots/1/snapshot/boot`, containing `initrd-7.3.5-1-default` | CONFIRMED for that archive |

Evidence: member inventories named in `card4-extent.tsv`; original card 4 in `D1/adjudication/HOLES.md`; generation/provenance evidence in `D1/adjudication/parts/l2-other.facts.md` and `D1/in/control/void/actions-logs/actions-logs/package_program.stderr`. These facts concern generated archives, not an unchanged shipped package file; a package-manager ghost placeholder does not establish unchanged receipt of the generated bytes. No fact is corrected by choosing one textual reading. No new boot or extraction probe was run, because the documented mechanism is known and cannot decide the textual boundary.

''' + s[end:]
replace('The same archive/member distinction used for card 4 is maintained here; unlike dracut\'s output, this archive satisfies Q1 as an installed package before any code question.', 'Unlike card 4, this object satisfies Q1 as an installed package before any code question; the decision does not require resolving how Q2 treats an archive.')
replace('Quote validation: `/usr/bin/python3 -I bin/check_quotes.py D1/RESULT.md` — 20 quotes checked; 0 not found in `TEXT.md`.', 'Quote validation for this corrected report: `/usr/bin/python3 -I bin/check_quotes.py D1/RESULT.md`; output in `D1/fix-d1-h-1/raw/quotes-result.log`. Mechanical checks are self-checks; independent acceptance is not claimed.')
p.write_text(s)
