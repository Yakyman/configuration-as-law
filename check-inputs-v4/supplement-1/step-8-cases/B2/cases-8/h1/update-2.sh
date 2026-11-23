#!/bin/bash
set -eu
printf 'ACTION_BEGIN h1.update-2\n'
python3 -B - <<'PY'
import hashlib,pathlib,urllib.request
url='https://deb.debian.org/debian/pool/main/e/ed/ed_1.22.5-1_amd64.deb'
with urllib.request.urlopen(url,timeout=60) as response:
    data=response.read()
assert hashlib.sha256(data).hexdigest()=='593a7915c2ec0e3c87f824c2b11b4f72d3d74d654183c6833a18c4320e5df6a0'
pathlib.Path('/tmp/ed_1.22.5-1_amd64.deb').write_bytes(data)
print('FETCH_VERIFIED',len(data),hashlib.sha256(data).hexdigest())
PY
/usr/bin/dpkg --install /tmp/ed_1.22.5-1_amd64.deb
test "$(/usr/bin/dpkg-query -W '-f=${Version}' ed)" = 1.22.5-1
/usr/bin/dpkg-query -W '-f=${Package} ${Version} ${db:Status-Status}\n' ed
printf 'ACTION_DONE h1.update-2\n'
