#!/usr/bin/env bash
# Fedora Workstation disposable guest; invoke as user, never on the host.
set -euo pipefail
source "$(dirname "$(readlink -f "$0")")/lib.sh"

developer_prerequisites() {
    # https://dnf5.readthedocs.io/en/latest/commands/install.8.html
    # https://dnf5.readthedocs.io/en/latest/misc/specs.7.html (file provides)
    # https://docs.brew.sh/Homebrew-on-Linux
    root dnf -y install /usr/bin/curl unzip git gcc gcc-c++ make glibc-devel ruby rubygems python3 golang micro openssh-clients procps-ng file dnf5-plugins
    mkdir -p "$HOME/Projects" "$HOME/.local/bin" "$HOME/.local/state/cal-developer"
    # Record original startup files before the installers change them.
    for startup in .bashrc .bash_profile .profile; do
        if [[ -f "$HOME/$startup" ]]; then
            cp "$HOME/$startup" "$HOME/.local/state/cal-developer/before-$startup"
        fi
    done
}

developer_julia() {
    # https://docs.julialang.org/en/v1/manual/installation/
    # https://github.com/JuliaLang/juliaup#command-line-arguments
    curl -fsSL https://install.julialang.org | sh -s -- --yes
    "$HOME/.juliaup/bin/julia" -e 'println(VERSION)'
}

developer_bun() {
    # https://bun.sh/docs/installation
    export SHELL=/bin/bash
    curl -fsSL https://bun.com/install | bash
    "$HOME/.bun/bin/bun" --version
}

developer_version_manager() {
    # https://github.com/JuliaLang/juliaup#using-juliaup
    "$HOME/.juliaup/bin/juliaup" add lts
    "$HOME/.juliaup/bin/juliaup" default release
    "$HOME/.juliaup/bin/julia" +lts -e 'println(VERSION)'
}

developer_global_tools() {
    # Three language package managers: RubyGems (Ruby), Bun (JavaScript), uv (Python).
    # https://guides.rubygems.org/command-reference/#gem-install
    # https://github.com/evilmartians/lefthook#install
    gem install --user-install --no-document lefthook
    # https://bun.com/docs/pm/cli/add#global
    "$HOME/.bun/bin/bun" add --global eslint
    # https://docs.astral.sh/uv/getting-started/installation/
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # https://docs.astral.sh/uv/guides/tools/#installing-tools
    "$HOME/.local/bin/uv" tool install ruff
}

developer_editor_plugins() {
    # https://github.com/10sr/editorconfig-micro#installation
    # https://github.com/micro-editor/micro/discussions/2635
    # https://raw.githubusercontent.com/micro-editor/plugin-channel/master/channel.json
    micro -plugin install editorconfig
    micro -plugin install filemanager
    # Micro can report errors without nonzero exit: require both plugin directories.
    test -d "${XDG_CONFIG_HOME:-$HOME/.config}/micro/plug/editorconfig"
    test -d "${XDG_CONFIG_HOME:-$HOME/.config}/micro/plug/filemanager"
}

developer_public_project() {
    # https://git-scm.com/docs/git-clone
    git clone --depth 1 https://github.com/boyter/scc.git "$HOME/Projects/scc"
    cd "$HOME/Projects/scc"
    # https://go.dev/ref/mod#go-mod-download
    # Project go.mod/go.sum select dependencies, installed in this project's cache.
    # https://go.dev/ref/mod#module-cache (GOMODCACHE)
    export GOMODCACHE="$HOME/Projects/scc/.cal-modcache"
    go mod download
    # https://github.com/boyter/scc#containers (upstream source-build recipe)
    # https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies (-p)
    # https://pkg.go.dev/runtime (GOMAXPROCS)
    GOMAXPROCS=2 go build -p 2 -ldflags='-s -w' -o scc .
    ./scc --version
    # https://git-scm.com/docs/git-rev-parse
    git rev-parse HEAD > "$HOME/.local/state/cal-developer/scc-commit.txt"
}

developer_git_hooks() {
    cd "$HOME/Projects/scc"
    # https://lefthook.dev/ ; https://guides.rubygems.org/faqs/#user-install
    local gem_bin
    gem_bin=$(ruby -r rubygems -e 'puts Gem.user_dir')
    export PATH="$gem_bin/bin:$PATH"
    # https://git-scm.com/docs/git-diff (--cached --check)
    cat > lefthook.yml <<'EOF'
pre-commit:
  jobs:
    - name: whitespace
      run: git diff --cached --check
EOF
    lefthook install
}

developer_container() {
    # https://docs.docker.com/engine/install/fedora/
    root dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo
    root dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    root systemctl enable --now docker
    mkdir -p "$HOME/Projects/development-web"
    cd "$HOME/Projects/development-web"
    printf '%s\n' 'Development preview' > index.html
    # https://docs.docker.com/reference/dockerfile/
    # https://hub.docker.com/_/busybox ; https://busybox.net/downloads/BusyBox.html#httpd
    cat > Dockerfile <<'EOF'
FROM docker.io/library/busybox:stable
WORKDIR /www
COPY index.html /www/index.html
EXPOSE 8080
CMD ["httpd", "-f", "-p", "8080", "-h", "/www"]
EOF
    # https://docs.docker.com/reference/cli/docker/buildx/build/
    root docker build --tag cal-development-web:local .
    # https://docs.docker.com/reference/cli/docker/container/run/
    root docker run --detach --name cal-development-web --restart unless-stopped \
        --publish 127.0.0.1:18080:8080 cal-development-web:local
}

developer_second_package_manager() {
    local installer cleanup
    # Preprovision the documented Linux prefix for noninteractive, unprivileged install.
    # https://docs.brew.sh/Installation#running-without-sudo
    root install -d -m 0755 -o user -g "$(id -gn)" /home/linuxbrew/.linuxbrew
    # https://docs.brew.sh/Installation#unattended-installation
    # curl(1) exit 56 is a receive failure. Retry this read-only download with
    # bounds; --output lets curl discard partial bytes before retrying.
    # https://curl.se/docs/manpage.html#--retry-all-errors
    installer=$(mktemp)
    printf -v cleanup 'rm -f -- %q' "$installer"
    trap "$cleanup" EXIT
    curl -fsSL --retry 3 --retry-all-errors --retry-max-time 120 \
        --connect-timeout 30 --max-time 120 --output "$installer" \
        https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
    NONINTERACTIVE=1 /bin/bash "$installer"
    rm -f -- "$installer"
    trap - EXIT
    # https://docs.brew.sh/Homebrew-on-Linux
    # shellcheck disable=SC2016 # Expand on later shell startup, not while writing.
    printf '%s\n' 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> "$HOME/.bashrc"
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    brew install hello
}

developer_user_service_timer() {
    # https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
    # https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
    mkdir -p "$HOME/.config/systemd/user" "$HOME/.local/share/cal-developer"
    cat > "$HOME/.local/bin/cal-project-summary" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
"$HOME/Projects/scc/scc" "$HOME/Projects/scc" > "$HOME/.local/share/cal-developer/project-summary.txt"
EOF
    chmod 0755 "$HOME/.local/bin/cal-project-summary"
    cat > "$HOME/.config/systemd/user/cal-project-summary.service" <<'EOF'
[Unit]
Description=Generate a development project summary
[Service]
Type=oneshot
ExecStart=%h/.local/bin/cal-project-summary
TimeoutStartSec=60
[Install]
WantedBy=default.target
EOF
    cat > "$HOME/.config/systemd/user/cal-project-summary.timer" <<'EOF'
[Unit]
Description=Refresh the project summary daily
[Timer]
OnCalendar=daily
Persistent=true
[Install]
WantedBy=timers.target
EOF
    # https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
    systemctl --user daemon-reload
    systemctl --user enable --now cal-project-summary.service cal-project-summary.timer
}

developer_shell_startup() {
    # Preserve real installer changes, rather than inventing replacement dotfiles.
    # https://github.com/JuliaLang/juliaup#command-line-arguments
    # https://bun.sh/docs/installation
    # https://docs.astral.sh/uv/reference/installer/
    # https://docs.brew.sh/Homebrew-on-Linux
    # https://guides.rubygems.org/faqs/#user-install
    # shellcheck disable=SC2016 # Preserve the literal startup command.
    printf '%s\n' 'export PATH="$(ruby -r rubygems -e '\''puts Gem.user_dir'\'')/bin:$PATH"' >> "$HOME/.bashrc"
    for startup in .bashrc .bash_profile .profile; do
        if [[ -f "$HOME/$startup" ]]; then
            cp "$HOME/$startup" "$HOME/.local/state/cal-developer/after-$startup"
        fi
    done
}

developer_ssh() {
    # https://man.openbsd.org/ssh-keygen ; https://man.openbsd.org/ssh_config
    umask 077
    mkdir -p "$HOME/.ssh"
    ssh-keygen -q -t ed25519 -N '' -C 'development' -f "$HOME/.ssh/id_ed25519_development"
    cat >> "$HOME/.ssh/config" <<'EOF'

Host development
    HostName 192.0.2.10
    User developer
    IdentityFile ~/.ssh/id_ed25519_development
    IdentitiesOnly yes
    ServerAliveInterval 30
EOF
    chmod 0600 "$HOME/.ssh/config"
}

actions() {
    cat <<'EOF'
developer_prerequisites 1200
developer_julia 1200
developer_bun 600
developer_version_manager 1200
developer_global_tools 1200
developer_editor_plugins 600
developer_public_project 1200
developer_git_hooks 120
developer_container 1200
developer_second_package_manager 1800
developer_user_service_timer 180
developer_shell_startup 60
developer_ssh 60
EOF
}
actions_main "$@"
