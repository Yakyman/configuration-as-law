#!/usr/bin/env python3
"""Compare collected categories exactly; raw files are never changed."""
import argparse
import difflib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('first_directory')
parser.add_argument('second_directory')
args = parser.parse_args()
left_path = Path(args.first_directory) / 'inventory.json'
right_path = Path(args.second_directory) / 'inventory.json'
left = json.loads(left_path.read_text())
right = json.loads(right_path.read_text())
for category in sorted(left.keys() | right.keys()):
    if category in left and category in right and left[category] == right[category]:
        print(f'{category}: IDENTICAL')
        continue
    print(f'{category}: DIFFERENT')
    a = json.dumps(left.get(category, '<missing category>'), indent=2, sort_keys=True).splitlines(keepends=True)
    b = json.dumps(right.get(category, '<missing category>'), indent=2, sort_keys=True).splitlines(keepends=True)
    print(''.join(difflib.unified_diff(a, b, fromfile=f'{left_path}:{category}', tofile=f'{right_path}:{category}')))
print('Raw inventories preserved in each input directory. Differences require review; no outcome assigned.')
