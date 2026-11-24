#!/usr/bin/env python3
"""Offline BC3 evidence audit. Never runs guests or alters input evidence.

Exit 0 means structurally complete, including honestly reported failed assertions.
Exit 1 means inconsistent/malformed evidence; exit 2 means incomplete evidence.
A nonzero suite exit is a result, not by itself an audit inconsistency.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

B2 = Path(__file__).resolve().parents[1]
REG = 'carried-suite/regressions/'
SUITES = ['cases.jsonl', 'objects.jsonl', 'objects-reboot.jsonl', 'shell.jsonl',
          'shell-reboot.jsonl', 'gate.jsonl', 'tools.jsonl',
          'supplement-direct.jsonl', 'supplement-extra.jsonl']
SUITES += ['carried-suite/' + x + '.jsonl' for x in ('language', 'applications', 'system', 'ordinary')]
SUITES += [REG + 'round' + str(x) + '.jsonl' for x in (1, 2, 3)]
SUITES += [REG + x for x in ('powercuts.jsonl', 'boot-order.jsonl', 'inventory.jsonl',
                             'independent-stand-compare.jsonl', 'original/D10-compare.jsonl')]
SUITES += ['combined/events.jsonl', 'combined/stand-compare.jsonl']
SUITES += ['combined/' + s + '-' + suffix for s in ('a', 'b')
           for suffix in ('exact.jsonl', 'reboot-exact.jsonl', 'schedule.jsonl')]
VERDICTS = ('passed', 'pass_', 'ok', 'equal')
DYNAMIC_COMPARISONS = {
    REG + 'independent-stand-compare.jsonl': (
        REG + 'peer-a/added.json', REG + 'peer-b/added.json',
        REG + 'peer-a/dev-add/machine.jsonl', REG + 'peer-b/dev-add/machine.jsonl'),
    REG + 'original/D10-compare.jsonl': (
        REG + 'original/peer-a/added.json', REG + 'original/peer-b/added.json',
        REG + 'original/peer-a/dev-add/machine.jsonl', REG + 'original/peer-b/dev-add/machine.jsonl'),
    'combined/stand-compare.jsonl': ('combined/a-snapshot.json', 'combined/b-snapshot.json', None, None),
}


class Audit:
    def __init__(self, root, baseline):
        self.root, self.baseline = root, baseline
        self.missing, self.errors, self.false, self.unavailable = [], [], [], []
        self.counts, self.controllers, self.cache = {}, {}, {}

    def need(self, relative):
        p = self.root / relative
        if not p.is_file():
            if relative not in self.missing: self.missing.append(relative)
            return None
        return p

    def error(self, text):
        self.errors.append(text)

    def document(self, relative):
        p = self.need(relative)
        if p is None: return None
        try: return json.loads(p.read_text())
        except (ValueError, OSError) as e:
            self.error(relative + ': ' + type(e).__name__)
            return None

    def records(self, relative):
        if relative in self.cache: return self.cache[relative]
        p = self.need(relative)
        rows = []
        if p:
            for number, line in enumerate(p.read_text().splitlines(), 1):
                # Native logs intentionally mix JSON, shell output and readbacks.
                if not line.startswith('{'): continue
                try:
                    value = json.loads(line)
                    if not isinstance(value, dict): raise ValueError()
                    rows.append(value)
                except ValueError: self.error(f'{relative}:{number}: malformed JSON record')
        self.cache[relative] = rows
        return rows

    @staticmethod
    def signature(row):
        if row.get('phase') == 'summary' or row.get('event') == 'summary': return None
        fields = tuple(k for k in VERDICTS if type(row.get(k)) is bool)
        return (row.get('id', row.get('name')), row.get('phase'), fields) if fields else None

    def observe(self, relative, rows):
        passed = failed = 0
        for index, r in enumerate(rows):
            if r.get('phase') == 'summary' or r.get('event') == 'summary': continue
            fields = [k for k in VERDICTS if type(r.get(k)) is bool]
            bad = [k for k in fields if not r[k]]
            if fields:
                failed += bool(bad); passed += not bad
            if bad:
                self.false.append({'file': relative, 'record': index,
                    'id': r.get('id', r.get('name')), 'false_fields': bad,
                    'required': r.get('required'),
                    'included_in_implemented_check_exit': r.get('included_in_implemented_check_exit')})
            status = str(r.get('status', r.get('phase', ''))).upper()
            if status in ('UNTESTED', 'UNAVAILABLE', 'NOT-TESTED', 'NOT_ESTABLISHED', 'FACT_UNKNOWN'):
                self.unavailable.append({'file': relative, 'record': index,
                    'id': r.get('id', r.get('name')), 'status': status})
        self.counts[relative] = {'passed_records': passed, 'false_records': failed,
                                 'boolean_records': passed + failed, 'json_records': len(rows)}

    def dynamic_comparison(self, relative, rows):
        snapshots = []
        a, b, da, db = DYNAMIC_COMPARISONS[relative]
        for snapshot_path, declaration_path in ((a, da), (b, db)):
            snapshot = self.document(snapshot_path)
            if snapshot is None: return
            if not isinstance(snapshot, list) or any(not isinstance(r, dict) or 'id' not in r for r in snapshot):
                self.error(snapshot_path + ': malformed reader snapshot'); return
            byid = {r['id']: r for r in snapshot}
            if len(byid) != len(snapshot): self.error(snapshot_path + ': duplicate reader IDs')
            if declaration_path:
                declaration = self.records(declaration_path)
                if self.root.joinpath(declaration_path).is_file():
                    expected = {r['id']: r['type'] for r in declaration}
                    if len(expected) != len(declaration): self.error(declaration_path + ': duplicate declaration IDs')
                    if {r['id']: r.get('type') for r in snapshot} != expected:
                        self.error(snapshot_path + ': current declaration/reader inventory differs')
            snapshots.append(byid)
        left, right = snapshots
        expected_ids = set(left) | set(right)
        actual_ids = [r.get('id') for r in rows]
        if len(actual_ids) != len(set(actual_ids)): self.error(relative + ': duplicate comparison IDs')
        absent = expected_ids - set(actual_ids)
        extra = set(actual_ids) - expected_ids
        if absent: self.missing.append({'file': relative, 'missing_current_reader_ids': sorted(absent)})
        if extra: self.error(relative + ': comparison IDs outside current readers: ' + repr(sorted(extra)))
        for row in rows:
            ident = row.get('id')
            if row.get('left') != left.get(ident) or row.get('right') != right.get(ident):
                self.error(relative + ': comparison payload differs from saved readers: ' + str(ident))
            if row.get('equal') != (left.get(ident) == right.get(ident)):
                self.error(relative + ': equality verdict contradicts current readers: ' + str(ident))

    def contract(self, relative, rows):
        if relative in DYNAMIC_COMPARISONS:
            self.dynamic_comparison(relative, rows)
            return
        # Baseline supplies fixed assertion identities, never expected truth values.
        p = self.baseline / relative
        if not p.exists() or relative == 'cases.jsonl': return
        expected = []
        for line in p.read_text().splitlines():
            if line.startswith('{'):
                try: expected.append(json.loads(line))
                except ValueError: continue
        left = Counter(x for x in map(self.signature, expected) if x)
        right = Counter(x for x in map(self.signature, rows) if x)
        absent = left - right
        extra = right - left
        if absent: self.missing.append({'file': relative, 'missing_assertions': [list(k) + [v] for k, v in absent.items()]})
        if extra: self.error(relative + ': unexpected assertion identities ' + repr(dict(extra)))

    def readback(self, relative, expected=None):
        p = self.need(relative)
        if not p: return
        seen = []
        for n, line in enumerate(p.read_text().splitlines(), 1):
            f = line.split('\t')
            if len(f) == 4 and f[2] in ('OK', 'FAIL'):
                seen.append(f[0])
                if f[2] == 'FAIL': self.false.append({'file': relative, 'line': n, 'id': f[0], 'false_fields': ['readback'], 'required': True})
        if not seen: self.missing.append(relative + ': no readback rows')
        if len(seen) != len(set(seen)): self.error(relative + ': duplicate readback IDs')
        if expected is not None and set(seen) != set(expected): self.error(relative + ': readback ID inventory differs')
        self.counts[relative] = {'readback_rows': len(seen)}

    def run(self):
        summary = self.document('summary.json')
        steps = self.document('steps.json')
        ledger = self.document('whole-suite-ledger.json')
        plan = self.document('lane-plan.json')
        self.controllers['parent'] = summary
        if summary and steps is not None:
            if summary.get('steps') != steps: self.error('summary steps disagree with steps.json')
            logs = [s.get('log') for s in steps]
            if len(logs) != len(set(logs)): self.error('duplicate parent step logs')
            required = {'peer-build.log', 'carried-console.jsonl', 'regressions-console.jsonl', 'assemble.log', 'combined-console.jsonl', 'cases-export.log', 'cases-filesystem-verify.jsonl', 'objects-export.log', 'factory-export.log'}
            for suite in ('cases', 'objects', 'shell', 'gate', 'tools', 'supplement'):
                required.update([suite + '-new.log', suite + '-verify.log'])
            required.update(SUITES[:9])
            for suite in ('objects', 'shell', 'supplement'):
                required.update(suite + suffix for suffix in ('-before-verify.log', '-stop.log', '-start.log'))
            for name in sorted(required - set(logs)): self.missing.append('controller step: ' + name)
            for s in steps:
                self.need(s['log'])
                if type(s.get('exit')) is not int: self.error('step missing integer exit: ' + s['log'])
            lanes = summary.get('lanes', {})
            if set(lanes) != {'components', 'round4', 'round3'}: self.missing.append('three completed lane results')
            if ledger and ledger.get('lanes') != lanes: self.error('lane ledger differs from summary')
            computed = int(any(s.get('exit', 1) for s in steps) or any(x.get('exit', 1) for x in lanes.values()))
            if summary.get('controller_exit') == 0 and computed: self.error('parent reports success despite failed step/lane')
            self.controllers['nonzero_steps'] = [s for s in steps if s.get('exit')]
            self.controllers['cleanup'] = {'remaining_vms': summary.get('remaining_vms'), 'peer_remaining': summary.get('peer_remaining')}
            if summary.get('remaining_vms') or summary.get('peer_remaining') is not False:
                self.false.append({'file': 'summary.json', 'id': 'cleanup', 'required': True, 'false_fields': ['cleanup']})
        if plan and plan.get('max_lanes') != 3: self.error('unexpected lane plan')
        for relative in SUITES:
            rows = self.records(relative)
            self.observe(relative, rows)
            self.contract(relative, rows)
        cases = [r for r in self.records('cases.jsonl') if r.get('phase') == 'case_result']
        fixture = self.document('recipe-inputs/bc3-fixtures.json')
        if fixture:
            wanted = {r['id'] for r in fixture['cases']} | {fixture['account']['id'], 'ordinary-work'}
            got = [r.get('id') for r in cases]
            if set(got) != wanted: self.missing.append('seventeen complete BC3 case results')
            if len(got) != len(set(got)): self.error('duplicate BC3 case results')
        self.observe('cases-filesystem-verify.jsonl', self.records('cases-filesystem-verify.jsonl'))
        for folder in ('carried-suite', 'carried-suite/regressions', 'combined'):
            self.controllers[folder] = self.document(folder + '/summary.json')
        carried = self.controllers['carried-suite']
        if carried and set(carried.get('suites', {})) != {'language', 'applications', 'system', 'ordinary'}:
            self.missing.append('four carried suite results')
        reg = self.controllers['carried-suite/regressions']
        if reg and (reg.get('regressions_run') is not True or reg.get('independent_peer_supplied') is not True):
            self.missing.append('regressions and independent peer execution')
        power = self.records(REG + 'powercuts.jsonl')
        expected_ids = {f'POWER-{kind}-{i}' for kind in ('ADD', 'CHANGE', 'REMOVE') for i in range(1, 4)}
        for phase in ('expected', 'cut', 'result'):
            items = [r['id'] for r in power if r.get('phase') == phase]
            if set(items) != expected_ids: self.missing.append('nine powercut ' + phase + ' records')
            if len(items) != len(set(items)): self.error('duplicate powercut ' + phase)
        for n in range(1, 10): self.need(REG + f'original/D{n:02d}.log')
        for name in ('D10-peer-a.log', 'D10-peer-b.log', 'D10-summary.log'):
            self.need(REG + 'original/' + name)
        original = self.need(REG + 'original-console.log')
        if original and 'DEVELOPMENT OBSERVATIONS COMPLETE' not in original.read_text():
            self.missing.append('original D01-D10 completion marker')
        if original:
            native_exits = dict(re.findall(r'^(\S+) EXIT (-?\d+)$', original.read_text(), re.M))
            for ident in [f'D{i:02d}' for i in range(1, 10)] + ['D10-peer-a', 'D10-peer-b']:
                if ident not in native_exits: self.missing.append('native completion: ' + ident)
                elif int(native_exits[ident]): self.false.append({'file': REG + 'original-console.log', 'id': ident, 'required': True, 'false_fields': ['controller_exit'], 'exit': int(native_exits[ident])})
            self.controllers['native_exits'] = native_exits
        for name in ('boot-attempts.json', 'independent-compare.json'): self.document(REG + name)
        compare = self.document(REG + 'independent-compare.json')
        if compare:
            if compare.get('values_equal') != (compare.get('left') == compare.get('right')):
                self.error('independent peer equality flag inconsistent')
            self.observe(REG + 'independent-compare.json', compare.get('left', []) + compare.get('right', []))
            for key in ('values_equal', 'declaration_bytes_equal'):
                if compare.get(key) is not True: self.false.append({'file': REG + 'independent-compare.json', 'id': key, 'required': True, 'false_fields': [key]})
        if compare:
            peers = []
            for side in ('a', 'b'):
                directory = self.root / REG / ('peer-' + side) / 'dev-add'
                self.need(REG + 'peer-' + side + '/dev-add/machine.jsonl')
                peers.append({p.name: p.read_bytes() for p in directory.iterdir() if p.is_file()} if directory.exists() else None)
            if all(x is not None for x in peers) and compare.get('declaration_bytes_equal') != (peers[0] == peers[1]):
                self.error('independent declaration equality flag inconsistent with exports')
        for name in ('cases', 'objects', 'shell', 'gate', 'tools', 'supplement'): self.readback(name + '-verify.log')
        for name in ('objects', 'shell', 'supplement'): self.readback(name + '-before-verify.log')
        for name in ('language', 'applications', 'system', 'ordinary'): self.readback('carried-suite/' + name + '-verify.jsonl')
        combined = self.controllers['combined']
        if combined:
            if combined.get('snapshot_sides') != ['a', 'b'] or set(combined.get('results', {})) != {'a', 'b'}:
                self.missing.append('combined replay on both images')
            for side in ('a', 'b'):
                rows = self.document('combined/' + side + '-snapshot.json')
                if rows is not None:
                    if len(rows) != combined.get('declaration_rows'): self.error('combined snapshot row count differs')
                    ids = [r['id'] for r in rows]
                    if len(ids) != len(set(ids)): self.error('combined snapshot duplicate IDs')
                    self.observe('combined/' + side + '-snapshot.json', rows)
                    for suffix in ('verify.jsonl', 'reboot-verify.jsonl'): self.readback('combined/' + side + '-' + suffix, ids)
        for name in ('image.json', 'validated-build.json', 'peer-image.json', 'complete-example.json', 'input-sha256.json'):
            self.document(name)
        hashes = self.document('input-sha256.json')
        if hashes:
            for relative, wanted in hashes.items():
                folder, name = relative.split('/', 1)
                p = self.need(('recipe-inputs/' if folder == 'build' else 'controller-inputs/') + name)
                if p and hashlib.sha256(p.read_bytes()).hexdigest() != wanted: self.error('frozen source hash mismatch: ' + relative)
        metadata = self.document('complete-example.json')
        if metadata:
            for side in ('a', 'b'):
                for suffix in ('exact.jsonl', 'reboot-exact.jsonl'):
                    for row in self.records('combined/' + side + '-' + suffix):
                        if row.get('files_sha256', {}).get('machine.jsonl') != metadata.get('machine_sha256'):
                            self.error('combined exact declaration identity differs: ' + side + '-' + suffix)
        self.need('recipe.log')
        self.need('peer-build.log')
        return {'audit_status': 'inconsistent' if self.errors else 'incomplete' if self.missing else 'complete',
                'errors': self.errors, 'missing': self.missing, 'counts': self.counts,
                'false_observations': self.false, 'unavailable_observations': self.unavailable,
                'controllers': self.controllers, 'historical_verdicts_reclassified': False,
                'inherited_comparison_scope': {
                    'peer': 'Original machine declaration and original reader rows only.',
                    'combined': 'Original combined machine declaration and original reader rows only.',
                    'excluded': 'No byte-equality claim for the five BC3 filesystem declarations or the eight-file complete declaration bundle.'},
                'hypothesis_outcome': '?', 'limitations': [
                    'Offline saved-evidence audit, not independent reproduction or acceptance.',
                    'Historical tests inspect their original declaration model; their false verdicts are retained.',
                    'Boolean counts are per top-level observation record, excluding summaries; nested assertions are not added again.',
                    'Controller exits and assertion truth are reported independently of structural completeness.',
                    'Inherited peer and combined comparisons do not compare the five BC3 filesystem declarations or eight-file complete bundle.']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--final', type=Path, default=B2 / 'raw/round-3/final-1-validation')
    p.add_argument('--baseline', type=Path, default=B2 / 'raw/round-2/final-1')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    result = Audit(a.final, a.baseline).run()
    text = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if a.output:
        if not a.output.resolve().is_relative_to((B2 / 'raw/round-3').resolve()):
            p.error('output must be inside this round evidence folder')
        a.output.write_text(text)
    print(text, end='')
    return {'complete': 0, 'inconsistent': 1, 'incomplete': 2}[result['audit_status']]


if __name__ == '__main__':
    raise SystemExit(main())
