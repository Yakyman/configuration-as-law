# Check 1 concrete inputs

Prepared 2026-11-22 UTC. Publication date is taken in UTC by the binding
TASK-C1 decision: cutoff 2026-11-21T23:59:59Z. Last joint look of the seven release
pages completed at 2026-11-22T05:14:22Z (`../fix-c1-1/raw/release-recheck.md` and JSON).
The later openSUSE look was 2026-11-22T05:15:24Z
(`../fix-c1-1/opensuse/raw/release-evidence.md`); the selected release is unchanged.
This versioned input record has not yet been committed to the repository of
check records. Commit these exact files before any first check observation.
No classification or property assessment is performed by laboratory preparation.
Runner version and system-by-system validation: `RUNNER-VALIDATION.md`.

## Releases and verified images

| System | Release | Image checksum | Release evidence |
|---|---|---|---|
| fedora | 45-1.4 | SHA256 `68338c6bfe4f0d64151f2e47efe9f44a8855ad05b460e56b844fb3fa2c9a3beb` | [2026-11-03](https://fedoraproject.org/workstation/download/): Download Fedora Workstation 45; RELEASE DATE: Tuesday, November 3, 2026 |
| opensuse | 20261120 | SHA256 `d60d111e1ee2bdfe2501e6bf50167e1e49293c31a69a52ef37ffa75aa2eb1e55` | [2026-11-21](https://download.opensuse.org/tumbleweed/iso/): openSUSE-Tumbleweed-DVD-x86_64-Snapshot20261120-Media.iso \| 21-Nov-2026 01:40 \| 4.3GiB |
| mint | 22.3 Cinnamon | SHA256 `a081ab202cfda17f6924128dbd2de8b63518ac0531bcfe3f1a1b88097c459bd4` | [2026-01-13](https://blog.linuxmint.com/?p=4981): The team is proud to announce the release of Linux Mint 22.3 “Zena”. |
| flatcar | 4757.2.3 stable | SHA512 `9a9858f45d9c00774f865f38cba856e866f937a49cebaae8a69c4849275dc347edb51499dd145a8a9ac49098ced8ff6f2b66f65242f8b85cb06910c3b9c38e4f` | [2026-10-29](https://www.flatcar.org/releases/): Release Date: Oct 29, 2026 |
| talos | 1.14.6 | SHA256 `c2264437db0ea7949771ce941940a95e049ce4e84f7b1860be067834137b8f23` | [2026-11-11](https://github.com/siderolabs/talos/releases/tag/v1.14.6): Talos 1.14.6 (2026-11-11) |

Image URLs, signature URLs and checksum references: `releases.tsv`, SHA256 `b289d1c8428eab859cfa36db6dda9c719d3f696a40438f64905cfaa89df4f08d`.
Original image verification is retained under `../raw/`; new openSUSE evidence is
under `../fix-c1-1/opensuse/raw/`. Mint command provenance: `STATUS-mint.md`.
NixOS has a published checksum; no ISO signature was linked by the consulted page.

## Clean installations and installation declarations

The Flatcar Ignition and Talos machine configuration are installation declarations.
openSUSE uses the official YaST DVD Snapshot20261120 and the system role
“Desktop with KDE Plasma”, the first role in the installer list. This is a choice
of this check under TASK-C1, not an installer default. Other defaults are retained.

| Selected installation input | SHA256 |
|---|---|
| `../install/fedora/ACTIONS.md` | `6147145d238122d550b30e3b3be159d1bf08709cda4138ec94369dd6eb184f55` |
| `../install/fedora/RECIPE.md` | `f9f9c5a7f500f56b02ede8281e5e0b3f553960d0f74360b6762300f5be6cfb96` |
| `../install/fedora/download-verify.sh` | `b4bdd9b6116e3ccf15171ff6ce41701e44f88cfb6f1c507027dc1b853446d767` |
| `../install/fedora/install.sh` | `c4459850bc4dde5c3f004e5f36e36646213e69a9f2664c8655a5573af573e8a3` |
| `../install/fedora/ks.cfg` | `20c244ffb25b9fe9cd767b12be6f797fb46a3094f56cc6c8d6fbb376ab4a7913` |
| `../fix-c1-1/opensuse/RECIPE.md` | `50cdee71fdcc619c0ca9d00f5c6b3c2476871888d6985cd78e36c6b162ccc552` |
| `../fix-c1-1/opensuse/launch.sh` | `d0a576608d8f738110c1548df7b3dbcfa8b69721e70812ae67958ca8efe8f6c1` |
| `../fix-c1-1/opensuse/verify-start.sh` | `933a74570ad530a86aab6851186763abcab9e794cb235d908425fc153ac1e375` |
| `../fix-c1-1/opensuse/terminal.py` | `607bc461d710db0ca74fc2c3512ed7d19cacada34e3183a5a6b7229a92582152` |
| `../fix-c1-1/opensuse/ui.py` | `9b4f900fbb17c867bfff7fdb51d8788b4a3e8310ad24d928d26f66c17fffdf80` |
| `../fix-c1-1/opensuse/raw/input-events.jsonl` | `1291f7cc9adee2bab38685eda32454e02793b4f31eb5c73d0cd20058b9b7bdbe` |
| `../fix-c1-1/opensuse/register.sh` | `a22a7c20cf80e5ebd0b0912c4c1a5e43ac57f353772719dd552acab54f9e4756` |
| `../install/mint/README.md` | `a3927f9610347a23c6e18c995aaa25fa6af08b1868a72624820e479ae2d8af25` |
| `../install/mint/boot.sh` | `1ff05f82268f3d9c1a046505ee743c050c088a668c57fc515921113485df1e14` |
| `../install/mint/console-input.py` | `bf3b485221fdd498d61f181cd310f0276460ae1a2c7dec11c93b4327b14ec6a8` |
| `../install/mint/enable-serial.sh` | `7152450c7d89a46519a45af0a1fadb68a41a11589007c5e9d3b28b8f1fe3882e` |
| `../install/mint/preseed.cfg` | `d8a99fa8af8aad824921622ef4394abe3cefa1277b72b6dfcd770ef7f37ce8e4` |
| `../install/mint/sendkey.py` | `2ba38e24d266bfecfea1a9b842c1bc37b43247bf6f77993e176c67975a460cd5` |
| `../install/flatcar/README.md` | `6be71bc334217aa5f9888cdc05f9535cd1eb09b7abba939a72f52f63dc8d55a9` |
| `../install/flatcar/boot.sh` | `d5d40da469d40a0a637ac07e772cca1a54f0de2ff43797958858d55a3061c3b6` |
| `../install/flatcar/ignition.json` | `b2096e195e8796f484e4ba1fdbddf2030572d7c9e6b6a22aeee9ee4d872794ab` |
| `../install/talos/README.md` | `9c2d5951207302e3ede228cfd336da8dbcac892b1d429a8286b447d66d147f5b` |
| `../install/talos/boot.sh` | `c37f7291349e9841a54995ceb3c54f5d16c020463b35faa628ff29a72011b99a` |
| `../install/talos/controlplane.yaml` | `b1cd87a66e85c2d239b213c2231370247d3e8b4e396119d76ebfc199258933fb` |

Only files in this table are selected installation inputs. Other files preserve
preparation history. Installation system defaults remain as recorded in recipes.

## Ordinary actions

The exact scripts below run as the ordinary user on fresh disposable desktop
clones. The user timer is the concrete form of the user script in the home
directory: the script runs once and is scheduled. The saved `cal-test` Wi-Fi
profile is the concrete form of connecting to a network on a machine without a
radio; the second virtual NIC uses MAC `52:54:00:ca:10:02`. No action enables
lingering. These input choices do not add conditions to the published text.

### Known before the first observation

The package-manager program was changed from `tree` to `hello` after a Fedora
rehearsal reported `tree` already installed. This is a preparation deviation;
it cannot be undone by suppressing subsequent output. The backing images remain
the check machines by TASK-C1's binding decision of 05:20 UTC. No subsequent
program choice is based on rehearsal output. The round-1 ordinary-action commands discarded guest stdout/stderr, but console
and smoke output were retained as disclosed below. Round-2 smoke runs retain
exit statuses only, discarding all command stdout/stderr.

| Facts exposed | Preserved evidence relative to C1/ |
|---|---|
| `tree-2.3.1-2.fc45.x86_64`, `podman-5:6.1.3-1.fc45.x86_64`, `flatpak-1.19.0^really1.18.4-1.fc45.x86_64` already installed on the Fedora clone | `raw/fedora-actions-attempt3-recovered.log`, lines 16–18; the input change is also documented in `raw/fedora-actions-preflight.txt` and `raw/instrument-corrections.md` |
| Fedora installed `hello` version `0:2.12.3-2.fc45` and weak dependency `info` version `0:7.3-3.fc45`; `podman` and `flatpak` reported already installed | `raw/fedora-actions.log`, package table and transaction output |
| Mint reported 0 upgraded, 17 newly installed, 0 removed, 498 not upgraded; 459783 files/directories in its database | `raw/mint-actions.txt`, summary and database progress |
| Mint's 17 new packages: `aardvark-dns`, `buildah`, `catatonit`, `conmon`, `containernetworking-plugins`, `crun`, `fuse-overlayfs`, `golang-github-containers-common`, `golang-github-containers-image`, `hello`, `libslirp0`, `libsubid4`, `netavark`, `passt`, `podman`, `slirp4netns`, `uidmap` | `raw/mint-actions.txt`, NEW packages and Get lines (the latter retain exact versions) |
| Mint suggested `containers-storage`, `libwasmedge0`, `docker-compose`; trigger output named `man-db`, `install-info`, `libc-bin` | `raw/mint-actions.txt`; suggestions do not establish installation |
| Fedora and Mint Flatpak output named `org.freedesktop.Platform.GL.default` branches `26.08` and `26.08-extra`, `org.freedesktop.Platform.codecs-extra/26.08-extra`, `org.gnome.Calculator.Locale/stable`, `org.gnome.Platform.Locale/51`, `org.gnome.Platform/51`, `org.gnome.Calculator/stable`; Mint additionally named `org.gtk.Gtk3theme.Mint-Y-Aqua/3.22` (all x86_64) | `raw/fedora-actions-attempt3-recovered.log`, `raw/fedora-actions.log`, `raw/mint-actions.txt` |
| Container pulls and runs exposed `docker.io/library/alpine:3.22` on Fedora and `docker.io/library/busybox:1.37.0` on Mint; their digest output is retained | Same rehearsal logs |
| openSUSE diagnostic retained “You are in rescue mode.”, “Enter root password for maintenance”, “Failed to start Save Transient machine-id to Disk.” and ordinary-user prompt terminator `>`. The prompt pattern was changed after this output and confirmed from the cited aaa_base source; this informed transport repair, not program selection. The rescue cause is not established. | `fix-c1-1/opensuse/raw/boot-transport-diagnostic.txt`; `fix-c1-1/raw/opensuse-prompt-plan.md` quotes https://raw.githubusercontent.com/openSUSE/aaa_base/master/files/etc/bash.bashrc |

Rehearsals also printed network-profile creation, timer symlink creation and
constant script/container output. They are authorized action results, retained
in the same logs; no classification or property assessment was made from them.


### fedora

File: `../actions/fedora.sh`; SHA256 `9a0b6b477cb6423e448387671d59fc03645b6738a5d9cb2ee1d58359dec1f05a`.

```bash
#!/bin/bash
# Run as user on a disposable desktop clone, never on its backing image.
set -euo pipefail
as_root() { printf '%s\n' cal-test | sudo -S -- "$@"; }
as_root dnf -y install hello podman flatpak
flatpak --user remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak --user install --noninteractive -y flathub org.gnome.Calculator
as_root nmcli connection add type ethernet con-name cal-secondary ifname '*' 802-3-ethernet.mac-address 52:54:00:ca:10:02 ipv4.method auto ipv4.never-default yes ipv6.method disabled
as_root nmcli --wait 60 connection up cal-secondary
as_root nmcli connection add type wifi con-name cal-test ifname '*' ssid cal-test connection.autoconnect no wifi-sec.key-mgmt wpa-psk wifi-sec.psk cal-test-password
mkdir -p "$HOME/.local/bin" "$HOME/.config/systemd/user"
cat > "$HOME/.local/bin/cal-hello" <<'SCRIPT'
#!/bin/sh
printf '%s\n' 'cal-test' >> "$HOME/cal-test.log"
SCRIPT
chmod 755 "$HOME/.local/bin/cal-hello"
"$HOME/.local/bin/cal-hello"
cat > "$HOME/.config/systemd/user/cal-hello.service" <<'UNIT'
[Unit]
Description=Write the laboratory greeting
[Service]
Type=oneshot
ExecStart=%h/.local/bin/cal-hello
UNIT
cat > "$HOME/.config/systemd/user/cal-hello.timer" <<'UNIT'
[Unit]
Description=Schedule the laboratory greeting
[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
[Install]
WantedBy=timers.target
UNIT
systemctl --user daemon-reload
systemctl --user enable --now cal-hello.timer
podman run --name cal-container docker.io/library/alpine:3.22 /bin/echo cal-test
```

### opensuse

File: `../actions/opensuse.sh`; SHA256 `057f88461ea541deaab6abeff28a3c9d6958e7528241f3408c357c16d4e191fe`.

```bash
#!/bin/bash
# Run as user on a disposable desktop clone, never on its backing image.
set -euo pipefail
as_root() { printf '%s\n' cal-test | sudo -S -- "$@"; }
as_root zypper --non-interactive install hello podman flatpak
flatpak --user remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak --user install --noninteractive -y flathub org.gnome.Calculator
as_root nmcli connection add type ethernet con-name cal-secondary ifname '*' 802-3-ethernet.mac-address 52:54:00:ca:10:02 ipv4.method auto ipv4.never-default yes ipv6.method disabled
as_root nmcli --wait 60 connection up cal-secondary
as_root nmcli connection add type wifi con-name cal-test ifname '*' ssid cal-test connection.autoconnect no wifi-sec.key-mgmt wpa-psk wifi-sec.psk cal-test-password
mkdir -p "$HOME/.local/bin" "$HOME/.config/systemd/user"
cat > "$HOME/.local/bin/cal-hello" <<'SCRIPT'
#!/bin/sh
printf '%s\n' 'cal-test' >> "$HOME/cal-test.log"
SCRIPT
chmod 755 "$HOME/.local/bin/cal-hello"
"$HOME/.local/bin/cal-hello"
cat > "$HOME/.config/systemd/user/cal-hello.service" <<'UNIT'
[Unit]
Description=Write the laboratory greeting
[Service]
Type=oneshot
ExecStart=%h/.local/bin/cal-hello
UNIT
cat > "$HOME/.config/systemd/user/cal-hello.timer" <<'UNIT'
[Unit]
Description=Schedule the laboratory greeting
[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
[Install]
WantedBy=timers.target
UNIT
systemctl --user daemon-reload
systemctl --user enable --now cal-hello.timer
podman run --name cal-container docker.io/library/alpine:3.22 /bin/echo cal-test
```

### mint

File: `../fix-c1-1/actions/mint.sh`; SHA256 `bf617770327e50a4d72a8475c5d5c8ffca112aa71bf3c54406c8c716a90549c5`.

```bash
#!/bin/bash
# Run as ordinary user on a disposable clone only.
set -euo pipefail
# Authenticate using the isolated lab account; keep sudo policy unchanged.
sudo() { command sudo -S -p "" "$@" <<< "cal-test"; }
sudo env DEBIAN_FRONTEND=noninteractive apt-get update
sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y hello podman
flatpak --user remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak --user install --noninteractive -y flathub org.gnome.Calculator
sudo nmcli connection add type ethernet ifname '*' 802-3-ethernet.mac-address 52:54:00:ca:10:02 con-name cal-wired ipv4.method auto ipv4.never-default yes ipv6.method disabled
sudo nmcli connection up cal-wired
sudo nmcli connection add type wifi ifname '*' con-name cal-test ssid cal-test connection.autoconnect no ipv4.method auto ipv6.method disabled
sudo nmcli connection modify cal-test wifi-sec.key-mgmt wpa-psk wifi-sec.psk cal-test-passphrase
mkdir -p "$HOME/.local/bin" "$HOME/.config/systemd/user"
cat > "$HOME/.local/bin/cal-user-script" <<'EOF'
#!/bin/sh
printf 'ordinary-action\n' >> "$HOME/cal-user-script.log"
EOF
chmod 755 "$HOME/.local/bin/cal-user-script"
"$HOME/.local/bin/cal-user-script"
cat > "$HOME/.config/systemd/user/cal-user-script.service" <<'EOF'
[Unit]
Description=Ordinary user script
[Service]
Type=oneshot
ExecStart=%h/.local/bin/cal-user-script
EOF
cat > "$HOME/.config/systemd/user/cal-user-script.timer" <<'EOF'
[Unit]
Description=Ordinary user timer
[Timer]
OnBootSec=10min
OnUnitActiveSec=1h
[Install]
WantedBy=timers.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now cal-user-script.timer
podman run --name cal-container docker.io/library/busybox:1.37.0 /bin/sh -c 'printf "ordinary-container\n"'
```

## Inventory instruments

`../fix-c1-1/lab.sh` SHA256 `0439b40388810002c9c9cb67be444e57f706d71e07ccd288542f7eeb5d0834db`.

`../fix-c1-1/collector/collect.sh` SHA256 `487b5290c97cc356be80264064ce1e8468c7015051412857eca62658cee47c1d`.

`../fix-c1-1/collector/talos-collect.sh` SHA256 `3a16bfad0fd1e914503dc517bd123f6aa56c3a7a2a97bbba0aaa009ad31a4802`.

The collector follows exactly the kinds named in Section 4.2 and the binding
TASK-C1 collection instructions. Conservative unresolved ownership and API
limitations are disclosed in `../fix-c1-1/collector/COLLECT.md` and `../fix-c1-1/collector/TALOS-COLLECT.md`.
A missing API inventory is reported as not inventoried, never as an absent object.
The general collector is developed and tested only on disposable Debian. The
Talos collection procedure is documentation-only and has not run on Talos.

## Classification and adjudication procedure (five lines)

The inventory is compiled with system tools.
Each object is decided twice, independently: whether it must be recorded.
Agreement is measured as the share of matching decisions and by Cohen’s kappa; an agreement threshold is not a condition of the check.
The two classifications are independent: each is made separately and without access to the other.
When they differ, a separate adjudication, made by neither classification, decides whether the text of Sections 2 and 3 resolves the case and quotes the sentence that resolves it; if no sentence resolves it, the case yields 0.
