# Gaps and competing readings in PAGE.md

This index includes every table row marked NOT_DECIDED or TWO_WAYS, exactly once. FACT_UNKNOWN describes missing object facts and is excluded; MIXED rows retain their member decisions in the tables. R5 is always applied before considering a separate U3 conflict.

## Fileless package identities

The text does not classify a fileless dependency-package identity, and U1 covers same-package companions rather than programs supplied by dependencies.

Sentences: Q1,Q2,Q3,U1.

Rows: D1 **20**; A1 **10**; A3R **0**.

Examples: D1 `fedora-6c4e6a443cca6462b71a16e4`; A1 `coreos-d49702b0f3`; D1 `fedora-edddb9b4b4275940143befca`.

## Runtime dependency targets

The text does not say that a runtime dependency target is an executed program, a service, a human-chosen value, or a program-written record.

Sentences: Q1,Q2,Q2a,Q3.

Rows: D1 **0**; A1 **6**; A3R **0**.

Examples: A1 `debian-8786c9eece`; A1 `debian-00a56889bd`; A1 `debian-6e3a25797c`.

## Observed mount objects

The text does not equate an observed runtime mount object with a device or human-decided setting value.

Sentences: Q1,Q2,Q2a,Q3.

Rows: D1 **0**; A1 **6**; A3R **0**.

Examples: A1 `debian-18fb2985ed`; A1 `debian-565df89b5f`; A1 `arch-565df89b5f`.

## Runtime process groups

The text does not classify a runtime process-group object as its member programs, a service, a human-selected value, or a written record.

Sentences: Q1,Q2,Q2a,Q3,U6.

Rows: D1 **0**; A1 **4**; A3R **0**.

Examples: A1 `debian-0ff15b2741`; A1 `debian-253d752b01`; A1 `debian-3bc8c8458c`.

## References to absent units

The text does not classify a runtime reference to an absent unit or equate the reference with an existing service.

Sentences: R3,Q1,Q2a,Q3.

Rows: D1 **0**; A1 **8**; A3R **0**.

Examples: A1 `nixos-9994d7ebc4`; A1 `nixos-97fdaec6aa`; A1 `arch-9994d7ebc4`.

## Runtime communication endpoints

The text does not classify the inventoried RPC pipes, socket endpoints and connection objects as executed programs, chosen values, or written records.

Sentences: Q1,Q2,Q2a,Q3.

Rows: D1 **0**; A1 **4**; A3R **0**.

Examples: A1 `coreos-0eecaaf2d8`; A1 `guix-ab6f354e5f`; A1 `guix-d0ad40aadd`.

## Setting values versus nonexecuted files

Q2/Q2a makes an operative setting value SETTING/YES while U3 makes its nonexecuted file MATERIAL/NO, and R5 gives no priority between those sentences.

Sentences: R1,R2,R5,Q2,Q2a,U3.

Rows: D1 **70**; A1 **88**; A3R **15**.

Examples: D1 `fedora-38e9eb1bb0adbd5a6cc1981b`; A1 `coreos-4c44b1402c`; A3R `24c2b14cafc1e66ac4c9b537`.

## Program records versus nonexecuted files

Q3 makes an operationally written file PROGRAM_RECORD/NO while U3 makes the same nonexecuted file MATERIAL/NO, with no sentence selecting its kind.

Sentences: R2,R5,Q3,U3.

Rows: D1 **201**; A1 **100**; A3R **61**.

Examples: D1 `flatcar-f680f2ced5cbbbb98c0f7e6e`; A1 `coreos-e51a3be8af`; A3R `2075201fef03f9b5ca794582`.

## Personal preferences versus nonexecuted files

U7 makes a personal preference file PROGRAM_RECORD, recorded when U8 applies, while U3 makes its nonexecuted file MATERIAL/NO without resolving their classifications.

Sentences: Q2,Q3,U3,U7,U8,R1,R2.

Rows: D1 **0**; A1 **6**; A3R **1**.

Examples: A1 `guix-9052456462`; A3R `54c86841fb0c34fd62a14f37`; A1 `guix-a008390f8b`.

Every included ID and its group are enumerated in `holes-members.tsv`. The separate-case answers additionally discuss declaration references and the undefined boundary of “system program”; those cases are not inventory-table rows.
