#!/usr/bin/env python3
"""Stage and atomically publish completed Round 1 evidence; never alter raw input."""
import fcntl,hashlib,json,os,pathlib,shutil,stat,tarfile,time
P=pathlib.Path
ROOT=P(__file__).resolve().parent.parent
CANDIDATE=ROOT/'candidate-1'
FINAL=CANDIDATE/'raw/round-1/final-2'
ARCHIVE=ROOT/'round1-publication.tar.gz'
PUBLISHED=ROOT/'round1-publication'
STAGE=ROOT/'round1-publication.tmp'
TAR_TMP=ROOT/'round1-publication.tar.gz.tmp'
MARKER=ROOT/'round1-publication-commit.json'
lock=(ROOT/'locks/round1-packaging.lock').open('a')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
def require(condition,message):
    if not condition:raise RuntimeError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def read_json(path):return json.loads(path.read_text())
def syncdir(path):
    fd=os.open(path,os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
def tree_inventory(path):
    require(path.exists() and not path.is_symlink(),'invalid retained input')
    out={}
    for p in [path]+(sorted(path.rglob('*')) if path.is_dir() else []):
        info=p.lstat();require(stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode),'unsupported retained input')
        key='.' if p==path else str(p.relative_to(path))
        out[key]={'type':'directory' if p.is_dir() else 'file','mode':stat.S_IMODE(info.st_mode),'uid':info.st_uid,'gid':info.st_gid}
        if p.is_file():out[key]['sha256']=digest(p.read_bytes())
    return out
def verify_pair(tree,archive):
    note=read_json(tree/'raw/round-1/publication.json')
    expected={r['file']:r['sha256'] for r in note['files']}
    require(len(expected)==len(note['files']),'duplicate manifest names')
    expected['raw/round-1/publication.json']=digest((tree/'raw/round-1/publication.json').read_bytes())
    require({str(p.relative_to(tree)) for p in tree.rglob('*') if p.is_file()}==set(expected),'publication tree inventory mismatch')
    for name,value in expected.items():
        p=tree/name;require(not p.is_symlink() and digest(p.read_bytes())==value,'publication tree digest mismatch')
    with tarfile.open(archive,'r:gz') as bundle:
        members=bundle.getmembers();require(len(members)==len(expected),'archive entry count mismatch')
        require({m.name for m in members}==set(expected),'archive inventory mismatch')
        for m in members:
            require(m.isfile() and not P(m.name).is_absolute() and '..' not in P(m.name).parts,'unsafe archive entry')
            require(m.uid==m.gid==0 and m.uname==m.gname=='' and m.mode==0o644,'non-public archive metadata')
            require(digest(bundle.extractfile(m).read())==expected[m.name],'archive digest mismatch: '+m.name)
    return len(expected)
if MARKER.exists():
    marker=read_json(MARKER)
    require(marker=={'state':'prepared','stage':STAGE.name,'published':PUBLISHED.name,'temporary_archive':TAR_TMP.name,'archive':ARCHIVE.name},'unknown publication recovery journal')
    require(STAGE.exists()!=PUBLISHED.exists(),'ambiguous publication tree recovery')
    require(TAR_TMP.exists()!=ARCHIVE.exists(),'ambiguous publication archive recovery')
    verify_pair(STAGE if STAGE.exists() else PUBLISHED,TAR_TMP if TAR_TMP.exists() else ARCHIVE)
    if STAGE.exists():os.rename(STAGE,PUBLISHED)
    if TAR_TMP.exists():os.rename(TAR_TMP,ARCHIVE)
    syncdir(ROOT);MARKER.unlink();syncdir(ROOT)
    print(json.dumps({'recovered':True,'archive':ARCHIVE.name,'sha256':digest(ARCHIVE.read_bytes())}))
    raise SystemExit(0)
def completion():
    main=read_json(FINAL/'summary.json');supp=read_json(FINAL/'supplement/summary.json')
    require(main['controller_exit']==0 and not main['remaining_vms'] and not main['peer_remaining'],'main validation incomplete')
    require(supp['controller_exit']==0 and not supp['remaining_owned_vm'],'supplement incomplete')
    require(not (CANDIDATE/'round1-peer').exists(),'peer remains')
    require(not list((CANDIDATE/'vms').iterdir()) and not list((ROOT/'vms').iterdir()),'owned guests remain')
    for name in ('carried-suite/summary.json','carried-suite/regressions/summary.json','combined/summary.json','peer-image.json','input-sha256.json','image.json','steps.json'):
        require((FINAL/name).is_file(),'required completion evidence missing: '+name)
    for name in ('shell.jsonl','shell-reboot.jsonl','gate.jsonl','tools.jsonl','shell-verify.log','gate-verify.log','tools-verify.log','supplement/direct.jsonl','supplement/extra.jsonl'):
        require((FINAL/name).is_file(),'required component evidence missing: '+name)
    for name in ('combined/events.jsonl','supplement/reboot.json','supplement/before-reboot-verify.jsonl','supplement/after-reboot-verify.jsonl','supplement/before-report.json','supplement/after-report.json','supplement/input-sha256.json','supplement/image.json','supplement/steps.json','supplement/new.log','supplement/stop.log','supplement/start.log','supplement/destroy.log'):
        require((FINAL/name).is_file(),'required raw evidence missing: '+name)
    for name in ('language.jsonl','applications.jsonl','system.jsonl','ordinary.jsonl','regressions/round1.jsonl','regressions/round2.jsonl','regressions/round3.jsonl','regressions/powercuts.jsonl'):
        require((FINAL/'carried-suite'/name).is_file(),'required carried evidence missing: '+name)
    require(all(s['exit']==0 for s in main['steps']),'failed validation step')
    for name,empty in [('carried-suite/summary.json','owned_vms_remaining'),('carried-suite/regressions/summary.json','vms_remaining'),('combined/summary.json','owned_vms_remaining')]:
        value=read_json(FINAL/name)
        require(value['suite_exit']==0 and not value[empty],'incomplete stage: '+name)
completion()
for p in (ARCHIVE,PUBLISHED,STAGE,TAR_TMP):require(not p.exists(),'publication destination exists: '+p.name)
roots=[(ROOT/'raw/round-1','raw/round-1',True),(CANDIDATE/'raw/round-1','raw/round-1',True),(CANDIDATE/'round1-example','example/round-1',False)]
entries={}
for folder,target,redact in roots:
    require(folder.is_dir() and not folder.is_symlink(),'required publication root missing or linked')
    for path in sorted(folder.rglob('*')):
        require(not path.is_symlink(),'linked publication input')
        if path.is_dir():continue
        require(path.is_file(),'unsupported publication file type')
        name=str(P(target)/path.relative_to(folder))
        require(name not in entries,'merged publication collision: '+name)
        entries[name]=(path,redact)
require('raw/round-1/publication.json' not in entries,'publication manifest collision')
supplement_manifest='raw/round-1/final-2-supplement-source-sha256.json'
require(supplement_manifest in entries,'frozen supplement manifest missing')
frozen=read_json(entries[supplement_manifest][0])
require(set(frozen)=={'v4-direct-selftest.py','v4-extra-selftest.py'},'frozen supplement inventory differs')
require(frozen==read_json(FINAL/'supplement/input-sha256.json'),'executed and frozen supplement manifests differ')
supplement_prefix='raw/round-1/final-2-supplement-inputs/'
require({name[len(supplement_prefix):] for name in entries if name.startswith(supplement_prefix)}==set(frozen),'frozen supplement payload set differs')
for name,value in frozen.items():require(digest(entries[supplement_prefix+name][0].read_bytes())==value,'frozen supplement payload differs: '+name)
replacements=[(str(CANDIDATE),'[candidate-root]','candidate-root'),(str(ROOT),'[stand-root]','stand-root'),(str(P.home()),'[host-home]','host-home')]
inventory=[];normalization=[]
try:
    STAGE.mkdir()
    for name,(path,redact) in entries.items():
        data=path.read_bytes();before=digest(data);classes=[]
        try:text=data.decode('utf-8')
        except UnicodeDecodeError:text=None
        if text is not None:
            for old,new,label in replacements:
                if old in text:
                    protected=(not redact or 'recipe-inputs' in P(name).parts or 'supplement-inputs' in name or path.name.endswith('source-sha256.json') or path.name in ('machine.jsonl','base-files.json','input-sha256.json'))
                    require(not protected,'protected source/declaration requires normalization: '+name)
                    text=text.replace(old,new);classes.append(label)
            data=text.encode('utf-8')
        after=digest(data)
        if before!=after:normalization.append({'file':name,'pre_normalization_sha256':before,'published_sha256':after,'replacement_classes':classes})
        target=STAGE/name;target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
        inventory.append({'file':name,'bytes':len(data),'sha256':after})
    note={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'normalization':'Only actual host task-root/account-home prefixes replaced in separate publication copies; raw inputs are not modified. Frozen sources and complete declarations retain exact bytes.','changed_files':normalization,'files':inventory,'retained_inputs':{name:tree_inventory(CANDIDATE/name) for name in ('build','tools','lab.py')}}
    manifest=STAGE/'raw/round-1/publication.json';manifest.write_text(json.dumps(note,indent=2,sort_keys=True)+'\n')
    with manifest.open('rb') as stream:os.fsync(stream.fileno())
    expected={r['file']:r['sha256'] for r in inventory};expected[str(manifest.relative_to(STAGE))]=digest(manifest.read_bytes())
    def public_header(member):
        member.uid=member.gid=0;member.uname=member.gname='';member.mode=0o644
        return member
    with tarfile.open(TAR_TMP,'w:gz',compresslevel=1) as bundle:
        for name in sorted(expected):bundle.add(STAGE/name,arcname=name,recursive=False,filter=public_header)
    verify_pair(STAGE,TAR_TMP)
    with TAR_TMP.open('rb') as stream:os.fsync(stream.fileno())
    # A recovery marker makes the two final renames explicit if interrupted.
    for directory in sorted([STAGE]+[p for p in STAGE.rglob('*') if p.is_dir()],key=lambda p:len(p.parts),reverse=True):syncdir(directory)
    marker=MARKER
    require(not marker.exists(),'publication commit journal exists')
    marker.write_text(json.dumps({'state':'prepared','stage':STAGE.name,'published':PUBLISHED.name,'temporary_archive':TAR_TMP.name,'archive':ARCHIVE.name})+'\n')
    with marker.open('rb') as stream:os.fsync(stream.fileno())
    syncdir(ROOT)
    os.rename(STAGE,PUBLISHED);os.rename(TAR_TMP,ARCHIVE);syncdir(ROOT)
    marker.unlink();syncdir(ROOT)
except Exception:
    # No authoritative raw input is ever changed. A commit journal, if present,
    # identifies prepared/published names for inspection before recovery.
    if not (ROOT/'round1-publication-commit.json').exists():
        if STAGE.exists():shutil.rmtree(STAGE)
        if TAR_TMP.exists():TAR_TMP.unlink()
    raise
print(json.dumps({'archive':ARCHIVE.name,'published_tree':PUBLISHED.name,'files':len(inventory),'normalized':len(normalization),'bytes':ARCHIVE.stat().st_size,'sha256':digest(ARCHIVE.read_bytes()),'members':len(expected)}))
