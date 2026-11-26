#!/usr/bin/env python3
"""Semantic test declarations; release bindings are frozen separately before a run."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def save(name,lines):
    (ROOT/'declarations'/name).write_text(json.dumps({'schema':1,'lines':lines},indent=2)+'\n')
def binding(lid,name): return {'id':lid,'kind':'binding','name':name}
base=[binding('base','base-source-lock'),binding('login','test-account-and-login'),binding('probe','case-probe-package'),
      binding('small','case-small-v1-package'),binding('service','test-service'),binding('access','test-access-rule'),
      binding('host','test-hostname'),binding('timezone','test-timezone'),
      {'id':'script','kind':'file','path':'@HOME@/bin/cases-report.sh','text':(ROOT/'payloads/cases-report.sh').read_text(),
       'mode':'0755','uid':1000,'gid':1000}]
save('D-test.json',base)
save('D-open.json',base+[{'id':'opening','kind':'open-folder','path':'@HOME@/opened','scope':'execute'}])
for name in ('D-accounts-fixed','D-accounts-open','D-latest','D-shared','D-radio','D-external-accounts'):
    save(name+'.json',base+[binding(name,name+'-native-lines')])
for i in range(3): save('D-T'+str(i)+'.json',[binding('base','system-update-state-T'+str(i))]+base[1:])
files=sorted(p for p in (ROOT/'payloads').iterdir() if p.is_file())
lock={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(ROOT/'declarations/payloads.lock.json').write_text(json.dumps(lock,indent=2)+'\n')
print('11 semantic declarations and payload hash lock written')
