# Separate mpv Lua and JavaScript candidate

2026-11-24 UTC. New private source/build/candidate tree:
`interpreter-inputs/flatpak-mpv-js-candidate/`. The earlier Lua-only candidate and
its hashes, metadata and future41 recipe remain unchanged. No guest, main source,
VERSION, shared package or numbered archive was changed.

`patch-flatpak-mpv-js-stream-draft.py` makes two source-file changes on a copy of
the pinned, already Lua-patched mpv source. A code-input flag flows through
`push_file_content`, `s_push_file` and `af_push_file` to the existing stream's
`STREAM_CODE_INPUT` check. `run_file` supplies this flag for initial JavaScript.
Embedded `@/` sources are still returned from compiled-in buffers before opening
a stream. The ordinary `script_read_file` supplies zero and remains a data API.

A separate `_read_code_file` native binding supplies `STREAM_CODE_INPUT` for
module loading. `defaults.js` uses it for module probing and the actual require
source read. The actual read is checked on its own opened descriptor; a successful
earlier probe does not authorize a reopened file. Existing exception cleanup is
retained. Explicit `mp.utils.read_file` plus `compile_js` remains the typed/data
route. These changes do not alter the MuJS library.

The new build used the same exact SDK, unchanged development overlay, original
manifest options and restored Sixel feature, under `MemoryMax=8G`, `CPUQuota=100%`
and one Ninja job. Only mpv and libmpv were rebuilt. The exact guarded LuaJIT bytes
were copied, not rebuilt.

| Candidate | SHA256 |
|---|---|
| `mpv` | `5c006b40eff5524ff10c24e9cb7392d776880f8acf7760f4a69accee139adf85` |
| `libmpv.so.2.6.0` | `90a5f3cc9b7c141b93f26a1e951571a02fca1cf5d66996d43648ce4d55df6c66` |
| `libluajit-5.1.so.2.1.1781966178` | `3f3d40eb32dbd6303717c3c1fccb0ff819775a053f2653147fac2eee835236cf` |

`probe-flatpak-mpv-js-candidate-draft.py` finishes with
`SEPARATE_JS_CANDIDATE_ALL_NATIVE_CONTROLS_PASS`. Original and candidate enabled
features and exported dynamic symbols match; SONAME is preserved and no new
symbol-version requirements appear. The previous absolute MuJS DT_NEEDED
difference remains documented and unchanged.

Original-runtime controls passed for Lua initial/nested loading, libmpv API
initialization/destruction, JS initial saved-file loading, typed-pipe JS, require,
explicit data reading/evaluation, and JS loading through libmpv until its script
shutdown event. The first libmpv JS harness used the CLI-only `script` alias and
was rejected by the original library. The corrected harness uses `scripts`; both
original and candidate then passed. Both logs are retained. These are unconfined
native controls, not mutable-code denial or declared-code guest results.

## Alternate future41 handoff

Only after the native controls passed,
`prepare-flatpak-mpv-js-integration41-draft.py` generated separate metadata and
concrete copies of the sealed40-gated composition/verification/patch recipes in
`interpreter-inputs/flatpak-mpv-js-integration41-draft/`.
The new metadata SHA256 is
`30740576db8a4f34e2ab6d77efb6c4c775a68f8f6c56a1346a62db43b618307b`.
Its original targets, bundle, OSTree objects, modes and symlinks match the earlier
inspection; only candidate paths/hashes and new payload names differ.

After sealed40 is available, the alternate entrypoint, from the build directory,
is `python3 interpreter-inputs/flatpak-mpv-js-integration41-draft/prepare-component.py`.
It still writes only a private draft package and invokes its own inheritance and
object-staging verifier. It is an alternative to the Lua-only recipe, not three
extra entries to stack on top of it. It has not been executed in this handoff.

The prior archive-input list remains required. Add the JS patch/build/probe/
metadata-generation/collection scripts, this document, the new full source and
candidate trees, new provenance/native-control reports, and generated alternate
recipes. `flatpak-mpv-js-archive41-paths-draft.py` emits this combined additive list.
SDK, historic host-compiler and dynamic-only metadata limitations remain those
in `flatpak-mpv-integration41-draft.md`; the unchanged inherited SDK/header inputs
are identified by their existing full checksum manifests.

Portable logs, full source/candidate hashes, comparisons, compiler settings and
alternate recipes are in `mpv-js-draft-evidence/`. Independent guest tests must
still check saved initial JS, automatic/directory scripts, require, file-descriptor
aliases, declared positives, data controls, removal and restart. No closure or
acceptance result is claimed.

After evidence and candidates were preserved, 301 disposable JS-build object
files were removed. Sources, build configuration, SDK/header inputs and candidate
bytes remain. No continuation unit remains running.
