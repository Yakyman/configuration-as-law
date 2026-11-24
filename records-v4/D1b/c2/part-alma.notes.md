# c2, part alma — notes

2026-11-23 UTC.

- Input `D1b/in/part-alma.tsv` holds the header only and no object rows. `D1b/in/READY.md` records why: the
  AlmaLinux handoff copy failed (`_csv.Error: field larger than field limit (131072)`), so 0 rows were delivered
  and 0 objects are to be decided. `D1b/in/FACTS.md` says: "No delivered object inventory; no facts asserted for
  this machine."
- `D1b/in/not-delivered-alma.tsv` lists the 5,711 original IDs that were not delivered. They are not input rows.
  The task forbids adding rows, so none of them is decided here.
- No scripted rules were used. No rows were checked by hand because there are no rows.
- Output `part-alma.tsv` holds the header only. No row has GAP-NONE or GAP-TWO, so `meaning-alma.tsv` holds the
  header only.
