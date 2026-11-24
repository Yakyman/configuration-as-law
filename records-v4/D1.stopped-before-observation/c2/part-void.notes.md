# c2, part void — notes

- Input `D1/in/part-void.tsv` holds only the header line `id	part	machine	kind	name	members	evidence`; it has
  0 object rows.
- `D1/in/FACTS.md` and (not published: record outside selected evidence) state that no inventory was taken: pre-observation input
  verification stopped (check-inputs-v4/PUBLISH.list checksum mismatch), no machine was created, no collector was run.
  A header-only table does not assert absence of objects.
- Consequently there is nothing to classify: no decisions were made, no script rules were written, no rows were
  checked by hand, no documentation was consulted.
- Output `D1/c2/part-void.tsv` holds only the required header. Verification script: (not published: record outside selected evidence).
