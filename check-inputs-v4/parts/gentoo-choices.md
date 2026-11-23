Gentoo choices (inputs, not observations)

- Plain amd64 multilib OpenRC stage3: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Stage says “When choosing a stage file, it's important to pick one with profile targets corresponding to the desired system type.” The task selects the plain OpenRC profile rather than a desktop target.
- Source builds without a binary package host: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Base labels the section “Optional: Adding a binary package host”. The task declines this option; the recipe explicitly disables binary package use.
- Distribution kernel built from source: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel says “To build a kernel with Gentoo patches from source, type:” followed by `emerge --ask sys-kernel/gentoo-kernel`. The task selects gentoo-kernel.
- Distribution-kernel initramfs: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel explains that distribution kernels require an initramfs because drivers are built as modules. The recipe selects installkernel with dracut.
- BIOS boot, MBR with an unused 2 MiB reserved partition, ext4 root, 40 GB target disk, an 8 GB swapfile, UTC and en_US.UTF-8 are concrete installation inputs; https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Disks says “Throughout the remainder of the handbook, we will discuss and explain two cases:” and lists UEFI/GPT and BIOS/MBR. It describes ext4 as “a reliable, all-purpose all-platform filesystem”. These are recorded choices, not claimed universal installer defaults.
- Instrument access: user in wheel, lab public key, SSH password authentication disabled, and passwordless sudo for the lab user. These access changes are expressly part of the instrument, not inferred defaults.
- Build capacity: four slots, 16 GB RAM, eight vCPU; MAKEOPTS=-j8. A Debian cloud VM is only an installation environment and is not the resulting Gentoo installation.

The 8 GB swapfile chooses the lower end of the Handbook recommendation for 8–64 GB RAM; swap is an installation input, not a measured property.
