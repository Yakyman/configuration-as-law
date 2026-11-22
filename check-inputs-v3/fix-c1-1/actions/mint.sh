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
