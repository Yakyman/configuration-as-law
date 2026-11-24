#!/usr/bin/env python3
"""Builds W1/m2/objects.tsv. Quotes are taken verbatim from SENTENCES.md by ID."""
import csv, re, sys, pathlib

NIGHT = pathlib.Path(__file__).resolve().parents[3]
SENT = {}
for line in (NIGHT / "SENTENCES.md").read_text().splitlines():
    m = re.match(r"- \*\*(S8\.\d-\d+)\*\* (.*)$", line)
    if m:
        SENT[m.group(1)] = m.group(2).replace("**", "")

def q(*ids):
    return " | ".join(f'{i} "{SENT[i]}"' for i in ids)

rows_in = list(csv.DictReader(open(NIGHT / "W1/OBJECTS.tsv"), delimiter="\t"))

# ---- decisions per object id -------------------------------------------------
ARCHIVE = ("Two-ways on the stored archive itself: S8.2-9 asks whether the object is code the computer executes; the "
           "computer executes the code inside it at every boot (read as yes: a program, covered by the line from which "
           "the system built it, S8.2-16 'a compiled copy'); read as no, the file is an archive the kernel unpacks, not "
           "executes (S8.2-23 distinguishes only executed-as-code and read-as-values), its unpacked contents exist only "
           "while the computer runs (S8.2-5), and the file is one a program (dracut) wrote as it ran: program record, "
           "S8.2-15, need not be recorded. No sentence says whether a stored container of executed code is code.")

D = {}

D["alma-889f8cd2dae65a248533322a"] = dict(
    decided="two-ways",
    sentence="S8.2-6; S8.2-7; S8.2-8; S8.2-11; S8.2-15; S8.2-16",
    quote=q("S8.2-6", "S8.2-7", "S8.2-11", "S8.2-15", "S8.2-16"),
    decision=("Members obtained with kernel-core and unchanged (vmlinuz, System.map, config, symvers.xz, .vmlinuz.hmac, "
              "modules.builtin, modules.builtin.modinfo) and with kernel-modules-core unchanged (modules.order, "
              ".block, .drm, .modesetting, .networking): Q1, installed object, covered by the package line. The depmod "
              "outputs (modules.dep/.alias/.symbols/.softdep/.devname/.builtin.*.bin and their .bin) and build/source "
              "are in the kernel-modules-core manifest with integrity unknown: FACT_UNKNOWN whether they remain as "
              "received. If as received: Q1, package line. If generated after installation: Q1 no; Q2 no (read as "
              "values, S8.2-23); Q3 is not decided: modules.alias holds device-to-driver values written by the driver "
              "authors that the computer as a whole obeys when it loads drivers (then a setting created during "
              "installation, covered by the package line, S8.2-17), or it is a file depmod wrote as it ran (Q4: "
              "program record, need not be recorded). S8.2-16 names 'a generated list' among what is installed but "
              "does not itself classify. Subdirectories kernel/, vdso/, systemtap/, updates/, weak-updates/ are "
              "separate objects."),
    meaning="yes, covered by another line: the line of the kernel package from which the system generates the module index",
    achievable="yes: the system regenerates the index from the recorded kernel packages on application; no ordinary action is restricted",
    note=("Manifest paths are under /lib, a symlink to usr/lib (D1/in/raw/alma/raw/0004-filesystem.out), so the collector "
          "left the group unresolved; D1/in/raw/alma/package-files.tsv rows 80f12386c89a189116c32abf (kernel-core) and "
          "cb17a1249bcc1797f96db6e8 (kernel-modules-core); members/889f8cd2dae65a248533322a.tsv"),
)

D["microos-a1f877f4c02acd2a5f9a0d97"] = dict(
    decided="two-ways",
    sentence="S8.2-7; S8.2-11; S8.2-14; S8.2-15; S8.2-17; S8.2-23",
    quote=q("S8.2-11", "S8.2-14", "S8.2-15", "S8.2-17"),
    decision=("Q1 no: stored outside packages, ownership complete (D1/in/raw/microos/metadata.json). Q2 no: XML, glob, "
              "magic and cache tables read as values (S8.2-23). Q3: the files are the MIME definitions written by the "
              "authors of the shared database, converted by update-mime-database. If only programs a person runs for "
              "himself or herself obey them, S8.2-14 decides: it launches nothing and grants no access, so a record of "
              "those programs, need not be recorded. If the computer as a whole obeys them, the text does not say "
              "whether a generated copy of author-chosen values is 'a value chosen by a person' (setting created during "
              "installation, covered by the package line, S8.2-17) or a file a program wrote as it ran (program record, "
              "S8.2-15). FACT_UNKNOWN: which programs obey the database."),
    meaning="yes, covered by another line: the line of the package whose definitions the system compiles into this database",
    achievable="yes: the system regenerates the database from the recorded packages on application; no ordinary action is restricted",
    note="D1/in/raw/microos/members/a1f877f4c02acd2a5f9a0d97.tsv; directory itself in raw/0004-filesystem.out",
)

D["void-4ab73c90e99c24b1fb10c341"] = dict(
    decided="two-ways",
    sentence="S8.2-7; S8.2-11; S8.2-14; S8.2-15; S8.2-17; S8.2-23",
    quote=q("S8.2-7", "S8.2-11", "S8.2-14", "S8.2-15", "S8.2-17"),
    decision=("505 per-type MIME XML files (mtime at the package installations of the actions). Q1: FACT_UNKNOWN, "
              "package ownership incomplete on this machine (XBPS manifests unavailable, D1/in/raw/void/metadata.json); "
              "if obtained with a package and as received: installed object, package line. Otherwise the same as the "
              "MicroOS /usr/share/mime object: Q2 no (read as values); if only programs a person runs for himself or "
              "herself obey them, S8.2-14: a record of those programs, need not be recorded; if the computer as a whole "
              "obeys them, setting covered by the package line (S8.2-17) or program record (S8.2-15), the text does not "
              "say which."),
    meaning="yes, covered by another line: the line of the package whose definitions the system compiles into these files",
    achievable="yes: the system regenerates them from the recorded packages on application; no ordinary action is restricted",
    note="D1/in/raw/void/members/4ab73c90e99c24b1fb10c341.tsv (505 rows, none executable)",
)

D["alma-3827efd6d880bbf3bcd0736f"] = dict(
    decided="yes",
    sentence="S8.2-6; S8.2-15; S8.2-2",
    quote=q("S8.2-15", "S8.2-2"),
    decision=("Q1 no: none of the six paths is in any package manifest (D1/in/raw/alma/package-files.tsv). Q2 no: "
              "index.db and CACHEDIR.TAG are read as values, the cat* directories are empty. Q3 no: an index that man-db "
              "computed, not a value a person chose. Q4: a program (man-db) recorded it as it ran: program record "
              "(a cache), need not be recorded."),
    meaning="no",
    achievable="yes: nothing is required; the cache may stay outside the declaration",
    note="D1/in/raw/alma/members/3827efd6d880bbf3bcd0736f.tsv",
)

D["microos-c111706edb49a56b42b0ff18"] = dict(
    decided="yes",
    sentence="S8.2-3; S8.2-6; S8.2-7; S8.2-9; S8.2-11; S8.2-15",
    quote=q("S8.2-3", "S8.2-7", "S8.2-9", "S8.2-11", "S8.2-15"),
    decision=("The /etc of snapshot 1, a previous root: the running root is snapshot 2 (/ and /.snapshots/2/snapshot "
              "share device 41) and the running /etc is device 42; this directory is device 77. It is on the computer "
              "(S8.2-3). Per member: a file obtained with a package installed on the computer and remaining as "
              "received: Q1, installed object, package line (FACT_UNKNOWN: integrity of snapshot paths is not in "
              "package-files.tsv). Code otherwise (shell start-up files, grub.d scripts): Q2, program, line of its own. "
              "passwd, shadow, group, fstab, hostname, locale.conf, vconsole.conf: Q3 no, the computer does not obey "
              "this copy; Q4: written by programs as they ran (useradd, installer), program record, need not be "
              "recorded. Section 8.5 (generations and rollback) is outside the definition and decides nothing here."),
    meaning="no: a retained previous generation, not what is installed or set now",
    achievable="yes: nothing is required for a previous generation; snapshots continue to work",
    note="D1/in/raw/microos/raw/0004-filesystem.out (device fields of /, /etc, /.snapshots/1/snapshot/etc, /.snapshots/2/snapshot); members/c111706edb49a56b42b0ff18.tsv",
)

D["void-982c71cf468c85befb1aa508"] = dict(
    decided="yes",
    sentence="S8.2-6; S8.2-7; S8.2-15; S8.2-2",
    quote=q("S8.2-7", "S8.2-15", "S8.2-2"),
    decision=("aux-cache of ldconfig. Q1: FACT_UNKNOWN only formally (Void package ownership incomplete); if it were "
              "obtained with a package and as received, installed object, package line. Otherwise Q2 no (read as "
              "values), Q3 no (computed by ldconfig, not chosen by a person), Q4: program record (a cache), need not be "
              "recorded."),
    meaning="no",
    achievable="yes: nothing is required",
    note="D1/in/raw/void/members/982c71cf468c85befb1aa508.tsv; D1/in/raw/void/metadata.json (package_ownership_complete false)",
)

D["alma-11d1bad65ac77ce3ba75e65d"] = dict(
    decided="yes",
    sentence="S8.2-9; S8.2-10; S8.2-16; S8.2-20",
    quote=q("S8.2-9", "S8.2-10", "S8.2-16", "S8.2-20"),
    decision=("300 GRUB i386-pc modules, in no manifest (Q1 no). Q2: code that the boot loader executes: program, "
              "belongs to what is installed, must be recorded; S8.2-16: covered by the line from which the system "
              "obtained it (the GRUB i386-pc modules package, copied by grub2-install at installation). FACT_UNKNOWN: "
              "whether this computer boots through BIOS GRUB; if it cannot execute them, S8.2-20: not a program, then "
              "Q3 no, Q4 program record (written by grub2-install as it ran), need not be recorded."),
    meaning="yes, covered by another line: the line of the GRUB package from which the boot-loader installation copied them",
    achievable="yes: the system installs the boot loader from the recorded package on application; no ordinary action is restricted",
    note="D1/in/raw/alma/members/11d1bad65ac77ce3ba75e65d.tsv; no /boot/grub2/i386-pc path in D1/in/raw/alma/package-files.tsv; firmware type is not in the inventory",
)

D["alma-9dacb0f7ce0a31c843d66c4c"] = dict(
    decided="yes",
    sentence="S8.2-6; S8.2-11; S8.2-15",
    quote=q("S8.2-11", "S8.2-15"),
    decision=("mimeinfo.cache of 13 bytes, in no manifest. 13 bytes hold the header '[MIME Cache]' and a newline and "
              "no association line, so it carries no value anyone chose and launches nothing: Q2 no, Q3 no, Q4 program "
              "record (written by update-desktop-database as it ran), need not be recorded."),
    meaning="no",
    achievable="yes: nothing is required",
    note="D1/in/raw/alma/members/9dacb0f7ce0a31c843d66c4c.tsv (size 13); the header length is arithmetic on the held size, content itself is not held",
)

D["alma-b2f53f97f94f1bd5d21e023d"] = dict(
    decided="two-ways",
    sentence="S8.2-11; S8.2-14; S8.2-15; S8.2-17",
    quote=q("S8.2-11", "S8.2-14", "S8.2-15", "S8.2-17"),
    decision=("mimeinfo.cache (6218 bytes), in no manifest; it lists which installed application opens each file type, "
              "collected from the MimeType values of packaged .desktop files. Q2 no (read as values). Q3: if a generated "
              "copy of the values chosen by the application authors counts as 'a value chosen by a person', it is "
              "obeyed by programs a person runs and launches something, so a setting (S8.2-14), created during "
              "installation and covered by the package lines (S8.2-17); if not, a program (update-desktop-database) "
              "recorded it as it ran: program record, a cache (S8.2-15), need not be recorded. The text does not say "
              "which."),
    meaning="yes, covered by another line: the lines of the packages whose .desktop files it indexes",
    achievable="yes: the system regenerates the index from the recorded packages on application; no ordinary action is restricted",
    note="D1/in/raw/alma/members/b2f53f97f94f1bd5d21e023d.tsv; creation cause not in the inventory (configuration-origin.tsv has no row for it)",
)

D["alma-c8b3dbb3f4d639cbde713085"] = dict(
    decided="two-ways",
    sentence="S8.2-8; S8.2-11; S8.2-13; S8.2-15; S8.2-17; S8.2-23",
    quote=q("S8.2-8", "S8.2-11", "S8.2-15", "S8.2-17"),
    decision=("gschemas.compiled, in no manifest: the default values of the installed GSettings schemas and vendor "
              "overrides compiled into one file; its sources include org.gnome.login-screen (what is permitted as a "
              "means of login, obeyed by the login screen). Q1 no (compiled, not received); Q2 no (read as values, "
              "S8.2-23). Q3: read as 'default values chosen by a person that the computer obeys' it is a setting created "
              "during installation, covered by the package lines (S8.2-17); read as a file glib-compile-schemas wrote "
              "as it ran it is a program record, a cache (S8.2-15), need not be recorded. The text does not say whether "
              "a compiled copy of chosen defaults is a value chosen by a person."),
    meaning="yes, covered by another line: the lines of the packages whose schemas it compiles",
    achievable="yes: the system recompiles it from the recorded packages on application; no ordinary action is restricted",
    note="D1/in/raw/alma/members/c8b3dbb3f4d639cbde713085.tsv; schema sources listed in D1/in/raw/alma/package-files.tsv under /usr/share/glib-2.0/schemas/",
)

for oid, extra in {
    "alma-c4a7c6d6eb439eb9d680a65e": "Q1 no: in the kernel-core manifest with integrity 'changed' (recorded installation size differs).",
    "alma-2c25c1a886c5db421b08087b": "Rescue initramfs; Q1 no: in no manifest.",
    "alma-9ba0bbb217552126cc411cf7": "kdump initramfs written during the actions; Q1 no: in no manifest.",
    "void-0d4bff48fce03ced27aa83a4": "Built by dracut when linux6.12-6.12.118_1 was installed in the actions; Q1: no manifest entry (Void ownership incomplete).",
    "void-a6e5bb36a961f99d2e09e83e": "Built by dracut when linux6.18-6.18.64_1 was installed in the actions; Q1: no manifest entry (Void ownership incomplete).",
    "void-86ecf4dcf8ddad2c3dbf136e": "Built at installation for kernel 6.12.11_1, whose package was replaced by 6.12.118_1 in the actions; on the 'program' reading nothing recorded builds it, so it needs a line of its own.",
}.items():
    D[oid] = dict(
        decided="two-ways",
        sentence="S8.2-5; S8.2-9; S8.2-15; S8.2-16; S8.2-23",
        quote=q("S8.2-9", "S8.2-23", "S8.2-5", "S8.2-15"),
        decision=extra + " " + ARCHIVE,
        meaning=("yes, by a line of its own or removed with its kernel: it boots a kernel whose package is no longer installed"
                 if oid.startswith("void-86ec") else
                 "yes, covered by another line: the kernel and initramfs-generator package lines (and the settings it copies) from which the system builds it"),
        achievable=("yes: the system either records the kept kernel or removes it on application; installing packages is not restricted"
                    if oid.startswith("void-86ec") else
                    "yes: the system rebuilds it from recorded lines on application; no ordinary action is restricted"),
        note="metadata in W1/OBJECTS.tsv members (mode 0600, executable false); manifest facts in D1/in/raw/<machine>/package-files.tsv; Void kernel change in D1/in/control/void/actions-logs/actions-logs/ (linux6.12 6.12.11_1 -> 6.12.118_1)",
    )

D["alma-632511e739337dc6b0644fd0"] = dict(
    decided="two-ways",
    sentence="S8.2-9; S8.2-10; S8.2-15; S8.2-16; S8.2-23",
    quote=q("S8.2-9", "S8.2-16", "S8.2-23", "S8.2-15"),
    decision=("Members not in any manifest. vmlinuz-0-rescue: Q2, a program (a kernel), covered by the line from which "
              "the system obtained it (copy of the kernel-core kernel, S8.2-16). .vmlinuz-0-rescue hmac: Q2 no, Q3 no, "
              "Q4 program record. initramfs-0-rescue and kdump initramfs: two-ways, see their own rows (archive of "
              "executed code: program by S8.2-9 or program record by S8.2-23/S8.2-15). efi/ and loader/ are separate "
              "objects."),
    meaning="yes, covered by other lines: the kernel, rescue and kdump package lines from which the system builds these files",
    achievable="yes: the system rebuilds them from recorded lines on application; no ordinary action is restricted",
    note="D1/in/raw/alma/members/632511e739337dc6b0644fd0.tsv",
)

D["void-386e90812bdecbec21d0785c"] = dict(
    decided="two-ways",
    sentence="S8.2-7; S8.2-9; S8.2-10; S8.2-15; S8.2-16; S8.2-23",
    quote=q("S8.2-7", "S8.2-9", "S8.2-16", "S8.2-23", "S8.2-15"),
    decision=("vmlinuz-6.12.11_1 and config-6.12.11_1 remain from package linux6.12-6.12.11_1, which the actions replaced "
              "by 6.12.118_1 (package-files.tsv lists only the new versions). vmlinuz-6.12.11_1: Q1 no (its package is no "
              "longer installed), Q2 yes (a kernel the boot loader can start), a program; nothing recorded builds it, "
              "so a line of its own (S8.2-16). config-6.12.11_1: Q2 no, Q3 no, Q4 program record (written by the "
              "installer as it ran), need not be recorded. The three initramfs files: two-ways, see their own rows. "
              "grub/ is a separate object."),
    meaning="yes: the kept previous kernel by a line of its own (or removed); the initramfs files covered by the kernel and generator package lines",
    achievable="yes: the system either records kept kernels or removes them on application; installing and updating packages is not restricted",
    note="D1/in/raw/void/members/386e90812bdecbec21d0785c.tsv; D1/in/raw/void/package-files.tsv (/boot rows of 6.12.118_1 and 6.18.64_1 only); D1/in/control/void/actions-logs/actions-logs/",
)

D["microos-62ccb03ff56e2af8ff91ff68"] = dict(
    decided="two-ways",
    sentence="S8.2-3; S8.2-9; S8.2-15; S8.2-23",
    quote=q("S8.2-3", "S8.2-9", "S8.2-23", "S8.2-15"),
    decision=("/boot of snapshot 1, a previous root (running root is snapshot 2, device 41; this is device 76). Symlinks "
              "into that snapshot's kernel files; mbrid written by the installer (Q4 program record); "
              "initrd-7.3.5-1-default, an initramfs archive: two-ways as for the other initramfs objects (program by "
              "S8.2-9 or program record by S8.2-23 and S8.2-15). On the computer (S8.2-3), so it is decided like any "
              "other stored object; Section 8.5 decides nothing here."),
    meaning="no: a retained previous generation",
    achievable="yes: nothing is required for a previous generation; snapshots continue to work",
    note="D1/in/raw/microos/members/62ccb03ff56e2af8ff91ff68.tsv; D1/in/raw/microos/raw/0004-filesystem.out (device fields)",
)

EXT = dict(
    decided="two-ways",
    sentence="S8.1-5; S8.1-6; S8.2-1; S8.2-6; S8.2-7; S8.2-8; S8.2-16; S8.2-21",
    quote=q("S8.1-5", "S8.1-6", "S8.2-7", "S8.2-1", "S8.2-21", "S8.2-6"),
    decision=("The .xpi of the ClearURLs add-on, installed through the browser's own add-on installation "
              "(browser_extension action via the browser's remote protocol). The browser counts as an installer in "
              "that part (S8.1-5), the add-on is what it installs and removes as a whole (S8.1-6): Q1, an installed "
              "object; S8.2-1: must be recorded, by a line of its own (S8.2-16). S8.2-21: code that runs inside a "
              "recorded program (the browser package) and cannot itself launch programs or change what is installed "
              "and the computer's settings need not be recorded. If the add-on can do neither, S8.2-1 and S8.2-21 decide "
              "in opposite ways, and S8.2-6 only fixes the order of the questions, not which of the two prevails. "
              "FACT_UNKNOWN: the add-on's permissions (the .xpi content is not in the inventory); if it can launch "
              "programs or change settings, Q1 and S8.2-1 decide alone."),
    meaning="yes, by a line of its own",
    achievable="yes: the browser's installer can add the add-on to the declaration as it installs it (the mechanism is outside the definition, 8.5); installing an extension stays allowed",
)
D["alma-2ea4b9f74eb9ce06f9d317ff"] = dict(EXT, note="D1/in/raw/alma/members/2ea4b9f74eb9ce06f9d317ff.tsv; D1/in/control/alma/actions-logs/browser_extension.log; Section 8.6 row 'A browser extension' reads it as recorded but is reasoning, not Sections 8.1-8.2")
D["void-61a9a88ad2b852b6cf106db6"] = dict(EXT, note="D1/in/raw/void/members/61a9a88ad2b852b6cf106db6.tsv; D1/in/control/void/actions-logs/actions-logs/browser_extension.log")

PKG = dict(
    decided="yes",
    sentence="S8.2-6; S8.2-7; S8.2-8; S8.2-1; S8.2-16",
    quote=q("S8.2-7", "S8.2-8", "S8.2-1", "S8.2-16"),
    meaning="yes, by a line of its own",
    achievable="yes: a recorded compiler stays usable; recording it restricts no ordinary action",
)
for oid, name in {"developer-763fc6a0cbe95f3edf0f2342": "make", "developer-718b98d43973ff60a8c3751b": "gcc",
                  "developer-b46f412ae8c4316f8b6ec549": "gcc-c++"}.items():
    D[oid] = dict(PKG,
        decision=(f"rpm package {name}, installed, reason explicit: Q1, an installed object; must be recorded (S8.2-1); "
                  "explicit, not a dependency of a recorded package, so by a line of its own (S8.2-16). Whether the "
                  "program also counts as an installer or built-in tool (S8.1-4, S8.1-7) does not change what it is or "
                  "its line."),
        note=f"A3/in/raw/developer/objects.tsv id {oid.split('-',1)[1]}; reason from raw/0014-package-reasons-dnf.out")

HOME_DEC = ("Members that bash executes as code at start-up or logout ({rc}): code by S8.2-23, Q2 program, not "
            "obtained as received with a package (Q1 no), so a line of its own. .bash_history: two-ways. Read by S8.2-9 "
            "it is code the computer can execute at a person's command (shell statements that bash replays with fc or "
            "!n, or runs as a script): a program, line of its own. Read by S8.2-23 bash only reads the file as values "
            "into its history list: not code, Q3 no, Q4 'history' named in S8.2-15: program record, need not be "
            "recorded. Nothing says which reading prevails. {other}")
D["developer-edb6bded22471341205ed0df"] = dict(
    decided="two-ways",
    sentence="S8.2-4; S8.2-9; S8.2-10; S8.2-15; S8.2-16; S8.2-23",
    quote=q("S8.2-9", "S8.2-23", "S8.2-15", "S8.2-4"),
    decision=HOME_DEC.format(rc=".bashrc, .bash_profile, .bash_logout",
        other=("actions-status.tsv: written by the action runner as it ran, Q4 program record. Subdirectories (.bun, "
               ".cache, .config, .julia, .juliaup, .local, .ssh, Projects, actions-logs, bin) are separate objects.")),
    meaning="yes by lines of their own for the shell start-up files; no for .bash_history and actions-status.tsv",
    achievable="yes: start-up files can be files of the declaration itself (S8.1-3 lets a person designate them); history and logs need nothing",
    note="A3/in/raw/developer/members/edb6bded22471341205ed0df.tsv; content of .bash_history is not in the inventory (signature only), the reading does not depend on it",
)
D["gaming-91c3f417acf495b9dc03a2d5"] = dict(
    decided="two-ways",
    sentence="S8.2-4; S8.2-9; S8.2-10; S8.2-14; S8.2-15; S8.2-16; S8.2-23",
    quote=q("S8.2-9", "S8.2-23", "S8.2-15", "S8.2-14"),
    decision=HOME_DEC.format(rc=".bashrc, .profile, .bash_logout",
        other=(".gtkrc-2.0, .gtkrc-xfce: values read by the person's own GTK programs, launch nothing: record of those "
               "programs (S8.2-14). .steampath, .steampid, .sudo_as_admin_successful, actions-status.tsv: written by "
               "programs as they ran, Q4 program record. Subdirectories are separate objects.")),
    meaning="yes by lines of their own for the shell start-up files; no for .bash_history and the other files",
    achievable="yes: start-up files can be files of the declaration itself (S8.1-3 lets a person designate them); history and records need nothing",
    note="A3/in/raw/gaming/members/91c3f417acf495b9dc03a2d5.tsv; content of .bash_history is not in the inventory (signature only), the reading does not depend on it",
)

COLS = ["gap", "id", "decided", "sentence", "quote", "decision", "meaning_answer", "achievable", "note"]
out = open(NIGHT / "W1/m2/objects.tsv", "w", newline="")
out.write("\t".join(COLS) + "\n")
n = 0
for r in rows_in:
    d = D[r["id"]]
    vals = [r["gap"], r["id"], d["decided"], d["sentence"], d["quote"], d["decision"], d["meaning"], d["achievable"], d["note"]]
    assert all("\t" not in v and "\n" not in v for v in vals), r["id"]
    out.write("\t".join(vals) + "\n")
    n += 1
out.close()
print(n)
