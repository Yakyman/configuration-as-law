# Ordinary actions

The exact script is `C1/actions/fedora.sh`; run as ordinary user on a throwaway clone, then destroy that clone. The package-manager program is GNU `hello`. `podman` and `flatpak` are installed through the same distribution package manager when needed by these ordinary actions, never added to the clean backing image. The application is GNOME Calculator (`org.gnome.Calculator`) from Flathub. One Alpine Linux container (`docker.io/library/alpine:3.22`) prints a constant and exits; its name is `cal-container`.

NetworkManager saves a connection bound to the lab's second virtual NIC by MAC and brings it up using DHCP, without changing the default route. It also saves the `cal-test` Wi-Fi profile without activation, since no radio exists. The home script appends a constant greeting, executes once, and is scheduled as a user timer.

References: https://docs.flatpak.org/en/latest/using-flatpak.html ; https://docs.flatpak.org/en/latest/flatpak-command-reference.html ; https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nmcli.html ; https://docs.podman.io/en/latest/markdown/podman-run.1.html ; https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html .

Test status is recorded in `C1/status-fedora-opensuse.md`. This document makes no success claim in advance.
