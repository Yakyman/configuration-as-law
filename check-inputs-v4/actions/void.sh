#!/usr/bin/env bash
ACTIONS_DIR=$(dirname "$(readlink -f "$0")")
source "$ACTIONS_DIR/lib.sh"
source "$ACTIONS_DIR/ordinary.sh"
PACKAGE_LIMIT=2400
BROWSER_LIMIT=2400

native_install() {
    # https://docs.voidlinux.org/xbps/index.html
    # https://man.voidlinux.org/xbps-install.1
    case "$1" in
        tree)
            # XBPS requires its own update transaction before newer repositories.
            # https://github.com/void-linux/xbps/blob/master/bin/xbps-install/transaction.c
            root xbps-install -Suy xbps
            root xbps-install -Suy
            root xbps-install -Sy tree ;;
        flatpak) root xbps-install -Sy flatpak ;;
        # Update installed C++ and SQLite runtimes explicitly: current Node
        # needs a newer C++ ABI and SQLite session support.
        # xbps-install(1): named installed packages are updated from repositories.
        node) root xbps-install -Sy nodejs 'libstdc++' sqlite ;;
        browser) root xbps-install -Sy firefox python3 python3-pip ;;
        git) root xbps-install -Sy git ;;
        network) root xbps-install -Sy NetworkManager dbus ;;
        ssh) root xbps-install -Sy openssh ;;
        container) root xbps-install -Sy docker ;;
        *) return 64 ;;
    esac
}
language_step() {
    local label=$1 start finish rc
    shift
    start=$(date +%s)
    set +e
    "$@"
    rc=$?
    set -e
    finish=$(date +%s)
    printf '%s\t%d\t%d\n' "$label" "$rc" "$((finish-start))" >> "$HOME/actions-status.tsv"
    return "$rc"
}
language_program() {
    language_step language_install_node native_install node
    # A project lock retains npm's direct/dependency installation records.
    language_step language_npm_install npm install --prefix "$HOME/.local" cowsay
    language_step language_cowsay "$HOME/.local/node_modules/.bin/cowsay" cal-test
}
wait_supervisor() {
    # runsvdir scans for new services at least every five seconds.
    # https://man.voidlinux.org/runsvdir.8
    # sv fails immediately if no supervisor owns the service yet.
    # https://man.voidlinux.org/sv.8
    local attempt
    for attempt in {1..30}; do
        root test -p "$1/supervise/ok" && return 0
        sleep 1
    done
    return 124
}
user_service() {
    # https://man.openbsd.org/ssh-agent
    # https://docs.voidlinux.org/config/services/user-services.html
    # https://docs.voidlinux.org/config/services/index.html
    native_install ssh
    mkdir -p "$HOME/service/cal-user" "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    cat > "$HOME/service/cal-user/run" <<'RUN'
#!/bin/sh
exec ssh-agent -D -a "$HOME/.ssh/cal-agent.sock"
RUN
    chmod 755 "$HOME/service/cal-user/run"
    local config
    config=$(mktemp)
    cat > "$config" <<'RUN'
#!/bin/sh
export USER=user
export HOME=$(getent passwd "$USER" | cut -d: -f6)
groups=$(id -Gn "$USER" | tr ' ' ':')
exec chpst -u "$USER:$groups" runsvdir "$HOME/service"
RUN
    install_root_file "$config" /etc/sv/runsvdir-user/run 755
    rm "$config"
    root ln -s /etc/sv/runsvdir-user /var/service/runsvdir-user
    wait_supervisor /var/service/runsvdir-user
    root sv -w 30 up /var/service/runsvdir-user
    wait_supervisor "$HOME/service/cal-user"
    sv -w 30 up "$HOME/service/cal-user"
}
start_network_manager() {
    # Void explicitly requires disabling competing network services first.
    # https://docs.voidlinux.org/config/network/networkmanager.html
    # The clean guest primary NIC uses DHCP; NetworkManager adopts it.
    local service
    for service in dhcpcd wpa_supplicant wicd; do
        if [[ -L /var/service/$service ]]; then
            root sv -w 30 down "/var/service/$service"
            root rm "/var/service/$service"
        fi
    done
    for service in dbus NetworkManager; do
        if [[ ! -e /var/service/$service ]]; then
            root ln -s "/etc/sv/$service" "/var/service/$service"
        fi
        wait_supervisor "/var/service/$service"
        root sv -w 30 up "/var/service/$service"
    done
}
container_run() {
    # https://raw.githubusercontent.com/void-linux/void-packages/master/srcpkgs/docker-cli/template
    # https://docs.docker.com/reference/cli/docker/container/run/
    # https://docs.voidlinux.org/config/services/index.html
    native_install container
    if [[ ! -e /var/service/docker ]]; then root ln -s /etc/sv/docker /var/service/docker; fi
    wait_supervisor /var/service/docker
    root sv -w 60 up /var/service/docker
    # The daemon process can start before its API is ready.
    # https://docs.docker.com/reference/cli/docker/info/
    local attempt ready=0
    for attempt in {1..60}; do
        if root docker info >/dev/null 2>&1; then ready=1; break; fi
        sleep 1
    done
    (( ready == 1 ))
    root docker run --name cal-container docker.io/library/busybox:1.37.0 /bin/echo ordinary-container
}
actions_main "$@"
