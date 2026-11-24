# Server classification c1

The following sections contain the rules, manual checks and evidence for all three disjoint parts. Structural validation checks exact input/output ID equality, counts, uniqueness, permitted decisions, sentence IDs, fields and word limits. No independent acceptance is claimed.


# Server classification: package and runtime subset

Only (not published: orchestration), TEXT.md, SENTENCES.md, A3/in/FACTS.md, the server input and server raw inventory were used. No other classification was consulted. These are classification decisions, not acceptance of a hypothesis or independent review.

## Interpretation and facts

The four questions are applied in order. S8.2-5 identifies runtime instances before a persistent object's four questions are needed. A running process is distinct from its stored executable; a kernel table is distinct from a saved firewall configuration. Installed-package coverage is asserted for a stored executable only when package-files.tsv reports unchanged. Package rows themselves are installed objects regardless of individual file integrity.

The runtime class is invariant when the creator's identity or own recording line is unknown. The task explicitly requires the invariant decision when every possible missing fact gives it. Therefore the process/socket remains RUNTIME, and its reason openly states that the creator or creator decision is UNKNOWN. Socket output contains no PID or executable ownership: standard port numbers cannot establish actual ownership. No undocumented name is supplied to fill that absence. Container process executable paths do not establish unchanged image contents.

Kernel-module names describe modules exposed by the running kernel, not new copies of their persistent files. All 41 names were matched to unique kernel package files and unchanged integrity. The runtime module instance follows that file's INSTALLED-PACKAGE decision. Both nft and nf_tables persistent binaries also have unchanged package integrity.

Firewall rows are kernel state reported by nft/iptables queries. KUBE/FLANNEL objects are attributed to the documented K3s networking controllers; Docker chains/interfaces to dockerd. Other base tables/chains belong to the nf_tables kernel subsystem. The cal_filter objects are loaded by nft. The dockerd executable has unknown integrity; this uncertainty is retained in its parent decision. A running extracted K3s executable is distinguished from its installation launcher. These attributions use recorded controller processes, concrete chain/interface identities, and documentation; they do not classify by inventory kind wording alone.

## Documentary support

- https://www.netfilter.org/projects/nftables/manpage.html: “rules in the Linux kernel, in the nftables framework.” This establishes that the query observes kernel firewall state.
- https://docs.docker.com/engine/network/firewall-iptables/: “Docker creates the following custom `iptables` chains in the `filter` table”. This supports the Docker chain attribution.
- https://docs.k3s.io/networking/networking-services: “K3s includes an embedded network policy controller.” This supports K3s network-policy attribution.
- https://docs.k3s.io/networking/basic-network-options: “The default backend for Flannel is `vxlan`.” The page describes Flannel as K3s network functionality.
- https://docs.k3s.io/blog/2025/03/25/K3s-initialization: “At this point, K3s will extract the binaries.” It documents the data directory containing extracted bundled executables.
- https://man7.org/linux/man-pages/man5/sysfs.5.html: “The sysfs filesystem is a pseudo-filesystem which provides an interface to kernel data structures.” This supports treating exposed module instances as runtime state.
- https://man7.org/linux/man-pages/man8/iptables-save.8.html: “iptables-save — dump iptables rules”. Generated comments and COMMIT separators are dump framing, not typed actions or independent firewall policies.

## Homogeneous rules

P — Installed dpkg package rows. Question one answers yes. Use the recorded explicit/dependency reason: explicit packages need their own line; dependencies are covered by their requesting package's line. Deciding sentences: S8.1-6, S8.2-6 through S8.2-8, S8.2-16. Integrity affects package members, not the fact that the package is installed.

X — Process instances. S8.2-5 gives RUNTIME. For the reason, independently join the executable path to package integrity, or use documented K3s extraction, or retain UNKNOWN for unestablished provenance. A separately supplied standalone executable has its own program line. Deciding sentences: S8.2-5, S8.2-7, S8.2-9, S8.2-10, S8.2-16.

M — Kernel module instances. S8.2-5 gives RUNTIME; each unique unchanged backing module is INSTALLED-PACKAGE under S8.2-7, S8.2-8, S8.2-16. The script asserts the unique unchanged join for every row.

L — Open sockets. S8.2-5 explicitly gives RUNTIME. All source rows omit socket ownership. Missing owner identity never changes this class; the reason states the unresolved creator decision.

F — Actual kernel firewall tables, chains and rules. S8.2-5 gives RUNTIME. Parent attribution is resolved separately as explained above. Dump framing is excluded before this rule. No assumption about persistent saved configuration is inferred from the live rules.

D — Generated dump comments and COMMIT framing. These are output recorded by the dump program; S8.2-15 gives RECORD after the earlier questions fail. COMMIT is not an action typed by a person and does not itself hold a firewall policy.

The following samples were displayed and checked manually against their full row metadata, resulting reason and relevant raw-file joins. Each list has ten IDs. P checks include explicit and dependency reasons; X includes unavailable executable identities; M checks module integrity; L checks TCP/UDP and missing ownership; F checks NFT/iptables objects and distinct parent branches; D checks both comments and terminators.

P: server-4830b005c5e95a80b9f05ea4, server-894f5d9c38cd1e3d38bd400a, server-7f79272f1d28c42f51277b05, server-e0a3fcedc0d8fc7f2c62819b, server-dd035f97841eb9c1044b6a0a, server-c5ad3ba1bcf58c05751986c3, server-a9a4344573c7ba68fe031a19, server-26b2cc84e0f18c65684980ac, server-ac29b0440441e8288cfb4d98, server-bb9e72f382f8bf301bbe6862.

X: server-cabd2fe206a1d620b3e41bad, server-eb5512b7d87a9d73d71980ba, server-4ee952c534b1127162151e32, server-6e2f004cb8fc03dbacfbb622, server-1421586b181f55637bdde0b8, server-5328ae6ea261addd2d5c2cb5, server-7fe924d095e53dae4a99f8e9, server-78e6bce75d501759ddc81955, server-82a020220e4fab69bebe0b17, server-bd383f6adda5449ee17f182b.

M: server-cafbb167cd3c3263e11c45af, server-72df891f8e9fbb3c82e182aa, server-ef17b770682f7c6d48df36ef, server-81c82a1e10a33a9ec991ba8d, server-7d5779b77057f6d8e522bbce, server-820b6ffacd170a3a74f3a610, server-eb412d6403b0bc1457e35413, server-443f97e416cabdd6b6d30460, server-ab26cfb98955a4597f6db852, server-9a13b95e77fca3a626a8d8ec.

L: server-2f5b482b083f366816d44e3f, server-c4d2aebc308b9235ab3cc3ea, server-9d7da68dc1067a79c753fb67, server-3cb5278e4dd09604d4b38f53, server-553a7bd762f9b89e286a67c4, server-256a6ae7114b5f2532bc9947, server-937210adca00b36db1edaad2, server-c9db236bc5e64bca80f177b6, server-0bda2359e78aad923356bfa7, server-9fd3e42a94561c2dbbfd8dba.

F: server-df39c40167f8ea0d545dc239, server-1be3fa2818d993c93cb99cfd, server-6f871340730b47a44335c957, server-5309ce530ffcc7acb81a8b50, server-4b83b7f6ba1008e10b9097d0, server-4e9b27c65dac31ea55eb5033, server-3ac8a7fed8fd8316ee5ec3cc, server-705809e00425cf00cf227a0d, server-c0780fcf72408c3372315333, server-b16b05c3819a49da8de0c367.

D: server-5502da6830c10a1165a74676, server-1ba2be3776f025f8783a28b1, server-e1388a90f4459e733417839b, server-8a3aeac968de2b8a45e679fe, server-9b75fa3ea1a9710aad2bf1e4, server-0c12b9253ef30ef4a3fde492, server-c810ba3b3d9d8b295861e0b0, server-6fb8e469e318c6fad6796d83, server-bb36907dcf8ea69d8b8eceba, server-ff146b3df6f16f6dfa28e559.

## Exact deciding sentences

- **S8.1-6** **Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.

- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?

- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.

- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.



# Classification c1: server code, service, and access subset

146 rows. Only the supplied text and input inventory and public documentation were consulted. Native install reasons, package-file integrity, configuration provenance and filesystem persistence were examined. Package-file absence is not proof that package metadata was never supplied by a package. No acceptance by an independent reviewer is claimed.

## Deciding text

- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?

- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.

- **S8.2-13** Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.

- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

## Rules applied by the script

The script appends each completed row and retains existing IDs. Each of the following rules had ten rows manually inspected; IDs and observations follow. All remaining cases were individually examined.

### Maintainer scripts

Persistent package metadata scripts are executable code, but question one must be resolved first. The digest inventory does not cover these paths, so unchanged supplied metadata versus modified code is UNKNOWN (S8.2-6,7,9,16). The collector's outside-packages label is not accepted as a classification. Primary documentation: https://www.debian.org/doc/debian-policy/ch-maintainerscripts — “Additionally, packages interacting with users using `debconf` in the `postinst` script should install a `config` script as a package metadata file.”

### Extracted executable helpers

Persistent executable helpers beneath the cluster binary extraction directory are PROGRAM-DERIVED (S8.2-9,10,16). These are runnable host programs extracted by the launcher, not guest-system code. Source: https://docs.k3s.io/blog/2025/03/25/K3s-initialization — “At this point, K3s will extract the binaries.” Documentation identifies the SHA directory as the bundled tarball's extraction location; inventory identifies the same layout and executable files. Native package membership is absent. Source-line coverage follows the extraction, rather than timestamps or executable permissions alone.

### Unchanged package unit files

A unit file with matching full package digest is INSTALLED-PACKAGE (S8.2-6,7,8,16). The row identifies the unit file; enablement columns do not turn that unchanged file into a separately supplied setting. All ten matched package-file entries were manually inspected. Source: https://www.freedesktop.org/software/systemd/man/261/systemctl.html — “List unit files installed on the system, in combination with their enablement state”.

### Service and timer selections with unresolved origin

Rows naming services or timers are treated as the named setting and its activation state (S8.1-11, S8.2-13,17), rather than as the underlying executable or unit file. UNKNOWN distinguishes a package installation default from a later choice, because state listings and provenance timestamps do not establish that history. Both running and inactive states are included. Custom nonpackage service definitions are individually SETTING-OWN instead.

## Manual rule checks


### maintainer

- server-864ed5793b9b589b11d1b404: bsd-mailx.postinst; persistent executable script; package metadata basename; no installation digest for this path.
- server-26a2a8d00197045af658b4e3: bsd-mailx.prerm; persistent executable script; package metadata basename; no installation digest for this path.
- server-dc58c0e0f50beba8677b5315: containerd.io.postinst; persistent executable script; package metadata basename; no installation digest for this path.
- server-0d2ef6588462d402a0dc0415: containerd.io.postrm; persistent executable script; package metadata basename; no installation digest for this path.
- server-3c36ff034958e52297c4e999: containerd.io.prerm; persistent executable script; package metadata basename; no installation digest for this path.
- server-aa083d0541e76f74f735461c: cron-daemon-common.postinst; persistent executable script; package metadata basename; no installation digest for this path.
- server-8c166c8dd28adef25146f86a: cron-daemon-common.postrm; persistent executable script; package metadata basename; no installation digest for this path.
- server-b8b99951078351799e6bcc7b: cron.postinst; persistent executable script; package metadata basename; no installation digest for this path.
- server-0fdcde3bd6b7f2667761d6bf: cron.postrm; persistent executable script; package metadata basename; no installation digest for this path.
- server-78e7ab054bbec1e3bc033c50: cron.preinst; persistent executable script; package metadata basename; no installation digest for this path.

### extracted

- server-eaad3ee4ff4e9178739e82ed: ebtables-legacy; persistent executable in documented extraction directory; native package manifest has no entry.
- server-d25d25bb8ac36aa7f8137d06: ebtablesd; persistent executable in documented extraction directory; native package manifest has no entry.
- server-88d932fa34b8f0dd4eeb99a1: ebtablesu; persistent executable in documented extraction directory; native package manifest has no entry.
- server-70a65dab23bf83724dd252c4: iptables-apply; persistent executable in documented extraction directory; native package manifest has no entry.
- server-0d0463028c57f32f625452e0: iptables-detect.sh; persistent executable in documented extraction directory; native package manifest has no entry.
- server-8fcd7930e6c7050a667f0741: nft; persistent executable in documented extraction directory; native package manifest has no entry.
- server-5f477ad712e3298f21687e18: xtables-legacy-multi; persistent executable in documented extraction directory; native package manifest has no entry.
- server-1e60decf067f7e8b2a7d6ffb: xtables-nft-multi; persistent executable in documented extraction directory; native package manifest has no entry.
- server-7a23f26b8bc530a3f46d4e68: xtables-set-mode.sh; persistent executable in documented extraction directory; native package manifest has no entry.
- server-cd543ab422e9487a66acbfc3: blkid; persistent executable in documented extraction directory; native package manifest has no entry.

### unit-package

- server-a1f7c71be11184927713be17: containerd.service; named unit file has unchanged full installation digest.
- server-895ebb80e4c6d53fc76f8546: cron.service; named unit file has unchanged full installation digest.
- server-2a38f4fc6a1c0fc3cb5ed7bd: docker.service; named unit file has unchanged full installation digest.
- server-cf76e42ff85f5f31d7c3d9a6: exim4-base.service; named unit file has unchanged full installation digest.
- server-fb24cbdfef0edc323abdd47d: exim4.service; named unit file has unchanged full installation digest.
- server-9977965a523746d36b0f65fb: logrotate.service; named unit file has unchanged full installation digest.
- server-599b027cac9be2a62bc07749: nftables.service; named unit file has unchanged full installation digest.
- server-127d4568edf3bdb1928d0987: exim4-base.timer; named unit file has unchanged full installation digest.
- server-b3e29e90ff81134b023d8b64: logrotate.timer; named unit file has unchanged full installation digest.
- server-62729f6011de36a57b75524d: user:dbus.service; named unit file has unchanged full installation digest.

### service-origin

- server-0147151515fd521ef169e058: containerd.service; service state present; listing does not record selection provenance.
- server-f13df310038bdd7c1cbca195: cron.service; service state present; listing does not record selection provenance.
- server-29d89b9e398461712a260865: docker.service; service state present; listing does not record selection provenance.
- server-5760aa675d991ee745f1fd3c: exim4-base.service; service state present; listing does not record selection provenance.
- server-2c3da97c87367b32a7436b5a: exim4.service; service state present; listing does not record selection provenance.
- server-088e995ac19c9091a8aa215f: k3s.service; service state present; listing does not record selection provenance.
- server-9547253ce828a65408ffeb16: ldconfig.service; service state present; listing does not record selection provenance.
- server-e61f0764e25caa250d108bbb: logrotate.service; service state present; listing does not record selection provenance.
- server-0bdb41a883a22103b825da88: systemd-journal-catalog-update.service; service state present; listing does not record selection provenance.
- server-5bd5a0ee786a0a8a05b79c97: systemd-machine-id-commit.service; service state present; listing does not record selection provenance.

## Individually resolved cases

- The network-allocation lock has zero bytes and is persistent: RECORD. A permission bit alone cannot supply executable code.
- Six shell startup/logout files have matching-sized familiar template content, but equality and dates cannot establish that the system copied them. Origin-dependent own versus derived program coverage remains UNKNOWN.
- The standalone metrics exporter runs as a host program and has no package owner or identified generator: PROGRAM-OWN.
- The standalone cluster launcher has documented manual and scripted installation paths; inventory does not settle original package receipt and unchanged condition: UNKNOWN.
- Generated cluster cleanup scripts are PROGRAM-DERIVED. https://docs.k3s.io/installation/uninstall states: “If you installed K3s using the installation script, a script to uninstall K3s was generated during installation.” For the killall companion, https://raw.githubusercontent.com/k3s-io/k3s/master/install.sh explicitly generates the KILLALL_K3S_SH file in create_killall.
- Four not-found service entries are references in memory, not existing services: RUNTIME, created by package-provided systemd (INSTALLED-PACKAGE). https://www.freedesktop.org/software/systemd/man/256/systemctl.html states: “List units that systemd currently has in memory.”
- Query headings in two privilege report rows are RECORD; the actual grant row is SETTING-OWN. The custom privilege files control access; the unchanged packaged PAM file is instead INSTALLED-PACKAGE because question one precedes question three.
- Account and group rows were separately examined: the local login identity and its membership are SETTING-OWN, while creation provenance for service identities is UNKNOWN. Package script references do not prove creation.
- Three container rows identify running host server programs instantiated from configuration and image, PROGRAM-DERIVED. Their composition source labels establish derivation. Containers retain stored state: they are not classified RUNTIME merely because currently running. https://docs.docker.com/engine/manage-resources/pruning states: “When you stop a container, it isn't automatically removed unless you started it with the `--rm` flag.”
- Three stored image rows are installer-managed application units; explicit acquisition versus derivation from the deployment source is not recorded, so UNKNOWN. Images are not treated as virtual-machine guests.

Section 8.5 leaves storage mechanisms and prevention mechanisms outside the definition; none was treated as a classification gap.


# Stored-object classification notes

This subset covers 366 stored groups and five unexpanded container-store objects. Every complete member table was read in full and its member count verified. Groups concern their immediate members; directory contents are not silently substituted for directory objects. The execute bit of a directory is search permission, not executable code. Persistent storage does not establish creation provenance.

Facts checked: (not published: direct evidence at least 2 MB), `raw/server/configuration-origin.tsv`, `raw/server/metadata.json`, the complete member tables, filesystem metadata, and selected metadata reads. No member path of these 366 groups matched a package-files path. This does not prove absence of package-derived control files: package metadata integrity is separately missing. Prefix signatures do not prove that a file remains as received. Configuration origin is explicitly unknown; names and modification dates are not substituted for creation facts. `raw/server/raw/0107-metadata-read-0.out` establishes privilege-rule contents but not installation causation.

All four questions remain ordered. UNKNOWN is used for missing facts, not for dissatisfaction with a definition. A generated non-executable cache is not installed merely because the coverage sentence mentions generated lists: the object must first satisfy one of the defining questions. No unavailable declaration or declaration implementation is presumed. Section 8.5 implementation choices are not treated as gaps.

## Exact deciding sentences

- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.
- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.
- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?
- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?
- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.
- **S8.2-11** Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?
- **S8.2-13** Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.
- **S8.2-14** A value obeyed only by a program that a person runs for himself or herself is a setting if it launches something or grants access; otherwise it is a record of that program.
- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.
- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.
- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.
- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

## Homogeneous rules and hand checks

R1 applies only to the fully read groups whose every immediate member has runtime persistence, with a program-created runtime role established by the member names, types and service inventory. S8.2-5 excludes these volatile objects before the four questions. The creator decision is separate: unknown integrity of a creator does not change the transient lifetime of its state. A namespace-handle group was decided separately, not through this rule. Persistent-filesystem socket pathnames are RECORD, distinct from the active socket endpoint. The runtime image-store directory was also separately inspected.
R2 applies only to the client discovery/HTTP cache groups. Complete membership consists of response JSON, response caches and their program-created storage directories. Under S8.2-6 and S8.2-15 these are RECORD; neither code nor selected host values occur. The rule does not apply to credential files.
R3 applies only to manual-page cache groups. Complete membership consists of cache markers, lookup databases and formatted-page cache directories. Under S8.2-6 and S8.2-15 these are RECORD. No package payload or executable cache occurs.
R4 applies only to the log-only groups under the log hierarchy, excluding the top-level group containing README. Members are logs, log symlinks and program-created log directories. Under S8.2-6 and S8.2-15 these are RECORD. Container paths do not turn log output into executable image contents.

### R1

Ten manually inspected rows:

- `server-1ac42e7d3357ddfcc6275ced`: 2 complete members; types 2 file; persistence 2 runtime. The actual member names and signatures were inspected; they fit R1.
- `server-4219ff0507e73311cf4cf6c4`: 16 complete members; types 11 file, 2 symlink, 3 directory; persistence 16 runtime. The actual member names and signatures were inspected; they fit R1.
- `server-32c093222cd0aac753e47b3d`: 8 complete members; types 7 socket, 1 fifo; persistence 8 runtime. The actual member names and signatures were inspected; they fit R1.
- `server-954c51802af12665b85654cb`: 11 complete members; types 7 file, 1 fifo, 1 directory, 2 symlink; persistence 11 runtime. The actual member names and signatures were inspected; they fit R1.
- `server-1ac44439b2ad881f9e0595ec`: 3 complete members; types 3 file; persistence 3 runtime. The actual member names and signatures were inspected; they fit R1.
- `server-81bb30798cd61ff94636f78b`: 8 complete members; types 4 socket, 3 file, 1 directory; persistence 8 runtime. The actual member names and signatures were inspected; they fit R1.
- `server-ac8ca9194225b7494eb37eaf`: 200 complete members; types 200 file; persistence 200 runtime. The actual member names and signatures were inspected; they fit R1.
- `server-60a5ccb43fec8147762b4cb8`: 1 complete members; types 1 symlink; persistence 1 runtime. The actual member names and signatures were inspected; they fit R1.
- `server-535315a281c49f50137acddf`: 3 complete members; types 2 socket, 1 directory; persistence 3 runtime. The actual member names and signatures were inspected; they fit R1.
- `server-17a17d5724ba447898c59485`: 6 complete members; types 6 directory; persistence 6 runtime. The actual member names and signatures were inspected; they fit R1.

### R2

Ten manually inspected rows:

- `server-74a3047db6a96a31b68defb0`: 1 complete members; types 1 directory; persistence 1 persistent. The actual member names and signatures were inspected; they fit R2.
- `server-1dd6b2b05508017fb65ca34b`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R2.
- `server-05f5c754211c0d1913f879a7`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R2.
- `server-739bc45d2e017f2f7c24571a`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R2.
- `server-0018c6f336f9e4cc01624826`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R2.
- `server-cd2ba6c2bdf8133829fa82fb`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R2.
- `server-14280d0d9e6acc59d31292dd`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R2.
- `server-ba07e0add77f3a972971264a`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R2.
- `server-bcbb2c5979ec15b9a481bf7f`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R2.
- `server-32da31e827953b7d4ece610c`: 6 complete members; types 1 directory, 5 file; persistence 6 persistent. The actual member names and signatures were inspected; they fit R2.

### R3

Ten manually inspected rows:

- `server-f80324ae58da1a55847e523f`: 35 complete members; types 2 file, 33 directory; persistence 35 persistent. The actual member names and signatures were inspected; they fit R3.
- `server-d3faa9ae4b23d4091bca6e23`: 5 complete members; types 2 file, 3 directory; persistence 5 persistent. The actual member names and signatures were inspected; they fit R3.
- `server-5a3589869555c7c51a04ceb4`: 6 complete members; types 2 file, 4 directory; persistence 6 persistent. The actual member names and signatures were inspected; they fit R3.
- `server-68a186e264bb445bfec5bbd9`: 6 complete members; types 2 file, 4 directory; persistence 6 persistent. The actual member names and signatures were inspected; they fit R3.
- `server-04aba3cb5241ddbfb4411c0d`: 5 complete members; types 2 file, 3 directory; persistence 5 persistent. The actual member names and signatures were inspected; they fit R3.
- `server-15f430ad206d451993aa0707`: 6 complete members; types 2 file, 4 directory; persistence 6 persistent. The actual member names and signatures were inspected; they fit R3.
- `server-4e01e9b2fd32e6f8ce51505c`: 5 complete members; types 2 file, 3 directory; persistence 5 persistent. The actual member names and signatures were inspected; they fit R3.
- `server-01fceeab2a5f47ddc974b58f`: 4 complete members; types 2 file, 2 directory; persistence 4 persistent. The actual member names and signatures were inspected; they fit R3.
- `server-5987e42184d62bb4eabad716`: 6 complete members; types 2 file, 4 directory; persistence 6 persistent. The actual member names and signatures were inspected; they fit R3.
- `server-e7517862a76e58a07660bd15`: 5 complete members; types 2 file, 3 directory; persistence 5 persistent. The actual member names and signatures were inspected; they fit R3.

### R4

Ten manually inspected rows:

- `server-6750aba5415c794389839b69`: 3 complete members; types 3 file; persistence 3 persistent. The actual member names and signatures were inspected; they fit R4.
- `server-ab7d25caac4d04fd823a5945`: 6 complete members; types 6 symlink; persistence 6 persistent. The actual member names and signatures were inspected; they fit R4.
- `server-b6a2eaa26b58d3673c0e4d74`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R4.
- `server-c8ca90c788b2a30e8d407ce0`: 1 complete members; types 1 directory; persistence 1 persistent. The actual member names and signatures were inspected; they fit R4.
- `server-45a6f6ecb2be81d0ed2fcfeb`: 2 complete members; types 2 file; persistence 2 persistent. The actual member names and signatures were inspected; they fit R4.
- `server-90155d6a4584b8fb3c9d10a3`: 5 complete members; types 5 directory; persistence 5 persistent. The actual member names and signatures were inspected; they fit R4.
- `server-47f2b013112b50287b5765d8`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R4.
- `server-f4cfb93fc7e2f31370202f6c`: 2 complete members; types 2 file; persistence 2 persistent. The actual member names and signatures were inspected; they fit R4.
- `server-7be6169d2db29b1aa147d385`: 1 complete members; types 1 file; persistence 1 persistent. The actual member names and signatures were inspected; they fit R4.
- `server-5cfa92553dc479eec41ffc6d`: 2 complete members; types 2 file; persistence 2 persistent. The actual member names and signatures were inspected; they fit R4.

## Documentation establishing object roles

- https://www.freedesktop.org/software/systemd/man/253/file-hierarchy.html — identifies `/run` as runtime storage and distinguishes persistent state/cache directories. Used with measured persistence, never as a replacement for it.
- https://kubernetes.io/docs/reference/kubectl/kubectl/ — `--cache-dir` identifies the client cache. The saved discovery JSON and HTTP response objects are this cache.
- https://www.freedesktop.org/software/systemd/man/251/file-hierarchy.html — “Persistent cache data of the package.” This concerns cache purpose, not installed-payload provenance.
- https://docs.python.org/3/tutorial/modules.html — “Python caches the compiled version of each module in the `__pycache__` directory”. The three bytecode groups satisfy question two and compiled-copy coverage. Their three immediate parent directory groups are RECORD.
- https://manpages.debian.org/testing/init-system-helpers/deb-systemd-helper.1p.en.html and https://sources.debian.org/src/init-system-helpers/1.69%2Bnmu3/script/deb-systemd-helper — distinguish remembered enabled-state bookkeeping from actual enablement. Applied to the four separately inspected helper groups.
- https://manpages.debian.org/bookworm/dpkg/update-alternatives.1.en.html — documents automatic and manual selection and separate executable/manual-page links. Actual targets and modes were not captured here, so these groups remain UNKNOWN.
- https://docs.docker.com/engine/daemon — identifies daemon storage as containing containers, images, volumes, service definitions and secrets; storage membership is not inferred when expansion is explicitly false.
- https://docs.k3s.io/blog/2025/03/25/K3s-initialization — “The embedded binaries are always deployed in the same directory”. The documented extraction establishes a possible derivation, but does not establish every stored member unchanged or every symlink target.
- https://docs.k3s.io/advanced — “K3s will generate a configuration file for containerd”. Generation does not itself prove whether the resulting values were human-chosen or installation defaults.
- https://docs.k3s.io/installation/packaged-components — describes deployed manifests and their replacement; actual received-state and selected/default provenance remain unavailable in this inventory.
- https://docs.cloud-init.io/en/latest/development/internal_files.html — “Cloud-init uses the filesystem to store its own internal state.” Input copies can still satisfy earlier questions; the mixed instance-data group is not uniformly labeled RECORD.
- https://github.com/canonical/cloud-init/blob/main/doc/var-lib-cloud.txt — identifies instance directories, execution semaphores, and scripts. Directories and markers were classified separately from absent script contents.
- https://www.debian.org/doc/manuals/debian-handbook/sect.package-meta-information.en.html — identifies installed control scripts in the package metadata directory. Their installation digests are unavailable; generated `.list` files are RECORD and other metadata members UNKNOWN.

## Runtime creators

Creator executables are checked against package-files.tsv: systemd, systemd-tmpfiles, cloud-init, mount, blkid, fsck, dbus-daemon, sshd, ssh-agent, exim4, uuidd, systemd-networkd and systemd-resolved have unchanged payload evidence, hence INSTALLED-PACKAGE. The netplan generate executable is `/usr/libexec/netplan/generate` (unchanged), distinguished from its generator symlink. systemd-udevd, dockerd and containerd have unknown installed-file integrity: their object decision is UNKNOWN. K3s launcher installation provenance remains UNKNOWN in this subset; the runtime classification is invariant under all its possible installed/program decisions.

For the mixed-creator root runtime group: blkid → blkid; cloud-init → cloud-init; containerd/nri → containerd; crond.pid/crond.reboot → cron; docker/docker.pid/docker.sock → dockerd; dbus → dbus-daemon; exim4 → exim4; fsck → fsck; ssh-unix-local/sshd/sshd.pid → sshd; uuidd → uuidd; udev → systemd-udevd; k3s → k3s; mount → mount; other bootstrap directories, links and service-manager runtime state → systemd/systemd-tmpfiles. cron also has unchanged installed-payload evidence. Some service-created directory attribution is indirect through service startup; it does not claim those directories contain package files.

## Exhaustive MIXED mappings

`part-server.stored.members.tsv` provides a decision for every member of every MIXED group. `member_index` is one-based in the exact complete inventory member table referenced by the input row. This avoids reproducing host-specific paths. Each compact reason gives the same mutually exclusive exhaustive mapping. UNKNOWN members retain the missing-fact explanation in the group reason.

- `server-deee96732af2d555a331d693`: RECORD=3, UNKNOWN=41. .pwd.lock, .updated, ld.so.cache: RECORD; all remaining members: UNKNOWN because contents, chosen values, execution, or creation provenance are insufficiently established.
- `server-d1f193302136c1c63cfef0a2`: RECORD=2, UNKNOWN=7. .sudo_as_admin_successful and actions-logs: RECORD; remaining members: UNKNOWN because script provenance, status producer, or directory creation is unestablished.
- `server-5776bb010310bc65df41dea4`: RECORD=5, UNKNOWN=9. boot-finished, datasource, handlers, scripts, sem: RECORD; remaining input/configuration copies and obj.pkl: UNKNOWN because contents and execution or selected-value roles are absent.
- `server-1b8a3f4dc2f72e04eb62b650`: RECORD=6, UNKNOWN=6. lock, lock-frontend, available, status, status-old, triggers: RECORD; remaining members: UNKNOWN because selected administrative policy versus generated state is not established.
- `server-4e5b11416af0e51f7dc1ad21`: RECORD=359, UNKNOWN=1267. *.list: RECORD; all remaining members: UNKNOWN because installed control-file integrity is unverified, affecting question one before code or record classification.
- `server-7acc0886d5e9730bfd7ef33a`: RECORD=1, UNKNOWN=1. berkeleydbvers.txt: RECORD; config.autogenerated: UNKNOWN because chosen values and installation-default provenance are not established by its generated filename.
- `server-f66f51027a0a4eabb8bb9536`: RECORD=3, UNKNOWN=1. .lock and the hash-named and cni directories: RECORD; current: UNKNOWN because its target and selection provenance were not collected.
- `server-a4edd37b5e963529a71018fc`: RECORD=7, UNKNOWN=3. kine.sock and cred, db, etc, manifests, static, tls: RECORD; agent-token, node-token, token: UNKNOWN because credential creation and selected-access provenance are missing.
- `server-9010e3402fd0dff2351ac71a`: RECORD=14, UNKNOWN=1. README: UNKNOWN because its link target and origin are absent; every other member: RECORD, storing logs or program-created log directories.

## Completion checks

371 unique subset ids were written, exactly matching the 366 stored-group and five store rows. All field lengths, sentence IDs, decision vocabulary and complete member counts were checked by script. The script is a structural verification, not independent acceptance. No independent acceptance is claimed. No previous classification was consulted.

## Socket pathnames and namespace handles

https://man7.org/linux/man-pages/man7/unix.7.html distinguishes a filesystem socket pathname from the live endpoint: the caller must delete the filesystem socket. The three persistent node-agent socket groups and the datastore socket member are therefore RECORD.

The namespace-handle group has filesystem magic `0x6e736673` in (not published: direct evidence at least 2 MB), despite the collector labeling it persistent. https://github.com/torvalds/linux/blob/master/include/uapi/linux/magic.h defines `NSFS_MAGIC` with that value; https://github.com/torvalds/linux/blob/master/fs/nsfs.c initializes it as a pseudo filesystem. These are namespace objects mounted beneath a volatile directory, not regular persisted file data, so S8.2-5 applies. No extra probe was needed.
