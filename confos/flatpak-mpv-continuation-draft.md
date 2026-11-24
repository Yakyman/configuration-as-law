# Pinned Flatpak mpv candidate continuation

2026-11-24 UTC. Private worker-only candidate; no numbered release or acceptance.

The retained state was ahead of the prior checkpoint: libplacebo and libass
development files existed. The actual stop was libcdio's recursive `install-data`
target attempting to link utility programs without its libraries. Targeted native
header and pkg-config install targets resolved this. Exact source archives and
the original app and runtime commits remain those in `flatpak-mpv-lua-draft.md`.
The guarded LuaJIT candidate was reused, not rebuilt.

`continue-flatpak-mpv-headers-draft.py` restored libcdio, libcdio-paranoia,
libdvdread, libdvdnav, rubberband, uchardet, zimg and libsixel development files.
Autotools and CMake configurations retain the original module options. Meson
header/data install-plan entries are copied without building library targets.
`meson install --tags devel` alone was insufficient for libdvdread because it
also includes a static library. No dependency library was replaced.

`prepare-flatpak-mpv-language-headers-draft.py` restores MuJS headers and its
native pkg-config target from the retained exact archive; its version comes from
the public header. LuaJIT's version header is regenerated with the already-built
command and upstream generator, using the retained `.relver`. Its pkg-config
substitutions are those in its original installation rule.

libbluray's complete configure stopped at missing libudfread metadata. Its public
headers have no generated feature-dependent layout: the installed headers are
listed in `src/libbluray/meson.build`, and its version header substitutes only
the source project version. `prepare-flatpak-mpv-bluray-public-draft.py` copies
that exact list and generates the version header. Its explicitly dynamic-only
pkg-config metadata names the unchanged original shared library. Private/static
dependency closure is not represented or claimed. This is not a libbluray build.

The first full mpv configure and compile succeeded with all manifest options,
using the retained SDK GCC 16.2.0. The original binary has no `.comment` section;
the full original build toolchain is not independently established. No compiler
substitution or reduced feature configuration was used to bypass a compiler
error. The candidate configuration, compiler metadata and Meson log are retained.

The first explicit runtime feature comparison found `sixel` missing: its original
option was automatic, so retaining only the manifest's enabled flags did not
preserve it. The exact libsixel archive was therefore fetched from the manifest
URL and verified against SHA256
`6242586083cc37d898825c25dabd8c7c0abb62fa29ae54edacf2b5eba4db1167`.
The final configure explicitly enables the already-existing Sixel feature.
The initial mismatch is retained in `flatpak-mpv-candidate-compile.log`.

Every continuation unit uses `MemoryMax=8G`, `CPUQuota=100%`, `TasksMax=128`;
native builds use one job. No guest or shared release package is modified.
Published evidence is collected with machine-specific build paths replaced by
`<build>`. Candidate binaries stay in the private worker directory
`interpreter-inputs/flatpak-mpv-lua-candidate/candidate/`.

Final feature/ABI and native runtime controls passed. Saved-code
confinement, declared-source positives, removal and restart remain for integration
and independent guest checks; these unconfined controls cannot establish them.

## Candidate and observed controls

| Candidate file | SHA256 |
|---|---|
| `mpv` | `42c25feff2de540289d7ec4245bd2d77785c042c994ce9978bab8c11437e6656` |
| `libmpv.so.2.6.0` | `a3fb816802e6fff0598e5326af29788155ee13b7275002dbb1f49095ddc52c68` |
| `libluajit-5.1.so.2.1.1781966178` (retained) | `3f3d40eb32dbd6303717c3c1fccb0ff819775a053f2653147fac2eee835236cf` |

`compile-flatpak-mpv-candidate-draft.py` finished with
`MPV_LIBMPV_CANDIDATE_ABI_FEATURE_CONTROLS_PASS`. Both executable and library
export sets match exactly; the complete observed enabled-feature lists match,
including Sixel. The libmpv SONAME remains `libmpv.so.2`.

`probe-flatpak-mpv-complete-runtime-draft.py` finished with
`COMPLETE_CANDIDATE_ORIGINAL_RUNTIME_NATIVE_CONTROLS_PASS`. Original and candidate
libmpv both returned API version 131078 and initialized/destroyed successfully.
Initial Lua input through a pipe and nested `loadfile`, `dofile`, `require` and
file-write controls passed in the exact original runtime with all three candidate
objects substituted together. This namespace has no ConfOS execution confinement.

The dynamic comparison adds no symbol-version requirements. One dependency
spelling differs: both candidates record `/app/lib/libmujs.so`, where the original
records `libmujs.so`. The original MuJS object has no SONAME, and the current Meson
link line resolves it to an absolute path. It is the same original object at the
fixed Flatpak application path; original-runtime loading passed. This difference
is retained explicitly in `mpv-dynamic-abi-comparison.json`, not hidden by a claim
of identical binaries or general relocatability.

Portable logs, compiler/build settings, final configuration, ABI comparisons,
and hashes of all restored development files and candidates are under
`mpv-draft-evidence/`. Replacements must target the original three regular files
and preserve existing symlinks; no replacement package has been made here.

## Retained inputs and handoff recipe

`checkpoint-flatpak-mpv-complete-inputs-draft.py` checksummed 40,608 SDK entries
(regular files by SHA256, symlinks by target) and 1,566 source/header/script inputs.
The manifests are `sdk-input-checksums.json` (SHA256
`fe2cf7ec58bcfa74d327676228515ddac9e05a7f5e27d1ba596321a1447b53e0`)
and `complete-input-checksums.json` (SHA256
`0f08d57cd2bcf6b0316a41dd3c9c0078b4a05e89eb59d356fd5c4ef74a002ff9`).
These include the patched full mpv source tree, development overlay, exact source
archives, patch/build scripts, and retained SDK deployment. The SDK commit remains
`a1b744b072d9f55d061e35382547ae80dad8d92abecc1da7dc1818de2daabfd3`.

On the retained worker state, the repeatable final commands are:

```sh
python3 compile-flatpak-mpv-candidate-draft.py
python3 probe-flatpak-mpv-complete-runtime-draft.py
python3 collect-flatpak-mpv-continuation-draft.py
python3 checkpoint-flatpak-mpv-complete-inputs-draft.py
```

Run those through the same resource-limited persistent worker-unit mechanism;
the compiler command itself uses one Ninja job. The existing initial scripts
retain the prior source extraction, descriptor-policy patch, SDK installation,
FFmpeg/libplacebo/libass metadata stages and their provenance. This continuation's
metadata sequence was libcdio, libcdio-paranoia, libdvdread, libdvdnav, language
headers, libbluray public headers, rubberband, uchardet, zimg, and libsixel.
All needed archives remain locally retained on the worker. This recipe reconstructs
the private candidate environment, not the upstream application's entire historic
build service or a claim of byte-for-byte upstream reproducibility.

After all candidates and checksum manifests were preserved and copied, cleanup
removed nine disposable intermediate mpv configure trees and the final build's
object files. Final Meson configuration, candidates, sources, SDK and development
headers remain; the repeat build regenerates the removed objects. No continuation
unit remains running. `mpv-draft-evidence/cleanup.log` records the removal counts.
