#!/usr/bin/env python3
"""Synthetic verification of the changed handoff only; no inventory or guest reads."""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('neutralize', HERE / 'neutralize.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def table(path, header, rows):
    with path.open('w', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)


def values(path):
    with path.open(newline='') as stream:
        return list(csv.reader(stream, delimiter='\t'))


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('report', type=Path, help='Must not exist')
args = parser.parse_args()
if args.report.exists():
    raise SystemExit('report already exists')
passed = []
with tempfile.TemporaryDirectory(prefix='synthetic-', dir=HERE) as work:
    work = Path(work)
    source = work / 'source'
    source.mkdir()
    (source / 'raw').mkdir()
    (source / 'members').mkdir()
    old = 'cache-identity-reference-not-install-receipt'
    # Deliberately use label-like strings in protected data fields.
    (source / 'raw/evidence.out').write_bytes(b'\x00\xff' + old.encode() + b'\nno-surviving-receipt\n')
    (source / 'members/synthetic.tsv').write_text('path\tvalue\n/test\tno-surviving-receipt\n')
    for name in ('objects.tsv', 'level-1.tsv', 'level-2.tsv'):
        table(source / name, ['id', 'machine', 'level', 'kind', 'name', 'members', 'evidence'],
              [['synthetic-id', 'synthetic', '2', 'synthetic-kind', old, '[]', 'raw/evidence.out']])
    table(source / 'npm-archive-sources.tsv', ['status', 'path'],
          [['verified-archive:' + old, old], ['archive-unreadable-or-integrity-mismatch', 'synthetic'],
           ['verified-archive:lock-receipt-reference', 'lock-receipt-reference']])
    table(source / 'old-package-member-integrity.tsv', ['path', 'status', 'expected', 'actual'],
          [['/test', 'no-surviving-receipt', '', ''], ['/other', 'equal', 'abc', 'abc'],
           ['/directory', 'directory-receipt', '', '']])
    (source / 'old-package-receipt-sources.tsv').write_text('source\tstatus\tevidence\n/manifest\tread\traw/evidence.out\n')
    table(source / 'void-configuration-facts.tsv', ['historical_creator', 'content_base64'],
          [['unknown: no creation event established by current file', 'AAE=']])
    alma_pairs = [
        ('recorded-snapshot-not-history', 'recorded-snapshot'),
        ('recorded-not-intent-proof', 'recorded-directives'),
        ('recorded-not-history-proof', 'recorded-current-query'),
        ('partial-evidence-not-complete-history', 'recorded-bounded-extract'),
        ('script-presence-not-execution-proof', 'recorded-script-text')]
    table(source / 'alma-facts.tsv', ['object_id', 'path', 'fact', 'value', 'status', 'evidence'],
          [['synthetic-id', '/test', 'synthetic', 'quoted\tvalue\n' + a, a, 'raw/evidence.out'] for a, _ in alma_pairs]
          + [['synthetic-id', '/test', 'synthetic', '', 'unavailable', 'raw/failure.err']])
    table(source / 'talos-fact-index.tsv', ['object_id', 'backing', 'image_integrity'],
          [['synthetic-id', 'unknown:mountinfo-unavailable', 'unknown:no-original-image-manifest']])
    (source / 'fact-summary.json').write_text(json.dumps({
        'adapters': {'npm': {old: 7, 'verified_archives': 7, 'lock-receipt-reference': 41},
                     'old-package': {'no-surviving-receipt': 9, 'equal': 4, 'directory-receipt': 4294,
                                     **{'unowned-with-receipt-' + s: i for i, s in enumerate(
                                         ['unknown', 'directory-receipt', 'equal', 'different-or-absent', 'different', 'absent'])}}},
        'counts': {'literal': old, 'objects': 1}}))
    before = {p.relative_to(source).as_posix(): p.read_bytes() for p in source.rglob('*') if p.is_file()}
    destination = work / 'handoff'
    result = module.handoff(source, destination, work / 'audit.json')
    assert len(result['changes']) == 21 and all(c['count'] == 1 for c in result['changes'])
    assert {(r['file'], r['field'], r['old'], r['new']) for r in module.rules()} == {
        (r['file'], r['field'], r['old'], r['new']) for r in result['changes']}
    assert values(destination / 'npm-archive-sources.tsv')[1:] == [
        ['verified-archive:cache-identity-reference', old], ['archive-unreadable-or-integrity-mismatch', 'synthetic'],
        ['verified-archive:lock-reference', 'lock-receipt-reference']]
    assert values(destination / 'old-package-member-integrity.tsv')[1:] == [
        ['/test', 'no-reference-found', '', ''], ['/other', 'equal', 'abc', 'abc'],
        ['/directory', 'directory-entry', '', '']]
    assert values(destination / 'void-configuration-facts.tsv')[1] == ['unknown:creator-field-empty', 'AAE=']
    alma_before = values(source / 'alma-facts.tsv')
    alma_after = values(destination / 'alma-facts.tsv')
    assert alma_before[0] == alma_after[0] and alma_before[-1] == alma_after[-1]
    for left, right, (_, expected) in zip(alma_before[1:-1], alma_after[1:-1], alma_pairs):
        assert right[4] == expected and left[:4] + left[5:] == right[:4] + right[5:]
    assert values(destination / 'talos-fact-index.tsv')[1] == [
        'synthetic-id', 'unknown:mountinfo-unavailable', 'unknown:image-reference-field-empty']
    summary = json.loads((destination / 'fact-summary.json').read_bytes())
    assert summary == {'adapters': {'npm': {'cache-identity-reference': 7, 'verified_archives': 7, 'lock-reference': 41},
                                    'old-package': {'no-reference-found': 9, 'equal': 4, 'directory-entry': 4294,
                                                    **{'unowned-with-reference-' + s: i for i, s in enumerate(
                                                        ['unknown', 'directory-entry', 'equal', 'different-or-absent', 'different', 'absent'])}}},
                       'counts': {'literal': old, 'objects': 1}}
    changed = {r['file'] for r in result['changes']}
    for name, data in before.items():
        assert (source / name).read_bytes() == data
        if name not in changed:
            assert (destination / name).read_bytes() == data
    passed += ['all 21 mapped cells/keys including every positive label and counter', 'only designated fields changed',
               'quoted multiline values preserved', 'unknowns, failures and empty values preserved',
               'objects, levels, members and raw evidence byte-identical', 'original source byte-identical',
               'diagnostic numeric values unchanged']
    assert (source / 'old-package-receipt-sources.tsv').read_bytes() == (destination / 'old-package-receipt-sources.tsv').read_bytes()
    assert all(r['new'].startswith('unknown:') for r in module.rules() if r['old'].startswith('unknown:'))
    passed += ['source-table filename and bytes preserved', 'every mapped unknown retains its prefix']

    # Reapplying the transformation to neutral data must be a byte-identical copy.
    second = work / 'second'
    again = module.handoff(destination, second, work / 'second-audit.json')
    assert again['changes'] == []
    assert all((second / name).read_bytes() == (destination / name).read_bytes() for name in before)
    passed.append('already neutral data byte-identical')

    def rejects(label, src, dst, report):
        try:
            module.handoff(src, dst, report)
        except (ValueError, OSError):
            passed.append(label)
        else:
            raise AssertionError('accepted invalid input: ' + label)

    rejects('existing destination rejected', source, destination, work / 'unused.json')
    rejects('existing audit rejected', source, work / 'unused', work / 'audit.json')
    rejects('destination inside source rejected', source, source / 'nested', work / 'unused.json')
    rejects('audit inside destination rejected', source, work / 'unused', work / 'unused/audit.json')
    link_source = work / 'links'
    link_source.mkdir()
    (link_source / 'outside').symlink_to(source)
    rejects('source links rejected', link_source, work / 'unused', work / 'unused.json')
    malformed = work / 'malformed'
    malformed.mkdir()
    (malformed / 'alma-facts.tsv').write_text('status\tvalue\nunavailable\n')
    rejects('malformed row rejected before copy', malformed, work / 'unused', work / 'unused.json')
    assert not (work / 'unused').exists()
    (malformed / 'alma-facts.tsv').write_text('value\nsynthetic\n')
    rejects('missing mapped field rejected', malformed, work / 'unused', work / 'unused.json')
    (malformed / 'alma-facts.tsv').unlink()
    (malformed / 'fact-summary.json').write_text(json.dumps({'adapters': {'npm': {old: 1, 'cache-identity-reference': 2}}}))
    rejects('counter collision rejected', malformed, work / 'unused', work / 'unused.json')
    partial = work / 'partial'
    partial.mkdir()
    (partial / 'metadata.json').write_text('{"filesystem_complete":false}\n')
    partial_result = module.handoff(partial, work / 'partial-handoff', work / 'partial-audit.json')
    assert partial_result['changes'] == [] and partial_result['source_files'] == 1
    passed.append('missing optional tables remain missing')
result = {'date_utc': '2026-11-23', 'passed': passed, 'checks_passed': len(passed),
          'live_queries': 0, 'rehearsal_inventory_reads': 0, 'synthetic_trees_deleted': True,
          'independent_acceptance': 'not performed by this check'}
with args.report.open('x') as stream:
    stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
