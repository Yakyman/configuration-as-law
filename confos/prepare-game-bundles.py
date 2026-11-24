#!/usr/bin/python3
"""Package pinned upstream source inputs and authored defaults, never saved output."""
import hashlib
import io
import json
from pathlib import Path
import tarfile

base = Path(__file__).resolve().parent
inputs = base/'game-inputs'
initial = '50dc4e551b661b9d1fa39c291068a16a66056aff'
releases = {
    '26.5.0': (initial, 'd100627a4b660a499cc717cba8c19ff41dc60fea744f704f1f2de9c1bf2f0424'),
    '26.6.0': ('9ca2e951c6e15d4db7184a60e1fd8a831b2cdb0f', 'd88eb97ba929db614971fc8bd09428b6225c741d385efd56d312ae5dd6ac1336'),
}
game_sha = 'ac359aebe0bf8fd568341876e3a8992d7c562ee6fdc4a8906bdbab47eae66cf3'
for release, (commit, checksum) in releases.items():
    files = {'initial.tar.gz': inputs/'linuxgsm-26.5.0.tar.gz',
             'target.tar.gz': inputs/f'linuxgsm-{release}.tar.gz',
             'game.tar.xz': inputs/'wet-2.60b.tar.xz',
             'common.cfg': base/'game-common.cfg', 'wetserver.cfg': base/'game-server.cfg'}
    expected = {'initial.tar.gz': releases['26.5.0'][1], 'target.tar.gz': checksum, 'game.tar.xz': game_sha}
    for name, digest in expected.items():
        with files[name].open('rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest, name
    manifest = json.dumps({'schema': 1, 'release': release, 'initial_commit': initial,
        'target_commit': commit, 'game_release': '2.60b', 'sha256': expected}, sort_keys=True).encode()+b'\n'
    output = inputs/f'linuxgsm-wet-{release}.tar'
    with tarfile.open(output, 'w') as archive:
        for name in sorted([*files, 'manifest.json']):
            info = tarfile.TarInfo(name)
            info.mode = 0o644
            info.mtime = 1795392000
            if name == 'manifest.json':
                info.size = len(manifest)
                archive.addfile(info, io.BytesIO(manifest))
            else:
                info.size = files[name].stat().st_size
                with files[name].open('rb') as stream:
                    archive.addfile(info, stream)
    with output.open('rb') as stream:
        print(hashlib.file_digest(stream, 'sha256').hexdigest(), output.name, flush=True)
