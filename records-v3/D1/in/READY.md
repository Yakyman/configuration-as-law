INVENTORY: 4 of 5 machines

Recorded 2026-11-22T09:08:55.302808+00:00.

Committed releases and inputs: (not published: outside selected checks and direct evidence), fixed by `GATES/INPUTS-1-PUSHED` at commit `43594a47b72707f836953b6b39d5849d5513f61a`. Input and remote instrument hashes: `control/input-verification.json`, `control/remote-instrument-hashes.json`.

Tables retain every row of the collector’s own `objects.tsv`, in the same order, with machine-prefixed identifiers and `L<level>:<kind>`. Names and members are unchanged. Evidence paths resolve from this directory. Produced inventories may be partial: failed queries are documented below and in the raw coverage records. No classification or hypothesis outcome is assigned.

Execution adaptations: the user-requested continuation after each failed command replaces the action scripts’ global stop-on-error behavior; command bodies are unchanged. The unchanged runner is deployed as task-local `lab.sh`, the filename required by the collector. Tumbleweed uses the committed runner system identifier `opensuse`. Host-only connection and service-launch adjustments are documented in `control/operator-notes.md`. These deployment details do not change committed command bodies, releases, runner bytes, collector bytes or VM bases. No object was selected by the operator, and no ordinary-action command body was changed, repaired, replaced or repeated.

## fedora

Committed release: **45-1.4**. Inventory objects: **5887**. Table: `part-fedora.tsv`.

| Kind | Objects |
|---|---:|
| L1:access-rule | 3 |
| L1:account | 54 |
| L1:container | 1 |
| L1:container-image | 1 |
| L1:driver | 61 |
| L1:firewall-chain | 84 |
| L1:firewall-ct helper | 1 |
| L1:firewall-rule | 136 |
| L1:firewall-table | 1 |
| L1:group | 83 |
| L1:module | 51 |
| L1:network | 5 |
| L1:network-link | 3 |
| L1:package:flatpak | 7 |
| L1:package:rpm | 3954 |
| L1:polkit-actions | 542 |
| L1:port | 12 |
| L1:process | 50 |
| L1:service | 216 |
| L1:timer | 7 |
| L1:unit-file | 474 |
| L1:user-service | 13 |
| L1:user-timer | 3 |
| L1:user-unit-file | 125 |

Source: `raw/fedora/objects.tsv`; counts: `control/object-counts.json`.

Ordinary actions: 15 commands succeeded; 0 failed; 0 without a recorded exit status. Exact command bodies: `control/actions-fedora.json`; output and per-command status: `control/fedora/actions.log`.

| Action command | Exit |
|---|---:|
| 01: `as_root dnf -y install hello podman flatpak` | 0 |
| 02: `flatpak --user remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo` | 0 |
| 03: `flatpak --user install --noninteractive -y flathub org.gnome.Calculator` | 0 |
| 04: `as_root nmcli connection add type ethernet con-name cal-secondary ifname '*' 802-3-ethernet.mac-address <MAC> ipv4.method auto ipv4.never-default yes ipv6.method disabled` | 0 |
| 05: `as_root nmcli --wait 60 connection up cal-secondary` | 0 |
| 06: `as_root nmcli connection add type wifi con-name <SSID> ifname '*' ssid <SSID> connection.autoconnect no wifi-sec.key-mgmt wpa-psk wifi-sec.psk <REDACTED>` | 0 |
| 07: `mkdir -p "$HOME/.local/bin" "$HOME/.config/systemd/user"` | 0 |
| 08: `cat > "$HOME/.local/bin/cal-hello" <<'SCRIPT'` | 0 |
| 09: `chmod 755 "$HOME/.local/bin/cal-hello"` | 0 |
| 10: `"$HOME/.local/bin/cal-hello"` | 0 |
| 11: `cat > "$HOME/.config/systemd/user/cal-hello.service" <<'UNIT'` | 0 |
| 12: `cat > "$HOME/.config/systemd/user/cal-hello.timer" <<'UNIT'` | 0 |
| 13: `systemctl --user daemon-reload` | 0 |
| 14: `systemctl --user enable --now cal-hello.timer` | 0 |
| 15: `podman run --name cal-container docker.io/library/alpine:3.22 /bin/echo cal-test` | 0 |

Collector coverage: 118 records, 74 with a nonzero recorded status. See `raw/fedora/coverage.tsv` and `raw/fedora/metadata.json`. Query failures and documented coverage limitations are not evidence of absent objects.

Filesystem coverage is incomplete: the committed filesystem query exited 1. The collector emitted 0 level-2 rows; missing stored-object rows do not establish absence. Evidence: `raw/fedora/metadata.json` and the filesystem query records in `raw/fedora/raw/`.

Transport coverage failures: 1 serial-login timeouts; 2 serial-command timeouts. Each is retained in the collector stderr files. No retry or transport repair was performed.

Deviations from the selected releases, command bodies and collector: none. The execution adaptations above apply.

Cleanup: VM directory removed = true. Lifecycle evidence: `control/fedora/status.json` and `control/fedora/destroy.log`.

## tumbleweed

Committed release: **20261120**. Inventory objects: **6779**. Table: `part-tumbleweed.tsv`.

| Kind | Objects |
|---|---:|
| L1:access-rule | 4 |
| L1:account | 27 |
| L1:container | 1 |
| L1:container-image | 1 |
| L1:driver | 62 |
| L1:firewall-chain | 139 |
| L1:firewall-rule | 207 |
| L1:firewall-table | 1 |
| L1:group | 50 |
| L1:module | 84 |
| L1:network | 5 |
| L1:package:flatpak | 8 |
| L1:package:gem | 190 |
| L1:package:pip | 90 |
| L1:package:pip3 | 90 |
| L1:package:rpm | 4780 |
| L1:polkit-actions | 304 |
| L1:port | 6 |
| L1:process | 83 |
| L1:service | 174 |
| L1:timer | 14 |
| L1:unit-file | 319 |
| L1:user-service | 47 |
| L1:user-timer | 4 |
| L1:user-unit-file | 89 |

Source: `raw/tumbleweed/objects.tsv`; counts: `control/object-counts.json`.

Ordinary actions: 15 commands succeeded; 0 failed; 0 without a recorded exit status. Exact command bodies: `control/actions-tumbleweed.json`; output and per-command status: `control/tumbleweed/actions.log`.

| Action command | Exit |
|---|---:|
| 01: `as_root zypper --non-interactive install hello podman flatpak` | 0 |
| 02: `flatpak --user remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo` | 0 |
| 03: `flatpak --user install --noninteractive -y flathub org.gnome.Calculator` | 0 |
| 04: `as_root nmcli connection add type ethernet con-name cal-secondary ifname '*' 802-3-ethernet.mac-address <MAC> ipv4.method auto ipv4.never-default yes ipv6.method disabled` | 0 |
| 05: `as_root nmcli --wait 60 connection up cal-secondary` | 0 |
| 06: `as_root nmcli connection add type wifi con-name <SSID> ifname '*' ssid <SSID> connection.autoconnect no wifi-sec.key-mgmt wpa-psk wifi-sec.psk <REDACTED>` | 0 |
| 07: `mkdir -p "$HOME/.local/bin" "$HOME/.config/systemd/user"` | 0 |
| 08: `cat > "$HOME/.local/bin/cal-hello" <<'SCRIPT'` | 0 |
| 09: `chmod 755 "$HOME/.local/bin/cal-hello"` | 0 |
| 10: `"$HOME/.local/bin/cal-hello"` | 0 |
| 11: `cat > "$HOME/.config/systemd/user/cal-hello.service" <<'UNIT'` | 0 |
| 12: `cat > "$HOME/.config/systemd/user/cal-hello.timer" <<'UNIT'` | 0 |
| 13: `systemctl --user daemon-reload` | 0 |
| 14: `systemctl --user enable --now cal-hello.timer` | 0 |
| 15: `podman run --name cal-container docker.io/library/alpine:3.22 /bin/echo cal-test` | 0 |

Collector coverage: 118 records, 72 with a nonzero recorded status. See `raw/tumbleweed/coverage.tsv` and `raw/tumbleweed/metadata.json`. Query failures and documented coverage limitations are not evidence of absent objects.

Filesystem coverage is incomplete: the committed filesystem query exited 1. The collector emitted 0 level-2 rows; missing stored-object rows do not establish absence. Evidence: `raw/tumbleweed/metadata.json` and the filesystem query records in `raw/tumbleweed/raw/`.

Transport coverage failures: 0 serial-login timeouts; 2 serial-command timeouts. Each is retained in the collector stderr files. No retry or transport repair was performed.

Deviations from the selected releases, command bodies and collector: none. The execution adaptations above apply.

Cleanup: VM directory removed = true. Lifecycle evidence: `control/tumbleweed/status.json` and `control/tumbleweed/destroy.log`.

## mint

Committed release: **22.3 Cinnamon**. Inventory objects: **2031**. Table: `part-mint.tsv`.

| Kind | Objects |
|---|---:|
| L1:account | 48 |
| L1:group | 78 |
| L1:package:dpkg-query | 1905 |

Source: `raw/mint/objects.tsv`; counts: `control/object-counts.json`.

Ordinary actions: 17 commands succeeded; 0 failed; 0 without a recorded exit status. Exact command bodies: `control/actions-mint.json`; output and per-command status: `control/mint/actions.log`.

| Action command | Exit |
|---|---:|
| 01: `sudo env DEBIAN_FRONTEND=noninteractive apt-get update` | 0 |
| 02: `sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y hello podman` | 0 |
| 03: `flatpak --user remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo` | 0 |
| 04: `flatpak --user install --noninteractive -y flathub org.gnome.Calculator` | 0 |
| 05: `sudo nmcli connection add type ethernet ifname '*' 802-3-ethernet.mac-address <MAC> con-name cal-wired ipv4.method auto ipv4.never-default yes ipv6.method disabled` | 0 |
| 06: `sudo nmcli connection up cal-wired` | 0 |
| 07: `sudo nmcli connection add type wifi ifname '*' con-name <SSID> ssid <SSID> connection.autoconnect no ipv4.method auto ipv6.method disabled` | 0 |
| 08: `sudo nmcli connection modify <SSID> wifi-sec.key-mgmt wpa-psk wifi-sec.psk <REDACTED>` | 0 |
| 09: `mkdir -p "$HOME/.local/bin" "$HOME/.config/systemd/user"` | 0 |
| 10: `cat > "$HOME/.local/bin/cal-user-script" <<'EOF'` | 0 |
| 11: `chmod 755 "$HOME/.local/bin/cal-user-script"` | 0 |
| 12: `"$HOME/.local/bin/cal-user-script"` | 0 |
| 13: `cat > "$HOME/.config/systemd/user/cal-user-script.service" <<'EOF'` | 0 |
| 14: `cat > "$HOME/.config/systemd/user/cal-user-script.timer" <<'EOF'` | 0 |
| 15: `systemctl --user daemon-reload` | 0 |
| 16: `systemctl --user enable --now cal-user-script.timer` | 0 |
| 17: `podman run --name cal-container docker.io/library/busybox:1.37.0 /bin/sh -c 'printf "ordinary-container\n"'` | 0 |

Collector coverage: 110 records, 106 with a nonzero recorded status. See `raw/mint/coverage.tsv` and `raw/mint/metadata.json`. Query failures and documented coverage limitations are not evidence of absent objects.

Filesystem coverage is incomplete: the committed filesystem query exited 1. The collector emitted 0 level-2 rows; missing stored-object rows do not establish absence. Evidence: `raw/mint/metadata.json` and the filesystem query records in `raw/mint/raw/`.

Transport coverage failures: 96 serial-login timeouts; 0 serial-command timeouts. Each is retained in the collector stderr files. No retry or transport repair was performed.

Deviations from the selected releases, command bodies and collector: none. The execution adaptations above apply.

Cleanup: VM directory removed = true. Lifecycle evidence: `control/mint/status.json` and `control/mint/destroy.log`.

## flatcar

Committed release: **4757.2.3 stable**. Inventory objects: **1827**. Table: `part-flatcar.tsv`.

| Kind | Objects |
|---|---:|
| L1:access-rule | 125 |
| L1:account | 39 |
| L1:driver | 29 |
| L1:group | 67 |
| L1:login-key | 1 |
| L1:module | 73 |
| L1:network-link | 3 |
| L1:package:system-image | 1 |
| L1:polkit-actions | 136 |
| L1:port | 8 |
| L1:process | 33 |
| L1:saved-network | 1 |
| L1:service | 132 |
| L1:timer | 7 |
| L1:unit-file | 296 |
| L1:user-service | 5 |
| L1:user-timer | 1 |
| L1:user-unit-file | 18 |
| L2:executable-code-outside-packages | 466 |
| L2:stored-outside-packages | 386 |

Source: `raw/flatcar/objects.tsv`; counts: `control/object-counts.json`.

Ordinary actions: not applicable to this system under the committed inputs.

Collector coverage: 124 records, 84 with a nonzero recorded status. See `raw/flatcar/coverage.tsv` and `raw/flatcar/metadata.json`. Query failures and documented coverage limitations are not evidence of absent objects.

Deviations from the selected releases, command bodies and collector: none. The execution adaptations above apply.

Identifier mapping: 8 repeated source ID occurrences receive an occurrence suffix; no row is removed.

Cleanup: VM directory removed = true. Lifecycle evidence: `control/flatcar/status.json` and `control/flatcar/destroy.log`.

## talos

Committed release: **1.14.6**. Inventory objects: **0**. Table: `part-talos.tsv`.

Inventory unavailable: Entire collector attempt terminated: its first pagemap read had streamed more than 137 GB after 1112 seconds; the saved listing contains 359 pagemap paths and 114323 regular files, all read fully without a bound before objects.tsv is written. Completion tonight is not credible. No repair, selective continuation or rerun.

Single-attempt termination is an execution deviation. Evidence: `control/talos/termination.json`, `control/talos/host-read-observation.json`, `control/talos/listing-operational-counts.json`, and independent review `control/review-talos-operation.md`. The partial API outputs remain under `raw/talos/raw/`; no object table was synthesized from them.

Ordinary actions: not applicable to this system under the committed inputs.

Execution failures/deviations: collector exited -15 (`control/talos/collector.log`). No failed ordinary-action command or collector observation was repeated.

Cleanup: VM directory removed = true. Lifecycle evidence: `control/talos/status.json` and `control/talos/destroy.log`.

Transfer and final cleanup: 1517 retained files matched their remote sizes and SHA-256 checksums before installation. Fresh local and remote checksums matched again before server staging was removed. No task process remained; all five VM directories were absent; 4 shared symlink targets were confirmed preserved. Evidence: `control/transfer-manifest.json`, `control/transfer-verification.json`, and `control/server-cleanup.json`.

Independent final acceptance and its scope: `control/review-final.md`.
