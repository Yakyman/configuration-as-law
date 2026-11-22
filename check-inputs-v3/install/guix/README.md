# GNU Guix System installation input

Release: 1.5.0. x86_64, BIOS, virtio disk, 32 GiB, 4 GiB RAM, two vCPUs. This is the non-desktop check-4 system. No explicit extra packages are requested. `config.scm` starts with base services and packages, ordinary wheel-group user, DHCP, UTC, English locale, BIOS boot, ext4 root, and serial console/getty required by the laboratory transport. The user password is `cal-test`; only its salted hash is stored in the declaration.

Official installation procedure: https://guix.gnu.org/manual/en/html_node/Proceeding-with-the-Installation.html . `install.sh` formats and mounts the empty target, starts cow-store, saves config.scm under the target /etc, and invokes `guix system init`, then sync and poweroff.

`launch.sh` boots the installation image with its extracted kernel/initrd under the first free slot lock. A second read-only ISO contains install.sh and config.scm. `drive-install.py` sends keyboard events to installer tty3 after Ctrl-Alt-F3, presses Enter to log into its root shell, mounts the input ISO, and runs install.sh with output redirected to ttyS0. These steps automate manual installation without an inventory.

The first boot using the generic QEMU CPU hit a Guile segmentation fault in the installer. The recipe now uses `-cpu host`. A keyboard automation attempt omitted dots from a filename; the mapping was corrected before installation started. Guix's installer has no serial login by default, so the installer terminal is driven through the QEMU monitor. This does not change the installed system; the declaration's agetty service supplies its subsequent serial login.

The selected base configuration is an explicit manual-installation choice. The graphical installer's desktop-choice defaults were not selected or examined. No claim of matching a graphical default desktop is made for this non-desktop check-4 machine.

Installation completed and installed the bootloader. The installer does not provide a `poweroff` command; the final recipe uses `herd power-off shepherd`, the documented Shepherd equivalent of halt (https://www.gnu.org/software/shepherd/manual/shepherd.pdf). This command completed a graceful poweroff. The clean backing image was then made read-only.
