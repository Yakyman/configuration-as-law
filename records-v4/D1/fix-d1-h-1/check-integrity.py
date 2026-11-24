"""Check preserved inputs and the changed output tables; no observations."""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

raw = Path('D1/fix-d1-h-1/raw')
before = json.loads((raw / 'frozen-input-hashes.json').read_text())
changed = [p for p, digest in before.items() if hashlib.sha256(Path(p).read_bytes()).hexdigest() != digest]
assert not changed, changed


def rows(name):
    with (raw / name).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


ledger = rows('gap-row-dispositions.tsv')
extent = rows('card4-extent.tsv')
search = rows('card4-search.tsv')
failure = rows('failure-condition-rows.tsv')
assert len({r['id'] for r in ledger}) == len(ledger) == 1364
assert len({r['id'] for r in extent}) == len(extent) == 9
assert len({r['id'] for r in search}) == len(search) == 16375
assert len({r['id'] for r in failure}) == len(failure) == 1362
assert all(r['c1_decision'] != r['c2_decision'] for r in failure)
assert {r['id'] for r in extent} == {r['id'] for r in ledger if r['fix_status'].startswith('CONFIRMED')}
assert sum(r['fix_status'] == 'UNDECIDED:row-audit' for r in ledger) == 284
assert sum(bool(r['additional_missing_facts']) for r in ledger) == 1070
assert Path('D1/RESULT.md').read_text().splitlines()[0] == 'CHECK 1: 1 confirmed gaps'
assert 'not found in TEXT.md: 0' in (raw / 'quotes-result.log').read_text()
assert 'not found in TEXT.md: 0' in (raw / 'quotes-fix.log').read_text()
report = {
    'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'frozen_sources_checked': len(before),
    'changed_frozen_sources': changed,
    'unique_complete_gap_ledger': True,
    'unique_complete_whole_table_search': True,
    'disagreement_clause_rows_checked': 1362,
    'confirmed_extent_matches_ledger': True,
    'undecided_rows': 284,
    'fact_limited_rows_including_one_gap_overlap': 1070,
    'quote_checks_passed': True,
    'independent_acceptance': False,
}
with (raw / 'integrity-check.json').open('x') as f:
    json.dump(report, f, indent=2)
    f.write('\n')
print(json.dumps(report, indent=2))
