#!/usr/bin/python3
"""Give upstream Configure the extracted library search paths explicitly."""
from pathlib import Path
import shutil
work=Path('interpreter-inputs/libperl-private').resolve()
p=work/'source/debian/config.debian'
text=p.read_text()
anchor='    -Dmksymlinks'
assert text.count(anchor)==1
paths=f"    -Dloclibpth='{work}/dependencies/usr/lib/x86_64-linux-gnu' \\\n    -Dlocincpth='{work}/dependencies/usr/include' \\\n"
p.write_text(text.replace(anchor,paths+anchor))
shutil.rmtree(work/'source/build-shared')
print('EXTRACTED DEPENDENCY PATHS ADDED TO CONFIGURE SEARCH')
