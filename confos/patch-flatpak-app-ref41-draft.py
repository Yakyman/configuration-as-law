#!/usr/bin/python3
"""Anchored app/runtime-ref validation patch; output is restricted to private draft."""
from pathlib import Path
import sys

def patched(text):
    old="re.fullmatch(r'runtime/[A-Za-z0-9_.-]+/x86_64/[A-Za-z0-9_.-]+', item['ref'])"
    new="re.fullmatch(r'(?:runtime|app)/(?![.]{1,2}/)[A-Za-z0-9_.-]+/x86_64/(?![.]{1,2}$)[A-Za-z0-9_.-]+', item['ref'])"
    assert text.count(old)==1, 'sealed40 ref-validation anchor mismatch'
    assert text.count("raise ValueError('invalid reader runtime ref')")==1
    return text.replace(old,new).replace("raise ValueError('invalid reader runtime ref')","raise ValueError('invalid reader app/runtime ref')")

if __name__=='__main__':
    source,target=map(Path,sys.argv[1:])
    draft=Path('interpreter-inputs/flatpak-mpv-integration41-draft').resolve()
    assert target.resolve().is_relative_to(draft) and target.resolve()!=source.resolve()
    data=patched(source.read_text())
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(data)
    print('PRIVATE_APP_RUNTIME_REF_PATCH_PREPARED; main source untouched')
