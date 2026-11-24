#!/usr/bin/python3
"""Apply Debian's own __post_configure module selection to the private build."""
from pathlib import Path
import re,shutil,subprocess as sp
work=Path('interpreter-inputs/libpython-private');root=work/'source'
assert (root/'Modules/Setup.local').read_text()=='# Edit this file for local setup changes\n'
shutil.copyfile(work/'candidate.so',work/'candidate-first.so')
names={r.split()[0] for r in (root/'debian/PVER-minimal.README.Debian.in').read_text().splitlines() if len(r.split())>=2 and r.split()[1]=='extension'}
pattern=re.compile('^#('+'|'.join(re.escape(name) for name in sorted(names))+'|XX)')
# Match Debian's prefix expression exactly: _stat also selects _statistics.
lines=[line[1:].replace('-Wl,-Bdynamic','').replace('-Wl,-Bstatic','') for line in (root/'Modules/Setup').read_text().splitlines() if pattern.search(line)]
assert len(lines)>=29
(root/'Modules/Setup.local').write_text('\n'.join(lines)+'\n')
shutil.copyfile(root/'Modules/Setup.local',work/'Setup.local')
sp.run(['make','Makefile','Modules/config.c'],cwd=root,check=True)
p=root/'Makefile';text=p.read_text();text='\n'.join(line for line in text.splitlines() if not (line.startswith('Modules/_math.o: ') and 'PY_STDMODULE_CFLAGS' in line))+'\n';p.write_text(text)
print('DEBIAN PRIVATE BUILTIN SELECTION',len(lines))
