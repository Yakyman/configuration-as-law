#!/usr/bin/python3
"""Apply once after guarded40 advance, before building any runtime package."""
from pathlib import Path
assert Path('VERSION').read_text().strip() == '0.40'
prepared = {}
def edit(name, old, new):
    text = prepared.get(name, Path(name).read_text())
    assert text.count(old) == 1, (name, old)
    prepared[name] = text.replace(old, new)
edit('package-base.py', 'RUNTIME = (', "RUNTIME = ('radio_inspect.py', ")
edit('confos', '\ntry:\n', '''
def radio_inspect():
    sys.path.insert(0, '/usr/lib/confos')
    import radio_inspect as native
    native.inspect(sys.argv[2:])

try:
''')
edit('confos', "{'status': status, 'apply': apply,", "{'radio-inspect': radio_inspect, 'status': status, 'apply': apply,")
edit('archive-source.sh', '    assemble.py ',
     '    radio_inspect.py wire-radio-inspection-040.py probe-radio-inspection.py document-radio-040.py \\\n    assemble.py ')
for name, text in prepared.items(): Path(name).write_text(text)
print('RADIO40 FIXED NATIVE INSPECTION WIRED; runtime rebuild required')
