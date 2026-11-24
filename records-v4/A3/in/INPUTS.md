# Input verification

The input gate (not published: orchestration or scratch) records commit `3e0207b104f9718793c5b2678810936c7c3c14d2`, 2026-11-23T11:10:54Z, 1017 files. The operator read (not published: orchestration) first, then the gate, check-inputs-v4/inputs-beyond-plan.md, check-inputs-v4/LAB.md and C1/COLLECT.md. This task is beyond the four published checks, under PROTOCOL.md Section 5.

`input-verification.tsv` records SHA-256 verification performed before any machine task started. All three lived-in scripts, their accompanying published action helpers, the published collector files and chunks, collect.sh, COLLECT.md, LAB.md and lab.sh match the input checksum table and are named by PUBLISH.list. Staging uses those files as they lie in C1; it does not use the publication-copy subtree or the unlisted unchunked probe archive.

One manifest discrepancy was found: PUBLISH.list itself has expected SHA-256 `63801d3b7bd13b1c5335d9dede8b6135b7e8506953aa93425aa06cabcda78660` but actual SHA-256 `4569378038e1142d9519dd9cd49e6e40575cce030fe1b3f835768943c1cd89b6`. No executable input was substituted or changed in response. The current list names all required verified inputs.

The default outer SSH invocation failed before connecting because a system SSH configuration file had unacceptable ownership/permissions. Explicitly selecting the existing user SSH configuration allowed the authorized laboratory connection without changing any host files. This is an outer transport adjustment, not a guest action change.

