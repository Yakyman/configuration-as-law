# ConfOS 0.49

The implementation as it stood before complete run 2 of the check of Section 9 of the fifth
paper. Committed on 24 November 2026 (UTC), before that run.

- Source archive: `confos-0.49-source.tar.gz`, SHA-256 `0f71e751f85a05fba1a8f8c726c823109a6dec6feaa1d27e210e5c729d9ef4db`,
  13405 files, 2291936655 bytes unpacked.
- Built image stated by the builder for this release: SHA-256 `815aaa6f40df4819bc9a0aa37c03f4b2b31df593c9582efa46a976c225c41ff1` (not stored here).

This folder holds every text file of the archive, unchanged (391 files). The other 13014 files
of the archive are not stored here: the packages that the build programs in this folder produce from the pinned
inputs; the pinned third-party inputs (`interpreter-inputs/`: source packages of the programs that the
implementation modifies, their descriptors, unpacked build dependencies); and working files of the build that
are not the implementation (drafts, raw logs of probes, scripts that move the working state). `BINARIES.tsv` gives
the path, the size and the SHA-256 of each. `components.txt` and `components/` pin every package of the base
system to an archive state. `SHA256SUMS` lists the files of this folder.

The code is under the MIT license (`LICENSE-CODE` in the root of the repository).
