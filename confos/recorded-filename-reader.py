#!/usr/bin/python3
"""Recorded interpreter diagnostic: execute the saved program named by argv[1]."""
import sys
from pathlib import Path
code=Path(sys.argv[1]).read_bytes()
exec(compile(code,sys.argv[1],'exec'))
