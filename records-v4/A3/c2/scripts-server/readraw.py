import os as _os; NIGHT_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../..")) + "/"  # night folder
"""Print decoded contents that the collector read for a path (or paths matching 'grep:REGEX'), with the raw file name.
Optional last arg 'list' only lists matching paths."""
import base64
import glob
import json
import os
import re
import sys

RAW = NIGHT_DIR + "A3/in/raw/server/raw/"
args = sys.argv[1:]
only_list = args and args[-1] == 'list'
if only_list:
    args = args[:-1]
for f in sorted(glob.glob(RAW + "*metadata-read*.out")):
    for line in open(f, errors='replace'):
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            j = json.loads(line)
        except Exception:
            continue
        p = j.get('path', '')
        ok = False
        for a in args:
            if a.startswith('grep:'):
                if re.search(a[5:], p):
                    ok = True
            elif p == a:
                ok = True
        if not ok:
            continue
        print('==', p, os.path.basename(f), j.get('status'), j.get('error', ''))
        if not only_list and 'data' in j:
            print(base64.b64decode(j['data']).decode('utf-8', 'replace'))
