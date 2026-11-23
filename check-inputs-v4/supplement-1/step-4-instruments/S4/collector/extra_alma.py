"""Alma-specific current content evidence; never infer historical intent."""
import base64
import json
import os
import shlex


def collect(ctx):
    from main import write_tsv
    rows = []
    origin_groups = {'/boot/grub2','/boot/loader/entries','/etc/NetworkManager/system-connections','/etc/alsa','/etc/firewalld/zones','/etc/kernel','/etc/sysconfig','/var/lib/selinux/targeted/active'}
    def historical_target(obj):
        return (obj[3] in ('saved-network','saved-network-file') or obj[4] in origin_groups
                or obj[3]=='package' and obj[4].startswith('rpm:gpg-pubkey@')
                or obj[3]=='unit-file' and obj[4] in ('rpmdb-migrate.service','rpmdb-rebuild.service'))
    def attach(path, fact, value, status, evidence, kinds=()):
        for obj in ctx.objects:
            name = obj[4]
            if name == path or (obj[2] == 2 and name == os.path.dirname(path)) or (kinds and obj[3] in kinds):
                rows.append([obj[0], path, fact, value, status, evidence])
    # Only these known non-secret configuration families are copied as text.
    prefixes = ('/etc/dconf/profile/', '/etc/dconf/db/', '/etc/alsa/',
                '/etc/firewalld/zones/', '/etc/kernel/', '/etc/sysconfig/',
                '/boot/loader/entries/', '/boot/grub2/')
    selected = [p for p, r in ctx.entries.items()
                if r.get('type') == 'file' and p.startswith(prefixes)
                and not (p.startswith('/etc/dconf/db/') and '/' not in p[len('/etc/dconf/db/'):])
                and not p.endswith(('.env', '.key', '.pem'))
                and 'network-scripts' not in p]
    # Never inspect private material in arbitrary files in these directories.
    selected = [p for p in selected if '/etc/sysconfig/' not in p or os.path.basename(p) in ('kernel','selinux','network','grub')]
    for path, (data, rc, ev) in ctx.safe_reads(selected, 16777216).items():
        attach(path, 'current-content-base64' if path.endswith('/grubenv') else 'current-content', (base64.b64encode(data).decode() if path.endswith('/grubenv') else data.decode(errors='replace')) if not rc else '', 'recorded' if not rc else 'unavailable', ev)
    network_script = r'''command -v python3 >/dev/null || exit 127
python3 - <<'ENDPY'
import configparser,glob,json,os
allowed={'connection':{'id','uuid','type','interface-name','autoconnect','timestamp'},'ethernet':{'mac-address','cloned-mac-address','mtu'},'ipv4':{'method','address1','gateway','dns','route1','route-metric','never-default'},'ipv6':{'method','address1','gateway','dns','route1','route-metric','never-default'}}
for path in glob.glob('/etc/NetworkManager/system-connections/*.nmconnection'):
    if os.path.islink(path):
        print(json.dumps({'path':path,'status':'symlink-not-read'}));continue
    try:
        with open(path,'rb') as handle: data=handle.read(1048577)
        if len(data)>1048576:
            print(json.dumps({'path':path,'status':'size-cap'}));continue
        parser=configparser.ConfigParser(interpolation=None)
        parser.read_string(data.decode())
        values={section:{key:parser[section][key] for key in sorted(keys) if key in parser[section]} for section,keys in allowed.items() if section in parser}
        print(json.dumps({'path':path,'status':'recorded-nonsecret-fields','values':values}))
    except (OSError,ValueError,configparser.Error,UnicodeError):print(json.dumps({'path':path,'status':'read-or-parse-failed'}))
ENDPY
'''
    data,rc,ev=ctx.query('s4-alma-network-nonsecret-values',network_script,60)
    for line in data.splitlines():
        try:
            item=json.loads(line);path=item['path']
        except (ValueError,KeyError):continue
        attach(path,'network-profile-nonsecret-values',json.dumps(item.get('values',{})),item.get('status','unavailable'),ev)
        identity=item.get('values',{}).get('connection',{}).get('id')
        for obj in ctx.objects:
            if obj[3]=='saved-network' and identity and obj[4].startswith(identity+':'):
                rows.append([obj[0],path,'network-profile-nonsecret-values',json.dumps(item.get('values',{})),item.get('status','unavailable'),ev])
    databases = [p for p,r in ctx.entries.items() if p.startswith('/etc/dconf/db/')
                 and '/' not in p[len('/etc/dconf/db/'):] and r.get('type') == 'file']
    for path in databases:
        # A temporary profile selects exactly one existing binary database. No update/write is run.
        script = ('command -v dconf >/dev/null || exit 127\n'
                  'profile=$(mktemp /tmp/s4-dconf-profile.XXXXXX) || exit 1\n'
                  'trap \'rm -f "$profile"\' EXIT HUP INT TERM\n'
                  'printf "%s\\n" '+shlex.quote('system-db:'+os.path.basename(path))+' > "$profile"\n'
                  'DCONF_PROFILE="$profile" dconf dump /\n')
        data,rc,ev=ctx.query('s4-dconf-dump',script,60)
        attach(path,'compiled-values',data.decode(errors='replace') if not rc else '', 'recorded' if not rc else 'unavailable',ev)
    # Preserve the schema that explains keys; a schema is not proof of a reader executing.
    schemas=[p for p,r in ctx.entries.items() if p.startswith('/usr/share/glib-2.0/schemas/') and p.endswith('.gschema.xml') and r.get('type')=='file']
    schema_refs=[]
    for p,(b,rc,ev) in ctx.safe_reads(schemas,16777216).items():
        if not rc:schema_refs.append([p,ev])
    for path in databases:
        attach(path,'key-semantics-schema-evidence',json.dumps(schema_refs),'recorded', ';'.join(sorted(set(x[1] for x in schema_refs))))
    script=r'''command -v python3 >/dev/null || exit 127
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
'''
    data,rc,ev=ctx.query('s4-dconf-current-readers',script,60)
    for path in databases:attach(path,'current-reader-snapshot',data.decode(errors='replace'), 'recorded-snapshot-not-history' if not rc else 'unavailable',ev)
    # Selected installation directives; exclude credentials and unbounded %post bodies.
    script=r'''for file in /root/anaconda-ks.cfg /root/original-ks.cfg; do
 if test -f "$file"; then
  printf 'FILE %s\n' "$file"
  awk '/^(network|bootloader|firewall|selinux|services|group|user|firstboot|keyboard|lang|timezone)( |$)/ { gsub(/--(password|rootpw|passphrase|wpakey)(=| )[[:graph:]]+/, "--credential=[REDACTED]"); print }' "$file"
 fi
done
'''
    data,rc,ev=ctx.query('s4-installation-directives',script,60)
    for obj in ctx.objects:
        if historical_target(obj):
            rows.append([obj[0],obj[4],'installer-directives',data.decode(errors='replace'),'recorded-not-intent-proof' if data and not rc else 'unavailable',ev])
    for label,script,kinds in [
        ('s4-rpm-key-history',"rpm -qa 'gpg-pubkey*' --qf '%{NAME}-%{VERSION}-%{RELEASE}\\t%{INSTALLTIME}\\t%{SUMMARY}\\n'\ndnf -C history list\n",('package',)),
        ('s4-unit-current-policy',"systemctl show rpmdb-migrate.service rpmdb-rebuild.service -p Id -p FragmentPath -p DropInPaths -p UnitFileState -p UnitFilePreset\n",('unit-file',)),
        ('s4-persistent-selinux-values',"if command -v semanage >/dev/null; then semanage boolean -l -C; else exit 127; fi\n",())]:
        data,rc,ev=ctx.query(label,script,90)
        for obj in ctx.objects:
            if (obj[3] in kinds and historical_target(obj)) or (not kinds and obj[4]=='/var/lib/selinux/targeted/active'):
                rows.append([obj[0],obj[4],label,data.decode(errors='replace'),'recorded-not-history-proof' if not rc else 'unavailable',ev])
    history_script = r"""command -v python3 >/dev/null || exit 127
python3 - <<'ENDPY'
import subprocess,json,re
commands=[['journalctl','--no-pager','--all','-o','json','_COMM=useradd','+','_COMM=usermod','+','_COMM=groupadd','+','_COMM=gpasswd','+','_COMM=dnf','+','_COMM=anaconda','+','_COMM=systemctl','+','_COMM=setsebool'],['ausearch','-m','ADD_USER,DEL_USER,ADD_GROUP,DEL_GROUP,USER_MGMT,GRP_MGMT','--raw']]
for cmd in commands:
    try:
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        total=0
        for raw in p.stdout:
            total+=len(raw)
            if total>16777216:
                p.kill();p.wait();print(json.dumps({'channel':cmd[0],'status':'output-cap'}));break
            text=raw.decode(errors='replace').strip()
            if cmd[0]=='journalctl':
                try:
                    r=json.loads(text);message=r.get('MESSAGE','')
                    if not isinstance(message,str): continue
                    # Only acquisition/account/configuration operations; never echo arbitrary journal events.
                    if not re.search(r'(?i)import|gpg|preset|disable|enable|created|useradd|usermod|groupadd|boolean|network|kickstart',message):continue
                    message=re.sub(r'(?i)(password|passwd|passphrase|psk|token|secret)([= :]+)\S+',r'\1\2[REDACTED]',message)
                    print(json.dumps({'channel':'journal','utc_usec':r.get('__REALTIME_TIMESTAMP'),'comm':r.get('_COMM'),'uid':r.get('_UID'),'message':message}))
                except ValueError: pass
            else:
                # Audit operation and result only; command/proctitle/payload fields are omitted.
                fields={}
                for key in ('type','msg','pid','uid','auid','ses','op','res'):
                    m=re.search(r'(?:^| )'+key+r'=([^ ]+)',text)
                    if m:fields[key]=m.group(1)
                if fields:print(json.dumps({'channel':'audit','fields':fields}))
        else:
            code=p.wait();print(json.dumps({'channel':cmd[0],'exit_status':code}))
    except FileNotFoundError: print(json.dumps({'channel':cmd[0],'status':'command-unavailable'}))
ENDPY
"""
    data,rc,ev=ctx.query('s4-alma-retained-history',history_script,90)
    scriptlets_script = r'''rpm -qa --qf '%{NAME}\n' | LC_ALL=C sort -u | while IFS= read -r package; do
 case "$package" in setup|systemd|NetworkManager|firewalld|alsa-utils|selinux-policy*|rpm|gdm|dconf) printf 'PACKAGE %s\n' "$package"; rpm -q --scripts "$package" ;; esac
done
'''
    scriptlets,src,sev=ctx.query('s4-alma-package-scriptlets',scriptlets_script,90)
    for obj in ctx.objects:
        if historical_target(obj):
            rows.append([obj[0],obj[4],'retained-event-evidence',data.decode(errors='replace'),'partial-evidence-not-complete-history' if not rc else 'unavailable',ev])
            rows.append([obj[0],obj[4],'package-scriptlet-evidence',scriptlets.decode(errors='replace'),'script-presence-not-execution-proof' if not src else 'unavailable',sev])
    write_tsv(ctx.out/'alma-facts.tsv',['object_id','path','fact','value','status','evidence'],rows)
    ctx.scan_counts['s4-alma-fact-rows']+=len(rows)
    ctx.scan_counts['s4-alma-dconf-databases']+=len(databases)
    if not hasattr(ctx,'s4_summary'):ctx.s4_summary={}
    ctx.s4_summary['alma']={'fact_rows':len(rows),'dconf_databases':len(databases),
        'compiled_value_rows_recorded':sum(r[2]=='compiled-values' and r[4]=='recorded' for r in rows),
        'current_content_rows_recorded':sum(r[2]=='current-content' and r[4]=='recorded' for r in rows),
        'historical_evidence_routes':3,
        'history_completeness_established':False}


