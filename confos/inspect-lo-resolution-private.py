#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
root=Path.cwd();apt=root/'images/confos-0.47-clean.work/apt'
opts=['-o','Dir::State::lists='+str(apt/'lists'),'-o','Dir::Etc::sourcelist='+str(apt/'etc/sources.list'),'-o','Dir::Etc::sourceparts=-','-o','Dir::Cache::pkgcache=','-o','Dir::Cache::srcpkgcache=']
for package in ('libreoffice-writer','libreoffice-base-core','libreoffice-core','libreoffice-common','libuno-cppu3','ure'):
 output=sp.check_output(['apt-cache',*opts,'show',package],text=True)
 print('\n'.join(line for line in output.splitlines() if line.startswith(('Package:','Version:','Depends:','Breaks:','Conflicts:'))))
