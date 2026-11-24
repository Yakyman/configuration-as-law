python3 -c '
import subprocess,json,sys
p=subprocess.run(['"'"'talosctl'"'"','"'"'get'"'"','"'"'StaticPods.kubernetes.talos.dev'"'"','"'"'-o'"'"','"'"'json'"'"'],capture_output=True,timeout=12)
if p.returncode:sys.stderr.buffer.write(p.stderr);sys.exit(p.returncode)
text=p.stdout.decode();decoder=json.JSONDecoder()
def images(value):
 if isinstance(value,dict):
  for key,item in value.items():
   if key=='"'"'image'"'"' and isinstance(item,str):yield item
   else:yield from images(item)
 elif isinstance(value,list):
  for item in value:yield from images(item)
while text.strip():
 text=text.lstrip();obj,end=decoder.raw_decode(text);text=text[end:]
 for image in sorted(set(images(obj.get('"'"'spec'"'"',{})))):print(json.dumps({'"'"'resource_id'"'"':obj.get('"'"'metadata'"'"',{}).get('"'"'id'"'"','"'"''"'"'),'"'"'image'"'"':image}))
'
