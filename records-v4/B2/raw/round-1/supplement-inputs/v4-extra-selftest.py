#!/usr/bin/python3 -B
"""Host-controlled supplementary Round 1 integration tests, sent on stdin.

No packages installed and no recipe changes. Expected records precede commands.
Documented language semantics are not hypotheses: the tested unknown is their
integration with the installed ordinary-shell policy and declaration boundary.
"""
import base64,hashlib,json,os,pathlib,shlex,shutil,subprocess,sys,tempfile,time
sys.dont_write_bytecode=True
sys.path.insert(0,'/usr/local/lib/stand')
import stand
import codeboundary
stand.POLICY=codeboundary
P=pathlib.Path
results=[]
implementation_failures=[]

def emit(**data):
    data['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    print(json.dumps(data,sort_keys=True),flush=True)

def snapshot():
    report=stand.ROOT/'last-success.json'
    return {'generation':stand.current_dir().name,
            'declaration_sha256':hashlib.sha256((stand.current_dir()/'machine.jsonl').read_bytes()).hexdigest(),
            'report':json.loads(report.read_text())}

def ordinary(command,data=None):
    return subprocess.run(['/usr/sbin/runuser','-u','stand','--','/usr/local/bin/stand-shell','-c',command],
                          input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)

def unavailable(ident,variants,reason,**extra):
    emit(phase='availability',id=ident,variants=variants,status='UNTESTED',reason=reason,**extra)
    results.append({'id':ident,'status':'UNTESTED','variants':variants})

def check(ident,variants,command,expected,marker=None,kind='saved',data=None,files=(),expected_stdout=None):
    before=snapshot()
    emit(phase='expected',id=ident,variants=variants,command=command,expected=expected,
         kind=kind,before=before,expected_stdout=expected_stdout,stdin_sha256=hashlib.sha256(data).hexdigest() if data is not None else None)
    try:
        p=ordinary(command,data)
        out=p.stdout.decode(errors='replace');err=p.stderr.decode(errors='replace')
        after=snapshot();same=after==before
        evidence=[]
        for filename in files:
            path=P(filename)
            if path.is_file():
                evidence.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                                 'bytes':path.stat().st_size,'mode':oct(path.stat().st_mode&0o7777)})
        observed=bool(marker and marker in out+err)
        if kind=='saved':
            # Presence of the distinctive effect is a concrete bypass. Its
            # absence is only one attempted route, never general closure.
            passed=same and not observed
            status='BOUNDARY_FAILED' if observed else 'ATTEMPT_REFUSED' if p.returncode else 'NO_EFFECT_OBSERVED'
        elif kind=='positive':
            passed=same and p.returncode==0 and (observed if marker else True) and (expected_stdout is None or out==expected_stdout)
            status='POSITIVE' if passed else 'IMPLEMENTATION_FAILED'
            if not passed:implementation_failures.append(ident)
        elif kind=='setup':
            passed=None
            status='FIXTURE_READY' if p.returncode==0 and same else 'FIXTURE_UNAVAILABLE'
        else:
            # Runtime-only memory does not need its own declaration line.
            # Policy refusal is a limitation, not a passed hypothesis check.
            passed=None
            status='RUNTIME_EXECUTED' if observed and p.returncode==0 else 'RUNTIME_RESTRICTED_OR_UNAVAILABLE'
        result={'id':ident,'variants':variants,'status':status,'passed':passed,'rc':p.returncode,
                'stdout':out[-6000:],'stderr':err[-6000:],'effect_marker_observed':observed,
                'declaration_and_report_unchanged':same,'after':after,'files':evidence}
        results.append(result);emit(phase='boundary_result' if kind=='saved' else 'result',**result)
        if not same:implementation_failures.append(ident+'-unexpected-declaration-change')
        return p
    except Exception as error:
        result={'id':ident,'variants':variants,'status':'ERROR','passed':False,'error':str(error)}
        results.append(result);emit(phase='result',**result);implementation_failures.append(ident)
        return None

def py(source):return 'python3 -B -c '+shlex.quote(source)

def fixture(path,data,mode=0o600):
    data=data.encode() if isinstance(data,str) else data
    emit(phase='fixture_expected',path=str(path),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),mode=oct(mode))
    path.write_bytes(data);path.chmod(mode);os.chown(path,1000,1000)
    return str(path)

DOCS={
 'bash':'https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html',
 'functions':'https://www.gnu.org/software/bash/manual/bash.html',
 'memfd':'https://docs.python.org/3/library/os.html#os.memfd_create',
 'mmap':'https://docs.python.org/3/library/mmap.html',
 'process_memory':'https://www.kernel.org/pub/linux/docs/man-pages/book/man-pages-6.17.pdf',
 'binfmt':'https://www.kernel.org/doc/html/latest/admin-guide/binfmt-misc.html',
 'git_hooks':'https://git-scm.com/docs/githooks',
 'git_config':'https://git-scm.com/docs/git-config',
 'make':'https://www.gnu.org/software/make/manual/html_node/Execution.html',
 'browser':'https://w3m.sourceforge.net/MANUAL',
}

def main():
    if os.geteuid()!=0:raise RuntimeError('root controller required')
    emit(phase='documentation',sources=DOCS,
         established='Bash startup and exported functions, anonymous file descriptors, executable mapping flags, process-memory access, binfmt registration, Git hooks/aliases and make recipes are documented mechanisms.',
         unknown='Integration with this frozen image and its enforcing stand-shell profile; no probe is intended to rediscover language semantics.')
    initial_rows=stand.load(stand.current_dir());initial_ids={r['id'] for r in initial_rows}
    initial_bytes=(stand.current_dir()/'machine.jsonl').read_bytes()
    with tempfile.TemporaryDirectory(prefix='v4-extra-',dir='/tmp') as tmp:
        folder=P(tmp);folder.chmod(0o700);os.chown(folder,1000,1000)
        cd='cd '+shlex.quote(tmp)+' && '
        check('EXTRA-SHELL-DOMAIN',[],cd+'cat /proc/self/attr/current','Actual ordinary child must be in the enforcing shell profile.',marker='stand-shell (enforce)',kind='positive')
        # Interactive interpreter input is a typed action, no saved instruction
        # file. An explicit marker distinguishes its actual execution.
        check('REPL-TYPED',['C7.06'],cd+'python3 -B -i -q','Interactive stdin evaluates typed statements with no declaration change.',
              marker='REPL_TYPED_EXECUTED',kind='positive',data=b"print('REPL_TYPED_EXECUTED')\nexit()\n")
        rc=fixture(folder/'startup.rc','printf "SAVED_RC_EXECUTED\\n"\n')
        check('RC-STARTUP',['C8.01'],cd+'bash --rcfile '+shlex.quote(rc)+' -i -c :',
              'Saved unrecorded startup code must not run under the ordinary shell boundary.',marker='SAVED_RC_EXECUTED',files=[rc])
        check('EXPORTED-FUNCTION-SUBSTITUTION',['C8.03'],cd+"f() { printf FUNCTION_FROM_ENV; }; export -f f; bash -c 'printf \"%s\\n\" \"$(f)\"'",
              'Typed exported function and command substitution execute as the person action, without a saved instruction file.',marker='FUNCTION_FROM_ENV',kind='positive')
        # ed has saved command input, not a plugin API. Test the supported input
        # honestly and retain the untested executable-config/plugin distinction.
        edcommands=fixture(folder/'commands.ed','!printf "SAVED_EDITOR_COMMAND_EXECUTED\\n"\nq\n')
        if P('/usr/bin/ed').exists():
            check('EDITOR-SAVED-COMMANDS',['C7.10','C8.04'],cd+'ed -s < '+shlex.quote(edcommands),
                  'Saved editor commands must not execute unrecorded instruction text through a shell helper.',marker='SAVED_EDITOR_COMMAND_EXECUTED',files=[edcommands])
        unavailable('EDITOR-PLUGIN-MODELINE',['C8.04'],'Supplied ed saved-command input is tested separately; no supported plugin/modeline facility is supplied by that editor. No new editor is installed.')
        # A complete disposable project, only if the tools exist in the image.
        if P('/usr/bin/git').exists():
            prepared=check('GIT-PROJECT-PREPARE',['C7.12','C8.05'],cd+'git init -q . && git config user.name fixture && git config user.email <REDACTED>',
                  'Prepare ordinary disposable repository; preparation must succeed before hook claims.',kind='positive')
            if prepared is not None and prepared.returncode==0 and (folder/'.git/hooks').is_dir():
                hook=fixture(folder/'.git/hooks/pre-commit','#!/bin/sh\nprintf "GIT_HOOK_EXECUTED\\n"\n',0o700)
                check('GIT-HOOK',['C7.12'],cd+'git -c commit.gpgsign=false commit --allow-empty -qm fixture',
                      'Unrecorded saved executable hook must not run.',marker='GIT_HOOK_EXECUTED',files=[hook])
                alias_value='!printf GIT_ALIAS_EXECUTED'
                prepared_alias=check('GIT-LOCAL-ALIAS-SETUP',['C8.05'],
                      cd+'git config alias.extra '+shlex.quote(alias_value)+' && git config --get alias.extra',
                      'Store the disposable alias and require exact configuration readback before testing its consumer.',
                      kind='positive',expected_stdout=alias_value+'\n',files=[folder/'.git/config'])
                if prepared_alias is not None and prepared_alias.returncode==0 and prepared_alias.stdout==(alias_value+'\n').encode():
                    check('GIT-LOCAL-ALIAS',['C8.05'],cd+'git extra',
                          'Stored project-local executable alias must not execute outside declaration.',marker='GIT_ALIAS_EXECUTED',files=[folder/'.git/config'])
                else:unavailable('GIT-LOCAL-ALIAS',['C8.05'],'Alias configuration was not successfully written and read back exactly; consumer not invoked.')
                fixture(folder/'input.extra','material\n')
                fixture(folder/'.gitattributes','*.extra filter=extra\n')
                filter_value='printf GIT_FILTER_EXECUTED >&2; cat'
                prepared_filter=check('GIT-LOCAL-FILTER-SETUP',['C8.05'],
                      cd+'git config filter.extra.clean '+shlex.quote(filter_value)+' && git config --get filter.extra.clean',
                      'Store the disposable filter and require exact configuration readback before testing its consumer.',
                      kind='positive',expected_stdout=filter_value+'\n',files=[folder/'.git/config',folder/'.gitattributes'])
                if prepared_filter is not None and prepared_filter.returncode==0 and prepared_filter.stdout==(filter_value+'\n').encode():
                    check('GIT-LOCAL-FILTER',['C8.05'],cd+'git add input.extra',
                          'Stored project-local executable filter must not execute outside declaration.',marker='GIT_FILTER_EXECUTED',files=[folder/'.git/config',folder/'.gitattributes'])
                else:unavailable('GIT-LOCAL-FILTER',['C8.05'],'Filter configuration was not successfully written and read back exactly; consumer not invoked.')
            else:
                unavailable('GIT-HOOK-ALIAS-FILTER',['C7.12','C8.05'],'Installed Git could not prepare the disposable project under the shell profile.')
        else:
            unavailable('GIT-HOOK',['C7.12'],'Git is absent from the supplied image.',path='/usr/bin/git')
            unavailable('GIT-LOCAL-ALIAS-FILTER',['C8.05'],'Git is absent from the supplied image.',path='/usr/bin/git')
        if P('/usr/bin/make').exists():
            recipe=fixture(folder/'Makefile','all:\n\t@printf "MAKE_RECIPE_EXECUTED\\n"\n')
            check('MAKE-SAVED-RECIPE',['C8.05'],cd+'make -s -f Makefile',
                  'Stored executable recipe must not run without coverage.',marker='MAKE_RECIPE_EXECUTED',files=[recipe])
        else:unavailable('MAKE-SAVED-RECIPE',['C8.05'],'make is absent from the supplied image.',path='/usr/bin/make')
        # Produce a real audit/preload/FFI library, not an invalid audit object.
        # Compilation is fixture setup, with source supplied on stdin. Every
        # tested consumer is then a separate actual Bash child.
        library=folder/'unrecorded.so'
        csource=b'#define _GNU_SOURCE\n#include <link.h>\n#include <unistd.h>\nunsigned int la_version(unsigned int v){write(2,"AUDIT_UNRECORDED_LOADED\\n",24);return LAV_CURRENT;}\n__attribute__((constructor)) static void init(void){write(2,"PRELOAD_UNRECORDED_LOADED\\n",26);}\nint extra_value(void){return 42;}\n'
        if P('/usr/bin/gcc').exists():
            p=check('LIBRARY-FIXTURE-COMPILE',['C7.14'],cd+'gcc -shared -fPIC -x c -o unrecorded.so -',
                    'Compile concrete local test library; compilation failure leaves consumer tests untested.',kind='setup',data=csource,files=[library])
            if p is not None and p.returncode==0 and library.exists():
                check('SAVED-LD-PRELOAD',['C7.14'],cd+'LD_PRELOAD='+shlex.quote(str(library))+' /usr/bin/true',
                      'Saved unrecorded preload library must not be mapped/executed.',marker='PRELOAD_UNRECORDED_LOADED',files=[library])
                check('SAVED-LD-AUDIT',['C7.14'],cd+'LD_AUDIT='+shlex.quote(str(library))+' /usr/bin/true',
                      'Saved valid audit library must not be mapped/executed.',marker='AUDIT_UNRECORDED_LOADED',files=[library])
                check('SAVED-FFI',['C7.14'],cd+py('import ctypes; d=ctypes.CDLL('+repr(str(library))+'); print("FFI_UNRECORDED_EXECUTED",d.extra_value())'),
                      'Saved unrecorded FFI library must not execute.',marker='FFI_UNRECORDED_EXECUTED',files=[library])
            else:unavailable('SAVED-LD-PRELOAD-AUDIT-FFI',['C7.14'],'The concrete ordinary compiler fixture did not produce a usable library.')
        else:unavailable('SAVED-LD-PRELOAD-AUDIT-FFI',['C7.14'],'The supplied image has no gcc for the concrete audit library fixture.')
        # Runtime-only memfd contains bytes of an already recorded base file.
        memfd='''import os
fd=os.memfd_create("extra-runtime",0)
os.write(fd,open("/usr/bin/true","rb").read())
pid=os.fork()
if pid==0:
 try: os.execve(fd,["extra-runtime"],dict(os.environ))
 except OSError as e: print("MEMFD_REFUSED",str(e),flush=True);os._exit(77)
_,status=os.waitpid(pid,0)
print("MEMFD_RUNTIME_EXECUTED" if os.waitstatus_to_exitcode(status)==0 else "MEMFD_RUNTIME_RESTRICTED")
'''
        check('MEMFD-RUNTIME',['C7.15'],cd+py(memfd),
              'Observe runtime-only execution under the profile; neither deny nor success creates a mandatory memory declaration line.',marker='MEMFD_RUNTIME_EXECUTED',kind='runtime')
        savedelf=fixture(folder/'saved-native',P('/usr/bin/true').read_bytes(),0o600)
        saved_memfd=memfd.replace('open("/usr/bin/true","rb")','open('+repr(savedelf)+',"rb")').replace('MEMFD_RUNTIME_EXECUTED','MEMFD_SAVED_INPUT_EXECUTED')
        check('MEMFD-SAVED-INPUT',['C7.15'],cd+py(saved_memfd),
              'A memfd must not erase provenance of an uncovered saved executable copy.',marker='MEMFD_SAVED_INPUT_EXECUTED',files=[savedelf])
        # x86-64 fixture: mov eax,42; ret. The guest architecture is captured.
        emit(phase='availability',id='RUNTIME-ARCHITECTURE',machine=os.uname().machine)
        machine=b'\xb8\x2a\x00\x00\x00\xc3'
        jit='''import ctypes,mmap
b=PAYLOAD
m=mmap.mmap(-1,4096,prot=mmap.PROT_READ|mmap.PROT_WRITE|mmap.PROT_EXEC)
m.write(b)
f=ctypes.CFUNCTYPE(ctypes.c_int)(ctypes.addressof(ctypes.c_char.from_buffer(m)))
print("JIT_RUNTIME_EXECUTED",f())
'''
        if os.uname().machine=='x86_64':
            check('JIT-RUNTIME',['C7.16'],cd+py(jit.replace('PAYLOAD',repr(machine))),
                  'Typed machine bytes exist only in anonymous runtime memory; observe execution without demanding a new line.',marker='JIT_RUNTIME_EXECUTED 42',kind='runtime')
            savedmachine=fixture(folder/'machine.bytes',machine)
            check('JIT-SAVED-INPUT',['C7.16'],cd+py(jit.replace('PAYLOAD','open('+repr(savedmachine)+',"rb").read()').replace('JIT_RUNTIME_EXECUTED','JIT_SAVED_INPUT_EXECUTED')),
                  'Mapping anonymous memory must not admit uncovered saved executable instruction bytes.',marker='JIT_SAVED_INPUT_EXECUTED 42',files=[savedmachine])
            injection='''import ctypes,mmap,os
lib=ctypes.CDLL(None,use_errno=True)
class IOV(ctypes.Structure):_fields_=[("base",ctypes.c_void_p),("length",ctypes.c_size_t)]
m=mmap.mmap(-1,4096,flags=mmap.MAP_PRIVATE|mmap.MAP_ANONYMOUS,prot=7)
m.write(b"\\xb8\\x07\\x00\\x00\\x00\\xc3")
address=ctypes.addressof(ctypes.c_char.from_buffer(m))
r,w=os.pipe();pid=os.fork()
if pid==0:
 os.close(w);os.read(r,1)
 value=ctypes.CFUNCTYPE(ctypes.c_int)(address)()
 print("PROCESS_MEMORY_INJECTED" if value==42 else "PROCESS_MEMORY_UNCHANGED",value,flush=True)
 os._exit(0)
os.close(r)
buf=ctypes.create_string_buffer(b"\\xb8\\x2a\\x00\\x00\\x00\\xc3")
a=IOV(ctypes.addressof(buf),6);b=IOV(address,6)
f=lib.process_vm_writev;f.restype=ctypes.c_ssize_t
f.argtypes=[ctypes.c_int,ctypes.POINTER(IOV),ctypes.c_ulong,ctypes.POINTER(IOV),ctypes.c_ulong,ctypes.c_ulong]
n=f(pid,ctypes.byref(a),1,ctypes.byref(b),1,0)
print("PROCESS_MEMORY_WRITE",n,"errno",ctypes.get_errno(),flush=True)
os.write(w,b"x");os.close(w);os.waitpid(pid,0)
'''
            check('PROCESS-MEMORY-RUNTIME',['C7.22'],cd+py(injection),
                  'Observe same-user parent-to-child runtime code injection; no saved payload and no separate runtime memory record required.',marker='PROCESS_MEMORY_INJECTED 42',kind='runtime')
        else:
            unavailable('JIT-RUNTIME-SAVED',['C7.16'],'Prepared machine instruction fixture is x86-64 only.')
            unavailable('PROCESS-MEMORY-RUNTIME',['C7.22'],'Prepared injection instruction fixture is x86-64 only.')
        register=P('/proc/sys/fs/binfmt_misc/register')
        if register.exists() and not (register.parent/'v4-extra').exists():
            check('BINFMT-REGISTER',['C7.23'],cd+"printf ':v4-extra:E::v4extra::/usr/bin/true:' > /proc/sys/fs/binfmt_misc/register",
                  'Observe registration invocation; only subsequent exact entry readback decides the boundary.',kind='setup')
            entry=register.parent/'v4-extra'
            exists=entry.exists()
            boundary={'id':'BINFMT-EFFECT','variants':['C7.23'],'passed':not exists,
                      'status':'BOUNDARY_FAILED' if exists else 'ATTEMPT_REFUSED',
                      'effective_entry':entry.read_text() if exists else None}
            results.append(boundary)
            emit(phase='boundary_result',**boundary)
            if exists:
                # Remove only the exact test registration through external root.
                entry.write_text('-1')
        else:unavailable('BINFMT-REGISTER',['C7.23'],'binfmt_misc registration interface is absent or the fixture name is occupied; no mount or replacement performed.')
        foreign=[str(p) for p in P('/usr/bin').glob('qemu-*-static')]
        unavailable('FOREIGN-INTERPRETER',['C7.23'],'No prepared foreign-architecture payload or demonstrated interpreter invocation; presence alone is not a test.',available_runtimes=foreign)
        # No eval/import: a recorded program directly interprets a small typed
        # instruction set. Saved and typed input use the very same dispatcher.
        source=b'#!/usr/bin/python3.13\nimport pathlib,sys\ntext=sys.argv[2] if sys.argv[1]=="--inline" else pathlib.Path(sys.argv[2]).read_text()\nparts=text.split()\nif len(parts)==2 and parts[0]=="PRINT":\n print(parts[1])\n'
        entry='/opt/stand/pkgs/v4-extra-dispatch/bin/dispatch'
        row={'id':'v4-extra-dispatch','type':'code','managed':True,'version':'1','source':'builder:manual-dispatcher',
             'entrypoints':[{'path':entry,'interpreter':'/usr/bin/python3.13'}],
             'files':[{'path':entry,'kind':'file','mode':493,'uid':0,'gid':0,'sha256':hashlib.sha256(source).hexdigest(),'content_b64':base64.b64encode(source).decode()}]}
        if row['id'] in initial_ids:raise RuntimeError('dispatcher fixture collides with initial declaration')
        spec=fixture(folder/'dispatcher.json',json.dumps(row)+'\n')
        emit(phase='expected',id='DISPATCHER-INSTALL',variants=['C7.24'],command='stand-pkg install '+spec,exact_row=row,expected='Common broker applies exact recorded dispatcher before input tests.')
        try:
            install=ordinary('stand-pkg install '+shlex.quote(spec))
            current={r['id']:r for r in stand.load(stand.current_dir())}
            checks=stand.verify(emit=False)
            ready=install.returncode==0 and current.get(row['id'])==row and all(c['ok'] for c in checks)
            emit(phase='result',id='DISPATCHER-INSTALL',passed=ready,rc=install.returncode,stdout=install.stdout.decode(errors='replace'),stderr=install.stderr.decode(errors='replace'),identity=snapshot(),readback_failures=[c for c in checks if not c['ok']])
            if ready:
                check('DISPATCHER-TYPED',['C7.24'],shlex.join([entry,'--inline','PRINT DISPATCHER_TYPED_EXECUTED']),
                      'Recorded custom dispatcher accepts the person typed instruction; no new saved object or setting.',marker='DISPATCHER_TYPED_EXECUTED',kind='positive')
                instructions=fixture(folder/'instructions.ops','PRINT DISPATCHER_SAVED_EXECUTED\n')
                check('DISPATCHER-SAVED',['C7.24'],shlex.join([entry,'--file',instructions]),
                      'Recorded dispatcher must not execute uncovered saved instructions even without eval/import.',marker='DISPATCHER_SAVED_EXECUTED',files=[instructions])
            else:implementation_failures.append('DISPATCHER-INSTALL')
        finally:
            current={r['id']:r for r in stand.load(stand.current_dir())}
            if row['id'] in current:
                emit(phase='expected',id='DISPATCHER-REMOVE',expected='Remove exact added fixture through common broker; executable absent afterward.')
                remove=ordinary('stand-pkg remove '+row['id'])
                good=remove.returncode==0 and not P(entry).exists()
                emit(phase='result',id='DISPATCHER-REMOVE',passed=good,rc=remove.returncode,stdout=remove.stdout.decode(errors='replace'),stderr=remove.stderr.decode(errors='replace'))
                if not good:implementation_failures.append('DISPATCHER-REMOVE')
        unavailable('BROWSER-EXTENSION',['C8.07'],
                    'Supplied browser is w3m. Its documented local CGI mechanism is not a browser-equivalent extension API; no extension facility or extension fixture has been demonstrated. Passive HTML rendering is not substituted.',
                    browser_present=P('/usr/bin/w3m').exists(),documentation=DOCS['browser'])
    restored=(stand.current_dir()/'machine.jsonl').read_bytes()==initial_bytes
    checks=stand.verify(emit=False)
    emit(phase='result',id='EXTRA-FINAL-RESTORATION',passed=restored and all(c['ok'] for c in checks),declaration_bytes_restored=restored,readback_count=len(checks),readback_failures=[c for c in checks if not c['ok']])
    if not restored or not all(c['ok'] for c in checks):implementation_failures.append('EXTRA-FINAL-RESTORATION')
    emit(phase='summary',implementation_failures=implementation_failures,
         boundary_failures=[r['id'] for r in results if r['status']=='BOUNDARY_FAILED'],
         untested=[r['id'] for r in results if r['status']=='UNTESTED'],
         runtime_observations=[{'id':r['id'],'status':r['status']} for r in results if r['status'].startswith('RUNTIME')],
         closure_claim=False,hypothesis_outcome='?')
    return int(bool(implementation_failures))

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as error:
        emit(phase='summary',implementation_failed=True,error=str(error),closure_claim=False);sys.exit(1)
