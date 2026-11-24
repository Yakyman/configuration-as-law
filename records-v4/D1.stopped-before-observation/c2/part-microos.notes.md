# c2, part microos — notes

- Input `D1/in/part-microos.tsv` holds only the header `id	part	machine	kind	name	members	evidence`; 0 object rows.
- Reason (from (not published: record outside selected evidence) and `D1/in/FACTS.md`): pre-observation input verification stopped
  (`check-inputs-v4/PUBLISH.list` checksum mismatch, `D1/in/control/input-verification.tsv`); no machine was created and no
  collector ran. `D1/in/FACTS.md`: "A header-only object table does not assert absence of objects."
- Output `D1/c2/part-microos.tsv` therefore holds only its header. No decisions were made, no scripted rule was used,
  and no rows were checked by hand.
- This empty output says nothing about the objects of a MicroOS machine; it only records that this part had no input.
