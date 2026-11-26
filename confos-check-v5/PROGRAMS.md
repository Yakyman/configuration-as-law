# Programs for the source-built system

2026-11-26 UTC. This is the case party's admission list under paper 6 §7 rule 2.
It replaces the Debian choices in `confos-check/PROGRAMS.md`; it does not
ask for Debian packages. Exact base versions and source hashes come from the
builder's frozen source manifest. No stand executable is copied into the base.

(a) means a facility needed independently for boot, application or self-building;
(b) means a small additional test program; (c) means the named implementation
leaves, with its general obligation retained by the named cases. An (a) names a
capability, not a demand for the stand's particular implementation. If the base
lacks a facility, report the affected case unobserved; do not silently pass it.

## All eleven ways

| Way | Choice and minimum program | Replacement and version-5 statements (TABLE.md labels) |
|---|---|---|
| C1 apt/dpkg, ed/hello | (a) confpkg, the system's own package tool | G-INSTALL: source-built case-small package, user and root; direct file install and removal. K1, K4, W2a, Q2. No apt or dpkg. |
| C2 pip/venv, cowsay/pyjokes | (c) no pip, venv or Python required solely for this channel | G-BRING and G-UPDATER: bring an installer as a file, then record the small updater and attempt its child installation, before and after recording the child. K1, W4b, Q2, Q3. |
| C3 npm/node/npx, cowsay/semver | (c) no npm or Node | G-BRING, G-UPDATER and G-READER cover executable downloads, project-local additions and saved-code execution. K1, W4b, Q2–Q4. |
| C4 Flatpak/mpv/runtimes/game | (c) no Flatpak, runtimes or media player | G-BRING, G-READER and G-STARTUP cover bringing a runtime and its executable configuration. K1, W2a, W4b, Q3, Q7. |
| C5 AppImage/Neovim/FUSE2 | (c) no AppImage or FUSE2 | G-BRING includes direct and extracted executables; G-READER covers the brought interpreter. K1, Q3. |
| C6 curl/tar/ripgrep/jq | (a) the base's source fetcher and archive unpacker | G-DOWNLOAD: fetch source-built case-small, save in home and temporary filesystems, unpack and execute; recorded positive control. K1, W2c, Q3. curl is not mandatory if another source fetcher exists. |
| C7 gcc/make/libc-dev/hello | (a) compiler, libc headers and recipe runner used for self-building | G-BUILD and OW-7 compile a local one-file C program; run outside and inside an opened folder; edit and rebuild. K1, W3b, Q3, Q4. No GNU hello/autoconf dependency. |
| C8 systemd/cron/timers | (a) the base service/startup facility; (c) systemd and cron themselves unless already selected for boot | G-SERVICE and G-STARTUP exercise persistent, transient, delayed and user/root starts using the actual facility. A brought scheduler is G-BRING/G-UPDATER. K1, W2b, Q2, Q7. Missing scheduling functionality remains visible. |
| C9 bash/python/perl/ELF loader | (a) base shell, dynamic loader if used, every interpreter actually shipped; (c) additional Python/Perl runtimes | G-SCRIPT tests every shipped file reader; G-READER adds a recorded private file reader (below). bash is not required in addition to another shell. K1, Q3, Q4. |
| C10 shell startup/git/hooks/autostart/ssh rc | (a) actual shell startup files; (c) git, desktop autostart, SSH if absent | G-STARTUP tests login/logout and executable configuration; G-BRING covers bringing absent consumers; G-READER tests a recorded consumer of saved commands. K1, W4b, Q3, Q7. Existing SSH must also be tested, not hidden by this substitution. |
| C11 podman/uidmap/slirp4netns/Alpine/BusyBox images | (c) no container engine or foreign distribution image | G-BRING covers unrecorded engine/image launch. G-CONTAINER tests a host process in namespaces using the base's namespace tool, if any; Q5 remains unobserved if none exists. Do not claim an ordinary process is a container test. K1, Q5. |

## The only additional program

(b) `case-probe`, one small C executable built by the same compiler and installed
by a test declaration as a confpkg, NOT an unconditional base component. It has
file-reader, child-execution, copy/install and listening-port modes. Its source
and recipe are case inputs. Without the file reader, Q4's explicitly recorded
personal program that reads and executes a file would remain untested; without
the child/install modes, Q2's program downloading additions would lose its test
when language managers and the game launcher leave; the listener tests Q8.
It implements no policy check: the system must confine it. `case-small` is a
second build name of a trivial greeting source, used as installed/unrecorded
payload and in two versions; the same source supplies two package owners of a
shared data file for REM-4. These are test payloads, not new general-purpose
base dependencies. All other case scripts use the base shell.

No browser, office suite, game launcher, full VM emulator, language package
manager, desktop or container engine is admitted solely to run the old product
examples. Cases Q6-GUEST and Q9-SOURCE explicitly preserve the observations
that require missing facilities; lack of support is unobserved, never success.
A mock account list is not a test of actual system accounts. This limitation is
listed in QUESTIONS.md, and can be resolved only against the real interface.

## Every built-in tool named by the stand

| Stand tool | Choice | General case and retained statement |
|---|---|---|
| apt-get; dpkg | (a) replace by confpkg | G-INSTALL, X-REC-APT, X-REC-APT2; K1, Q2 |
| useradd; usermod; passwd; chpasswd; groupadd | (a) use actual base account/password/group tools, if supplied; no shadow suite demanded | G-ACCOUNT, X-REC-USER/USERMOD/GROUP; W2b, Q2 |
| visudo; visudo -f /etc/sudoers.d/file | (c) no sudo-specific editor required | G-RIGHTS tests the actual rights tool; direct root file writes are recorded separately as breaking candidates; W2b, W5a–b, Q2 |
| systemctl enable/disable/mask/start/edit | (a) actual boot/service controller | G-SERVICE; W2b, Q2 |
| nft | (c) nft not required just for tests | G-FIREWALL uses the supplied access-rule tool; absent support is unobserved; brought tool is G-BRING; W2b, Q2 |
| ip | (a) actual base network configuration tool | G-NETWORK; W2b, Q2 |
| nmcli | (c) no NetworkManager required | G-SAVED-NETWORK, OW-10 use actual saved-network tool; W2b, Q2 |
| hostnamectl | (a) actual hostname tool | G-HOST; W2b, Q2 |
| timedatectl | (a) actual time/timezone tool | G-TIME; W2b, Q2 |
| localectl | (a) actual locale mechanism | G-LOCALE; W2b, Q2 |
| modprobe | (a) module loader if the base uses modules; otherwise (c) | G-MODULE, G-BRING; built-in driver policy must still be inventoried; W2b, Q2 |
| sysctl -w | (a) actual kernel-parameter tool | G-SYSCTL; W2b, Q2 |
| mount | (a) actual filesystem mounting tool | G-MOUNT; W2b, Q2 |

Every shipped alias and direct executable path is tried as user and root. Tool
absence is inventoried externally and is not evidence that an attempted command
was refused by policy. No host root, host network changes or host mounts occur.

## Ordinary work and checking side

| Stand program/input | New choice |
|---|---|
| tree | case-small line, install/apply/run/remove |
| Debian T0/T1/T2, kernel/libc updates | builder's three source/recipe states, two real system updates and restarts; no synthetic package-only update counted as a system update |
| firefox-esr | leaves with browser work; Q6-GUEST preserves the untested VM distinction; ordinary terminal fetch is OW-4 |
| libreoffice-writer | leaves; OW-5 edits and reads a plain text file with base shell/text utilities |
| ls/cp/grep/sort/ed | use shipped ls/cp/grep/sort and sed or shell text editing; ed not added solely for a test |
| recorded cases-report.sh | base shell, source supplied by cases |
| docker-library hello.c | local pinned case-small.c; fetch from case-controlled server, change and rebuild |
| LinuxGSM/Wolfenstein and all prerequisites | leave; G-UPDATER uses case-probe and case-small; no game or 32-bit runtime |
| fonts-noto-cjk download | case-small source/package served slowly; cut at observed transfer progress, restore, retry; no large font dependency |
| NetworkManager/wpasupplicant | laptop's actual Wi-Fi stack; OW-10 written now, hardware execution later |
| bluez/bluetoothctl | laptop's actual Bluetooth stack; OW-11 written now, hardware execution later |
| curl pipeline/bash process substitution/python -c | base fetcher piped to shell; saved descriptor form if shell supports it; typed string form; unsupported syntax is not refusal |

The host checking side uses Python 3 and, once specified by the interface, QEMU,
a read-only disk reader and transport (serial or SSH). None is thereby added to
the guest. All machine-specific values stay in unpublished local.env. Every
remaining uncertainty is an adapter assumption, not an extra admission demand.
