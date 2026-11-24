#!/usr/bin/env python3
"""Mechanical handoff conversion and invocation of the fixed matching rule."""
import collections
import csv
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
SYSTEMS = ('alma', 'void', 'gentoo', 'microos', 'talos')
HEADER = ['id', 'part', 'machine', 'kind', 'name', 'members', 'evidence']
csv.field_size_limit(536870912)


def read(path):
    with path.open(newline='', encoding='utf-8') as source:
        return list(csv.DictReader(source, delimiter='\t'))


def write(path, columns, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', newline='', encoding='utf-8') as output:
        writer = csv.DictWriter(output, fieldnames=columns, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    target = ROOT / 'D1b/in'
    summaries, mappings, statuses = {}, [], []
    handoff_status = {r['machine']: int(r['exit_status']) for r in read(target / 'operator/handoff-status.tsv')}
    for machine in SYSTEMS:
        source = ROOT / 'D1b/handoff' / machine / 'objects.tsv'
        delivered = handoff_status[machine] == 0 and source.is_file()
        raw_rows = read(source) if delivered else []
        rows = []
        for original in raw_rows:
            assert original['machine'] == 'd1b-' + machine
            assert original['level'] in ('1', '2')
            ident = 'd1b-' + machine + '-' + original['id']
            rows.append(dict(id=ident, part=machine, machine=original['machine'],
                             kind='L' + original['level'] + ':' + original['kind'],
                             name=original['name'], members=original['members'], evidence=original['evidence']))
            mappings.append(dict(id=ident, machine=machine, raw_id=original['id']))
        assert len({r['id'] for r in rows}) == len(rows)
        all_path = target / ('all-' + machine + '.tsv')
        write(all_path, HEADER, rows)
        output = target / 'match' / machine
        inventory = source.parent if delivered else all_path
        command = ['python3', 'S4/collector/match.py', str(inventory.relative_to(ROOT)),
                   'D1/review/unknown-rows.tsv', 'D1/review/additional-unknown-rows.tsv',
                   str(output.relative_to(ROOT))]
        run = subprocess.run(command, cwd=ROOT, capture_output=True)
        (target / 'operator' / ('match-' + machine + '.stdout')).write_bytes(run.stdout)
        (target / 'operator' / ('match-' + machine + '.stderr')).write_bytes(run.stderr)
        statuses.append(dict(machine=machine, exit_status=run.returncode, command=' '.join(command)))
        if run.returncode:
            raise RuntimeError('Fixed matcher failed for ' + machine + '; no repair or retry performed')
        matched_all, unmatched_all = read(output / 'matched.tsv'), read(output / 'unmatched.tsv')
        matched = [r for r in matched_all if r['machine'] == machine]
        unmatched = [r for r in unmatched_all if r['machine'] == machine]
        write(target / 'match' / ('matched-' + machine + '.tsv'),
              ['first_id', 'new_id', 'machine', 'kind', 'first_name', 'new_name', 'match_rule'], matched)
        write(target / 'match' / ('unmatched-' + machine + '.tsv'),
              ['first_id', 'machine', 'kind', 'first_name', 'match_status', 'candidate_count'], unmatched)
        selected = {r['new_id'] for r in matched}
        part = [r for r, original in zip(rows, raw_rows)
                if machine == 'gentoo' or original['id'] in selected]
        write(target / ('part-' + machine + '.tsv'), HEADER, part)
        if not delivered:
            original_path = ROOT / 'D1b/raw' / machine / 'objects.tsv'
            undelivered = read(original_path) if original_path.is_file() else []
            write(target / ('not-delivered-' + machine + '.tsv'), ['id', 'machine', 'raw_id'],
                  [dict(id='d1b-' + machine + '-' + r['id'], machine=machine, raw_id=r['id']) for r in undelivered])
        metadata = source.parent / 'metadata.json'
        summaries[machine] = dict(delivered=delivered, all=len(rows), decide=len(part),
                                  matched=len(matched), unmatched=len(unmatched),
                                  kinds=dict(sorted(collections.Counter(r['kind'] for r in rows).items())),
                                  levels=dict(collections.Counter(r['level'] for r in raw_rows)),
                                  metadata=json.loads(metadata.read_text()) if delivered and metadata.is_file() else None)
        assert sum(summaries[machine]['kinds'].values()) == len(rows)
        assert machine == 'gentoo' or len(part) == len(matched)
    write(target / 'object-id-map.tsv', ['id', 'machine', 'raw_id'], mappings)
    write(target / 'operator/match-status.tsv', ['machine', 'exit_status', 'command'], statuses)
    (target / 'operator/inventory-summary.json').write_text(json.dumps(summaries, indent=2) + '\n')
    n = sum(s['delivered'] for s in summaries.values())
    k = sum(s['decide'] for s in summaries.values())
    u = sum(s['unmatched'] for s in summaries.values())
    print(f'D1b INVENTORY: {n} of 5 machines; {k} objects to decide; {u} first-night objects without a match')


if __name__ == '__main__':
    main()
