#!/usr/bin/python3
"""Compose named code-reader component with exact Flatpak replacement payloads."""
import gzip,hashlib,json,os,re,subprocess,sys,tempfile
from pathlib import Path
version,baseline_name,baseline_digest,manifest_name,output_name=sys.argv[1:]
baseline,manifest_path,output=map(Path,(baseline_name,manifest_name,output_name))
assert re.fullmatch(r'[0-9]+[.][0-9]+',version)
assert hashlib.sha256(baseline.read_bytes()).hexdigest()==baseline_digest
candidate=json.loads(manifest_path.read_text())
output=output.resolve()
output.parent.mkdir(parents=True,exist_ok=True)
epoch=1795392000
with tempfile.TemporaryDirectory(prefix='flatpak-readers-',dir=output.parent) as temp:
    root=Path(temp)/'root'
    subprocess.run(['dpkg-deb','-R',baseline,root],check=True)
    directory=root/'usr/lib/confos/flatpak-reader-overrides'
    directory.mkdir()
    items=[]
    for index,row in enumerate(candidate['readers']):
        source=Path(row['candidate_worker_path'])
        data=source.read_bytes()
        assert hashlib.sha256(data).hexdigest()==row['candidate_sha256']
        payload=f'reader-{index}.gz'
        (directory/payload).write_bytes(gzip.compress(data,compresslevel=9,mtime=epoch))
        prefix=candidate['runtime_ref']+'/'+candidate['commit']+'/files/'
        assert row['target'].startswith(prefix)
        items.append(dict(ref=candidate['runtime_ref'],commit=candidate['commit'],
            bundle_sha256=candidate['runtime_bundle_sha256'],target=row['target'][len(prefix):],
            original_sha256=row['sha256'],objects=row['object_paths'],payload=payload,
            sha256=row['candidate_sha256'],mode=0o755))
    (directory/'manifest.json').write_text(json.dumps(items,sort_keys=True,indent=2)+'\n')
    docs=root/'usr/share/doc/confos-code-readers/flatpak'
    docs.mkdir(parents=True)
    for name in ('flatpak-reader-candidate-manifest.json','flatpak-reader-provenance-draft.md',
                 'flatpak-python-shared-draft.md','flatpak-bash-compatible-draft.md',
                 'patch-flatpak-python.py','patch-python-code.py','patch-flatpak-bash.py',
                 'code-file-policy.h','build-flatpak-python-shared.sh',
                 'build-flatpak-bash-compatible.sh','link-flatpak-bash-compatible.sh',
                 'flatpak_readers.py','package-flatpak-reader-overrides.py'):
        (docs/name).write_bytes(Path(name).read_bytes())
    for label,path in [('bash-COPYING','interpreter-inputs/flatpak-bash-compatible/COPYING'),
                       ('python-LICENSE','interpreter-inputs/flatpak-python-shared/LICENSE')]:
        (docs/label).write_bytes(Path(path).read_bytes())
    patchbase=Path('interpreter-inputs/flatpak-sdk-provenance/89e0d095f472b2620f985f509b263e2b4d853d5a/patches')
    for path in (patchbase/'bash/0001-bash-config.patch',patchbase/'python3/python3-multiarch-include.patch'):
        (docs/path.name).write_bytes(path.read_bytes())
    control=root/'DEBIAN/control'
    assert 'Package: confos-code-readers\n' in control.read_text()
    control.write_text(re.sub(r'^Version: .+$','Version: '+version,control.read_text(),flags=re.M))
    for path in [*root.rglob('*'),root]:
        if path.is_dir(): path.chmod(0o755)
        elif not path.is_symlink() and not path.stat().st_mode&0o111: path.chmod(0o644)
        os.utime(path,(epoch,epoch),follow_symlinks=False)
    artifact=Path(temp)/'payload.deb'
    subprocess.run(['dpkg-deb','--root-owner-group','--uniform-compression','-Zgzip','-z9','--build',root,artifact],check=True,
        env=dict(os.environ,SOURCE_DATE_EPOCH=str(epoch),TZ='UTC',LC_ALL='C'))
    digest=hashlib.sha256(artifact.read_bytes()).hexdigest()
    os.replace(artifact,output)
    output.with_suffix('.deb.sha256').write_text(digest+'\n')
    print('FLATPAK READER COMPONENT',digest,output.name)

