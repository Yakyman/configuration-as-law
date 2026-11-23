# c2 — part talos — notes

- Input `../in/part-talos.tsv` contains the header only: 0 object rows.
- Reason, from `../in/READY.md` (section "talos"): "Inventory objects: **0**" and "The partial API outputs remain
  under `raw/talos/raw/`; no object table was synthesized from them."
- The task decides the rows of the input table. With 0 rows there is nothing to decide. No object was taken from
  `D1/in/raw/talos/raw/`: the objects of the task are the rows of the table, and creating rows would add ids that
  the input does not hold.
- No script rule was used; no hand checks apply (0 rows).
- Output `part-talos.tsv`: header only. Verification: `tools/verify_talos.py`.
