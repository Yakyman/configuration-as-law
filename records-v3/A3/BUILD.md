# Lived-in machine build

Operator build on 2026-11-22 UTC. One Debian 13 VM, 8 GiB RAM, 4 vCPU, two shared slot locks. The stopped disk snapshot `before-lived-build` precedes installation. The retained disk is `A3/C1/vms/a3-lived/disk.qcow2` relative to the server laboratory root. Resource evidence: (not published: outside selected checks and direct evidence).

The VM was created with `lab.sh new a3-lived debian` in the task-local laboratory root. The controller and collector are byte-identical to the supplied files ((not published: outside selected checks and direct evidence)). The source Debian backing image remains read-only. Installations use documented project methods; each installer is bounded by 1,200 seconds. The installation sources and short supporting passages are in (not published: outside selected checks and direct evidence), (not published: outside selected checks and direct evidence), and (not published: outside selected checks and direct evidence); commands and repairs are in `scripts/`.

## Installed material

Every listed version/commit is from saved guest output. Native dependency versions are fully listed in (not published: outside selected checks and direct evidence); their package downloads appear in apt logs. Python dependencies and editable Flask requirements are in (not published: outside selected checks and direct evidence); Neovim plugin commits are in (not published: outside selected checks and direct evidence); Emacs package versions appear in (not published: outside selected checks and direct evidence) and the recorded ELPA file names. The five selected IDE extensions each have tens of millions of installations ((not published: outside selected checks and direct evidence)); their automatically installed dependencies are also retained. Public project popularity is saved in (not published: outside selected checks and direct evidence).

| Item | Source URL | Installed version / commit | Evidence |
|---|---|---|---|
| XFCE | https://packages.debian.org/trixie/xfce4 | 4.20.1 | (not published: supporting build record) |
| LightDM | https://packages.debian.org/trixie/lightdm | 1.32.0-6+deb13u1 | (not published: supporting build record) |
| Zsh | https://packages.debian.org/trixie/zsh | 5.9-8+b25 | (not published: supporting build record) |
| direnv | https://packages.debian.org/trixie/direnv | 2.32.1-2+b16 | (not published: supporting build record) |
| Emacs | https://packages.debian.org/trixie/emacs-gtk | 1:30.1+1-6+deb13u1 | (not published: supporting build record) |
| Python | https://packages.debian.org/trixie/python3 | 3.13.5-1 | (not published: supporting build record) |
| pipx | https://packages.debian.org/trixie/pipx | 1.7.1-1 | (not published: supporting build record) |
| Git | https://packages.debian.org/trixie/git | 1:2.47.3-0+deb13u1 | (not published: supporting build record) |
| Make | https://packages.debian.org/trixie/make | 4.4.1-2 | (not published: supporting build record) |
| Podman | https://packages.debian.org/trixie/podman | 5.4.2+ds1-2+b2 | (not published: supporting build record) |
| Podman Compose | https://packages.debian.org/trixie/podman-compose | 1.3.0-1 | (not published: supporting build record) |
| Firefox ESR | https://packages.debian.org/trixie/firefox-esr | 153.7.0esr-1~deb13u1 | (not published: supporting build record) |
| KeePassXC | https://packages.debian.org/trixie/keepassxc | 2.7.10+dfsg1-1 | (not published: supporting build record) |
| LibreOffice | https://packages.debian.org/trixie/libreoffice | 4:25.2.3-2+deb13u12 | (not published: supporting build record) |
| CUPS PDF driver | https://packages.debian.org/trixie/printer-driver-cups-pdf | 3.0.2-3 | (not published: supporting build record) |
| NetworkManager | https://packages.debian.org/trixie/network-manager | 1.52.1-1 | (not published: supporting build record) |
| WireGuard tools | https://packages.debian.org/trixie/wireguard-tools | 1.0.20210914-3 | (not published: supporting build record) |
| GnuPG | https://packages.debian.org/trixie/gnupg | 2.4.7-21+deb13u1 | (not published: supporting build record) |
| pass | https://packages.debian.org/trixie/pass | 1.7.4-7 | (not published: supporting build record) |
| cron | https://packages.debian.org/trixie/cron | 3.0pl1-197 | (not published: supporting build record) |
| systemd | https://packages.debian.org/trixie/systemd | 257.13-1~deb13u1 | (not published: supporting build record) |
| nftables | https://packages.debian.org/trixie/nftables | 1.1.3-1 | (not published: supporting build record) |
| sudo | https://packages.debian.org/trixie/sudo | 1.9.16p2-3+deb13u5 | (not published: supporting build record) |
| polkit | https://packages.debian.org/trixie/polkitd | 126-2 | (not published: supporting build record) |
| OpenSSH client | https://packages.debian.org/trixie/openssh-client | 1:10.0p1-7+deb13u4 | (not published: supporting build record) |
| OpenSSL | https://packages.debian.org/trixie/openssl | 3.5.9-1~deb13u1 | (not published: supporting build record) |
| Desktop kernel metapackage | https://packages.debian.org/trixie/linux-image-amd64 | 6.12.117-1 | (not published: supporting build record) |
| Public dotfiles | https://github.com/mathiasbynens/dotfiles | b7c7894e7bb2de5d60bfb9a2f5e46d01a61300ea | (not published: supporting build record) |
| Oh My Zsh | https://github.com/ohmyzsh/ohmyzsh | c0140703a53eb0d22be44f7bac318d0baacc927c | (not published: supporting build record) |
| LazyVim starter | https://github.com/LazyVim/starter | 803bc181d7c0d6d5eeba9274d9be49b287294d99 | (not published: supporting build record) |
| LazyVim | https://github.com/LazyVim/LazyVim | 0fa4a847929fc6beae40a3063615a58115678c34 | (not published: supporting build record) |
| lazy.nvim | https://github.com/folke/lazy.nvim | 85c7ff3711b730b4030d03144f6db6375044ae82 | (not published: supporting build record) |
| Emacs Prelude / package.el | https://github.com/bbatsov/prelude | 11a42655b9cba88933660768fa83e2340524e407 | (not published: supporting build record) |
| nvm | https://github.com/nvm-sh/nvm | ea0fcdbe1658d13783f981a930d03106a82c5927 | (not published: supporting build record) |
| Flask | https://github.com/pallets/flask | 49943b5a94413a530761350f04e896f76e8d620e | (not published: supporting build record) |
| Express | https://github.com/expressjs/express | 43fca52d28a422c8be48fd489cbd4f2d6152bab6 | (not published: supporting build record) |
| zlib | https://github.com/madler/zlib | 617e19a81f38c15ff04de9f86882f42ad8a8ffd1 | (not published: supporting build record) |
| Compose project | https://github.com/docker/awesome-compose | 503c0dcef31b07fb77b2d4c5556bfafdf86f4f1a | (not published: supporting build record) |
| Neovim | https://github.com/neovim/neovim/releases/tag/v0.12.6 | 0.12.6 | (not published: supporting build record) |
| Visual Studio Code | https://code.visualstudio.com/docs/setup/linux | 1.147.0-1794903003 | (not published: supporting build record) |
| dbaeumer.vscode-eslint | https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint | 3.0.34 | (not published: supporting build record) |
| esbenp.prettier-vscode | https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode | 12.4.0 | (not published: supporting build record) |
| ms-python.debugpy | https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy | 2026.6.0 | (not published: supporting build record) |
| ms-python.python | https://marketplace.visualstudio.com/items?itemName=ms-python.python | 2026.10.0 | (not published: supporting build record) |
| ms-python.vscode-pylance | https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance | 2026.4.1 | (not published: supporting build record) |
| ms-python.vscode-python-envs | https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-python-envs | 1.44.0 | (not published: supporting build record) |
| ms-vscode.cpptools | https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools | 1.35.6 | (not published: supporting build record) |
| pipx: httpie | https://pypi.org/project/httpie/ | 3.2.4 | (not published: supporting build record) |
| pipx: pre-commit | https://pypi.org/project/pre-commit/ | 4.7.0 | (not published: supporting build record) |
| Node.js | https://nodejs.org/ | v26.13.1 | (not published: supporting build record) |
| npm global: npm | https://www.npmjs.com/package/npm | 11.20.0 | (not published: supporting build record) |
| npm global: prettier | https://www.npmjs.com/package/prettier | 3.10.1 | (not published: supporting build record) |
| npm global: typescript | https://www.npmjs.com/package/typescript | 7.0.2 | (not published: supporting build record) |
| rustup manager | https://rustup.rs/ | 1.29.3 (edbc831ce 2026-11-02) | (not published: supporting build record) |
| Rust via rustup | https://rust-lang.org/tools/install/ | rustc 1.100.0; stable-x86_64-unknown-linux-gnu | (not published: supporting build record); (not published: supporting build record) |
| hexyl via cargo install | https://github.com/sharkdp/hexyl | 0.17.0 | (not published: supporting build record) |
| hey via go install | https://github.com/rakyll/hey | 0.1.5 | (not published: supporting build record) |
| Jupyter IPython kernel | https://ipython.readthedocs.io/en/stable/install/kernel_install.html | ipykernel 7.4.0; kernel name flask-development | (not published: supporting build record); (not published: supporting build record) |
| Tree-sitter CLI via Mason | https://github.com/tree-sitter/tree-sitter | 0.27.2 | (not published: supporting build record) |
| com.github.tchx84.Flatseal | https://flathub.org/apps/com.github.tchx84.Flatseal | 2.4.1 | (not published: supporting build record) |
| io.github.flattool.Warehouse | https://flathub.org/apps/io.github.flattool.Warehouse | 2.2.0 | (not published: supporting build record) |
| Obsidian AppImage | https://github.com/obsidianmd/obsidian-releases/releases/download/v1.15.1/Obsidian-1.15.1.AppImage | v1.15.1 | (not published: supporting build record); (not published: supporting build record) |
| Zotero tarball | https://www.zotero.org/download/client/dl?channel=release&platform=linux-x86_64 | 10.0.8 | (not published: supporting build record); (not published: supporting build record) |
| Firefox: ublock-origin | https://addons.mozilla.org/firefox/addon/ublock-origin/ | 1.76.6 | (not published: supporting build record); (not published: supporting build record) |
| Firefox: bitwarden-password-manager | https://addons.mozilla.org/firefox/addon/bitwarden-password-manager/ | 2026.11.0 | (not published: supporting build record); (not published: supporting build record) |
| Firefox: keepassxc-browser | https://addons.mozilla.org/firefox/addon/keepassxc-browser/ | 1.10.4.1 | (not published: supporting build record); (not published: supporting build record) |
| Netdata static service | https://get.netdata.cloud/kickstart.sh | 2.13.0 | (not published: supporting build record) |
| CirrOS stored VM image | https://download.cirros-cloud.net/0.6.3/cirros-0.6.3-x86_64-disk.img | 0.6.3; SHA256 7d6355852aeb6dbcd191bcda7cd74f1536cfe5cbf8a10495a7283a8396e4b75b | (not published: supporting build record) |
| Public macro document | https://www.pitonyak.org/AndrewFontMacro.odt | SHA256 ece85e9dcb9a7e76bf64b74cf91bd57917dcd7c690b3eabdd98cae2708206443 | (not published: supporting build record); (not published: supporting build record) |
| Local CA entry | https://letsencrypt.org/certs/isrgrootx1.pem | ISRG Root X1; fingerprint in evidence | (not published: supporting build record) |
| Downloaded HTTP specification | https://www.rfc-editor.org/rfc/rfc9110.txt | RFC 9110 | (not published: supporting build record) |

## Containers

The initial images are `docker.io/library/nginx:stable-alpine` and `docker.io/library/redis:7-alpine`. The public `nginx-flask-mongo` project also pulls nginx, MongoDB and Python and builds its Flask backend. Exact image digests, including the built image, are retained in (not published: outside selected checks and direct evidence) and (not published: outside selected checks and direct evidence). The Compose source is the committed upstream repository listed above. `development-web` is running with restart policy `always`; the restart unit is enabled. The Compose project was built and started once; its other containers may be stopped after the verification reboot because upstream assigns no restart policy.

## Local configuration and use

- Shell: upstream dotfiles applied with its bootstrap script; Oh My Zsh initialized; direnv hook and an allowed Flask `.envrc`; Git aliases execute shell commands. Bash and Zsh were run, including an interactive shell session.
- Development: Flask venv has a frozen requirements file, editable package, Jupyter kernel and SQLite development state; pipx tools were run; Express dependencies, npm scripts and generated lockfile exist; Rust and Go tools were built and run. zlib's Makefile build and upstream `make test` succeeded. Emacs opened and edited a notes document; Neovim was launched with the starter configuration and completed its tree-sitter tool installation.
- Desktop/application state: XFCE/LightDM; two Flatpak applications; executable Obsidian AppImage; Zotero unpacked under the guest home with its supplied desktop launcher and copied autostart entry. All GUI applications were launched; first launches under Xvfb retain portal/graphics warnings in `raw/guest-build/use-*.log`. Firefox has three active requested extensions. KeePassXC native-host registration exists; no external account or browser-to-vault login is claimed.
- Office/content: LibreOffice opened the original public macro-bearing document and exported a PDF; its macros were not executed. Project notes, a work document, printed PDF, and downloaded RFC/CirrOS/Zotero files exist. Histories, logs, caches, package databases and application state are retained intentionally.
- Settings: hostname `lived-workstation`, timezone Europe/London, system locale en_GB.UTF-8, additional en_US.UTF-8 for upstream dotfiles, local CA entry, inotify sysctl drop-in, USB serial udev rule, sudoers and polkit rules, nftables rules, WireGuard profile and two saved Wi-Fi profiles, PDF printer, 512 MiB swap file, tmpfs fstab entry, and `printk.time=1` kernel parameter. The locally installed ISRG Root X1 is also already present in Debian's global trust set; the added local-administrator entry is recorded without claiming a newly trusted identity.
- Identity/scheduling: generated SSH key pair and authorized key, SSH ProxyCommand configuration, generated GPG signing/encryption keys, encrypted pass entry, user crontab, user cleanup service and timer, and running script-installed Netdata service. No host private key or user secret is copied into publication evidence.

(not published: outside selected checks and direct evidence) records final guest checks. Per-item installation status files retain diagnostic failures even when later repaired; (not published: outside selected checks and direct evidence) explains these corrections. No hypothesis classification or decision about object necessity is made.

## Skipped

- Firmware boot-order change: BIOS firmware does not expose EFI BootOrder. Evidence: (not published: outside selected checks and direct evidence) and (not published: outside selected checks and direct evidence).

## Inventory method

The exact documented Debian command is `C1/collect.sh --instrument-test a3-lived in/raw/lived`. This is the additional authorized lived-in inventory, not one of the published check machines. The collector's `--observe` guard is not bypassed. Its coverage limitations, failed queries and unresolved ownership remain explicit in (not published: outside selected checks and direct evidence) and `coverage.tsv`.

(not published: outside selected checks and direct evidence) is a mechanical projection of every collector object except native dpkg packages and positively dpkg-owned system services/timers/unit-file entries/modules. All user units, unresolved ownership, other package managers, processes, accounts, rules, ports, saved networks and stored/code objects are retained. Collector IDs, names, kinds and members are unchanged; `part=1`, `machine=lived`, and evidence paths are rooted at `raw/lived/`. The complete exclusion audit is (not published: outside selected checks and direct evidence); uncertain cases remain in (not published: outside selected checks and direct evidence).
