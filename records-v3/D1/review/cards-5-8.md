# Review of cards 5–8

Recorded 2026-11-22 UTC. Read with `../../TEXT.md` Sections 2–5 and `../../SENTENCES.md`; examples and facts are checked against `../compare/joined.tsv`, `../adjudication/rows.tsv`, and the evidence below. No removal experiment was added.

## Card 5 — REFUTED as an established inventory counterexample; factual applicability UNKNOWN

S3-2: “If what the object does remains unknown, the case yields ?.”

The source card assumes that current device absence makes removal inert and that the missing device could be attached. The saved inventories establish current bound drivers, not both of those premises for these objects. They do not establish an actual object on which the alleged hardware-scope ambiguity decides between MUST and NOT. This is an evidentiary refutation under S3-2, not a claim that S2.2-1 settles every possible hardware counterfactual.

The independent challenge in `card5-challenge.md` retains the two readings for the record: operations on fixed observed hardware versus operations after a hardware addition. The latter is not merely a delayed action by an existing program. No choice between those readings is used to assert a confirmed inventory hole.

The original seven example objects are: `fedora-94e7f0db6259f31f490e456b` root:qcom-wwan-firmware; `fedora-9f61c67c043a3651bdaf564b` user:b43-openfwwf; `tumbleweed-616fcce7fd547116d0d09fc7` root:wireless-regdb; `fedora-1b58d19cc948a0cd43fcb240` root:usb_modeswitch-data; `fedora-6e50f07c99ff596cc9d0fc4c` root:alsa-ucm; `tumbleweed-9767c3f823fd0b3c16059410` user:libwacom-data; `tumbleweed-c77416992eb1732fe822e2b9` root:media-player-info. Four Fedora examples have an independent MUST reason: exact installed dependency metadata in (not published: adjudication scratch) requires linux-firmware-whence for qcom-wwan-firmware; module-init-tools and udev for b43-openfwwf; systemd and usb_modeswitch for usb_modeswitch-data; and alsa-lib for alsa-ucm. Those package-manager constraints satisfy S2.2-1, independently of their hardware payload. The other three original examples are independently MUST as well: installed libwacom9 requires libwacom-data and patterns-base-enhanced_base recommends wireless-regdb in the exact-version Tumbleweed metadata; media-player-info requires /bin/sh. Installed Fedora libwacom also requires libwacom-data. Thus all seven original examples are decided by S2.2-1; among all 58 original card rows only the two alsa-sof-firmware rows retain unresolved whole-object facts. Driver lists alone do not prove their entire present or possible use.

Evidence and exact search membership: `card5-extent.tsv` searches the entire joined table by kind/name, including agreed firmware packages and inactive boot-module paths. Its final statuses incorporate independently deciding package metadata; no actual inventory row is proved to instantiate the alleged hardware-scope gap. All 58 original rows were found. Membership uncertainty is separate from a complete reclassification of the objects and must not be added mechanically to object UNKNOWN totals.

## Card 6 — REFUTED

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”

S2.5-3: “Nor is the form of the declaration part of the definition: it may be a list or an algorithm that computes what is recorded.”

All six examples are described as operational inputs on which behaviour depends, so S2.2-1 decides MUST. Their later regeneration does not negate that dependency; the text does not say that every negative removal test is an exemption, or that every automatically recreated file is cache. Whether a declaration computes the object or lists it is explicitly outside the definition. A genuinely dispensable cache would instead have to satisfy S2.2-5's stated condition; regeneration alone does not establish it.

| Example id | Name | Application of S2.2-1 |
|---|---|---|
| tumbleweed-106b78a49881386e5c2089f8 | user:app-org.kde.discover.notifier@autostart.service | The generated unit controls the notifier's automatic launch. |
| flatcar-769ce88f8a54e2150b5cbec9 | /run/systemd/generator/serial-getty@.service.d | The drop-in controls serial-getty autologin. |
| flatcar-e8c3dd1b118f12e4905f5300 | /run/systemd/generator/sockets.target.wants | The generated link selects the socket to activate. |
| flatcar-6abd3cc93dfc5b3e66f60427 | /run/systemd/generator.late | Generated mount/automount units control the boot mount. |
| flatcar-778d999ce314fbfc50ce240f | /run/tmpfiles.d | The generated static-node list controls device-node creation. |
| flatcar-b9083577b011da27bfb86f15 | /run/systemd/resolve | The resolver configuration supplies the name-resolution settings read by clients. |

The directory entries contain those MUST members; this does not make every other member MUST. Evidence: `../in/raw/tumbleweed/raw/072-user-user-unit-file.out`, `../in/raw/flatcar/raw/105-filesystem.out`, and the matching notes in `../adjudication/rows.tsv` establish their roles. This refutation accepts the card's operational-dependency premise and shows that regeneration supplies no contrary sentence.

## Card 7 — FACT-WRONG

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.2-11: “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.”

The card substitutes having some effects through an API for being able to do whatever the executing program can do. Conversely, code using an interface is not thereby confined to that interface. Its examples do not establish both predicates at once:

| Example id | Name | Factual check |
|---|---|---|
| fedora-d23b5ec58a99a2d5dd98c6d0 | root:cockpit-storaged | Browser code requests operations from a separate server-side bridge. The bridge's rights are not the browser program's rights. |
| fedora-d1549cca8e2e2802d54afae6 | user:cockpit-system | The same browser/bridge separation applies. System management effects do not establish unrestricted execution with the browser's rights. |
| tumbleweed-b8d3bce61d0c4d8c4fd618cc | user:plasma6-theme-openSUSE | Layout scripting and QML are different mechanisms; being executed through an API does not establish confinement. The package contains both. |
| tumbleweed-c225ad126cda23f96aa4609e | user:plasma6-sddm-theme-openSUSE | QML is not a security confinement merely because it draws a greeter; its execution must not be equated with a sandboxed web page. |
| tumbleweed-458bd2d25764f4b4b0aa2150 | user:libreoffice-filters-optional | The installed 26.8.1.1 transformer explicitly forbids file writes, directory creation and network access by XSLT, while permitting local file reads. It cannot do whatever the office program can do. |
| tumbleweed-58bfaed75b767465bff8e84a | user:augeas-lenses | Lenses describe text/tree transformations. Selecting a configuration file and transforming its contents does not supply unrestricted host-program operations. The adjudication itself records no I/O primitives. |

Primary evidence, saved under `D1/review/raw/` with URL manifest `raw/sources.json`:

- [Cockpit developer guide](https://docs.cockpit-project.org/cockpit-guide/368/guide/development.html): “On the server side the man:cockpit-bridge[1] connects to various system APIs that the front end UI requests it to.” Saved as `cockpit-development.html`. This identifies two executing components, not one shared browser privilege context.
- [Qt handling untrusted data](https://doc.qt.io/qt-6/untrusteddata.html): “QML does not have the concept of separate privacy domains.” Saved as `qt-untrusted.html`. This refutes an assumption of QML confinement; it does not by itself classify every installed QML package.
- [LibreOffice 26.8.1.1 source](https://raw.githubusercontent.com/LibreOffice/core/libreoffice-26.8.1.1/filter/source/xsltfilter/LibXSLTTransformer.cxx), lines 322–339, saved as `libreoffice-xslt.cxx`; installed version in `../in/raw/tumbleweed/raw/004-packages-root-rpm.out`. The explicit security preference loop contradicts unrestricted rights.
- [Augeas lens reference](https://augeas.net/docs/lenses.html): “Lenses are the basic building blocks for establishing the mapping from files into the Augeas tree and back.” Saved as `augeas-lenses.html`; see its documented primitives and combinators. Package payloads are in (not published: adjudication scratch).

This rejects the factual basis of the proposed collision. In addition, all 14 package rows have an independent MUST reason under S2.2-1: installed dependency metadata controls package-manager selection. The six Fedora Cockpit rows require the bridge and other operational packages ((not published: adjudication scratch)). Exact-version Tumbleweed metadata in (not published: downloaded distribution package metadata) shows that augeas-lenses requires libaugeas0; libreoffice-filters-optional requires the office component programs; and both Plasma theme packages require their shell/QML runtime components and wallpaper packages. Versions match D1/in/raw/tumbleweed/raw/004-packages-root-rpm.out. Therefore the still-unestablished QML execution privileges do not leave these whole-package rows UNKNOWN. The package verdict does not assert a separate verdict for every payload member.

## Card 8 — FACT-WRONG for the package premise; guest-code collision REFUTED

S2.2-11: “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.”

S2.2-12: “This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.”

The text explicitly calls this an exemption. Code executed only in the guest is precisely the exempted object, whereas the host emulator is required. Needing guest code to boot a guest does not convert it into a host process. However, the inventory objects are packages: the file lists for both edk2-ovmf and seabios-bin also contain host-read firmware-selection descriptors under /usr/share/qemu/firmware. Thus the card’s code-only premise is false for those packages, and the guest-code exemption cannot classify their entire payloads.

| Example id | Name | Literal decision |
|---|---|---|
| fedora-8a717666be03995676d7c21d | user:edk2-ovmf | Guest UEFI code is NOT; package is MUST through host firmware-selection descriptors used by installed libvirt to configure QEMU. |
| fedora-729138f682023c574071c098 | root:seabios-bin | Guest BIOS code is NOT; package is MUST through 80-seabios-default.json and 80-seabios-microvm.json used by installed libvirt to configure QEMU. |
| fedora-21a722be1d318ec0f86e5189 | user:ipxe-roms-qemu | NOT: the emulated NIC option ROM runs inside the guest. |
| fedora-d42127df5b3b98e4059e07bb | user:seavgabios-bin | NOT: the emulated VGA option ROM runs inside the guest. |

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

Evidence: named entries in (not published: adjudication scratch); the card and matching adjudication notes establish the guest-code execution context but overlook the package-level descriptor issue. `cards-6-8-check.md` records the independent correction. The follow-up establishes the consumer: D1/in/raw/fedora/raw/004-packages-root-rpm.out lists libvirt-daemon-driver-qemu 12.6.0-2.fc45 and qemu-kvm 11.1.2-1.fc45. The [libvirt domain-format specification](https://libvirt.org/formatdomain) states: “The selection process scans for files describing installed firmware images” and explicitly lists /usr/share/qemu/firmware. 

Thus the descriptor participates in configuring a separate emulator process, deciding MUST by S2.2-1, consistently with card 4. This is available functionality; an already running guest is unnecessary. No new textual hole is demonstrated.
