# Future41 mpv integration preparation

2026-11-24 UTC. Draft scripts only; no main-source change, version transition,
numbered archive, guest run or acceptance. Sealed40 is the mandatory baseline.

## Exact inputs and replacement boundaries

Application ref `app/io.mpv.Mpv/x86_64/stable`, commit
`13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc`;
bundle `flatpak-inputs/mpv.flatpak`, SHA256
`66d65390ff1b7a526b25a448f12d137f72df5859460c1d05e17508ed6a88bed9`.
Native inspection identified the following regular files, each mode 0755 and
hard-linked to its original repository object:

| Target under deployment `files/` | Repository object under `repo/objects/` |
|---|---|
| `bin/mpv` | `7c/af52a2b7889c5ba35029dab06708b329f674ae4734a8a6d07621cc61414445.file` |
| `lib/libmpv.so.2.6.0` | `87/a3508d1277def6f05a50f083695a150286dd79584dae1208277b2849913204.file` |
| `lib/libluajit-5.1.so.2.1.1781966178` | `b4/439190066f7f36b90f776e4f0cd979eba4711a14847c9e77240c379cb2590d.file` |

The complete originals/replacements hashes, exact object paths, modes and symlink
targets are in `flatpak-mpv-app-overrides41-draft.json`, SHA256
`4ada6b113190b3cbf44ddaec16be03967fc05224c66ab89566cca94b5d8da0bf`.
It is copied from private worker metadata, not inferred from filenames.
The two libmpv and two LuaJIT aliases retain their current symlink targets.

`patch-flatpak-app-ref41-draft.py` changes only the anchored ref validator and its
error wording; `flatpak-app-ref41-draft.patch` is the reviewable two-line diff.
The validator accepts `runtime/` or `app/`, still x86_64 and the
same component character sets; it additionally rejects literal `.`/`..` path
segments, which the prior regex inadvertently permitted. All digest, target,
payload, mode, containment, original-object identity and replacement checks stay
unchanged. Output is restricted to the private draft tree. Positive app/runtime
and negative validation controls pass in `flatpak-mpv-integration41-preparation.log`.

## Sealed-baseline-gated package recipe

After sealed40 exists, run `prepare-flatpak-mpv-package41-draft.py` in a persistent
worker unit with `MemoryMax=8G`, `CPUQuota=100%`, `TasksMax=128`. It refuses unless
the source archive matches `releases/release-0.40.sha256`, its `VERSION` is 0.40,
and its embedded code-readers package equals the retained40 package exactly.
It takes the module to patch from that sealed archive, not the changing worktree.

The script produces only
`interpreter-inputs/flatpak-mpv-integration41-draft/confos-code-readers_0.41_amd64.deb`,
its checksum, a patched private module and composition provenance. It appends
three `mpv41-*.gz` payloads and manifest entries, preserving the three inherited
runtime entries and every inherited file except the deliberately extended
manifest. New documentation uses a separate `mpv41` subdirectory. It never writes
the main packages directory, VERSION, runtime source, or releases.

`verify-flatpak-mpv-package41-draft.py` compares every inherited payload byte,
mode, owner and link; checks the exact allowed additions and manifest prefix;
then tests the patched module on copies of the actual original app objects in a
disposable tree. That staging test checks wrong-bundle refusal, original-object
preservation, new inode replacement, unchanged symlinks and both original-object
policy aliases. It does not run a guest or establish confinement.

## Rebuild/provenance inputs and remaining limitations

`flatpak-mpv-archive41-paths-draft.py` emits additive archive paths only. It includes
the exact mpv/LuaJIT/MuJS archives, all dependency archives and submodule inputs,
patched source, candidate bytes, restored headers and metadata, build/patch/probe
scripts, provenance, complete input checksum manifests, both original Flatpak
bundles, and the sealed40 reader package. It does not edit the archive recipe or
create a numbered archive; the final transition must append these paths while
retaining every existing40 archive member.

The SDK tree is explicitly identified rather than copied into this additive
archive list: `runtime/org.freedesktop.Sdk/x86_64/26.08`, commit
`a1b744b072d9f55d061e35382547ae80dad8d92abecc1da7dc1818de2daabfd3`, installed by
`fetch-flatpak-mpv-sdk-draft.py`. Its metadata and complete 40,608-entry checksums
are included. For an offline rebuild the retained SDK deployment must additionally
be archived; no claim is made that the archive list alone supplies an offline SDK.
The exact original app/runtime link libraries are supplied by the two bundles.

mpv was built with that SDK's GCC 16.2.0; historical upstream full toolchain
identity is unproven. The retained guarded LuaJIT candidate was built earlier with
the worker compiler; its bytes and source/patch provenance are archived, but a
bit-identical reconstruction of that historical host compiler environment is not
claimed. Dynamic-only FFmpeg/libbluray metadata does not describe static private
dependency closure. The MuJS absolute DT_NEEDED difference and observed matching
feature/symbol sets are documented in `flatpak-mpv-continuation-draft.md`.

The final transition remains separate: apply the reviewed module patch to the
future source, promote only the verified private component, build the matching
runtime component, update its lock through the normal release process, and then
perform positive/negative app and libmpv saved-Lua guest controls, original-object
alias checks, ordinary media/JavaScript/native-plugin regressions, removal and
restart checks. No result from these future steps is asserted here.

Preparation status: native target discovery and app/runtime validator controls
passed, and every path emitted by the additive archive helper exists on the
worker. The sealed40 archive and release checksum were not yet present at handoff;
private package composition and its inheritance/object-staging verifier therefore
remain unexecuted. No sealed-baseline requirement was bypassed.
