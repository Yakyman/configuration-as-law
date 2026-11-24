#!/usr/bin/env python3
"""Index of files whose contents the gaming collector read (metadata-read queries, JSON lines with path/data).
Usage: gread.py --list            -> list path<TAB>outfile
       gread.py PATH [maxbytes]   -> print decoded content (an '@' in PATH stands for '/')."""
import base64, glob, json, os, sys

RAW = '<HOME>/Projects/ideas/cal-paper/night-1123/A3/in/raw/gaming/raw/'


def index():
    idx = {}
    for out in sorted(glob.glob(RAW + '*-metadata-read-*.out')):
        for line in open(out, errors='replace'):
            line = line.strip()
            if not line.startswith('{'):
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            p = d.get('path')
            if p is None:
                p = '?' + os.path.basename(out)
            idx.setdefault(p, []).append((out, d))
    return idx


def decode(d):
    if 'data' in d:
        return base64.b64decode(d['data']).decode('utf-8', 'replace')
    return json.dumps(d)


if __name__ == '__main__':
    idx = index()
    if sys.argv[1] == '--list':
        for p, outs in sorted(idx.items(), key=lambda kv: str(kv[0])):
            print(p, os.path.basename(outs[-1][0]), outs[-1][1].get('status'), sep='\t')
    else:
        p = sys.argv[1].replace('@', '/')
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
        for out, d in idx.get(p, []):
            print('==', os.path.basename(out), d.get('status'))
            print(decode(d)[:n])
