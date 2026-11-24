#!/usr/bin/python3
"""Derive standard release plumbing, preserving the previous release scripts."""
from pathlib import Path
def remap(text):
 for old,new in [('0.43','@NEW@'),('0.42','@OLD@'),('0.41','@DROP@')]:text=text.replace(old,new)
 return text.replace('@NEW@','0.44').replace('@OLD@','0.43').replace('@DROP@','0.42').replace('nft-ed','tools').replace('043','044')
for source,target in [('archive-nft-ed-043.sh','archive-tools-044.sh'),
                      ('cleanup-nft-ed-043.sh','cleanup-tools-044.sh'),
                      ('fetch-nft-ed-evidence-043.sh','fetch-tools-evidence-044.sh')]:
 text=remap(Path(source).read_text())
 text=text.replace('CANDIDATE43 NFT ED AND REGRESSIONS PASS','CANDIDATE44 VISUDO SSH AND REGRESSIONS PASS')
 text=text.replace('CANONICAL43 NFT RECORDING NINE CUTS AND ED READERS PASS','CANONICAL44 VISUDO NINE CUTS AND SSH READERS PASS')
 text=text.replace('prepare-tools-component-044.py','prepare-ssh-component-044.py')
 text=text.replace('tools-044-fixture/declaration.conf','tools-044-fixture/inputs/declaration.conf')
 if target=='archive-tools-044.sh':
  text=text.replace("grep -qx 'UPDATES PASS' logs/updates-0.44.log\n",
                    "grep -qx 'UPDATES PASS' logs/updates-0.44.log\ngrep -qx 'CANONICAL44 RECORDED VISUDO EDITOR PASS' logs/visudo-editor-0.44.log\n")
  text=text.replace(' logs/readers-0.43.log logs/mpv-0.42.log logs/radio-0.40.log',
                    ' logs/nft-ed-0.43.log logs/readers-0.42.log logs/mpv-0.41.log')
  text=text.replace("'tools-archive-paths-044.py'","'tools-archive-paths-044.py','ssh-archive-paths-044.py'")
 if target=='cleanup-tools-044.sh':
  text=text.replace('images/tools-044.work experiments/', 'images/tools-044.work tools-044-fixture experiments/')
 if target=='fetch-tools-evidence-044.sh':
  text=text.replace('inventory-0.44 underived-0.44;do','inventory-0.44 underived-0.44 visudo-editor-0.44;do')
 Path(target).write_text(text)
print('44 RELEASE PLUMBING PREPARED')
