# c2, part gentoo — notes

The input `D1/in/part-gentoo.tsv` holds only its header and no object rows. `D1/in/FACTS.md` (section "gentoo")
and `D1/in/raw/gentoo/NOT-RUN.md` record that no inventory was obtained: the single machine start returned 1
(`lab: VM failed to start`), and the collector was not run.

No row exists, so no decision was made, no rule was applied by a script, and no hand check was possible.
The output `D1/c2/part-gentoo.tsv` holds the required header and zero rows. The check
(not published: orchestration or scratch) confirmed the header, equal id sets (0 = 0) and wrote (not published: orchestration or scratch).
