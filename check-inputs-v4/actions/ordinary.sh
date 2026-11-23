#!/usr/bin/env bash
# Exact shared implementations of check 1 actions; not an entry point.

package_program() {
    # Fixed without inspecting any guest: tree, even if already present.
    native_install tree
}

application_package() {
    # Installing Flatpak is part of this action on every system lacking it.
    # https://docs.flatpak.org/en/latest/using-flatpak.html
    # https://docs.flatpak.org/en/latest/flatpak-command-reference.html
    native_install flatpak
    flatpak --user remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
    flatpak --user install --noninteractive -y flathub org.gnome.Calculator
}

language_program() {
    # https://docs.npmjs.com/cli/v11/commands/npm-install/
    native_install node
    npm install --global --prefix "$HOME/.local" cowsay
    "$HOME/.local/bin/cowsay" cal-test
}

browser_extension() {
    # The distribution Firefox and Python/pip are installed here if absent.
    # https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-t
    # https://firefox-source-docs.mozilla.org/python/marionette_driver.html
    # https://wiki.mozilla.org/Firefox/CommandLineOptions
    native_install browser
    python3 -m pip install --no-input --target "$HOME/.local/lib/cal-marionette" marionette_driver
    mkdir -p "$HOME/.mozilla/firefox/cal-check" "$HOME/Downloads"
    firefox --headless -CreateProfile "cal-check $HOME/.mozilla/firefox/cal-check"
    PYTHONPATH="$HOME/.local/lib/cal-marionette" python3 "$ACTIONS_DIR/firefox-addon.py"
}

personal_setting() {
    # Git's own command, not direct editing of its configuration.
    # https://git-scm.com/docs/git-config
    native_install git
    git config --global color.ui false
}

network_connection() {
    # https://networkmanager.dev/docs/api/latest/nmcli.html
    # https://networkmanager.dev/docs/api/latest/nm-settings-nmcli.html
    native_install network
    start_network_manager
    root nmcli connection add type ethernet con-name cal-secondary ifname '*' \
        802-3-ethernet.mac-address 52:54:00:ca:10:02 \
        ipv4.method auto ipv4.never-default yes ipv6.method disabled
    root nmcli --wait 90 connection up cal-secondary
    root nmcli connection add type wifi con-name cal-test ifname '*' ssid cal-test \
        connection.autoconnect no ipv4.method auto ipv6.method disabled \
        wifi-sec.key-mgmt wpa-psk wifi-sec.psk cal-test-passphrase
    # The Wi-Fi profile is saved, never activated: there is no radio.
}

home_script() {
    mkdir -p "$HOME/.local/bin"
    cat > "$HOME/.local/bin/cal-user-script" <<'SCRIPT'
#!/bin/sh
printf '%s\n' 'ordinary-action' >> "$HOME/cal-user-script.log"
SCRIPT
    chmod 755 "$HOME/.local/bin/cal-user-script"
    "$HOME/.local/bin/cal-user-script"
}

actions() {
    # Gentoo compiles distribution packages; all limits are wall-clock seconds.
    printf '%s\n' \
        "package_program $PACKAGE_LIMIT" \
        "application_package $PACKAGE_LIMIT" \
        "language_program $PACKAGE_LIMIT" \
        "browser_extension $BROWSER_LIMIT" \
        "personal_setting $PACKAGE_LIMIT" \
        "user_service $PACKAGE_LIMIT" \
        "network_connection $PACKAGE_LIMIT" \
        'home_script 30' \
        "container_run $PACKAGE_LIMIT"
}
