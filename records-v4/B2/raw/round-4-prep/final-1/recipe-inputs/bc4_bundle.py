#!/usr/bin/python3 -B
"""Export and apply the complete existing BC3 declaration and exact content blobs.

The bundle format is unchanged. blobs.json is transport, not another declaration.
Application is root-only, uses stand-apply and the filesystem application API,
and reports success only after all eight selected declaration files match.
"""
import argparse, base64, hashlib, json, os, pathlib, socket, stat, subprocess, tempfile
from bc3_account_rows import account_rows

P=pathlib.Path
MOUNTS={'home':'/home/stand','tmp':'/tmp','vartmp':'/var/tmp','shm':'/dev/shm','etc':'/etc'}
MACHINE='/var/lib/stand/current/machine.jsonl'
MANIFEST='/var/lib/stand/current/base-files.json'
DESIGNATION='/etc/stand/bc3-primary.json'
def fs_path(key):return '/var/lib/stand-fs/'+key+'/current/declaration.json'
def encode(value):return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(data):return hashlib.sha256(data).hexdigest()

def validate_filesystem(state, blobs):
    if state['format']!='bc3-declared-filesystem-v1':raise ValueError('unknown filesystem format')
    if type(state['generation']) is not int or type(state['next_inode']) is not int or state['generation']<0:raise ValueError('invalid counters')
    paths,objects=state['paths'],state['objects']
    if '/' not in paths:raise ValueError('missing root')
    if not stat.S_ISDIR(objects[paths['/']]['st_mode']):raise ValueError('root is not a directory')
    if not objects or any(not i.isdigit() or int(i)<1 for i in objects) or state['next_inode']<=max(map(int,objects)):raise ValueError('invalid inode allocation counter')
    if set(paths.values())!=set(objects):raise ValueError('unreachable or missing inode; close retained handles before export')
    for name,inode in paths.items():
        if not name.startswith('/') or str(P(name))!=name or '..' in P(name).parts:raise ValueError('invalid path')
        if not str(inode).isdigit():raise ValueError('invalid inode')
        if name!='/':
            parent=name.rsplit('/',1)[0] or '/'
            if parent not in paths or not stat.S_ISDIR(objects[paths[parent]]['st_mode']):raise ValueError('missing directory')
    for node in objects.values():
        for key in ('st_mode','st_uid','st_gid','st_atime','st_mtime','st_ctime','st_size','xattrs'):node[key]
        kind=stat.S_IFMT(node['st_mode'])
        if kind==stat.S_IFREG:
            content=blobs[node['sha256']]
            if sha(content)!=node['sha256'] or len(content)!=node['st_size']:raise ValueError('content mismatch')
        elif kind==stat.S_IFLNK:
            if not isinstance(node['target'],str):raise ValueError('missing symlink target')
        elif kind!=stat.S_IFDIR:raise ValueError('unsupported node kind')
        for value in node['xattrs'].values():base64.b64decode(value,validate=True)
    if 'account_rows' in state:
        databases={}
        for name in ('passwd','group','shadow','gshadow','subuid','subgid'):
            inode=paths.get('/'+name)
            if inode is not None:databases['/etc/'+name]=blobs[objects[inode]['sha256']]
        if account_rows(databases)!=state['account_rows']:raise ValueError('account semantics do not match database requirements')

def export(destination):
    destination.mkdir(parents=True,exist_ok=False)
    files={p:P(p).read_text() for p in (MACHINE,MANIFEST,DESIGNATION)}
    blobs={}
    for key in MOUNTS:
        path=fs_path(key);data=P(path).read_bytes();files[path]=data.decode()
        state=json.loads(data)
        for node in state['objects'].values():
            if 'sha256' in node:
                digest=node['sha256'];content=(P('/var/lib/stand-fs')/key/'blobs'/digest).read_bytes()
                if sha(content)!=digest:raise ValueError('source blob mismatch')
                blobs[digest]=base64.b64encode(content).decode()
        if P(path).read_bytes()!=data:raise ValueError('filesystem changed during export')
    if any(P(p).read_bytes()!=t.encode() for p,t in files.items()):raise ValueError('complete declaration changed during export')
    (destination/'declaration.json').write_bytes(encode({'format':'bc3-complete-declaration-v1','files':files}))
    (destination/'blobs.json').write_bytes(encode(blobs))
    print(json.dumps({'declaration_sha256':sha((destination/'declaration.json').read_bytes()),'blobs':len(blobs)}))

def apply(source):
    bundle=json.loads((source/'declaration.json').read_bytes())
    if bundle['format']!='bc3-complete-declaration-v1':raise ValueError('unknown bundle format')
    files=bundle['files'];expected={MACHINE,MANIFEST,DESIGNATION}|{fs_path(k) for k in MOUNTS}
    if set(files)!=expected:raise ValueError('complete eight-file description required')
    designation=json.loads(files[DESIGNATION])
    if set(designation['primary_files'])!={MACHINE}|{fs_path(k) for k in MOUNTS}:raise ValueError('changed primary designation')
    if designation['filesystem_mounts']!=MOUNTS:raise ValueError('changed mount mapping')
    blobs={k:base64.b64decode(v,validate=True) for k,v in json.loads((source/'blobs.json').read_bytes()).items()}
    for key in MOUNTS:
        state=json.loads(files[fs_path(key)])
        if key=='etc' and 'account_rows' not in state:raise ValueError('account database semantics required')
        validate_filesystem(state,blobs)
    etc=json.loads(files[fs_path('etc')]);node=etc['objects'][etc['paths']['/stand/bc3-primary.json']]
    if blobs[node['sha256']]!=files[DESIGNATION].encode():raise ValueError('designation contradicts filesystem')
    with tempfile.TemporaryDirectory(prefix='bundle-',dir='/var/lib/stand') as folder:
        root=P(folder)
        (root/'machine.jsonl').write_text(files[MACHINE]);(root/'base-files.json').write_text(files[MANIFEST])
        subprocess.run(['/usr/local/bin/stand-apply',str(root)],check=True)
        for key in MOUNTS:
            state=json.loads(files[fs_path(key)])
            needed={n['sha256'] for n in state['objects'].values() if 'sha256' in n}
            request={'declaration':files[fs_path(key)],'blobs':{k:base64.b64encode(blobs[k]).decode() for k in needed}}
            with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as client:
                client.settimeout(120);client.connect('/var/lib/stand-fs/'+key+'/apply.sock')
                client.sendall(encode(request));client.shutdown(socket.SHUT_WR)
                answer=b''
                while True:
                    data=client.recv(65536)
                    if not data:break
                    answer+=data
            result=json.loads(answer)
            if result.get('status')!='success':raise RuntimeError(str(result))
    subprocess.run(['/usr/bin/systemctl','daemon-reload'],check=True)
    subprocess.run(['/usr/local/bin/stand-verify'],check=True)
    subprocess.run(['/usr/bin/python3','-B','/usr/local/lib/stand/bc3-state.py','verify'],check=True)
    mismatches=[p for p,text in files.items() if P(p).read_bytes()!=text.encode()]
    if mismatches:raise RuntimeError('selected declaration differs: '+str(mismatches))
    receipt={'status':'success','complete_declaration_sha256':sha((source/'declaration.json').read_bytes()),
             'file_sha256':{p:sha(t.encode()) for p,t in files.items()}}
    import stand
    stand.atomic(P('/var/lib/stand')/'complete-last-success.json',encode(receipt),0o600)
    print('COMPLETE SUCCESS '+receipt['complete_declaration_sha256'])

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('operation',choices=['export','apply']);parser.add_argument('directory',type=P);args=parser.parse_args()
    if os.geteuid()!=0:raise SystemExit('root application/export credential required')
    (export if args.operation=='export' else apply)(args.directory)
if __name__=='__main__':main()
