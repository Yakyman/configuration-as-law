import ctypes, os, sys
libc=ctypes.CDLL(None, use_errno=True)
PR_GET_SECUREBITS=27
PR_SET_SECUREBITS=28
mask=0xf00
before=libc.prctl(PR_GET_SECUREBITS,0,0,0,0)
rc=libc.prctl(PR_SET_SECUREBITS,before|mask,0,0,0)
after=libc.prctl(PR_GET_SECUREBITS,0,0,0,0)
print(f'SET rc={rc} errno={ctypes.get_errno()} before={before:#x} after={after:#x}',flush=True)
if rc!=0 or after & mask !=mask:
    print('PREREQUISITE_FAILED',flush=True)
    raise SystemExit(77)
os.setgroups([])
os.setgid(65534)
os.setuid(65534)
os.execv(sys.executable,[sys.executable,'-I','-S','-c','import ctypes,os; print(f"CHILD euid={os.geteuid()} bits={ctypes.CDLL(None).prctl(27,0,0,0,0):#x}"); print("PYTHON_CODE_RAN")'])
