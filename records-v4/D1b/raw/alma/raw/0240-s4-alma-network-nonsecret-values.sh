command -v python3 >/dev/null || exit 127
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

