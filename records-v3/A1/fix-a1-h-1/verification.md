# Independent verification of FX-A1-H-1

Date: 2026-11-22 UTC.

Scope: findings 1–4 in `../REVIEW.md`. This verification uses the frozen review and inventory records, the revised H1 records, and the published text. It does not decide either unresolved reading or accept a scientific conclusion.

## Result

The final correction passes this verification for findings 1–4. No remaining numerical, stale-link, blanket-exclusion, sample-identity, or manager-scope contradiction was found in the checked records.

| Check | Result | Evidence and independent recomputation |
|---|---|---|
| 1. Unit-file single-program premise | Pass | `hole-1-extent.tsv` has 914 unchanged IDs and a complete status partition: 85 `CONFIRMED-STANDALONE`, 29 `CONFIRMED-CONSTITUENT`, 243 `FACTUAL-UNKNOWN`, 522 `READING-DEPENDENT`, and 35 exclusions. The 598 originally confirmed unit-related rows split exactly into 522 inventory units now reading-dependent and 76 stored unit files now factual unknown. Thus 721 minus 598 minus two unit-only aggregates minus seven enablement-dependent groups is 114 established rows. `counts.json` reports the same figures. |
| 2. Unit-object/file boundary | Pass | Every one of the 522 `READING-DEPENDENT` rows is an inventory `system-unit` or `user-unit`; none is counted as confirmed. The record states the two object readings without selecting either, and does not turn this reading question into `S3-2` factual unknown. The 76 stored-file cases remain separately factual unknown. |
| 3. Affected samples and grouping states | Pass | The revised resolved audit retains all 40 frozen sample IDs in identical order; the agreed audit retains all 60. Recomputed dispositions are resolved: 14 supported, 15 refuted, 3 fact-wrong, 6 outside, 1 confirmed H1, 1 factual unknown; agreed: 48 supported, 1 confirmed H1, 8 reading-dependent, 3 factual unknown. The `coreos-4d2a7c7537` group is factual unknown, not confirmed. The two retained `/etc/systemd` groups state their independent non-unit constituents, while unit/enablement members do not contribute to established membership. |
| 4. Exact procps evidence | Pass | The five multiple-reader records name one applicable saved inventory file and line each: `A1/in/raw/nixos/system-closure.txt:142` or `A1/in/raw/coreos/packages.tsv:397`. No templated alternative file field remains in their revised evidence. |

## Conditional disabled-state evidence

The final `unit-file-reader-check.tsv` contains 598 checked rows and 21 conditional second-applier findings. They are explicitly conditional on the hypothetical file reading; their actual inventory objects remain `READING-DEPENDENT`. The saved `disabled` state is tied to the same manager scope: no established system-unit row uses `user-list-unit-files.txt`, and no established user-unit row uses `unit-files.txt`. This removes the three cross-scope basename matches found during verification. The documented meaning of `disabled` is saved at `raw/systemctl-v260.xml:1116-1117`.

## Reproducibility checks

Independent CSV recomputation over `../review/hole-1-extent.tsv`, `hole-1-extent.tsv`, `../review/resolved-audit.tsv`, and `../review/agreed-audit.tsv` produced the counts above. It also confirmed the status transitions: 522 `CONFIRMED-STANDALONE` to `READING-DEPENDENT`, 76 `CONFIRMED-STANDALONE` to `FACTUAL-UNKNOWN`, and 9 `CONFIRMED-CONSTITUENT` to `FACTUAL-UNKNOWN`. The original card-1 anchors remain 68 standalone confirmations, 18 constituent confirmations, 8 factual unknowns, and 3 multiple-reader exclusions. `bin/check_quotes.py A1/RESULT.md` reports 10 checked quotations and zero absent from `../../TEXT.md`.

The 114 / 243 / 522 H1 figures and the revised sample counts are therefore supported by the checked records. This record verifies record consistency only; it does not select the unresolved unit reading or determine the trial outcome.
