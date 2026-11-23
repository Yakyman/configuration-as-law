# Package classification notes

Only the supplied package rows and the permitted inventory were used. Package status establishes installation, not function. Official Debian package descriptions establish functions. The release index and English descriptions were read from:

- https://deb.debian.org/debian/dists/bookworm/main/binary-amd64/Packages.xz
- https://deb.debian.org/debian/dists/bookworm/main/i18n/Translation-en.xz

Descriptions were inspected for program, library, data, configuration and dependency-only roles. Package installation alone was never used as a MUST rule. Package rows represent packages, not grouped directory members; a package containing code and ancillary documentation is classified by its executable contribution.

## Rule P: executable programs

S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”

Apply MUST to documented executable utilities, daemons, interpreters and operating-system code. The installation evidence establishes their presence; the documented function supplies the removal reasoning. Pure data, configuration and dependency-only packages were excluded and individually decided.

Ten hand-checked rule P rows:
- debian-7ac0ecf630 (adduser): add and remove users and groups. The described object is an executable program, so rule P fits.
- debian-52a6e89c50 (apt): commandline package manager. The described object is an executable program, so rule P fits.
- debian-7e581bffc1 (bash): GNU Bourne Again SHell. The described object is an executable program, so rule P fits.
- debian-aeb3d018e8 (curl): command line tool for transferring data with URL syntax. The described object is an executable program, so rule P fits.
- debian-e99d8e16f1 (dpkg): Debian package management system. The described object is an executable program, so rule P fits.
- debian-9573ee576e (grep): GNU grep, egrep and fgrep. The described object is an executable program, so rule P fits.
- debian-dd3aa38850 (openssh-server): secure shell (SSH) server, for secure access from remote machines. The described object is an executable program, so rule P fits.
- debian-50e2bf1471 (systemd): system and service manager. The described object is an executable program, so rule P fits.
- debian-b48d271d11 (tar): GNU version of the tar archiving utility. The described object is an executable program, so rule P fits.
- debian-21b48c46af (vim): Vi IMproved - enhanced vi editor. The described object is an executable program, so rule P fits.

## Rule L: directly executed library/module code

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

Apply MUST to runtime shared libraries and Python modules loaded into the consuming program. Their API code executes with the caller’s rights. A library implementing a sandbox remains executable host code; possible confined inputs to that library are different objects. Prefixes only dispatch already-reviewed descriptions; data/common/dependency exceptions are removed first.

Ten hand-checked rule L rows:
- debian-5d52ef819a (libacl1): access control list - shared library. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-66f672bca8 (libc6): GNU C Library: Shared libraries. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-5a7fa751a2 (libcurl4): easy-to-use client-side URL transfer library (OpenSSL flavour). Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-6643bd2a37 (libssl3): Secure Sockets Layer toolkit - shared libraries. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-f72e8ae6ef (libsqlite3-0): SQLite 3 shared library. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-2611cd5289 (libzstd1): fast lossless compression algorithm. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-ebf827c02b (python3-apt): Python 3 interface to libapt-pkg. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-a51a155fba (python3-requests): elegant and simple HTTP library for Python3, built for human beings. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-5f4f0aab5c (python3-yaml): YAML parser and emitter for Python3. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.
- debian-0fb500bd4c (python3-jinja2): small but fast and easy to use stand-alone template engine. Documentation identifies a runtime library/module; code executes in the caller, so rule L fits.

## Individually decided cases

The script special-case table contains the individual reasoning. In addition, libpython3-stdlib was checked by its file list and description: it is a dependency package without runtime library code itself; further dependency-semantics review below establishes MUST. Pure metapackages are not silently treated as the executable packages they depend on. No package removal or other probe was performed.

Selected package file lists are preserved in part-2.packages.filelists.json, each with its URL. They establish, for example, gcc-12-base has only documents, while vim-common also supplies /usr/bin/helpztags.

Additional sources:

- https://manpages.debian.org/bookworm/libaudit-common/libaudit.conf.5.en.html: “The file /etc/libaudit.conf contains configuration information for user space applications that link to libaudit.”
- https://manpages.debian.org/bookworm/libtirpc-common/netconfig.5.en.html: “The netconfig file defines a list of” transport names and descriptions (transport table evidence).
- https://packages.debian.org/bookworm/linux-image-6.1.0-56-cloud-amd64: “Linux 6.1 for x86-64 cloud (signed)”.
- https://packages.debian.org/bookworm/libpython3-stdlib: “This package is a dependency package”.

## Package documentation excerpts

The following short exact title excerpts are from the official package descriptions. The runtime/data distinction also used their full descriptions during classification.
- https://packages.debian.org/bookworm/libacl1: “access control list - shared library”.
- https://packages.debian.org/bookworm/adduser: “add and remove users and groups”.
- https://packages.debian.org/bookworm/apparmor: “user-space parser utility for AppArmor”.
- https://packages.debian.org/bookworm/libapparmor1: “changehat AppArmor library”.
- https://packages.debian.org/bookworm/apt: “commandline package manager”.
- https://packages.debian.org/bookworm/apt-utils: “package management related utility programs”.
- https://packages.debian.org/bookworm/libapt-pkg6.0: “package management runtime library”.
- https://packages.debian.org/bookworm/apt-listchanges: “package change history notification tool”.
- https://packages.debian.org/bookworm/libargon2-1: “memory-hard hashing function - runtime library”.
- https://packages.debian.org/bookworm/libattr1: “extended attribute handling - shared library”.
- https://packages.debian.org/bookworm/libaudit-common: “Dynamic library for security auditing - common files”.
- https://packages.debian.org/bookworm/libaudit1: “Dynamic library for security auditing”.
- https://packages.debian.org/bookworm/base-files: “Debian base system miscellaneous files”.
- https://packages.debian.org/bookworm/base-passwd: “Debian base system master password and group files”.
- https://packages.debian.org/bookworm/bash: “GNU Bourne Again SHell”.
- https://packages.debian.org/bookworm/bash-completion: “programmable completion for the bash shell”.
- https://packages.debian.org/bookworm/bind9-host: “DNS Lookup Utility”.
- https://packages.debian.org/bookworm/bind9-libs: “Shared Libraries used by BIND 9”.
- https://packages.debian.org/bookworm/python3-blinker: “Fast, simple object-to-object and broadcast signaling (Python3)”.
- https://packages.debian.org/bookworm/libbrotli1: “library implementing brotli encoder and decoder (shared libraries)”.
- https://packages.debian.org/bookworm/libbz2-1.0: “high-quality block-sorting file compressor library - runtime”.
- https://packages.debian.org/bookworm/ca-certificates: “Common CA certificates”.
- https://packages.debian.org/bookworm/libdebconfclient0: “Debian Configuration Management System (C-implementation library)”.
- https://packages.debian.org/bookworm/genisoimage: “Creates ISO-9660 CD-ROM filesystem images”.
- https://packages.debian.org/bookworm/python3-chardet: “Universal Character Encoding Detector (Python3)”.
- https://packages.debian.org/bookworm/cloud-init: “initialization system for infrastructure cloud instances”.
- https://packages.debian.org/bookworm/cloud-initramfs-growroot: “automatically resize the root partition on first boot”.
- https://packages.debian.org/bookworm/cloud-guest-utils: “cloud guest utilities”.
- https://packages.debian.org/bookworm/cloud-image-utils: “cloud image management utilities”.
- https://packages.debian.org/bookworm/cloud-utils: “metapackage for installation of upstream cloud-utils source”.
- https://packages.debian.org/bookworm/python3-configobj: “simple but powerful config file reader and writer for Python 3”.
- https://packages.debian.org/bookworm/coreutils: “GNU core utilities”.
- https://packages.debian.org/bookworm/cpio: “GNU cpio -- a program to manage archives of files”.
- https://packages.debian.org/bookworm/libcryptsetup12: “disk encryption support - shared library”.
- https://packages.debian.org/bookworm/curl: “command line tool for transferring data with URL syntax”.
- https://packages.debian.org/bookworm/libcurl3-gnutls: “easy-to-use client-side URL transfer library (GnuTLS flavour)”.
- https://packages.debian.org/bookworm/libcurl4: “easy-to-use client-side URL transfer library (OpenSSL flavour)”.
- https://packages.debian.org/bookworm/libsasl2-2: “Cyrus SASL - authentication abstraction library”.
- https://packages.debian.org/bookworm/libsasl2-modules-db: “Cyrus SASL - pluggable authentication modules (DB)”.
- https://packages.debian.org/bookworm/dash: “POSIX-compliant shell”.
- https://packages.debian.org/bookworm/libdb5.3: “Berkeley v5.3 Database Libraries [runtime]”.
- https://packages.debian.org/bookworm/dbus: “simple interprocess messaging system (system message bus)”.
- https://packages.debian.org/bookworm/dbus-bin: “simple interprocess messaging system (command line utilities)”.
- https://packages.debian.org/bookworm/dbus-daemon: “simple interprocess messaging system (reference message bus)”.
- https://packages.debian.org/bookworm/dbus-session-bus-common: “simple interprocess messaging system (session bus configuration)”.
- https://packages.debian.org/bookworm/dbus-system-bus-common: “simple interprocess messaging system (system bus configuration)”.
- https://packages.debian.org/bookworm/libdbus-1-3: “simple interprocess messaging system (library)”.
- https://packages.debian.org/bookworm/python3-dbus: “simple interprocess messaging system (Python 3 interface)”.
- https://packages.debian.org/bookworm/debconf: “Debian configuration management system”.
- https://packages.debian.org/bookworm/python3-debconf: “interact with debconf from Python 3”.
- https://packages.debian.org/bookworm/debian-archive-keyring: “GnuPG archive keys of the Debian archive”.
- https://packages.debian.org/bookworm/debianutils: “Miscellaneous utilities specific to Debian”.
- https://packages.debian.org/bookworm/runit-helper: “dh-runit implementation detail”.
- https://packages.debian.org/bookworm/diffutils: “File comparison utilities”.
- https://packages.debian.org/bookworm/python3-distro-info: “information about distributions' releases (Python 3 module)”.
- https://packages.debian.org/bookworm/distro-info-data: “information about the distributions' releases (data files)”.
- https://packages.debian.org/bookworm/dpkg: “Debian package management system”.
- https://packages.debian.org/bookworm/libduktape207: “embeddable Javascript engine, library”.
- https://packages.debian.org/bookworm/e2fsprogs: “ext2/ext3/ext4 file system utilities”.
- https://packages.debian.org/bookworm/libcom-err2: “common error description library”.
- https://packages.debian.org/bookworm/libext2fs2: “ext2/ext3/ext4 file system libraries”.
- https://packages.debian.org/bookworm/libss2: “command-line interface parsing library”.
- https://packages.debian.org/bookworm/logsave: “save the output of a command in a log file”.
- https://packages.debian.org/bookworm/libefiboot1: “Library to manage UEFI variables”.
- https://packages.debian.org/bookworm/libefivar1: “Library to manage UEFI variables”.
- https://packages.debian.org/bookworm/libelf1: “library to read and write ELF files”.
- https://packages.debian.org/bookworm/ethtool: “display or change Ethernet device settings”.
- https://packages.debian.org/bookworm/libexpat1: “XML parsing C library - runtime library”.
- https://packages.debian.org/bookworm/file: “Recognize the type of data in a file using "magic" numbers”.
- https://packages.debian.org/bookworm/libmagic-mgc: “File type determination library using "magic" numbers (compiled magic file)”.
- https://packages.debian.org/bookworm/libmagic1: “Recognize the type of data in a file using "magic" numbers - library”.
- https://packages.debian.org/bookworm/findutils: “utilities for finding files--find, xargs”.
- https://packages.debian.org/bookworm/libfreetype6: “FreeType 2 font engine, shared library files”.
- https://packages.debian.org/bookworm/libfstrm0: “Frame Streams (fstrm) library”.
- https://packages.debian.org/bookworm/libfuse2: “Filesystem in Userspace (library)”.
- https://packages.debian.org/bookworm/libfuse3-3: “Filesystem in Userspace (library) (3.x version)”.
- https://packages.debian.org/bookworm/gcc-12-base: “GCC, the GNU Compiler Collection (base package)”.
- https://packages.debian.org/bookworm/libgcc-s1: “GCC support library”.
- https://packages.debian.org/bookworm/libstdc++6: “GNU Standard C++ Library v3”.
- https://packages.debian.org/bookworm/libgdbm6: “GNU dbm database routines (runtime version)”.
- https://packages.debian.org/bookworm/gdisk: “GPT fdisk text-mode partitioning tool”.
- https://packages.debian.org/bookworm/gettext-base: “GNU Internationalization utilities for the base system”.
- https://packages.debian.org/bookworm/libglib2.0-0: “GLib library of C routines”.
- https://packages.debian.org/bookworm/libc-bin: “GNU C Library: Binaries”.
- https://packages.debian.org/bookworm/libc-l10n: “GNU C Library: localization files”.
- https://packages.debian.org/bookworm/libc6: “GNU C Library: Shared libraries”.
- https://packages.debian.org/bookworm/locales: “GNU C Library: National Language (locale) data [support]”.
- https://packages.debian.org/bookworm/libgmp10: “Multiprecision arithmetic library”.
- https://packages.debian.org/bookworm/gpgv: “GNU privacy guard - signature verification tool”.
- https://packages.debian.org/bookworm/libgnutls30: “GNU TLS library - main runtime library”.
- https://packages.debian.org/bookworm/libgpm2: “General Purpose Mouse - shared library”.
- https://packages.debian.org/bookworm/grep: “GNU grep, egrep and fgrep”.
- https://packages.debian.org/bookworm/groff-base: “GNU troff text-formatting system (base system components)”.
- https://packages.debian.org/bookworm/grub-cloud-amd64: “GRand Unified Bootloader (cloud setup)”.
- https://packages.debian.org/bookworm/grub-efi-amd64-signed: “GRand Unified Bootloader, version 2 (amd64 UEFI signed by Debian)”.
- https://packages.debian.org/bookworm/grub-common: “GRand Unified Bootloader (common files)”.
- https://packages.debian.org/bookworm/grub-efi-amd64-bin: “GRand Unified Bootloader, version 2 (EFI-AMD64 modules)”.
- https://packages.debian.org/bookworm/grub-pc-bin: “GRand Unified Bootloader, version 2 (PC/BIOS modules)”.
- https://packages.debian.org/bookworm/grub2-common: “GRand Unified Bootloader (common files for version 2)”.
- https://packages.debian.org/bookworm/gzip: “GNU compression utilities”.
- https://packages.debian.org/bookworm/hostname: “utility to set/show the host name or domain name”.
- https://packages.debian.org/bookworm/libicu72: “International Components for Unicode”.
- https://packages.debian.org/bookworm/init: “metapackage ensuring an init system is installed”.
- https://packages.debian.org/bookworm/init-system-helpers: “helper tools for all init systems”.
- https://packages.debian.org/bookworm/initramfs-tools: “generic modular initramfs generator (automation)”.
- https://packages.debian.org/bookworm/initramfs-tools-core: “generic modular initramfs generator (core tools)”.
- https://packages.debian.org/bookworm/iproute2: “networking and traffic control tools”.
- https://packages.debian.org/bookworm/iptables: “administration tools for packet filtering and NAT”.
- https://packages.debian.org/bookworm/libip4tc2: “netfilter libip4tc library”.
- https://packages.debian.org/bookworm/libip6tc2: “netfilter libip6tc library”.
- https://packages.debian.org/bookworm/libxtables12: “netfilter xtables library”.
- https://packages.debian.org/bookworm/iputils-ping: “Tools to test the reachability of network hosts”.
- https://packages.debian.org/bookworm/isc-dhcp-client: “DHCP client for automatically obtaining an IP address”.
- https://packages.debian.org/bookworm/libjemalloc2: “general-purpose scalable concurrent malloc(3) implementation”.
- https://packages.debian.org/bookworm/python3-jinja2: “small but fast and easy to use stand-alone template engine”.
- https://packages.debian.org/bookworm/jq: “lightweight and flexible command-line JSON processor”.
- https://packages.debian.org/bookworm/libjq1: “lightweight and flexible command-line JSON processor - shared library”.
- https://packages.debian.org/bookworm/libjson-c5: “JSON manipulation library - shared library”.
- https://packages.debian.org/bookworm/libkeyutils1: “Linux Key Management Utilities (library)”.
- https://packages.debian.org/bookworm/klibc-utils: “small utilities built with klibc for early boot”.
- https://packages.debian.org/bookworm/libklibc: “minimal libc subset for use with initramfs”.
- https://packages.debian.org/bookworm/kmod: “tools for managing Linux kernel modules”.
- https://packages.debian.org/bookworm/libkmod2: “libkmod shared library”.
- https://packages.debian.org/bookworm/libgssapi-krb5-2: “MIT Kerberos runtime libraries - krb5 GSS-API Mechanism”.
- https://packages.debian.org/bookworm/libk5crypto3: “MIT Kerberos runtime libraries - Crypto Library”.
- https://packages.debian.org/bookworm/libkrb5-3: “MIT Kerberos runtime libraries”.
- https://packages.debian.org/bookworm/libkrb5support0: “MIT Kerberos runtime libraries - Support library”.
- https://packages.debian.org/bookworm/less: “pager program similar to more”.
- https://packages.debian.org/bookworm/libaio1: “Linux kernel AIO access library - shared library”.
- https://packages.debian.org/bookworm/libbpf1: “eBPF helper library (shared library)”.
- https://packages.debian.org/bookworm/libbsd0: “utility functions from BSD systems - shared library”.
- https://packages.debian.org/bookworm/libcap-ng0: “alternate POSIX capabilities library”.
- https://packages.debian.org/bookworm/libcap2: “POSIX 1003.1e capabilities (library)”.
- https://packages.debian.org/bookworm/libcap2-bin: “POSIX 1003.1e capabilities (utilities)”.
- https://packages.debian.org/bookworm/libcbor0.8: “library for parsing and generating CBOR (RFC 7049)”.
- https://packages.debian.org/bookworm/libedit2: “BSD editline and history libraries”.
- https://packages.debian.org/bookworm/libffi8: “Foreign Function Interface library runtime”.
- https://packages.debian.org/bookworm/libfido2-1: “library for generating and verifying FIDO 2.0 objects”.
- https://packages.debian.org/bookworm/libgcrypt20: “LGPL Crypto library - runtime library”.
- https://packages.debian.org/bookworm/libgpg-error0: “GnuPG development runtime library”.
- https://packages.debian.org/bookworm/libidn2-0: “Internationalized domain names (IDNA2008/TR46) library”.
- https://packages.debian.org/bookworm/libmaxminddb0: “IP geolocation database library”.
- https://packages.debian.org/bookworm/libmd0: “message digest functions from BSD systems - shared library”.
- https://packages.debian.org/bookworm/libmnl0: “minimalistic Netlink communication library”.
- https://packages.debian.org/bookworm/libnetfilter-conntrack3: “Netfilter netlink-conntrack library”.
- https://packages.debian.org/bookworm/libnfnetlink0: “Netfilter netlink library”.
- https://packages.debian.org/bookworm/libnftnl11: “Netfilter nftables userspace API library”.
- https://packages.debian.org/bookworm/libnsl2: “Public client interface for NIS(YP) and NIS+”.
- https://packages.debian.org/bookworm/libonig5: “regular expressions library”.
- https://packages.debian.org/bookworm/libpcap0.8: “system interface for user-level packet capture”.
- https://packages.debian.org/bookworm/libpipeline1: “Unix process pipeline manipulation library”.
- https://packages.debian.org/bookworm/libpng16-16: “PNG library - runtime (version 1.6)”.
- https://packages.debian.org/bookworm/libpsl5: “Library for Public Suffix List (shared libraries)”.
- https://packages.debian.org/bookworm/libseccomp2: “high level interface to Linux seccomp filter”.
- https://packages.debian.org/bookworm/libselinux1: “SELinux runtime shared libraries”.
- https://packages.debian.org/bookworm/libsemanage-common: “Common files for SELinux policy management libraries”.
- https://packages.debian.org/bookworm/libsemanage2: “SELinux policy management library”.
- https://packages.debian.org/bookworm/libsepol2: “SELinux library for manipulating binary security policies”.
- https://packages.debian.org/bookworm/libsodium23: “Network communication, cryptography and signaturing library”.
- https://packages.debian.org/bookworm/libssh2-1: “SSH2 client-side library”.
- https://packages.debian.org/bookworm/libtasn1-6: “Manage ASN.1 structures (runtime)”.
- https://packages.debian.org/bookworm/libtirpc-common: “transport-independent RPC library - common files”.
- https://packages.debian.org/bookworm/libtirpc3: “transport-independent RPC library”.
- https://packages.debian.org/bookworm/libunistring2: “Unicode string library for C”.
- https://packages.debian.org/bookworm/liburing2: “Linux kernel io_uring access library - shared library”.
- https://packages.debian.org/bookworm/libutempter0: “privileged helper for utmp/wtmp updates (runtime)”.
- https://packages.debian.org/bookworm/libuv1: “asynchronous event notification library - runtime library”.
- https://packages.debian.org/bookworm/libcrypt1: “libcrypt shared library”.
- https://packages.debian.org/bookworm/libxml2: “GNOME XML library”.
- https://packages.debian.org/bookworm/libyaml-0-2: “Fast YAML 1.1 parser and emitter library”.
- https://packages.debian.org/bookworm/libzstd1: “fast lossless compression algorithm”.
- https://packages.debian.org/bookworm/zstd: “fast lossless compression algorithm -- CLI tool”.
- https://packages.debian.org/bookworm/linux-base: “Linux image base package”.
- https://packages.debian.org/bookworm/linux-image-cloud-amd64: “Linux for x86-64 cloud (meta-package)”.
- https://packages.debian.org/bookworm/liblmdb0: “Lightning Memory-Mapped Database shared library”.
- https://packages.debian.org/bookworm/lsb-release: “Linux Standard Base version reporting utility (minimal implementation)”.
- https://packages.debian.org/bookworm/dmsetup: “Linux Kernel Device Mapper userspace library”.
- https://packages.debian.org/bookworm/libdevmapper1.02.1: “Linux Kernel Device Mapper userspace library”.
- https://packages.debian.org/bookworm/liblz4-1: “Fast LZ compression algorithm library - runtime”.
- https://packages.debian.org/bookworm/man-db: “tools for reading manual pages”.
- https://packages.debian.org/bookworm/manpages: “Manual pages about using a GNU/Linux system”.
- https://packages.debian.org/bookworm/python3-markdown-it: “Python port of markdown-it and some its associated plugins”.
- https://packages.debian.org/bookworm/python3-markupsafe: “HTML/XHTML/XML string library”.
- https://packages.debian.org/bookworm/mawk: “Pattern scanning and text processing language”.
- https://packages.debian.org/bookworm/python3-mdurl: “Python port of the JavaScript mdurl package”.
- https://packages.debian.org/bookworm/media-types: “List of standard media types and their usual file extension”.
- https://packages.debian.org/bookworm/mokutil: “tools for manipulating machine owner keys”.
- https://packages.debian.org/bookworm/nano: “small, friendly text editor inspired by Pico”.
- https://packages.debian.org/bookworm/libncursesw6: “shared libraries for terminal handling (wide character support)”.
- https://packages.debian.org/bookworm/libtinfo6: “shared low-level terminfo library for terminal handling”.
- https://packages.debian.org/bookworm/ncurses-base: “basic terminal type definitions”.
- https://packages.debian.org/bookworm/ncurses-bin: “terminal-related programs and man pages”.
- https://packages.debian.org/bookworm/netbase: “Basic TCP/IP networking system”.
- https://packages.debian.org/bookworm/python3-netifaces: “portable network interface information - Python 3.x”.
- https://packages.debian.org/bookworm/libnetplan0: “YAML network configuration abstraction runtime library”.
- https://packages.debian.org/bookworm/netplan.io: “YAML network configuration abstraction for various backends”.
- https://packages.debian.org/bookworm/libhogweed6: “low level cryptographic library (public-key cryptos)”.
- https://packages.debian.org/bookworm/libnettle8: “low level cryptographic library (symmetric and one-way cryptos)”.
- https://packages.debian.org/bookworm/libnewt0.52: “text mode windowing with slang”.
- https://packages.debian.org/bookworm/whiptail: “Displays user-friendly dialog boxes from shell scripts”.
- https://packages.debian.org/bookworm/libnghttp2-14: “library implementing HTTP/2 protocol (shared library)”.
- https://packages.debian.org/bookworm/libnuma1: “Libraries for controlling NUMA policy”.
- https://packages.debian.org/bookworm/libldap-2.5-0: “OpenLDAP libraries”.
- https://packages.debian.org/bookworm/openssh-client: “secure shell (SSH) client, for secure access to remote machines”.
- https://packages.debian.org/bookworm/openssh-server: “secure shell (SSH) server, for secure access from remote machines”.
- https://packages.debian.org/bookworm/openssh-sftp-server: “secure shell (SSH) sftp server module, for SFTP access from remote machines”.
- https://packages.debian.org/bookworm/libssl3: “Secure Sockets Layer toolkit - shared libraries”.
- https://packages.debian.org/bookworm/openssl: “Secure Sockets Layer toolkit - cryptographic utility”.
- https://packages.debian.org/bookworm/libp11-kit0: “library for loading and coordinating access to PKCS#11 modules - runtime”.
- https://packages.debian.org/bookworm/libpam-modules: “Pluggable Authentication Modules for PAM”.
- https://packages.debian.org/bookworm/libpam-modules-bin: “Pluggable Authentication Modules for PAM - helper binaries”.
- https://packages.debian.org/bookworm/libpam-runtime: “Runtime support for the PAM library”.
- https://packages.debian.org/bookworm/libpam0g: “Pluggable Authentication Modules library”.
- https://packages.debian.org/bookworm/pci.ids: “PCI ID Repository”.
- https://packages.debian.org/bookworm/libpci3: “PCI utilities (shared library)”.
- https://packages.debian.org/bookworm/pciutils: “PCI utilities”.
- https://packages.debian.org/bookworm/libpcre2-8-0: “New Perl Compatible Regular Expression Library- 8 bit runtime files”.
- https://packages.debian.org/bookworm/perl-base: “minimal Perl system”.
- https://packages.debian.org/bookworm/libpolkit-agent-1-0: “polkit Authentication Agent API”.
- https://packages.debian.org/bookworm/libpolkit-gobject-1-0: “polkit Authorization API”.
- https://packages.debian.org/bookworm/polkitd: “framework for managing administrative policies and privileges”.
- https://packages.debian.org/bookworm/libpopt0: “lib for parsing cmdline parameters”.
- https://packages.debian.org/bookworm/libproc2-0: “library for accessing process information from /proc”.
- https://packages.debian.org/bookworm/procps: “/proc file system utilities”.
- https://packages.debian.org/bookworm/libprotobuf-c1: “Protocol Buffers C shared library (protobuf-c)”.
- https://packages.debian.org/bookworm/psmisc: “utilities that use the proc file system”.
- https://packages.debian.org/bookworm/python3-pycurl: “Python bindings to libcurl (Python 3)”.
- https://packages.debian.org/bookworm/python3-pygments: “syntax highlighting package written in Python 3”.
- https://packages.debian.org/bookworm/python3-jwt: “Python 3 implementation of JSON Web Token”.
- https://packages.debian.org/bookworm/python3-pyparsing: “alternative to creating and executing simple grammars - Python 3.x”.
- https://packages.debian.org/bookworm/python3-pyrsistent: “persistent/functional/immutable data structures for Python”.
- https://packages.debian.org/bookworm/python3-serial: “pyserial - module encapsulating access for the serial port”.
- https://packages.debian.org/bookworm/python3-pysimplesoap: “simple and lightweight SOAP Library (Python 3)”.
- https://packages.debian.org/bookworm/python-apt-common: “Python interface to libapt-pkg (locales)”.
- https://packages.debian.org/bookworm/python3-apt: “Python 3 interface to libapt-pkg”.
- https://packages.debian.org/bookworm/python3-attr: “Attributes without boilerplate (Python 3)”.
- https://packages.debian.org/bookworm/python3-certifi: “root certificates for validating SSL certs and verifying TLS hosts (python3)”.
- https://packages.debian.org/bookworm/python3-cffi-backend: “Foreign Function Interface for Python 3 calling C code - runtime”.
- https://packages.debian.org/bookworm/python3-charset-normalizer: “charset, encoding and language detection (Python 3)”.
- https://packages.debian.org/bookworm/python3-cryptography: “Python library exposing cryptographic recipes and primitives (Python 3)”.
- https://packages.debian.org/bookworm/python3-debian: “Python 3 modules to work with Debian-related data formats”.
- https://packages.debian.org/bookworm/python3-debianbts: “Python interface to Debian's Bug Tracking System”.
- https://packages.debian.org/bookworm/python3-distro: “Linux OS platform information API”.
- https://packages.debian.org/bookworm/python3-httplib2: “comprehensive HTTP client library written for Python3”.
- https://packages.debian.org/bookworm/python3-idna: “Python IDNA2008 (RFC 5891) handling (Python 3)”.
- https://packages.debian.org/bookworm/python3-jsonpatch: “library to apply JSON patches - Python 3.x”.
- https://packages.debian.org/bookworm/python3-json-pointer: “resolve JSON pointers - Python 3.x”.
- https://packages.debian.org/bookworm/python3-jsonschema: “An(other) implementation of JSON Schema (Draft 3, 4, 6, 7)”.
- https://packages.debian.org/bookworm/python3-oauthlib: “generic, spec-compliant implementation of OAuth for Python3”.
- https://packages.debian.org/bookworm/python3-urllib3: “HTTP library with thread-safe connection pooling for Python3”.
- https://packages.debian.org/bookworm/libpython3-stdlib: “interactive high-level object-oriented language (default python3 version)”.
- https://packages.debian.org/bookworm/python3: “interactive high-level object-oriented language (default python3 version)”.
- https://packages.debian.org/bookworm/python3-minimal: “minimal subset of the Python language (default python3 version)”.
- https://packages.debian.org/bookworm/libpython3.11-minimal: “Minimal subset of the Python language (version 3.11)”.
- https://packages.debian.org/bookworm/libpython3.11-stdlib: “Interactive high-level object-oriented language (standard library, version 3.11)”.
- https://packages.debian.org/bookworm/python3.11: “Interactive high-level object-oriented language (version 3.11)”.
- https://packages.debian.org/bookworm/python3.11-minimal: “Minimal subset of the Python language (version 3.11)”.
- https://packages.debian.org/bookworm/python3-yaml: “YAML parser and emitter for Python3”.
- https://packages.debian.org/bookworm/qemu-utils: “QEMU utilities”.
- https://packages.debian.org/bookworm/libreadline8: “GNU readline and history libraries, run-time libraries”.
- https://packages.debian.org/bookworm/readline-common: “GNU readline and history libraries, common files”.
- https://packages.debian.org/bookworm/python3-reportbug: “Python modules for interacting with bug tracking systems”.
- https://packages.debian.org/bookworm/reportbug: “reports bugs in the Debian distribution”.
- https://packages.debian.org/bookworm/python3-requests: “elegant and simple HTTP library for Python3, built for human beings”.
- https://packages.debian.org/bookworm/python3-rich: “render rich text, tables, progress bars, syntax highlighting, markdown and more”.
- https://packages.debian.org/bookworm/librtmp1: “toolkit for RTMP streams (shared library)”.
- https://packages.debian.org/bookworm/screen: “terminal multiplexer with VT100/ANSI terminal emulation”.
- https://packages.debian.org/bookworm/sed: “GNU stream editor for filtering/transforming text”.
- https://packages.debian.org/bookworm/sensible-utils: “Utilities for sensible alternative selection”.
- https://packages.debian.org/bookworm/python3-pkg-resources: “Package Discovery and Resource Access using pkg_resources”.
- https://packages.debian.org/bookworm/sgml-base: “SGML infrastructure and SGML catalog file support”.
- https://packages.debian.org/bookworm/login: “system login tools”.
- https://packages.debian.org/bookworm/passwd: “change and administer password and group data”.
- https://packages.debian.org/bookworm/shim-unsigned: “boot loader to chain-load signed boot loaders under Secure Boot”.
- https://packages.debian.org/bookworm/shim-helpers-amd64-signed: “boot loader to chain-load signed boot loaders (signed by Debian)”.
- https://packages.debian.org/bookworm/shim-signed: “Secure Boot chain-loading bootloader”.
- https://packages.debian.org/bookworm/shim-signed-common: “Secure Boot chain-loading bootloader (common helper scripts)”.
- https://packages.debian.org/bookworm/python3-six: “Python 2 and 3 compatibility library”.
- https://packages.debian.org/bookworm/libslang2: “S-Lang programming library - runtime version”.
- https://packages.debian.org/bookworm/socat: “multipurpose relay for bidirectional data transfer”.
- https://packages.debian.org/bookworm/libsqlite3-0: “SQLite 3 shared library”.
- https://packages.debian.org/bookworm/ssh-import-id: “securely retrieve an SSH public key and install it locally”.
- https://packages.debian.org/bookworm/sudo: “Provide limited super user privileges to specific users”.
- https://packages.debian.org/bookworm/libnss-myhostname: “nss module providing fallback resolution for the current hostname”.
- https://packages.debian.org/bookworm/libpam-systemd: “system and service manager - PAM module”.
- https://packages.debian.org/bookworm/libsystemd-shared: “systemd shared private library”.
- https://packages.debian.org/bookworm/libsystemd0: “systemd utility library”.
- https://packages.debian.org/bookworm/libudev1: “libudev shared library”.
- https://packages.debian.org/bookworm/systemd: “system and service manager”.
- https://packages.debian.org/bookworm/systemd-resolved: “systemd DNS resolver”.
- https://packages.debian.org/bookworm/systemd-sysv: “system and service manager - SysV compatibility symlinks”.
- https://packages.debian.org/bookworm/systemd-timesyncd: “minimalistic service to synchronize local time with NTP servers”.
- https://packages.debian.org/bookworm/udev: “/dev/ and hotplug management daemon”.
- https://packages.debian.org/bookworm/sysvinit-utils: “System-V-like utilities”.
- https://packages.debian.org/bookworm/tar: “GNU version of the tar archiving utility”.
- https://packages.debian.org/bookworm/libwrap0: “TCP wrappers library”.
- https://packages.debian.org/bookworm/tcpdump: “command-line network traffic analyzer”.
- https://packages.debian.org/bookworm/traceroute: “Traces the route taken by packets over an IPv4/IPv6 network”.
- https://packages.debian.org/bookworm/tzdata: “time zone and daylight-saving time data”.
- https://packages.debian.org/bookworm/ucf: “Update Configuration File(s): preserve user changes to config files”.
- https://packages.debian.org/bookworm/libuchardet0: “universal charset detection library - shared library”.
- https://packages.debian.org/bookworm/unattended-upgrades: “automatic installation of security upgrades”.
- https://packages.debian.org/bookworm/usr-is-merged: “Transitional package to assert a merged-/usr system”.
- https://packages.debian.org/bookworm/bsdextrautils: “extra utilities from 4.4BSD-Lite”.
- https://packages.debian.org/bookworm/bsdutils: “basic utilities from 4.4BSD-Lite”.
- https://packages.debian.org/bookworm/eject: “ejects CDs and operates CD-Changers under Linux”.
- https://packages.debian.org/bookworm/fdisk: “collection of partitioning utilities”.
- https://packages.debian.org/bookworm/libblkid1: “block device ID library”.
- https://packages.debian.org/bookworm/libfdisk1: “fdisk partitioning library”.
- https://packages.debian.org/bookworm/libmount1: “device mounting library”.
- https://packages.debian.org/bookworm/libsmartcols1: “smart column output alignment library”.
- https://packages.debian.org/bookworm/libuuid1: “Universally Unique ID library”.
- https://packages.debian.org/bookworm/mount: “tools for mounting and manipulating filesystems”.
- https://packages.debian.org/bookworm/util-linux: “miscellaneous system utilities”.
- https://packages.debian.org/bookworm/util-linux-extra: “interactive login tools”.
- https://packages.debian.org/bookworm/uuid-runtime: “runtime components for the Universally Unique ID library”.
- https://packages.debian.org/bookworm/vim: “Vi IMproved - enhanced vi editor”.
- https://packages.debian.org/bookworm/vim-common: “Vi IMproved - Common files”.
- https://packages.debian.org/bookworm/vim-runtime: “Vi IMproved - Runtime files”.
- https://packages.debian.org/bookworm/vim-tiny: “Vi IMproved - enhanced vi editor - compact version”.
- https://packages.debian.org/bookworm/wget: “retrieves files from the web”.
- https://packages.debian.org/bookworm/xml-core: “XML infrastructure and XML catalog file support”.
- https://packages.debian.org/bookworm/libxxhash0: “shared library for xxhash”.
- https://packages.debian.org/bookworm/liblzma5: “XZ-format compression library”.
- https://packages.debian.org/bookworm/xz-utils: “XZ-format compression utilities”.
- https://packages.debian.org/bookworm/zlib1g: “compression library - runtime”.

GRUB defaults source: https://www.gnu.org/software/grub/manual/grub/html_node/Simple-configuration.html states: “It is sourced by a shell script, and so must be valid POSIX shell input”. This establishes the code classification for grub-cloud-amd64.

## Review corrections

D-Bus configuration (debian-6551aee88e, debian-2102ddaaf0) governs interprogram communication, so its effect is not confined inside one program. Both rows are MUST under S2.2-1 and S2.2-2.

Recognition rules in libmagic-mgc (debian-f1ae2388d8) and media-types (debian-ad283af0ea) change automatic classification capabilities. The unchanged-behaviour condition in S2.2-4 is unmet, so both are MUST under S2.2-1 and S2.2-2.

zlib1g (debian-5ba05539a3) is library code under rule L, with S2.2-10 rather than S2.2-9.

## Dependency and maintainer-script review

The five former dependency-only HOLE cases are resolved from additional documentation; no unresolved ambiguity is attributed to dependency removal.

For cloud-utils (debian-e62af4f5a5), init (debian-95bb80c619), linux-image-cloud-amd64 (debian-d805aa0253), and libpython3-stdlib (debian-ec71209928), the package descriptions identify operational dependency packages. Their installed requirements maintain the corresponding suite, init implementation, kernel series, or standard-library version. Removing the requirement loses that package-maintenance constraint even if already-installed binaries remain at that instant. Therefore S2.2-1 and S2.2-2 yield MUST.

Official semantics: https://www.debian.org/doc/debian-policy/ch-relationships.html states “A package will not be configured unless all of the packages listed in its Depends field have been correctly configured”. This makes dependency metadata operational rather than reference content.

https://manpages.debian.org/bookworm/apt/apt-get.8.en.html states that dist-upgrade “also intelligently handles changing dependencies with new versions of packages”. Dependency-package presence determines continued dependency-driven upgrades; autoremove additionally distinguishes packages still needed by dependencies.

For usr-is-merged (debian-01d10767da), the ordinary file list was insufficient: package maintainer scripts are control-archive files, absent from that payload list. Reading the official source archive https://deb.debian.org/debian/pool/main/u/usrmerge/usrmerge_37~deb12u1.tar.xz established debian/usr-is-merged.preinst defines `fail_if_unmerged` and debian/usr-is-merged.postinst defines `cleanup_biarch_dirs`. Both have shell interpreter headers; the latter contains `cleanup_biarch_dirs` in the configure branch. The scripts check filesystem layout and clean obsolete architecture directories with installer rights. S2.2-10 and S2.2-13 therefore yield MUST. No script was executed and no file was removed.

## Repository templates and shared recognition database

python-apt-common (debian-9e34733f17) is MUST, not a whole-package aggregation HOLE. The official source archive https://deb.debian.org/debian/pool/main/p/python-apt/python-apt_2.6.0.tar.xz contains aptsources/distro.py. Its get_sources method searches matcher templates; when source_template remains absent, it executes `raise NoDistroTemplateException`. The diagnostic is “Error: could not find a distribution template for %s/%s”. Thus template removal breaks distribution-aware source operations; translations accompanying the templates do not cancel the package’s operational role.

The official API https://apt-team.pages.debian.net/python-apt/library/aptsources.sourceslist.html documents matcherPath as `/usr/share/python-apt/templates/` and `save()` as “save the current sources”. https://apt-team.pages.debian.net/python-apt/library/aptsources.distro.html describes get_sources as “Find the corresponding template, main and child sources for the distribution”. These are repository-management operations used by library consumers, not merely displayed reference content.

libmagic-mgc (debian-f1ae2388d8) remains MUST. The shared-library API https://manpages.debian.org/bookworm/libmagic-dev/libmagic.3.en.html specifies that database loading is required before magic queries and allows client programs to load the system database; this capability is not confined to the file command.

Debian’s exact file 5.44 patch archive https://deb.debian.org/debian/pool/main/f/file/file_5.44-3.debian.tar.xz contains debian/patches/local.support-local-definitions-in-etc-magic.patch. Its library-build definition is `AM_CPPFLAGS = -DMAGIC='"/etc/magic:$(MAGIC)"'`. Therefore the local magic path also belongs to the shared-library default search path.

The corresponding upstream source https://deb.debian.org/debian/pool/main/f/file/file_5.44.orig.tar.gz, src/apprentice.c, contains “Compatibility with old code that looked in .mime” followed by a MAGIC_MIME branch checking the corresponding .mime filename. This establishes that local MIME rules can likewise be consumed by shared-library clients. Whether the particular local files contain any effective rules is a separate evidence question; no file contents were inferred from these default search semantics.
