# Stored-object classification notes

Scope: all 3,174 `L2:stored-outside-packages` input rows. Only the permitted task text and this system's raw inventory were consulted. Each exact member TSV was read in full, its count checked against the source JSON, and its completeness flag checked. Filesystem persistence came from the member TSV and the exact per-path filesystem record. Package-file integrity was joined by exact path; raw RPM manifest paths were also inspected for the residual groups. No snapshot-prefix stripping was used to transfer installation integrity. A prefix hash, read-only status, executable permission, and a suggestive inventory label are not installation-integrity evidence.

`part-microos.stored.py` preserves existing output rows and flushes every appended row. Its manually enumerated residual groups are individual decisions, not inferred matches from a generic name classifier.

In every MIXED reason, **member N means data row N of the exact member TSV named in that row's basis**, counting from one and excluding its header. Ranges include both endpoints. Each MIXED reason partitions the complete member list. UNKNOWN members share the stated missing fact; UNKNOWN does not claim two already-established member classes.

## Deciding text

- S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”
- S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”
- S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”
- S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”
- S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”
- S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”
- S8.2-17: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”
- S8.2-23: “A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.”

## Rule S: snapshot-member provenance uncertainty

Applies to 2,964 groups rooted at the retained snapshot tree. Every member is persistent, and none has an exact-path package-file integrity entry. These are homogeneous in the decisive missing provenance/integrity fact, not homogeneous in file format. A current-root manifest does not establish that a differently stored snapshot member was obtained with an installed package and remains as received. If that fact is true, question one precedes code, settings, and records; if false, those later questions and source-line provenance matter. Public snapshot documentation cannot establish the missing historical facts of these particular copies. Therefore UNKNOWN, not a text gap, and not a blanket exemption for snapshots. Section 8.5's exclusion of rollback mechanism design does not exempt executable snapshot members from question two.

Primary documentation: https://susedoc.github.io/doc-sle/main/html/opensuse-reference/cha-snapper.html — “Snapshots taken from the root file system (defined by Snapper's root configuration), can be used to do a system rollback.”

Ten hand checks (complete lists inspected):

- microos-e8d4e9636694c6a9239e60d8: one font; persistent; prefix hash only, no snapshot installation record.
- microos-6f2ef8904d971d8fd45b6017: 37 translation files; same missing snapshot provenance despite descriptive suffixes.
- microos-6f297717869bcff1f5915701: two audit plugin configuration files; package defaults versus later copies not established.
- microos-968f58408e01fc92ebbbcbd1: one audit rules file; chosen/default/history origin absent.
- microos-8394dfb686660b222beb8a3c: one policy module directory; directory execute permission does not prove code.
- microos-b1b47346e524f424ba948e3b: three policy compilation files; prefix signatures do not prove package reception.
- microos-86e5186fbb5ecac0fe6e4396: three other policy compilation files; same missing provenance.
- microos-b2124efe0ac2ac768edc2061: three policy compilation files; no exact snapshot manifest coverage.
- microos-3dd84eae292aa0d8e3b96fa4: one compressed kernel module; code character does not bypass unknown question one.
- microos-537cfac91331a77bceee0878: six executable shared libraries; execute permission does not establish own versus package/derived coverage.

## Rule R: verified volatile working objects

Applies only when every member's persistence is `runtime`. These members exist in volatile runtime storage; S8.2-5 supplies RUNTIME before the four-object questions. Each reason names its creating service program and that program's decision. The package-file table establishes unchanged executable files for systemd, systemd-udevd, NetworkManager, chronyd, dbus-broker, fsck, blkid, LVM, mount, polkitd, rebootmgrd, sysextmgrd, wtmpdbd, agetty, auditd, dmeventd, dracut, and systemd-tmpfiles. They are INSTALLED-PACKAGE by S8.2-7 and S8.2-16. The grouped runtime root lists the multiple service creators. Persistent service-private storage was excluded from this rule.

Primary documentation: https://www.freedesktop.org/software/systemd/man/latest/udev.html — “The udev daemon, systemd-udevd.service(8), receives device uevents directly from the kernel”. This identifies the device-state producer; the raw persistence facts establish volatility.

Ten hand checks:

- microos-7b376f05940c758d2a37f25a: NetworkManager temporary configuration; one runtime member.
- microos-d56837a491224b6057bb1911: three runtime NetworkManager device records.
- microos-b9d5df898e3b476d5283db7d: three runtime NetworkManager connection files.
- microos-7ea3796712ff653f4dd19185: two blkid runtime cache files.
- microos-5d2c58c61ea05295e1882e18: chronyd PID and socket; both runtime.
- microos-d77c5bfcfd114e48a21363af: D-Bus container directory and bus socket; both runtime.
- microos-b664fb9fdbf168a622097c76: filesystem-check runtime lock.
- microos-811fd00b5fe4dbf0eae1b7ca: runtime LVM lock directory.
- microos-c3cebce608b5dd1fdb376dd0: three mount runtime bookkeeping files.
- microos-093d7f542f7d7820ae05b230: one udev runtime device-link record.

## Rule C: repository metadata cache

The 19 ZYpp cache groups contain repository metadata, signatures, solver indexes/cookies, and their storage directories. No installed RPM package archive or executable program appears in these lists. S8.2-15 expressly includes caches and working state. The fact that metadata can influence an installer does not make it code or a person's chosen system value. Accordingly RECORD.

Primary documentation: https://manpages.opensuse.org/Tumbleweed/zypper/zypper.8.en.html — “storing it in local cache (typically under /var/cache/zypp/raw/alias directory)”. The documented refresh operation also builds the solver cache.

Ten hand checks:

- microos-0a99fc43b8282959128ea705: one geographic mirror cache entry.
- microos-973779de3806881d2bacaf6b: one repository medium metadata file.
- microos-044b73e102c0cdee25dc3c66: one other repository medium metadata file.
- microos-e2e22c31f0b2d7ea6b4f5823: repository check marker and metadata directories.
- microos-aa22e2a773f9357d2fbbc775: repository check marker and metadata directory.
- microos-7cc2a7c5eef50507eed81020: cookie, solver data, and index.
- microos-117734517486366eda298f3b: cookie, solver data, and index.
- microos-d4e3c6c7eed7627e851bcbe0: cookie, solver data, and index.
- microos-30730ffcfc3d76aac8b29438: cookie, solver data, and index.
- microos-4c2af10b2e15f152df0dff86: cookie, solver data, and index.

## Rule M: generated MIME data

The 14 MIME groups contain generated type-description XML, indexes/cache files, and their generated directories. None of these members is an input package XML file. S8.2-23 distinguishes values from code; these generated descriptions are not a person's chosen setting. S8.2-15 therefore gives RECORD. S8.2-16 governs which line covers what has already qualified as installed; it does not reverse the ordered questions to classify every generated data file as installed.

Primary documentation: https://specifications.freedesktop.org/shared-mime-info/latest-single/ — “It scans all the XML files in the packages subdirectory, combines the information in them, and creates a number of output files.”

Ten hand checks; complete member metadata was checked for file type, persistent storage, XML extension, and absence of exact package membership:

- microos-cfb3363718fdffa8e2decf3b: one chemical type description.
- microos-694303c3e26c4258aea1d9c7: five font type descriptions.
- microos-d57b64903524ac552f704f80: seven inode type descriptions.
- microos-93512b44fa58fc3da7d64afe: seven message type descriptions.
- microos-39fc4d3ee2703d92a368043c: eleven model type descriptions.
- microos-f44edeb7bae64c93251b6196: nine multipart type descriptions.
- microos-d11025d3c1706c2bf1f18c68: 33 video type descriptions.
- microos-4a6d90938dee0cb1148e2714: 19 content type descriptions.
- microos-e0e96d11a6b0449ff18790d9: one application type description.
- microos-819a45f8a130b43da2bc3d8c: 68 audio type descriptions.

## Rule D: directories with unknown creator

For the explicitly enumerated residual persistent directory-only groups, no member appears in the raw RPM file manifest, and no captured creation record identifies the creator. Directory execute bits mean traversal. Program-created working storage and person-created material are different S8.2-15 cases; therefore UNKNOWN. No inference is made from directory names alone. Ten hand checks: microos-9b1fbc813c5876fd618e71f2, microos-7e85ee24d5a79ba81acd55bf, microos-10f3f32ef128ab5c54608484, microos-13a878fb75c30087a0c945f2, microos-f259b60aca1fd13da7a98094, microos-fb60b6412ee79d20c1e490c3, microos-20f675737a015be831213148, microos-c3584b79f29f4bed45c410e1, microos-cbf1329980f813598d30e154, microos-1c25959e8ab1f682fdbeb3a3. Every listed member in these ten groups is a persistent directory; creation provenance is missing.

## Individual residual decisions

GRUB and EFI objects have recognizable functions, but their actual generation/installation lineage is absent. The documented normal installation procedure cannot prove how these particular copies arose. Primary documentation: https://www.gnu.org/software/grub/manual/grub/html_node/Invoking-grub_002dinstall.html — “generates a GRUB core image using grub-mkimage and installs it on your system.”

NetworkManager's persistent configuration/state files were separated from its leases, generated identity seed, and histories. Primary documentation: https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/NetworkManager.conf.html identifies the internal configuration file; the actual user-chosen versus default contents were not captured.

Generated certificate stores were not automatically called installed objects or inert cache. Their role is system trust; whether particular values represent selected policy or installation defaults is unretained. Primary documentation: https://github.com/openSUSE/ca-certificates — “by generating the certificate stores in /var/lib/ca-certificates”. The three exact groups are individually UNKNOWN for that missing origin fact.

Login accounting databases, journal files, timer trigger stamps, package history, and update cookies record events/state. No runtime-only exemption was inferred for their persistent storage. The eight persistent service-private temporary subdirectories and their parent group were each inspected and assigned RECORD as working storage. Authorized login keys are SETTING-OWN by S8.2-13 and S8.2-17.

No result here settles a hypothesis outcome or repairs the definition. Separate review remains external to this classification.
