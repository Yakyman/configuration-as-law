#!/usr/bin/python3
"""Ordinary work, import/build and user jobs on a fresh BC4 guest."""
import base64,hashlib,http.server,json,os,pathlib,subprocess,sys,threading,time
P=pathlib.Path;failures=[]
def record(**r):r['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());print(json.dumps(r,sort_keys=True),flush=True)
def expect(ident,expected,**kw):record(phase='expected',id=ident,expected=expected,**kw)
def result(ident,ok,**kw):
    record(phase='result',id=ident,passed=bool(ok),**kw)
    if not ok:failures.append(ident)
def command(ident,args,success=True,contains=None,data=None):
    expect(ident,'successful recorded operation' if success else 'refusal',command=list(map(str,args)))
    p=subprocess.run(list(map(str,args)),input=data,capture_output=True,timeout=600)
    out=p.stdout.decode(errors='replace');err=p.stderr.decode(errors='replace')
    result(ident,(p.returncode==0 if success else p.returncode!=0) and (contains is None or contains in out),rc=p.returncode,output=out[-5000:],stderr=err[-2000:])
    return p
def session(ident,*fields,**kw):return command(ident,['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-session','-c','\t'.join(map(str,fields))],**kw)
def document(name,b):return session('WRITE-'+name,'run','/usr/bin/dd','/home/stand/'+name,data=b if isinstance(b,bytes) else b.encode())
def spec(name,obj):document(name,json.dumps(obj)+'\n');return '/home/stand/'+name

dev=P('/usr/local/share/stand/dev');row=json.loads((dev/'worker-1.json').read_text());payload=base64.b64decode(row['files'][0]['content_b64'])
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):self.send_response(200);self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
    def log_message(self,*args):pass
expect('DOWNLOAD','ordinary curl receives exact development bytes from temporary external fixture server; bytes remain inert')
server=http.server.HTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
try:
    p=subprocess.run(['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-session','-c','run\t/usr/bin/curl\thttp://127.0.0.1:'+str(server.server_port)+'/development'],capture_output=True,timeout=30)
    result('DOWNLOAD',p.returncode==0 and p.stdout==payload,rc=p.returncode,bytes=len(p.stdout),sha256=hashlib.sha256(p.stdout).hexdigest())
finally:server.shutdown();server.server_close();thread.join()
document('downloaded-program',p.stdout)
session('DOWNLOAD-INERT','run','/home/stand/downloaded-program',success=False)
import_spec=spec('download.json',{'id':'downloaded','version':'1','source':'builder-download:development-worker','sha256':hashlib.sha256(payload).hexdigest(),'path':'/home/stand/downloaded-program'})
session('DOWNLOAD-IMPORT','broker','stand-import','install',import_spec)
session('DOWNLOAD-RUN','run','/opt/stand/pkgs/downloaded/bin/program',contains='development-version-1')
session('DOWNLOAD-UNRECORDED-COPY','run','/home/stand/downloaded-program',success=False)
source=b'#include <stdio.h>\nint main(void){puts("BUILT_SOURCE_OK");return 0;}\n'
document('source.c',source)
source_spec=spec('source.json',{'id':'source-example','version':'1','source':'builder-source:ordinary-c','sha256':hashlib.sha256(source).hexdigest(),'path':'/home/stand/source.c'})
session('SOURCE-RECORD','broker','stand-import','source',source_spec)
session('SOURCE-BUILD','broker','stand-build','build','source:source-example',contains='BUILT INERT')
session('BUILD-INERT','run','/home/stand/source-example.built',success=False)
session('BUILD-IMPORT','broker','stand-import','install','/home/stand/source-example.built.json')
session('BUILD-RUN','run','/opt/stand/pkgs/source-example-built/bin/program',contains='BUILT_SOURCE_OK')
session('UNRECORDED-BUILD','broker','stand-build','build','source:missing',success=False)
session('MUTABLE-OUTPUT-OVERWRITE','run','/usr/bin/cp','/home/stand/source-example.built','/opt/stand/pkgs/source-example-built/bin/program',success=False)
session('USER-SERVICE-PROGRAM','broker','stand-pkg','install',dev/'worker-1.json')
session('USER-SERVICE','broker','systemctl','--user','add',dev/'service.json')
text='[Unit]\nDescription=Declared user timer\n[Timer]\nOnBootSec=1h\nOnUnitActiveSec=1h\nUnit=stand-development.service\nPersistent=false\n[Install]\nWantedBy=timers.target\n'
timer={'id':'round4-user-timer','type':'timer','managed':True,'unit':'stand-user-example.timer','enabled':'enabled','active':True,'unit_text':text,'unit_sha256':hashlib.sha256(text.encode()).hexdigest()}
timerfile=spec('timer.json',timer)
session('USER-TIMER','broker','systemd-run','--user','add-timer',timerfile)
schedule=spec('schedule.json',{'id':'scheduled-example','command':'/opt/stand/pkgs/source-example-built/bin/program','on_boot':'1s','interval':'1min'})
session('SCHEDULE-COMMAND','broker','crontab','add',schedule)
expect('SCHEDULE-EXECUTED','timer actually executes recorded command under user identity')
deadline=time.monotonic()+5;output=''
while time.monotonic()<deadline:
    p=subprocess.run(['/usr/bin/journalctl','-u','stand-scheduled-example.service','--no-pager','-o','cat'],capture_output=True,text=True);output=p.stdout
    if 'BUILT_SOURCE_OK' in output:break
    time.sleep(.2)
result('SCHEDULE-EXECUTED','BUILT_SOURCE_OK' in output,output=output)
for name,args in [('systemctl',['--user','enable','unrecorded.service']),('systemd-run',['--user','/home/stand/unrecorded']),('crontab',['-'])]:
    session('JOB-REFUSE-'+name,'broker',name,*args,success=False)
    command('JOB-ROOT-REFUSE-'+name,['/usr/local/bin/'+name,*args],success=False)
document('ordinary-document.txt','First document\n')
session('DOCUMENT-EDIT','run','/usr/bin/red','ordinary-document.txt',data=b'1c\nEdited document\n.\nw\nq\n')
session('DOCUMENT-READ','run','/usr/bin/cat','/home/stand/ordinary-document.txt',contains='Edited document')
session('EDITOR-SHELL-REFUSED','run','/usr/bin/red','ordinary-document.txt',data=b'!id\nq\n',success=False)
session('EDITOR-COMMAND-READ-REFUSED','run','/usr/bin/red','ordinary-document.txt',data=b'r !id\nq\n',success=False)
document('ordinary-page.html','<html><body>Ordinary browser works</body></html>\n')
session('BROWSER','run','/usr/bin/w3m','/home/stand/ordinary-page.html',contains='Ordinary browser works')
session('WIFI-SAVED','broker','nmcli','add',dev/'wifi.json')
session('BLUETOOTH-PREPARED','broker','bluetoothctl','add',dev/'bluetooth.json')
record(phase='hardware',wifi='not tested on hardware',bluetooth='not tested on hardware',paired=False)
command('ORDINARY-VERIFY',['/usr/local/bin/stand-verify'])
examples=P('/var/lib/stand/channel-examples');examples.mkdir(exist_ok=True)
ordinary_rows=[json.loads(line) for line in P('/var/lib/stand/current/machine.jsonl').read_text().splitlines()]
(examples/'ordinary.jsonl').write_text(''.join(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n' for r in ordinary_rows if r.get('managed')))
for ident in ['schedule:scheduled-example:timer','schedule:scheduled-example:service','round4-user-timer','dev-service','dev-worker','import:source-example-built','source:source-example','import:downloaded','dev-wifi','dev-bluetooth']:
    session('REMOVE-'+ident,'broker','stand-line','remove',ident)
session('REMOVED-DOWNLOAD','run','/opt/stand/pkgs/downloaded/bin/program',success=False)
session('REMOVED-BUILD','run','/home/stand/source-example.built',success=False)
command('FINAL-VERIFY',['/usr/local/bin/stand-verify'])
for profile in ('stand-format-parser','stand-build'):
    command('POLICY-DRIFT-'+profile,['/usr/sbin/apparmor_parser','-r','-T','-C','/etc/apparmor.d/'+profile])
    command('POLICY-DRIFT-DETECTED-'+profile,['/usr/local/bin/stand-verify'],success=False,contains='code-boundary\trule\tFAIL')
    command('POLICY-RESTORED-'+profile,['/usr/local/bin/stand-apply','/var/lib/stand/current'])
command('CHANNEL-POLICY-FINAL-VERIFY',['/usr/local/bin/stand-verify'])
record(phase='summary',passed=not failures,failures=failures)
sys.exit(bool(failures))
