# Verification

Date: 2026-11-22 UTC.

`/usr/bin/python3 -I bin/check_quotes.py A1/RESULT.md`

quotes checked: 10; not found in TEXT.md: 0

`/usr/bin/python3 -I bin/check_quotes.py A1/review/resolved-audit.tsv quote`

quotes checked: 40; not found in TEXT.md: 0

`/usr/bin/python3 -I bin/check_quotes.py A1/review/agreed-audit.tsv exact_quotes`

quotes checked: 60; not found in TEXT.md: 0

All six recorded input hashes match `counts.json`. The fixed samples were rechecked against seeds 112221 and 112222, their eligible pools and saved selection order.

hole-1-extent: {'EXCLUDED-MULTIPLE-READERS': 5, 'FACTUAL-UNKNOWN': 158, 'CONFIRMED-STANDALONE': 683, 'CONFIRMED-CONSTITUENT': 38, 'EXCLUDED-FACT': 15, 'EXCLUDED-STATE': 15}.

hole-4-extent: {'FACTUAL-UNKNOWN': 7, 'CONFIRMED-CONSTITUENT': 1, 'CONFIRMED-STANDALONE': 4, 'FACT-WRONG': 7}.

All 5,200 input IDs occur in the H1 scan. Confirmed sample H1 IDs are in its extent. Local links in RESULT.md resolve. Independent findings and final acceptance are recorded in `final-boundaries.md` and `independent-review.md`.
