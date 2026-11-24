# Recorded Flatpak mpv Lua reader: source inspection draft

2026-11-24 UTC. The private guarded LuaJIT and mpv/libmpv candidates now build;
the original-runtime feature, symbol and native controls are recorded in
`flatpak-mpv-continuation-draft.md`. The earlier dependency checkpoint below is
retained as history and is superseded by that continuation.
No confined saved-code result, guest run, integrated repair or acceptance is claimed.

The next repair needs **both mpv and its exact LuaJIT library**. mpv's initial Lua
script reader reads bytes through its own stream API and calls `luaL_loadbuffer`.
It does not use LuaJIT's `luaL_loadfilex`, so the existing LuaJIT file-loader patch
alone cannot cover `--script` or automatically discovered scripts.

## Exact retained inputs

App ref: `app/io.mpv.Mpv/x86_64/stable`.
App commit: `13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc`.
Runtime commit: `df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c`
of `runtime/org.freedesktop.Platform/x86_64/26.08`.
Original application manifest SHA256:
`1b3eb1849b2cbf159505b214fc8ac68a4c0ae3d80ecfec24d330e34a4a431751`.

| Original app object | SHA256 |
|---|---|
| `/app/bin/mpv` | `a6de4a9af6d84e78d7451bc0b68150de958c9c369ce010e8c2b9575b6e954cbb` |
| `/app/lib/libmpv.so.2.6.0` | `1fcd8306d860def640c68c2fec47f20e38fc9c5f3bc4176d04fe2c6ca39902e4` |
| `/app/lib/libluajit-5.1.so.2.1.1781966178` | `565e9aa1f51c3880a66e9189d3fe505dd536b0ff4e8c34ad100c7ab76ceee523` |
| `/app/lib/libmujs.so` | `6934411b878eb686564042e5d120651714d01436e3b8a108621bb75c935b96f5` |

`readelf -d` shows both mpv and libmpv require `libluajit-5.1.so.2`.
The two LuaJIT library aliases point to the versioned object above, whose SONAME
is `libluajit-5.1.so.2`. Its strings identify `LuaJIT 2.1.1781966178` and
`luaJIT_version_2_1_1781966178`. The original mpv source's `MPV_VERSION` is `0.42.0`.
These observations establish targets, not binary compatibility of a replacement.

The original manifest pins mpv source commit
`b985c3634ef056b185e3f13c7ac597b3611f5774` from the mpv repository, and LuaJIT source
commit `b411bec3ce550ef9968fc83bca094455cf812c1f` from the `openresty/luajit2`
repository. This is not an assumption that the Neovim LuaJIT source is identical.
The source archive URLs and hashes are:

- [mpv pinned archive](https://codeload.github.com/mpv-player/mpv/tar.gz/b985c3634ef056b185e3f13c7ac597b3611f5774):
  `48c4704dd6b93279e93a7f3ba48d1bab444b15d9196e400db11ea362069a891f`.
- [LuaJIT pinned archive](https://codeload.github.com/openresty/luajit2/tar.gz/b411bec3ce550ef9968fc83bca094455cf812c1f):
  `718f9ebb54b715ec4cd86ef1605177a9a2c1c80a0b6de4c26f3e1ccc8e5fd327`.

These archives already exist under `interpreter-inputs/flatpak-readers/` and were
not downloaded again. Archive member prefixes match the manifest commits.
The inspection copies selected original members directly from those archives,
avoiding any earlier patches in extracted work trees. Source member hashes and
archive provenance are in `flatpak-mpv-lua-draft-sources.json`; the original members
and manifest are retained under `interpreter-inputs/flatpak-mpv-lua-draft/`.

The manifest lists no source patches for either module. mpv uses Meson with
`-Dcplayer=true`, `-Dlibmpv=true`, `-Dlua=enabled`, `-Djavascript=enabled`,
`-Dcplugins=enabled`, `-Dbuild-date=false` and the feature list preserved in the
inspection log. Its extra source is application metadata, and its post-install
edit removes the desktop file's smb protocol entry. LuaJIT is built with
`BUILDMODE=dynamic` and the application prefix, then its command, headers and
pkg-config metadata are removed. The separate custom module installs the wrapper
and a configuration containing only the screenshot-directory setting.

## Original source call paths

All line numbers here refer to the original archive members copied by the script.

- `mpv/options/options.c:560` defines `scripts`, with `script` an alias of
  `scripts-append`; `load-scripts` controls automatic discovery and defaults true
  at line 1043. `config-dir` is also exposed.
- `mpv/player/scripting.c:279`, `mp_load_scripts`, first loads explicit script
  paths, then searches all configured `scripts` directories when automatic loading
  is enabled. `mp_load_script` also resolves directory scripts to `main.*`.
- `mpv/player/lua.c:230`, `load_file`, calls `stream_read_file` followed by
  `luaL_loadbuffer`. Both explicit and automatic initial Lua scripts reach it.
  Built-in Lua sources follow the separate embedded-buffer loader and must remain
  available. Initialization filters relative `package.path`/`package.cpath`
  entries, but allows absolute paths and prepends a script-directory Lua path;
  this is not a saved-code authority check.
- `mpv/stream/stream.c:901`, `stream_read_file2`, opens a stream then reads it
  completely. `mpv/stream/stream_file.c:298` handles `fd://` and `fdclose://`,
  and line 334 opens a pathname. This is where the actual backing descriptor
  becomes available for a race-free code-input check.
- `luajit/src/lib_base.c:387` and `:453` implement `loadfile` and `dofile` through
  `luaL_loadfilex`/`luaL_loadfile`. `luajit/src/lib_package.c:370` implements Lua
  `require` loading through `luaL_loadfile` after search-path resolution.
- `luajit/src/lj_load.c:98`, `luaL_loadfilex`, opens the file and invokes
  `lua_loadx` on that same stream. The original source contains exactly one
  anchor matching `patch-luajit-code.py` and no ConfOS guard. This is evidence
  that the patch shape can be reused, not evidence of an ABI-compatible build.
- C module loading in `luajit/src/lib_package.c:44` uses `dlopen`; this is distinct
  from Lua text loading and still requires a native-load regression. The manifest
  also enables MuJS JavaScript and mpv C plugins, which this Lua proposal does
  not repair or claim to cover.

## Concrete next repair proposal

1. Start a fresh source tree from each exact retained archive. Apply the existing
   descriptor policy to the exact LuaJIT `luaL_loadfilex` anchor, maintaining its
   existing cleanup/error contract. Build the dynamic library with the original
   version identity and SONAME; do not substitute a Neovim library. Compare
   exported symbols, symbol versions and required libraries against the original
   before any replacement is packaged.
2. Add an explicit **code-reading mode** to mpv's stream path used by Lua
   `load_file`. Propagate it to the file/fd backend, check the descriptor after
   opening and before reading, and use that same descriptor for the bytes passed
   to Lua. Do not check a pathname and reopen it, and do not apply the guard to
   ordinary media/data streams. Non-file script backends need an explicit policy
   or a documented refusal; they must not silently bypass the code-reading mode.
   Retain typed pipe input under the existing policy and retain embedded scripts.
3. Rebuild both `/app/bin/mpv` and `/app/lib/libmpv.so.2.6.0`, since both contain
   the Lua reader, together with the exact LuaJIT target. Pin original object
   hashes and replacement hashes in the existing Flatpak override mechanism,
   retain symlink topology, include source/patch provenance, and rebuild against
   the matching runtime dependencies. Library replacement alone is insufficient.
4. Run native probes only after resources are available: mutable `--script`,
   automatic config-directory Lua scripts, directory `main.lua`, and a declared
   Lua script attempting `loadfile`, `dofile` and `require` from mutable files.
   Add descriptor/proc aliases and symlink attempts. For each include the positive
   declared-source counterpart, an ordinary media/data read, and built-in-script
   startup. Use observable sentinel effects rather than relying on mpv's exit
   code. Exercise both the command and libmpv entry; verify native C loading
   independently. Record post-apply and restart behavior before making a claim.

## Inspection result

Command on the retained build workspace:
`python3 inspect-flatpak-mpv-lua-draft.py`.
The complete successful output is `flatpak-mpv-lua-draft-inspect.log`, ending in
`SOURCE_INSPECTION_COMPLETE`. The script uses archive reads, hashing, `readelf`
and `strings`; it executes no app binary and makes no runtime changes.

An initial attempt to fetch the pinned mpv `player/lua.c` from the raw source
endpoint returned HTTP 404. Inspection continued using the already retained exact
archive. No fresh mpv/LuaJIT source fetch is needed. Full source
identity is pinned by the manifest and retained archive; the failed raw endpoint
does not establish a different source or permission to substitute a release.

## Private candidate and dependency checkpoint

The continuation used separate systemd user units with `MemoryMax=8G`,
`CPUQuota=200%`, and `TasksMax=128`; compilation used `make -j2`. All units started
for this draft have finished. No guest was started and no existing image, runtime
package, component lock or shared integration source was changed.

`patch-mpv-lua-stream-draft.py` now implements the proposed initial-reader change
on the pinned source: `load_file` passes a new `STREAM_CODE_INPUT` flag to
`stream_read_file2`; only the file/fd backends accept that flag; `open_f` checks
its actual descriptor before any source read. Failure closes only a descriptor
owned by that stream. The ordinary stream mode and embedded buffers are unchanged.
The current Lua path retains its existing local-files-only flag, including
ordinary filesystem and proc-fd aliases. This patch has not yet been compiled.

The existing `patch-luajit-code.py` was applied to a fresh exact archive tree.
`build-flatpak-mpv-lua-draft.sh` produced the dynamic candidate
`interpreter-inputs/flatpak-mpv-lua-candidate/candidate/libluajit-5.1.so.2.1.1781966178`,
SHA256 `3f3d40eb32dbd6303717c3c1fccb0ff819775a053f2653147fac2eee835236cf`.
The candidate command is retained beside it as `luajit`. Original-source,
patched-source, policy, patch-script and candidate hashes are in
`flatpak-mpv-lua-candidate-provenance.json`.

`probe-flatpak-mpv-luajit-abi-draft.py` compared exported dynamic symbols and
ran the original mpv in the original application/runtime trees, substituting only
that library in a private mount namespace. No original export is missing.
Both original and substituted runs passed `--version`, typed-pipe Lua startup,
and native `loadfile`, `dofile`, `require`, and ordinary `io.open` controls.
The log ends `ORIGINAL_RUNTIME_LUAJIT_ABI_AND_TYPED_PIPE_CONTROLS_PASS` in
`flatpak-mpv-luajit-abi-draft.log`. Those runs were unconfined; they do not prove
refusal of mutable saved code, execution of a declared line, or initial mpv Lua
closure. The build used the worker compiler, not an asserted reconstruction of
the original build toolchain. Runtime compatibility was observed only for these
explicit controls and the symbol comparison.

### Exact SDK and application dependency gap

The upstream runtime ref lookup still returned the recorded `df26da...` commit.
The SDK ref returned
`a1b744b072d9f55d061e35382547ae80dad8d92abecc1da7dc1818de2daabfd3`.
`fetch-flatpak-mpv-sdk-draft.py` installed that exact SDK into a separate private
store using retained native Flatpak inside a mount/user namespace. An initial
mount attempt failed because `/var/lib/flatpak` is a symlink; the successful
retry mounted the private store at its real target. No host installation occurred.
The private SDK is retained for the next stage, about 1.8 GB. SDK identity here
means that pinned deployment, not proof that it is the app's original whole SDK.

The SDK supplies FFmpeg headers for `libavcodec` 62.28.103, while the app's original
library is 63.1.102. The SDK also lacks several app-specific development packages.
`flatpak-mpv-sdk-dependencies-draft.log` records the full query. Some reported
missing names are non-pkg-config/platform-specific probes; the authoritative next
blocker is the actual full-feature Meson configure below. No app feature was
disabled to accommodate the SDK.

Eleven exact source archives for app dependencies are now retained under
`interpreter-inputs/flatpak-mpv-lua-candidate/dev-sources/`. Their complete original
manifest entries, requested archive URLs and verified hashes are in
`flatpak-mpv-dev-sources-draft.json`. An initial FFmpeg gitweb request returned
HTTP 200 with an HTML challenge, not an archive. It was rejected and removed.
The same exact manifest commit `ce8f11b9fac4cd7ccfb41ca7c01bc17f5cda8cc3` was
retrieved from the project's source mirror; archive SHA256 is
`979e06585856b823e07a94bb9560106e4eb73ac7d061000556e2484270afc09c`.
The final checkpoint verifies all eleven as readable archives as well as checking
their hashes. Initial and corrected fetch logs are retained separately.

### Completed bounded FFmpeg header stage

Command: `python3 prepare-flatpak-mpv-ffmpeg-headers-draft.py` in its resource-limited
worker unit. It generated development headers and pkg-config metadata only, using
native configure and `make -j2 install-headers` from the exact source. No FFmpeg
library was compiled, installed, replaced or relinked.

The source explicitly defines the public generated configuration list as only
`bigendian` and `fast_unaligned` (`configure:2456`). The installed header contains
`AV_HAVE_BIGENDIAN 0` and `AV_HAVE_FAST_UNALIGNED 1`; the script verifies the
original library ELF objects are little-endian x86-64, matching the source's
architecture defaults and the manifest's lack of overrides for those values.
It uses a deliberately minimal **metadata-only configuration**, whose exact flags
are recorded. It does not claim that this configuration reproduces every private
feature of the existing FFmpeg libraries. In particular generated pkg-config
`Requires.private` is not evidence of the original optional/static dependency
closure. Only dynamic linking against the unchanged original app libraries is
intended; static linking with this metadata is not supported by this draft.

The output is merged into the private `development-overlay/include` and
`development-overlay/lib/pkgconfig`. Existing app headers/metadata are preserved;
the namespace binds the overlay directories over the original read-only app,
while its `.so` objects remain the original bytes. Their before/after hashes and
every installed generated-file hash are in `flatpak-mpv-ffmpeg-headers-provenance.json`.

A single mpv configure retry used every original manifest feature option,
`--wrap-mode=nofallback`, and only reduced parallel linking capacity to two.
It found the correct versions:

| Dependency | Configure result |
|---|---|
| libavcodec | 63.1.102 |
| libavfilter | 12.1.102 |
| libavformat | 63.1.102 |
| libavutil | 61.1.102 |
| libswresample | 7.1.102 |
| libswscale | 10.1.102 |
| libplacebo | Missing development metadata; configure stopped |

`flatpak-mpv-ffmpeg-headers-draft.log` ends with `MPV_CONFIGURE_STATUS 1` and
`BOUNDED_FFMPEG_HEADER_STAGE_COMPLETE; no FFmpeg library or mpv executable compiled`.
This resolves the first development-input blocker, not the Lua saved-code repair.

### Next bounded stage and retained work

The next exact source is libplacebo commit
`451d8ea5661c868562725e6500deda7fdd4e9a1e`, archive SHA256
`63251b5af660e264abcf70b2d4dbadc5817443e3d10a6e03f03d4f0647b48ac6`.
Its original manifest uses Meson with `-Dvulkan=enabled -Dshaderc=enabled`.
Next commands to obtain the private source tree are:

```sh
mkdir -p interpreter-inputs/flatpak-mpv-lua-candidate/libplacebo-source
tar -xf interpreter-inputs/flatpak-mpv-lua-candidate/dev-sources/libplacebo.archive --strip-components=1 -C interpreter-inputs/flatpak-mpv-lua-candidate/libplacebo-source
```

Then reuse the pinned SDK/original-app/private-development-overlay namespace in
`prepare-flatpak-mpv-ffmpeg-headers-draft.py` for libplacebo's original Meson
configuration. Inspect its generated public feature/version headers and native
development-only install targets; retain original `libplacebo.so.387` bytes.
Do not silently switch its Vulkan/shaderc features or build fallback dependencies.
After matching headers and pkg-config metadata are staged, retry the complete mpv
configure and record the next dependency. libass and several optional app
dependencies remain missing in the SDK query, but have not yet reached that
configure's next failure. No speculative full dependency rebuild was started.

`checkpoint-flatpak-mpv-lua-draft.py` retains candidates, patched mpv/LuaJIT source,
the exact archives, SDK and development overlay, plus native configuration logs.
It cleans LuaJIT compiler outputs and removes disposable failed Meson/FFmpeg
configuration trees after copying their evidence. The checkpoint output is
`flatpak-mpv-lua-draft-checkpoint.log`. `collect-flatpak-mpv-lua-draft.py` copies
portable logs and manifests, replacing machine-specific build paths.
Future confined probes still require an independently allocated private guest and
the complete mpv/libmpv candidate; all saved/declared/removal/restart claims remain
unverified. This task is checkpointed, not closed as repaired.
