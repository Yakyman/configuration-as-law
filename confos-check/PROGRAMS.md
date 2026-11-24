# Programs of the cases

Written by the case party, 2026-11-24 UTC. The base system is Debian 13 (trixie); the point release current on that
day is 13.8 (`dists/trixie/Release`: `Version: 13.8`, `Date: Sat, 21 Nov 2026 09:15:44 UTC`). Every Debian version
below is the version in `trixie/main/binary-amd64/Packages` on 2026-11-24, and every external source answered HTTP
200 on that day; the output of the check is `tools/verify-programs.out`, the script `tools/verify-programs.sh`.
Versions are pinned again, by checksum, when the inputs are committed before the first complete run (Section 9.5).

Each channel has ONE program that the test declaration records and installs through that channel (Paper 3,
Section 4.3: “The test declaration names everything it permits: the base system and, for each channel below, one
program installed through that channel”). Each channel also has the object that the P4 cases try to install, launch
or change WITHOUT a line (“the unrecorded object”); it is never named in any declaration of the cases.

## Channels of installation and launch (Paper 3, Section 4.3)

| # | Channel | Tool (Debian 13 package, version) | Recorded program (installed through the channel by a line) | Unrecorded object (P4 attempts) |
|---|---|---|---|---|
| C1 | System package manager | `apt` / `dpkg` (part of the base) | Debian `ed` 1.21.1-1 | Debian `hello` 2.10-5 (`apt-get install hello`; `dpkg -i hello_2.10-5_amd64.deb`, as the user and as root) |
| C2 | Language package manager: pip | `python3-pip` 25.1.1+dfsg-1, `python3-venv` 3.13.5-1 | PyPI `cowsay==6.1` (console script `cowsay`) | PyPI `pyjokes==0.8.3` (console script `pyjoke`), by `pip install --user --break-system-packages`, by a venv in the home directory, and by `pip download` + `pip install <wheel>` |
| C3 | Language package manager: npm | `npm` 9.2.0~ds1-3, `nodejs` 20.19.2+dfsg-1+deb13u3 | npm `cowsay@1.6.0` (bin `cowsay`) | npm `semver@7.6.3` (bin `semver`), by `npm install -g --prefix ~/.npm-global`, by `npm install` in a project directory, and by `npx` |
| C4 | Application packages: Flatpak | `flatpak` 1.16.6-1~deb13u3 | Flathub `io.mpv.Mpv` (runtime `org.freedesktop.Platform//26.08`) | Flathub `net.sourceforge.ExtremeTuxRacer` (runtime `org.freedesktop.Platform//25.08`), `flatpak install --user flathub …`, and `flatpak remote-add --user` of a second remote |
| C5 | Application packages: AppImage | `libfuse2t64` 2.9.9-9 (FUSE 2 for type-2 AppImages) | Neovim v0.10.4 `nvim-linux-x86_64.appimage` (GitHub release) | Neovim v0.9.5 `nvim.appimage` (GitHub release), run directly and with `--appimage-extract-and-run` |
| C6 | Direct download of programs and archives | `curl` 8.14.1-2+deb13u7, `tar` (base) | ripgrep 14.1.1 `ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz` (GitHub release, binary `rg`) | jq 1.7.1 `jq-linux-amd64` (GitHub release), downloaded with `curl`, `chmod +x`, run from `~`, `/tmp`, `/dev/shm`, `/var/tmp` |
| C7 | Building from source in the home directory | `gcc` 4:14.2.0-1, `make` 4.4.1-2, `libc6-dev` 2.41-12+deb13u5 | `hello.c` of docker-library/hello-world, commit `522bcd2faf422c60b9d20e64d7cd6d56600aec97` (the program of step 8, history 2) | GNU hello 2.12.1 (`https://ftp.gnu.org/gnu/hello/hello-2.12.1.tar.gz`), `./configure --prefix=$HOME/.local && make && make install`; and a one-file C program written in the home directory and compiled with `gcc` |
| C8 | User services and schedulers | `systemd` 257.13-1~deb13u1 (`systemd --user`), `cron` 3.0pl1-197 | a user timer unit `cases-tick.timer` with its service, recorded by its line | a user unit written to `~/.config/systemd/user/` and enabled; `systemd-run --user` (transient, and `--on-calendar`); a crontab installed with `crontab FILE`; root's crontab and `/etc/cron.d/` file as root |
| C9 | Interpreters executing scripts | `python3` 3.13.5-1 (also `bash` 5.2.37-2+b10 and `perl-base` 5.40.1-6+deb13u1 of the base) | the person's own script `~/bin/cases-report.sh`, recorded (ordinary work, Paper 4 Section 9.3) | a script saved in `~`, `/tmp`, `/dev/shm` and run by `bash FILE`, `python3 FILE`, `perl FILE`, `./FILE` after `chmod +x`, and a binary run through `/lib64/ld-linux-x86-64.so.2 FILE` |
| C10 | Shell startup files and executable program settings | `bash` (startup files `~/.bashrc`, `~/.profile`, `~/.bash_logout`), `git` 1:2.47.3-0+deb13u1 (executable settings) | a recorded line in `~/.bashrc` that sets `PATH` to include `~/bin`; a recorded git alias | appended `~/.bashrc` / `~/.profile` command that starts a program at login; a git `alias.x = !cmd` and a `core.hooksPath` hook; an `~/.config/autostart/*.desktop` entry; `~/.ssh/rc` |
| C11 | Containers | `podman` 5.4.2+ds1-2+b2 (rootless; `uidmap` 1:4.17.4-2, `slirp4netns` 1.2.1-1.1) | image `docker.io/library/alpine:3.20.3` run with `podman run` | image `docker.io/library/busybox:1.36.1`: `podman pull`, `podman run -d`, `podman build` of a one-line Containerfile, and `podman generate systemd` / quadlet file in `~/.config/containers/systemd/` |

Built-in tools tried directly with superuser privileges (Table 9, P4, “the built-in tools, including the system's own
package installer, are also tried directly with superuser privileges”): `apt-get`, `dpkg`, `useradd`/`usermod`/
`passwd`/`chpasswd`/`groupadd`, `visudo`/a file in `/etc/sudoers.d/` written with `visudo -f`, `systemctl`
(enable/disable/mask/start/edit), `nft`, `ip`, `nmcli`, `hostnamectl`, `timedatectl`, `localectl`, `modprobe`,
`sysctl -w`, `mount`. Each is run as root through the means of obtaining superuser privileges that `build/INTERFACE.md`
documents.

The command that downloads and executes code without saving it (Paper 4, Section 9.3): `curl -fsS URL | bash`,
`bash <(curl -fsS URL)` and `python3 -c "$(curl -fsS URL)"`, where URL is a script served by the host to the guest over
user-mode networking (`http://10.0.2.2:PORT/`). The script starts a background process, writes a user unit and a
crontab line, and appends to `~/.bashrc`; after a restart none of them may be in force.

## Programs of the ordinary work (Section 9.3 of the plan)

| Item | Program and exact input |
|---|---|
| Install a program | Debian `tree` 2.2.1-1, by adding its line and applying |
| Two updates, a restart after each | the whole system moved from archive state T0 to T1, then from T1 to T2 (`https://snapshot.debian.org/archive/debian/<T>/` and `…/debian-security/<T>/`). T0 = `20260801T000000Z` (point release 13.6), T1 = `20261001T000000Z` (13.7), T2 = `20261123T000000Z` (13.8, the latest); each move changes the version of installed packages, among them `linux-image-amd64` 6.12.94-1 → 6.12.107-1 → 6.12.117-1 and `libc6` 2.41-12+deb13u3 → +deb13u4 → +deb13u5 (`tools/update-diff.sh`, output `tools/update-diff.out`; 1,134 and 1,924 source lines of `Packages` change). If the base must be built at the latest state, T0 is that state and the case uses the two latest earlier states for a fresh base instead; the choice is entry Q1 of `QUESTIONS.md` |
| Work in a browser | Debian `firefox-esr` 153.5.1esr-1~deb13u1: `firefox-esr --headless --screenshot` of a page served by the host, and of a local file; the PNG must exist and be non-empty |
| Edit a document | Debian `libreoffice-writer` 4:25.2.3-2+deb13u9: `soffice --headless --convert-to odt` of a text file, a change of the text, a second conversion, and `soffice --headless --cat` of the result |
| Ordinary commands and one's own recorded script | `ls`, `cp`, `grep`, `sort`, `ed` on a file in `~`; the recorded script `~/bin/cases-report.sh` (C9) |
| Fetch, build, change, rebuild a small program | `hello.c` of docker-library/hello-world, commit `522bcd2faf422c60b9d20e64d7cd6d56600aec97`, SHA-256 `cb95a0ed950c272471e7eb2a6b4261d857174bc3750874f538ac60e20af16d34`; built with `gcc`; the greeting line changed and rebuilt, three times (step 8, history 2) |
| Launcher and the game it downloads | LinuxGSM `linuxgsm.sh` v26.5.0 (commit `50dc4e551b661b9d1fa39c291068a16a66056aff`), self-updated with `update-lgsm` to v26.6.0 (commit `9ca2e951c6e15d4db7184a60e1fd8a831b2cdb0f`); the game it downloads: Wolfenstein: Enemy Territory dedicated server 2.60b (`wetserver`), archive SHA-256 `ac359aebe0bf8fd568341876e3a8992d7c562ee6fdc4a8906bdbab47eae66cf3`; its Debian prerequisites (step 8, `h3/prerequisites.json`): `bc bsdmainutils bzip2 distro-info jq lib32gcc-s1 lib32stdc++6 libc6-i386 libevent-core-2.1-7t64 libjq1 libonig5 ncal pigz tmux unzip` |
| Installation during which the network is lost | Debian `fonts-noto-cjk` 1:20240730+repack1-1 (one `.deb` of 56,674,044 bytes, so that the link is cut while it downloads); the link is cut and restored from the host with QMP `set_link` |
| Connect to Wi-Fi (real hardware) | `network-manager` 1.52.1-1 (`nmcli`), `wpasupplicant` 2:2.10-24 — not performed in this run: real hardware |
| Pair a Bluetooth device (real hardware) | `bluez` 5.82-1.1 (`bluetoothctl`) — not performed in this run: real hardware |

## Programs of the checking side (not part of ConfOS, run on the server)

`guestfish` / `virt-ls` / `virt-cat` (libguestfs 1.54) read the stopped disk; `ssh` asks the running machine with its
standard tools (`dpkg-query`, `systemctl`, `ps`, `getent`, `lsmod`, `ss`, `nft`, `nmcli`); `qemu-system-x86_64` and
its QMP socket cut the power and the link; Python 3 runs `inventory`, `derive`, `compare` and `run`.
