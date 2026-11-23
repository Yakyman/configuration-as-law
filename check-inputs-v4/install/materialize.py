#!/usr/bin/env python3
"""Reconstruct exact installation inputs with the separately retained lab public key."""
import argparse,pathlib,re
ap=argparse.ArgumentParser();ap.add_argument('lab_root',type=pathlib.Path);ap.add_argument('public_key',type=pathlib.Path);ap.add_argument('--previous-lab-root',type=pathlib.Path);args=ap.parse_args()
if not args.lab_root.is_absolute():raise SystemExit('LAB_ROOT must be absolute')
previous=args.previous_lab_root or args.lab_root.parent/'previous-lab'
if not previous.is_absolute():raise SystemExit('Previous lab root must be absolute')
if not all(re.fullmatch(r'/[A-Za-z0-9_./-]+',str(p)) for p in (args.lab_root,previous)):raise SystemExit('Use simple absolute laboratory paths')
key=args.public_key.read_text().strip()
if not re.fullmatch(r'ssh-ed25519 [A-Za-z0-9+/=]+(?: [^\n]+)?',key):raise SystemExit('Expected an Ed25519 laboratory public key')
source=pathlib.Path(__file__).resolve().parent/'recipes'
for p in source.rglob('*.in'):
 rel=p.relative_to(source);dest=args.lab_root/'install'/str(rel)[:-3]
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(p.read_text().replace('@LAB_PUBLIC_KEY@',key).replace('@LITERAL_LAB_PUBLIC_KEY@','@LAB_PUBLIC_KEY@').replace('@LAB_ROOT@',str(args.lab_root)).replace('@PREVIOUS_LAB_ROOT@',str(previous)))
 if dest.suffix in ('.sh','.py') or dest.name in ('dialog','combustion'):dest.chmod(0o755)
for dest in (args.lab_root/'install/access-key.pub',args.lab_root/'keys/lab.pub'):
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(key+'\n')
