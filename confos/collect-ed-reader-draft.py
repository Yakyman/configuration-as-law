#!/usr/bin/python3
"""Preserve private ed evidence, then remove only its disposable trees."""
import hashlib,json,shutil,subprocess as sp
from pathlib import Path
root=Path.cwd();work=root/'interpreter-inputs/ed-reader-draft'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sp.check_output(['systemctl','--user','show','confos-ed-reader-guest-draft','-p','ActiveState','--value'],text=True).strip() in ('inactive','failed')
log=(work/'guest-build-run.log').read_text()
assert 'ED_READER_PRIVATE41_PIPELINE_PASS' in log
evidence=work/'evidence';evidence.mkdir(exist_ok=True)
for path in work.glob('*.log'):
    (evidence/path.name).write_text(path.read_text().replace(str(root),'<build>'))
for folder in ('build-tree-first-failure','build-tree-second-failure','build-tree'):
    dest=evidence/folder;dest.mkdir(exist_ok=True)
    for name in ('main_loop.c','Makefile.in','confos-ed-reader-policy.h','confos-ed-reader-policy.c'):
        p=work/folder/name
        if p.exists():shutil.copyfile(p,dest/name)
guest=work/'guest'
archives=guest/'disk.work/apt/archives'
assert digest(archives/'ed_1.21.1-1_amd64.deb')==json.loads((work/'input-pins.json').read_text())['ed_1.21.1-1_amd64.deb']
libc=next(archives.glob('libc6_*.deb'));libc_copy=work/libc.name
shutil.copyfile(libc,libc_copy)
libc_tree=work/'libc-verification';sp.run(['dpkg-deb','-x',str(libc_copy),str(libc_tree)],check=True)
library_report={'archive':libc.name,'archive_sha256':digest(libc_copy),'files':{}}
for relative in ('usr/lib/x86_64-linux-gnu/libc.so.6','usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2'):
    expected=digest(libc_tree/relative)
    assert digest(guest/'disk.work/root'/relative)==expected
    library_report['files'][relative]=expected
(evidence/'guest-unchanged-libraries.json').write_text(json.dumps(library_report,indent=2)+'\n')
shutil.rmtree(libc_tree)
for name in ('composition.json','inputs'):
    p=guest/name;dest=evidence/name
    if p.is_dir():shutil.copytree(p,dest,dirs_exist_ok=True)
    else:shutil.copyfile(p,dest)
shutil.copyfile(root/'code-file-policy.h',work/'code-file-policy.h')
comparison=json.loads((work/'comparison.json').read_text())
metadata={'package':'ed','binary_version':'1.21.1-1','source_version':'1.21.1-1',
 'target':'/usr/bin/ed','mode':0o755,'original_sha256':comparison['original']['sha256'],
 'sha256':comparison['candidate']['sha256'],'candidate_path':'interpreter-inputs/ed-reader-draft/candidate/ed',
 'red':{'target':'/usr/bin/red','sha256':digest(work/'original/usr/bin/red'),'type':'regular shell launcher','unchanged':True},
 'inputs':[{'path':str((work/name).relative_to(root)),'sha256':sha} for name,sha in json.loads((work/'input-pins.json').read_text()).items()],
 'licences':[{'path':str(p.relative_to(root)),'sha256':digest(p)} for p in (work/'source/COPYING',work/'source/debian/copyright')],
 'reader_policy':{'path':'interpreter-inputs/ed-reader-draft/code-file-policy.h','sha256':digest(work/'code-file-policy.h')},
 'recipe':[{'path':name,'sha256':digest(root/name)} for name in ('prepare-ed-reader-draft.py','build-ed-reader-draft.py','verify-ed-reader-abi-draft.py','build-ed-reader-guest-draft.py','run-ed-reader-guest-draft.sh','probe-ed-reader-guest-draft.py','collect-ed-reader-draft.py')],
 'guest_libraries':library_report,
 'baseline_source':{'path':'releases/confos-0.41-source.tar.gz','sha256':'2c73f6a664a2754cc78a7244d31bb77c7ac3d5253f45653a3c12cdfb418e4ca9'},
 'comparison':comparison,'guest_evidence':'interpreter-inputs/ed-reader-draft/evidence/guest-build-run.log',
 'status':'private native and guest proof only; independent case review and numbered integration pending'}
(work/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
for name in ('build-tree-first-failure','build-tree-second-failure','build-tree','guest'):
    shutil.rmtree(work/name)
print('ED_READER_EVIDENCE_AND_CLEANUP_PASS',digest(work/'metadata.json'))
