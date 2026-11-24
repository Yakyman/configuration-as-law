# Documentation evidence for the changed card 4 reasoning

Consulted 2026-11-23 UTC. Source: [Linux kernel documentation, Ramfs, rootfs and initramfs](https://docs.kernel.org/filesystems/ramfs-rootfs-initramfs.html), section `What is initramfs?`.

> After extracting, the kernel checks to see if rootfs contains a file “init”, and if so it executes it as PID 1.

The `External initramfs images` section also describes extracting an external archive before attempting to run `/init`. The source establishes extraction followed by execution of the extracted program. It does not define the hypothesis's terms code and reads as values, and therefore does not select between the two readings of S8.2-9/23. No experiment is warranted: the mechanism is already documented and the remaining issue is textual.

Inventory evidence is indexed per row in `card4-extent.tsv`; generation evidence remains in `D1/adjudication/parts/l2-other.facts.md` and `D1/in/control/void/actions-logs/actions-logs/package_program.stderr`.
