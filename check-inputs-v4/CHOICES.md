# Installation choices and instrument access

Publication cutoff: 2026-11-23T01:19:00Z. These are prepared inputs, not observations or hypothesis outcomes. System-specific records cite the documentation behind installer defaults and explicit choices.

# AlmaLinux installation inputs

Cutoff: 2026-11-23T01:19:00Z. The official release table places 10.3 on 2026-11-16 and has no newer stable major/minor release at the cutoff: https://wiki.almalinux.org/release-notes/ . The announcement is linked in `alma-release.tsv`.

- Select x86_64 and the full DVD image. Official installation guide https://wiki.almalinux.org/documentation/installation-guide.html offers architectures and says: “AlmaLinux has 3 types of ISOs for each supported architecture”. The DVD supplies the installer defaults offline; a minimal image would restrict the available environment. The guide offers BIOS and UEFI without a unique selection: use QEMU BIOS, 40 GB disk, 4 GB RAM, 2 vCPU.
- Preserve the default software selection with `%packages --default`. The primary Kickstart documentation https://pykickstart.readthedocs.io/en/latest/sections.html says: “Install the default environment.” Its following explanation equates this with leaving the interactive package screen unchanged. No package names or optional environments are supplied by this recipe.
- The installation guide requires choosing language and a user account, and describes selectable keyboard and timezone rather than fixing them. Use English (US), US keyboard, UTC, one ordinary account `user` in `wheel`, as the task prescribes. Automatic partitioning delegates the layout to the installer. Root password is locked.
- SSH lab public key, enabled SSH access through the firewall, and passwordless sudo for `user` are instrument access. No guest inventory is performed. The kickstart is the exact input; installer and post-install output are discarded. The firstboot interactive wizard is disabled to allow unattended access.

Expected instrument test, written before execution: the installed VM boots; the supplied SSH key logs in as `user`; an empty script returns zero and `exit 37` returns 37. All guest output goes to `/dev/null`. These are installation and transport tests, not observations of either check.

# Void installation choices

Recorded before installation; cutoff: 2026-11-23T01:19:00Z.

- Official current image: 20250202, x86_64 glibc base live image. The official download page offers base and Xfce images, and glibc and musl variants; the task fixes base/glibc/x86_64. https://voidlinux.org/download/
- Package source: Local, retaining the image's installer-selected packages. https://docs.voidlinux.org/installation/live-images/guide.html describes the Local and Network alternatives. No repository update is performed.
- Partitioning: BIOS, MBR, one ext4 root partition using the 24 GiB virtual disk. The installation guide states: “Void does not provide a preset partition scheme”. This explicitly requires a check choice. Same source, Partition section.
- Keyboard: us; timezone: Etc/UTC; ordinary login and descriptive name: user. The guide requires selecting keyboard, timezone and user details. Its prescribed default login is changed to user as the task requires. The default supplementary group selection includes wheel; the answer file retains that selection. Locale and hostname settings are omitted, preserving installer fallback behavior.
- Root and ordinary-user setup passwords: void-lab-install, limited to this isolated disposable lab. The installer requires passwords; there is no prescribed password value.
- GRUB: install onto /dev/vda, preserving graphical-terminal default. Services checklist is cancelled, preserving its existing selection.
- Instrument access only: a lab SSH public key is installed for user; the sshd service is enabled; a dedicated sudoers entry allows noninteractive root execution. These are explicit instrument additions after the unchanged void-installer completes.
- Unattended interface: a PATH-local dialog shim supplies Install, affirmative installation confirmation, default-preserving services cancellation, no reboot, then Exit. It does not save dialog text. The official program itself is executed unchanged. The recipe uses its configuration interface documented in the public upstream source: https://github.com/void-linux/void-mklive/blob/master/installer.sh .
- Initial transport: blind serial login uses the documented live root password. Bytes received from the console are discarded into /dev/null, never decoded or retained. The public serial setup implementation is https://github.com/void-linux/void-mklive/blob/master/dracut/vmklive/getty-serial.sh . Subsequent lab use is SSH.

Gentoo choices (inputs, not observations)

- Plain amd64 multilib OpenRC stage3: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Stage says “When choosing a stage file, it's important to pick one with profile targets corresponding to the desired system type.” The task selects the plain OpenRC profile rather than a desktop target.
- Source builds without a binary package host: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Base labels the section “Optional: Adding a binary package host”. The task declines this option; the recipe explicitly disables binary package use.
- Distribution kernel built from source: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel says “To build a kernel with Gentoo patches from source, type:” followed by `emerge --ask sys-kernel/gentoo-kernel`. The task selects gentoo-kernel.
- Distribution-kernel initramfs: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel explains that distribution kernels require an initramfs because drivers are built as modules. The recipe selects installkernel with dracut.
- BIOS boot, MBR with an unused 2 MiB reserved partition, ext4 root, 40 GB target disk, an 8 GB swapfile, UTC and en_US.UTF-8 are concrete installation inputs; https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Disks says “Throughout the remainder of the handbook, we will discuss and explain two cases:” and lists UEFI/GPT and BIOS/MBR. It describes ext4 as “a reliable, all-purpose all-platform filesystem”. These are recorded choices, not claimed universal installer defaults.
- Instrument access: user in wheel, lab public key, SSH password authentication disabled, and passwordless sudo for the lab user. These access changes are expressly part of the instrument, not inferred defaults.
- Build capacity: four slots, 16 GB RAM, eight vCPU; MAKEOPTS=-j8. A Debian cloud VM is only an installation environment and is not the resulting Gentoo installation.

The 8 GB swapfile chooses the lower end of the Handbook recommendation for 8–64 GB RAM; swap is an installation input, not a measured property.

## MicroOS

Release input: Snapshot20261121, x86_64 DVD installer. MicroOS is rolling; its official site says: “As rolling release distribution the software is always up-to-date.” Source: https://microos.opensuse.org/ . The official release index lists the selected snapshot on 22 November 2026, before the 23 November 2026 01:19 UTC cutoff (raw/microos/releases.html). No later snapshot appears in that index at retrieval.

System role: the unattended profile is configuration-equivalent to the first interactive role, `micro_os_role`. AutoYaST does not select or inherit that role: its separate `autoinstallation` workflow omits the `system_role` module, and no profile field is invented for it. The first role has no partitioning, software, network, global, or service overrides; its only additional element is the interactive `inst_microos_role` dialog, which the unattended workflow skips. The profile retains the top-level product storage defaults and explicitly supplies the product default patterns. For the interactive role dialog, the installer specification says: “System roles by default preselect the first defined entry”. Source: https://github.com/yast/yast-installation/blob/master/doc/control-file.md . The MicroOS control file lists `micro_os_role` first with order 100, then `container_host_role` with order 200. Source: https://github.com/yast/skelcd-control-MicroOS/blob/10960584093d59fad1b43575f115a8af0868343f/control/control.MicroOS.xml (last applicable commit 2026-09-16T09:12:19Z). The AutoYaST input explicitly transcribes the product’s four default patterns (`microos_base`, `microos_base_zypper`, `microos_defaults`, `hardware`) and optional `32bit` pattern; it retains the default storage proposal, security policy, and network manager. The optional pattern uses the installer’s supported regex form `/^32bit$/`, so it is selected only if available. Recommended packages are disabled as specified by the MicroOS control’s `clone_install_recommended_default=false` and minimalistic software policy. The sole added package, `combustion`, supplies the mandated first-boot instrument access. Upstream AutoYaST does not automatically inherit the interactive installer’s default patterns: https://github.com/yast/yast-packager/blob/master/src/modules/Packages.rb (`patterns_to_install`); regex support: https://github.com/yast/yast-autoinstallation/blob/master/src/modules/AutoinstSoftware.rb (`Import`).

First-boot mechanism: choose Combustion with QEMU fw_cfg. There is no single required mechanism: the official Combustion documentation says “There are multiple ways to provide the configuration.” Source: https://github.com/openSUSE/combustion/blob/master/README.md . That same document describes QEMU's `opt/org.opensuse.combustion/script` blob, user creation, SSH keys, and enabling SSH. The ordinary account `user`, lab public key, and passwordless sudo are instrument access, not workload inputs. The account has no usable password. The first-boot preparation removes the installation-time machine-id and regenerates the initramfs without host-only filtering, so documented first-boot detection and the Combustion module apply. This preparation is explicitly part of the access recipe.

Hardware/instrument choices: 4 GB RAM, 2 vCPU, 40 GB blank virtio disk, UEFI firmware, NAT with a loopback-only forwarded SSH port. UEFI permits the installer's preferred systemd-boot choice. AutoYaST uses automatic partitioning and the explicitly transcribed product software defaults; its documentation says “AutoYaST can come up with a sensible partitioning layout without any user indication.” Source: https://doc.opensuse.org/projects/autoyast/index.html . English/US keyboard, UTC product default, the default noninteractive license behavior (`confirm_base_product_license=false`), no second stage, and reboot are automation choices. Root password login is locked. These choices are fixed before any check observation.

## Talos Linux

A single control-plane node is the task's choice. Official guide:
https://docs.siderolabs.com/talos/v1.14/getting-started/getting-started —
“Boot additional machines as worker nodes (this is optional).”
The guide has the operator specify the cluster endpoint and install disk;
there is no hardware-independent automatic choice. The recipe fixes the endpoint
from the defined user network and `/dev/vda` from its QEMU device definition.
The minimal configuration is generated by the verified release client with
comments/examples omitted; defaults are otherwise retained, apart from the
instrument's loopback certificate SAN. Talos authentication uses its client
certificate because the system has no SSH shell.

## NixOS and GNU Guix System

The task expressly retains the previous installation recipes when releases match.
Both match: NixOS 26.05.14979.94c3211b0ee8 and Guix 1.5.0. Copies of their
previous verified images and clean installations are used. Their original
host-authored declarations are retained under `install/nixos/` and `install/guix/`.
Access declarations add the laboratory key, SSH and passwordless administrative
execution; these additions belong to the instrument.

NixOS official manual, https://nixos.org/manual/nixos/stable/:
“The minimal images will boot to a command line.” Manual installation requires
the supplied declaration. No desktop is chosen in the preserved recipe.

Guix manual source, https://codeberg.org/guix/guix/raw/tag/v1.5.0/doc/guix.texi,
section `operating-system` Reference, describes `sudoers-file`; OpenSSH service
reference describes `authorized-keys`. The preserved manual declaration supplies
the explicit base-services choice, rather than asserting a graphical installer default.

# Guix instrument access

The release and original clean installation are reused as explicitly requested.
The preserved base-system declaration is the exact prior input, not an inferred
inventory. Only access declarations are added in `C1/install/guix/config.scm`.

Primary documentation: GNU Guix manual, SSH Services and operating-system
reference, https://guix.gnu.org/manual/en/html_node/SSH-Services.html and
https://guix.gnu.org/manual/en/html_node/operating_002dsystem-Reference.html ;
saved source `C1/raw/guix/manual.texi`.

- OpenSSH `authorized-keys` has an empty-list default: “This is the list of authorized keys.” The declared file-like public key authorizes the lab user.
- `sudoers-file`: “The contents of the /etc/sudoers file as a file-like object”. The declaration supplies a passwordless wheel rule for the instrument.

These are explicit instrument-access changes, not claims that the installer has
no default. Initial serial access exists in the previous recipe; it is used
only to apply the known declaration. The intended final instrument uses SSH; its preparation did not complete.

Host-only declaration review: the tagged 1.5.0 `(gnu)` composite module includes
`(guix gexp)` in its publicly re-exported module interfaces. Thus the existing
`(use-modules (gnu))` import supplies `plain-file`; no additional import is
required. Evidence: `C1/raw/guix/gnu-module-excerpt.scm`, source
https://git.savannah.gnu.org/cgit/guix.git/plain/gnu.scm?h=v1.5.0 .

Recovery-only inputs are recorded in `install/guix/README.md`: a Debian helper,
the known original partition target, temporary helper CA certificates, and the
official `https://ci.guix.gnu.org` substitute source. These do not replace the
original installed-system declaration. All failed recovery candidates were
removed after the final timeout; no SSH-enabled Guix base is registered.

## Auxiliary systems outside the checks

Debian and debian-server use the same verified stable cloud image and NoCloud lab-key seed; the latter receives 8 GB, 4 vCPU and a 40 GB disk. Fedora and Mint retain the previous immutable clean installations as direct backing images and add lab-key SSH/sudo in a new read-only overlay. Their source-location correction and access recipes are documented under `install/` and `parts/auxiliary-notes.md`.

## KIT2: active late-system preparation choices

Recorded 2026-11-23 UTC. These choices supersede the unsuccessful access and
installation plans above for the two late systems; the earlier records remain
as their history. No check observation is made during this preparation.

### MicroOS: same-release preconfigured virtual-machine image

After the corrected unattended DVD installation timed out with status 124
(`raw/microos/status.log`), use the explicitly authorized ready-made plain
KVM/XEN image `openSUSE-MicroOS.x86_64-16.0.0-kvm-and-xen-Snapshot20261121.qcow2`.
The release remains Snapshot20261121. This is a recorded change of installation
input, not a claim of equivalence to a completed DVD installation.

The official download page, https://get.opensuse.org/microos/, offers “KVM and
XEN image” separately from “KVM and XEN Container Host”; choose the plain image.
Its deployment guidance says: “Both preconfigured and self-installed images
are intended to be used with Combustion”. Saved passage:
`raw/microos-kit2/download-page.html`. The image, checksum and detached signature
are listed in `raw/microos-kit2/appliances.html`, source
https://download.opensuse.org/tumbleweed/appliances/ .

The first boot supplies ordinary user `user`, the lab key and administrative
instrument access through Combustion. Its official README states: “There are
multiple ways to provide the configuration.” Select its documented QEMU fw_cfg
blob `opt/org.opensuse.combustion/script`. Source:
https://github.com/openSUSE/combustion/blob/master/README.md; saved source
`raw/microos-kit2/combustion-readme.md`. Exact access and hardware inputs are in
`install/microos/kit2/` and `parts/microos-kit2.md`. No packages are added by
this access recipe.

The first ready-image boot did not establish SSH access. The next first-boot
input omits the optional `combustion: network` marker: all configuration is
local, delivered by fw_cfg. The same Combustion README explains that this
marker requests networking before the script runs; the recipe does not need
that extra dependency. This change does not establish the cause of the failed
boot/login attempt. A separate serial channel retains only predetermined
installation-command exit statuses, with fixed stage labels and a token;
ordinary console output is discarded. Attempt history is retained in
`parts/microos-kit2.md`.

The diagnostic first-boot attempt returned `useradd` status 6. The saved
upstream manual maps that status to a missing specified group
(`raw/microos-kit2/useradd-man.xml`). The corrected access recipe creates
`user` with its own primary group and omits the unnecessary supplementary
`wheel` request. MicroOS has no task requirement for that group; the explicit
per-user sudo rule supplies administrative instrument access. No guest group
lookup was performed. The correction was first applied in
`install/microos/kit2/attempt-3/`. That attempt completed the access script
with status 0 but never established SSH login (timeout 124). The next immutable
input, `install/microos/kit2/attempt-4/`, restores the documented network marker
while retaining the corrected user creation. This is a different input
combination, not a claim that networking caused the preceding failure.

Further primary-document review found a missing initialization step. The
Combustion user-creation example in the official guide places `mount /home`
before `useradd -m EXAMPLE_USER`; the published image definition declares a
separate home subvolume. Source:
https://documentation.suse.com/sle-micro/6.2/html/Micro-deployment-selfinstall-images/index.html
(section Creating new users), saved `raw/microos-kit2/combustion-users.html`.
The immutable `install/microos/kit2/attempt-5/` mounts that subvolume before
creating the user and key, then unmounts it after labeling. The preceding
attempt was stopped for this documented input correction, not reported as a
timeout. No guest mount state was queried, and no prior runtime cause is
asserted.

The mounted-home recipe passed standalone SSH and privileged exit 37, but
its first shared-runner clone failed boot/login with status 1. Its preparation
used a different virtual NIC MAC and only one NIC. The next immutable input
`install/microos/kit2/attempt-6/` retains the access script and matches the
runner hardware: primary MAC `52:54:00:ca:10:01` on its default user network
and secondary MAC `52:54:00:ca:10:02` on `10.0.3.0/24`, in the same order.
This removes a host-authored input mismatch without querying guest network
state or claiming that the mismatch explains the failed clone. The failed
clone and superseded base were removed. Attempt 6 passed fresh shared-runner
boot/login and ordinary/privileged exit-status checks; it is the active selected
MicroOS recipe.

### Guix: unchanged clean installation and original serial access

Guix 1.5.0 is unchanged. Reuse the byte-identical copied clean installation and
its original declaration, with the existing serial user/password access.
The earlier SSH declaration applications timed out with status 124
(`raw/guix/recovery-attempt6.txt`, `raw/guix/recovery-attempt7.txt`); they are
not retried or represented as successful. No installed lab key is claimed.
The task expressly permits the original serial transport in this situation.

The Guix manual describes `agetty-service-type`: “Type of the service that runs
agetty, which implements virtual and serial console log-in.” Source:
https://guix.gnu.org/manual/en/html_node/Base-Services.html; saved source
`raw/guix/manual.texi`. The preserved declaration explicitly supplies this
serial login. The runner restores the preceding recipe's passive initial login,
without changing the installed system. Exact inputs: `install/guix/KIT2.md`,
`original-config.scm`, `kit2-base.json`, and `kit2-passive.patch`.
