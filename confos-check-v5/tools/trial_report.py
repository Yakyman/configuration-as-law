# SPDX-License-Identifier: MIT
"""Merge the evidence of one or more native executions into one report.

Usage: python3 -I tools/trial_report.py --title 'Trial 1' --release 0.65 --out TRIAL-1.md EVIDENCE.json...
Counts at the top, then one row per case and check, then every fail/unobserved with its
request evidence (command, output, expected), shortened for reading; the full evidence
stays in the JSON files. A trial is not a run.
"""
import argparse, json, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import aggregate


def short(v, n=300):
    t = v if isinstance(v, str) else json.dumps(v, sort_keys=True, default=str)
    t = t.replace('|', '\\|').replace('\n', ' ')
    return t if len(t) <= n else t[:n] + ' …'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--title', required=True); ap.add_argument('--release', required=True)
    ap.add_argument('--note', default=''); ap.add_argument('--out', required=True)
    ap.add_argument('evidence', nargs='+')
    a = ap.parse_args()
    rows, requests = [], []
    for f in a.evidence:
        d = json.loads(Path(f).read_text())
        rows += d['rows']; requests += d['requests']
    counts = Counter(r['outcome'] for r in rows)
    by_case = defaultdict(list)
    for r in rows:
        by_case[(r['case'], r.get('variant') or '-')].append(r)

    def result(rs):
        # A logic-only case has no summary row: its result follows its rows.
        s = [r['outcome'] for r in rs if r['part'] == 'case-summary']
        if s:
            return s[0]
        o = {r['outcome'] for r in rs}
        return next((k for k in ('fail', 'unobserved', 'undecided') if k in o), 'pass')
    summaries = list(by_case)
    scounts = Counter(result(rs) for rs in by_case.values())
    out = ['# ' + a.title, '', 'Release: %s. %s' % (a.release, a.note), '',
           'Executions (case × variant): %d — %s.' % (len(summaries), ', '.join('%s %d' % (k, scounts[k]) for k in ('pass', 'fail', 'undecided', 'unobserved'))),
           'Check rows: %d — %s.' % (len(rows), ', '.join('%s %d' % (k, counts[k]) for k in ('pass', 'fail', 'undecided', 'unobserved'))),
           'Operational verdict of the rows: %s (not a verdict of the plan).' % aggregate(rows), '',
           '## Executions', '', '| Case | Variant | Result | First reason |', '|---|---|---|---|']
    for (case, var), rs in sorted(by_case.items()):
        res = result(rs)
        first = next((r for r in rs if r['outcome'] != 'pass' and r['part'] != 'case-summary'), None)
        out.append('| %s | %s | %s | %s |' % (case, short(var, 60), res, short(first['detail'], 220) if first else '-'))
    out += ['', '## Every row', '', '| Case | Variant | Check | Part | Outcome | Detail |', '|---|---|---|---|---|---|']
    for r in rows:
        out.append('| %s | %s | %s | %s | %s | %s |' % (r['case'], short(r.get('variant') or '-', 60), r['check'], r['part'],
                                                    r['outcome'], short(r['detail'], 200)))
    Path(a.out).write_text('\n'.join(out) + '\n')
    print('%s: %d executions, rows %s' % (a.out, len(summaries), dict(counts)))


if __name__ == '__main__':
    main()
