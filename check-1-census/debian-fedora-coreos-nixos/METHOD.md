# V1 census method (2026-11-19)

Provisioning research and collector inspection were done as a separate step,
without classifications. The second, independent classification (V2) and the comparison (V3)
are separate steps; V1 does not read either classifier's other outputs.

Work runs only on `<HOST>` inside disposable VMs under
`<WORKDIR>/v1`. Each VM has 6144 MiB RAM and 2 vCPUs.
Long-lived jobs use user systemd units. Host sudo is never used; guest sudo is
used only to administer these disposable machines and obtain a complete census.

The logical VM names used in TSV `machine` are `debian`, `coreos`, `nixos`, matching
the launcher argument, server subdirectory, and `cal-v1-*` service name.
Official source URLs and checksum results are in each `raw/<machine>/source.txt`
and `checksum.txt`. Images are downloaded over HTTPS and checked against official
published digests; detached signatures were not verified.

The day of use is a short scripted CLI session, **not 24 hours of elapsed time**:
one added program, one user setting, documents, then at least 120 seconds of
service activity. Debian: apt/jq, `.nanorc`, Markdown+JSON; CoreOS: rpm-ostree/tree,
`.bashrc`, Markdown, a deployment reboot; NixOS: nix-env/hello in a normal user's
profile, `.vimrc`, Markdown. Timestamps and command results are in `day*.log`.
`loginctl enable-linger census` is disclosed instrumentation, set during the day
script before collection so a user service manager can be enumerated.

`collect.sh` saves package inventories/file membership, all loaded system and
user units (including inactive/missing entries), unit files and timers, processes
and executable paths, passwd/groups, loaded modules and module filenames,
device-driver bindings, mount topology, and a filesystem walk. Missing units are
observations of systemd's reference graph, **not claims of running programs**.

The walk uses the personal-machine census roots `/etc /var /opt /usr/local /srv /home /root` and adds
`/boot`, local descendant mounts, and `/nix/var`. Symlinked roots are resolved;
entries are deduplicated. Symlinks below roots are not followed. `/proc`, `/sys`,
`/dev`, `/run`, `/tmp` are not general file-walk roots; targeted facilities supply
some observations there. Unowned files elsewhere under `/usr`, firmware state,
and the complete CoreOS `/sysroot/ostree` backing store are outside this walk.
Current/saved CoreOS deployments are separately represented by rpm-ostree status.
Inactive unit-file listings and device-driver binding listings remain raw-only
coverage; module objects are classified. These are coverage limits, not absent
objects or successful classifications. The collector's own processes occur in
the process census. Disappearing processes have no subsequent executable link.

`preclass.py` reuses `canon`, `group`, `is_data` and constants from an exact saved
snapshot of `A/preclass.py` (`raw/a1-preclass-reference.py`). It adds observed path
aliases, CoreOS home spelling, per-scope unit metadata, and Nix closure membership.
The package-membership convention of the personal-machine census is an **operational recorded proxy**;
it does not demonstrate a person-designated primary declaration, P1, or P4.
For NixOS only objects in the current system closure get that proxy; arbitrary
store membership does not. User-profile-only and other store objects are residual.
Packaged unit fragments with unowned drop-ins also remain residual.
All remaining decisions in `c1-classes.tsv` are the first classification,
not additions to deterministic pre-classification or revised definitions.

Counts are counts of grouped observations, not disjoint physical objects:
packages, files, units and processes can refer to the same underlying program.
`member_count` retains cardinality for automatically classified groups; raw group
JSON retains every stored member. No residual row is silently truncated.
The initial reduction produced 478 residual rows. To meet the 400-row bound,
directory-only groups (no files, links or other non-directory entries) are retained
in a per-machine structural group with a complete `directory-only-groups.json`
manifest, and Nix's 32 build users become one account family with every passwd
entry retained. No content-bearing directory groups are merged and no class is
assigned by this grouping. Unknown provenance of these structural groups is an
evidence limitation, not a demonstrated §9.2 counterexample.

First attempts are retained: Debian's first unit-path query failed on `-.mount`,
so the complete day was repeated in a new clean VM; CoreOS's first Ignition config
lacked passwordless sudo, so the image was recreated with an explicit sudo rule;
NixOS's first auto-type mount failed, then explicit `-t ext4` succeeded. These are
stand defects and are not hypothesis counterexamples. CoreOS escaped unit names
were passed through xargs without a newline delimiter; the full unit listing
remains intact, but some escaped-name metadata cannot be matched. Those entries
remain residual. The delimiter was fixed for the final Debian/NixOS collections.

The definitions and failure condition remain PAPER.html §5 and §9.2 unchanged.
Evidence/provenance gaps must be distinguished from demonstrated definition
counterexamples; the final independent comparison is a separate step.

## FV1 reporting clarification (2026-11-19)

Package/image membership remains an inventory proxy only, uniformly for automatic
and residual observations. It never proves person designation under §5. All
reported class counts are counts of the submitted labels; the 2,649 automatic
`recorded` labels are proxy counts, not validated class assignments. Debian and
CoreOS recorded membership is unestablished, including in the pooled count;
NixOS source/import/closure evidence is stronger but is not a general membership
rule. The 71 residual `designation+evidence-gap` disagreements remain unresolved.
No collection, original label, definition or failure condition changes in FV1.
The amended adjudications and comparisons are frozen in `raw/fv1-comparison/`;
`FIX-1.md` records finding dispositions and independent review.
