# Supplemental package-function evidence

Twenty-two matching input rows represent twenty-one requested package names, because there are two locale outputs. Each proposed row was assessed individually. Package versions identify inventory objects; current upstream descriptions establish stable program roles, not claims that a different version was installed. No classification from another task was consulted.

Native library objects implement code executed with their calling process rights, so S2.2-10 and the capability-removal test S2.2-2 apply. Standalone executable utilities additionally meet S2.2-9. Content and operational data were assessed separately. The serialized rows are explicit decisions, not a name-prefix classifier.

## Primary evidence by package

| Package | Source and short exact excerpt | Application to the object |
|---|---|---|
| zbar-minimal | https://zbar.sourceforge.net/api/ — "ZBar Bar Code Reader Library Documentation" | The minimal barcode implementation retains native decoding code. |
| keybinder | https://github.com/kupferlauncher/keybinder — "library for registering global key bindings" | Native global-shortcut library. |
| libsrtp | https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/telephony.scm — "Secure RTP (SRTP) Reference Implementation" | Native secure transport implementation. |
| debianutils | https://salsa.debian.org/debian/debianutils — "a number of small utilities" | Executable system utilities. |
| libmd | https://github.com/guillemj/libmd/blob/main/README — "Message Digest functions from BSD systems" | Native hash-function implementation. |
| libxcrypt | https://github.com/besser82/libxcrypt — "Extended crypt library" | Executable hashing implementation, distinct from stored passwords. |
| python-minimal-wrapper | https://github.com/lfam/guix/blob/master/gnu/packages/python.scm — "Wrapper for the Python 3 commands" | `python-minimal-wrapper` invokes `wrap-python3`; the builder creates unversioned command links and an executable shell wrapper for the configuration-query command. |
| udftools | https://github.com/pali/udftools — "Linux tools for UDF filesystems and DVD/CD-R(W) drives" | Executable filesystem tools. |
| keyutils | https://man7.org/linux/man-pages/man2/keyctl.2.html — "libkeyutils library (provided by the keyutils package)" | Library wrappers and tools invoke kernel key management. |
| iso-codes | https://salsa.debian.org/iso-codes-team/iso-codes — "lists of various ISO standards (countries, languages, language scripts, and currency names)" | Reference names and their translations are content under S2.2-4. |
| libslirp | https://gitlab.com/qemu-project/libslirp/-/raw/master/README.md — "libslirp is a user-mode networking library" | Host-side native networking code, not guest code confined within a virtual machine. |
| glibc-utf8-locales | https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/base.scm — `make-glibc-utf8-locales` uses `localedef` to generate locale definitions; https://man7.org/linux/man-pages/man3/setlocale.3.html — "The return value is NULL if the request cannot be honored." | These definitions determine shared collation, character classification, and formatting. Removing them prevents selecting the corresponding locales. Both matching locale rows are MUST. |
| usb-modeswitch-data | https://www.draisberghof.de/usb_modeswitch/ — "It contains the device database and the rules file" | Device configuration and automatic event rules enable hardware mode changes. This is operational data, not merely reference content. |
| libnfs | https://github.com/sahlberg/libnfs — "NFS client library" | Native network-filesystem access code. |
| elfutils | https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/elf.scm — "Collection of utilities and libraries to handle ELF files" | Guix separates executable utilities into a `bin` output; the unsuffixed default output holds native libraries such as libelf. The proposed row specifically describes the default library output. |
| cyrus-sasl | https://www.cyrusimap.org/sasl/ — "Cyrus SASL provides a number of authentication plugins out of the box." | Native authentication implementation, not exempt account-password material. |
| libical | https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/calendar.scm — "iCalendar protocols and data formats implementation" | Calendar processing code, not calendar content. |
| liburcu | https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/datastructures.scm — "User-space RCU data synchronisation library" | Native concurrency implementation. |
| nilfs-utils | https://nilfs.sourceforge.io/en/manual.html — "These manual pages are bundled in nilfs-utils package" | Listed tools include filesystem creation, mounting, cleaning, resizing, and checkpoint manipulation. |
| zix | https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/datastructures.scm — "C library of portability wrappers and data structures" | Native allocation, threading, filesystem, and container implementation. |
| bdb | https://www.oracle.com/database/technologies/related/berkeleydb.html — "embedded key-value database libraries" | Database engine code, not database contents. Guix `bdb-6` metadata identifies version 6.2.32, with `bdb` aliasing this implementation. |

## Manual checks

The following ten representative native-code rows were checked against their own package source rather than assumed from a library-shaped name: guix-9230f521b9 (barcode decoding), guix-22c51eb1c5 (key bindings), guix-96a7070d1a (secure transport), guix-525e566986 (digests), guix-191f4a26d4 (password hashing), guix-35b0a2de06 (networking), guix-ff5349cd06 (NFS), guix-d13a209977 (calendar processing), guix-b44271a638 (synchronization), guix-ebe1a53639 (data structures). The common conclusion follows from S2.2-10, "code that another program executes must be recorded if the program runs it with the program’s own rights". Utility, wrapper, locale, ISO-content, and device-rule rows were checked separately.

Raw source fetches for some large modules returned connection resets. Where necessary, the public source was read through the repository contents API or rendered source page. Only role evidence was extracted. No software was installed, built, or executed.
