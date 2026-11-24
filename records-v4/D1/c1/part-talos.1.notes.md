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
