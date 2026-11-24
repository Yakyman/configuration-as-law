#!/usr/bin/python3
from pathlib import Path
def remap(text):
 for old,new in [('0.45','@NEW@'),('0.44','@OLD@'),('0.43','@DROP@')]:text=text.replace(old,new)
 return text.replace('@NEW@','0.46').replace('@OLD@','0.45').replace('@DROP@','0.44').replace('radio-recording','libpython').replace('radio-045','libpython-046').replace('045','046')
for old,new in [('fetch-radio-recording-045.sh','fetch-libpython-046.sh'),('cleanup-radio-recording-045.sh','cleanup-libpython-046.sh')]:
 text=remap(Path(old).read_text())
 if new.startswith('cleanup'):
  text='\n'.join('cp libpython-046-fixture/inputs/declaration.conf records/libpython-046/' if line.startswith('cp libpython-046-fixture/boot-') else line for line in text.splitlines())+'\n'
  text=text.replace('mkdir -p records/libpython-046','mkdir -p records/libpython-046')
 Path(new).write_text(text)
print('46 FETCH/CLEANUP PLUMBING PREPARED')
