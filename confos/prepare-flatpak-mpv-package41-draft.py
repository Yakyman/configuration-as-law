#!/usr/bin/python3
"""Sealed40-gated additive future41 component, restricted to private draft output."""
import gzip,hashlib,json,os,subprocess,tarfile,tempfile
from pathlib import Path
root=Path.cwd()
draft=root/'interpreter-inputs/flatpak-mpv-integration41-draft'
archive=root/'releases/confos-0.40-source.tar.gz'
seal=root/'releases/release-0.40.sha256'
baseline=root/'packages/confos-code-readers_0.40_amd64.deb'
def digest(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()
assert archive.is_file() and seal.is_file(), 'sealed40 baseline unavailable; no composition allowed'
lines=[line.split() for line in seal.read_text().splitlines()]
hashes=[row[0] for row in lines if len(row)==2 and row[1].lstrip('*')=='releases/confos-0.40-source.tar.gz']
assert len(hashes)==1 and digest(archive)==hashes[0], 'sealed40 archive checksum mismatch'
with tarfile.open(archive) as tar:
    assert tar.extractfile('VERSION').read()==b'0.40\n'
    assert tar.extractfile('packages/confos-code-readers_0.40_amd64.deb').read()==baseline.read_bytes()
    source=tar.extractfile('flatpak_readers.py').read()
draft.mkdir(exist_ok=True)
(draft/'sealed40-flatpak_readers.py').write_bytes(source)
subprocess.run(['python3','patch-flatpak-app-ref41-draft.py',str(draft/'sealed40-flatpak_readers.py'),str(draft/'source/flatpak_readers.py')],check=True)
assert digest(draft/'mpv-app-overrides.json')=='4ada6b113190b3cbf44ddaec16be03967fc05224c66ab89566cca94b5d8da0bf'
rows=json.loads((draft/'mpv-app-overrides.json').read_text())
assert len(rows)==3 and len({x['target'] for x in rows})==3
assert {x['ref'] for x in rows}=={'app/io.mpv.Mpv/x86_64/stable'}
epoch=1795392000
manifest_name='usr/lib/confos/flatpak-reader-overrides/manifest.json'
output=draft/'confos-code-readers_0.41_amd64.deb'
assert not output.exists(), 'private output already exists; inspect it instead of overwriting'
with tempfile.TemporaryDirectory(prefix='compose-',dir=draft) as temp:
    stage=Path(temp)/'root'
    subprocess.run(['dpkg-deb','-R',str(baseline),str(stage)],check=True)
    manifest=stage/manifest_name; original=json.loads(manifest.read_text())
    assert len(original)==3 and all(x['ref'].startswith('runtime/') for x in original)
    appended=[]
    for row in rows:
        item={k:row[k] for k in ('ref','commit','bundle_sha256','target','original_sha256','sha256','objects','mode','payload')}
        assert not any(x['ref']==item['ref'] and x['commit']==item['commit'] and x['target']==item['target'] for x in original)
        assert item['mode']==0o755 and '/' not in item['payload']
        path=manifest.parent/item['payload']; assert not path.exists()
        data=(root/row['candidate_worker_path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==item['sha256']
        path.write_bytes(gzip.compress(data,compresslevel=9,mtime=epoch));path.chmod(0o644)
        appended.append(item)
    manifest.write_text(json.dumps(original+appended,indent=2,sort_keys=True)+'\n')
    namespace={}
    exec(compile((draft/'source/flatpak_readers.py').read_text(),'private-flatpak-readers','exec'),namespace)
    assert namespace['_items'](stage)==original+appended
    docs=stage/'usr/share/doc/confos-code-readers/mpv41'
    docs.mkdir()
    for path in [draft/'mpv-app-overrides.json',root/'flatpak-mpv-continuation-draft.md',root/'flatpak-mpv-integration41-draft.md',root/'patch-flatpak-app-ref41-draft.py',root/'patch-mpv-lua-stream-draft.py',root/'patch-luajit-code.py',root/'code-file-policy.h']:
        (docs/path.name).write_bytes(path.read_bytes())
    control=stage/'DEBIAN/control';text=control.read_text()
    assert text.count('Version: 0.40\n')==1 and 'Package: confos-code-readers\n' in text
    control.write_text(text.replace('Version: 0.40\n','Version: 0.41\n'))
    # Preserve every inherited mode, owner and link; normalize timestamps only.
    for path in [*stage.rglob('*'),stage]: os.utime(path,(epoch,epoch),follow_symlinks=False)
    subprocess.run(['dpkg-deb','--root-owner-group','-Zxz','-z6','--build',str(stage),str(output)],check=True,env={**os.environ,'SOURCE_DATE_EPOCH':str(epoch)})
output.with_suffix('.deb.sha256').write_text(digest(output)+'\n')
(draft/'composition-provenance.json').write_text(json.dumps({'baseline_archive_sha256':hashes[0],'baseline_component_sha256':digest(baseline),'draft_component_sha256':digest(output),'inherited_rows':original,'appended_rows':appended,'baseline_module_sha256':hashlib.sha256(source).hexdigest(),'patched_module_sha256':digest(draft/'source/flatpak_readers.py')},indent=2)+'\n')
subprocess.run(['python3','verify-flatpak-mpv-package41-draft.py'],check=True)
print('PRIVATE_FUTURE41_COMPONENT_PREPARED; no main transition or guest test')
