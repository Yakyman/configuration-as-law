#!/usr/bin/python3
"""Repair private observation hook only, retaining isolated source and inputs."""
from pathlib import Path
import ast, subprocess as sp
root=Path(__file__).resolve().parent;work=root/'radio-lifecycle-private';source=work/'source'
tree=ast.parse((root/'radio-lifecycle-private.py').read_text())
inject=next(ast.literal_eval(node.value) for node in tree.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='inject' for t in node.targets))
p=source/'runtime-init';text=p.read_text();start=text.index('# PRIVATE LIFECYCLE TEST ONLY.');end=text.index(') &\n',start)+4
p.write_text(text[:start]+inject+text[end:])
version=(source/'VERSION').read_text().strip()
sp.run(['python3','package-base.py','packages/confos-runtime_'+version+'_all.deb'],cwd=source,check=True)
(work/'disk.qcow2').unlink()
sp.run(['bash','build.sh',str(work/'inputs/declaration.conf'),str(work/'disk.qcow2')],cwd=source,check=True)
