# D1 c2, part tumbleweed: notes

Input: `../in/part-tumbleweed.tsv` (6779 rows). Output: `part-tumbleweed.tsv` (6779 rows; verified by (not published: orchestration and working notes)).
Counts: MUST 6213, NOT 218, HOLE 348, UNKNOWN 0, MIXED 0 (`part-tumbleweed.done`).

Decisions use only Section 2.2 and indicator S3-1/S3-2. Nothing was removed anywhere; the removal test (S2.2-2) was
applied by reasoning from what each object does.

## Sources for "what the object does"

- Inventory evidence and files under `../in/raw/tumbleweed/raw/`.
- RPM packages: the public openSUSE Tumbleweed repository metadata (primary + filelists),
  `https://download.opensuse.org/tumbleweed/repo/oss/repodata/`, read on 2026-11-22 (one day after the inventory
  release 20261120). 2385 of 2386 package names were found (`gpg-pubkey` is not a repository package). The extract
  (name, summary, full file list) is kept as `raw/pkginfo.jsonl.gz`; per-package category and first matching file:
  `raw/rpm-cat.tsv`; non-code packages with their files: `raw/rpm-detail.tsv`, `raw/manual-view.tsv`.
- `xorg-x11-driver-video`: the package's three `xorg.conf.d` files are fully commented out (`raw/xorg-x11-driver-video-confs.txt`).
- Documentation cited in rows: NetworkManager 1.42 release notes (loopback configured without a profile); systemd.generator(7)
  (generator output is recreated on every daemon-reload); polkit(8); dracut (not published: external working record) (installs
  NetworkManager's own initrd units into initrd images); KDE ECM `ECMQtDeclareLoggingCategory` (categories files are in
  KDebugSettings format; KDebugSettings is not in the rpm list); the selinux-autorelabel spec (generator and relabel units).

## Reading of "NOT" when no exemption names the object

S2.2-1 defines what must be recorded; P1 (S2.3-4) requires only what "must be recorded under Section 2.2". An object
whose removal changes nothing the computer does or can do is outside S2.2-1, so the text does not require it: NOT, citing
S2.2-1, S2.2-2. The exemptions S2.2-4..S2.2-7 are applied as stated ("need not be recorded").

## Rules applied by script ((not published: orchestration and working notes), templates in (not published: orchestration and working notes))

| Rule | Objects | Decision | Sentences |
|---|---|---|---|
| account | L1:account | MUST | S2.2-15 (accounts) |
| access-rule | sudo rules `(ALL) ALL` | MUST | S2.2-15 (right to become superuser) |
| firewall-rule | nftables rules | MUST | S2.2-15 |
| firewall-chain / table | chains and the firewalld table | MUST | S2.2-15, S2.2-2 (hold and hook the rules) |
| port | listening sockets | MUST | S2.2-15 |
| group | group entries | MUST | S2.2-1, S2.2-2 (carry access rights; names resolved by units/rules) |
| polkit-actions | action declarations | MUST | S2.2-1, S2.2-2, S2.2-13 (used by polkitd and the mechanism, so not one program) |
| module | loaded kernel modules | MUST | S2.2-10, S2.2-2 |
| driver | device-driver bindings | MUST | S2.2-1, S2.2-2 |
| process | running processes (incl. the inventory's own shells) | MUST | S2.2-9 |
| service (loaded) | services active or startable | MUST | S2.1-3, S2.2-9, S2.2-2 |
| service not-found inactive | names referenced without unit file | NOT | S2.2-1, S2.2-2 |
| service not-found active exited | completed first-boot SELinux relabel oneshots, unit files gone | NOT | S2.2-1, S2.2-2 |
| timer | system and user timers | MUST | S2.1-3, S2.2-2 |
| unit-file | enabled/disabled/static/indirect/enabled-runtime unit files | MUST | S2.1-3, S2.2-2 |
| unit-alias | alias names (D-Bus activation, display-manager, network) | MUST | S2.2-2, S2.1-3 |
| pip / pip3 / gem | Python distributions and Ruby gems | MUST | S2.2-10, S2.2-2 |
| rpm-bin | package ships an executable in bin/sbin/libexec | MUST | S2.2-9, S2.2-2 |
| rpm-lib | package ships a shared object (no executable) | MUST | S2.2-10, S2.2-2 |
| rpm-script | package ships .py/.pm/.rb modules | MUST | S2.2-10, S2.2-2 |
| rpm-FIRMWARE | kernel-firmware-* files | MUST | S2.2-16, S2.2-2 |
| rpm-doc | only documents or license texts | NOT | S2.2-4 |
| rpm-META (patterns) | pattern packages holding one description text | HOLE | S2.2-1, S2.2-2, S2.2-4 |

All other rows were decided row by row: 352 RPM package names in (not published: orchestration and working notes) (name, template, what it does,
from the file lists), `gpg-pubkey` (repository signing keys: MUST), the five network profiles, the eight Flatpak refs,
the container and its image, the seven generated/transient unit files and the three masked-runtime unit files.

## Hand check of the scripted rules (10 random rows per rule, fewer where the rule has fewer rows)

Rows and their evidence are listed in `raw/spotcheck-samples.txt`; each was compared with the rule by hand and fits it.
IDs:

- access-rule: `tumbleweed-e55fa16314dd42978bb4d9dc`, `tumbleweed-71fa379da109c0a4b248ec44`, `tumbleweed-e95a02bb8e22aa56aed4066d`, `tumbleweed-46ccb95936c821188da69e15`
- account: `tumbleweed-cd0f3b3a6ccab31025140aeb`, `tumbleweed-c7cf6cddd02d97c5fbe5cd90`, `tumbleweed-9c539b4f426a9c8635cbfb38`, `tumbleweed-aa127faf1be6c7071d4193c6`, `tumbleweed-d75ec6e7d9650fc3be6a914c`, `tumbleweed-36da60582c8b4e5b33be0e77`, `tumbleweed-e75c0b0bf5aaf22630e5f3f5`, `tumbleweed-1a8c4213c64502604d5d206b`, `tumbleweed-22ca45c25bed95776c034ed4`, `tumbleweed-cf1c8960eb5905508e385d35`
- driver: `tumbleweed-44b9710dc4448d2b295d9396`, `tumbleweed-22353892b03a9daca64bef10`, `tumbleweed-5a7de061b10cdc1561847a8e`, `tumbleweed-56e8f4d0d304f1bad5cb7728`, `tumbleweed-075810a1d64af51e9d579551`, `tumbleweed-a7ba9d182fcc6f88a6e7680d`, `tumbleweed-aee799cb00bcc80ec18d561a`, `tumbleweed-0ee3a86fdd2779fdcb1d1c46`, `tumbleweed-5e5853b382ea0e8c6f9a5289`, `tumbleweed-254acfbc38b48dd263d145d7`
- firewall-chain: `tumbleweed-e44f0a48fe137b939ddbc5cb`, `tumbleweed-7324d1d70b57deb5d1bc03cd`, `tumbleweed-18ed12f1f12078bffad8c06e`, `tumbleweed-3366149c1bf5b9b6ba227492`, `tumbleweed-959f615abb732bbc17f180c6`, `tumbleweed-6cb898cf645819eef3fa4a00`, `tumbleweed-4644bd571d0ed414625ad015`, `tumbleweed-892fa0a17b0f0c37e5f79071`, `tumbleweed-38fde7d00ba6b7abe9aac4c2`, `tumbleweed-fb2a1f64053b324f1d243bfd`
- firewall-rule: `tumbleweed-99d001d757ab5fcfd3714237`, `tumbleweed-743bd8de4e9b1373934aa8f7`, `tumbleweed-12c30ebbf5a976db6d610550`, `tumbleweed-a41dba85163a537dd24b8a74`, `tumbleweed-72c2641a1aa11bd53002efe5`, `tumbleweed-d4f5f92874f05d68afa41fb6`, `tumbleweed-552ea430853759c46dd7d18e`, `tumbleweed-d6b59c14d0a37eaaa6d9e8c0`, `tumbleweed-193f6decb40ba357e64b3ea4`, `tumbleweed-bacb5a5f42427e01c1f6cc31`
- group: `tumbleweed-927e65070463ed5e1c1621a5`, `tumbleweed-0c37af051268bd769de241f3`, `tumbleweed-2d6d7f8259f4060819d145e1`, `tumbleweed-911b87d49d566828d0354673`, `tumbleweed-3e74d8370c58cbaa32698f3a`, `tumbleweed-f624f601a38fee776be43d1a`, `tumbleweed-1378325ce7b713cfae9a45c3`, `tumbleweed-65cf0103a122a0414f06e804`, `tumbleweed-134367a9b232485936c6c738`, `tumbleweed-ab89538c092a354a7a392ab4`
- module: `tumbleweed-f3e889153ed4c24db9fd7798`, `tumbleweed-8a676fc4c576d4af060cd7de`, `tumbleweed-52ec0f5162743fdc4b2e9f66`, `tumbleweed-47c87d8630c9ab5b81cf6611`, `tumbleweed-3d953105c5fc23ab4bc4c838`, `tumbleweed-c0782ea86863b653c84d6e11`, `tumbleweed-1fd97c95e78160d7206473ad`, `tumbleweed-b85d0367d337c4109867f469`, `tumbleweed-92a9dee6a35f48521839ee1b`, `tumbleweed-dd94169d7720478b6085af45`
- package:gem: `tumbleweed-0e0cef699f6476577578c11a`, `tumbleweed-8044772b11c078f1a10054e8`, `tumbleweed-552492d50339a28be20781b9`, `tumbleweed-1085f898e112c30b6811a779`, `tumbleweed-bf4f41629bc727245f9088eb`, `tumbleweed-6da2d0ab4a542eb062999998`, `tumbleweed-2238738718a8af193683ec15`, `tumbleweed-c94e7fd1c76ca5cc7d533392`, `tumbleweed-9878bcd1204a3c86a1e64b74`, `tumbleweed-4c2966f6977630fa60640622`
- pip: `tumbleweed-e2bd5999eca591661b5a97d1`, `tumbleweed-2bf84c7062774098917d5c1e`, `tumbleweed-6efe8a14890faf7e1dfc2fa5`, `tumbleweed-c2c87352413b422411e024b9`, `tumbleweed-b620f62a74a3ac8f9dbf5bd9`, `tumbleweed-798935bf97271df198732736`, `tumbleweed-97e5967b7f65f79c15b2ebe6`, `tumbleweed-df8af457ad5f845946c3a1a8`, `tumbleweed-db5e34d4fcbe3fb9ed947557`, `tumbleweed-4561fe425867de0080bca75e`
- polkit-actions: `tumbleweed-c6b42e305ac527b414a01750`, `tumbleweed-35cbacc401cb686e9efb3a2a`, `tumbleweed-fd9f790ab51d38fb7b518136`, `tumbleweed-0dd38154fc169a0501ef0d42`, `tumbleweed-745af93d9e40632337413927`, `tumbleweed-30917e77490aac57a916ecf0`, `tumbleweed-0f608a2480cf2957a58f1b9b`, `tumbleweed-02f6f24328c40a33ee0a9864`, `tumbleweed-a4663384ac1aa071d9a4a652`, `tumbleweed-d6e51174e3f196d501bc2442`
- port: `tumbleweed-5254a014d31c9226f0767152`, `tumbleweed-b3301c8d53cbc9d569a18b78`, `tumbleweed-c02d0e9052ef4a9195188b3f`, `tumbleweed-44953ab7f7bdc81732c84e2c`, `tumbleweed-dcdc56a06be335845b07422e`, `tumbleweed-92bc101232efef1c8c840eaa`
- process: `tumbleweed-a7344c170c38c55903843a5a`, `tumbleweed-4759ee1ff9ab03395084ef70`, `tumbleweed-2109899b54d0fa2ba9e0171b`, `tumbleweed-c0700594866d1e8bf23f17c1`, `tumbleweed-b675c205ee5d78755ca68010`, `tumbleweed-6e3c8927e22e23fd16ca97f0`, `tumbleweed-744374a4b70bc7abe5ae9782`, `tumbleweed-b636a586ed42cd13d6a79ccd`, `tumbleweed-5a2e5833ff711bb1e411d473`, `tumbleweed-907128b7054f3226f42ecd88`
- rpm-bin: `tumbleweed-be04af6b012ef94436e0a1e1`, `tumbleweed-8cae9640648d6dad17258945`, `tumbleweed-a2dc079fa3159c193fc42f4f`, `tumbleweed-835a51655831e9a7d9994281`, `tumbleweed-766b792874c35874d8f8ba12`, `tumbleweed-f7cc63ff05c7a74b846cebc0`, `tumbleweed-ba67839d344599c99d37e799`, `tumbleweed-3613efb73b71a8b88120aab8`, `tumbleweed-55f043a2f19e7ddd5c30ec24`, `tumbleweed-9b68dd88ab75a037970749f3`
- rpm-data:doc: `tumbleweed-d8d1488f6343d4b8f0a28624`, `tumbleweed-21c473dcf355645958b2923e`, `tumbleweed-82f198b84f0a837b3d019a68`, `tumbleweed-ce54db5c43dcf480996ace27`, `tumbleweed-64435b11463ed9cdda92a153`, `tumbleweed-17fdad9c009ebecc797d552f`, `tumbleweed-34f1d68aa8f99541fd83b097`, `tumbleweed-0f41df0655e967611e3bf2d4`, `tumbleweed-9a4285c07ae72d8659b65ada`, `tumbleweed-584ac100b9634a333ea60306`
- rpm-FIRMWARE: `tumbleweed-990ea4d898d398e3a6522940`, `tumbleweed-798825e63087dcf733dd5a63`, `tumbleweed-c0a1bfc65c995f7aa0792cc7`, `tumbleweed-98dd1a65d745b16e6f5968b5`, `tumbleweed-eb63f49b4fd3630fec409702`, `tumbleweed-965548f1e3677392b64fecde`, `tumbleweed-96f09be02a293394fdff5140`, `tumbleweed-724711caee15a8fa7ea2080c`, `tumbleweed-f057cdb52209ca0d28de1bf1`, `tumbleweed-3c43506891076f87da3a8f72`
- rpm-lib: `tumbleweed-b096fd4f76d69a03d3be403b`, `tumbleweed-1c59c9972ffc2008499a3cdd`, `tumbleweed-d5974e71d8c93f591f3e5596`, `tumbleweed-cc17b8c3db5a16466fb1ac9c`, `tumbleweed-10b56ecda9789c9f743ffc39`, `tumbleweed-e1c4e89331b7708e0e5e0247`, `tumbleweed-d037fc0e1bc51ea56325bdb3`, `tumbleweed-0cf8483055a181aff3b52b70`, `tumbleweed-56fdf21eb52068b033ed0143`, `tumbleweed-5fbbced58279ea01e82068a4`
- rpm-META: `tumbleweed-39d920fe4bb3267d031f47ab`, `tumbleweed-03e1dd87a3a21ed4f6e57df3`, `tumbleweed-7ff02912d648f6301fd0d572`, `tumbleweed-3cdfa4915c67696983abab0e`, `tumbleweed-52d0ec7abe75e7cc657a37db`, `tumbleweed-ea2db2110b837567aa4548a6`, `tumbleweed-46d7dfbc72a2231daf3f2e00`, `tumbleweed-18336274de691b65e6fd87be`, `tumbleweed-887caba836a7c23b3fedba9d`, `tumbleweed-2c805dfaabebdc57dd7cc660`
- rpm-script: `tumbleweed-76bec7078666d4adf09dec2d`, `tumbleweed-1a967f710140d32bb345b4d0`, `tumbleweed-9685e74ea78e68c5287224f2`, `tumbleweed-c42520ee0117143487de0aa7`, `tumbleweed-b53387a9910ffadbfe0c0b5d`, `tumbleweed-1c0e689c0de2ec8c1119da88`, `tumbleweed-1eb6fd1223be46b2794ef121`, `tumbleweed-d096da4dfb4e737d8f3de6d1`, `tumbleweed-b8f6cb7228e4ca56dd126324`, `tumbleweed-02167429f6b880fb6760d82e`
- service-MUST: `tumbleweed-46ee6d98dbd711ee7ec0f366`, `tumbleweed-71b93ad70a4ecce0ec6497e8`, `tumbleweed-9574db615606377925ab9a53`, `tumbleweed-43aaf0ec5194afe00d8fbe2f`, `tumbleweed-60f3460029c7e47bfa5f37e5`, `tumbleweed-1ca2a442f2503e0911e8c000`, `tumbleweed-fd599ffb8d460c84c1853507`, `tumbleweed-a38e153a4b753f4e41e8fb73`, `tumbleweed-f374c2d012ae34fe0c6d34e5`, `tumbleweed-647ce81eb71e768007455de7`
- service-NOT: `tumbleweed-6190555eb7a3114f0d7984dc`, `tumbleweed-43d7a486e97fd124525e4c06`, `tumbleweed-61a2d4d7b3e6e49ebab1ef81`, `tumbleweed-b3447b1649a103d5c7cfc61e`, `tumbleweed-c54af871826c1b06cedb4020`, `tumbleweed-6b08d0bfe5fa3da841ba453a`, `tumbleweed-2779d9368b0e8c9a1813e64d`, `tumbleweed-6e0094e8058997661f26eca0`, `tumbleweed-79402fb4e68213b060748cc4`, `tumbleweed-927d5da2f7acbe853c0fc730`
- timer: `tumbleweed-d1360bd75a992972bf43dd18`, `tumbleweed-85cda803b179d556b63a750f`, `tumbleweed-126f50c11de036a60e79336d`, `tumbleweed-85e4a6617be8dfa6608f1d9e`, `tumbleweed-6cd55076d3529716f2955fa3`, `tumbleweed-3e3f8109f66399c96d241e6e`, `tumbleweed-ad5107d9ca769418f2fef487`, `tumbleweed-7d4f21e2b2018c41000f2612`, `tumbleweed-7ef1a1a31e9e3538fb5d352a`, `tumbleweed-5ec41c8c8a44e9971d9d72d9`
- unit-alias: `tumbleweed-663b15ba995e33bebff25c0e`, `tumbleweed-d9668840a28516a986543299`, `tumbleweed-af390a1104469a129ef03945`, `tumbleweed-0685b477ddb115cb5ae524cd`, `tumbleweed-466950ca21179ed0bda7916c`, `tumbleweed-0f996c3936bf7e01048cb9ae`, `tumbleweed-defd49884ab502da201e7ae3`, `tumbleweed-ef3a8da4da4e6cd9cb9e8fd7`, `tumbleweed-36413eda9c536e462eca29a5`, `tumbleweed-a850ed2938c42e7b62d38764`
- unit-file: `tumbleweed-b55d16a4aedef023fc56f592`, `tumbleweed-30aa73d7f3f80c291f51f8d4`, `tumbleweed-db75852797cb9d92daf2b6cb`, `tumbleweed-1c8836d2207b54a076ad3b07`, `tumbleweed-66d3fe835d3fc3294cf324aa`, `tumbleweed-7c534ed3918ddc6663db0eff`, `tumbleweed-cb0872aa8c37d42937c455b1`, `tumbleweed-37b8bf7ec3ea5fe24083a6b9`, `tumbleweed-5e0ec76a7e4e3eed7a716e35`, `tumbleweed-459f27f3f6809ce32b384a3b`

## HOLE patterns (what the text lacks)

1. Presentation data (fonts, icon/cursor/sound/GTK themes, message translations, Flatpak Locale extensions; 179 rows):
   the text does not say whether appearance or message language is part of behaviour (S2.2-1) or only content (S2.2-4);
   S2.2-7 exempts a theme only when in force inside one program. Themes used by one program only (GRUB, Plymouth, YaST,
   LibreOffice, Firefox branding) are NOT under S2.2-7.
2. Metapackages and patterns (no files or only documents; 80 rows): their files do nothing (S2.2-4, removal stops nothing),
   but their dependencies steer later package-manager runs (S2.2-1); the text does not say whether package metadata counts.
3. A setting read by one system program whose effect reaches the whole computer (daemon configs, presets, sysusers files,
   rpm macros, session entry; 56 rows): "in force only inside one program" (S2.2-7) can mean "read by one program" (NOT) or
   "effect confined to one program" like the browser examples (then S2.2-1 gives MUST).
4. Reference databases (ISO codes, provider/APN list, public suffix list, PDF CMaps, MIBs, number/unit data, language
   models, time-zone table; 18 rows): S2.2-4 "contents of databases" vs S2.2-2 (lookups using them become impossible).
5. Code run by one program inside its own API (Augeas lenses, LibreOffice XSLT filters, QML greeter theme, Plasma layout
   script; 8 rows): code by S2.2-13, but the text does not say whether such an API is confinement (S2.2-11, S2.2-7) or the
   program's own rights (S2.2-10).
6. Derived unit files (5 generated from XDG autostart entries, 2 transient from D-Bus activation): behaviour depends on them
   (S2.2-1), yet they are recreated automatically, so removal changes nothing (S2.2-2; cache-like S2.2-5).

## Points to note for adjudication

- `ucode-amd` is MUST under S2.2-16; this machine is a virtual machine, where the guest kernel does not load microcode;
  the decision follows "where the system is able to change them" read as the operating system's ability.
- Firmware for devices absent from the VM is MUST because removal makes using such devices impossible (S2.2-2, S2.2-16).
- Running processes of the inventory itself (shells, `gawk`, `base64`, `python3.13`, `sudo`) are MUST under S2.2-9 as
  written.
- `Wired connection 1` (Ethernet profile with no device) is MUST: a saved network configuration NetworkManager can activate.
