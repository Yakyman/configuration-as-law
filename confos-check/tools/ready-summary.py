#!/usr/bin/env python3
"""The summary of a run for READY.md ([n3-C]): counts by part and outcome, and for every `fail` row one
line naming the object or the probe that counts against it.

ready-summary.py RUNS_DIR/NAME

For a P1 row: the first UNRECORDED or changed stored object of its compare-p1.tsv (with its reason). For a P2 row: the
first MISSING or DIFFERS line of its comparison. For an UND row: the first line of the easier reading's comparison that
counts. For a P4 row: the probe that counts, else the first line of attempt-effect.tsv. For other rows: the first
reason of the outcome file. Python 3 standard library only.
"""
import collections
import json
import sys
from pathlib import Path

STORED = {'file', 'dir', 'symlink', 'other', 'vfile', 'vdir', 'vsymlink', 'vother'}


def outcome_file(run, rel):
    p = run / rel
    reasons, extra = [], {}
    if not p.exists():
        return reasons, extra
    text = p.read_text(errors='replace')
    head, sep, tail = text.partition('\n{')
    for line in head.splitlines():
        if line.startswith('reason: '):
            reasons.append(line[8:])
    if sep:
        try:
            extra = json.loads('{' + tail)
        except ValueError:
            extra = {}
    return reasons, extra


def first_line(run, rel, verdicts, stored_differs=False):
    p = run / rel if rel else None
    if not p or not p.exists():
        return None
    for line in p.read_text(errors='replace').splitlines():
        f = line.split('\t')
        if f[0] in verdicts or (stored_differs and f[0] == 'DIFFERS' and len(f) > 1 and f[1] in STORED):
            return ' '.join(f)[:300]
    return None


def main():
    run = Path(sys.argv[1])
    rows = [l.split('\t') for l in (run / 'results.tsv').read_text().splitlines() if l.strip()]
    counts = collections.Counter((r[1], r[2]) for r in rows)
    parts = sorted({r[1] for r in rows})
    outs = ('pass', 'fail', 'unobserved', 'undecided')
    print('| part | ' + ' | '.join(outs) + ' | all |')
    print('|---|' + '---|' * (len(outs) + 1))
    for p in parts:
        print(f'| {p} | ' + ' | '.join(str(counts[(p, o)]) for o in outs) + f' | {sum(counts[(p, o)] for o in outs)} |')
    print(f'| all | ' + ' | '.join(str(sum(counts[(p, o)] for p in parts)) for o in outs) + f' | {len(rows)} |')
    print()
    for r in rows:
        if r[2] != 'fail':
            continue
        rid, part, _, ev = r[:4]
        reasons, extra = outcome_file(run, ev)
        what = None
        if part == 'P1':
            what = first_line(run, extra.get('compare'), ('UNRECORDED',), stored_differs=True)
        elif part == 'P2':
            what = first_line(run, extra.get('compare'), ('MISSING', 'DIFFERS'))
        elif part == 'UND':
            easy = (extra.get('easier') or {}).get('compare')
            what = first_line(run, easy, ('UNRECORDED', 'DIFFERS', 'MISSING'))
        elif part == 'P4':
            probe = next((x for x in reasons if x.startswith('probe ')), None)
            if probe:
                what = probe
            else:
                eff = run / ev.split('/')[0] / 'attempt-effect.tsv'
                if eff.exists():
                    lines = [l for l in eff.read_text(errors='replace').splitlines() if l.strip()]
                    if lines:
                        what = ' '.join(lines[0].split('\t'))[:300] + (f' (+{len(lines) - 1} more)' if len(lines) > 1
                                                                        else '')
        if what is None:
            what = (reasons[0] if reasons else 'no reason recorded')[:300]
        print(f'- `{rid}` ({part}): {what}')


if __name__ == '__main__':
    main()
