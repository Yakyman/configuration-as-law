"""Make the two bundles of the `linuxgsm` line (build/DECLARATION.md revision 18+: "BUNDLE is a tar containing
manifest.json, initial.tar.gz, target.tar.gz, game.tar.xz, common.cfg and wetserver.cfg. The manifest names the
initial/target source commits, exact releases and the three inner archive checksums"), in the folder DIR given, from
the upstream archives fetched there by tools/make-inputs.sh (step game) and the two default configurations of the
published release source. The checksums of the upstream archives are those the published release names for them.

Usage: python3 -I tools/make-game-bundle.py DIR
"""
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile

d = Path(sys.argv[1])
initial = '50dc4e551b661b9d1fa39c291068a16a66056aff'
releases = {'26.5.0': (initial, 'd100627a4b660a499cc717cba8c19ff41dc60fea744f704f1f2de9c1bf2f0424'),
            '26.6.0': ('9ca2e951c6e15d4db7184a60e1fd8a831b2cdb0f',
                       'd88eb97ba929db614971fc8bd09428b6225c741d385efd56d312ae5dd6ac1336')}
game_sha = 'ac359aebe0bf8fd568341876e3a8992d7c562ee6fdc4a8906bdbab47eae66cf3'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


for release, (commit, checksum) in releases.items():
    files = {'initial.tar.gz': d / 'linuxgsm-26.5.0.tar.gz', 'target.tar.gz': d / f'linuxgsm-{release}.tar.gz',
             'game.tar.xz': d / 'wet-2.60b.tar.xz', 'common.cfg': d / 'game-common.cfg',
             'wetserver.cfg': d / 'game-server.cfg'}
    expected = {'initial.tar.gz': releases['26.5.0'][1], 'target.tar.gz': checksum, 'game.tar.xz': game_sha}
    for name, digest in expected.items():
        got = sha(files[name])
        if got != digest:
            sys.exit(f'{files[name].name}: sha256 {got}, expected {digest}')
    manifest = json.dumps({'schema': 1, 'release': release, 'initial_commit': initial, 'target_commit': commit,
                           'game_release': '2.60b', 'sha256': expected}, sort_keys=True).encode() + b'\n'
    out = d / f'linuxgsm-wet-{release}.tar'
    with tarfile.open(out, 'w') as archive:
        for name in sorted([*files, 'manifest.json']):
            info = tarfile.TarInfo(name)
            info.mode = 0o644
            info.mtime = 1795392000
            data = manifest if name == 'manifest.json' else files[name].read_bytes()
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    print(sha(out), out.name)
