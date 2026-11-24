import json, subprocess, sys
from pathlib import Path
base = Path('S5/raw/cases')
for n in range(1, 18):
    out = subprocess.run([sys.executable, '-I', 'S5/tools/analyse_case.py', str(base), f'{n:02d}', 'B2/build/bc3-fixtures.json'], capture_output=True, text=True)
    if out.returncode: print('FAIL', n, out.stderr); continue
    (base / f'{n:02d}-analysis.json').write_text(out.stdout)
for n in range(1, 18):
    d = json.load(open(base / f'{n:02d}-analysis.json'))
    print(f"== {n:02d} problems={d['problems']} stderr_file={(base / f'{n:02d}.stderr').read_text()!r} exit={(base / f'{n:02d}.exit').read_text().strip()}")
    for s in d['steps']:
        if 'role' not in s:
            print('  ', {k: v for k, v in s.items() if v is not None}); continue
        diff = s['diff']; fsd = {k: v for k, v in diff.items() if k != 'primary'}
        print('  ', s['role'], 'rc', s['rc'], 'out', repr(s['stdout'])[:200], 'err', repr(s['stderr'])[:200])
        print('     flags', {k: v for k, v in s['controller_flags'].items() if v is not None})
        print('     primary unchanged', diff['primary']['unchanged'], '+', diff['primary']['rows_added'], '-', diff['primary']['rows_removed'])
        for k, v in fsd.items():
            print('     fs', k, 'gen', v['generation'], 'added', [(a['path'], (a['sha256'] or '')[:12], a['mode']) for a in v['added']], 'removed', v['removed'], 'changed', [(c['path'], (c['sha256_before'] or '')[:8], (c['sha256_after'] or '')[:8]) for c in v['changed']], 'unlinked', v['unlinked_objects_after'])
        print('     audit', [(a['fs'], a['generation'], a['operation'], [(c[0], c[1]) for c in a['changes']]) for a in s['audit']][:14])
        if 'coverage_before' in s:
            print('     cov before', {p: c['covered'] for p, c in s['coverage_before'].items()}, 'after', {p: (c['covered'], c.get('generation')) for p, c in s['coverage_after'].items()})
        if 'account_rows' in s:
            print('     account', s['account'], 'rows', s['account_rows'], 'parse_err', s['etc_parse_error'])
