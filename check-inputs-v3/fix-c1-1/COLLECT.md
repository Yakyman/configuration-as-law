# Inventory collector draft

`collect.sh` runs on the host and invokes `lab.sh run VM --root` for guest system
tools. It installs no package in a guest. It has been designed for Section 4.2's
two inventory levels, not for deciding whether an object must be recorded.

```
C1/collect.sh --instrument-test instrument-debian OUTPUT_DIRECTORY
CAL_INPUTS_COMMIT=COMMITTED_REVISION C1/collect.sh --observe MACHINE OUTPUT_DIRECTORY
```

The first mode rejects every system other than Debian by reading host metadata.
The second is reserved for a future authorized check and currently refuses all
use before any guest command because required coverage is incomplete. The draft
commit-identifier field does not itself verify a Git commit or supply authorization. Neither command is to be run on a check machine
in this preparation task. Output directories must be new, preventing overwriting
an earlier record.

## Output and interpretation

`objects.tsv`, `level-1.tsv`, and `level-2.tsv` have the seven columns
`id, machine, level, kind, name, members, evidence`. IDs are stable hashes of the
synthetic machine ID, level, kind, name, and members; a state/version change changes
the identifier. Members are JSON strings/lists inside
TSV fields; tabs/newlines in object names are CSV-quoted. Raw commands, stdout,
stderr and exit codes are retained separately; `coverage.tsv` distinguishes
absence (127), failed queries and successful empty results. Never turn a failed
query into evidence that an object is absent. `metadata.json` records UTC and
coverage limitations. No classification is generated.

Level 1 contains package-manager reports for root and login users, system and
user service/timer states and unit-file states, process IDs and executable
links, accounts, groups, sudo reports, global SSH configuration reports, polkit actions/rules, loaded
modules, device-driver links, listening ports, firewall rule sets, saved network
metadata, cron entries and container engine reports. Package-manager support
includes native dpkg/rpm/pacman/apk/opkg/xbps, Flatpak, Snap, Nix/Guix, pip/pipx,
npm/pnpm/yarn, RubyGems, Cargo/rustup, Go, Conda/Mamba, Composer, GHC/Cabal,
OPAM, LuaRocks, R, Julia, dotnet and Homebrew. A report may include inactive
candidates with their states; it is not a claim that each listed candidate is in
force. Package results and user-service queries depend on available tools and
existing user managers; the collector never starts missing managers.

Level 2 traverses the whole stored filesystem, including all homes and mounted
filesystems. `/proc`, `/sys` and `/dev` are pseudo-filesystems and are excluded
from stored-object grouping; process/driver/module observations use them at
level 1. `find` errors are retained. Native package file manifests, Flatpak
locations, and Python distribution file manifests parsed as data on the host form the ownership union;
usrmerge aliases are canonicalized from observed symlinks. Non-owned entries are
grouped by immediate containing directory. A separate list contains executable
regular files, files beginning `#!`, and known shell startup file names even
when their executable bit is not set. Metadata retains mode, UID, GID, file
type and symlink target. Package-environment metadata paths are additional
evidence, not silently presumed unowned application data.

Network queries deliberately omit password values. No shadow password database,
private key, host identity, or publication-machine account data is requested.
The machines and accounts in results are disposable laboratory identifiers.

## Outstanding completeness limitations

This is **not yet an exhaustive collector**. Non-Python local language package
environments are discovered but ownership is not fully resolved. Arbitrary
additional package managers need an adapter. Container reports identify images
and containers but do not yet inventory every package inside their filesystems.
Native package databases with newline-containing paths cannot be unambiguously
parsed from newline-delimited command output. Flatcar's immutable OS content
needs an official image-manifest ownership adapter. All effective
PAM/access policy combinations, user namespaces, and code loaded by arbitrary
programs need coverage review. Unparsed reports are evidence bundles rather than fabricated individual objects.
Python query/distribution-manifest reconciliation remains incomplete. Unknown
ownership is not proof of no ownership;
unresolved entries must not be classified from this draft alone.

The Talos adapter and its documented limitations are separate. It is prepared
from published API documentation only and has never been run against Talos.
These gaps prevent marking the collector ready for a first check observation.

## Sources consulted before instrument tests

- https://manpages.debian.org/trixie/dpkg/dpkg-query.1.en.html — `--listfiles`
  lists package-owned files; `--show` supplies installed-package database data.
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html —
  `list-units --all` and `list-unit-files` cover distinct loaded/file sets.
- https://docs.flatpak.org/en/latest/flatpak-command-reference.html — `list`
  reports refs and `info --show-location` gives deployment locations.
- https://docs.python.org/3/library/importlib.metadata.html — distribution
  metadata and file manifests.
- https://www.gnu.org/software/findutils/manual/html_mono/find.html — NUL
  delimiters and whole-tree traversal.
