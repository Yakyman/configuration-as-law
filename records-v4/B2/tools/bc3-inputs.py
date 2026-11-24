#!/usr/bin/env python3
"""Fetch two fixed additional binary recipe inputs on the build host."""
import hashlib,json,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parent.parent
cache=ROOT/'downloads/packages'
manifest=ROOT/'downloads/packages.sha256'
items=[
 ('libfuse2t64_2.9.9-9_amd64.deb','https://deb.debian.org/debian/pool/main/f/fuse/libfuse2t64_2.9.9-9_amd64.deb','e60474070e983693ac461af291b876c2304340f75a6b8379a3ba017e4848341e'),
 ('python3-fusepy_3.0.1-5_all.deb','https://deb.debian.org/debian/pool/main/p/python-fusepy/python3-fusepy_3.0.1-5_all.deb','f5bc8f25146b4285d662ad4c53aa822bc3a03a6119a78682a2eb85cc6bd6ead1')]
if not manifest.is_file():raise SystemExit('complete inherited cache manifest required')
expected={line.split()[1]:line.split()[0] for line in manifest.read_text().splitlines()}
for name,url,digest in items:
    path=cache/name
    if not path.exists():
        data=urllib.request.urlopen(url,timeout=60).read()
        if hashlib.sha256(data).hexdigest()!=digest:raise RuntimeError('download identity mismatch')
        path.write_bytes(data)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise RuntimeError('cached identity mismatch')
    if name in expected and expected[name]!=digest:raise RuntimeError('manifest conflict')
    expected[name]=digest
manifest.write_text(''.join(expected[name]+'  '+name+'\n' for name in sorted(expected)))
print(json.dumps({'fixed_inputs':[{'name':n,'url':u,'sha256':h} for n,u,h in items]}))
