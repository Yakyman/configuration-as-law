#!/usr/bin/python3
"""Emit additive NUL-separated future archive inputs; never create an archive."""
import sys
from pathlib import Path
work='interpreter-inputs/flatpak-mpv-lua-candidate/'
paths=['flatpak-mpv-integration41-draft.md','flatpak-mpv-continuation-draft.md','flatpak-mpv-lua-draft.md',
 'inspect-flatpak-mpv-integration41-draft.py','patch-flatpak-app-ref41-draft.py',
 'prepare-flatpak-mpv-package41-draft.py','verify-flatpak-mpv-package41-draft.py',
 'test-flatpak-app-ref41-draft.py','flatpak-mpv-archive41-paths-draft.py','flatpak-app-ref41-draft.patch',
 'flatpak-mpv-app-overrides41-draft.json','flatpak-mpv-integration41-preparation.log',
 'patch-mpv-lua-stream-draft.py','patch-luajit-code.py','code-file-policy.h',
 'build-flatpak-mpv-lua-draft.sh','fetch-flatpak-mpv-sdk-draft.py','fetch-flatpak-mpv-dev-sources-draft.py',
 'fetch-flatpak-mpv-libplacebo-submodules-draft.py','prepare-flatpak-mpv-ffmpeg-headers-draft.py',
 'prepare-flatpak-mpv-libplacebo-headers-draft.py','prepare-flatpak-mpv-dependency-headers-draft.py',
 'continue-flatpak-mpv-headers-draft.py','prepare-flatpak-mpv-language-headers-draft.py',
 'prepare-flatpak-mpv-bluray-public-draft.py','compile-flatpak-mpv-candidate-draft.py',
 'probe-flatpak-mpv-luajit-abi-draft.py','probe-flatpak-mpv-complete-runtime-draft.py',
 'collect-flatpak-mpv-continuation-draft.py','checkpoint-flatpak-mpv-complete-inputs-draft.py',
 'flatpak-mpv-lua-candidate-provenance.json','flatpak-mpv-dev-sources-draft.json',
 'flatpak-mpv-ffmpeg-headers-provenance.json','flatpak-mpv-libplacebo-headers-provenance.json',
 'mpv-draft-evidence','flatpak-inputs/mpv.flatpak','flatpak-inputs/runtime.flatpak',
 'packages/confos-code-readers_0.40_amd64.deb','packages/confos-code-readers_0.40_amd64.deb.sha256',
 'interpreter-inputs/flatpak-readers/mpv.tar.gz','interpreter-inputs/flatpak-readers/luajit.tar.gz',
 'interpreter-inputs/flatpak-readers/mujs.tar.gz',work+'candidate',work+'dev-sources',
 work+'development-overlay',work+'mpv',work+'luajit',work+'candidate-provenance.json',
 work+'continuation-publish',work+'ffmpeg-headers-provenance.json',work+'libplacebo-headers-provenance.json',work+'sdk-store/runtime/org.freedesktop.Sdk/x86_64/26.08/a1b744b072d9f55d061e35382547ae80dad8d92abecc1da7dc1818de2daabfd3/metadata']
paths += [str(path) for path in sorted(Path(work).glob('*-development-provenance.json'))]
for name in paths:
    assert Path(name).exists(),name
    sys.stdout.buffer.write(name.encode()+b'\0')
