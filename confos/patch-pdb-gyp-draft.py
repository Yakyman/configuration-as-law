#!/usr/bin/python3
"""Guarded pure-source draft. Writes only a new output directory, never packages."""
import ast
import hashlib
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
EXPECTED={
    'pdb.py':'8c200bf9066bb6baeac7bdb174db4d3a354ed0bff8c947b022e72566084cdb70',
    'gyp-input.py':'524dbc9400ef166fa74919c4872ba73d35f64ccebce13fae1b97f3b0576251da',
}

def patch(inputs, output):
    originals={name:(inputs/name).read_bytes() for name in EXPECTED}
    for name,data in originals.items():
        assert hashlib.sha256(data).hexdigest()==EXPECTED[name],('unexpected source',name)
    prepared={name:data.decode() for name,data in originals.items()}
    def replace(name,old,new):
        assert prepared[name].count(old)==1,(name,old)
        prepared[name]=prepared[name].replace(old,new)
    replace('pdb.py','import io\n','import io\nimport _io\n')
    for path in ("os.path.expanduser('~/.pdbrc')",'".pdbrc"'):
        old='''                with open(PATH, encoding='utf-8') as rcFile:
                    self.rcLines.extend(rcFile)
            except OSError:
                pass'''.replace('PATH',path)
        new='''                with _io.open_code(PATH) as raw:
                    with io.TextIOWrapper(raw, encoding='utf-8') as rcFile:
                        self.rcLines.extend(rcFile)
            except FileNotFoundError:
                pass'''.replace('PATH',path)
        replace('pdb.py',old,new)
    replace('gyp-input.py','import ast\n','import ast\nimport _io\nimport io\n')
    replace('gyp-input.py','        build_file_contents = open(build_file_path, encoding="utf-8").read()',
        '        with _io.open_code(build_file_path) as raw:\n'
        '            with io.TextIOWrapper(raw, encoding="utf-8") as build_file:\n'
        '                build_file_contents = build_file.read()')
    for name,text in prepared.items():ast.parse(text,filename=name)
    output.mkdir() # Refuse reuse; do not overwrite a previous experiment.
    for name,text in prepared.items():(output/name).write_text(text)
    lines=[]
    for name in sorted(prepared):
        lines.append(hashlib.sha256((output/name).read_bytes()).hexdigest()+'  '+name)
    (output/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
    print('PDB GYP SOURCE PATCH GENERATED; NO NATIVE EXECUTION TEST',flush=True)
    print('\n'.join(lines),flush=True)

if __name__=='__main__':
    assert len(sys.argv)==3,'usage: patch-pdb-gyp-draft.py INPUT_DIRECTORY NEW_OUTPUT_DIRECTORY'
    patch(Path(sys.argv[1]),Path(sys.argv[2]))
