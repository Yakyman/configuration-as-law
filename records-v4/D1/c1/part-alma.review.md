# Independent review of the alma classification

## Result

Accepted. No concrete classification error was found within the retained evidence. The output is structurally complete, the high-risk provenance and integrity rules reproduce from raw facts, and sampled `UNKNOWN` decisions name facts that the retained inventory and action logs do not supply.

## Full structural checks

- The output has exactly 6,293 data rows, exactly one for every input ID, with no duplicate or extra IDs.
- Every decision is one of the 15 permitted categories. All sentence IDs exist, all evidence fields use permitted prefixes, all referenced raw paths exist, and the two prose limits pass.
- All 1,647 stored-group rows match their complete raw member TSVs in member count, path, and order.
- Every homogeneous stored group has the same decision as all of its members. Every one of the 108 `MIXED` rows has more than one member decision: 98 partition into `INSTALLED-PACKAGE` and `UNKNOWN`; 10 partition into `RECORD` and `UNKNOWN`.

## High-risk manual checks

### Native-owned language packages

All 47 native-owned Python package entities retain nonempty `native_package_ids`. The classification uses that recorded package-entity provenance and does not transfer the language-manager installation reason. The retained fact identifies the containing native package line; individual stored files remain subject to their separate integrity evidence. No contrary retained fact was found.

The 195 native-owned npm package entities use the same package-entity rule. Their notes additionally report the separate native-manifest check for observed non-directory descendants. User-installed npm contents without matching per-file provenance remain `UNKNOWN` where required.

### Relocated Python entry scripts

All eight console entry scripts under the pip target were reconstructed independently from `D1/in/raw/alma/raw/0009-metadata-read-256.out`. For each script, `size=signature_bytes`, the retained signature covers the complete file, and its SHA-256 and size equal the corresponding installed-distribution `RECORD` entry. The eight `INSTALLED-PACKAGE` integrity decisions are supported.

### Volatile objects and creators

The two individual volatile files attributed to `crun` have `persistence=runtime`; the retained package-file table establishes unchanged integrity for the creator executable. Runtime stored groups were checked from every member's persistence field rather than from path names. Sampled process, kernel, firewall, timer, port, and generated-unit rows preserve `UNKNOWN` for the creator when the executable or image fact is unavailable.

### Unit files

Every `unit-file` and `user-unit-file` decision was checked against the selected path and its retained filesystem and package-integrity facts. All 391 `INSTALLED-PACKAGE` rows select a persistent file or symlink with `integrity=unchanged`; all 15 `RUNTIME` rows select a runtime-backed generated file or symlink; the local user unit is a persistent non-package setting; and the 10 unresolved aliases remain conservative `UNKNOWN`.

The state and preset columns accompanying the unit-file listing do not invalidate the file decision. The persistent enablement links and runtime generator links are separate stored objects in the complete member inventory. For example, the persistent `vgauthd.service` enablement link is separately `UNKNOWN` in `alma-1e33fe58f57b8be4bcbaadc4`, while the runtime generator and invocation links for `systemd-remount-fs.service` are separately `RUNTIME` in `alma-904ac6b1c3dde89ef0c1ae58` and `alma-a59e8fb1350c7f27463b5297`.

### Conservative unknowns

Representative `UNKNOWN` rows were checked for package integrity, installation reason, directory creation provenance, executable content, installation defaults, state origin, and unexpanded membership. The raw package table omits directory integrity, unsupported npm provenance remains absent, opaque stores remain unexpanded, and the named action logs do not supply the missing origins. No sampled missing fact could be resolved from the retained data.
