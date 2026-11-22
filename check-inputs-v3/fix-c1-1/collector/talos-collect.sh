#!/bin/sh
# Documentation-derived API collector; never exercised on a check system.
exec python3 - "$@" <<'PY'
import os,sys,pathlib,subprocess,csv,json,hashlib,datetime,re,collections
out=pathlib.Path(sys.argv[1]);machine=sys.argv[2] if len(sys.argv)>2 else 'talos'
out.mkdir(parents=True,exist_ok=False);(out/'raw').mkdir()
base=['talosctl','--talosconfig',os.environ['TALOSCONFIG'],'--endpoints',os.environ.get('TALOS_ENDPOINT',os.environ.get('TALOS_ENDPOINTS','')),'--nodes',os.environ.get('TALOS_NODE',os.environ.get('TALOS_NODES',''))]
rows=[];coverage=[]
def obj(level,kind,name,members,ev):
 ident=hashlib.sha256(json.dumps([machine,level,kind,name,members],sort_keys=True).encode()).hexdigest()[:24]
 rows.append([ident,machine,level,kind,name,json.dumps(members),ev])
NETWORK_KINDS=set("BGPInstanceConfig BlackholeRouteConfig BondConfig BridgeConfig DHCPv4Config DHCPv6Config DummyLinkConfig EthernetConfig HCloudVIPConfig HostnameConfig KubeSpanConfig KubeSpanEndpointsConfig HTTPProbeConfig Layer2VIPConfig LinkAliasConfig LinkConfig NetworkDefaultActionConfig NetworkRuleConfig ResolverConfig RoutingRuleConfig StaticHostConfig TCPProbeConfig TimeSyncConfig VethConfig VLANConfig VRFConfig WireguardConfig".split())
def saved_networks(data):
 gaps=[]
 def scrub(value):
  if isinstance(value,dict):return {k:('[REDACTED]' if re.search('secret|password|token|private|key|cert|psk|credential',str(k),re.I) else scrub(v)) for k,v in value.items()}
  if isinstance(value,list):return [scrub(v) for v in value]
  return value
 def walk(value,decode_strings=True):
  found=[]
  if isinstance(value,dict):
   if value.get('kind') in NETWORK_KINDS:return [scrub(value)]
   for k,v in value.items():
    if str(k).lower()=='network':found.append(scrub(v))
    else:found.extend(walk(v,decode_strings))
  elif isinstance(value,list):
   for v in value:found.extend(walk(v,decode_strings))
  elif isinstance(value,str) and decode_strings and (':' in value or value.lstrip().startswith(('{','['))):
   try:
    import yaml
    for doc in yaml.safe_load_all(value):
     if isinstance(doc,(dict,list)):found.extend(walk(doc,False))
   except Exception:gaps.append('embedded configuration could not be decoded')
  return found
 decoder=json.JSONDecoder();text=data.decode(errors='replace');net=[]
 try:
  while text.strip():
   text=text.lstrip();value,end=decoder.raw_decode(text);text=text[end:];net.extend(walk(value))
 except (ValueError,TypeError):gaps.append('configuration JSON could not be decoded')
 if not net:gaps.append('no decodable saved network configuration')
 return net,gaps
def query(kind,args,level=1):
 n=len(coverage)+1;ev=f'raw/{n:03d}-{kind}.txt'
 p=subprocess.run(base+args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if kind=='machine-configuration':
  # Retain network configuration only; redact before any raw write.
  net,gaps=saved_networks(p.stdout)
  records=[{'metadata':{'id':str(i)+':'+str(item.get('kind','legacy-network') if isinstance(item,dict) else 'legacy-network')},'spec':item} for i,item in enumerate(net)]
  p.stdout=json.dumps(records).encode()
  for gap in gaps:coverage.append(['machineconfig-network-extraction',3,gap,''])
  p.stderr=b'' if p.returncode==0 else b'machineconfig request failed; response omitted to protect credentials\n'
 (out/ev).write_bytes(p.stdout);(out/(ev+'.err')).write_bytes(p.stderr)
 coverage.append([json.dumps(args),p.returncode,ev,ev+'.err'])
 if p.returncode:return
 # Preserve each API/table record independently. Resource JSON can be a stream.
 text=p.stdout.decode(errors='replace')
 if '-o' in args:
  decoder=json.JSONDecoder();rest=text
  while rest.strip():
   rest=rest.lstrip()
   try:r,end=decoder.raw_decode(rest)
   except ValueError:obj(level,'unparsed-api-evidence',kind,[text],ev);return
   rest=rest[end:]
   for item in r if isinstance(r,list) else [r]:
    meta=item.get('metadata',{}) if isinstance(item,dict) else {}
    obj(level,kind,str(meta.get('id',meta.get('name',len(rows)))),item,ev)
 else:
  for i,line in enumerate(text.splitlines(),1):
   if not line.strip() or line.startswith('NODE '):continue
   obj(level,kind,line.split()[1] if len(line.split())>1 else line,[line],ev+':'+str(i))
for kind,args in [
 ('resource-definition',['get','rd','-o','json']),('service',['service']),
 ('process',['processes']),('mount',['mounts']),('port',['netstat']),
 ('module',['get','loadedkernelmodules','-o','json']),('driver-device',['get','pcidevices','-o','json']),
 ('extension',['get','extensions','-o','json']),('software-component',['get','sbom','-o','json']),
 ('machine-configuration',['get','machineconfig','-o','json']),
 ('saved-network-link',['get','links','-o','json']),
 ('network-link',['get','linkstatuses','-o','json']),('network-address',['get','addresses','-o','json']),
 ('network-route',['get','routes','-o','json']),('network-ethernet',['get','ethernetstatuses','-o','json']),
 ('firewall-rule',['get','nftableschains','-o','json']),
 ('account',['read','/etc/passwd']),('group',['read','/etc/group']),
 ('module-text',['read','/proc/modules']),('driver-text',['read','/proc/devices'])]:query(kind,args)
for namespace in ('system','cri','taloscontainers','inmem'):
 query('container-'+namespace,['containers','--namespace',namespace])
 query('image-'+namespace,['image','list','--namespace',namespace])
# CLI source fixes NAME at the table header's column; one endpoint only.
args=['list','/','--recurse','--long'];p=subprocess.run(base+args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
ev='raw/filesystem.txt';(out/ev).write_bytes(p.stdout);(out/(ev+'.err')).write_bytes(p.stderr)
coverage.append([json.dumps(args),p.returncode,ev,ev+'.err'])
lines=p.stdout.decode(errors='replace').splitlines();groups=collections.defaultdict(list)
column=next((line.index('NAME') for line in lines if line.startswith('NODE') and 'NAME' in line),None)
if column is not None:
 for line in lines:
  if line.startswith('NODE') or len(line)<=column:continue
  prefix=line[:column].split();path='/'+line[column:].split(' -> ',1)[0].lstrip('/')
  if len(prefix)<2:continue
  mode=prefix[1];groups[str(pathlib.PurePosixPath(path).parent)].append(path)
  # Ownership unavailable: conservatively list every exposed path as unowned.
  if mode.startswith('-'):
   proc=subprocess.Popen(base+['read',path],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
   first=proc.stdout.read(2)
   while proc.stdout.read(1048576):pass
   rc=proc.wait();coverage.append([json.dumps(['read',path]),rc,'prefix-only; contents discarded',''])
   startup=pathlib.PurePosixPath(path).name in ('.profile','.bashrc','.bash_profile','.zshrc','.zshenv','config.fish') or path.startswith('/etc/profile.d/')
   if 'x' in mode or first==b'#!' or startup:
    obj(2,'executable-code-outside-packages',path,[mode,'shebang='+str(first==b'#!')],ev)
 for directory,paths in sorted(groups.items()):obj(2,'stored-outside-packages',directory,paths,ev)

with (out/'objects.tsv').open('w') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['id','machine','level','kind','name','members','evidence']);w.writerows(rows)
with (out/'coverage.tsv').open('w') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['command','exit_code','stdout','stderr']);w.writerows(coverage)
(out/'limitations.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'not_inventoried':['Filesystem paths not exposed by the API','Package ownership unavailable: all exposed paths conservatively unowned','Workload-internal package managers','System/user timers not exposed as resources','Full process executable linkage','Complete effective firewall rules beyond exposed nftableschains','Access rules not exposed as resources'],'documentation_only_validation':True},indent=2)+'\n')
PY
