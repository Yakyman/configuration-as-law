#!/usr/bin/python3 -B
"""Supplementary fresh-guest observations of actual Bash file/build routes.

Send this frozen test payload on the laboratory root connection's stdin.
It is a test controller, not an installed system component.
"""
import hashlib, http.server, io, json, os, pathlib, shlex, shutil, subprocess, tarfile, threading, time
P=pathlib.Path
work=P('/home/stand/v4-direct')
results=[]
def emit(**value):
    value['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    print(json.dumps(value,sort_keys=True),flush=True)
def state():
    return {'declaration':hashlib.sha256(P('/var/lib/stand/current/machine.jsonl').read_bytes()).hexdigest(),
            'report':hashlib.sha256(P('/var/lib/stand/last-success.json').read_bytes()).hexdigest()}
def run(ident,variants,command,marker=None,expect='deny',files=(),tools=(),hashes=None,links=None):
    missing=[tool for tool in tools if not P(tool).is_file()]
    if missing:
        row=dict(phase='unavailable',id=ident,variants=variants,passed=None,missing=missing)
        results.append(row);emit(**row);return row
    before=state()
    emit(phase='expected',id=ident,variants=variants,command=command,
         expected='saved unrecorded code cannot execute' if expect=='deny' else 'ordinary work succeeds',
         marker=marker,before=before)
    try:
        r=subprocess.run(['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-shell','-c',
                          'cd '+shlex.quote(str(work))+'; '+command],capture_output=True,text=True,timeout=180)
        concrete=[]
        for name in files:
            p=work/name
            concrete.append({'path':str(p),'exists':p.exists(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None})
        same=state()==before
        ran=marker is not None and marker in r.stdout
        policy_diagnostic=any(x in r.stderr.lower() for x in ('permission denied','operation not permitted','failed to map segment'))
        exact=all((work/name).is_file() and hashlib.sha256((work/name).read_bytes()).hexdigest()==want for name,want in (hashes or {}).items())
        exact=exact and all((work/name).is_symlink() and os.readlink(work/name)==want for name,want in (links or {}).items())
        passed=same and exact and ((not ran and r.returncode!=0 and policy_diagnostic) if expect=='deny' else (r.returncode==0 and (marker is None or ran)))
        row=dict(phase='result',id=ident,variants=variants,passed=passed,
                 assertion_kind='boundary' if expect=='deny' else 'ordinary_work',
                 exit=r.returncode,stdout=r.stdout,stderr=r.stderr,marker_observed=ran,
                 declaration_and_report_unchanged=same,files=concrete,required_hashes=hashes,
                 required_links=links,fixture_exact=exact,policy_diagnostic=policy_diagnostic)
    except Exception as error:
        row=dict(phase='result',id=ident,variants=variants,passed=False,error=str(error))
    results.append(row);emit(**row)
    return row
def write(name,data,mode=0o644):
    p=work/name;p.write_bytes(data);p.chmod(mode);os.chown(p,1000,1000)
    emit(phase='fixture',path=str(p),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
def main():
    if work.exists():raise RuntimeError('fresh guest required')
    work.mkdir();os.chown(work,1000,1000)
    # The language/build semantics are documented. Only the installed policy
    # integration is observed here; this is not a language-semantics experiment.
    emit(phase='sources',references=[
        {'url':'https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html','quote':'Compilation can involve up to four stages: preprocessing, compilation proper, assembly and linking, always in that order.'},
        {'url':'https://docs.python.org/3/library/functions.html#exec','topic':'exec evaluates supplied Python code'},
        {'url':'https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html','topic':'typed commands and evaluation of supplied text'}],
        unknown='Whether this rebuilt image mediates the concrete saved output and interpreter routes under actual Bash')
    # A real HTTP save and a nested archive give provenance/effect evidence in
    # addition to the simpler copied-ELF attempt in the installed shell suite.
    native=P('/usr/bin/true').read_bytes()
    inner=io.BytesIO()
    with tarfile.open(fileobj=inner,mode='w') as bundle:
        entry=tarfile.TarInfo('renamed.payload');entry.size=len(native);entry.mode=0o755
        bundle.addfile(entry,io.BytesIO(native))
    outer=io.BytesIO()
    with tarfile.open(fileobj=outer,mode='w') as bundle:
        data=inner.getvalue();entry=tarfile.TarInfo('inner.tar');entry.size=len(data)
        bundle.addfile(entry,io.BytesIO(data))
    responses={'/native':native,'/nested':outer.getvalue()}
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            data=responses.get(self.path)
            if data is None:self.send_error(404);return
            self.send_response(200);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        def log_message(self,*args):pass
    server=http.server.HTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base='http://127.0.0.1:'+str(server.server_port)
    try:
        h=hashlib.sha256(native).hexdigest()
        ready=run('DIRECT-HTTP-SAVE',['C4.1','C4.3'],
            'curl -fsS '+base+'/native -o downloaded && chmod +x downloaded',expect='work',
            files=['downloaded'],tools=['/usr/bin/curl','/usr/bin/chmod'],hashes={'downloaded':h})
        if ready.get('passed'):
            run('DIRECT-HTTP-NATIVE',['C4.1','C4.3'],'./downloaded && printf HTTP_NATIVE_RAN',
                'HTTP_NATIVE_RAN',files=['downloaded'],hashes={'downloaded':h})
        ready=run('DIRECT-NESTED-EXTRACT',['C4.2'],
            'curl -fsS '+base+'/nested -o outer.tar && tar xf outer.tar && tar xf inner.tar',expect='work',
            files=['outer.tar','inner.tar','renamed.payload'],tools=['/usr/bin/curl','/usr/bin/tar'],hashes={'renamed.payload':h})
        if ready.get('passed'):
            run('DIRECT-NESTED-ARCHIVE',['C4.2'],'./renamed.payload && printf ARCHIVE_RAN',
                'ARCHIVE_RAN',files=['renamed.payload'],hashes={'renamed.payload':h})
    finally:server.shutdown();server.server_close();thread.join()
    # A compiler is ordinary work; it may create material output. Running a
    # saved executable output requires coverage. Separating those assertions
    # prevents a compiler denial from masquerading as output admission.
    write('source.c',b'#include <stdio.h>\nint main(void){puts("COMPILED_OUTPUT_RAN");return 0;}\n')
    build=run('DIRECT-COMPILE',['C5.1','C5.2'],'gcc source.c -o built',expect='work',files=['built'],tools=['/usr/bin/gcc'])
    if build.get('passed') and (work/'built').is_file():
        run('DIRECT-COMPILED-RUN',['C5.1','C5.2'],'./built','COMPILED_OUTPUT_RAN',files=['built'])
        ready=run('DIRECT-PREFIX-SETUP',['C5.3'],'mkdir -p prefix/bin && cp built prefix/bin/probe && ln -s probe prefix/bin/linked',expect='work',
                  files=['prefix/bin/probe'],tools=['/usr/bin/mkdir','/usr/bin/cp','/usr/bin/ln'],
                  hashes={'prefix/bin/probe':hashlib.sha256((work/'built').read_bytes()).hexdigest()},links={'prefix/bin/linked':'probe'})
        if ready.get('passed'):
            run('DIRECT-PREFIX-PATH',['C5.3'],'PATH="$PWD/prefix/bin:$PATH" linked','COMPILED_OUTPUT_RAN',files=['prefix/bin/probe'])
    else:emit(phase='unavailable',id='DIRECT-COMPILED-RUN',variants=['C5.1','C5.2','C5.3'],reason='no output produced; compiler denial is not a saved-output admission result')
    write('plugin.c',b'#include <stdio.h>\nint plugin_is_GPL_compatible;\nint plugin_init(void*a,void*b){puts("COMPILER_PLUGIN_RAN");return 0;}\n')
    ready=run('DIRECT-PLUGIN-BUILD',['C5.5'],'gcc -shared -fPIC plugin.c -o plugin.so',expect='work',files=['plugin.so'],tools=['/usr/bin/gcc'])
    if ready.get('passed') and (work/'plugin.so').is_file():
        run('DIRECT-COMPILER-PLUGIN',['C5.5'],'gcc -fplugin="$PWD/plugin.so" -c source.c -o plugin-output.o','COMPILER_PLUGIN_RAN',files=['plugin.so','plugin-output.o'])
    else:emit(phase='unavailable',id='DIRECT-COMPILER-PLUGIN',variants=['C5.5'],reason='shared plugin fixture could not be built')
    write('saved.sh',b'#!/usr/bin/bash\nprintf SAVED_DIRECT_RAN\n',0o755)
    run('DIRECT-SHEBANG',['C7.02'],'./saved.sh','SAVED_DIRECT_RAN',files=['saved.sh'],tools=['/usr/bin/bash'])
    run('DIRECT-REDIRECT-STDIN',['C7.05'],'bash < saved.sh','SAVED_DIRECT_RAN',tools=['/usr/bin/bash'])
    run('DIRECT-PROC-FD',['C7.05'],'exec 3<saved.sh; bash /proc/self/fd/3','SAVED_DIRECT_RAN',tools=['/usr/bin/bash'])
    write('saved.py',b'print("READ_EXEC_RAN")\n')
    run('DIRECT-READ-EXEC',['C7.08'],"python3 -B -c 'exec(open(\"saved.py\").read())'",'READ_EXEC_RAN',tools=['/usr/bin/python3'])
    write('saved.awk',b'BEGIN { print "AWK_FILE_RAN" }\n')
    run('DIRECT-AWK-FILE',['C7.10'],'awk -f saved.awk','AWK_FILE_RAN',tools=['/usr/bin/awk'])
    run('DIRECT-SCRIPT-HELPER',['C7.11'],"find . -maxdepth 0 -exec bash saved.sh ';'",'SAVED_DIRECT_RAN',tools=['/usr/bin/find','/usr/bin/bash'])
    # Typed own-rights definitions are actions. Saving and then sourcing them
    # is a different input provenance route and remains a boundary assertion.
    run('DIRECT-RUNTIME-ALIAS',['C8.06'],"bash -O expand_aliases -c $'alias v4say=\"printf RUNTIME_ALIAS_OK\"\\nv4say'",'RUNTIME_ALIAS_OK',expect='work',tools=['/usr/bin/bash'])
    shutil.rmtree(work)
    emit(phase='cleanup',fixture_directory_absent=not work.exists())
    emit(phase='summary',failures=[r['id'] for r in results if r['passed'] is False],unavailable=[r['id'] for r in results if r['passed'] is None],
         result_count=len(results),hypothesis_outcome='?',
         exit_semantics='Observation controller completed; failed property/ordinary-work rows remain failures')
    return 0
if __name__=='__main__':raise SystemExit(main())
