#!/usr/bin/python3
"""Read-only check of exact private curl handoff inputs."""
import hashlib
import json
from pathlib import Path
import stat

root=Path.cwd();meta=json.loads((root/'curl-config-metadata-draft.json').read_text())
assert meta['package']=='curl' and meta['binary_version']==meta['source_version']=='8.14.1-2+deb13u7'
assert meta['target']=='/usr/bin/curl' and meta['mode']==0o755
items=meta['inputs']+meta['licences']+[
    {'path':meta['candidate_path'],'sha256':meta['sha256']},
    {'path':meta['original_executable_path'],'sha256':meta['original_sha256']}]
for item in items:
    path=root/item['path']
    assert path.resolve().is_relative_to(root/'interpreter-inputs/curl-config-draft')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],item['path']
assert stat.S_IMODE((root/meta['candidate_path']).stat().st_mode)==meta['mode']
assert 'CURL_CONFIG_PRIVATE39_GUEST_MATRIX_PASS 32' in (root/meta['guest_evidence']).read_text()
print('CURL_CONFIG_EXACT_HANDOFF_METADATA_PASS',len(items))
