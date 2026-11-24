# Gentoo c1 classification notes

2026-11-23 UTC.

The work used (not published: orchestration), the fixed definition and numbered sentences, this part's input, FACTS.md and the Gentoo handoff. No other classification, rehearsal output, adjudication or earlier-night records were used. The current classification did not participate in supplement step 4 parts 1–3. Current parallel shards were combined only within c1.

The table contains direct member objects listed by each group, not an inferred recursive expansion. Every named member TSV was completely parsed and its row count checked against `members.count`; all were complete. A directory's search bit is not executable program code. Its separately inventoried contents do not substitute for the directory object. All package-file entries were read, as were package reasons, creation-origin facts, persistence and the raw filesystem scan. The full-digest table supplies observations, not an original reference or a historical creator. Missing factual predicates yield UNKNOWN, not a textual gap.

The two parallel parts are documented in `part-gentoo.1.notes.md` and `part-gentoo.2.notes.md`; their rules and hand checks are incorporated below. Group code is in `gentoo-groups.py` and `gentoo-groups-rest.py`. `gentoo-refine.py` records the pre-freeze clarification of direct directories and runtime parent names. All decisions were written incrementally; only these explanations and direct-directory interpretations were refined before the completed table was verified and frozen. There was no pre-existing output from an earlier attempt.

## Literal deciding text

- **S8.2-1** Everything that is installed and every setting must be recorded.

- **S8.2-2** The rest need not be recorded.

- **S8.2-3** The rule applies to objects that are on the computer.

- **S8.2-4** A command that a person typed himself or herself is that person’s action, not an object.

- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?

- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.

- **S8.2-11** Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?

- **S8.2-12** Then it is a **setting**, however it was entered and whatever file stores it.

- **S8.2-13** Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.

- **S8.2-14** A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.

- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.

- **S8.2-18** A line may take a list from outside the declaration, for example accounts from an organisation’s server; in that case, what counts as recorded is the source named in the line.

- **S8.2-19** What need not be recorded may also be recorded in the declaration.

- **S8.2-20** A file containing code that cannot be executed on this computer is not a program.

- **S8.2-21** Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.

- **S8.2-22** A program that runs as its own process on the computer, including in a container, is a program.

- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

## Evidence joins

`raw:D1b/handoff/gentoo/...` in the table is a handoff evidence path, not the forbidden inventory original. Groups cite their complete member tables. Package coverage is joined by exact path after resolving only five observed directory aliases from `raw/0004-filesystem.out`: `/bin` and `/sbin` to `/usr/bin`, `/lib` to `/usr/lib`, `/lib64` to `/usr/lib64`, and `/usr/sbin` to `/usr/bin`. The actual symlink targets are respectively `usr/bin`, `usr/bin`, `usr/lib`, `usr/lib64`, and `bin`. No basename or digest matching substitutes for provenance. For every INSTALLED-PACKAGE result, an unchanged package-files.tsv comparison is required. Unknown package installation reason does not invalidate coverage of a component by that package's line.

The supplied package-file comparison does not compare unlisted directory nodes with originally installed metadata. Such nodes remain UNKNOWN unless their documented role establishes program-created working state. A timestamp, location or prefix signature is not treated as a creation event. `configuration-origin.tsv` has unknown origins for the inspected settings; this prevents assuming a personal choice or an installation default.

`gentoo-member-decisions.tsv` gives exact member partitions for the 901 remaining groups, including every MIXED row with a long partition. The 125 homogeneous kernel MIXED groups have the simpler exhaustive partition stated directly in their reasons: all regular files are unchanged package members; every directory has unrecorded provenance. The 861 homogeneous file-only groups have all members unchanged. A group with only UNKNOWN members is UNKNOWN, not MIXED merely because the possible underlying classes differ.

## Public documentation and factual limits

- [Gentoo ebuild format](https://devmanual.gentoo.org/ebuild-writing/file-format/index.html): “An ebuild is a `bash` script which is executed within a special environment.” This establishes executable recipes, not their historical acquisition on this machine.
- [Gentoo repository layout](https://devmanual.gentoo.org/general-concepts/tree/index.html): identifies ebuilds, manifests, patches, metadata, profiles and directories. Repository data has no installation/reference comparison or acquisition history in this handoff. Code may require its own or a source line; noncode may be a program record or material. A repository name does not decide that missing fact.
- [Portage configuration reference](https://dev.gentoo.org/~zmedico/portage/doc/man/portage.5.html): `/var/db/pkg/` is a “database to track installed packages”; `/var/cache/edb/` contains “misc internal cache files”. VDB directories, local counters, installed CONTENTS and consolidated metadata are written bookkeeping. Other receipt fields can originate in binary-package metadata or local build output; neither original-copy comparisons nor a causal source-line record is supplied.
- [Portage database implementation](https://github.com/gentoo/portage/blob/master/lib/portage/dbapi/vartree.py): counter writing and database metadata handling establish local bookkeeping roles. This source's descriptions do not establish this machine's historical acquisition of every receipt.
- [Portage ebuild executor](https://github.com/gentoo/portage/blob/master/bin/ebuild.sh): it sources the saved environment. [Portage API](https://dev.gentoo.org/~zmedico/portage/doc/api/portage.package.ebuild.doebuild.html) describes extraction of `environment.bz2`. Consequently executable receipt content cannot simply be called a record by its database location.
- [pip caching](https://pip.pypa.io/en/stable/topics/caching/): “This cache functions like a web browser cache.” The documentation identifies HTTP response storage and locally built wheels. Metadata and cache directories are RECORD; opaque bodies/wheels lack the content needed to decide executable code. A wheel can contain importable code; a response body can instead be noncode data. The observed hash alone does not choose.
- [Python zipimport](https://docs.python.org/3/library/zipimport.html) documents imports from ZIP archives. [Python modules](https://docs.python.org/3/tutorial/modules.html#compiled-python-files) documents compiled-module caching. A `__pycache__` directory is bookkeeping, not the bytecode stored inside it.
- [Firefox HTTP cache](https://firefox-source-docs.mozilla.org/networking/cache2/doc.html): entry files store responses. [JavaScript startup bytecode cache](https://blog.mozilla.org/javascript/2017/12/12/javascript-startup-bytecode-cache/) establishes that a browser cache can contain code. Opaque payloads therefore cannot receive RECORD solely from their path. Browser profiles and telemetry bookkeeping are distinct from launch/access preferences and unread databases.
- [Firefox profiles](https://github.com/mozilla-firefox/firefox-dev/blob/main/toolkit/profile/docs/index.md) describes profile directory and selection bookkeeping. A stored directory itself is separated from its unread descendants.
- [Hardware database](https://www.freedesktop.org/software/systemd/man/262/hwdb.html) describes compilation into `hwdb.bin`; [iconvconfig](https://man7.org/linux/man-pages/man8/iconvconfig.8.html) describes the conversion-module configuration cache. These generated noncode lookup caches are records when no package comparison or chosen setting value is established by the inventory.
- [GNU Texinfo](https://www.gnu.org/s/texinfo/manual/texinfo/texinfo.pdf) describes install-info updating the top-level `dir` index. These are program-written lookup indexes.

Documentation establishes program behavior and object purpose, not an unrecorded historical event. It does not turn UNKNOWN into a gap. Section 8.5 mechanisms and declaration design are outside the classification.

## Homogeneous group rules and hand checks

Each rule applies only after member lists, persistence and package comparisons are inspected. The four questions remain in order. Below are the ten manually checked rows per rule; if a branch has fewer than ten applicable rows, all its applicable rows are checked. No additional test objects were introduced.

### unchanged-package-members

S8.2-6,S8.2-7,S8.2-8,S8.2-16. Every member has an unchanged package comparison after observed alias resolution. The first question decides INSTALLED-PACKAGE, even for executable modules.

- `d1b-gentoo-b1b155b9a227461f3d3c6d3b` — `/usr/lib/dhcpcd/dhcpcd-hooks`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-c818ff1f5fd3895fffd731a2` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/gpu/drm/scheduler/tests`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-8dab307284848bdd185fd73b` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/md/bcache`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-a7f37658a312ccee73abceb2` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/misc/sgi-gru`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-c16bf82bf0e42c5c3ebdcabe` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/net/ethernet/myricom/myri10ge`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-e18d1f0b9e35b4163fd94206` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/net/wireless/quantenna/qtnfmac`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-ff176ef59f57130a31848941` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/scsi/cxgbi/cxgb3i`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-79848f36cb84186ab584f460` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/fs/befs`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-289bfc2e938c9bb83e92a026` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/net/rds`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-81f09811183b9835caee5a05` — `/usr/lib64/tc`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.

### package-files-and-unverified-directories

S8.2-7,S8.2-8,S8.2-15,S8.2-16. Every regular file has an unchanged package comparison; directory nodes have no original metadata/creator record. MIXED partitions files as INSTALLED-PACKAGE and directories as UNKNOWN.

- `d1b-gentoo-a5c588c439947b545cb2ec4d` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/arch/x86/events`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-31fd29c5421404d7d68fe70b` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/fwctl`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-f7e156ec4d53e5e4872ceb83` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/mtd`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-7b86bfe1021a42c9c21bf726` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/net/ethernet/qlogic`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-34f84db2d16c6b4f19464f11` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/net/wwan`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-9911bd3272729ca1bb15bb4f` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/target/iscsi`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-0e16f6bee8e5715256a67b1d` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/vfio`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-78fa0b8027383a5699bf4962` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/lib/math`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-98f3b7f9de84e5c8c13e2798` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/net/nfc`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-2dfebfd687a901652b1f8948` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/sound/synth`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.

### unverified-module-directories

S8.2-7,S8.2-15. All direct members are persistent directory nodes without original directory metadata or creator history. UNKNOWN; no executable meaning is assigned to directory search permission.

- `d1b-gentoo-176a173739760ad0c80c4ede` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/arch`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-11ec65ca29fa791cfd3d10dd` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/bus/mhi`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-50941453bc010e792a98d815` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/hwtracing`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-2a3ba4c9c75728c68f43c988` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/media/mmc`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-b1b868c9feead997ff4b0048` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/net/ethernet/chelsio`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-be7e9836e8ac1581bacf6ed0` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/net/ethernet/myricom`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-f82dddadd83c73f9abd67f88` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/net/wireless/quantenna`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-75a9d4fa57b3da1a71f382c8` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/platform`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-0a9bf599789ccfa88e6d265e` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/drivers/ufs`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-8cad12c5a961bb8649121070` — `/usr/lib/modules/6.18.64-p1-gentoo-dist/kernel/virt`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.

### repository-provenance

S8.2-7,S8.2-9,S8.2-15,S8.2-16. Persistent repository entries have no package comparison or historical acquisition/source-line record. Record UNKNOWN; this is a factual distinction between system acquisition and personally supplied entries, for both code and noncode.

- `d1b-gentoo-40f9b81ab90846da84b77156` — `/var/db/repos`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-7eff7f76e5b25e7ff11f4adb` — `/var/db/repos/gentoo/app-emacs/semi/files`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-3767338a4cbb125a8fd1dbee` — `/var/db/repos/gentoo/dev-haskell/cryptohash-md5`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-d14313805c70cd624c4f7559` — `/var/db/repos/gentoo/dev-perl/Dist-Build-XS-PkgConfig`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-153e6e4f0e0ee8e0d1c8cfcf` — `/var/db/repos/gentoo/dev-python/recommonmark`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-5b2b83b0dc9f624a41f36825` — `/var/db/repos/gentoo/games-puzzle/xwelltris/files`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-ac791748c8086f20f08fa6c2` — `/var/db/repos/gentoo/media-sound/dir2ogg`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-a4f5dd3ecbdedc3830505d30` — `/var/db/repos/gentoo/profiles/arch/mips/mipsel/mips64el/n64`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-a746ec552b3db16ac5492245` — `/var/db/repos/gentoo/sys-apps/fwupd`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.
- `d1b-gentoo-b3b443eb8f3918a3c03d9ecc` — `/var/db/repos/gentoo/xfce-extra/xfdashboard`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.

### Member branch: directory-origin

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Directory creator and original package metadata are unrecorded; package-supplied, program-created and personal directories have different decisions. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-0d021149a1badb08ee1d1fba` — `/`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-77fceff412bc619c5e89ff1c` — `/home/user`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-6eb353353727c1b8472f7c9c` — `/home/user/.local/lib/cal-marionette`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-e655b275bb1c3ba66011a5ba` — `/home/user/.local/lib/cal-marionette/mozlog`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-15836158311a866b79688054` — `/opt`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-560e6ec57a1278d3c21ee2d7` — `/usr/lib`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-bfc5adf2ef28dcb06bff0cc3` — `/usr/lib64`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-2e3f9af917d55d8ae7e70f05` — `/usr/local`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-8cd9660a96a31f55f45b1b1e` — `/var/cache`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-e0d2220a268fc66500c0dd15` — `/var/tmp/portage`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: swap-storage

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Swap backing is persistent; creation/default provenance and active filesystem configuration are unrecorded. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-0d021149a1badb08ee1d1fba` — `/`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: boot-origin

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Boot-file installation or generation source and original-copy integrity are not recorded; package, derived program and noncode alternatives remain. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-eebdc98099b000ffb05933b4` — `/boot`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-bfe74bd831905308b43e4731` — `/boot/grub`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-636930d99fb5d13fad6ebe9a` — `/boot/grub/fonts`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-9ba8c0af6e44fb4f67e165e5` — `/boot/grub/i386-pc`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-5e397182571e2e3782940075` — `/boot/grub/locale`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-3a52136a3c5dcc1e3a267e0f` — `/boot/grub/themes/starfield`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: individual-overlap

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Archive contents and its generating inputs are unrecorded; package membership, executable members, and source-line coverage cannot be established. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-eebdc98099b000ffb05933b4` — `/boot`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-9ba8c0af6e44fb4f67e165e5` — `/boot/grub/i386-pc`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-f07c260d1b0895b757e38ea7` — `/etc`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-b1977cb4d26aaac4c0c6be22` — `/etc/sudoers.d`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-77fceff412bc619c5e89ff1c` — `/home/user`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-6adff8f5eb824996475259dc` — `/home/user/.local/bin`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-f98f27a408d4695398d34f1d` — `/home/user/.local/lib/cal-cowsay/bin`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-4d76889173ae42b094e77cc8` — `/home/user/.local/lib/cal-marionette/bin`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-8a8984fd4d5567200b2e0e8c` — `/home/user/.local/opt`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-ecb433fd6be457c0512aa933` — `/var/lib`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: generated-state

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Program-generated cache, log, working state or lock; not executable code or a chosen system value. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-f07c260d1b0895b757e38ea7` — `/etc`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-3d1f6dded5bf9cff4956a9b9` — `/etc/udev`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-7c806ad4af629fa888040e0e` — `/home/user/.mozilla/firefox/Crash Reports`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-9249e8e75f9a5367a26967ff` — `/home/user/.mozilla/firefox/cal-check/datareporting`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-47d25a5e4ddd0ef3ee2404dd` — `/home/user/.mozilla/firefox/cal-check/datareporting/archived/2026-11`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-6f78e43d66ee0236ce9fe51e` — `/home/user/.mozilla/firefox/cal-check/datareporting/glean/events`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-58a1ed794b793867792bfa46` — `/usr/lib64/gconv`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-086dbb5d5a436209fb559839` — `/var/cache/rc/console`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-fae6ac16930a97e8cc902a32` — `/var/lib/seedrng`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-b19324df4b33859c0df0b087` — `/var/log/portage/elog`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: configuration-origin

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Historical creation and original package comparison are missing; personally chosen settings, installation defaults or generated state require different decisions. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-f07c260d1b0895b757e38ea7` — `/etc`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-2db74e5e21a3dea95b3dbc22` — `/etc/env.d`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-88468a4b8b8fc750a63f1d8e` — `/etc/env.d/gcc`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-8fc218bc12a11b0e7a756b9c` — `/etc/portage`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-ed2a8894895ef7eb91e9dcbc` — `/etc/portage/profile`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-f1226970d0298119891dca07` — `/etc/runlevels/default`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-5f759d504585b4e5b0fb3118` — `/etc/xml`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-fd0ef9f78c2b6823ad4135fc` — `/home/user/.config/rc`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-e792254d9a6ca6d39cd60b5c` — `/home/user/.config/rc/runlevels/default`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-f4ab77d484e30e377ee57b2c` — `/var/lib/portage`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: account-backup

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Account tools retain previous database contents as backup working state. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-f07c260d1b0895b757e38ea7` — `/etc`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: user-object

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Stored user object contents and origin are missing; executable code, launch/access values and personal records require different decisions. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-77fceff412bc619c5e89ff1c` — `/home/user`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: cache-structure

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Browser or packaging tools create cache metadata and directory structure as working state. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-bd4bb63f492bfb9cdb9d9eeb` — `/home/user/.cache`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-99c51d3c42637e5c05c741e9` — `/home/user/.cache/AppImage-Cache`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-1e7cb088557da4ebd7d448e9` — `/home/user/.cache/AppImage-Cache/fontconfig`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-6d05cb3763c838d4155b306f` — `/home/user/.cache/AppImage-Cache/mozilla`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-cbd7470fe36b9321699af024` — `/home/user/.cache/AppImage-Cache/mozilla/firefox`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-192dd2c9b51c9d92e88dba3c` — `/home/user/.cache/AppImage-Cache/mozilla/firefox/cal-check`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-ccd534adfb86233d1a4db107` — `/home/user/.cache/AppImage-Cache/mozilla/firefox/cal-check/cache2`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: opaque-preferences

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Preference database contents are unavailable; launch/access values versus personal preferences are not established. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-2e3da7f2390387c24462605f` — `/home/user/.cache/AppImage-Cache/dconf`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: opaque-browser-cache

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Response bytes and capabilities are unrecorded; cannot establish whether cached code satisfies the limited-browser-code clarification. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-74cb2b959ad9f0180a56d987` — `/home/user/.cache/AppImage-Cache/mozilla/firefox/cal-check/cache2/entries`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: browser-script-cache

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Cached script or startup payload is opaque; originating executable code and its covering source line are unrecorded. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-7621a902823abbf69f872186` — `/home/user/.cache/AppImage-Cache/mozilla/firefox/cal-check/startupCache`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: browser-url-cache

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Browser records URL cache state. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-7621a902823abbf69f872186` — `/home/user/.cache/AppImage-Cache/mozilla/firefox/cal-check/startupCache`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: pip-bookkeeping

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Pip writes response metadata and cache directory structure while downloading. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-3c2512962c85121878181139` — `/home/user/.cache/pip`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-a51643b329e3ce022a60a235` — `/home/user/.cache/pip/http-v2/1/9/f/8/1`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-d97d4d26efa20786cc0394c1` — `/home/user/.cache/pip/http-v2/3/0`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-3c6c604953f19dd9e84d400b` — `/home/user/.cache/pip/http-v2/4/3/3/f`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-cf58b47b11085713f08aba97` — `/home/user/.cache/pip/http-v2/7`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-cc202aa713e48384198883e7` — `/home/user/.cache/pip/http-v2/9/8/f/8/d`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-f3e43ffce2148a875fb05cde` — `/home/user/.cache/pip/http-v2/a/e/d/a/c`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-0e4d08a44a34dc15309bdb4b` — `/home/user/.cache/pip/http-v2/b/b/7`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-17de89d85a3a585d56f80f58` — `/home/user/.cache/pip/http-v2/e/5/7`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-2546496f6d830f0509d2db6c` — `/home/user/.cache/pip/wheels/40/8f/0b/d808189c2e26aa4a5f606f2921820952459398a6f69f10925d`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: pip-payload

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Cached payload content is unavailable; executable archive versus noncode response determines whether a program line is required. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-9bd07964b6ec0095829c01df` — `/home/user/.cache/pip/http-v2/0/4/1/8/c`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-ed731cb35dde90d690d1a36d` — `/home/user/.cache/pip/http-v2/1/b/2/b/c`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-ad430b0e40c6598dfabc0c7a` — `/home/user/.cache/pip/http-v2/3/0/9/6/6`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-f744b1c71b9d72497d7e7efc` — `/home/user/.cache/pip/http-v2/4/e/5/9/c`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-25cf0074a49751e8977b5886` — `/home/user/.cache/pip/http-v2/7/4/b/d/f`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-cc202aa713e48384198883e7` — `/home/user/.cache/pip/http-v2/9/8/f/8/d`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-f3e43ffce2148a875fb05cde` — `/home/user/.cache/pip/http-v2/a/e/d/a/c`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-1e09f06d08dfcd14924d45df` — `/home/user/.cache/pip/http-v2/b/9/3/0/2`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-a48e92bcc6efad511068be0e` — `/home/user/.cache/pip/http-v2/e/3/4/7/2`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-2546496f6d830f0509d2db6c` — `/home/user/.cache/pip/wheels/40/8f/0b/d808189c2e26aa4a5f606f2921820952459398a6f69f10925d`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: python-cache-directory

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Python creates a directory for compiled-module cache working state; this member is the directory, not its bytecode. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-2b6d87c76766b4a465ff7cec` — `/home/user/.local/lib/cal-cowsay/cowsay`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-79e34d0d87ea04e1754ea2d8` — `/home/user/.local/lib/cal-marionette/blessed`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-dc0a580be6edee5e7da83799` — `/home/user/.local/lib/cal-marionette/jinxed/terminfo`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-d2b9219270052fcd0c146a4e` — `/home/user/.local/lib/cal-marionette/mozfile`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-6ef10bdb44b36c841dcfbf2e` — `/home/user/.local/lib/cal-marionette/mozlog/formatters`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-cb7dd3324bc009bc67411dfd` — `/home/user/.local/lib/cal-marionette/mozlog/pytest_mozlog`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-d3043faabdf1bfc5034edc38` — `/home/user/.local/lib/cal-marionette/mozprocess`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-136de33d21fb4c0abddfac02` — `/home/user/.local/lib/cal-marionette/mozrunner/base`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-78b7c2a6628fedad42d13c64` — `/home/user/.local/lib/cal-marionette/mozterm`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-6f45437aa7f11e6b172498ac` — `/home/user/.local/lib/cal-marionette/wcwidth/table_grapheme_overrides`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: browser-profile-record

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Firefox maintains profile bookkeeping, history, credentials or directory structure while running. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-e9a454eb0c9183b6415322b5` — `/home/user/.mozilla`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-f3ba3772cd19dfbfb39ccb96` — `/home/user/.mozilla/firefox`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-9ab6aa89c58514dc11461ff0` — `/home/user/.mozilla/firefox/cal-check`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: opaque-browser-preference

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Unrecorded stored values may grant access or launch code; content and scope are needed for the ordered questions. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-9ab6aa89c58514dc11461ff0` — `/home/user/.mozilla/firefox/cal-check`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-0c7e9143f402e9485a900bfb` — `/home/user/.mozilla/firefox/cal-check/security_state`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: opaque-browser-database

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Stored database payloads are unread; cannot distinguish ordinary application records from stored executable code or launch/access values. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-660f10f6c24835bad08201fc` — `/home/user/.mozilla/firefox/cal-check/extension-store`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-3d51966666ffe659e40f6349` — `/home/user/.mozilla/firefox/cal-check/storage`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-8693aef7fc881215527aba6f` — `/home/user/.mozilla/firefox/cal-check/storage/default`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-4940a554cdcc9b25a53b9718` — `/home/user/.mozilla/firefox/cal-check/storage/default/moz-extension+++<REDACTED>^userContextId=4294967295`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-90462069e8eb815902992f61` — `/home/user/.mozilla/firefox/cal-check/storage/default/moz-extension+++<REDACTED>^userContextId=4294967295/idb`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-b1ff6dde9f5d5b1671e1b52f` — `/home/user/.mozilla/firefox/cal-check/storage/permanent`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-e172f49901fc924831cdeaf0` — `/home/user/.mozilla/firefox/cal-check/storage/permanent/chrome`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-62101b845e1efb5765fa0e6e` — `/home/user/.mozilla/firefox/cal-check/storage/permanent/chrome/idb`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: extension-archive

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Extension installation reason and package provenance are not established for this stored archive. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-b982d72da69a54e22c24fd99` — `/home/user/.mozilla/firefox/cal-check/extensions`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: download

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Downloaded bytes and acquisition history are not established; archive execution and package installation cannot be determined from a filename. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-d366c590629c496123b00a73` — `/home/user/Downloads`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: runtime-members

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. agetty creates this transient member; parent decision INSTALLED-PACKAGE. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-ea1d6248e2d33b8c99785f09` — `/run`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-78839e64f21c567b36f2a936` — `/run/docker/extensions`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-71b9af17f90171513ecfb468` — `/run/openrc/daemons/docker`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-aed6219593c43c4dc43bf2c2` — `/run/openrc/options/docker`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-7581074b12b11755a7fec317` — `/run/udev/data`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-2c53f6716fe4b21d3b4b919c` — `/run/udev/links/disk\x2fby-partuuid\x2f3f049718-01`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-7bd6fe7ec0f6942a87187bd1` — `/run/udev/links/disk\x2fby-path\x2fpci-0000:00:05.0-part\x2fby-partnum\x2f2`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-cf7e9369452f6314d8e9f450` — `/run/udev/links/dri\x2fby-path\x2fpci-0000:00:02.0-card`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-b756eb86575cde6ae04aad88` — `/run/udev/tags/systemd`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-1b5ab43c43bb060471b5cbe0` — `/run/user/1000/openrc/started`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: link-origin

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Link provenance and original target comparison are missing; package membership, generated selection and personal link creation remain unresolved. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-3ad454af425e08be996b0aef` — `/tmp`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-c182f830d8ab49985277b6d4` — `/usr/bin`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-560e6ec57a1278d3c21ee2d7` — `/usr/lib`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-51ed596c1fee2b1ae52809a3` — `/usr/lib/rust`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-93b3f7863e81b11305fa8808` — `/usr/share/doc`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-6c488187ed00177ca3733789` — `/usr/share/man/man1`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-eda2b64ed4b94064053ded83` — `/usr/src`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-39c10a971c39215e02cde828` — `/usr/x86_64-pc-linux-gnu/bin`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-f717b46b4a5d2cf2b5063a50` — `/usr/x86_64-pc-linux-gnu/binutils-bin/lib/bfd-plugins`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-b342f94679ef80f2734d9307` — `/usr/x86_64-pc-linux-gnu/lib`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: temporary-origin

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. The file is persistent; contents and historical creator are unrecorded, so its name does not establish runtime or program-record status. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-3ad454af425e08be996b0aef` — `/tmp`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: package-member

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Unchanged package member after observed alias resolution. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-c182f830d8ab49985277b6d4` — `/usr/bin`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-560e6ec57a1278d3c21ee2d7` — `/usr/lib`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-054b57cfa0dd0fefb1b383dc` — `/usr/lib/dhcpcd`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-52af587a7c7e9c9c1b073e71` — `/usr/lib/gentoo`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-9edbda04a425ad7c62a9710c` — `/usr/lib/netifrc`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-bfc5adf2ef28dcb06bff0cc3` — `/usr/lib64`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-dae1ecaed281a2a55eabfe99` — `/usr/lib64/security`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: comparison-unknown

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Original package member comparison is unknown; original versus modified object changes the deciding question. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-c182f830d8ab49985277b6d4` — `/usr/bin`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-bfc5adf2ef28dcb06bff0cc3` — `/usr/lib64`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: system-file-origin

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. No original package-file comparison or generated-source record covers this member; package, program and noncode alternatives require those facts. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-78626a13cda1ec25be6c31be` — `/usr/libexec/rc/console`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: info-index

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. install-info maintains the generated Info document index. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-3ac196c1878a7f4e5e074f0f` — `/usr/share/binutils-data/x86_64-pc-linux-gnu/2.47/info`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-303940095bf51269babb3e81` — `/usr/share/gcc-data/x86_64-pc-linux-gnu/16/info`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-31fbedb8c8cb3c83d72b24d0` — `/usr/share/info`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: mirror-cache

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Portage records mirror lookup cache data. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-b92d06df7c2cb763db610d04` — `/var/cache/distfiles`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: source-archive

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Archive contents and executable formats are unrecorded; a filename and prefix digest do not decide executable code versus cached data. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-b92d06df7c2cb763db610d04` — `/var/cache/distfiles`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: portage-cache

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Portage writes counters, metadata-cache directories and processing state. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-54736aa7422c7d85245b2e27` — `/var/cache/edb`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-17ebb7fcdb739bc1d4839d6e` — `/var/cache/edb/dep`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-3b10dde9880511c22b0c2133` — `/var/cache/edb/dep/var`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-b0fa82698304e6290df59174` — `/var/cache/edb/dep/var/db`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-2d4df94025838a785b30593b` — `/var/cache/edb/dep/var/db/repos`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: opaque-pickle

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Pickle payload and deserialization behavior are not recorded; data-only cache versus executable reconstruction is unresolved. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-54736aa7422c7d85245b2e27` — `/var/cache/edb`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: vdb-generated

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Portage records installation inventory, counters and database structure. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-913b74c7aea623d095c40f55` — `/var/db/pkg`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-7f777eb29e316f577fb354f4` — `/var/db/pkg/app-alternatives/gzip-1`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-4469db3942ff326222f25bba` — `/var/db/pkg/app-portage/getuto-2.0`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-890490f579081b07dc1db695` — `/var/db/pkg/dev-libs/json-c-0.19-r3`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-b70363799ea10e497d776d57` — `/var/db/pkg/dev-perl/Pod-Parser-1.660.0`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-cb7cbe7afe7cd56427460915` — `/var/db/pkg/dev-python/poetry-core-2.5.0`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-423dad6c047f4b269de39691` — `/var/db/pkg/net-libs/libtirpc-1.3.7-r2`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-7b2d27169017ccd8a885ac9e` — `/var/db/pkg/sys-apps/util-linux-2.42.3`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-f8a60a291ac4b05938e8ecc0` — `/var/db/pkg/virtual/dev-manager-0-r2`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-773d90810859f441935860eb` — `/var/db/pkg/virtual/zlib-1.3.1-r1`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: vdb-receipts

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Binary-package versus locally generated receipt origin and original-copy comparison are missing; executable receipts additionally lack derivation evidence. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-c4c15b61714c76a8566a2e71` — `/var/db/pkg/acct-group/audio-0-r3`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-7f777eb29e316f577fb354f4` — `/var/db/pkg/app-alternatives/gzip-1`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-fae68adeb2466450f9327d78` — `/var/db/pkg/app-text/build-docbook-catalog-2.4`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-3a8b5e83b6466a9ae2be26e3` — `/var/db/pkg/dev-libs/libgpg-error-1.61`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-a2c62894a01ca1946ea8f94c` — `/var/db/pkg/dev-perl/Syntax-Keyword-Try-0.310.0`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-b4e82c745e5c38c618d6df7e` — `/var/db/pkg/dev-python/pluggy-1.7.0`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-45755ae721c99128b7dff5ce` — `/var/db/pkg/net-misc/curl-8.23.0-r1`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-8469dbdc2c59b5803765dcf4` — `/var/db/pkg/sys-auth/pambase-20251104-r1`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-907ad4c74095232815e779e9` — `/var/db/pkg/virtual/libelf-3-r1`. Member role, listed type, persistence and applicable evidence checked.
- `d1b-gentoo-773d90810859f441935860eb` — `/var/db/pkg/virtual/zlib-1.3.1-r1`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: dhcp-state

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Lease, identity or authentication contents and origin are unrecorded; person-chosen network values versus automatic working state are unresolved. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-8e0be6f89a81d9867acdad1a` — `/var/lib/dhcpcd`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: portage-state

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Portage records library preservation and configuration-file update bookkeeping. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-f4ab77d484e30e377ee57b2c` — `/var/lib/portage`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: mailbox

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. Mailbox payload and creator history are not read; received material versus program-written mailbox state remains unresolved. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-1a4f14e41972604eae913753` — `/var/spool/mail`. Member role, listed type, persistence and applicable evidence checked.

### Member branch: persistent-fifo

S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. FIFO persists on disk; installation/default provenance and its creation history are not recorded. The script predicate restricts this branch to the documented object role or the named missing fact.

- `d1b-gentoo-073207f082435ae243f8b99b` — `/var/spool/nullmailer`. Member role, listed type, persistence and applicable evidence checked.

## Individual groups and finalization

All remaining groups were inspected by their listed members. The per-member ledger records each member's concrete reason rather than substituting the inventory's class-like `kind` label. Boot files lack reference/source lineage; configuration values lack historical default provenance; persistent FIFOs and temporary files are not called runtime merely by name. Long groups in command/library directories are partitioned by actual package comparison, not by directory name.

Before freeze, eight direct-directory interpretations were clarified: the directory member `docker` in the parent library-state group was not recursively replaced by the separately classified store; browser storage directory entries were classified as working-state records rather than as their unread database descendants. Runtime explanations were expanded to identify parents and use INSTALLED-PACKAGE for executables with unchanged comparisons. Unknown boot/session creators are explicitly retained, because any possible parent leaves their runtime lifetime unchanged. These refinements precede the final full-table verification and meaning answers.

## Incorporated current shard notes: part-gentoo.1.notes.md

# Gentoo L1 classification notes

Scope: the 1210 L1 rows only. No previous decisions were consulted. No gap decisions were found. Output was appended incrementally; existing rows were retained.

Evidence: D1b/in/part-gentoo.tsv, the Gentoo handoff level-1 table, package-files.tsv, configuration-origin.tsv, metadata.json, coverage.tsv, and the exact saved queries named in rows. Package-file comparisons and stored-path persistence were used where relevant. No member-group row occurs in this shard.

All raw: references name the handoff copy, not the original collector directory. Uncertainty about history is UNKNOWN, not a gap in the text. Runtime child classification is invariant even when its parent covering-line decision is unknown.

## Documentation

- https://docs.kernel.org/filesystems/sysfs.html — “sysfs is a RAM-based filesystem initially based on ramfs.” Kernel objects are exported through its directories.
- https://github.com/OpenRC/openrc/blob/master/man/rc-update.8 — “Show all enabled services and the runlevels they belong to.”
- https://github.com/OpenRC/openrc/blob/master/man/rc-status.8 — service status and runlevel reporting.
- https://docs.docker.com/engine/network/firewall-iptables/ — describes Docker-created chains and bridge forwarding rules.
- https://docs.docker.com/reference/cli/docker/container/create/ — “creates a new container from the specified image, without starting it.”
- https://docs.docker.com/reference/cli/docker/image/pull/ — image download operation; local acquisition history remains unrecorded.

## Rules and manual checks

### identity-origin

Account and group records describe identities and rights. Their observed presence does not establish whether a person chose them or installation created a default. The exact /etc/passwd and /etc/group origin rows both report unknown; no historical creation is inferred from names or times.

Deciding sentences: S8.2-11,S8.2-13,S8.2-17.

Applied to 58 rows. Manually inspected 10 rows: d1b-gentoo-e272e21fd7b107c7d58b9c76, d1b-gentoo-fdc55a4d0313f6aaab480c5a, d1b-gentoo-b7cf591e3ab77265ce170990, d1b-gentoo-7d2a3f86f9b9f98285696b48, d1b-gentoo-e79203c58c5c36338fc46d97, d1b-gentoo-9f816d6aaf49d6723f5a74d1, d1b-gentoo-fe102a2958c1aae8f6e863d4, d1b-gentoo-04b148bd3b767bbe132b4d93, d1b-gentoo-1148fb2f6f0f3736676a9437, d1b-gentoo-58a607cc8e179df013d34712.

### unknown-package

An installed package whose recorded reason is unknown is an installed object, but the choice between its own line and a dependency source line is factual uncertainty. Native ownership of Python metadata alone does not demonstrate the original provenance and unchanged identity of every member of the whole Python distribution.

Deciding sentences: S8.2-7,S8.2-8,S8.2-16.

Applied to 428 rows. Manually inspected 10 rows: d1b-gentoo-4fdc4b1911980b52450bbf10, d1b-gentoo-d9983f17255eb43c36121149, d1b-gentoo-01ca783200f999e21857cbd3, d1b-gentoo-fd8079e26d2bed6e22aeeee9, d1b-gentoo-0b046ac2c03535e126e3f6ed, d1b-gentoo-a9fd0bf89b44f25efdafbf91, d1b-gentoo-50bb43ce22d5f3d3073da192, d1b-gentoo-2176025dbf0b8ef6188bfc27, d1b-gentoo-d29c4a206306e3868c96289f, d1b-gentoo-cad993822d5aa6ea8393a546.

### explicit-package

A package with the recorded installation reason explicit needs its own line. Both Portage selected records and Python REQUESTED markers establish explicit selection; a package need not contain executable code.

Deciding sentences: S8.1-6,S8.2-7,S8.2-8,S8.2-16.

Applied to 12 rows. Manually inspected 10 rows: d1b-gentoo-03ab718ffeb8bd7f475b9750, d1b-gentoo-22e6e62867c2fcb815e74dce, d1b-gentoo-3115c484fad41a4aae69007f, d1b-gentoo-a62af40e3db10b9417e7d8c7, d1b-gentoo-2e7f25f868158505ef5ffaa1, d1b-gentoo-52841bb58b7ce19e5e4a44cf, d1b-gentoo-7781b2b4e81b9c04c52a3031, d1b-gentoo-ac2fa413e9d9aad6ecd71faf, d1b-gentoo-604bd37308c9f06b26334e39, d1b-gentoo-d5bbcfc6e11fe7cd72e2f5a5.

### report-heading

Only literal report headings, firewall dump comment lines, table delimiters, and COMMIT markers qualify. These are generated report text, not separately selected objects or policy rules. Actual services, policies and grants are handled separately.

Deciding sentences: S8.2-15.

Applied to 34 rows. Manually inspected 10 rows: d1b-gentoo-e167549a8682797373a1a5c4, d1b-gentoo-8430e5795c0707e38860524b, d1b-gentoo-45ef9067dbdc3f4e451d311b, d1b-gentoo-5191c249cd9aab3c0edb442b, d1b-gentoo-1e1513f9393dda27ca436098, d1b-gentoo-ebd4818f3527c71b7ccaec8b, d1b-gentoo-ce0baa82db05edefc225bc92, d1b-gentoo-84799630cad19588e9b277c5, d1b-gentoo-de804971e1fc377a47515aac, d1b-gentoo-2f42e4f8fba9cf8b4589633d.

### service-origin

Actual OpenRC service rows describe system service state or runlevel membership, including empty membership. The queries establish present state but not whether installation supplied the service selection as a default. That missing history changes the covering line.

Deciding sentences: S8.1-11,S8.2-13,S8.2-17.

Applied to 99 rows. Manually inspected 10 rows: d1b-gentoo-1f7a8f22060477eb66e5abbc, d1b-gentoo-c069a0eb4a117250e85314d5, d1b-gentoo-df1b2772f764d4ec112e2e70, d1b-gentoo-5f90c8bae415389b1c88f4b4, d1b-gentoo-d055f3daf9bf9a343bfc281e, d1b-gentoo-a3af20876d0705bb02a0f118, d1b-gentoo-7f565521e2ea17c244217a23, d1b-gentoo-16b16f2aab269a0e088ab854, d1b-gentoo-67156eb50d06723a40b63b08, d1b-gentoo-d8da4222836a4e1aaf621088.

### port-runtime

All four sockets were examined separately. ss -H -lntu omits owning processes, so customary port numbers cannot identify their creators. All possible owners still produce RUNTIME; the unknown owning program and parent decision are explicit.

Deciding sentences: S8.2-5.

Applied to 4 rows. Manually inspected all rows: d1b-gentoo-c02e398bd5c8a0bae2860313, d1b-gentoo-ea1f82e39558b89b20a24828, d1b-gentoo-27672cb523b1883b9b525655, d1b-gentoo-34c624b77ec72f186fedaa31.

### firewall-policy-runtime

Live kernel chain policies with packet counters are runtime state. Their creating firewall configuration is not historically established; its covering-line decision remains UNKNOWN. This does not assign the same decision to a saved persistent firewall configuration.

Deciding sentences: S8.2-5,S8.2-13,S8.2-17.

Applied to 16 rows. Manually inspected 10 rows: d1b-gentoo-69af780b609e10ca5719fb38, d1b-gentoo-770aa1b77291bbf51814af09, d1b-gentoo-80b7e078b358e882dffcdddc, d1b-gentoo-1a4ed5f8610511e75ef1c3f5, d1b-gentoo-abc084c4e182152eb129d224, d1b-gentoo-a0409a32c13ca5f94008fe20, d1b-gentoo-c5127618ad9fffa99577dfac, d1b-gentoo-7986252740507091f9798ff2, d1b-gentoo-e9b4948f50421f398d2fbe9a, d1b-gentoo-ebd90ebf5be55cf8ff4a54d7.

### docker-firewall-runtime

The Docker-named bridge chains and Docker bridge forwarding/NAT rules are generated live network objects. Docker documentation describes their creator. The exact /usr/bin/dockerd comparison is unchanged, giving its INSTALLED-PACKAGE parent decision.

Deciding sentences: S8.2-5,S8.2-7,S8.2-16.

Applied to 33 rows. Manually inspected 10 rows: d1b-gentoo-9759df30fc573cc5b93730f8, d1b-gentoo-bfde43e8587f343a3204c9bf, d1b-gentoo-8e7ea69660e2a3d7fd3d98ab, d1b-gentoo-d8228f9ee29c01fdbe656c1a, d1b-gentoo-32088e1b7c56b2d209037199, d1b-gentoo-f68b30603f9b063676ae4505, d1b-gentoo-88541c1952d5d71015331d91, d1b-gentoo-c25aeb8733d5311b49e58649, d1b-gentoo-3f167da76b87fb52d02e5c99, d1b-gentoo-672d37e9a7d6628062b7dced.

### docker-container

Decided individually: the exited container has a specific BusyBox image and echo command, and may be restarted. Docker created the executable container from that image; its program is covered by the image line. This is the named container object, not a classification of an unexpanded directory of unrelated members.

Deciding sentences: S8.2-9,S8.2-10,S8.2-16,S8.2-22.

Applied to 1 rows. Manually inspected all rows: d1b-gentoo-009d18a3e62a822161837e0d.

### docker-image

Decided individually: the BusyBox image is stored and obtained/removed as a whole by Docker. The listing does not establish whether its acquisition was explicit or derived from another recorded source, leaving its covering line unknown.

Deciding sentences: S8.1-4,S8.1-6,S8.2-7,S8.2-16.

Applied to 1 rows. Manually inspected all rows: d1b-gentoo-f23478e06580c65ea0aab234.

### process-runtime

The /proc executable query identifies processes. They are runtime objects independently of executable identity. Exact unchanged package-file matches supply INSTALLED-PACKAGE parent decisions. The saved filesystem scan proves /bin and /sbin point to usr/bin and /usr/sbin to bin; these aliases are used. Unresolved executable lookups retain UNKNOWN parent identity and provenance; the collector probe also lacks a covering-line provenance record.

Deciding sentences: S8.2-5,S8.2-7,S8.2-16.

Applied to 159 rows. Manually inspected 10 rows: d1b-gentoo-60b3154fd682601fdb7eacb0, d1b-gentoo-5bceda139eb3f7ad85389754, d1b-gentoo-1f3139e1dc920af69a8dfdbf, d1b-gentoo-078fd0180ad6fe04fc6eb4fc, d1b-gentoo-eac129292a84ac1087181af8, d1b-gentoo-c8e85b34f3e05ede056ed810, d1b-gentoo-5334045df96a06e76d09c59a, d1b-gentoo-eac85e57277cfb810ada3353, d1b-gentoo-39a75bb127ad944cf4f8159b, d1b-gentoo-d10368a6d343d30596dc5876.

### sysfs-runtime

The commands enumerate live sysfs registrations, not the stored module binaries. The kernel produces these RAM-only objects. The running kernel has not been causally matched to a stored image by these queries; its covering-line decision remains UNKNOWN. Every possible parent gives the same RUNTIME child decision.

Deciding sentences: S8.2-5.

Applied to 330 rows. Manually inspected 10 rows: d1b-gentoo-7f655affe70e9a7d4012ef8c, d1b-gentoo-ab7b8509deea3333dbe05c10, d1b-gentoo-038650d716463104da7f678b, d1b-gentoo-b04706e4a1e56d8f5a162c41, d1b-gentoo-30db09f1a731981d35eea3b1, d1b-gentoo-0241adadff0eb0a20d756ce1, d1b-gentoo-0183467663e46873c357fcf0, d1b-gentoo-09cef42fcfb6c1e57f384fe2, d1b-gentoo-943a6f3459b47c547e024fba, d1b-gentoo-a17b3e09aac58e0b38da7b20.

### sudo-value-origin

Each effective sudo value was examined. The full sudoers file changed, but this does not show which individual values changed. Effective defaults and grants thus have unknown default-versus-chosen history. The extra privilege fragment likewise has unknown creation history.

Deciding sentences: S8.2-11,S8.2-13,S8.2-17.

Applied to 7 rows. Manually inspected all rows: d1b-gentoo-6f51347974368c552609ddb2, d1b-gentoo-b992048addde720093ff1d8a, d1b-gentoo-c8c38db0bc1241adc8f3df1a, d1b-gentoo-5e7b09c16cfc6ffc6d65fb79, d1b-gentoo-3723b9c8dba35b1e42923cdf, d1b-gentoo-ffdde1d593e1c69a5f8ff67f, d1b-gentoo-fbff0f882b48563672b5e31d.

### changed-sudoers

Decided individually: /etc/sudoers differs from the package reference. Its policy is read as values, not executed as code. Its modified access policy needs its own setting line.

Deciding sentences: S8.2-11,S8.2-13,S8.2-17,S8.2-23.

Applied to 1 rows. Manually inspected all rows: d1b-gentoo-a92864cc3f7c848973b61c3f.

### unchanged-access

An exact package-file comparison of unchanged makes the authentication/authorization file an installed object under the first question. This precedes interpreting its contents as settings. Its supplying package covers it.

Deciding sentences: S8.2-6,S8.2-7,S8.2-8,S8.2-16.

Applied to 26 rows. Manually inspected 10 rows: d1b-gentoo-5a9707475341ed2f91485f93, d1b-gentoo-1743f4a807887c456ba5856f, d1b-gentoo-00dd24dbeafa018c0de496a6, d1b-gentoo-3215c6576e30311f1f9b2f79, d1b-gentoo-d0216e5ede1ae840324f9252, d1b-gentoo-7ab58862a2edf8a302a12d5c, d1b-gentoo-d3fc34717aecb5e29b0cfacc, d1b-gentoo-ac4c8886e07b449b56168bb4, d1b-gentoo-98a170756f4ea41345af3722, d1b-gentoo-65bb99c997263e34b8ca30f8.

### unowned-access

Decided individually: the additional passwordless privilege policy has no matching package file and an unknown historical origin. Whether installation created this default remains unknown, determining its own versus package-default line.

Deciding sentences: S8.2-11,S8.2-13,S8.2-17.

Applied to 1 rows. Manually inspected all rows: d1b-gentoo-7e370ee14c2dfa91d3c5c5e9.

## Literal deciding sentences

- **S8.1-4** **Installer**—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.
- **S8.1-6** **Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.
- **S8.1-11** A service is in force if it is enabled; an account, if it exists.
- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.
- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.
- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?
- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.
- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?
- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.
- **S8.2-11** Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?
- **S8.2-13** Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.
- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.
- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.
- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.
- **S8.2-22** A program that runs as its own process on the computer, including in a container, is a program.
- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

## Incorporated current shard notes: part-gentoo.2.notes.md

# c1 code and image shard

No participation in preceding preparation or rehearsal tasks. Only the authorized text, sentence list, facts description, this input part, and this machine's handoff were used. No classification from another task was read.

## Rule A: unchanged supplied files

S8.2-6 gives the first question priority; S8.2-7 and S8.2-8 classify unchanged supplied objects, and S8.2-16 covers them by their supplying package. Exact package-files comparisons are unchanged for 251 rows. Package installation reason was consulted in objects.tsv: whether that supplying package is explicit or a dependency does not change the member's package coverage.

The complete filesystem scan records actual symlinks /bin and /sbin to usr/bin, /lib to usr/lib, /lib64 to usr/lib64, and /usr/sbin to bin. These resolve the otherwise apparently missing exact package paths. No equality of hashes alone was used to infer provenance. All these input objects have persistent backing. The eight direct GRUB image members and 243 alias members obey this rule.

Manually inspected IDs, comparing persistent metadata, exact alias and unchanged package record:

- d1b-gentoo-8f6945623c206e0ded79c948: agetty, /sbin manifest alias.
- d1b-gentoo-120b2a9358fefbd2c3cd47a9: dhcpcd, /sbin alias.
- d1b-gentoo-e5f6b730cbc2fe00acc04acf: genl, /sbin alias.
- d1b-gentoo-266b0fb4c5eeab755b2eee56: killall5, /sbin alias.
- d1b-gentoo-fba66f0d14b29bd79288a1c0: nft, /sbin alias.
- d1b-gentoo-2dd528d744754e75ffec3b13: rtmon, /sbin alias.
- d1b-gentoo-a607e502c298e194d7978dfc: vdpa, /sbin alias.
- d1b-gentoo-9e3ea9ac9b5fdfc7281c6e94: librt, /lib alias.
- d1b-gentoo-f771ad1a15de095e38253431: libpthread, /lib64 alias.
- d1b-gentoo-35bceff2764ca2688e5f4987: pam_localuser, /lib64 alias.

Evidence: (not published: over 20 MB); objects.tsv; raw/0004-filesystem.out. Each package-files row retains its original manifest and digest evidence.

## Rule B: repository script provenance unresolved

1358 persistent repository files carry shebang markers. They are not assumed material just because they occur in a source repository. S8.2-9 precedes the fourth question. No exact or alias package comparison exists. The full-digests table establishes current bytes, not historical acquisition. Neither an interpreter marker nor a repository directory establishes whether a person supplied the file independently or the system obtained it from a source line. S8.2-16 permits materially different recording lines for these factual possibilities. UNKNOWN records that missing fact; it is not a textual gap. No assumption that all code has an own line was made merely from missing ownership.

Ten manually inspected persistent shebang rows, with absent exact/alias package comparisons:

- d1b-gentoo-d1a1869b5087cbcc4f6df688: brltty startup script.
- d1b-gentoo-23bbb40d652f108ca13fd6c3: xendomains startup script.
- d1b-gentoo-3e2e302d1ec4f9c631549bbe: mysql log-s6 script.
- d1b-gentoo-0ae660cc0e13306f1496504f: minecraft-server startup script.
- d1b-gentoo-042cbc03a8da5fa4d141ce5d: srs init script.
- d1b-gentoo-9e103ab513022fb651570e90: shorewall startup script.
- d1b-gentoo-997cc2b89a096a2103cb06c4: icingadb startup script.
- d1b-gentoo-1d78bcd5b5ce8439ea750064: havp startup script.
- d1b-gentoo-c4180608424019fe720438c0: man-db cron script.
- d1b-gentoo-c62f739e6cbc0cbddec9ccb7: rpc.rquotad startup script.

Evidence: input metadata, raw/0004-filesystem.out, package-files.tsv, object-fact-index.tsv and full-digests.tsv. The index supplies only full-digest references for these objects. Public documentation cannot establish their historical acquisition.

## Individual cases

The remaining 24 rows were considered individually. The boot directory images lack package references and recorded generating input lists. The GRUB manual identifies first-stage boot code and core-image generation, but does not establish this machine's generating inputs: https://www.gnu.org/software/grub/manual/grub/grub.html . Relevant exact passage: “It is built dynamically from the kernel image and an arbitrary list of modules”.

The initramfs archive has no expansion, so executable membership and generation inputs remain unknown. Shell startup files, local service scripts, command wrappers, Python command entry scripts and the AppImage each have no recorded comparison or historical producing line. Python package presence alone does not prove entry-script integrity. configuration-origin.tsv explicitly records unknown creation for profile.env and the local command script. Prefix signatures and timestamps do not close these missing facts.

The Firefox times.json row is not code simply because a collector marked it as startup-related. Mozilla documents a profile timestamp written during creation: https://docs.telemetry.mozilla.org/concepts/profile/profile_creation . Exact passage: “a `times.json` containing a timestamp of the current time is stored inside that profile directory”. This is program state under S8.2-15.

Both complete store-member tables were consumed: 493 containerd entries and 37 Docker entries, all persistent; traversal_complete is 1 for both in store-coverage.tsv. Each member was checked for type, persistence and role. The containerd keep file has an unchanged package comparison. Metadata databases and UUID are program records; snapshot payloads and content blobs lack recorded image-member comparisons and source lineage. Docker logs, caches and engine identifiers are program records; saved host and container configuration controls launch parameters; remaining database or special members lack sufficient contents or originating-value facts. These heterogeneous stores therefore receive MIXED, with unresolved subsets explicitly identified, rather than inventing homogeneous image coverage.

## Completion

The append script is classify-gentoo-2.py. It verified exactly 1633 distinct input IDs, exactly the same output ID set and count, allowed decisions, and field word limits. Counts: INSTALLED-PACKAGE 251; RECORD 1; UNKNOWN 1379; MIXED 2. The classification table is frozen. PROTOCOL.md Section 2 was then read; there are no GAP-NONE or GAP-TWO rows, so the meaning table contains only its required header.


## Final verification and meaning answers

2026-11-23 UTC. The final table has 32,775 rows, exactly the input ID multiset, each once. All decisions, field bounds and sentence IDs pass `verify-gentoo.py`. The separate validation is recorded in `part-gentoo.validation.md`. `part-gentoo.done` gives all fifteen decision counts, including zeros. No GAP-NONE or GAP-TWO rows occur. After reading only Section 2 of PROTOCOL.md, `meaning-gentoo.tsv` therefore contains its required header alone. No classification-table changes were made after final verification.

Final table SHA256: `b21ea06965daf9875ea2afc9bc92073e328d58cbb9b19dcc24a8fae98a59c7fb`.
