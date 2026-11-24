# c1 developer: level-one inventory objects

Scope: all 855 rows whose kind starts `1:`. Input kinds are evidence labels, not classification premises. The ordered questions are applied before the clarifications. No other classification was read. Section 8.5 excludes storage mechanisms, execution-prevention design, and declaration representation from the definition; these were not treated as gaps.

## Deciding sentences

- S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”
- S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”
- S8.2-15: “Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.”
- S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”
- S8.2-17: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”

## Documentation and evidence

- [Runtime versus permanent firewall configuration](https://firewalld.org/documentation/configuration/runtime-versus-permanent.html): “The runtime configuration will be lost with a firewalld service stop.” Active nftables objects are runtime representations, not the persistent configuration files. `raw/developer/raw/0288-firewall-nft.out` records kernel objects; (not published: over 20 MB) confirms the firewalld executable unchanged.
- [Docker firewall integration](https://docs.docker.com/engine/network/packet-filtering-firewalls/): “On Linux, Docker creates firewall rules to implement network isolation, port publishing and filtering.” Docker chains and their dispatch rules occur in the raw nftables and iptables dumps. Integrity of dockerd is explicitly unknown; that does not turn its volatile kernel objects into persistent objects.
- [systemctl](https://www.freedesktop.org/software/systemd/man/255/systemctl.html): “List timer units currently in memory, ordered by the time they elapse next.” The timer rows describe computed schedules and service relationships, not unit file contents. The separately inventoried named unit files can be joined to unchanged package files. Services themselves are settings under S8.2-13; installation-default provenance is not inferred from being enabled or from timestamps.
- [Docker objects](https://docs.docker.com/get-started/docker-overview): “A container is a runnable instance of an image.” A container survives stopping; its object is not identical to its live process. The image and container rows do not identify the source from which the software was built or obtained. Hence UNKNOWN recording-line coverage, not a claim that container programs escape recording.
- [NetworkManager profile flags](https://www.networkmanager.dev/docs/api/latest/nm-dbus-types.html): “the profile was generated to represent an external configuration of a networking device.” The docker0 and loopback listing lacks these flags and profile filenames; persistence and selection provenance cannot be inferred from its inventory label.
- [uv caching](https://docs.astral.sh/uv/concepts/cache/): “uv uses aggressive caching to avoid re-downloading (and re-building) dependencies that have already been accessed in prior runs.” The cached distribution has package-file evidence for adjacent modules, a distribution script and metadata. The package row therefore cannot be reduced to metadata alone; installation status, integrity and recording-line provenance remain unknown.

## Rules and individual cases

The append script is `part-developer.runtime.build.py`. The rule register is `part-developer.runtime.rules.json`. Ten rows per homogeneous rule were inspected by hand, sampled across the rule's input order. Groups smaller than ten were inspected in full. The following lists name those rows and the check performed.

### group-provenance (1 rows)

Individual case: docker group exists. Rights are settings, but installation creation is not established by a script mentioning the group. S8.2-13/S8.2-17 leave default-versus-own coverage factually UNKNOWN.

Checked ids: developer-d6ef3204d2d59f03d916cd3f.

### packages-dependency (28 rows)

S8.2-7, S8.2-8, S8.2-16: each checked package has dependency or weak-dependency installation evidence, so INSTALLED-DERIVED.

Checked ids: developer-d4d82f71485e9b140ac1d1f4, developer-6b9313a5721f92ed06291713, developer-b311524f4a8678ba9d8a5f00, developer-591ec08ea347e8cacdf947d9, developer-f465d627c5732faa48fc2818, developer-6845e9adffcd5e2bd74ec2da, developer-a9c234e9e53100aaefb19797, developer-38f8b5645e0eced184ebfde9, developer-3d78f74ecf21220545a26372, developer-046ac8e3ec113c36853b15dc.

### packages-unknown (159 rows)

S8.2-7, S8.2-16: checked unknown reasons span RPM, Ruby and JavaScript packages. A name suggesting a dependency or native ownership is not installation provenance; UNKNOWN.

Checked ids: developer-f694215d525567ac79d0d548, developer-50bb2df9598f4b34122627af, developer-bd09f6b5aef9f19750f63155, developer-0a464868e534278d123e2d81, developer-44f35df4c754d1872548bb22, developer-00214b07b4d92d07e427d616, developer-af6ff0ccf4a800ddaa14abe2, developer-26e76176d6d66a7c4c9a9530, developer-32455c9601f6e8be3bafbb10, developer-620b132f11d8e6e2cddef774.

### packages-explicit (14 rows)

S8.2-7, S8.2-8, S8.2-16: each checked package has explicit native user reason or Python REQUESTED evidence, so INSTALLED-OWN. Package-file modifications do not revoke a package object being installed.

Checked ids: developer-af9c0a608cc0f364c46b411d, developer-701daecbee6e1a3ef1b528be, developer-763fc6a0cbe95f3edf0f2342, developer-718b98d43973ff60a8c3751b, developer-697868ba0250259f643d941b, developer-adace3ff93d390f5f20468bb, developer-418a6a4cdfe581b79ef85399, developer-03ae8d81719aee482d47b7fe, developer-9eadffa74288093eda2a239a, developer-7a079508519a5bf9d2a34ff7.

### cache-metadata (1 rows)

Individual case: the cached ruff distribution includes adjacent executable payload in its keyed package-file evidence. Cache location does not settle the first question or recording-line coverage. S8.2-6/S8.2-7/S8.2-9/S8.2-16 give UNKNOWN pending installation and derivation provenance.

Checked ids: developer-d1fbc4bd76f69c08a8b6ecf7.

### service-provenance (3 rows)

All three service cases inspected: containerd active, Docker active, virtqemud inactive. Their settings exist independently of packaged definitions. Whether state is installation-created default is not established, so UNKNOWN under S8.2-17.

Checked ids: developer-fbb9f41d4bfb9efb171f8f18, developer-317d285ab5339720849a2225, developer-97bf9d1dfc2e32ee6be3fcca.

### timer-observation (8 rows)

All eight schedule rows inspected, including the elapsed boot-success timer and user project-summary timer. Their timestamps and service relationships are runtime systemd products, so RUNTIME under S8.2-5; unchanged systemd executable is INSTALLED-PACKAGE.

Checked ids: developer-25988c74c9fc12cdd769d948, developer-ab7b63cc59abb629c9c0613d, developer-66dce0401f1031f1845995d8, developer-1f084ceb2e58b566a9075372, developer-57de0524b6f8df2ca477e95a, developer-a1e56f9fd0aadf1ee2bf123e, developer-031adf6dac2a13eba8f0f2c8, developer-534b8a8f0b0bb2bffac420af.

### unit-files (2 rows)

Both named system definitions inspected: package-files.tsv confirms containerd.service and docker.service unchanged. S8.2-7 takes precedence over S8.2-13; INSTALLED-PACKAGE.

Checked ids: developer-a527b386b205ae5c08fb5ee5, developer-207fda98bdbbe5567d1044cb.

### ports-live (15 rows)

S8.2-5: checked IPv4/IPv6 UDP and TCP observations are sockets. Standard port numbers alone do not prove program identity. The published container endpoint is matched to the container row and docker-proxy process; other owners remain UNKNOWN while every socket remains RUNTIME.

Checked ids: developer-7ec797c80a19cd58ceeb4e72, developer-d2d418b88270ce6396b53c64, developer-c1e89d71b39ebf8da50254a4, developer-f90e22fa51928e7a2543dc6a, developer-f8a4ca4e256a8a92b7a2a529, developer-902766ba06a1746b879e79eb, developer-1a4634ed14e7b7e0bb3642e0, developer-9d83af2dfc3bbfca8c08a0b1, developer-3c70ec2c0365aa1d508d10a0, developer-c1ce7858c570e6bd6d331189.

### firewall-live (516 rows)

S8.2-5: checked entries span tables, chains, nft expressions and IPv6 iptables rules; all describe active kernel structures. Firewalld versus Docker is identified from table/chain evidence. Creator integrity may be UNKNOWN, but every possible integrity outcome leaves the child RUNTIME.

Checked ids: developer-d53a52d9d07990c7e90a48b3, developer-e94fbd6f4653fb5fe4a3d222, developer-337af727cfc1246adabdaf7a, developer-283acc4471b6f4a70430b22c, developer-479950380e888e59b6ce1041, developer-87b2428a8f9281a1d518eccd, developer-79fcb054556c5ca19cc26e69, developer-4a9058c98307ae73b4976262, developer-eff231f11c2588a9e0cfe8ed, developer-a59bf80d82452c8f9994c2cc.

### dump-markers (15 rows)

S8.2-15: checked export comments and COMMIT delimiters are program-generated serialization text. They do not identify independent kernel rules or person-typed actions; RECORD.

Checked ids: developer-d44dc05c00ee82aae4b19fcc, developer-31753c65fe96cf90eeb71e47, developer-fc27f336bee149a225fa68b3, developer-ca8176047cba3cff3dd8129c, developer-ccf4158c3a6735e6f1745666, developer-c5c4bcd2326cbf521ac6f49b, developer-adf13e98722463e3fa976ecd, developer-afacb1fa7d8bea24ff9996a2, developer-6f5fafb489533507b56a44cd, developer-9736a05ec42eb40dc640f190.

### network-provenance (2 rows)

Both docker0 and loopback profile records inspected. Neither includes on-disk storage nor generated/external flags. NetworkManager documentation permits volatile external profiles, so UNKNOWN rather than assuming a saved person-selected network.

Checked ids: developer-576dfc23d438538fedc140bc, developer-e67ac394759cef48535ff171.

### container-object (1 rows)

Individual running web container inspected: filesystem, port, command, image reference and zero changed-byte size are present, but installation/build source lineage is not. A stopped container can persist; its complete object is not just the volatile process. UNKNOWN recording-line coverage.

Checked ids: developer-59a4ddfe60a8a1b18f6627c9.

### container-image (1 rows)

Individual local web image inspected: image identity and size establish stored executable software, but the local tag and creation timestamp do not establish build source or installation lineage. UNKNOWN under S8.2-16.

Checked ids: developer-78e8326714450972e0134fb6.

### process-live (74 rows)

S8.2-5: checked PID observations include identified unchanged executables, unknown executables, and dockerd with unknown integrity. All are live process instances, not executable files. Known executables are joined individually to package-files.tsv; absence of identity is explicitly retained.

Checked ids: developer-a60611693bc80a3b1d22e8a5, developer-ae0bce02c33762c6a56b10c2, developer-a93cba06bf41abde8d450d31, developer-c21f181244c1042808b8b05a, developer-03062b76ddbfefd62fe485b4, developer-2ea7ee9d50cb25f5a2a46fdb, developer-69109f05650d6625339330f4, developer-6641f8cd5d91872c6aa1f372, developer-70f3c0799678f658fdc28fbb, developer-7b6aa50ce473ea712ac7b9ad.

### modules-live (12 rows)

S8.2-5, S8.2-7, S8.2-16: checked module names are loaded instances; each corresponding .ko.xz file has unchanged package integrity. The stored file is INSTALLED-PACKAGE; its loaded instance is RUNTIME.

Checked ids: developer-147457400648caa4c843cf2d, developer-2db63ae53d18252e01db1118, developer-38dad286fdf7c16943f96b0a, developer-81a50ce037b63cab624feca6, developer-91077c880e54f5669e42d829, developer-69a2455cf656b1ef5b93f13b, developer-f474e9be8bfc620ad4cbbcdf, developer-a316fdff356162cce27895cb, developer-caac0e8c41b1566d9fffa9d1, developer-3b5704fa0d42b0775e12a76a.

### user-service (1 rows)

Individual user project-summary service is enabled according to the separate unit-file listing, though inactive now. Its installation-default versus later-selection provenance is unestablished, so UNKNOWN under S8.2-13/S8.2-14/S8.2-17.

Checked ids: developer-5eb44d0def12c43daae1fbb3.

### user-unit-files (2 rows)

Both project summary files inspected in members/8eec9396036ab3dbdc3aa47b.tsv: persistent unit-value files launching work. Their user directory and custom names do not establish creation provenance; configuration-origin.tsv says created=unknown. Default versus own coverage therefore remains UNKNOWN under S8.2-14/S8.2-17/S8.2-23.

Checked ids: developer-525ed7742d9bd835216a4b96, developer-da97ea3d424d9e95f97e9301.

## Validation

855 input and output ids match exactly, each once; six fields per row; all decisions belong to the allowed vocabulary; description and reason word limits hold. Existing completed rows are preserved by the append script. No whole-file integrity is inferred from prefix signatures.

Final reviewed partition counts: 625 RUNTIME, 171 UNKNOWN, 28 INSTALLED-DERIVED, 15 RECORD, 14 INSTALLED-OWN, 2 INSTALLED-PACKAGE. The four corrected rows are reflected in the main output; the partition TSV retains its initial decisions as a working record.
