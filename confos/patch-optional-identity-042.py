#!/usr/bin/python3
"""Pure future42 transformation; never silently replace an unknown original."""

def patched(text):
    anchor = "        path.write_bytes(data)\n"
    assert text.count(anchor) == 1
    return text.replace(anchor, """        original = item.get('original_sha256')
        if original is not None and hashlib.sha256(path.read_bytes()).hexdigest() != original:
            raise ValueError('reader override original checksum mismatch: '+str(target))
"""+anchor)
