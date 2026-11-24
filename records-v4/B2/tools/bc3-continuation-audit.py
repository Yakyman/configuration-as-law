#!/usr/bin/env python3
"""Separate offline continuation audit; never modifies or merges original results.

0: complete, consistent continuation evidence (false observations remain false).
1: inconsistent/malformed evidence. 2: missing continuation/original evidence.
The original full suite remains incomplete for every exit value.
"""
import argparse
import ast
import base64
from collections import Counter
import hashlib
import json
from pathlib import Path

B2 = Path(__file__).resolve().parents[1]
GUEST = 'evidence/bc3-round2-continuation/'


def sha(data): return hashlib.sha256(data).hexdigest()


class Audit:
    def __init__(self, root, original, historic, plan):
        self.root, self.original, self.historic, self.plan = root, original, historic, plan
        self.missing, self.errors, self.false = [], [], []
        self.report = {'original_whole_suite_remains_incomplete': True,
                       'primary_audit_unchanged': True, 'results_merged_into_original': False}

    def read(self, path):
        if not path.is_file():
            self.missing.append(str(path.relative_to(B2)) if path.is_relative_to(B2) else path.name)
            return None
        return path.read_bytes()

    def doc(self, path):
        data = self.read(path)
        if data is None: return None
        try: return json.loads(data)
        except ValueError:
            self.errors.append(path.name + ': malformed JSON')
            return None

    def rows(self, path):
        data = self.read(path)
        rows = []
        if data is not None:
            for n, line in enumerate(data.decode().splitlines(), 1):
                if not line.startswith('{'): continue
                try: rows.append(json.loads(line))
                except ValueError: self.errors.append(f'{path.name}:{n}: malformed JSON record')
        return rows

    def insist(self, condition, message):
        if not condition: self.errors.append(message)

    @staticmethod
    def observations(rows):
        return [r for r in rows if type(r.get('passed')) is bool and r.get('phase') != 'summary']

    def run(self):
        plan = self.doc(self.plan)
        if plan is None: return self.finish()
        source = self.read(self.root / 'round2-selftest.py')
        probe = self.read(self.root / 'round2-probe.c')
        continuation = self.read(self.root / 'round2-continuation.py')
        host = self.read(self.root / 'host-controller.py')
        expected_hashes = {'round2-selftest.py': plan['original_sha256'],
                           'round2-probe.c': plan['probe_sha256'],
                           'round2-continuation.py': plan['continuation_sha256']}
        inputs = self.doc(self.root / 'input-sha256.json')
        if inputs:
            self.insist(set(inputs) == set(expected_hashes) | {'host-controller.py'}, 'input hash inventory differs')
            for name, digest in inputs.items():
                data = self.read(self.root / name)
                if data is not None: self.insist(sha(data) == digest, 'input digest differs: ' + name)
        for name, digest in expected_hashes.items():
            data = self.read(self.root / name)
            if data is not None: self.insist(sha(data) == digest, 'fixed plan digest differs: ' + name)
        if source:
            lines = source.decode().splitlines(keepends=True)
            suffix = ''.join(lines[177:-1]).encode()
            self.insist(sha(suffix) == plan['unchanged_suffix_sha256'], 'original suffix digest differs')
        if continuation:
            try:
                tree = ast.parse(continuation)
                assignments = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)}
                if source is not None: self.insist(base64.b64decode(assignments['SOURCE_B64']) == source, 'embedded original source differs')
                if probe is not None: self.insist(base64.b64decode(assignments['PROBE_B64']) == probe, 'embedded original probe differs')
                embedded = assignments['MANIFEST']
                self.insist(embedded == {k: v for k, v in plan.items() if k != 'continuation_sha256'}, 'embedded plan differs')
            except (ValueError, KeyError, SyntaxError): self.errors.append('continuation provenance extraction failed')
        guest_plan = self.doc(self.root / GUEST / 'provenance.json')
        if guest_plan:
            self.insist(guest_plan == {k: v for k, v in plan.items() if k != 'continuation_sha256'}, 'guest provenance differs')
        for name, data in [('round2-selftest.py', source), ('round2-probe.c', probe)]:
            exported = self.read(self.root / GUEST / name)
            if exported is not None and data is not None: self.insist(exported == data, 'guest original bytes differ: ' + name)
        rows = self.rows(self.root / 'suffix.jsonl')
        guest_rows = self.rows(self.root / GUEST / 'observations.jsonl')
        if rows and guest_rows: self.insist(rows == guest_rows, 'stdout and exported observation records differ')
        observed = self.observations(rows)
        ids = [r.get('id') for r in observed]
        expected = plan['expected_result_ids']
        if len(observed) < len(expected): self.missing.append('continuation suffix result records')
        self.insist(ids == expected[:len(ids)], 'suffix result order/identity differs or earlier test repeated')
        self.insist(len(ids) == len(set(ids)), 'duplicate suffix result IDs')
        self.insist(all(r.get('continuation_scope') == 'suffix' for r in observed), 'setup or foreign result counted as suffix')
        setup = [r for r in rows if r.get('phase') == 'setup_result']
        if len(setup) < 4: self.missing.append('four fixture setup results')
        self.insist([r.get('id') for r in setup] == plan['setup_ids'][:len(setup)], 'setup result IDs/order differs')
        self.insist(all('passed' not in r and r.get('continuation_scope') == 'setup' for r in setup), 'setup contaminated assertion results')
        if observed:
            self.insist(len(setup) == 4 and all(r.get('setup_passed') is True for r in setup), 'suffix entered without four successful setup operations')
        untested = [r for r in rows if r.get('phase') == 'not-tested']
        if not untested: self.missing.append('explicit SEALED-FIFO NOT-TESTED record')
        else:
            self.insist(len(untested) == 1 and untested[0].get('id') == 'SEALED-FIFO' and untested[0].get('status') == 'NOT-TESTED' and 'passed' not in untested[0], 'FIFO unavailable record differs or claims pass')
        self.insist(not any(r.get('id') == 'SEALED-FIFO' and r.get('phase') in ('expected', 'result') for r in rows), 'FIFO attempted again')
        for r in observed:
            if not r['passed']: self.false.append({'scope': 'suffix', 'id': r['id'], 'passed': False})
        for r in setup:
            if r.get('setup_passed') is not True: self.false.append({'scope': 'setup', 'id': r.get('id'), 'setup_passed': r.get('setup_passed')})
        completions = [r for r in rows if r.get('phase') == 'continuation_completion']
        if not completions: self.missing.append('continuation completion record')
        else:
            self.insist(len(completions) == 1, 'duplicate continuation completion')
            end = completions[0]
            self.insist(end.get('observed_ids') == ids and end.get('observed_results') == len(ids), 'completion inventory differs')
            self.insist(end.get('result_inventory_complete') == (ids == expected), 'completion completeness flag inconsistent')
            self.insist(end.get('whole_original_suite_complete') is False, 'completion falsely closes original suite')
            self.insist(end.get('suffix_exit') == int(any(not r['passed'] for r in observed)), 'suffix exit contradicts results')
        original_rows = self.rows(self.original)
        original = self.observations(original_rows)
        old_ids = [r.get('id') for r in original]
        historical = self.observations(self.rows(self.historic))
        historical_ids = [r.get('id') for r in historical]
        if historical_ids: self.insist(len(historical_ids) == len(set(historical_ids)) == 133, 'historical 133-result inventory differs')
        if not original: self.missing.append('original carried prefix observations')
        else:
            if len(old_ids) < 73: self.missing.append('all 73 original prefix observations')
            self.insist(len(old_ids) <= 73, 'original prefix exceeds fixed 73 observations')
            if historical_ids: self.insist(old_ids == historical_ids[:len(old_ids)], 'original prefix identities differ')
            self.insist(not any(r.get('phase') == 'summary' for r in original_rows), 'original abort unexpectedly has completed summary')
        self.insist(not set(old_ids) & set(ids), 'prior test repeated in suffix')
        if historical_ids: self.insist(historical_ids[73:] == ['SEALED-FIFO'] + expected, 'continuation does not match original unexecuted suffix inventory')
        for r in original:
            if not r['passed']: self.false.append({'scope': 'original-prefix', 'id': r['id'], 'passed': False})
        self.report['counts'] = {'original_observed': len(original), 'suffix_observed': len(observed),
            'original_passed': sum(r['passed'] for r in original), 'suffix_passed': sum(r['passed'] for r in observed),
            'distinct_observed_ids': len(set(old_ids) | set(ids)), 'expected_distinct_available': 132,
            'setup_results_excluded': len(setup), 'unavailable': len(untested), 'historic_inventory': len(historical)}
        self.report['not_tested'] = untested
        summary = self.doc(self.root / 'summary.json')
        steps = self.doc(self.root / 'steps.json')
        image = self.doc(self.root / 'image.json')
        if host and image:
            try:
                expected_image = next(ast.literal_eval(n.value) for n in ast.parse(host).body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'EXPECTED_IMAGE' for t in n.targets))
                self.insist(image.get('sha256') == image.get('expected_sha256') == expected_image and image.get('unchanged') is True, 'frozen image identity mismatch')
            except (StopIteration, ValueError, SyntaxError): self.errors.append('host image identity extraction failed')
        self.report['image'] = image
        self.report['controller'] = summary
        if summary and steps is not None:
            self.insist(summary.get('steps') == steps, 'controller step ledger differs')
            logs = [s.get('log') for s in steps]
            for name in ('new.log', 'copy.log', 'suffix.jsonl', 'export.log', 'destroy.log'):
                if name not in logs: self.missing.append('controller step ' + name)
            self.insist(len(logs) == len(set(logs)), 'duplicate controller steps')
            for step in steps:
                self.read(self.root / step['log'])
                if step.get('exit'):
                    self.false.append({'scope': 'controller', 'id': step['log'], 'exit': step['exit']})
            if summary.get('controller_exit') == 0:
                # A failed first destroy may legitimately be followed by successful fallback.
                required = [s for s in steps if s['log'] in ('new.log', 'copy.log', 'suffix.jsonl', 'export.log')]
                self.insist(all(s.get('exit') == 0 for s in required), 'controller success contradicts required step exit')
            if summary.get('owned_guest_remaining') is not False:
                self.false.append({'scope': 'controller', 'id': 'cleanup', 'passed': False})
        return self.finish()

    def finish(self):
        self.report.update(audit_status='inconsistent' if self.errors else 'incomplete' if self.missing else 'complete',
            errors=self.errors, missing=self.missing, false_observations=self.false,
            hypothesis_outcome='?', limitations=[
                'Separate offline continuation audit, not independent guest reproduction or acceptance.',
                'Setup records are excluded; original controller failure and unavailable FIFO remain unchanged.',
                'No result is merged into the primary whole-suite audit, whose missing suffix remains visible.'])
        return self.report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--final', type=Path, default=B2 / 'raw/round-3/final-1-continuation')
    p.add_argument('--original', type=Path, default=B2 / 'raw/round-3/final-1-validation/carried-suite/regressions/round2.jsonl')
    p.add_argument('--historic', type=Path, default=B2 / 'raw/round-2/final-1/carried-suite/regressions/round2.jsonl')
    p.add_argument('--plan', type=Path, default=B2 / 'raw/round-3/parts/round2-continuation.json')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    result = Audit(a.final, a.original, a.historic, a.plan).run()
    data = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if a.output:
        if not a.output.resolve().is_relative_to((B2 / 'raw/round-3').resolve()): p.error('output must stay in round-3')
        a.output.write_text(data)
    print(data, end='')
    return {'complete': 0, 'inconsistent': 1, 'incomplete': 2}[result['audit_status']]


if __name__ == '__main__': raise SystemExit(main())
