# Void c1 classification notes

Only (not published: orchestration), TEXT.md, SENTENCES.md, the assigned input, its fact index, permitted retained void evidence, and public documentation were consulted. No other classification or earlier night was read. The two stored-group portions were independent parallel parts of this classification.

## Fixed sentences

- **S8.1-6** **Package**—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.

- **S8.1-11** A service is in force if it is enabled; an account, if it exists.

- **S8.2-2** The rest need not be recorded.

- **S8.2-5** What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.

- **S8.2-6** What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.

- **S8.2-7** Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?

- **S8.2-8** Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.

- **S8.2-9** Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?

- **S8.2-10** Then it is a **program**, whoever wrote it and wherever it came from; a program belongs to what is installed.

- **S8.2-11** Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?

- **S8.2-13** Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.

- **S8.2-15** Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.

- **S8.2-16** What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

- **S8.2-17** A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.

- **S8.2-23** A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.

## Scripted rules and manual checks

The scripts append and flush each finished row and skip existing IDs. The following ten evenly spaced cases per rule were displayed and manually examined against the relevant metadata, content, and joins. A sample ID is an object reference; generic account home paths are omitted here.

### package-explicit

An actually installed package with explicit selection answers question 1. In the absence of containing-package or derivation evidence, S8.2-16 requires its own line: INSTALLED-OWN.

Manually checked: void-bd17767441e3004ea755186c, void-f719417689a9d6d8aefcb9ef, void-12627fc1c2a40c3ba4efd727, void-b634b9e73a6cc90dcb9368b5, void-e987a07b4ee6091f251b0353, void-935c8700e38d3c90051c0e0e, void-1cccca1d50dee9738694e965, void-bbf048357171b7089e69dcbc, void-2e391e3678099208f53f49ee, void-505225f6690f31ffd8dd977a.

### package-dependency

An actually installed dependency answers question 1 and is covered by the requesting package line under S8.2-16: INSTALLED-DERIVED. This is the required recording relation, not an assertion that this machine already has a declaration.

Manually checked: void-d56f25389acf3fcb4c8141f9, void-d01f7bfa810deab761d1dfd6, void-fc6bbb0f79f4aafa6cbf36fc, void-9c89eb3f584a541e14d44d9d, void-90f2cde43eef6d2eba977b51, void-6ed36d7b25e43ab4d6d3c9b2, void-8e0a9b1df9084576321531fe, void-9e6a19a0ec4344a3bd602418, void-f0f93cbb8b0d44c555f9773a, void-adc18047cf9bcbd8ce616750.

### python-dependencies

The browser action log expressly names the dependency chain and successful installation of each distribution under marionette_driver. This independently resolves the inventory reason=unknown for these 16 rows: INSTALLED-DERIVED. The distro row has an erroneous collected display name; its distribution location and version identify the installed distro wheel, not a separate operating system.

Manually checked: void-95a26f7573adef2ac3df8403, void-20cf6c4cf9eca43d060d1cf6, void-9e105ad03c68f4b5b08f514b, void-5036206ec506f2d855dc5daf, void-e74ebec3619385a1ee6b9d58, void-764279a8e8b32744a79df34e, void-e0b0e8994a33e796048eb20e, void-b82b7df979b9df02a9810656, void-7c1bfc2199c1ed6f7c17639e, void-cf3f98e5e78b065628a1d136.

### package-unknown

The package is installed, but neither a reason nor complete containing-package provenance is established. UNKNOWN records the missing fact controlling S8.2-16. Native ownership of metadata alone does not prove native ownership of the complete language package.

Manually checked: void-227a63d831426a6cc06074fc, void-69d6aaad32710086115d942f, void-43704c1979467dae73119212, void-7935af71fd08561d6217dfaa, void-96487ed2ae3c07911df19502, void-33c406b7a9ce020187463905, void-696efabec67b27c589b3cf5c, void-2f753b00714dd834bb178918, void-ccfefb21c8f05587df0ee506, void-de4c7b28bc7de4e9c443fc90.

### unchanged-files

Exact path joins establish package ownership and integrity=unchanged. S8.2-6 gives question 1 priority even for executable policy code and configuration defaults: INSTALLED-PACKAGE. This includes the supplied wpa_supplicant default file and ten GRUB files.

Manually checked: void-d48d1d29feb095bf50fd8763, void-f82b56aabbbb95b80fba17c0, void-b959641f896bb9f89663beb9, void-5e30dd05b42f8291e4683eb9, void-a365d3e3b518437e36e7036a, void-77209f372ef83118f9d013c0, void-bcd233813ff0859190d52439, void-50572aaa7cbff23d967c2ffe, void-4274b44cba9f63d0468821f7, void-25974ebdb76a51fc1b4b793d.

### polkit-packaged

Each registered action identifier was matched to XML content in the retained policy files, which have unchanged integrity. These definitions are parts of those packages, giving INSTALLED-PACKAGE before the setting question. An action identifier is not a performed human action.

Manually checked: void-7a2072c1026c26f1f80a0a39, void-7f79ca365277e3dfb5aa28b3, void-e0ac902d4d91e210fd29f3c0, void-38349dbf9e98c643c7084d94, void-d8ecd890f7e2c7fb08f2de4d, void-b708f176147d8553d46fd804, void-45027ff58a36585e8348d2f8, void-4907807d7df1bf45e1d8f4d4, void-dd1272697ad0b083ce01772b, void-cddf35608213254777be0e2b.

### sysfs-runtime

The actual collection commands enumerate sysfs module and driver registrations, not stored module binaries. These are kernel-created runtime objects, hence RUNTIME under S8.2-5. The running kernel image and its installation integrity are not identified: parent decision UNKNOWN.

Manually checked: void-d938110bb8b92e7e5646bdea, void-6506276564ca0644bef8f65b, void-8e75c9587708af72962421aa, void-66b6b8359d56b7950d9c9258, void-d7730c6bf4667faf998fc69a, void-c09978337c8abdb13200e90a, void-2c94b1afa2e2cc84a7b328b0, void-7a9f01ab7d33c023f12d2b44, void-34c53562dd878922e82673d1, void-c65cf2b3090c9480cdcf980b.

### process-runtime

Each row is an observed process from procfs. S8.2-5 gives RUNTIME for every executable identity. The reason names its executable and INSTALLED-PACKAGE where exact current-file integrity is unchanged, otherwise UNKNOWN. Deleted executables are not equated to replacement package bytes. The supplied inventory probe is independently bootstrapped code.

Manually checked: void-a7420a8bf6c5210f17e9760e, void-b3f34114ee2f0398028414e0, void-80500b8525ba1a7efd08b887, void-b43c86109752e08a007e2471, void-63a8614367263166b6962d8e, void-574fd0543432b90afbc79038, void-0b4992bd02316ac1925f2021, void-1c040d0929549edf7de8136c, void-2f0ca1c43f05b9f5f30dd9b8, void-62015fe1c1b824bd4c968b0e.

### dump-record

Comment lines and serialization delimiters emitted by iptables-save are query output, not live access rules or person-typed commands. S8.2-15 gives RECORD.

Manually checked: void-55d99c0ce07ba7097a94c507, void-1b321b290a5f18c33e48d80b, void-64be9863feb6738b330ad65a, void-2e5a1b0e5e5f129efa9c61e5, void-ece6c6df81fedaa49c0f8b45, void-e809e31c7231e673f093a515, void-53790aba31a820a2b8048e4c, void-7f1053316aead06b2de8e988, void-1d127d95c48ae95931e688e2, void-e507fe0d0068afce8a0de770.

### firewall-runtime

Rows representing kernel-resident chains, counters, and rules have runtime lifetime. No saved rule file is represented by this query. S8.2-5 gives RUNTIME; Docker-marked bridge rules name the daemon, other kernel tables name netfilter. Their creator recording decision is UNKNOWN rather than guessed from an unverified executable.

Manually checked: void-96ccf4c70d6602138747709d, void-4c5108fb121f46dd42ff5721, void-6f1cd9c734a41b77969f2793, void-155dcadaf33242464f01ba9a, void-b5d4b9c61e2eca3cfc0b636f, void-1ed8f362554935dbdcd5b27a, void-ae7d8d40f26161f44b2a33bb, void-538695f62dbcdc9f59246ec6, void-b4b96f01acab094e95896dd3, void-c46b8efc2aa230d1e63ce3af.

### identity-origin

Existing passwd/group records establish local identities and rights under S8.2-13. The particular identity origin is not established, so SETTING-OWN versus SETTING-DEFAULT cannot be selected. Installation-created identities proved by action output are handled individually instead.

Manually checked: void-f206810b0ca7fdc4efe49d2d, void-9057fe3ba05d77a64fd10ff0, void-42e702141b85c625a027002e, void-eba9a3b7a364bd047890d52b, void-a79ab0c43b6a5f6b6bc68dd9, void-40cbd298cd2f93cf1954b60f, void-98f4451ccb5b835a1596336b, void-66a1ca62db4453448e5dfbf5, void-85e237c86d64fe782a5e4450, void-bb1e57bd747437d926fd33e5.

### service-origin

The symlinks select enabled runit services under S8.1-11 and S8.2-13. Their original creation as installation defaults versus separately chosen values is unrecorded, giving UNKNOWN under S8.2-17. A successful run status alone does not establish link creation provenance.

Manually checked: void-59e0e7fd507094a2cd50772c, void-65591628311f83a7842469aa, void-c0cb3119704e10793188cbe6, void-d52da1f1caef22e5561527a8, void-c207d3e73efb5375c370739c, void-e5f7874dc6c11b0a4bc1b166, void-a2ef5743af3fd4b335be2059, void-bd4679d294e8e804046cf36b, void-4313937f45bb4f0ceb53a94c, void-9b3a8028de655c880e021515.

### code-origin

The shebang/startup/interpreter evidence identifies code, and persistence is known. The retained file manifest lacks ownership/integrity for each exact path. Earlier question 1 and S8.2-16 can therefore change the category or line; UNKNOWN names those missing facts. Executable permission by itself was not used: times.json was individually excluded.

Manually checked: void-55038c8f27c67d661a934aae, void-233c4f60ada019828b28d808, void-e1ffabe2aa31236c5d55dd16, void-0ed9627f14a9fda4351091cf, void-c06d3c9fa0bbceb398c94b3f, void-c2ef3b96118be7442667a8a2, void-306361fa8acf5241d11b2cb5, void-048a35c6eaf295ed7ffae025, void-2ea663ec72ebc29d34ae596a, void-7808b60bc0c176ea8c6176ea.

## Individual decisions and evidence limits

- Installation output expressly creates _tss, polkitd, _flatpak, dbus, and docker identities during package installation. Their account/group values are SETTING-DEFAULT. The relevant application_package, network_connection, and container_run logs are under `D1/in/control/void/actions-logs/actions-logs/`.
- The network log expressly adds cal-secondary and cal-test after package installation. Their logical profiles and persistent files are SETTING-OWN. Other connection rows do not distinguish saved versus generated transient profiles.
- The sudo output headings are RECORD. secure_path, visudo environment preservation, and root authorization were checked against the retained unchanged sudoers content. Supplemental wheel and lab rules lack origin evidence and remain UNKNOWN.
- Open sockets remain RUNTIME despite the socket query omitting process ownership. The missing parent decision is expressly UNKNOWN; a conventional port number was not used to guess its process.
- Firefox times.json is timestamp data despite its executable mode. Public profile-creation documentation and the observed fresh profile establish RECORD. It is not code merely because the collector put it among executable candidates.
- The boot action stderr explicitly records generation of the 6.12.118 and 6.18.64 initramfs images. GAP-TWO states the two readings: PROGRAM-DERIVED if an archive of executable payload is itself code, RECORD if only the archive container is classified as generated storage. S8.2-9 does not define the archive boundary; S8.2-16 supplies coverage only after the object category is known. This is distinct from a known non-executed HTTP cache wrapper.
- The old initramfs and installed GRUB boot copies lack current receipt/generation facts, giving UNKNOWN. The ten unchanged GRUB package-source files answer question 1 and never reach this issue.
- The BusyBox image is an opaque filesystem image rather than a running container process. GAP-NONE names the absent treatment of such an image as a package, code itself, or filesystem material. S8.2-22 explicitly addresses the running program, not the stored image. The stopped container separately lacks a member inventory of its writable layer: UNKNOWN.
- Opaque persistent application/container stores were not called runtime. Their contents were not expanded, so their member decisions cannot be established.

## Public sources and supporting passages

- https://www.kernel.org/doc/html/latest/filesystems/sysfs.html — “sysfs is a RAM-based filesystem initially based on ramfs.” This establishes the lifetime and kernel-export function of the enumerated registrations.
- https://docs.voidlinux.org/config/services/index.html — “Void uses the runit(8) supervision suite to run system services and daemons.” The service-directory links select enabled services; documentation does not establish each observed link's origin.
- https://www.freedesktop.org/software/polkit/docs/master/pkaction.1.html — “pkaction is used to obtain information about registered polkit actions.” The query lists definitions rather than performed human actions.
- https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html — “Actions are defined by applications.” The action definitions are matched to retained XML policy content and its installation integrity.
- https://docs.docker.com/engine/network/firewall-iptables — “Docker creates iptables rules in the host's network namespace for bridge networks.” This identifies the bridge firewall producer, not persistent configuration provenance.
- https://www.gnu.org/software/bash/manual/html_node/Interactive-Shell-Behavior.html — “Bash reads and executes startup files as described in Bash Startup Files.” Thus shell startup files reach the code question if not unchanged package objects.
- https://docs.telemetry.mozilla.org/concepts/profile/profile_creation — “a times.json containing a timestamp of the current time is stored inside that profile directory”. This identifies the profile timestamp record.
- https://www.gnu.org/software/grub/manual/grub/html_node/Invoking-grub_002dinstall.html — “The program grub-install generates a GRUB core image using grub-mkimage and installs it on your system.” Actual provenance of the observed boot copies is still not retained.
- https://www.kernel.org/pub/linux/utils/boot/dracut/dracut.html — “dracut - low-level tool for generating an initramfs/initrd image”. Generation of two observed images is independently recorded in the action stderr.
- https://docs.docker.com/engine/storage — “By default all files created inside a container are stored on a writable container layer”. The exited container's reported changes are not an inventory of those files.

## Stored groups

The rules, exact sentence quotations, ten manual checks per rule, and individual group decisions are retained in [part a notes](part-void.a.notes.md) and [part b notes](part-void.b.notes.md). These form part of this notes file by reference. Complete MIXED assignments are in `part-void.a.members.tsv` for part a and in the individual-case section of `part-void.b.notes.md` for part b. They describe every immediate member, not inferred recursive contents. The final output's basis points to the actual retained member table.

Section 8.5's implementation and storage-policy exclusions were not counted as gaps. No hypothesis outcome or gap weight is assigned by this classification. Mechanical output validation is not independent acceptance of the classification.
