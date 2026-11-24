# Part void classification notes

No object rows were supplied, so no classification rules were applied and no hand-check sample exists.

Evidence: `D1/in/FACTS.md` states: "No inventory was taken because pre-observation input verification failed." (not published: record outside selected evidence) states: "No machine was created and no action or collector was run."

The input consists solely of the expected header encoded with literal backslash-t separators and a literal backslash-n terminator. This exact header-only representation was recognized as zero object rows; the source was not modified. The output uses actual tab separators and a newline.

Verification: input and output each contain zero object IDs; their ID sets and counts match, with no duplicate IDs or invalid decisions. Zero counts describe the supplied table, not absence of objects on a machine.
