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
