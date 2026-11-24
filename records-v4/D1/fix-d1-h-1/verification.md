# Self-check of FX-D1-H-1; not independent acceptance

Recorded 2026-11-23 UTC. This record corrects the label and status of the frozen `D1/review/verification.md`. That earlier file's title and assertion of no blocking finding are not evidence of independent verification and are superseded here. The earlier file is preserved as evidence, not rewritten.

Changed work only:

- `/usr/bin/python3 -I D1/fix-d1-h-1/audit-changes.py` — saved output `raw/audit-changes.log`; supporting tables and `raw/changed-counts.json`. No new observations or sample selections. The original GAP set has 1,364 unique rows; 1,362 satisfy the disagreement clause; the changed extent search returns 9 archive-gap rows; all original GAP rows receive an explicit audit status.
- `/usr/bin/python3 -I (not published: orchestration or scratch) D1/RESULT.md` — saved output `raw/quotes-result.log`.
- `/usr/bin/python3 -I (not published: orchestration or scratch) D1/FIX-D1-H-1.md` — saved output `raw/quotes-fix.log`.
- `/usr/bin/python3 -I D1/fix-d1-h-1/check-integrity.py` — frozen-source hash comparison and output consistency assertions; saved output `raw/integrity-check.json`.

Original samples, unchanged statistics, and original unknown-row unions were not rerun. Their saved evidence remains in `D1/review/`, with the external review's positive checks in findings 7–9. The 284 row audits explicitly marked undecided remain a limitation. Independent acceptance of the corrected work is not claimed.
