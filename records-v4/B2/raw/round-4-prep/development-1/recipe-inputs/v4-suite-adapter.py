#!/usr/bin/python3 -B
"""Run compatible channel assertions through Bash without editing old suites.

Broker requests become ordinary command lines; sealed application launches are
explicit commands in Bash. Old refusal assertions about the sealed launcher
remain compatibility checks, never proof of the free-shell text-input boundary.
"""
import json,pathlib,runpy,shlex,subprocess,sys,time
P=pathlib.Path
original=subprocess.Popen
class ThroughShell(original):
    def __init__(self,args,*a,**kw):
        if isinstance(args,(list,tuple)) and '/usr/local/bin/stand-session' in args:
            args=list(map(str,args));i=args.index('/usr/local/bin/stand-session')
            if len(args)==i+3 and args[i+1]=='-c':
                fields=args[i+2].split('\t')
                if fields[0]=='broker':
                    command=shlex.join(['/usr/local/bin/'+fields[1],*fields[2:]])
                else:
                    command=shlex.join(args[i:])
                args=args[:i]+['/usr/local/bin/stand-shell','-c',command]
                print(json.dumps({'phase':'v4-shell-entry','actual_command':args,
                    'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}),flush=True)
        super().__init__(args,*a,**kw)
subprocess.Popen=ThroughShell
suite=P('/usr/local/lib/stand')/sys.argv[1]
if suite.name not in ('language-selftest.py','app-selftest.py','system-selftest.py','round4-selftest.py'):
    raise SystemExit('only compatible channel suites supported')
sys.argv=[str(suite),*sys.argv[2:]]
runpy.run_path(str(suite),run_name='__main__')
