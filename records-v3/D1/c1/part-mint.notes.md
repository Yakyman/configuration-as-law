# Classification c1: part mint

Only COMMON.md, TEXT.md Sections 2 and 3, SENTENCES.md, this input part, its raw inventory, and public documentation were used. No removals or machine probes were performed. Inventory classification language was disregarded. This part contains individual account, group, and package objects; its `members` cells are JSON lists, not numerical group sizes.

## Deciding sentences for account and group rules

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”

S3-2: “If what the object does remains unknown, the case yields ?.”

## Rule A: account entries

Apply MUST under S2.2-15 to the 48 account objects. The inventory command is `getent passwd` (D1/in/raw/mint/raw/001-accounts.sh); every member is a seven-field account entry. The object is the account, not the separate password. The shell can disable interactive login without changing the fact that an account exists. The script checks the member shape and appends each result immediately.

Primary documentation: https://man7.org/linux/man-pages/man5/passwd.5.html — “The /etc/passwd file is a text file that describes user login accounts for the system.” The documented fields establish identity, primary group, and login environment. Actual row values come from D1/in/raw/mint/raw/001-accounts.out.

Ten manually checked rows, including ordinary, special-purpose and disabled-login accounts:

| ID | Raw line | Check |
| --- | --- | --- |
| mint-5c5eccdd174330ced50eb5b5 | 1 | Numeric identity zero and interactive shell; account rule applies. |
| mint-17392cade12061eb0faefc18 | 5 | Special-purpose shell; still an account. |
| mint-6f5770ff4128a75451a53cb6 | 10 | Service identity with nologin shell. |
| mint-7996a837561515a1930e9fd6 | 15 | Mailing service identity with nologin shell. |
| mint-a9c53dec9fdf5cea9d7ce89b | 20 | Time service account and numeric group. |
| mint-811bb0167d5526ddfc928ec0 | 25 | Policy service account and numeric group. |
| mint-bde291fca4b659593ce1b038 | 30 | UUID service identity with nologin shell. |
| mint-d68d457313e92ddc4d608567 | 35 | DNS service identity with nologin shell. |
| mint-f9dd740c06843ced4c93e8b7 | 40 | Speech service account with false shell. |
| mint-abab13f01e23dcfddcf0ca38 | 48 | Identity service account with nologin shell. |

## Rule G: system group definitions

Apply MUST under S2.2-1 and S2.2-2 to the 78 group objects. The inventory command is `getent group` (D1/in/raw/mint/raw/002-groups.sh). Each four-field entry defines a group name, numeric group identity, and supplementary member list. Removing the definition prevents using that group identity by name for ownership and credential operations. The removal argument does not assume that files are currently owned by every group, or that empty supplementary membership means an unused group. Numerical ownership can remain after deletion; that does not preserve named identity operations. These are system identity definitions used across programs, not settings confined to one program or documents whose only role is displaying their content.

Primary documentation and short exact passages:

- https://man7.org/linux/man-pages/man5/group.5.html — “The /etc/group file is a text file that defines the groups on the system.”
- https://man7.org/linux/man-pages/man3/getgrnam.3.html — “or NULL if the matching entry is not found”. The documented API maps group names and identifiers through the group database.
- https://man7.org/linux/man-pages/man1/chgrp.1.html — “Change the group of each FILE to GROUP.” Its example uses a group name.
- https://man7.org/linux/man-pages/man7/credentials.7.html — “This is a set of additional group IDs that are used for permission checks when accessing files and other shared resources.”

Actual definitions are in D1/in/raw/mint/raw/002-groups.out. Ten entries were checked manually, spanning empty and populated supplementary membership, primary service groups, and privilege-related names:

| ID | Raw line | Check |
| --- | --- | --- |
| mint-3136b62060275c8fadd91328 | 1 | Group identity zero; empty supplementary list does not erase named identity. |
| mint-2c82f05b6c0de4580bd403c3 | 5 | Named group with two supplementary members. |
| mint-57580dfdf8374b94021919bb | 13 | Service group identity with empty supplementary list. |
| mint-75d1185b7139b087daf57f7a | 21 | Named group with one member; no unobserved privilege rule assumed. |
| mint-2a6d75cc8d6c83eeb0000709 | 29 | Empty supplementary list; named identity operation remains the removal test. |
| mint-9b54f9c71f99640a51d4e9dc | 37 | Named group with one supplementary member. |
| mint-1ae8becb3f9d9632fd1f0928 | 45 | Empty group list; no specific device permission assumed. |
| mint-ebb2156f5d946a18a6982fa1 | 53 | Named service group and numeric identifier. |
| mint-23169a70e48971ae8b22d2d2 | 65 | Named service group and numeric identifier. |
| mint-424eaad680639755098a3b98 | 78 | Named group and numeric identifier with empty supplementary list. |

The account/group application script is part-mint.accounts-groups.py. Package reasoning and checks are recorded in part-mint.1.notes.md, part-mint.2.notes.md, and part-mint.3.notes.md and incorporated into this notes file when complete.

<!-- Consolidated component notes -->

---

Source record: part-mint.1.notes.md

# Package classification notes, assigned first segment

Scope: first 635 dpkg-query rows. No earlier classification was consulted. Installed identities and versions were established from the supplied inventory. Public archive metadata establishes package function; archive descriptions are not inventory classifications. No objects were removed and no machine experiments were run.

Each inventory row here is one package, not a directory group of independently enumerated members. A package containing runnable code is classified by the contribution of that code; accompanying manuals do not turn the entire package into exempt content. Dependency-only packages were examined separately.

## Sentences used

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-16** the boot order and device firmware must be recorded where the system is able to change them.
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Homogeneous rules and manual checks

No name prefix alone determines executable status. The explicitly selected ordinary-program and runtime-library sets were read against their package descriptions. Data, configuration, firmware, compiler dependency packages, debugging packages and common-file packages received separate examination.

R1: A package supplying an independently runnable program is MUST under S2.2-9. The following ten entries were checked manually: each description identifies the executable and its task.

- `mint-2fefc3b8c16ec0f56484edbe` (`7zip`): “7-Zip file archiver with a high compression ratio”; checked against MUST rationale.
- `mint-bd39a4b50da417df00c2ed50` (`aardvark-dns`): “Container-focused DNS server”; checked against MUST rationale.
- `mint-f797f068d0ef2976862c010a` (`accountsservice`): “query and manipulate user account information”; checked against MUST rationale.
- `mint-6ea8e65211f3781437f7f7d4` (`acl`): “access control list - utilities”; checked against MUST rationale.
- `mint-87ba567c3238acd25165e3c4` (`adduser`): “add and remove users and groups”; checked against MUST rationale.
- `mint-830aa35501eb790fcfdd3ec6` (`alsa-utils`): “Utilities for configuring and using ALSA”; checked against MUST rationale.
- `mint-79ef6e77e3a19e49879c881d` (`anacron`): “cron-like program that doesn't go by time”; checked against MUST rationale.
- `mint-cd7b0939c55f505e0c2dd134` (`apg`): “Automated Password Generator - Standalone version”; checked against MUST rationale.
- `mint-8efdad51d1629955aed654f7` (`apparmor`): “user-space parser utility for AppArmor”; checked against MUST rationale.
- `mint-fc1849859d4f829a7eebd8c8` (`apt`): “commandline package manager”; checked against MUST rationale.

R2: A documented executable library or native runtime module is MUST under S2.2-10 and S2.2-13: the caller executes its code with the caller’s rights. This rule excludes detached symbols, development data and common-file packages. Ten manually checked entries follow.

- `mint-18b7e44d1c0c7dc9eb446aa6` (`libaa1`): “ASCII art library”; checked against MUST rationale.
- `mint-7080b3647d35809c7e0ee687` (`libabsl20220623t64`): “extensions to the C++ standard library”; checked against MUST rationale.
- `mint-2ba6a194b244a3386c326c52` (`libabw-0.1-1`): “library for reading and writing AbiWord(tm) documents”; checked against MUST rationale.
- `mint-22b27c537106c98e4554e21e` (`libaccountsservice0`): “query and manipulate user account information - shared libraries”; checked against MUST rationale.
- `mint-88ac1ecee4af06163c0684f3` (`libacl1`): “access control list - shared library”; checked against MUST rationale.
- `mint-a7fc920ee57e0b45f388b00e` (`libadwaita-1-0`): “Library with GTK widgets for mobile phones”; checked against MUST rationale.
- `mint-7da534cefd43b685e5a481cb` (`libaio1t64`): “Linux kernel AIO access library - shared library”; checked against MUST rationale.
- `mint-7c415b17bb0b9a2c1ae267bd` (`libao4`): “Cross Platform Audio Output Library”; checked against MUST rationale.
- `mint-4851fbe3937eac150dcc43c9` (`libaom3`): “AV1 Video Codec Library”; checked against MUST rationale.
- `mint-71132d962002eb2894698309` (`libapparmor1`): “changehat AppArmor library”; checked against MUST rationale.

R3: Runtime introspection metadata is MUST under S2.2-1 and S2.2-2 because it enables language bindings to call the native API. It is not displayed document content. Official project documentation at https://gi.readthedocs.io/en/latest/ states: “Then language bindings can read this metadata and automatically provide bindings to call into the C library.” Ten manually checked package descriptions identify introspection or typelib data.

- `mint-46991dc3899466deda689a67` (`gir1.2-accountsservice-1.0`): “GObject introspection data for AccountService”; checked against MUST rationale.
- `mint-c86ec8818dc63110eed70a07` (`gir1.2-atk-1.0`): “ATK accessibility toolkit (GObject introspection)”; checked against MUST rationale.
- `mint-383bf53be2ec4cbb69bd2479` (`gir1.2-atspi-2.0`): “Assistive Technology Service Provider (GObject introspection)”; checked against MUST rationale.
- `mint-c215a52ef23efe90c5cefafd` (`gir1.2-ayatanaappindicator3-0.1`): “Typelib files for libayatana-appindicator3-1 (GTK-3+ version)”; checked against MUST rationale.
- `mint-d8db6c23e8d114b6ea4b15c6` (`gir1.2-camel-1.2`): “GObject introspection for the Camel library”; checked against MUST rationale.
- `mint-331c8df8e56c9265832b4ec8` (`gir1.2-caribou-1.0`): “GObject introspection for the Caribou library”; checked against MUST rationale.
- `mint-b70e8b5f8580baa331445b78` (`gir1.2-cinnamondesktop-3.0`): “Introspection data for CinnamonDesktop”; checked against MUST rationale.
- `mint-01a0e344c3a86cdd43accc9e` (`gir1.2-clutter-1.0`): “GObject introspection data for the Clutter 1.0 library”; checked against MUST rationale.
- `mint-b2533eab240462bfcf322e16` (`gir1.2-clutter-gst-3.0`): “GObject introspection data for Clutter GStreamer elements”; checked against MUST rationale.
- `mint-8e8c9b316e863ad0f1b3a461` (`gir1.2-cmenu-3.0`): “GObject introspection data for the Cinnamon menu library”; checked against MUST rationale.

R4: Font packages are HOLE under S2.2-2 and S2.2-4: removing glyphs and metrics can mean only losing graphical content, or losing the ability to render particular characters correctly. The text supplies no boundary between these readings. Ten manually checked packages supply glyphs and metrics, not font-management executables.

- `mint-235d4ec522642882f926eb27` (`fonts-dejavu-core`): “Vera font family derivate with additional characters”; checked against HOLE rationale.
- `mint-333828a5247abd0aa698d26b` (`fonts-dejavu-mono`): “Vera font family derivate with additional characters”; checked against HOLE rationale.
- `mint-2c4f8ff5a67ee625bef68c4e` (`fonts-droid-fallback`): “handheld device font with extensive style and language support (fallback)”; checked against HOLE rationale.
- `mint-1162f68e41f0d35b2f9c9343` (`fonts-liberation`): “fonts with the same metrics as Times, Arial and Courier”; checked against HOLE rationale.
- `mint-f6b90fa1b7acc162814857e2` (`fonts-mathjax`): “JavaScript display engine for LaTeX and MathML (fonts)”; checked against HOLE rationale.
- `mint-af6961bcf790f4f792437f97` (`fonts-noto-cjk`): “"No Tofu" font families with large Unicode coverage (CJK regular and bold)”; checked against HOLE rationale.
- `mint-854622d42bc8ca5d899db0ff` (`fonts-noto-color-emoji`): “color emoji font from Google”; checked against HOLE rationale.
- `mint-8ddfd74bd50c9296043d6b74` (`fonts-noto-core`): “"No Tofu" font families with large Unicode coverage (core)”; checked against HOLE rationale.
- `mint-daac7e63db042cc2f3b04b9a` (`fonts-noto-mono`): “"No Tofu" monospaced font family with large Unicode coverage”; checked against HOLE rationale.
- `mint-76c2c41ca55b1bec436fe365` (`fonts-opensymbol`): “OpenSymbol TrueType font”; checked against HOLE rationale.

R5: Pure text, image and descriptive-content packages are NOT under S2.2-4: removal loses the supplied content while leaving executable capabilities. This rule is not applied automatically to every data/common suffix. Ten manually checked entries below identify such content; system-routing configuration, processing schemas, code hidden in data packages and other exceptions were examined separately.

- `mint-463205593f6d946eda63ffd4` (`adwaita-icon-theme`): “default icon theme of GNOME”; checked against NOT rationale.
- `mint-183fe54bb88d761c24d4f814` (`app-install-data`): “Ubuntu applications (data files)”; checked against NOT rationale.
- `mint-b33afdd28c39888aab1502e8` (`aptdaemon-data`): “data files for clients”; checked against NOT rationale.
- `mint-a7968d3e1a82bd508b18e515` (`aptitude-common`): “architecture independent files for the aptitude package manager”; checked against NOT rationale.
- `mint-0aaf5fda87db3c90b7de32b7` (`binutils-common`): “Common files for the GNU assembler, linker and binary utilities”; checked against NOT rationale.
- `mint-b76380704db4b5b4af9e52c1` (`cinnamon-control-center-data`): “configuration applets for Cinnamon - data files”; checked against NOT rationale.
- `mint-f029447dfa5b81e83920cfc2` (`cinnamon-l10n`): “Translation files for the Cinnamon desktop”; checked against NOT rationale.
- `mint-e8d247fed81713d4e7067b06` (`circle-flags-svg`): “Circle flags in SVG format”; checked against NOT rationale.
- `mint-35798aaf81b02f78c722892e` (`distro-info-data`): “information about the distributions' releases (data files)”; checked against NOT rationale.
- `mint-c5e3f9597065613a57deaa42` (`dmz-cursor-theme`): “Style neutral, scalable cursor theme”; checked against NOT rationale.

## Individually assessed exceptions

The explicit per-index assignments in part-mint.1.finish.py record individual assessments, not a suffix-derived blanket rule. Their row reasons state the relevant removal consequence or missing boundary. The following distinctions were checked:

- Firmware packages change device behavior; system-update availability establishes the condition in S2.2-16.
- Shared hardware routing, keyboard configuration, desktop schemas and interprocess messaging extend across programs and therefore do not fit the one-program setting exemption.
- Dependency-only metapackages expose an unspecified removal boundary: remove just the dependency record, or the functionality selected through it. No external package-manager removal semantics were silently substituted for the text.
- Detached debugging symbols expose content versus symbolic-debugging-capability readings. The separate unstripped-binary debugging package explicitly supplies executable code and was classified MUST.
- Dictionaries, processing schemas, templates, color profiles and keyboard maps received individual HOLE explanations; knowing their role does not resolve the text’s content/capability boundary.
- Shared-library configuration exposes a separate one-program versus multiple-caller ambiguity.
- Data/common names are insufficient: the primary file lists establish executable modules in cinnamon-common and hplip-data, service activation in evolution-data-server-common, and only documentation in gcc base packages.
- No UNKNOWN was needed after consulting the public metadata and file lists.

## Package-specific documentary evidence

The following quotations are package description titles, keyed to exact inventory ids. Additional full descriptions and file lists were consulted for ambiguous titles; selected file paths follow below. The descriptions establish roles, not normative decisions. Current archive descriptions are used for stable package purpose; an installed version need not equal the archive revision. Mint-origin descriptions replace conflicting distribution descriptions, notably the browser package.

- `mint-2fefc3b8c16ec0f56484edbe` (`7zip`): “7-Zip file archiver with a high compression ratio” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-bd39a4b50da417df00c2ed50` (`aardvark-dns`): “Container-focused DNS server” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-f797f068d0ef2976862c010a` (`accountsservice`): “query and manipulate user account information” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6ea8e65211f3781437f7f7d4` (`acl`): “access control list - utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-87ba567c3238acd25165e3c4` (`adduser`): “add and remove users and groups” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-463205593f6d946eda63ffd4` (`adwaita-icon-theme`): “default icon theme of GNOME” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-92428f010df383fc106c30ec` (`alsa-base`): “ALSA driver configuration files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-fab95c6164242c351cacd8ab` (`alsa-topology-conf`): “ALSA topology configuration files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-03b033faa5ae44b97e1c4451` (`alsa-ucm-conf`): “ALSA Use Case Manager configuration files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-830aa35501eb790fcfdd3ec6` (`alsa-utils`): “Utilities for configuring and using ALSA” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ea1b58590e4983ba0b5a4c81` (`amd64-microcode`): “Processor microcode firmware for AMD CPUs” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-79ef6e77e3a19e49879c881d` (`anacron`): “cron-like program that doesn't go by time” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cd7b0939c55f505e0c2dd134` (`apg`): “Automated Password Generator - Standalone version” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-183fe54bb88d761c24d4f814` (`app-install-data`): “Ubuntu applications (data files)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-8efdad51d1629955aed654f7` (`apparmor`): “user-space parser utility for AppArmor” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-00c01f0d858a3a050187e679` (`appstream`): “Software component metadata management” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-fc1849859d4f829a7eebd8c8` (`apt`): “commandline package manager” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-25b030329863626725c526c4` (`apt-utils`): “package management related utility programs” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ab04fffce23e3f588ec39855` (`aptdaemon`): “transaction based package management service” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b33afdd28c39888aab1502e8` (`aptdaemon-data`): “data files for clients” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2962d7796e675f8f94209532` (`aptitude`): “terminal-based package manager” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-a7968d3e1a82bd508b18e515` (`aptitude-common`): “architecture independent files for the aptitude package manager” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-a658b9f516a866c13e30783a` (`aptkit`): “transaction based package management service” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz
- `mint-f7571bb4b98bfde89674e92d` (`aspell`): “GNU Aspell spell-checker” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3201e0d0d24b245bd86db97d` (`aspell-en`): “English dictionary for GNU Aspell” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-327a4160e21ec1bdca3d633c` (`at-spi2-common`): “Assistive Technology Service Provider Interface (common files)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-de404a66a515223d1924d09b` (`at-spi2-core`): “Assistive Technology Service Provider Interface (D-Bus core)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-75ac4edf5ec65be995673f87` (`attr`): “utilities for manipulating filesystem extended attributes” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d19563f2278c5b0ec1499c82` (`avahi-autoipd`): “Avahi IPv4LL network address configuration daemon” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-ed30dbf2aa796692abab474b` (`avahi-daemon`): “Avahi mDNS/DNS-SD daemon” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-5928c6b340781abfcc2aec26` (`avahi-utils`): “Avahi browsing, publishing and discovery utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-58aef8a4df8c49ac764caa99` (`baobab`): “GNOME disk usage analyzer” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8221d0b24ac32d06ce1123ac` (`base-files`): “Debian base system miscellaneous files” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-74d8182c1dfac517321485b6` (`base-passwd`): “Debian base system master password and group files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-0b4c0322dde5f9a4c4c6307c` (`bash`): “GNU Bourne Again SHell” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7c7aff1f1cf775dde31d9ded` (`bash-completion`): “programmable completion for the bash shell” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4658e56e468c4e23e607b2f3` (`bc`): “GNU bc arbitrary precision calculator language” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-86a6ee80461a1149ae0772a2` (`bind9-dnsutils`): “Clients provided with BIND 9” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-104122af3bbbd703d3c629c6` (`bind9-host`): “DNS Lookup Utility” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-51c3a0b00f9cf87aed70a186` (`bind9-libs`): “Shared Libraries used by BIND 9” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9dc97fb0b7802333fc15cca2` (`binutils`): “GNU assembler, linker and binary utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-0aaf5fda87db3c90b7de32b7` (`binutils-common`): “Common files for the GNU assembler, linker and binary utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a0c1503e78a6720e5314e97c` (`binutils-x86-64-linux-gnu`): “GNU binary utilities, for x86-64-linux-gnu target” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f5cca40488112690f7538c00` (`blueman`): “Graphical bluetooth manager” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-abfe052ec72b3e4d59ff2dd7` (`bluetooth`): “Bluetooth support (metapackage)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-b53934c81b5f55bbc7143798` (`bluez`): “Bluetooth tools and daemons” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ccf5cd036761c5877a359401` (`bluez-cups`): “Bluetooth printer driver for CUPS” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-90f60d8af200a9d3f04f9559` (`bluez-obexd`): “bluez obex daemon” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f75b5f104a80ee8637ad3175` (`bolt`): “system daemon to manage thunderbolt 3 devices” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-541845641e039a9006fb173c` (`brasero-common`): “Common files for the Brasero CD burning application and library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-5ffb8680deea7f620f5a8750` (`brltty`): “Access software for a blind person using a braille display” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-31ae7722c16aaaa739fef225` (`bsdextrautils`): “extra utilities from 4.4BSD-Lite” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-707115569cc9db1dee20f946` (`bsdutils`): “basic utilities from 4.4BSD-Lite” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b25c8579928f9c881d3226e0` (`btrfs-progs`): “Checksumming Copy on Write Filesystem utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-dffe0d053cc1722cf5c5c86d` (`bubblewrap`): “utility for unprivileged chroot and namespace manipulation” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-267e53cbb404e5549ed2f412` (`build-essential`): “Informational list of build-essential packages” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-79efb7f744f99783bddc0c3c` (`buildah`): “CLI tool to facilitate building OCI images” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-eba8e78e63b1fdb925fe56f9` (`bulky`): “Bulk Renamer” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz
- `mint-66f7e7fa38548ef7ae408ff7` (`busybox-initramfs`): “Standalone shell setup for initramfs” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a28a0cd896f35288bf5ed357` (`busybox-static`): “Standalone rescue shell with tons of builtin utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a59bdfdd3e0f29abe44e9972` (`bzip2`): “high-quality block-sorting file compressor - utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1dc109a34e4f261672fd46a8` (`ca-certificates`): “Common CA certificates” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6713630719ac5ab25a1c841c` (`captain`): “Collection of APT tools” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz
- `mint-469ad5b9d60d1435429befd8` (`casper`): “Run a "live" preinstalled system from read-only media” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1f08dcc499fc0f8519f92e39` (`catatonit`): “init process for containers” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-65fde47cef6f821c3abbf569` (`catdoc`): “text extractor for MS-Office files” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-c2501a47eb5f1f4510c69322` (`celluloid`): “simple GTK+ frontend for mpv” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-b538029289c257f1fb275e1d` (`cifs-utils`): “Common Internet File System utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-aa25a70e5aba48a2f8b07404` (`cinnamon`): “Modern Linux desktop” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-08a8ab049ff24665c1b8e05b` (`cinnamon-common`): “Cinnamon desktop (Common data files)” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-b3e8120298329b23b7f67b2f` (`cinnamon-control-center`): “utilities to configure the Cinnamon desktop” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-b76380704db4b5b4af9e52c1` (`cinnamon-control-center-data`): “configuration applets for Cinnamon - data files” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-ff58418b0703f7cafb0e40ac` (`cinnamon-control-center-dbg`): “utilities to configure the Cinnamon desktop - debug symbols” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-6bce92151e226b7ac96fe618` (`cinnamon-dbg`): “Debugging symbols for the Cinnamon desktop” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-2e97d4a2f5457c35f02bb14b` (`cinnamon-desktop-data`): “Common files for Cinnamon desktop apps” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-f029447dfa5b81e83920cfc2` (`cinnamon-l10n`): “Translation files for the Cinnamon desktop” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-8ebfa20ac94cc62b737bec51` (`cinnamon-screensaver`): “Cinnamon screen saver and locker” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-2ee36b2ebfaa3b2855ba573d` (`cinnamon-session`): “Cinnamon Session Manager - Minimal runtime” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-8dbbc24f24270afd1dc329fe` (`cinnamon-session-common`): “Cinnamon Session Manager - common files” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-9a03bc8a14e517fe8244ada7` (`cinnamon-settings-daemon`): “daemon handling the Cinnamon session settings” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-e8d247fed81713d4e7067b06` (`circle-flags-svg`): “Circle flags in SVG format” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz
- `mint-41d9842314e159e8de75a958` (`cjs`): “Mozilla-based javascript bindings for the Cinnamon platform (cli tool)” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-5d5e6b701e89300c1432d2d8` (`colord`): “system service to manage device colour profiles -- system daemon” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ce92df556ddfea81b035e5f6` (`colord-data`): “system service to manage device colour profiles -- data files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9206cf60155118abbad833d6` (`command-not-found`): “Suggest installation of packages in interactive bash sessions” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-919220f84897eef7dfa90f2a` (`conmon`): “OCI container runtime monitor” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-54c554cf9dbf17285ed80c7f` (`console-setup`): “console font and keymap setup program” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b26420cf3111572dc2261203` (`console-setup-linux`): “Linux specific part of console-setup” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-237e7b89d823183a280136eb` (`containernetworking-plugins`): “standard networking plugins - binaries” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-1ffc5a279bde8b78c119d186` (`coreutils`): “GNU core utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b198828af0c51a48e53d8c75` (`cpdb-backend-cups`): “Common Print Dialog Backends - CUPS/IPP Backend” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-b58263847f1e720551582b32` (`cpio`): “GNU cpio -- a program to manage archives of files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-0f6201505f4a66083482ec1f` (`cpp`): “GNU C preprocessor (cpp)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-81e7b15e35416b42196e086a` (`cpp-13`): “GNU C preprocessor” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d4b09144dfa32d9b0c6e9ca3` (`cpp-13-x86-64-linux-gnu`): “GNU C preprocessor for x86_64-linux-gnu” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-623892068141aebfb288e80e` (`cpp-x86-64-linux-gnu`): “GNU C preprocessor (cpp) for the amd64 architecture” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c8c83d574dd3641905059587` (`cracklib-runtime`): “runtime support for password checker library cracklib2” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-51a5d1d9a8e19d3007819733` (`cron`): “process scheduling daemon” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-01716d4dba025cae1f39bfe5` (`cron-daemon-common`): “process scheduling daemon's configuration files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9e358a6c5110de88bc68bfb2` (`crun`): “lightweight OCI runtime for running containers” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-c54b8dff78ef60fbe619b7d6` (`cryptsetup`): “disk encryption support - startup scripts” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-5bd219f51f8b16191ae4251d` (`cryptsetup-bin`): “disk encryption support - command line tools” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3addbac73a09d48929f7cf6a` (`cryptsetup-initramfs`): “disk encryption support - initramfs integration” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6aa9efe951df245c72547e24` (`cups`): “Common UNIX Printing System(tm) - PPD/driver support, web interface” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9aa267da1dea488cb6e2824d` (`cups-browsed`): “OpenPrinting cups-browsed” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8d9bb22ac6c7df6fcc923cfc` (`cups-bsd`): “Common UNIX Printing System(tm) - BSD commands” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-13bfa582982e7213e44f945f` (`cups-client`): “Common UNIX Printing System(tm) - client programs (SysV)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-5411c6ec3ac75c4b2f97d742` (`cups-common`): “Common UNIX Printing System(tm) - common files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ad216d55d5899cf9f9b5e969` (`cups-core-drivers`): “Common UNIX Printing System(tm) - driverless printing” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-85657925d49e093de38f7471` (`cups-daemon`): “Common UNIX Printing System(tm) - daemon” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-08455455af303b7ab2d26008` (`cups-filters`): “OpenPrinting CUPS Filters - Main Package” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1e58b6801f30b5f30a85f8de` (`cups-filters-core-drivers`): “OpenPrinting CUPS Filters - Driverless printing” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-29c59085aa5bde1c65cf8eec` (`cups-ipp-utils`): “Common UNIX Printing System(tm) - IPP developer/admin utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-66e0f4e0093159ed824105c7` (`cups-pk-helper`): “PolicyKit helper to configure cups with fine-grained privileges” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-880cee7d47e32321b429c613` (`cups-ppdc`): “Common UNIX Printing System(tm) - PPD manipulation utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e2442700a14fd214191b7801` (`cups-server-common`): “Common UNIX Printing System(tm) - server common files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1c5bbd4d7ea46c38c7e90a14` (`curl`): “command line tool for transferring data with URL syntax” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-5f79ff45e489886af89ff59c` (`dash`): “POSIX-compliant shell” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-edd4f2cd522101e326ea4974` (`dbus`): “simple interprocess messaging system (system message bus)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3fe1596e4b4912125cff7cc4` (`dbus-bin`): “simple interprocess messaging system (command line utilities)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-033dd40fd6065001ceac3d1d` (`dbus-daemon`): “simple interprocess messaging system (reference message bus)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-047568654150fb9d73f4db26` (`dbus-session-bus-common`): “simple interprocess messaging system (session bus configuration)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-41c4c8398834984717f15241` (`dbus-system-bus-common`): “simple interprocess messaging system (system bus configuration)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-797856d6b6be758fb4c16eae` (`dbus-user-session`): “simple interprocess messaging system (systemd --user integration)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6fbd2445209b7db91868bf7f` (`dbus-x11`): “simple interprocess messaging system (X11 deps)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e505c154eb14b1ee0f22ba86` (`dc`): “GNU dc arbitrary precision reverse-polish calculator” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-673be87bb67110cca26bd09e` (`dconf-cli`): “simple configuration storage system - utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-eb3052409c0b3aac620730f4` (`dconf-gsettings-backend`): “simple configuration storage system - GSettings back-end” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-671a78898715e3735af187ee` (`dconf-service`): “simple configuration storage system - D-Bus service” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-5873622f6ff42103fee36a41` (`dcraw`): “decode raw digital camera images” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-49404ecf878ec00473e26b1b` (`dctrl-tools`): “Command-line tools to process Debian package information” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-fe6d2ae83c2de9c01616ab79` (`debconf`): “Debian configuration management system” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6adef65ce0f4a6ce74a24418` (`debconf-i18n`): “full internationalization support for debconf” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4adddeb8c42e96cba3651c3a` (`debianutils`): “Miscellaneous utilities specific to Debian” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ecb560485187bdfd9c6927a0` (`desktop-file-utils`): “Utilities for .desktop files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-fcbdcbec3a07aad3358e90fe` (`dhcpcd-base`): “DHCPv4 and DHCPv6 dual-stack client (binaries and exit hooks)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c6a56107c07a1761931278fa` (`dialog`): “Displays user-friendly dialog boxes from shell scripts” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-bd73eff51c43aa5bace713f5` (`dictionaries-common`): “spelling dictionaries - common utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ab950f8c94156503e9a29da2` (`diffutils`): “File comparison utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3a868ac8fc439a5b0c66b6a1` (`dirmngr`): “GNU privacy guard - network certificate management service” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-130e37eb3402311fcac93f84` (`distro-info`): “provides information about the distributions' releases” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-35798aaf81b02f78c722892e` (`distro-info-data`): “information about the distributions' releases (data files)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6f50715299cbf6e9220c1b0a` (`dkms`): “Dynamic Kernel Module System (DKMS)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-919dfda78a1234b23b15b18a` (`dmeventd`): “Linux Kernel Device Mapper event daemon” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-93db2fb21b083b8ad5fe2411` (`dmidecode`): “SMBIOS/DMI table decoder” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6f4b8d04b19222d344e5f044` (`dmraid`): “Device-Mapper Software RAID support tool” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-68ab1e3b09a50cc59c5749c2` (`dmsetup`): “Linux Kernel Device Mapper userspace library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c5e3f9597065613a57deaa42` (`dmz-cursor-theme`): “Style neutral, scalable cursor theme” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b15c1998a84609fb2c469839` (`dns-root-data`): “DNS root data including root zone and DNSSEC key” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-94d205778350de3289e8f00f` (`dnsmasq-base`): “Small caching DNS proxy and DHCP/TFTP server - executable” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c3b484127e106ad7b41be3a8` (`docbook-xml`): “standard XML documentation system for software and systems” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cf36c6f906e80cde31094d6a` (`dosfstools`): “utilities for making and checking MS-DOS FAT filesystems” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-fc6f4befc9b8c5089c618cc0` (`dpkg`): “Debian package management system” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-590bbee4efaec69b1755d170` (`dpkg-dev`): “Debian package development tools” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7e44dfa9cfe28e946c898113` (`dpkg-repack`): “Debian package archiving tool” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-12e784286bc19596dd238be0` (`dracut-install`): “dracut is an event driven initramfs infrastructure (dracut-install)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-27551f795723209ef580db34` (`drawing`): “simple drawing application for the GNOME desktop” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-0a5812a6d914bcb9f44e7868` (`e2fsprogs`): “ext2/ext3/ext4 file system utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-23f7a3424c752b9645ec5459` (`ecryptfs-utils`): “ecryptfs cryptographic filesystem (utilities)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-e4822a2d8ca23c72a28451a0` (`ed`): “classic UNIX line editor” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c60e0ed2b242924853c4d7a4` (`efibootmgr`): “Interact with the EFI Boot Manager” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-823a481d6ce08ada5c278725` (`eject`): “ejects CDs and operates CD-Changers under Linux” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f9adda0c62a1463ab282fa61` (`emacsen-common`): “Common facilities for all emacsen” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c2c7c38f0674f1c6bd273a64` (`enchant-2`): “Wrapper for various spell checker engines (binary programs)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-64b6282dd6f7dfb6c0fdf80a` (`espeak-ng-data`): “Multi-lingual software speech synthesizer: speech data files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9777cdc51ccdb8e55b338a65` (`ethtool`): “display or change Ethernet device settings” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-0014d252400d48a574d259a7` (`evolution-data-server`): “evolution database backend server” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8d75c5911789669cba52a7e3` (`evolution-data-server-common`): “architecture independent files for Evolution Data Server” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e083c62b35b37ba2d1e40c34` (`exfat-fuse`): “read and write exFAT driver for FUSE” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-1beff73051db6e96e4362c0d` (`exfatprogs`): “exFAT file system utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-c1321e6463ecaf9983e00cc4` (`exif`): “command-line utility to show EXIF information in JPEG files” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-fd1a6a0468a055f1c8181f06` (`fakeroot`): “tool for simulating superuser privileges” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e3fb48c626ddf4a5d4b7b156` (`fdisk`): “collection of partitioning utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6046f51a549c13bdef983664` (`ffmpegthumbnailer`): “fast and lightweight video thumbnailer” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-2c9f7d24199e2c96d32bc234` (`file`): “Recognize the type of data in a file using "magic" numbers” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-477b7e57e7a5ca7ef02988a0` (`file-roller`): “archive manager for GNOME” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-9b4094cfd4f081023163e62b` (`finalrd`): “final runtime directory for shutdown” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6a6e12df08f3bc316528f202` (`findutils`): “utilities for finding files--find, xargs” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-85f4b22ff6d8b349606dfd7b` (`fingwit`): “Fingerprint Configuration Tool” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-fdecb77a3635f99c8dfb361d` (`firefox`): “The Firefox web browser” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-f0ea7dcf8aaf9dd02a599025` (`firefox-locale-en`): “English language packs for Firefox” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-71d8eb353373c078ebfbf3ca` (`firmware-sof-signed`): “Intel SOF firmware - signed” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a75a78932e46c69311ab6bf6` (`flatpak`): “Application deployment framework for desktop apps” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-def665262327d61aa497d55a` (`folder-color-switcher`): “Change a folder color” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz
- `mint-ec6cc07d40792a090a99203f` (`fontconfig`): “generic font configuration library - support binaries” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e4b9946a71ee5e493dca3419` (`fontconfig-config`): “generic font configuration library - configuration” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-235d4ec522642882f926eb27` (`fonts-dejavu-core`): “Vera font family derivate with additional characters” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-333828a5247abd0aa698d26b` (`fonts-dejavu-mono`): “Vera font family derivate with additional characters” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2c4f8ff5a67ee625bef68c4e` (`fonts-droid-fallback`): “handheld device font with extensive style and language support (fallback)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1162f68e41f0d35b2f9c9343` (`fonts-liberation`): “fonts with the same metrics as Times, Arial and Courier” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f6b90fa1b7acc162814857e2` (`fonts-mathjax`): “JavaScript display engine for LaTeX and MathML (fonts)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-af6961bcf790f4f792437f97` (`fonts-noto-cjk`): “"No Tofu" font families with large Unicode coverage (CJK regular and bold)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-854622d42bc8ca5d899db0ff` (`fonts-noto-color-emoji`): “color emoji font from Google” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8ddfd74bd50c9296043d6b74` (`fonts-noto-core`): “"No Tofu" font families with large Unicode coverage (core)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-daac7e63db042cc2f3b04b9a` (`fonts-noto-mono`): “"No Tofu" monospaced font family with large Unicode coverage” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-76c2c41ca55b1bec436fe365` (`fonts-opensymbol`): “OpenSymbol TrueType font” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-515816f17b3f22b0d4757ac2` (`fonts-ubuntu`): “sans-serif font set from Ubuntu” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6d32375033464cb6d41228c0` (`fonts-urw-base35`): “font set metric-compatible with the 35 PostScript Level 2 Base Fonts” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-dbfdf274539591521116d6fc` (`foomatic-db-compressed-ppds`): “OpenPrinting printer support - Compressed PPDs derived from the database” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4188ee1d485ce089f81a67c6` (`fprintd`): “D-Bus daemon for fingerprint reader access” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f660bd938800a476890205b7` (`friendly-recovery`): “Make recovery boot mode more user-friendly” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-283909d2e9d052078ee95400` (`ftp`): “dummy transitional package for tnftp” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8fbbb2a5787eb593b7e6b7cc` (`fuse-overlayfs`): “implementation of overlay+shiftfs in FUSE for rootless containers” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-ac836d426c60309e606fcdfd` (`fuse3`): “Filesystem in Userspace (3.x version)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-611955b90707846f7c8a7369` (`fwupd`): “Firmware update daemon” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-edbb471da6f6c3a500e656d4` (`fwupd-signed`): “Linux Firmware Updater EFI signed binary” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-266d7bc541381992b978ee95` (`g++`): “GNU C++ compiler” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-47e572fa131b5a7f189dadcf` (`g++-13`): “GNU C++ compiler” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3a506ef4bfa3353af3eaf7bb` (`g++-13-x86-64-linux-gnu`): “GNU C++ compiler for x86_64-linux-gnu architecture” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-466cafeb2dc117b088fd1d96` (`g++-x86-64-linux-gnu`): “GNU C++ compiler for the amd64 architecture” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-83a50943f5d979feba49b327` (`gamemode`): “Optimise Linux system performance on demand” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-50589b5b4e59f82bb2adccf9` (`gamemode-daemon`): “Optimise Linux system performance on demand (daemon)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a69a8af3259a95cbcd14d1cd` (`gcc`): “GNU C compiler” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7a6d1e637a285717a49f4628` (`gcc-13`): “GNU C compiler” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d9fa506d50754c763b7ba8f0` (`gcc-13-base`): “GCC, the GNU Compiler Collection (base package)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1e180478b1eadcfca9f4ade6` (`gcc-13-x86-64-linux-gnu`): “GNU C compiler for the x86_64-linux-gnu architecture” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2eff8ca7533a01281d1f6c11` (`gcc-14-base`): “GCC, the GNU Compiler Collection (base package)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-16cba5d08f45171ba26fbc86` (`gcc-x86-64-linux-gnu`): “GNU C compiler for the amd64 architecture” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-46fe291af9c8b4133199847b` (`gcr`): “GNOME crypto services (daemon and tools)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-dd0d38e526377fd955b33730` (`gcr4`): “GNOME crypto services (daemon and tools)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2f93077d5570b6786b03cce5` (`gdb`): “GNU Debugger” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4ae6e1102437204c6994b73d` (`gdisk`): “GPT fdisk text-mode partitioning tool” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-0e23fe82a69f3180465cb2da` (`genisoimage`): “Creates ISO-9660 CD-ROM filesystem images” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-69e3af0fec199f18c087b88f` (`geoclue-2.0`): “geoinformation service” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ce912c6d04cb481509f2e631` (`geocode-glib-common`): “icons for the geocode-glib library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ad84f7151f824a2826d6faed` (`geoip-database`): “IP lookup command line tools that use the GeoIP library (country database)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-f29a911d524a708ed24e4c88` (`gettext`): “GNU Internationalization utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-bbb1b4440b9762928ea56cc7` (`gettext-base`): “GNU Internationalization utilities for the base system” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-eb80057319d9f209cdf4b8c8` (`ghostscript`): “interpreter for the PostScript language and for PDF” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-46991dc3899466deda689a67` (`gir1.2-accountsservice-1.0`): “GObject introspection data for AccountService” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c86ec8818dc63110eed70a07` (`gir1.2-atk-1.0`): “ATK accessibility toolkit (GObject introspection)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-383bf53be2ec4cbb69bd2479` (`gir1.2-atspi-2.0`): “Assistive Technology Service Provider (GObject introspection)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c215a52ef23efe90c5cefafd` (`gir1.2-ayatanaappindicator3-0.1`): “Typelib files for libayatana-appindicator3-1 (GTK-3+ version)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d8db6c23e8d114b6ea4b15c6` (`gir1.2-camel-1.2`): “GObject introspection for the Camel library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-331c8df8e56c9265832b4ec8` (`gir1.2-caribou-1.0`): “GObject introspection for the Caribou library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-b70e8b5f8580baa331445b78` (`gir1.2-cinnamondesktop-3.0`): “Introspection data for CinnamonDesktop” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-01a0e344c3a86cdd43accc9e` (`gir1.2-clutter-1.0`): “GObject introspection data for the Clutter 1.0 library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-b2533eab240462bfcf322e16` (`gir1.2-clutter-gst-3.0`): “GObject introspection data for Clutter GStreamer elements” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-8e8c9b316e863ad0f1b3a461` (`gir1.2-cmenu-3.0`): “GObject introspection data for the Cinnamon menu library” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-a76d5805385927e839e23f39` (`gir1.2-cogl-1.0`): “GObject introspection data for the Cogl 1.0 library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-fbda5f9498d7ccaa766c5e12` (`gir1.2-coglpango-1.0`): “GObject introspection data for the CoglPango 1.0 library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-d0637ddfdcd4a772adde3005` (`gir1.2-cvc-1.0`): “Introspection data for Cinnamon pulseaudio abstraction” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-3b88a208c60f1e9fbae6d05f` (`gir1.2-dbusmenu-glib-0.4`): “typelib file for libdbusmenu-glib4” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-5589559941bf330f1ea5600f` (`gir1.2-dee-1.0`): “GObject introspection data for the Dee library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-82cf7afa6839da2780d967e6` (`gir1.2-ecal-2.0`): “GObject introspection for the ECal library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-662fd464551cce5f20c686cc` (`gir1.2-edataserver-1.2`): “GObject introspection for the EDataServer library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d87bc089fc28bad55655aee4` (`gir1.2-flatpak-1.0`): “Application deployment framework for desktop apps (introspection)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-b92c7475329fa4a19130e933` (`gir1.2-freedesktop`): “Introspection data for some FreeDesktop components” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1e40332cd50551779e293804` (`gir1.2-gck-1`): “GObject introspection data for the GCK library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-68ed3eccd69d540ff55af63f` (`gir1.2-gcr-3`): “GObject introspection data for the GCR library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cb1c8ae2c7b6dd785307d6b2` (`gir1.2-gdesktopenums-3.0`): “GObject introspection for GSettings desktop-wide schemas” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-27e536121a9c9fcd27ccf802` (`gir1.2-gdkpixbuf-2.0`): “GDK Pixbuf library - GObject-Introspection” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-be8771b29afaa8ba41b35a3a` (`gir1.2-girepository-2.0`): “Introspection data for GIRepository library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f13bb4176f57825366128e87` (`gir1.2-gkbd-3.0`): “GObject introspection data for the GnomeKbd library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ec79599c10e72b1af96e465f` (`gir1.2-glib-2.0`): “Introspection data for GLib, GObject, Gio and GModule” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-49c309b6cd64fd282800f257` (`gir1.2-gnomedesktop-3.0`): “Introspection data for GnomeDesktop (GTK 3)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7d92bbc354680e91fa2233fa` (`gir1.2-graphene-1.0`): “library of graphic data types (introspection files)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-fba7430554d94d62fb18a668` (`gir1.2-gsound-1.0`): “small library for playing system sounds (gir bindings)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e40f86698448bff1be0aebec` (`gir1.2-gspell-1`): “spell-checking library for GTK+ applications - GObject introspection” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ddba1589486cbcace9734220` (`gir1.2-gst-plugins-base-1.0`): “GObject introspection data for the GStreamer Plugins Base library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-60f4ed2afded96dd89d248b1` (`gir1.2-gstreamer-1.0`): “GObject introspection data for the GStreamer library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-99b8451933209593749c10b4` (`gir1.2-gtk-3.0`): “GTK graphical user interface library -- gir bindings” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-61cf46076e7e829b56e50cea` (`gir1.2-gtkclutter-1.0`): “GObject introspection data for the GTK+ Clutter library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-c8935a7df00f9ecd2f3807e0` (`gir1.2-gtksource-3.0`): “gir files for the GTK+ syntax highlighting widget” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-8100d28cdb8a11adf1ddaeff` (`gir1.2-gtksource-4`): “gir files for the GTK+ syntax highlighting widget” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-16829ea269a2c04e57fee085` (`gir1.2-gtop-2.0`): “gtop system monitoring library (gir bindings)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c8381a58359b8370f42edee6` (`gir1.2-gudev-1.0`): “libgudev-1.0 introspection data” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4e5b7714216ce80aca95d489` (`gir1.2-handy-1`): “GObject introspection files for libhandy” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-038b4193155dc3c5ea298c71` (`gir1.2-harfbuzz-0.0`): “OpenType text shaping engine (GObject introspection data)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1db35c7f451c9a146793daf4` (`gir1.2-ibus-1.0`): “Intelligent Input Bus - introspection data” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9667bb0c93739b60ba28765d` (`gir1.2-ical-3.0`): “iCalendar library implementation in C (GObject Introspection)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-52b157930a62c78596788ec1` (`gir1.2-javascriptcoregtk-4.1`): “JavaScript engine library from WebKitGTK - GObject introspection data” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-0de16027885a385be863a89c` (`gir1.2-json-1.0`): “GLib JSON manipulation library (introspection data)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-37575fc5ee206419acdf88a0` (`gir1.2-keybinder-3.0`): “registers global key bindings for applications - Gtk+3 - typelib” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-a31bba13563f9d1731b3d814` (`gir1.2-matedesktop-2.0`): “GObject introspection data for the libmate-desktop library” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-c6444601488ba584e3cbc030` (`gir1.2-matemenu-2.0`): “GObject introspection data for the MATE menu specification” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-08bc4c3b5fabbf48d8ab21a8` (`gir1.2-matepanelapplet-4.0`): “GObject introspection data for MATE panel” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-8259e0403dc65891be3c2aac` (`gir1.2-meta-muffin-0.0`): “GObject introspection data for Muffin” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-bc25ed802c8187943f9c8b13` (`gir1.2-nemo-3.0`): “libraries for nemo components - gir bindings” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-12f4b10e579860c608a27e59` (`gir1.2-nm-1.0`): “GObject introspection data for the libnm library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e5bd6c3725003fbada11f289` (`gir1.2-nma-1.0`): “GObject introspection data for libnma” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-3b1bdbfc5e75ed274fc0af28` (`gir1.2-notify-0.7`): “sends desktop notifications to a notification daemon (Introspection files)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-eb9ed4eaae71e384b847fc1e` (`gir1.2-packagekitglib-1.0`): “GObject introspection data for the PackageKit GLib library” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-4345c50f44fd67e655a47ea7` (`gir1.2-pango-1.0`): “Layout and rendering of internationalized text - gir bindings” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-688207f3f9ba1fa2b675793a` (`gir1.2-peas-1.0`): “Application plugin library (introspection files)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a164f0148a5d75888a568d64` (`gir1.2-polkit-1.0`): “GObject introspection data for polkit” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8e9289d5d16361e73a14a8ea` (`gir1.2-rb-3.0`): “GObject introspection data for the rhythmbox music player” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-55f4638e749c897a93dbe436` (`gir1.2-secret-1`): “Secret store (GObject-Introspection)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3b60abb072e8489221d50f7e` (`gir1.2-soup-2.4`): “GObject introspection data for the libsoup HTTP library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b78c6c5b531491389469c38b` (`gir1.2-soup-3.0`): “GObject introspection data for the libsoup HTTP library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-702ca478a3ea6c6112a73129` (`gir1.2-timezonemap-1.0`): “typelib interface for libtimezonemap” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b6cdc6211a58c39b14ccab25` (`gir1.2-udisks-2.0`): “GObject based library to access udisks2 - introspection data” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8c87eb6503573fb7d5ee1277` (`gir1.2-upowerglib-1.0`): “GObject introspection data for upower” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-07602302e06e773845c5a94f` (`gir1.2-vte-2.91`): “GObject introspection data for the VTE library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a2add8db0e28a2d396cd9fda` (`gir1.2-webkit2-4.1`): “Web content engine library for GTK - GObject introspection data” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cf1821301c35121670b987b3` (`gir1.2-wnck-3.0`): “GObject introspection data for the WNCK library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-77cba8556e54053fbcfc873b` (`gir1.2-xapp-1.0`): “Introspection data for XApp” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-b58ee9991c8a18a6ffe59576` (`gir1.2-xkl-1.0`): “X Keyboard Extension high-level API - introspection data” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e639e4b4b503240d6acb6975` (`gir1.2-xmlb-2.0`): “GObject introspection data for libxmlb” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-07c71d3d39850b0868ef14da` (`gir1.2-xreader`): “GObject introspection data for Xreader” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-77314fa9f88941a3c425975b` (`gir1.2-xviewer-3.0`): “GObject introspection data for Xviewer” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-44d4702b54d4b8bccbb4a85e` (`gkbd-capplet`): “GNOME control center tools for libgnomekbd” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-388cc2c9956f9d415771603a` (`glib-networking`): “network-related giomodules for GLib” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-539b39c1a4cfb5978629626c` (`glib-networking-common`): “network-related giomodules for GLib - data files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-dc7f3557d7035ff6400c0841` (`glib-networking-services`): “network-related giomodules for GLib - D-Bus services” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a6f85bbf6c13e15ddbdfef31` (`gnome-accessibility-themes`): “High Contrast GTK 2 theme and icons” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e9bbcfd0a6dfcfccdd470bca` (`gnome-calculator`): “GNOME desktop calculator” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-433a750626380c6835c4a725` (`gnome-calendar`): “Calendar application for GNOME” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-33a8d744e6723f38bd466fd1` (`gnome-desktop3-data`): “Common files for GNOME desktop apps” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e41555ea552768c6fc02dbdf` (`gnome-disk-utility`): “manage and configure disk drives and media” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a07ade575db890711c9da16d` (`gnome-font-viewer`): “font viewer for GNOME” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-72c159f7417d186ee8e4541f` (`gnome-keyring`): “GNOME keyring services (daemon and tools)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d65084f3deb87526297616ba` (`gnome-keyring-pkcs11`): “GNOME keyring module for the PKCS#11 module loading library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b220cf67b9d177eddeb22f61` (`gnome-menus`): “GNOME implementation of the freedesktop menu specification” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-59de98322b0121e73684d67f` (`gnome-online-accounts`): “service to manage online accounts for the GNOME desktop” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-99df303f656b63e8f7f01fc7` (`gnome-online-accounts-gtk`): “GUI Utility for logging into online accounts for the” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-d15c83b9ee595fce52b01924` (`gnome-power-manager`): “power management tool for the GNOME desktop” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-42569a594af282404ce0a68e` (`gnome-screenshot`): “screenshot application for GNOME” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-a8122077f24e478187f53673` (`gnome-session-canberra`): “GNOME session log in and log out sound events” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8bc59d6313222356de0ed3c2` (`gnome-settings-daemon-common`): “daemon handling the GNOME session settings - common files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-40cb0cf9aa5bd40c3d4cb5a2` (`gnome-system-monitor`): “Process viewer and system resource monitor for GNOME” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-bd64297f6666227de0104b10` (`gnome-terminal`): “GNOME terminal emulator application” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-707cb6be107ec462ef11c223` (`gnome-terminal-data`): “Data files for the GNOME terminal emulator” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-77fa30d9a86e8ce9e3c9771d` (`gnome-themes-extra`): “Adwaita GTK 2 theme — engine” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-be231c5c769a75aa0fb3b726` (`gnome-themes-extra-data`): “Adwaita GTK 2 theme and Adwaita-dark GTK 3 theme — common files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-531e5f4850c6f53d92fd4607` (`gnupg`): “GNU privacy guard - a free PGP replacement” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-5000f6f88f8b8d4ec28c86a8` (`gnupg-utils`): “GNU privacy guard - utility programs” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-48953385bb2e313693fb3ed4` (`golang-github-containers-common`): “Common files for github.com/containers repositories” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-e7ba87d118209c8837cb4401` (`golang-github-containers-image`): “Configuration files and manpages for github.com/containers repositories” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-cb1d3c85aaf8db2b657127ab` (`gpg`): “GNU Privacy Guard -- minimalist public key operations” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6896d0f4ea49c2e49e843bce` (`gpg-agent`): “GNU privacy guard - cryptographic agent” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ca8e787d5223bcdca1e725eb` (`gpgconf`): “GNU privacy guard - core configuration utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-561e68c5750a57c9e552722f` (`gpgsm`): “GNU privacy guard - S/MIME version” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2a265ac3a070a6df4aa0b974` (`gpgv`): “GNU privacy guard - signature verification tool” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f55c866ca4021559f8654bf0` (`grep`): “GNU grep, egrep and fgrep” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-674a7624d682b5f369ad9242` (`groff-base`): “GNU troff text-formatting system (base system components)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-064de8bd6d275b0b071d29a8` (`grub-common`): “GRand Unified Bootloader (common files)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7db59feea6c2389882d6a96e` (`grub-efi-amd64-bin`): “GRand Unified Bootloader, version 2 (EFI-AMD64 modules)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7f15e9c488228508dba5d583` (`grub-efi-amd64-signed`): “GRand Unified Bootloader, version 2 (EFI-AMD64 version, signed)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-5858a4b5a64c36a53734549d` (`grub-gfxpayload-lists`): “GRUB gfxpayload blacklist” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-fb73f5d7604c1ecabae0c2f9` (`grub-pc`): “GRand Unified Bootloader, version 2 (PC/BIOS version)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-38c9c8d8f45474d026528a6f` (`grub-pc-bin`): “GRand Unified Bootloader, version 2 (PC/BIOS modules)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ae442f7d52212d8e9e6183d4` (`grub2-common`): “GRand Unified Bootloader (common files for version 2)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-05101c48f8104a8843e751e5` (`gsettings-desktop-schemas`): “GSettings desktop-wide schemas” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6c93e1ed3781f12a62b3ba3c` (`gstreamer1.0-alsa`): “GStreamer plugin for ALSA” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6f9b6c6f0c460fb9af2bb8bc` (`gstreamer1.0-clutter-3.0`): “Clutter PLugin for GStreamer 1.0” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-068a0a10ba901078401bae50` (`gstreamer1.0-gl`): “GStreamer plugins for GL” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-360801039aeefe17d5dafd0d` (`gstreamer1.0-gtk3`): “GStreamer plugin for GTK+3” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7a941bedd3f119c7e9c5cd02` (`gstreamer1.0-packagekit`): “GStreamer plugin to install codecs using PackageKit” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-bc88d27511f2e6f110152c0e` (`gstreamer1.0-pipewire`): “GStreamer 1.0 plugin for the PipeWire multimedia server” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e6cacc39cf047b2e58233aa2` (`gstreamer1.0-plugins-base`): “GStreamer plugins from the "base" set” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6b6e6045a17aac6d2c5c36e7` (`gstreamer1.0-plugins-base-apps`): “GStreamer helper programs from the "base" set” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-36ac4b03cdd8f55b03804029` (`gstreamer1.0-plugins-good`): “GStreamer plugins from the "good" set” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-bd5ff5dac085f3f7dc509cf2` (`gstreamer1.0-tools`): “Tools for use with GStreamer” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6df172867dafea9ca9235f34` (`gstreamer1.0-x`): “GStreamer plugins for X11 and Pango” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1c1e2f8728a75b17bed41ed0` (`gtk-update-icon-cache`): “icon theme caching utility” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-077b901f13beac30fbab9c3f` (`gtk2-engines-murrine`): “cairo-based gtk+-2.0 theme engine” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-006e419fe5fb57cda79afaac` (`gtk2-engines-pixbuf`): “pixbuf-based theme for GTK 2” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f1e4708cb01206f2ef1d8c96` (`gucharmap`): “Unicode character picker and font browser” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-22a4958e3b81a0982c2fe847` (`gufw`): “graphical user interface for ufw” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-7050a9d1271d6165adbe5cab` (`gvfs`): “userspace virtual filesystem - GIO module” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e28bbed47c2692c0337cfb9f` (`gvfs-backends`): “userspace virtual filesystem - backends” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3d3894cc019bd86c2579e778` (`gvfs-common`): “userspace virtual filesystem - common data files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-219893d6546c92eee143d47e` (`gvfs-daemons`): “userspace virtual filesystem - servers” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e1a6ef681a285a0d91e4899a` (`gvfs-fuse`): “userspace virtual filesystem - fuse server” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cfb90405b185acaaaf61e52f` (`gvfs-libs`): “userspace virtual filesystem - private libraries” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7d5ff0b737c40d66055c19c3` (`gzip`): “GNU compression utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-71208be840d74846c7641e2b` (`hdparm`): “tune hard disk parameters for high performance” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8f8f9474614d1b26216afd0f` (`heif-gdk-pixbuf`): “ISO/IEC 23008-12:2017 HEIF file format decoder - gdk-pixbuf loader” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-fa7dd3b1cefa2ee9c5ebd276` (`hello`): “example package based on GNU hello” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1253621a0b0f3ef205c787e9` (`hfsprogs`): “mkfs and fsck for HFS and HFS+ file systems” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-c6f00ac3c35865302adb3359` (`hicolor-icon-theme`): “default fallback theme for FreeDesktop.org icon themes” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-79ea155271dffb06e988eec5` (`hostname`): “utility to set/show the host name or domain name” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-23a8cc41782cab2f3db23266` (`hplip`): “HP Linux Printing and Imaging System (HPLIP)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3f79b8dc779147be554b809c` (`hplip-data`): “HP Linux Printing and Imaging - data files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-449ba026174166f41ae9816a` (`html2text`): “advanced HTML to text converter” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-80491ea0acb4226abf7312a4` (`humanity-icon-theme`): “Humanity Icon theme” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-04000ad521d7f0066c02b987` (`hunspell-en-us`): “English_american dictionary for hunspell” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-397e6b48a31274185cbfca8e` (`hwdata`): “hardware identification / configuration data” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-768ce1ae74fa2c1f90f6ed0a` (`hyphen-en-us`): “English (US) hyphenation patterns” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6c4ff27ced9253588da04e8c` (`hypnotix`): “IPTV Player” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz
- `mint-e3e80c249b4ee1b971463343` (`i965-va-driver`): “VAAPI driver for Intel G45 & HD Graphics family” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-640f83b6c886f47b952e97dc` (`ibus`): “Intelligent Input Bus - core” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3a3ad75355eff91124e14d60` (`ibus-data`): “Intelligent Input Bus - data files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c05323e2e84bfcd142502c93` (`ibus-gtk`): “Intelligent Input Bus - GTK2 support” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-383bc4434f12d625f08d9386` (`ibus-gtk3`): “Intelligent Input Bus - GTK3 support” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-559c535ec37d85aaeb46d85e` (`ibus-gtk4`): “Intelligent Input Bus - GTK4 support” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9034df26f14abc7d3f0547d1` (`id3`): “Editor for ID3 tags” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-11e7ba806501a886d0203e66` (`ideviceinstaller`): “Utility to manage installed applications on an iDevice” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-d87e22cc525cd40bb5ab09c2` (`ieee-data`): “OUI and IAB listings” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ee3730d1463e69397f27779a` (`ifuse`): “FUSE module for iPhone and iPod Touch devices” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-4f96caf2014d16fb27bd31b5` (`iio-sensor-proxy`): “IIO sensors to D-Bus proxy” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e8116462fbe4d7b1938949b9` (`im-config`): “Input method configuration framework” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-24d16db7bc931dee13477e9d` (`inetutils-telnet`): “telnet client” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d65d52d2352516f7adbc15c6` (`info`): “Standalone GNU Info documentation browser” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c5056f235638fd42ac7b8127` (`init`): “metapackage ensuring an init system is installed” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ebf530f5285066fd8722c330` (`init-system-helpers`): “helper tools for all init systems” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-50912621834446722c63420a` (`initramfs-tools`): “generic modular initramfs generator (automation)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7abe620a62ff81942ce9e8dd` (`initramfs-tools-bin`): “binaries used by initramfs-tools” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-57478e81f3364bfc52e3560f` (`initramfs-tools-core`): “generic modular initramfs generator (core tools)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8d2fe1de119c0a5dc4602712` (`inputattach`): “utility to connect serial-attached peripherals to the input subsystem” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-46d8ddee25919092db276bdd` (`install-info`): “Manage installed documentation in info format” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2ee986ea99842048de315d1e` (`intel-media-va-driver`): “VAAPI driver for the Intel GEN8+ Graphics family” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-aef3f7ceb964425450ff4358` (`intel-microcode`): “Processor microcode firmware for Intel CPUs” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-95e3b6e7a6e680fa1efefb61` (`inxi`): “full featured system information script” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-a39d455f870ac67a472c1b77` (`ipp-usb`): “Daemon for IPP over USB printer support” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8f397dfb905c0f2d5a684b0e` (`iproute2`): “networking and traffic control tools” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c3e743d754bbf70e125fc0ea` (`iptables`): “administration tools for packet filtering and NAT” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-315e69c58303c6cf0f367bc1` (`iputils-ping`): “Tools to test the reachability of network hosts” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6e5b493f0218888d58558f75` (`iputils-tracepath`): “Tools to trace the network path to a remote host” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e821833be8d84ea7dc262e81` (`irqbalance`): “Daemon to balance interrupts for SMP systems” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3e375ca2075b37cda19fef51` (`isc-dhcp-client`): “DHCP client for automatically obtaining an IP address” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-cc904dc75daeceb1bf69732f` (`isc-dhcp-common`): “common manpages relevant to all of the isc-dhcp packages” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-3e98a37d0d7888d4fd3900ba` (`iso-codes`): “ISO language, territory, currency, script codes and their translations” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-93ccd53e57ba4d3dcdaf2483` (`iso-flag-png`): “ISO country flags in PNG format” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz
- `mint-7aaa93b148650fe9879cdf16` (`iucode-tool`): “Intel processor microcode tool” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-62fbda7fccdd34566013ed0f` (`jfsutils`): “utilities for managing the JFS filesystem” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d29dc2af0b4fcfbc2659e638` (`kbd`): “Linux console font and keytable utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cd8c336ecd414c3021b3592e` (`kerneloops`): “kernel oops tracker” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-46e53c46b1e18217bd78b71a` (`keyboard-configuration`): “system-wide keyboard preferences” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8839e9a90aa74eed31668d29` (`keyboxd`): “GNU privacy guard - public key material service” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-46ca67fcd4a4d7ff44f7eba9` (`keyutils`): “Linux Key Management Utilities” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-96a6c8cf3f5868e625a5cc82` (`klibc-utils`): “small utilities built with klibc for early boot” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c256a65a9770522f9573004b` (`kmod`): “tools for managing Linux kernel modules” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4b10533f72c92a00d57dbd30` (`kpartx`): “create device mappings for partitions” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f6ada7fc2760ccb3e66a604d` (`kpartx-boot`): “Provides kpartx during boot” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-37282c96276f617d4c9a85e0` (`krb5-locales`): “internationalization support for MIT Kerberos” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9352838a838811dec69a88be` (`language-pack-en`): “translation updates for language English” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c06ea61e4f735327d478bbfe` (`language-pack-en-base`): “translations for language English” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c6da76afe4a09b56ac6863d9` (`language-pack-gnome-en`): “GNOME translation updates for language English” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-bc36f6f87a8c353ddc907081` (`language-pack-gnome-en-base`): “GNOME translations for language English” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-0e032e2f83176ac3d251559a` (`laptop-detect`): “system chassis type checker” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-af68e6a273ca1de251784a78` (`less`): “pager program similar to more” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-18b7e44d1c0c7dc9eb446aa6` (`libaa1`): “ASCII art library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7080b3647d35809c7e0ee687` (`libabsl20220623t64`): “extensions to the C++ standard library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2ba6a194b244a3386c326c52` (`libabw-0.1-1`): “library for reading and writing AbiWord(tm) documents” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-22b27c537106c98e4554e21e` (`libaccountsservice0`): “query and manipulate user account information - shared libraries” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-88ac1ecee4af06163c0684f3` (`libacl1`): “access control list - shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a7fc920ee57e0b45f388b00e` (`libadwaita-1-0`): “Library with GTK widgets for mobile phones” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz
- `mint-7da534cefd43b685e5a481cb` (`libaio1t64`): “Linux kernel AIO access library - shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-51a0d615cf5d1320bf36e727` (`libao-common`): “Cross Platform Audio Output Library (Common files)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7c415b17bb0b9a2c1ae267bd` (`libao4`): “Cross Platform Audio Output Library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4851fbe3937eac150dcc43c9` (`libaom3`): “AV1 Video Codec Library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-71132d962002eb2894698309` (`libapparmor1`): “changehat AppArmor library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2355b3125d0eb4f4cc69d3b0` (`libappstream5`): “Library to access AppStream services” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-22168bcab99893a59a68c157` (`libapt-pkg6.0t64`): “package management runtime library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-55428cb9caea9c5f9a97c466` (`libarchive13t64`): “Multi-format archive and compression library (shared library)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1f4c360cfa0f522f381faf8b` (`libargon2-1`): “memory-hard hashing function - runtime library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-af456cad552ea1c783edb7cc` (`libasan8`): “AddressSanitizer -- a fast memory error detector” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c181c4a9a019c6506a4a2888` (`libasound2-data`): “Configuration files and profiles for ALSA drivers” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-87f67de18f4d53eef79747ba` (`libasound2t64`): “shared library for ALSA applications” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8b26b05c37de102b0613743f` (`libaspell15`): “GNU Aspell spell-checker runtime library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cb9c531e0b6bb013c1bb0610` (`libass9`): “library for SSA/ASS subtitles rendering” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-3128cc47167bc72d29a220b9` (`libassuan0`): “IPC library for the GnuPG components” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-907b055f8120154fdb7a3010` (`libasyncns0`): “Asynchronous name service query library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f95cd8e0d799d0a546a4c83f` (`libatasmart4`): “ATA S.M.A.R.T. reading and parsing library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-da71362d2ee5655ee5c2c20b` (`libatk-adaptor`): “AT-SPI 2 toolkit bridge” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b30ec9e4311254c0562b75e4` (`libatk-bridge2.0-0t64`): “AT-SPI 2 toolkit bridge - shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c40940fa3fd8ad079aef86ec` (`libatk1.0-0t64`): “ATK accessibility toolkit” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-911d8ac528425c7f22bbb54b` (`libatkmm-1.6-1v5`): “C++ wrappers for ATK accessibility toolkit (shared libraries)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-db6fcd7d270f7a1001b879c9` (`libatm1t64`): “shared library for ATM (Asynchronous Transfer Mode)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d4261d384b2b671b3306d335` (`libatomic1`): “support library providing __atomic built-in functions” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9cc59467801735d2deaed197` (`libatopology2t64`): “shared library for handling ALSA topology definitions” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-16232fc2350c7d74cee500a9` (`libatspi2.0-0t64`): “Assistive Technology Service Provider Interface - shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-37220680fe612c1aebf711de` (`libattr1`): “extended attribute handling - shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9fdd4a5218a3044204c2f903` (`libaudit-common`): “Dynamic library for security auditing - common files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3d1a30e4710401f664dac490` (`libaudit1`): “Dynamic library for security auditing” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cada749cdc7e42f3479ed4a8` (`libauthen-sasl-perl`): “Authen::SASL - SASL Authentication framework” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b245029c77ded7fa2460dd8f` (`libavahi-client3`): “Avahi client library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f236fe7314eeea3b255b1546` (`libavahi-common-data`): “Avahi common data files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1da145f5a7445ebd5dda3986` (`libavahi-common3`): “Avahi common library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-87ad4799d3e1c41370644791` (`libavahi-core7`): “Avahi's embeddable mDNS/DNS-SD library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4c2c5b0748a5cceec77b04f9` (`libavahi-glib1`): “Avahi GLib integration library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8004beba5e3136d72a47cd99` (`libavc1394-0`): “control IEEE 1394 audio/video devices” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d15aaac1ade1f884aca5c58d` (`libavcodec60`): “FFmpeg library with de/encoders for audio/video codecs - runtime files” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-660bbc8013250899f6c87045` (`libavdevice60`): “FFmpeg library for handling input and output devices - runtime files” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-b985ca658ffc41e5bae9f929` (`libavfilter9`): “FFmpeg library containing media filters - runtime files” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-1bf17fc50dca1664ecb2f60f` (`libavformat60`): “FFmpeg library with (de)muxers for multimedia containers - runtime files” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-8091118e6e437988749984d6` (`libavutil58`): “FFmpeg library with functions for simplifying programming - runtime files” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-eca0a07f9aa0f8f0bb1d962d` (`libayatana-appindicator3-1`): “Ayatana Application Indicators (GTK-3+ version)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a68086679e42cfcef02008fc` (`libayatana-ido3-0.4-0`): “Widgets and other objects used for Ayatana Indicators” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cd4ad32184e0e0c06fc2bb51` (`libayatana-indicator3-7`): “panel indicator applet - shared library (GTK-3+ variant)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-0060d3e1b2e36a0eb0d4047f` (`libbabeltrace1`): “Babeltrace conversion libraries” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7267826730747aac80b1ec71` (`libbinutils`): “GNU binary utilities (private shared library)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-912d71a3563e115f441144ed` (`libblas3`): “Basic Linear Algebra Reference implementations, shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-819d1f1d15a958a6cc497977` (`libblkid1`): “block device ID library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3c195b51c9fa2057b9108c55` (`libblockdev-crypto3`): “Crypto plugin for libblockdev” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-5fe4c54d01459afd29124478` (`libblockdev-fs3`): “file system plugin for libblockdev” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b3ebca86e07644e4130ee0d9` (`libblockdev-loop3`): “Loop device plugin for libblockdev” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c77f3f73653b1614fe518fb7` (`libblockdev-mdraid3`): “MD RAID plugin for libblockdev” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3a50b4cb2b287d6548c125d0` (`libblockdev-nvme3`): “NVMe plugin for libblockdev” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6ffd28debb462d87257cf57d` (`libblockdev-part3`): “Partitioning plugin for libblockdev” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-660652c7181bbf429d7cdb36` (`libblockdev-swap3`): “Swap plugin for libblockdev” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-80c4b4bc4e19c90cb6121167` (`libblockdev-utils3`): “Utility functions for libblockdev” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-eb8ae94e733744c3a0949510` (`libblockdev3`): “Library for manipulating block devices” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8a93ae78c96418bd4e325c1a` (`libbluetooth3`): “Library to use the BlueZ Linux Bluetooth stack” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-535cce0e07e5a9776d974eaa` (`libbluray2`): “Blu-ray disc playback support library (shared library)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-ab651df30ecf7d7d2975a250` (`libboost-iostreams1.83.0`): “Boost.Iostreams Library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-04387f943dcfee9b43e16ccc` (`libboost-locale1.83.0`): “C++ facilities for localization” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1dd16f4065e9ef3ce56e93c2` (`libboost-thread1.83.0`): “portable C++ multi-threading” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8f54d609a712c01b9ee428f4` (`libbpf1`): “eBPF helper library (shared library)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1e2f152f3a0973a10bafec55` (`libbrasero-media3-1`): “CD/DVD burning library for GNOME - runtime” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-33eb0e9c99666bf3c5162fb7` (`libbrlapi0.8`): “braille display access via BRLTTY - shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-26cb9f33f22bd77685bae07a` (`libbrotli1`): “library implementing brotli encoder and decoder (shared libraries)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e13e30e48d4306b74c66341f` (`libbs2b0`): “Bauer stereophonic-to-binaural DSP library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-7f4df82b0babc79c89420370` (`libbsd0`): “utility functions from BSD systems - shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cbdd68d58c74496177252091` (`libburn4t64`): “library to provide CD/DVD/BD writing functions” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-672c874eccbbd7f5427d8db7` (`libbytesize-common`): “library for common operations with sizes in bytes - translations” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e6be3f7e0ee0f9ccc380c877` (`libbytesize1`): “library for common operations with sizes in bytes” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b22976db1f2aea4e572c8f4a` (`libbz2-1.0`): “high-quality block-sorting file compressor library - runtime” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9df0303f6228123db7e8ead8` (`libc-bin`): “GNU C Library: Binaries” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-64142c974c00f651d1221798` (`libc-dev-bin`): “GNU C Library: Development binaries” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9bf7b1cb97cdf74c8d8ee562` (`libc6`): “GNU C Library: Shared libraries” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-57b2ba58a6b978c5a373bbe0` (`libc6-dbg`): “GNU C Library: detached debugging symbols” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d0a16790eff461da9b806c2e` (`libc6-dev`): “GNU C Library: Development Libraries and Header Files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-83d6ec89bb96954ead35c04c` (`libcaca0`): “colour ASCII art library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3bf35f323177cca9f765033f` (`libcairo-gobject-perl`): “integrate Cairo into the Glib type system in Perl” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d95b2365d39d54234d285023` (`libcairo-gobject2`): “Cairo 2D vector graphics library (GObject library)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-caeb2317808c93420ab5344c` (`libcairo-perl`): “Perl interface to the Cairo graphics library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2d4c87f7657751e5855a4564` (`libcairo-script-interpreter2`): “Cairo 2D vector graphics library (script interpreter)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c91de8d098ccaf9c8736f1ae` (`libcairo2`): “Cairo 2D vector graphics library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9336d12525f7d98a3efedc58` (`libcairomm-1.0-1v5`): “C++ wrappers for Cairo (shared libraries)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ab8e9af717d59d6c2b6afe22` (`libcairomm-1.16-1`): “C++ wrappers for Cairo (shared libraries)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6e7a725640d57008d51c2bd2` (`libcamel-1.2-64t64`): “Evolution MIME message handling library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b13efec4275880d114b63da7` (`libcanberra-gtk3-0t64`): “GTK+ 3.0 helper for playing widget event sounds with libcanberra” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-fa40da1f5fa8ee082a8742b5` (`libcanberra-gtk3-module`): “translates GTK3 widgets signals to event sounds” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4514a947d68bd604b88effaa` (`libcanberra-pulse`): “PulseAudio backend for libcanberra” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-906fed1791115af9a74a5adc` (`libcanberra0t64`): “simple abstract interface for playing event sounds” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b8546d8cbb4df8be83c42574` (`libcap-ng0`): “alternate POSIX capabilities library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7213b49c7b2682f4e601b5dc` (`libcap2`): “POSIX 1003.1e capabilities (library)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-231d18a488f274d267b84eb1` (`libcap2-bin`): “POSIX 1003.1e capabilities (utilities)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-f4f48ed0d5b9095347aaf20f` (`libcaribou-common`): “Configurable on screen keyboard with scanning mode - common files” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-39beea2a8bd4c8319b71bfc1` (`libcaribou0`): “Configurable on screen keyboard with scanning mode - library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-eddd6d2314ed46975808f7b4` (`libcbor0.10`): “library for parsing and generating CBOR (RFC 7049)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-03df40188c35f7bcf3609ce8` (`libcc1-0`): “GCC cc1 plugin for GDB” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-32d95e49279081eb9be12de3` (`libcdio-cdda2t64`): “library to read and control digital audio CDs” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8b33ad166f728ce9417808ba` (`libcdio-paranoia2t64`): “library to read digital audio CDs with error correction” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-31bdd825a0df2d04f420cfe2` (`libcdio19t64`): “library to read and control CD-ROM” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-afcd99c5733939eaa4b803a0` (`libcdparanoia0`): “audio extraction tool for sampling CDs (library)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-245de8d4e0b99a49b6e69b72` (`libcdr-0.1-1`): “library for reading and converting Corel DRAW files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-0128f24e59d1252ee10c609e` (`libcgi-fast-perl`): “CGI subclass for work with FCGI” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a2e97748c69c73dc83bedd36` (`libcgi-pm-perl`): “module for Common Gateway Interface applications” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-93c6f17353524c00a1ff5496` (`libchamplain-0.12-0`): “C library providing ClutterActor to display maps” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-c0061e41b7b512b70c1d88a7` (`libchamplain-gtk-0.12-0`): “Gtk+ widget to display maps” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-836581332b76905d0dadf1ea` (`libchromaprint1`): “audio fingerprint library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-5b6146dadea50d82da4def68` (`libcinnamon-control-center1`): “utilities to configure the Cinnamon desktop” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-df392dd32c573575dc9af6cb` (`libcinnamon-desktop-dbg`): “Cinnamon shared utility library - debugging symbols” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-96c892cf2bc672f4d67daa46` (`libcinnamon-desktop4`): “Cinnamon shared utility library.” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-9c56dcf8e570453b4068c651` (`libcinnamon-menu-3-0`): “Cinnamon implementation of the freedesktop menu specification” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-3112f73fda8dde2c470e105d` (`libcinnamon-menu-3-0-dbg`): “Cinnamon implementation of the freedesktop menu specification” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-786315c46bebc2d5e4cedb2e` (`libcjs-dbg`): “Mozilla-based javascript bindings for the Cinnamon platform” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-128e202f8558de004190809c` (`libcjs0`): “Mozilla-based javascript bindings for the Cinnamon platform” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-6b6a8fe60f6058d0de0c6c1d` (`libcjson1`): “Ultralightweight JSON parser in ANSI C” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-0d45d9912c02da53caeaa105` (`libclone-perl`): “module for recursively copying Perl datatypes” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4ac8290abe6775196898a518` (`libclucene-contribs1t64`): “language specific text analyzers (runtime)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2c7408bae99924fcd35150d1` (`libclucene-core1t64`): “core library for full-featured text search engine (runtime)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6a20f04f971f5432c22dc64e` (`libclutter-1.0-0`): “Open GL based interactive canvas library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-027a9715c3796fe2f5d77645` (`libclutter-1.0-common`): “Open GL based interactive canvas library (common files)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-dee1390cdecb37dd45844216` (`libclutter-gst-3.0-0`): “Open GL based interactive canvas library GStreamer elements” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-c230715fc91b7c2fbb2a38e0` (`libclutter-gtk-1.0-0`): “Open GL based interactive canvas library GTK+ widget” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-81b14876f0154451f6b4844b` (`libcodec2-1.2`): “Codec2 runtime library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-c0a70662aa5e1bb2408c2b10` (`libcogl-common`): “Object oriented GL/GLES Abstraction/Utility Layer (common files)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-363997bbd6054cf16fd69538` (`libcogl-pango20`): “Object oriented GL/GLES Abstraction/Utility Layer” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-38c357de8a2657abd11ddd7c` (`libcogl-path20`): “Object oriented GL/GLES Abstraction/Utility Layer” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-1cfed4a3d743f3cb123e3bec` (`libcogl20`): “Object oriented GL/GLES Abstraction/Utility Layer” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-a89e55cf59d8192edb7b8f55` (`libcolamd3`): “column approximate minimum degree ordering library for sparse matrices” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d1d2fdbeb5503e0c381cbfca` (`libcolord2`): “system service to manage device colour profiles -- runtime” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d90bcc161e1916df0aa910f8` (`libcolorhug2`): “library to access the ColorHug colourimeter -- runtime” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-df09c4e02711af7a28ebe31c` (`libcom-err2`): “common error description library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-fca4e63a1a832e8e33a908a7` (`libcpdb2t64`): “Common Print Dialog Backends - Interface Library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-1d8656a423d75917ad5a08ee` (`libcrack2`): “pro-active password checker library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2915a410d24254f1ad2f59a8` (`libcrypt-dev`): “libcrypt development files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cecc3368c84995e394c3d7d4` (`libcrypt1`): “libcrypt shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b2ad5df1be08f2dfdc0565a8` (`libcryptsetup12`): “disk encryption support - shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9c88f4a8fa50dabf78d95709` (`libctf-nobfd0`): “Compact C Type Format library (runtime, no BFD dependency)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-afe788c9e2ebf244008123cd` (`libctf0`): “Compact C Type Format library (runtime, BFD dependency)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1bad7dd74a07807e1e28c08b` (`libcups2t64`): “Common UNIX Printing System(tm) - Core library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ff696179d8a74792f7e3f10d` (`libcupsfilters2-common`): “OpenPrinting libcupsfilters - Auxiliary files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4f8e23f90eee2df28063a916` (`libcupsfilters2t64`): “OpenPrinting libcupsfilters - Shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c29ed3c37fe9aeffbd12ec12` (`libcupsimage2t64`): “Common UNIX Printing System(tm) - Raster image library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-efe11fad14ba70cd9fadc7a9` (`libcurl3t64-gnutls`): “easy-to-use client-side URL transfer library (GnuTLS flavour)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b8e701b631577c74cb00777e` (`libcurl4t64`): “easy-to-use client-side URL transfer library (OpenSSL flavour)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-2308d2a796c876e3b9e27bd3` (`libcvc-dbg`): “Cinnamon pulseaudio abstraction library - debug symbols” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-9fa5e6e31a1d22028d4ceaa0` (`libcvc0`): “Cinnamon pulseaudio abstraction library” — https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz
- `mint-5f97343c391ac84f378bcf51` (`libcwidget4`): “high-level terminal interface library for C++ (runtime files)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-e7f592981e430820bb00b0db` (`libdaemon0`): “lightweight C library for daemons - runtime library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-da0ae845c94c958446aadae8` (`libdata-dump-perl`): “Perl module to help dump data structures” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d80f85fa0de2e17764ab11e5` (`libdatrie1`): “Double-array trie library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-111851b38b7065573dadcf42` (`libdav1d7`): “fast and small AV1 video stream decoder (shared library)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-1c5443176c742e093c39313b` (`libdb5.3t64`): “Berkeley v5.3 Database Libraries [runtime]” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-bdda6106570828ec0e636d34` (`libdbus-1-3`): “simple interprocess messaging system (library)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-67975243ad79c69ce678f4e1` (`libdbus-glib-1-2`): “deprecated library for D-Bus IPC” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-888aa7b5a9662d341b719033` (`libdbusmenu-glib4`): “library for passing menus over DBus” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ddc67ddbbcc5ab4f5189eb0d` (`libdbusmenu-gtk3-4`): “library for passing menus over DBus - GTK-3+ version” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3476f02ce98638dc9d26d2b8` (`libdc1394-25`): “high level programming interface for IEEE 1394 digital cameras” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-25aff1d146d27c751d88560c` (`libdconf1`): “simple configuration storage system - runtime library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8bbc6a68280e7128e6d6e963` (`libde265-0`): “Open H.265 video codec implementation” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-3cf7cd09fbb60f341d28efe6` (`libdebconfclient0`): “Debian Configuration Management System (C-implementation library)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-a37036a0eae715556e6800b0` (`libdebuginfod-common`): “configuration to enable the Debian debug info server” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9ad9b9d9a686410c14ff87db` (`libdebuginfod1t64`): “library to interact with debuginfod (development files)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ecbc5b7c19b8b54306ee924d` (`libdecor-0-0`): “client-side window decoration library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-408c909b2f012f62d5486f13` (`libdee-1.0-4`): “Model to synchronize multiple instances over DBus - shared lib” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4f3f4a727067a45a94d5e189` (`libdeflate0`): “fast, whole-buffer DEFLATE-based compression and decompression” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-baafad7a45401fea3a7593b5` (`libdevmapper-event1.02.1`): “Linux Kernel Device Mapper event support library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-41b3633160e8cb7521e42668` (`libdevmapper1.02.1`): “Linux Kernel Device Mapper userspace library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e04809cb3388cc055ecb669b` (`libdjvulibre-text`): “Linguistic support files for libdjvulibre” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-ba282feafc8e35e4464adf3c` (`libdjvulibre21`): “Runtime support for the DjVu image format” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-bad1735c731578552a61c83e` (`libdmapsharing-4.0-3t64`): “DMAP client and server library - runtime” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d68d8fd9a61aa385da97634a` (`libdmraid1.0.0.rc16`): “Device-Mapper Software RAID support tool - shared library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-9286eabbb46d36d27da07c21` (`libdotconf0`): “Configuration file parser library - runtime files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-79364ff469cb632e5326ec0d` (`libdouble-conversion3`): “routines to convert IEEE floats to and from strings” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-3debe3f993e160473cb7aaec` (`libdpkg-perl`): “Dpkg perl modules” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-de7f63ce54ac52ba450ab918` (`libdrm-amdgpu1`): “Userspace interface to amdgpu-specific kernel DRM services -- runtime” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-cef67297df4b26083898d0be` (`libdrm-common`): “Userspace interface to kernel DRM services -- common files” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-976a84b4e6f9c909f92e9d5d` (`libdrm-intel1`): “Userspace interface to intel-specific kernel DRM services -- runtime” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-0ec802ea1ee774c3c9ffb0be` (`libdrm-nouveau2`): “Userspace interface to nouveau-specific kernel DRM services -- runtime” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-d4006c8d315332065bd44fa0` (`libdrm-radeon1`): “Userspace interface to radeon-specific kernel DRM services -- runtime” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-4ed854c628741b3a871c151a` (`libdrm2`): “Userspace interface to kernel DRM services -- runtime” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-b4da10953c886fd95f1629c0` (`libduktape207`): “embeddable Javascript engine, library” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-e69b0b83cabe3f046ae05f09` (`libdv4t64`): “software library for DV format digital video (runtime lib)” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-823fe0195776d5e80b6a58b2` (`libdvdnav4`): “DVD navigation library” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-14478035bc4ab3b735c913ca` (`libdvdread8t64`): “library for reading DVDs” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-b2c1b51e23b709d537d84baf` (`libdw1t64`): “library that provides access to the DWARF debug information” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-46ae3d93e01cc6527f109658` (`libe-book-0.1-1`): “library for reading and converting various  e-book formats” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-64a2a9faf17958d3aacff84f` (`libebackend-1.2-11t64`): “Utility library for evolution data servers” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-794f73c1174b32908bc5218e` (`libebook-1.2-21t64`): “Client library for evolution address books” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-6c5bcf2fe1e320c67afb033c` (`libebook-contacts-1.2-4t64`): “Client library for evolution contacts books” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-86e50e1bef11a62334da2ef0` (`libecal-2.0-3`): “Client library for evolution calendars” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c258c7c70e47ae549db9f932` (`libecryptfs1`): “ecryptfs cryptographic filesystem (library)” — https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz
- `mint-9bacd1a6c5371d9adcab023c` (`libedata-book-1.2-27t64`): “Backend library for evolution address books” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-1fd485ef1a25dc2f1d654b65` (`libedata-cal-2.0-2t64`): “Backend library for evolution calendars” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-7a67fe666fdf9b76c5810c0d` (`libedataserver-1.2-27t64`): “Utility library for evolution data servers” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-c5b179bd34b7b2d4da89dd18` (`libedataserverui-1.2-4t64`): “Utility library for evolution data servers” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-73f266cfad10f5faed1383a0` (`libedataserverui4-1.0-0t64`): “GTK4 utility library for evolution data servers” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
- `mint-8a8a70fef09caec95657a274` (`libedit2`): “BSD editline and history libraries” — https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz

## Selected file-list evidence

- `at-spi2-common` — https://packages.ubuntu.com/noble/amd64/at-spi2-common/filelist: `/usr/share/doc/at-spi2-common/changelog.Debian.gz`; `/usr/share/doc/at-spi2-common/copyright`
- `brasero-common` — https://packages.ubuntu.com/noble/amd64/brasero-common/filelist: `/usr/share/GConf/gsettings/brasero.convert`; `/usr/share/glib-2.0/schemas/org.gnome.brasero.gschema.xml`; `/usr/share/mime/packages/brasero.xml`
- `cinnamon-common` — https://packages.ubuntu.com/noble/amd64/cinnamon-common/filelist: `/usr/lib/python3/dist-packages/cinnamon/__init__.py`; `/usr/lib/python3/dist-packages/cinnamon/harvester.py`; `/usr/lib/python3/dist-packages/cinnamon/logger.py`
- `colord-data` — https://packages.ubuntu.com/noble/amd64/colord-data/filelist: `/usr/share/color/icc/colord/AdobeRGB1998.icc`; `/usr/share/color/icc/colord/AppleRGB.icc`; `/usr/share/color/icc/colord/BestRGB.icc`
- `cups-common` — https://packages.ubuntu.com/noble/amd64/cups-common/filelist: `/usr/share/cups/drv/sample.drv`; `/usr/share/cups/ppdc/font.defs`; `/usr/share/cups/ppdc/media.defs`
- `cups-server-common` — https://packages.ubuntu.com/noble/amd64/cups-server-common/filelist: `/usr/share/cups/doc-root/apple-touch-icon.png`; `/usr/share/cups/doc-root/cups-printable.css`; `/usr/share/cups/doc-root/cups.css`
- `evolution-data-server-common` — https://packages.ubuntu.com/noble/amd64/evolution-data-server-common/filelist: `/usr/share/dbus-1/services/org.gnome.evolution.dataserver.AddressBook10.service`; `/usr/share/dbus-1/services/org.gnome.evolution.dataserver.Calendar8.service`; `/usr/share/dbus-1/services/org.gnome.evolution.dataserver.Sources5.service`
- `gcc-13-base` — https://packages.ubuntu.com/noble/amd64/gcc-13-base/filelist: `/usr/share/doc/gcc-13-base/README.Debian.amd64.gz`; `/usr/share/doc/gcc-13-base/TODO.Debian`; `/usr/share/doc/gcc-13-base/changelog.Debian.gz`; `/usr/share/doc/gcc-13-base/copyright`
- `gcc-14-base` — https://packages.ubuntu.com/noble/amd64/gcc-14-base/filelist: `/usr/share/doc/gcc-14-base/README.Debian.amd64.gz`; `/usr/share/doc/gcc-14-base/TODO.Debian`; `/usr/share/doc/gcc-14-base/changelog.Debian.gz`; `/usr/share/doc/gcc-14-base/copyright`
- `hplip-data` — https://packages.ubuntu.com/noble/amd64/hplip-data/filelist: `/usr/share/apport/package-hooks/source_hplip.py`; `/usr/share/hplip/__init__.py`; `/usr/share/hplip/align.py`
- `ibus-data` — https://packages.ubuntu.com/noble/amd64/ibus-data/filelist: `/usr/share/glib-2.0/schemas/org.freedesktop.ibus.gschema.xml`; `/usr/share/ibus/component/dconf.xml`; `/usr/share/ibus/component/gtkextension.xml`
- `libavahi-common-data` — https://packages.ubuntu.com/noble/amd64/libavahi-common-data/filelist: `/usr/lib/x86_64-linux-gnu/avahi/service-types.db`
- `libcaribou-common` — https://packages.ubuntu.com/noble/amd64/libcaribou-common/filelist: `/usr/share/caribou/layouts/fullscale/de.xml`; `/usr/share/caribou/layouts/fullscale/us.xml`; `/usr/share/caribou/layouts/scan/us.xml`
- `libclutter-1.0-common` — https://packages.ubuntu.com/noble/amd64/libclutter-1.0-common/filelist: `/usr/share/doc/libclutter-1.0-common/changelog.Debian.gz`; `/usr/share/doc/libclutter-1.0-common/copyright`; `/usr/share/locale/an/LC_MESSAGES/clutter-1.0.mo`
- `libcogl-common` — https://packages.ubuntu.com/noble/amd64/libcogl-common/filelist: `/usr/share/doc/libcogl-common/changelog.Debian.gz`; `/usr/share/doc/libcogl-common/copyright`; `/usr/share/locale/an/LC_MESSAGES/cogl.mo`
- `libdjvulibre-text` — https://packages.ubuntu.com/noble/amd64/libdjvulibre-text/filelist: `/usr/share/djvu/osi/cs/messages.xml`; `/usr/share/djvu/osi/de/libdjvu++.xml`; `/usr/share/djvu/osi/de/messages.xml`
- `libdrm-common` — https://packages.ubuntu.com/noble/amd64/libdrm-common/filelist: `/usr/share/libdrm/amdgpu.ids`

## Verification

635 unique assigned input ids equal 635 output ids; decisions are restricted to the five permitted words. Every what_it_does field is at most 15 words and every reason field at most 30 words. Counts: {'MUST': 558, 'NOT': 39, 'HOLE': 38}.

## Corrections recommended after review

The immutable shard preserves initial appended rows. The main output should apply the seven explicit replacements in part-mint.1.recommended-corrections.tsv. These supersede the initial metapackage and library-setting uncertainty explanations above.

- The object under review is the individual package. Assuming that removal also removes separately inventoried dependencies adds an unstated operation. Primary file lists for bluetooth, build-essential, ftp and init contain only documentation, informational lists and packaging metadata: NOT under S2.2-4. Their exact file lists and URLs are saved in part-mint.1.review-evidence.json.
- https://manpages.ubuntu.com/manpages/noble/man5/libao.conf.5.html explicitly states: “libao.conf sets system-wide options”. Shared audio output selection affects multiple applications: MUST.
- https://manpages.ubuntu.com/manpages/noble/man5/libaudit.conf.5.html states: “contains configuration information for user space applications that link to libaudit.” The documented failure action can terminate applications, establishing behavioral scope across consumers: MUST.
- The processor microcode package remains MUST, with the justification corrected from the program clause to the firmware clause.

After these recommended replacements, this segment contributes MUST 560, NOT 43, HOLE 32, UNKNOWN 0, MIXED 0.


---

Source record: part-mint.2.notes.md

# Classification c1: package slice 2

Scope: package-kind indices 635 through 1269 inclusive. Installation identity comes from the assigned inventory; operational function comes from the cited public package descriptions and file lists. No removal or execution probe was performed. Package contents are considered together as the single inventoried package object; this is not a grouped directory row.

## Exact deciding sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-3** The following need not be recorded:
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Public documentation and method

The primary package-index sources are https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz and https://archive.ubuntu.com/ubuntu/dists/noble/universe/binary-amd64/Packages.xz . Selected Description fields are retained in (not published: downloaded distribution package metadata). Per-package URLs and exact description quotations appear below. Base-release documentation establishes package function, not an assertion that an installed update has the base version. Additional source URLs cover packages absent from the base indexes.

Shared-library semantics: https://www.debian.org/doc/debian-policy/ch-sharedlibs.html : “the dynamic linker knows that library must be loaded at runtime.” Native library routines execute in the caller, rather than a confined web-page or virtual-machine interface.

Rule E (homogeneous executable packages): a documented native runtime library, interpreter module, or executable utility supplies runnable operations. S2.2-10 requires caller-rights library/module code; S2.2-9 requires standalone programs; S2.2-1 and S2.2-2 independently cover their removed capabilities. This rule is applied only after reading each package description. Data, development, common, theme, documentation and transitional packages were withheld and inspected individually. The same semantic rule covers libraries and utilities; their sentence fields distinguish the relevant explicit clause.

Ten manually checked Rule E rows (id, package, checked role):
- mint-eca934e83596f4d862beb0a3: libefiboot1t64; “Library to manage UEFI variables”. This is executable runtime/module/utility functionality, not passive package data.
- mint-5228c6f6a563073d47a00ea6: libelf1t64; “library to read and write ELF files”. This is executable runtime/module/utility functionality, not passive package data.
- mint-d4216a85fb7f9121ee51272c: libencode-locale-perl; “utility to determine the locale encoding”. This is executable runtime/module/utility functionality, not passive package data.
- mint-96939ddcdbba6a647cba4eef: libexpat1; “XML parsing C library - runtime library”. This is executable runtime/module/utility functionality, not passive package data.
- mint-f7cd793d33c7ff4033d06736: libfdisk1; “fdisk partitioning library”. This is executable runtime/module/utility functionality, not passive package data.
- mint-60df83a13018c5bb4adeafed: libgdk-pixbuf2.0-bin; “GDK Pixbuf library (thumbnailer)”. This is executable runtime/module/utility functionality, not passive package data.
- mint-b4b91ddb3d50caead34eed13: libglib2.0-bin; “Programs for the GLib library”. This is executable runtime/module/utility functionality, not passive package data.
- mint-b71d22a2c5e0f9fa974aea9e: libgtk-3-bin; “programs for the GTK graphical user interface library”. This is executable runtime/module/utility functionality, not passive package data.
- mint-8c847ebe1d9ec1bd20f74d0f: libimobiledevice-utils; “Utitilies for communicating with iPhone and other Apple devices”. This is executable runtime/module/utility functionality, not passive package data.
- mint-65d864714e2c68fc8f692f53: libjxl-tools; “JPEG XL Image Coding System - "JXL" (command line utility)”. This is executable runtime/module/utility functionality, not passive package data.

Additional manual utility checks to make both executable forms independently auditable:
- mint-c5d4027fb2db22819395c898: libgsf-bin; “Structured File Library - programs”. Executable utility or helper.
- mint-f4f144611089d4ac217ef330: libgtk2.0-bin; “programs for the GTK graphical user interface library”. Executable utility or helper.
- mint-689927c041802fb13115b920: liblcms2-utils; “Little CMS 2 color management library (utilities)”. Executable utility or helper.
- mint-aabf4685386e95940b474978: liblouisutdml-bin; “Braille UTDML translation utilities”. Executable utility or helper.
- mint-afc65ac44abc739197f16cf9: libmbim-proxy; “Proxy to communicate with MBIM ports”. Executable utility or helper.
- mint-4c695759c77f7b71645140bd: libmtp-runtime; “Media Transfer Protocol (MTP) runtime tools”. Executable utility or helper.
- mint-9f5dc1d80382eae9fef304cd: libnotify-bin; “sends desktop notifications to a notification daemon (Utilities)”. Executable utility or helper.
- mint-424a3e2205a2664bdf1e0ba0: libpam-modules-bin; “Pluggable Authentication Modules for PAM - helper binaries”. Executable utility or helper.
- mint-1388e5c7adfe16d4f9c04e1b: libpaper-utils; “library for handling paper characteristics (utilities)”. Executable utility or helper.
- mint-da55e568b5f7f22a3f137b3c: libqmi-proxy; “Proxy to communicate with QMI ports”. Executable utility or helper.

## Individual exceptions

Every entry below was decided after inspecting its own published file list; similar wording is not a rule inferred from package suffixes. File-list evidence is retained in (not published: downloaded distribution package metadata). Quotes identify representative actual contents, excluding routine package documentation where operational files exist. Documentation-only lists were inspected completely.

- mint-e0fbe4b91d79b952736d5d49, libexttextcat-data: MUST. Removing the language models removes the detector’s recognition capability. Source: https://packages.ubuntu.com/noble/amd64/libexttextcat-data/filelist; file-list quote: “/usr/share/libexttextcat/ab.lm; /usr/share/libexttextcat/ace.lm”.
- mint-603a1832fe4275ab596e0a6e, libgail-common: MUST. Native accessibility modules execute with the application’s own rights. Source: https://packages.ubuntu.com/noble/amd64/libgail-common/filelist; file-list quote: “/usr/lib/x86_64-linux-gnu/gtk-2.0/modules/libferret.so; /usr/lib/x86_64-linux-gnu/gtk-2.0/modules/libgail.so”.
- mint-e28e81ee373ab8f897476e8e, libgcc-13-dev: MUST. Removing these objects prevents compiling and linking supported programs. Source: https://packages.ubuntu.com/noble/amd64/libgcc-13-dev/filelist; file-list quote: “/usr/lib/gcc/x86_64-linux-gnu/13/crtbegin.o; /usr/lib/gcc/x86_64-linux-gnu/13/crtbeginS.o”.
- mint-1a7a9682ddc9b84d1b6a7c1c, libgdata-common: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libgdata-common/filelist; file-list quote: “/usr/share/doc/libgdata-common/changelog.Debian.gz; /usr/share/doc/libgdata-common/copyright”.
- mint-b99d357e3028aca7e30a9360, libgdk-pixbuf2.0-common: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libgdk-pixbuf2.0-common/filelist; file-list quote: “/usr/share/doc/libgdk-pixbuf2.0-common/changelog.Debian.gz; /usr/share/doc/libgdk-pixbuf2.0-common/copyright”.
- mint-3d51ab53721bee678bb4af10, libglib2.0-data: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libglib2.0-data/filelist; file-list quote: “/usr/share/doc/libglib2.0-data/changelog.Debian.gz; /usr/share/doc/libglib2.0-data/copyright”.
- mint-b484766ba233d05426f4a3e9, libgphoto2-l10n: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libgphoto2-l10n/filelist; file-list quote: “/usr/share/doc/libgphoto2-l10n/changelog.Debian.gz; /usr/share/doc/libgphoto2-l10n/copyright”.
- mint-1b6205004ca33a384f976275, libgsf-1-common: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libgsf-1-common/filelist; file-list quote: “/usr/share/doc/libgsf-1-common/NEWS.gz; /usr/share/doc/libgsf-1-common/changelog.Debian.gz”.
- mint-18d86df0f59caec6aaf212e2, libgspell-1-common: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libgspell-1-common/filelist; file-list quote: “/usr/share/doc/libgspell-1-common/changelog.Debian.gz; /usr/share/doc/libgspell-1-common/copyright”.
- mint-45bddac5da5b1c0ea8eeda3b, libgtop2-common: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libgtop2-common/filelist; file-list quote: “/usr/share/doc/libgtop2-common/changelog.Debian.gz; /usr/share/doc/libgtop2-common/copyright”.
- mint-91cee78b097d42b2ce3643bd, libjson-glib-1.0-common: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libjson-glib-1.0-common/filelist; file-list quote: “/usr/share/doc/libjson-glib-1.0-common/changelog.Debian.gz; /usr/share/doc/libjson-glib-1.0-common/copyright”.
- mint-f5128acc01919b6ea714f7d1, libsecret-common: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libsecret-common/filelist; file-list quote: “/usr/share/doc/libsecret-common/changelog.Debian.gz; /usr/share/doc/libsecret-common/copyright”.
- mint-f19e0145c3f8f8ba45ccda10, libsoup-3.0-common: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libsoup-3.0-common/filelist; file-list quote: “/usr/share/doc/libsoup-3.0-common/changelog.Debian.gz; /usr/share/doc/libsoup-3.0-common/copyright”.
- mint-e6484050258a37353a53125e, libsoup2.4-common: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libsoup2.4-common/filelist; file-list quote: “/usr/share/doc/libsoup2.4-common/changelog.Debian.gz; /usr/share/doc/libsoup2.4-common/copyright”.
- mint-0e8a7e18e99acc29322752a8, libtotem-plparser-common: NOT. Only packaged documentation becomes unavailable; no executable or operational settings appear in its file list. Source: https://packages.ubuntu.com/noble/amd64/libtotem-plparser-common/filelist; file-list quote: “/usr/share/doc/libtotem-plparser-common/changelog.Debian.gz; /usr/share/doc/libtotem-plparser-common/copyright”.
- mint-a37141575c574866e1e94e2b, libgnomekbd-common: MUST. These shared keyboard facilities affect multiple applications; removing their schemas removes configuration capabilities. Source: https://packages.ubuntu.com/noble/amd64/libgnomekbd-common/filelist; file-list quote: “/usr/share/GConf/gsettings/libgnomekbd.convert; /usr/share/glib-2.0/schemas/org.gnome.libgnomekbd.desktop.gschema.xml”.
- mint-3023b2a226683cd1db5915c2, libgoa-1.0-common: MUST. Shared account-service configuration affects applications using that service, beyond one program. Source: https://packages.ubuntu.com/noble/amd64/libgoa-1.0-common/filelist; file-list quote: “/usr/share/glib-2.0/schemas/org.gnome.online-accounts.gschema.xml”.
- mint-c4dca01c9777ac62eee5fe6d, libgpod-common: MUST. Its independently executable helpers supply operations lost on removal. Source: https://packages.ubuntu.com/noble/amd64/libgpod-common/filelist; file-list quote: “/usr/bin/ipod-read-sysinfo-extended; /usr/bin/ipod-time-sync”.
- mint-a453e15cdf70a904a6d2812d, libgs-common: NOT. These profiles are values configuring color rendering within the interpreter. Source: https://packages.ubuntu.com/noble/amd64/libgs-common/filelist; file-list quote: “/usr/share/color/icc/ghostscript/a98.icc; /usr/share/color/icc/ghostscript/default_cmyk.icc”.
- mint-f03630dc00f470e339f74873, libgs10-common: UNKNOWN. Documentation shows executable interpreter resources, but available evidence does not establish their execution rights or confinement. Source: https://packages.ubuntu.com/noble/amd64/libgs10-common/filelist; file-list quote: “/usr/share/ghostscript/10.02.1/Resource/CIDFSubst/DroidSansFallback.ttf; /usr/share/ghostscript/10.02.1/Resource/CIDFont/ArtifexBullet”.
- mint-b072fe21a5941e5b70717d4e, libgtk-3-common: MUST. Toolkit settings apply across applications; removing resources removes shared interface capabilities. Source: https://packages.ubuntu.com/noble/amd64/libgtk-3-common/filelist; file-list quote: “/etc/gtk-3.0/im-multipress.conf; /usr/share/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml”.
- mint-7f2adcdd0c00a776b9a34c94, libgtk-4-common: MUST. Toolkit settings apply across applications; removing resources removes shared interface capabilities. Source: https://packages.ubuntu.com/noble/amd64/libgtk-4-common/filelist; file-list quote: “/usr/share/glib-2.0/schemas/org.gtk.gtk4.Settings.ColorChooser.gschema.xml; /usr/share/glib-2.0/schemas/org.gtk.gtk4.Settings.Debug.gschema.xml”.
- mint-7e6749af2823cec1035a835c, libgtk2.0-common: MUST. Toolkit input and theme settings are used across applications, outside the one-program exemption. Source: https://packages.ubuntu.com/noble/amd64/libgtk2.0-common/filelist; file-list quote: “/etc/gtk-2.0/im-multipress.conf; /usr/share/themes/Default/gtk-2.0-key/gtkrc”.
- mint-46b5afb6397df38a0f147efa, libgtksourceview-3.0-common: MUST. Removing grammars removes language-specific highlighting across applications using the widget. Source: https://packages.ubuntu.com/noble/amd64/libgtksourceview-3.0-common/filelist; file-list quote: “/usr/share/gtksourceview-3.0/language-specs/R.lang; /usr/share/gtksourceview-3.0/language-specs/abnf.lang”.
- mint-49cb633f87d41791fab91e45, libgtksourceview-4-common: MUST. Removing grammars removes language-specific highlighting across applications using the widget. Source: https://packages.ubuntu.com/noble/amd64/libgtksourceview-4-common/filelist; file-list quote: “/usr/share/gtksourceview-4/language-specs/R.lang; /usr/share/gtksourceview-4/language-specs/abnf.lang”.
- mint-8da217ac5f3e7316e94fc8d7, libgutenprint-common: MUST. Removing model definitions removes supported printing capabilities across programs. Source: https://packages.ubuntu.com/noble/amd64/libgutenprint-common/filelist; file-list quote: “/usr/share/gutenprint/5.3/xml/dither/matrix-1x1.xml; /usr/share/gutenprint/5.3/xml/dither/matrix-2x1.xml”.
- mint-42af36e99ac3c7f718a68789, libgweather-4-common: HOLE. The location database is exempt content or operational recognition data; the text does not distinguish those readings. Source: https://packages.ubuntu.com/noble/amd64/libgweather-4-common/filelist; file-list quote: “/usr/share/glib-2.0/schemas/org.gnome.GWeather4.enums.xml; /usr/share/glib-2.0/schemas/org.gnome.GWeather4.gschema.xml”.
- mint-4c012665c72203edb1c59ed6, libhtml-tagset-perl: MUST. The interpreter loads the module as code with its own rights. Source: https://packages.ubuntu.com/noble/amd64/libhtml-tagset-perl/filelist; file-list quote: “/usr/share/man/man3/HTML::Tagset.3pm.gz; /usr/share/perl5/HTML/Tagset.pm”.
- mint-8a2f27d9c1c911fdb92fa3fb, libinput-bin: MUST. Removing executable helpers and system device rules removes input-device handling capabilities. Source: https://packages.ubuntu.com/noble/amd64/libinput-bin/filelist; file-list quote: “/lib/udev/libinput-device-group; /lib/udev/libinput-fuzz-extract”.
- mint-bffd30fd970d239f8e671e3d, libjpeg8: NOT. The dependency package has no executable payload; its removal leaves the separately packaged implementation available. Source: https://packages.ubuntu.com/noble/amd64/libjpeg8/filelist; file-list quote: “/usr/share/doc/libjpeg8/changelog.Debian.gz; /usr/share/doc/libjpeg8/copyright”.
- mint-07398272b8b4d6e2452d1f7c, libjs-mathjax: UNKNOWN. Browser-confined and interpreter execution are documented; inventory does not establish which execution rights apply here. Source: https://packages.ubuntu.com/noble/amd64/libjs-mathjax/filelist; file-list quote: “/usr/share/javascript/mathjax/MathJax.js; /usr/share/javascript/mathjax/config/AM_CHTML-full.js”.
- mint-a282c662d65102e813baff88, liblangtag-common: MUST. Removing tag definitions removes recognition of supported language identifiers across dependent programs. Source: https://packages.ubuntu.com/noble/amd64/liblangtag-common/filelist; file-list quote: “/usr/share/liblangtag/common/bcp47/calendar.xml; /usr/share/liblangtag/common/bcp47/collation.xml”.
- mint-d91138aecb724ed87b5a3f1d, liblouis-data: MUST. Removing translation tables prevents the supported braille conversions. Source: https://packages.ubuntu.com/noble/amd64/liblouis-data/filelist; file-list quote: “/usr/share/liblouis/tables/Es-Es-G0.utb; /usr/share/liblouis/tables/IPA-unicode-range.uti”.
- mint-82b76eb7cd94a92667d29af3, liblouisutdml-data: MUST. Removing semantics and translation definitions prevents supported document-to-braille conversions. Source: https://packages.ubuntu.com/noble/amd64/liblouisutdml-data/filelist; file-list quote: “/usr/share/liblouisutdml/lbu_files/ThML.sem; /usr/share/liblouisutdml/lbu_files/Workbook.sem”.
- mint-d08abb4b5a6de9256af74302, libmagic-mgc: MUST. Removing signature rules removes file-type recognition across programs; they are operational rules rather than a speed-only cache. Source: https://packages.ubuntu.com/noble/amd64/libmagic-mgc/filelist; file-list quote: “/usr/lib/file/magic.mgc; /usr/share/file/magic.mgc”.
- mint-b47c33a97bcc8cb6c0f83166, libmateweather-common: HOLE. Weather locations can be read as exempt database content or capability-defining data; the text does not distinguish them. Source: https://packages.ubuntu.com/noble/amd64/libmateweather-common/filelist; file-list quote: “/usr/share/glib-2.0/schemas/org.mate.weather.gschema.xml; /usr/share/icons/hicolor/16x16/status/weather-clear-night-000.png”.
- mint-1a0754df8cfbdeb1f7840808, libmtp-common: MUST. Its device rules and executable hook affect system access and run beyond one program’s interface. Source: https://packages.ubuntu.com/noble/amd64/libmtp-common/filelist; file-list quote: “/usr/lib/udev/hwdb.d/69-libmtp.hwdb; /usr/lib/udev/rules.d/69-libmtp.rules”.
- mint-0abdd0ecc4d167f671611a4a, libnma-common: MUST. Network authentication configuration is shared across users of the library, beyond one program. Source: https://packages.ubuntu.com/noble/amd64/libnma-common/filelist; file-list quote: “/usr/share/glib-2.0/schemas/org.gnome.nm-applet.eap.gschema.xml”.
- mint-30733059fb89dae7514595f5, libopenal-data: MUST. Audio configuration and profiles affect applications using the shared library; removal removes spatial-rendering capabilities. Source: https://packages.ubuntu.com/noble/amd64/libopenal-data/filelist; file-list quote: “/etc/openal/alsoft.conf; /usr/share/openal/alsoftrc.sample”.
- mint-aa0e81ea3d43187befdb7bb4, libpam-runtime: MUST. Authentication helpers are programs and their shared access rules govern system login. Source: https://packages.ubuntu.com/noble/amd64/libpam-runtime/filelist; file-list quote: “/etc/pam.conf; /etc/pam.d/other”.
- mint-d26ce339ea8777f96a700d2c, libpeas-common: NOT. Only image content becomes unavailable; the file list contains no executable plugin implementation. Source: https://packages.ubuntu.com/noble/amd64/libpeas-common/filelist; file-list quote: “/usr/share/icons/hicolor/16x16/actions/libpeas-plugin.png; /usr/share/icons/hicolor/22x22/actions/libpeas-plugin.png”.
- mint-b989bc66a213f8f3501280a8, libpkcs11-helper1t64: MUST. The shared library executes with the calling program’s own rights. Source: https://packages.ubuntu.com/noble/amd64/libpkcs11-helper1t64/filelist; file-list quote: “/usr/lib/x86_64-linux-gnu/libpkcs11-helper.so.1; /usr/lib/x86_64-linux-gnu/libpkcs11-helper.so.1.0.0”.
- mint-52f095f05ca53fba848d19b8, libppd2-common: MUST. Removing headers and format definitions prevents supported printer-description compilation. Source: https://packages.ubuntu.com/noble/amd64/libppd2-common/filelist; file-list quote: “/usr/share/ppdc/epson.h; /usr/share/ppdc/font.defs”.
- mint-733875e389a687498d4e2634, libproxy1-plugin-gsettings: NOT. The transitional package contains no plugin implementation; removing it leaves the replacement implementation available. Source: https://packages.ubuntu.com/noble/amd64/libproxy1-plugin-gsettings/filelist; file-list quote: “/usr/share/doc/libproxy1-plugin-gsettings/changelog.Debian.gz; /usr/share/doc/libproxy1-plugin-gsettings/copyright”.
- mint-532486c3efcfce3b07649c2f, libproxy1-plugin-networkmanager: NOT. The transitional package contains no plugin implementation; removing it leaves the replacement implementation available. Source: https://packages.ubuntu.com/noble/amd64/libproxy1-plugin-networkmanager/filelist; file-list quote: “/usr/share/doc/libproxy1-plugin-networkmanager/changelog.Debian.gz; /usr/share/doc/libproxy1-plugin-networkmanager/copyright”.
- mint-faf613bbc932d574906aa6db, libpwquality-common: MUST. The policy configures shared authentication facilities rather than settings confined to one program. Source: https://packages.ubuntu.com/noble/amd64/libpwquality-common/filelist; file-list quote: “/etc/security/pwquality.conf; /usr/share/man/man5/pwquality.conf.5.gz”.
- mint-d0cf3bfc0f782be651893767, libpython3-stdlib: NOT. This dependency package contains no standard-library implementation; removing it leaves separately packaged library code available. Source: https://packages.ubuntu.com/noble/amd64/libpython3-stdlib/filelist; file-list quote: “/usr/share/doc/libpython3-stdlib/README.Debian; /usr/share/doc/libpython3-stdlib/changelog.Debian.gz”.
- mint-76e392db70d39d833ae72908, librda-common: NOT. The translated message content disappears; executable remote-desktop functions remain. Source: https://packages.ubuntu.com/noble/amd64/librda-common/filelist; file-list quote: “/usr/share/locale/af/LC_MESSAGES/librda.mo; /usr/share/locale/am/LC_MESSAGES/librda.mo”.
- mint-e3bcf64cf309bedddb22d4fd, libreoffice-common: MUST. The package includes executable launchers and scripts required to start and operate the suite. Source: https://packages.ubuntu.com/noble/amd64/libreoffice-common/filelist; file-list quote: “/etc/apparmor.d/usr.lib.libreoffice.program.oosplash; /etc/apparmor.d/usr.lib.libreoffice.program.senddoc”.
- mint-2f6aa703da9fafd44daec271, libreoffice-help-common: NOT. Help content and its browser-interface scripts are explicitly exempt. Source: https://packages.ubuntu.com/noble/amd64/libreoffice-help-common/filelist; file-list quote: “/usr/lib/libreoffice/share/config/images_helpimg.zip; /usr/share/bug/libreoffice-help-common/presubj”.
- mint-bb5504062eb6b3dc716be62d, libreoffice-help-en-us: NOT. Help documents are content; navigation scripts remain within the browser interface. Source: https://packages.ubuntu.com/noble/amd64/libreoffice-help-en-us/filelist; file-list quote: “/usr/share/bug/libreoffice-help-en-us/presubj; /usr/share/libreoffice/help/en-US/bookmarks.js”.
- mint-17cfe851192ecea13111cb1a, libreoffice-style-colibre: NOT. Theme values affect only the office program’s interface and are expressly exempt. Source: https://packages.ubuntu.com/noble/amd64/libreoffice-style-colibre/filelist; file-list quote: “/usr/lib/libreoffice/share/config/images_colibre.zip; /usr/lib/libreoffice/share/config/images_colibre_dark.zip”.
- mint-f0792203cfac5c896f5acde5, libreoffice-uiconfig-calc: NOT. These interface values are settings confined to the office program; the explicit setting exemption applies. Source: https://packages.ubuntu.com/noble/amd64/libreoffice-uiconfig-calc/filelist; file-list quote: “/usr/lib/libreoffice/share/config/soffice.cfg/modules/scalc/menubar/menubar.xml; /usr/lib/libreoffice/share/config/soffice.cfg/modules/scalc/popupmenu/anchor.xml”.
- mint-488c9c6152f9a5f984d35271, libreoffice-uiconfig-common: NOT. These interface values are settings confined to the office program; the explicit setting exemption applies. Source: https://packages.ubuntu.com/noble/amd64/libreoffice-uiconfig-common/filelist; file-list quote: “/usr/lib/libreoffice/share/config/soffice.cfg/cui/ui/aboutconfigdialog.ui; /usr/lib/libreoffice/share/config/soffice.cfg/cui/ui/aboutdialog.ui”.
- mint-c09b84ff3052885b9e908970, libreoffice-uiconfig-draw: NOT. These interface values are settings confined to the office program; the explicit setting exemption applies. Source: https://packages.ubuntu.com/noble/amd64/libreoffice-uiconfig-draw/filelist; file-list quote: “/usr/lib/libreoffice/share/config/soffice.cfg/modules/sdraw/menubar/menubar.xml; /usr/lib/libreoffice/share/config/soffice.cfg/modules/sdraw/popupmenu/3dobject.xml”.
- mint-2f697d16e5c6412108030251, libreoffice-uiconfig-impress: NOT. These interface values are settings confined to the office program; the explicit setting exemption applies. Source: https://packages.ubuntu.com/noble/amd64/libreoffice-uiconfig-impress/filelist; file-list quote: “/usr/lib/libreoffice/share/config/soffice.cfg/modules/simpress/menubar/menubar.xml; /usr/lib/libreoffice/share/config/soffice.cfg/modules/simpress/popupmenu/3dobject.xml”.
- mint-f7c8cbe48c2d0e2049d5d92c, libreoffice-uiconfig-writer: NOT. These interface values are settings confined to the office program; the explicit setting exemption applies. Source: https://packages.ubuntu.com/noble/amd64/libreoffice-uiconfig-writer/filelist; file-list quote: “/usr/lib/libreoffice/share/config/soffice.cfg/modules/sweb/menubar/menubar.xml; /usr/lib/libreoffice/share/config/soffice.cfg/modules/sweb/popupmenu/anchor.xml”.
- mint-25cba3f3f64f39fb77d2d18d, librsvg2-common: MUST. The image-loader module executes with its calling program’s own rights. Source: https://packages.ubuntu.com/noble/amd64/librsvg2-common/filelist; file-list quote: “/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-svg.so; /usr/share/lintian/overrides/librsvg2-common”.
- mint-969c0d0a7ab22f765397a4fe, libsane-common: MUST. Backend selection and device settings govern scanning through multiple applications; removing them removes supported access. Source: https://packages.ubuntu.com/noble/amd64/libsane-common/filelist; file-list quote: “/etc/sane.d/abaton.conf; /etc/sane.d/agfafocus.conf”.
- mint-81531ef6d83130e53c064a6b, libsemanage-common: MUST. System access-policy settings affect multiple programs, beyond the one-program exemption. Source: https://packages.ubuntu.com/noble/amd64/libsemanage-common/filelist; file-list quote: “/etc/selinux/semanage.conf; /usr/share/man/man5/semanage.conf.5.gz”.
- mint-7e1d554495ea2538edd6bce3, libsensors-config: MUST. Sensor values are interpreted by multiple consumers of the shared library, beyond one program. Source: https://packages.ubuntu.com/noble/amd64/libsensors-config/filelist; file-list quote: “/etc/sensors.d/.placeholder; /etc/sensors3.conf”.
- mint-c5095a8e093bb7ef63c31a8d, libsnmp-base: MUST. Removing these definitions removes management and code-generation capabilities across the tool suite. Source: https://packages.ubuntu.com/noble/amd64/libsnmp-base/filelist; file-list quote: “/etc/snmp/snmp.conf; /usr/share/man/man5/mib2c.conf.5.gz”.
- mint-f3a27734d1c9e9356a0e2c91, libsource-highlight-common: NOT. Grammar and style values configure highlighting inside the program; the setting exemption applies. Source: https://packages.ubuntu.com/noble/amd64/libsource-highlight-common/filelist; file-list quote: “/usr/share/source-highlight/Hello.css; /usr/share/source-highlight/Hello2.css”.
- mint-bdf8f6d772ec2e8c8641b3ee, libstdc++-13-dev: MUST. Removing these development objects prevents supported compilation and linking. Source: https://packages.ubuntu.com/noble/amd64/libstdc++-13-dev/filelist; file-list quote: “/usr/include/c++/13/algorithm; /usr/include/c++/13/any”.
- mint-7588ce4f54fd792c9bd42dd5, libtag1v5: NOT. The package has no library implementation; removing it leaves the separately packaged implementation available. Source: https://packages.ubuntu.com/noble/amd64/libtag1v5/filelist; file-list quote: “/usr/share/doc/libtag1v5/README.bindings; /usr/share/doc/libtag1v5/changelog.Debian.gz”.
- mint-a5f5ff7e91db3d3684bcf0d8, libthai-data: MUST. Removing the dictionary removes language-specific word segmentation across dependent programs. Source: https://packages.ubuntu.com/noble/amd64/libthai-data/filelist; file-list quote: “/usr/share/libthai/thbrk.tri”.
- mint-29bb86e1f410b4e9273b2a6c, libtimezonemap-data: HOLE. Geographical entries can be exempt content or operational timezone-selection data; the text does not distinguish the readings. Source: https://packages.ubuntu.com/noble/amd64/libtimezonemap-data/filelist; file-list quote: “/usr/share/libtimezonemap/backward; /usr/share/libtimezonemap/ui/admin1Codes.txt”.
- mint-ef80a80feb7709633f6d40e4, libtirpc-common: MUST. Network transport definitions govern multiple RPC consumers; removal removes configured transport capabilities. Source: https://packages.ubuntu.com/noble/amd64/libtirpc-common/filelist; file-list quote: “/etc/netconfig; /usr/share/man/man5/netconfig.5.gz”.
- mint-f1de460c4c30e051eff71e46, libvte-2.91-common: MUST. Shell startup code and helper programs run with their executing programs’ rights. Source: https://packages.ubuntu.com/noble/amd64/libvte-2.91-common/filelist; file-list quote: “/etc/profile.d/vte-2.91.sh; /etc/profile.d/vte.csh”.

MathJax execution uncertainty is supported by https://docs.mathjax.org/en/v2.7/ : “MathJax on NodeJS” and “works in all modern browsers.” The installed inventory does not select the execution context. Interpreter initialization resources likewise do not establish their installed confinement mode merely by their presence.

HOLE rows concern the actual classification boundary for operational location databases; they do not ask how a system should transfer or preserve state. The text supplies no boundary between geographical database content and capability-defining lookup data.

## Per-package function quotations

- mint-eca934e83596f4d862beb0a3: https://packages.ubuntu.com/noble/libefiboot1t64 — “Library to manage UEFI variables”.
- mint-a3580006e5de28b40bb369e8: https://packages.ubuntu.com/noble/libefivar1t64 — “Library to manage UEFI variables”.
- mint-d661684c26d823f384bd7aea: https://packages.ubuntu.com/noble/libegl-mesa0 — “free implementation of the EGL API -- Mesa vendor library”.
- mint-132cc7706b2bb70d4bac7554: https://packages.ubuntu.com/noble/libegl1 — “Vendor neutral GL dispatch library -- EGL support”.
- mint-5228c6f6a563073d47a00ea6: https://packages.ubuntu.com/noble/libelf1t64 — “library to read and write ELF files”.
- mint-7fe359c43b744f41fb93e4fc: https://packages.ubuntu.com/noble/libenchant-2-2 — “Wrapper library for various spell checker engines (runtime libs)”.
- mint-d4216a85fb7f9121ee51272c: https://packages.ubuntu.com/noble/libencode-locale-perl — “utility to determine the locale encoding”.
- mint-4ed8b81ceaad03991b93adcc: https://packages.ubuntu.com/noble/libeot0 — “Library for parsing/converting Embedded OpenType files”.
- mint-737b24971bbdbd1fae379677: https://packages.ubuntu.com/noble/libepoxy0 — “OpenGL function pointer management library”.
- mint-5377ed57cfef914bdb0bd2c2: https://packages.ubuntu.com/noble/libepubgen-0.1-1 — “EPUB generator library”.
- mint-67b6cc759e512681a14a262d: https://packages.ubuntu.com/noble/libespeak-ng1 — “Multi-lingual software speech synthesizer: shared library”.
- mint-fb2b3a86911d2c9a8ed7ae78: https://packages.ubuntu.com/noble/libestr0 — “Helper functions for handling strings (lib)”.
- mint-8f252042fb027bc10d92ad99: https://packages.ubuntu.com/noble/libetonyek-0.1-1 — “library for reading and converting Apple Keynote presentations”.
- mint-c7bd0e0afcafabc41c201f8c: https://packages.ubuntu.com/noble/libevdev2 — “wrapper library for evdev devices”.
- mint-ca0ec4e2640f8fbb8dd03ee0: https://packages.ubuntu.com/noble/libevent-2.1-7t64 — “Asynchronous event notification library”.
- mint-994f3f736dd634b03c81e018: https://packages.ubuntu.com/noble/libexempi8 — “library to parse XMP metadata (Library)”.
- mint-e4530b3719815bf04babe84d: https://packages.ubuntu.com/noble/libexif12 — “library to parse EXIF files”.
- mint-85dc9cf21979c582a86c3053: https://packages.ubuntu.com/noble/libexiv2-27 — “EXIF/IPTC/XMP metadata manipulation library”.
- mint-96939ddcdbba6a647cba4eef: https://packages.ubuntu.com/noble/libexpat1 — “XML parsing C library - runtime library”.
- mint-3d5de8ef1639e3906873ed31: https://packages.ubuntu.com/noble/libext2fs2t64 — “ext2/ext3/ext4 file system libraries”.
- mint-c08b415c807b2eb08e4d3310: https://packages.ubuntu.com/noble/libexttextcat-2.0-0 — “Language detection library”.
- mint-e0fbe4b91d79b952736d5d49: https://packages.ubuntu.com/noble/libexttextcat-data — “Language detection library - data files”.
- mint-b7ae639746bf4427799617f7: https://packages.ubuntu.com/noble/libextutils-depends-perl — “Perl module for building extensions that depend on other extensions”.
- mint-7e54cbb38e27427bda4f1027: https://packages.ubuntu.com/noble/libfakeroot — “tool for simulating superuser privileges - shared libraries”.
- mint-f2a076a1fe2ac780c332507d: https://packages.ubuntu.com/noble/libfastjson4 — “fast json library for C”.
- mint-d8a23ec513fe0693732ec12b: https://packages.ubuntu.com/noble/libfcgi-perl — “helper module for FastCGI”.
- mint-66b6011ba4a51973f93be0ea: https://packages.ubuntu.com/noble/libfcgi0t64 — “shared library of FastCGI”.
- mint-f7cd793d33c7ff4033d06736: https://packages.ubuntu.com/noble/libfdisk1 — “fdisk partitioning library”.
- mint-f45896d03a66880bf38c01bc: https://packages.ubuntu.com/noble/libffi8 — “Foreign Function Interface library runtime”.
- mint-1160eeb7502dfda0ae6a01ba: https://packages.ubuntu.com/noble/libffmpegthumbnailer4v5 — “shared library for ffmpegthumbnailer”.
- mint-e04e43e3c6d80cc9d6f1049a: https://packages.ubuntu.com/noble/libfftw3-double3 — “Library for computing Fast Fourier Transforms - Double precision”.
- mint-2ce32403edb60b677dfd22fe: https://packages.ubuntu.com/noble/libfftw3-single3 — “Library for computing Fast Fourier Transforms - Single precision”.
- mint-be8b6cf91015bf4a3d06d84d: https://packages.ubuntu.com/noble/libfido2-1 — “library for generating and verifying FIDO 2.0 objects”.
- mint-5a4c477a8282805097fc5632: https://packages.ubuntu.com/noble/libfile-basedir-perl — “Perl module to use the freedesktop basedir specification”.
- mint-aed872e4910b52a36e0f22eb: https://packages.ubuntu.com/noble/libfile-desktopentry-perl — “Perl module to handle freedesktop .desktop files”.
- mint-5c3eb31a1c31f281675dc8e4: https://packages.ubuntu.com/noble/libfile-fcntllock-perl — “Perl module for file locking with fcntl(2)”.
- mint-49f501e7cfe7e252454cf0a4: https://packages.ubuntu.com/noble/libfile-listing-perl — “module to parse directory listings”.
- mint-8adc3768eba3e65114db6ac9: https://packages.ubuntu.com/noble/libfile-mimeinfo-perl — “Perl module to determine file types”.
- mint-ad2774df99c9afd78ac4fce9: https://packages.ubuntu.com/noble/libflac12t64 — “Free Lossless Audio Codec - runtime C library”.
- mint-16ea369c6e19f1a57259f320: https://packages.ubuntu.com/noble/libflashrom1 — “Identify, read, write, erase, and verify BIOS/ROM/flash chips - library”.
- mint-6fe29d6ec2d08d2b1ae0afbf: https://packages.ubuntu.com/noble/libflatpak0 — “Application deployment framework for desktop apps (library)”.
- mint-87520183ff798db3465fddb5: https://packages.ubuntu.com/noble/libflite1 — “Small run-time speech synthesis engine - shared libraries”.
- mint-c4935977c61d7a2f5191d2e8: https://packages.ubuntu.com/noble/libfont-afm-perl — “Perl interface to Adobe Font Metrics files”.
- mint-9ec737b74087da081298e25b: https://packages.ubuntu.com/noble/libfontconfig1 — “generic font configuration library - runtime”.
- mint-63b8892f6d9a78e73c4eb088: https://packages.ubuntu.com/noble/libfontenc1 — “X11 font encoding library”.
- mint-d1c0789fec15915336a7b40f: https://packages.ubuntu.com/noble/libfprint-2-2 — “async fingerprint library of fprint project, shared libraries”.
- mint-45c1782df723bbaa0e398e81: https://packages.ubuntu.com/noble/libfprint-2-tod1 — “async fingerprint library of fprint project, drivers shared libraries”.
- mint-1bb81b95deb55ec7b4ef0c93: https://packages.ubuntu.com/noble/libfreeaptx0 — “Free implementation of aptX”.
- mint-04ecaae7e92de290e12e4281: https://packages.ubuntu.com/noble/libfreehand-0.1-1 — “Library for parsing the FreeHand file format structure”.
- mint-78cb17010cee754e8ce85cdc: https://packages.ubuntu.com/noble/libfreetype6 — “FreeType 2 font engine, shared library files”.
- mint-86015c75190fb90c56e23f8a: https://packages.ubuntu.com/noble/libfribidi0 — “Free Implementation of the Unicode BiDi algorithm”.
- mint-aff1eb30afa9c6f50b44ab4f: https://packages.ubuntu.com/noble/libftdi1-2 — “C Library to control and program the FTDI USB controllers”.
- mint-ef3d7b1c81a6316bf1bbf18f: https://packages.ubuntu.com/noble/libfuse2t64 — “Filesystem in Userspace (library)”.
- mint-7304dd9b254afc490c31dd13: https://packages.ubuntu.com/noble/libfuse3-3 — “Filesystem in Userspace (library) (3.x version)”.
- mint-310d0a3cd09de10d6f9f3ffe: https://packages.ubuntu.com/noble/libfwupd2 — “Firmware update daemon library”.
- mint-07541f3b91f6ddacb729f214: https://packages.ubuntu.com/noble/libgail-3-0t64 — “GNOME Accessibility Implementation Library -- shared libraries”.
- mint-603a1832fe4275ab596e0a6e: https://packages.ubuntu.com/noble/libgail-common — “GNOME Accessibility Implementation Library -- common modules”.
- mint-de9721580c9cae9ba32f14e3: https://packages.ubuntu.com/noble/libgail18t64 — “GNOME Accessibility Implementation Library -- shared libraries”.
- mint-b97a5900cf5c3af0ae1d07c1: https://packages.ubuntu.com/noble/libgamemode0 — “Optimise Linux system performance on demand (host library)”.
- mint-83df1b53c79c5b725d3b101a: https://packages.ubuntu.com/noble/libgamemodeauto0 — “Optimise Linux system performance on demand (client library)”.
- mint-20875b358480c6f3bcda7bdd: https://packages.ubuntu.com/noble/libgbm1 — “generic buffer management API -- runtime”.
- mint-e28e81ee373ab8f897476e8e: https://packages.ubuntu.com/noble/libgcc-13-dev — “GCC support library (development files)”.
- mint-46233cf5e03e0c4e9152e692: https://packages.ubuntu.com/noble/libgcc-s1 — “GCC support library”.
- mint-183dbfa8e921df5c0dbd5661: https://packages.ubuntu.com/noble/libgck-1-0 — “Glib wrapper library for PKCS#11 - runtime”.
- mint-05921d1038c89daf26615bf9: https://packages.ubuntu.com/noble/libgck-2-2 — “Glib wrapper library for PKCS#11 - runtime”.
- mint-9fffd0b90b9d25c99bd8dac2: https://packages.ubuntu.com/noble/libgcr-4-4 — “Library for Crypto related tasks”.
- mint-cc49d2b92173f03511810c44: https://packages.ubuntu.com/noble/libgcr-base-3-1 — “Library for Crypto related tasks”.
- mint-c3f067534930a3d0ec48d842: https://packages.ubuntu.com/noble/libgcr-ui-3-1 — “Library for Crypto UI related tasks”.
- mint-6b0bbf67cc843dc9c20741aa: https://packages.ubuntu.com/noble/libgcrypt20 — “LGPL Crypto library - runtime library”.
- mint-0c21b46300ab4cba62ba6c68: https://packages.ubuntu.com/noble/libgd3 — “GD Graphics Library”.
- mint-1a7a9682ddc9b84d1b6a7c1c: https://packages.ubuntu.com/noble/libgdata-common — “Library for accessing GData webservices - common data files”.
- mint-9d2c5dccaa774420e7cdf82a: https://packages.ubuntu.com/noble/libgdata22 — “Library for accessing GData webservices - shared libraries”.
- mint-166e21ad9d01845741e3f356: https://packages.ubuntu.com/noble/libgdbm-compat4t64 — “GNU dbm database routines (legacy support runtime version) ”.
- mint-20c3a6dd2ca94224d2828338: https://packages.ubuntu.com/noble/libgdbm6t64 — “GNU dbm database routines (runtime version) ”.
- mint-7170ec9568f2b1815555de25: https://packages.ubuntu.com/noble/libgdk-pixbuf-2.0-0 — “GDK Pixbuf library”.
- mint-60df83a13018c5bb4adeafed: https://packages.ubuntu.com/noble/libgdk-pixbuf2.0-bin — “GDK Pixbuf library (thumbnailer)”.
- mint-b99d357e3028aca7e30a9360: https://packages.ubuntu.com/noble/libgdk-pixbuf2.0-common — “GDK Pixbuf library - data files”.
- mint-2855469bed65d1b358167383: https://packages.ubuntu.com/noble/libgee-0.8-2 — “GObject based collection and utility library”.
- mint-61467c590fe6c97fc37c0933: https://packages.ubuntu.com/noble/libgeoclue-2-0 — “convenience library to interact with geoinformation service”.
- mint-3e1ba2bf03626c130f386976: https://packages.ubuntu.com/noble/libgeocode-glib-2-0 — “geocoding and reverse geocoding GLib library using Nominatim”.
- mint-99bae2280dff6d3aa4214254: https://packages.ubuntu.com/noble/libgexiv2-2 — “GObject-based wrapper around the Exiv2 library”.
- mint-ac1aa474350dca06dfc87902: https://packages.ubuntu.com/noble/libgfortran5 — “Runtime library for GNU Fortran applications”.
- mint-c7a6a17bdece834cbad57bc7: https://packages.ubuntu.com/noble/libgif7 — “library for GIF images (library)”.
- mint-873875a33f1a0a1bb52ade5a: https://packages.ubuntu.com/noble/libgirepository-1.0-1 — “Library for handling GObject introspection data (runtime library)”.
- mint-5b6f2e03f98b3c105d2c33a1: https://packages.ubuntu.com/noble/libgl1 — “Vendor neutral GL dispatch library -- legacy GL support”.
- mint-3ede1ab866c6316bdf1fa1f5: https://packages.ubuntu.com/noble/libgl1-mesa-dri — “free implementation of the OpenGL API -- DRI modules”.
- mint-dc37532e4f8cb7bc095b0d32: https://packages.ubuntu.com/noble/libglapi-mesa — “free implementation of the GL API -- shared library”.
- mint-8707cc3a010c96bb64419a11: https://packages.ubuntu.com/noble/libgles2 — “Vendor neutral GL dispatch library -- GLESv2 support”.
- mint-66832badba472bd5821487a7: https://packages.ubuntu.com/noble/libglib-object-introspection-perl — “Perl bindings for gobject-introspection libraries”.
- mint-2c54c71bb31debd192cf71e8: https://packages.ubuntu.com/noble/libglib-perl — “interface to the GLib and GObject libraries”.
- mint-dc982e357b6400afb4b89936: https://packages.ubuntu.com/noble/libglib2.0-0t64 — “GLib library of C routines”.
- mint-b4b91ddb3d50caead34eed13: https://packages.ubuntu.com/noble/libglib2.0-bin — “Programs for the GLib library”.
- mint-3d51ab53721bee678bb4af10: https://packages.ubuntu.com/noble/libglib2.0-data — “Common files for GLib library”.
- mint-c13462589beed73c8bd4f6fd: https://packages.ubuntu.com/noble/libglibmm-2.4-1t64 — “C++ wrapper for the GLib toolkit (shared libraries)”.
- mint-35e92f38fb76519ba0f3dcc8: https://packages.ubuntu.com/noble/libglibmm-2.68-1t64 — “C++ wrapper for the GLib toolkit (shared libraries)”.
- mint-83fb8dc73a88eb7e93f91811: https://packages.ubuntu.com/noble/libglu1-mesa — “Mesa OpenGL utility library (GLU)”.
- mint-0082544be1931dac6ea6a1ba: https://packages.ubuntu.com/noble/libglvnd0 — “Vendor neutral GL dispatch library”.
- mint-7c59d0fb28c8eb5147a1fbef: https://packages.ubuntu.com/noble/libglx-mesa0 — “free implementation of the OpenGL API -- GLX vendor library”.
- mint-9001ef1d9d52a8e4e5f23484: https://packages.ubuntu.com/noble/libglx0 — “Vendor neutral GL dispatch library -- GLX support”.
- mint-4c9e086d609a6dcc5de3cb49: https://packages.ubuntu.com/noble/libgme0 — “Playback library for video game music files - shared library”.
- mint-c1436c994dce656fbad22509: https://packages.ubuntu.com/noble/libgmp10 — “Multiprecision arithmetic library”.
- mint-d3de492adc0d57c847132c3d: https://packages.ubuntu.com/noble/libgnome-desktop-3-20t64 — “Utility library for the GNOME desktop - GTK 3 version”.
- mint-a37141575c574866e1e94e2b: https://packages.ubuntu.com/noble/libgnomekbd-common — “GNOME library to manage keyboard configuration - common files”.
- mint-820731b605d795163a865296: https://packages.ubuntu.com/noble/libgnomekbd8 — “GNOME library to manage keyboard configuration - shared library”.
- mint-174b73735c614d2cbdcc5184: https://packages.ubuntu.com/noble/libgnutls30t64 — “GNU TLS library - main runtime library”.
- mint-d5c1f430700a0f69bcd67c37: https://packages.ubuntu.com/noble/libgoa-1.0-0b — “library for GNOME Online Accounts”.
- mint-3023b2a226683cd1db5915c2: https://packages.ubuntu.com/noble/libgoa-1.0-common — “library for GNOME Online Accounts - common files”.
- mint-13201b063f933b889fbae35f: https://packages.ubuntu.com/noble/libgoa-backend-1.0-2 — “backend library for GNOME Online Accounts”.
- mint-eddbe0e9a6f634a78696fc96: https://packages.ubuntu.com/noble/libgomp1 — “GCC OpenMP (GOMP) support library”.
- mint-b94e695372565a1a5902b709: https://packages.ubuntu.com/noble/libgpg-error0 — “GnuPG development runtime library”.
- mint-a0d69fe48043258ab0fe5e80: https://packages.ubuntu.com/noble/libgpgme11t64 — “GPGME - GnuPG Made Easy (library)”.
- mint-0f9fd98c1a3c52e8c9cd4e54: https://packages.ubuntu.com/noble/libgpgmepp6t64 — “C++ wrapper library for GPGME”.
- mint-9ec29c2aee46f54e08018816: https://packages.ubuntu.com/noble/libgphoto2-6t64 — “gphoto2 digital camera library”.
- mint-b484766ba233d05426f4a3e9: https://packages.ubuntu.com/noble/libgphoto2-l10n — “gphoto2 digital camera library - localized messages”.
- mint-a4adb9f0451827aade1f9fc5: https://packages.ubuntu.com/noble/libgphoto2-port12t64 — “gphoto2 digital camera port library”.
- mint-3ac91cfad22dd3dc0a6d4123: https://packages.ubuntu.com/noble/libgpm2 — “General Purpose Mouse - shared library”.
- mint-c4dca01c9777ac62eee5fe6d: https://packages.ubuntu.com/noble/libgpod-common — “common files for libgpod”.
- mint-a337a7639a5ef0f5ee35009b: https://packages.ubuntu.com/noble/libgpod4t64 — “library to read and write songs and artwork to an iPod”.
- mint-62c687385fe2b41c2cfb651d: https://packages.ubuntu.com/noble/libgprofng0 — “GNU Next Generation profiler (runtime library)”.
- mint-878da04640490ece2f2faefa: https://packages.ubuntu.com/noble/libgraphene-1.0-0 — “library of graphic data types”.
- mint-d2251826215d1b2d116b1c09: https://packages.ubuntu.com/noble/libgraphite2-3 — “Font rendering engine for Complex Scripts -- library”.
- mint-d5582cf3f796efacae8d6954: https://packages.ubuntu.com/noble/libgrilo-0.3-0 — “Framework for discovering and browsing media - Shared libraries”.
- mint-a453e15cdf70a904a6d2812d: https://packages.ubuntu.com/noble/libgs-common — “interpreter for the PostScript language and for PDF - ICC profiles”.
- mint-a45246537561af70202f912f: https://packages.ubuntu.com/noble/libgs10 — “interpreter for the PostScript language and for PDF - Library”.
- mint-f03630dc00f470e339f74873: https://packages.ubuntu.com/noble/libgs10-common — “interpreter for the PostScript language and for PDF - common files”.
- mint-94041c0492e00805761952ef: https://packages.ubuntu.com/noble/libgsf-1-114 — “Structured File Library - runtime version”.
- mint-1b6205004ca33a384f976275: https://packages.ubuntu.com/noble/libgsf-1-common — “Structured File Library - common files”.
- mint-c5d4027fb2db22819395c898: https://packages.ubuntu.com/noble/libgsf-bin — “Structured File Library - programs”.
- mint-b809e3e90ec18155e101b583: https://packages.ubuntu.com/noble/libgsm1 — “Shared libraries for GSM speech compressor”.
- mint-a8aaa3b6e087af0d3ada0d69: https://packages.ubuntu.com/noble/libgsound0t64 — “small library for playing system sounds”.
- mint-3020256d943a511d8d381830: https://packages.ubuntu.com/noble/libgspell-1-2 — “spell-checking library for GTK+ applications”.
- mint-18d86df0f59caec6aaf212e2: https://packages.ubuntu.com/noble/libgspell-1-common — “libgspell architecture-independent files”.
- mint-3dbe94f53d02e40f1c866ae1: https://packages.ubuntu.com/noble/libgssapi-krb5-2 — “MIT Kerberos runtime libraries - krb5 GSS-API Mechanism”.
- mint-d2fd8055df12740634b57a59: https://packages.ubuntu.com/noble/libgstreamer-gl1.0-0 — “GStreamer GL libraries”.
- mint-995746a182909d8463137eef: https://packages.ubuntu.com/noble/libgstreamer-plugins-base1.0-0 — “GStreamer libraries from the "base" set”.
- mint-ff1ed548198957ef2e795371: https://packages.ubuntu.com/noble/libgstreamer-plugins-good1.0-0 — “GStreamer development files for libraries from the "good" set”.
- mint-3b5cba6cabe151e5d4747661: https://packages.ubuntu.com/noble/libgstreamer1.0-0 — “Core GStreamer libraries and elements”.
- mint-d4fffe320fc58d39634f76ac: https://packages.ubuntu.com/noble/libgtk-3-0t64 — “GTK graphical user interface library”.
- mint-b71d22a2c5e0f9fa974aea9e: https://packages.ubuntu.com/noble/libgtk-3-bin — “programs for the GTK graphical user interface library”.
- mint-b072fe21a5941e5b70717d4e: https://packages.ubuntu.com/noble/libgtk-3-common — “common files for the GTK graphical user interface library”.
- mint-63d1ffd9e93fced619a43681: https://packages.ubuntu.com/noble/libgtk-4-1 — “GTK graphical user interface library”.
- mint-7f2adcdd0c00a776b9a34c94: https://packages.ubuntu.com/noble/libgtk-4-common — “common files for the GTK graphical user interface library”.
- mint-5410f469d9d3ece1d9c4b918: https://packages.ubuntu.com/noble/libgtk-layer-shell0 — “Wayland Layer Shell protocol desktop component library”.
- mint-8e169b6261f3869ca604e24d: https://packages.ubuntu.com/noble/libgtk2.0-0t64 — “GTK graphical user interface library - old version”.
- mint-f4f144611089d4ac217ef330: https://packages.ubuntu.com/noble/libgtk2.0-bin — “programs for the GTK graphical user interface library”.
- mint-7e6749af2823cec1035a835c: https://packages.ubuntu.com/noble/libgtk2.0-common — “common files for the GTK graphical user interface library”.
- mint-d6a5252dd06ccb3790962c3a: https://packages.ubuntu.com/noble/libgtk3-perl — “Perl bindings for the GTK+ graphical user interface library”.
- mint-7bb705bd14867baeeb2d0108: https://packages.ubuntu.com/noble/libgtkmm-3.0-1t64 — “C++ wrappers for GTK+ (shared libraries)”.
- mint-5176d72898ca181f8e2476f2: https://packages.ubuntu.com/noble/libgtkmm-4.0-0 — “C++ wrappers for GTK4 (shared libraries)”.
- mint-a863f1cffd728707812b8e8f: https://packages.ubuntu.com/noble/libgtksourceview-3.0-1 — “shared libraries for the GTK+ syntax highlighting widget”.
- mint-46b5afb6397df38a0f147efa: https://packages.ubuntu.com/noble/libgtksourceview-3.0-common — “common files for the GTK+ syntax highlighting widget”.
- mint-f6093bdc4479ead6d5ed6283: https://packages.ubuntu.com/noble/libgtksourceview-4-0 — “shared libraries for the GTK+ syntax highlighting widget”.
- mint-49cb633f87d41791fab91e45: https://packages.ubuntu.com/noble/libgtksourceview-4-common — “common files for the GTK+ syntax highlighting widget”.
- mint-f01335af188b182884d423cc: https://packages.ubuntu.com/noble/libgtop-2.0-11 — “gtop system monitoring library (shared)”.
- mint-45bddac5da5b1c0ea8eeda3b: https://packages.ubuntu.com/noble/libgtop2-common — “gtop system monitoring library (common)”.
- mint-7aa4c59ec718540c4a92c0c1: https://packages.ubuntu.com/noble/libgucharmap-2-90-7 — “Unicode browser widget library (shared library)”.
- mint-bd26a25aed7c9d7280e4c69d: https://packages.ubuntu.com/noble/libgudev-1.0-0 — “GObject-based wrapper library for libudev”.
- mint-6d46ad96ad1a8c7d10c6bf20: https://packages.ubuntu.com/noble/libgusb2 — “GLib wrapper around libusb1”.
- mint-8da217ac5f3e7316e94fc8d7: https://packages.ubuntu.com/noble/libgutenprint-common — “support files for the Gutenprint printer driver library”.
- mint-6316b93f1e4b35d7f88c7bc8: https://packages.ubuntu.com/noble/libgutenprint9 — “runtime for the Gutenprint printer driver library”.
- mint-e47c1078329c6a5b2ed38ac3: https://packages.ubuntu.com/noble/libgweather-4-0t64 — “GWeather shared library”.
- mint-42af36e99ac3c7f718a68789: https://packages.ubuntu.com/noble/libgweather-4-common — “GWeather common files”.
- mint-e1beb866ebbbd3970153bd42: https://packages.ubuntu.com/noble/libgxps2t64 — “handling and rendering XPS documents (library)”.
- mint-8a02e709116805673c953672: https://packages.ubuntu.com/noble/libhandy-1-0 — “Library with GTK widgets for mobile phones”.
- mint-d7f85a255526d0cea77446d8: https://packages.ubuntu.com/noble/libharfbuzz-gobject0 — “OpenType text shaping engine ICU backend (GObject library)”.
- mint-9abc64f3d705308ff8f1009d: https://packages.ubuntu.com/noble/libharfbuzz-icu0 — “OpenType text shaping engine ICU backend”.
- mint-e7a6f09480a8833751f15f6f: https://packages.ubuntu.com/noble/libharfbuzz0b — “OpenType text shaping engine (shared library)”.
- mint-92449971c0f42c7a032e2ad0: https://packages.ubuntu.com/noble/libheif-plugin-aomdec — “ISO/IEC 23008-12:2017 HEIF file format decoder - aomdec plugin”.
- mint-447679a870980290c648d50a: https://packages.ubuntu.com/noble/libheif-plugin-libde265 — “ISO/IEC 23008-12:2017 HEIF file format decoder - libde265 plugin”.
- mint-8929cb723198fc635ddd14d1: https://packages.ubuntu.com/noble/libheif1 — “ISO/IEC 23008-12:2017 HEIF file format decoder - shared library”.
- mint-80b2b73afd661ab67f785c9d: https://packages.ubuntu.com/noble/libhogweed6t64 — “low level cryptographic library (public-key cryptos)”.
- mint-ba6d6a3026d90c1277d6c3a9: https://packages.ubuntu.com/noble/libhpmud0 — “HP Multi-Point Transport Driver (hpmud) run-time libraries”.
- mint-82633dca0996a30cdd461227: https://packages.ubuntu.com/noble/libhtml-form-perl — “module that represents an HTML form element”.
- mint-07f0a4a3a86c7f5dd0f54f29: https://packages.ubuntu.com/noble/libhtml-format-perl — “module for transforming HTML into various formats”.
- mint-8ca88d7a39bdb0e942483697: https://packages.ubuntu.com/noble/libhtml-parser-perl — “collection of modules that parse HTML text documents”.
- mint-4c012665c72203edb1c59ed6: https://packages.ubuntu.com/noble/libhtml-tagset-perl — “data tables pertaining to HTML”.
- mint-b19b492128d29fe52de7cedf: https://packages.ubuntu.com/noble/libhtml-tree-perl — “Perl module to represent and create HTML syntax trees”.
- mint-ea4f1a66388e5af28e0121e1: https://packages.ubuntu.com/noble/libhttp-cookies-perl — “HTTP cookie jars”.
- mint-88be8ddbc2a99d420d5f3524: https://packages.ubuntu.com/noble/libhttp-daemon-perl — “simple http server class”.
- mint-1808089e3c88e91c0a910d7f: https://packages.ubuntu.com/noble/libhttp-date-perl — “module of date conversion routines”.
- mint-874be7ef9d4173e78d5844c3: https://packages.ubuntu.com/noble/libhttp-message-perl — “perl interface to HTTP style messages”.
- mint-81ed493fce9c3a68bf27595b: https://packages.ubuntu.com/noble/libhttp-negotiate-perl — “implementation of content negotiation”.
- mint-37a7439630a110f0236ef403: https://packages.ubuntu.com/noble/libhunspell-1.7-0 — “spell checker and morphological analyzer (shared library)”.
- mint-f6cb1c9818b10f15296df4ae: https://packages.ubuntu.com/noble/libhwasan0 — “AddressSanitizer -- a fast memory error detector”.
- mint-97c5486cec105a00e80891bb: https://packages.ubuntu.com/noble/libhwy1t64 — “Efficient and performance-portable SIMD wrapper (runtime files)”.
- mint-ca8de94a1b1600ca3436a935: https://packages.ubuntu.com/noble/libhyphen0 — “ALTLinux hyphenation library - shared library”.
- mint-d58bf53bcfda0ea6dee2c743: https://packages.ubuntu.com/noble/libibus-1.0-5 — “Intelligent Input Bus - shared library”.
- mint-69540213faf620f00135fbce: https://packages.ubuntu.com/noble/libibverbs1 — “Library for direct userspace use of RDMA (InfiniBand/iWARP)”.
- mint-fa585afdb9c58920a83596fd: https://packages.ubuntu.com/noble/libical3t64 — “iCalendar library implementation in C (runtime)”.
- mint-58048f9c9d1c84b1d60c76af: https://packages.ubuntu.com/noble/libice6 — “X11 Inter-Client Exchange library”.
- mint-357cfa5b74c0fd02ce9cf2da: https://packages.ubuntu.com/noble/libicu74 — “International Components for Unicode”.
- mint-eb18943026362ac02c473d61: https://packages.ubuntu.com/noble/libidn12 — “GNU Libidn library, implementation of IETF IDN specifications”.
- mint-32318603adf6a93c34ae9a95: https://packages.ubuntu.com/noble/libidn2-0 — “Internationalized domain names (IDNA2008/TR46) library”.
- mint-20d074a0442046f798a31aef: https://packages.ubuntu.com/noble/libiec61883-0 — “partial implementation of IEC 61883 (shared lib)”.
- mint-1db7165eec0b534632624409: https://packages.ubuntu.com/noble/libieee1284-3t64 — “cross-platform library for parallel port access”.
- mint-171945c3031192cf9b1f5506: https://packages.ubuntu.com/noble/libigdgmm12 — “Intel Graphics Memory Management Library -- shared library”.
- mint-188dfe2a91644f8956e5faf9: https://packages.ubuntu.com/noble/libijs-0.35 — “IJS raster image transport protocol: shared library”.
- mint-457b64ed8bb94314ab8835b0: https://packages.ubuntu.com/noble/libimagequant0 — “palette quantization library”.
- mint-6252d283a3df0571f91f11a8: https://packages.ubuntu.com/noble/libimath-3-1-29t64 — “Utility libraries from ASF used by OpenEXR - runtime”.
- mint-8c847ebe1d9ec1bd20f74d0f: https://packages.ubuntu.com/noble/libimobiledevice-utils — “Utitilies for communicating with iPhone and other Apple devices”.
- mint-b2fb13a75e4ce6fc1cfc6454: https://packages.ubuntu.com/noble/libimobiledevice6 — “Library for communicating with iPhone and other Apple devices”.
- mint-66a36ad26f916d5749aa920d: https://packages.ubuntu.com/noble/libinih1 — “simple .INI file parser”.
- mint-8a2f27d9c1c911fdb92fa3fb: https://packages.ubuntu.com/noble/libinput-bin — “input device management and event handling library - udev quirks”.
- mint-571a1cc7b52244acb71be4d3: https://packages.ubuntu.com/noble/libinput10 — “input device management and event handling library - shared library”.
- mint-6eaebfbdcccfccaee848e986: https://packages.ubuntu.com/noble/libio-html-perl — “open an HTML file with automatic charset detection”.
- mint-9ed68bc0ec1bf64b70d6370a: https://packages.ubuntu.com/noble/libio-socket-ssl-perl — “Perl module implementing object oriented interface to SSL sockets”.
- mint-c72a90decdda8fda77f95528: https://packages.ubuntu.com/noble/libip4tc2 — “netfilter libip4tc library”.
- mint-12034b5eb515f515ee234f9f: https://packages.ubuntu.com/noble/libip6tc2 — “netfilter libip6tc library”.
- mint-dd75de689ce95b14b09833b3: https://packages.ubuntu.com/noble/libipc-system-simple-perl — “Perl module to run commands simply, with detailed diagnostics”.
- mint-4b35b74c7b6adb97f50a2f3e: https://packages.ubuntu.com/noble/libipt2 — “Intel Processor Trace Decoder Library”.
- mint-3554c85b80f6e3c225dd5d4a: https://packages.ubuntu.com/noble/libisl23 — “manipulating sets and relations of integer points bounded by linear constraints”.
- mint-0629a76391b1ca627431ba94: https://packages.ubuntu.com/noble/libisofs6t64 — “library to create ISO 9660 images”.
- mint-1c8ecb261e7c89df55bdd4c4: https://packages.ubuntu.com/noble/libitm1 — “GNU Transactional Memory Library”.
- mint-d12f60b5a5046320476cdca3: https://packages.ubuntu.com/noble/libiw30t64 — “Wireless tools - library”.
- mint-601c3823475203f9482cc95b: https://packages.ubuntu.com/noble/libjack-jackd2-0 — “JACK Audio Connection Kit (libraries)”.
- mint-37ae51307a189345ce64a866: https://packages.ubuntu.com/noble/libjansson4 — “C library for encoding, decoding and manipulating JSON data”.
- mint-e1c3ef40ee73950e8770ef62: https://packages.ubuntu.com/noble/libjavascriptcoregtk-4.1-0 — “JavaScript engine library from WebKitGTK”.
- mint-fdbdd37ada711cbee68327d5: https://packages.ubuntu.com/noble/libjavascriptcoregtk-6.0-1 — “JavaScript engine library from WebKitGTK”.
- mint-829815141b7fc4dc5970201d: https://packages.ubuntu.com/noble/libjbig0 — “JBIGkit libraries”.
- mint-63805265b0a0284075720bb2: https://packages.ubuntu.com/noble/libjbig2dec0 — “JBIG2 decoder library - shared libraries”.
- mint-ad1622132a15fd46c12e540a: https://packages.ubuntu.com/noble/libjcat1 — “JSON catalog library”.
- mint-5a77382df1239ed210339a5f: https://packages.ubuntu.com/noble/libjpeg-turbo8 — “libjpeg-turbo JPEG runtime library”.
- mint-bffd30fd970d239f8e671e3d: https://packages.ubuntu.com/noble/libjpeg8 — “Independent JPEG Group's JPEG runtime library (dependency package)”.
- mint-07398272b8b4d6e2452d1f7c: https://packages.ubuntu.com/noble/libjs-mathjax — “JavaScript display engine for LaTeX and MathML”.
- mint-251724e04271790652d9e793: https://packages.ubuntu.com/noble/libjson-c5 — “JSON manipulation library - shared library”.
- mint-8512750b97a4b2385a891334: https://packages.ubuntu.com/noble/libjson-glib-1.0-0 — “GLib JSON manipulation library”.
- mint-91cee78b097d42b2ce3643bd: https://packages.ubuntu.com/noble/libjson-glib-1.0-common — “GLib JSON manipulation library (common files)”.
- mint-65d864714e2c68fc8f692f53: https://packages.ubuntu.com/noble/libjxl-tools — “JPEG XL Image Coding System - "JXL" (command line utility)”.
- mint-2bf94ea0475eb23cf378811c: https://packages.ubuntu.com/noble/libjxl0.7 — “JPEG XL Image Coding System - "JXL" (shared libraries)”.
- mint-297490712ae744457e12b705: https://packages.ubuntu.com/noble/libk5crypto3 — “MIT Kerberos runtime libraries - Crypto Library”.
- mint-68c36c2f3f3068161b9bc135: https://packages.ubuntu.com/noble/libkeybinder-3.0-0 — “registers global key bindings for applications - Gtk+3”.
- mint-9cff017826d6d72265b1c616: https://packages.ubuntu.com/noble/libkeyutils1 — “Linux Key Management Utilities (library)”.
- mint-4616ec8b0cc3eb3071c1bc5d: https://packages.ubuntu.com/noble/libklibc — “minimal libc subset for use with initramfs”.
- mint-493f20c0d56f5b6556dd8104: https://packages.ubuntu.com/noble/libkmod2 — “libkmod shared library”.
- mint-0639cd04b33742397b62a0e2: https://packages.ubuntu.com/noble/libkpathsea6 — “TeX Live: path search library for TeX (runtime part)”.
- mint-5b117d1f3063d45725ca6f0c: https://packages.ubuntu.com/noble/libkrb5-3 — “MIT Kerberos runtime libraries”.
- mint-39ea67cf20efe6189fb55604: https://packages.ubuntu.com/noble/libkrb5support0 — “MIT Kerberos runtime libraries - Support library”.
- mint-683e09637f0394b87d5d5194: https://packages.ubuntu.com/noble/libksba8 — “X.509 and CMS support library”.
- mint-a282c662d65102e813baff88: https://packages.ubuntu.com/noble/liblangtag-common — “library to access tags for identifying languages -- data”.
- mint-ec77fa265353efe082e5676a: https://packages.ubuntu.com/noble/liblangtag1 — “library to access tags for identifying languages”.
- mint-e4fc5ab320c315fdb5327e97: https://packages.ubuntu.com/noble/liblapack3 — “Library of linear algebra routines 3 - shared version”.
- mint-f45fcc9a5ee8bf08ed97eaac: https://packages.ubuntu.com/noble/liblc3-1 — “Low Complexity Communication Codec (shared library)”.
- mint-a92aab4a900b49eb3a494d19: https://packages.ubuntu.com/noble/liblcms2-2 — “Little CMS 2 color management library”.
- mint-689927c041802fb13115b920: https://packages.ubuntu.com/noble/liblcms2-utils — “Little CMS 2 color management library (utilities)”.
- mint-baf228edf39222cb6f01dab8: https://packages.ubuntu.com/noble/libldacbt-abr2 — “LDAC Bluetooth ABR library (shared library)”.
- mint-92a0d75b20fd88b9afc20a79: https://packages.ubuntu.com/noble/libldacbt-enc2 — “LDAC Bluetooth encoder library (shared library)”.
- mint-c3d9dea0c0408bcb95f87809: https://packages.ubuntu.com/noble/libldap2 — “OpenLDAP libraries”.
- mint-f381720595bd5fdf1e51b4ef: https://packages.ubuntu.com/noble/libldb2 — “LDAP-like embedded database - shared library”.
- mint-26dfba72d3cad4775b8cc269: https://packages.ubuntu.com/noble/liblerc4 — “Limited Error Raster Compression library”.
- mint-93df7b64419253e4b8269294: https://packages.ubuntu.com/noble/liblightdm-gobject-1-0 — “LightDM GObject client library”.
- mint-d1f9d5892ba4b38c12596f2a: https://packages.ubuntu.com/noble/liblilv-0-0 — “library for simple use of LV2 plugins”.
- mint-9584283651ca860f89a6a068: https://packages.ubuntu.com/noble/liblirc-client0t64 — “infra-red remote control support - client library”.
- mint-84c03f79f13ae2de77d10430: https://packages.ubuntu.com/noble-updates/libllvm20 — “Modular compiler and toolchain technologies, runtime library”.
- mint-ec0e44e14d9762b6857d25b4: https://packages.ubuntu.com/noble/liblmdb0 — “Lightning Memory-Mapped Database shared library”.
- mint-3888578474ccc5a7a7f37976: https://packages.ubuntu.com/noble/liblocale-gettext-perl — “module using libc functions for internationalization in Perl”.
- mint-d91138aecb724ed87b5a3f1d: https://packages.ubuntu.com/noble/liblouis-data — “Braille translation library - data”.
- mint-53527ae2886cfb433eb2edc9: https://packages.ubuntu.com/noble/liblouis20 — “Braille translation library - shared libs”.
- mint-aabf4685386e95940b474978: https://packages.ubuntu.com/noble/liblouisutdml-bin — “Braille UTDML translation utilities”.
- mint-82b76eb7cd94a92667d29af3: https://packages.ubuntu.com/noble/liblouisutdml-data — “Braille UTDML translation library - data”.
- mint-032cf720038ed45e5c1a610b: https://packages.ubuntu.com/noble/liblouisutdml9t64 — “Braille UTDML translation library - shared libs”.
- mint-a1d89a9b68cc3918cdfaa051: https://packages.ubuntu.com/noble/liblsan0 — “LeakSanitizer -- a memory leak detector (runtime)”.
- mint-b7ec2256466f10aff447e5ba: https://packages.ubuntu.com/noble/libltdl7 — “System independent dlopen wrapper for GNU libtool”.
- mint-020d757dc024dd8731e71a77: https://packages.ubuntu.com/noble/liblua5.2-0 — “Shared library for the Lua interpreter version 5.2”.
- mint-798c08264f8172add12afd6a: https://packages.ubuntu.com/noble/liblua5.4-0 — “Shared library for the Lua interpreter version 5.4”.
- mint-7a3fe236ae1d629b5f84cfdd: https://packages.ubuntu.com/noble/liblvm2cmd2.03 — “LVM2 command library”.
- mint-f5f769a0898566458ac533e1: https://packages.ubuntu.com/noble/liblwp-mediatypes-perl — “module to guess media type for a file or a URL”.
- mint-26b758aacf1ac70d6aba54f2: https://packages.ubuntu.com/noble/liblwp-protocol-https-perl — “HTTPS driver for LWP::UserAgent”.
- mint-a2b62d060ede5a5eae6760c6: https://packages.ubuntu.com/noble/liblz4-1 — “Fast LZ compression algorithm library - runtime”.
- mint-3855bc8de6e4579a41cd9779: https://packages.ubuntu.com/noble/liblzma5 — “XZ-format compression library”.
- mint-32a35b2b5d5ec29c0f741a6a: https://packages.ubuntu.com/noble/liblzo2-2 — “data compression library”.
- mint-d08abb4b5a6de9256af74302: https://packages.ubuntu.com/noble/libmagic-mgc — “File type determination library using "magic" numbers (compiled magic file)”.
- mint-c2672f0c98a3e8e65bbe6152: https://packages.ubuntu.com/noble/libmagic1t64 — “Recognize the type of data in a file using "magic" numbers - library”.
- mint-bc28c31e88c969ce0328e657: https://packages.ubuntu.com/noble/libmalcontent-0-0 — “library for parental control of applications”.
- mint-01428ec1ae4cc8ec25cde72a: https://packages.ubuntu.com/noble/libmanette-0.2-0 — “Simple GObject game controller library”.
- mint-56ff6ee1169ba807eb8730f9: https://packages.ubuntu.com/noble/libmate-desktop-2-17t64 — “Library with common API for various MATE modules (library)”.
- mint-4fcf9f75ec88f8f1d42a8447: https://packages.ubuntu.com/noble/libmate-menu2 — “implementation of the freedesktop menu specification for MATE (library)”.
- mint-7b200a8322616c8e2777d2ee: https://packages.ubuntu.com/noble/libmate-panel-applet-4-1 — “library for MATE Panel applets”.
- mint-b47c33a97bcc8cb6c0f83166: https://packages.ubuntu.com/noble/libmateweather-common — “MateWeather shared library (common files)”.
- mint-11d436e5ac0ca8b54cbab709: https://packages.ubuntu.com/noble/libmateweather1t64 — “MateWeather shared library”.
- mint-6ea9d843d83025598606bcea: https://packages.ubuntu.com/noble/libmaxminddb0 — “IP geolocation database library”.
- mint-e21c3c1085ca41d4904ea235: https://packages.ubuntu.com/noble/libmbedcrypto7t64 — “lightweight crypto and SSL/TLS library - crypto library”.
- mint-7a76b7763a2eb8292999d7d1: https://packages.ubuntu.com/noble/libmbim-glib4 — “Support library to use the MBIM protocol”.
- mint-afc65ac44abc739197f16cf9: https://packages.ubuntu.com/noble/libmbim-proxy — “Proxy to communicate with MBIM ports”.
- mint-679456f9cf9198a826358775: https://packages.ubuntu.com/noble/libmd0 — “message digest functions from BSD systems - shared library”.
- mint-6c4b5cdb4bfd61a7255294f0: https://packages.ubuntu.com/noble/libmd4c0 — “Markdown for C”.
- mint-c563cd760bf135c62bad4a9f: https://packages.ubuntu.com/noble/libmetacity3 — “library for the Metacity window manager”.
- mint-5900ba7bba2b6416ba109ae0: https://packages.ubuntu.com/noble/libmhash2 — “Library for cryptographic hashing and message authentication”.
- mint-d6be1f10c49586c8c9df7a8f: https://packages.ubuntu.com/noble/libminiupnpc17 — “UPnP IGD client lightweight library”.
- mint-c5344678292255fe582fb6ae: https://packages.ubuntu.com/noble/libmm-glib0 — “D-Bus service for managing modems - shared libraries”.
- mint-bd5c259a64e9a9190d49b5ed: https://packages.ubuntu.com/noble/libmnl0 — “minimalistic Netlink communication library”.
- mint-82dc1aa91bcd1046bdfe431a: https://packages.ubuntu.com/noble/libmount1 — “device mounting library”.
- mint-6115acce0c75755b965b4f3e: https://packages.ubuntu.com/noble/libmozjs-115-0t64 — “SpiderMonkey JavaScript library”.
- mint-21baa94ff063d2b3458df708: https://packages.ubuntu.com/noble/libmp3lame0 — “MP3 encoding library”.
- mint-8d845a0a108ff39abfdb001a: https://packages.ubuntu.com/noble/libmpc3 — “multiple precision complex floating-point library”.
- mint-3a719a83127b9f97d06300ed: https://packages.ubuntu.com/noble/libmpfr6 — “multiple precision floating-point computation”.
- mint-7542a5d33cb473a613cb92a5: https://packages.ubuntu.com/noble/libmpg123-0t64 — “MPEG layer 1/2/3 audio decoder (shared library)”.
- mint-39e6385786e7ba3cadb2eedb: https://packages.ubuntu.com/noble/libmpv2 — “video player based on MPlayer/mplayer2 (client library)”.
- mint-2f360e4d1ef5c1b7bac88ed9: https://packages.ubuntu.com/noble/libmsgraph-0-1 — “library for accessing the Microsoft Graph API”.
- mint-1ad906e4ac328e9dcd7c77d4: https://packages.ubuntu.com/noble/libmspub-0.1-1 — “library for parsing the mspub file structure”.
- mint-06085030697713f3fb2179c5: https://packages.ubuntu.com/noble/libmtdev1t64 — “Multitouch Protocol Translation Library - shared library”.
- mint-1a0754df8cfbdeb1f7840808: https://packages.ubuntu.com/noble/libmtp-common — “Media Transfer Protocol (MTP) common files”.
- mint-4c695759c77f7b71645140bd: https://packages.ubuntu.com/noble/libmtp-runtime — “Media Transfer Protocol (MTP) runtime tools”.
- mint-d95a587fe05a94e58adc5cfb: https://packages.ubuntu.com/noble/libmtp9t64 — “Media Transfer Protocol (MTP) library”.
- mint-df51292bd765230816381683: https://raw.githubusercontent.com/linuxmint/muffin/master/debian/control — “window and compositing manager (shared library)”.
- mint-ce199f909931e3130d05f6ce: https://packages.ubuntu.com/noble/libmujs3 — “Lightweight JavaScript interpreter library”.
- mint-ea86e5758b66e87f68cca0bc: https://packages.ubuntu.com/noble/libmusicbrainz5-2 — “Library to access the MusicBrainz.org database (C wrapper functions)”.
- mint-6a7a2a0529d4a35c3cfca2cf: https://packages.ubuntu.com/noble/libmusicbrainz5cc2v5 — “Library to access the MusicBrainz.org database”.
- mint-448eeddc2d2baeadd07a9669: https://packages.ubuntu.com/noble/libmwaw-0.3-3 — “import library for some old Mac text documents”.
- mint-43362c7392ccaca1114115cf: https://packages.ubuntu.com/noble/libmysofa1 — “library to read HRTFs stored in the AES69-2015 SOFA format”.
- mint-0f34e57d491cf6717a9d196d: https://packages.ubuntu.com/noble/libmythes-1.2-0 — “simple thesaurus library”.
- mint-76a2e06075a4dcead088518d: https://packages.ubuntu.com/noble/libnatpmp1t64 — “portable and fully compliant implementation of NAT-PMP”.
- mint-4e75571462f4a5a43b09fe01: https://packages.ubuntu.com/noble/libnautilus-extension4 — “libraries for nautilus components - runtime version”.
- mint-be69d22dfba5e2a4329a81df: https://packages.ubuntu.com/noble/libncurses6 — “shared libraries for terminal handling”.
- mint-48fb104cfb9ac283f432c92a: https://packages.ubuntu.com/noble/libncursesw6 — “shared libraries for terminal handling (wide character support)”.
- mint-030ab82ffda8efb94b17a55a: https://packages.ubuntu.com/noble/libndp0 — “Library for Neighbor Discovery Protocol”.
- mint-f0c3be3d599e21da875324dd: https://packages.ubuntu.com/noble/libnemo-extension1 — “Nemo component system facilities”.
- mint-c777b3e0d7b0711dcb435e9d: https://packages.ubuntu.com/noble/libneon27t64-gnutls — “HTTP and WebDAV client library (GnuTLS enabled)”.
- mint-4d94910b4911072fcd628aec: https://packages.ubuntu.com/noble/libnet-dbus-perl — “Perl extension for the DBus bindings”.
- mint-7a5c3026b9da8afe21673b7a: https://packages.ubuntu.com/noble/libnet-http-perl — “module providing low-level HTTP connection client”.
- mint-9c5b2702543bb3cd09fbd186: https://packages.ubuntu.com/noble/libnet-libidn-perl — “Perl bindings for GNU Libidn”.
- mint-5a534899850183611b7792ae: https://packages.ubuntu.com/noble/libnet-ssleay-perl — “Perl module for Secure Sockets Layer (SSL)”.
- mint-cbc17c0ac42128f74895d3ed: https://packages.ubuntu.com/noble/libnetfilter-conntrack3 — “Netfilter netlink-conntrack library”.
- mint-a1d8fab252e1186a7a94df1e: https://packages.ubuntu.com/noble/libnetplan1 — “Declarative network configuration runtime library”.
- mint-b811fccd669d677f39c6c9c7: https://packages.ubuntu.com/noble/libnettle8t64 — “low level cryptographic library (symmetric and one-way cryptos)”.
- mint-6dc870074c36af28cd935af5: https://packages.ubuntu.com/noble/libnewt0.52 — “text mode windowing with slang”.
- mint-d6794c8b917a75af56918c8c: https://packages.ubuntu.com/noble/libnfnetlink0 — “Netfilter netlink library”.
- mint-4f2603edec7b0640298611af: https://packages.ubuntu.com/noble/libnfs14 — “NFS client library (shared library)”.
- mint-dc99cfca67e04dc9a463e60a: https://packages.ubuntu.com/noble/libnftables1 — “Netfilter nftables high level userspace API library”.
- mint-5c431045418c54deeded4b21: https://packages.ubuntu.com/noble/libnftnl11 — “Netfilter nftables userspace API library”.
- mint-008f9132e5bdf9904a6ea169: https://packages.ubuntu.com/noble/libnghttp2-14 — “library implementing HTTP/2 protocol (shared library)”.
- mint-d74f56f2a0a466c9f6c45743: https://packages.ubuntu.com/noble/libnl-3-200 — “library for dealing with netlink sockets”.
- mint-654ee0ce76d3c20042f6f9c0: https://packages.ubuntu.com/noble/libnl-genl-3-200 — “library for dealing with netlink sockets - generic netlink”.
- mint-b854b82721f32750f64a384f: https://packages.ubuntu.com/noble/libnl-route-3-200 — “library for dealing with netlink sockets - route interface”.
- mint-6fec576cd2533c892c042694: https://packages.ubuntu.com/noble/libnm0 — “GObject-based client library for NetworkManager”.
- mint-0abdd0ecc4d167f671611a4a: https://packages.ubuntu.com/noble/libnma-common — “NetworkManager GUI library - translations”.
- mint-02f1f4ad6ae6f3f3c8b2aff7: https://packages.ubuntu.com/noble/libnma-gtk4-0 — “NetworkManager GUI GTK4 library”.
- mint-aa48c9f8e0086b7c697e4000: https://packages.ubuntu.com/noble/libnma0 — “NetworkManager GUI library”.
- mint-322dd5d4ebd5d8a2e7eb7c5a: https://packages.ubuntu.com/noble/libnorm1t64 — “NACK-Oriented Reliable Multicast (NORM) library”.
- mint-9f5dc1d80382eae9fef304cd: https://packages.ubuntu.com/noble/libnotify-bin — “sends desktop notifications to a notification daemon (Utilities)”.
- mint-dffa303dcb97d2e6f9c82d8c: https://packages.ubuntu.com/noble/libnotify4 — “sends desktop notifications to a notification daemon”.
- mint-f07899fe21c6fbc0e94fcaa9: https://packages.ubuntu.com/noble/libnpth0t64 — “replacement for GNU Pth using system threads”.
- mint-859e5e8d981ba31836b9207e: https://packages.ubuntu.com/noble/libnspr4 — “NetScape Portable Runtime Library”.
- mint-63e879ba5ee8c49695c94ea9: https://packages.ubuntu.com/noble/libnss-mdns — “NSS module for Multicast DNS name resolution”.
- mint-3e0953fc8a356ef023ac8006: https://packages.ubuntu.com/noble/libnss-myhostname — “nss module providing fallback resolution for the current hostname”.
- mint-e161c421d5159f531ad448b5: https://packages.ubuntu.com/noble/libnss-systemd — “nss module providing dynamic user and group name resolution”.
- mint-50fa406764c8bfe7716b1f8a: https://packages.ubuntu.com/noble/libnss3 — “Network Security Service libraries”.
- mint-ea04caddfd5f3533173495ba: https://packages.ubuntu.com/noble/libntfs-3g89t64 — “read/write NTFS driver for FUSE (runtime library)”.
- mint-aba347c793f8465e8a6cb4bc: https://packages.ubuntu.com/noble/libnuma1 — “Libraries for controlling NUMA policy”.
- mint-c13d2ddd80a801407099cb60: https://packages.ubuntu.com/noble/libnvme1t64 — “NVMe management library (library)”.
- mint-705af05b3cc7379b8e4adae6: https://packages.ubuntu.com/noble/libodfgen-0.1-1 — “library to generate ODF documents”.
- mint-ee0fff993a334b2c1f3d8ac3: https://packages.ubuntu.com/noble/libogg0 — “Ogg bitstream library”.
- mint-30733059fb89dae7514595f5: https://packages.ubuntu.com/noble/libopenal-data — “Software implementation of the OpenAL audio API (data files)”.
- mint-f51a08c3ef112b24caafd88a: https://packages.ubuntu.com/noble/libopenal1 — “Software implementation of the OpenAL audio API (shared library)”.
- mint-2cafdd51c08be3bbe7329679: https://packages.ubuntu.com/noble/libopenexr-3-1-30 — “runtime files for the OpenEXR image library”.
- mint-d53340e53394251e4b8a5ed3: https://packages.ubuntu.com/noble/libopengl0 — “Vendor neutral GL dispatch library -- OpenGL support”.
- mint-a1770139aeeb28e0a5278e37: https://packages.ubuntu.com/noble/libopenjp2-7 — “JPEG 2000 image compression/decompression library”.
- mint-4236d691049c03832119e768: https://packages.ubuntu.com/noble/libopenmpt0t64 — “module music library based on OpenMPT -- shared library”.
- mint-35567007f5d02a1218dcabc1: https://packages.ubuntu.com/noble/libopus0 — “Opus codec runtime library”.
- mint-17d8368add1013e4028041d4: https://packages.ubuntu.com/noble/liborc-0.4-0t64 — “Library of Optimized Inner Loops Runtime Compiler”.
- mint-e82129880c36dd099009ea3d: https://packages.ubuntu.com/noble/liborcus-0.18-0 — “library for processing spreadsheet documents”.
- mint-644bd92766d752c7a63be3e6: https://packages.ubuntu.com/noble/liborcus-parser-0.18-0 — “library for processing spreadsheet documents - parser library”.
- mint-ab8065704b3b331a6c21034b: https://packages.ubuntu.com/noble/libostree-1-1 — “content-addressed filesystem for operating system binaries (library)”.
- mint-25e088fddf92f988adf7411a: https://packages.ubuntu.com/noble/libp11-kit0 — “library for loading and coordinating access to PKCS#11 modules - runtime”.
- mint-9c1ff1caf1e412e9560325e2: https://packages.ubuntu.com/noble/libpackagekit-glib2-18 — “Library for accessing PackageKit using GLib”.
- mint-7e624bb165a1f21c2d258cb9: https://packages.ubuntu.com/noble/libpagemaker-0.0-0 — “Library for importing and converting PageMaker Documents”.
- mint-077cc3f84053ff9b6f1dcdee: https://packages.ubuntu.com/noble/libpam-cap — “POSIX 1003.1e capabilities (PAM module)”.
- mint-ace650ef7d15cb498511d260: https://github.com/xapp-project/fingwit — “Fingwit uses two PAM modules:”.
- mint-68e0f1596556c0dc06370a31: https://packages.ubuntu.com/noble/libpam-fprintd — “PAM module for fingerprint authentication through fprintd”.
- mint-84d29be334f8d774d263a9c2: https://packages.ubuntu.com/noble/libpam-gnome-keyring — “PAM module to unlock the GNOME keyring upon login”.
- mint-96b512f632b1a357067ad984: https://packages.ubuntu.com/noble/libpam-modules — “Pluggable Authentication Modules for PAM”.
- mint-424a3e2205a2664bdf1e0ba0: https://packages.ubuntu.com/noble/libpam-modules-bin — “Pluggable Authentication Modules for PAM - helper binaries”.
- mint-aa0e81ea3d43187befdb7bb4: https://packages.ubuntu.com/noble/libpam-runtime — “Runtime support for the PAM library”.
- mint-b89417b62fb6dfde8881a62c: https://packages.ubuntu.com/noble/libpam-systemd — “system and service manager - PAM module”.
- mint-cfbdc29a0f396e2858a73509: https://packages.ubuntu.com/noble/libpam0g — “Pluggable Authentication Modules library”.
- mint-9d21fcc5b187c6f3c8c045f6: https://packages.ubuntu.com/noble/libpango-1.0-0 — “Layout and rendering of internationalized text”.
- mint-2c7fa490349c9646a30536bd: https://packages.ubuntu.com/noble/libpangocairo-1.0-0 — “Layout and rendering of internationalized text”.
- mint-b45dce10b5d02fcc97b9a005: https://packages.ubuntu.com/noble/libpangoft2-1.0-0 — “Layout and rendering of internationalized text”.
- mint-4c54b33f402962bafca966ef: https://packages.ubuntu.com/noble/libpangomm-1.4-1v5 — “C++ Wrapper for pango (shared libraries)”.
- mint-e2cb49b63209b01fd54a560e: https://packages.ubuntu.com/noble/libpangomm-2.48-1t64 — “C++ Wrapper for pango (shared libraries)”.
- mint-8d364a0afe256183b7542feb: https://packages.ubuntu.com/noble/libpangoxft-1.0-0 — “Layout and rendering of internationalized text”.
- mint-1388e5c7adfe16d4f9c04e1b: https://packages.ubuntu.com/noble/libpaper-utils — “library for handling paper characteristics (utilities)”.
- mint-f4a13b2d34ea8d8a0ebcd5b5: https://packages.ubuntu.com/noble/libpaper1 — “library for handling paper characteristics”.
- mint-c2cd2575da9057142c6c02c6: https://packages.ubuntu.com/noble/libparted2t64 — “disk partition manipulator - shared library”.
- mint-b50583656a9e8716ee472d1a: https://packages.ubuntu.com/noble/libpcap0.8t64 — “system interface for user-level packet capture”.
- mint-7339c134079cb09e87c994a9: https://packages.ubuntu.com/noble/libpcaudio0 — “C API to different audio devices - shared library”.
- mint-e148a2445bbbc75670391df1: https://packages.ubuntu.com/noble/libpci3 — “PCI utilities (shared library)”.
- mint-91a7c835966da583e7da26b0: https://packages.ubuntu.com/noble/libpciaccess0 — “Generic PCI access library for X”.
- mint-3e72faa102f2738ebf4fe506: https://packages.ubuntu.com/noble/libpcre2-16-0 — “New Perl Compatible Regular Expression Library - 16 bit runtime files”.
- mint-ed6789b21dde4e53d2099193: https://packages.ubuntu.com/noble/libpcre2-32-0 — “New Perl Compatible Regular Expression Library - 32 bit runtime files”.
- mint-3f615b6c99a1205183b7fb4d: https://packages.ubuntu.com/noble/libpcre2-8-0 — “New Perl Compatible Regular Expression Library- 8 bit runtime files”.
- mint-272ca2b2e7d4e9290f9f7cc4: https://packages.ubuntu.com/noble/libpcsclite1 — “Middleware to access a smart card using PC/SC (library)”.
- mint-550334f9e8e50982657972b8: https://packages.ubuntu.com/noble/libpeas-1.0-0 — “Application plugin library”.
- mint-d26ce339ea8777f96a700d2c: https://packages.ubuntu.com/noble/libpeas-common — “Application plugin library (common files)”.
- mint-e8e17a12ca9103842cf946ff: https://packages.ubuntu.com/noble/libperl5.38t64 — “shared Perl library”.
- mint-07bfd77b9b72fbfece1ee24d: https://packages.ubuntu.com/noble/libperlio-gzip-perl — “module providing a PerlIO layer to gzip/gunzip”.
- mint-4cf34e3d02dbeb5a2ae06c33: https://packages.ubuntu.com/noble/libpgm-5.3-0t64 — “OpenPGM shared library”.
- mint-cb31fb237799a021eb3ed976: https://packages.ubuntu.com/noble/libphonenumber8 — “parsing/formatting/validating phone numbers”.
- mint-4554990d2fc018ed7ff6ec86: https://packages.ubuntu.com/noble/libpipeline1 — “Unix process pipeline manipulation library”.
- mint-fb7d61c00e873b49a7c82c42: https://packages.ubuntu.com/noble/libpipewire-0.3-0t64 — “libraries for the PipeWire multimedia server”.
- mint-6ed13e629fe419561a6aeab0: https://packages.ubuntu.com/noble/libpipewire-0.3-modules — “libraries for the PipeWire multimedia server - modules”.
- mint-d9bf728a8e8010abb04b9bb9: https://packages.ubuntu.com/noble/libpixman-1-0 — “pixel-manipulation library for X and cairo”.
- mint-b989bc66a213f8f3501280a8: https://packages.ubuntu.com/noble/libpkcs11-helper1t64 — “library that simplifies the interaction with PKCS#11”.
- mint-5e3980b7fe483915962e8c88: https://packages.ubuntu.com/noble/libpkgconf3 — “shared library for pkgconf”.
- mint-cd77fe4619d6f827ae0a2e39: https://packages.ubuntu.com/noble/libplacebo338 — “GPU-accelerated video/image rendering primitives (shared library)”.
- mint-aacbf45a963382af169ff79c: https://packages.ubuntu.com/noble/libplist-2.0-4 — “Library for handling Apple binary and XML property lists”.
- mint-e8c8c1273a01b3e3610b5e81: https://packages.ubuntu.com/noble/libplymouth5 — “graphical boot animation and logger - shared libraries”.
- mint-93c245db7213450527814d58: https://packages.ubuntu.com/noble/libpng16-16t64 — “PNG library - runtime (version 1.6)”.
- mint-381cd864bb775ddbd8828556: https://packages.ubuntu.com/noble/libpocketsphinx3 — “Speech recognition tool - front-end library”.
- mint-47f79e53bf7ddfdb58364178: https://packages.ubuntu.com/noble/libpolkit-agent-1-0 — “polkit Authentication Agent API”.
- mint-beb3db2783cbb0f86dd97c23: https://packages.ubuntu.com/noble/libpolkit-gobject-1-0 — “polkit Authorization API”.
- mint-b15850b7f2f2086f6b720162: https://packages.ubuntu.com/noble/libpoppler-cpp0t64 — “PDF rendering library (CPP shared library)”.
- mint-7d1b937976c4c82dbf6e7f81: https://packages.ubuntu.com/noble/libpoppler-glib8t64 — “PDF rendering library (GLib-based shared library)”.
- mint-9e3c9bdc5dc8db60ad19f26a: https://packages.ubuntu.com/noble/libpoppler134 — “PDF rendering library”.
- mint-3991def5a13bcb38427c6f2f: https://packages.ubuntu.com/noble/libpopt0 — “lib for parsing cmdline parameters”.
- mint-b3cbc9d90751981501dfc8a1: https://packages.ubuntu.com/noble/libportaudio2 — “Portable audio I/O - shared library”.
- mint-519c6ed9c7449698571b2ce2: https://packages.ubuntu.com/noble/libpostproc57 — “FFmpeg library for post processing - runtime files”.
- mint-b5a6d83db15c7855ae3ac5e1: https://packages.ubuntu.com/noble/libppd2 — “OpenPrinting libppd - Shared library”.
- mint-52f095f05ca53fba848d19b8: https://packages.ubuntu.com/noble/libppd2-common — “OpenPrinting libppd - Auxiliary files”.
- mint-bf5a98d77e8c7005a34163de: https://packages.ubuntu.com/noble/libproc2-0 — “library for accessing process information from /proc”.
- mint-d77a076e0943da600a97c47d: https://packages.ubuntu.com/noble/libprotobuf-c1 — “Protocol Buffers C shared library (protobuf-c)”.
- mint-2cadd1d705a0e7967e1941d2: https://packages.ubuntu.com/noble/libprotobuf32t64 — “protocol buffers C++ library”.
- mint-733875e389a687498d4e2634: https://packages.ubuntu.com/noble/libproxy1-plugin-gsettings — “transitional package for libproxy GSettings plugin”.
- mint-532486c3efcfce3b07649c2f: https://packages.ubuntu.com/noble/libproxy1-plugin-networkmanager — “transitional package for libproxy NetworkManager plugin”.
- mint-ee5519186176b3d1dabbd63b: https://packages.ubuntu.com/noble/libproxy1v5 — “automatic proxy configuration management library (shared)”.
- mint-d50f48d92626e9ecd76840d3: https://packages.ubuntu.com/noble/libpsl5t64 — “Library for Public Suffix List (shared libraries)”.
- mint-6ae62969dfc62a2d79de62cf: https://packages.ubuntu.com/noble/libpugixml1v5 — “Light-weight C++ XML processing library”.
- mint-588ab066a2653ddaaa7fefe5: https://packages.ubuntu.com/noble/libpulse-mainloop-glib0 — “PulseAudio client libraries (glib support)”.
- mint-f8b817c374acda207d29745d: https://packages.ubuntu.com/noble/libpulse0 — “PulseAudio client libraries”.
- mint-faf613bbc932d574906aa6db: https://packages.ubuntu.com/noble/libpwquality-common — “library for password quality checking and generation (data files)”.
- mint-45f00b686f9f5b16c1c8c3ff: https://packages.ubuntu.com/noble/libpwquality1 — “library for password quality checking and generation”.
- mint-d0cf3bfc0f782be651893767: https://packages.ubuntu.com/noble/libpython3-stdlib — “interactive high-level object-oriented language (default python3 version)”.
- mint-3cddf7fd77c89451ea91b65c: https://packages.ubuntu.com/noble/libpython3.12-minimal — “Minimal subset of the Python language (version 3.12)”.
- mint-497e083a2dae8763c380735c: https://packages.ubuntu.com/noble/libpython3.12-stdlib — “Interactive high-level object-oriented language (standard library, version 3.12)”.
- mint-52e7b8ce86423a6e2125d60c: https://packages.ubuntu.com/noble/libpython3.12t64 — “Shared Python runtime library (version 3.12)”.
- mint-8d4ed0de6fa557f7a146e6da: https://packages.ubuntu.com/noble/libqmi-glib5 — “Support library to use the Qualcomm MSM Interface (QMI) protocol”.
- mint-da55e568b5f7f22a3f137b3c: https://packages.ubuntu.com/noble/libqmi-proxy — “Proxy to communicate with QMI ports”.
- mint-efbacfda9d1c1c7672f7901d: https://packages.ubuntu.com/noble/libqpdf29t64 — “runtime library for PDF transformation/inspection software”.
- mint-46d2171cc3950919cc1b752f: https://packages.ubuntu.com/noble/libqrtr-glib0 — “Support library to use the QRTR protocol”.
- mint-eb910b49dca53723f9bd65b2: https://packages.ubuntu.com/noble/libqt5core5t64 — “Qt 5 core module”.
- mint-71326e528a9c1fbcf5dcdf53: https://packages.ubuntu.com/noble/libqt5dbus5t64 — “Qt 5 D-Bus module”.
- mint-f1440c1f98a2b3e35cc739c6: https://packages.ubuntu.com/noble/libqt5gui5t64 — “Qt 5 GUI module”.
- mint-bb4011a7a0a4d24560287d28: https://packages.ubuntu.com/noble/libqt5network5t64 — “Qt 5 network module”.
- mint-afb9e74edb23338067fc954a: https://packages.ubuntu.com/noble/libqt5svg5 — “Qt 5 SVG module”.
- mint-e909a770346c7e950823061b: https://packages.ubuntu.com/noble/libqt5widgets5t64 — “Qt 5 widgets module”.
- mint-6031e90d50f2710cae0068b6: https://packages.ubuntu.com/noble/libquadmath0 — “GCC Quad-Precision Math Library”.
- mint-94541352e783272a7fbc90d4: https://packages.ubuntu.com/noble/librabbitmq4 — “AMQP client library written in C”.
- mint-61feed6c955b3704b43c5cc5: https://packages.ubuntu.com/noble/libraptor2-0 — “Raptor 2 RDF syntax library”.
- mint-99c5a7b06dbc8273974f3b30: https://packages.ubuntu.com/noble/libraqm0 — “Library for complex text layout”.
- mint-cf0921dcf0b038a10cf6f4b7: https://packages.ubuntu.com/noble/librasqal3t64 — “Rasqal RDF query library”.
- mint-cf5686b7ddddd63735b03e88: https://packages.ubuntu.com/noble/librav1e0 — “Fastest and safest AV1 encoder - shared library”.
- mint-f8346fbb7c9d18d6a6ce01e5: https://packages.ubuntu.com/noble/libraw1394-11 — “library for direct access to IEEE 1394 bus (aka FireWire)”.
- mint-a92ea68fc23f21e4d16cb968: https://packages.ubuntu.com/noble/libraw23t64 — “raw image decoder library”.
- mint-76e392db70d39d833ae72908: https://packages.ubuntu.com/noble/librda-common — “Remote Desktop Awareness (common files)”.
- mint-2aff7043722a8be6d9caf151: https://packages.ubuntu.com/noble/librda0 — “Remote Desktop Awareness (shared library)”.
- mint-faefc8eec11f14104e9c768b: https://packages.ubuntu.com/noble/librdf0t64 — “Redland Resource Description Framework (RDF) library”.
- mint-af4f9e1986fd7a33c52e0bec: https://packages.ubuntu.com/noble/libreadline8t64 — “GNU readline and history libraries, run-time libraries”.
- mint-3412cacb539927a303b49df8: https://packages.ubuntu.com/noble/libreiserfscore0t64 — “ReiserFS core library”.
- mint-5dbd0e22eb48a9fdcec6777b: https://packages.ubuntu.com/noble/libreoffice-base-core — “office productivity suite -- shared library”.
- mint-f2d38b07b8d37cb79ec25fd5: https://packages.ubuntu.com/noble/libreoffice-calc — “office productivity suite -- spreadsheet”.
- mint-e3bcf64cf309bedddb22d4fd: https://packages.ubuntu.com/noble/libreoffice-common — “office productivity suite -- arch-independent files”.
- mint-1a420a2eeb3dbc2c011ca0eb: https://packages.ubuntu.com/noble/libreoffice-core — “office productivity suite -- arch-dependent files”.
- mint-47a0da6634298243888e32cf: https://packages.ubuntu.com/noble/libreoffice-draw — “office productivity suite -- drawing”.
- mint-acb273c03159784933ff217f: https://packages.ubuntu.com/noble/libreoffice-gnome — “office productivity suite -- GNOME integration”.
- mint-7818ff3154f8cc1098de64b3: https://packages.ubuntu.com/noble/libreoffice-gtk3 — “office productivity suite -- GTK+ 3 integration”.
- mint-2f6aa703da9fafd44daec271: https://packages.ubuntu.com/noble/libreoffice-help-common — “office productivity suite -- common files for LibreOffice help”.
- mint-bb5504062eb6b3dc716be62d: https://packages.ubuntu.com/noble/libreoffice-help-en-us — “office productivity suite -- English_american help”.
- mint-413854f71d5ed74377a4f75e: https://packages.ubuntu.com/noble/libreoffice-impress — “office productivity suite -- presentation”.
- mint-17cfe851192ecea13111cb1a: https://packages.ubuntu.com/noble/libreoffice-style-colibre — “office productivity suite -- colibre symbol style”.
- mint-f0792203cfac5c896f5acde5: https://packages.ubuntu.com/noble/libreoffice-uiconfig-calc — “UI data ("config") for LibreOffice Calc”.
- mint-488c9c6152f9a5f984d35271: https://packages.ubuntu.com/noble/libreoffice-uiconfig-common — “UI data ("config") for LibreOffice ("common" set)”.
- mint-c09b84ff3052885b9e908970: https://packages.ubuntu.com/noble/libreoffice-uiconfig-draw — “UI data ("config") for LibreOffice Draw”.
- mint-2f697d16e5c6412108030251: https://packages.ubuntu.com/noble/libreoffice-uiconfig-impress — “UI data ("config") for LibreOffice Impress”.
- mint-f7c8cbe48c2d0e2049d5d92c: https://packages.ubuntu.com/noble/libreoffice-uiconfig-writer — “UI data ("config") for LibreOffice Writer”.
- mint-aa8a8692f4cbac3703851f3d: https://packages.ubuntu.com/noble/libreoffice-writer — “office productivity suite -- word processor”.
- mint-11f3387c13ddd7bcb26b729d: https://packages.ubuntu.com/noble/librest-1.0-0 — “REST service access library”.
- mint-fee6b1f92bd0978663694780: https://packages.ubuntu.com/noble/librevenge-0.0-0 — “Base Library for writing document interface filters”.
- mint-1865b5e0986289b574fd6141: https://packages.ubuntu.com/noble/librhythmbox-core10 — “support library for the rhythmbox music player”.
- mint-21b8b102e882a8f5db70a14f: https://packages.ubuntu.com/noble/librist4 — “Reliable Internet Stream Transport -- shared library”.
- mint-064c97ed44814cfe56147600: https://packages.ubuntu.com/noble/libroc0.3 — “real-time audio streaming over the network (shared library)”.
- mint-b015d63cfb25f38c7ecdbdd5: https://packages.ubuntu.com/noble/librsvg2-2 — “SAX-based renderer library for SVG files (runtime)”.
- mint-25cba3f3f64f39fb77d2d18d: https://packages.ubuntu.com/noble/librsvg2-common — “SAX-based renderer library for SVG files (extra runtime)”.
- mint-400ef7e6d28aca272d4b0d20: https://packages.ubuntu.com/noble/librtmp1 — “toolkit for RTMP streams (shared library)”.
- mint-b67f497692d4230016e674c6: https://packages.ubuntu.com/noble/librubberband2 — “audio time-stretching and pitch-shifting library”.
- mint-7d8c7fbc623ace5e44ccbc26: https://packages.ubuntu.com/noble/libsamplerate0 — “Audio sample rate conversion library”.
- mint-969c0d0a7ab22f765397a4fe: https://packages.ubuntu.com/noble/libsane-common — “API library for scanners -- documentation and support files”.
- mint-01ef9712b6765311b5a88439: https://packages.ubuntu.com/noble/libsane-hpaio — “HP SANE backend for multi-function peripherals”.
- mint-0f95f632fc6ba607e13998ce: https://packages.ubuntu.com/noble/libsane1 — “API library for scanners”.
- mint-5b97ac99709d189dc4fdf737: https://packages.ubuntu.com/noble/libsasl2-2 — “Cyrus SASL - authentication abstraction library”.
- mint-fb94560f49822e5d31ed40d5: https://packages.ubuntu.com/noble/libsasl2-modules — “Cyrus SASL - pluggable authentication modules”.
- mint-d07cd0af52a6927d6950af8d: https://packages.ubuntu.com/noble/libsasl2-modules-db — “Cyrus SASL - pluggable authentication modules (DB)”.
- mint-736a84236c9e7af1339282e3: https://packages.ubuntu.com/noble/libsasl2-modules-gssapi-mit — “Cyrus SASL - pluggable authentication modules (GSSAPI)”.
- mint-fd60df32210d201eeed287e0: https://packages.ubuntu.com/noble/libsbc1 — “Sub Band CODEC library - runtime”.
- mint-0bb576df17fbbe7dc65a99ce: https://packages.ubuntu.com/noble/libsdl2-2.0-0 — “Simple DirectMedia Layer”.
- mint-5eb3a96981831774f984c02f: https://packages.ubuntu.com/noble/libseccomp2 — “high level interface to Linux seccomp filter”.
- mint-5b458327ceabc882e9bda08d: https://packages.ubuntu.com/noble/libsecret-1-0 — “Secret store”.
- mint-f5128acc01919b6ea714f7d1: https://packages.ubuntu.com/noble/libsecret-common — “Secret store (common files)”.
- mint-d30df01facb26d99c6830535: https://packages.ubuntu.com/noble/libselinux1 — “SELinux runtime shared libraries”.
- mint-81531ef6d83130e53c064a6b: https://packages.ubuntu.com/noble/libsemanage-common — “Common files for SELinux policy management libraries”.
- mint-9c36d412fcbe42376feb3f8a: https://packages.ubuntu.com/noble/libsemanage2 — “SELinux policy management library”.
- mint-7e1d554495ea2538edd6bce3: https://packages.ubuntu.com/noble/libsensors-config — “lm-sensors configuration files”.
- mint-1ea8ea8187aa08becec889ec: https://packages.ubuntu.com/noble/libsensors5 — “library to read temperature/voltage/fan sensors”.
- mint-494739e6b579775c4a7ec79b: https://packages.ubuntu.com/noble/libsepol2 — “SELinux library for manipulating binary security policies”.
- mint-ea09c435505e0ba1d0460a5d: https://packages.ubuntu.com/noble/libserd-0-0 — “lightweight RDF syntax library”.
- mint-a91bf1ff9fe31f8d37422ffa: https://packages.ubuntu.com/noble/libsframe1 — “Library to handle the SFrame format (runtime library)”.
- mint-07fbe5027ac92c4f854ea9fb: https://packages.ubuntu.com/noble/libsgutils2-1.46-2 — “utilities for devices using the SCSI command set (shared libraries)”.
- mint-e83605623c96a288822ea2d5: https://packages.ubuntu.com/noble/libsharpyuv0 — “Library for sharp RGB to YUV conversion”.
- mint-7ce0d92df429f452aa5ec78c: https://packages.ubuntu.com/noble/libshine3 — “Fixed-point MP3 encoding library - runtime files”.
- mint-60fc1ad4a337194ccb63e978: https://packages.ubuntu.com/noble/libshout3 — “MP3/Ogg Vorbis broadcast streaming library”.
- mint-2f05dfff749d29c830ea383e: https://packages.ubuntu.com/noble/libsigc++-2.0-0v5 — “type-safe Signal Framework for C++ - runtime”.
- mint-ad906a2382eb943f164ae8f5: https://packages.ubuntu.com/noble/libsigc++-3.0-0 — “type-safe Signal Framework for C++ - runtime”.
- mint-796eb775466547ef46087a1a: https://packages.ubuntu.com/noble/libsixel1 — “DEC SIXEL graphics codec implementation (runtime)”.
- mint-ee335fbcd32f6db6029ac871: https://packages.ubuntu.com/noble/libslang2 — “S-Lang programming library - runtime version”.
- mint-6e67bbc7b9ff50cdf02ef453: https://packages.ubuntu.com/noble/libslirp0 — “General purpose TCP-IP emulator library”.
- mint-a9d65167a14ad7cf9e1301cc: https://packages.ubuntu.com/noble/libsm6 — “X11 Session Management library”.
- mint-789f475adef69009207ef83d: https://packages.ubuntu.com/noble/libsmartcols1 — “smart column output alignment library”.
- mint-2d52f802ceb7d8079b38b3d3: https://packages.ubuntu.com/noble/libsmbclient0 — “shared library for communication with SMB/CIFS servers”.
- mint-af828dfc3e4a24a12f8698c2: https://packages.ubuntu.com/noble/libsnapd-glib-2-1 — “GLib snapd library”.
- mint-e4a75deb1bd361a7bad20246: https://packages.ubuntu.com/noble/libsnappy1v5 — “fast compression/decompression library”.
- mint-31a59cb74a8f6a2e160467e2: https://packages.ubuntu.com/noble/libsndfile1 — “Library for reading/writing audio files”.
- mint-b32b4790ace7c43038cb3de8: https://packages.ubuntu.com/noble/libsndio7.0 — “Small audio and MIDI framework from OpenBSD, runtime libraries”.
- mint-c5095a8e093bb7ef63c31a8d: https://packages.ubuntu.com/noble/libsnmp-base — “SNMP configuration script, MIBs and documentation”.
- mint-9a6161554cd145f40ecb9aa0: https://packages.ubuntu.com/noble/libsnmp40t64 — “SNMP (Simple Network Management Protocol) library”.
- mint-0bd22b5a9d79130dd51df177: https://packages.ubuntu.com/noble/libsodium23 — “Network communication, cryptography and signaturing library”.
- mint-40fa0d4c2b89833e46209e6c: https://packages.ubuntu.com/noble/libsonic0 — “Simple library to speed up or slow down speech”.
- mint-918b9edff0751d498be96988: https://packages.ubuntu.com/noble/libsord-0-0 — “library for storing RDF data in memory”.
- mint-2034944553145201eb479604: https://packages.ubuntu.com/noble/libsoup-2.4-1 — “HTTP library implementation in C -- Shared library”.
- mint-77a102aabbbbedae32817b21: https://packages.ubuntu.com/noble/libsoup-3.0-0 — “HTTP library implementation in C -- Shared library”.
- mint-f19e0145c3f8f8ba45ccda10: https://packages.ubuntu.com/noble/libsoup-3.0-common — “HTTP library implementation in C -- Common files”.
- mint-661e8b3ba52c91b0b877783b: https://packages.ubuntu.com/noble/libsoup-gnome-2.4-1 — “HTTP library implementation in C -- GNOME support library”.
- mint-e6484050258a37353a53125e: https://packages.ubuntu.com/noble/libsoup2.4-common — “HTTP library implementation in C -- Common files”.
- mint-f3a27734d1c9e9356a0e2c91: https://packages.ubuntu.com/noble/libsource-highlight-common — “architecture-independent files for source highlighting library”.
- mint-ad77f495098e46b926c97869: https://packages.ubuntu.com/noble/libsource-highlight4t64 — “source highlighting library”.
- mint-847ce165703c5779cb3a9c3c: https://packages.ubuntu.com/noble/libsoxr0 — “High quality 1D sample-rate conversion library”.
- mint-503fb04e196a9eabacaea453: https://packages.ubuntu.com/noble/libspa-0.2-bluetooth — “libraries for the PipeWire multimedia server - bluetooth plugins”.
- mint-6ae7c864928f8fa18c5a51d4: https://packages.ubuntu.com/noble/libspa-0.2-modules — “libraries for the PipeWire multimedia server Simple Plugin API - modules”.
- mint-c5805c4a16ae8dbb6a66dea7: https://packages.ubuntu.com/noble/libspectre1 — “Library for rendering PostScript documents”.
- mint-8fc2d9cdebb2ce8830192888: https://packages.ubuntu.com/noble/libspeechd2 — “Speech Dispatcher: Shared libraries”.
- mint-490f7a3542dd0d019813dc91: https://packages.ubuntu.com/noble/libspeex1 — “The Speex codec runtime library”.
- mint-9b54294b921b0e7907954141: https://packages.ubuntu.com/noble/libspeexdsp1 — “DSP library derived from speex”.
- mint-8bb54dbbb53a3c3d811451a6: https://packages.ubuntu.com/noble/libsphinxbase3t64 — “Speech recognition tool - shared library”.
- mint-e6879089850288fa46ac1809: https://packages.ubuntu.com/noble/libsqlite3-0 — “SQLite 3 shared library”.
- mint-089342beb207f70063e3e79a: https://packages.ubuntu.com/noble/libsratom-0-0 — “library for serialising LV2 atoms to/from Turtle”.
- mint-eabd5f60ddb1e970a7c582c5: https://packages.ubuntu.com/noble/libsrt1.5-gnutls — “Secure Reliable Transport UDP streaming library (GnuTLS flavour)”.
- mint-1bf0009d1cc3054ec97cf5ac: https://packages.ubuntu.com/noble/libss2 — “command-line interface parsing library”.
- mint-305219228853767f2de3d7e2: https://packages.ubuntu.com/noble/libssh-4 — “tiny C SSH library (OpenSSL flavor)”.
- mint-c3fe77974827885a1032464c: https://packages.ubuntu.com/noble/libssh-gcrypt-4 — “tiny C SSH library (gcrypt flavor)”.
- mint-cc6d90e9abcf014cd7a173a4: https://packages.ubuntu.com/noble/libssl3t64 — “Secure Sockets Layer toolkit - shared libraries”.
- mint-15dc0ec0800b5b6437d17503: https://packages.ubuntu.com/noble/libstartup-notification0 — “library for program launch feedback (shared library)”.
- mint-bdf8f6d772ec2e8c8641b3ee: https://packages.ubuntu.com/noble/libstdc++-13-dev — “GNU Standard C++ Library v3 (development files)”.
- mint-c6fe68a10cfe96e265200a9e: https://packages.ubuntu.com/noble/libstdc++6 — “GNU Standard C++ Library v3”.
- mint-ffe6eab780cf04ebbc9b91a0: https://packages.ubuntu.com/noble/libstemmer0d — “Snowball stemming algorithms for use in Information Retrieval”.
- mint-0b1dbeae492b495e9bb93bb0: https://packages.ubuntu.com/noble/libsubid4 — “subordinate id handling library -- shared library”.
- mint-488e196e1addbc87b6578108: https://packages.ubuntu.com/noble/libsuitesparseconfig7 — “configuration routines for all SuiteSparse modules”.
- mint-2bd09fc8978f6d9f71d97b46: https://packages.ubuntu.com/noble/libsvtav1enc1d1 — “Scalable Video Technology for AV1 (libsvtav1enc shared library)”.
- mint-a7a247d394008f5fbecc6e44: https://packages.ubuntu.com/noble/libswresample4 — “FFmpeg library for audio resampling, rematrixing etc. - runtime files”.
- mint-73c32ee1cd91796503ec85f9: https://packages.ubuntu.com/noble/libswscale7 — “FFmpeg library for image scaling and various conversions - runtime files”.
- mint-37ab8f48cdc25ff1a13c3e65: https://packages.ubuntu.com/noble/libsystemd-shared — “systemd shared private library”.
- mint-dbfa434f23ea19b6241686ef: https://packages.ubuntu.com/noble/libsystemd0 — “systemd utility library”.
- mint-7588ce4f54fd792c9bd42dd5: https://packages.ubuntu.com/noble/libtag1v5 — “audio meta-data library”.
- mint-69504cfae45843edca55e431: https://packages.ubuntu.com/noble/libtag1v5-vanilla — “audio meta-data library - vanilla flavour”.
- mint-405359acf0cf63a2169cd519: https://packages.ubuntu.com/noble/libtalloc2 — “hierarchical pool based memory allocator”.
- mint-2cd78129113487db5c19d4f0: https://packages.ubuntu.com/noble/libtasn1-6 — “Manage ASN.1 structures (runtime)”.
- mint-3b140876178364173ece7617: https://packages.ubuntu.com/noble/libtcl8.6 — “Tcl (the Tool Command Language) v8.6 - run-time library files”.
- mint-9d64b10aa5bb947674dac12e: https://packages.ubuntu.com/noble/libtcmalloc-minimal4t64 — “efficient thread-caching malloc”.
- mint-68a19f8268b14060b2525def: https://packages.ubuntu.com/noble/libtdb1 — “Trivial Database - shared library”.
- mint-236e1c8234798d39beb26721: https://packages.ubuntu.com/noble/libteamdctl0 — “library for communication with `teamd` process”.
- mint-9c72e6f895c58b49ed7a204a: https://packages.ubuntu.com/noble/libtevent0t64 — “talloc-based event loop library - shared library”.
- mint-3941bf98a1ab3d45f2e628d0: https://packages.ubuntu.com/noble/libtext-charwidth-perl — “get display widths of characters on the terminal”.
- mint-7bcd4f937205135373b2a3bc: https://packages.ubuntu.com/noble/libtext-iconv-perl — “module to convert between character sets in Perl”.
- mint-36eb4e4c4e4eb48c17985111: https://packages.ubuntu.com/noble/libtext-wrapi18n-perl — “internationalized substitute of Text::Wrap”.
- mint-a5f5ff7e91db3d3684bcf0d8: https://packages.ubuntu.com/noble/libthai-data — “Data files for Thai language support library”.
- mint-7ae0c9f4c3aca34f81b0661c: https://packages.ubuntu.com/noble/libthai0 — “Thai language support library”.
- mint-3c659bb14e8affcf15147c8d: https://packages.ubuntu.com/noble/libtheora0 — “Theora Video Compression Codec”.
- mint-d33297e633bc0f0a775ccf11: https://packages.ubuntu.com/noble/libtie-ixhash-perl — “Perl module to order associative arrays”.
- mint-3e44addcf712af26092f7b8b: https://packages.ubuntu.com/noble/libtiff6 — “Tag Image File Format (TIFF) library”.
- mint-bf1107e4812fb5082125689c: https://packages.ubuntu.com/noble/libtimedate-perl — “collection of modules to manipulate date/time information”.
- mint-29bb86e1f410b4e9273b2a6c: https://packages.ubuntu.com/noble/libtimezonemap-data — “GTK+3 timezone map widget - data files”.
- mint-d30b69af2b980f39329c5896: https://packages.ubuntu.com/noble/libtimezonemap1 — “GTK+3 timezone map widget”.
- mint-85ce0120d49cc826b322ddca: https://packages.ubuntu.com/noble/libtinfo6 — “shared low-level terminfo library for terminal handling”.
- mint-ef80a80feb7709633f6d40e4: https://packages.ubuntu.com/noble/libtirpc-common — “transport-independent RPC library - common files”.
- mint-e9a990c6c59c0c9cafa76572: https://packages.ubuntu.com/noble/libtirpc3t64 — “transport-independent RPC library”.
- mint-0e8a7e18e99acc29322752a8: https://packages.ubuntu.com/noble/libtotem-plparser-common — “Totem Playlist Parser library - common files”.
- mint-c351ca95c29037b2f79d1993: https://packages.ubuntu.com/noble/libtotem-plparser18 — “Totem Playlist Parser library - runtime files”.
- mint-3809023013bafa3422693414: https://packages.ubuntu.com/noble/libtry-tiny-perl — “module providing minimalistic try/catch”.
- mint-1ec4738805ce37d9a42a9252: https://packages.ubuntu.com/noble/libtsan2 — “ThreadSanitizer -- a Valgrind-based detector of data races (runtime)”.
- mint-2fa33c3a711f0e97179c8698: https://packages.ubuntu.com/noble/libtspi1 — “open-source TCG Software Stack (library)”.
- mint-e9e0ae0e4ba417afc25d7f29: https://packages.ubuntu.com/noble/libtss2-esys-3.0.2-0t64 — “TPM2 Software stack library - TSS and TCTI libraries”.
- mint-f4a20baca7175b290e11c0bc: https://packages.ubuntu.com/noble/libtss2-mu-4.0.1-0t64 — “TPM2 Software stack library - TSS and TCTI libraries”.
- mint-dd1d43b42b53e0f1cd3e1ef6: https://packages.ubuntu.com/noble/libtss2-sys1t64 — “TPM2 Software stack library - TSS and TCTI libraries”.
- mint-3136bfd84c88897a87d4f5fc: https://packages.ubuntu.com/noble/libtss2-tcti-cmd0t64 — “TPM2 Software stack library - TSS and TCTI libraries”.
- mint-559b4166c0b461441c211195: https://packages.ubuntu.com/noble/libtss2-tcti-device0t64 — “TPM2 Software stack library - TSS and TCTI libraries”.
- mint-6ae717eb1f74ec48c2651cfc: https://packages.ubuntu.com/noble/libtss2-tcti-mssim0t64 — “TPM2 Software stack library - TSS and TCTI libraries”.
- mint-97d892645fa3fd659a7b079e: https://packages.ubuntu.com/noble/libtss2-tcti-swtpm0t64 — “TPM2 Software stack library - TSS and TCTI libraries”.
- mint-71d97985adb80d184a6a8b50: https://packages.ubuntu.com/noble/libtwolame0 — “MPEG Audio Layer 2 encoding library”.
- mint-22ce3deba3269cc6fd5ab825: https://packages.ubuntu.com/noble/libubsan1 — “UBSan -- undefined behaviour sanitizer (runtime)”.
- mint-8870b5941ef66cc09f30a443: https://packages.ubuntu.com/noble/libuchardet0 — “universal charset detection library - shared library”.
- mint-db603f6468f1861a7340539c: https://packages.ubuntu.com/noble/libudev1 — “libudev shared library”.
- mint-88ae52fe36c99d33134c8dc1: https://packages.ubuntu.com/noble/libudfread0 — “UDF reader library”.
- mint-0531b220a25e16bc37c3d62f: https://packages.ubuntu.com/noble/libudisks2-0 — “GObject based library to access udisks2”.
- mint-7c14c3bdb8b7cc507f0bb95c: https://packages.ubuntu.com/noble/libunibreak5 — “line breaking library for Unicode (shared library)”.
- mint-995f1bf3ce632592e771bf62: https://packages.ubuntu.com/noble/libunistring5 — “Unicode string library for C”.
- mint-a7b59b21ce3db47b23c2d93d: https://packages.ubuntu.com/noble/libuno-cppu3t64 — “LibreOffice UNO runtime environment -- CPPU public library”.
- mint-03e68abfec9b0459b53f38bb: https://packages.ubuntu.com/noble/libuno-cppuhelpergcc3-3t64 — “LibreOffice UNO runtime environment -- CPPU helper library”.
- mint-6855337293eaa3e8d4cf0cc8: https://packages.ubuntu.com/noble/libuno-purpenvhelpergcc3-3t64 — “LibreOffice UNO runtime environment -- "purpose environment" helper”.
- mint-cee9362bc9481842f62bf81f: https://packages.ubuntu.com/noble/libuno-sal3t64 — “LibreOffice UNO runtime environment -- SAL public library”.
- mint-7dbfcf85d95851a4b5990107: https://packages.ubuntu.com/noble/libuno-salhelpergcc3-3t64 — “LibreOffice UNO runtime environment -- SAL helpers for C++ library”.
- mint-638deddfb420d124d2e13906: https://packages.ubuntu.com/noble/libunwind8 — “library to determine the call-chain of a program - runtime”.
- mint-68f4d1b0169a4e50e27c4676: https://packages.ubuntu.com/noble/libupower-glib3 — “abstraction for power management - shared library”.
- mint-da7df9c43fe2bf6b9d6550cd: https://packages.ubuntu.com/noble/liburcu8t64 — “userspace RCU (read-copy-update) library”.
- mint-d45638d03e6d97b372a9be3a: https://packages.ubuntu.com/noble/liburi-perl — “module to manipulate and access URI strings”.
- mint-fbe3932b89bc149a5b9f99f1: https://packages.ubuntu.com/noble/liburing2 — “Linux kernel io_uring access library - shared library”.
- mint-62c9db2169e2fc3bf2e9152a: https://packages.ubuntu.com/noble/libusb-1.0-0 — “userspace USB programming library”.
- mint-1e6163eb9a9fab1f1478868c: https://packages.ubuntu.com/noble/libusbmuxd6 — “USB multiplexor daemon for iPhone and iPod Touch devices - library”.
- mint-6a62045db8c7330a1c88d5d9: https://packages.ubuntu.com/noble/libuuid1 — “Universally Unique ID library”.
- mint-fff6fb352a3edcefdeef7893: https://packages.ubuntu.com/noble/libuv1t64 — “asynchronous event notification library - runtime library”.
- mint-41abbdab5255a457477e9802: https://packages.ubuntu.com/noble/libv4l-0t64 — “Collection of video4linux support libraries”.
- mint-35e8c231bf9dfb9b54b84d68: https://packages.ubuntu.com/noble/libv4lconvert0t64 — “Video4linux frame format conversion library”.
- mint-f76414d6d3802cd7057f0502: https://packages.ubuntu.com/noble/libva-drm2 — “Video Acceleration (VA) API for Linux -- DRM runtime”.
- mint-880c0e5a898a4a5fbdfc4314: https://packages.ubuntu.com/noble/libva-wayland2 — “Video Acceleration (VA) API for Linux -- Wayland runtime”.
- mint-f63db37939c2670c6b1c8411: https://packages.ubuntu.com/noble/libva-x11-2 — “Video Acceleration (VA) API for Linux -- X11 runtime”.
- mint-e9ba9f0109f90c659bde10ee: https://packages.ubuntu.com/noble/libva2 — “Video Acceleration (VA) API for Linux -- runtime”.
- mint-ae066d4d6075493c9d50aa5f: https://packages.ubuntu.com/noble/libvdpau1 — “Video Decode and Presentation API for Unix (libraries)”.
- mint-4905aefb789a35b6b57351be: https://packages.ubuntu.com/noble/libvidstab1.1 — “video stabilization library (shared library)”.
- mint-2ad23bb13b611fdb528ddaa0: https://packages.ubuntu.com/noble/libvisio-0.1-1 — “library for parsing the visio file structure”.
- mint-58a93efdf1c84f581f36133a: https://packages.ubuntu.com/noble/libvisual-0.4-0 — “audio visualization framework”.
- mint-56694454eec3c637692736fe: https://packages.ubuntu.com/noble/libvisual-0.4-plugins — “audio visualization framework plugins”.
- mint-d146fa0997bd7eb8dc4a104b: https://packages.ubuntu.com/noble/libvolume-key1 — “Library for manipulating storage encryption keys and passphrases”.
- mint-f990d8adbaaa8205dffe0a6d: https://packages.ubuntu.com/noble/libvorbis0a — “decoder library for Vorbis General Audio Compression Codec”.
- mint-b98703bb1123153267b8fe86: https://packages.ubuntu.com/noble/libvorbisenc2 — “encoder library for Vorbis General Audio Compression Codec”.
- mint-fe54d23dadad7ed4e4876443: https://packages.ubuntu.com/noble/libvorbisfile3 — “high-level API for Vorbis General Audio Compression Codec”.
- mint-84ee33598c51154e544d5498: https://packages.ubuntu.com/noble/libvpl2 — “oneAPI Video Processing Library -- shared library”.
- mint-c41e7865ae15c30b0b8fb012: https://packages.ubuntu.com/noble/libvpx9 — “VP8 and VP9 video codec (shared library)”.
- mint-a8f8a9b35e2f233c518cab24: https://packages.ubuntu.com/noble/libvte-2.91-0 — “Terminal emulator widget for GTK+ 3.0 - runtime files”.
- mint-f1de460c4c30e051eff71e46: https://packages.ubuntu.com/noble/libvte-2.91-common — “Terminal emulator widget for GTK+ 3.0 - common files”.
- mint-4a2191140a7153e12006a698: https://packages.ubuntu.com/noble/libvulkan1 — “Vulkan loader library”.

## Mechanical verification

Exactly 635 assigned ids, each once; no additions or omissions; all decisions valid; field word limits verified.

MUST: 601, NOT: 29, HOLE: 3, UNKNOWN: 2, MIXED: 0.


---

Source record: part-mint.3.notes.md

# Package classification, segment 3

Only the assigned input, Sections 2 and 3, numbered sentences, and public package documentation were consulted. Inventory class labels were ignored. No removal test or probe was performed.

## Fixed text

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;

- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.

- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S2.2-16** the boot order and device firmware must be recorded where the system is able to change them.

- **S3-2** If what the object does remains unknown, the case yields ?.

## Scripted homogeneous rule: executable capabilities

Runtime programs, interpreters, libraries and modules documented to perform an operation are MUST under S2.2-1, S2.2-2, S2.2-9 and S2.2-10. Libraries and interpreter modules execute in the caller’s rights; neither their packaging nor their installation location supplies an exemption. The manually selected exclusion set removes metapackages, common-data packages, themes and ambiguous descriptions from this rule. Package name alone is not the rule.

Ten manual checks follow, covering binaries, native libraries, interpreter modules and services. Each description establishes an executable operation rather than passive content.

- mint-486d3e71b63a9871233e8b6a (`libwacom-bin`): "Wacom model feature query library -- binaries" — https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz
- mint-668fecc5ea52f782b49e4f1d (`libwavpack1`): "audio codec (lossy and lossless) - library" — https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz
- mint-75e5f5d6365454b8a1908057 (`libx11-6`): "X11 client-side library" — https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz
- mint-7c7f74e40a77f719c686abde (`libxml-parser-perl`): "Perl module for parsing XML files" — https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz
- mint-c6894bf5f42225da5d3174d8 (`lightdm`): "Display Manager" — https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz
- mint-ee5a4467c12e6db4a0d87057 (`login`): "system login tools" — https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz
- mint-4b056b07482dd11f028ceb45 (`mount`): "tools for mounting and manipulating filesystems" — https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz
- mint-0bbf1dd67e7b12a88901aa98 (`python3-apt`): "Python 3 interface to libapt-pkg" — https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz
- mint-a231610c1f79cace35c12cc1 (`python3-httplib2`): "comprehensive HTTP client library written for Python3" — https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz
- mint-cb23aa1c1d78e3f94323138e (`systemd`): "system and service manager" — https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz

## Individually reviewed exceptions

The explicit index-to-decision table in part-mint.3.exceptions.txt records separate judgments for every nonhomogeneous row; the append script only serializes those decisions. The rows are single package objects, not groups of all their dependency packages. No dependency removal or autoremove is assumed. Safely removable transition packages do not inherit the function of their dependency. For dependency selectors without an express safe-removal description, the unresolved issue is future dependency-driven update behavior versus current executable capability.

Public package descriptions establish functionality, not a claim that the currently published version is byte-identical to the inventoried version. Versioned kernel entries were matched by exact package name in the update repository. Package archive file listings were inspected without installation or execution. The saved filelist contains the source archive URL and exact member paths. Data-only package names were never assumed to exclude code: file inspection found helper scripts in several common-data packages.

## Per-object documentation evidence

- mint-486d3e71b63a9871233e8b6a (`libwacom-bin`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Wacom model feature query library -- binaries". 
- mint-0f10370e18f44273059b241b (`libwacom-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Wacom model feature query library (common files)". Archive https://archive.ubuntu.com/ubuntu/pool/main/libw/libwacom/libwacom-common_2.10.0-2_all.deb; inspected entries: `./usr/lib/udev/hwdb.d/65-libwacom.hwdb`, `./usr/lib/udev/rules.d/65-libwacom.rules`.
- mint-35d473dfe02bd365515ece71 (`libwacom9`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Wacom model feature query library". 
- mint-668fecc5ea52f782b49e4f1d (`libwavpack1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "audio codec (lossy and lossless) - library". 
- mint-3bbe54d2485f0b90b8c0eb74 (`libwayland-client0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "wayland compositor infrastructure - client library". 
- mint-448738c1e9a06b891125e3db (`libwayland-cursor0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "wayland compositor infrastructure - cursor library". 
- mint-af1863bc8720e62d8ebcfc79 (`libwayland-egl1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "wayland compositor infrastructure - EGL library". 
- mint-c1fbcd34571a5deedd8d3469 (`libwayland-server0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "wayland compositor infrastructure - server library". 
- mint-11c20db4bc029bbb008241c5 (`libwbclient0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Samba winbind client library". 
- mint-eecaef77255ea67eb42e6666 (`libwebkit2gtk-4.1-0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Web content engine library for GTK". 
- mint-f9c638855109accec04bf82e (`libwebkitgtk-6.0-4`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Web content engine library for GTK". 
- mint-01a8f19432d36b389ce07c4f (`libwebp7`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Lossy compression of digital photographic images". 
- mint-47c6f5627ff04365c580fffc (`libwebpdemux2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Lossy compression of digital photographic images.". 
- mint-14d22a7c180c19741bd897cb (`libwebpmux3`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Lossy compression of digital photographic images". 
- mint-bd27d6b604d082191a0ae85d (`libwebrtc-audio-processing1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "AudioProcessing module from the WebRTC project.". 
- mint-167c9bb69f23372bfbb64503 (`libwireplumber-0.4-0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Shared libraries for WirePlumber". 
- mint-19a8b4ccd6faa43d098dfd02 (`libwmf-0.2-7`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Windows metafile conversion library". 
- mint-8b633134fefe53cf2aacc066 (`libwmf-0.2-7-gtk`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Windows metafile conversion GTK pixbuf plugin". 
- mint-2a48a16a6f2133f3cd6ca5be (`libwmf0.2-7-gtk`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Windows metafile conversion GTK pixbuf plugin - transitional package". 
- mint-3167ada4da3ccc04ec2d9665 (`libwmflite-0.2-7`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Windows metafile conversion lite library". 
- mint-11051843c07e54b2ad22584a (`libwnck-3-0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Window Navigator Construction Kit - runtime files". 
- mint-e9fa0e8060168eabdcf27a98 (`libwnck-3-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Window Navigator Construction Kit - common files". 
- mint-4e5673176a9db38ed6c0baeb (`libwoff1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "library for converting fonts to WOFF 2.0". 
- mint-33b348e1f4170309b6c65a6e (`libwpd-0.10-10`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Library for handling WordPerfect documents (shared library)". 
- mint-dd3affb0527b721839bcbda3 (`libwpg-0.3-3`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "WordPerfect graphics import/convert library (shared library)". 
- mint-15eed78d45eb34849d73848d (`libwps-0.4-4`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Works text file format import filter library (shared library)". 
- mint-8280537a8fb85f09206bd007 (`libwrap0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "TCP wrappers library". 
- mint-dde9b3ef606e8db4d35d77d6 (`libwww-perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "simple and consistent interface to the world-wide web". 
- mint-6dee2ece19272d8f26e27c8e (`libwww-robotrules-perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "database of robots.txt-derived permissions". 
- mint-75e5f5d6365454b8a1908057 (`libx11-6`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 client-side library". 
- mint-f281dd26c02a813bc3e4856a (`libx11-data`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 client-side library". 
- mint-f56a0b4cd24c32bc5535f61f (`libx11-protocol-perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Perl module for the X Window System Protocol, version 11". 
- mint-f8165c983a72b8a46326b2e6 (`libx11-xcb1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Xlib/XCB interface library". 
- mint-d07bdd5532d695f6653cc89a (`libx264-164`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "x264 video coding library". 
- mint-741917b37d9c01d56eb11f73 (`libx265-199`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "H.265/HEVC video stream encoder (shared library)". 
- mint-64c720eb95895b14f11c085c (`libxapian30`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Search engine library". 
- mint-d2d1733fc59983c1d2917a2d (`libxapp1`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "XApp library". 
- mint-eb65b92d9d17365f46f94311 (`libxatracker2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X acceleration library -- runtime". 
- mint-0c9b9fa9bbd3c903255e8df0 (`libxau6`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 authorisation library". 
- mint-c673cb23c16128c1d89d19f1 (`libxaw7`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Athena Widget library". 
- mint-48598509145fea01e7a5ee1a (`libxcb-damage0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, damage extension". 
- mint-3016f213d2f6513f2c12cceb (`libxcb-dri2-0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, dri2 extension". 
- mint-2b03043c8145c16776bca888 (`libxcb-dri3-0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, dri3 extension". 
- mint-b4219497d9b8f97ec4e31aa0 (`libxcb-glx0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, glx extension". 
- mint-4e5e47c7e12ac4777aa24911 (`libxcb-icccm4`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "utility libraries for X C Binding -- icccm". 
- mint-b47b6ba625e3e580338501d5 (`libxcb-image0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "utility libraries for X C Binding -- image". 
- mint-1408a71a9fb90aa8f2b9c55d (`libxcb-keysyms1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "utility libraries for X C Binding -- keysyms". 
- mint-b33b146b526f68f0a1a33f54 (`libxcb-present0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, present extension". 
- mint-54a22138f750c1161abe1bf4 (`libxcb-randr0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, randr extension". 
- mint-514e249f979b08d2034e68c4 (`libxcb-render-util0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "utility libraries for X C Binding -- render-util". 
- mint-3ea9b74361c4c656b76d211e (`libxcb-render0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, render extension". 
- mint-5075aa40675d5ce72ddc2abd (`libxcb-res0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, res extension". 
- mint-fd05c953f68a02d4abca5707 (`libxcb-shape0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, shape extension". 
- mint-5e9bd67af6a644e2d148e9d9 (`libxcb-shm0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, shm extension". 
- mint-f5239483dc4b1bcb1b1acfca (`libxcb-sync1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, sync extension". 
- mint-258ec83daec91246a34d3304 (`libxcb-util1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "utility libraries for X C Binding -- atom, aux and event". 
- mint-687518aef916c465d49ccf90 (`libxcb-xfixes0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, xfixes extension". 
- mint-7b53d110bfb821b7a6f20060 (`libxcb-xinerama0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, xinerama extension". 
- mint-905d1c8e5d580a2c98cdc66a (`libxcb-xinput0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, xinput extension". 
- mint-ef3513fe5f03f67f3212c403 (`libxcb-xkb1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, XKEYBOARD extension". 
- mint-bc4db20984475b1970825bc9 (`libxcb-xv0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding, xv extension". 
- mint-50814af124218fb3e0b190cc (`libxcb1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X C Binding". 
- mint-b36838a8f62de72c5fa7b227 (`libxcomposite1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Composite extension library". 
- mint-384de93b0cb9b4ddf764b66f (`libxcursor1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X cursor management library". 
- mint-c8903ee6e611034e9ce2cee2 (`libxcvt0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "VESA CVT standard timing modelines generator -- shared library". 
- mint-e6d4ef4bf5294d70a92779d6 (`libxdamage1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 damaged region extension library". 
- mint-535d0c90d3e476c14c408a79 (`libxdmcp6`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Display Manager Control Protocol library". 
- mint-b570f32bb16e7a0cde621629 (`libxdo3`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "library for simulating (generating) X11 keyboard/mouse input events". 
- mint-4be067900be64a60afc31bea (`libxext6`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 miscellaneous extension library". 
- mint-bc786792d3f5938a97bc4763 (`libxfixes3`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 miscellaneous 'fixes' extension library". 
- mint-520422119e52d58c1a7f404a (`libxfont2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 font rasterisation library". 
- mint-99e86a9c635e167330d0d220 (`libxft2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "FreeType-based font drawing library for X". 
- mint-daf204df1dfb8e82feb11785 (`libxi6`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Input extension library". 
- mint-b15717438bed230c38e7238e (`libxinerama1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Xinerama extension library". 
- mint-0f6ab330f121a37ba33bb52a (`libxkbcommon-x11-0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "library to create keymaps with the XKB X11 protocol". 
- mint-d291bc7eac0c418f943c0f38 (`libxkbcommon0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "library interface to the XKB compiler - shared library". 
- mint-3c178c5a80944a52a67fe749 (`libxkbfile1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 keyboard file manipulation library". 
- mint-099b659adae61e36ae7dbf5e (`libxkbregistry0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "library to query available RMLVO". 
- mint-ffeadb5ed28e87c0ebff2190 (`libxklavier16`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X Keyboard Extension high-level API". 
- mint-d6eacbc7c9cdfbe99e384885 (`libxml-namespacesupport-perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Perl module for supporting simple generic namespaces". 
- mint-7c7f74e40a77f719c686abde (`libxml-parser-perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Perl module for parsing XML files". 
- mint-9812dff666026a99dc3dfa6b (`libxml-sax-base-perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "base class for SAX drivers and filters". 
- mint-a9b2eb76d99f87b62d1e1490 (`libxml-sax-expat-perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Perl module for a SAX2 driver for Expat (XML::Parser)". 
- mint-5d41327a2360139c41365fae (`libxml-sax-perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Perl module for using and building Perl SAX2 XML processors". 
- mint-16cab4b0f8c2048aa18afda3 (`libxml-twig-perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Perl module for processing huge XML documents in tree mode". 
- mint-2bd89ebed94fe43729a98cf0 (`libxml-xpathengine-perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "re-usable XPath engine for DOM-like trees". 
- mint-aa8d204e09a032bae47b8ae3 (`libxml2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GNOME XML library". 
- mint-a005802fca4096f3caefdc72 (`libxmlb2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Binary XML library". 
- mint-694422ebf8dfcc92d68ec7a8 (`libxmlsec1t64`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "XML security library". 
- mint-c97616ea784d0ea1d26ff598 (`libxmlsec1t64-nss`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Nss engine for the XML security library". 
- mint-771b74c7e74071a536ef8cef (`libxmu6`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 miscellaneous utility library". 
- mint-16acc491202bf94ea0d76f6d (`libxmuu1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 miscellaneous micro-utility library". 
- mint-b52dfc318122c8b4bf5ce152 (`libxpm4`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 pixmap library". 
- mint-836ff87870695d149d005e67 (`libxpresent1`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "X11 Present extension library". 
- mint-d08133aa2d309f591e1b1c81 (`libxrandr2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 RandR extension library". 
- mint-c839aadbfb9d338a9e9083bd (`libxreaderdocument3`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Document rendering library". 
- mint-47dba8e81627e38a01ab0123 (`libxreaderview3`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Document viewing library". 
- mint-40a3fb46ada3ae1f5033c826 (`libxrender1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X Rendering Extension client library". 
- mint-01acfc75d27a9d789a75d7bf (`libxres1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Resource extension library". 
- mint-7b3435630b0e5199c64976b4 (`libxshmfence1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X shared memory fences - shared library". 
- mint-ea7b4969eab576814d78204d (`libxslt1.1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "XSLT 1.0 processing library - runtime library". 
- mint-9c98f2a3f82303d0e726018e (`libxss1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Screen Saver extension library". 
- mint-5e25458c52362290efa7d04e (`libxt6t64`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 toolkit intrinsics library". 
- mint-f59be90eb3468e0707261f53 (`libxtables12`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "netfilter xtables library". 
- mint-7c0d3a0e1e51fb94d3f10f88 (`libxtst6`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Testing -- Record extension library". 
- mint-10a5326b39b51e474c8d1c95 (`libxv1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Video extension library". 
- mint-c1518578c86c09952524bf37 (`libxvidcore4`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Open source MPEG-4 video codec (library)". 
- mint-522873260d4a1fac38d8be25 (`libxvmc1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Video extension library". 
- mint-fd969115ef42d718a2fde421 (`libxxf86dga1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 Direct Graphics Access extension library". 
- mint-40dddc62b44989abc29d2b1d (`libxxf86vm1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 XFree86 video mode extension library". 
- mint-729d9946a750ee32642f984f (`libxxhash0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "shared library for xxhash". 
- mint-6fc8c7c2c3c34e2488c6af95 (`libyajl2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Yet Another JSON Library". 
- mint-22289eb08d4b869e1e568482 (`libyaml-0-2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Fast YAML 1.1 parser and emitter library". 
- mint-6e5b74be64f7d8439aa56084 (`libyelp0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Library for the GNOME help browser". 
- mint-57d25d05763a7da24251794e (`libzimg2`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "scaling, colorspace, depth conversion library (shared library)". 
- mint-edfe9c076c46e125eb7693b2 (`libzip4t64`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "library for reading, creating, and modifying zip archives (runtime)". 
- mint-9ec291391e46296ef9e76acd (`libzix-0-0`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "library of portability wrappers and data structures (shared library)". 
- mint-7db12ffcf71f29d94619732f (`libzmq5`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "lightweight messaging kernel (shared library)". 
- mint-692d8f27bc25e9982827dec2 (`libzstd1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "fast lossless compression algorithm". 
- mint-c393bda3b18c8f61865b2819 (`libzvbi-common`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Vertical Blanking Interval decoder (VBI) - common files". 
- mint-1f60f63deeeda9c81b2c8ee3 (`libzvbi0t64`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Vertical Blanking Interval decoder (VBI) - runtime files". 
- mint-c6894bf5f42225da5d3174d8 (`lightdm`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Display Manager". 
- mint-a3ff05edb0b3cd92ba626749 (`lightdm-settings`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "LightDM configuration tool". 
- mint-6b6c50923eddf7dd3c82d51c (`linux-base`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Linux image base package". 
- mint-f1bf97170e168712af812520 (`linux-firmware`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Firmware for Linux kernel drivers (metapackage)". 
- mint-113e18df451dd886766290a4 (`linux-generic-hwe-24.04`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Complete Generic Linux kernel and headers". 
- mint-a546e0583fc7d7668009b889 (`linux-headers-6.14.0-37-generic`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Linux kernel headers for version 6.14.0". 
- mint-3177c342fa78688f4cc720db (`linux-headers-generic-hwe-24.04`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Generic Linux kernel headers". 
- mint-032c457b30aed9c038c42e2f (`linux-hwe-6.14-headers-6.14.0-37`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Header files related to Linux kernel version 6.14.0". 
- mint-189d66dffc0eb435f9052c86 (`linux-image-6.14.0-37-generic`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Signed kernel image generic". 
- mint-449bad2904a4781cf8e19aa5 (`linux-image-generic-hwe-24.04`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Generic Linux kernel image". 
- mint-e6ce9664b5f66c1d17c096b4 (`linux-libc-dev`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Linux Kernel Headers for development". 
- mint-42a02e20b6a2cf9e24aa866a (`linux-modules-6.14.0-37-generic`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Linux kernel extra modules for version 6.14.0". 
- mint-5427c67219e2fd13f009bb2d (`linux-modules-extra-6.14.0-37-generic`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "Linux kernel extra modules for version 6.14.0". 
- mint-368aa34030d7588701e94635 (`linux-sound-base`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "base package for ALSA and OSS sound systems". 
- mint-52a9706e35cc8050e6f8abb0 (`linuxmint-keyring`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "GnuPG key of the Linux Mint repository". 
- mint-cf0b6dce496b48fbc5d62d47 (`lm-sensors`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "utilities to read temperature/voltage/fan sensors". 
- mint-251662c577f62ba582110911 (`localechooser-data`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Lists of locales supported by the installer". 
- mint-9a98a8542722dc27f6c88eaa (`locales`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GNU C Library: National Language (locale) data [support]". 
- mint-ee5a4467c12e6db4a0d87057 (`login`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "system login tools". 
- mint-4ce79e5598be5740d4564e03 (`logrotate`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Log rotation utility". 
- mint-b982b41950146e5b4b2e5335 (`logsave`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "save the output of a command in a log file". 
- mint-0acd8faca8ac919b0748474f (`lp-solve`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Solve (mixed integer) linear programming problems". 
- mint-7ce5180311c314972ec5657f (`lsb-release`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Linux Standard Base version reporting utility (minimal implementation)". 
- mint-d93bf9d0996942d6e9846551 (`lshw`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "information about hardware configuration". 
- mint-8decdc4219773e40bfdb3c0d (`lsof`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "utility to list open files". 
- mint-95b17a814c7eff02a0baf201 (`lto-disabled-list`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "list of packages not to build with LTO". 
- mint-e566ef6a831bf8f605ee8115 (`ltrace`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Tracks runtime library calls in dynamically linked programs". 
- mint-5dba566bc3dd6530eada8f4d (`lvm2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Linux Logical Volume Manager". 
- mint-d575d855664feb486b13f522 (`mailcap`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Debian's mailcap system, and support programs". 
- mint-73874f68b5c8650100f0aacb (`make`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "utility for directing compilation". 
- mint-bc8798c1d8ffd58716597e5c (`man-db`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "tools for reading manual pages". 
- mint-7c372b5d7c6f05289917388b (`manpages`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Manual pages about using a GNU/Linux system". 
- mint-8f52bff83eeab1dcf01ecd2b (`mate-desktop`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Library with common API for various MATE modules". 
- mint-9aee0fb23028e3e622790b19 (`mate-desktop-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Library with common API for various MATE modules (common files)". Archive https://mirrors.kernel.org/linuxmint-packages/pool/upstream/m/mate-desktop/mate-desktop-common_1.26.2-1.1mint1+zara_all.deb; inspected entries: `./usr/share/glib-2.0/schemas/org.mate.accessibility-keyboard.gschema.xml`, `./usr/share/glib-2.0/schemas/org.mate.accessibility-startup.gschema.xml`, `./usr/share/glib-2.0/schemas/org.mate.applications-at-mobility.gschema.xml`, `./usr/share/glib-2.0/schemas/org.mate.applications-at-visual.gschema.xml`.
- mint-811bb57e47da239a14d15976 (`mate-menus`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "implementation of the freedesktop menu specification for MATE". 
- mint-21acd6938b184c4842b6bcf5 (`mate-panel`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "launcher and docking facility for MATE". 
- mint-e5858e424fab50db0bf97eb7 (`mate-panel-common`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "launcher and docking facility for MATE (common files)". Archive https://archive.ubuntu.com/ubuntu/pool/universe/m/mate-panel/mate-panel-common_1.27.1-2build3_all.deb; inspected entries: `./usr/share/doc/mate-panel-common/changelog.Debian.gz`, (not published: external working record), `./usr/share/help/C/mate-clock/index.docbook`, `./usr/share/help/C/mate-clock/legal.xml`.
- mint-5a26ac3424c57910f8738835 (`mate-polkit`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "MATE authentication agent for PolicyKit-1". 
- mint-b7005b2d4632f34851d9501e (`mate-polkit-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "MATE authentication agent for PolicyKit-1 (common files)". Archive https://mirrors.kernel.org/linuxmint-packages/pool/upstream/m/mate-polkit/mate-polkit-common_1.26.1+mint1_all.deb; inspected entries: `./etc/xdg/autostart/polkit-mate-authentication-agent-1.desktop`.
- mint-a628216001b934add965cc6e (`mawk`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Pattern scanning and text processing language". 
- mint-a6956c6f8b5ee156c87a1401 (`mdadm`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "tool for managing Linux MD devices (software RAID)". 
- mint-9cb9e637346c655a41bb1782 (`media-player-info`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Media player identification files". 
- mint-829651f8c86d896cb7dae9d0 (`media-types`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "List of standard media types and their usual file extension". 
- mint-59668859131af231c384abb9 (`mesa-libgallium`): https://archive.ubuntu.com/ubuntu/dists/noble-updates/main/binary-amd64/Packages.gz — "shared infrastructure for Mesa drivers". 
- mint-d82587113f6c9143d4abaf0e (`mesa-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Miscellaneous Mesa utilities -- symlinks". 
- mint-d17d08f283e3b48eb227f628 (`mesa-utils-bin`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Miscellaneous Mesa utilities -- native applications". 
- mint-1a42b266e3e0845580bb3cbd (`mesa-va-drivers`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Mesa VA-API video acceleration drivers". 
- mint-9e73ec9507ccba2bf25c9334 (`mesa-vdpau-drivers`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Mesa VDPAU video acceleration drivers". 
- mint-971e96e6c87fd95a11ab6911 (`mesa-vulkan-drivers`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Mesa Vulkan graphics drivers". 
- mint-c1df0151621330dfb0a40943 (`metacity`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "lightweight GTK window manager". 
- mint-58e5bd7e0186ed5eb3afb4a9 (`metacity-common`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "shared files for the Metacity window manager". Archive https://archive.ubuntu.com/ubuntu/pool/universe/m/metacity/metacity-common_3.52.0-1build1_all.deb; inspected entries: `./usr/share/glib-2.0/schemas/org.gnome.metacity.gschema.xml`, `./usr/share/glib-2.0/schemas/org.gnome.metacity.keybindings.gschema.xml`, `./usr/share/glib-2.0/schemas/org.gnome.metacity.theme.gschema.xml`.
- mint-5717fd738c8a772af6c2c041 (`mint-artwork`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Linux Mint Artwork and Resources". Archive https://mirrors.kernel.org/linuxmint-packages/pool/main/m/mint-artwork/mint-artwork_1.9.2_all.deb; inspected entries: `./etc/X11/Xsession.d`, `./etc/X11/Xsession.d/99mint`, `./etc/lightdm/lightdm-gtk-greeter.conf.d`, `./etc/lightdm/lightdm-gtk-greeter.conf.d/99_linuxmint.conf`.
- mint-a3f9714b5654642ca94d19dc (`mint-backgrounds-wallpapers`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Desktop backgrounds - Wallpapers". 
- mint-0050505245ab51d8d6ed4382 (`mint-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Common scripts and resources for Linux Mint". 
- mint-af4892a921ca8c42310979b2 (`mint-cursor-themes`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Linux Mint Cursor themes". 
- mint-93f4e80faefef86dec4982df (`mint-info-cinnamon`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Necessary information about the Linux Mint release and edition.". 
- mint-a1980b1ef78710f022b44853 (`mint-l-icons`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Mint-L icon theme". 
- mint-8c9a57a0630f529dde9df2ec (`mint-l-theme`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Mint-L theme". 
- mint-c53985fe7e4e1719c8e2a38f (`mint-meta-cinnamon`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Set of packages installed by default in the Cinnamon edition of Linux Mint". 
- mint-7bda0a7a54573354b473943c (`mint-meta-core`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Core Linux Mint packages". 
- mint-419c2821ae90f4ead396bde4 (`mint-mirrors`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Linux Mint Repository mirrors". 
- mint-080d921edec13ac525101e7e (`mint-themes`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Mint themes". 
- mint-4366c6860989f1b8e80e3e40 (`mint-translations`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Translation files for Linux Mint". 
- mint-6d01ce1cf145a4d2f6ea5a2f (`mint-upgrade-info`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Information about upgrade paths". 
- mint-82ead54536f2e4992fff6c7e (`mint-x-icons`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Mint-X icon theme". 
- mint-630c4e50d42ba211a08f9d77 (`mint-y-icons`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Mint-Y icon theme". 
- mint-00bb082ab77e989d479936cf (`mintbackup`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Home Directory Backup Tool". 
- mint-ab22cb18c49db68a1534c914 (`mintchat`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Chat integration for Linux Mint". 
- mint-84e1a490ea3e626eefce4f62 (`mintdrivers`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Driver Manager". 
- mint-f317f28addb47d4d2bca3c31 (`mintinstall`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Software Manager". 
- mint-a96071724e1608e5483ddd7e (`mintlocale`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Language selection tool". 
- mint-4fca36170d78f0d8c50ce092 (`mintmenu`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Advanced MATE menu". 
- mint-89ad3a5355b6350559207f54 (`mintreport`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Troubleshooting tool for Linux Mint". 
- mint-48f72b2c7592e677f50e0ae2 (`mintsources`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Software Sources configuration tool". 
- mint-6ec5d52104d1b40a830ad8b9 (`mintstick`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "write .img and .iso files to USB sticks". 
- mint-f88a49d73a3914290364d16b (`mintsysadm`): https://mirrors.kernel.org/linuxmint-packages/dists/zena/main/binary-amd64/Packages.gz — "System Administration tool". 
- mint-41db892ee2dd7102853fcaf6 (`mintsystem`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Linux Mint System Base Package". 
- mint-12a1319e02bdf4e78b821954 (`mintupdate`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "The Linux Mint Update Manager". 
- mint-e2ebece2e063c2c7e658c7f0 (`mintwelcome`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Welcome screen for Linux Mint". 
- mint-5a04225dd007cc68ad3ad821 (`mobile-broadband-provider-info`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "database of mobile broadband service providers". 
- mint-135a7c66c18d49eb9e9ad208 (`modemmanager`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "D-Bus service for managing modems". 
- mint-da9a49bca1b8e451e6710602 (`mokutil`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "tools for manipulating machine owner keys". 
- mint-4b056b07482dd11f028ceb45 (`mount`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "tools for mounting and manipulating filesystems". 
- mint-694937eae28e31206e1cf504 (`mousetweaks`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "mouse accessibility enhancements for the GNOME desktop". 
- mint-2c999295f4066391e40c5d66 (`mscompress`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Microsoft "compress.exe/expand.exe" compatible (de)compressor". 
- mint-68ce521ca00bda343aca42f0 (`mtools`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Tools for manipulating MSDOS files". 
- mint-da924915dc3c0d04f575293d (`mtr-tiny`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Full screen ncurses traceroute tool". 
- mint-bfd56f20b6d9f8610a94619a (`muffin`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "window and compositing manager". 
- mint-697fbd758f1959606489bfb1 (`muffin-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "window and compositing manager (data files)". Archive https://mirrors.kernel.org/linuxmint-packages/pool/backport/m/muffin/muffin-common_6.4.1+xia_all.deb; inspected entries: `./usr/share/glib-2.0/schemas/org.cinnamon.muffin.gschema.xml`, `./usr/share/glib-2.0/schemas/org.cinnamon.muffin.wayland.gschema.xml`, `./usr/share/glib-2.0/schemas/org.cinnamon.muffin.x11.gschema.xml`.
- mint-0485f4f637e07234412cee1b (`muffin-dbg`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "window and compositing manager (debugging symbols)". 
- mint-cbe21a27d956eab31ed127a6 (`mythes-en-us`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "English (USA) Thesaurus for LibreOffice". 
- mint-276b0702f516d6a4ea800dbe (`nano`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "small, friendly text editor inspired by Pico". 
- mint-799ef1effb65ec56ca44deb1 (`nautilus-data`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "data files for nautilus". Archive https://archive.ubuntu.com/ubuntu/pool/main/n/nautilus/nautilus-data_46.0-0ubuntu2_all.deb; inspected entries: `./usr/share/glib-2.0/schemas/org.gnome.nautilus.gschema.xml`.
- mint-56d8278373afc1f4b2d04ca5 (`ncurses-base`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "basic terminal type definitions". 
- mint-0de8cbe41d6b94b34f85fc13 (`ncurses-bin`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "terminal-related programs and man pages". 
- mint-3140bf7a1d3de8ddeee31d53 (`nemo`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "file manager and graphical shell for Cinnamon". 
- mint-3c9b11bf75e7dcd4e8eccf6a (`nemo-data`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "data files for nemo". Archive https://mirrors.kernel.org/linuxmint-packages/pool/backport/n/nemo/nemo-data_6.4.5+xia_all.deb; inspected entries: `./usr/share/glib-2.0/schemas/org.nemo.gschema.xml`, (not published: external working record), (not published: external working record), (not published: external working record).
- mint-7edd253b844e18b8ddcdadd2 (`nemo-dbg`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "file manager and graphical shell for Cinnamon - debugging version". 
- mint-725bfae9233b84eef500ef28 (`nemo-emblems`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Change a folder or file emblem". 
- mint-ad6ab11929b4582fec776519 (`nemo-fileroller`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "File Roller integration for Nemo". 
- mint-ab427dd1e3ca101bdfd50577 (`nemo-preview`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "nemo-preview is a quick previewer for nemo". 
- mint-1c0289a0e411c32fb1f32a11 (`nemo-share`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Nemo extension to share folder using Samba". 
- mint-0c2dd565b5a0f2860b1c9c02 (`neofetch`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Shows Linux System Information with Distribution Logo". 
- mint-017053a23ed5537fa40f4acc (`net-tools`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "NET-3 networking toolkit". 
- mint-c38aafc369a9213ff55fd712 (`netavark`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Rust based network stack for containers". 
- mint-c0138f2eddacb5bdeb1d8d2d (`netbase`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Basic TCP/IP networking system". 
- mint-03ec5ffb618618da67a5fd44 (`netcat-openbsd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "TCP/IP swiss army knife". 
- mint-ab5142af2871375b18357ccf (`netplan-generator`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Declarative network configuration systemd-generator". 
- mint-f04355cf7d46f4f661532482 (`netplan.io`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Declarative network configuration for various backends". 
- mint-d09b73d4a113c804609d6e5a (`network-manager`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "network management framework (daemon and userspace tools)". 
- mint-71adb6e1255fa5a5c5656998 (`network-manager-config-connectivity-ubuntu`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "NetworkManager configuration to enable connectivity checking". 
- mint-8f8202b3e154445d8fb8e876 (`network-manager-gnome`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "network management framework (GNOME frontend)". 
- mint-d6dea8f159c32cad9af02165 (`network-manager-openvpn`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "network management framework (OpenVPN plugin core)". 
- mint-1e4f7fb6d39a10da99b1bc18 (`network-manager-openvpn-gnome`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "network management framework (OpenVPN plugin GNOME GUI)". 
- mint-85ffe364f68ba71f9d855551 (`network-manager-pptp`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "network management framework (PPTP plugin core)". 
- mint-984544409d4d4003028a9f49 (`network-manager-pptp-gnome`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "network management framework (PPTP plugin GNOME GUI)". 
- mint-c86079063a019a92aa93ea3e (`networkd-dispatcher`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Dispatcher service for systemd-networkd connection status changes". 
- mint-b71ee6b4b16834312c7a3e11 (`nftables`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Program to control packet filtering rules by Netfilter project". 
- mint-5179b7c18690aeac2c06e883 (`ntfs-3g`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "read/write NTFS driver for FUSE". 
- mint-16c1a6b1d520090ed3d380b7 (`nvidia-prime-applet`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "An applet for NVIDIA Prime". 
- mint-e36bb013ad81131670b49a98 (`ocl-icd-libopencl1`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Generic OpenCL ICD Loader". 
- mint-82f7d27edecb0df56a4a7537 (`onboard`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Simple On-screen Keyboard". 
- mint-e35f9cbd729535781d677c5c (`onboard-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Simple On-screen Keyboard (common files)". Archive https://mirrors.kernel.org/linuxmint-packages/pool/upstream/o/onboard/onboard-common_1.4.1+mint4+wilma_all.deb; inspected entries: `./usr/share/dbus-1/services/org.onboard.Onboard.service`, `./usr/share/doc/onboard/onboard-default-settings.gschema.override.example`, `./usr/share/doc/onboard/onboard-defaults.conf.example.gz`, (not published: external working record).
- mint-483181687d4226dff8464dc8 (`openprinting-ppds`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "OpenPrinting printer support - PostScript PPD files". 
- mint-dd7c73b4cc09007e162c0481 (`openssh-client`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "secure shell (SSH) client, for secure access to remote machines". 
- mint-8e0a1d8e7b6f313a2f0eb93e (`openssl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Secure Sockets Layer toolkit - cryptographic utility". 
- mint-2eb0a909f3443677e6df73ad (`openvpn`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "virtual private network daemon". 
- mint-d4509b1c45fe69a48753407b (`orca`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Scriptable screen reader". 
- mint-47bbe6be6ae1ea99bf4cce5e (`os-prober`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "utility to detect other OSes on a set of drives". 
- mint-b9fab2db36763b1dcb45e6c2 (`p11-kit`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "p11-glue utilities". 
- mint-8d0d9a19a34bbe71f852a487 (`p11-kit-modules`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "p11-glue proxy and trust modules". 
- mint-e5e46ec71c79edd74a05817d (`p7zip`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "transitional package". 
- mint-3cc441e16770ba7feebfb87b (`p7zip-full`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "transitional package". 
- mint-34b513885c56b9f4846e5454 (`packagekit`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Provides a package management service". 
- mint-fc9cca617452d08569e7353e (`packagekit-tools`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Provides PackageKit command-line tools". 
- mint-5af41a9f36332985c630e745 (`papirus-icon-theme`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Papirus open source icon theme for Linux". 
- mint-5fd3cb80f794ee951f643ac3 (`parted`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "disk partition manipulator". 
- mint-41bf5502c837fe2b5194c558 (`passt`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "user-mode networking daemons for virtual machines and namespaces". 
- mint-532126679c03c6332014197e (`passwd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "change and administer password and group data". 
- mint-c493ee2f6782ddb5af1fcb0a (`patch`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Apply a diff file to an original". 
- mint-9cc90be4bb452bb3191884a8 (`patchutils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Utilities to work with patches". 
- mint-5462275c4788020f9e36154c (`pci.ids`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "PCI ID Repository". 
- mint-fda1d3579ac56dc2a206dd4d (`pciutils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "PCI utilities". 
- mint-d45135d069bb9e307b1dac98 (`pcmciautils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "PCMCIA utilities for Linux 2.6". 
- mint-3b6fdf4eb18c896839c4d852 (`perl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "This package contains the Perl interpreter and core modules.". 
- mint-9141c93e39245e9cd8120977 (`perl-base`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "minimal Perl system". 
- mint-4611c56d6edcd7a4cbb1a28d (`perl-modules-5.38`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Core Perl modules". 
- mint-61506276b93614c6294d721f (`perl-openssl-defaults`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "version compatibility baseline for Perl OpenSSL packages". 
- mint-384cdddb100a7fee98844fe2 (`pinentry-curses`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "curses-based PIN or pass-phrase entry dialog for GnuPG". 
- mint-36b3ceb59773dc16e7143a36 (`pinentry-gnome3`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GNOME 3 PIN or pass-phrase entry dialog for GnuPG". 
- mint-1186b00ba13d19de8bfa641c (`pipewire`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "audio and video processing engine multimedia server". 
- mint-119aec4e9403c188c3f7de64 (`pipewire-alsa`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "PipeWire ALSA plugin, for ALSA applications to output via PipeWire". 
- mint-c0787986efe6c9b79d180892 (`pipewire-audio`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "recommended set of PipeWire packages for a standard audio desktop use". 
- mint-00498cfd9071eff9ca6fb269 (`pipewire-bin`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "PipeWire multimedia server - programs". 
- mint-56e73c458a7f6be382205555 (`pipewire-pulse`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "PipeWire PulseAudio daemon". 
- mint-3b4a0216d539064ab0b68934 (`pix`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "image viewer and browser". 
- mint-11ea76b71b17cb2a11ce5b11 (`pix-data`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "image viewer and browser - arch-independent files". Archive https://mirrors.kernel.org/linuxmint-packages/pool/backport/p/pix/pix-data_3.4.7+zara_all.deb; inspected entries: `./usr/share/glib-2.0/schemas/org.x.pix.catalogs.gschema.xml`, `./usr/share/glib-2.0/schemas/org.x.pix.change-date.gschema.xml`, `./usr/share/glib-2.0/schemas/org.x.pix.comments.gschema.xml`, `./usr/share/glib-2.0/schemas/org.x.pix.contact-sheet.gschema.xml`.
- mint-64c62b8bf5b610e37b30e296 (`pix-dbg`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "image viewer and browser - debugging symbols". 
- mint-8b0b47f137537e7687b1fe6f (`pkexec`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "run commands as another user with polkit authorization". 
- mint-4f07c1852c4f7870063c16db (`pkg-config`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "manage compile and link flags for libraries (transitional package)". 
- mint-1f153e9f200886e789238249 (`pkgconf`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "manage compile and link flags for libraries". 
- mint-12fb64b034f3623851174869 (`pkgconf-bin`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "manage compile and link flags for libraries (binaries)". 
- mint-7c5959566ec114da047ce47d (`plocate`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "much faster locate". 
- mint-97a5e225e9a6052eb7a9cc21 (`plymouth`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "boot animation, logger and I/O multiplexer". 
- mint-82a64197f2a0678574114f9c (`plymouth-label`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "boot animation, logger and I/O multiplexer - label control". 
- mint-24a16618d485340831275abc (`plymouth-theme-spinner`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "boot animation, logger and I/O multiplexer - spinner theme". 
- mint-0a7c3145c6f26bcc948cb292 (`plymouth-theme-ubuntu-text`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "boot animation, logger and I/O multiplexer - ubuntu text theme". 
- mint-d0b12edea3dbeb345c16716a (`pm-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "utilities and scripts for power management". 
- mint-bb0d5634684c514b97cb6a79 (`podman`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "tool to manage containers and pods". 
- mint-1125d8187dc51c0b4ebc07e1 (`policykit-1`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "transitional package for polkitd and pkexec". 
- mint-781e41078f9585d0ed991e0d (`policykit-1-gnome`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "authentication agent for PolicyKit". 
- mint-941fe040b0ed9278c5e4abaf (`policykit-desktop-privileges`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "run common desktop actions without password". 
- mint-88b0ba9eec3e43fc5de25a7d (`polkitd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "framework for managing administrative policies and privileges". 
- mint-4a572b8695fa7140761d2d1f (`poppler-data`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "encoding data for the poppler PDF rendering library". 
- mint-02911b1b8cdceb336abfdbb0 (`poppler-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "PDF utilities (based on Poppler)". 
- mint-23034ddca52c724cce685b62 (`power-profiles-daemon`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Makes power profiles handling available over D-Bus.". 
- mint-09881b5a4d38d9ee5abdb562 (`powermgmt-base`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "common utils for power management". 
- mint-504f83838ea0f361e8322e47 (`ppp`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Point-to-Point Protocol (PPP) - daemon". 
- mint-492a04f18262d87f035c0de5 (`pptp-linux`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Point-to-Point Tunneling Protocol (PPTP) Client". 
- mint-a33aa0ca487d4320d1e4ec6c (`printer-driver-brlaser`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer driver for (some) Brother laser printers". 
- mint-c46e38889ef2b94dc2eb58f3 (`printer-driver-c2esp`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer driver for Kodak ESP AiO color inkjet Series". 
- mint-9b81e8235ace2c1c2956202e (`printer-driver-foo2zjs`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer driver for ZjStream-based printers". 
- mint-efe7b0e7b5c41bd0f541b877 (`printer-driver-foo2zjs-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer driver for ZjStream-based printers - common files". Archive https://archive.ubuntu.com/ubuntu/pool/main/f/foo2zjs/printer-driver-foo2zjs-common_20200505dfsg0-2ubuntu6_all.deb; inspected entries: `./usr/bin/foo2ddst-wrapper`, `./usr/bin/foo2hbpl2-wrapper`, `./usr/bin/foo2hiperc-wrapper`, `./usr/bin/foo2hp2600-wrapper`.
- mint-8760dbb00f251d2f3474e926 (`printer-driver-gutenprint`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer drivers for CUPS". 
- mint-97044758d9df26da00124a2c (`printer-driver-hpcups`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "HP Linux Printing and Imaging - CUPS Raster driver (hpcups)". 
- mint-cdb5438fb82f6a60e3db23ba (`printer-driver-m2300w`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer driver for Minolta magicolor 2300W/2400W color laser printers". 
- mint-d1abeb1635c22bc85272ddc9 (`printer-driver-min12xxw`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer driver for KonicaMinolta PagePro 1[234]xxW". 
- mint-24577aec6bebbacf47beaae5 (`printer-driver-pnm2ppa`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer driver for HP-GDI printers". 
- mint-09613ec98a5f85c0d49570fe (`printer-driver-postscript-hp`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "HP Printers PostScript Descriptions". 
- mint-870e3edea384cf319aa11059 (`printer-driver-ptouch`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer driver Brother P-touch label printers". 
- mint-f5604e1f5969022917bd617e (`printer-driver-pxljr`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer driver for HP Color LaserJet 35xx/36xx". 
- mint-bae2a54fe408ebe6a6de1be9 (`printer-driver-sag-gdi`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "printer driver for Ricoh Aficio SP 1000s/SP 1100s". 
- mint-9077cfeb39963e0032f04528 (`printer-driver-splix`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Driver for Samsung and Xerox SPL2 and SPLc laser printers". 
- mint-49e5c12e71397457615996ed (`procps`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "/proc file system utilities". 
- mint-eb723c5ae080bdd52645fa90 (`psmisc`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "utilities that use the proc file system". 
- mint-776e4c47009d316c25544098 (`publicsuffix`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "accurate, machine-readable list of domain name suffixes". 
- mint-89a5f657411ad54a0b4a21f6 (`pulseaudio-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Command line tools for the PulseAudio sound server". 
- mint-d75c910ab047073a2f894ce0 (`python-apt-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python interface to libapt-pkg (locales)". 
- mint-fe458f2cf3dbe28278730c23 (`python-babel-localedata`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "tools for internationalizing Python applications - locale data files". 
- mint-62b65b8600cb487a09f23cc5 (`python-nemo`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Python binding for Nemo components". 
- mint-005b8160a306ae4e41f82fed (`python-tinycss2-common`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Low-level CSS parser (test data)". 
- mint-7cf1b3c6be667b4f1f2ff354 (`python3`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "interactive high-level object-oriented language (default python3 version)". 
- mint-f2caf4782203506e094b7cb5 (`python3-apport`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 library for Apport crash report handling". 
- mint-0bbf1dd67e7b12a88901aa98 (`python3-apt`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 interface to libapt-pkg". 
- mint-67145c03ce3b4c3d9d954ee1 (`python3-aptdaemon`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 module for the server and client of aptdaemon". 
- mint-cba4af808189dbfc0dd575ae (`python3-aptdaemon.gtk3widgets`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 GTK+ 3 widgets to run an aptdaemon client". 
- mint-88c42173f40b7ebe33b2220c (`python3-babel`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "tools for internationalizing Python applications - Python 3.x". 
- mint-8ee3131943c912a32bd833a9 (`python3-blinker`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Fast, simple object-to-object and broadcast signaling (Python3)". 
- mint-6e5ca3be110095b05087996e (`python3-brlapi`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Braille display access via BRLTTY - Python3 bindings". 
- mint-142e7fdd66fc576f07ade5d1 (`python3-brotli`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "lossless compression algorithm and format (Python 3 version)". 
- mint-68c9513fce04a811fdaab13a (`python3-bs4`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "error-tolerant HTML parser for Python 3". 
- mint-0a89337808532777718c1e52 (`python3-cairo`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python3 bindings for the Cairo vector graphics library". 
- mint-bc303a6452c6289048b62bc1 (`python3-certifi`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "root certificates for validating SSL certs and verifying TLS hosts (python3)". 
- mint-c1037d93056eb72620118b9e (`python3-cffi-backend`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Foreign Function Interface for Python 3 calling C code - runtime". 
- mint-1af2a8d2c2d46ae37116da33 (`python3-chardet`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Universal Character Encoding Detector (Python3)". 
- mint-8e04e80d975bb4ad7101bcfa (`python3-click`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Wrapper around optparse for command line utilities - Python 3.x". 
- mint-84d725eabe376ff52a34a233 (`python3-colorama`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Cross-platform colored terminal text in Python - Python 3.x". 
- mint-9b375790d75ef79048513c4f (`python3-commandnotfound`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 bindings for command-not-found.". 
- mint-95883e706eb23f7a3cea218e (`python3-configobj`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "simple but powerful config file reader and writer for Python 3". 
- mint-cb5a75cdc3fcec10e9ce1e51 (`python3-cryptography`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python library exposing cryptographic recipes and primitives (Python 3)". 
- mint-32cbef5600df8b61424c359e (`python3-cups`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python3 bindings for CUPS". 
- mint-731675ed6d6d928685dfafb9 (`python3-cupshelpers`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python utility modules around the CUPS printing system". 
- mint-33c769521cef86a6a49da508 (`python3-dbus`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "simple interprocess messaging system (Python 3 interface)". 
- mint-8fd66913a712e80838b656bf (`python3-debian`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 modules to work with Debian-related data formats". 
- mint-c7d1969c6117e78589e66a9e (`python3-defer`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Small framework for asynchronous programming (Python 3)". 
- mint-81b49b9c7ce06c0e0d63aabf (`python3-deprecation`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Library to handle automated deprecations". 
- mint-c8d466a1ed1576a11152b0e6 (`python3-dill`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Serialize all of Python 3 (almost)". 
- mint-08511a33256c8e72225a61e9 (`python3-distro`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Linux OS platform information API". 
- mint-322e6afde4c5db14494fc7be (`python3-eyed3`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Python module for id3-tags manipulation (Python 3 version)". 
- mint-bcd57eec13208737b4332988 (`python3-filelock`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "platform independent file locking module". 
- mint-942db62b49c8742f5994a011 (`python3-filetype`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Infer file type and MIME type of any file/buffer". 
- mint-813f8c2dabfc36694604beec (`python3-gdbm`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GNU dbm database support for Python 3.x". 
- mint-451acb08bbac06d3a572bc25 (`python3-gi`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 bindings for gobject-introspection libraries". 
- mint-4bb8f3c0a17ff88dc18cf1c8 (`python3-gi-cairo`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 Cairo bindings for the GObject library". 
- mint-30d3ae9cbb5b144f68f1d1fe (`python3-gnupg`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Python wrapper for the GNU Privacy Guard (Python 3.x)". 
- mint-b6546e483d5eeabbd2f6c184 (`python3-html2text`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Python module for converting HTML to Markdown text (Python3 version)". 
- mint-a231610c1f79cace35c12cc1 (`python3-httplib2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "comprehensive HTTP client library written for Python3". 
- mint-ce528a381b0ff7d15bf0dc9e (`python3-ibus-1.0`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Intelligent Input Bus - introspection overrides for Python (Python 3)". 
- mint-b185fcfe336d2025d037135f (`python3-icu`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 extension wrapping the ICU C++ API". 
- mint-18a966370ffb36ac03644c4c (`python3-idna`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python IDNA2008 (RFC 5891) handling (Python 3)". 
- mint-e31ee8e9db0e5e2759ff432d (`python3-ifaddr`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Pure Python implementation for detecting IP addresses". 
- mint-8016dd66a79a05dbb3ceb93b (`python3-jwt`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 implementation of JSON Web Token". 
- mint-c435c856d3c256a90929177e (`python3-launchpadlib`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Launchpad web services client library (Python 3)". 
- mint-6284d9537752b59338fe6f40 (`python3-lazr.restfulclient`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "client for lazr.restful-based web services (Python 3)". 
- mint-3d6d337f4b48699a266a86a7 (`python3-lazr.uri`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "library for parsing, manipulating, and generating URIs". 
- mint-8aa588f248e5b99270b73553 (`python3-ldb`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 bindings for LDB". 
- mint-6e755d8356b8de2a7020946f (`python3-libevdev`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Python 3 wrapper for libevdev". 
- mint-024d6881b4a9fe043f4eb567 (`python3-louis`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python bindings for liblouis". 
- mint-381ba46175f7adbd462f105a (`python3-lxml`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "pythonic binding for the libxml2 and libxslt libraries". 
- mint-720bc48427b54cf769b5830f (`python3-mako`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "fast and lightweight templating for the Python 3 platform". 
- mint-1b516cfd9f219ec4e023063b (`python3-markdown`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "text-to-HTML conversion library/tool (Python 3 version)". 
- mint-1d492c5522ff2022433a90b3 (`python3-markdown-it`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python port of markdown-it and some its associated plugins". 
- mint-899bd6c82ec0d77126cddd9a (`python3-markupsafe`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "HTML/XHTML/XML string library". 
- mint-c1d404391cba3bf45cc7853f (`python3-mdurl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python port of the JavaScript mdurl package". 
- mint-44fe31aabc9e10e57448ad0e (`python3-minimal`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "minimal subset of the Python language (default python3 version)". 
- mint-28673c77b17a9a9fe8cb810b (`python3-multiprocess`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "better multiprocessing and multithreading in Python". 
- mint-c271d09580b11bd451f224bc (`python3-mutagen`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "audio metadata editing library (Python 3)". 
- mint-904684ac8a5c7b0159ca66b8 (`python3-nacl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python bindings to libsodium (Python 3)". 
- mint-a4b3a2cd1d6eea1604c8cbca (`python3-netaddr`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "manipulation of various common network address notations (Python 3)". 
- mint-36874967a0021b316e47696f (`python3-netifaces`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "portable network interface information - Python 3.x". 
- mint-41673db08739d82218d475d3 (`python3-netplan`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Declarative network configuration Python bindings". 
- mint-8554fd93a04f0152c31602c1 (`python3-oauthlib`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "generic, spec-compliant implementation of OAuth for Python3". 
- mint-18942bd2a92cd76a3669af76 (`python3-packaging`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "core utilities for python3 packages". 
- mint-77b7da4ae6a6571e7cbda5ce (`python3-pam`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python interface to the PAM library". 
- mint-359a73c6664145b39049c9fc (`python3-parted`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Python 3 interface for libparted". 
- mint-11dff5147ca6577093f08261 (`python3-pexpect`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 module for automating interactive applications". 
- mint-742888505eae4885ac726be4 (`python3-pil`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python Imaging Library (Python3)". 
- mint-ed18a393154983969e25ef9a (`python3-pkg-resources`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Package Discovery and Resource Access using pkg_resources". 
- mint-b3ffd37e40e692336039bb14 (`python3-png`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Pure Python PNG Reader/Writer (Python 3)". 
- mint-9395787096f7fbb0c032e209 (`python3-problem-report`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 library to handle problem reports". 
- mint-fa82f0aa3109acc27a2ea25a (`python3-psutil`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "module providing convenience functions for managing processes (Python3)". 
- mint-803cfc27e08cc8471b04b87c (`python3-ptyprocess`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Run a subprocess in a pseudo terminal from Python 3". 
- mint-c6f52a1d19efdc3283f3b691 (`python3-pyasyncore`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "asyncore for Python 3.12 onwards". 
- mint-0ae966c0cb3669678df7b1a0 (`python3-pyatspi`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Assistive Technology Service Provider Interface - Python3 bindings". 
- mint-8f5795ddb387b053b27b5e32 (`python3-pycryptodome`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "cryptographic Python library (Python 3)". 
- mint-aea976c16c2c439296485fde (`python3-pycurl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python bindings to libcurl (Python 3)". 
- mint-688c3276f07aa36a167e7e64 (`python3-pyelftools`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "pure-python3 library for parsing ELF and DWARF". 
- mint-c9224f4e83c44446dbad4505 (`python3-pygments`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "syntax highlighting package written in Python 3". 
- mint-5c43485e4d022fc7637d1451 (`python3-pyinotify`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "simple Linux inotify Python bindings". 
- mint-989cd5120396226c9e658b36 (`python3-pyparsing`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "alternative to creating and executing simple grammars - Python 3.x". 
- mint-b4df061e591a6bc5706eb325 (`python3-pyudev`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python3 bindings for libudev". 
- mint-db166bd94bfd6c3f5bcc8e8b (`python3-qrcode`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "QR Code image generator library - Python 3.x". 
- mint-ce13d68a5042699ce84a0b2e (`python3-repolib`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/import/binary-amd64/Packages.gz — "Repository Management for APT in Python (Python 3)". 
- mint-5471e9e965f01beb04f67788 (`python3-requests`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "elegant and simple HTTP library for Python3, built for human beings". 
- mint-d07c1cedcbc49df11f07b32d (`python3-requests-file`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "File transport adapter for Requests - Python 3.X". 
- mint-f069c83178d1736571ca4ed6 (`python3-rich`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "render rich text, tables, progress bars, syntax highlighting, markdown and more". 
- mint-171782191733ff6cbed3bef1 (`python3-samba`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 bindings for Samba". 
- mint-9dcd6a4096fd8a96b549bee2 (`python3-setproctitle`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Setproctitle implementation for Python 3". 
- mint-241a9a5abb74818dff8f614e (`python3-six`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 2 and 3 compatibility library". 
- mint-519802b3c24f6b248448a5ce (`python3-soupsieve`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "modern CSS selector implementation for BeautifulSoup (Python 3)". 
- mint-cb3bae5352133a62f3427ce9 (`python3-speechd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python interface to Speech Dispatcher". 
- mint-6024c9bb6e4b20b0faa41be5 (`python3-systemd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 bindings for systemd". 
- mint-c9214648f328b3465c13f4e2 (`python3-talloc`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "hierarchical pool based memory allocator - Python3 bindings". 
- mint-82273fc728a3a7fd6dac6ff2 (`python3-tdb`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python3 bindings for TDB". 
- mint-4cce8eed9b91ed01de913a00 (`python3-tinycss2`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Low-level CSS parser (Python3 version)". 
- mint-2b2793496ab80f927f944044 (`python3-tldextract`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Python library for separating TLDs". 
- mint-22381f65570ee263718e58f5 (`python3-typing-extensions`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Backported and Experimental Type Hints for Python". 
- mint-960e6bb6738c4d1161b6af7c (`python3-tz`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python3 version of the Olson timezone database". 
- mint-3a23c064cc2ce024743b50bb (`python3-unidecode`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "ASCII transliterations of Unicode text (Python 3 module)". 
- mint-9f7759283d7ac5887a43b04f (`python3-uno`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python-UNO bridge". 
- mint-5f7ea2e842d5d7bd05ace7ae (`python3-urllib3`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "HTTP library with thread-safe connection pooling for Python3". 
- mint-8a2eed9011c5c12d54202405 (`python3-wadllib`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 library for navigating WADL files". 
- mint-fa1caa429c9ab0fb8527ed00 (`python3-webencodings`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python implementation of the WHATWG Encoding standard". 
- mint-aac1b6506329afb87d13295e (`python3-websockets`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "implementation of the WebSocket Protocol (RFC 6455)". 
- mint-2e02e27ea867e280a9d8d3b1 (`python3-xapp`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Python 3 XApp library". 
- mint-f7dce1d369292fc6cc980372 (`python3-xdg`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Python 3 library to access freedesktop.org standards". 
- mint-1bc5332110b61a32b8154252 (`python3-xkit`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "library for the manipulation of xorg.conf files (Python 3)". 
- mint-4e0fd4028980cd0cf7102b10 (`python3-xlib`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "interface for Python 3 to the X11 protocol". 
- mint-5e3f84ae457fb277ad359614 (`python3-xlrd`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "extract data from Microsoft Excel spreadsheet files (Python3 version)". 
- mint-4b5bf550a538e35ad173ac71 (`python3-yaml`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "YAML parser and emitter for Python3". 
- mint-fbc273a65e9acdb88c8a3ba8 (`python3.12`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Interactive high-level object-oriented language (version 3.12)". 
- mint-09e0234e1272c8cc1ff7f624 (`python3.12-minimal`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Minimal subset of the Python language (version 3.12)". 
- mint-4d53d21e0b3d00ab83fd6e58 (`qt5-gtk-platformtheme`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Qt 5 GTK+ 3 platform theme". 
- mint-e1dd53f025aabc039c5ca0de (`qt5-gtk2-platformtheme`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Qt 5 extra widget styles - GTK+ 2 Platform theme". 
- mint-71778e4fdc544f054602c2c0 (`qt5-style-plugin-cleanlooks`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Qt 5 extra widget styles - Cleanlooks". 
- mint-696079887be7d69dbe1b0ec9 (`qt5-style-plugin-motif`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Qt 5 extra widget styles - Motif". 
- mint-d65764e64a5287e50ed956f9 (`qt5-style-plugin-plastique`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Qt 5 extra widget styles - Plastique". 
- mint-8a371d8839102003d120caed (`qt5-style-plugins`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Qt 5 extra widget styles". 
- mint-d9a28359736350879dd89ffc (`qttranslations5-l10n`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "translations for Qt 5". 
- mint-d1f7ccb24caf7ba11fc20aa5 (`rdate`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "sets the system's date from a remote host with network time protocol". 
- mint-f8dd8a8684649a0247de6294 (`readline-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GNU readline and history libraries, common files". Archive https://archive.ubuntu.com/ubuntu/pool/main/r/readline/readline-common_8.2-4build1_all.deb; inspected entries: `./usr/share/doc/readline-common/inputrc.arrows`, `./usr/share/readline/inputrc`.
- mint-f278f644e57b7c7332269d8a (`reiserfsprogs`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "User-level tools for ReiserFS filesystems". 
- mint-8ad0fbf7639bb8af81715fc0 (`rename`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Perl extension for renaming multiple files". 
- mint-cb7d844801799cc5b9c5ac3d (`rfkill`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "tool for enabling and disabling wireless devices". 
- mint-a823e8cb31c60e632e06d5db (`rhythmbox`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "music player and organizer for GNOME". 
- mint-b24f59ed65e9bd783fdb01b4 (`rhythmbox-data`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "data files for rhythmbox". Archive https://archive.ubuntu.com/ubuntu/pool/main/r/rhythmbox/rhythmbox-data_3.4.7-2ubuntu6_all.deb; inspected entries: (not published: external working record), `./usr/share/dbus-1/services/org.gnome.Rhythmbox3.service`, `./usr/share/glib-2.0/schemas/org.gnome.rhythmbox.gschema.xml`.
- mint-73217a2361552980ce5a3434 (`rhythmbox-plugin-tray-icon`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "A tray icon plugin for rhythmbox music player". 
- mint-b050409a55bc527db0ca8cf1 (`rhythmbox-plugins`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "plugins for rhythmbox music player". 
- mint-a8fd2f8ffd3a9dd3687782af (`rpcsvc-proto`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "RPC protocol compiler and definitions". 
- mint-c59be9d706d0ca5a64376172 (`rsync`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "fast, versatile, remote (and local) file-copying tool". 
- mint-d9b01cea4189d1576ac405ed (`rsyslog`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "reliable system and kernel logging daemon". 
- mint-10bc6681469afebdef895177 (`rtkit`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Realtime Policy and Watchdog Daemon". 
- mint-d5c5e6b170ac78983c84c671 (`samba-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "common files used by both the Samba server and client". Archive https://archive.ubuntu.com/ubuntu/pool/main/s/samba/samba-common_4.19.5+dfsg-4ubuntu9_all.deb; inspected entries: `./usr/share/doc/samba-common/examples/smb.conf.default`, `./usr/share/samba/smb.conf`.
- mint-def000f9770c314940c97286 (`samba-common-bin`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Samba common files used by both the server and the client". 
- mint-bb7a8648c94efb41d2963ab1 (`samba-libs`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Samba core libraries". 
- mint-f32e1a1ec132b42ebc522868 (`sane-airscan`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "SANE backend for AirScan (eSCL) and WSD document scanner". 
- mint-f895de76e6ebf3ea4a152dc7 (`sane-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "API library for scanners -- utilities". 
- mint-d455610e1bf49a5d4f3367b3 (`sbsigntool`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Tools to manipulate signatures on UEFI binaries and drivers". 
- mint-5840b826eccb00fe34526fba (`seahorse`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GNOME front end for GnuPG". 
- mint-495dccc52fcedfaf0d88e99a (`secureboot-db`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Secure Boot updates for DB and DBX". 
- mint-cc126b101b0ed8687c98a049 (`sed`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GNU stream editor for filtering/transforming text". 
- mint-c1b08ae6fd6fad0327bc30ab (`sensible-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Utilities for sensible alternative selection". 
- mint-50d4c34b7ffec81a3735aba9 (`session-migration`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Tool to migrate in user session settings". 
- mint-c91198101e4c2623d46b5a8c (`sgml-base`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "SGML infrastructure and SGML catalog file support". 
- mint-83f70d92b33dc9a05f18fa66 (`sgml-data`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "common SGML and XML data". 
- mint-3efe7c7fcb41029cad42ee77 (`shared-mime-info`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "FreeDesktop.org shared MIME database and spec". 
- mint-3c4374fd749d66f2137b1758 (`shim-signed`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Secure Boot chain-loading bootloader (Microsoft-signed binary)". 
- mint-c20e87607de5e5c07f5b43a1 (`simple-scan`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Simple Scanning Utility". 
- mint-e1f0f906a6b9960e13cd6a1b (`slick-greeter`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Slick-looking LightDM greeter". 
- mint-790c3516e883cd0981ea48d9 (`slirp4netns`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "User-mode networking for unprivileged network namespaces". 
- mint-e830238a165faaf16283f95d (`smbclient`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "command-line SMB/CIFS clients for Unix". 
- mint-c724979d072923946fba7d05 (`sound-theme-freedesktop`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "freedesktop.org sound theme". 
- mint-8c487f776b6a66a40113648a (`speech-dispatcher`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Common interface to speech synthesizers". 
- mint-6c46dfe312977b3d3c585291 (`speech-dispatcher-audio-plugins`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Speech Dispatcher: Audio output plugins". 
- mint-ab0af6501828626a6630f60a (`speech-dispatcher-espeak-ng`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Speech Dispatcher: Espeak-ng output module". 
- mint-73fdff64588bbdad18554a02 (`squashfs-tools`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Tool to create and append to squashfs filesystems". 
- mint-b847f6703d81d5cc1d01f9fc (`ssl-cert`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "simple debconf wrapper for OpenSSL". 
- mint-fda72642a699b8a17c5fd156 (`sticky`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Sticky Notes app". 
- mint-5e1387f5416db3badd95a123 (`strace`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "System call tracer". 
- mint-ea2d540c7e0729459a691bcf (`streamer`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "television capture tool (images/movies)". 
- mint-f104273e3880a4a97ac44df9 (`sudo`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Provide limited super user privileges to specific users". 
- mint-1a04c2efcb121fe4751b0e22 (`switcheroo-control`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "D-Bus service to check the availability of dual-GPU". 
- mint-eeda94d1119519cfe20b8c1a (`syslinux`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "collection of bootloaders (DOS FAT and NTFS bootloader)". 
- mint-b23f0aab8660a8ba3e5f0f31 (`syslinux-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "collection of bootloaders (common)". Archive https://archive.ubuntu.com/ubuntu/pool/main/s/syslinux/syslinux-common_6.04~git20190206.bf6db5b4+dfsg1-3ubuntu3_all.deb; inspected entries: `./usr/lib/syslinux/modules/bios/cat.c32`, `./usr/lib/syslinux/modules/bios/chain.c32`, `./usr/lib/syslinux/modules/bios/cmd.c32`, `./usr/lib/syslinux/modules/bios/cmenu.c32`.
- mint-ef35df24da8db727a0178c71 (`syslinux-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "collection of bootloaders (utilities)". 
- mint-c3190f19aca1a944376efe87 (`system-config-printer`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "graphical interface to configure the printing system". 
- mint-da81a9251a22cd2e513ee48e (`system-config-printer-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "backend and the translation files for system-config-printer". 
- mint-599f0c92c6ed2614231b71dc (`system-config-printer-udev`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Utilities to detect and configure printers automatically". 
- mint-98edfa954d2e1d848f843be1 (`system-tools-backends`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "System Tools to manage computer configuration -- scripts". 
- mint-cb23aa1c1d78e3f94323138e (`systemd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "system and service manager". 
- mint-e34698d1ccc968eb2cc3cfdc (`systemd-coredump`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "tools for storing and retrieving coredumps". 
- mint-14e4ef55d0c999091494e411 (`systemd-dev`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "systemd development files". 
- mint-b45f676681fc354259939508 (`systemd-hwe-hwdb`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "udev rules for hardware enablement (HWE)". 
- mint-ce8481869884cec8f02c1506 (`systemd-resolved`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "systemd DNS resolver". 
- mint-12e7ad2163fcb25cdc89fbc4 (`systemd-sysv`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "system and service manager - SysV compatibility symlinks". 
- mint-442812ead0b1c1d6dd2ad943 (`systemd-timesyncd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "minimalistic service to synchronize local time with NTP servers". 
- mint-e845fda0fb200d5d6cd8d5ef (`sysvinit-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "System-V-like utilities". 
- mint-e7dcdc4be2d0b3f2f102a67e (`t1utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Collection of simple Type 1 font manipulation programs". 
- mint-33890bbde3ad0048af487de8 (`tar`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GNU version of the tar archiving utility". 
- mint-447ffa22ad707cbd4a2bc47a (`tcl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Tool Command Language (default version) - shell". 
- mint-0bd4b01ffa6e2d36ed7a5ffe (`tcl8.6`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Tcl (the Tool Command Language) v8.6 - shell". 
- mint-207e185c0ef6a0f7a7bb54d9 (`tcpdump`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "command-line network traffic analyzer". 
- mint-ed7808a3a1bd18b85f5b4e5d (`telnet`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "transitional dummy package for inetutils-telnet default switch". 
- mint-002feba7c933b943340b5583 (`thermald`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Thermal monitoring and controlling daemon". 
- mint-6b36a3d8b1affe20e71c7880 (`thingy`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Document Manager". 
- mint-0e33df480b6c7df63fe4ce00 (`thunderbird`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Email, RSS and newsgroup client with integrated spam filter". 
- mint-364051b8277d58fbbf204245 (`thunderbird-locale-en`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "English language packs for Thunderbird". 
- mint-07c707625517cdd020cc62d0 (`thunderbird-locale-en-us`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Transitional package for Thunderbird language packs.". 
- mint-f6020224c45b9c9fa5389537 (`time`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GNU time program for measuring CPU resource usage". 
- mint-5687d19e6d9ba3cd7ac941af (`timeshift`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "System restore utility". 
- mint-33fdfacc4de2e666db1892d2 (`tnftp`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "enhanced ftp client". 
- mint-2930693153da9d4077debd9e (`touchegg`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/import/binary-amd64/Packages.gz — "Multi-touch gesture recognizer". 
- mint-327eaf6fec88b664c4edd16b (`tpm-udev`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "udev rules for TPM modules". 
- mint-3419c485bbc415287fa3601b (`transmission-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "lightweight BitTorrent client (common files)". Archive https://mirrors.kernel.org/linuxmint-packages/pool/upstream/t/transmission/transmission-common_4.0.5-1build5mint2+mint22_amd64.deb; inspected entries: `./usr/share/transmission/public_html/index.html`.
- mint-3f709cbd4da1b3cda97b1d1d (`transmission-gtk`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "lightweight BitTorrent client (GTK+ interface)". 
- mint-834c14e84040a0295661fbe2 (`tzdata`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "time zone and daylight-saving time data". 
- mint-224d1a39f1d0649a9ac98390 (`tzdata-legacy`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "time zone data for TAI minus ten seconds". 
- mint-88227ec040d89c24cd82e6c8 (`ubuntu-dbgsym-keyring`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GnuPG keys of the Ubuntu Debug Symbols Archive". 
- mint-b5e748f57cf1ec3407a5515c (`ubuntu-drivers-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Detect and install additional Ubuntu driver packages". 
- mint-4f5c80f4825cd0df76ebab30 (`ubuntu-keyring`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GnuPG keys of the Ubuntu archive". 
- mint-11aae2ec3c65791e6a33f4fd (`ubuntu-mono`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Ubuntu Mono Icon theme". 
- mint-32e981bbfcb0baa1e9f5592d (`ubuntu-system-adjustments`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Adjustments to the Ubuntu package base". Archive https://mirrors.kernel.org/linuxmint-packages/pool/main/u/ubuntu-system-adjustments/ubuntu-system-adjustments_2025.05.20-zara_all.deb; inspected entries: `./etc/NetworkManager/conf.d/ubuntu-system-adjustments.conf`, `./etc/apt/apt.conf.d`, `./etc/apt/apt.conf.d/00mint`, `./etc/sysctl.d/20-apparmor-mint.conf`.
- mint-9077b74547c1c4d6bbd12c9a (`ucf`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Update Configuration File(s): preserve user changes to config files". 
- mint-7e8c9cdb9057d41768de349f (`udev`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "/dev/ and hotplug management daemon". 
- mint-cf8430bf6817b817c6c3f7f1 (`udisks2`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "D-Bus service to access and manipulate storage devices". 
- mint-0aa3d88de8b64b1420ff08c5 (`ufw`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "program for managing a Netfilter firewall". 
- mint-3d0f6689a804710f91d2ae40 (`uidmap`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "programs to help use subuids". 
- mint-e09e7abf65bf56e5e38dfc7e (`uno-libs-private`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "LibreOffice UNO runtime environment -- private libraries used by public ones". 
- mint-4dd0bf2f4af866f562ac263f (`untex`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "remove LaTeX commands from input". 
- mint-2907398b720377ff2b8381ef (`unzip`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "De-archiver for .zip files". 
- mint-4c5f0f57a2d487a75945cbf2 (`update-inetd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "inetd configuration file updater". 
- mint-9c7685f7b975c99f91a6fc5e (`upower`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "abstraction for power management". 
- mint-ce83bf02d1ca7fc184883cbd (`ure`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "LibreOffice UNO runtime environment". 
- mint-b4da97e66efaefe734ddc5e2 (`usb-modeswitch`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "mode switching tool for controlling "flip flop" USB devices". 
- mint-8f2a9f7703e55326c4cbac18 (`usb-modeswitch-data`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "mode switching data for usb-modeswitch". 
- mint-53b4f1fdd00f31004638f092 (`usb.ids`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "USB ID Repository". 
- mint-d71372938b2fc9c5a0eac842 (`usbmuxd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "USB multiplexor daemon for iPhone and iPod Touch devices". 
- mint-6c35651d0ed5551c5e778a35 (`usbutils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Linux USB utilities". 
- mint-6d2e6e5664a50aadebcadf60 (`user-setup`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Set up initial user and password". 
- mint-6589732ad16c2bb64e384f20 (`util-linux`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "miscellaneous system utilities". 
- mint-62551d871048f524d49d8da0 (`uuid-runtime`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "runtime components for the Universally Unique ID library". 
- mint-224e806a9e786a6e195a3fb8 (`va-driver-all`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Video Acceleration (VA) API -- driver metapackage". 
- mint-a0d6e39727c667f280b18ae2 (`vim-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Vi IMproved - Common files". Archive https://archive.ubuntu.com/ubuntu/pool/main/v/vim/vim-common_9.1.0016-1ubuntu7_all.deb; inspected entries: `./usr/bin/helpztags`, `./usr/share/applications/vim.desktop`.
- mint-5bd06c9282f29aff0f1bf341 (`vim-tiny`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Vi IMproved - enhanced vi editor - compact version". 
- mint-96f89ae2a9103a0c829d911b (`vulkan-tools`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "Miscellaneous Vulkan utilities". 
- mint-5a56059734a84f2ab479ccc8 (`wamerican`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "American English dictionary words for /usr/share/dict". 
- mint-165c1fa101a689d31a9fe743 (`warpinator`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Allows simple local network file sharing.". 
- mint-0aa9453ea0eaeed5ac0cfe70 (`wbritish`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "British English dictionary words for /usr/share/dict". 
- mint-c08671b4f95d45d04c96f709 (`webapp-manager`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Web Application Manager". 
- mint-e6eb63e109573e637e850caf (`webp-pixbuf-loader`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "WebP Image format GdkPixbuf loader". 
- mint-c46f34c1f3c1cc2fef1a659e (`wget`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "retrieves files from the web". 
- mint-4d69585d2571bcf4ffb4415c (`whiptail`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Displays user-friendly dialog boxes from shell scripts". 
- mint-daa855be48d2c15dc61b7754 (`wireless-regdb`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "wireless regulatory database". 
- mint-7d7499d8e0e1d4b4135f9204 (`wireless-tools`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Tools for manipulating Linux Wireless Extensions". 
- mint-475c1326a038737d5af27050 (`wireplumber`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "modular session / policy manager for PipeWire". 
- mint-6668f4a74a00afb91a73d2af (`wmctrl`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "control an EWMH/NetWM compatible X Window Manager". 
- mint-10b82560495de5bd319ff5a9 (`wpasupplicant`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "client support for WPA and WPA2 (IEEE 802.11i)". 
- mint-b9846fd2074d63596ff57586 (`x11-apps`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X applications". 
- mint-fc00b9c5a410fb3cb8a2cf63 (`x11-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X Window System (X.Org) infrastructure". Archive https://archive.ubuntu.com/ubuntu/pool/main/x/xorg/x11-common_7.7+23ubuntu3_all.deb; inspected entries: `./etc/X11/Xsession`, `./etc/X11/Xsession.d`, `./etc/X11/Xsession.d/20x11-common_process-args`, `./etc/X11/Xsession.d/30x11-common_xresources`.
- mint-9216b118ef5f1d6179dbfcdb (`x11-session-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X session utilities". 
- mint-6bcbca0dc146347a866aca2a (`x11-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 utilities". 
- mint-787acc807811ddf117702677 (`x11-xkb-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X11 XKB utilities". 
- mint-4f875d7a7dd30aa61596b7c5 (`x11-xserver-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X server utilities". 
- mint-6bce89689daa96187a0620bb (`xapp-appimage-thumbnailer`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "AppImage thumbnailer". 
- mint-6c38a438219ea779387b6f3e (`xapp-epub-thumbnailer`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "ePub thumbnailer". 
- mint-92d0e127f88f84f0f9ac3fe1 (`xapp-jxl-thumbnailer`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "JPEG XL thumbnailer". 
- mint-f23ac92eb135d9eb5cb71af7 (`xapp-mp3-thumbnailer`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "MP3 thumbnailer". 
- mint-d03a61e5c2eef744325a4b2e (`xapp-ora-thumbnailer`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "OpenRaster thumbnailer". 
- mint-cde33549925a1f41d86c54e2 (`xapp-raw-thumbnailer`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "RAW thumbnailer". 
- mint-45efec5eb4a6f4d9b7a47608 (`xapp-symbolic-icons`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Set of symbolic icons for GTK applications". 
- mint-4d0aa2ef59e29028bf6a2216 (`xapp-thumbnailers-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/main/binary-amd64/Packages.gz — "Common files for XApp thumbnailers". Archive https://mirrors.kernel.org/linuxmint-packages/pool/main/x/xapp-thumbnailers/xapp-thumbnailers-common_1.2.10_all.deb; inspected entries: (not published: external working record).
- mint-0a587ab240e3609716e5838b (`xapps-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Common files for XApp desktop apps". 
- mint-c4b7612b77b7e529c79df01b (`xauth`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X authentication utility". 
- mint-6664f8b8e8874969ef7f0027 (`xawtv-plugins`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "television viewer - plugins". 
- mint-c9fc3b32e77f0287c84e1519 (`xbitmaps`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Base X bitmaps". 
- mint-8a6cd898d5a88c582fcb258f (`xbrlapi`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Access software for a blind person using a braille display - xbrlapi". 
- mint-9a7ce130d37af94befefa618 (`xcvt`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "VESA CVT standard timing modelines generator". 
- mint-51c3705b9c258f526f383f86 (`xdg-dbus-proxy`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "filtering D-Bus proxy". 
- mint-237166abab967de23f143606 (`xdg-desktop-portal`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "desktop integration portal for Flatpak and Snap". 
- mint-cb56f279cce5545aa29dfb8a (`xdg-desktop-portal-gtk`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "GTK+/GNOME portal backend for xdg-desktop-portal". 
- mint-09b523239e0ecfb8b4ef2ce4 (`xdg-desktop-portal-xapp`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Xapp's Cinnamon, MATE and XFCE backends for xdg-desktop-portal.". 
- mint-ac8923f22e8cccbb8551b439 (`xdg-user-dirs`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "tool to manage well known user directories". 
- mint-3758560352d7ca3fa10f511b (`xdg-user-dirs-gtk`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "tool to manage well known user directories (Gtk extension)". 
- mint-eb6a2571fdb61552be0e19d2 (`xdg-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "desktop integration utilities from freedesktop.org". 
- mint-99cef124ee10bc43a8fe8448 (`xed`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Text editor". 
- mint-c4c19df68728a2834f6e3951 (`xed-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Text editor (common files)". Archive https://mirrors.kernel.org/linuxmint-packages/pool/backport/x/xed/xed-common_3.8.4+zara_all.deb; inspected entries: `./usr/share/glib-2.0/schemas/org.x.editor.gschema.xml`, `./usr/share/glib-2.0/schemas/org.x.editor.plugins.filebrowser.gschema.xml`, `./usr/share/glib-2.0/schemas/org.x.editor.plugins.spell.gschema.xml`, `./usr/share/glib-2.0/schemas/org.x.editor.plugins.time.gschema.xml`.
- mint-1d2ad4a6b5f28aaa86d733fa (`xed-dbg`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Text editor (debugging symbols)". 
- mint-7d71487e062c447dc7da4c65 (`xfonts-base`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "standard fonts for X". 
- mint-3163a342af599b02ba8bd575 (`xfonts-encodings`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Encodings for X.Org fonts". 
- mint-c474b8fdac30d0b2f5c11e45 (`xfonts-scalable`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "scalable fonts for X". 
- mint-c8554a9505c9e0445bf8e4a6 (`xfonts-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X Window System font utility programs". 
- mint-fa984f383310a0e3ced5b7c0 (`xfsprogs`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Utilities for managing the XFS filesystem". 
- mint-a0ceaa04d58d3b1983d847f3 (`xinit`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X server initialisation tool". 
- mint-9a359440c6b3f6f0231bb48b (`xinput`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Runtime configuration and test of XInput devices". 
- mint-b62a0008e41f12910c76f4e4 (`xkb-data`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X Keyboard Extension (XKB) configuration data". 
- mint-9485adbd196ca947825110b7 (`xml-core`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "XML infrastructure and XML catalog file support". 
- mint-edd08984f5139b4648ed596c (`xorg`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X Window System". 
- mint-e8b41ae40a75964414c3991a (`xorg-docs-core`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Core documentation for the X.org X Window System". 
- mint-6ccc1619d0bf0ef69bbf4e3a (`xreader`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Document viewer". 
- mint-292b91a8f301ac1d6493487c (`xreader-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Document viewer (common files)". Archive https://mirrors.kernel.org/linuxmint-packages/pool/backport/x/xreader/xreader-common_4.6.8+wilma_all.deb; inspected entries: `./usr/share/doc/xreader-common/changelog.gz`, (not published: external working record), `./usr/share/help/C/xreader/index.docbook`, `./usr/share/help/C/xreader/legal.xml`.
- mint-37e69dec2f3bf295ebcfb997 (`xreader-dbg`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Document viewer (debugging symbols)". 
- mint-5856f651fdf9454252650399 (`xserver-common`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "common files used by various X servers". Archive https://archive.ubuntu.com/ubuntu/pool/main/x/xorg-server/xserver-common_21.1.12-1ubuntu1_all.deb; inspected entries: (not published: external working record), `./usr/share/doc/xserver-common/changelog.Debian.gz`, `./usr/share/man/man1/Xserver.1.gz`, `./var/lib/xkb/README.compiled`.
- mint-01f5a14ade3427207363bad3 (`xserver-xephyr`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "nested X server". 
- mint-c5924d8b2d8e93353e93c93f (`xserver-xorg`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server". 
- mint-215359052f989f19d0722aba (`xserver-xorg-core`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Xorg X server - core server". 
- mint-226e21b0b497c42cd88dbe0c (`xserver-xorg-input-all`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- input driver metapackage". 
- mint-da32ead3de5ff60c181adbf9 (`xserver-xorg-input-libinput`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- libinput input driver". 
- mint-6f9f93e49e19949282b76dbc (`xserver-xorg-input-wacom`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- Wacom input driver". 
- mint-96d809ff4ca70268f78433a1 (`xserver-xorg-legacy`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "setuid root Xorg server wrapper". 
- mint-10d2b7fe70e9862d28583c28 (`xserver-xorg-video-all`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- output driver metapackage". 
- mint-80b35a4c2191bf5baf812b5f (`xserver-xorg-video-amdgpu`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- AMDGPU display driver". 
- mint-bb2cbc8587ca66f8325d105a (`xserver-xorg-video-ati`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- AMD/ATI display driver wrapper". 
- mint-424cad0376583b4c5474a97f (`xserver-xorg-video-fbdev`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- fbdev display driver". 
- mint-0592f3c360f460ceccb96ba3 (`xserver-xorg-video-intel`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- Intel i8xx, i9xx display driver". 
- mint-c703754c3a0945ebc40b5bc6 (`xserver-xorg-video-nouveau`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- Nouveau display driver". 
- mint-e4fc26c5314813c5df28acce (`xserver-xorg-video-qxl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- QXL display driver". 
- mint-523e0ec57514cbe10f42a800 (`xserver-xorg-video-radeon`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- AMD/ATI Radeon display driver". 
- mint-a10efff5d186e909a2829227 (`xserver-xorg-video-vesa`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- VESA display driver". 
- mint-8c0a94e23f4bc8c503eaf29d (`xserver-xorg-video-vmware`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X.Org X server -- VMware display driver". 
- mint-6588d4abd8b228984c63c691 (`xviewer`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Image viewer". 
- mint-ba031043427419853fa62812 (`xviewer-dbg`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "Image viewer - debugging symbols". 
- mint-69512eabe1f5d48b076029c7 (`xviewer-plugins`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/backport/binary-amd64/Packages.gz — "set of plugins for xviewer". 
- mint-5a3d16a92bc2e3f9d29fc928 (`xwayland`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "X server for running X clients under Wayland". 
- mint-9c046affea94d33fd7f78c78 (`xxd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "tool to make (or reverse) a hex dump". 
- mint-4eb5ff6b0e390b7b7c78f78e (`xz-utils`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "XZ-format compression utilities". 
- mint-ea86e240ac04beb0508b36c6 (`yaru-theme-icon`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Yaru icon theme from the Ubuntu Community". 
- mint-d136941ddac15c1275a78492 (`yelp`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Help browser for GNOME". 
- mint-d2b5ce4a3bf501bc717a298a (`yelp-xsl`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "XSL stylesheets for the yelp help browser". 
- mint-06a5b3c528b189bab5199312 (`yt-dlp`): https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz — "downloader of videos from YouTube and other sites". 
- mint-41358d018a61b3e0d4756c84 (`zenity`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Display graphical dialog boxes from shell scripts". 
- mint-5df8214610acc5b0d2a99002 (`zenity-common`): https://mirrors.kernel.org/linuxmint-packages/dists/zara/upstream/binary-amd64/Packages.gz — "Display graphical dialog boxes from shell scripts (common files)". Archive https://mirrors.kernel.org/linuxmint-packages/pool/upstream/z/zenity/zenity-common_3.44.2-1+wilma_all.deb; inspected entries: `./usr/share/zenity/zenity.ui`.
- mint-ec2c3d3e24b4f18147a95347 (`zip`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "Archiver for .zip files". 
- mint-bf32577558e8b22f7e3f57ed (`zlib1g`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "compression library - runtime". 
- mint-7b0ac62a03e4ad24fc54ac19 (`zstd`): https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz — "fast lossless compression algorithm -- CLI tool". 

## Validation

635 assigned ids equal 635 output ids, each once. All decisions use the allowed vocabulary; all summaries and reasons satisfy the word limits. Counts: MUST 559, NOT 33, HOLE 43, UNKNOWN 0, MIXED 0.

## Subsequent evidence review corrections

The 15 rows in part-mint.3.corrections.tsv supersede the corresponding judgments in the original shard for final merging. The shard itself remains unchanged to preserve its completed append-only record. Dependency constraints govern future update selection, which is behavior under S2.2-1; restricting removal to current executable capability would add an unsupported temporal boundary. Explicitly safely removable transition packages retain their earlier judgments.

The theme archives contain `gtk-2.0/gtkrc`, `gtk-3.0/gtk.css`, `cinnamon/cinnamon.css` and `metacity-1/metacity-theme-3.xml`. These establish multiple-program scope, so mint-l-theme and mint-themes are MUST, rather than ambiguous single-program settings. Source archive URLs and exact paths are saved in part-mint.3.filelists.json.

The interface definitions of xed-common and zenity-common are single-program values under S2.2-13 and exempt under S2.2-7. Lost interface operation alone does not defeat an explicit exemption. pix-data differs: its `usr/share/aclocal/pix.m4` contains `AC_DEFUN([PIX_EXTENSION_INIT],` and `AC_DEFUN([PIX_EXTENSION_RULES],` plus shell commands invoking package discovery, translation and sed. Thus executable build macros justify MUST. Source: https://mirrors.kernel.org/linuxmint-packages/pool/backport/p/pix/pix-data_3.4.7+zara_all.deb. Selected code is saved in part-mint.3.pix-macro.json.

The confinement boundary of yelp-xsl remains factual uncertainty, hence UNKNOWN under S3-2; it was incorrectly labeled a textual HOLE in the original shard.


---

Source record: part-mint.final-notes.md

# Final c1 consolidation notes

All rows produced in this attempt were saved incrementally. No earlier output rows existed at its start. The component tables retain their first completed decisions. Evidence-based corrections made during consolidation are listed in part-mint.corrections.json; part-mint.correction-audit.json preserves the original and final fields. The consolidated part-mint.tsv is the final classification. No input object, inventory file, or prior result was removed.

## Shared highlighting definitions

For mint-f3a27734d1c9e9356a0e2c91, libsource-highlight-common, the final decision is MUST under S2.2-1 and S2.2-2. S2.2-7 and S2.2-13 do not exempt shared settings used across separate programs. Primary upstream documentation in https://ftp.gnu.org/gnu/src-highlite/source-highlight-3.1.9.tar.gz, doc/source-highlight.texi, describes the library as enabling consumers to “add highlighting functionalities to their programs”. The library manual, doc/source-highlight-lib.texi, describes recognition: “the library detects (using regular expressions based on language definition files)”. The shared data directory supplies definitions and output styles to those consumers. The removal argument concerns loss of shared recognition capability, not arbitrary execution of grammar files as host-rights scripts.

## Additional check of interpreter resources

The UNKNOWN decision for mint-f03630dc00f470e339f74873, libgs10-common, is retained. Its file list establishes interpreter resources; the available inventory does not establish the execution mode and rights of those resources. Further primary documentation was consulted at https://ghostscript.readthedocs.io/en/gs10.02.1/Use.html and https://ghostscript.readthedocs.io/en/latest/Psfiles.html. The former states “Sometimes the initialization files are compiled into Ghostscript and cannot be changed.” The latter describes gs_init.ps: “Ghostscript reads this automatically when it starts up.” These establish function and possible packaging arrangements, but do not supply this machine's invocation or build settings. No execution/removal probe was made. This is a factual evidence limitation under S3-2, not an alleged gap in the definition.

## Validation

part-mint.merge-verify.py checks the exact header, one row per input identifier, identical identifier sets and counts, uniqueness, the five permitted decisions, permitted sentence IDs, field word limits, single-line fields, and basis prefixes. It writes part-mint.done only when the complete identifier comparison succeeds.

## Dependency selectors: final individual decisions

The final decision for bluetooth, build-essential, init, and libpython3-stdlib is MUST under S2.2-1 and S2.2-2. Their documented dependencies govern package operations. This is not a claim that deleting the selector also deletes installed dependencies; those are separate objects. It is a change in which packages subsequent package operations select or allow. No sentence limits computer behavior to currently running executable payloads. These individual corrections supersede the intermediate documentation-only reasoning for bluetooth, build-essential, and init in component 1, and for libpython3-stdlib in component 2.

Each was checked individually against its full description retained in part-mint.1.sources.json or part-mint.3.full-metadata.json:

- bluetooth, mint-abfe052ec72b3e4d59ff2dd7: https://archive.ubuntu.com/ubuntu/dists/noble/universe/i18n/Translation-en.xz documents provision of all supported stack plugins through this metapackage. Its payload file list alone omits the operative dependency selection.
- build-essential, mint-267e53cbb404e5549ed2f412: https://archive.ubuntu.com/ubuntu/dists/noble/main/i18n/Translation-en.xz documents dependency on the essential build tools and states the package is required for package building. Its informational list does not erase that dependency role.
- init, mint-c5056f235638fd42ac7b8127: the same primary index documents selection among initialization systems while ensuring one remains available at all times. That is an operative constraint, not just descriptive content.
- libpython3-stdlib, mint-d0cf3bfc0f782be651893767: the same primary index identifies a dependency on the distribution's default interpreter version's standard library. Tracking selection through upgrades is inferred from the versioned dependency, not an assertion that its payload contains runtime implementation.

The ftp package remains NOT: the primary description identifies an obsolete dummy transition to the separately inventoried tnftp implementation. Its individual removal leaves that replacement in place. This differs from an ongoing current-default or completeness constraint. The nine selectors in component 3 likewise have operative documented dependency-selection roles; their final MUST rows and individual supporting descriptions appear in that component's correction notes.

All source and correction decisions are classified as c1. The counts in component notes describe their own intermediate or corrected component tables; only part-mint.done reports the final consolidated totals.

