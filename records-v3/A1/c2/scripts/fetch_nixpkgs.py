"""Fetch NixOS module sources (public documentation of the program) into A1/c2/raw/nixpkgs/."""
import os
import sys
import urllib.request

BASE = "https://raw.githubusercontent.com/NixOS/nixpkgs/master/"
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for f in sys.argv[2:]:
    dst = os.path.join(out, f.replace("/", "_"))
    if os.path.exists(dst):
        continue
    try:
        data = urllib.request.urlopen(BASE + f, timeout=30).read()
        with open(dst, "wb") as fh:
            fh.write(data)
        print("ok", f, len(data))
    except Exception as e:  # noqa: BLE001
        print("fail", f, e)
