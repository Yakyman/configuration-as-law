# Shared Flatpak Python prototype, 2026-11-24

No production integration. Build `build-flatpak-python-shared.sh`;
worker tree `interpreter-inputs/flatpak-python-shared`.
Evidence: `records/flatpak-python-shared-build.log`,
`records/flatpak-python-shared-abi.log`.
Source/SDK patch provenance: `flatpak-reader-provenance-draft.md`.

| Payload | SHA256 |
|---|---|
| New `python` (target `/usr/bin/python3.14`) | `9b61acc3353ec7dc339bb38ce54c88acc0dfd1dcfacd3fd612255609f52f0896` |
| New `libpython3.14.so.1.0` | `626cf3792f74e7f8d1c81c6965e88d54c7e78204c24c12c4879d6213ca465896` |
| Original executable | `3c9c31e89f288c647647be8291e96b7757a0ac6a245089855b8ef4445073f9db` |
| Original shared library | `e5c4b181660a9e668b98867325fc9cf3360c242649442590f6c521c09ef2bf8c` |

Build uses upstream CPython3.14.9 archive and pinned SDK multiarch patch, then
ConfOS descriptor guards and regenerated frozen importlib. Recorded configure
options are retained, including shared/LTO/system expat+ffi/gdbm/SQLite options,
multiarch includes, and no static libpython. Compiler flags match recorded
flags plus a source-path map. Host GCC14.2 replaces original GCC16.2; build
epoch is 2026-11-23 versus original recorded 2011-11-10. Missing host headers
disable SQLite and omit dbm/gdbm/Tk build modules. **Those newly built modules
are not used**: replacement consists only of core executable and shared
library, keeping original runtime stdlib and every native extension unchanged.

`probe-flatpak-python-shared-abi.py` uses a private bwrap root from retained
runtime, overlays two files read-only, and imports all74 original native
extensions. Baseline and patched both import all74 successfully, including
SQLite/gdbm/zstd/curses. All original shared-library exported symbols remain
present. ELF dynamic/version records saved. This is observed compatibility,
not proof of every native-extension behavior or a reconstructed SDK build.

Guest checks passed via `probe-flatpak-python-shared.sh`, using
sealed35 source archive SHA256
`62def64a3f293f4771f6fb50bdc1ec3bd3d1d59090c5baeeb3662b036d9da7cb`.
Fixture declares core files in /usr/local, then offline appends an initramfs
archive overriding /init to bind those files over exact deployment targets
before switch_root. This leaves original OSTree inodes unchanged. Fixture
initramfs identities and source/target identities are logged. It is explicitly
external fixture instrumentation, not a declaration-derived production boot
mechanism or completed P1/P2 integration. Existing original OSTree reader
objects remain exposed; replacement integration must address their aliases.

Guest evidence: `records/flatpak-python-shared-0.35.log` and
`records/flatpak-python-shared-fixture-boot.log`. Both fixture boots show
`confos-flatpak (enforce)` and exact replacement digests. On each boot,
21 saved-code attempts (script/stdin/import/-m/pyc/zip/startup across source
home/tmp/shm) are refused; seven recorded/typed/pipe/data/import/extension
controls pass. As in the earlier probe, generated pyc/zip from home input
are placed in /tmp, so this does not cover pyc/zip physically in home.
Original SQLite/gdbm/zstd and other representative extensions also import
inside the confined app. The original standard library and all original
extensions remain unchanged. No independent C embedding program or complete
extension test suites were run. Restart reinstalls only the explicitly
documented fixture bind mounts; it is not evidence for a production override.
Disposable guest/image/fixture archive removed; build/source inputs retained.
