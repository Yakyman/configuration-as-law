# Final c1 consolidation notes

All rows produced in this attempt were saved incrementally. No earlier output rows existed at its start. The component tables retain their first completed decisions. Evidence-based corrections made during consolidation are listed in part-mint.corrections.json; part-mint.correction-audit.json preserves the original and final fields. The consolidated part-mint.tsv is the final classification. No input object, inventory file, or prior result was removed.

## Shared highlighting definitions

For mint-f3a27734d1c9e9356a0e2c91, libsource-highlight-common, the final decision is MUST under S2.2-1 and S2.2-2. S2.2-7 and S2.2-13 do not exempt shared settings used across separate programs. Primary upstream documentation in https://ftp.gnu.org/gnu/src-highlite/source-highlight-3.1.9.tar.gz, doc/source-highlight.texi, describes the library as enabling consumers to “add highlighting functionalities to their programs”. The library manual, doc/source-highlight-lib.texi, describes recognition: “the library detects (using regular expressions based on language definition files)”. The shared data directory supplies definitions and output styles to those consumers. The removal argument concerns loss of shared recognition capability, not arbitrary execution of grammar files as host-rights scripts.

## Additional check of interpreter resources

The UNKNOWN decision for mint-f03630dc00f470e339f74873, libgs10-common, is retained. Its file list establishes interpreter resources; the available inventory does not establish the execution mode and rights of those resources. Further primary documentation was consulted at https://ghostscript.readthedocs.io/en/gs10.02.1/Use.html and https://ghostscript.readthedocs.io/en/latest/Psfiles.html. The former states “Sometimes the initialization files are compiled into Ghostscript and cannot be changed.” The latter describes gs_init.ps: “Ghostscript reads this automatically when it starts up.” These establish function and possible packaging arrangements, but do not supply this machine's invocation or build settings. No execution/removal probe was made. This is a factual evidence limitation under S3-2, not an alleged gap in the definition.

## Validation

part-mint.merge-verify.py checks the exact header, one row per input identifier, identical identifier sets and counts, uniqueness, the five permitted decisions, permitted sentence IDs, field word limits, single-line fields, and basis prefixes. It writes part-mint.done only when the complete identifier comparison succeeds.

## Dependency selectors: final individual decisions

The final decision for bluetooth, build-essential, init, and libpython3-stdlib is MUST under S2.2-1 and S2.2-2. Their documented dependencies govern package operations. This is not a claim that deleting the selector also deletes installed dependencies; those are separate objects. It is a change in which packages subsequent package operations select or allow. No sentence limits computer behavior to currently running executable payloads. These individual corrections supersede the intermediate documentation-only reasoning for bluetooth, build-essential, and init in component 1, and for libpython3-stdlib in component 2.

Each was checked individually against its full description retained in part-mint.1.sources.json or part-mint.3.full-metadata.json:

- bluetooth, mint-abfe052ec72b3e4d59ff2dd7: https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz documents provision of all supported stack plugins through this metapackage. Its payload file list alone omits the operative dependency selection.
- build-essential, mint-267e53cbb404e5549ed2f412: https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz documents dependency on the essential build tools and states the package is required for package building. Its informational list does not erase that dependency role.
- init, mint-c5056f235638fd42ac7b8127: the same primary index documents selection among initialization systems while ensuring one remains available at all times. That is an operative constraint, not just descriptive content.
- libpython3-stdlib, mint-d0cf3bfc0f782be651893767: the same primary index identifies a dependency on the distribution's default interpreter version's standard library. Tracking selection through upgrades is inferred from the versioned dependency, not an assertion that its payload contains runtime implementation.

The ftp package remains NOT: the primary description identifies an obsolete dummy transition to the separately inventoried tnftp implementation. Its individual removal leaves that replacement in place. This differs from an ongoing current-default or completeness constraint. The nine selectors in component 3 likewise have operative documented dependency-selection roles; their final MUST rows and individual supporting descriptions appear in that component's correction notes.

All source and correction decisions are classified as c1. The counts in component notes describe their own intermediate or corrected component tables; only part-mint.done reports the final consolidated totals.
