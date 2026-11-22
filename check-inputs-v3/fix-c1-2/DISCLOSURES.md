# Known before the first observation

Recorded 2026-11-22 UTC. These disclosures apply to the selected input manifests.

## Check 1: rehearsal output

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

## Check 4: installer output

`C1/raw/nixos-install-transcript.txt` and `C1/raw/guix-install-transcript.txt`
contain installed package closures in installer output. The records are retained,
were not read for any property assessment, and are explicitly disclosed here.
New installations retain only exit statuses, apart from the generated NixOS
hardware declaration captured as an input before installation. TASK-C1's binding
05:20 UTC decision settles their status without an outstanding author question.

| Facts exposed | Preserved evidence relative to C1/ |
|---|---|
| NixOS sudo printed its standard lecture (privacy, thinking before typing, responsibility) and that the password would not be visible; constant user/root smoke messages also appeared. | `fix-c1-1/nixos/raw/smoke.txt`, timestamp `2026-11-22T05:18:26Z` |

The NixOS timestamp precedes the 05:20 UTC retention decision; the review's
claim that this record was made after that decision is not supported. Its omission
from the disclosure was still a gap. No property assessment was made from it.
The openSUSE diagnostic, including the rescue text and subsequent prompt
observation, was retained after the decision; this was a preparation deviation.
