# c2, part gentoo: notes

- Input `D1/in/part-gentoo.tsv` holds only the header line (`id	part	machine	kind	name	members	evidence`) and no object rows.
- Reason (from `D1/in/raw/gentoo/NOT-RUN.md` and `D1/in/FACTS.md`): pre-observation input verification failed on `check-inputs-v4/PUBLISH.list`; no machine was created and no collector was run. A header-only table does not assert absence of objects.
- Consequently no object was classified, no rule was applied by script, and no rows were checked by hand.
- Output `D1/c2/part-gentoo.tsv` holds the required header and 0 rows; verified by (not published: orchestration or scratch).
