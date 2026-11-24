#!/usr/bin/python3
"""External-root fixtures; every attack executes through the ordinary launcher.
Sources/expected mechanisms: B2/raw/round-2/REVIEW.md. Run once per fresh
image as an integration self-test, not as a probe of documented Linux semantics.
"""
import base64,hashlib,json,os,pathlib,pwd,shutil,subprocess,sys,time,zipfile,py_compile,socket,pty,re,struct
P=pathlib.Path
OUT=P(sys.argv[1] if len(sys.argv)>1 else '/var/lib/stand/round2.jsonl')
OUT.parent.mkdir(parents=True,exist_ok=True)
log=OUT.open('w',buffering=1);failed=[];counter=0
HOME=P('/home/stand');WORK=HOME/'round2';WORK.mkdir(exist_ok=True)
uid=pwd.getpwnam('stand').pw_uid;gid=pwd.getpwnam('stand').pw_gid
MARK='UNRECORDED_CODE'
def record(obj):
 obj['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());log.write(json.dumps(obj,sort_keys=True)+'\n');print(json.dumps(obj,sort_keys=True),flush=True)
def run(id,variants,args,expected='deny',stdin=None,env=None,contains=None,fd=None):
 record(dict(phase='expected',id=id,variants=variants,command=args,stdin=stdin,environment=env,expected=expected,contains=contains,source='B2/raw/round-2/REVIEW.md'))
 try:
  p=subprocess.run(args,input=stdin if fd is None else None,stdin=fd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,timeout=300)
  ok=(p.returncode!=0 if expected=='deny' else p.returncode==0) and MARK not in p.stdout and (contains is None or contains in p.stdout)
  result=dict(rc=p.returncode,output=p.stdout)
 except subprocess.TimeoutExpired as e:ok=False;result=dict(rc='timeout',output=str(e))
 record(dict(phase='result',id=id,variants=variants,passed=ok,**result))
 if not ok:failed.append(id)
 return result

def session(id,variants,fields,**kw):
 # env placed after runuser: hostile loader variables must reach the launcher,
 # not alter the external-root fixture's own executable loader.
 env=kw.pop('env',None)
 args=['/usr/sbin/runuser','-u','stand','--']
 if env:args+=['/usr/bin/env']+[k+'='+v for k,v in env.items()]
 return run(id,variants,args+['/usr/local/bin/stand-session','-c','\t'.join(fields)],**kw)
def write(path,text,mode=0o644):
 path=P(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text);path.chmod(mode);os.chown(path,uid,gid);return path

def artifact(name,body,interpreter=None,mode=0o644):
 global counter
 path='/opt/stand/pkgs/round2/'+name
 data=body.encode() if isinstance(body,str) else body
 f=dict(path=path,kind='file',mode=mode,uid=0,gid=0,sha256=hashlib.sha256(data).hexdigest(),content_b64=base64.b64encode(data).decode())
 return f,dict(path=path,interpreter=interpreter) if interpreter else None

def main():
 files=[];eps=[]
 run('SERVICE-ORDINARY-LAUNCHER',['C7.01','C7.24'],['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-session','--service','stand-development.service'])
 run('SERVICE-ORDINARY-TRUSTED-PATH',['C7.01','C7.24'],['/usr/sbin/runuser','-u','stand','--','/usr/local/lib/stand/service-launch','--service','stand-development.service'])
 run('SERVICE-OPERATOR-NOT-MANAGER',['C7.01','C7.24'],['/usr/local/lib/stand/service-launch','--service','stand-development.service'])
 def script(name,body,interpreter='/usr/bin/python3.13'):
  f,ep=artifact(name,body,interpreter);files.append(f);eps.append(ep);return f['path']
 evil=write(WORK/'evil.py',"print('"+MARK+"')\n")
 shell=write(WORK/'evil.sh',"#!/bin/bash\nprintf '"+MARK+"'\n",0o755)
 write(WORK/'evilmod.py',evil.read_text())
 with zipfile.ZipFile(WORK/'evil.zip','w') as z:z.writestr('zipmod.py',evil.read_text())
 py_compile.compile(str(evil),cfile=str(WORK/'evil.pyc'))
 write(HOME/'.bashrc',shell.read_text());write(HOME/'.profile',shell.read_text());write(HOME/'.bash_profile',shell.read_text())
 write(HOME/'.pythonrc',evil.read_text());write(HOME/'.inputrc',shell.read_text())
 write(WORK/'.git/hooks/pre-commit',shell.read_text(),0o755)
 write(WORK/'.git/config','[alias]\n pwn = !printf '+MARK+'\n[filter "pwn"]\n clean = printf '+MARK+'\n')
 write(WORK/'.gitattributes','*.txt filter=pwn\n')
 (WORK/'evil.wasm').write_bytes(b'\x00asm\x01\x00\x00\x00')
 write(WORK/'Makefile','all:\n\t@printf '+MARK+'\n')
 write(HOME/'.exrc','!printf '+MARK+'\n');write(HOME/'.vimrc','python3 '+evil.read_text())
 positive=script('positive.py',"print('RECORDED_OK')\n")
 source=script('source.sh','. /home/stand/round2/evil.sh\n','/usr/bin/bash')
 execfile=script('execfile.py',"exec(open('/home/stand/round2/evil.py').read())\n")
 evalfile=script('evalfile.py',"eval(open('/home/stand/round2/evil.py').read())\n")
 imports=script('import.py',"import sys\nsys.path.insert(0,'/home/stand/round2')\nimport evilmod\n")
 zipimports=script('zip.py',"import sys\nsys.path.insert(0,'/home/stand/round2/evil.zip')\nimport zipmod\n")
 custom=script('loader.py',"import importlib.machinery\nimportlib.machinery.SourceFileLoader('evil','/home/stand/round2/evil.py').load_module()\n")
 bytecode=script('bytecode.py',"import importlib.machinery\nimportlib.machinery.SourcelessFileLoader('evil','/home/stand/round2/evil.pyc').load_module()\n")
 stdincheck=script('stdin.py',"import sys\nassert sys.stdin.read()==''\nprint('STDIN_EMPTY')\n")
 envcheck=script('env.py',"import os\nassert not any(k in os.environ for k in ['BASH_ENV','ENV','PYTHONSTARTUP','PYTHONPATH','LD_PRELOAD','LD_AUDIT'])\nprint('ENV_CLEAN')\n")
 shellpositive=script('shell.sh',"printf 'SHELL_RECORDED_OK\\n'\n",'/usr/bin/bash')
 dispatch=script('dispatch.py',"for instruction in open('/home/stand/round2/evil.py'):\n print(instruction)\n")
 oracle=script('oracle.py',"""import os,errno
paths=['/home/stand/round2/evil.py','/home/stand/round2/absent-oracle']
for method in ['stat','opath']:
 results=[]
 for path in paths:
  try:
   if method=='stat': os.stat(path)
   else:
    fd=os.open(path,os.O_PATH);os.close(fd)
   results.append(0)
  except OSError as error: results.append(error.errno)
 assert results==[errno.ENOENT,errno.ENOENT],(method,results)
try:
 os.listdir('/home/stand/round2')
 raise AssertionError('unrecorded home tree visible')
except OSError as error:
 assert error.errno==errno.ENOENT,error.errno
print('SNAPSHOT_ORACLE_HIDDEN')
""")
 metadata=script('metadata.py',"import os\nsize=os.stat('/home/stand/round2/evil.py').st_size\nprint('UNRECORDED_CODE',size)\n")
 directory=script('directory.py',"import os\nnames=os.listdir('/home/stand')\nprint('UNRECORDED_CODE',names)\n")
 binfmt=script('binfmt.py',"open('/proc/sys/fs/binfmt_misc/register','w').write(':round2:M::R2MAGIC::/usr/bin/python3.13:')\n")
 pickle=script('pickle.py',"import pickle\npickle.load(open('/home/stand/round2/payload.pickle','rb'))\n")
 write(WORK/'payload.pickle',"cos\nsystem\n(S'printf "+MARK+"'\ntR.")
 compiler=shutil.which('cc') or shutil.which('gcc')
 probe=P(__file__).with_name('round2-probe.c')
 if not compiler:raise RuntimeError('guest compiler required for native fixtures')
 run('FIXTURE-COMPILE',[],[compiler,str(probe),'-o',str(WORK/'native'),'-ldl'],expected='ok')
 run('FIXTURE-LIBRARY',[],[compiler,'-shared','-fPIC','-x','c','-o',str(WORK/'libprobe.so'),'-'],expected='ok',stdin='#include <unistd.h>\n__attribute__((constructor)) static void init(void){write(2,"UNRECORDED_CODE",15);}\n')
 f,_=artifact('native',(WORK/'native').read_bytes(),mode=0o755);files.append(f);native=f['path']
 run('FIXTURE-HOLDER',[],[compiler,str(probe),'-DHOLDER','-o',str(WORK/'holder'),'-ldl'],expected='ok')
 f,_=artifact('holder',(WORK/'holder').read_bytes(),mode=0o755);files.append(f);holder=f['path']
 row=dict(id='round2',type='code',version='2',source='selftest-fixtures',managed=True,files=files,entrypoints=eps)
 line=write(WORK/'line.json',json.dumps(row))
 session('ADMIT',['C5.1'],['broker','stand-line','add',str(line)],expected='ok')
 session('POSITIVE',[],['run',positive],expected='ok',contains='RECORDED_OK')
 # Builder-only malformed-native admission attempts. Each candidate replaces
 # just the fixture row and must fail before policy activation.
 run('FIXTURE-EXECSTACK',[],[compiler,str(probe),'-Wl,-z,execstack','-o',str(WORK/'execstack'),'-ldl'],expected='ok')
 bad_native=[('EXECSTACK',(WORK/'execstack').read_bytes())]
 foreign=bytearray((WORK/'native').read_bytes());struct.pack_into('<H',foreign,18,183)
 bad_native.append(('FOREIGN-ELF',bytes(foreign)))
 wx=bytearray((WORK/'native').read_bytes());phoff=struct.unpack_from('<Q',wx,32)[0];phsize,phnum=struct.unpack_from('<HH',wx,54)
 for idx in range(phnum):
  off=phoff+idx*phsize
  if struct.unpack_from('<I',wx,off)[0]==1:
   flags=struct.unpack_from('<I',wx,off+4)[0];struct.pack_into('<I',wx,off+4,flags|3);break
 bad_native.append(('WX-ELF',bytes(wx)))
 for kind,data in bad_native:
  badfile,_=artifact('bad-'+kind.lower(),data,mode=0o755)
  badrow=dict(row,files=files+[badfile]);badline=write(WORK/('bad-'+kind.lower()+'.json'),json.dumps(badrow))
  run('ADMISSION-'+kind,['C7.16','C7.23'],['/usr/local/bin/stand-line','add',str(badline)])
 for label,suffix in [('TAB','bad\tdata'),('NEWLINE','bad\nrun')]:
  badfile,badep=artifact(suffix,"print('RECORDED_OK')\n",'/usr/bin/python3.13')
  badrow=dict(row,files=files+[badfile],entrypoints=eps+[badep]);badline=write(WORK/('bad-'+label.lower()+'.json'),json.dumps(badrow))
  before_generation=str(P('/var/lib/stand/current').resolve());before_table=P('/etc/stand/launch.tsv').read_bytes()
  record(dict(phase='expected',id='ADMISSION-'+label+'-UNCHANGED',variants=['C7.01'],expected='generation and launch table unchanged after rejected malformed entrypoint'))
  run('ADMISSION-'+label,['C7.01'],['/usr/local/bin/stand-line','add',str(badline)])
  unchanged=str(P('/var/lib/stand/current').resolve())==before_generation and P('/etc/stand/launch.tsv').read_bytes()==before_table
  record(dict(phase='result',id='ADMISSION-'+label+'-UNCHANGED',variants=['C7.01'],passed=unchanged))
  if not unchanged:failed.append('ADMISSION-'+label+'-UNCHANGED')
 session('EXISTENCE-ORACLE',['C7.24'],['run',oracle],expected='ok',contains='SNAPSHOT_ORACLE_HIDDEN')
 session('METADATA-DISPATCH',['C7.24'],['run',metadata])
 session('DIRECTORY-DISPATCH',['C7.24'],['run',directory])
 session('POSITIVE-AFTER-REFUSALS' ,[],['run',positive],expected='ok',contains='RECORDED_OK')
 for name,args in [('CONFIGURE',['-o',str(WORK/'configure-probe'),'-x','c','-']),('GENERATOR',['-o',str(WORK/'generator'),str(probe)]),('PLUGIN',['-fplugin='+str(WORK/'libprobe.so'),'-c',str(probe)])]:
  session('COMPILER-'+name,['C5.2','C5.5'],['run',compiler,*args],stdin='int main(void){return 0;}\n')
 session('BINFMT-REGISTER',['C7.23'],['run',binfmt])
 # Exhaustive installed-interpreter inventory; removed general launch interfaces
 # are tested with concrete language inputs, never inferred from file suffixes.
 candidates={'bash':['-c','printf '+MARK], 'sh':['-c','printf '+MARK], 'dash':['-c','printf '+MARK], 'python3':['-c',"print('"+MARK+"')"], 'python3.13':['-c',"print('"+MARK+"')"], 'perl':['-e',"print '"+MARK+"'"], 'awk':['BEGIN {print "'+MARK+'"}'], 'mawk':['BEGIN {print "'+MARK+'"}'], 'make':['-f',str(WORK/'Makefile')], 'find':[str(WORK),'-exec','/bin/sh','-c','printf '+MARK,';'], 'git':['-C',str(WORK),'pwn'], 'vi':['-c','!printf '+MARK], 'vim':['-c','!printf '+MARK], 'gdb':['-ex','python print("'+MARK+'")'], 'sqlite3':[':memory:','.shell printf '+MARK], 'node':['-e','console.log("'+MARK+'")'], 'lua':['-e','print("'+MARK+'")'], 'ruby':['-e','puts "'+MARK+'"'], 'tclsh':[str(shell)], 'qemu-x86_64':[str(WORK/'native')], 'wasmtime':['--dir',str(WORK),str(WORK/'evil.wasm')]}
 inventory={k:shutil.which(k) for k in candidates};record(dict(phase='inventory',interpreters=inventory,launch_table=P('/etc/stand/launch.tsv').read_text()))
 for name,path in inventory.items():
  if path:session('INTERPRETER-'+name,['C7.03','C7.10','C7.11','C7.12','C8.05'],['run',path,*candidates[name]])
 for name in ('bash','python3','perl','awk'):
  path=inventory.get(name)
  if not path:continue
  session('FILE-'+name,['C7.01','C4.4'],['run',path,str(evil)])
  session('PIPE-'+name,['C7.04','C4.5'],['run',path],stdin=evil.read_text())
  with evil.open() as stream:session('REDIRECT-'+name,['C7.05'],['run',path],fd=stream)
  session('INTERACTIVE-'+name,['C7.06'],['run',path,'-i'],stdin=evil.read_text())
 session('SHEBANG',['C7.02'],['run',str(shell)])
 # These removed-entrypoint requests run even if inventory says the underlying
 # executable is absent. They evidence launcher removal, not runtime behavior.
 literal_routes=[
 ('GIT-HOOK',['C7.12'],['run','/usr/bin/git','-C',str(WORK),'commit','--allow-empty','-m','fixture']),
 ('GIT-ALIAS',['C8.05'],['run','/usr/bin/git','-C',str(WORK),'pwn']),
 ('GIT-FILTER',['C8.05'],['run','/usr/bin/git','-C',str(WORK),'-c','filter.pwn.clean=printf '+MARK,'hash-object','--path=document.txt',str(evil)]),
 ('HOOK-DIRECT',['C7.12'],['run',str(WORK/'.git/hooks/pre-commit')]),
 ('HOOK-INTERPRETER',['C7.12'],['run','/usr/bin/bash',str(WORK/'.git/hooks/pre-commit')]),
 ('MAKE-RECIPE',['C5.2','C7.11','C8.05'],['run','/usr/bin/make','-f',str(WORK/'Makefile')]),
 ('WASI-PREOPEN',['C7.21'],['run','/usr/bin/wasmtime','--dir',str(WORK),str(WORK/'evil.wasm')])]
 for literal_id,variants,fields in literal_routes:session(literal_id,variants,fields)

 session('PROC-FD',['C7.05'],['run','/usr/bin/python3.13','/proc/self/fd/0'],stdin=evil.read_text())
 for name,path,var in [('SOURCE',source,'C7.07'),('EXEC-OPEN',execfile,'C7.08'),('EVAL-OPEN',evalfile,'C7.08'),('IMPORT',imports,'C7.09'),('ZIPIMPORT',zipimports,'C7.09'),('CUSTOM-LOADER',custom,'C7.08'),('BYTECODE',bytecode,'C7.09'),('DISPATCH',dispatch,'C7.24'),('PICKLE',pickle,'C7.20')]:session(name,[var]+(['C7.18'] if name=='BYTECODE' else []),['run',path])
 session('SEALED-ARGS',['C7.03','C7.24'],['run',positive,'-c',evil.read_text()])
 session('SEALED-PIPE',['C7.04','C7.24'],['run',stdincheck],stdin=evil.read_text(),expected='ok',contains='STDIN_EMPTY')
 with evil.open() as stream:session('SEALED-REDIRECT',['C7.05'],['run',stdincheck],fd=stream,expected='ok',contains='STDIN_EMPTY')
 hostile={'BASH_ENV':str(shell),'ENV':str(shell),'PYTHONSTARTUP':str(evil),'PYTHONPATH':str(WORK),'BASH_FUNC_pwn%%':'() { printf '+MARK+'; }'}
 fifo=WORK/'fifo';os.mkfifo(fifo);fifo_fd=os.open(fifo,os.O_RDWR|os.O_NONBLOCK);os.write(fifo_fd,evil.read_bytes())
 session('SEALED-FIFO',['C7.04'],['run',stdincheck],fd=fifo_fd,expected='ok',contains='STDIN_EMPTY');os.close(fifo_fd)
 left,right=socket.socketpair();left.sendall(evil.read_bytes());left.shutdown(socket.SHUT_WR)
 session('SEALED-SOCKET',['C7.04'],['run',stdincheck],fd=right.fileno(),expected='ok',contains='STDIN_EMPTY');left.close();right.close()
 master,slave=pty.openpty();os.write(master,evil.read_bytes())
 session('REPL-PTY',['C7.06'],['run','/usr/bin/python3.13','-i'],fd=slave);os.close(master);os.close(slave)
 session('ENVIRONMENT',['C8.02','C8.03'],['run',envcheck],env=hostile,expected='ok',contains='ENV_CLEAN')
 session('PRELOAD',['C7.14'],['run',envcheck],env={'LD_PRELOAD':str(WORK/'libprobe.so'),'LD_AUDIT':str(WORK/'libprobe.so'),'LD_LIBRARY_PATH':str(WORK)},expected='ok',contains='ENV_CLEAN')
 session('SHELL-STARTUP',['C8.01','C8.02','C8.03'],['run',shellpositive],env=hostile,expected='ok',contains='SHELL_RECORDED_OK')
 for name,text in [('TYPED','/usr/bin/cat /home/stand/round2/evil.py'),('FUNCTION','pwn() { printf '+MARK+'; }; pwn'),('ALIAS',"alias pwn='printf "+MARK+"'; pwn"),('SUBSTITUTION','echo $(printf '+MARK+')'),('PROCESS-SUBSTITUTION','bash <(printf '+MARK+')'),('HEREDOC','bash <<EOF\nprintf '+MARK+'\nEOF')]:session(name,['C7.17','C8.06','C7.04'],[text])
 session('LOADER',['C7.13'],['run','/lib64/ld-linux-x86-64.so.2',str(WORK/'native')])
 session('NATIVE-KERNEL',['C7.11','C7.14','C7.15','C7.16','C7.22','C7.25'],['run',native],expected='ok',contains='FEXECVE DENIED')
 # Safe values-only tools retain ordinary document and browser operation.
 doc=write(WORK/'document.txt','Before\n')
 session('EDITOR-POSITIVE',[],['run','/usr/bin/dd',str(doc)],stdin='After\n',expected='ok')
 session('EDITOR-READ',[],['run','/usr/bin/cat',str(doc)],expected='ok',contains='After')
 record(dict(phase='assert',id='EDITOR-CONTENT',passed=doc.read_text()=='After\n',content=doc.read_text()))
 if doc.read_text()!='After\n':failed.append('EDITOR-CONTENT')
 session('EDITOR-ESCAPE',['C7.10','C7.11','C8.06'],['run','/usr/bin/ed',str(doc)],stdin='!printf '+MARK+'\nq\n')
 for label,commands in [('GLOBAL','g/After/s/After/changed/\nw\nq\n'),('SOURCE','r !/usr/bin/bash '+str(shell)+'\nq\n'),('DEFINITION','g/After/\\\n!printf '+MARK+'\nq\n')]:
  session('EDITOR-'+label,['C7.10','C8.06'],['run','/usr/bin/ed',str(doc)],stdin=commands)
 modeline=write(WORK/'modeline.txt','Before\n')
 modeline_text='vim: set makeprg=printf\\ '+MARK+':\n!printf '+MARK+'\n'
 session('EDITOR-MODELINE',['C8.04','C8.08'],['run','/usr/bin/dd',str(modeline)],stdin=modeline_text,expected='ok')
 record(dict(phase='assert',id='EDITOR-MODELINE-CONTENT',passed=modeline.read_text()==modeline_text,content=modeline.read_text()))
 if modeline.read_text()!=modeline_text:failed.append('EDITOR-MODELINE-CONTENT')
 session('WRITER-OPERAND',['C8.06'],['run','/usr/bin/dd','of='+str(WORK/'operand-target')],stdin='literal document\n')
 session('WRITER-EXTRA-OPTION',['C8.06'],['run','/usr/bin/dd',str(doc),'of='+str(WORK/'operand-target')],stdin='literal document\n')
 session('WRITER-NO-TARGET',['C8.06'],['run','/usr/bin/dd'],stdin='literal document\n')
 page=write(WORK/'page.html','<html><body>Browser path works<script>document.write("'+MARK+'")</script></body></html>')
 session('BROWSER',['C7.19'],['run','/usr/bin/w3m',str(page)],expected='ok',contains='Browser path works')
 browser_config=write(WORK/'w3m-config','extbrowser /usr/bin/bash -c "printf '+MARK+'"\n')
 session('BROWSER-OPTIONS',['C8.07'],['run','/usr/bin/w3m','-config',str(browser_config)])
 extension=WORK/'extension';extension.mkdir(exist_ok=True)
 write(extension/'manifest.json',json.dumps({'manifest_version':3,'name':'round2','version':'1','background':{'service_worker':'background.js'}}))
 write(extension/'background.js',"fetch('file:///home/stand/round2/evil.py').then(x=>x.text()).then(eval)\n")
 browser_inventory={name:shutil.which(name) for name in ('chromium','chromium-browser','firefox','w3m')}
 record(dict(phase='inventory',browser_capabilities=browser_inventory,extension_fixture=str(extension)))
 session('BROWSER-EXTENSION-REQUEST',['C8.07'],['run','/usr/bin/chromium','--load-extension='+str(extension),'about:blank'])
 page_one=write(WORK/'home-one.html','<html><body>Home preference one</body></html>')
 page_two=write(WORK/'home-two.html','<html><body>Home preference two</body></html>')
 session('HOME-PREFERENCE-ONE',['C8.08'],['run','/usr/bin/w3m',str(page_one)],expected='ok',contains='Home preference one')
 session('HOME-PREFERENCE-TWO',['C8.08'],['run','/usr/bin/w3m',str(page_two)],expected='ok',contains='Home preference two')
 # Native location/suffix/alias routes are independent of the source transport.
 for name in ['downloaded','nested/extracted.renamed','build/output','prefix/bin/app','old-copy']:
  dest=WORK/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(WORK/'native',dest)
  session('NATIVE-'+name.replace('/','-'),['C4.1','C4.2','C4.3','C5.1','C5.2','C5.3'],['run',str(dest)])
 alias=WORK/'alias';alias.symlink_to(WORK/'native');session('NATIVE-SYMLINK',['C5.3'],['run',str(alias)])
 session('OVERWRITE',['C5.4'],['run','/usr/bin/cp',str(WORK/'native'),native])
 active_rows=[json.loads(x) for x in (P('/var/lib/stand/current')/'machine.jsonl').read_text().splitlines() if x.strip()]
 login_key=next(r['path'] for r in active_rows if r['id']=='key:stand')
 key_before=P(login_key).read_bytes()
 record(dict(phase='expected',id='LOGIN-KEY-UNCHANGED',variants=['C8.01'],expected='ordinary data tools cannot overwrite protected login key'))
 session('LOGIN-KEY-CP',['C8.01'],['run','/usr/bin/cp',str(evil),login_key])
 session('LOGIN-KEY-WRITER',['C8.01'],['run','/usr/bin/dd',login_key],stdin='replacement-key\n')
 session('LOGIN-KEY-ED',['C8.01'],['run','/usr/bin/ed',login_key],stdin='a\nreplacement-key\n.\nw\nq\n')
 key_same=P(login_key).read_bytes()==key_before
 record(dict(phase='result',id='LOGIN-KEY-UNCHANGED',variants=['C8.01'],passed=key_same))
 if not key_same:failed.append('LOGIN-KEY-UNCHANGED')

 # A declared timer is an activation edge even when its service row does not
 # change.  Changing the recorded executable must stop both before revoke and
 # restart only the candidate after the snapshot and policy are installed.
 service_program_id='round2-service-program';service_path='/opt/stand/pkgs/'+service_program_id+'/holder'
 holder_v1=(WORK/'holder').read_bytes();holder_v2=holder_v1+b'ROUND2-V2\n'
 def service_program(data,version):
  f=dict(path=service_path,kind='file',mode=0o755,uid=0,gid=0,sha256=hashlib.sha256(data).hexdigest(),content_b64=base64.b64encode(data).decode())
  return dict(id=service_program_id,type='program',version=version,source='selftest-service-fixture',managed=True,files=[f])
 def unit_row(ident,typ,unit,text,active):
  return dict(id=ident,type=typ,managed=True,unit=unit,enabled='disabled',active=active,unit_text=text,unit_sha256=hashlib.sha256(text.encode()).hexdigest())
 service_unit='''[Unit]\nDescription=Round 2 lifecycle service\n[Service]\nType=simple\nUser=stand\nExecStart='''+service_path+'''\nRestart=no\nKillMode=control-group\nTimeoutStopSec=5\nMemoryDenyWriteExecute=yes\nNoNewPrivileges=yes\nProtectSystem=strict\nPrivateTmp=yes\n[Install]\nWantedBy=multi-user.target\n'''
 timer_unit='''[Unit]\nDescription=Round 2 lifecycle timer\n[Timer]\nOnUnitActiveSec=1s\nUnit=stand-round2-lifecycle.service\nPersistent=false\n[Install]\nWantedBy=timers.target\n'''
 service_row=unit_row('round2-service','service','stand-round2-lifecycle.service',service_unit,True)
 timer_row=unit_row('round2-timer','timer','stand-round2-lifecycle.timer',timer_unit,True)
 program_line=write(WORK/'service-program.json',json.dumps(service_program(holder_v1,'1')))
 session('SERVICE-PROGRAM-ADMIT',['M4.01','M4.02'],['broker','stand-line','add',str(program_line)],expected='ok')
 for label,replacement in (
  ('PIPE-ARG',service_unit.replace('ExecStart='+service_path,'ExecStart='+service_path+' literal|argument')),
  ('RESTART',service_unit.replace('Restart=no','Restart=always')),
 ):
  bad=unit_row('round2-bad-'+label.lower(),'service','stand-round2-bad-'+label.lower()+'.service',replacement,False)
  badline=write(WORK/('service-bad-'+label.lower()+'.json'),json.dumps(bad))
  session('SERVICE-ADMISSION-'+label,['C6.6','C7.24'],['broker','stand-line','add',str(badline)])
 service_line=write(WORK/'service.json',json.dumps(service_row))
 timer_line=write(WORK/'timer.json',json.dumps(timer_row))
 session('SERVICE-LIFECYCLE-ADMIT',['M4.01','M4.02'],['broker','stand-line','add',str(service_line)],expected='ok')
 session('TIMER-LIFECYCLE-ADMIT',['M4.01','M4.03'],['broker','stand-line','add',str(timer_line)],expected='ok')
 def service_pids():
  deadline=time.monotonic()+10
  while time.monotonic()<deadline:
   q=subprocess.run(['/usr/bin/systemctl','show','stand-round2-lifecycle.service','-p','MainPID','--value'],text=True,stdout=subprocess.PIPE)
   try:mainpid=int(q.stdout.strip())
   except ValueError:mainpid=0
   if mainpid:
    descendants=[];pending=[mainpid];seen={mainpid}
    while pending:
     parent=pending.pop()
     try:children=[int(x) for x in P('/proc',str(parent),'task',str(parent),'children').read_text().split()]
     except FileNotFoundError:children=[]
     for child in children:
      if child not in seen:seen.add(child);descendants.append(child);pending.append(child)
    if len(descendants)>=2:return [mainpid,*descendants]
   time.sleep(.05)
  return []
 def pid_alive(pid):
  try:return P('/proc',str(pid),'stat').read_text().split(') ',1)[1][0]!='Z'
  except FileNotFoundError:return False
 old_service_pids=service_pids()
 record(dict(phase='expected',id='SERVICE-TIMER-CODE-CHANGE',variants=['M4.01','M4.02','M4.03'],expected='old relay, target and fork descendant absent before candidate restart',old_pids=old_service_pids))
 program_line.write_text(json.dumps(service_program(holder_v2,'2')));os.chown(program_line,uid,gid)
 session('SERVICE-TIMER-UPDATE',['M4.01','M4.02','M4.03'],['broker','stand-line','add',str(program_line)],expected='ok')
 new_service_pids=service_pids()
 lifecycle_changed=len(old_service_pids)>=3 and len(new_service_pids)>=3 and not any(pid_alive(pid) for pid in old_service_pids) and not set(old_service_pids)&set(new_service_pids) and hashlib.sha256(P(service_path).read_bytes()).hexdigest()==hashlib.sha256(holder_v2).hexdigest()
 record(dict(phase='result',id='SERVICE-TIMER-CODE-CHANGE',variants=['M4.01','M4.02','M4.03'],passed=lifecycle_changed,old_pids=old_service_pids,new_pids=new_service_pids))
 if not lifecycle_changed:failed.append('SERVICE-TIMER-CODE-CHANGE')
 session('TIMER-LIFECYCLE-REMOVE',['M4.03'],['broker','stand-line','remove','round2-timer'],expected='ok')
 removal_pids=service_pids()
 session('SERVICE-LIFECYCLE-REMOVE',['M4.01','M4.02'],['broker','stand-line','remove','round2-service'],expected='ok')
 lifecycle_removed=len(removal_pids)>=3 and not any(pid_alive(pid) for pid in removal_pids)
 record(dict(phase='assert',id='SERVICE-LIFECYCLE-REMOVED',variants=['M4.01','M4.02'],passed=lifecycle_removed,pids=removal_pids))
 if not lifecycle_removed:failed.append('SERVICE-LIFECYCLE-REMOVED')
 session('SERVICE-PROGRAM-REMOVE',['M4.02'],['broker','stand-line','remove',service_program_id],expected='ok')

 removed_profiles={x.split('\t')[2] for x in P('/etc/stand/launch.tsv').read_text().splitlines() if x.split('\t')[0].startswith('/opt/stand/pkgs/round2/')}
 record(dict(phase='expected',id='REMOVE-PROFILES',variants=['M4.02'],expected='all removed profile names absent from kernel active profile list',profiles=sorted(removed_profiles)))
 holder_log=(WORK/'holder.log').open('w+')
 holder_cmd=['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-session','-c','run\t'+holder]
 record(dict(phase='expected',id='REMOVE-HOLDER',variants=['M4.01'],command=holder_cmd,expected='running parent and descendant revoked before remove completes'))
 process=subprocess.Popen(holder_cmd,stdout=holder_log,stderr=subprocess.STDOUT,text=True)
 deadline=time.monotonic()+10;holders=[]
 while time.monotonic()<deadline:
  holder_log.seek(0);holder_text=holder_log.read();holders=[int(x) for x in re.findall(r'HOLDER ([0-9]+)',holder_text)]
  if len(holders)>=2:break
  time.sleep(.05)
 session('REMOVE',[],['broker','stand-line','remove','round2'],expected='ok')
 try:process.wait(timeout=10)
 except subprocess.TimeoutExpired:process.kill();failed.append('REMOVE-HOLDER-TIMEOUT')
 def alive(pid):
  try:return P('/proc',str(pid),'stat').read_text().split(') ',1)[1][0]!='Z'
  except FileNotFoundError:return False
 gone=len(holders)>=2 and not any(alive(pid) for pid in holders)
 record(dict(phase='result',id='REMOVE-HOLDER',variants=['M4.01'],passed=gone,pids=holders,output=holder_text))
 if not gone:
  failed.append('REMOVE-HOLDER')
  for pid in holders:
   if alive(pid):os.kill(pid,9)
 holder_log.close()
 active_profiles={x.rsplit(' (',1)[0] for x in P('/sys/kernel/security/apparmor/profiles').read_text().splitlines()}
 remaining=sorted(removed_profiles & active_profiles)
 record(dict(phase='result',id='REMOVE-PROFILES',variants=['M4.02'],passed=bool(removed_profiles) and not remaining,remaining=remaining))
 if not removed_profiles or remaining:failed.append('REMOVE-PROFILES')
 session('REMOVED-SCRIPT' ,['M4.02'],['run',positive]);session('REMOVED-NATIVE',['M4.02'],['run',native])
 session('REMOVED-COPY',['M4.02'],['run',str(WORK/'old-copy')])
 run('VERIFY',[],['/usr/local/bin/stand-verify'],expected='ok')
 record(dict(phase='summary',passed=not failed,failures=failed))
 return bool(failed)
if __name__=='__main__':sys.exit(main())
