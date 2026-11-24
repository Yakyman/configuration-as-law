#!/usr/bin/python3 -I
"""Document editor with an integrated exact-artifact package installer.

v4-editor read FILE
v4-editor write FILE       (document bytes on standard input)
v4-editor append FILE      (document bytes on standard input)
v4-editor package-install ROW.json
v4-editor package-remove LINE_ID

Document operations run with the caller's identity. Installation delegates to
stand-pkg, whose broker validates exact package bytes and applies a declaration.
"""
import pathlib
import subprocess
import sys

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 64
    operation, target = sys.argv[1:]
    if operation in ('package-install', 'package-remove'):
        return subprocess.run(['/usr/local/bin/stand-pkg',
                               'install' if operation == 'package-install' else 'remove', target]).returncode
    path = pathlib.Path(target)
    if operation == 'read':
        sys.stdout.buffer.write(path.read_bytes())
    elif operation in ('write', 'append'):
        with path.open('wb' if operation == 'write' else 'ab') as output:
            while chunk := sys.stdin.buffer.read(65536):
                output.write(chunk)
    else:
        raise ValueError('unknown document operation')
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print('FAILED ' + str(error), file=sys.stderr)
        sys.exit(1)
