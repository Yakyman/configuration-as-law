#!/usr/bin/python3
"""Read-only native solver comparison for an older exact Writer request."""
import json,re,subprocess as sp
from pathlib import Path
root=Path.cwd();apt=root/'images/confos-0.47-clean.work/apt'
opts=['-o','Dir::State::status=/dev/null','-o','Dir::State::lists='+str(apt/'lists'),'-o','Dir::Etc::sourcelist='+str(apt/'etc/sources.list'),'-o','Dir::Etc::sourceparts=-','-o','Dir::Cache::pkgcache=','-o','Dir::Cache::srcpkgcache=','-o','Dir::Etc::parts=-','-o','Dir::Etc::main=-','-o','APT::Install-Recommends=false','-o','APT::Install-Suggests=false']
requests=dict(line.split('=',1) for line in Path('components/20261123T000000Z.txt').read_text().splitlines() if not line.startswith('confos-'))
requests['libreoffice-writer']='4:25.2.3-2+deb13u9'
arguments=[name+'='+version for name,version in sorted(requests.items())]
out=Path('records/lo-solver-private');out.mkdir(exist_ok=True)
for label,flags in [('default',[]),('solver3',['--solver','3.0']),('solver3-all-versions',['--solver','3.0','--no-strict-pinning'])]:
 command=['apt-get',*opts,*flags,'--simulate','install',*arguments]
 r=sp.run(command,capture_output=True,text=True,timeout=45)
 (out/(label+'.log')).write_text(('COMMAND '+repr(command)+'\nEXIT '+str(r.returncode)+'\n'+r.stdout+r.stderr).replace(str(root),'REMOTE_BUILD'))
 selected=dict((n.split(':')[0],v) for n,v in re.findall(r'^Inst (\S+) \((\S+) ',r.stdout,re.M))
 violations={n:[v,selected.get(n)] for n,v in requests.items() if selected.get(n)!=v}
 print(label,'EXIT',r.returncode,'SELECTED',len(selected),'EXPLICIT_REQUEST_VIOLATIONS',violations,flush=True)
 if r.returncode==0:assert not violations
