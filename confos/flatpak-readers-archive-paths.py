#!/usr/bin/python3
"""Emit NUL-delimited required extra paths for archive-source.sh; no archive mutation.
Parent adds: --null -T <(python3 flatpak-readers-archive-paths.py)
to the existing tar invocation, preserving all prior archive members.
"""
from pathlib import Path
import json,sys
paths=['archive-source.sh','archive-readers-039.sh','cleanup-readers-039.sh','document-flatpak-readers-039.py','flatpak_readers.py','package-flatpak-reader-overrides.py','flatpak-reader-candidate-manifest.json','flatpak-reader-provenance-draft.md','flatpak-python-shared-draft.md','flatpak-bash-compatible-draft.md','patch-flatpak-python.py','patch-flatpak-bash.py','build-flatpak-python-shared.sh','build-flatpak-bash-compatible.sh','link-flatpak-bash-compatible.sh','probe-flatpak-python-shared-abi.py','probe-flatpak-bash-compatible-abi.py','flatpak-readers-archive-paths.py','advance-flatpak-readers-release.py','prepare-flatpak-readers-component-039.py','check-flatpak-readers-inheritance.py','build-flatpak-readers-fixture-039.py','prepare-flatpak-readers-039.sh','probe-flatpak-readers-039.sh','sync-flatpak-readers-039.sh','flatpak-bash-compatible-probes.sh','flatpak-python-shared-probes.sh','flatpak-readers-integration-probes.sh','test-flatpak-readers-module.py','interpreter-inputs/flatpak-readers/bash.tar.gz','interpreter-inputs/flatpak-readers/python.tar.gz','interpreter-inputs/flatpak-bash-compatible/COPYING','interpreter-inputs/flatpak-python-shared/LICENSE','packages/confos-code-readers_0.38_amd64.deb','packages/confos-code-readers_0.38_amd64.deb.sha256','interpreter-inputs/flatpak-sdk-provenance/89e0d095f472b2620f985f509b263e2b4d853d5a']
paths += [r['candidate_worker_path'] for r in json.loads(Path('flatpak-reader-candidate-manifest.json').read_text())['readers']]
# Runtime bundle supplies exact link libraries and retained stdlib/sysconfig/manifests.
paths += ['flatpak-inputs/runtime.flatpak']
for name in paths:
    assert Path(name).exists(),name
    sys.stdout.buffer.write(name.encode()+b'\0')
