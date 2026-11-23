#!/usr/bin/env python3
"""Run the exact two-case delta used for final shell-sync validation."""
from pathlib import Path
p=Path(__file__).with_name('serial-fixture.py')
s=p.read_text().replace("4 if kind=='normal'", "2 if kind=='normal'").replace("for kind in ('normal','bad-wrapper','bad-payload','bad-ack','bad-stty'):", "for kind in ('normal','bad-sync'):")
exec(compile(s,str(p.resolve()),'exec'),{'__file__':str(p.resolve())})
