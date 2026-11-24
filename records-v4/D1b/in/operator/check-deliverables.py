#!/usr/bin/env python3
"""Check mechanical preservation of already collected and delivered records."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SYSTEMS = ('alma', 'void', 'gentoo', 'microos', 'talos')
HEADER = ['id', 'part', 'machine', 'kind', 'name', 'members', 'evidence']
csv.field_size_limit(536870912)


def read(path, header=None):
    with path.open(newline='', encoding='utf-8') as source:
        reader = csv.DictReader(source, delimiter='\t')
        if header is not None:
            assert reader.fieldnames == header, str(path.relative_to(ROOT))
        return list(reader)


def main():
    target = ROOT / 'D1b/in'
    results = {}
    inventory_ids, mapped_ids = set(), set()
    total_old = 0
    for machine in SYSTEMS:
        folder = ROOT / 'D1b/handoff' / machine
        audit_path = ROOT / 'D1b/handoff-audit' / (machine + '.json')
        if audit_path.is_file():
            audit = json.loads(audit_path.read_text())
            expected_files = {r['path'] for r in audit['files']}
            assert audit['source_unchanged'] is True
            for tree, field in (('raw', 'source_sha256'), ('handoff', 'handoff_sha256')):
                base = ROOT / 'D1b' / tree / machine
                assert {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()} == expected_files
                for row in audit['files']:
                    with (base / row['path']).open('rb') as stream:
                        assert hashlib.file_digest(stream, 'sha256').hexdigest() == row[field]
        raw = read(folder / 'objects.tsv') if (folder / 'objects.tsv').is_file() else []
        all_rows = read(target / ('all-' + machine + '.tsv'), HEADER)
        part = read(target / ('part-' + machine + '.tsv'), HEADER)
        assert len(all_rows) == len(raw)
        raw_ids = {r['id'] for r in raw}
        assert len(raw_ids) == len(raw)
        member_groups = member_rows = 0
        for before, after in zip(raw, all_rows):
            assert after['id'] == 'd1b-' + machine + '-' + before['id']
            assert after['part'] == machine
            assert after['kind'] == 'L' + before['level'] + ':' + before['kind']
            assert all(after[k] == before[k] for k in ('machine', 'name', 'members', 'evidence'))
            assert after['id'] not in inventory_ids
            inventory_ids.add(after['id'])
            members = json.loads(before['members'])
            if isinstance(members, str):
                try:
                    members = json.loads(members)
                except ValueError:
                    pass
            if isinstance(members, dict) and 'file' in members:
                p = folder / members['file']
                assert p.is_file()
                count = sum(1 for _ in csv.DictReader(p.open(newline=''), delimiter='\t'))
                assert count == int(members['count'])
                member_groups += 1
                member_rows += count
        matched = read(target / 'match' / ('matched-' + machine + '.tsv'))
        unmatched = read(target / 'match' / ('unmatched-' + machine + '.tsv'))
        assert all(r['machine'] == machine for r in matched + unmatched)
        assert len({r['first_id'] for r in matched + unmatched}) == len(matched) + len(unmatched)
        assert not ({r['first_id'] for r in matched} & {r['first_id'] for r in unmatched})
        assert all(r['new_id'] in raw_ids for r in matched)
        matched_ids = {'d1b-' + machine + '-' + r['new_id'] for r in matched}
        expected = all_rows if machine == 'gentoo' else [r for r in all_rows if r['id'] in matched_ids]
        assert part == expected
        total_old += len(matched) + len(unmatched)
        results[machine] = dict(all=len(all_rows), part=len(part), matched=len(matched), unmatched=len(unmatched),
                                member_groups=member_groups, member_rows=member_rows,
                                exact_preserved_rows=True, exact_part_selection=True,
                                original_and_handoff_hashes_match_audit=audit_path.is_file())
    for row in read(target / 'object-id-map.tsv', ['id', 'machine', 'raw_id']):
        assert row['id'] == 'd1b-' + row['machine'] + '-' + row['raw_id']
        assert row['id'] not in mapped_ids
        mapped_ids.add(row['id'])
    assert mapped_ids == inventory_ids
    assert total_old == 2007
    result = dict(passed=True, fixed_first_night_ids_accounted=total_old, unique_inventory_ids=len(inventory_ids), machines=results)
    (target / 'operator/deliverable-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
