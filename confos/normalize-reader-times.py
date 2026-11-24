#!/usr/bin/python3
"""Keep shipped generated build files usable without unpinned generator tools."""
from pathlib import Path
import os
import sys
for root in map(Path, sys.argv[1:]):
    for path in root.rglob('*'):
        os.utime(path, (1795392000, 1795392000), follow_symlinks=False)
