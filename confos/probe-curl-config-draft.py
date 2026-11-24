#!/usr/bin/python3
"""Compare private curl CLI and run unconfined loopback controls only."""
import hashlib
import http.server
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading

root=Path.cwd(); work=root/'interpreter-inputs/curl-config-draft'
assert Path('/proc/self/attr/current').read_text().strip() == 'unconfined'
lib=work/'dependencies/usr/lib/x86_64-linux-gnu'
paths={'original':work/'original-package/usr/bin/curl','candidate':work/'candidate/curl'}
records={}
for label,path in paths.items():
    dynamic=subprocess.check_output(['readelf','-d',str(path)],text=True)
    symbols=subprocess.check_output(['readelf','--dyn-syms','--wide',str(path)],text=True)
    versions=subprocess.check_output(['readelf','-V',str(path)],text=True)
    records[label]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'needed':sorted(re.findall(r'\(NEEDED\).*\[(.*?)\]',dynamic)),
        'rpath':re.findall(r'\((?:RPATH|RUNPATH)\).*\[(.*?)\]',dynamic),
        'exports':sorted(line.split()[-1] for line in symbols.splitlines()
            if len(line.split())>=8 and line.split()[4] in ('GLOBAL','WEAK') and line.split()[6]!='UND'),
        'versions':sorted(set(re.findall(r'Name: (\S+)',versions))),
        'version':subprocess.check_output([str(path),'--version'],env={**os.environ,'LD_LIBRARY_PATH':str(lib)},text=True)}
assert records['original']['version']==records['candidate']['version'], records
assert records['original']['needed']==records['candidate']['needed'], records
assert records['candidate']['rpath']==[], records
assert records['original']['exports']==records['candidate']['exports'], records
assert not set(records['candidate']['versions'])-set(records['original']['versions']),records

class Handler(http.server.BaseHTTPRequestHandler):
    received=[]
    def do_GET(self):
        length=int(self.headers.get('Content-Length','0'))
        self.received.append({'agent':self.headers.get('User-Agent'),
                              'custom':self.headers.get('X-Draft'),
                              'body':self.rfile.read(length).decode()})
        self.send_response(200);self.end_headers();self.wfile.write(b'CURL-DRAFT-RESPONSE')
    do_POST=do_GET
    def log_message(self,*args): pass

server=http.server.HTTPServer(('127.0.0.1',0),Handler)
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
controls=[]
try:
    with tempfile.TemporaryDirectory(prefix='native-controls-',dir=work) as temporary:
        folder=Path(temporary);config=folder/'options';child=folder/'nested'
        data=folder/'data';data.write_text('CURL-DRAFT-BODY')
        headers=folder/'headers';headers.write_text('X-Draft: HEADER-DATA\n')
        config.write_text('user-agent = CONFIG-DRAFT\n')
        child.write_text('config = "'+str(config)+'"\n')
        (folder/'.curlrc').write_text('user-agent = AUTO-DRAFT\n')
        for label,path in paths.items():
            env={**os.environ,'LD_LIBRARY_PATH':str(lib),'HOME':str(folder),'CURL_HOME':str(folder),'LC_ALL':'C'}
            env.pop('XDG_CONFIG_HOME',None)
            def request(name,args,agent,input_data=None,fd=None,body='',custom=None):
                Handler.received.clear()
                result=subprocess.run([str(path),*args,'--noproxy','*','--max-time','5','-sS',
                    'http://127.0.0.1:'+str(server.server_port)+'/'],env=env,text=True,
                    input=input_data,stdin=fd,capture_output=True,timeout=8)
                assert result.returncode==0 and result.stdout=='CURL-DRAFT-RESPONSE', (name,result)
                assert Handler.received==[{'agent':agent,'custom':custom,'body':body}],(name,Handler.received)
                controls.append(label+':'+name)
            request('automatic',[], 'AUTO-DRAFT')
            request('explicit',['-q','--config',str(config)],'CONFIG-DRAFT')
            request('nested',['-q','--config',str(child)],'CONFIG-DRAFT')
            request('typed-pipe',['-q','--config','-'],'PIPE-DRAFT',input_data='user-agent = PIPE-DRAFT\n')
            with config.open() as stream:
                request('regular-stdin-unconfined',['-q','--config','-'],'CONFIG-DRAFT',fd=stream)
            request('typed-option',['-q','-A','TYPED-DRAFT'],'TYPED-DRAFT')
            request('transfer-data',['-q','-A','DATA-DRAFT','--data-binary','@'+str(data),
                    '-H','@'+str(headers)],'DATA-DRAFT',body='CURL-DRAFT-BODY',custom='HEADER-DATA')
finally:
    server.shutdown();server.server_close();thread.join()
(work/'comparison-controls.json').write_text(json.dumps({'comparison':records,'native_controls':controls,
    'limitation':'Unconfined native controls only; saved-config refusal and recorded guest positives pending'},indent=2)+'\n')
print('CURL_CONFIG_NATIVE_COMPARISON_AND_CONTROLS_PASS; no guest claim')
