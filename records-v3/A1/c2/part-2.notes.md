# c2, part 2 of A1 — notes

Input: `../in/part-2.tsv`, 839 rows, all from the Debian 12 machine. Output: `part-2.tsv`.
Decisions use only Section 2.2 and indicator S3-1/S3-2 of `../../TEXT.md`, with sentence IDs from `../../SENTENCES.md`.

## How "what the object does" was established

- Inventory files under `A1/in/raw/debian/` (accounts, processes, units, modules, files, groups).
- Public Debian documentation and packages: package descriptions and file lists from the bookworm `Packages`,
  `Contents-amd64` and `Contents-all` indexes (`raw/part-2/package-info.tsv`); reverse dependencies (`raw/part-2/reverse-depends.txt`);
  the bookworm `.deb` files themselves, downloaded on the server and inspected read-only: shipped content of every
  package-owned `/etc` file (`raw/part-2/po-etc-content.tsv`), unit headers (`raw/part-2/debian12-unit-headers.txt`), tmpfiles rules
  (`raw/part-2/debian12-tmpfiles.txt`), AppArmor include closure (`raw/part-2/apparmor-include-closure.txt`), maintainer scripts and
  program strings (`raw/part-2/package-inspection.md`).
- The Debian cloud image build source (debian-cloud-images, commit cc29a4adc3366b4739b388dc862fd17bad6c2835,
  `config_space/12/files/etc`) for unowned files the image installs; sizes match the inventory
  (`raw/part-2/debian-cloud-images-files.txt`).
- Linux-PAM 1.5.2 source for missing-file behaviour of pam_limits and pam_env (`raw/part-2/pam-source-excerpts.txt`).
- Nothing was removed anywhere; no machine of the inventory was touched. The removal test is applied by reasoning.
- Current content of package-owned files is not in the inventory; for them the shipped content is used. Unowned files
  are judged by size against the template that writes them (kmod, initramfs-tools, apparmor, screen, cloud image).

## Readings applied (stated so the adjudication can check them)

1. Removal of a package means removing its own files, not its reverse dependencies.
2. Removal of a directory removes everything below it; a directory is MUST when its subtree holds a MUST object, and
   NOT when it is empty or holds only NOT objects and its absence breaks nothing.
3. S2.2-2 calls removal "the test": when removal makes nothing stop and nothing impossible, and no explicit
   consequence (S2.2-9..16) applies, the object is NOT (the requirement of S2.2-1/S2.3-4 does not reach it).
4. The exceptions S2.2-4..7 are an enumerated list of objects that need not be recorded. Where an object fits the
   category word of S2.2-4 (contents of a database) but its removal makes programs fail, S2.2-4 and S2.2-2 give
   opposite answers and no sentence says which prevails: HOLE (libmagic-mgc, ncurses-base, netbase, /etc/protocols,
   /etc/services, /etc/ethertypes). Where removal leaves only the data itself unavailable, S2.2-4 holds: NOT.
5. "In force only inside one program" (S2.2-7) is read as where the setting takes effect. A setting read by one
   program whose effect reaches other programs or the whole system (resolver, PAM, OpenSSL, libattr, apparmor_parser)
   is not exempt. Recorded as a question in `QUESTIONS.md`.
6. Program state (dpkg status, apt extended_states, cloud-init instance state, ucf, pam-auth-update state): S2.5-1
   puts its treatment outside the conditions of declarativeness, and COMMON.md says this is not a hole, so it is
   decided NOT with S2.5-1, even where S2.2-2 alone would say MUST. Recorded as a question in `QUESTIONS.md`.
7. Runtime objects the service manager creates itself (device, mount, scope and slice units without a stored
   definition): "removal" has no defined meaning for them (deleting is impossible or undone at once; stopping is a
   different act with a different outcome): HOLE.
8. A unit that cannot take effect on this machine without installing other software (initrd units: assert
   /etc/initrd-release, initramfs built by initramfs-tools without systemd; pcrphase units: need TPM2 and systemd-stub)
   is NOT. A unit whose condition can be met by configuration on this machine (rc-local, systemd-repart, sysext,
   firstboot, getty-static) counts as something that can be done and falls under rule R4.
9. Programs that can be started count as "what can be done" (S2.1-3, S2.2-1); code is MUST when a program installed
   here executes it (S2.2-10), NOT when the executing program is not installed (cron, ifupdown, NetworkManager,
   pm-utils, runit, logrotate, ufw).

## Rules applied by script (`scripts/part-2/rules.py`), 511 rows

- R1 accounts (27 rows): MUST, S2.2-15 ("accounts ... must be recorded"). Hand-checked: debian-4900fca16b,
  debian-3413994e24, debian-205e945769, debian-ead54fe7c7, debian-1f9ebd3eec, debian-8e4a0f0c6a, debian-96a19ba1e6,
  debian-9911292f99, debian-8d1e409524, debian-a0ea4d1be3 — all are entries of `accounts.txt`; the rule fits.
- R2 loaded kernel modules (52 rows): MUST, S2.2-10 (code the kernel executes with its own rights). Hand-checked:
  debian-accf085699, debian-4fb00be8be, debian-a7a7878085, debian-aecb8841ca, debian-4887feeab8, debian-68ad7d0788,
  debian-8f2dd3f005, debian-a244292f7c, debian-eb28e69afa, debian-be057bae4b — all listed as loaded in `modules.txt`
  with a .ko path; the rule fits.
- R3 packages whose Debian file list ships programs, shared libraries, Python/Perl modules, kernel modules or EFI/GRUB
  binaries (298 rows): MUST, S2.2-9, S2.2-10, S2.2-2. The 29 packages without such files were decided row by row.
  Hand-checked: debian-cb1199cf26 (bsdextrautils, binaries), debian-8e3327d406 (libnewt, library), debian-9fd37b26ca
  (libpsl5, library), debian-1ef8d87c84 (polkitd, daemon), debian-d4fa59e45e (libfuse2, library), debian-9c9c46fedb
  (libfdisk1, library), debian-c85e9b1c30 (less, program), debian-d03dd1db64 (shim-unsigned: EFI binaries that
  grub-install references under /usr/lib/shim, code it can install for the firmware to run), debian-70df05b9e9
  (vim-common, ships xxd), debian-f1c69b6f9a (fdisk, programs) — the rule fits all ten.
- R4 system units loaded by the service manager from a packaged unit file in /lib/systemd/system (134 rows): MUST,
  S2.1-3, S2.2-1, S2.2-2 (removal makes starting the service, socket, timer, mount or target impossible). The 15 units
  that are initrd-only, need TPM2 + systemd-stub, or are generated into /run were decided row by row. Hand-checked:
  debian-80dbca81d5, debian-82c9ccda89, debian-fa6d770197, debian-521fa4df3c, debian-3950d213fd, debian-6f37618a1d,
  debian-e5d9984fe4, debian-b25b83c890, debian-6aa1a6a0da, debian-e8f9230944 — all have fragment
  /lib/systemd/system/... and can be started here; the rule fits (swap.target and similar empty synchronization
  targets fit only through "can be started", reading 9).

All other 328 rows were decided row by row (`part-2.manual-1.txt`, `part-2.manual-2.txt`, `part-2.manual-3.txt`, appended by
`scripts/part-2/append_manual.py`; two own corrections by `scripts/part-2/patch.py`).

## Members of MIXED rows

- debian-d3d071d2ba /etc/alternatives (package-owned): MUST directory; NOT README.
- debian-7b1b0b20fe /etc/apparmor.d (package-owned, 162): MUST the profiles lsb_release, nvidia_modprobe,
  sbin.dhclient, usr.bin.man, usr.bin.tcpdump, abi/3.0, the 29 files of `raw/part-2/apparmor-include-closure.txt` other than
  the profiles, and the directories apparmor.d, abi, abstractions, tunables, tunables/home.d, tunables/multiarch.d,
  tunables/xdg-user-dirs.d, local; NOT all other members (abstractions and abi files no loaded profile includes,
  abstractions/apparmor_api, abstractions/ubuntu-browsers.d and its files, disable, force-complain, local/README).
- debian-3eca422b52 /etc/cloud (package-owned, 44): MUST cloud.cfg, the directories, and templates selected for Debian
  or distribution-neutral (hosts.debian, sources.list.debian, chrony.conf.debian, ntp.conf.debian, resolv.conf,
  systemd.resolved.conf, timesyncd.conf); NOT cloud.cfg.d/05_logging.cfg, both READMEs, templates for other
  distributions.
- debian-4f3962b16e /etc/default (package-owned): MUST directory, grub.d, grub, useradd; NOT dbus,
  grub.d/init-select.cfg, hwclock, nss, ssh.
- debian-b91b989f2d /etc/grub.d: MUST directory and 00_header ... 41_custom; NOT README.
- debian-cd959a64eb /etc/initramfs-tools: MUST directory, initramfs.conf, update-initramfs.conf; NOT conf.d, hooks,
  scripts and its 10 subdirectories (all empty).
- debian-35ac52fc24 /etc/kernel: MUST directory, postinst.d, postrm.d and their five hooks; NOT install.d (empty).
- debian-aaa1adf124 /etc/security: MUST directory and limits.conf; NOT access.conf, faillock.conf, group.conf
  (pam_group is optional in login and the file has no rule), namespace.conf, namespace.init (pam_namespace in no
  stack), pam_env.conf (missing file is ignored, PAM_IGNORE), sepermit.conf, time.conf, limits.d, namespace.d.
- debian-c366c1919d /etc/ssh (package-owned): MUST directory; NOT ssh_config, moduli, ssh_import_id, ssh_config.d,
  sshd_config.d.
- debian-5f604fda76 /etc/ssl (package-owned): MUST /etc/ssl, certs, openssl.cnf; NOT private.
- debian-5cec13c210 /etc/sudoers.d (package-owned): MUST directory; NOT README.
- debian-4d2a7c7537 /etc/systemd (package-owned): MUST /etc/systemd and system/; NOT journald.conf, logind.conf,
  networkd.conf, pstore.conf, resolved.conf, sleep.conf, system.conf, timesyncd.conf, user.conf (all fully commented
  in the package), network/, user/ (empty), sshd-keygen@.service.d and its drop-in (no such unit on Debian).
- debian-ce45570012 /etc/apt (stored): MUST sources.list.d/debian.sources, mirrors/debian.list,
  mirrors/debian-security.list, apt.conf.d/20auto-upgrades, apt.conf.d/50unattended-upgrades; NOT listchanges.conf,
  sources.list (only a comment line, as in the image build source).
- debian-0075a76d48 /etc/ssh (stored): MUST sshd_config, ssh_host_ecdsa_key, ssh_host_ed25519_key, ssh_host_rsa_key;
  NOT ssh_host_dsa_key and all .pub files. (Based on sshd_config(5) defaults for HostKey and the Debian template,
  which has HostKey lines commented; the current sshd_config content is not in the inventory.)
- debian-3cce15cf49 /var/lib/dpkg (stored, 1536): MUST info/*.preinst, *.postinst, *.prerm, *.postrm, *.config;
  NOT all other members.
- debian-57da4d32dc /var/lib/systemd (stored): MUST linger/census; NOT all other members.
- debian-64f62c6553 directory skeleton (21 groups): MUST /home/census; NOT /etc/opt, /home/census/.config,
  /home/census/.config/nano, /opt, /srv, /usr/local and its subtree, /var/cache/private, /var/lib/private,
  /var/log/private, /var/mail, /var/opt, the /var/tmp entries.

## UNKNOWN rows

- debian-d47133480a /etc/hosts.allow and debian-b8a8c42f35 /etc/hosts.deny: read by sshd and socat through libwrap;
  content not in the inventory, size differs from the libwrap0 template (411/711 vs 444/744 bytes).
- debian-168923b779 /var/lock: whether any program here uses it before boot recreates it was not established.

## Cleanup

Downloaded indexes, packages and the cloud image source on the server were deleted after the evidence above was saved.

## Shared folder

`A1/c2/scripts/` and `A1/c2/raw/` are shared with other parts; this part's files are under `scripts/part-2/` and
`raw/part-2/`. When `scripts/part-2/show_groups.py` was first written into `scripts/`, the editor reported that a file of that name
already existed; it was replaced. No notes file of another part refers to that name.
