import ast,base64,hashlib,json,pathlib
P=pathlib.Path
root=P('B2/raw/round-1/final-2')
ids=['SAVED-SCRIPT','SAVED-PIPE','SAVED-SOURCE','STARTUP-ENV','PYTHON-IMPORT','PICKLE-CODE','DIRECT-REDIRECT-STDIN','DIRECT-PROC-FD','DIRECT-READ-EXEC','DIRECT-AWK-FILE','DIRECT-SCRIPT-HELPER','RC-STARTUP','EDITOR-SAVED-COMMANDS','JIT-SAVED-INPUT','DISPATCHER-SAVED']
logs={}
for name in ['shell.jsonl','tools.jsonl','supplement/direct.jsonl','supplement/extra.jsonl']:
 logs[name]=[json.loads(l) for l in (root/name).read_text().splitlines()]
files={}
def file(path,data,mode=0o644):
 if isinstance(data,str):data=data.encode()
 files[path]=dict(path=path,content_b64=base64.b64encode(data).decode(),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),mode=mode,uid=1000,gid=1000)
file('/home/stand/saved.txt',b'printf SAVED_CODE_RAN\n')
file('/home/stand/loose_module.py',b'print("IMPORTED_UNRECORDED")\n')
file('/home/stand/serialized',b"cbuiltins\nprint\n(S'PICKLE_EXECUTED'\ntR.")
for name in ['direct','extra']:
 tree=ast.parse(P('B2/raw/round-1/final-2-supplement-inputs/v4-'+name+'-selftest.py').read_text())
 for n in ast.walk(tree):
  if not isinstance(n,ast.Call) or not isinstance(n.func,ast.Name):continue
  if name=='direct' and n.func.id=='write' and isinstance(n.args[0],ast.Constant) and n.args[0].value in ('saved.sh','saved.py','saved.awk'):
   file('/home/stand/v4-direct/'+n.args[0].value,ast.literal_eval(n.args[1]),ast.literal_eval(n.args[2]) if len(n.args)>2 else 0o644)
  if name=='extra' and n.func.id=='fixture' and isinstance(n.args[0],ast.BinOp) and isinstance(n.args[0].right,ast.Constant) and n.args[0].right.value in ('startup.rc','commands.ed','instructions.ops'):
   file('/tmp/v4-extra-7z89hz2f/'+n.args[0].right.value,ast.literal_eval(n.args[1]),0o600)
file('/tmp/v4-extra-7z89hz2f/machine.bytes',b'\xb8\x2a\x00\x00\x00\xc3',0o600)
# Verify exact known source bytes against original observations.
verified=[]
for name,rows in logs.items():
 for row in rows:
  entries=row.get('files',[])
  if row.get('phase') in ('fixture','fixture_expected'):entries=entries+[row]
  for e in entries:
   if e.get('path') in files and 'sha256' in e:
    assert e['sha256']==files[e['path']]['sha256'],e
    verified.append(dict(path=e['path'],sha256=e['sha256'],source=str(root/name)))
source_map={
'SAVED-SCRIPT':'saved.txt','SAVED-PIPE':'saved.txt','SAVED-SOURCE':'saved.txt','STARTUP-ENV':'saved.txt',
'PYTHON-IMPORT':'loose_module.py','PICKLE-CODE':'serialized','DIRECT-REDIRECT-STDIN':'v4-direct/saved.sh','DIRECT-PROC-FD':'v4-direct/saved.sh','DIRECT-SCRIPT-HELPER':'v4-direct/saved.sh','DIRECT-READ-EXEC':'v4-direct/saved.py','DIRECT-AWK-FILE':'v4-direct/saved.awk',
'RC-STARTUP':'/tmp/v4-extra-7z89hz2f/startup.rc','EDITOR-SAVED-COMMANDS':'/tmp/v4-extra-7z89hz2f/commands.ed','JIT-SAVED-INPUT':'/tmp/v4-extra-7z89hz2f/machine.bytes','DISPATCHER-SAVED':'/tmp/v4-extra-7z89hz2f/instructions.ops'}
markers=['SAVED_CODE_RAN']*4+['IMPORTED_UNRECORDED','PICKLE_EXECUTED','SAVED_DIRECT_RAN','SAVED_DIRECT_RAN','READ_EXEC_RAN','AWK_FILE_RAN','SAVED_DIRECT_RAN','SAVED_RC_EXECUTED','SAVED_EDITOR_COMMAND_EXECUTED','JIT_SAVED_INPUT_EXECUTED 42','DISPATCHER_SAVED_EXECUTED']
cases=[]
for ident,marker in zip(ids,markers):
 found=[(name,r) for name,rows in logs.items() for r in rows if r.get('id')==ident and r.get('phase')=='expected']
 assert len(found)==1
 name,row=found[0];path=source_map[ident]
 if not path.startswith('/'):path='/home/stand/'+path
 cases.append(dict(id=ident,command=row['command'],cwd='/home/stand/v4-direct' if ident.startswith('DIRECT-') else '/home/stand',marker=marker,files=[path],source_log=str(root/name),inline_writes=ident in ('SAVED-SCRIPT','PYTHON-IMPORT','PICKLE-CODE')))
account=next(r for r in logs['tools.jsonl'] if r.get('id')=='root-native-account-bypass' and r.get('phase')=='expected')
dispatcher=next(r['exact_row'] for r in logs['supplement/extra.jsonl'] if r.get('id')=='DISPATCHER-INSTALL' and r.get('phase')=='expected')
out=dict(version=1,cases=cases,account=dict(id='root-native-account-bypass',command=account['command'],source_log=str(root/'tools.jsonl')),files=list(files.values()),dispatcher_row=dispatcher,verified_original_hashes=verified)
P('B2/build/bc3-fixtures.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('15 exact commands,',len(files),'fixtures,',len(verified),'original hash matches')
