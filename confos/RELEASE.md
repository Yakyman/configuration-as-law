# ConfOS 0.32

The implementation as it stood before complete run 1 of the check of Section 9 of the fifth
paper. Committed on 24 November 2026 (UTC), before that run.

- Source archive: `confos-0.32-source.tar.gz`, SHA-256 `61d290744606b4804b298217d340df5445cf276ea2b3ad69cc024e9457261001`,
  152 files, 521064672 bytes unpacked.
- Built image stated by the builder for this release: SHA-256 `d7210025c438c970f622bb8a472144c712bfcbab190608087c85fb76159cdf39` (not stored here).

This folder holds every text file of the archive, unchanged (101 files). The other 51 files
of the archive are not stored here: the packages that the build programs in this folder produce from the pinned
inputs, and the pinned source packages of the programs that the implementation modifies. `BINARIES.tsv` gives
the path, the size and the SHA-256 of each. `components.txt` and `components/` pin every package of the base
system to an archive state. `SHA256SUMS` lists the files of this folder.

The code is under the MIT license (`LICENSE-CODE` in the root of the repository).
