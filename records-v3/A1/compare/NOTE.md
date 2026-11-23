# Note on “Problems of form” in STATS.md

The lines “duplicate row” in `STATS.md` do not concern the classifications. The comparison script read, besides the
final file of each part (`c1/part-<n>.tsv`), the intermediate files that c1 wrote while working
(`c1/part-<n>.<name>.tsv`), and reported their rows as duplicates. The final files were read last, so the joined
table holds the final decisions: a separate check ((not published: orchestration and working notes)) compared `joined.tsv` with the final part
files of c1 and c2 — 5,200 objects, 0 differences. The script was corrected afterwards to read only the final files.
