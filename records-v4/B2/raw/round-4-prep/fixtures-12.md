# Cases 1 and 2 fixture preparation

Recorded 2026-11-23 UTC. Preparation only; no case was performed and no virtual machine was started by this fixture preparation part.

## Committed question and selected inputs

`SUP1/step-6.md` fixes opposite package installation order with a byte-identical last-applied declaration. `TEXT.md` Appendix A.4.4 requires every stated value and the account name, identifier, groups, shell and home. S8.1-12 says: “The required state of a recorded object is stated by its line.” S8.2-17 says: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.” These fixtures use explicit own account lines and package installation applies them in the same transaction.

`B2/build/bc4-fixtures-12.py` prepares inert artifacts without installing accounts or packages. Each package installs one read-only JSON file describing its account, and creates that account through the existing account activation in `B2/build/stand.py`. The account database tools are unchanged. The output directory defaults to `/usr/local/share/stand/bc4`.

| Artifact | Package ID / exact registered identity | Account ID / name | UID / GID |
|---|---|---|---|
| `check-inputs-v4/supplement-1/step-6-cases/B2/cases-6/artifacts/package-alpha.json` | `bc4-package-alpha` / `stand:bc4-account-alpha:1` | `bc4-account-alpha` / `bc4alpha` | 2201 / 2201 |
| `check-inputs-v4/supplement-1/step-6-cases/B2/cases-6/artifacts/package-beta.json` | `bc4-package-beta` / `stand:bc4-account-beta:1` | `bc4-account-beta` / `bc4beta` | 2202 / 2202 |

Both accounts state their own primary group and no supplementary group, `/usr/sbin/nologin`, `/home/NAME`, and exact GECOS text `BC4 alpha account` or `BC4 beta account`. Both package payloads have mode 0444, UID/GID 0, exact SHA-256 and base64 bytes, version `1` and an explicit local source identifier. The package has exact `package_contribution_ids`, validated to refer to existing managed rows, and a `package_identity` handled by the inherited registration mechanism. The four rows are emitted in stable alpha-package, alpha-account, beta-package, beta-account order as `case-2a-rows.jsonl`. Two intermediate row fragments are `rows-alpha.jsonl` and `rows-beta.jsonl`. None of these fragments alone is a complete machine declaration.

## General mechanism and recipe integration

`B2/build/bc4_packages.py` accepts the exact `stand-package-bundle-v1` artifact envelope through `stand-pkg`, `apt`, or `apt-get`; the `B2/build/v4_tools.py` dispatcher routes it to the common transaction. Each envelope contains a registered package row and managed contribution rows. Existing declaration admission validates every row and applies the entire candidate atomically. `B2/build/guard.py` checks the contribution relation for every candidate, including direct `stand-apply`. Removing an owned contribution while retaining the package refuses as an inconsistent package requirement. Generic bundle removal removes its rows together, retaining a contribution referenced by another remaining bundle. This is a mechanism for exact multi-row packages, not an account-name or command-specific exception. The account row schema and UID policy were not extended.

The image recipe must install `bc4_packages.py` beside `v4_tools.py` and invoke `bc4-fixtures-12.py` before factory capture. The generator itself must be included in the frozen recipe input manifest. No fixture package is installed into the frozen clean image.

Opposite order is produced on fresh guests by these ordinary commands:

```sh
# First guest
stand-pkg install /usr/local/share/stand/bc4/package-alpha.json
stand-pkg install /usr/local/share/stand/bc4/package-beta.json
# Second guest
stand-pkg install /usr/local/share/stand/bc4/package-beta.json
stand-pkg install /usr/local/share/stand/bc4/package-alpha.json
```

The integrated procedure must then apply the same complete frozen declaration to both guests, including all five designated filesystem descriptions. Applying the same `machine.jsonl` alone is insufficient: `B2/build/bc3-state.py` exports five additional declarations containing exact account database bytes, inode maps and metadata. Account database append order can differ after the installation commands. `B2/build/bc3_filesystem.py` records timestamps, inode identities and generation numbers. The integration supplies complete-bundle application; this fixture preparation does not claim the existing `stand-apply` already replays those files.

## Case 2b: not expressible on this testbed

`B2/build/stand.py`, function `load`, directly reads `r['uid']` and requires managed UID 1100–60000. `expected_account` requires name, UID, GID, groups, shell, home and GECOS. Function `activate` passes explicit `-u` and `-g` to the native account tools and refuses changing the numeric identifiers of an existing account. `B2/build/guard.py`, account branch, additionally requires numeric GID 1100–60000, the account's own group, `/home/NAME`, `/usr/sbin/nologin` and GECOS. There is no UID omission, automatic allocation token or default in the managed account format. Omitting `uid` fails before account application; omitting the account row conflicts with the package's required contribution.

Using the native account tool without `-u` does not provide a declaration line omitting UID: `B2/build/bc3_account_rows.py`, function `account_rows`, emits an explicit numeric UID/GID and exact encoded account database contents in the designated filesystem declaration. Such a command can choose an identifier, but its last-applied declaration states that identifier. The original case is therefore marked not expressible; no alternative default or format was invented.

## Case 1 unambiguity support

These two package and account pairs may be reused in case 1. For each package line, exact package identity, version, payload bytes/hash, destination, permissions and ownership determine its installed object and file. Its contribution IDs identify specific account rows rather than an external source or environment-dependent choice. For each account line, all seven fields read by the account observer are explicit, with fixed numeric UID/GID and exact group list. No account value is left for allocation. The integrated case-1 declaration must additionally explain every inherited factory and filesystem row; this note establishes only these four new rows.

## Static verification and limits

Local static verification parsed `bc4_packages.py`, `bc4-fixtures-12.py`, `v4_tools.py` and `guard.py` with `ast.parse`; constructed both artifacts in memory; validated the complete four-row relation; and verified that removing `bc4-account-alpha` while retaining its package raises `ValueError`. Output:

```text
Missing owned contribution rejected: package contribution line missing
AST parsing and static bundle consistency passed; no fixture installed
```

This is a source/data check, not a case outcome or runtime installation claim. The integrator must trial readiness on a disposable copy if needed, preserve the final image/declaration identities, and publish the frozen case commands before independent attempts. The ordinary shell and privileged direct-edit breaking remain available. No hypothesis outcome is assigned here.

## Integration source review

Recorded 2026-11-23 UTC. `stand.py:frontend` calls `v4_tools.dispatch` before the older single-row `stand-pkg` branch, including after normalizing `reinstall` and `downgrade`. The added dispatch therefore handles the bundle before the older parser looks for a top-level `type`. `guard.validate` invokes the contribution check for direct full-candidate application as well as package installation. The account row remains an explicit own setting: modifying its fields through its configuration tool changes the desired account while leaving the received package-default JSON file unchanged. Removing only the account while the package requires it is rejected. No additional source correction was needed for these case inputs.

Review of the integration's initial `bc4_bundle.py` found two items communicated for correction: (1) its original complete-success path checked stored description bytes after filesystem import but did not reverify machine requirements after `/etc` had been replaced; a contradictory account or unit filesystem description must not produce a complete success; (2) export originally checked each filesystem only immediately after reading its blobs; all eight descriptions must be reread at the end to reject a mixed-time bundle. These are review findings about that intermediate source, not observations from an executed case. The integrator owns their final disposition.

Complete targets should be exported after a successful trial application of the fixture machine rows and verification, with the matching current `/etc` account databases, derived semantic rows, unit files and generated policy state, rather than combining newly edited machine rows with stale base filesystem bytes. Export directories must be outside the five mediated roots. Exact blobs accompany all referenced filesystem objects. A stable final complete export is needed even when the machine declaration itself is byte-identical.
