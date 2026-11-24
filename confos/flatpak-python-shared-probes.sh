#!/bin/bash
set -u
binary=/usr/bin/python3.14
recorded=/home/user/bin/recorded-flatpak-python.py
failures=0
check() {
    local expected=$1 output status
    shift
    output=$(timeout -k 2 30 flatpak run --command="$binary" io.mpv.Mpv "$@" 2>&1); status=$?
    printf '\nCOMMAND '; printf '%q ' "$@"; printf '\n%s\nEXIT %s\n' "$output" "$status"
    if [ "$expected" = refuse ]; then
        if [[ $output != *'Permission denied'* || $output == *UNRECORDED-PYTHON-RAN* ]]; then failures=$((failures+1)); fi
    elif [ "$status" != 0 ] || [[ $output != *RECORDED-PYTHON-RAN* ]]; then failures=$((failures+1)); fi
}
printf 'print("UNRECORDED-PYTHON-RAN")\n' >/home/user/flatpak_python_material.py
for directory in /home/user /tmp /dev/shm; do
    file="$directory/flatpak_python_material.py"
    for route in script stdin import module bytecode zip startup; do
        check refuse -c '
import os,sys,marshal,importlib.util,zipfile
p,route,exe=sys.argv[1:]
if not p.startswith("/home/user/"): open(p,"w").write("print(\"UNRECORDED-PYTHON-RAN\")\n")
if route=="script": os.execv(exe,[exe,p])
elif route=="stdin":
 os.dup2(os.open(p,os.O_RDONLY),0); os.execv(exe,[exe])
elif route=="import":
 sys.path.insert(0,os.path.dirname(p)); __import__("flatpak_python_material")
elif route=="module":
 os.chdir(os.path.dirname(p)); os.environ["PYTHONPATH"]=os.path.dirname(p); os.execv(exe,[exe,"-m","flatpak_python_material"])
elif route=="bytecode":
 q=os.path.join("/tmp" if p.startswith("/home/user/") else os.path.dirname(p),"material.pyc"); print("GENERATED_CODE_PATH",q,flush=True); open(q,"wb").write(importlib.util.MAGIC_NUMBER+b"\0"*12+marshal.dumps(compile(open(p).read(),p,"exec"))); os.execv(exe,[exe,q])
elif route=="zip":
 q=os.path.join("/tmp" if p.startswith("/home/user/") else os.path.dirname(p),"material.zip"); print("GENERATED_CODE_PATH",q,flush=True)
 with zipfile.ZipFile(q,"w") as z: z.write(p,"__main__.py")
 os.execv(exe,[exe,q])
elif route=="startup":
 os.environ["PYTHONSTARTUP"]=p; os.dup2(os.open("/dev/null",os.O_RDONLY),0); os.execv(exe,[exe,"-i"])
' "$file" "$route" "$binary"
    done
done
check recorded "$recorded"
check recorded -c 'import sys; sys.path.insert(0,"/home/user/bin"); import recorded_flatpak_module'
check recorded -c 'print("RECORDED-PYTHON-RAN")'
check recorded -c 'import os; os.environ["PYTHONSTARTUP"]="/home/user/bin/recorded-flatpak-python.py"; os.execv(__import__("sys").argv[1],[__import__("sys").argv[1],"-i"])' "$binary" </dev/null
check recorded -c 'import ssl,sqlite3,dbm.gnu,_zstd,ctypes,zlib,bz2,curses,json,hashlib; print("RECORDED-PYTHON-RAN",ssl.OPENSSL_VERSION)'
check recorded -c 'p="/tmp/data"; open(p,"w").write("RECORDED-PYTHON-RAN"); print(open(p).read())'
check recorded -c 'import subprocess,sys; subprocess.run([sys.argv[1]],input="print(\"RECORDED-PYTHON-RAN\")\n",text=True,check=True)' "$binary"
echo "FLATPAK PYTHON FAILURES $failures"
test "$failures" = 0
