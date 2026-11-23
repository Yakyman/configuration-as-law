"""c2 classification of D1 part flatcar. Usage: classify_flatcar.py <input.tsv> <filesystem.out> <out.tsv> <members.tsv>
Rules are documented in D1/c2/part-flatcar.notes.md (rule ids R..)."""
import csv, json, re, sys

csv.field_size_limit(10**9)
inp, fsout, outp, memp = sys.argv[1:5]
rows = list(csv.DictReader(open(inp, encoding='utf-8'), delimiter='\t'))

D_SYSFB = 'doc:https://github.com/torvalds/linux/blob/master/drivers/firmware/sysfb.c'
D_GRUBI = 'doc:https://github.com/flatcar/scripts/blob/main/build_library/grub_install.sh'
D_GRUBC = 'doc:https://github.com/flatcar/scripts/blob/main/build_library/grub.cfg'
D_GRUBL = 'doc:https://github.com/rhboot/grub2/tree/fedora-40/grub-core/normal'
D_KEEP = 'doc:https://devmanual.gentoo.org/function-reference/install-functions/'
D_GEN = 'doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.generator.html'
D_VARL = 'doc:https://www.freedesktop.org/software/systemd/man/latest/varlinkctl.html'
D_USERDB = 'doc:https://systemd.io/USER_GROUP_API/'
D_UDEV = 'doc:https://www.freedesktop.org/software/systemd/man/latest/udev.html'
D_POLKIT = 'doc:https://github.com/polkit-org/polkit/blob/main/src/polkitbackend/polkitbackendinteractiveauthority.c'
D_SSHD = 'doc:https://man.openbsd.org/sshd_config'
D_SUDO = 'doc:https://www.sudo.ws/docs/man/sudoers.man/'
D_UNIT = 'doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html'
D_IGN = 'doc:https://github.com/coreos/ignition/blob/main/docs/release-notes.md'
D_SHADOW = 'doc:https://man7.org/linux/man-pages/man5/shadow.5.html'
D_BLKID = 'doc:https://man7.org/linux/man-pages/man8/blkid.8.html'
D_BASH = 'doc:https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html'
D_EXEC = 'doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html'

def T(dec, sent, what, basis, reason):
    return (dec, sent, what, basis, reason)

# ---------- L2 member rules: (regex on path, optional type filter, result) ----------
RM = 'S2.2-1,S2.2-2'
NOTHING = 'removal changes nothing the computer does or can do, so the removal test is negative'
CONTENT_UNKNOWN = ('UNKNOWN', 'S3-1,S3-2')

MEMBER_RULES = [
    # --- /boot ---
    (r'^/boot/EFI/boot/[^/]+\.efi$', None, T('NOT', RM, 'UEFI loader (shim, GRUB, MokManager); runs only on UEFI firmware', D_SYSFB,
        'machine booted via BIOS (kernel registered vga-framebuffer, a VGA text-mode boot); the UEFI loader never runs here, so removal changes nothing')),
    (r'^/boot/boot/grub/menu\.lst$', None, T('NOT', RM, 'boot menu for Xen PV pvgrub', D_GRUBI,
        'used only when booted as a Xen PV guest; this machine is a QEMU/KVM guest (virtio, fw_cfg drivers), so removal changes nothing')),
    (r'^/boot/xen/pvboot-x86_64\.elf$', None, T('NOT', RM, 'GRUB image for Xen PV boot', D_GRUBI,
        'executed only when booted as a Xen PV guest; this machine is a QEMU/KVM guest (virtio, fw_cfg drivers), so removal changes nothing')),
    (r'^/boot/flatcar/grub/x86_64-xen/', None, T('NOT', RM, 'GRUB module or list for the Xen PV platform', D_GRUBI,
        'read or executed only by the Xen PV GRUB; this machine is a QEMU/KVM guest, so removal changes nothing')),
    (r'^/boot/flatcar/vmlinuz-a$', None, T('MUST', 'S2.2-2,S2.2-9', 'Linux kernel image booted by GRUB from USR-A', D_GRUBC,
        'the kernel is a program that runs on the computer; without it the machine cannot boot this /usr')),
    (r'^/boot/flatcar/grub/grub\.cfg\.tar$', None, T('NOT', RM, 'build input: grub.cfg packed into the GRUB core image memdisk', D_GRUBI,
        'grub-mkimage embeds it as memdisk at image build; GRUB reads the embedded copy at boot, so removing this file changes nothing')),
    (r'^/boot/flatcar/grub/[^/]+/load\.cfg$', None, T('NOT', RM, 'build input: early config embedded into the GRUB core image', D_GRUBI,
        'passed to grub-mkimage --config at image build; GRUB uses the embedded copy, so removing this file changes nothing')),
    (r'^/boot/flatcar/grub/i386-pc/(core\.img|boot\.img|mbr\.bin)$', None, T('NOT', RM, 'copy of BIOS boot code already written to MBR and BIOS-BOOT partition', D_GRUBI,
        'grub-bios-setup wrote it to the MBR and BIOS-BOOT partition; firmware runs those copies, so removing this file changes nothing')),
    (r'^/boot/flatcar/grub/i386-pc/[^/]+\.mod$', None, T('MUST', 'S2.2-2,S2.2-10', 'GRUB module loaded and executed by BIOS GRUB from its prefix', D_GRUBC,
        'BIOS GRUB (this boot) executes it with full machine rights (insmod/autoload, prefix /flatcar/grub); without it its function in GRUB becomes impossible')),
    (r'^/boot/flatcar/grub/i386-pc/(command|fs|crypto|terminal|parttool)\.lst$', None, T('HOLE', 'S2.2-2,S2.2-7,S2.2-13', 'autoload list GRUB reads at boot to find modules for commands', D_GRUBL,
        'read as values by GRUB only (setting); removal breaks autoload, e.g. of linux, so booting stops; text lacks whether such a setting is in force only inside one program')),
    (r'^/boot/flatcar/grub/i386-pc/(moddep|partmap|video|fdt)\.lst$', None, T('NOT', RM, 'list used only by GRUB build and install tools', D_GRUBL,
        'no runtime GRUB code reads it (only grub-core build files reference it), so removal changes nothing at boot')),
    # --- /etc: accounts and access ---
    (r'^/etc/(passwd|group)$', None, T('MUST', 'S2.2-15', 'local account and group database', D_SHADOW,
        'holds the accounts of the machine and group memberships granting rights, including sudo group; accounts must be recorded')),
    (r'^/etc/(shadow|gshadow)$', None, T('MUST', 'S2.2-15', 'password hashes and lock state per account', D_SHADOW,
        'hash need not be recorded, but the lock/empty field is the rule whether password login is allowed for each account, which must be')),
    (r'^/etc/(passwd|group|shadow|gshadow|subuid|subgid)-$', None, T('NOT', RM, 'backup copy written by shadow tools before an edit', D_SHADOW,
        'no program reads the backup in normal operation; ' + NOTHING)),
    (r'^/etc/(subuid|subgid)$', None, T(*CONTENT_UNKNOWN, 'subordinate id ranges for user namespaces', 'none',
        'contents not in the inventory; whether any account has ranges whose removal makes rootless containers impossible cannot be established')),
    (r'^/etc/\.pwd\.lock$', None, T('NOT', RM, 'lock file used by shadow tools during edits', 'evidence', 'lock taken only during an edit; ' + NOTHING)),
    (r'^/etc/ssh/sshd_config$', None, T('MUST', 'S2.2-2,S2.2-15', 'main sshd configuration, includes sshd_config.d', D_SSHD,
        'sshd, started per connection here, exits without its config file, so SSH login stops; it also holds the password-login rule')),
    (r'^/etc/ssh/sshd_config\.d/', None, T(*CONTENT_UNKNOWN, 'drop-in sshd settings (Flatcar, Gentoo)', 'none',
        'contents not in the inventory; which sshd values (password-login rule, PAM) each file sets cannot be established')),
    (r'^/etc/ssh/ssh_host_[a-z0-9_]+_key$', None, T('HOLE', 'S2.2-2,S2.2-7,S2.2-15', 'private host key sshd uses to prove the server identity', D_SSHD,
        'not a key to log in to an account (S2.2-15); read only by sshd (S2.2-7) yet removal stops sshd offering that key; no sentence decides')),
    (r'^/etc/ssh/ssh_host_[a-z0-9_]+_key\.pub$', None, T(*CONTENT_UNKNOWN, 'public half of a host key', 'none',
        'sshd derives the public key itself; which other programs here read the .pub file is not established')),
    (r'^/etc/ssh/moduli$', None, T('NOT', 'S2.2-7', 'Diffie-Hellman groups for sshd group-exchange key exchange', D_SSHD,
        'a setting read only by sshd for its own key exchange; S2.2-7 exempts settings in force only inside one program')),
    (r'^/etc/ssh/(ssh_config|ssh_config\.d/.*|ssh_revoked_hosts)$', None, T('NOT', 'S2.2-7', 'settings of the ssh client program', 'doc:https://man.openbsd.org/ssh_config',
        'settings read only by the ssh client and in force only inside it; S2.2-7 exempts them')),
    (r'^/home/user/\.ssh/authorized_keys$', None, T('MUST', 'S2.2-15', 'public keys allowed to log in as user', 'raw:raw/123-login-keys-0.out',
        'keys used to log in to an account must be recorded')),
    (r'^/home/user/\.ssh/authorized_keys\.d/ignition$', None, T('MUST', 'S2.2-15', 'login-key fragment merged into authorized_keys by update-ssh-keys', 'doc:https://www.flatcar.org/docs/latest/setup/customization/adding-users/',
        'holds the key used to log in to the account; merged into authorized_keys, so it is the source of a login key')),
    (r'^/home/user/(\.authorized_keys\.d\.lock|\.ssh/\.authorized_keys\.d\.old)$', None, T('NOT', RM, 'lock file and backup directory of update-ssh-keys', 'evidence', NOTHING)),
    # --- shell code ---
    (r'^/home/user/\.(bashrc|bash_profile|bash_logout)$', None, T('MUST', 'S2.2-10', 'bash startup file of user, executed by bash', D_BASH,
        'shell startup files are code the shell runs with its own rights')),
    (r'^/etc/bash/(bashrc|bash_logout|bashrc\.d/.*)$', None, T('MUST', 'S2.2-10', 'system-wide bash startup code (Gentoo layout)', D_BASH,
        'sourced by bash for every interactive shell; shell startup files are code executed with the shell rights')),
    (r'^/etc/profile\.d/[^/]+\.sh$', None, T('MUST', 'S2.2-10', 'shell code sourced by /etc/profile for login shells', D_BASH,
        'sourced by bash login shells; shell startup files are code executed with the shell rights')),
    (r'^/etc/profile\.d/gawk\.csh$', None, T('NOT', RM, 'csh startup code for gawk', 'raw:raw/105-filesystem.out',
        'no csh or tcsh exists on the machine, so nothing executes it; ' + NOTHING)),
    (r'^/etc/X11/xinit/xinitrc\.d/50-systemd-user\.sh$', None, T('NOT', RM, 'xinit session script importing environment into systemd user', 'raw:raw/105-filesystem.out',
        'no xinit, startx or X server exists on the machine, so nothing executes it; ' + NOTHING)),
    (r'^/etc/skel/', None, T('HOLE', 'S2.2-2,S2.2-7,S2.2-10', 'template copied by useradd into new home directories', 'doc:https://man7.org/linux/man-pages/man8/useradd.8.html',
        'not executed in place, only copied by useradd (S2.2-7 setting); removal stops useradd placing startup code in new homes (S2.2-2); no sentence decides')),
    (r'^/etc/vim$', None, T('MUST', 'S2.2-10', 'holds vimrc link: system vim startup in Vim script', 'raw:raw/105-filesystem.out',
        'an editor configuration written in the editor language is code that must be recorded')),
    # --- placeholders, stamps, records ---
    (r'/\.keep_[^/]+$', None, T('NOT', RM, 'empty Gentoo placeholder keeping a directory in the package', D_KEEP,
        'an empty file no program reads as configuration; ' + NOTHING)),
    (r'^/(etc|var)/\.updated$', None, T('NOT', 'S2.2-6', 'timestamp of last /usr update for ConditionNeedsUpdate', D_UNIT,
        'a record of when update tasks last ran; records of the past need not be recorded')),
    (r'^/etc/\.ignition-result\.json$', None, T('NOT', 'S2.2-6', 'report of the Ignition first-boot run', D_IGN,
        'a report of what happened at provisioning; records of the past need not be recorded')),
    (r'^/etc/[^/]*\.example$|^/etc/.*/[^/]*\.example$|^/etc/sssd/sssd-example\.conf$|^/etc/openldap/ldap\.conf\.default$|^/etc/sudoers\.dist$', None,
        T('NOT', RM, 'example or distribution copy of a configuration file', 'evidence', 'programs read the real file name, not the example copy; ' + NOTHING)),
    (r'^/etc/machine-id$', None, T('HOLE', 'S2.2-1,S2.2-2', 'unique machine identifier used by systemd, journald, DHCP', 'doc:https://www.freedesktop.org/software/systemd/man/latest/machine-id.html',
        'removal makes systemd generate a new id at boot; text lacks whether a value replaced by a different one means the computer stops doing something')),
    (r'^/etc/resolv\.conf$|^/run/systemd/resolve/resolv\.conf$', None, T('MUST', RM, 'resolver configuration naming the DNS servers, via symlink into /run', 'doc:https://man7.org/linux/man-pages/man5/resolv.conf.5.html',
        'without it the libc resolver falls back to a name server on the local machine (127.0.0.1), where none listens here, so DNS lookups fail')),
    (r'^/etc/(coreos|issue|motd|mtab)$', 'l', T('UNKNOWN', 'S3-1,S3-2', 'compatibility symlink into /run or /etc/flatcar', 'raw:raw/105-filesystem.out',
        'which programs on this machine open the path through this link is not established')),
    (r'^/etc/xdg/systemd/user$', 'l', T('UNKNOWN', 'S3-1,S3-2', 'XDG path symlink to /etc/systemd/user', 'raw:raw/105-filesystem.out',
        'which program reads units through this path is not established')),
    (r'^/etc/extensions/oem-qemu\.raw$', None, T('MUST', 'S2.2-2,S2.2-9', 'activates the OEM QEMU system extension image (sysext)', 'doc:https://www.flatcar.org/docs/latest/provisioning/sysext/',
        'systemd-sysext merges the image (programs for this platform, e.g. qemu-ga) into /usr; removal makes them unavailable')),
    (r'^/etc/extension-release\.d/', None, T(*CONTENT_UNKNOWN, 'release file of the default confext', 'none', 'contents and readers not established')),
    (r'^/etc/\.systemd-confext/', None, T(*CONTENT_UNKNOWN, 'state of systemd-confext merge of /etc', 'none', 'what systemd-confext reads from these files is not documented')),
    (r'^/etc/ssl/certs$', None, T('MUST', 'S2.2-1,S2.2-2', 'CA certificate links used for TLS verification', 'raw:raw/105-filesystem.out',
        'removing the trust store makes TLS verification, e.g. update downloads, impossible')),
    (r'^/etc/cifs-utils$', None, T('MUST', 'S2.2-10', 'holds idmap-plugin link: shared object loaded by cifs.idmap', 'raw:raw/105-filesystem.out',
        'a plugin library is code that cifs.idmap executes with its own rights')),
    (r'^/etc/init\.d$', None, T(*CONTENT_UNKNOWN, 'holds link to Gentoo functions.sh', 'raw:raw/105-filesystem.out', 'which scripts on this machine source it is not established')),
    (r'^/etc/systemd/system/timers\.target\.wants$', None, T('MUST', 'S2.2-2', 'enables google-oslogin-cache.timer', 'raw:raw/105-filesystem.out',
        'the link enables a timer; removal stops it being started; enabled services must be recorded')),
    (r'^/etc/ld\.so\.cache$', None, T(*CONTENT_UNKNOWN, 'dynamic linker library search cache', 'doc:https://man7.org/linux/man-pages/man8/ldconfig.8.html',
        'whether libraries outside default paths exist (removal would then break programs, not only slow them) is not established')),
    (r'^/etc/udev/hwdb\.bin$', None, T(*CONTENT_UNKNOWN, 'compiled udev hardware database', 'doc:https://www.freedesktop.org/software/systemd/man/latest/hwdb.html',
        'whether a copy also exists under /usr/lib/udev, so removal only falls back, is not established')),
    (r'^/etc/(whois\.conf|xattr\.conf|mke2fs\.conf|e2scrub\.conf|kexec\.conf|nvme/discovery\.conf|isns/isnsadm\.conf|warnquota\.conf|quotagrpadmins|quotatab|ethertypes|default/mdadm|netconfig|bindresvport\.blacklist|azure-ephemeral-disk-setup\.conf|dracut\.conf)$', None,
        T(*CONTENT_UNKNOWN, 'configuration file read as values by one program', 'none',
          'contents not in the inventory; whether it sets values that differ from defaults and act beyond the program cannot be established')),
]
# generic /etc configuration: unknown contents
GENERIC_ETC = T(*CONTENT_UNKNOWN, 'configuration file read as values by a system program', 'none',
                'contents not in the inventory; removal effect depends on the values it sets, which cannot be established')

RUN_RULES = [
    (r'^/run/systemd/inaccessible/|^/run/user/1000/systemd/inaccessible/', None, T('MUST', RM, 'inaccessible nodes systemd mounts over paths for sandboxing', D_EXEC,
        'units using InaccessiblePaths or ProtectHome need them; removal makes starting such units impossible')),
    (r'^/run/varlink/registry/|^/run/user/1000/varlink/registry/', None, T('MUST', RM, 'registry entry point for a local Varlink service', D_VARL,
        'clients find and reach the service by interface name here; removal makes that impossible')),
    (r'^/run/systemd/userdb/', None, T('MUST', RM, 'user database service entry point', D_USERDB,
        'userdb clients (userdbctl, sshd AuthorizedKeysCommand) query user records through it; removal makes those lookups impossible')),
    (r'^/run/systemd/generator(\.late)?/', None, T('NOT', RM, 'unit or drop-in written by a generator', D_GEN,
        'generators delete and rewrite their output at every boot and manager reload; ' + NOTHING)),
    (r'^/run/systemd/units/invocation:', None, T(*CONTENT_UNKNOWN, 'invocation id of a running unit', 'none', 'which programs read these links and what stops without them is not documented')),
    (r'^/run/user/1000/systemd/units/invocation:', None, T(*CONTENT_UNKNOWN, 'invocation id of a running user unit', 'none', 'which programs read these links and what stops without them is not documented')),
    (r'^/run/udev/data/', None, T('MUST', RM, 'udev database of one device properties', D_UDEV,
        'libudev clients (systemd, networkd, logind) read device properties here; removal makes them unavailable until the next event')),
    (r'^/run/udev/tags/', None, T('MUST', RM, 'udev tag index entry for one device', D_UDEV,
        'enumeration by tag (systemd devices, logind seats, power switches) uses it; removal makes the device not found by tag')),
    (r'^/run/udev/links/', None, T(*CONTENT_UNKNOWN, 'udev bookkeeping of which device claims a /dev symlink', 'none', 'the effect of removing it on the /dev links is not documented')),
    (r'^/run/udev/watch/', None, T(*CONTENT_UNKNOWN, 'udev bookkeeping of inotify watches on devices', 'none', 'the effect of removing it is not documented')),
    (r'^/run/udev/(links\.lock|rules\.d)$', None, T('NOT', RM, 'lock directory and empty runtime rules directory of udev', 'raw:raw/105-filesystem.out', 'empty; ' + NOTHING)),
    (r'^/run/(initramfs/log/(btmp|lastlog|wtmp)|utmp)$', None, T('NOT', 'S2.2-6', 'login accounting records', 'doc:https://man7.org/linux/man-pages/man5/utmp.5.html',
        'records of logins; records of the past need not be recorded')),
    (r'^/run/blkid/blkid\.tab$', None, T('NOT', 'S2.2-5', 'libblkid cache of probed block devices', D_BLKID, 'a cache: without it blkid probes devices again, only slower')),
    (r'^/run/(issue|issue\.d/.*|flatcar/motd)$', None, T('NOT', 'S2.2-4', 'generated login banner text', 'doc:https://man7.org/linux/man-pages/man8/agetty.8.html',
        'banner text shown at login; after removal the computer does the same, only the text is unavailable')),
    (r'^/run/(docker\.pid|fsck/vda\.lock|xtables\.lock)$', None, T('NOT', RM, 'pid or lock file', 'evidence', 'pid and lock files are recreated when needed; ' + NOTHING)),
    (r'^/run/systemd/journal/streams/', None, T(*CONTENT_UNKNOWN, 'journald state of one stdout stream', 'none', 'used by journald to restore streams after restart; effect of removal not documented')),
]
GENERIC_SOCKET = T('MUST', RM, 'listening socket of a running service', 'raw:raw/105-filesystem.out',
                   'clients connect to the service through it; removal makes connecting impossible')
GENERIC_RUN = T(*CONTENT_UNKNOWN, 'runtime state file or directory of a running program', 'none',
                'which programs read it and what stops if it is removed is not established')
VAR_RULES = [
    (r'^/var/log/(btmp|faillog|lastlog|wtmp)$|^/var/log/journal/.*\.journal$', None, T('NOT', 'S2.2-6', 'log or login accounting record', 'evidence', 'records of the past need not be recorded')),
    (r'^/var/lib/systemd/timers/stamp-', None, T('NOT', 'S2.2-6', 'last-trigger time of a persistent timer', 'doc:https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html',
        'records when the timer last ran; records of the past need not be recorded')),
    (r'^/var/cache/ldconfig/aux-cache$', None, T('NOT', 'S2.2-5', 'ldconfig auxiliary cache', 'doc:https://man7.org/linux/man-pages/man8/ldconfig.8.html', 'a cache: without it ldconfig rescans, only slower')),
    (r'^/var/lib/systemd/catalog/database$', None, T('NOT', 'S2.2-5', 'compiled journal message catalog', 'doc:https://www.freedesktop.org/software/systemd/man/latest/journalctl.html',
        'rebuilt from catalog sources by journalctl --update-catalog; behaves as a cache for message explanations')),
    (r'^/var/lib/systemd/random-seed$', None, T(*CONTENT_UNKNOWN, 'saved entropy seed for the kernel RNG', 'doc:https://www.freedesktop.org/software/systemd/man/latest/systemd-random-seed.service.html',
        'whether removal changes anything beyond initial entropy crediting is not established')),
    (r'^/var/lib/systemd/timesync/clock$', None, T(*CONTENT_UNKNOWN, 'timestamp timesyncd uses as minimum clock at boot', 'none', 'effect of removal on this machine not established')),
    (r'^/var/lib/(containerd/io\.containerd\.metadata\.v1\.bolt/meta\.db|docker/.*\.db|docker/image/overlay2/repositories\.json|docker/engine-id|nfs/(etab|rmtab|xtab|state)|tpm/system\.data)$', None,
        T(*CONTENT_UNKNOWN, 'state database of a container engine, NFS or TPM daemon', 'none',
          'contents not in the inventory; whether it holds images, networks or exports whose loss stops something is not established')),
    (r'^/var/lib/docker/volumes/backingFsBlockDev$', None, T(*CONTENT_UNKNOWN, 'device node docker uses for volume quota', 'none', 'effect of removal not documented')),
    (r'^/var/(lock|run)$', 'l', T('UNKNOWN', 'S3-1,S3-2', 'compatibility symlink to /run', 'raw:raw/105-filesystem.out', 'which programs use the legacy path here is not established')),
    (r'^/var/lib/dbus/machine-id$', 'l', T('UNKNOWN', 'S3-1,S3-2', 'legacy D-Bus machine-id symlink', 'raw:raw/105-filesystem.out', 'which programs read the legacy path here is not established')),
    (r'^/var/lib/extensions\.mutable/etc$', 'l', T('UNKNOWN', 'S3-1,S3-2', 'mutable-mode link for confext /etc', 'none', 'role in systemd-confext mutable mode on this machine not established')),
    (r'^/var/empty$', None, T('MUST', RM, 'sshd privilege separation directory, home of account sshd', D_SSHD,
        'sshd refuses to start without its privilege separation directory, making SSH login impossible')),
]
EMPTY_DIR = T(*CONTENT_UNKNOWN, 'empty directory', 'raw:raw/105-filesystem.out',
              'holds nothing; whether some program requires it to exist cannot be established from the inventory')
OEM_RULES = [
    (r'^/oem/grub\.cfg$', None, T('MUST', 'S2.2-10,S2.2-13', 'OEM GRUB script sourced by the main grub.cfg', D_GRUBC,
        'GRUB executes it as script code with full machine rights (source command); a file executed as code counts as code')),
    (r'^/oem/oem-release$', None, T(*CONTENT_UNKNOWN, 'OEM identification file', 'none', 'which programs read it and with what effect is not established')),
    (r'^/oem/sysext/oem-qemu-4757\.2\.3\.raw$', None, T('MUST', 'S2.2-9', 'OEM system extension image with platform programs', 'doc:https://www.flatcar.org/docs/latest/provisioning/sysext/',
        'holds programs merged into /usr (e.g. qemu-ga); programs that run must be recorded')),
    (r'^/oem/sysext/active-oem-qemu$', None, T(*CONTENT_UNKNOWN, 'marker of the active OEM sysext', 'none', 'which program reads it is not documented')),
]

def match(rules, p, t):
    for rx, tf, res in rules:
        if tf and tf != t:
            continue
        if re.search(rx, p):
            return res
    return None

# filesystem listing
fs = open(fsout, 'rb').read().split(b'\0')
ftype = {}
nkids = {}
for i in range(0, len(fs) - 5, 6):
    p = fs[i].decode('utf-8', 'replace')
    ftype[p] = fs[i + 1].decode()
    par = p.rsplit('/', 1)[0] or '/'
    nkids[par] = nkids.get(par, 0) + 1
# group ids that own a file with group read or write permission (from the same listing)
gid_files = {}
for i in range(0, len(fs) - 5, 6):
    mode, g = fs[i + 2].decode(), fs[i + 4].decode()
    if mode and len(mode) >= 2 and int(mode[-2]) & 6:
        gid_files.setdefault(g, fs[i].decode('utf-8', 'replace'))
# login accounts (shell is not nologin), excluding root
LOGIN = set()
for r0 in rows:
    if r0['kind'] == 'L1:account':
        f0 = json.loads(r0['members'])[0].split(':')
        if f0[0] != 'root' and not f0[6].endswith('nologin'):
            LOGIN.add(f0[0])

def decide_member(p):
    t = ftype.get(p, '?')
    for rules in (MEMBER_RULES, RUN_RULES, VAR_RULES, OEM_RULES):
        r = match(rules, p, t)
        if r:
            return r
    if t == 's':
        return GENERIC_SOCKET
    if t == 'd' and nkids.get(p, 0) == 0:
        return EMPTY_DIR
    if p.startswith('/etc/'):
        return GENERIC_ETC
    if p.startswith('/run/'):
        return GENERIC_RUN
    return T(*CONTENT_UNKNOWN, 'stored object outside packages', 'none', 'what it does is not established from the inventory')

# ---------- L1 rules ----------
SSH_MUST = {
 'port': 'port open for connection', 'listenaddress': 'addresses where the SSH port is open', 'AddressFamily': 'address families of the open SSH port',
 'PasswordAuthentication': 'rule whether password login is allowed', 'KbdInteractiveAuthentication': 'keyboard-interactive (PAM password) login rule',
 'PermitEmptyPasswords': 'rule whether empty-password login is allowed', 'UsePAM': 'PAM authentication including passwords', 'KerberosAuthentication': 'password check through Kerberos',
 'KerberosOrLocalPasswd': 'fallback to local password check', 'AuthenticationMethods': 'required login methods', 'PermitRootLogin': 'whether and how root may log in',
 'PubkeyAuthentication': 'whether login keys are accepted', 'AuthorizedKeysFile': 'where login keys of accounts are read', 'AuthorizedKeysCommand': 'program that supplies login keys',
 'AuthorizedKeysCommandUser': 'account running the login-key program', 'TrustedUserCAKeys': 'CA keys accepted for login certificates',
}
SSH_NOT = {'X11DisplayOffset','PrintMotd','PrintLastLog','Banner','VersionAddendum','LogLevel','SyslogFacility','FingerprintHash','PidFile','Compression',
 'TCPKeepAlive','ipqos','rekeylimit','ClientAliveInterval','ClientAliveCountMax','UnusedConnectionTimeout','ChannelTimeout','UseDNS','KerberosTicketCleanup',
 'GSSAPICleanupCredentials','GSSAPIStrictAcceptorCheck','ModuliFile','Ciphers','Macs','KexAlgorithms','HostKeyAlgorithms','HostbasedAcceptedAlgorithms',
 'LoginGraceTime','MaxAuthTries','MaxSessions','maxstartups','persourcemaxstartups','persourcenetblocksize','persourcepenalties','PerSourcePenaltyExemptList',
 'HostKeyAgent','SecurityKeyProvider','StreamLocalBindMask','XAuthLocation','IgnoreUserKnownHosts','HostbasedUsesNameFromPacketOnly'}
# everything else: HOLE (forwarding, sessions, auth-adjacent settings acting beyond sshd)

def l1(r):
    k, n, ev = r['kind'], r['name'], r['evidence']
    m = json.loads(r['members'])
    evb = 'raw:' + ev.split(':')[0] if ev.startswith('raw/') else 'evidence'
    evb = evb.replace('raw:raw/flatcar/', 'raw:')
    if k == 'L1:account':
        return T('MUST', 'S2.2-15', 'local account ' + n, evb, 'accounts must be recorded')
    if k == 'L1:group':
        line = m[0]
        mem = line.split(':')[3] if line.count(':') >= 3 else ''
        if n in ('wheel', 'sudo') and mem:
            return T('MUST', 'S2.2-15', 'group granting its members sudo rights', evb, 'membership gives the right to become superuser, which must be recorded')
        gid = line.split(':')[2]
        logins = [x for x in mem.split(',') if x in LOGIN]
        if logins and gid in gid_files:
            return T('MUST', 'S2.2-1,S2.2-2', 'grants ' + ' '.join(logins) + ' group access, e.g. ' + gid_files[gid], 'raw:raw/105-filesystem.out',
                     'removal drops the login members from the group, so access to the group-owned objects becomes impossible for them')
        if mem:
            return T('UNKNOWN', 'S3-1,S3-2', 'group ' + n + ' with members ' + mem.replace(',', ' '), evb,
                     'members are root (unaffected by group permissions) or system accounts, or no listed file is group-accessible; what removal stops is not established')
        return T('UNKNOWN', 'S3-1,S3-2', 'group ' + n + ' with no members', evb,
                 'no members; whether a unit, device rule or file grant depends on the group name is not in the inventory')
    if k == 'L1:login-key':
        return T('MUST', 'S2.2-15', 'key allowed to log in as user', evb, 'keys used to log in to an account must be recorded')
    if k == 'L1:saved-network':
        return T('NOT', RM, 'empty Gentoo placeholder in the networkd configuration directory', D_KEEP,
                 'not a saved network: networkd reads only .network, .link and .netdev files; ' + NOTHING)
    if k == 'L1:package:system-image':
        return T('MUST', 'S2.2-9', 'the Flatcar /usr image holding the system programs', evb, 'holds the programs that run on the computer, which must be recorded')
    if k in ('L1:module',):
        return T('MUST', 'S2.2-2,S2.2-10', 'loaded kernel module ' + n, evb, 'code the kernel executes with kernel rights; removal stops what it provides')
    if k == 'L1:driver':
        drv = m[0].split('\t')[-1].rsplit('/', 1)[-1]
        return T('MUST', 'S2.2-2,S2.2-10', 'kernel driver ' + drv + ' bound to a device', evb, 'driver code runs with kernel rights; unbinding or removing it stops the device working')
    if k == 'L1:port':
        return T('MUST', 'S2.2-2,S2.2-15', 'socket open for incoming traffic', evb, 'ports open for connection must be recorded; closing it stops the service (DNS, DHCP, SSH, containerd) receiving')
    if k == 'L1:process':
        exe = m[0].split('\t')[-1]
        if not exe.startswith('/'):
            return T('UNKNOWN', 'S3-1,S3-2', 'process ids with no executable path recorded', evb,
                     'the inventory recorded no executable for these ids (kernel threads or exited processes); what they run cannot be established')
        return T('MUST', 'S2.2-9', 'running program ' + exe, evb, 'a program that runs on the computer must be recorded')
    if k == 'L1:network-link':
        return T('MUST', RM, 'network interface state ' + m[0].split()[1], evb,
                 'removing the interface or its configuration stops networking over it (lo carries the local DNS stub)')
    if k == 'L1:polkit-actions':
        return T('MUST', RM, 'registered polkit action ' + n, D_POLKIT,
                 'polkit refuses authorization for unregistered actions, so removal makes the action impossible for unprivileged callers')
    if k in ('L1:service', 'L1:user-service'):
        st = m[0].split()
        if len(st) > 1 and st[1] == 'not-found':
            return T('NOT', RM, 'name referenced by other units, no unit file exists', evb, 'nothing is installed under this name; ' + NOTHING)
        return T('MUST', 'S2.2-2,S2.2-9', 'service unit ' + n.replace('user:', '') + ' (' + ' '.join(st[1:3]) + ')', evb,
                 'loaded service unit: it runs or can be started; removal makes starting it impossible')
    if k in ('L1:timer', 'L1:user-timer'):
        return T('MUST', 'S2.2-2', 'active timer ' + n.replace('user:', ''), evb, 'scheduled start of a service; removal stops those runs')
    if k in ('L1:unit-file', 'L1:user-unit-file'):
        st = m[0].split()[1]
        return T('MUST', 'S2.2-2', 'unit file ' + n.replace('user:', '') + ' state ' + st, evb,
                 'defines a unit that is enabled, startable, an alias or a dependency; removal makes starting it impossible')
    if k == 'L1:access-rule':
        if n.startswith('ssh-access:'):
            key = n.split(':', 1)[1]
            val = m[0]
            if key in SSH_MUST:
                return T('MUST', 'S2.2-15', 'sshd: ' + SSH_MUST[key], 'raw:raw/085-ssh-access.out',
                         'S2.2-15 names open ports, login keys, the right to become superuser and the rule that password login is allowed')
            if key in SSH_NOT:
                return T('NOT', 'S2.2-7', 'sshd internal setting: ' + key, D_SSHD,
                         'shapes only how sshd itself runs its protocol, logs or limits; settings in force only inside one program need not be recorded')
            return T('HOLE', 'S2.2-1,S2.2-7', 'sshd setting governing what can be done via sshd: ' + key, D_SSHD,
                     'read only by sshd (S2.2-7) yet it decides what can be done on the computer through sshd (S2.2-1); no sentence decides which applies')
        if n.startswith('sudo-'):
            return T('MUST', 'S2.2-15', 'sudo rule granting full superuser rights', D_SUDO, 'the right to become superuser must be recorded')
        if n.endswith('.rules.example'):
            return T('NOT', RM, 'example polkit rules file, not loaded', D_POLKIT, 'polkit loads only files ending in .rules; ' + NOTHING)
        if n.endswith('.rules'):
            return T('MUST', 'S2.2-10,S2.2-13', 'polkit JavaScript rules deciding authorizations', D_POLKIT,
                     'polkitd executes the file as JavaScript code; it decides who may perform privileged actions')
        if '/.keep_' in n:
            return T('NOT', RM, 'empty Gentoo placeholder in a configuration directory', D_KEEP,
                     'sudo skips names with a dot, PAM and polkit read only service or .rules names; ' + NOTHING)
    if k == 'L2:executable-code-outside-packages':
        return decide_member(n)
    return None

out = []
members_out = []
l2rows = {r['name']: r for r in rows if r['kind'] == 'L2:stored-outside-packages'}
agg_cache = {}

def agg(name):
    if name in agg_cache:
        return agg_cache[name]
    r = l2rows[name]
    decs = {}
    for mpath in json.loads(r['members']):
        if mpath == name:
            continue
        if mpath in l2rows:
            d = agg(mpath)[0]
            members_out.append((r['id'], mpath, d, 'see own row'))
        else:
            res = decide_member(mpath)
            d = res[0]
            members_out.append((r['id'], mpath, d, res[1]))
        decs.setdefault(d, []).append(mpath)
    if len(decs) == 1:
        d = next(iter(decs))
        res = (d, None, decs)
    else:
        res = ('MIXED', None, decs)
    agg_cache[name] = res
    return res

for r in rows:
    if r['kind'] == 'L2:stored-outside-packages':
        d, _, decs = agg(r['name'])
        mem = json.loads(r['members'])
        mem = [m for m in mem if m != r['name']]
        if d != 'MIXED':
            # all members same decision: reuse the member rule texts when homogeneous
            first = [m for m in mem if m not in l2rows]
            if first:
                res = decide_member(first[0])
                sents, basis = res[1], res[3]
                rs = {decide_member(m)[4] for m in first}
                reason = res[4] if len(rs) == 1 else 'every member gets ' + d + ' by its own rule; see part-flatcar.members.tsv'
            else:
                sents, basis, reason = 'S2.2-1,S2.2-2', 'raw:raw/105-filesystem.out', 'all members are subdirectories decided ' + d + ' in their own rows'
            if first and len(rs) == 1:
                what = ' '.join(('%d objects, each: %s' % (len(mem), res[2])).split()[:15])
            else:
                what = 'directory of %d stored objects' % len(mem)
            out.append((r['id'], d, sents, what, basis, reason))
        else:
            parts = ', '.join('%s %d' % (k, len(v)) for k, v in sorted(decs.items()))
            named = '; '.join('%s: %s' % (k, ' '.join(x.rsplit('/', 1)[-1] for x in v)) for k, v in sorted(decs.items()))
            if len(named.split()) <= 22:
                parts = named
            sents = set()
            for m in mem:
                if m not in l2rows:
                    sents.update(decide_member(m)[1].split(','))
            out.append((r['id'], 'MIXED', ','.join(sorted(sents)) or 'S2.2-1,S2.2-2', 'directory of %d stored objects with different decisions' % len(mem),
                        'raw:raw/105-filesystem.out', 'members split: ' + parts + '; per-member decisions in part-flatcar.members.tsv'))
    else:
        res = l1(r)
        if res is None:
            raise SystemExit('no rule for ' + r['id'] + ' ' + r['kind'] + ' ' + r['name'])
        out.append((r['id'],) + res)

for o in out:
    for f in o:
        assert '\t' not in f and '\n' not in f, o
    assert len(o[3].split()) <= 15, ('what too long', o)
    assert len(o[5].split()) <= 30, ('reason too long', o)

with open(outp, 'a', encoding='utf-8') as f:
    for o in out:
        f.write('\t'.join(o) + '\n')
with open(memp, 'w', encoding='utf-8') as f:
    f.write('row_id\tmember\tdecision\tsentences\n')
    seen = set()
    for m in members_out:
        if (m[0], m[1]) in seen:
            continue
        seen.add((m[0], m[1]))
        f.write('\t'.join(m) + '\n')
print(len(out))
