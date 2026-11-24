# MicroOS classification c1

Scope: 747 rows of `D1b/in/part-microos.tsv`. Only the specified definition, sentence list, input facts and handoff were consulted. No participation in the preceding construction steps, rehearsal outputs, other classifications, earlier nights, or other supplement steps. This is classification, not acceptance of the hypothesis.

The two disjoint parallel portions are documented in `part-microos.units.notes.md` and `part-microos.selinux.notes.md`; their rules and manual samples are part of these notes. Their output was appended to the principal table after the remaining rows. `part-microos.local.py` appends the local rows without overwriting completed rows.

## Decision order

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-8: “Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

Persistent stored files are not runtime objects. Snapshot location is not an exemption from question one. Section 8.5 excludes implementation questions concerning generations and rollback, not objects stored in a snapshot. No decision uses the inventory's suggested class.

## Rule A: account and group values with missing creation history

The first 22 rows are effective account/group database values. S8.2-13 identifies accounts and rights as settings. S8.2-17: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”

`configuration-origin.tsv` records unknown creation for `/etc/passwd` and `/etc/group`. `raw/0002-metadata-read-0.out` and `raw/0003-metadata-read-0.out` establish the records. `raw/0154-s4-microos-scriptlet-sources.out` contains conditional creation code, including initial shadow/trusted/users groups, but no historical execution event. Current resemblance to defaults cannot establish installation provenance. UNKNOWN distinguishes SETTING-DEFAULT from SETTING-OWN; this is missing historical fact, not a textual gap. The rule is applied only to these account/group rows.

Ten hand-checked rows (record names, IDs, and database origin were checked individually):

- messagebus account: d1b-microos-62e69634eb677cc7b715d241
- polkitd account: d1b-microos-44968babf50ac013fbdb5e04
- shadow group: d1b-microos-89d72e1d004fe5a1cbfcbfc1
- trusted group: d1b-microos-d4d9a26cf3efa0ddbc282e7a
- users group: d1b-microos-788f3669ea0e88fffdb28029
- nogroup group: d1b-microos-6fcd8e4101758b33879caad5
- kmem group: d1b-microos-3663e1d2597d977b6b38e435
- lock group: d1b-microos-0a3a40b7fc3652cc69a3cce5
- tty group: d1b-microos-9935d1821c44a013296fa959
- utmp group: d1b-microos-23af84186633b91bde0b5f42

The other twelve account/group records were also displayed and checked before applying this rule.

## Rule B: ten unchanged snapshot package files

The ten individual files at input positions 283–292 have persistent metadata and complete equal SHA256 comparisons against their snapshot RPM package manifest in `s4-microos-snapshot-files.tsv`. The supplying packages also occur in `objects.tsv`: aaa_base, glib2-tools and grub2-common have dependency reasons; ignition is explicit. Those reasons affect coverage of the package itself, not the fact that its unchanged members are covered by its package line. Question one and S8.2-16 give INSTALLED-PACKAGE for every file; no executable-code inference is needed.

All ten hand-checked rows:

- d1b-microos-f9572b723ebb51b53c3e492a: bash.bashrc, aaa_base, equal
- d1b-microos-12effc2b423489dd6407334f: 00_header, grub2-common, equal
- d1b-microos-554d9e3930246896719a0d2c: 10_linux, grub2-common, equal
- d1b-microos-10c1c900a8219351fcbe8208: 20_linux_xen, grub2-common, equal
- d1b-microos-09f3842e92f45717460dac8d: 30_os-prober, grub2-common, equal
- d1b-microos-955fecad9ca6b11df02d78c7: 31_efi_bootnext, grub2-common, equal
- d1b-microos-2ecfde8f1f5a331dbebc8607: profile, aaa_base, equal
- d1b-microos-e497e7c25f6e6792e8685786: zzz-glib2.csh, glib2-tools, equal
- d1b-microos-4d3f7b36794fbf3cb93fbf10: zzz-glib2.sh, glib2-tools, equal
- d1b-microos-c558f5f40c06faa4b4f934ee: ignition, ignition, equal

## Remaining rows: individual examination

Every referenced member TSV for these groups was read completely, retaining directories as members rather than treating their descendants as the listed objects. Membership-only comparisons are not content/integrity comparisons. Raw manifest samples supply directory modes but not a complete original directory state. Unknown original state and unknown creator are factual uncertainties, not a new classification rule. MIXED reasons enumerate all listed members; commas without spaces separate basenames.

- Sudo authorization: `raw/0042-sudo-root.out` proves the effective `(ALL : ALL) ALL` grant, but not the supplying rule or whether it is an installation default. UNKNOWN.
- `/etc`: the inline metadata identify a persistent directory, marked expanded; no member file or complete expansion is supplied for this atom. Neither snapshot labeling nor execute permission establishes package receipt or code. UNKNOWN.
- Snapshot audit (six members): audit-stop.rules and auditd.conf have equal package digests. audit.rules has unknown reference comparison; audit.rules.prev has no package reference or creator event; plugins.d and rules.d have directory membership only. MIXED.
- Snapshot audit/rules.d (one member): audit.rules has no usable original digest. Neither the source nor its creation event is established. UNKNOWN.
- Snapshot crypto-policies (five members): config lacks an original digest; four directories have membership only. Scriptlet source conditionally writes DEFAULT or FIPS, without proving its execution or subsequent modifications. UNKNOWN for each member.
- Snapshot grub.d: all seventeen members have equal supplying-package digests, including README and non-executable 25_bli. INSTALLED-PACKAGE for every member.
- Snapshot lvm: lvm.conf and lvmlocal.conf equal package digests; four directories have membership only. MIXED.
- Snapshot profile.d: all four gawk/GLib scripts equal their package digests. INSTALLED-PACKAGE.
- Snapshot selinux: fixfiles_exclude_dirs and semanage.conf equal package digests. config lacks usable original comparison; targeted has membership only; remaining markers/final lack original receipt or historical creator evidence. MIXED.
- Snapshot policy/policy.35: full bytes differ from the package. This is a kernel access-policy database, not executable machine code. A missing creation/selection history prevents choosing between a default, chosen setting or historical program record. UNKNOWN.
- Snapshot ssl: three OpenSSL files have equal package digests; two trust-store symlinks lack original receipt/origin; private has directory membership only. MIXED.
- Snapshot zypp: four files equal package digests; all nine listed directories have membership-only comparisons. MIXED.
- Snapshot Ignition module: all eighteen members equal the ignition package digest, including services, shell code and executable. INSTALLED-PACKAGE.
- /boot/grub2: five members are persistent. The saved source of grubenv contains only the environment-block header and padding, with no values. The four directory creators and original receipts are unrecorded; the environment-block format does not establish whether this particular block was generated or brought in. UNKNOWN for each member.

## Public documentation used to identify objects

[GNU GRUB environment block](https://www.gnu.org/software/grub/manual/grub/html_node/Environment-block.html): “The environment block is a preallocated 1024-byte file”. This identifies the blank saved block; no boot-choice value was inferred from the filename.

[SELinux binary policy](https://github.com/SELinuxProject/selinux-notebook/blob/main/src/types_of_policy.md): “This is also know as the kernel policy”. The documented policy location matches the stored policy. [Policy store files](https://github.com/SELinuxProject/selinux-notebook/blob/main/src/policy_store_config_files.md) describes building the binary policy and installing it at policy.<ver>. These descriptions establish format and function, not the history of this machine's modified policy.

No machine mutation, system experiment, or heavy computation was performed. Mechanical completeness verification is recorded by `part-microos.verify.py`; it does not constitute independent substantive acceptance.

After the table was completed and verified, only Section 2 of PROTOCOL.md was read. There are no GAP-NONE or GAP-TWO rows; meaning-microos.tsv therefore contains the required header alone. The classification table was not changed afterwards.
