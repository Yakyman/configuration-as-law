#!/usr/bin/python3 -B
"""Version 4 shell observations; failures of the boundary are kept as failures."""
import base64, hashlib, http.server, json, os, pathlib, shlex, subprocess, sys, threading, time
P=pathlib.Path
results=[]
def emit(**r):
    r['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    print(json.dumps(r,sort_keys=True),flush=True)
def call(ident, variants, command, expected, check, data=None, requirement=True):
    emit(phase='expected',id=ident,variants=variants,command=command,expected=expected)
    try:
        p=subprocess.run(['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-shell','-c',command],input=data,capture_output=True,text=True,timeout=180)
        code,out,err=p.returncode,p.stdout,p.stderr
    except subprocess.TimeoutExpired:
        code,out,err=124,'','timeout'
    good=bool(check(code,out,err))
    row=dict(id=ident,variants=variants,passed=good,requirement=requirement,exit=code,output=out,stderr=err)
    results.append(row);emit(phase='result',**row)
    return row
def ok(code,out,err):return code==0
def deny(code,out,err):return code!=0
def exact(text):return lambda c,o,e:c==0 and text in o
def root(args):return subprocess.run(args,capture_output=True,text=True,timeout=300)
def saved():
    return json.loads(P('/var/lib/stand/last-success.json').read_text())
def lines():return [json.loads(x) for x in P('/var/lib/stand/current/machine.jsonl').read_text().splitlines()]

def main():
    if '--after' in sys.argv:
        meta=json.loads(P('/var/lib/stand/v4-unsaved-check.json').read_text())
        token=meta['token']
        found=[]
        for p in P('/proc').glob('[0-9]*/cmdline'):
            try:
                if token.encode() in p.read_bytes():found.append(str(p))
            except OSError:pass
        same=saved()==meta['report']
        emit(phase='result',id='UNSAVED-AFTER-REBOOT',variants=['C4.5','C7.04'],passed=not found and same,
             matching_processes=found,report_unchanged=same,payload_sha256=meta['payload_sha256'])
        return int(bool(found) or not same)
    before=saved()
    call('SHELL-PROFILE',['C7.17'],'cat /proc/self/attr/current','ordinary child inherits enforcing shell domain',exact('stand-shell (enforce)'))
    call('FREE-COMMANDS',['C7.03','C7.17','C8.03','C8.06'],
         '''message='two words'; f() { printf '%s\\n' "$1"; }; f "$message" | tr a-z A-Z > document.txt; cat < document.txt''',
         'free quoting, arguments, function, pipeline and both redirections; document output',exact('TWO WORDS'))
    call('DOCUMENT-EDIT',['C7.10'],"printf '1c\\nEdited document\\n.\\nw\\nq\\n' | ed -s document.txt; cat document.txt",'document editor saves exact new text',exact('Edited document'))
    call('BROWSER',['C4.3'],"printf '<html><body>Browser document</body></html>\\n' > page.html; w3m -dump -config /etc/stand/w3m.conf page.html",'browser renders ordinary material',exact('Browser document'))
    emit(phase='result',id='MATERIAL-NO-LINE',variants=['C7.17'],passed=saved()==before,report_unchanged=saved()==before)
    # A declaration is the input to installation; the user command is never logged as one.
    payload=b'#!/usr/bin/bash\nprintf "PERSONAL_SCRIPT_OK:%s\\n" "$1"\n'
    path='/opt/stand/pkgs/v4-personal/bin/personal'
    row={'id':'v4-personal','type':'code','managed':True,'version':'1','source':'builder:personal-script',
         'entrypoints':[{'path':path,'interpreter':'/usr/bin/bash'}],
         'files':[{'path':path,'kind':'file','mode':493,'uid':0,'gid':0,'sha256':hashlib.sha256(payload).hexdigest(),'content_b64':base64.b64encode(payload).decode()}]}
    P('/tmp/v4-personal.json').write_text(json.dumps(row))
    call('PERSONAL-INSTALL',['C7.01','C7.02'], 'stand-pkg install /tmp/v4-personal.json','record exact own script and interpreter, then apply',exact('SUCCESS '))
    call('PERSONAL-RUN',['C7.01','C7.02','C7.17'],path+" 'ordinary argument'",'recorded personal script accepts an argument in the command shell',exact('PERSONAL_SCRIPT_OK:ordinary argument'))
    emit(phase='result',id='PERSONAL-COVERAGE',variants=['C7.01','C7.02'],passed=row in lines(),line=row,last_success=saved())
    call('NATIVE-COPY',['C4.1','C4.2','C5.3'], 'cp /usr/bin/true ./unrecorded-native; chmod +x ./unrecorded-native; ./unrecorded-native', 'unrecorded copied native file cannot execute',deny)
    call('NATIVE-LOADER',['C4.4','C7.13'], '/lib64/ld-linux-x86-64.so.2 ./unrecorded-native','direct loader cannot map saved unrecorded native code',deny)
    call('NATIVE-HELPER',['C7.11'], "find . -maxdepth 0 -exec ./unrecorded-native ';'", 'helper cannot execute saved native file; inspect effect/diagnostic',lambda c,o,e:'Permission denied' in e)
    call('RECORDED-REPLACE',['C5.4'], 'cp ./unrecorded-native '+path,'ordinary copy cannot overwrite recorded required bytes',deny)
    call('SAVED-SCRIPT',['C4.4','C7.01','C7.05','C7.08'],
         "printf 'printf SAVED_CODE_RAN\\n' > saved.txt; bash saved.txt",'required boundary: saved unrecorded script must not execute',lambda c,o,e:'SAVED_CODE_RAN' not in o,requirement=False)
    call('SAVED-PIPE',['C7.04','C7.05','C7.24'], 'cat saved.txt | bash','required boundary: piping a saved instruction file must not remove its need for coverage',lambda c,o,e:'SAVED_CODE_RAN' not in o,requirement=False)
    call('SAVED-SOURCE',['C7.07','C8.01'], 'source saved.txt','required boundary: source must not execute unrecorded saved code',lambda c,o,e:'SAVED_CODE_RAN' not in o,requirement=False)
    call('STARTUP-ENV',['C8.02'], 'BASH_ENV="$HOME/saved.txt" bash -c :','required boundary: environment-selected saved startup code cannot execute',lambda c,o,e:'SAVED_CODE_RAN' not in o,requirement=False)
    call('PYTHON-IMPORT',['C2.6','C7.09'], "printf 'print(\"IMPORTED_UNRECORDED\")\\n' > loose_module.py; python3 -B -c 'import loose_module'",'required boundary: unrecorded module cannot import',lambda c,o,e:'IMPORTED_UNRECORDED' not in o,requirement=False)
    call('PICKLE-CODE',['C7.20'], '''python3 -B -c 'import pickle; p=b"cbuiltins\\nprint\\n(S\\x27PICKLE_EXECUTED\\x27\\ntR."; open("serialized","wb").write(p); pickle.load(open("serialized","rb"))' ''','required boundary: serialized saved code must not execute',lambda c,o,e:'PICKLE_EXECUTED' not in o,requirement=False)
    call('USER-SERVICE',['C6.1','C6.2'], "mkdir -p .config/systemd/user; printf '[Service]\\nExecStart=/usr/bin/sleep 300\\n[Install]\\nWantedBy=default.target\\n' > .config/systemd/user/unrecorded.service; systemctl --user enable unrecorded.service", 'unrecorded service is not enabled',deny)
    p=root(['/usr/bin/systemctl','is-enabled','unrecorded.service'])
    emit(phase='result',id='USER-SERVICE-STATE',variants=['C6.1','C6.2'],passed=p.stdout.strip() not in ('enabled','enabled-runtime'),enabled=p.stdout.strip())
    call('TRANSIENT-JOB',['C6.3'], 'systemd-run --user --unit=unrecorded /usr/bin/sleep 300','unrecorded transient job is refused',deny)
    call('CRON-JOB',['C6.4'], "printf '@reboot /usr/bin/sleep 300\\n' | crontab -",'unrecorded cron registration is refused',deny)
    call('RAW-SETTINGS',['C10.1','C10.2'], "printf x >> /etc/passwd",'ordinary direct write to system account state is refused',deny)
    call('USER-NAMESPACE',['C9.2','C9.5'], "unshare -Urnm sh -c 'mount -t tmpfs tmpfs /tmp; cp /usr/bin/true /tmp/native; /tmp/native; printf NAMESPACE_ESCAPE'",'new namespace cannot gain mount/execution authority beyond the shell domain',lambda c,o,e:'NAMESPACE_ESCAPE' not in o)
    call('OCI-ALTERNATE',['C9.2','C9.3','C9.5'], "podman run --privileged --userns=keep-id -v /home/stand:/work local:mutable /work/unrecorded-native",'unrecorded privileged mutable container configuration is refused',deny)
    call('OCI-WRITABLE-OVERLAY',['C9.3','C9.4'], "podman commit unrecorded local:mutable",'mutable container commit does not install unrecorded image',deny)
    call('PERSONAL-REMOVE',['C7.01'], 'stand-pkg remove v4-personal','remove declared own script through built-in tool',exact('SUCCESS '))
    # Actual execution without saving: HTTP response exists only in fixture memory
    # and a pipe. A fresh runtime nonce excludes the installed test source itself.
    token='V4_UNSAVED_'+os.urandom(12).hex()
    code=('printf "UNSAVED_EXECUTED\\n"; exec -a '+token+' /usr/bin/sleep 600\n').encode()
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200);self.send_header('Content-Length',str(len(code)));self.end_headers();self.wfile.write(code)
        def log_message(self,*args):pass
    server=http.server.HTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    command='curl -fsS http://127.0.0.1:'+str(server.server_port)+'/runtime | bash'
    emit(phase='expected',id='UNSAVED-EXECUTE',variants=['C4.5','C7.04'],command=command,expected='response executes from pipe; process lives; no payload file; reboot kills all contribution')
    p=subprocess.Popen(['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-shell','-c',command],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    import select
    ready=select.select([p.stdout],[],[],15)[0]
    output=p.stdout.readline() if ready else ''
    server.shutdown();server.server_close();thread.join()
    processes=[]
    for q in P('/proc').glob('[0-9]*/cmdline'):
        try:
            if token.encode() in q.read_bytes():processes.append(str(q))
        except OSError:pass
    matches=[]
    # Search writable stores for exact response bytes while the response is alive.
    for folder in ('/home/stand','/tmp','/var/tmp','/dev/shm','/var/lib/stand'):
        for q in P(folder).rglob('*'):
            try:
                if q.is_file() and not q.is_symlink() and q.stat().st_size==len(code) and q.read_bytes()==code:matches.append(str(q))
            except OSError:pass
    record={'token':token,'payload_sha256':hashlib.sha256(code).hexdigest(),'report':saved()}
    P('/var/lib/stand/v4-unsaved-check.json').write_text(json.dumps(record))
    emit(phase='result',id='UNSAVED-EXECUTE',variants=['C4.5','C7.04'],passed=bool(processes) and output=='UNSAVED_EXECUTED\n' and not matches,
         output=output,processes=processes,payload_files=matches,payload_bytes=len(code),payload_sha256=record['payload_sha256'])
    # The observation parent exits; the managed guest is rebooted by the driver.
    p.stdout.close();p.stderr.close()
    emit(phase='summary',implemented_checks_passed=all(x['passed'] for x in results if x['requirement']),
         boundary_failures=[x['id'] for x in results if not x['passed']],hypothesis_outcome='?')
    return int(any(not x['passed'] for x in results if x['requirement']) or not processes or bool(matches))

if __name__=='__main__':sys.exit(main())
