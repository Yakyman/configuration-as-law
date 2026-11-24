#!/usr/bin/python3
"""Read-only ABI evidence; does not rebuild or alter candidate bytes."""
import json,subprocess as sp
from pathlib import Path
work=Path('interpreter-inputs/ed-reader-draft')
report=json.loads((work/'comparison.json').read_text())
for label,path in [('original',work/'original/usr/bin/ed'),('candidate',work/'candidate/ed')]:
    symbols=sp.check_output(['readelf','--dyn-syms','--wide',str(path)],text=True)
    report[label]['exports']=sorted(line.split()[7] for line in symbols.splitlines() if len(line.split())>=8 and line.split()[4] in ('GLOBAL','WEAK') and line.split()[6]!='UND')
    (work/(label+'-symbols.txt')).write_text(symbols)
assert report['original']['exports']==report['candidate']['exports']
(work/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
print('ED_READER_EXACT_EXPORTED_SYMBOL_NAMES_PASS',report['candidate']['exports'])
