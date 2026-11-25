# ConfOS 0.55

The implementation as it stood before complete run 3 of the check of Section 9 of the fifth
paper. Committed on 25 November 2026 (UTC), before that run.

- Source archive: `confos-0.55-source.tar.gz`, SHA-256 `eb901118dc725dfbadfc46ee56069f4fa631903fdb08eec25bf763f6a12acdd1`,
  504 files, 411141528 bytes unpacked.

This folder holds every text file of the archive, unchanged (498 files). The other 6 files
of the archive are not stored here: the packages that the build programs in this folder produce from the pinned
inputs; the pinned third-party inputs (`interpreter-inputs/`: source packages of the programs that the
implementation modifies, their descriptors, unpacked build dependencies); and working files of the build that
are not the implementation (drafts, raw logs of probes, scripts that move the working state). `BINARIES.tsv` gives
the path, the size and the SHA-256 of each. `components.txt` and `components/` pin every package of the base
system to an archive state. `SHA256SUMS` lists the files of this folder.

The code is under the MIT license (`LICENSE-CODE` in the root of the repository).
