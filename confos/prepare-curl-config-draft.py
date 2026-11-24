#!/usr/bin/python3
"""Fetch only exact cached-index curl inputs into a new private draft subtree."""
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

root = Path.cwd()
work = root/'interpreter-inputs/curl-config-draft'
work.mkdir(exist_ok=True)
sources = root/'interpreter-inputs/git/apt/lists/snapshot.debian.org_archive_debian_20261123T000000Z_dists_trixie_main_source_Sources'
packages = root/'images/confos-0.40-clean.work/apt/lists/snapshot.debian.org_archive_debian_20261123T000000Z_dists_trixie_main_binary-amd64_Packages'
version = '8.14.1-2+deb13u7'
source = next(x for x in sources.read_text().split('\n\n') if x.startswith('Package: curl\n') and '\nVersion: '+version+'\n' in x)
package = next(x for x in packages.read_text().split('\n\n') if x.startswith('Package: curl\n') and '\nVersion: '+version+'\n' in x)
(work/'source-index.txt').write_text(source+'\n')
(work/'package-index.txt').write_text(package+'\n')
inputs = {}
for name, expected in [
    ('curl_8.14.1-2+deb13u7.dsc', 'a559b829ff852b2ee1ac0e448b5d9c18e0f94875bc820d037609d4d807ac6f57'),
    ('curl_8.14.1.orig.tar.gz', '6766ada7101d292b42b8b15681120acd68effa4a9660935853cf6d61f0d984d4'),
    ('curl_8.14.1.orig.tar.gz.asc', '39cc2ec8ddc39d04e3e7101bbed46d858d0875cbb297a6bfa20959fa2bc7d5c7'),
    ('curl_8.14.1-2+deb13u7.debian.tar.xz', 'e0f627ee2b9ae61078b2835edc25c8b94a0b57e180a1bc72dd8636ef260c370b'),
    ('curl_8.14.1-2+deb13u7_amd64.deb', '135636bd8b713c582d33e50ec4e36ea55cc3c5da3f12bbeb6b87d2bcbd3a0649'),
]:
    assert expected in (package if name.endswith('.deb') else source)
    url = 'https://snapshot.debian.org/archive/debian/20261123T000000Z/pool/main/c/curl/'+name
    path = work/name
    if not path.exists():
        with urllib.request.urlopen(url, timeout=90) as response:
            data = response.read()
        assert hashlib.sha256(data).hexdigest() == expected, name
        path.write_bytes(data)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name
    inputs[name] = {'sha256': expected, 'url': url}
    print('VERIFIED', name, expected, flush=True)
(work/'input-provenance.json').write_text(json.dumps({'version': version, 'inputs': inputs,
    'source_index_sha256': hashlib.sha256(sources.read_bytes()).hexdigest(),
    'package_index_sha256': hashlib.sha256(packages.read_bytes()).hexdigest()}, indent=2)+'\n')
if not (work/'source').exists():
    subprocess.run(['dpkg-source', '--no-check', '-x', 'curl_8.14.1-2+deb13u7.dsc', 'source'], cwd=work, check=True)
print('EXACT_CURL_CONFIG_SOURCE_EXTRACTED; no compilation')
