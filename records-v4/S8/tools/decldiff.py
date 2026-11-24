#!/usr/bin/env python3
"""Offline difference of the declarations held in two step-8 observation JSON files (S8 reading aid)."""
import json
import sys


def load(path):
    o = json.load(open(path))
    files = o['complete_declaration']['files'] if 'complete_declaration' in o else o['files']
    rows = {}
    for line in files['/var/lib/stand/current/machine.jsonl'].splitlines():
        if line.strip():
            r = json.loads(line)
            rows[r['id']] = r
    for r in list(rows.values()):
        if 'files_manifest' in r:
            r = dict(r)
            r['files'] = json.loads(files['/var/lib/stand/current/' + r.pop('files_manifest')])
            r.pop('manifest_sha256', None)
            rows[r['id']] = r
    fs = {}
    for k, v in files.items():
        if k.startswith('/var/lib/stand-fs/'):
            j = json.loads(v)
            key = k.split('/')[4]
            for p, ino in j['paths'].items():
                fs[key + ':' + p] = j['objects'][ino]
            for a in j.get('account_rows', []):
                fs[key + ':account:' + a['id']] = a
    return rows, fs


def main():
    a_rows, a_fs = load(sys.argv[1])
    b_rows, b_fs = load(sys.argv[2])
    out = {'machine_added': sorted(set(b_rows) - set(a_rows)),
           'machine_removed': sorted(set(a_rows) - set(b_rows)),
           'machine_changed': {k: sorted(f for f in set(a_rows[k]) | set(b_rows[k]) if a_rows[k].get(f) != b_rows[k].get(f))
                               for k in set(a_rows) & set(b_rows) if a_rows[k] != b_rows[k]},
           'fs_added': {k: {f: v for f, v in b_fs[k].items() if f in ('sha256', 'st_mode', 'st_uid', 'st_size', 'target')}
                        for k in sorted(set(b_fs) - set(a_fs))},
           'fs_removed': sorted(set(a_fs) - set(b_fs)),
           'fs_changed': {k: sorted(f for f in set(a_fs[k]) | set(b_fs[k]) if a_fs[k].get(f) != b_fs[k].get(f))
                          for k in sorted(set(a_fs) & set(b_fs)) if a_fs[k] != b_fs[k]}}
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == '__main__':
    main()
