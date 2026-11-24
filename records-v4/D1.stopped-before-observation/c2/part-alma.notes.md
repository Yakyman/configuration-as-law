# c2, part alma — notes

- Input `D1/in/part-alma.tsv` holds only the header `id	part	machine	kind	name	members	evidence`; it has 0 object rows.
- `D1/in/FACTS.md` and `D1/in/READY.md`: no inventory was taken on any machine; pre-observation input verification
  stopped (publication list checksum mismatch). (not published: record outside selected evidence) documents the stop only; it is not
  collector output. No package, packaged-file, group-member or persistence facts exist.
- Therefore no decision was made: the output `D1/c2/part-alma.tsv` holds only the required header.
- No scripted rule was used, so no hand-checked rows are listed.
- A header-only table does not assert that the machine has no objects (FACTS.md); this part gives no evidence for or
  against the text.
- Verification: (not published: record outside selected evidence) (run from the night folder) checks header, id set and decision words, and writes
  (not published: orchestration or scratch).
