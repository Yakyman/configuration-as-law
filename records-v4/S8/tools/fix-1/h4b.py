import json, sys, lzma, re, hashlib
g = json.load(lzma.open(sys.argv[1]))
do = g['disconnected_observation']
for k in ('identity_before','identity_at_comparison','identity_after'):
    v = do[k]
    print('\n==', k, list(v.keys()) if isinstance(v, dict) else type(v))
    for kk, vv in v.items():
        if isinstance(vv, dict):
            for a, b in vv.items():
                if 'etc' in a or 'pending' in a or 'stand-ready' in a or 'last-success' in a:
                    s = b if isinstance(b, str) else json.dumps(b)
                    print('  ', kk, a, '->', (s[:200] if len(s) < 400 else 'sha256(len %d)=%s' % (len(s), hashlib.sha256(s.encode()).hexdigest()[:12])))
        else:
            print('  ', kk, str(vv)[:200])
raw = json.dumps(g)
print('\ndev-worker contexts:')
for m in re.finditer(r'.{100}dev-worker.{100}', raw):
    print('  ..', m.group(0).replace('\\n',' ')[:220])
print('exit', g['exit'], 'stdout', g['stdout'][-400:], 'stderr', g['stderr'][-300:])
print('times', {k: g[k] for k in ('started_utc','ready_utc','cut_seen_utc','finished_utc','output_utc','observation_finished_utc')})
