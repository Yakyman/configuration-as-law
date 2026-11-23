import sys,json,pathlib
sys.path.insert(0,'/usr/local/lib/stand')
import stand,codeboundary
p=pathlib.Path('/var/lib/stand/pending.json');d=pathlib.Path('/var/lib/stand/generations')/json.loads(p.read_text())['candidate']
print(json.dumps(codeboundary.verify_policy(stand.load(d),d)))
