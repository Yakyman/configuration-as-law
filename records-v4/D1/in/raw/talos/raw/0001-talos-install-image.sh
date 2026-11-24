python3 -c 'import json,re,subprocess,sys
p=subprocess.run(['"'"'talosctl'"'"','"'"'get'"'"','"'"'machineconfig'"'"','"'"'v1alpha1'"'"','"'"'-o'"'"','"'"'json'"'"'],capture_output=True,timeout=12)
if p.returncode:
 sys.stderr.buffer.write(p.stderr);sys.exit(p.returncode)
try:
 spec=json.loads(p.stdout)['"'"'spec'"'"']
 if not isinstance(spec,str): raise ValueError('"'"'machine config spec is not YAML text'"'"')
 images=[]
 for doc in re.split(r'"'"'^---\s*$'"'"',spec,flags=re.M):
  wanted=['"'"'installer'"'"','"'"'image'"'"'] if re.search(r'"'"'^kind: UnattendedInstallConfig\s*$'"'"',doc,re.M) else ['"'"'machine'"'"','"'"'install'"'"','"'"'image'"'"']
  stack=[]
  for line in doc.splitlines():
   m=re.match(r'"'"'^( *)([A-Za-z][A-Za-z0-9]*):(?: (.*))?$'"'"',line)
   if not m: continue
   n=len(m.group(1))
   while stack and stack[-1][0]>=n: stack.pop()
   keys=[v for _,v in stack]+[m.group(2)]
   if keys==wanted and m.group(3): images.append(m.group(3).strip().strip('"'"'\"\'"'"''"'"'))
   stack.append((n,m.group(2)))
 images=[i for i in images if re.fullmatch(r'"'"'[A-Za-z0-9._/@:+-]+'"'"',i)]
 print(json.dumps({'"'"'images'"'"':images}))
except (ValueError,KeyError,TypeError):
 print('"'"'active machine configuration image could not be decoded'"'"',file=sys.stderr);sys.exit(65)
'
