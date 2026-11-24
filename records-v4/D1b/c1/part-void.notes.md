# Void classification notes

The input contains 1,143 rows. This classification did not participate in parts
1–3 of supplement step 4. No previous classification, rehearsal, other
classification, comparison, or adjudication was consulted. Inventory evidence
was read from `D1b/handoff/void/`, replacing the raw-copy location in the task.
Only the names in `S4/CLASSIFICATION-INPUTS.list` were read from S4; none of the
three listed documents was needed. Sections 8.1–8.3 and 8.5 of TEXT.md and
SENTENCES.md govern the decisions.

## Exact controlling sentences

- S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”
- S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”
- S8.2-8: “Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.”
- S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”
- S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”
- S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”
- S8.2-17: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”
- S8.2-23: “A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.”

## Complete member and fact handling

`classify-void.py` decodes every selected member specification, reads each named
member TSV completely, and asserts its count and completeness. Package metadata,
package-file comparisons, npm source and integrity tables, and old-package
reference comparisons are joined by exact path or unchanged raw ID. The npm
archives are read directly from their saved base64 evidence, in memory; no
archive is extracted or executable run. The scripts perform lightweight reads
of the delivered evidence only.

All selected npm and older-kernel members record persistent backing. These are
stored objects, not transient processes or mounts. The complete filesystem
scan is `raw/0004-filesystem.out`; the member tables preserve its observations.
The two rules below are the only bulk classification rules. All remaining
cases are explicit individual decisions, including six npm exceptions.

## Rule N: verified npm archive payload — 48 rows

Apply INSTALLED-PACKAGE if every member is a file with an equal full comparison
against the verified archive of its installed npm package, or a directory
containing that archive's payload (verified against the saved archive member
names). Exclude dependency-package roots and installer-created `node_modules`
containers. The installed package objects are in `objects.tsv`; source archives
and comparisons are in `npm-archive-sources.tsv` and
`npm-member-integrity.tsv`. Each archive has `verified-archive:lock-reference`.
Every regular selected file has `equal` and matching expected/actual hashes.
The script separately checks archive path prefixes for internal directories;
the bare comparison status `directory` is not treated as a byte comparison.

S8.2-6–8 decide before code, values, or records. S8.2-16 provides package-line
coverage. A dependency reason for the supplying package does not change a
payload file into a dependency package: the payload is covered by that
package's line; its package may itself be covered by a requesting package.

Ten rows checked by hand, with all their direct members inspected:

| ID | Member inspection |
|---|---|
| d1b-void-24a499239824205666b89950 | cowsay cli.js: one equal persistent file |
| d1b-void-73cc04ccce5732f0ebcc3c0f | wrap-ansi index.js: one equal persistent file |
| d1b-void-e3d7e7593a77dd0242dde8df | ansi-regex: four equal files |
| d1b-void-f704aef3611f060e64673ba6 | ansi-styles: five equal files, including TypeScript declarations |
| d1b-void-060a42ae4f6373f859fcdd9b | camelcase: five equal files |
| d1b-void-87f8a4777ec1b6b4ebd3987e | nested ansi-regex: five equal files, matching nested package root |
| d1b-void-07095d4690ec63e9f293a332 | color-convert: seven equal code, license, metadata and documentation files |
| d1b-void-f7eea8285ff10a4a9ee33add | color-name: four equal files |
| d1b-void-778e31483ba845148b4e8b5e | emoji-regex: six equal files and archive's es2015 directory |
| d1b-void-332df21266b8eebf271e9bdc | yargs/build: lib directory containing archive payload |

## Six npm rows decided individually

The [npm folder reference](https://docs.npmjs.com/cli/v11/configuring-npm/folders/)
says: “Packages are dropped into the `node_modules` folder under the `prefix`.”
The [lockfile reference](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/)
says: “It describes the exact tree that was generated”. These descriptions,
the saved lock (`raw/0005-metadata-read-0.out`), installed package objects and
verified archives establish the dependency-tree roles. This is not an inference
from an executable bit or from the inventory's class-like names.

- d1b-void-a74472d9bb92730824ba2b8e: cliui/node_modules has exactly four installed
  package roots: ansi-regex, is-fullwidth-code-point, string-width, strip-ansi.
  All four carry the recorded dependency reason. INSTALLED-DERIVED, S8.2-16.
- d1b-void-2671e0c8194a80cfbd661158: wrap-ansi/node_modules has the same four
  dependency package names at its own exact paths. INSTALLED-DERIVED.
- d1b-void-7d33ae31b2b79c994ad2c971: yargs/node_modules has those four dependency
  package names at its own exact paths. INSTALLED-DERIVED.
- d1b-void-1d3093e090ec37303afa298b: cliui's five regular members are unchanged
  payload, INSTALLED-PACKAGE. Its node_modules member is the generated package
  container, not a delivered archive payload or itself a package: RECORD under
  S8.2-15. MIXED.
- d1b-void-891ba9e7d2557d2187c34f3e: wrap-ansi's four regular members are unchanged
  payload, INSTALLED-PACKAGE; its node_modules container is RECORD. MIXED.
- d1b-void-a397c6c5091c03df1faba489: yargs's six regular files and build/locales
  archive directories are INSTALLED-PACKAGE; its node_modules container is
  RECORD. MIXED.

The three container-directory decisions refer to the directory itself; their
dependency packages receive the distinct installed decisions just listed.
This does not classify a package's contents as records merely because an
installer wrote them.

## Rule K: older kernel tree without original references — 1,068 rows

Apply UNKNOWN to the selected groups of persistent members at or under the
6.12.11_1 module tree, for which every member has `no-reference-found` in
`old-package-member-integrity.tsv`, and no exact-path package-file comparison.
The complete lists contain 5,450 regular files and 1,067 directory entries.
The later installed linux6.12 package is 6.12.118_1; linux6.18 is 6.18.64_1;
both have recorded dependency reasons. Their receipts and cached manifests
do not compare the older 6.12.11_1 members. The cache-manifest commands
`raw/0135-s4-old-kernel-cache-manifest.sh` through `raw/0143-s4-old-kernel-cache-manifest.sh`
name later kernel, kernel-base, and firmware archives, not the missing version.

The [kernel handbook](https://docs.voidlinux.org/config/kernel.html) says:
“When updating the kernel, old versions are left behind in case it is necessary to roll back to an older version.”
The [vkpurge manual](https://man.voidlinux.org/vkpurge.8) distinguishes versions
“not provided by any installed xbps package.” These explain why a current
package manifest cannot establish the provenance and unchanged state of every
older member. They do not supply the missing machine-specific comparison or
the original source line. A current digest or familiar suffix cannot fill it.

The missing provenance matters: unchanged members obtained with an installed
package satisfy question 1; independently changed or supplied code can instead
reach question 2 and require its own or a generating line; non-code directory
and list members additionally depend on their creator under question 4.
No complete resolved partition is established. UNKNOWN records missing facts,
not a conflict in the text, and does not assert homogeneous file contents.

Ten complete rows checked by hand against the exact-path reference results:

| ID | Complete member inspection |
|---|---|
| d1b-void-5933a7ab38ed2c6e261307b0 | one older-version directory |
| d1b-void-b4cd9e948b5e6364db664f8a | one x86 directory |
| d1b-void-24d9d6d7eb95d8bdab469dc7 | crypto, events, kernel and kvm directories |
| d1b-void-9513a6e235138055ff92a31c | thunderbolt_net.ko.zst |
| d1b-void-ac2fd621364bd38d737f88f6 | nvme host and target directories |
| d1b-void-3500e669d3d9734a41089a81 | all 31 lib entries: modules and subdirectories |
| d1b-void-f6121851bcb5d7c224130ead | hwpoison-inject.ko.zst |
| d1b-void-31518b199557513af1e374e0 | snd-usb-us122l.ko.zst and snd-usb-usx2y.ko.zst |
| d1b-void-f469b8cdfbc8bf1bb3060aa9 | virtio_snd.ko.zst |
| d1b-void-be5c7d915853b31e2828fef3 | snd-hdmi-lpe-audio.ko.zst |

All listed members are persistent and all exact reference statuses are
`no-reference-found`. No successful comparison was inferred from timestamps,
directory traversal, present-day digests, package names or a filename suffix.

## Boot group, individually

d1b-void-e2eaf799995627549514724b contains exactly config-6.12.11_1,
vmlinuz-6.12.11_1, the grub directory, and initramfs images for 6.12.11_1,
6.12.118_1 and 6.18.64_1. All six entries are persistent. Every exact member
has `no-reference-found`; no member has an exact package-file comparison.
The equal comparisons also indexed to this group for newer config/vmlinuz
files are not among its six members and are therefore not applied to this row.
The member list, scan, and opaque image metadata establish current files,
not their original content or the historical generating inputs. UNKNOWN:
the boot artifacts' original package comparison and generating source are
missing. Documentation of a normal initramfs generation mechanism would not
establish those facts for these particular images.

## Other individual rows

The 16 account, group, configuration and directory cases are documented in
`part-void.settings.notes.md`. The four store-related cases, including the
exact Flatpak package identities in the two MIXED results, are documented in
`part-void.stores.notes.md`. Both parts read the complete relevant member tables
and the delivered supporting facts. Their rows are merged by exact input ID;
the main table is the authoritative result. No gap weighting or meaning
judgment is used to change a classification.

## Completion verification

The final table contains 1,143 unique input IDs, with exact input/output set and
count equality. Every decision, sentence ID, field length and evidence path
passed verification. Saved scan observations agree with persistence and type
for all 7015 selected stored paths. Counts are in part-void.done; the table digest
is in part-void.verification.json. After this verification, only Section 2 of
PROTOCOL.md was read. There are no GAP-NONE or GAP-TWO rows, so meaning-void.tsv
contains its required header alone. The classification table was not changed
after completion verification.
