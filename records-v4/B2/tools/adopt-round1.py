#!/usr/bin/env python3
"""Adopt accepted Round 1 files through staged, journaled swaps; no guest work."""
import fcntl,hashlib,json,os,pathlib,shutil,stat,tarfile,time
P=pathlib.Path
ROOT=P(__file__).resolve().parent.parent
CANDIDATE=ROOT/'candidate-1'
PUBLISHED=ROOT/'round1-publication'
WORK=ROOT/'round1-adoption.tmp'
JOURNAL=ROOT/'round1-adoption-journal.json'
ACCEPT=ROOT/'round1-acceptance.json'
lock=(ROOT/'locks/round1-packaging.lock').open('a')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
def require(condition,message):
    if not condition:raise RuntimeError(message)
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def read(path):return json.loads(path.read_text())
def syncdir(path):
    fd=os.open(path,os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
def atomic_json(path,obj):
    temp=path.with_name(path.name+'.tmp')
    fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_TRUNC|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'w') as stream:json.dump(obj,stream,indent=2,sort_keys=True);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    os.replace(temp,path);syncdir(path.parent)
def inventory(path):
    require(path.exists() and not path.is_symlink(),'missing or linked inventory root')
    items=[path]+(sorted(path.rglob('*')) if path.is_dir() else [])
    out={}
    for item in items:
        info=item.lstat();rel='.' if item==path else str(item.relative_to(path))
        require(stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode),'unsupported file type in '+rel)
        out[rel]={'type':'directory' if item.is_dir() else 'file','mode':stat.S_IMODE(info.st_mode),'uid':info.st_uid,'gid':info.st_gid}
        if item.is_file():out[rel]['sha256']=sha(item)
    return out
def copy_exact(source,dest):
    if source.is_dir():shutil.copytree(source,dest)
    else:shutil.copy2(source,dest)
    require(inventory(source)==inventory(dest),'staged copy differs')
    for item in ([dest]+list(dest.rglob('*')) if dest.is_dir() else [dest]):
        if item.is_file():
            with item.open('rb') as stream:os.fsync(stream.fileno())
    if dest.is_dir():
        for item in sorted([dest]+[p for p in dest.rglob('*') if p.is_dir()],key=lambda p:len(p.parts),reverse=True):syncdir(item)
def remove(path):
    if path.is_dir():shutil.rmtree(path)
    elif path.exists():path.unlink()
def finish_cleanup(journal):
    require(journal['state']=='committed','cleanup requires committed journal')
    record=ROOT/'raw/round-1/adoption.json'
    require(record.is_file(),'committed adoption record missing')
    for name in ('candidate-1','round1-publication','round1-adoption.tmp','round1-publication.tar.gz','round1-acceptance.json','round1-metrics.json','round1-final-review.md'):
        remove(ROOT/name)
    data=read(record);data.update(cleanup_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),candidate_duplicate_removed=True,publication_staging_removed=True,backup_removed=True)
    atomic_json(record,data)
    JOURNAL.unlink();syncdir(ROOT)
    print(json.dumps(data,sort_keys=True))
def rollback(journal):
    for op in reversed(journal['operations']):
        target=ROOT/op['target'];fresh=WORK/op['new'];old=WORK/op['old']
        if old.exists():
            require(inventory(old)==op['previous'],'rollback backup mismatch')
            if target.exists():
                require(inventory(target)==op['candidate'],'unexpected replacement during rollback')
                require(not fresh.exists(),'duplicate staged candidate')
                os.rename(target,fresh);syncdir(target.parent);syncdir(fresh.parent)
            os.rename(old,target);syncdir(target.parent);syncdir(old.parent)
        elif op['previous'] is None:
            if target.exists():
                require(inventory(target)==op['candidate'] and not fresh.exists(),'unexpected new target')
                os.rename(target,fresh);syncdir(target.parent);syncdir(fresh.parent)
        else:require(inventory(target)==op['previous'],'original target missing or changed')
    remove(WORK);JOURNAL.unlink();syncdir(ROOT)
    raise SystemExit('Interrupted adoption rolled back; original retained files restored. Re-run only after inspection.')
if JOURNAL.exists():
    journal=read(JOURNAL)
    if journal['state']=='committed':finish_cleanup(journal)
    else:rollback(journal)
    raise SystemExit(0)
require(not WORK.exists(),'uncommitted staging tree requires inspection')
require(not (ROOT/'round1-publication-commit.json').exists(),'publication commit incomplete')
final=CANDIDATE/'raw/round-1/final-2'
main=read(final/'summary.json');supp=read(final/'supplement/summary.json')
require(main['controller_exit']==0 and not main['remaining_vms'] and not main['peer_remaining'],'main validation incomplete')
require(all(s['exit']==0 for s in main['steps']),'failed main step')
require(supp['controller_exit']==0 and not supp['remaining_owned_vm'],'supplement incomplete')
require(not list((ROOT/'vms').iterdir()) and not list((CANDIDATE/'vms').iterdir()),'owned guests remain')
require(not (CANDIDATE/'round1-peer').exists(),'peer root remains')
for name,empty in [('carried-suite/summary.json','owned_vms_remaining'),('carried-suite/regressions/summary.json','vms_remaining'),('combined/summary.json','owned_vms_remaining')]:
    value=read(final/name);require(value['suite_exit']==0 and not value[empty],'validation summary incomplete: '+name)
identity=read(final/'image.json')
require(sha(CANDIDATE/'base/stand.qcow2')==identity['sha256'],'candidate image identity mismatch')
require(stat.S_IMODE((CANDIDATE/'base/stand.qcow2').stat().st_mode)==0o444,'candidate image must be read-only')
require(inventory(CANDIDATE/'keys')==inventory(ROOT/'keys'),'key inventories differ')
require((ROOT/'example').is_symlink() and (ROOT/'example').readlink()==P('channel-example'),'unexpected example parent')
require((ROOT/'example').resolve()==ROOT/'channel-example','example parent escapes retained root')
require(not (ROOT/'channel-example/round-1').exists(),'example destination already exists')
acceptance=read(ACCEPT)
acceptance_digest=sha(ACCEPT)
require(acceptance.get('accepted') is True and acceptance.get('image_sha256')==identity['sha256'],'independent acceptance missing/mismatched')
for name,key in [('round1-metrics.json','metrics_sha256'),('round1-final-review.md','review_sha256')]:
    require(sha(ROOT/name)==acceptance[key],'acceptance artifact mismatch: '+name)
require(sha(PUBLISHED/'raw/round-1/publication.json')==acceptance['publication_sha256'],'accepted publication differs')
require(sha(final/'input-sha256.json')==acceptance['input_manifest_sha256'],'accepted recipe identity differs')
require(read(ROOT/'round1-metrics.json')['controller']['controller_exit']==0,'accepted metrics incomplete')
manifest=read(PUBLISHED/'raw/round-1/publication.json')
expected={r['file']:r['sha256'] for r in manifest['files']}
require(len(expected)==len(manifest['files']),'duplicate publication paths')
actual={str(p.relative_to(PUBLISHED)) for p in PUBLISHED.rglob('*') if p.is_file()}
require(actual==set(expected)|{'raw/round-1/publication.json'},'publication inventory differs')
for name,digest in expected.items():require(sha(PUBLISHED/name)==digest,'published file mismatch: '+name)
archive=ROOT/'round1-publication.tar.gz'
require(sha(archive)==acceptance['archive_sha256'],'accepted archive digest mismatch')
archive_expected={**expected,'raw/round-1/publication.json':acceptance['publication_sha256']}
with tarfile.open(archive,'r:gz') as bundle:
    members=bundle.getmembers()
    require(len(members)==acceptance['archive_members']==len(archive_expected),'accepted archive count mismatch')
    require({m.name for m in members}==set(archive_expected),'accepted archive inventory mismatch')
    for item in members:
        require(item.isfile() and not P(item.name).is_absolute() and '..' not in P(item.name).parts,'unsafe accepted archive entry')
        require(item.uid==item.gid==0 and item.uname==item.gname=='' and item.mode==0o644,'non-public archive metadata')
        require(hashlib.sha256(bundle.extractfile(item).read()).hexdigest()==archive_expected[item.name],'accepted archive member mismatch')
accepted_inputs=manifest['retained_inputs']
require(set(accepted_inputs)=={'build','tools','lab.py'},'accepted operational source incomplete')
for name,items in accepted_inputs.items():require(inventory(CANDIDATE/name)==items,'accepted operational source differs: '+name)
inputs=read(final/'input-sha256.json')
require({p.name:sha(p) for p in (CANDIDATE/'build').iterdir() if p.is_file()}==inputs,'candidate recipe changed')
for p in (CANDIDATE/'build').iterdir():require(p.is_file() and not p.is_symlink(),'unexpected recipe entry')
# Fully preflighted destinations; raw publication contains both source raw trees.
sources=[(CANDIDATE/'build','build'),(CANDIDATE/'tools','tools'),(CANDIDATE/'lab.py','lab.py'),(CANDIDATE/'base/stand.qcow2','base/stand.qcow2'),(PUBLISHED/'raw/round-1','raw/round-1'),(PUBLISHED/'example/round-1','channel-example/round-1')]
for source,name in sources:
    inventory(source);target=ROOT/name
    require(target.parent.is_dir() and not target.is_symlink(),'unsafe adoption target: '+name)
    if target.exists():inventory(target)
WORK.mkdir();(WORK/'new').mkdir();(WORK/'old').mkdir()
operations=[]
record={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'retained_image':'base/stand.qcow2','sha256':identity['sha256'],'mode':'0o444','retained_recipe':'build/','example':'example/round-1/','remaining_owned_vms':[],'candidate_duplicate_removed':False,'hypothesis_outcome':'?','acceptance':'acceptance.json','publication':'publication.json','recipe_files':len(inputs)}
try:
    for index,(source,name) in enumerate(sources):
        dest=WORK/'new'/str(index);copy_exact(source,dest)
        if name=='raw/round-1':
            for external,inside in [(ACCEPT,'acceptance.json'),(ROOT/'round1-metrics.json','metrics.json'),(ROOT/'round1-final-review.md','REVIEW-FINAL.md')]:
                require(not (dest/inside).exists(),'new publication record collision: '+inside)
                shutil.copy2(external,dest/inside)
                with (dest/inside).open('rb') as stream:os.fsync(stream.fileno())
            syncdir(dest)
            atomic_json(dest/'adoption.json',record)
            require(sha(dest/'acceptance.json')==acceptance_digest,'staged acceptance changed')
            require(sha(dest/'metrics.json')==acceptance['metrics_sha256'],'staged metrics changed')
            require(sha(dest/'REVIEW-FINAL.md')==acceptance['review_sha256'],'staged review changed')
            require(sha(dest/'publication.json')==acceptance['publication_sha256'],'staged publication manifest changed')
        if name in accepted_inputs:require(inventory(dest)==accepted_inputs[name],'staged operational source changed: '+name)
        if name=='base/stand.qcow2':
            require(sha(dest)==identity['sha256'] and stat.S_IMODE(dest.stat().st_mode)==0o444,'staged image changed')
        if name in ('raw/round-1','channel-example/round-1'):
            prefix='raw/round-1/' if name=='raw/round-1' else 'example/round-1/'
            required={k[len(prefix):]:v for k,v in expected.items() if k.startswith(prefix)}
            extras={'publication.json','acceptance.json','metrics.json','REVIEW-FINAL.md','adoption.json'} if name=='raw/round-1' else set()
            require({str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file()}==set(required)|extras,'staged publication inventory changed')
            for relative,digest in required.items():require(sha(dest/relative)==digest,'staged publication content changed')
        operations.append({'target':name,'new':'new/'+str(index),'old':'old/'+str(index),'candidate':inventory(dest),'previous':inventory(ROOT/name) if (ROOT/name).exists() else None})
    for name,items in accepted_inputs.items():require(inventory(CANDIDATE/name)==items,'operational source changed during staging')
    require(sha(ACCEPT)==acceptance_digest and sha(archive)==acceptance['archive_sha256'],'acceptance/archive changed during staging')
    require(not list((ROOT/'vms').iterdir()) and not list((CANDIDATE/'vms').iterdir()),'guest appeared during staging')
    journal={'state':'prepared','operations':operations,'image_sha256':identity['sha256']}
    atomic_json(JOURNAL,journal)
    for op in operations:
        target=ROOT/op['target'];fresh=WORK/op['new'];old=WORK/op['old']
        if target.exists():os.rename(target,old);syncdir(target.parent);syncdir(old.parent)
        os.rename(fresh,target);syncdir(target.parent);syncdir(fresh.parent)
    for op in operations:require(inventory(ROOT/op['target'])==op['candidate'],'committed inventory mismatch')
    journal['state']='committed';atomic_json(JOURNAL,journal)
except Exception:
    # Original targets remain in durable backups. Next invocation rolls back
    # any interrupted pre-commit sequence, based on exact inventories.
    if not JOURNAL.exists():remove(WORK)
    raise
finish_cleanup(journal)
