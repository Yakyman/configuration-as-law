# Pinned Debian curl configuration-reader draft

2026-11-24 UTC. Source inspection, private compilation and native compatibility
controls passed. A separately authorized private sealed39 derivative passed the
bounded 32-control guest matrix below. No main release source, version or shared
package changed. Earlier source-only statements describe that checkpoint.

Search request entry 1 reports release 0.32 attempt 241 obeying a mutable
automatic `.curlrc` containing a user-agent option. This draft targets the Debian
curl command's option-file parser. It does not modify libcurl or Flatpak curl,
and does not claim the reported route has been refused in a guest.

## Exact inputs

The retained authenticated-snapshot indexes in the build cache name curl
`8.14.1-2+deb13u7`, architecture amd64. No matching source tree or curl binary
package was found in the inspected build subtrees. `prepare-curl-config-draft.py`
therefore fetched these exact files from the same Debian snapshot into the new
private `interpreter-inputs/curl-config-draft/` directory and verified each against
the cached index SHA256. No version selection from current repositories occurred.

| Input | SHA256 |
|---|---|
| `curl_8.14.1-2+deb13u7_amd64.deb` | `135636bd8b713c582d33e50ec4e36ea55cc3c5da3f12bbeb6b87d2bcbd3a0649` |
| `curl_8.14.1-2+deb13u7.dsc` | `a559b829ff852b2ee1ac0e448b5d9c18e0f94875bc820d037609d4d807ac6f57` |
| `curl_8.14.1.orig.tar.gz` | `6766ada7101d292b42b8b15681120acd68effa4a9660935853cf6d61f0d984d4` |
| `curl_8.14.1.orig.tar.gz.asc` | `39cc2ec8ddc39d04e3e7101bbed46d858d0875cbb297a6bfa20959fa2bc7d5c7` |
| `curl_8.14.1-2+deb13u7.debian.tar.xz` | `e0f627ee2b9ae61078b2835edc25c8b94a0b57e180a1bc72dd8636ef260c370b` |

The extracted original `/usr/bin/curl` SHA256 is
`52e9ceef96bd7c7dd4c2c9d8ac4c5f466c563dc0d16817720518b430da7a94b7`.
Package metadata requires `libcurl4t64 (= 8.14.1-2+deb13u7)`. Extraction used
`dpkg-source` to apply the exact Debian patch series. The extraction command skips
fresh signature checking because every input was already matched to the retained
index checksums; this task did not independently reauthenticate the old indexes.
Index contents/hashes and download URLs are retained in `input-provenance.json`,
`source-index.txt` and `package-index.txt`. Upstream maintainer identities in those
verbatim third-party indexes are not local personal information.

## Source boundary and proposed change

After Debian patches, `src/tool_parsecfg.c` SHA256 is
`5c8a2a3418c993229e7180c4f5c1e50fc891f016184135e1eeb4e1982b3dbf76`.
`parseconfig()` opens the automatic discovered file, opens an explicit filename,
or selects stdin for `-`. It then repeatedly calls `my_get_line()` and passes
each parsed option to `getparameter()`. `C_CONFIG` in `tool_getparam.c` calls
`parseconfig()` again, covering nested option files.

`tool_findfile.c` searches CURL_HOME, XDG_CONFIG_HOME, HOME and fallback locations.
Its discovery open/close is only a pathname probe. Authorization must follow the
actual later fopen, rather than trusting the discovery descriptor. The patch
checks `fileno(file)` immediately after stream selection and before any config
line is consumed. On failure it closes owned streams, frees the allocated path,
and returns failure; it never closes stdin.

`patch-curl-config-draft.py` requires the exact source/header hashes and unique
anchors. It writes only `patched/src/tool_parsecfg.c`, a private policy-header
copy, a reviewable diff and `reader-provenance.json`. The upstream extracted source
is unchanged. The diff SHA256 is
`ff36969f566c0c8bf0e0009fee4cb73806de38fe6e568c0192dfa34f4e9b9f9d`;
the patched C file SHA256 is
`c54538b3f1b43f7e15ca94db32dd41831c253910fd6584b84587a6fc92597b9a`.
The diff requires the accompanying header; it is not a standalone build recipe.

The exact `code-file-policy.h` is copied as `confos-curl-config-policy.h`, hash
`64e344ca44ea9859708b0f84fe3c8a41c6a56942eafc3e05a75a1f00434fbea2`.
Reusing its descriptor authorization is appropriate here because a curl option
file controls application behavior, including unattended automatic configuration.
This does not classify arbitrary transferred data as code. Its existing diagnostic
still says `ConfOS: Permission denied for saved code input`; no global helper
semantics or wording was changed.

The helper permits unconfined staging, permits nonregular descriptors, and for
confined regular files requires read-only storage without noexec. Thus recorded
configuration can remain usable, ordinary typed/pipe input remains usable, and
regular-file stdin is checked rather than exempted solely because its descriptor
number is zero. Whether the intended recorded configuration paths carry those
mount properties must be verified in the guest.

Only the config parser is guarded. The shared `my_get_line()` function is also
used for ordinary option data such as header files, so placing the guard in that
generic reader would wrongly broaden this change. HTTP bodies, upload files,
header data, certificates, cookies, netrc and other libcurl data routes are outside
this patch. Explicitly piping file bytes through a typed data-producing command
retains the R4 route rather than attempting provenance tracking through pipes.

`tool_operate.c:2233` deliberately ignores automatic config parse failure.
Accordingly the proposed guard emits a denial and skips a denied automatic file,
but command-line transfer options can still run successfully. Explicit `--config`
propagates failure as `PARAM_READ_ERROR`. A test must check the actual configured
effect and denial diagnostic; a zero transfer exit does not prove automatic
config acceptance. This draft does not change that upstream error-handling choice.

## Proposed controls, all pending

Use a controlled loopback HTTP endpoint recording headers and body bytes, unique
config markers, and isolated environment/home directories. First confirm each
negative's original unpatched control actually applies the marker. In the patched
confined run require the exact policy diagnostic and absence of the configured
marker, not just a failed request. Positive controls must demonstrate delivery.

| Route | Negative or positive observation required |
|---|---|
| Automatic HOME `.curlrc` | Mutable file marker absent with denial; otherwise identical recorded file marker observed |
| CURL_HOME and XDG_CONFIG_HOME discovery/fallbacks | Separate tests establish which file was selected, then verify its descriptor policy |
| `-K file` / `--config file` | Mutable regular file denied; recorded positive applies options |
| Nested `config = ...` | Recorded parent cannot authorize mutable child; recorded child positive works |
| Symlink, hardlink, inherited `/proc/self/fd/N`, `/dev/fd/N` | Underlying mutable regular descriptor denied; recorded descriptor positive works |
| `-K - < mutable-file` | Regular stdin denied; declared regular stdin positive works |
| Typed config pipe, FIFO, process substitution | Intended nonregular-input controls apply marker successfully |
| Explicit typed producer reading data into `-K -` | Preserve R4 data route; do not report it as a direct saved-file bypass |
| `-q` as first option | Upstream automatic-config bypass remains effective; explicit config still checked |
| No config file, command-line user-agent/options | Ordinary transfers and exit behavior unchanged |
| Upload/POST data, header-file data, downloads, TLS inputs | Byte-level data and protocol controls unchanged; no generic-reader guard |
| Recorded-config removal and reboot | Contributions disappear/reappear only according to applied declaration and restart state |

Build work, if separately authorized, must preserve Debian options, protocol/TLS
features and exact library dependencies, compare `curl --version` and dynamic
metadata, and package only the CLI replacement with original-object protection
appropriate to the existing Debian reader mechanism. At the source-only checkpoint
no binary, candidate package or runtime/guest probe had been produced.

## Subsequent private native candidate

The authorized build completed using GCC 14.2.0 (Debian 14.2.0-19), Debian
hardening flags and the inspected OpenSSL configure recipe. Private include/library
search paths and the GSSAPI prefix point to the extracted dependency tree. Only
the curl CLI was built, with the generated makefile's libcurl link prerequisite
overridden to the exact original shared library. No libcurl replacement was built.
The OpenSSL development/runtime packages were fetched with the cached snapshot
hashes; all other dependency packages came from the retained exact snapshot cache.
All archives are now copied into the curl private subtree. Host toolchain package
versions are recorded; a fully hermetic historical build environment is not claimed.

Candidate `interpreter-inputs/curl-config-draft/candidate/curl` SHA256:
`cf221d19c07407cc275bd2653bbf8417283d383a46e0a9d5824cfeae3e792095`.
The original and candidate `--version` output is identical, including all reported
protocols, features and security-patch version. The configure summary also reports
the same complete protocols/features, including OpenSSL QUIC/HTTP3. DT_NEEDED and
dynamic export sets match; no new symbol versions or RPATH/RUNPATH appear.

Fourteen unconfined native controls passed across original and candidate:
automatic, explicit and nested config, typed config pipe, regular config stdin,
typed options, and upload/header-file data. The loopback server verified actual
received headers/body, and each command returned the expected response body.
Regular stdin was intentionally accepted in these unconfined controls; no
confined refusal can be inferred from that run.

`build-curl-config-draft.py`, `probe-curl-config-draft.py` and
`collect-curl-config-draft.py` preserve the recipe and observations. Portable
evidence lives under `interpreter-inputs/curl-config-draft/publish/`, including
9,380 source/header/dependency/script/candidate checksum entries, configure log,
generated configuration, compiler/package versions and comparison/control output.
The disposable build tree was removed after preservation; exact source, patch,
dependency archives/tree and candidate remain. Both native units completed
successfully. The private subtree was 203 MiB after that cleanup.

## Private sealed39 guest proof

`build-curl-config-guest-draft.py` extracted a bounded private derivative of sealed
0.39, source SHA256
`b2742ec67b48e3735e82b84c52e4a54c23dbd44e3eb5e17fd2dd42f376f5eb57`.
It appended one optional curl payload to a private reader component, preserving
inherited file bytes except its extended manifest. Baseline component SHA256:
`cc6c38c00d1ff3842352650d4dd76d674a862201205b9dafe3ba787dbc6ce28e`.
Private component SHA256:
`c924e04f3ecd6ceec7e14e797b726448edf73bb852a241dbb27c2c2551f6bb69`.
The package version remains 0.39 solely inside this isolated derivative. It is
not a replacement for sealed39 or an approved later-release component.

The first image stopped at its preboot dependency assertion. The native cache
used Kerberos `1.21.3-5+deb13u1`; the guest's authenticated security snapshot
selected `1.21.3-5+deb13u2`. `libkrb5.so.3` bytes differ. The failure is retained.
`repair-curl-config-guest-dependency-draft.py` verified every expected guest
library against its exact selected package archive and matched each package
checksum to its retained authenticated APT index. It updated only the private
expected-library fixture and rebuilt the image; no library was replaced.
Per-package native/guest versions and differing hashes are recorded in
`guest-library-provenance.json`. The two dependency sets are not identical.

The persistent unit was limited to 8 GiB and 100% CPU; its single guest used
3 GiB, two virtual CPUs and the shared slot mechanism. Inside the guest, the
installed candidate and original control hashes, all listed dependency-library
hashes, and original/candidate `--version` equality were verified. The probe ran
under `confos-session (enforce)` as the ordinary user. The unmodified original
ELF was separately declared in this private test, so each negative route could
first demonstrate its configured effect.

The final log contains `CURL_CONFIG_PRIVATE39_GUEST_MATRIX_PASS 32` and
`CURL_CONFIG_PRIVATE39_PIPELINE_PASS`. Observations:

- Mutable automatic HOME, CURL_HOME and XDG_CONFIG_HOME configurations emit the
  exact denial. Transfers return the actual HTTP response with exit zero, but
  neither the mutable user-agent nor its configured header reaches the server.
- Explicit, nested, symlink, hardlink, inherited `/proc/self/fd` and `/dev/fd`
  configurations and regular-file stdin are denied before any HTTP request.
- Recorded automatic, explicit and nested configs, recorded stdin and recorded
  descriptor input apply their expected headers successfully.
- First-option `-q`, typed options, typed config pipes and an explicit data
  producer feeding config stdin work. The last route intentionally applies bytes
  read as data under R4; it is not a direct saved-config refusal.
- Upload body data and header-file data arrive intact, and the client receives
  the actual loopback HTTP response body.

Evidence is in `curl-config-guest-draft-evidence/` locally and
`interpreter-inputs/curl-config-draft/guest-evidence/` on the build machine:
portable final/first-failure logs, serial output, fixture bytes, provenance,
private component, scripts and SHA256 manifest. Exact guest dependency archives
remain under `guest-library-archives/`. The stopped guest's image, private source
and image worktrees, and staging directory were removed after preservation.

These bounded builder controls do not cover all protocols/TLS behavior, every
discovery fallback or FIFO/process-substitution variant, removal/reboot,
independent acceptance, or numbered integration. Those broader matrix rows
remain pending. Observed private guest controls: 1; release acceptance: ?.

`curl-config-metadata-draft.json` is the compact future-integration handoff,
SHA256 `33027ae952d91f63771bd300f3dbaed610d637db3b8fc1200327c2dc9fd509bf`.
It records package/release, target/mode, original executable hash (distinct from
the Debian archive hash), candidate path/hash, exact binary/source inputs and
licence files. `verify-curl-config-metadata-draft.py` matched all nine referenced
artifacts and the guest success marker. A future optional-reader entry should
require `original_sha256` before replacement, leaving inherited entries unchanged;
this draft does not implement or integrate that precondition.
