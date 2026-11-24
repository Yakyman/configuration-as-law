command -v python3 >/dev/null || exit 127
python3 - <<'ENDPY'
import glob,json,os
for proc in sorted(glob.glob('/proc/[0-9]*')):
    profile=None
    try:
        with open(proc+'/environ','rb') as handle: env_bytes=handle.read(1048577)
        if len(env_bytes)>1048576:
            print(json.dumps({'status':'environment-cap','pid':proc.rsplit('/',1)[-1]}));continue
        env=env_bytes.split(b'\0')
        for item in env:
            if item.startswith(b'DCONF_PROFILE='): profile=item.split(b'=',1)[1].decode(errors='replace')
        paths=[]
        with open(proc+'/maps','rb') as handle: map_bytes=handle.read(1048577)
        if len(map_bytes)>1048576:
            print(json.dumps({'status':'maps-cap','pid':proc.rsplit('/',1)[-1]}));continue
        map_lines=map_bytes.decode(errors='replace').splitlines()
        for line in map_lines:
            fields=line.split(None,5)
            if len(fields)==6 and fields[5].strip().startswith('/etc/dconf/db/'): paths.append(fields[5].strip())
        if profile is not None or paths:
            try: exe=os.readlink(proc+'/exe')
            except OSError: exe='unavailable'
            print(json.dumps({'pid':proc.rsplit('/',1)[-1], 'executable':exe,'DCONF_PROFILE':profile,'mapped_databases':sorted(set(paths))}))
    except (OSError,ProcessLookupError): print(json.dumps({'status':'process-inaccessible-or-exited','pid':proc.rsplit('/',1)[-1]}))
ENDPY

