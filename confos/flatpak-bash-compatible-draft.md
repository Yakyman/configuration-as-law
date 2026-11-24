# Compatible Flatpak Bash candidate, 2026-11-24

Candidate worker path `interpreter-inputs/flatpak-bash-compatible/bash`.
Build scripts: `build-flatpak-bash-compatible.sh`,
`link-flatpak-bash-compatible.sh`. No production integration.

| Target | SHA256 / alias |
|---|---|
| Runtime original `files/bin/bash` | `9b814ddc2495f9a0fecd2049f1dff711cee00f0a2fdde946cf5c29e5f8cbb97b` |
| Replacement `files/bin/bash` | `27f0efbc3d136c6c8b8d8d54a3f35c7a17a9c67615d49142d6d7fae32f3d9e3b` |
| `files/bin/sh` | existing symlink `bash`, unchanged |

Exact deployment: runtime/org.freedesktop.Platform/x86_64/26.08 commit
`df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c`.
Upstream Bash commit `9c465866b7d849378369ef700cbe2965aa9691e3`,
archive SHA256 `91a4dcfbf1c170b0f8ed619e9625813b9301e5a8f79c710d4bebb30796d56bb8`.
Verified SDK patch SHA256 `e7a38fe0c52924d0b99c3d1bbde5e01e517e810ad4b20832b47ea81733d32719`
enables NON_INTERACTIVE_LOGIN_SHELLS; applied before descriptor code guards.
See `flatpak-reader-provenance-draft.md` for pinned official URLs.

Configure follows matching SDK recipe: installed readline, curses/libtinfo,
job control, no Bash allocator, recorded cache answers. Native GCC14.2,
host configuration/header detection and -O2/-g0 differ from a full SDK build;
source paths mapped, epoch pinned. Exact SDK build/toolchain remains unknown.
Initial host Readline link failed (missing Bash5.3 symbols). Next target
library link found host ncurses version mismatch; rpath-link fixed lookup but
target terminfo requires GLIBC2.42 unavailable on host. Final link defers
shared-library undefined references with --allow-shlib-undefined, then tests
actual execution in the retained complete runtime. No RPATH or new libraries
are installed. Exact original libraries used at link time:

| Library | SHA256 |
|---|---|
| libreadline.so.8 | `ec59e0c0c3c23f5fb2f2cad1e7e9af9fac44b0b3bf3f6e91b525fd42486b410a` |
| libhistory.so.8 | `1c8832c73ef34aa9b44aed7aff5d3297387e1011003e0a7e6492a9366832dc98` |
| libtinfo.so.6 | `b77d281e18a31f2e05984f743e039ef57d80264474c4c0b72431ff53c3ca5da4` |

Bwrap controls execute candidate /usr/bin/bash and sh alias in original runtime.
`probe-flatpak-bash-compatible-abi.py` confirms identical version, builtin
list and default shopt/set options versus original. ELF dependencies and
versions saved in link log. This is bounded compatibility evidence, not
complete interactive/NSS/job-control regression or an identical SDK rebuild.

Guest fixture checks passed. Fixture declared payload and appended a private
initramfs /init override to bind it over exact target on each boot; original
OSTree inodes unchanged. Original object aliases remain executable and need
separate production treatment. Fixture is external test instrumentation,
not completed declaration-derived integration.

Evidence: `records/flatpak-bash-compatible-build.log` (first failure),
`records/flatpak-bash-compatible-link-first.log`, `*-link-second.log`,
`*-link.log` (final successful link/runtime test), `*-abi.log`,
`records/flatpak-bash-compatible-0.35.log`, and `*-fixture-boot.log`.
Actual `confos-flatpak (enforce)` and exact replacement identities recorded.
On each of two boots, both /usr/bin/bash and /usr/bin/sh refuse all9 saved
script/source/stdin routes across home/tmp/shm. Both pass recorded script,
recorded source, typed, piped and data-read controls. Bash additionally passes
recorded BASH_ENV and refuses unrecorded BASH_ENV; startup may refuse the
input yet return0 for the subsequent `-c :`, as the log records.

The SDK config patch is exercised specifically by `exec -a -bash` with
noninteractive `-c :`: a recorded HOME/.bash_profile runs and an unrecorded
/tmp/login/.bash_profile is refused, on both boots. This closes the earlier
prototype's omitted configuration behavior. No full interactive readline,
NSS or job-control suite was run. Direct bwrap/unshare attempts to make
unrecorded material read-only remain untested; guest cleanup had completed
before that additional diagnostic was requested. No generic namespace
closure is claimed.

Disposable guest/image/initramfs fixture removed. Source/build retained.
Original repository object identities and symlink aliases are recorded in
`flatpak-reader-object-aliases.md` and
`records/flatpak-reader-original-objects.json`. Production integration still
needs exact original-checksum guards, atomic replacement, derivable payload
ownership and execution/mapping restrictions for original object aliases.
