#!/usr/bin/python3
"""Combined additive archive input list for the optional separate JS candidate."""
import subprocess,sys
from pathlib import Path
subprocess.run(['python3','flatpak-mpv-archive41-paths-draft.py'],check=True)
work='interpreter-inputs/flatpak-mpv-js-candidate/'
paths=['patch-flatpak-mpv-js-stream-draft.py','build-flatpak-mpv-js-candidate-draft.py',
 'probe-flatpak-mpv-js-candidate-draft.py','prepare-flatpak-mpv-js-integration41-draft.py',
 'collect-flatpak-mpv-js-draft.py','flatpak-mpv-js-archive41-paths-draft.py',
 'flatpak-mpv-js-candidate-draft.md','mpv-js-draft-evidence',work+'mpv',work+'candidate',
 work+'candidate-provenance.json',work+'native-controls-passed.json',work+'native-js-controls',
 work+'publish','interpreter-inputs/flatpak-mpv-js-integration41-draft']
for name in paths:
    assert Path(name).exists(),name
    sys.stdout.buffer.write(name.encode()+b'\0')
