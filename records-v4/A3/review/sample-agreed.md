# Agreed-row sample audit

Seed: `2026112303`. Eligible population: 2,998 rows of `A3/compare/joined.tsv` with `same=yes` and no id in `A3/adjudication/rows.tsv`. Sorted by id before `random.Random(2026112303).sample(eligible, 60)`. The draw order, all 60 ids, exact deciding sentences, evidence references and individual reasoning are in [sample-agreed.tsv](sample-agreed.tsv).

Results: 58 affirmative classifications supported; 2 existing UNKNOWN classifications validated as missing facts; 0 unsupported decisions requiring a new gap card; 0 confirmed gaps. Sample composition: developer 17, gaming 14, server 29. Decisions: RUNTIME 38, INSTALLED-OWN 9, RECORD 8, UNKNOWN 2, INSTALLED-PACKAGE 2, INSTALLED-DERIVED 1.

The two UNKNOWN rows are `server-b7f34f100f522f35b95809ec` (`/var/lib/dpkg/info/exim4-daemon-light.postinst`) and `server-3c36ff034958e52297c4e999` (`/var/lib/dpkg/info/containerd.io.prerm`). Their original package-control contents were not compared with installed contents. This prevents deciding whether question one applies; it does not expose an undefined object kind.

Three challenges were considered explicitly:

- Runtime firewall rules, processes, open ports and volatile member groups: S8.2-5 directly excludes a separate object. Where creator identity or integrity remains unknown, this audit does not promote that creator to a known class; the row's RUNTIME decision still follows. All sampled member groups classified RUNTIME contain only members whose saved persistence field is runtime.
- Four manifest-cache files have a shebang flag. The [upstream serializer](https://raw.githubusercontent.com/oven-sh/bun/main/src/install/npm.rs) uses a shebang header for binary manifest data; its `write` routine serializes metadata, not executable source. That explains the flag without turning these metadata files into programs. S8.2-23 and S8.2-15 decide RECORD; no conflict follows from the collector's code-candidate label.
- Explicitly selected packages: S8.2-16 permits their own lines. The agreed decision is supported, but the classifiers' wording that an explicit selection necessarily excludes every possible generating declaration algorithm is stronger than the sentence. No actual alternative generating line is present in the evidence and no new gap is established.

Package ownership/digest evidence was checked for the sampled unit file and executable alias; /sbin is recorded as a symlink to usr/sbin. The manual and automatic package lists contain each sampled package with its stated provenance. All 60 sampled ids exist in the raw object inventories. This sample makes no assertion about unsampled agreements and assigns no check outcome to the beyond-plan folder.
