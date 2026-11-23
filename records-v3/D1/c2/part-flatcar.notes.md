# c2, part flatcar: notes

Input: `../in/part-flatcar.tsv` (1827 rows). Output: `part-flatcar.tsv` (one row per input id).
Per-member decisions of the 386 directory rows (`L2:stored-outside-packages`): `part-flatcar.members.tsv`
(`row_id, member, decision, sentences`; a member that is itself a directory row carries that row's
decision). Script: `scripts/classify_flatcar.py` (run as
`classify_flatcar.py <input.tsv> <raw/105-filesystem.out> <out.tsv> <members.tsv>`). Downloaded documentation
sources that were quoted are kept in `raw/flatcar-doc-sources/`.

Decisions use only Section 2.2 and S3-1/S3-2. Nothing was removed anywhere. The removal test is applied by
reasoning from what the object does.

## Readings applied (stated, not resolved; see "Questions for the author")

1. **NOT through a negative removal test.** S2.2-2 says "The test is removal". When removing an object changes nothing the
   computer does or can do, I read the test as negative, and S2.2-1 gives no requirement, so the object is NOT
   (sentences S2.2-1,S2.2-2). Examples: empty Gentoo `.keep_*` placeholders, example files, lock files, build inputs
   embedded elsewhere, generator output that is rewritten on every reload.
2. **S2.2-7 is an exemption from S2.2-2 within its scope.** The list after S2.2-3 is read as carve-outs. The example
   in S2.2-7 is a browser home page, theme and extensions, whose removal does change what the browser does. When a
   setting acts only inside its program (protocol details, logging, keepalive), the decision is NOT (S2.2-7). When a
   setting read by one program decides what can be done on the computer through it (forwarding, forced commands,
   GRUB autoload lists whose loss stops the boot, useradd skeleton files), it is a HOLE: the text does not say whether
   such a setting is "in force only inside one program".
3. **Content not in the inventory → UNKNOWN.** The inventory lists paths, types and modes but not file contents. A
   configuration file that a program reads as values has a removal effect that depends on its values: shipped
   commented defaults change nothing, set values change something. Where the contents could not be established, the
   case is UNKNOWN (S3-2). Most UNKNOWN rows come from this.
4. **Program state in /run is decided by S2.2 alone.** The task allows only S2.2 and S3-1/S3-2, so S2.5-1 was not used.
   Sockets, Varlink registry links, userdb entry points, the udev database and tags: removing them makes connecting or
   lookup impossible, so they are MUST (S2.2-1,S2.2-2). Pid, lock and stamp files are NOT. Cache is NOT (S2.2-5),
   logs and login records are NOT (S2.2-6), banners are NOT (S2.2-4). State files whose readers are not documented
   are UNKNOWN.

## Boot path of this machine (decides the /boot rows)

- The machine booted through **BIOS**, not UEFI. Evidence: the udev database holds
  `+platform:vga-framebuffer.0` (`part-flatcar.members.tsv`, `/run/udev/data`). Linux `sysfb.c` registers
  `vga-framebuffer` only for `VIDEO_TYPE_VGAC` (VGA text mode). Under UEFI it registers `efi-framebuffer`
  (https://github.com/torvalds/linux/blob/master/drivers/firmware/sysfb.c, switch after "if the FB is incompatible,
  create a legacy framebuffer device").
- The machine is a QEMU/KVM guest, not Xen PV: its drivers are virtio_blk, virtio_net, virtio-pci and fw_cfg, and the
  qemu_fw_cfg module is loaded ((not published: external working record), (not published: external working record)).
- Flatcar GRUB layout (https://github.com/flatcar/scripts/blob/main/build_library/grub_install.sh):
  - `load.cfg` and `grub.cfg.tar` are passed to `grub-mkimage --config/--memdisk`, so they are embedded in the core
    image;
  - i386-pc non-core modules and lists are copied, xz-compressed, to `flatcar/grub/i386-pc`;
  - `grub-bios-setup` writes boot code to the MBR and the BIOS-BOOT partition, and `mbr.bin` is a restore copy;
  - the x86_64-xen target produces `xen/pvboot-x86_64.elf` and `boot/grub/menu.lst`.
- `grub.cfg` (https://github.com/flatcar/scripts/blob/main/build_library/grub.cfg) runs `set prefix=($root)/flatcar/grub`
  and `insmod all_video`, and sources `($oem)/grub.cfg`. So BIOS GRUB loads modules from `i386-pc/` at boot.
- GRUB reads `command.lst`, `fs.lst`, `crypto.lst`, `terminal.lst` and `parttool.lst` at runtime
  (`grub-core/normal/dyncmd.c`, `autofs.c`, `crypto.c`, `term.c`, `commands/parttool.c`; copies in
  `raw/flatcar-doc-sources/`). A code search of `rhboot/grub2` finds `video.lst`, `partmap.lst`, `moddep.lst` and
  `fdt.lst` only in build files (`Makefile.am`, `genmoddep.awk`, `genmod.sh.in`).

## Rules applied by the script, with the rows checked by hand

Each rule follows from the sentences in its output rows. For each rule decided by a script, I checked up to 10 sampled
rows by hand (`scripts/samples.py`, seed 1122; `scripts/samples.txt` lists the samples with names). One fix came out
of the hand check before the final run:

- `RefuseConnection` was moved from NOT to HOLE.
- Groups whose members are only root or nologin system accounts, or whose gid owns no group-accessible listed file,
  were moved from MUST to UNKNOWN.

### L1 rules

- **Accounts** → MUST, S2.2-15.
- **Login key** → MUST, S2.2-15.
- **sudo rules** → MUST, S2.2-15.
- **Groups:**
  - `wheel` and `sudo` with members → MUST (S2.2-15, right to become superuser).
  - Groups with a login member other than root, whose gid owns a group-accessible file in `../in/raw/flatcar/raw/105-filesystem.out` →
    MUST (S2.2-1,S2.2-2). These are `docker` (`/run/docker.sock` 660) and `systemd-journal` (`/var/log/journal`).
  - All other groups → UNKNOWN (S3-2).
- **Kernel modules and bound drivers** → MUST (S2.2-2,S2.2-10).
- **Ports** (listening TCP and bound UDP sockets) → MUST (S2.2-2,S2.2-15).
- **Processes with an executable** → MUST (S2.2-9). The row with only process ids and no executable path → UNKNOWN.
- **Network links** lo, eth0, eth1 → MUST (S2.2-1,S2.2-2).
- **polkit actions** → MUST (S2.2-1,S2.2-2). polkit fails authorization for an action that is not registered
  ("Action %s is not registered", `check_authorization_sync`,
  https://github.com/polkit-org/polkit/blob/main/src/polkitbackend/polkitbackendinteractiveauthority.c).
- **polkit `.rules` files** → MUST: JavaScript executed by polkitd (S2.2-10,S2.2-13). `.rules.example` → NOT.
- **Loaded services, timers, unit files** (system and user) → MUST (S2.2-2, plus S2.2-9 for services). Removal makes
  starting the unit impossible. Unit conditions were not examined: unit file contents are not in the inventory.
  Services in state `not-found` → NOT (no unit file exists).
- **sshd effective settings** (`sshd -T`, (not published: external working record)):
  - MUST (S2.2-15), the items S2.2-15 names: open port (`port`, `listenaddress`, `AddressFamily`), login keys
    (`PubkeyAuthentication`, `AuthorizedKeysFile`, `AuthorizedKeysCommand(User)`, `TrustedUserCAKeys`), root login
    (`PermitRootLogin`) and the password-login rule (`PasswordAuthentication`, `KbdInteractiveAuthentication`,
    `PermitEmptyPasswords`, `UsePAM`, `KerberosAuthentication`, `KerberosOrLocalPasswd`, `AuthenticationMethods`).
  - NOT (S2.2-7): protocol, logging and limit settings internal to sshd.
  - HOLE (S2.2-1 vs S2.2-7): everything else, i.e. settings that decide what can be done through sshd (forwarding,
    tunnels, `ForceCommand`, `ChrootDirectory`, `AcceptEnv`, `subsystem`, `HostKey`, accepted key algorithms,
    `RefuseConnection` …).
- **Saved network** (`/etc/systemd/network/.keep_sys-apps_systemd-0`, empty) → NOT. It is not a saved network:
  networkd reads only `.network`, `.link` and `.netdev` files.
- **System image** → MUST (S2.2-9).

### L2 rules

Code rows and directory members follow the path rules in `MEMBER_RULES`, `RUN_RULES`, `VAR_RULES` and `OEM_RULES` of the
script. The main ones:

- **i386-pc GRUB `.mod`** → MUST (S2.2-2,S2.2-10).
- **i386-pc runtime `.lst`** → HOLE (S2.2-2,S2.2-7,S2.2-13).
- **i386-pc build-only `.lst`, `core.img`, `boot.img`, `mbr.bin`, `load.cfg`, `grub.cfg.tar`** → NOT.
- **All x86_64-xen files, `pvboot-x86_64.elf`, `menu.lst`, the UEFI loaders** → NOT (not executed on this BIOS
  QEMU/KVM machine).
- **`vmlinuz-a`** → MUST (S2.2-9).
- **`/oem/grub.cfg`** → MUST (S2.2-10,S2.2-13).
- **User and system bash startup files and `profile.d/*.sh`** → MUST (S2.2-10).
- **`gawk.csh` and the xinitrc.d script** → NOT. No csh, tcsh, xinit or X server is present in
  `../in/raw/flatcar/raw/105-filesystem.out`.
- **`/etc/skel/*`** → HOLE.
- **`/etc/passwd`, `group`, `shadow`, `gshadow`** → MUST (S2.2-15). Their `-` backups → NOT.
- **`sshd_config`** → MUST. sshd exits without it, and sshd runs per connection here.
- **`authorized_keys` and `authorized_keys.d/ignition`** → MUST (S2.2-15).
- **Host private keys** → HOLE (S2.2-2,S2.2-7,S2.2-15).
- **ssh client settings, `moduli`** → NOT (S2.2-7).
- **`.keep_*`, examples, locks, `.updated`, `.ignition-result.json`** → NOT.
- **`machine-id`** → HOLE (S2.2-1,S2.2-2).
- **`/etc/resolv.conf` and its target** → MUST.
- **`/etc/ssl/certs`, `/etc/vim`, `/etc/cifs-utils`, `timers.target.wants`** → MUST.
- **OEM sysext image and its `/etc/extensions` link** → MUST.
- **Generic `/etc` configuration with unknown contents** → UNKNOWN.
- **Sockets, systemd inaccessible nodes, Varlink registry, userdb entry points, udev data and tags** → MUST
  (S2.2-1,S2.2-2).
- **Generator output** → NOT (systemd.generator(7): units written by generators are removed when the configuration is
  reloaded).
- **Login records and logs** → NOT (S2.2-6).
- **blkid cache, ldconfig aux-cache, journal catalog** → NOT (S2.2-5).
- **Banners** → NOT (S2.2-4).
- **Empty directories other than `/var/empty`** → UNKNOWN. `/var/empty` → MUST: it is the sshd privilege separation
  directory.
- **Other `/run` and `/var/lib` state** → UNKNOWN.
- **Directory rows:** a row whose members all get one decision gets that decision. Otherwise it is MIXED, with the
  split in `reason` and in `part-flatcar.members.tsv`.

Hand-checked ids per rule (from `scripts/samples.txt`):

- `L1:access-rule HOLE` (read only by sshd (S2.2-7) yet it decides what can be done o…): flatcar-bb00b6291ec9cf7304e52e97 flatcar-0bdf73041c7a3ae7fca3aeb0 flatcar-8b8029cbafe7ea635a895b25 flatcar-f7c7fedce0e2f18bdceec831 flatcar-c2ecb15cf6b0b94511e9a53b flatcar-e11dc946353e182416f820ab flatcar-155c77b5a3f4cbe62a885b35 flatcar-c488b0dd3a035637e0c2c96d flatcar-c7cd4ec65c79b30667e89512 flatcar-faa0d984fc169a0430fedf1e
- `L1:access-rule MUST` (polkitd executes the file as JavaScript code; it decides who…): flatcar-00a172f9be4f7fb57422e3c0 flatcar-d53111470b3a1e4a5d1bc7b1 flatcar-15ba5068cd79ebbb2cbfa7c6 flatcar-29b1443a7d9cde03252e5b0e flatcar-77c4aad4b1ed58435970beb1
- `L1:access-rule MUST` (S2.2-15 names open ports, login keys, the right to become su…): flatcar-110d66925baf0a6a1a4bd6f7 flatcar-a907f4e61106ab3b830ee0c4 flatcar-b861218844402b2dfa2ca967 flatcar-e04ac31632b8fb0ca58fa72c flatcar-44c137335a4d9727246bae27 flatcar-0918da7edd64a48b206ff7dd flatcar-944dcf74467877c671f6168f flatcar-c188897f093c5117ff868a85 flatcar-5fbfdeb2e75c8a8fd2ae6155 flatcar-4ef274c21fc9bb60b53020d4
- `L1:access-rule MUST` (the right to become superuser must be recorded…): flatcar-480b364e0b40b0d8496c9960 flatcar-13853be1586d85a3431f6d8d flatcar-d0def0f9090d3e5e462a0e09 flatcar-eac163ea2bf938616e4c57fc
- `L1:access-rule NOT` (shapes only how sshd itself runs its protocol, logs or limit…): flatcar-55ce7a4c373a37e87f1c5ecb flatcar-cde34ae0a06e9c836b514587 flatcar-27deb26d2fe4af2f7297e996 flatcar-f659cb06ab962a0351f51a9a flatcar-227f50458b0ebd69dc62a385 flatcar-b0129c4b9296d9b55bc5be05 flatcar-70171fb23917b95641bb05b4 flatcar-d9080f1b18cd7b9d52ee5bf4 flatcar-27668ef22c0c53aded70245e flatcar-9a331615508f9e7abf819565
- `L1:access-rule NOT` (sudo skips names with a dot, PAM and polkit read only servic…): flatcar-2988e2c9c125829707f86771 flatcar-95a29987a00d50b5e0c6efdb flatcar-37f513275dbc89536b67600d
- `L1:account MUST` (accounts must be recorded…): flatcar-9446ea4c2ea6643ef119fe94-occurrence-2 flatcar-ac20110ce769e4192a4a6be3 flatcar-b0f10a67b85e66452010f1cb flatcar-14982f6f26c34ac0ccfc61dc flatcar-7e5392f811c152a212b09b9e flatcar-a40c56482ad628e59ed33432 flatcar-1ec43cfe3b1053c5baa53feb flatcar-1ec43cfe3b1053c5baa53feb-occurrence-2 flatcar-767928423e022addf55bffa7 flatcar-30782725c151193b416611bc
- `L1:driver MUST` (driver code runs with kernel rights; unbinding or removing i…): flatcar-44bd92356b91b0b47cf8277a flatcar-541edec51d6ad87c14a2bfdd flatcar-e9f177838b9a761d15cf452b flatcar-bc8c732576c2b08f4d089545 flatcar-ccb25ba2988673ebec8ccad2 flatcar-3ec540466dde50c24e4e6a58 flatcar-3d0421dd3fe9ece92d5747d4 flatcar-38e53d99da881f7e44f46688 flatcar-f680f2ced5cbbbb98c0f7e6e flatcar-df01bcfe563b4d2806ab81ed
- `L1:group MUST` (membership gives the right to become superuser, which must b…): flatcar-0f70a3390c41fa2b59c6884e flatcar-a0f0da27341af53b58df6bd9 flatcar-0f70a3390c41fa2b59c6884e-occurrence-2
- `L1:group MUST` (removal drops the login members from the group, so access to…): flatcar-4f9bee274fd71767025c64e9 flatcar-99dccc2b5ae11e3bbbc90ae6 flatcar-4f9bee274fd71767025c64e9-occurrence-2 flatcar-99dccc2b5ae11e3bbbc90ae6-occurrence-2
- `L1:group UNKNOWN` (members are root (unaffected by group permissions) or system…): flatcar-02ebf59a3162d26c558a50df flatcar-9d5f35ad72bf396d264cc47d flatcar-3e7acd7861265a9c89184e3b flatcar-0e24d84385923800dea83498 flatcar-a7245c0c58caf4e0f270123e flatcar-b6f99fb03eecfbb41312f1c9 flatcar-5660feb17732bd3e2d11db19 flatcar-986b4afdeaabbb2011c3a071 flatcar-f7c3c15c9088a1e93c85517b flatcar-6d011a00027adadf3a3b9238
- `L1:group UNKNOWN` (no members; whether a unit, device rule or file grant depend…): flatcar-cfc75235c662052fb431b2e4-occurrence-2 flatcar-cfc75235c662052fb431b2e4 flatcar-8d7d3d230bf2e7ac07fcb476 flatcar-5444af82cd728dc8663d5fb9 flatcar-24624e77c6b9861313861ae8 flatcar-29f1259c13068e383ee9e66a flatcar-bdb33c58f9ef84b3eda8bb79 flatcar-c242b201a2284a2bacd4a5eb flatcar-42b94f5513549dd2f613cc26 flatcar-319d7cfc624b3cd6ffe82242
- `L1:module MUST` (code the kernel executes with kernel rights; removal stops w…): flatcar-7f1899fa1bffaf94112e7ce8 flatcar-e9b69f245750fd6e3417fa44 flatcar-e7c7810e23180e2e4c4621b1 flatcar-cd1afe2cf8a66a0bc2e7d8fc flatcar-c43c1adce6ddc40a62f534c2 flatcar-e230a69fbbc051a901faa6d5 flatcar-5c43b8075926c3cc3bc53f18 flatcar-24cff6cc66e677cae7e467dc flatcar-9a9bfa09927e65bccee92bc0 flatcar-7b8afdbe189c8b2d81d9b6a7
- `L1:network-link MUST` (removing the interface or its configuration stops networking…): flatcar-c6a67a3b1893eff325db70bb flatcar-09fca72ff3a5c7f7c8db554c flatcar-03af7fc8fc60f58774afa3ed
- `L1:polkit-actions MUST` (polkit refuses authorization for unregistered actions, so re…): flatcar-f177842f241084c0fc74e7d7 flatcar-e0997af04e629723b140d669 flatcar-b8f6fbf337e4613292e46fea flatcar-3e98ad3ff39e98db542af611 flatcar-5a2bce5064afe99fabfee054 flatcar-04a3439853aa9599bd9df690 flatcar-2fa8190bd3f76f168878c9d5 flatcar-5fffb0162f0ed61366c27a77 flatcar-3285ba8050719fbaf821ec88 flatcar-4ca6628617b60a596dca2c2a
- `L1:port MUST` (ports open for connection must be recorded; closing it stops…): flatcar-c6a37f7ad7eadbc4acd5dd16 flatcar-c1abfa56a8f1dc6a7b63a838 flatcar-eb410f8eb72c484b4f3618a1 flatcar-2fffc9fd766184f8c9779733 flatcar-763cd0d8c894d815f66a35c8 flatcar-70ed69761e61ccd609f70d98 flatcar-d0a1622131831c067e683bd5 flatcar-95580f2aa9160e767f2e07af
- `L1:process MUST` (a program that runs on the computer must be recorded…): flatcar-55032763f65826e491b088f3 flatcar-64633c534f8105437f520998 flatcar-284cd771182864c383eb7a85 flatcar-f05ee8f3e8364b10957df1b9 flatcar-d0784996137a79baac0fb07a flatcar-97c34088c0761cda1d40a1f8 flatcar-a9acca8e8575bf93b0a201bf flatcar-8185176747a03f9fcad21155 flatcar-c492be43fae992e473e5ae06 flatcar-ba8d8237dfa44ef3a053444c
- `L1:service MUST` (loaded service unit: it runs or can be started; removal make…): flatcar-91a5501fe59caaf866234d6c flatcar-c4b49de6aacd7b5df43159ca flatcar-f5db6b07b72c1baecc961894 flatcar-7ca566af22562d99a36c1a77 flatcar-3be3ebc66a02328cbc1974fa flatcar-5d63c2f4f2c84aa622b62f10 flatcar-12e7e5f8483fd20111e0f61b flatcar-9ecfe389f9eb39cd9410385f flatcar-82b438e9061c3a944e1c771f flatcar-f5e74028b54e6d6b25966e36
- `L1:timer MUST` (scheduled start of a service; removal stops those runs…): flatcar-b1eda66d7e67081774f8ceb0 flatcar-6d3caa2905268b8d64ed1a07 flatcar-6e8dcd63de37fa0391b40c06 flatcar-ee1581dc1254fdbe37316bc4 flatcar-dacbb4dd9598455c3c0e8887 flatcar-ffe62ef38bd1a2097c86a56e flatcar-ad654aeb87b83c1471f2bee4
- `L1:unit-file MUST` (defines a unit that is enabled, startable, an alias or a dep…): flatcar-0a0dfc33687671373fd47b13 flatcar-1d1466ff8c794cfd61be10ca flatcar-c89d41fe75cf8c6fbccfb055 flatcar-5cda9747a42854a1a038b854 flatcar-10e165df73846611af0fbb39 flatcar-0e0e6cd7c41d5d32c774d55d flatcar-68bf92f16f8d9e204b5aa17c flatcar-ad47dc9104503759d20170b2 flatcar-9a5e78d5df470fc79bf0ee37 flatcar-144f3a873b61c0334ea852e9
- `L1:user-service MUST` (loaded service unit: it runs or can be started; removal make…): flatcar-36902b7d91efb89edf0757e2 flatcar-9a7760bb9fcb1500a8579345 flatcar-25d332624af38f3b7a12f31c flatcar-70b2e39fdff6d3dda69ee69f flatcar-905e902eefa63160a0ddd48c
- `L1:user-unit-file MUST` (defines a unit that is enabled, startable, an alias or a dep…): flatcar-f3eeea78985d3ac16b60ca20 flatcar-194640cbe88827831ab4807e flatcar-2e7f92f7feef2b1b03e25a0a flatcar-540adbe06f7170c7e7d89301 flatcar-a8ce43c79b814f572b275c08 flatcar-cfe7cce48a6426db75fd76a1 flatcar-19a0e1d4f8287374c6f606d3 flatcar-641c726f1b5678e738183893 flatcar-2db3435e61f3b7410b61dfcc flatcar-4f99893a5673bd026ad1ab6c
- `L2 HOLE` (not executed in place, only copied by useradd (S2.2-7 settin…): flatcar-e99d01540d33e0f07a650d86 flatcar-20ac2453d5813a360f4d5a48 flatcar-b7763493bf96dc9f0d8a962a
- `L2 HOLE` (read as values by GRUB only (setting); removal breaks autolo…): flatcar-e5869975107dd1606ec51809 flatcar-1d509ff72f6ebda06a74f24b flatcar-7904e536689dfb4920c065e2 flatcar-0e6c4297e1c7ee27ea640213 flatcar-cbb532e843582afa0c475968
- `L2 MUST` (BIOS GRUB (this boot) executes it with full machine rights (…): flatcar-4b4e4471cf5a703812ea458d flatcar-c6184643cea67dae3139d142 flatcar-671910952676415f63149e08 flatcar-28ade5ddfd33bf1d62f088a6 flatcar-53e45b8aeadd239a7b149bb9 flatcar-91648cf8bc33bfac3e62751d flatcar-f6ede53e5ed5b770cbb6aada flatcar-77a646d272b3493e5a5e255d flatcar-40d6712c5b383ea03ed7c8f9 flatcar-b63524de6eeaa857f3aaf7d5
- `L2 MUST` (shell startup files are code the shell runs with its own rig…): flatcar-27a9bbed5ceb9ff7953cd293 flatcar-198385181ff22d0d558e1c21 flatcar-ea39cc839176e502604c2907
- `L2 MUST` (sourced by bash login shells; shell startup files are code e…): flatcar-39b74ce4ac43077561ded8b6 flatcar-d7a371cb24bd93a5b6087625
- `L2 NOT` (grub-bios-setup wrote it to the MBR and BIOS-BOOT partition;…): flatcar-334558d67d5b17a1a48f6580 flatcar-fdce05a11eb6580b746ee991 flatcar-14a05bb2f57c924ebf089310
- `L2 NOT` (machine booted via BIOS (kernel registered vga-framebuffer, …): flatcar-b59146c6ef774b9d1e7896fc flatcar-a9f169a0287b9bcda5746db1 flatcar-a4945760c4931e2ae3f22053
- `L2 NOT` (no runtime GRUB code reads it (only grub-core build files re…): flatcar-a57831f044e17b543418e523 flatcar-85dcb992af130d2188c69228 flatcar-0a3e3cfe3ac4624ab107909d flatcar-772bb06922e0fe319ced9341
- `L2 NOT` (passed to grub-mkimage --config at image build; GRUB uses th…): flatcar-37041f258c25177429d46e43 flatcar-f0f44dff73a1ee2661dd6c9b
- `L2 NOT` (read or executed only by the Xen PV GRUB; this machine is a …): flatcar-914fc60e5e35c78a1f863970 flatcar-34ad325e95cb675633917d4f flatcar-6c8e3d47615b70755164e735 flatcar-8dfa5dc29481add1c8427b0e flatcar-c31f2b878480cef9a39ed1c6 flatcar-b9514664b1b532dcb0be1a22 flatcar-7884a74be5ede6d288711bd1 flatcar-bc9cd5e0582c2cd3c73a01bb flatcar-9561934f5c0219f7cfc9ae15 flatcar-a7800400f790c43f9639d085

Rules matching a single row (for example `vmlinuz-a`, `/oem/grub.cfg`, `/etc/machine-id`) and all directory rows were
decided row by row. Their reasons are in the output rows.

## Questions for the author (not decided here)

- S2.2-7 scope: is a setting read by one program "in force only inside one program" when it decides what can be done
  on the computer through that program? Examples: sshd forwarding, GRUB autoload lists, useradd skeleton. Reading A:
  NOT. Reading B: MUST by S2.2-2.
- S2.2-15 names keys to log in to an account but not server host keys; host keys are HOLE here.
- S2.2-2: does a value that is regenerated with a different content on removal (`machine-id`) count as the computer
  "stopping doing something"?
