#!/usr/bin/python3 -B
"""Wait for the expected FUSE mount, never report an underlying tree ready."""
import pathlib,sys,time
target=sys.argv[1]
for _ in range(1200):
    for line in pathlib.Path('/proc/self/mountinfo').read_text().splitlines():
        pre,post=line.split(' - ',1)
        if pre.split()[4]==target and post.split()[0].startswith('fuse'):
            raise SystemExit(0)
    time.sleep(.1)
raise SystemExit('declaration filesystem did not mount')
