# Fedora c1 classification notes

These sections document the current independent c1 classification, its rules, sources and manual checks. The append-only result is `part-fedora.tsv`. The merger retains existing rows and rejects conflicting duplicates. Each shard is restricted to disjoint input kinds.

# Fedora c1: accounts, execution, devices, networking and application formats

Only the assigned input and its raw Fedora inventory were read. No removal was performed. Classification applies S2.2 and S3-1/S3-2. Inventory labels from an earlier definition are disregarded. Rows identify logical inventory objects: a driver link evidences its bound driver, a socket line evidences its socket, and a process line evidences its identified process. The saved inventory text itself is not the object being classified.

The process collector in `../in/raw/fedora/raw/076-process.sh` prints the PID and a tab before `readlink`, but prints no newline when `readlink` fails. Consequently, several PIDs occur on one physical line. The name in each input row is the first PID. Only a two-field line establishes that PID's executable. The later executable cannot be assigned to an earlier PID. This is missing observational information, not a defect in the definition. No public documentation can recover the missing historical PID identity.

The output is an independent classification, not acceptance of the hypothesis or of another classification.

## Primary documentation

- https://docs.kernel.org/filesystems/proc.html — “Link to the executable of this process”; “List of loaded modules”. These describe `/proc/PID/exe` and `/proc/modules`, the actual inventory sources.
- https://docs.kernel.org/driver-api/driver-model/binding.html — “Driver binding is the process of associating a device with a device driver that can control it.” The document also describes driver initialization and removal.
- https://docs.kernel.org/kbuild/modules.html — “The module foo.ko, consist of bar.o and baz.o”. Modules are compiled kernel objects, not interpreted interface content.
- https://networkmanager.dev/docs/api/latest/nmcli.html — “nmcli is used to create, display, edit, delete, activate, and deactivate network connections”. `083-network.sh` requests connection name, UUID, type and device.
- https://www.freedesktop.org/software/systemd/man/latest/networkctl.html — “Show a list of existing links and their status.” `084-networkd.sh` inventories links; unmanaged is networkd's management status.
- https://docs.flatpak.org/en/latest/basic-concepts.html — “this runtime must be installed on the host system for the application to run.” This establishes runtime dependency, not merely archive storage.
- https://docs.flatpak.org/en/latest/extension.html — “Extension for graphics drivers”; “This is the successor to `org.freedesktop.Platform.ffmpeg-full`”. The extension list identifies GL.default, its extra branch and codecs-extra; library-path mounting makes these runtime code.
- https://docs.flatpak.org/en/latest/flatpak-builder-command-reference.html — “Separate out locale files and translations to an extension runtime.” The application Locale extension supplies translated interface content; the runtime extension also supplies library locale rules, as established by the source chain below.
- https://apps.gnome.org/Calculator/ — “Calculator is an application that solves mathematical equations.”
- https://docs.podman.io/en/latest/markdown/podman-start.1.html — “Start one or more containers using container IDs or names as input.” An exited container can be started again.
- https://docs.podman.io/en/latest/markdown/podman-run.1.html — “Run a process in a new container.” Its filesystem comes from the image; this is executable container backing, not merely an unrelated downloaded archive.

## Sentence text

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-3** The following need not be recorded:
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-14** a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Rule: accounts

Every row is a parsed local account entry. Apply the explicit account requirement S2.2-15, including service accounts. No password is recorded by this decision.

Ten manually inspected rows (input and corresponding raw lines were checked):

- `fedora-e4ed2edd4ccc307519c5d468`: Defines a local account and its user identity. Source `D1/in/raw/fedora/raw/001-accounts.out:1`.
- `fedora-2e6de269b4b10b3e6a9823ab`: Defines a local account and its user identity. Source `D1/in/raw/fedora/raw/001-accounts.out:2`.
- `fedora-0eea6d09d6acacd5e4fe7cc8`: Defines a local account and its user identity. Source `D1/in/raw/fedora/raw/001-accounts.out:3`.
- `fedora-3b40dcf16ab4d4e50d84c4a3`: Defines a local account and its user identity. Source `D1/in/raw/fedora/raw/001-accounts.out:14`.
- `fedora-6f915c5d7c4a80e4bddbb727`: Defines a local account and its user identity. Source `D1/in/raw/fedora/raw/001-accounts.out:15`.
- `fedora-73e4893fb30465e27f3b4c4d`: Defines a local account and its user identity. Source `D1/in/raw/fedora/raw/001-accounts.out:17`.
- `fedora-1ecb309e6edc8edee34eb660`: Defines a local account and its user identity. Source `D1/in/raw/fedora/raw/001-accounts.out:21`.
- `fedora-e570cabb701548a01b208208`: Defines a local account and its user identity. Source `D1/in/raw/fedora/raw/001-accounts.out:41`.
- `fedora-ef48382848a9c95fdcd3d608`: Defines a local account and its user identity. Source `D1/in/raw/fedora/raw/001-accounts.out:51`.
- `fedora-cd935a85f60855018f037509`: Defines a local account and its user identity. Source `D1/in/raw/fedora/raw/001-accounts.out:54`.

## Rule: processes

A two-field line associates one PID with its executable. Such a running program is required by S2.2-9/12, independently of the details of its command-line workload.

Ten manually inspected rows (input and corresponding raw lines were checked):

- `fedora-590923a3d1b07bd0709051ad`: Runs systemd as a process. Source `D1/in/raw/fedora/raw/076-process.out:1`.
- `fedora-f6d746d5afe5d266c6d79357`: Runs crond as a process. Source `D1/in/raw/fedora/raw/076-process.out:3`.
- `fedora-aec3e2386de93419f760fa4c`: Runs kmscon as a process. Source `D1/in/raw/fedora/raw/076-process.out:4`.
- `fedora-46859551cc6ce23e533bbf94`: Runs systemd-executor as a process. Source `D1/in/raw/fedora/raw/076-process.out:7`.
- `fedora-e2ed7ec77652e12929fd9b85`: Runs dbus-broker-launch as a process. Source `D1/in/raw/fedora/raw/076-process.out:10`.
- `fedora-c462d4fdc8c9a3cdcb2b3409`: Runs dbus-broker as a process. Source `D1/in/raw/fedora/raw/076-process.out:11`.
- `fedora-392610b617a68fcd01f28f09`: Runs systemd-userdbd as a process. Source `D1/in/raw/fedora/raw/076-process.out:16`.
- `fedora-dbf65a00973cf7c8aeede32e`: Runs systemd-userwork as a process. Source `D1/in/raw/fedora/raw/076-process.out:23`.
- `fedora-1ae763913ae608a115750a6f`: Runs systemd-userwork as a process. Source `D1/in/raw/fedora/raw/076-process.out:24`.
- `fedora-c5c2d14ddbf97dac3dd4dc66`: Runs avahi-daemon as a process. Source `D1/in/raw/fedora/raw/076-process.out:26`.

## Rule: unidentified_processes

A line with multiple numeric fields establishes no executable for its first PID. S3-2 requires UNKNOWN; do not substitute the final PID executable. This homogeneous rule is about the identical evidence failure, not guessed process roles.

Ten manually inspected rows (input and corresponding raw lines were checked):

- `fedora-75876cae6b37d970268e6022`: Process function is unidentified because the inventory joins several PIDs. Source `D1/in/raw/fedora/raw/076-process.out:2`.
- `fedora-c1b06a71daa3183f8bb707bb`: Process function is unidentified because the inventory joins several PIDs. Source `D1/in/raw/fedora/raw/076-process.out:5`.
- `fedora-0630a103ed7d87f90879cea5`: Process function is unidentified because the inventory joins several PIDs. Source `D1/in/raw/fedora/raw/076-process.out:6`.
- `fedora-3bb57218f1c926de8bb86718`: Process function is unidentified because the inventory joins several PIDs. Source `D1/in/raw/fedora/raw/076-process.out:8`.
- `fedora-67a84a7fec95df7a4be19897`: Process function is unidentified because the inventory joins several PIDs. Source `D1/in/raw/fedora/raw/076-process.out:9`.
- `fedora-8a86a417e50b10384b88e9c9`: Process function is unidentified because the inventory joins several PIDs. Source `D1/in/raw/fedora/raw/076-process.out:12`.
- `fedora-4186187c9918c8d29eceefdf`: Process function is unidentified because the inventory joins several PIDs. Source `D1/in/raw/fedora/raw/076-process.out:13`.
- `fedora-b1fc537fbe4d04253cf4af87`: Process function is unidentified because the inventory joins several PIDs. Source `D1/in/raw/fedora/raw/076-process.out:14`.
- `fedora-fb364c6193d616102d3710c4`: Process function is unidentified because the inventory joins several PIDs. Source `D1/in/raw/fedora/raw/076-process.out:15`.
- `fedora-d33a20f315ba0bc4af9cc5ce`: Process function is unidentified because the inventory joins several PIDs. Source `D1/in/raw/fedora/raw/076-process.out:17`.

## Rule: modules

Every row is a Live kernel module from /proc/modules. Apply S2.2-10 to code loaded into and executed with the kernel rights. Usage counts do not turn executable code into content.

Ten manually inspected rows (input and corresponding raw lines were checked):

- `fedora-67f2369b783cb1d10f8b1453`: Runs tun code inside the kernel. Source `D1/in/raw/fedora/raw/077-module.out:1`.
- `fedora-7bcc3c34f88f6689c9d7ad98`: Runs overlay code inside the kernel. Source `D1/in/raw/fedora/raw/077-module.out:2`.
- `fedora-61584db5bdaa082ebc1774b4`: Runs nf_conntrack_netbios_ns code inside the kernel. Source `D1/in/raw/fedora/raw/077-module.out:3`.
- `fedora-bcb15ce132aafc966e7b9a08`: Runs nf_tables code inside the kernel. Source `D1/in/raw/fedora/raw/077-module.out:20`.
- `fedora-9270a9964346b07156989aba`: Runs kvm_amd code inside the kernel. Source `D1/in/raw/fedora/raw/077-module.out:25`.
- `fedora-5ab3c9a4df950daea09945bd`: Runs kvm code inside the kernel. Source `D1/in/raw/fedora/raw/077-module.out:27`.
- `fedora-d89d9d85dace36c89a81a1ea`: Runs virtio_net code inside the kernel. Source `D1/in/raw/fedora/raw/077-module.out:31`.
- `fedora-06e8c7dd343e7d7737853a2d`: Runs zram code inside the kernel. Source `D1/in/raw/fedora/raw/077-module.out:38`.
- `fedora-2098e6e9511391bff5d152cd`: Runs virtiofs code inside the kernel. Source `D1/in/raw/fedora/raw/077-module.out:50`.
- `fedora-8f90682e734721510476a1da`: Runs fuse code inside the kernel. Source `D1/in/raw/fedora/raw/077-module.out:51`.

## Rule: drivers

Every row supplies a device-to-driver symlink. Treat the listed object as the bound driver evidenced by that link. Kernel driver code executes with kernel rights (S2.2-10); its binding supplies device operations (S2.2-1/2). This does not classify the link as a separately installed program.

Ten manually inspected rows (input and corresponding raw lines were checked):

- `fedora-7ccc14c47555c1b288da935f`: Binds parport_pc kernel driver code to a device. Source `D1/in/raw/fedora/raw/078-driver.out:1`.
- `fedora-bd86c876d23b39492468e86d`: Binds i8042 aux kernel driver code to a device. Source `D1/in/raw/fedora/raw/078-driver.out:2`.
- `fedora-6421c2ca8894a571970a7748`: Binds ctrl kernel driver code to a device. Source `D1/in/raw/fedora/raw/078-driver.out:3`.
- `fedora-453980b300dde57659acdd6c`: Binds port kernel driver code to a device. Source `D1/in/raw/fedora/raw/078-driver.out:4`.
- `fedora-2d8ad3fffd8454bd2d8aa029`: Binds kgdboc kernel driver code to a device. Source `D1/in/raw/fedora/raw/078-driver.out:7`.
- `fedora-6d3597abac552cf11b2dd813`: Binds acpi-button kernel driver code to a device. Source `D1/in/raw/fedora/raw/078-driver.out:8`.
- `fedora-dad65f771ad8af15c770baeb`: Binds i8042 kernel driver code to a device. Source `D1/in/raw/fedora/raw/078-driver.out:43`.
- `fedora-1231accbb0d7665518c938b4`: Binds virtio_net kernel driver code to a device. Source `D1/in/raw/fedora/raw/078-driver.out:48`.
- `fedora-9ef65b3bb9a83314dcaac2ba`: Binds virtio_blk kernel driver code to a device. Source `D1/in/raw/fedora/raw/078-driver.out:56`.
- `fedora-02ffdc6dc3654f6abf2cd0e9`: Binds faux_driver kernel driver code to a device. Source `D1/in/raw/fedora/raw/078-driver.out:61`.

## Rule: ports

Every row is a bound receiving UDP socket or listening TCP socket. S2.2-1/2 require its communication capability; S2.2-15 explicitly includes open ports. Loopback scope does not negate that capability.

Ten manually inspected rows (input and corresponding raw lines were checked):

- `fedora-95bc3adaf9c715e687224ff6`: Accepts UDP traffic at 0.0.0.0:5353. Source `D1/in/raw/fedora/raw/079-port.out:1`.
- `fedora-7bf1a5aa29254d2fb0b9f708`: Accepts UDP traffic at 0.0.0.0:5355. Source `D1/in/raw/fedora/raw/079-port.out:2`.
- `fedora-4eb8eb0aaef7b9a755a6a130`: Accepts UDP traffic at 127.0.0.54:53. Source `D1/in/raw/fedora/raw/079-port.out:3`.
- `fedora-e165d70be8ce19b7fb4b0ab2`: Accepts UDP traffic at 127.0.0.53%lo:53. Source `D1/in/raw/fedora/raw/079-port.out:4`.
- `fedora-20833db50c06e91d73bf5acc`: Accepts UDP traffic at 127.0.0.1:323. Source `D1/in/raw/fedora/raw/079-port.out:5`.
- `fedora-9df4745bd8719264b0be0477`: Accepts UDP traffic at [::]:5353. Source `D1/in/raw/fedora/raw/079-port.out:6`.
- `fedora-39f6d1978fe023b825f93913`: Accepts UDP traffic at [::]:5355. Source `D1/in/raw/fedora/raw/079-port.out:7`.
- `fedora-f04408001178a91733a72992`: Accepts UDP traffic at [::1]:323. Source `D1/in/raw/fedora/raw/079-port.out:8`.
- `fedora-7cb43c13130113d18a0cc5f6`: Accepts TCP traffic at 127.0.0.53%lo:53. Source `D1/in/raw/fedora/raw/079-port.out:9`.
- `fedora-253b7e3459a1941d07d1de59`: Accepts TCP traffic at 127.0.0.54:53. Source `D1/in/raw/fedora/raw/079-port.out:10`.

## Individual decisions

The seven Flatpak entries, five connection profiles, three network links, three sudo grants, container and image were examined individually. Their row-specific decisions and sources are in the TSV. The Wi-Fi exception is explicit. Ethernet and loopback profiles control networking for other programs, so they are not settings confined to NetworkManager. The inactive Ethernet profile still supplies a saved connection that can be activated. The image is the executable root filesystem source for the observed container, whose echo command ran and remains restartable. Calculator.Locale supplies localized interface content. Platform.Locale supplies library locale definitions, affecting operations across applications. GL/codecs and platform runtimes supply executable capabilities.

## Current-run review corrections

The missing-unit reasons were corrected in their own section to discuss absence of the service rather than deletion of inventory text. Platform.Locale was corrected from NOT to MUST after establishing that it contains library locale definitions as well as translated text. Calculator.Locale remains NOT; its description is narrowed to calculator interface translations. All prior current-run row values are preserved in `part-fedora.corrections.jsonl`; no input IDs were removed.

The runtime source chain is:

- https://raw.githubusercontent.com/GNOME/gnome-build-meta/master/elements/flatpak/platform/locale.bst — `directory: '%{datadir}/runtime/locale'`.
- https://raw.githubusercontent.com/GNOME/gnome-build-meta/master/elements/flatpak/platform/filesystem.bst — `freedesktop-sdk.bst:integration/split-locales.bst`.
- https://gitlab.com/freedesktop-sdk/freedesktop-sdk/-/raw/master/elements/integration/split-locales.bst — `movelocale "lib" "%{indep-libdir}/locale"`. The same source splits translated messages as well.
- https://man7.org/linux/man-pages/man7/locale.7.html — “This category governs the collation rules used for sorting and regular expressions”. Locale categories also affect character conversion and numeric parsing. These operations use rules across applications, so the runtime extension does more than supply unavailable content.


# Service and timer classification

Scope: exactly 838 rows of kinds L1:service, L1:timer, L1:unit-file, L1:user-service, L1:user-timer, and L1:user-unit-file in the supplied part. All represented units have service or timer suffixes. Classification concerns the represented service, timer, or unit definition, not the inventory text as a historical document. No removal was performed. No earlier classification was consulted.

## Deciding text

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S3-2: “If what the object does remains unknown, the case yields ?.”

The relevant function is activation or supervision, rather than every operation performed by the activated executable. Service configurations affect separate processes. Their effects are not confined inside the service manager, so S2.2-7 does not exempt them. Disabled or static unit definitions still supply an activation capability; the test is not restricted to currently running services. Templates supply instantiated activation. Timers for cache creation or log rotation are schedulers, not caches or logs themselves.

## Documentation checked

- https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html: “A unit configuration file whose name ends in ".service" encodes information about a process controlled and supervised by systemd.” The same page explains parameterized service templates.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html: “For each timer file, a matching unit file must exist, describing the unit to activate when the timer elapses.”
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html: “Units can be aliased (have an alternative name), by creating a symlink from the new name to the existing name”. Alias names participate in activation and dependencies.
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html: “not-found” means “The unit file does not exist.” The documentation distinguishes loaded inactive units from missing definitions and explains enabled, disabled, static, indirect, alias, and generated states. Generated service definitions are implicitly enabled by their generator; generation alone does not make them a speed-only cache.

Local evidence: each input row points to a numbered raw listing line under D1/in/raw/fedora/raw/. The inspected files are 070-user-user-service.out, 071-user-user-timer.out, 072-user-user-unit-file.out, 073-service.out, 074-timer.out, and 075-unit-file.out. The input members field reproduces these listing lines. The public documentation supplies semantics of the observed type and state. No behavior is inferred from earlier inventory classification labels.

## Homogeneous rules and manual checks

The script part-fedora.units.rules.py applies the following mutually exclusive rules in order and flushes every appended row. Manual checks inspect the individual name, type, state, and, where present, description in the raw listing reproduced by members. They check whether the documented common activation function fits; they do not infer executable contents from names.

### Missing references: 25 NOT

Require not-found and inactive/dead in the listing. These entries name no present service definition or active process. The reference cannot contribute the activation capability of a nonexistent service. The represented absent service supplies no capability whose removal could change behavior, giving NOT under S2.2-1 and S2.2-2. This does not classify any referring dependency file or a hypothetical installed version of the service.

Ten inspected IDs, all explicitly not-found inactive dead:

- fedora-5bce747654431241a4d6bc20
- fedora-c4ba1e303a5b06a244a2c543
- fedora-ab84f6b9e1ecca8b4b1856b1
- fedora-23ade8bacea1099397d76aaa
- fedora-e7583a06ca8dfc7bcc4d7160
- fedora-24130668c2ebf98dc9f4044c
- fedora-044a62eb377fe1b5f6d7e42e
- fedora-80fb7cc958ad23682989d6e0
- fedora-73b6736a48ef2979375baf88
- fedora-59df04a65312698106bfa46a

### Aliases: 34 MUST

Require alias state. The name provides an alternate activation route. Removal loses activation through that name even if the canonical unit remains. S2.2-1 and S2.2-2 apply to that capability.

Ten inspected IDs, all explicitly alias state (the last is a timer; the others are services):

- fedora-f92d69422a90f003ac015874
- fedora-7cd81feb1d2fb5406b9249c7
- fedora-87cf507caf824ef3cf35c2a1
- fedora-03f1f55f3416f6012ccc8e20
- fedora-7e765dd0af40adb9e39cbbd9
- fedora-2cca1132663f2d2e49f5979e
- fedora-dae8f067d32a55e5fd79017d
- fedora-2ffadba1415671bd1377a609
- fedora-4ea2a9cf3345ef2c54842db0
- fedora-513c98e74b27b2c622b44332

### Non-alias timers: 30 MUST

Require timer suffix, either a listed timer with activation target or an installed timer unit file. Removal loses the defined scheduled activation. S2.2-1 and S2.2-2 apply even when its timer has no next deadline or is disabled.

Ten inspected IDs:

- fedora-c0bce46ab638fcb6c9e46ed8: scheduled greeting service activation.
- fedora-8d5f91d9f6cf286e5f87e057: enabled greeting timer definition.
- fedora-7dca37cb0ca3a8d59904101c: enabled temporary-file cleanup timer definition.
- fedora-ec10a3f2d2519412545f1958: scheduled anchor service activation.
- fedora-3a14403d9a02cffeee58c8a0: scheduled log rotation activation.
- fedora-d1955eb82588abebd52fd46b: disabled timer definition; activation remains definable.
- fedora-d23c67bac03e17e8a6a4b727: static timer template; supplies instances.
- fedora-8f622caccf1fdd031295ac69: disabled timer definition.
- fedora-f46f15409eeaf32abea9354b: enabled raid-check timer definition.
- fedora-3e479dbd339f437ef4e385a6: enabled anchor timer definition.

### Present non-alias services: 749 MUST

Require service suffix and either loaded state in the service listing or an installed unit-file listing with enabled, enabled-runtime, disabled, static, indirect, or generated state. These are activation/supervision definitions for separate processes. S2.2-1 and S2.2-2 require recording the supplied capability. The rule does not claim that a loaded inactive service is currently executing.

Ten inspected IDs:

- fedora-af780df7858da6b4e6b6bf49: loaded inactive greeting service.
- fedora-d60236de2dd55e421870952e: static service definition.
- fedora-b8578c1bee42b665078317c0: loaded inactive service; process activation definition present.
- fedora-39ebb2564c943b45b01d8ad9: loaded active running journal service.
- fedora-e7b7a4af481719edd89fa924: static service definition.
- fedora-c39b6bdb3f742383e8e9dd64: disabled service definition.
- fedora-12da29ca3a02120dce8ff699: static service definition.
- fedora-9a52e02b6c7ef113248b233b: static service definition.
- fedora-245444cddcb7003ef53b36b7: static service template, supplies instance definitions.
- fedora-bba51b40dc7e5e7653bec176: disabled service definition.

Additionally all five generated user service definitions were individually inspected: fedora-c9dbd9bdf1fc3c59975f7e12, fedora-b7cf28ddde9848c778fd6e05, fedora-854247fcecbb4e66fc8bfd9b, fedora-985d4a5a2683f835e235312b, and fedora-bb51b9533828b697b1ed77dd. Each is explicitly a generated autostart service. Each supplies process activation, so the same service rule fits. The evidence does not describe them as speed-only caches.

## Verification

The script verified exact identity and cardinality of the assigned input/output IDs, each once, and all decisions in the permitted vocabulary. All rows meet the 15-word function and 30-word reason limits. Result: 813 MUST, 25 NOT, 0 HOLE, 0 UNKNOWN, 0 MIXED.

Review correction: the 25 absent-service reasons now concern the represented absent service itself, not removal of its inventory listing. Decisions and counts remain unchanged.


# c1: system groups, authorization actions, and firewall objects

Scope: 847 rows in the six assigned kinds. Only the supplied part, its raw inventory, the fixed text, and primary documentation were consulted. No objects were removed. The classifier appends and flushes each completed row, preserving existing IDs.

## Deciding text

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”

S3-1 supplies the evidence standard; S3-2 was considered, but the generic operative functions needed for these decisions are established. Neither an actual permission grant nor an actively used group membership is inferred merely from a name.

## Primary documentation

- https://man7.org/linux/man-pages/man5/group.5.html — “The /etc/group file is a text file that defines the groups on the system.” The entry fields identify a system group and its members.
- https://man7.org/linux/man-pages/man3/getgrnam.3.html — “getgrnam, getgrnam_r, getgrgid, getgrgid_r - get group file entry”. The documented lookup maps group names to records and reports absence when no matching record exists.
- https://man7.org/linux/man-pages/man1/chgrp.1.html — “Change the group of each FILE to GROUP.” Its named-group example establishes an operational use of this mapping. This is the upstream command manual reproduced in the manual collection.
- https://polkit.pages.freedesktop.org/polkit/pkaction.1.html — “pkaction is used to obtain information about registered polkit actions.” The raw command is exactly `pkaction`; without verbose output it lists registered identifiers, not successful authorization results.
- https://polkit.pages.freedesktop.org/polkit/polkit.8.html — “A mechanism needs to declare a set of actions in order to use polkit.” The manual describes cross-process authorization between requesting clients and privileged mechanisms, with action defaults and separate authorization rules.
- https://netfilter.org/projects/nftables/manpage.html — “Chains are containers for rules.” Also: “The chain must not contain any rules or be used as jump target.” The latter is the deletion precondition. Tables contain chains and other firewall objects; base chains connect rules to network hooks; helper objects supply named protocol-specific connection tracking.

The two requests to the upstream web version of the group-ownership command manual timed out; its reproduced upstream manual above was available. No experimental probe was needed.

## Homogeneous rule G: system group records — MUST

Apply S2.2-1 and S2.2-2 to the system group identity and name-to-identifier mapping. Removing an entry prevents selecting that identity by its group name for system ownership operations. This is not an assertion that removing a name removes the kernel's numeric group identifier or existing numeric permissions. Nor is it an inference that groups are accounts under S2.2-15. The content exemption does not apply: group selection and ownership operations change, beyond displaying the missing record. The record is used across system programs, not solely inside one program.

Source: `../in/raw/fedora/raw/002-groups.out`, produced by `getent group`. All 83 rows are individual group entries, not grouped directories. Ten rows checked by hand, including empty member lists and explicit supplementary members:

- fedora-bf3968c3ee4b6b46b56352b9 — identifier zero, empty supplementary list.
- fedora-81d3ebc1e32cdaadadd06ebf — identifier ten, one supplementary member.
- fedora-051419ac00bd6f4530b91c71 — identifier 36, one supplementary member.
- fedora-cdc6dd1af931be3d7c954426 — identifier 65534, empty supplementary list.
- fedora-9a53f3c878d66d483b4c3c14 — identifier 59, one supplementary member.
- fedora-f81a1c43861924b6db17a1b5 — identifier 114, empty supplementary list.
- fedora-da1cbce314ddc16627c4051b — identifier 32, empty supplementary list.
- fedora-5b3f6d68da37b1125492dbd8 — identifier 107, empty supplementary list.
- fedora-7f2950438c77270ef864f43a — identifier 42, empty supplementary list.
- fedora-989875f16bc5f7faddfd22ba — identifier 1000, empty supplementary list.

## Homogeneous rule P: registered authorization operations — MUST

Apply S2.2-1 and S2.2-2: action declaration is a prerequisite for mechanisms to perform authorization checks through polkit. The object here is the registered operation, not a human-readable description or an authorization granted to a particular user. These definitions mediate requests between processes, so S2.2-7's single-program setting exemption does not fit. The inventory does not establish the current defaults, and the classification does not invent them. Different operation names do not change the registration function relevant to this rule.

Source: `../in/raw/fedora/raw/087-polkit-actions.out`. Ten rows checked by hand against their identifiers:

- fedora-cb8d2c789a374112fc825a6c — parental-control account-information operation.
- fedora-74a693502cb6731e91793cb6 — directory mount operation.
- fedora-9ad8631bcbff806d7276bdf4 — application parental-control override operation.
- fedora-d826f7637004e4bc0e8d0eb1 — device enrollment operation.
- fedora-a2d1da167acc835765138467 — managed account update operation.
- fedora-500c90df04a2b06279496d3e — suspension with multiple sessions operation.
- fedora-40edc7f41ea98e563bfa54a3 — portable-image management operation.
- fedora-261374587fd389b936a73351 — disk health-information update operation.
- fedora-5dc5ad60a0a5245e5d175f7e — date/time configuration operation.
- fedora-4b9ea5ee69fc1e890eca03ec — low-level USB access operation.

These labels describe the identifier only; the MUST decision relies on documented action-registration semantics, not guessed implementation of the underlying operation.

## Homogeneous rule F: kernel firewall instructions — MUST

S2.2-15 explicitly requires firewall rules. Apply it to all 136 actual `rule` objects in the JSON ruleset, including jumps into empty chains. Their rule status is established by the raw schema, not by earlier inventory classification language. No assumption that each rule changes the final verdict of some currently observed packet is needed for this explicit sentence.

Source: `../in/raw/fedora/raw/080-firewall-nft.out`. Ten rows checked by hand:

- fedora-6041e2be782bf4485a8b070c — unconditional prerouting dispatch jump.
- fedora-95bd3160686c20c63d707bd6 — output-interface conditional jump.
- fedora-5fbb0b0d3a5c12dbb7d88205 — IPv6 destination rejection.
- fedora-fb4cee357f60168281580b05 — output-interface filtering dispatch.
- fedora-6f2076a680a8c3afadbdeac6 — acceptance verdict.
- fedora-395cef7f9d7998d5595b0a6b — jump to empty deny chain.
- fedora-2708de9da8345c5cc45c7865 — jump to empty NAT allow chain.
- fedora-c54c41773dd81473ea8d8e84 — jump to empty output NAT deny chain.
- fedora-7c92415ccc9b4b3f8d491b20 — jump to postrouting tail chain.
- fedora-f15d1f9101d6a5c11fe71a1c — jump to IPv6 policy pre-chain.

## Homogeneous rule C: prerequisites for existing firewall instructions — MUST

Apply S2.2-1 and S2.2-2 to chains that either connect existing rules to a network hook or provide a target used by existing jump/goto instructions. Every regular chain has incoming references in the supplied ruleset; every base chain has contained rules. The script verifies both facts from JSON. Removing a referenced target makes the corresponding existing instructions impossible. This reasoning does not equate an empty chain with an independent filtering rule, and does not claim it changes the final packet verdict. Removing other instructions as well would be a different removal counterfactual. A chain unused by any existing instruction is outside this rule and was not present.

Ten rows checked by hand, including empty targets:

- fedora-5f230e12f63dbb3f1c4fb369 — prerouting hook with a dispatch rule.
- fedora-f3aa6c9931855919cccaf245 — referenced dispatch chain with three rules.
- fedora-e6f248386082280bc6db2d52 — filtering prerouting hook with two rules.
- fedora-eba07334e63c2ed58ef85450 — input hook with six rules.
- fedora-a09e1d191830beff24acacbd — referenced input chain with six rules.
- fedora-7aeffc68321609723be3052a — empty input pre-chain, targeted by handle 166.
- fedora-879cbb5c45893deffca93378 — empty NAT pre-chain, targeted by handle 177.
- fedora-757c1020231e367eaf7e0173 — empty output deny chain, targeted by handle 214.
- fedora-26324e275f3515bbc13660cc — referenced IPv6 allow chain with eight rules.
- fedora-b60d46ad8f22cd89decf21b8 — empty mangling post-chain, targeted by handle 299.

## Individual decisions

- fedora-4e11dec134c34000bcde519b: MUST, S2.2-1 and S2.2-2. The table holds the supplied active chains, 136 instructions, and helper. Removing the container removes that operational firewall configuration.
- fedora-645f6cb16a52b5849f7bbe16: MUST, S2.2-1 and S2.2-2. The NetBIOS UDP helper is selected by rule handle 200 for UDP destination port 137. Removing this definition prevents that helper assignment. It is a protocol-processing object, not merely a historical connection record.

## Verification

`part-fedora.policy.py` checks all firewall member objects against the raw JSON, validates every regular-chain reference and base-chain population, writes append-only rows with immediate flushes, and verifies assigned IDs equal output IDs exactly once. It verifies the decision vocabulary and length bounds. Result: 847 MUST, zero NOT, HOLE, UNKNOWN, or MIXED.


# RPM classification notes

Scope: 3,954 RPM inventory rows representing 1,977 named packages in two inventory contexts. Each input identifier is retained. Installation evidence establishes package presence; it is not used as proof that every package is executable. No object was removed and no machine probe was performed.

## Sources and method

The two RPM inventory outputs are `../in/raw/fedora/raw/004-packages-root-rpm.out` and `../in/raw/fedora/raw/039-packages-user-rpm.out`. Their names, versions and architectures were matched to public package descriptions. The supplied ownership and filesystem outputs are empty and were not used to infer payloads.

Public package descriptions: [https://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/repodata/400ba6e734c9d65d685823ab30724d33c1a11a2c370cd22477e2c843a75636f5-primary.xml.zst](https://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/repodata/400ba6e734c9d65d685823ab30724d33c1a11a2c370cd22477e2c843a75636f5-primary.xml.zst). Public payload listings: [https://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/repodata/b3d721ca63b972a2aa46803df239cbc337d948f9ce14743d4c49c7b156290aab-filelists.xml.zst](https://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/repodata/b3d721ca63b972a2aa46803df239cbc337d948f9ce14743d4c49c7b156290aab-filelists.xml.zst). Selected records were streamed without installing or executing packages. The saved source extraction is (not published: downloaded distribution package metadata). Public repository documentation establishes package purpose; it does not certify byte-for-byte identity with the inventoried versions.

The descriptions contain the following exact functional terms used in rule checks: "policy", "wallpaper", "directories", "Documentation", "Firmware", "font", "library", "metapackage", "module", "plugin", "programs", "data", "Translations". These short quotations refer to descriptions, not to the earlier inventory labels. Detailed functions are paraphrased in the output.

The implementation is `rpm-classify.py`, with individually reviewed cases in `rpm-special.py` and current-run corrections in `rpm-revisions.py`. Settled rows were appended and flushed individually. Later review corrections are retained in `part-fedora.rpm.correction-audit.tsv`; `part-fedora.rpm.corrections.tsv` supplies replacement rows. No earlier classification was consulted.

## Applicable sentences, quoted exactly

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;

- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.

- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.

- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S2.2-16** the boot order and device firmware must be recorded where the system is able to change them.

- **S3-2** If what the object does remains unknown, the case yields ?.

## Homogeneous rules and ten manually inspected rows per rule

### access

MUST (S2.2-1, S2.2-2, S2.2-15): documented access-control policies change which operations are permitted. Policy tools and libraries are separately classified as code.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-401aafc2c93db29a7f5d5188`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-39cf27cf6ac22aa82e3197e4`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-dad5194586ffa57ebd05f2bf`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-3d4376a27db4488991133c68`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-e81c2a9068cf6ee6c9da7cad`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-6106d7b48d4bf43f8eead688`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-690eb0c69aac5b3c98f0a0a8`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-acb236ec9892ce5f40c0f5c6`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-5f51df55119cfdaea7f025f8`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-ee442f3e06d6d5aed46a8f1a`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.

### art

NOT (S2.2-4): decorative pictures, icons, wallpapers, cursors and sounds lose their particular content on removal; the programs using them retain their operations.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-2d9f69baa45edd8c5d7a7e91`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-a18249c9d0fa708e1a1d6876`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-dac714d5ac6cb167e4a9910f`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-079731ebe92e3045b8360192`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-3268c5874ca30fd36dbc7144`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-b356fc11d9d7be7a4dd5483f`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-44a45b04d40a4002cfed09ad`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-c3cf87397d9c67b42cb8aa4a`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-0b9b7984a9eb8451ef2e6bc9`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-62390e1a2474b226d6fa4743`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.

### directories

UNKNOWN (S3-2): documentation identifies directory ownership, but the inventory lacks occupancy and operative dependence on empty directories. No recursive removal is assumed. Packages containing scripts, system-account rules, essential compatibility paths or macros were separated.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-5e338f6bb866db8e2a41edeb`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-a72bbb3ac6e34b6db736c8d9`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-57a389ab36fffa295005c147`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-370f9670318663db7d7af56f`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-4f8074a48708dd529c75b65e`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-d39abe1ddedcb3a27506a9ef`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-041e3807da84dd9e46186c79`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-9053b3a7e45ae753a4a9e8d3`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-f531a43938c67a1109b6ed09`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-8a6c610e96f3dbcc46ae487b`: Owns directories used by other packages. Verified against the description and payload listing.

### documents

NOT (S2.2-4): documentation and license payloads make only their document content unavailable. A documentation directory containing actual executable code is not classified by this rule.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-da3964ef0015cfae111f13df`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-b6269203e737dac13108c5ca`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-7b84a6c2dd78d79e9b065092`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-bb97dc4efa67462e903bb8f3`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-39013d59b6fb9efe514d7c81`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-bfe273ab545974dcd8ac0bf2`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-75345b8b036158dc98895e20`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-c479d4b18ce742f1c1b0b781`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-ffc8a677ec4afd093afcfa2f`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-a33452db9baecef4fd4f3f12`: Supplies documentation or licensing text. Verified against the description and payload listing.

### firmware

MUST (S2.2-1, S2.2-2, S2.2-16): device firmware images and firmware-loading support enable device initialization or updates. Their removal prevents supplying that functionality. Guest firmware and uncertain BIOS deployment are separate cases.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-eaecd855d3b238f815d51e72`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-f733db428ec6a29ecb85d28e`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-f53e71d57d5f3afc074c36c2`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-03c77549892b6a8193035af4`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-1fef7c4b0de4ef9b38eeda7e`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-4aeb8ef58f03412cf56ccd3a`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-d175e0f65161fea9fcb47a66`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-ef952e201e9d3b706b3fe18e`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-661d2912f0d98de7b4160da2`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-fbf97f188c89cc143ec3bd8a`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.

### fonts

NOT (S2.2-4): the payload provides typeface and glyph-shape content. Removing that content leaves rendering programs and algorithms available. Particular designs cease to be available. Operational character-processing rules are separate cases.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-a5b953eef1bebf50abae063b`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-cda4a44cc707192c93f66698`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-8c1cc1fbc16837c841d7b68c`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-14928d3664ea72ff24c8269f`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-3b918dfc4f83c367dcb026cf`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-2ec107617e982d64ea2a92da`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-da70b55dde55d6da634a2481`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-57e4db925137d63d11a40631`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-8c1bbecc2b543f8b3d3e1f83`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-547407149020ad146ca7ed47`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.

### library

MUST (S2.2-1, S2.2-10): documented executable library routines run under the calling program authority. Library-looking names alone were insufficient; descriptions establish runtime-library functionality.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-edb09599722384f6bb836965`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-21e312548b0f8d7d4e2182be`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-f619198a4461ebe7240c5dd8`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-9a450a0179f3679402f3102c`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-55ce98be0c44a6502c367997`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-377d221dd0fcdb2297dc97b4`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-276bb55c296f439e02d1f675`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-2b10e107afcacf2988c7b2af`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-223761c229fbf1974686ac3c`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-bcb572405c43442f9f518ea2`: Supplies executable library routines used by other programs. Verified against the description and payload listing.

### meta

NOT (S2.2-1, S2.2-2): dependency-selection packages lacking runtime payload leave separately installed dependencies available when the selected package is removed. Catalog descriptions, documentation, and licensing material add no runtime operation. An apparently similar package containing executable helper scripts was separated.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-138a10d5278297b267d354ee`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-be5599ad26429f507c08c013`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-8730ac5a39bf84af93b38e20`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-7ea45e943d0bb511c6ebe3b5`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-07515c2535408ee07c36d1f6`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-fca703a8f1ced7ff190c701b`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-438f4ce9019643929958b0b6`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-149f51b465b82779d0c664a1`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-6747d55fa0766abda60b7a7e`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-9599a741b857ba787b4dec0a`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.

### module

MUST (S2.2-10): documented interpreter modules supply executable routines running with interpreter authority. The rule is not applied merely because a name has a language prefix; dependency-only extras were separated.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-27e2d2dc939310b3a9d142fc`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-d0d306da7b26b866dfc2f1c5`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-76997ee765a0cefaf538ea45`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-708c4c2d0a85f498e5b37957`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-49b7a78fbb82a92881309900`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-727574267f9860a5616d294a`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-f17c3f67492a6f5922f38468`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-e8fb5374118fc855a77c2f1d`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-3342f3d007a3e8507fea11c0`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-23a9ae7dc603e18f4eac7ca9`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.

### native

MUST (S2.2-1, S2.2-10): documented plugins, drivers, parsers, codecs and implementation modules supply executable operations within the calling program. Guest-confined firmware is separate. Host-side emulator device implementations are host code, not guest code.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-78a07f368dd66bf0c5c34f6e`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-ba44be2d1b32f9dbc8620e1d`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-92e7cb16325d58b3242234a9`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-8bb8455c1e98d47cd64570cd`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-1c67dbedae42aa60e8d74fb4`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-48d48c2d61923f8c709beb8f`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-bf034164763b7026389b7711`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-c5ea8e158aef9f1932ef4bd2`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-53d2dfb5c3c8dbec48863fec`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-91dd7ff34401ed0f818e2a36`: Supplies executable modules implementing program operations. Verified against the description and payload listing.

### program

MUST (S2.2-9, S2.2-12): command-path payloads or documented standalone daemons/helpers establish executable programs. Their installation method does not change the explicit program requirement.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-2a4f52995c5b6597c9ae4da9`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-40f67601ab760fef41d8c68d`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-f0000db9d3e3bdff190dc1d0`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-e8070a5f3ff2f24403e24375`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-de5e84503da6254598d4ff6b`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-bb9c02d258f9dc2fc6500734`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-dcf5934f834be0b44aff15c8`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-fdb52d37ebe4e4ad86277d77`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-3013dd5332806971f55d351b`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-e915f0e88118eda90fbbc096`: Provides installed executable commands. Verified against the description and payload listing.

### tables

HOLE (S2.2-1, S2.2-2, S2.2-4): non-executable reference tables participate in lookup, validation, spelling, input, or processing. One reading treats losing these particular operations as lost capability; another treats the absent entries as unavailable database content. The text does not specify the boundary between an operation and a lookup of missing content. Each package purpose was checked independently before admission to this rule.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-ddf7aee0dfcb6861fd6c11a4`: Maps encoded characters to glyph identifiers for text rendering. Verified against the description and payload listing.
- `fedora-758ab1b54089d36f3f204298`: Supplies searchable application metadata and software-center icons. Verified against the description and payload listing.
- `fedora-3bee2fde6a0a4c7940913aa4`: Supplies a weather-location database. Verified against the description and payload listing.
- `fedora-ba642d8c7dc65763670a545f`: Supplies Australian English spelling dictionaries. Verified against the description and payload listing.
- `fedora-14c56b96b1d25a343c22e542`: Supplies American English spelling dictionaries. Verified against the description and payload listing.
- `fedora-b792b3d284c8bb4f1a50a00f`: Supplies language-tag and locale reference tables. Verified against the description and payload listing.
- `fedora-30e08c6eb3ac2e6152819be2`: Supplies input maps and language-specific text rendering tables. Verified against the description and payload listing.
- `fedora-d4649655477796f4959ebaf9`: Describes terminal capabilities for terminal-aware programs. Verified against the description and payload listing.
- `fedora-e13fc67638ebe9ce37446135`: Identifies domain suffix boundaries for cookie security decisions. Verified against the description and payload listing.
- `fedora-d2d21c3359edaae41805b76b`: Supplies XML schemas and catalogs used by XML processors. Verified against the description and payload listing.

### translations

NOT (S2.2-4): message catalogs and localized document content supply alternative strings or documents; their absence does not remove the program operations. Locale archives governing collation, parsing and conversion are separate MUST cases.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-7dbeecbdde5eb164d415b5b4`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-61ac71638a43dd6e94f9bf51`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-338b8f40f8960cbf67b044bd`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-58e2a0e95887ed95992d1c20`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-382a4d8641dbb641d7c7f9d0`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-28e9960e5a220ec503448f10`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-7312414364c476331e693454`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-65e9be2f1322a296f55563cd`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-0932683cb5f85283b3295b76`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-07334ecf67889302253474d8`: Supplies translated messages or localized document content. Verified against the description and payload listing.

## Individual distinctions and supporting quotations

- [RPM manual](https://rpm.org/docs/4.20.x/man/rpm.8): "erase individual software packages". The object-removal reasoning removes the selected package, not separately inventoried dependencies. No dependency autoremove operation was assumed.
- [RPM removal implementation](https://raw.githubusercontent.com/rpm-software-management/rpm/master/lib/fsm.cc): `unlinkat(dirfd, path, AT_REMOVEDIR)`. A nonempty directory is not recursively deleted. Missing occupancy information therefore remains an evidence limitation for directory-only packages.
- [Locale documentation](https://man7.org/linux/man-pages/man7/locale.7.html): "This category governs the collation rules used for sorting and regular expressions". The locale archive supplies behavioral rules, unlike translation-only catalogs.
- [Shell extension documentation](https://gjs.guide/extensions/overview/anatomy.html): "The code in `extension.js` is executed in the same process as `gnome-shell`". The five installed extension packages contain this entry-point code, so S2.2-10 applies.
- [RPM keyring documentation](https://rpm.org/docs/4.20.x/man/rpmkeys.8): "Digital signatures cannot be verified without a public key." The imported-key pseudo-package is classified by signature verification, not by the package label.

The package rows represent individual packages, not directory-member groups. A package containing required code together with exempt documentation is MUST: recording the package records its required contribution. No package row was converted into a synthetic MIXED directory group.

Further individually checked distinctions include host daemons packaged as data, shell initialization and kernel-install scripts, account rules in directory packages, guest-only firmware, browser-only administrative pages, and default configurations shared across programs. Macro expansion and stylesheet execution rights remain UNKNOWN when the actual behavior is not established. HOLE is reserved for a textual boundary with established object function.

## Validation

Validated: input/output identifiers have the same set and count, each once; all decisions are allowed; all field word limits pass. Counts: MUST 3380, NOT 450, HOLE 80, UNKNOWN 44, MIXED 0.



## Final verification

The completed output contains 5,887 rows. Input and output ID counters are identical, every ID occurs once, all decisions belong to the five permitted words, and field lengths satisfy the requested bounds. All raw-file references checked exist. No input row has multiple stored members. The current-run review is recorded in `part-fedora.review.md`. The final decision counts are stored in `part-fedora.done`.
