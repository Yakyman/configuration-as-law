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
