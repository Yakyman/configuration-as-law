# Review: part 2 classification

Result: no remaining defects found.

Reviewed the 839 decisions in `part-2.tsv`: 94 core, 165 unit, 327 package, and 253 stored-object rows. The final distribution is 661 MUST, 45 NOT, 2 HOLE, 70 UNKNOWN, and 61 MIXED.

The review checked each decision against S2.2 and S3-1/S3-2, including the content, cache, history, single-program-setting, executable-code, account, and removal conditions. The remaining HOLE cases retain conflicting applicable text; UNKNOWN is used where the object's functional effect is unestablished.

The core, unit, package, and stored notes provide the required rules and ten manual checks for each homogeneous rule. The merged file has one row per input ID; fragment decisions match it. All `what_it_does` and `reason` fields meet the 15-word and 30-word limits.
