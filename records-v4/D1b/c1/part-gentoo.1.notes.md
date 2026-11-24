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
