# A1 classification rules

Script rule count: **8**.

The script is (not published: trial helper scripts). It appends missing IDs. Explicit `MANUAL` entries are row-by-row decisions selected after examining each row; the helper only serializes those decisions and shares wording for the same observed role. These explicit assignments are not pattern-based classification rules. Small groups have individually entered decisions, not invented ten-row samples.

Read scope: PAGE.md, this task folder, and evidence-named inventory files in the permitted A1 raw root. The raw-X1, raw-X2 and raw-E6 files named by later A1 rows were not found in the permitted raw roots; supplied evidence excerpts were used without looking in other project directories.

Directory decisions concern the directory object rather than every descendant. Runtime NO follows R5; containing-program record is stated in the reason. L1/L2 coverage means an eligible source/package line, not proof that an actual declaration already has it.

## A1-1. Packages in the CoreOS image

Sentences: I2,Q1,R1,L1. Each named installed RPM is part of the clean CoreOS operating-system image. Classify INSTALLED/COVERED by the image line. The ten checks cover metadata packages, coreutils data, dbus, EFI scaffolding, release identification, FUSE support, locales, kernel metapackage, libreport data, and Moby directory scaffolding.

Technical documentation: https://github.com/coreos/fedora-coreos-docs/blob/main/modules/ROOT/pages/storage.adoc

Ten manually inspected rows:
- `coreos-d49702b0f3` — containers-common-extra
- `coreos-3ed34b954a` — coreutils-common
- `coreos-5ddf73f1ac` — dbus
- `coreos-bc2b712980` — efi-filesystem
- `coreos-d9db8ebd61` — fedora-release-coreos
- `coreos-4c44b1402c` — fuse-common
- `coreos-80c805d99c` — glibc-minimal-langpack
- `coreos-326325fdeb` — kernel
- `coreos-bd48096336` — libreport-filesystem
- `coreos-cc816199e8` — moby-filesystem

## A1-2. Debian packages with unknown selection provenance

Sentences: Q1,R1,L1. The ii status establishes installation, but these records do not establish direct selection versus automatically installed dependency. Classify INSTALLED/NA/FACT_UNKNOWN. Each checked row has a package name/version and installed status, but no manual/automatic flag.

Ten manually inspected rows:
- `debian-e62af4f5a5` — cloud-utils
- `debian-95bb80c619` — init
- `debian-f1ae2388d8` — libmagic-mgc
- `debian-d805aa0253` — libpython3-stdlib:amd64
- `debian-44132e21a0` — libsemanage-common
- `debian-8e648115c5` — libtirpc-common
- `debian-ad283af0ea` — media-types
- `debian-9c32a751d6` — ncurses-base
- `debian-614d6e2913` — netbase
- `debian-9e34733f17` — python-apt-common

## A1-3. Package-owned directory objects

Sentences: Q1,R6,R1,L1. Intersect the named files.tsv entries with package-files.txt and require every selected member to have type d. Classify INSTALLED/COVERED. The object is the package-owned directory itself, not its recursive contents or a separate permission value. All ten checked entries exist, are package-owned directories, and have one listed member.

Ten manually inspected rows:
- `coreos-3cd182c07b` — /boot
- `coreos-827c5914e9` — /boot/efi
- `coreos-037231a728` — /etc
- `coreos-d3d071d2ba` — /etc/alternatives
- `coreos-c0faa16997` — /etc/binfmt.d
- `coreos-43399114f3` — /etc/credstore
- `coreos-edd98ae366` — /etc/credstore.encrypted
- `coreos-fc1b65b090` — /etc/depmod.d
- `coreos-31a0673933` — /etc/dnsmasq.d
- `coreos-1ae98d3e98` — /etc/dracut.conf.d

## A1-4. Nix store outputs with unknown covering source

Sentences: I1,I2,Q1,R1,L1. The exact store paths exist in packages.tsv, but that file inventories the whole store. Neither path existence nor immutability establishes current-system membership, dependency edges or a covering construction line. Classify INSTALLED/NA/FACT_UNKNOWN. Ten checks: nix.conf, dhcpcd.conf, hosts, gai.conf, mailcap, fuse.conf, nixos-init, restart-trigger data, hostname and tmpfiles.d. Their existence is established; source coverage is not.

Technical documentation: https://nix.dev/manual/nix/2.24/store/store-object

Ten manually inspected rows:
- `nixos-a332c16c0a` — /nix/store/00gmmr7b9slac4srbg4rqlwrw1k9rxnf-nix.conf
- `nixos-bd414d6b6a` — /nix/store/07n7039ak38i26hgf2s3501y9l5f6fs2-dhcpcd.conf
- `nixos-e78f81d36e` — /nix/store/0f5y6wcik5ldry8d1kl4a2f7hi5mq9pn-hosts
- `nixos-903eca0ec8` — /nix/store/0fhmy5gh22w9ysg62aj04bah31xyb0a5-etc-gai.conf
- `nixos-e3ea449be8` — /nix/store/0kk05fksy78xybp0jvvbnyiindqxz7ag-mailcap-2.1.54
- `nixos-70bca474fd` — /nix/store/0qqf2bnfp16a6y3448n7bz1rl9yyfvjq-etc-fuse.conf
- `nixos-90649e5e3f` — /nix/store/0xppmwrpx3d3wrvzq57kqkg9mlrim6r6-nixos-init-0.1.0
- `nixos-a738960c81` — /nix/store/15qy3pqkq3503xgypbmp3dbinngslxy6-X-Restart-Triggers-reload-systemd-vconsole-setup
- `nixos-d3ac6fc3e9` — /nix/store/1za4k4r5lkd3j0hnxhrazwwvyy9x61s6-etc-hostname
- `nixos-532c5e327b` — /nix/store/24ky217wazac3asqmzw1jy76nx7b368v-tmpfiles.d

## A1-8. Guix store output units

Sentences: I1,I2,Q1,R6,R1,L1. Guix installer-managed immutable output units include compiled/imported modules, generated system configuration, profile integration and received package data. These units are covered by their system construction line. Ten individually checked roles: module import, D-Bus configuration, icon package, desktop database, elogind configuration, another module import, groupmod wrapper, Guile launcher source, fonts directory and system test source.

Technical documentation: https://guix.gnu.org/manual/en/guix.pdf

Ten manually inspected rows:
- `guix-2a85615a21` — /gnu/store/0ibs0670s2b86pgrv53zph81h31ad1cx-module-import
- `guix-331ca6e362` — /gnu/store/0icq9vkz96352mgq8f31wm1d5rnxjy9w-dbus-configuration
- `guix-d8c1d6933d` — /gnu/store/18ngrsi4i7y2d05bz3xxpg1znqiq2bw1-hicolor-icon-theme-0.17
- `guix-f0f6c755c7` — /gnu/store/1mh7p4gzgndd576qlnc1p0ypjp2p965b-xdg-desktop-database
- `guix-ad573531ab` — /gnu/store/1rf9x4sy3mgjhvkppsj0mxbbrqmd2zcx-etc-elogind
- `guix-a1c1e67353` — /gnu/store/1vq19qhhqhx68lr3cp0a6kxpfrq7cd0q-module-import
- `guix-2838d57c33` — /gnu/store/207kx6f9a0j2nixr8225bka6147x4j4a-groupmod
- `guix-9e59c1810b` — /gnu/store/2dvxx7hdc8fsy4mfhddx16kyh4kf3cbm-guile-launcher.c
- `guix-987332f8d2` — /gnu/store/2ll8zirz0ih1yvzfzmpckhic7gbm160b-fonts-dir
- `guix-cf8bd029de` — /gnu/store/2mc7g2khyf8n49101f5nx6g8skx9lq7a-guix-system-tests-source

## A1-5. Owned content without unchangedness evidence

Sentences: Q1,Q2,Q3,Q4,L1,L2. The path inventory establishes ownership, but at least one member is content-bearing. No captured checksum/content comparison establishes that it remains as received. Unchanged content is Q1/COVERED; changed code or selected values can require an own line, and changed passive values can become optional. Classify NONE/NA/FACT_UNKNOWN. Each of the ten checks contains a non-directory member and lacks comparison evidence.

Ten manually inspected rows:
- `coreos-1d70ce548d` — /boot/grub2
- `coreos-cc15017ada` — /etc/GREP_COLORS
- `coreos-9945c88deb` — /etc/NetworkManager
- `coreos-0a38e83850` — /etc/X11
- `coreos-d20d960ea0` — /etc/adjtime
- `coreos-341d2df2d9` — /etc/aliases
- `coreos-a4c2c16ae9` — /etc/audit
- `coreos-e2885ad43a` — /etc/authselect
- `coreos-f536dafd04` — /etc/azure-ephemeral-disk-setup.conf
- `coreos-d68859230e` — /etc/bindresvport.blacklist

## A1-6. Runtime representations

Sentences: R5,Q1,Q3a,L1,L2. Classify live device, mount, scope, slice, unresolved manager reference, swap and process representations RUNTIME/NO/DECIDED. Name their creating program or setting and its record separately. Creator coverage uncertainty cannot change the runtime object's own NO. The ten checks identify devices twice, two /run-generated service representations, further devices, mounts, init/session scopes, slices, user devices and user mounts. Stored files are not included merely because their paths contain run.

Technical documentation: https://www.freedesktop.org/software/systemd/man/254/systemd.device.html

Ten manually inspected rows:
- `coreos-a3f2270221` — unpackaged *.device
- `coreos-88335c6c87` — unpackaged *.device
- `debian-96787848d5` — netplan-ovs-cleanup.service
- `debian-0758efc3b0` — systemd-growfs@-.service
- `debian-a3f2270221` — unpackaged *.device
- `debian-18fb2985ed` — unpackaged *.mount
- `debian-0ff15b2741` — unpackaged *.scope
- `debian-253d752b01` — unpackaged *.slice
- `debian-88335c6c87` — unpackaged *.device
- `debian-565df89b5f` — unpackaged *.mount

## A1-7. Installation-provided service defaults

Sentences: Q3a,R1,L2. The row denotes a service/target, not its on-disk fragment file. A standard systemd fragment under /lib/systemd/system with no drop-ins supplies the installation default: SETTING/COVERED. The ten manually checked initrd service/target entries each name their fragment and an empty drop-in list.

Ten manually inspected rows:
- `debian-6b5b5b2232` — initrd-cleanup.service
- `debian-8786c9eece` — initrd-fs.target
- `debian-646aa477ec` — initrd-parse-etc.service
- `debian-00a56889bd` — initrd-root-device.target
- `debian-6e3a25797c` — initrd-root-fs.target
- `debian-c1428e493e` — initrd-switch-root.service
- `debian-bc71f8a67c` — initrd-switch-root.target
- `debian-cc14a4c724` — initrd-udevadm-cleanup-db.service
- `debian-59f9abe755` — initrd-usr-fs.target
- `debian-101133305f` — initrd.target

## Additional documentation for individual decisions

- Guile compiled Scheme cache: https://www.gnu.org/software/guile/manual/guile.pdf
- APK supplied configuration copies: https://docs.alpinelinux.org/user-handbook/0.1a/Working/apk.html
- Ghostscript PostScript files: https://ghostscript.readthedocs.io/en/latest/Develop.html
- Kyua Lua configuration: https://man.freebsd.org/cgi/man.cgi?manpath=FreeBSD+14.3-RELEASE&query=kyua.conf&sektion=5
- Guix store and system construction: https://guix.gnu.org/manual/en/guix.pdf

## Independent-review points

- Independent review changed all 122 individual Nix store-output rows to FACT_UNKNOWN because the evidence establishes existence but not a covering dependency or construction source. No unreferenced closure file was used.
- Mutable package-owned paths have only type/path/size evidence, so their unchangedness is left factual rather than presumed from ownership.
- Explicit service rows describe service defaults; package-owned fragment-file rows describe stored objects. These are different objects under Q1/Q3a.

## Individually reviewed link and state exceptions

The following are explicit row-by-row corrections, not an additional script rule:
- Channel/profile selectors: nixos-3e7f003ce6, nixos-a5c695f848, nixos-63d8a049ea, guix-76e4372b50 — SETTING; default-versus-choice provenance unknown.
- CoreOS boot scaffolding: coreos-3620611c7e — INSTALLED/COVERED by its image.
- Vendor/palette selectors: ubuntu-7740cdd4af, ubuntu-de7f67781f — SETTING; default-versus-choice provenance unknown.
- Persistent mtab symlinks: debian-6b4026dd02, nixos-6b4026dd02, guix-6b4026dd02 — package receipt versus separately generated provenance unknown; runtime-target status does not classify the persistent link.
- Release-identification link: arch-6a38277ef0 — package receipt versus separate generation unknown.
- Mail-alias selector: freebsd-0b0c34385f — SETTING; default-versus-choice provenance unknown.
- NixOS marker: nixos-c093c82f20 — package receipt versus separate generation unknown.
- Account reconciliation state: nixos-ec96d00e30 — active account-control values versus passive history unknown.

## Final independent-review corrections

(not published: trial helper scripts) revises twenty explicit individual rows after reviewing their actual evidence. `coreos-2d7adb8ef6`, `nixos-bfd49e603a`, `guix-da5f01a3ef`, and `freebsd-c2cf70a5ff` become FACT_UNKNOWN because the alleged mixed member decisions were not established. `guix-a2b4d23600` and `guix-d084f3423e` are RUNTIME/NO; their PID files are not independently persistent settings. `guix-c2cf70a5ff` is NONE/NO/DECIDED: runtime and directory-container alternatives all need no own line. These are individual corrections, not an additional scripted classification rule.

Further individual corrections distinguish actual per-machine GRUB evidence, correct GTK accelerator-map data under U4, separate received dpkg control metadata from generated status/lists, and leave Guix checkout code coverage conditional. These corrections are recorded explicitly in (not published: trial helper scripts), not inferred from a new pathname rule. Technical references: https://www.gnu.org/software/grub/manual/grub/html_node/Environment-block.html ; https://docs.gtk.org/gtk3/class.AccelMap.html .
