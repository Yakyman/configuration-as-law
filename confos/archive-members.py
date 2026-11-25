#!/usr/bin/python3
"""Expand archive-members.txt to the files of the source archive of a release.

Usage: archive-members.py VERSION [--lines]
Each line of archive-members.txt is a path or a shell pattern relative to the source folder;
`@VERSION@` stands for the release. A folder stands for every file below it. A line that
matches nothing is an error. Output: the file paths, sorted, separated by NUL (or by line
feeds with --lines).
"""
import glob
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
version = sys.argv[1]
files = set()
for number, line in enumerate((here/'archive-members.txt').read_text().splitlines(), 1):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    pattern = line.replace('@VERSION@', version)
    matches = sorted(glob.glob(pattern, root_dir=here))
    if not matches:
        raise SystemExit(f'archive-members.txt line {number}: nothing matches {pattern}')
    for match in matches:
        path = here/match
        if path.is_dir() and not path.is_symlink():
            found = [p for p in path.rglob('*') if p.is_file() or p.is_symlink()]
            if not found:
                raise SystemExit(f'archive-members.txt line {number}: empty folder {match}')
            files.update(p.relative_to(here).as_posix() for p in found)
        else:
            files.add(match)
separator = '\n' if '--lines' in sys.argv else '\0'
sys.stdout.write(''.join(name+separator for name in sorted(files)))
