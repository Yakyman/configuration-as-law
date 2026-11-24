#!/usr/bin/python3
import gzip,hashlib,json,os,tempfile
from pathlib import Path
import flatpak_readers as readers
h=lambda x:hashlib.sha256(x).hexdigest()
with tempfile.TemporaryDirectory() as name:
 root=Path(name)
 store=root/'usr/lib/confos/flatpak'
 ref='runtime/org.example.Runtime/x86_64/stable'; commit='a'*64; bundle='b'*64
 old=b'original'; new=b'guarded'
 obj='repo/objects/ab/'+'c'*62+'.file'
 target=store/ref/commit/'files/bin/bash'; target.parent.mkdir(parents=True)
 target.write_bytes(old); target.chmod(0o755)
 original=store/obj; original.parent.mkdir(parents=True); os.link(target,original)
 directory=root/Path(readers.MANIFEST).parent; directory.mkdir(parents=True,exist_ok=True)
 payload=directory/'bash.gz'; payload.write_bytes(gzip.compress(new))
 manifest=[dict(ref=ref,commit=commit,bundle_sha256=bundle,target='bin/bash',original_sha256=h(old),objects=[obj],payload='bash.gz',sha256=h(new),mode=0o755)]
 (root/readers.MANIFEST).write_text(json.dumps(manifest))
 def refused(label,fn):
  try: fn()
  except ValueError: print(label,'REFUSED')
  else: raise AssertionError(label)
  assert target.read_bytes()==old and os.path.samefile(target,original)
 target.write_bytes(b'other original')
 try: readers.apply(root,store,ref,commit,'f'*64)
 except ValueError: print('wrong original object REFUSED')
 else: raise AssertionError('wrong original object')
 assert target.read_bytes()==b'other original' and os.path.samefile(target,original)
 target.write_bytes(old)
 payload.write_bytes(gzip.compress(b'wrong'))
 refused('wrong payload',lambda:readers.apply(root,store,ref,commit,bundle))
 payload.write_bytes(gzip.compress(new))
 before=original.stat().st_ino
 # Another export of the same commit (another bundle checksum) is accepted from 0.49.
 paths=readers.apply(root,store,ref,commit,'f'*64)
 assert original.stat().st_ino==before and original.read_bytes()==old
 assert target.read_bytes()==new and not os.path.samefile(target,original)
 assert target.stat().st_mode&0o777==0o755
 assert len(paths)==2 and all(obj in x for x in paths)
 assert readers.policy(root).count(' mx,')==2
 target.write_bytes(b'tampered')
 try: readers.denial_paths(root)
 except ValueError: print('tampered replacement REFUSED')
 else: raise AssertionError('tampering accepted')
 print('ATOMIC NEW-INODE REPLACEMENT AND EXACT ALIAS POLICY PASS')

