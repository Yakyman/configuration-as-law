#!/usr/bin/env python3
"""The body of RUN-<n>.md for a complete run: counts by part and outcome, then one line for every row that is not
`pass` — the row, the outcome, the questions it depends on, one sentence of reason, the evidence file — and, for a P1
or UND row that is `undecided` because of `QUESTION` objects, each such object with its kind (`data-only`: Q11,
`any-only`: Q12) and its path, read from the compare table that decided the row.

run-report.py RUNS_DIR/NAME

Not one of the programs of the check: it reads only what the run wrote. Python 3 standard library only.
"""
import collections
import gzip
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util
_spec = importlib.util.spec_from_file_location('ready_summary', Path(__file__).resolve().parent / 'ready-summary.py')
rs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rs)

TAG = re.compile(r'\b(Q\d+|D\d+|R\d+|S8\.\d-\d+)\b')
OUTS = ('pass', 'fail', 'unobserved', 'undecided')


def read_text(p):
    if p.exists():
        return p.read_text(errors='replace')
    gz = Path(str(p) + '.gz')
    if gz.exists():
        with gzip.open(gz, 'rt', errors='replace') as f:
            return f.read()
    return None


def routes_kind(table, path):
    """data-only / any-only from routes.tsv beside the compare table, else from the Q number in the line."""
    rt = read_text(table.parent / 'routes.tsv')
    if rt:
        for line in rt.splitlines():
            f = line.split('\t')
            if len(f) > 1 and f[0] == path and f[1] in ('data-only', 'any-only'):
                return f[1]
    return None


def question_objects(run, rel):
    if not rel:
        return []
    table = run / rel
    text = read_text(table)
    if text is None:
        return [('?', f'(compare table {rel} not found)')]
    out = []
    for line in text.splitlines():
        f = line.split('\t')
        if f[0] != 'QUESTION' or len(f) < 3:
            continue
        path = f[2]
        why = f[3] if len(f) > 3 else ''
        kind = routes_kind(table, path)
        if kind is None:
            kind = 'data-only' if 'Q11' in why else 'any-only' if 'Q12' in why else 'other: ' + why[:120]
        out.append((kind, f'{f[1]} {path}'))
    return out


TOOL = re.compile(r'the built-in tool \(([^)]*)\) refused')


def short_reason(part, outcome, reasons, extra):
    """One sentence for the usual forms of the runner's outcome text; None for any other form (then the text
    itself is printed, cut at 400 characters)."""
    joined = ' | '.join(reasons)
    easy = extra.get('easier') or {}
    hard = extra.get('harder') or {}
    if outcome == 'undecided' and part in ('P1', 'UND') and (
            'reading A of Q4' in joined or (part == 'UND' and easy.get('outcome') == 'fail')):
        # run, p1_und_rows: an inventory `-before` of a P4-PIPE case that would fail is `undecided` by Q4 (reading A
        # judges only the state after the restart); the UND reason text of the runner names D1–D6 there instead
        what = (f'{easy.get("counts")} against the reference installation' if part == 'UND'
                else reasons[0].split(': ', 1)[-1])
        return (f'Q4: the state before the restart, {what}: counts under reading B of Q4, is not judged under '
                'reading A' + ('; the runner\'s reason text names D1–D6 here, the outcome comes from Q4 (run, '
                               'p1_und_rows)' if part == 'UND' else ''))
    if part == 'UND' and outcome == 'undecided' and 'met under one reading only' in joined:
        s = (f'met against the reference installation (easier reading: {easy.get("outcome")}, '
             f'{easy.get("counts") or {}}), not under the derivation from the declaration alone '
             f'(harder reading: {hard.get("outcome")}); D1, D3–D6')
        if easy.get('outcome') == 'undecided':
            s += '; the easier reading itself is undecided by QUESTION objects (Q11/Q12), listed below'
        return s
    if part == 'P1' and outcome == 'undecided' and reasons and reasons[0].startswith('objects that equal neither'):
        return (reasons[0].replace('objects that equal neither the derivation nor the reference installation, after '
                                   'the four questions: ', 'after the four questions, objects that equal neither the '
                                   'derivation nor the reference installation: ')
                + '; undecided only by QUESTION (Q11, Q12) or BOTHWAYS (Q2), listed below')
    if part == 'P4' and outcome == 'undecided' and 'reading A of S8.3-7' in joined:
        m = TOOL.search(joined)
        return (f'S8.3-7: the built-in tool ({m.group(1) if m else "?"}) refused and nothing of the attempt is in '
                'force (met under reading A); it did not add the change to the declaration (not met under reading B); '
                'R3 of the review applies'
                + ''.join(f'; {x}' for x in reasons if x.startswith('note:')))
    return None


def main():
    run = Path(sys.argv[1])
    rows = [l.split('\t') for l in (run / 'results.tsv').read_text().splitlines() if l.strip()]
    counts = collections.Counter((r[1], r[2]) for r in rows)
    parts = sorted({r[1] for r in rows})
    print('| part | ' + ' | '.join(OUTS) + ' | all |')
    print('|---|' + '---|' * (len(OUTS) + 1))
    for p in parts:
        print(f'| {p} | ' + ' | '.join(str(counts[(p, o)]) for o in OUTS) + f' | {sum(counts[(p, o)] for o in OUTS)} |')
    print('| all | ' + ' | '.join(str(sum(counts[(p, o)] for p in parts)) for o in OUTS) + f' | {len(rows)} |')
    print()
    for r in rows:
        rid, part, outcome, ev = r[:4]
        if outcome == 'pass':
            continue
        reasons, extra = rs.outcome_file(run, ev)
        tags = []
        for x in reasons:
            for t in TAG.findall(x):
                if t not in tags:
                    tags.append(t)
        what = None
        if outcome == 'fail':
            if part == 'P1':
                what = rs.first_line(run, extra.get('compare'), ('UNRECORDED',), stored_differs=True)
            elif part == 'P2':
                what = rs.first_line(run, extra.get('compare'), ('MISSING', 'DIFFERS'))
            elif part == 'UND':
                what = rs.first_line(run, (extra.get('easier') or {}).get('compare'),
                                     ('UNRECORDED', 'DIFFERS', 'MISSING'))
        reason = short_reason(part, outcome, reasons, extra)
        if reason is None:
            reason = ' | '.join(x for x in reasons if not x.startswith('P1: fail on')) or 'no reason recorded'
            reason = reason.replace('\n', ' ')[:400]
        if what:
            reason = f'{reason}; first object: {what}'
        if '--long' in sys.argv:
            reason = ' | '.join(reasons)
        print(f'- `{rid}` ({part}) **{outcome}** [{", ".join(tags) or "-"}]: {reason} — `{ev}`')
        if outcome == 'undecided' and part in ('P1', 'UND'):
            tables = [extra.get('compare')] if part == 'P1' else [(extra.get('easier') or {}).get('compare')]
            for t in tables:
                for kind, obj in question_objects(run, t):
                    print(f'  - QUESTION `{kind}` {obj} (`{t}`)')
                if reason.startswith('Q4:'):
                    text = read_text(run / t) if t else None
                    for line in (text or '').splitlines():
                        f = line.split('\t')
                        if f[0] == 'UNRECORDED':
                            print(f'  - UNRECORDED {f[1]} {f[2]}: {(f[3] if len(f) > 3 else "")[:200]} (`{t}`)')


if __name__ == '__main__':
    main()
