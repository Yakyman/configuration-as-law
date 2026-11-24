#!/usr/bin/env bash
ACTIONS_DIR=$(dirname "$(readlink -f "$0")")
source "$ACTIONS_DIR/lib.sh"
source "$ACTIONS_DIR/ordinary.sh"
PACKAGE_LIMIT=1800
BROWSER_LIMIT=1800

native_install() {
    # https://dnf.readthedocs.io/en/latest/command_ref.html
    case "$1" in
        tree) root dnf -y install tree ;;
        flatpak) root dnf -y install flatpak ;;
        node) root dnf -y install nodejs npm ;;
        browser) root dnf -y install firefox python3 python3-pip ;;
        git) root dnf -y install git ;;
        network) root dnf -y install NetworkManager ;;
        ssh) root dnf -y install openssh-clients ;;
        container) root dnf -y install podman ;;
        *) return 64 ;;
    esac
}
user_service() {
    # https://man.openbsd.org/ssh-agent
    # https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
    # https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
    native_install ssh
    mkdir -p "$HOME/.config/systemd/user"
    cat > "$HOME/.config/systemd/user/cal-user.service" <<'UNIT'
[Unit]
Description=User authentication agent
[Service]
ExecStart=/usr/bin/ssh-agent -D -a %t/cal-agent.sock
Restart=on-failure
[Install]
WantedBy=default.target
UNIT
    systemctl --user daemon-reload
    systemctl --user enable --now cal-user.service
    systemctl --user is-active --quiet cal-user.service
}
start_network_manager() {
    root systemctl enable --now NetworkManager.service
}
container_run() {
    # https://docs.podman.io/en/latest/markdown/podman-run.1.html
    native_install container
    root podman run --name cal-container docker.io/library/busybox:1.37.0 /bin/echo ordinary-container
}
actions_main "$@"
