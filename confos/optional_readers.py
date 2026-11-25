"""Apply declared component's byte-exact reader overrides to installed packages.

The original component carries compressed payloads and a declarative manifest.
An override is active only when its Debian package is selected. A removed package
does not leave its executable behind merely because enforcement is available.
"""
import gzip
import hashlib
import json
from pathlib import Path

def apply(root, package_names):
    root = Path(root)
    directory = root/'usr/lib/confos/reader-overrides'
    manifest = directory/'manifest.json'
    if not manifest.exists():
        return
    for item in json.loads(manifest.read_text()):
        if item['package'] not in package_names:
            continue
        target = Path(item['target'])
        payload = Path(item['payload'])
        if (not target.is_absolute() or '..' in target.parts or payload.is_absolute()
                or len(payload.parts) != 1 or payload.name in ('.', '..')):
            raise ValueError('invalid reader override pathname')
        data = gzip.decompress((directory/payload).read_bytes())
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('reader override checksum mismatch')
        path = root/str(target).lstrip('/')
        if not path.is_file() or path.is_symlink():
            raise ValueError('reader override requires the original package file: '+str(target))
        original = item.get('original_sha256')
        current = hashlib.sha256(path.read_bytes()).hexdigest() if original is not None else None
        if original is not None and current != original and ('other_releases' in item or 'unlisted_release' in item):
            # A guard that is a replacement of a few bytes at a recorded place: for another
            # listed release of the package the same replacement is made in that release's
            # own file, so that the release the line names stays in force. A release that
            # the record does not list has no guard; the declaration is refused.
            listed = next((entry for entry in item.get('other_releases', ()) if entry['original_sha256'] == current), None)
            if listed is None:
                raise ValueError('no guarded '+str(target)+' exists for this release of '+item['package']
                                 +'; guarded releases: '+', '.join(
                                     [str(item.get('source_version'))]+[entry['version'] for entry in item.get('other_releases', ())]))
            data = bytearray(path.read_bytes())
            before, after = bytes.fromhex(listed['original']), bytes.fromhex(listed['replacement'])
            offset = listed['offset']
            if len(before) != len(after) or bytes(data[offset:offset+len(before)]) != before:
                raise ValueError('reader guard does not fit '+str(target))
            data[offset:offset+len(after)] = after
            if hashlib.sha256(data).hexdigest() != listed['sha256']:
                raise ValueError('reader guard checksum mismatch: '+str(target))
            path.write_bytes(data)
            path.chmod(item['mode'])
            print('reader guard applied in place to '+str(target)+' of release '+listed['version']+' of '+item['package'], flush=True)
            continue
        if original is not None and current != original:
            # Another release of the package than the one this guarded file was built
            # from. Releases 0.42-0.51 refused the whole declaration here, so a system
            # whose archive state has an older curl or libperl could not be built or
            # updated (complete run 2 on 0.49, OW-2 and OW-3). The guarded file is
            # installed, as the overrides without a recorded original always were,
            # and the assembly log says so.
            print('reader override built from release '+str(item.get('source_version'))+' replaces '+str(target)
                  +' of another release of '+item['package'], flush=True)
        path.write_bytes(data)
        path.chmod(item['mode'])
