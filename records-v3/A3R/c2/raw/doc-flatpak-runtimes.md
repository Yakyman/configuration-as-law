# Runtimes required by the installed Flatpak applications

| App (installed version) | runtime / runtime-version | Manifest read | Quoted lines |
|---|---|---|---|
| com.github.tchx84.Flatseal 2.4.1 | org.gnome.Platform / 50 | https://raw.githubusercontent.com/flathub/com.github.tchx84.Flatseal/master/com.github.tchx84.Flatseal.json | "runtime": "org.gnome.Platform", "runtime-version": "50"; source "tag": "v2.4.1" |
| io.github.flattool.Warehouse 2.2.0 | org.gnome.Platform / 49 | https://raw.githubusercontent.com/flathub/io.github.flattool.Warehouse/master/io.github.flattool.Warehouse.json | "runtime": "org.gnome.Platform", "runtime-version": "49"; source "tag": "2.2.0" |

Flatpak documentation, https://docs.flatpak.org/en/latest/basic-concepts.html (Runtimes): "this runtime must be installed on the host system for the application to run."
Installed refs: raw/lived/raw/009-packages-root-flatpak.out (inventory).
