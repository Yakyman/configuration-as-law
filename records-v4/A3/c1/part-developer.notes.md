# Classification c1: developer part

The ordered questions in Section 8.2 govern this classification. Runtime objects are handled by S8.2-5 before treating stored objects. Inventory labels are not classifications. Section 8.5 exclusions are not gaps. No earlier classification or other task folder was consulted.

Sources: (not published: orchestration), TEXT.md Sections 8.1–8.3 and 8.5, SENTENCES.md, (not published: direct evidence at least 2 MB), A3/in/FACTS.md, and the inventory under A3/in/raw/developer/. The executable and package/runtime partitions have separate notes, incorporated below when complete.

## Rule G1: development payloads with unresolved provenance

Apply only to persistent member lists in development installation, distribution, or module trees selected in part-developer.groups.py. Read every complete member table and join every member path against package-files.tsv. The join is empty for these groups. FACTS.md and metadata.json explicitly identify missing manifests and integrity coverage. A current hash, even covering the whole small file, has no installation hash to compare with. Public documentation establishes function and layout, not the historical bytes received on this particular computer.

S8.2-6: “What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.”

S8.2-7: “Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?”

S8.2-16: “What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.”

These unresolved facts affect whether package coverage applies or later questions must be answered. The result is UNKNOWN, not a textual gap. The rule does not infer code from an executable permission or treat an entire package tree as a cache record. A group with undetermined membership classifications is UNKNOWN; MIXED requires established differing member decisions.

Manual checks (member lists read, functions compared, empty ownership joins and persistence verified):

- developer-6a7c157fa38a970254916264: hello.mo translation; no installed comparison digest.
- developer-1a97c34a462cc1410fa25ce0: Homebrew command source files and subdirectory; executable source does not answer the earlier provenance question.
- developer-3e36e481b6ad4beb1ea17a1e: ESLint JavaScript and directories; package metadata does not establish unchanged payloads.
- developer-0d9f9a717a59bc5f7f480362: Julia executable; current signature lacks an installation comparison.
- developer-c848e848496d7effed8c8ec8: Julia startup source; default versus altered code unresolved.
- developer-13595c89248060943a644cc6: Go module source, licenses and directories; downloaded module integrity not collected.
- developer-ad5a8688079bb0eaac678aea: gem payload directories; gem file manifest unsupported.
- developer-b62fee8be986a1229ba680e5: uv extracted wheel directories; no joined installed file records.
- developer-ed92a9464f72120acbd88eaf: linked manual resource; target and installation comparison absent.
- developer-466af1de352740b969a5beb1: Bun cached package license, documentation, metadata and code directory; registry-cache status alone does not exclude installed payloads.

Documentation consulted:

- https://bun.sh/docs/pm/global-cache — “Bun stores every package downloaded from the registry in a global cache”; documents hardlink sharing with installed modules.
- https://github.com/JuliaLang/juliaup — “Juliaup will by default use the Julia depot at (not published: record outside this collection) to store Julia versions and configuration files.”
- https://go.dev/ref/mod#module-cache — “The module cache is the directory where the go command stores downloaded module files.”

The documentation explains what these trees contain but cannot establish installation integrity on the inventoried computer.

## Rule G2: Go build cache, revised after review

The cache implementation at https://go.dev/src/cmd/go/internal/cache/cache.go states: “An OutputID is a cache output key, the hash of an output of a computation.” It stores cached executables in directories rather than regular output files. Every member list was checked: the root contains 256 directories and cache bookkeeping; the 256 bucket groups contain only non-executable regular files. Nevertheless, a regular output file's exact content and possible execution through another program are not recorded. Groups containing `-d` outputs are therefore UNKNOWN under S8.2-9, S8.2-15, S8.2-16, and S8.2-20. Permissions are not proof that code cannot execute. The initial RECORD decisions for these 253 groups were corrected before completion.

S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?”

S8.2-20: “A file containing code that cannot be executed on this computer is not a program.”

Ten manually checked output-bearing buckets: developer-96805d38cf622a0b45a638f4, developer-650d3dab1c8508be4ef8a326, developer-08aca4caf42acd1a6cea5018, developer-ac78bae1601bb68233bcbcc4, developer-d9058bb9bd574c10f8c108c0, developer-0cc6871e90c4404ce9d12b9d, developer-bd6fd6d1e30ca860911a8252, developer-ade31a61eaf818d6da23f745, developer-8fd957c1444d5052df4fe883, developer-f63cbda01ff1adffa1c9bd5d. All contain regular `-d` outputs with no captured payload.

The four remaining cases were inspected individually: developer-a9570087e095af2bb34ce922 (cache root), developer-8e4741c8990fe035b816f7bf, developer-0e5ee95188114b28bd055b8d, developer-5bd472ce02d9a509e8a327b3 (only `-a` action-index metadata). Their data role is established by the documented layout; all are RECORD.

## Rule G3: Git databases and reference history

Only `.git/objects`, `.git/logs`, and `.git/refs` member groups are covered. Repository configuration and hook directories are excluded and handled individually. The complete lists contain database files and directories, not executable hooks. Git creates the stored database representation and reference history; these are RECORD under S8.2-14/S8.2-15. https://git-scm.com/docs/gitrepository-layout states: “Records of changes made to refs are stored in this directory.” It separately documents loose object storage and compressed packs.

Ten manually checked groups: developer-34ff1266d97dfc438fffa565 (HEAD log and directory), developer-90e7760b30e36f3c7cf280e2 (reference log), developer-1d3287e35199c7706dd1f2a0, developer-c2f1f76accb01c614f63add5, developer-6249738d7d0e0c657e17ba88, developer-f643dc4c3df7cc143e497044, developer-5f756792fa0da827e02d428f, developer-21002117106a6f6fe09693b1 (loose objects), developer-f364153a1af2824fe9ef23ca (pack/index/reverse-index files), developer-e3d0750d70c70672b308f622 (branch reference). Persistence and non-code database roles were checked for each.

## Rule G4: repository and manual-page metadata caches

The 58 PackageKit, libdnf5, and man-db cache groups contain metadata, indexes, cache tags, and directories. They have no installed-manifest joins and no executable files. The documented stored metadata role, rather than permission alone, supplies RECORD under S8.2-15.

- https://dnf5.readthedocs.io/en/latest/misc/caching.7.html — “These contain metadata files in the repodata directory and solver-generated cached files in the solv directory.”
- https://www.freedesktop.org/software/PackageKit/doc/method.Client.refresh_cache.html — “Refresh the cache, i.e. download new metadata from a remote URL so that package lists are up to date.”
- https://manpages.debian.org/unstable/man-db/mandb.8.en.html — “mandb is used to initialise or manually update index database caches.” This is the distributed upstream manual.

Ten manually checked groups: developer-f5524e72d9d4c40489a58532, developer-6f9a52bcac80bffc6cfb44b7, developer-b32d8806cb04ca116160a832, developer-a419b07b4143f33a89f73f20, developer-f3f15ce185eac70efee373b2, developer-11683639d2042e12d59db836, developer-85370bd02a407aa5cd74a307, developer-822543efc953f75e4043391e, developer-b954f300ec78ea9bf5f431fd, developer-c4a22e672a8fcf730bd68d47. These span cache root directories, solver caches, compressed XML, and manual indexes; all listed members fit the rule.

## Rule G5: volatile member groups

All 149 groups whose complete members have runtime filesystem facts are RUNTIME under S8.2-5. Each is joined to its immediate creating program; unchanged executable package-file integrity yields INSTALLED-PACKAGE for that creator. Missing creator integrity is explicitly UNKNOWN. That missing fact does not change the child's runtime-only status. Source settings remain separately classifiable; the sentence permits the program **or** setting creating the runtime object.

S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”

Ten manually checked groups: developer-b3741e882fd6a9f3371ef873 (NetworkManager state), developer-b2a1a353004ebffe9bd74868 (Avahi pid/socket), developer-15e7d233131bb14980287027 (chrony pid/socket), developer-88524d1062d840ebb324d24b (containerd sockets/state), developer-723a48eb2873379d74575875 (CUPS socket), developer-602f7a1d42dcb854cab79b53 (system bus socket), developer-17c028b0c940ab1051886b1b (Docker runtime state), developer-d915c2e0f38299dd33c19f1f (generated systemd units), developer-a81068bd512224d05af9acc2 (udev link index), developer-bfafb8972d007473d4280335 (service private temporary directory). Every member is runtime. Creator binary integrity is taken from package-files.tsv, not guessed from package installation.

Review corrected the generic libvirtd mapping: developer-df39a529b53c474304339913 contains modular-daemon sockets; developer-bc2eff9fbcd1c8ce543692ad is QEMU daemon state. These remain RUNTIME with more precise creators.

## Rule G6: vendored dependency groups

The 268 vendored Go dependency groups are UNKNOWN because installation equality, source acquisition, and generation lineage are not recorded. Vendor directory names do not establish whether these are received package parts, generated copies covered by source lines, or independently brought source material. S8.2-7/S8.2-9/S8.2-15/S8.2-16 apply. Public Go module documentation establishes the role of vendored source, but not these machine-specific facts.

Ten manually checked groups: developer-a2d454adf72b7ce2898862f7 (module index/root), developer-da9790aecea91fae6029286c (cryptography source), developer-9e2eed9d988f26e3b02a23e7 (license/directories), developer-702037008bf04c53714c3411 (tree source), developer-ad29964745c5dbe52e663c8b (filemode source), developer-eaec09a075c1b9887c172796 (transport source), developer-5943b0e7f62029f8ca95c7e0 (dependency directory), developer-3d1aed13d9f02b3cb916f43e (logging dependency directory), developer-cf2588417916cb42778a118d (conversion source), developer-c3de997739e7fad7a691cb02 (hash source). Complete lists are persistent and lack package-file joins.

## Rule G7 and individual residual decisions

The 225 residual groups were inspected individually. Their explicit decision ledger is part-developer.individual.tsv, produced by the indexed ledger in part-developer.finish-groups.py. Its only fallback is a checked, directory-only rule: 34 groups contain exclusively persistent directory members, with no recorded installation or creation provenance. A directory's search permission does not make it executable code. Whether it is a received package directory, program-created storage, or a person-created material directory changes the answer to S8.2-7/S8.2-15/S8.2-16, so UNKNOWN.

Ten directory-rule manual checks: developer-dbda9c2db4e034cde4638a44, developer-2b039a17e2a57d841b207b78, developer-8059a05cc81e6520c9bba28c, developer-e738a23ce6f94d1293e85462, developer-d7d8677c46ce0ff9dd33a05e, developer-c0dc57ef91e4b593c5b65569, developer-1c90312d29ecb155d5f5d1de, developer-496739a27f456e87f7332b82, developer-b8d1544904823ce3d0eb45e3, developer-6294c2d52e1576fe08d85586. Each complete member list consists only of directories on persistent filesystems; none has a per-path installation manifest match.

Special residual evidence:

- configuration-origin.tsv reports `created=unknown`; timestamps and package-script mentions do not prove defaults. Firewall, service-property, and custom unit groups therefore retain UNKNOWN where default-versus-own coverage is unestablished.
- https://go.dev/doc/telemetry — “By default, telemetry data is kept only on the local computer”. Counter files are records, not executable payloads or the telemetry-mode setting.
- https://docs.astral.sh/uv/concepts/cache/ documents dependency caches and generated metadata; no assumption that all cached payload is non-code is made. Receipt, interpreter-index, and resolver metadata groups were separated from extracted payloads.
- https://github.com/SELinuxProject/selinux/wiki/High-Level-Language-Infrastructure — “The HLL data, cached CIL data, and HLL extension are stored”. CIL/HLL files and language metadata were inspected separately from policy booleans; source and default provenance remain missing.
- https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/NetworkManager.conf.html documents NetworkManager's internal configuration file. Its captured name does not disclose the actual selected values; the group also contains leases and history, so no single known member classification is asserted.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html documents private temporary directories. Persistent private storage is not inferred volatile solely from its name; stored working directories are RECORD, while tmpfs groups are RUNTIME.

Four objects expose the collector's broad filesystem-label limitation. developer-b18fbe731b7c03811a1b2eea has raw filesystem magic `0x6e736673` (nsfs). developer-2fb915987929c6ab62914533, developer-c68f5b7002f3124253c1983b, and developer-7146368fa3d417ecf4ad4529 have `0x67596969` (rpc_pipefs). The raw type is more specific than the collector's generic persistent label:

- https://github.com/torvalds/linux/blob/master/include/uapi/linux/magic.h identifies the magic numbers.
- https://raw.githubusercontent.com/torvalds/linux/master/fs/nsfs.c uses `init_pseudo(fc, NSFS_MAGIC)`.
- https://raw.githubusercontent.com/torvalds/linux/master/net/sunrpc/rpc_pipe.c describes “Userland/kernel interface for rpcauth_gss.”

These are kernel interfaces, not persistent stored files. The namespace handle belongs to dockerd (binary integrity UNKNOWN). The unchanged sunrpc.ko.xz package member establishes the SUNRPC creator as INSTALLED-PACKAGE. No live probe was needed.


## Incorporated code-candidate rules and checks

# Code-candidate subset: independent classification notes

Scope: 619 input rows. The inventory label was not used as a class. All objects have persistent filesystem metadata. None joins to an installed per-file manifest in (not published: over 20 MB). A missing match is not a proof of non-package origin: `A3/in/raw/developer/metadata.json` records incomplete ownership, unavailable adapters, and missing language-package file provenance. Installation reason is consulted in package object metadata but cannot determine the origin or integrity of an individual file absent a manifest. Prefix signatures do not prove unchanged package bytes. No experiment was performed.

## Exact deciding text

- S8.2-6: "What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order."
- S8.2-7: "Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?"
- S8.2-9: "Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?"
- S8.2-15: "Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines."
- S8.2-16: "What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package."
- S8.2-20: "A file containing code that cannot be executed on this computer is not a program."
- S8.2-23: "A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code."

## Homogeneous rules

R1, registry: the 76 `.npm` binary response caches are RECORD. The documented purpose is data caching, not executable package payload. Package metadata downloaded from a registry is not itself an installed package. S8.2-23 distinguishes data from code even though the inventory marks a shebang; S8.2-15 therefore applies. The file permission is non-executable in all 76 rows. Official documentation, https://bun.sh/docs/pm/cli/install: "Bun uses a binary format for caching npm registry responses." This establishes the function; the inventory establishes the stored instances and persistence.

R2, payload: 467 files in package-manager/distribution payload trees lack a per-file package provenance and integrity record. UNKNOWN follows from the missing first-question facts, not from their directory names or permissions. The rule applies to an evidentially homogeneous deficiency, not a claim that all these objects contain code. An unchanged received file answers question one; a modified or independently supplied file requires later questions and a different label. Native reason facts cannot cure missing file provenance. Even foreign-architecture executables and non-code maps can be installed objects if unchanged package parts. Names alone cannot demonstrate their unmodified status. Documentation establishes functions but cannot establish these machine-specific facts.

R3, project: 68 project-tree files lack recorded supply/generation lineage. UNKNOWN records missing package origin or whether system derivation supplies coverage under S8.2-16. Project location does not prove material, and a script marker does not establish compatibility of a fixture. A general-purpose checkout or copy is not automatically an installer. No declaration-source or build-origin relation for these individual files is present in the supplied evidence. These missing facts change the result; this is not a textual gap.

Official context checked: https://github.com/JuliaLang/juliaup describes "Julia installer and version manager"; its add/remove operations establish installer purpose, not per-file integrity. https://git-scm.com/docs/git-init states "The sample hooks are all disabled by default." Disabled hook automation does not prove code cannot be executed manually; nor does a matching filename establish this particular copy's origin. Therefore Git sample hooks were not automatically labeled records or assigned derived coverage.

## Hand checks

For each listed row, the input metadata, path role, size, shebang/executable flags, persistence and absent manifest match were individually inspected. R1 checks confirm documented binary manifest-cache names. R2 deliberately includes data maps, archived fixtures, libraries and a foreign-platform executable to check that permissions do not replace question one. R3 includes scripts, hook samples, a tiny shell fixture and vendor code to check provenance rather than infer it from the project directory.

R1: developer-caf849f32050f8f8d12ca9c9, developer-1351463a6c67a00b6ee824ce, developer-4d82397294549802f9a0a5d6, developer-13f3e979b7195c668b372e8e, developer-704817ab60b35f13c0e2005e, developer-da2f14a256b5b59480761bc6, developer-6a6f2d7a3174a472748920b6, developer-e59844a05db92d3fa2608cb5, developer-af3b6882902935de10d39fb1, developer-cbfa619e0e3a123f9def8ee1.

R2: developer-2b53d455423cfccaa4ae8081, developer-695307ca85aebccd79b75006, developer-3e0790e8049f62cc71573ccc, developer-372014b2910fad6fad91da8e, developer-ed2ac74ec772f402f717c2df, developer-95586c676e3caba1d88defbc, developer-b965a1722c56137354b94d1e, developer-b288f685882c7c05021a4cd0, developer-48981bee5071dfce5d670349, developer-e0df0b0557ce677d8b3377f1.

R3: developer-9c4f107f9425a7455cd22c18, developer-8e112490c91a0cf94ff6eb1a, developer-5b44798ac7cac25ba65ace08, developer-f5570a6f0e6ae6957e5d423e, developer-4bfe0e664e563e64a225a044, developer-dd8872530d8a274849e8595e, developer-cca6f855eac328e8e043ca40, developer-e30974b2a09f5aa1302aaa27, developer-2c0fd3c3d00e154b409fc979, developer-6be81830b9c95010f8cbead7.

## Eight individual decisions

The two shell startup files differ from the untouched-base signatures and sizes. Both are shell code, but the recorded changes have no author or generator provenance; own versus derived remains unknown. Their initial and final metadata are in the respective `raw/0004-filesystem.out` files and creation provenance remains unknown in `configuration-origin.tsv`.

The runtime executable and two Python-tool executables have neither a manifest match nor full installation digest; installation origin and integrity remain unknown. The project-summary script is executable but the inventory does not preserve its source or creation method. The hook-manager command wrapper might be generated or received; its wrapper creation provenance is absent. The compiler runtime library lacks a current manifest match despite the compiler runtime package being present; package presence alone does not establish that this file remains as received.

Checks: 619 unique output IDs, exactly the subset IDs; 543 UNKNOWN and 76 RECORD. All output descriptions and reasons satisfy the word limits. Output is appended and flushed row by row; restarting the script preserves existing rows.


## Incorporated level-one rules and checks

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


## Final review and validation

The independent review is recorded in part-developer.review.md. Its retained findings were applied: 253 Go payload-cache groups became UNKNOWN; two libvirt runtime creator descriptions were corrected; three project-summary settings became UNKNOWN because creation provenance is absent; the cached ruff distribution became UNKNOWN because its package evidence includes executable payload. Earlier values are preserved in part-developer.revisions.tsv. The final main TSV supersedes working partition TSVs.

part-developer.finalize.py validates the exact header, all 6,409 input IDs with equal set and count, uniqueness, permitted decisions, sentence IDs, six fields, and description/reason word limits. The completed count file is part-developer.done. No machine experiment was performed.
