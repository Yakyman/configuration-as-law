# Part 4, first store-object segment

Scope: first 431 `system-closure-store-object` input rows. No alternate classification or previous-night material was consulted. The closure label was discarded as classificatory evidence. Package metadata supplied by another reader was public-documentation metadata only, without decisions. No objects were removed and no execution experiments were performed.

## Deciding text

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S3-2: “If what the object does remains unknown, the case yields ?.”

## Scripted rule P: documented executable package outputs

Match an inventory package name, including a documented inherited variant, to its package definition and synopsis. A documented executable program or native/interpreter library is MUST under S2.2-1/2/9/10: removal removes its installed executable capability. The criterion is executable function, not dependency-closure membership. Data-only packages, headers, fonts, certificates, schemas, aggregate profiles, and bare generated names are excluded and considered individually. A package output is a single input object when `members=1`; incidental manuals do not make it a group row.

The extraction helper finds package definitions and inherited synopses. (not published: downloaded distribution package metadata) retains neutral documentary observations, including URL and original synopsis. Current source and an older source mirror establish functional identity, not exact file lists or version equivalence. Functional descriptions in the result are paraphrases. Retrieval failures and missing generated bodies do not become evidence of executable function.

Ten manually checked applications of P:

| ID | Inspection |
|---|---|
| guix-0d48c6bf44 | Chromaprint is an audio-fingerprinting library, not stored fingerprint content. |
| guix-18b042cc42 | The session locker is an executable program, not a lock-state value. |
| guix-c8d1d95195 | The syscall-filter interface is executable library code, not a saved filter policy. |
| guix-689f8cdd35 | The HTTP library supplies networking routines. |
| guix-d385fad5dd | The Scheme JSON module is executable parsing/serialization code. |
| guix-72b5be6d4c | Multiple-precision arithmetic is implemented by library routines. |
| guix-472ca4444d | The RAID package supplies management commands, not merely array metadata. |
| guix-cab4c5bf44 | Asynchronous-I/O support is a library interface. |
| guix-6e3094f6d6 | The transfer package supplies executable networking operations. |
| guix-97eae529eb | The compression package is a program, not already-compressed user content. |

## Scripted rule C: identified interpreter and service code

Observed `primitive-load` calls establish activation code. Service provenance includes actual Scheme service expressions; the documented service language and executable source capability establish MUST under S2.2-2/10/13. Compiled service objects are directly loaded into the service manager and likewise MUST. Being generated, or called a configuration, is not an exemption. Initial uncertainty about source versus compiled loading was resolved using the capability test: recognizable executable service source can be loaded independently even when the normal boot path uses its compiled counterpart.

Ten manually checked applications of C:

| ID | Inspection |
|---|---|
| guix-4a1178fa90 | Exact activation path occurs in the saved activation script’s primitive-load list. |
| guix-196447bb11 | Same observed activation loading mechanism. |
| guix-7c626a4b70 | Same observed activation loading mechanism. |
| guix-99564c37c5 | Same observed activation loading mechanism. |
| guix-0d20337c18 | Same observed activation loading mechanism. |
| guix-928bb56800 | Same observed activation loading mechanism. |
| guix-f83a146d79 | Same observed activation loading mechanism. |
| guix-2de6dc679f | Saved boot code creates runtime state and launches the service manager. |
| guix-5782dfe617 | Provenance supplies a Scheme service expression for the time service. |
| guix-da1388031e | Compiled service-definition artifact fits the documented direct compiled loading mechanism. |

Documentation: [Shepherd service construction](https://codeberg.org/guix/guix/raw/commit/d58da8a56b75af73a7b5466f7ef8a81679713aa3/gnu/services/shepherd.scm): `(load-compiled file)` and `'#$(map scm->go files)`. [Shepherd manual](https://www.gnu.org/software/shepherd/manual/shepherd.pdf): “The configuration file contains Scheme code”. Saved `guix/configuration/run/current-system/activate` supplies `(primitive-load action)`; `../in/raw/guix/service-provenance.tsv` supplies actual service expressions.

## Scripted rule U: unresolved generated-object role

Where the only surviving evidence identifies a generated store object, but neither captured contents, consuming references, nor retrieved documentation establishes its function, assign UNKNOWN under S3-1/2. This rule is about insufficient evidence, not an exemption and not a textual hole. Searches used the exact store path against the allowed inventory and configuration captures. Name resemblance alone cannot identify arbitrary generated content. Configuration roles established through a standard destination or a live command were decided separately; exact setting values are unnecessary when the established role decides the class.

Ten manually checked applications of U:

| ID | Inspection |
|---|---|
| guix-2a85615a21 | Module-import object lacks captured module bodies or a proven consuming reference. |
| guix-a1c1e67353 | Another module-import object with the same missing evidence. |
| guix-2917f3f574 | Module-import directory contents and distinct use were not captured. |
| guix-7526df5a8f | Additional module-import directory lacks captured module bodies and a proven consumer. |
| guix-3cc7726cb4 | Additional module-import directory lacks captured module bodies and a proven consumer. |
| guix-f3ca6aa7c1 | Artwork checkout name does not establish whether this checkout contains only visual content. |
| guix-4693999f1c | Compiled module aggregate lacks the relevant module contents or proven load reference. |
| guix-a36c632a1b | A second compiled aggregate has the same evidence limitation. |
| guix-9b6df1084f | A third compiled aggregate has the same evidence limitation. |
| guix-5d1d3b6b13 | Skeleton directory destination is known, but full content and executable portions are not. |

## Individually resolved operational inputs

`../in/raw/guix/herd-all-service-status.txt` connects the exact SSH, DHCP and time configuration objects to the running daemon commands, and identifies the log-cleanup command as periodically executed. `../in/raw/guix/files.tsv` and `../in/raw/guix/unowned-groups.json` establish standard system destinations. No legacy classification fields were read. Sudo rights and account policy use S2.2-15; filesystem, network, clock, device and interprocess configuration use S2.2-1/2 because their effects extend across the system. Font and theme assets are content under S2.2-4; development headers are operational build interfaces. The operating-system identity file is an operational input for software OS selection, not exempt merely because it contains descriptive information.

The following short documentation excerpts support these individual role determinations:

- [Shell list](https://man7.org/linux/man-pages/man5/shells.5.html): “pathnames of valid login shells”.
- [Login defaults](https://man7.org/linux/man-pages/man5/login.defs.5.html): “The /etc/login.defs file defines the site-specific configuration”.
- [Mount table](https://man7.org/linux/man-pages/man5/fstab.5.html): “filesystems the system can mount”.
- [Login banner](https://man7.org/linux/man-pages/man5/issue.5.html): “prelogin message and identification file”.
- [System name](https://man7.org/linux/man-pages/man5/hostname.5.html): “configures the name of the local system”.
- [SSH configuration](https://man.openbsd.org/sshd_config): “or the file specified with -f on the command line”.
- [DHCP client configuration](https://man.freebsd.org/cgi/man.cgi?query=dhcpcd.conf): “dhcpcd configuration file”.
- [Time configuration](https://www.ntp.org/documentation/4.2.8-series/ntp.conf/): “specify the synchronization sources, modes and other related information”.
- [Sudo policy](https://www.sudo.ws/docs/man/1.9.14/sudoers.man.pdf): “sudoers”. The manual describes the privilege policy and its file protections.
- [System identity](https://www.freedesktop.org/software/systemd/man/251/os-release.html): “If you are using this file to determine the OS”.
- [Hardware database](https://www.freedesktop.org/software/systemd/man/latest/hwdb.html): “During runtime, only the binary database is used.”
- [Device rules](https://www.freedesktop.org/software/systemd/man/261/udev.html): “The permissions for the device node.”
- [Message bus](https://dbus.freedesktop.org/doc/dbus-daemon.1.html): “Multiple programs connect to the message bus daemon and can exchange messages with one another.”
- [MIME rules](https://specifications.freedesktop.org/shared-mime-info/latest-single/): “Shared MIME-info Database”.
- [Application associations](https://specifications.freedesktop.org/mime-apps/latest/): “which application should open a file by default”.
- [Image loader registry](https://gnome.pages.gitlab.gnome.org/gtk/gdk-pixbuf/type_func.Pixbuf.init_modules.html): “Initalizes the gdk-pixbuf loader modules referenced by the loaders.cache file”. A registry called a cache is not automatically a performance-only cache.
- [Bash startup](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files): “it first reads and executes commands from the file /etc/profile”.
- [Python runtime](https://www.python.org/doc/essays/blurb/): “Python is an interpreted, object-oriented, high-level programming language”.
- [Image mathematics](https://imath.readthedocs.io/en/latest/): “2D and 3D vectors”.
- [RDF library](https://tracker.api.gnome.org/): “executes a series of SPARQL updates and RDF data insertions”.
- [Printing](https://www.cups.org/): “printing to local and network printers”.
- [Service discovery](https://github.com/avahi/avahi): “implementation of DNS Service Discovery”.
- [Line editor](https://www.gnu.org/software/ed/): “GNU ed is a line-oriented text editor.”
- [Compiler support](https://llvm.org/): “modular and reusable compiler and toolchain technologies”.
- [Camera support](https://libcamera.org/): “A complex camera support library”.

No MIXED decisions occur because these input rows each have one member. Mechanical verification checks input/output identity, uniqueness, decision vocabulary, and field word limits. This is validation, not independent acceptance.

## Package-source documentary samples
The retained neutral metadata maps every matched package to its own synopsis. Below is one short verbatim sample per source file, keeping quotations compact.
- [acl.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/acl.scm): “Library and tools for manipulating access control lists”.
- [admin.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/admin.scm): “Standard login and process accounting utilities”.
- [aspell.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/aspell.scm): “Spell checker”.
- [audio.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/audio.scm): “AdLib sound player library”.
- [base.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/base.scm): “Example GNU package”.
- [bash.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/bash.scm): “The GNU Bourne-Again SHell”.
- [compression.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/compression.scm): “Compression library”.
- [cups.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/cups.scm): “Brother laser printer driver”.
- [curl.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/curl.scm): “Command line tool for transferring data with URL syntax”.
- [databases.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/databases.scm): “Run temporary PostgreSQL databases”.
- [disk.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/disk.scm): “Tools for the Linux kernel block layer cache”.
- [enchant.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/enchant.scm): “Fast and safe spellchecking C++ library”.
- [file.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/file.scm): “File type guesser”.
- [fonts.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/fonts.scm): “Proportional variant of font-0xproto”.
- [fontutils.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/fontutils.scm): “Font rendering library”.
- [freedesktop.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/freedesktop.scm): “Tools and libraries to work with AppStream metadata”.
- [gawk.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gawk.scm): “Text scanning and processing language”.
- [gl.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gl.scm): “Mesa OpenGL Utility library”.
- [glib.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/glib.scm): “Message bus for inter-process communication (IPC)”.
- [gnome.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gnome.scm): “UPnP IGD for GNOME”.
- [gnupg.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gnupg.scm): “Library of error values for GnuPG components”.
- [gtk.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gtk.scm): “Application Menu applet”.
- [guile-xyz.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/guile-xyz.scm): “Web application framework written in Guile”.
- [guile.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/guile.scm): “Scheme implementation intended especially for extensions”.
- [hunspell.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/hunspell.scm): “Spell checker”.
- [image.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/image.scm): “Batch image converter and resizer”.
- [imagemagick.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/imagemagick.scm): “Create, edit, compose, or convert bitmap images”.
- [less.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/less.scm): “Paginator for terminals”.
- [libbsd.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/libbsd.scm): “Utility functions from BSD systems”.
- [libedit.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/libedit.scm): “Portable alternative to GNU Readline”.
- [libevent.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/libevent.scm): “Event notification library”.
- [libusb.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/libusb.scm): “User-space USB library”.
- [linux.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/linux.scm): “Debian patches”.
- [llvm.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/llvm.scm): “Runtime library for Clang/LLVM”.
- [mp3.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/mp3.scm): “MPEG audio decoder”.
- [multiprecision.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/multiprecision.scm): “Multiple-precision arithmetic library”.
- [nettle.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/nettle.scm): “C library for low-level cryptographic functionality”.
- [networking.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/networking.scm): “SCTP user-land implementation”.
- [openldap.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/openldap.scm): “Implementation of the Lightweight Directory Access Protocol”.
- [pcre.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/pcre.scm): “Perl Compatible Regular Expressions”.
- [pdf.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/pdf.scm): “Color-managed PDF generator”.
- [photo.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/photo.scm): “Fast and easy focus stacking”.
- [pkg-config.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/pkg-config.scm): “Helper tool used when compiling applications and libraries”.
- [polkit.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/polkit.scm): “Simple polkit authentication agent for Hyprland”.
- [pulseaudio.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/pulseaudio.scm): “Reading and writing files containing sampled sound”.
- [rdf.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/rdf.scm): “RDF syntax library”.
- [scanner.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/scanner.scm): “SANE backend for eSCL (AirScan) and WSD document scanners”.
- [sdl.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/sdl.scm): “Cross platform game development library”.
- [serialization.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/serialization.scm): “Data serialization system”.
- [speech.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/speech.scm): “Speech synthesis system”.
- [ssh.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/ssh.scm): “Interactive SSH client for multiple servers”.
- [suckless.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/suckless.scm): “Scroll-back buffer program for st”.
- [tcl.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/tcl.scm): “The Tcl scripting language”.
- [texinfo.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/texinfo.scm): “The GNU documentation format”.
- [tls.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/tls.scm): “ASN.1 library”.
- [version-control.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/version-control.scm): “Decentralized revision control system”.
- [video.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/video.scm): “Browse and watch anime from the command line”.
- [vulkan.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/vulkan.scm): “Machine-readable files from the SPIR-V Registry”.
- [web.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/web.scm): “Weighs the soul of incoming HTTP requests to stop AI crawlers”.
- [wget.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/wget.scm): “Non-interactive command-line utility for downloading files”.
- [xdisorg.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/xdisorg.scm): “Record, replay and distribute user actions under X11”.
- [xfce.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/xfce.scm): “Basic utility library for Xfce”.
- [xiph.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/xiph.scm): “Library for manipulating the ogg multimedia format”.
- [xml.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/xml.scm): “Library to help create and query binary XML blobs”.
- [xorg.scm](https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/xorg.scm): “Source code configuration and build system”.
- [algebra.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/algebra.scm): “Arithmetic of polynomials over arbitrary precision numbers”.
- [backup.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/backup.scm): “Encrypted backup using rsync algorithm”.
- [cdrom.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/cdrom.scm): “C library to access data on a CDDB server”.
- [dns.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/dns.scm): “Asynchronous DNS client library and utilities”.
- [ghostscript.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/ghostscript.scm): “Little CMS, a small-footprint colour management engine”.
- [gnome.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/gnome.scm): “UPnP IGD for GNOME”.
- [graphics.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/graphics.scm): “Memory Mapped Machine”.
- [gstreamer.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/gstreamer.scm): “1394-Based Digital Camera Control Library”.
- [icu4c.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/icu4c.scm): “International Components for Unicode”.
- [image.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/image.scm): “Batch image converter and resizer”.
- [libunistring.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/libunistring.scm): “C library for manipulating Unicode strings”.
- [mate.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/mate.scm): “Common files for development of MATE packages”.
- [nss.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/nss.scm): “Netscape API for system level and libc-like functions”.
- [package-management.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/package-management.scm): “Functional package manager for installed software packages and versions”.
- [popt.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/popt.scm): “Command line option parsing library”.
- [spice.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/spice.scm): “Tools for sending USB device traffic over a network”.
- [text-editors.scm](https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/text-editors.scm): “Line-oriented text editor”.

## Named module aggregates and launcher generation

Further generator documentation resolves the named Guix source/module aggregates independently of arbitrary module-import names. [Generator source](https://raw.githubusercontent.com/Millak/guix/master/guix/self.scm) describes unions “that provide Guile modules.” The `scheme-node` constructors identify cli-core, extra, system and system-test code; `node-source+compiled` assembles source and object paths; `program-file` makes the command entry point. The quiet interpreter wrapper compiles the launcher C source. These are MUST under the executable-capability rule; the C compilation input separately satisfies S2.2-2. Exact compact evidence is retained in `part-4.1-generator-excerpts.txt`.

Final segment verification: 431 rows; exact ID set and count; unique IDs; all decisions valid; all field word limits passed. Segment counts before any subsequent parent review: MUST=354, NOT=9, HOLE=0, UNKNOWN=68, MIXED=0.

## Paired boot module cache

Final reconsideration of guix-eaca1bed67: HOLE, not MUST. The saved boot script configures corresponding source and compiled module search paths. [Guile module loading](https://www.gnu.org/software/guile/manual/guile.pdf) states: “it will be loaded instead of the source file.” Source fallback leaves the compiled counterpart as a speed optimization, while its contents are also executed with interpreter rights. S2.2-5 exempts that cache; S2.2-10 requires that code. Neither supplies precedence. This does not apply to directly loaded Shepherd compiled files. Revised counts: MUST=353, NOT=9, HOLE=1, UNKNOWN=68, MIXED=0; 431 rows remain validated.
