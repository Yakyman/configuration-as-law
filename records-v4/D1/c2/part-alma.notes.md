# Classification c2, part alma: rules and notes

Output: `part-alma.tsv` (6293 rows; one per input row). Script: (not published: orchestration or scratch) (reads only `D1/in/`
and the setup source fetched to (not published: record outside selected evidence)). Per-member decisions for MIXED group rows:
`raw/mixed-members.tsv`. Per-member facts for stored groups: `raw/members-facts.tsv` (built by
(not published: orchestration or scratch)). Hand-check samples: `raw/handcheck-sample*.txt`. All times UTC.

## Facts established before the rules

- **Ownership after usr-merge.** The rpm file list (`raw/raw/0019-package-files-rpm.out`) records many
  paths as `/lib/...`, `/lib64/...`, `/bin`, `/sbin`; on this machine these are symlinks to `usr/...`
  (`raw/raw/0004-filesystem.out`: `/lib -> usr/lib`, `/lib64 -> usr/lib64`, `/bin -> usr/bin`,
  `/sbin -> usr/sbin`). The inventory did not resolve these aliases, so 666 "unresolved" stored groups
  (all of `/usr/lib/modules/...` but one) consist only of package files. A member counts as "as received"
  when: file - in the rpm list as a regular file and `integrity=unchanged` in `package-files.tsv`;
  directory - in the rpm list as a directory with the same permission bits; symlink - in the rpm list as a
  symlink with the same target (`target` in 0004).
- **Package transaction window.** ctimes on the disk cluster at 05:52-05:54 (122k entries), 25 at 05:55,
  1385 at 05:56 ((not published: orchestration or scratch)). Kernel posttrans (rescue initramfs 05:55:34), file triggers
  (`gschemas.compiled` 05:56:06, `icon-theme.cache` 05:56:07) belong to the rpm transaction; the installer's
  own configuration follows (05:56:13 `/etc/sysconfig/kernel`, 05:56:14 `/etc/kernel/cmdline` and
  rewritten BLS entries, 05:56:17 `default.target`, `firewalld/zones/public.xml`, 05:56:18 `ens3`
  profile, 05:56:57 `sudoers.d/lab-access`, `anaconda-ks.cfg`). Every enablement/alias link under
  `/etc/systemd/{system,user}` except `default.target` has mtime 05:52:39-05:54:22, i.e. made by package
  scriptlets/presets during installation. The authselect output (05:54:16) and the dconf databases
  (05:55:35) also fall inside the transaction.
- **Ordinary actions** (`control/alma/d1-alma-operator/actions/ordinary.sh`, `alma.sh`, `firefox-addon.py`)
  establish what the person did: npm `cowsay` (global, prefix (not published: record outside this collection)), pip `marionette_driver` into
  (not published: record outside this collection), Flatpak `org.gnome.Calculator` (user), Firefox profile `cal-check` and
  extension ClearURLs, `git config --global color.ui false`, user unit `cal-user.service`, nmcli
  connections `cal-secondary` and `cal-test`, (not published: record outside this collection), rootful `podman run`.
- **pip/npm files unchanged.** All 512 entries under (not published: record outside this collection) have ctime
  11:17:23.157-11:17:23.410 and all 682 under `cal-marionette/` 11:17:33.9-11:17:34.4 ((not published: orchestration or scratch)),
  i.e. nothing changed them after the installing command (a content or metadata change sets ctime, inode(7)).
- **setup's shipped passwd/group.** (not published: record outside selected evidence) holds the CentOS Stream 10 dist-git of `setup`
  (https://gitlab.com/redhat/centos-stream/rpms/setup) and its source `setup-2.14.5.tar.gz` from the
  lookaside (sha512 matches `sources`). `shadowconvert.sh` (run in `%prep`) replaces the password field
  by `x`; `add-clock-group.patch` adds `clock::103:`. The installed setup is 2.14.5-7.el10 and the shipped
  passwd size (575) equals the converted source size.
- **dnf reasons**: `explicit` = dnf `user`; `dependency` = dnf dependency or weak dependency; 261 rpm rows
  have native reason `group` (selected group/environment); 1 (`gpg-pubkey`) has none.
- **Python/npm packages with `native_package_ids`** (242): every package-file record under their metadata
  location is `unchanged` ((not published: orchestration or scratch)).
- **polkit**: all 45 files in `/usr/share/polkit-1/actions/` are package files, unchanged; there is no
  `/etc/polkit-1/actions`.
- **Processes**: 1238 of 1280 have exe `unknown` (`readlink` failed for the collector,
  `raw/raw/0211-process-executables.sh`).

## Rules applied by the script (each checked by hand on the listed ids)

R1 rpm packages (S8.2-7, S8.2-8, S8.2-16). Q1 first clause: a package installed on the computer. dnf
`user` -> INSTALLED-OWN; dnf dependency/weak dependency -> INSTALLED-DERIVED ("a package installed as a
dependency of a recorded package"); dnf `group` -> INSTALLED-DERIVED (S8.2-16 "a line from which the
system itself built or obtained it": the system obtained it from the selected group/environment);
no reason -> UNKNOWN.

R2 language packages shipped inside an RPM (S8.2-7 second clause, S8.2-16): obtained as part of that RPM,
files unchanged -> INSTALLED-PACKAGE.

R3 user-installed language/application packages: the one the command named (cowsay, marionette_driver,
org.gnome.Calculator) -> INSTALLED-OWN; the others in the same tree/runtime set -> INSTALLED-DERIVED
(dependencies installed with it; npm nests them in `cowsay/node_modules`, pip installs requirements,
flatpak installs the runtime and its extensions).

R4 processes, ports, sysfs module/driver entries, nftables tables/chains/rules, systemd load/active states,
timer elapses, `sudo -l` lines -> RUNTIME (S8.2-5). The reason names the creating program and its
decision; where exe was unreadable the program cannot be named, but every value gives RUNTIME.

R5 polkit actions and access-rule files obtained with a package and unchanged -> INSTALLED-PACKAGE
(S8.2-7, S8.2-8: "default setting values"). `/etc/sudoers.d/lab-access` (no package) -> SETTING-OWN.

R6 unit files. The row is the unit's enablement value (S8.1-11, S8.2-13). `static` -> no enablement value;
the unit file is a package file, unchanged -> INSTALLED-PACKAGE. `alias` shipped in /usr/lib ->
INSTALLED-PACKAGE; alias link in /etc made in the transaction window -> SETTING-DEFAULT; alias only in
/run/systemd/generator -> RUNTIME. `generated`, `enabled-runtime` -> RUNTIME. `enabled`/`disabled` equal to
the vendor preset, and `indirect` -> SETTING-DEFAULT (S8.2-17). Individually: `cal-user.service`
SETTING-OWN; `vgauthd.service` SETTING-DEFAULT (link `vmtoolsd.service.requires/vgauthd.service`, 05:53:44);
`rpmdb-migrate/-rebuild.service` UNKNOWN (disabled while preset says enabled: nothing records who left it so).

R7 accounts and groups (S8.2-13). Record identical to setup's shipped file -> INSTALLED-PACKAGE (Q1 comes
before Q3; S8.2-8 "default setting values"). `wheel` (member `user` added) and `user` -> SETTING-OWN.
Other system accounts/groups -> SETTING-DEFAULT (created by an installed package at its installation,
S8.2-17). Only the passwd/group records were captured; shadow entries were not.

R8 stored groups (members file per row). Each member is decided, then: all equal -> that decision;
otherwise MIXED. Member rules, first match wins:
- in the rpm list and as received -> INSTALLED-PACKAGE;
- on tmpfs (`persistence=runtime`) -> RUNTIME, creator named by subtree;
- `/etc/systemd/{system,user}` links and `.wants/.requires` directories made in the transaction window ->
  SETTING-DEFAULT; `default.target` (05:56:17) -> UNKNOWN (installer);
- an explicit path table in (not published: orchestration or scratch) (`MEMBER_RULES`): copies/builds that are code (GRUB modules
  and core.img, rescue kernel, initramfs, `00_tuned`, skel copies `.bash*` identical to bash's
  `/etc/skel` digests, pip console scripts, V8 and Firefox script caches) -> PROGRAM-DERIVED
  (S8.2-9, S8.2-16, S8.2-23); caches, logs, state, backups, generated indexes (depmod `modules.*` which are
  rpm `%ghost` paths with no digest, MIME/icon/font caches) -> RECORD (S8.2-15, S8.2-23);
  alternatives links/state, microcode links, policy modules in the SELinux store, compiled dconf
  defaults, `gschemas.compiled`, authselect output -> SETTING-DEFAULT (made by package scriptlets/triggers
  during installation, S8.2-17); files written by the installer's configuration step whose value a person
  may have chosen in the (not captured) recipe -> UNKNOWN; person's network profiles, sudo rule,
  `authorized_keys`, user unit -> SETTING-OWN; downloads -> MATERIAL; `cal-user-script` -> PROGRAM-OWN;
  the installed extension `.xpi` -> INSTALLED-OWN (S8.1-5, S8.1-6);
- pip/npm package files whose ctime is the install moment -> INSTALLED-PACKAGE;
- directories not in any manifest: made by the person's `mkdir -p` in the actions -> MATERIAL; otherwise
  -> RECORD (Q1 does not fit: the directory is not part of the package's file list; Q2/Q3 no; Q4: written by
  a program as it ran).

R9 L2 code rows: package file under an alias path -> INSTALLED-PACKAGE, otherwise the member rules.
L2 images: package file -> INSTALLED-PACKAGE; boot code built by dracut/kdumpctl/grub2-install ->
PROGRAM-DERIVED.

## Rows decided individually

`sudo-access` (9), `port` (9), `saved-network` and `saved-network-file` (8), `container` (2),
`container-image` (2), `image-container-store` (3), `timer`/`user-timer`, the unit exceptions above,
`wheel`/`user`, `gpg-pubkey`, and all 23 MIXED rows (members in `raw/mixed-members.tsv`).

## Readings applied (for adjudication)

1. dnf `group` packages: S8.2-16's general clause ("a line from which the system itself built or obtained
   it") covers a package the system obtained from a selected group line -> INSTALLED-DERIVED.
2. Directories not listed in any manifest: Q1 "obtained as part of such a package" would need "or created
   while installing it"; Q4 fits literally -> RECORD (or MATERIAL when the person made them).
3. Container `cal-container`: its configuration is read as values (S8.2-23), obeyed only by podman run at
   the person's will, and it launches a process -> SETTING-OWN by S8.2-14. Image: podman's documentation does
   not describe it as installing programs (S8.1-4), so not a package; code (S8.2-22) obtained by the system
   from the container's line -> PROGRAM-DERIVED.
4. `sudo -l` lines are rights computed by sudo while it runs -> RUNTIME, belonging to `/etc/sudoers`,
   the wheel membership and `lab-access`.
5. Opaque stores (`expanded: false`) holding several kinds of objects are reported as MIXED with the
   kinds named, because the store is not one object.
6. Installer-written values (ens3 profile, `/etc/kernel/cmdline`, `/etc/sysconfig/{kernel,network}`,
   BLS entries, `grubenv`, firewalld zone, `default.target`): the recipe content is not in the inventory
   (`/root/*-ks.cfg` contents were not read). Chosen by a person -> SETTING-OWN; installer default -> not
   "a value chosen by a person". Recorded as UNKNOWN with this fact named.

## Hand checks (10 ids per rule or all rows if fewer)

Each id below was read in input and output side by side (`raw/handcheck-sample*.txt`); every one fits its rule.
- `L1:access-rule` (10): alma-5f408bc081af8550b7f562f0 alma-663ed09ee4e3481f10948ea3 alma-b757d425afa1c40fee02272f alma-ae0ae63bcff8098fb66381dd alma-06afd1d80a7e402d5ddd3f64 alma-ab1bf5e61fb603f2bdd197a9 alma-14344435a85c82bd18168f9e alma-a64abca9bb1581657a0acb63 alma-63a48864e0946a2f04254529 alma-12be01350933aeecf40f4d3a
- `L1:account` (10): alma-106a6c34cca11fa1251f6f87 alma-32aefb7b1a685c8f5c72b70d alma-c84d4346e3f2284453ab0b62 alma-0047744d514007858597b3fc alma-ed4f61c09832e1f1e99f0f6c alma-448646fafcede98990f077af alma-64d442354dc245386b748937 alma-f2a49fc92129b682d23e5a37 alma-71966c5e14f6b1d3115de310 alma-4ac7de7bcefdd55c4543d13e
- `L1:driver` (10): alma-64ef392521700197aa1cde6a alma-6b142d762c6a6a29c25d7fe1 alma-a4d7ede6991bff951ae7e775 alma-a012692612f170b27eae158b alma-0283946602ba408b0c1ec948 alma-f58a2ea7ef5b0ba5207dc0a6 alma-9ee5d285b0170478745da9d8 alma-0c69c5f6aaa71f9605b9241b alma-907fff851500b49838d0295a alma-f8d52efb58b9be84b4564b2e
- `L1:firewall-chain` (10): alma-4c09961dc1ad6649c83e4a73 alma-d95b886a2678efe57878244d alma-0b07368ad9eb349620c59132 alma-0ea736c89afe6380e6acce3f alma-2a913c9e708e3f03eebec634 alma-82e0084fb701c9c108e0239e alma-03e8f6d27a77ee312e7e0676 alma-362756f90afb6079467dc133 alma-95e64c79dad202e3092edf76 alma-55d70bc0461faa64054ebe2d
- `L1:firewall-rule` (10): alma-8747babd18ee3f3179dd8c50 alma-d9253a95d4a20f890ade4251 alma-ad706c157d772a8ef7ffd2cd alma-637f76c3070818ee059eef52 alma-823b3e11341d91647d428ff2 alma-3fb9518c8abb04db8f8acb55 alma-90d5d1ead45a039fa3eac00a alma-071d75f197f0242f3041c63d alma-70771bbf68d66fcff6fc4955 alma-15d8c54b3aa654e135e330ff
- `L1:group` (10): alma-54956ae2303ee3c782ccc5c7 alma-d908962ffab30046eab5a388 alma-e41687eeae0430810cd909a8 alma-b2d7c89996c6643ffb3ea0d1 alma-7dfc29a5f91593f28b385a8c alma-a73a3e918691339df34e3f8a alma-66ff73459d6da4b27c218efa alma-48c62b69877687f362686592 alma-b82ccdef02f31567f709f637 alma-b235986631e93601ba5b4b7c
- `L1:module-name` (10): alma-e954c8d31c96c2119b50495c alma-a748f8364f8d1d0610c09552 alma-a16100128ec51ea7dc23723e alma-ee1aea40084f10c543078f06 alma-c51f8db1cb33c4054581cb32 alma-82bf4ef156e8b7a3761fa261 alma-9d801d871690a60e668ac4ae alma-5b7bcad82d0ca6ee6e6deb21 alma-ae969f7e4adb46b98f057e94 alma-0b81fc9ad7e1a078a37e337f
- `L1:polkit-action` (10): alma-a860e4e90172eca0a66c8897 alma-1b30a2eef1364d7c2b2a56f7 alma-765fb469f2c1589991951b7a alma-a1644b54d4f0ee649012d078 alma-d946e0dce8f3c512813d7308 alma-8baad71b1e033049c43311fe alma-6ba80194fdd57dee9418d3ec alma-c00fd038da1a9e1c6d91b5e2 alma-dbbf39cb99d1a8633e057076 alma-7857843c71756fe2432755a0
- `L1:process` (10): alma-b518ef58549934e0332bd2c9 alma-c62a96981116ef78f29976e5 alma-732f8d9acee562939baa392b alma-462a81c1045f81b270d782a9 alma-2ed13ea8b4febbcda967ed3e alma-2b50946909df541374dc8581 alma-7e8874731ca5488bb0f23a0a alma-0962589467f296e0b2d8c7ae alma-76cb768ee8954c11959f5cfd alma-4c567d6b22c71f900e8fcc1b
- `L1:service` (10): alma-60802f02d5ade1d176b45c54 alma-e242cb0c5954f135249da8dc alma-dd6019006ad230a8d618e135 alma-b273a6fe06297afc598c4647 alma-a47a730d015bad403629919a alma-725fc7b3daec24a66963bfaa alma-97632eb7ba997c047c22a4e6 alma-c0411eed574d1c9e19fb3d05 alma-454c6b120d5090ab03a09514 alma-5aa457fc750047b02dcd6f96
- `L1:timer` (7): alma-261a7a3a90e36b704dbc7001 alma-31f01d5991193d82156273f0 alma-929c4159e2f3d0a81f68b64d alma-02e882963b0a187029ce4d0f alma-6f09e788229a52376c55f438 alma-41b45830fd2058744acb420f alma-5050a712c0f7de93aa46a2d0
- `L1:user-service` (10): alma-62fc9f9a3458c3bda3e6d31b alma-432b959ef45e60a45447c024 alma-0a6f77c8ec70cf4910637674 alma-8139ef69281009a3ce58a19f alma-e1572d027ebea4d400cc3726 alma-b6093b5640fe4e04a3bcbe2a alma-6b417793212e3a4cea4b3d12 alma-4c27ada6e462646ba666c90e alma-45d3a4efc5b521894f205604 alma-591bf9e27277984924761a90
- `R12-stored-INSTALLED-OWN` (1): alma-2ea4b9f74eb9ce06f9d317ff
- `R12-stored-INSTALLED-PACKAGE` (10): alma-2460bb20b5b68447d0e285c8 alma-5e08070a4e03ba3d54f0797e alma-6445e96dd324fa98aa08a7db alma-8eaaa8ce6928c2d10f0532ab alma-06ae721e33c49429fef097b4 alma-dbea6d3a9bef22576a11a43f alma-8c678d588e270243a1c45a70 alma-73c66ec99ed598ce6d265fd3 alma-5bd0d1230301c9d25fe2d592 alma-04cb22f01964553fe20c2372
- `R12-stored-MATERIAL` (3): alma-c605f21df76c759160940695 alma-042cb4cbb0e4f47fccd33163 alma-baf76d61c6ad95e30e863125
- `R12-stored-MIXED` (10): alma-02565ed2145d532039503ede alma-0775bdced8f5e336e1899de5 alma-c83f99622553a56e7b5bad36 alma-f436dd1c81663a6be2feb765 alma-3d21e04a8d06b030e2bb4f02 alma-a647fcfdbb97b91e83721827 alma-af27daed7a703d9138e44c5a alma-babf6a10543af22e535e0c4e alma-a21b5980f2d69a44b6509823 alma-ad9fb12eeb027086dae92d57
- `R12-stored-PROGRAM-DERIVED` (3): alma-70de7fc7f553163fc60718af alma-383dc4644881a5acdc97817a alma-b00aa976d81ff928ec33f54c
- `R12-stored-RECORD` (10): alma-38ce2ed4ed0b2618485457a1 alma-da426c047078d79b69116b85 alma-d3c38c836744f93483b34a4b alma-3258ae3d5f26d765ddd4f18f alma-53242fc87d6f5938c40b3e59 alma-1924e7e7c98621387285db92 alma-dcf033b7880be5ebaf8f0cfe alma-e0b9a5a60bbeb8375a158b68 alma-6990321f35168eb2d918e4a0 alma-083ec27a7ce94aac68b52a9c
- `R12-stored-RUNTIME` (10): alma-7d3b25b913ddd47068b2dbfb alma-d7d4d6f74925956d5296154e alma-61f1eb28c19ef6c2bb547ac2 alma-a7a98e456112106bcaa35153 alma-abc3e1d04735ab930a624c37 alma-2ab87cb73cbd2e087708bf95 alma-2b524c3fe7d3ff0909e02508 alma-6253ca1def2105a53e86eddb alma-75478788402be8c7b6967a4a alma-5b633e93a260cc6e4bb12437
- `R12-stored-SETTING-DEFAULT` (10): alma-a2a4dad76ebf3ae13a87aecb alma-130bd3c32242f60379fad449 alma-dfbbec8c0f7d667d72597960 alma-e4dd63f73ebe8ee244c10cd4 alma-2598e57f0f6bff95725398e9 alma-37a6b00f2a2f30cc17fdc85c alma-3d942f05d6c68541a4a01fd0 alma-2b25403fe7f9aed63ba0c09f alma-b9f1455d007149f01ba5d60c alma-7753d30a8947c87d83d747be
- `R12-stored-SETTING-OWN` (4): alma-9b55d85b3e8beb263c1f1957 alma-436688690a5e6cf085aad702 alma-0684819f2449b7aed3e871b5 alma-1fdc6107b61543ccef8bb780
- `R12-stored-UNKNOWN` (4): alma-5bafee22bc69b6fb7e9b4c37 alma-dab39645202d97d80dcf72f3 alma-894535cc1ce55c243421555b alma-6417296a51f56e3cd1211479
- `R1-rpm-dependency` (10): alma-debca842b44e987a7cb79790 alma-a9c9a3ce44ebc606ea42ab1a alma-54faa1b7b68d434983134795 alma-d0b30ed1231ee9799bd5f13f alma-49c08c071606f5414e5dc1f9 alma-28c983ae40efbe8b2251b3a2 alma-5afa4c0a0dce696bd17e557b alma-5f8a03dc580ee00aa6783bc9 alma-36dfd42418275f7e8b7f3dd6 alma-e744c9ad937836b534717789
- `R1-rpm-explicit` (9): alma-be4c32ab04af87c5779a4749 alma-0bf4bac5d7339175cef0fcc4 alma-e7c6fc3e717bdc39acbe0e65 alma-b3424c7b994bde3ef591023b alma-428e5a4f2a5fc06ec88be098 alma-d4c310682a69ef1b1b34efcb alma-8382f1a398a03ad8fa7f7a63 alma-b13ee5598b7640875532d838 alma-94dfeac4d8730bd5b75b6398
- `R1-rpm-group` (10): alma-256f67c2627763211ad1ba4e alma-0da44fbde036825a912256ae alma-ba2ca7c592f696045b77c0c3 alma-c3d2fc7fa39bf083647d7034 alma-f3ec2ec0443045577ca9a0cb alma-80290065bf5a3054a1cadcf7 alma-a56ad6dc630cd07c19141811 alma-c6d7da6ee972fcb077356d13 alma-068c161c655a3865697f8c95 alma-0ae548da607a8b7b6c8a3b40
- `R1-rpm-unknown` (1): alma-61c67b50804440435a6bc944
- `R2R3-lang-flatpak-user` (5): alma-beac6397c176f674bd20a66c alma-43a1261dbd85bcb7f04d936d alma-a57f38f6b78a000a07a15024 alma-4426938d9cfaf66a2d7f76ac alma-77ccb9a9685c546ff4b596ea
- `R2R3-lang-npm-inrpm` (10): alma-a046b023b85549e505a7eee3 alma-5451e374439ccf1930b423ba alma-a1e1283243706c4551e5d5c7 alma-628130e90d4f6924e66ed983 alma-f572ebfd27b78c67f240bd24 alma-99d3c9a0b9fb1b83da0ddbb5 alma-45e3bd83b5fd6bb666dddc64 alma-19ba7f6964d5347c3ee86b34 alma-879fddcd8927f91c1c196ebb alma-c6ebf3ccdbbefbf85189e520
- `R2R3-lang-npm-user` (10): alma-63e52383e16c3cb876b4fac5 alma-51979b9787b54c773380118d alma-a07c86c4290f7922affee999 alma-918df928c73b67bddbc6dee3 alma-e2db7c96951e6e9d00df8cd4 alma-07938f91d3cc710bf5bbf3f0 alma-dca0a538df1f2f78d1e2ae88 alma-fc0ab776a17654724c93d521 alma-4960644711ce1ac9111b5c99 alma-322ac306bc90a97439565b83
- `R2R3-lang-python-inrpm` (10): alma-c068992fc9d59026f796decc alma-1f13e5d5fde8f28562017c50 alma-9c23ebcd29c06347fc2c9da3 alma-16f4db58c56fc8ac377ebaf6 alma-7736d3ec069bcaf04bf71919 alma-f620e45c5f534d79f98b0a79 alma-cdc11f2102fb81dad50de13a alma-26f877d895aa69dba5d2ed14 alma-2a694362ec3cd66b8c4cb755 alma-b807e07aedb6ccb5f20276dc
- `R2R3-lang-python-user` (10): alma-afbb55e45941dbf71aea7846 alma-7d6e6f5f07c76142e3708452 alma-5e792ad7daa2de59dfabb7dd alma-c9bb0ec522288aabf4ffe0fd alma-ecd06cbb22d0bef5d632150f alma-b321ebb1d8d25e3ff86b1922 alma-2478b390d4b644352dc24f74 alma-6abd4427a1ad9fd362febeeb alma-4d28c424ee4ade8ada6f7e37 alma-7f428fa2591f062abaa11a62
- `R9-unit-INSTALLED-PACKAGE` (10): alma-be7346e476646c24f0e06940 alma-f23a7e02a71b8834d29958cd alma-3f656e5156eac0ce8b8d5b16 alma-5521631eae0eb4b3e22bbd87 alma-c441a1684777150b8b26f3a5 alma-bac10e10ac5192ab0bd76402 alma-39fd838b80d6aa4714f789b9 alma-adfb4cd80627d9400946a86f alma-fbc46ab5260439832074c2f5 alma-e4ca8583bcb32199fa7b3be7
- `R9-unit-RUNTIME` (10): alma-8898645dca3b62ddb2105752 alma-acd8b737aa3042ae900d4f9c alma-d32fe613a6f6d8415791f199 alma-00db3c1558544f64741d6b8c alma-4470550b14a38af750fa56ec alma-681a12c25d037c20fee1a21b alma-5686d686dcf011ae61a55765 alma-448485c93c45a4d564aa0e32 alma-6aae5cb6ed514c755e95a947 alma-b003b3b06adec97cd9c072d1
- `R9-unit-SETTING-DEFAULT` (10): alma-5a4ac8b90836834cfc244333 alma-d1a38487c268c66e3db360f5 alma-b6ce86bcee88298ac0f67fcc alma-c88a39c886e1c4850847f27d alma-c0617e7f68c160c19e1a1386 alma-9542ca24f09085db6db474c3 alma-8cf9b5f0b770d635edbeba9f alma-88c0f40b80186b45928773bf alma-367ce6094cc5cd99fe778ad1 alma-6446b595d5390e3decd13d0b
- `R9-unit-SETTING-OWN` (1): alma-da3f264207304e46c5f26236
- `R9-unit-UNKNOWN` (2): alma-15147e7885ba0fa16cd90853 alma-5979198b1523e9e8195df68e
