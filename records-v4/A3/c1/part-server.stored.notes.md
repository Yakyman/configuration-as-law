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
