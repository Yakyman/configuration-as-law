#!/usr/bin/env python3
"""Prepare credential-free recipe templates; no guest state is read."""
import argparse,hashlib,pathlib,re,shutil
parser=argparse.ArgumentParser()
parser.add_argument('--source-home-relative',required=True)
parser.add_argument('--previous-lab-name',required=True)
args=parser.parse_args()
source_relative=args.source_home_relative
previous_name=args.previous_lab_name
if not re.fullmatch(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*',source_relative) or '..' in source_relative.split('/') or not re.fullmatch(r'[A-Za-z0-9_-]+',previous_name):
 raise SystemExit('Source locations must be simple relative components')
c=pathlib.Path(__file__).resolve().parents[1]
recipes=c/'install/recipes'
# This directory contains only this builder's generated templates.
if recipes.exists():shutil.rmtree(recipes)
recipes.mkdir()
excluded={'access-key.pub','talosconfig','controlplane.yaml','release-key.gpg'}
rows=[]
expected_key=(c/'install/access-key.pub').read_text().strip()
if not re.fullmatch(r'ssh-ed25519 [A-Za-z0-9+/=]+(?: lab-access)?',expected_key):raise SystemExit('Unexpected laboratory public-key format')
for p in sorted((c/'install').rglob('*')):
 if not p.is_file() or recipes in p.parents or p.suffix=='.pyc':continue
 rel=p.relative_to(c/'install')
 if p.name in excluded or p.name.startswith('status') or p.name in ('materialize.py',):continue
 if p.suffix not in ('.sh','.py','.md','.nix','.scm','.xml','.cfg','.template','.patch','.json') and p.name not in ('dialog','combustion'):continue
 raw=p.read_bytes()
 try:text=raw.decode()
 except UnicodeDecodeError:continue
 # Preserve markers that are literal data in reusable source templates/drivers.
 text=text.replace('@LAB_PUBLIC_KEY@','@LITERAL_LAB_PUBLIC_KEY@')
 if re.search(r'BEGIN (?:OPENSSH|RSA|EC|PRIVATE).*PRIVATE KEY|client-key-data:',text):raise SystemExit('Credential-bearing input outside exclusions: '+str(rel))
 # Replace only generated SSH public keys; do not publish their material.
 for match in re.findall(r'ssh-ed25519 [A-Za-z0-9+/=]+(?: lab-access)?',text):
  if match.split()[:2]!=expected_key.split()[:2]:raise SystemExit('Unrecognized public key in recipe: '+str(rel))
 text=re.sub(r'ssh-ed25519 [A-Za-z0-9+/=]+(?: lab-access)?','@LAB_PUBLIC_KEY@',text)
 if re.search(r'-----BEGIN [A-Z ]*(?:PRIVATE KEY|PUBLIC KEY|CERTIFICATE)-----|(?:ssh-(?:rsa|dss|ed25519)|ecdsa-sha2-[^ ]+) [A-Za-z0-9+/=]{20,}|(?:client-key-data|client-certificate-data|private_key|private-key)\s*:\s*[A-Za-z0-9+/=]{20,}',text,re.I):
  raise SystemExit('Credential-bearing recipe rejected: '+str(rel))
 if re.search(r'/home/(?!user/|linuxbrew/|calops/)[a-zA-Z][a-zA-Z0-9_-]*/',text):
  raise SystemExit('Personal location in recipe rejected: '+str(rel))
 # Materialize laboratory locations explicitly; no machine home layout is published.
 text=text.replace("pathlib.Path.home()/"+repr(source_relative), "pathlib.Path('@LAB_ROOT@')")
 text=text.replace("Path.home()/"+repr(source_relative), "Path('@LAB_ROOT@')")
 text=text.replace('$HOME/'+source_relative, '@LAB_ROOT@').replace('~/'+source_relative, '@LAB_ROOT@')
 text=text.replace('../'+previous_name, '@PREVIOUS_LAB_ROOT@').replace("'"+previous_name, "'@PREVIOUS_LAB_ROOT@")
 text=text.replace(source_relative, '@LAB_ROOT@')
 # These installer diagnostics are host-generated tokens, not access credentials.
 target=recipes/(str(rel)+'.in');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
 rows.append(target.relative_to(c).as_posix())
# Ship bounded chunks; reconstruction is byte-identical, without recompilation.
packed=c/'collector/probe-linux-amd64.gz'
data=packed.read_bytes()
for stale in (c/'collector').glob('probe-linux-amd64.gz.part-*'):stale.unlink()
for i,start in enumerate(range(0,len(data),250000)):
 (c/f'collector/probe-linux-amd64.gz.part-{i:03d}').write_bytes(data[start:start+250000])
(c/'rehearsal/recipe-paths.txt').write_text('\n'.join(rows)+'\n')
print('recipe_templates',len(rows),'binary_parts',(len(data)+249999)//250000)
