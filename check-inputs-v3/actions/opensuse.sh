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
