#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$(readlink -f "$0")")/lib.sh"

# SSH action transport attaches to the existing desktop session.
# https://www.x.org/releases/current/doc/man/man7/X.7.xhtml
# https://dbus.freedesktop.org/doc/dbus-specification.html#transports-unix-domain-sockets
export DISPLAY=${DISPLAY:-:0}
export XAUTHORITY=${XAUTHORITY:-$HOME/.Xauthority}
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/run/user/$(id -u)}
export DBUS_SESSION_BUS_ADDRESS=${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}
export PYTHONPATH="$(dirname "$(readlink -f "$0")")${PYTHONPATH:+:$PYTHONPATH}"

# Base: clean Linux Mint 22.3 Cinnamon; execute in user user's graphical session.
# Each function is executed separately by lib.sh under its advertised time limit.
# Infrastructure commands: https://manpages.debian.org/bookworm/apt/apt-get.8.en.html
# https://manpages.debian.org/bookworm/dpkg/dpkg.1.en.html
# https://curl.se/docs/manpage.html
# https://docs.python.org/3/library/subprocess.html

# Bound connection and idle-data waits; keep repositories and packages unchanged.
# https://manpages.debian.org/trixie/apt/apt-transport-http.1.en.html
# https://manpages.debian.org/trixie/apt/apt.conf.5.en.html
gaming_apt_get() {
    root env DEBIAN_FRONTEND=noninteractive apt-get \
        -o Acquire::http::Timeout=30 -o Acquire::https::Timeout=30 \
        -o Acquire::Retries=2 "$@"
}

gaming_prerequisites() {
    set -euo pipefail
    : "${DISPLAY:?Run in the existing Cinnamon X11 session}"
    : "${DBUS_SESSION_BUS_ADDRESS:?Run with the user session bus}"
    printf "%s\n" "prerequisites: adding i386 architecture" >&2
    root dpkg --add-architecture i386
    printf "%s\n" "prerequisites: updating repository indexes" >&2
    gaming_apt_get update
    printf "%s\n" "prerequisites: installing packages" >&2
    gaming_apt_get install -y \
        curl ca-certificates python3 python3-gi gir1.2-atspi-2.0 at-spi2-core xvfb xauth dbus-daemon \
        flatpak lutris wine wine32:i386 wine64 libgl1-mesa-dri:i386 \
        libgl1:i386 libc6:i386 libstdc++6:i386 pulseaudio-utils mangohud
    mkdir -p "$HOME/Games" "$HOME/.local/share/cal-gaming"
}

gaming_store_runtime() {
    set -euo pipefail
    # Repository client, not the upstream .deb:
    # https://packages.ubuntu.com/noble/steam-installer
    # Runtime path: https://github.com/ValveSoftware/steam-runtime/blob/master/README.md
    # Client launch: https://github.com/ValveSoftware/steam-for-linux
    # Noble source: debian/scripts/steam.in has a first-run Zenity Install prompt.
    # debian/steam-installer.templates has no license acceptance debconf question.
    # https://archive.ubuntu.com/ubuntu/pool/universe/s/steam-installer/steam-installer_1.0.0.79~ds-2.debian.tar.xz
    printf "%s\n" "store runtime: installing distribution client" >&2
    gaming_apt_get install -y steam-installer
    gsettings set org.cinnamon.desktop.interface toolkit-accessibility true
    # A private virtual display and bus provide unattended GUI transport.
    # https://manpages.debian.org/bookworm/xvfb/xvfb-run.1.en.html
    # https://dbus.freedesktop.org/doc/dbus-run-session.1.html
    xvfb-run -a dbus-run-session -- python3 - <<'PY'
import os, pathlib, signal, subprocess, time
import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi, GLib
from gui_guard import start as start_gui, stop as stop_gui
home = pathlib.Path.home()
env = dict(os.environ, LC_ALL='C', GTK_MODULES='gail:atk-bridge', NO_AT_BRIDGE='0')
proc = start_gui(['steam'], env=env)
def own_group(pid):
    try:
        return os.getpgid(pid) == proc.pid
    except ProcessLookupError:
        return False
def nodes(obj, depth=0):
    if depth > 24:
        return
    yield obj
    for index in range(obj.get_child_count()):
        child = obj.get_child_at_index(index)
        if child is not None:
            yield from nodes(child, depth + 1)
def confirm_bootstrap():
    # This is the distribution wrapper's own Install dialog, not arbitrary prompts.
    desktop = Atspi.get_desktop(0)
    for i in range(desktop.get_child_count()):
        app = desktop.get_child_at_index(i)
        try:
            if not own_group(app.get_process_id()):
                continue
            for window in nodes(app):
                if window.get_name() != 'Steam installer':
                    continue
                for node in nodes(window):
                    state = node.get_state_set()
                    if (node.get_role() == Atspi.Role.PUSH_BUTTON
                        and node.get_name().replace('_', '') == 'Install'
                        and state.contains(Atspi.StateType.SHOWING)
                        and state.contains(Atspi.StateType.SENSITIVE)):
                        action = node.get_action_iface()
                        if action and action.get_n_actions() and action.do_action(0):
                            return
        except GLib.Error:
            pass
def steam_running(root):
    executable = (root / 'ubuntu12_32/steam').resolve()
    for entry in pathlib.Path('/proc').iterdir():
        if not entry.name.isdecimal() or not own_group(int(entry.name)):
            continue
        try:
            if (entry / 'exe').resolve(strict=True) == executable:
                return True
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            pass
    return False
def stop(*_):
    raise SystemExit(143)
signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
try:
    deadline = time.monotonic() + 1000
    while time.monotonic() < deadline:
        root = home / '.steam/root'
        runtime = root / 'ubuntu12_32/steam-runtime/run.sh'
        client = root / 'ubuntu12_32/steamclient.so'
        confirm_bootstrap()
        marker = root / 'deb-installer/version'
        if (runtime.is_file() and os.access(runtime, os.X_OK) and client.is_file()
            and marker.is_file() and steam_running(root)):
            # Both are downloaded/extracted by the client; no login is required.
            print('Steam client and scout runtime present after first launch', flush=True)
            break
        if proc.poll() is not None:
            raise SystemExit(81)  # Supervised client group exited before completion.
        time.sleep(1)
    else:
        raise SystemExit(82)  # Client/runtime completion deadline.
except AttributeError:
    raise SystemExit(83)  # Unsupported accessibility interface.
except GLib.Error:
    raise SystemExit(84)  # Accessibility bus failure.
finally:
    stop_gui(proc)
PY
}

gaming_anonymous_download() {
    set -euo pipefail
    # Distribution-maintained Steam package manifest publishes this bootstrap URL:
    # https://github.com/flathub/com.valvesoftware.Steam/blob/beta/com.valvesoftware.Steam.yml
    # Exact anonymous application commands and ID:
    # https://docs.smartlydressedgames.com/en/stable/servers/steamcmd.html
    local dir="$HOME/.local/share/steamcmd"
    mkdir -p "$dir"
    curl -fL --connect-timeout 30 --max-time 180 -o "$dir/bootstrap.tar.gz" \
        https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
    tar -xzf "$dir/bootstrap.tar.gz" -C "$dir"
    rm "$dir/bootstrap.tar.gz"
    cd "$dir"
    # Explicit destination avoids relocation by the updated client.
    # https://github.com/ValveSoftware/steam-for-linux/issues/8298
    ./steamcmd.sh +force_install_dir "$HOME/Games/U3DS" +login anonymous +app_update 1110390 validate +quit
    test -f "$HOME/Games/U3DS/ServerHelper.sh" || return 87
}

gaming_flatpak_game() {
    set -euo pipefail
    # https://docs.flatpak.org/en/latest/flatpak-command-reference.html
    # https://flathub.org/apps/org.gnome.Chess
    flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    flatpak install --user --noninteractive -y flathub org.gnome.Chess
    flatpak info --user org.gnome.Chess
}

gaming_launcher_tool() {
    set -euo pipefail
    # Lutris has no --unattended flag. Drive its real installer buttons with AT-SPI.
    # https://github.com/lutris/lutris/blob/v0.5.17/docs/installers.rst
    # https://github.com/lutris/lutris/blob/v0.5.17/lutris/gui/installerwindow.py
    # https://gnome.pages.gitlab.gnome.org/at-spi2-core/libatspi/method.Action.do_action.html
    # https://gnome.pages.gitlab.gnome.org/at-spi2-core/libatspi/method.Accessible.get_action_iface.html
    # Archive URL: https://7-zip.org/download.html (23.01 Linux x86-64).
    # Enable toolkit access through Cinnamon's own setting:
    # https://github.com/linuxmint/cinnamon-desktop/blob/master/schemas/org.cinnamon.desktop.interface.gschema.xml.in
    # https://help.gnome.org/system-admin-guide/gsettings-browse.html
    gsettings set org.cinnamon.desktop.interface toolkit-accessibility true
    cat > "$HOME/.local/share/cal-gaming/7zip.yml" <<'YAML'
name: 7-Zip archive tool
game_slug: cal-7zip-tool
version: Linux 23.01
slug: cal-7zip-tool-linux
runner: linux
script:
  files:
    - archive: https://7-zip.org/a/7z2301-linux-x64.tar.xz
  game:
    exe: $GAMEDIR/7zz
    args: i
  installer:
    - extract:
        file: archive
        dst: $GAMEDIR
YAML
    # A private virtual display and bus provide unattended GUI transport.
    # https://manpages.debian.org/bookworm/xvfb/xvfb-run.1.en.html
    # https://dbus.freedesktop.org/doc/dbus-run-session.1.html
    xvfb-run -a dbus-run-session -- python3 - <<'PY'
import os, pathlib, signal, sqlite3, subprocess, time
import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi, GLib
from gui_guard import start as start_gui, stop as stop_gui
home = pathlib.Path.home()
# Own-process GUI only. YAML is consumed by Lutris, never interpreted here.
env = dict(os.environ, LC_ALL='C', GTK_MODULES='gail:atk-bridge', NO_AT_BRIDGE='0')
proc = start_gui(['lutris', '--install', str(home / '.local/share/cal-gaming/7zip.yml')], env=env)
def stop(*_):
    raise SystemExit(143)
signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
def nodes(obj, depth=0):
    if depth > 24:
        return
    yield obj
    for index in range(obj.get_child_count()):
        child = obj.get_child_at_index(index)
        if child is not None:
            yield from nodes(child, depth + 1)
def installed():
    # Read-only confirmation, not direct installation or database modification.
    # https://github.com/lutris/lutris/blob/v0.5.17/lutris/database/games.py
    database = home / '.local/share/lutris/pga.db'
    if not database.is_file():
        return False
    try:
        with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True, timeout=1) as db:
            row = db.execute('SELECT directory FROM games WHERE slug=? AND installed=1', ('cal-7zip-tool',)).fetchone()
        return bool(row and (pathlib.Path(row[0]) / '7zz').is_file())
    except sqlite3.OperationalError:
        return False
try:
    deadline = time.monotonic() + 600
    while time.monotonic() < deadline:
        if installed():
            print('Lutris registered the installed tool and its executable exists', flush=True)
            break
        if proc.poll() is not None:
            raise SystemExit(85)  # Launcher exited before verified installation.
        desktop = Atspi.get_desktop(0)
        clicked = False
        for i in range(desktop.get_child_count()):
            app = desktop.get_child_at_index(i)
            try:
                if os.getpgid(app.get_process_id()) != proc.pid:
                    continue
            except ProcessLookupError:
                continue
            try:
                for node in nodes(app):
                    state = node.get_state_set()
                    if (node.get_role() == Atspi.Role.PUSH_BUTTON
                        and node.get_name().replace('_', '') in ('Install', 'Continue')
                        and state.contains(Atspi.StateType.SHOWING)
                        and state.contains(Atspi.StateType.SENSITIVE)):
                        interface = node.get_action_iface()
                        if interface and interface.get_n_actions() > 0:
                            if not interface.do_action(0):
                                raise RuntimeError('Installer button action rejected')
                            clicked = True
                            break
            except GLib.Error:
                # The installer replaces its pages; inspect the next live page.
                pass
            if clicked:
                break
        time.sleep(1)
    else:
        raise SystemExit(86)  # Installer completion deadline.
except AttributeError:
    raise SystemExit(83)  # Unsupported accessibility interface.
except GLib.Error:
    raise SystemExit(84)  # Accessibility bus failure.
finally:
    stop_gui(proc)
PY
}

gaming_windows_program() {
    set -euo pipefail
    # https://7-zip.org/download.html identifies the official Windows console binary.
    # https://manpages.debian.org/bookworm/wine/wine.1.en.html (wine, WINEPREFIX)
    # https://manpages.debian.org/bookworm/wine/wineserver.1.en.html (-w/-k)
    local exe="$HOME/.local/share/cal-gaming/7zr.exe"
    curl -fL --connect-timeout 30 --max-time 180 -o "$exe" \
        https://github.com/ip7z/7zip/releases/download/26.06/7zr.exe
    export WINEPREFIX="$HOME/Games/wine-tools"
    export WINEDLLOVERRIDES="mscoree,mshtml="
    trap 'wineserver -k || true' EXIT
    # The console-only binary needs no .NET, browser engine, or installer dialog.
    # i: https://github.com/ip7z/7zip/blob/main/CPP/7zip/UI/Console/Main.cpp
    wine "$exe" i
    wineserver -w
    test -s "$WINEPREFIX/user.reg"
    test -d "$WINEPREFIX/drive_c"
}

gaming_overlay() {
    set -euo pipefail
    # https://github.com/flightlessmango/MangoHud#hud-configuration
    mkdir -p "$HOME/.config/MangoHud"
    cat > "$HOME/.config/MangoHud/MangoHud.conf" <<'CONF'
fps
frame_timing
position=top-left
CONF
    # Older distribution wrappers execute their argument and have no --version option.
    # https://github.com/flightlessmango/MangoHud/blob/v0.6.9/bin/mangohud.in
    mangohud /usr/bin/true
}

gaming_user_settings() {
    set -euo pipefail
    # https://help.gnome.org/system-admin-guide/gsettings-browse.html
    # https://github.com/linuxmint/cinnamon-desktop/blob/master/schemas/org.cinnamon.desktop.interface.gschema.xml.in
    # Graphics preference: turn off desktop animations and enlarge UI text.
    gsettings set org.cinnamon.desktop.interface enable-animations false
    gsettings set org.cinnamon.desktop.interface text-scaling-factor 1.15
    # PulseAudio protocol is provided by the Mint session's PipeWire service.
    # https://manpages.debian.org/bookworm/pulseaudio-utils/pactl.1.en.html
    pactl set-sink-volume @DEFAULT_SINK@ 35%
    pactl set-sink-mute @DEFAULT_SINK@ 0
    gsettings get org.cinnamon.desktop.interface enable-animations
    gsettings get org.cinnamon.desktop.interface text-scaling-factor
    pactl get-sink-volume @DEFAULT_SINK@
}

gaming_autostart() {
    set -euo pipefail
    # https://specifications.freedesktop.org/autostart-spec/latest/
    # https://specifications.freedesktop.org/desktop-entry-spec/latest/
    mkdir -p "$HOME/.config/autostart"
    cat > "$HOME/.config/autostart/lutris.desktop" <<'DESKTOP'
[Desktop Entry]
Type=Application
Name=Lutris
Exec=lutris
TryExec=lutris
Terminal=false
DESKTOP
}

actions() {
    cat <<'ACTIONS'
gaming_prerequisites 1800
gaming_store_runtime 1800
gaming_anonymous_download 2400
gaming_flatpak_game 1800
gaming_launcher_tool 660
gaming_windows_program 480
gaming_overlay 30
gaming_user_settings 30
gaming_autostart 30
ACTIONS
}
actions_main "$@"
