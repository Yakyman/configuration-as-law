#!/usr/bin/python3
"""Exercise a future guard against an incompatible original package payload."""
import gzip
import hashlib
import json
from pathlib import Path
import runpy
import tempfile

text = Path('optional_readers.py').read_text()
if "original = item.get('original_sha256')" not in text:
    text = runpy.run_path('patch-optional-identity-042.py')['patched'](text)
module = {}
exec(compile(text, 'future42-optional_readers.py', 'exec'), module)
digest = lambda data: hashlib.sha256(data).hexdigest()
with tempfile.TemporaryDirectory(prefix='confos-identity-check-') as temp:
    root = Path(temp)
    target = root/'usr/bin/example'; target.parent.mkdir(parents=True)
    directory = root/'usr/lib/confos/reader-overrides'; directory.mkdir(parents=True)
    old = b'pinned-original'; incompatible = b'other-package-release'; new = b'guarded-reader'
    target.write_bytes(incompatible)
    (directory/'reader.gz').write_bytes(gzip.compress(new, mtime=0))
    (directory/'manifest.json').write_text(json.dumps([dict(package='example',
        target='/usr/bin/example', payload='reader.gz', mode=0o755,
        original_sha256=digest(old), sha256=digest(new))]))
    module['apply'](root, set())
    assert target.read_bytes() == incompatible
    try:
        module['apply'](root, {'example'})
    except ValueError as error:
        assert str(error) == 'reader override original checksum mismatch: /usr/bin/example'
        print('INCOMPATIBLE ORIGINAL REJECTED', str(error))
    else:
        raise AssertionError('incompatible original was silently replaced')
    assert target.read_bytes() == incompatible
    target.write_bytes(old)
    module['apply'](root, {'example'})
    assert target.read_bytes() == new and target.stat().st_mode & 0o777 == 0o755
print('OPTIONAL42 ORIGINAL IDENTITY REFUSAL AND EXACT POSITIVE PASS; DRAFT ONLY')
