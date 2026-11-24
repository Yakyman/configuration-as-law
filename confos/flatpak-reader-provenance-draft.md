# Flatpak reader source provenance, 2026-11-24

No rebuild or integration performed. Evidence: `records/flatpak-sdk-provenance.log`, `records/flatpak-reader-sources.log`, `records/flatpak-runtime-python-config.log`. Fetch script: `fetch-flatpak-sdk-provenance.py`. Exact upstream bytes retained on worker at `interpreter-inputs/flatpak-sdk-provenance/<commit>/<upstream-path>`.

## Matching source-list candidate

Freedesktop-SDK release/26.08 commit `89e0d095f472b2620f985f509b263e2b4d853d5a` (2026-10-22) matches both reader source revisions and patch paths in the installed runtime manifest:

| Reader | Source commit | Distribution patch |
|---|---|---|
| Bash | `9c465866b7d849378369ef700cbe2965aa9691e3` | `patches/bash/0001-bash-config.patch` |
| CPython 3.14.9 | `ead82c07db1f111d613926ed1b6667411d768125` | `patches/python3/python3-multiarch-include.patch` only |

Pinned original files (SHA256):

| File | SHA256 |
|---|---|
| [Bash patch](https://gitlab.com/freedesktop-sdk/freedesktop-sdk/-/raw/89e0d095f472b2620f985f509b263e2b4d853d5a/patches/bash/0001-bash-config.patch) | `e7a38fe0c52924d0b99c3d1bbde5e01e517e810ad4b20832b47ea81733d32719` |
| [Python patch](https://gitlab.com/freedesktop-sdk/freedesktop-sdk/-/raw/89e0d095f472b2620f985f509b263e2b4d853d5a/patches/python3/python3-multiarch-include.patch) | `0c23f1bbc4ddfe9a5836091f64ccf4f31e47c9e944e19c7d30db8c76c0fff271` |
| `elements/include/python3.yml` | `87d39a679b743523798b045128a21b76e986239488657e7e599545c0135d9c53` |
| `elements/components/python3.bst` | `5045504191665d100ad54d7d948ae3c2aa4d83f651880891613e0c0eb36848a6` |
| `elements/bootstrap/bash.bst` | `677ebcc025b8372739a7edbe72a986f4c0ccf6522987b5f8d88c805331d477ea` |

Bash patch enables `NON_INTERACTIVE_LOGIN_SHELLS`; prototype omitted it. Matching SDK recipe uses installed readline, curses/libtinfo and job control, unlike the static prototype's bundled readline configuration.

Python multiarch patch changes generated header/include configuration, adds `--with-conf-includedir`, and changes sysconfig/python-config include paths. It is listed in the actual manifest and needed to reproduce its configuration, not an optional extra for a matching replacement. Actual runtime sysconfig records shared Python, SOABI `cpython-314-x86_64-linux-gnu`, `/usr/include/x86_64-linux-gnu`, and matching recipe options: shared, no ensurepip, system expat/ffi, loadable SQLite, gdbm, LTO, no static libpython, platlibdir=lib. Full arguments/compiler flags saved in config evidence.

## Constant interning and rejected candidates

Actual runtime manifest does **not** list `python3-constant-interning.patch`. File returns 404 at matching candidate. Release commit `7d29fb963f5bc553b4746da2bb5718d5180c4c9d` (2026-10-29) subsequently adds it. Parent of release 3.14.10 update, `a56f991aa3c2d9175dea9702f36fa0be05edfef5`, still pins 3.14.9 but lists both patches, so does not match manifest patch list. Extra patch retained there for comparison, SHA256 `9f3969daa2b6d4af8464922e3e1e92637c8fffb4e142b4b2d6c1162cb262e11b`.

Master candidate `5e0e27cf9a5507d561f46111968c0486753920c3` pins 3.14.8 and both patches; release HEAD `065b03eb32d03aad00aba962834a8aa4538da9a5` pins 3.14.10. Neither matches this runtime.

## Remaining uncertainty

This recovers pinned distribution patch bytes at an SDK revision whose reader source lists match installed manifest and whose Python recipe options agree with installed sysconfig. Manifest names patch paths, not patch digests or SDK repository commit. Matching two components does not identify exact revision of whole SDK, toolchain, all dependency builds, or demonstrate these bytes produced shipped executables. No reconstructed runtime or bit-identical rebuild is claimed.

Both prototypes unchanged; original runtime readers remain exposed. Apply recovered patches in a later matching build and rerun startup, ABI, extension, embedded-library and ordinary application controls.

