# 0.41 mpv Lua and JavaScript reader contribution

Released by builder, 2026-11-24 UTC, REQUESTS73. Canonical two-boot input,
discovery/libmpv/descriptor and original-object controls, actual decoded media
EOF and app/last-runtime removal passed: records/mpv-0.41.log. Extended smoke,
fresh-source equality and external inventory passed (13,699 objects/303 force
rows/zero errors). Source archive SHA256:
2c73f6a664a2754cc78a7244d31bb77c7ac3d5253f45653a3c12cdfb418e4ca9.
Earlier fixture/event-timing/traceback observation failures remain in records.
This update supersedes the draft status inside the immutable41 archive; it does
not establish independent acceptance or a hypothesis outcome. The combined
Lua+JS candidate below is the actual released payload, unchanged during testing.

## Exact payloads and inputs

All three files are retained under
`interpreter-inputs/flatpak-mpv-js-candidate/candidate/`. The proposed app entries
use mode 0755 and these uncompressed SHA256 values:

| Payload | Deployment target under `files/` | SHA256 |
|---|---|---|
| `mpv41js-0.gz` | `bin/mpv` | `5c006b40eff5524ff10c24e9cb7392d776880f8acf7760f4a69accee139adf85` |
| `mpv41js-1.gz` | `lib/libmpv.so.2.6.0` | `90a5f3cc9b7c141b93f26a1e951571a02fca1cf5d66996d43648ce4d55df6c66` |
| `mpv41js-2.gz` | `lib/libluajit-5.1.so.2.1.1781966178` | `3f3d40eb32dbd6303717c3c1fccb0ff819775a053f2653147fac2eee835236cf` |

The metadata file is
`interpreter-inputs/flatpak-mpv-js-integration41-draft/mpv-app-overrides.json`,
SHA256 `30740576db8a4f34e2ab6d77efb6c4c775a68f8f6c56a1346a62db43b618307b`.
It records the exact original hashes and repository object paths, inspected from
the native app rather than inferred. The original regular files each had two
hard links. Staging must replace only deployment files, preserve original OSTree
object bytes, and retain both libmpv and both LuaJIT symlink aliases.

The application is `app/io.mpv.Mpv/x86_64/stable`, commit
`13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc`.
Its bundle SHA256 is
`66d65390ff1b7a526b25a448f12d137f72df5859460c1d05e17508ed6a88bed9`.
The runtime is `runtime/org.freedesktop.Platform/x86_64/26.08`, commit
`df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c`;
its bundle SHA256 is
`072d80f7f24a5c5ff75e2c244fdd5aea032216fcb6e6138af175e18ee76054e3`.

The mpv source commit is `b985c3634ef056b185e3f13c7ac597b3611f5774`, archive
SHA256 `48c4704dd6b93279e93a7f3ba48d1bab444b15d9196e400db11ea362069a891f`.
The OpenResty LuaJIT source commit is
`b411bec3ce550ef9968fc83bca094455cf812c1f`, archive SHA256
`718f9ebb54b715ec4cd86ef1605177a9a2c1c80a0b6de4c26f3e1ccc8e5fd327`.
The combined candidate copies the already guarded LuaJIT binary unchanged.
Its new mpv source differs from the earlier Lua candidate in precisely
`player/javascript.c` and `player/javascript/defaults.js`.

## Saved-code readers and explicit data

`patch-mpv-lua-stream-draft.py` adds `STREAM_CODE_INPUT` to initial Lua source
loading. File and descriptor stream backends check the descriptor actually read;
other stream backends are refused for this code-input flag. The LuaJIT patch
checks its file-loading route used by nested `loadfile`, `dofile` and Lua modules.

`patch-flatpak-mpv-js-stream-draft.py` carries the same flag through JavaScript
`run_file`, including initial files. Embedded `@/` sources use their compiled-in
buffers. The private `_read_code_file` binding applies the flag to module probing
and the later actual `require` source read. A successful probe cannot authorize
a different descriptor opened afterward.

The shared descriptor helper checks kernel confinement state. For confined
regular files it requires a read-only filesystem without the noexec flag; typed
input and other nonregular descriptors retain their existing route. Unconfined
build services remain permitted. Consequently unconfined native tests cannot
prove this enforcement. A filename extension or pathname alone is not the
authorization decision.

Ordinary Lua `io.open` and JavaScript `mp.utils.read_file` remain data readers.
Explicit reading of data followed by `compile_js` is retained under the R4
typed/data route; the change does not attempt to infer whether arbitrary data
will later be evaluated. Ordinary media reads likewise must remain available.
Native plugins use their existing executable/library policy rather than these
Lua/JS source-reader hooks and need their own regression controls.

## Build and compatibility evidence

mpv and libmpv were built using SDK
`runtime/org.freedesktop.Sdk/x86_64/26.08`, commit
`a1b744b072d9f55d061e35382547ae80dad8d92abecc1da7dc1818de2daabfd3`, GCC 16.2.0,
with the retained development overlay and original app/runtime link libraries.
Builds used one job, MemoryMax 8G and CPUQuota 100%. No dependency shared library
was replaced. The full historical upstream toolchain has not been established.
The earlier LuaJIT build used the build host compiler; historical bit-identical
compiler-environment reconstruction is not claimed.

Observed enabled features match the original, including JavaScript, LuaJIT,
native plugins and Sixel. Sixel was initially absent because its original option
was automatic; its exact headers were restored and the final option explicitly
enabled it. The initial mismatch remains in the earlier logs. Dynamic exported
symbol sets match, libmpv SONAME remains `libmpv.so.2`, and no new symbol-version
requirements were observed. These checks do not prove all behavioral ABI aspects.

Both new binaries name `/app/lib/libmujs.so` in DT_NEEDED where the original names
`libmujs.so`. The original MuJS library has no SONAME and the current link command
resolved its absolute path. The same original object loads at the fixed Flatpak
path in native controls. General relocatability or identical dynamic metadata is
not claimed. FFmpeg/libbluray reconstructed metadata describes dynamic linking,
not static private dependency closure.

`mpv-js-draft-evidence/` contains source/candidate hashes, native logs and ABI
comparisons. Inherited input manifests in `mpv-draft-evidence/` identify 40,608 SDK
entries and 1,566 source/header/script inputs. Their hashes are respectively
`fe2cf7ec58bcfa74d327676228515ddac9e05a7f5e27d1ba596321a1447b53e0` and
`0f08d57cd2bcf6b0316a41dd3c9c0078b4a05e89eb59d356fd5c4ef74a002ff9`.
The additive archive helper includes retained sources, headers, recipes, bundles
and evidence. It identifies the SDK by commit and complete checksums; an offline
rebuild additionally requires archiving its retained deployment. Portable text
uses archive-relative paths or `<build>`; pinned upstream inputs and binary
debug strings must not be rewritten to sanitize provenance.

## Completed native controls

The corrected native log ends with
`SEPARATE_JS_CANDIDATE_ALL_NATIVE_CONTROLS_PASS`. Original and candidate passed
initial/nested Lua loading, typed input, libmpv initialization/destruction,
saved initial JavaScript, JavaScript `require`, explicit data read/evaluation,
and JavaScript through libmpv until script shutdown. libmpv API version was
131078. The first JS libmpv harness incorrectly used CLI alias `script`; the
original rejected it. The corrected harness uses `scripts`, and both logs remain.
These controls run in the original runtime namespace without ConfOS confinement.

The app/runtime ref-validator controls also passed. The proposed widening keeps
digest, target, mode, containment and original-object checks, and rejects literal
dot/dot-dot ref segments. Private package composition requires sealed 0.40 and
must preserve every inherited reader payload while appending exactly these three
entries. It is an alternative to the Lua-only draft, not an additional three
entries on top of it. No package-composition or guest result is asserted here.

## Pending gates and review findings

The initial bounded review found the following gaps. A subsequently authorized
edit changed only `mpv41-app-probe.py` and `build-mpv-fixture-041.py` to address
items 1, 2, 3 and the explicit-evaluation part of item 4. References below describe
the initially reviewed versions; they are not current line numbers.

1. `mpv41-app-probe.py:63` tests ordinary media with `idle=yes` and a watchdog
   that quits successfully after two seconds. Exit zero alone can pass without
   loading the WAV. Require an observed file-loaded/audio event and successful
   end-file status, with the watchdog treated as failure for this control.
2. `mpv41-app-probe.py:88-95` treats absence of shutdown within three seconds
   as a successful libmpv negative. Unrelated loading failure also satisfies it.
   Require captured policy-denial evidence and absence of a script marker, with
   declared positives proving the same harness and loader work.
3. `mpv41-app-probe.py:52-57` exercises an explicit config include. Global
   `--no-config --load-scripts=no` means it does not test automatic scripts
   directory discovery. Add automatic/directory Lua and JS negatives and recorded
   positives before claiming those routes.
4. Guest data fixtures check only data reading. Add explicit data plus JS
   `compile_js` evaluation and its marker to preserve the already native-tested
   R4 route. Test mutable regular-file descriptors through `/proc/self/fd` and
   `/dev/fd` as well as pipes; the current mutable symlink does not cover an
   already-open regular descriptor. Native-plugin regressions are also pending.
5. `advance-mpv-release-041.py` does not add this newly requested document to
   its explicit archive additions, and `sync-mpv-041.sh` does not copy it. The
   parent must include it explicitly if adopting it for the release handoff.

The revised media fixture requires a file-loaded event with decoder sample rate
8000 and an end-file event with reason `eof`. Its ten-second timeout exits with
failure, and the probe requires its success marker. The libmpv control captures
both API log-message events and fd 2: the descriptor helper writes directly to
fd 2, so log events alone would miss its diagnostic. Each negative now requires
the exact saved-code denial and absence of an execution marker; declared Lua and
JS positives require their own log markers. The existing exact helper-denial
assertion in the subprocess runner is retained.

Automatic discovery now uses a temporary config directory with load-scripts
enabled, separately testing ordinary script entries and `main.lua`/`main.js`
directory entry points. Mutable sources must be denied, then symlinks to declared
sources must produce their positive markers. The new JS data fixture explicitly
reads mutable data with `mp.utils.read_file`, evaluates it using `compile_js`, and
requires its marker. Native source/API definitions were inspected for these
options, event layouts and entry-point conventions. Both Python files passed
`py_compile`; the generated cache files were removed. No build or guest test was
started. Actual descriptor-alias and native-plugin coverage remains pending.

The proposed scripts include inherited reader regressions, two boots, original
object invocation/loading checks, live app removal and last-runtime removal.
Their implementation is not evidence that these gates passed. Sealed-baseline
composition and object-preservation verification, correct payload deployment,
confined negatives/positives, original-object alias denial, data/media/plugin
regressions, removal and restart must all be observed before a guest claim.

Review status: native compatibility evidence 1; guest enforcement and release
acceptance ?. Only this draft and the two explicitly authorized future41 fixture
scripts changed. No main source, version, package or archive changed.
