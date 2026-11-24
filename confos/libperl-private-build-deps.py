#!/usr/bin/python3
"""Extract pinned build dependencies without installing anything on the host."""
import hashlib,json,shutil,subprocess as sp
from pathlib import Path
root=Path.cwd();work=root/'interpreter-inputs/libperl-private';downloads=work/'debs';deps=work/'dependencies'
downloads.mkdir();deps.mkdir()
apt=root/'images/confos-0.46-clean.work/apt'
opts=['-o','Dir::State::lists='+str(apt/'lists'),'-o','Dir::Etc::sourcelist='+str(apt/'etc/sources.list'),'-o','Dir::Etc::sourceparts=-','-o','APT::Sandbox::User=root','-o','Acquire::Check-Valid-Until=false']
packages=['libdb5.3-dev=5.3.28+dfsg2-9','libdb5.3t64=5.3.28+dfsg2-9','libgdbm-dev=1.24-2','libgdbm-compat-dev=1.24-2','libgdbm6t64=1.24-2','libgdbm-compat4t64=1.24-2']
sp.run(['apt-get',*opts,'download',*packages],cwd=downloads,check=True)
for p in downloads.glob('*.deb'):sp.run(['dpkg-deb','-x',str(p),str(deps)],check=True)
(work/'build-dependencies.json').write_text(json.dumps({'requests':packages,'archives':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in downloads.glob('*.deb')}},indent=2)+'\n')
shutil.rmtree(work/'source/build-shared')
print('PRIVATE PERL BUILD DEPENDENCIES EXTRACTED')
