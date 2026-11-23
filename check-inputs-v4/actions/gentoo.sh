#!/usr/bin/env bash
ACTIONS_DIR=$(dirname "$(readlink -f "$0")")
source "$ACTIONS_DIR/lib.sh"
source "$ACTIONS_DIR/ordinary.sh"
PACKAGE_LIMIT=600
BROWSER_LIMIT=420

native_install() {
    # Source builds, using the prepared clean guest's Portage profile and USE flags.
    # https://wiki.gentoo.org/wiki/Handbook:AMD64/Working/Portage
    case "$1" in
        tree) root emerge --ask=n --noreplace app-text/tree ;;
        flatpak) root emerge --ask=n --noreplace sys-apps/flatpak ;;
        node) root emerge --ask=n --noreplace net-libs/nodejs ;;
        browser) root emerge --ask=n --noreplace www-client/firefox dev-python/pip ;;
        git) root emerge --ask=n --noreplace dev-vcs/git ;;
        network) root emerge --ask=n --noreplace net-misc/networkmanager ;;
        ssh) root emerge --ask=n --noreplace net-misc/openssh ;;
        container) root emerge --ask=n --noreplace app-containers/docker app-containers/docker-cli ;;
        *) return 64 ;;
    esac
}
user_service() {
    # https://man.openbsd.org/ssh-agent
    # Requires current OpenRC with user mode; missing user runtime state is created below.
    # https://github.com/OpenRC/openrc/blob/master/user-guide.md
    # https://github.com/OpenRC/openrc/blob/master/service-script-guide.md
    native_install ssh
    # Headless SSH may lack a PAM-created runtime directory. Create the user
    # runtime directory for native OpenRC user state; no service emulation.
    export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
    root install -d -m 700 -o "$(id -u)" -g "$(id -g)" "$XDG_RUNTIME_DIR"
    mkdir -p "$HOME/.config/rc/init.d" "$HOME/.config/rc/runlevels/default"
    cat > "$HOME/.config/rc/init.d/cal-user" <<'RC'
#!/sbin/openrc-run
description="User authentication agent"
command=/usr/bin/ssh-agent
command_args="-D -a ${XDG_RUNTIME_DIR}/cal-agent.sock"
command_background=true
pidfile="${XDG_RUNTIME_DIR}/cal-user.pid"
RC
    chmod 755 "$HOME/.config/rc/init.d/cal-user"
    rc-update --user add cal-user default
    openrc --user default
    rc-service --user cal-user status
}
start_network_manager() {
    # https://wiki.gentoo.org/wiki/NetworkManager
    # https://wiki.gentoo.org/wiki/Handbook:AMD64/Working/Initscripts
    # Migrate the DHCP primary NIC from netifrc/dhcpcd if present.
    local service
    for service in /etc/init.d/net.* /etc/init.d/dhcpcd; do
        [[ -e $service ]] || continue
        service=${service##*/}
        [[ $service != net.lo ]] || continue
        if root rc-service "$service" status >/dev/null 2>&1; then root rc-service "$service" stop; fi
        if [[ -L /etc/runlevels/default/$service ]]; then root rc-update del "$service" default; fi
        if [[ -L /etc/runlevels/boot/$service ]]; then root rc-update del "$service" boot; fi
    done
    root rc-update add dbus default
    root rc-service dbus start
    root rc-update add NetworkManager default
    root rc-service NetworkManager start
}
container_run() {
    # https://docs.docker.com/reference/cli/docker/container/run/
    # https://wiki.gentoo.org/wiki/Handbook:AMD64/Working/Initscripts
    native_install container
    root rc-update add docker default
    root rc-service docker start
    root docker run --name cal-container docker.io/library/busybox:1.37.0 /bin/echo ordinary-container
}
# Same-category alternatives evaluated after the bounded source-build rehearsal.
application_package() {
    # https://github.com/pkgforge-dev/Firefox-AppImage: self-contained AppImage.
    # A user application package does not enable a binary Portage package host.
    mkdir -p "$HOME/.local/opt" "$HOME/.local/bin"
    python3 - <<'FETCH_FIREFOX'
from pathlib import Path
import urllib.request
url = 'https://github.com/pkgforge-dev/Firefox-AppImage/releases/download/160.0.1%402026-11-20_1795187897/Firefox-160.0.1-anylinux-x86_64.AppImage'
with urllib.request.urlopen(url, timeout=180) as response:
    with (Path.home() / '.local/opt/firefox.AppImage').open('wb') as target:
        while block := response.read(1024 * 1024):
            target.write(block)
FETCH_FIREFOX
    printf '%s  %s\n' '5fa35b88256946ac33e7f92c93eaa6ce21a68b4365ce216c3a526856aefd7c24' \
        "$HOME/.local/opt/firefox.AppImage" | sha256sum --check
    chmod 755 "$HOME/.local/opt/firefox.AppImage"
    cat > "$HOME/.local/bin/firefox" <<'FIREFOX'
#!/bin/sh
export APPIMAGE_EXTRACT_AND_RUN=1 DISABLE_AUTO_UPDATES=1
exec "$HOME/.local/opt/firefox.AppImage" "$@"
FIREFOX
    chmod 755 "$HOME/.local/bin/firefox"
    "$HOME/.local/bin/firefox" --version
}
language_program() {
    # https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-t
    root emerge --ask=n --noreplace dev-python/pip
    python3 -m pip install --no-input --target "$HOME/.local/lib/cal-cowsay" cowsay
    PYTHONPATH="$HOME/.local/lib/cal-cowsay" python3 -m cowsay -t cal-test
}
browser_extension() {
    root emerge --ask=n --noreplace dev-python/pip
    python3 -m pip install --no-input --target "$HOME/.local/lib/cal-marionette" marionette_driver
    export PATH="$HOME/.local/bin:$PATH"
    mkdir -p "$HOME/.mozilla/firefox/cal-check" "$HOME/Downloads"
    firefox --headless -CreateProfile "cal-check $HOME/.mozilla/firefox/cal-check"
    PYTHONPATH="$HOME/.local/lib/cal-marionette" python3 "$ACTIONS_DIR/gentoo-firefox-addon.py"
}
network_connection() {
    # Same Section 9.2 network connection via the installed DHCP client.
    # https://man.archlinux.org/man/dhcpcd.8.en
    local device interface=''
    for device in /sys/class/net/*; do
        if [[ $(cat "$device/address") == 52:54:00:ca:10:02 ]]; then
            interface=${device##*/}
            break
        fi
    done
    [[ -n $interface ]] || return 79
    mkdir -p "$HOME/.config"
    cat > "$HOME/.config/cal-secondary-dhcpcd.conf" <<CONF
interface $interface
nogateway
noipv4ll
nohook resolv.conf,hostname
CONF
    root ip link set "$interface" up
    root dhcpcd --config "$HOME/.config/cal-secondary-dhcpcd.conf" \
        --ipv4only --waitip=4 --timeout 90 "$interface"
    ip -4 -o address show dev "$interface" scope global | grep -q ' inet '
}


actions_main "$@"
