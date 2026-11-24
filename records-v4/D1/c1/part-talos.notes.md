# Talos classification c1 notes

(not published: orchestration) was read first. The decision standard is TEXT.md Sections 8.1–8.3, with Section 8.5 exclusions; SENTENCES.md supplies the cited identifiers. Only the assigned Talos input and its indexed raw evidence were used. The other classification, comparison, adjudication and earlier nights were not consulted.

The three parallel parts partitioned input indices 0–91, 92–212 and 213–277. Their decisions are consolidated without removing image aliases or repeated paths: input row identity is preserved.

## Container image rule

Rows 213–224 are containerd image observations. The first question, together with the installer/package definitions, takes precedence over describing their executable payload as a program. S8.2-16 requires selecting a recording line. The observations establish image presence and CRI management, but not whether an image was obtained explicitly or from another recorded object. Both acquisition routes are possible; this is a missing instance fact, not a conflict in the text. All twelve decisions are UNKNOWN.

Ten rows were checked manually against the complete image metadata, matching image reference, digest, timestamp, size and management labels. The first eight are tag/digest pairs for the API server, controller manager, scheduler and pause image; the next two are image-ID aliases of controller manager and scheduler. None contains acquisition-reason or source-line evidence:

- talos-ad5f9ee7ce61d8724bb1f543
- talos-fc367f32307655c2a5babe38
- talos-655133309975caeeb6640386
- talos-c2b615022e7beec6f21748c3
- talos-5defa9092f0736a78e47ecd5
- talos-a004b567792051e3e6965bc9
- talos-a20f4b312088c2c878ded20c
- talos-f4c9f6b3c25df46210a80b66
- talos-4e385729d820ae8a12c281ea
- talos-70f7ef9c1053aac7ea64a328

The remaining two image-ID aliases were also checked individually against the pause and API server digests. Management and pinned labels do not identify the acquisition source.

Primary documentation:

- https://github.com/containerd/containerd/blob/main/docs/cri/crictl.md : “The pull command tells the container runtime to download a container image from a container registry.” The same guide documents image loading from an archive. Neither establishes how these particular images arrived.
- https://github.com/containerd/containerd/blob/main/cmd/ctr/commands/images/pull.go : “Fetch and prepare an image for use in containerd.” This identifies image acquisition functionality rather than a conventional native package manager.

## Stored objects: individual assessments

Every row from 225 through 277 was assessed individually. All 35 complete immediate member tables were read, including every listed member of the large udev data, links and watch groups. The other rows are eleven opaque directories and seven executable-permission candidates. Each output explanation identifies the missing instance fact; no classification rule based on the collector's kind label was used.

FACTS.md explicitly states that all member persistence fields are unknown, signatures were not collected, and the mount observations are not a certified object-to-covering-mount persistence map. The 287 captured package-file candidates also have unknown integrity. No unchanged package ownership is inferred for paths outside that bounded candidate list.

Mount relationships and stored directory entries are distinct input objects. An active mount is runtime, but its path alone does not establish the origin of the underlying stored directory or the backing of every nested member. The container rootfs mounts below /run are a concrete reason not to extrapolate the enclosing tmpfs to opaque descendants. General documentation cannot certify an unobserved bind mount, file content, integrity, or creator on this instance.

The listing's executable flag for /run/mdadm/autorebuild.pid was not treated as code. Upstream source identifies the file as a process identifier written with mode 0700. The unresolved decision is its actual storage lifetime, rather than whether an execute bit automatically makes a program.

Primary documentation and scope of use:

- https://kernel.googlesource.com/pub/scm/linux/kernel/git/hare/mdadm/+/f7a6246bab1541d7208a5f0f9f0c6cac114e38da/Monitor.c : `open(path, O_WRONLY | O_CREAT | O_TRUNC, 0700)` and `fprintf(fp, "%d\n", pid)` identify PID-file creation and explain the misleading execute bit.
- https://www.cni.dev/plugins/current/ : “These are general-purpose CNI network plugins maintained by the containernetworking team.” Individual entries identify bridge creation, local address allocation, firewall rules and port mapping. This establishes the named programs' roles, not the signatures or provenance of the inventoried files.
- https://docs.kernel.org/filesystems/sysfs.html : “sysfs is a RAM-based filesystem initially based on ramfs.” This identifies sysfs semantics; the opaque /sys directory observation does not itself certify its mount identity or expanded contents.
- https://docs.kernel.org/filesystems/proc.html : “The proc file system acts as an interface to internal data structures in the kernel.” This identifies procfs semantics without supplying the missing instance mount observation.
- https://cdn.kernel.org/doc/html/latest/filesystems/tmpfs.html : “Tmpfs is a file system which keeps all of its files in virtual memory.” This explains why object-specific backing matters: a transient object and a persistent working record can have different decisions.

No group is marked MIXED merely because filenames suggest heterogeneous purposes: differing decisions must be established. For these stored groups, the missing facts prevent definitive member decisions. This is UNKNOWN rather than a defect of the text. Section 8.5 implementation questions were not counted as gaps.

## Deciding sentences

- **S8.1-4** **Installer**—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.

- **S8.1-6** **Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.

- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-11** Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?

- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.

- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

## Part 1 notes

# Part 1 classification notes

Scope: input indices 0–91, 92 rows. Only (not published: orchestration), TEXT.md, SENTENCES.md, the assigned input, FACTS.md, and this input system's raw records were consulted. Section 8.5 adds no classification conditions.

Facts: FACTS.md and package-files.tsv establish unknown integrity for every captured image file; read-only backing is not integrity evidence. Stored-object persistence is unknown. The installed image package has explicit installation reason. Neither uncertainty changes the classification of live processes or mount relationships: S8.2-5 applies to these runtime instances, not their underlying stored files.

## Applied rules and manual checks

1. Current mounts and mount-status resources are RUNTIME under S8.2-5. Actual mount records name an active mounted target; resource metadata names a controller and runtime namespace. Creator decisions remain UNKNOWN under S8.2-7 and S8.2-16 because unchanged executable identity is not established. Container rootfs mounts are attributed to containerd; boot mounts and block mount resources to machined. Ten manually inspected rows, checking mount targets, API owner, or active filesystem columns:
- talos-b02c86d496a85cd38e7e387d
- talos-4adb7ee22e4573244c86f62f
- talos-112f6ce3cb5100c97870cc46
- talos-5e264ed8df4e6bacf058b2bb
- talos-6bbaab687adf3605094a0dd9
- talos-c0e1e3024ad9131bc0c424c2
- talos-47175859997987bc259f9388
- talos-6a46e501fb1992e34e0b00c1
- talos-a3c68f4b469259b6ad8f61a5
- talos-016636da9c246655145b92ca

2. Observed processes are RUNTIME under S8.2-5. PID, command, state, and memory fields identify execution instances. The command executable is named in reason; worker processes belong to systemd-udevd. The executable's decision remains UNKNOWN because provenance/integrity cannot distinguish S8.2-7 from S8.2-9 or choose its S8.2-16 line. Ten manually inspected commands and process records:
- talos-766637443513dd04c7175be0
- talos-394a1f54323cd0848f6846f4
- talos-466c019323ca75c7a29014a7
- talos-8f6ce810650c787d7fb51560
- talos-125c353a5a649ae6d2736beb
- talos-ebfec63b284ab43530bea97d
- talos-de8222af24eecec481851884
- talos-0bc874346da246e30e75149c
- talos-b11d0fde55a1da20a3f7d9c1
- talos-903be24c0d10e796b8913ff7

3. Loaded-module status resources are RUNTIME under S8.2-5. Each record identifies runtime.KernelModuleStatusController, a live state, reference count, and memory address. These are observations of loaded code, not separately inventoried module files. Creator machined remains UNKNOWN for the preceding integrity reason. All ten manually inspected records:
- talos-2786c8805d2d10a875f176ff
- talos-f5a3f3a37d6e525c620e500c
- talos-e30336268d6a95b7eeb96bc7
- talos-df94dd9ec61a8656d22d0685
- talos-8cb9be484b02d7ed85022630
- talos-64d78123c87a2749fdb4eeab
- talos-e48c1b1d7bf40d74239fc1d0
- talos-c6f2d0ceb3c08113cdb26d1c
- talos-fa52cd69e366d5a87a93558c
- talos-e308c4b29560ae80db17cc99

4. A named system service is a setting under S8.2-13, but the service-status query alone does not establish its configuration's origin. S8.2-7 precedes S8.2-11; S8.2-17 distinguishes default from separately chosen values. Therefore UNKNOWN: a running service does not prove unchanged packaged configuration, installation defaults, or personal selection. This does not treat service status as evidence that every service was explicitly enabled. Ten manually inspected service names, states, and last-event fields:
- talos-2460ff1bf90731c4d0396e53
- talos-ea25f1cd0ddf09183b339dfe
- talos-720a4c38c495d5f81d0920c8
- talos-0562357a4d7bc8da0fb6544f
- talos-1f95e03e468aa8e91113c4a7
- talos-b6b695f738a4b20f37d515bb
- talos-ac61467428d376073f3b4466
- talos-7f23712d563026482709ffc1
- talos-9311e018d90e007503711ee3
- talos-999b2dc7cbd5907385abd795

## Individual decisions

The four block-device rows were inspected individually: loop0 and loop1 expose loop-backed filesystem image devices; sr0 exposes the virtual optical device; vda exposes the virtual disk. The supplied objects are Disks.block.talos.dev resources, with runtime namespace and block.DisksController owner. RUNTIME refers to these runtime discovery resources, not to disk contents or physical hardware. Each reason identifies the creating controller and machined's UNKNOWN classification.

The image row is INSTALLED-OWN: S8.1-6 explicitly makes the installed image a package; S8.2-7 and S8.2-8 classify that package, while its explicit reason selects its own S8.2-16 line. File-integrity uncertainty does not negate the installed package's identity.

## Primary documentation

- https://raw.githubusercontent.com/siderolabs/talos/main/internal/app/machined/pkg/controllers/block/mount.go : “MountController performs actual mount/unmount operations based on the MountRequests.” Supports the mount-controller role.
- https://raw.githubusercontent.com/siderolabs/talos/main/internal/app/machined/pkg/controllers/block/disks.go : “DisksController provides a detailed view of blockdevices of type 'disk'.” Supports interpreting the resource as a discovered runtime view.
- https://raw.githubusercontent.com/siderolabs/talos/main/internal/app/machined/pkg/controllers/runtime/kernel_module_status.go : “KernelModuleStatusController presents both built-in and dynamically loaded Linux kernel modules as resources in the runtime.” Supports identifying the status representation.
- https://raw.githubusercontent.com/siderolabs/talos/main/internal/app/machined/main.go : “Package machined provides machined implementation.” Source imports the controllers' host runtime and service packages; init dispatches the system service executable. Documentation identifies program roles only; it cannot establish integrity of this machine's executables.

The script appends completed records and flushes every row. It verifies exact assigned IDs, unique count, and field word limits. Counts: RUNTIME 79; UNKNOWN 12; INSTALLED-OWN 1.

## Part 2 notes

# Part 2 classification notes

Scope: zero-based input indices 92–212 inclusive, 121 rows. Only the fixed text, sentence list, fact index, assigned input, its raw inventory and official public source/documentation were consulted.

## Rule N: in-memory network resources

S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”

Rows 92–144 represent API resource instances in the network namespace, not the persistent machine-configuration source. All are RUNTIME. Their raw metadata identifies the creating merge/status controller. The controller runs within machined. Its own installed/program classification remains UNKNOWN because packaged-file integrity was not established; this does not change the resource instance's RUNTIME decision.

Official source matching the observed v1.14.6 version: https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/internal/app/machined/pkg/runtime/v1alpha2/v1alpha2_state.go . NewState selects `inmem.NewStateWithOptions` for each namespace. The namespace registration explicitly includes network and network-config. The resource registration includes each inspected spec/status class. This establishes resource-instance lifetime separately from unknown stored-file persistence in FACTS.md.

Manual checks: read the complete raw metadata/spec of the following ten input rows, matching id and owner. Three LinkSpecs and the loopback AddressSpec have default layers; two physical AddressSpecs and two RouteSpecs have operator layers; the DNS forwarding AddressSpec and ResolverSpec also have operator layers. No operator label was treated as evidence of a human choice. All ten are merged in-memory objects.

- talos-6998c9d70456b15188cbe45a
- talos-bf5eb87a0976ac7dfdb8bbad
- talos-3a372dbbd8996d951d2d9ff6
- talos-846c6d9627d5b430af7382a7
- talos-ab374453e69e6dcf4c90aca8
- talos-26b02098e721b15ae85cc44e
- talos-c53c0d03e040c6ad4e14d59a
- talos-580f529f02d78acb23c0b7ad
- talos-37f5b08127cb39525bcde935
- talos-07fd45398afa808b12852ac0

## Rule S: live sockets

S8.2-5 explicitly excludes open ports as separate objects. Rows 145–210 are live TCP/UDP socket observations; all are RUNTIME regardless of owner. The raw netstat columns omit process identifiers, so endpoints alone do not establish arbitrary client ownership. Unknown ownership and inherited decision are stated without converting a certainly ephemeral socket into a separate UNKNOWN object.

Official constants for v1.14.6 identify documented server ports: https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/pkg/machinery/constants/constants.go . Relevant literal assignments: `EtcdClientPort = 2379`, `EtcdPeerPort = 2380`, `EtcdClientHTTPPort = 2383`, `KubeletPort = 10250`, `ApidPort = 50000`, `TrustdPort = 50001`, `DefaultKubePrismPort = 7445`. Together with running-service observations these support the stated server roles, but do not establish client owners. Package integrity and derived coverage of the creator remain unknown.

Official host DNS documentation: https://docs.siderolabs.com/talos/v1.14/networking/host-dns . It states the resolver listens on 127.0.0.53:53 using TCP and UDP; DNS forwarding allocates 169.254.116.108. Its enablement can be default or explicitly selected, so no particular source-setting decision is presumed.

Manual checks: compared the following ten input rows with raw/0019-talos-ports.out. Verified listen states at the two DNS addresses, arbitrary local listeners, kubelet health listener, KubePrism listener, established connections and TIME_WAIT. Each remains live socket state; no owner was inferred from a remote endpoint alone.

- talos-d8c29fedf733e0a4a51ba28e
- talos-54afd7caa5900923ae1dfd8c
- talos-555a2e3a32a654473a1432af
- talos-2bfebb9ec925a4d41df41abe
- talos-04dfc8d284fa6b7475781e80
- talos-a78300a1c6acec3a99072b47
- talos-e4281c282fe155a27501bfb8
- talos-6c9033b76edb05447045f278
- talos-c8ba828a7254100ad6de102d
- talos-380f8868bcaa19b810085ca0

## Individual container cases

Rows 211 and 212 were read individually from raw/0020-talos-containers.out and cross-checked against raw/0008-talos-processes.out. They identify RUNNING apid and trustd instances with PIDs, rather than image packages. The containerd shim command lines name these instances. S8.2-5 therefore gives RUNTIME; executable contents remain separately classifiable under S8.2-7/9/22. Containerd's own classification is UNKNOWN because file integrity is unknown.

Validation: 121 assigned input IDs, 121 output IDs, exactly equal with no duplicates. All decisions RUNTIME. Text word limits checked during writing. No stored-object persistence assumptions were introduced.

## Final mechanical verification

Verified 278 input IDs and 278 output IDs: identical sets and counts, each once. All decisions belong to the fifteen allowed words; all sentence identifiers, field limits, field delimiters and raw evidence paths passed validation.
