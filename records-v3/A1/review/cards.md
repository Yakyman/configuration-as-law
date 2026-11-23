# Independent review of original cards 1, 2, 3, 5, 6 and 7

**Superseded judgment for card 1:** The initial REFUTED judgment below is withdrawn. The revised CONFIRMED judgment and extent are in `hole-1-notes.md` and `hole-1-extent.tsv`. The original reasoning is preserved below as an audit trail.

Scope: `../../TEXT.md` Sections 2–5, `../../SENTENCES.md`, `../adjudication/HOLES.md`, `../adjudication/rows.tsv`, `../compare/joined.tsv`, and cited inventory/supporting records. This review tests the cards on their stated facts; a fact need not be independently disproved when the proposed contradiction already fails on those facts. No confirmed hole among these six cards, so no full-table confirmed extent is claimed.

## Card 1 — REFUTED

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

The exemption says where a setting is in force, not how many programs read its file. Counting readers replaces its words with a different condition. Reading values determines that an object is a setting; it does not establish the narrower exemption. On the card's explicit premise that effects reach beyond the program, its examples require recording:

| Example | Application of the sentences |
|---|---|
| nixos-009e4f8fbe `/etc/modules-load.d` | Loading kernel modules affects facilities available to other programs; it is not a setting in force only inside the loader. |
| nixos-4d1b734b98 `…-50-coredump.conf` | Kernel parameters govern system behaviour after the applying tool exits. |
| nixos-99f150a190 `…-logrotate.conf` | Rotation/deletion operates on other programs' log files; the exempt past records are distinct from the rules performing rotation. |
| nixos-195e0d56cd `…-etc-systemd-logind.conf` | KillUserProcesses controls survival of other processes, not only logind's own operation. |
| guix-331ca6e362 `…-dbus-configuration` | System bus access policy governs communications between other processes. |
| guix-f8cae21bbc `…-ntpd.conf` | The selected servers determine the system clock used beyond ntpd. |
| coreos-d159c2f1cf `/etc/request-key.d` | The configuration launches helper processes for kernel key requests. |
| coreos-a4c2c16ae9 `/etc/audit` | Audit rules are applied in the kernel; audit daemon log/disk actions also extend beyond values internal to the daemon. |
| debian-desktop-bbe4c8f871 `/etc/netplan` | Generated backend configuration controls the network interface; removal stops its configuration. |
| freebsd-83dfca210b `/var/crash` (`minfree`) | The threshold controls creation of crash dump files on disk. It is not the saved crash record itself. |

Evidence: the matching example entries in `../adjudication/rows.tsv` and `../compare/joined.tsv`; supporting source records in (not published: adjudication scratch) (logind and system configuration), (not published: adjudication scratch) (netplan and savecore), and `(not published: adjudication scratch)`.

## Card 2 — REFUTED

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

The database exception includes its functional qualification: the computer still does and can do the same, and only content is unavailable. The card expressly asserts loss of lookup operations or program functions, so it fails that qualification. The file's being a database is insufficient to satisfy the full sentence; being read as values does not independently exempt it either.

| Example | Application: operation lost beyond merely unavailable content |
|---|---|
| debian-614d6e2913 `netbase` | Service/protocol/RPC name resolution through libc fails. |
| debian-9c32a751d6 `ncurses-base` | Full-screen terminal programs cannot operate on affected terminals. |
| debian-f1ae2388d8 `libmagic-mgc` | File-type identification by libmagic clients fails. |
| debian-b26e3ddcb0 `tzdata` | Applications cannot perform the supplied zone-rule lookups/conversions. |
| debian-425798e82a `/etc/locale.alias` | Locale alias resolution stops working. |
| nixos-7d271b79b7 `…-iana-etc-20251215` | Service/protocol name lookups used by programs fail. |
| nixos-d42821389f `…-glibc-locales-2.42-103` | Programs lose the compiled locale functionality supplied by the archive. |
| coreos-ec7d8d80c0 `/etc/udev` (`hwdb.bin`) | Device-property lookups fail. |
| ubuntu-86abcca5d5 `/var/lib/command-not-found` | Command-to-package suggestion functionality fails. |
| freebsd-1166c4aa4a `/etc/mtree` | Creating the supplied base hierarchy from its specifications fails. |

On the card's own facts, these losses meet S2.2-2 and require recording. Evidence: the example rows in `../adjudication/rows.tsv`, their evidence fields in `../compare/joined.tsv`, the database package file lists in `(not published: adjudication scratch)`, `deb-filelist-ncurses-base.html`, and `deb-filelist-libmagic-mgc.html`; command-not-found provenance in (not published: adjudication scratch).

## Card 3 — REFUTED

S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

The exemption is not the word cache alone. It states what happens after removal. Origin in another file or eventual regenerability is not the stated condition. On the asserted facts, all six examples lose functionality, rather than merely speed, and therefore require recording:

| Example | Application |
|---|---|
| coreos-d9f9f1c4e7 `/etc/ld.so.cache` | The program needing the library cannot load it. |
| debian-53f7b0994c `/var/lib/apt` | Installing from the missing package indexes fails until a separate refresh. |
| nixos-bfd49e603a `/nix/store outside current system closure` | Channel-based rebuild evaluation cannot proceed without the channel. |
| guix-317d6b1fbf `…-glib-schemas` | GSettings programs abort without the compiled schema data. |
| guix-546939a102 `…-manual-database` | apropos/whatis no longer perform their lookup. |
| guix-f62a370c22 `…-gtk-im-modules` | GTK cannot load the specified input-method modules. |

Evidence: corresponding `../adjudication/rows.tsv` notes; profile hook sources in `(not published: adjudication scratch)` and (not published: adjudication scratch); library lookup investigation saved under (not published: adjudication scratch) and `mdapi-pkg-wasmedge-rt.json`. No claim that something named cache is always exempt is present in the numbered sentence.

## Card 5 — OUTSIDE

S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”

S3-1: “**Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.”

The card asks how to remove a runtime reflection separately from the state it reflects. These are questions of treatment of program state, which S2.5-1 explicitly puts outside the definition; it does not supply a general exemption from recording programs or their configuration. S3-1 also permits documentation and observation to establish what an object does, so inability to delete a standalone file is not by itself a gap in the behavioural rule.

| Example | Why the stated problem concerns state treatment |
|---|---|
| coreos-88335c6c87 `unpackaged *.device` | Manager state reflecting currently present devices. |
| debian-18fb2985ed `unpackaged *.mount` | Manager state reflecting/generated from configured or active mounts. |
| debian-0ff15b2741 `unpackaged *.scope` | Manager state grouping currently running processes. |
| debian-253d752b01 `unpackaged *.slice` | Runtime control-group state maintained by the manager. |
| arch-2540fd3280 `swap-swapfile.swap` | Manager state reflecting the active swap area, with no fragment file. |
| silverblue-8d6e6c94ec `dev-zram0.swap` | Manager state reflecting active zram swap, with no fragment file. |
| coreos-0eecaaf2d8 `/var/lib/nfs` | Kernel-maintained rpc_pipefs communication state in a mounted pseudo-filesystem. |

Evidence: (not published: adjudication scratch) (units), (not published: adjudication scratch) (rpc_pipefs), and the named objects' evidence in `../compare/joined.tsv`. This judgment concerns the card's demand for independent removal, not an assertion that every mount configuration is exempt.

## Card 6 — REFUTED

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

Neither sentence says now or immediately. Both concern what the computer does and can do; the second is a positive implication, not a prohibition on the first covering other changed behaviour.

- debian-f17149d114 `/etc/subuid`: on the card's facts, later useradd no longer allocates subordinate UID ranges. The computer's account-creation behaviour depends on this object, so S2.2-1 requires recording it.
- debian-f18cbc897b `/etc/subgid`: the same direct application holds for later allocation of subordinate GID ranges.

Evidence: (not published: adjudication scratch) records the files, absent consumers, and shadow's file-present condition; `../adjudication/rows.tsv` expressly records the later behavioural difference. Restricting the removal test to the present moment adds a restriction absent from the text.

## Card 7 — REFUTED

S2.2-6: “records of the past—logs, history;”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

For debian-47c62f375a `/var/log`, the card distinguishes the directory whose existence selects persistent logging from the past log records it contains. A switch selecting future logging behaviour is not a record of the past; its removal stops persistent logging, so S2.2-2 requires recording that directory's relevant existence. S2.2-6 still exempts the past log records, and neither sentence extends their exemption to everything containing them.

Evidence: `../adjudication/rows.tsv` for debian-47c62f375a and (not published: adjudication scratch) for the package-created journal directory and the documented Storage=auto behaviour. No inheritance of an exemption from contents to container is stated in Sections 2–3.
