# Package adapters

Inherited check-1 adapter documentation, with the S4 digest limit updated below. Earlier fixture/rehearsal statements describe check 1; S4 validation and added receipt/source tables are documented in `../COLLECT.md`, `../READY.md` and the S4 part reports.
`packages.py` never executes package scripts, gemspecs, Nix or Guix. Discovery uses `command -v` and the bounded filesystem inventory. Every command uses the query deadline/output cap. Metadata reads have a 16 MiB per-file cap; S4 whole-file digest reads permit up to 1 GiB plus the run deadline and reject an unstable read. Large, unreadable, special and symlinked files remain unknown. Size equality alone never establishes unchanged. Package files are not read through pseudo-filesystem paths.

| Adapter | Reason record | Ownership / integrity |
|---|---|---|
| dpkg / apt | `apt-mark showmanual`, `apt-mark showauto`; unmatched unknown | `dpkg-query -W`, installed `.list`, `.md5sums`, `${Conffiles}`. Bounded full MD5 comparison. |
| RPM / dnf / zypp | `dnf -C repoquery --installed --qf` with full version/architecture identity and stored `%{reason}`: user explicit; dependency/weak dependency dependency; group/external/unavailable unknown. Readable `/var/lib/zypp/AutoInstalled`: members dependency, others explicit. | RPM `FILENAMES`, `FILESIZES`, `FILEDIGESTS`, `FILEDIGESTALGO`. Bounded full digest comparison; recorded size mismatch proves changed. Versions and architectures separate. |
| pacman | `pacman -Qqe`, `pacman -Qqd` | `pacman -Ql`; integrity unknown; mtree verification unimplemented. |
| apk | Installed database plus `/etc/apk/world`; members explicit, others dependency | Installed `F`/`R` paths and `Q1` SHA-1 records. Other digest formats unknown. |
| XBPS | Native pkgdb-0.38.plist automatic-install flag: true/dependency, false or absent/manual explicit | Bounded native compressed or plain file plists; files/conf_files SHA256 verification; links compare the captured literal target to the native recorded target; directories retain ownership only. |
| Portage | Native selected-set expansion with a unique installed match explicit; ambiguous matches and all other reasons unknown | `/var/db/pkg/*/*/CONTENTS`, bounded object MD5 and recorded symlink-target comparison; directories retain ownership only. No ebuild execution. |
| Flatpak | System and user `flatpak list --app`: explicit; `--runtime`: dependency | Role distinction, not historical intent. Deployment ownership/integrity not collected. |
| Snap | `snap list --all`, reason unknown | Images not expanded; image verification not collected. |
| Python | `.dist-info/METADATA`; `REQUESTED` presence explicit, absence unknown | CSV `RECORD` ownership and bounded digest/size comparison. Missing RECORD is an ownership gap. No interpreter startup or `.pth` execution. |
| npm | Installed lockfile `packages`: root direct dependencies explicit, remaining entries dependency; hidden locks without root marks unknown | Lock records identify packages only. No ownership inferred from directory containment or publish-time file patterns; per-file provenance unresolved and coverage incomplete. Installed package.json records without matching locks are inventoried with unknown reason. |
| Cargo | `.crates2.json` install records explicit | Listed binaries, integrity unknown. Legacy `.crates.toml` without JSON is a gap. |
| RubyGems | Installed gemspec names; reason unknown | File manifest unavailable; gemspec code never evaluated. |

Ownership failure clears `package_ownership_complete`; remaining paths must not be presented as proven unowned. Discovered unsupported conda, Composer, LuaRocks, Go and legacy Python records produce explicit gaps. This version does not claim complete language-manager support. Overlapping native/language ownership records remain separate. Missing is reported only when the verifier reports absence; missing scan entries alone do not prove absent files. Digest equality establishes content equality to the manager record, not record authenticity or permission equality. Directories retain ownership without entering the file denominator. Symlink integrity is known only when a supported native target record and captured current target are both available.

## Primary sources consulted

- [dpkg query manual](https://manpages.debian.org/trixie/dpkg/dpkg-query.1.en.html): `${Conffiles}` and status fields.
- [dpkg verification manual](https://manpages.debian.org/unstable/dpkg/dpkg.1.en.html): “Currently the only functional check performed is an md5sum verification”. This adapter bounds reads instead of running unrestricted verification.
- [RPM manual](https://rpm.org/docs/latest/man/rpm.8): “Output format of each queried package”. Tags supply metadata without verify-script execution.
- [dnf repoquery source](https://github.com/rpm-software-management/dnf/blob/master/dnf/cli/commands/repoquery.py): `userinstalled` and `reason` queries.
- [pacman manual](https://man.archlinux.org/man/pacman.8): “Mark a package as non-explicitly installed”.
- [Alpine handbook](https://docs.alpinelinux.org/user-handbook/0.1a/Working/apk.html): “The packages you want to have explicitly installed are listed in the” world file.
- [XBPS manual](https://man.voidlinux.org/xbps-query.1): `automatic-install` property and installed file lists.
- [Portage source](https://github.com/gentoo/portage): CONTENTS and selected-set records; current dependency edges never prove historical install reason.
- [Flatpak reference](https://docs.flatpak.org/en/latest/flatpak-command-reference.html): “Show the application or runtime ID”.
- [Python installed-project standard](https://packaging.python.org/en/latest/specifications/recording-installed-packages/): RECORD and METADATA.
- [PEP 627](https://peps.python.org/pep-0627/): “REQUESTED was to be written when a project was installed by direct user request”.
- [npm lockfile reference](https://docs.npmjs.com/files/package-lock.json.html/): root empty-string key and relative package paths.
- [Cargo Home](https://doc.rust-lang.org/cargo/guide/cargo-home.html): “These hidden files contain package information of crates installed via” the install command.
- [RubyGems guide](https://guides.rubygems.org/gemfile-and-gemspec/): “Ruby projects declare dependencies in two different files”. Gem specifications can contain executable code.

## Validation state

Local Python syntax compilation passed. No machine collection was run by this adapter task. Disposable-machine tests belong to the main task. Untested adapters remain explicitly unverified in `COL-READY.md`.

Synthetic adapter fixture (in-memory records only) passed: one manual dpkg package, one changed conffile, one matching MD5, one verifier-reported missing file and one file with no recorded digest yielded respectively explicit, changed, unchanged, missing and unknown. This checks parsing and state transitions, not guest commands or manager compatibility. Output: `Synthetic dpkg fixture: explicit reason, changed conffile, unchanged digest, missing path, unknown without digest: PASS`.

Review correction: npm directory containment no longer assigns file ownership. This preserves locally added files as unresolved instead of hiding them among known package files. Unlocked node_modules package metadata, incomplete Python distribution metadata and additional discovered unsupported language databases clear ownership completeness. No local collector fixtures were run for this correction; authorized guest validation remains pending.

## Native-packaged Python metadata reconciliation

A Python distribution with an explicitly native-owned `METADATA` and no scanned `RECORD` uses the native package manifest for file provenance. The Python object lists `native_package_ids`; the native objects and package-file rows retain their own installation reason and integrity evidence. Python reason remains unknown unless its own REQUESTED record exists. No directory-based ownership is inferred and files added locally remain outside the native manifest. A present but unreadable/truncated RECORD still creates a gap. A separately installed distribution whose metadata is not explicitly native-owned still creates an ownership gap when RECORD is unavailable.

Native-owned legacy PKG-INFO or a regular egg-info metadata file is represented as a Python package linked to native package IDs. A native-owned egg-info directory alone does not justify this reconciliation; the actual metadata file must be native-owned and readable. This removes a redundant missing-language-manifest gap without extending the native manifest.

Package manager discovery also runs `command -v` for each login user with standard user package-manager bin directories and observed npm bin locations added to that query's PATH. It does not execute discovered manager binaries or shell startup files. Discovery failures clear ownership completeness. Present pipx, Poetry, uv, pnpm, Yarn and Bun, as well as conda, Composer, LuaRocks and Go, create explicit unsupported-adapter gaps; no complete inventory is inferred from their presence. Native-owned Python reconciliation and expanded user discovery passed the authorized Debian/Rocky full runs; see `../raw/debian-validation.json` and `../raw/rpm-validation.json`. Unsupported managers remain untested.
