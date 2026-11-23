# Executable-candidate classification notes

Scope: 466 assigned rows. The inventory label is ignored. `../in/raw/flatcar/raw/113-code-candidates.sh` selects executable permissions, shebangs, or shell filenames. Its output contains paths, not file contents. Therefore the candidate list is not itself proof of executable code. Public primary documentation and program source identify the functions below. No objects were removed or executed.

## Deciding sentences (exact quotations)

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;

- **S3-2** If what the object does remains unknown, the case yields ?.

## Primary documentation

- https://www.gnu.org/software/grub/manual/grub/grub.html: “Everything else in GRUB resides in dynamically loadable modules.” The image-file discussion identifies `.mod` files as GRUB native modules. They are executable extensions, not merely files marked executable.
- https://raw.githubusercontent.com/rhboot/grub2/master/grub-core/kern/dl.c: `mod->init = (void (*) (grub_dl_t)) sym->st_value;`. Native module symbols are resolved and relocated into GRUB; their initialization code has GRUB's execution privileges.
- https://raw.githubusercontent.com/flatcar/scripts/main/build_library/grub_install.sh: “# Generate a memdisk containing the appropriately generated grub.cfg.” and “# boot.img gets manipulated by grub-bios-setup”. The installer copies/compresses module and list files, embeds load.cfg and grub.cfg.tar, generates core.img/EFI/Xen executables, copies shim and MokManager, and saves patched MBR bytes for restoration. Its target-specific layout matches the inventory. These are semantic identification sources, not proof that each optional module ran during inventory.
- https://raw.githubusercontent.com/rhboot/grub2/master/grub-core/Makefile.am: “# generate global module dependencies list”. The `.lst` rules generate name-to-module maps and module lists for commands, filesystems, partitions, terminals, device-tree drivers, video, cryptography, and dependencies. These are values, not native code.
- https://raw.githubusercontent.com/flatcar/scripts/main/build_library/menu.lst: `kernel  /xen/pvboot-x86_64.elf`. This command selects the Xen bootloader rather than an interface preference.
- https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files: “it reads and executes commands from”. The documented startup/logout paths establish execution by Bash; these files are specifically covered by S2.2-10.
- https://www.gnu.org/software/gawk/manual/html_node/Shell-Startup-Files.html: “containing functions to aid in manipulating the AWKPATH and AWKLIBPATH environment variables.” This identifies both shell drop-ins as executable shell definitions.
- https://raw.githubusercontent.com/gentoo/gentoo/master/app-shells/bash/files/profile.d/00-prompt-command.sh: `eval 'PROMPT_COMMAND=()'`. This drop-in executes code to initialize the prompt-command array, rather than supplying a passive setting.
- https://man7.org/linux/man-pages/man8/useradd.8.html: “create the new user's home directory and copy initial files.” The upstream useradd manual establishes the skeleton's copying role but does not reveal the actual contents of these three inventoried templates.

## Homogeneous rule M: native GRUB modules

Apply only to the 427 `.mod` files in the two installed GRUB platform directories. Documentation establishes that these are loadable native code, and the Flatcar installer specifically places compressed modules there. S2.2-10 requires code executed with its executing program's privileges. GRUB's native module loader supplies those privileges without interface confinement. The same rule covers filesystem, cryptographic, device, and utility modules; no claim that every module was loaded at inventory time is needed to decide the recording requirement. This classification addresses the inventoried computer, not a surrounding virtualization host.

Ten manually checked input rows (checked individual pathname, platform directory, membership record, presence in candidate output, and `.mod` semantic match):

- flatcar-7448f108721fc286a373fef3: `/boot/flatcar/grub/i386-pc/acpi.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-1c84704d39e7c2374054ce7b: `/boot/flatcar/grub/i386-pc/adler32.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-d18ed0114c49adbad77896d5: `/boot/flatcar/grub/i386-pc/affs.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-963a17b6f6604bdc51a9a125: `/boot/flatcar/grub/i386-pc/datehook.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-06f005b6405f60df4ac8a3d1: `/boot/flatcar/grub/i386-pc/gcry_whirlpool.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-a8ba5105a035f510e7ad2666: `/boot/flatcar/grub/i386-pc/luks2.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-17f994f3de9765795d080467: `/boot/flatcar/grub/i386-pc/pxe.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-7bc4d8cd80654c2d82ec3be2: `/boot/flatcar/grub/i386-pc/xnu.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-3845c4685cf7d3661ddec733: `/boot/flatcar/grub/x86_64-xen/gcry_serpent.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-9c9c9b222a2f193273b2964a: `/boot/flatcar/grub/x86_64-xen/zstd.mod` — native module in the documented installed module directory; rule M applies.

## Homogeneous rule L: GRUB value lists

Apply only to 18 platform `.lst` rows, excluding the boot menu `menu.lst`. Their generation rules establish values rather than executable code (S2.2-13). These module-selection values configure only GRUB; S2.2-7 explicitly exempts settings confined to one program. The general capability rule does not defeat that explicit exemption. Decision: NOT.

Ten manually checked input rows (all nine list types on BIOS, plus the corresponding Xen command map):

- flatcar-e5869975107dd1606ec51809: `/boot/flatcar/grub/i386-pc/command.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-1d509ff72f6ebda06a74f24b: `/boot/flatcar/grub/i386-pc/crypto.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-a57831f044e17b543418e523: `/boot/flatcar/grub/i386-pc/fdt.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-7904e536689dfb4920c065e2: `/boot/flatcar/grub/i386-pc/fs.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-85dcb992af130d2188c69228: `/boot/flatcar/grub/i386-pc/moddep.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-0a3e3cfe3ac4624ab107909d: `/boot/flatcar/grub/i386-pc/partmap.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-0e6c4297e1c7ee27ea640213: `/boot/flatcar/grub/i386-pc/parttool.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-cbb532e843582afa0c475968: `/boot/flatcar/grub/i386-pc/terminal.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-772bb06922e0fe319ced9341: `/boot/flatcar/grub/i386-pc/video.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-5c299521082131f80720b170: `/boot/flatcar/grub/x86_64-xen/command.lst` — list type individually matched to its upstream generation rule; rule L applies.

## Remaining rows: individual decisions

Each remaining row has an individual rationale and documentation URL in the TSV. No additional homogeneous rule is applied.

- flatcar-27a9bbed5ceb9ff7953cd293 (.bash_logout): MUST; S2.2-10.
- flatcar-198385181ff22d0d558e1c21 (.bash_profile): MUST; S2.2-10.
- flatcar-ea39cc839176e502604c2907 (.bashrc): MUST; S2.2-10.
- flatcar-37041f258c25177429d46e43 (load.cfg): UNKNOWN; S2.2-10,S2.2-13,S3-2.
- flatcar-334558d67d5b17a1a48f6580 (core.img): MUST; S2.2-9.
- flatcar-fdce05a11eb6580b746ee991 (boot.img): MUST; S2.2-9.
- flatcar-14a05bb2f57c924ebf089310 (mbr.bin): HOLE; S2.2-1,S2.2-2,S2.2-6.
- flatcar-13aed24415f036f8d1bd6cba (grub.cfg.tar): UNKNOWN; S2.2-10,S2.2-13,S3-2.
- flatcar-f0f44dff73a1ee2661dd6c9b (load.cfg): UNKNOWN; S2.2-10,S2.2-13,S3-2.
- flatcar-844d2924dea652c3192b9304 (load.cfg): UNKNOWN; S2.2-10,S2.2-13,S3-2.
- flatcar-b59146c6ef774b9d1e7896fc (grubx64.efi): MUST; S2.2-9.
- flatcar-a9f169a0287b9bcda5746db1 (mmx64.efi): MUST; S2.2-9.
- flatcar-a4945760c4931e2ae3f22053 (bootx64.efi): MUST; S2.2-9.
- flatcar-24dc8be7f77d9dae39bfed08 (pvboot-x86_64.elf): MUST; S2.2-9.
- flatcar-029508e7f993a11ad8cbd8d4 (menu.lst): MUST; S2.2-1,S2.2-2,S2.2-13.
- flatcar-39b74ce4ac43077561ded8b6 (00-prompt-command.sh): MUST; S2.2-10,S2.2-13.
- flatcar-3415242185dd23520c96ddd0 (gawk.csh): MUST; S2.2-10.
- flatcar-d7a371cb24bd93a5b6087625 (gawk.sh): MUST; S2.2-10.
- flatcar-e99d01540d33e0f07a650d86 (.bash_logout): UNKNOWN; S3-2.
- flatcar-20ac2453d5813a360f4d5a48 (.bash_profile): UNKNOWN; S3-2.
- flatcar-b7763493bf96dc9f0d8a962a (.bashrc): UNKNOWN; S3-2.

## Correction audit

Review rechecked five objects after the initial 466-row completion. Their initial decisions were MUST. For load.cfg (three rows) and grub.cfg.tar, the initial rationale incorrectly transferred the embedded copy's execution to the distinct stored source object. They are now UNKNOWN: build-time use is documented, but no captured evidence establishes later consumers of the installed copies. For mbr.bin, the initial removal rationale assumed recovery capability alone decided the case. It is now HOLE: the snapshot also records past bytes, and S2.2-6 does not delimit whether recovery snapshots qualify. This is a scope question about the explicit exemption, not an invented precedence rule.

Corrected IDs:

- flatcar-37041f258c25177429d46e43: MUST → UNKNOWN.
- flatcar-14a05bb2f57c924ebf089310: MUST → HOLE.
- flatcar-13aed24415f036f8d1bd6cba: MUST → UNKNOWN.
- flatcar-f0f44dff73a1ee2661dd6c9b: MUST → UNKNOWN.
- flatcar-844d2924dea652c3192b9304: MUST → UNKNOWN.

Additional exact sentence: S2.2-6: “records of the past—logs, history;”

## Validation

The finish script verifies 466 rows, equal input/output ID sets, uniqueness, permitted decisions, and field word limits. The correction script records the explicit five-row correction. Current totals: MUST 440; NOT 18; HOLE 1; UNKNOWN 7; MIXED 0. No group rows occur in this assigned kind.

## Rule L correction audit

The 18 list rows originally received HOLE, citing S2.2-1,S2.2-7,S2.2-13, because their internal settings affected bootloader capabilities. Review rejected that rationale: S2.2-7 already explicitly exempts settings confined to one program; general capability effects establish no additional ambiguity. All 18 now receive NOT under S2.2-7,S2.2-13. The ten individual checks above remain valid. Native modules and the five earlier individual corrections are unchanged.

- flatcar-e5869975107dd1606ec51809: HOLE → NOT.
- flatcar-1d509ff72f6ebda06a74f24b: HOLE → NOT.
- flatcar-a57831f044e17b543418e523: HOLE → NOT.
- flatcar-7904e536689dfb4920c065e2: HOLE → NOT.
- flatcar-85dcb992af130d2188c69228: HOLE → NOT.
- flatcar-0a3e3cfe3ac4624ab107909d: HOLE → NOT.
- flatcar-0e6c4297e1c7ee27ea640213: HOLE → NOT.
- flatcar-cbb532e843582afa0c475968: HOLE → NOT.
- flatcar-772bb06922e0fe319ced9341: HOLE → NOT.
- flatcar-5c299521082131f80720b170: HOLE → NOT.
- flatcar-6cf96cf62a5c025915a5304f: HOLE → NOT.
- flatcar-169971c66f71b58b99c4405f: HOLE → NOT.
- flatcar-835444a1e99d596b1bb77428: HOLE → NOT.
- flatcar-452c72fd408533fcf34dd6a6: HOLE → NOT.
- flatcar-77796baf3bc41ca5cf2c1fd9: HOLE → NOT.
- flatcar-87d65840836e70d225b4fbf3: HOLE → NOT.
- flatcar-974618a7c5fc08b7d44dc4e8: HOLE → NOT.
- flatcar-a38dc4a119724473b97a7092: HOLE → NOT.
