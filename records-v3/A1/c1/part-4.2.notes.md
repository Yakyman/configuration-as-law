# Part 4, second store-object slice

Scope: 431 `system-closure-store-object` rows, positions 431–861 within that kind in input order. Every assigned row has `members=1`. A package store directory is therefore classified as the supplied object: removing an output containing executable code loses that code, even if the output also carries manuals. MIXED is reserved for grouped inventory rows with separately classified members.

Only Sections 2.2 and the first indicator of Section 3 supply decision rules. No removal or runtime experiment was performed. Inventory closure annotations were ignored. Raw service provenance, boot and activation expressions establish functions where available; public package and generator source establishes other functions. No other classification was consulted.

## Rules and manual checks

**P: executable software outputs.** A documented native executable, driver, runtime library, or interpreter module is MUST under S2.2-1, S2.2-2, S2.2-9 and S2.2-10. Removing the entire output prevents invoking its code or dependent operations. This rule is applied only to identified software outputs, not documentation, images, generated settings, protocol descriptions, or caches. Package names are matched to their own definitions or documented minimal variants; an inventory closure label is never the basis. The following ten rows were individually read against their package descriptions and checked as software rather than assets:

- guix-5e69024ed7: video capture utilities.
- guix-c451c2dd83: executable widget toolkit routines.
- guix-b087324c7e: account authentication commands.
- guix-f0f9aee420: Perl socket encryption module.
- guix-a5258762b5: desktop event playback library.
- guix-be089e96b2: color-management service.
- guix-47c22e3cb7: XML parsing library.
- guix-cd4404b821: executable audio plugins.
- guix-49b16208f4: network commands.
- guix-94e54f1dfa: desktop helper library.

**A: directly evaluated activation actions.** A file explicitly listed in `configuration/run/current-system/activate` and passed to `primitive-load` is MUST under S2.2-10 and S2.2-13. The saved expression uses `(primitive-load action)` inside `save-module-excursion`; the rule concerns executable action files, not values-only settings. Nine assigned rows match. Ten manual checks, including one additional input row solely to check the rule, were: guix-360efff222, guix-54c3549e3c, guix-ed7d9f5fc5, guix-7db6ef3aab, guix-4dbd370b6f, guix-51a7118274, guix-12c0b22b0a, guix-3eaf0083db, guix-c862ad9abd, guix-4a1178fa90. Each exact store path appears in that action list; the last row belongs to the other slice and is not output here.

**G: directly loaded compiled service definitions.** These are MUST under S2.2-2 and S2.2-10. The pinned generator loads the compiled file directly, so deleting it prevents service registration; this is not merely a slower module-cache miss. Ten manually checked definitions: guix-218dace6bc (time), guix-9250837ddd (discovery), guix-0d9b370edb (remote login), guix-e9ff5d3e91 (logging), guix-584e17b8e9 (timer), guix-b0e790d9d9 (console font), guix-06f908f7b3 (shared-memory mount), guix-b8b2e33f43 (console font), guix-80821e9370 (store mount), guix-9f4c6e2fbf (devices). The source file/service identity and compiled-name transformation were checked.

**S: executable Scheme service definitions.** These are MUST under S2.2-2, S2.2-10 and S2.2-13. Raw `../in/raw/guix/service-provenance.tsv` records an actual service constructor expression for the source file; the public generator establishes that its body defines service procedures. The conclusion is about interpreter-executable capability, not a claim that normal boot chooses the source instead of its compiled counterpart. Ten manual checks against the source expressions: guix-7d2ba848d0 (console font), guix-d83bcfd4e4 (random seed), guix-f3806e7f4d (control-group mount), guix-e1e9bab070 (loopback), guix-5dec5147fc (remote login), guix-1e02d84784 (terminal), guix-ef2b10eb77 (terminal), guix-8de9a639ef (system naming), guix-e5e5836647 (console font), guix-e6bdf0fcbb (runtime mount).

**M: identified package-management module nodes.** Public `guix/self.scm` explicitly constructs these names with `scheme-node`, producing executable Scheme modules, source trees, or bundles linking both source and compiled trees. Those identified code objects are MUST under S2.2-2 and S2.2-10. The rule does not extend to arbitrary unreferenced `module-import` basenames. Ten manually checked nodes: guix-40ac3ffda1 (base packages bundle), guix-c9c3fe4c21 (CLI bundle), guix-403ebb9bec (CLI core source), guix-1d030f4b23 (module bundle), guix-b1cda82d20 (system test bundle), guix-9e2b09e306 (base packages), guix-d6f4da0567 (additional modules), guix-9849b393fe (CLI core), guix-3321d7b173 (base package source), guix-0c0c8b4f78 (CLI). Source and bundle identity was read from generator structure, rather than inferred from the closure inventory.

All other rows were considered individually; the explicit row-by-row decisions are retained in the generation scripts and final TSV.

## Boundary decisions

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

- The activation header explicitly pairs source and compiled module paths for guix-5e84abb70c. Guile's documented module loader falls back to source if compiled code is missing. This yields HOLE between S2.2-5 and S2.2-10 for that acceleration-only compiled directory. Direct `load-compiled` service files are different. Unmatched generic import directories remain UNKNOWN because their contents and consumers are absent.
- A theme supplying shared widget styling is HOLE between internal-setting, content, and behavior readings. Icon collections, background pictures, and sound samples are classified as content under S2.2-4. This distinction is about what they contain, not whether many applications can use them.
- ALSA's system-global configuration is read independently by multiple applications, establishing that its routing and conversion settings are not limited to one program. It is MUST. Configurations consumed by one power, discovery, session, or cache daemon leave “in force only inside one program” ambiguous relative to effects on clients or the machine; these specified cases are HOLE.
- PAM files named `slim`, `chfn`, `useradd`, and `sudo` were identified through the PAM generator, not mistaken for similarly named binaries. Their authentication permissions are MUST.
- System locale tables and keyboard mappings provide operational parsing, formatting, and input capabilities. Glyph outlines and bitmap glyphs are graphical content. Header and protocol-description inputs retain the content-versus-development-capability ambiguity as HOLE.
- UNKNOWN is used for unavailable generated contents or an unresolved removal-relevant function, not because the object is merely old or outside a profile. Public descriptions and inventory links were checked first. No assumption was made that a basename containing “cache” guarantees the S2.2-5 removal behavior.

## Generator and runtime documentation

- https://codeberg.org/guix/guix/raw/commit/d58da8a56b75af73a7b5466f7ef8a81679713aa3/gnu/services/shepherd.scm — exact fragments: `(load-compiled file)` and `'#$(map scm->go files)`. The service-file constructor produces Scheme service definitions.
- https://raw.githubusercontent.com/Millak/guix/master/guix/self.scm — “Return a node that builds the given Scheme MODULES, and depends on DEPENDENCIES”. The inspected `node-source+compiled` function links source and object trees under their respective interpreter search locations.
- https://raw.githubusercontent.com/Millak/guix/master/guix/profiles.scm — “Return a derivation that builds the cache files for input method modules”. Other inspected functions construct certificate bundles, documentation indices, module dependencies, and editor startup Lisp.
- https://raw.githubusercontent.com/Millak/guix/master/gnu/system/pam.scm — “Return a file for pam_env(8) that contains environment variables VARS.” The same source explicitly emits root-permission and fallback authentication policies.
- https://raw.githubusercontent.com/Millak/guix/master/gnu/services/base.scm — `(program-file "set-up-network"` and `(program-file "tear-down-network"`; the inspected file also generates device rules, name mappings, ownership checks, and channel expressions.
- https://raw.githubusercontent.com/Millak/guix/master/gnu/services/desktop.scm — `(program-file "elogind-dbus-shepherd-sync"`; inspected constructors also identify power, authorization, and location configurations.
- https://raw.githubusercontent.com/Millak/guix/master/gnu/services/xorg.scm — `(program-file "startx" exp)`; login and display configuration builders were also inspected.
- https://raw.githubusercontent.com/Millak/guix/master/gnu/services/networking.scm — “when a modeswitchable USB device is detected.” The wrapper builder establishes event-triggered executable behavior.
- https://raw.githubusercontent.com/Millak/guix/master/gnu/system.scm — “Return the directory containing the locales compiled for the definitions listed in OS.”
- https://www.gnu.org/software/guile/manual/guile.pdf — “Guile comes with an interface module to the readline library”. The Modules and the File System section also establishes source fallback when compiled modules are absent.
- https://www.alsa-project.org/wiki/Asoundrc — “When an alsa application starts both configuration files are read.”
- https://man7.org/linux/man-pages/man5/sysctl.conf.5.html — “Linux kernel configuration parameters”.
- https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html — “polkit provides an authorization API intended to be used by privileged programs”.
- https://man7.org/linux/man-pages/man7/udev.7.html — “manages permissions of device nodes”.

The package documentation sources below were inspected for package purpose. Short quoted anchors identify the relevant declarations; row descriptions paraphrase their functionality.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/admin.scm — “shadow”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/algebra.scm — “Computing the discrete Fourier transform”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/attr.scm — “Library and tools for manipulating extended attributes”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/audio.scm — “LDAC Bluetooth encoder and ABR library”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/autotools.scm — “System-independent dlopen wrapper of GNU libtool”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/base.scm — “patch”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/bash.scm — “The GNU Bourne-Again SHell, stripped down for non-interactive”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/cdrom.scm — “Audio CD reading utility”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/compression.scm — “High-quality data compression program”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/cryptsetup.scm — “Set up transparent encryption of block devices using”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/cups.scm — “OpenPrinting CUPS filters and backends”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/disk.scm — “libblockdev”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/dns.scm — “Resolvconf POSIX compliant implementation, a middleman for resolv.conf”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/freedesktop.scm — “libqmi”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/fribidi.scm — “Implementation of the Unicode bidirectional algorithm”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gcc.scm — “gcc”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/ghostscript.scm — “Little CMS, a small-footprint colour management engine”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gl.scm — “Alternative to the OpenGL Utility Toolkit (GLUT)”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gnome.scm — “colord”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gnupg.scm — “npth”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/graphviz.scm — “Graph visualization software”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/groff.scm — “Minimalist variant of Groff for use by man-db”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gstreamer.scm — “Oil runtime compiler”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/gtk.scm — “Assistive Technology Service Provider Interface, core components”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/guile-xyz.scm — “Netlink protocol implementation for Guile”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/guile.scm — “guile-bytestructures”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/image.scm — “libjpeg-turbo”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/kerberos.scm — “MIT Kerberos 5”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/libcanberra.scm — “Implementation of the XDG Sound Theme and Name”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/libdaemon.scm — “Lightweight C library that eases the writing of”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/libffi.scm — “libffi”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/libidn.scm — “Internationalized domain name library for IDNA2008”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/libunwind.scm — “Determining the call chain of a program”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/libusb.scm — “libusb”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/linux.scm — “alsa-plugins”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/man.scm — “C library for manipulating pipelines of subprocesses”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/mp3.scm — “Console audio player”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/multiprecision.scm — “C library for arbitrary-precision floating-point arithmetic”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/ncurses.scm — “Terminal emulation (termcap, terminfo) library”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/networking.scm — “libproxy”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/nss.scm — “Netscape API for system level and libc-like functions”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/ntp.scm — “Real time clock synchronization system”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/perl.scm — “Implementation of the Perl programming language”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/polkit.scm — “Authorization API for privilege management”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/pulseaudio.scm — “libsndfile”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/python.scm — “High-level, dynamically-typed programming language”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/readline.scm — “Edit command lines while typing, with history support”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/samba.scm — “The standard Windows interoperability suite of programs for”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/sdl.scm — “Cross platform game development library”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/sqlite.scm — “The SQLite database management system”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/ssh.scm — “Client and server for the secure shell (ssh)”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/tls.scm — “openssl”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/version-control.scm — “HTTP and WebDAV client library”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/video.scm — “Realtime video capture utilities for Linux”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/vulkan.scm — “API and commands for processing SPIR-V modules”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/web.scm — “Nearly transparent SSL encapsulation for IO::Socket::INET”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/xdisorg.scm — “startup-notification”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/xfce.scm — “Extension library for Xfce”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/xml.scm — “C parser for XML”.

- https://codeberg.org/guix/guix/raw/branch/master/gnu/packages/xorg.scm — “Xorg XToolkit Intrinsics library”.

- https://dbus.freedesktop.org/doc/dbus-python/ — “dbus-python is a Python binding for”.

- https://duktape.org/ — “Duktape is an embeddable Javascript engine”.

- https://github.com/Yubico/libfido2 — “Provides library functionality for FIDO2”.

- https://github.com/deepin-community/libdisplay-info — “EDID and DisplayID library.”.

- https://github.com/exfatprogs/exfatprogs — “exFAT filesystem userspace utilities”.

- https://github.com/freeswitch/spandsp — “SpanDSP is a library of DSP functions for telephony”.

- https://github.com/iwamatsu/slim — “a graphical login manager for X11”.

- https://github.com/linux-nfs/nfs-utils/blob/master/README — “the Linux NFS userland utility package”.

- https://github.com/lsof-org/lsof — “LiSt Open Files”.

- https://github.com/rootless-containers/slirp4netns — “User-mode networking for unprivileged network namespaces”.

- https://github.com/storaged-project/libbytesize — “working with arbitrary big sizes in bytes”.

- https://guix.gnu.org/lt/cookbook/pt-br/guix-cookbook.pt_BR.pdf — “guix-daemon is responsible for spawning build processes and downloads”.

- https://libgd.github.io/ — “GD Graphics Library”.

- https://pcsclite.apdu.fr/ — “Middleware to access a smart card using SCard API”.

- https://raw.githubusercontent.com/Millak/guix/d58da8a56b75af73a7b5466f7ef8a81679713aa3/gnu/packages/admin.scm — “Dynamic Host Configuration Protocol (DHCP) tools”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/backup.scm — “libarchive”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/bdw-gc.scm — “conservative garbage collector”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/file.scm — “File type guesser”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/fonts.scm — “font-bitstream-vera”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/freedesktop.scm — “shared-mime-info”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/glib.scm — “glib”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/gnome.scm — “gnome-backgrounds”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/linux.scm — “alsa-ucm-conf”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/onc-rpc.scm — “Transport-independent Sun/ONC RPC implementation”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/pciutils.scm — “Programs for inspecting and manipulating PCI devices”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/photo.scm — “Read and manipulate EXIF data in digital photographs”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/rdf.scm — “Library for RDF syntax supporting Turtle and NTriples”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/text-editors.scm — “Small, user-friendly console text editor”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/xfce.scm — “elementary-xfce-icon-theme”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/xiph.scm — “Library for manipulating the ogg multimedia format”.

- https://raw.githubusercontent.com/Millak/guix/master/gnu/packages/xorg.scm — “xorgproto”.

- https://www.draisberghof.de/usb_modeswitch/ — “mode switching tool”.

- https://www.gnu.org.ua/software/gdbm/manual/ — “a library of functions implementing a hashed database”.

- https://raw.githubusercontent.com/shimmerproject/Greybird/master/light/gtk-3.0/_common.scss — exact rule `-GtkWidget-text-handle-width: 20;`. Inspected stylesheet also specifies spacing and scrollbar interaction geometry, distinguishing this object from a collection of decorative images.

## Validation

The slice contains exactly 431 unique input IDs, each exactly once in the output. All decisions are permitted, all sentence IDs exist, and both field word limits hold. Counts: MUST=396, NOT=10, HOLE=10, UNKNOWN=15, MIXED=0.
