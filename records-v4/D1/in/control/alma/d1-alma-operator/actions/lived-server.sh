#!/usr/bin/env bash
# Debian stable amd64 cloud guest; run as ordinary user with sudo authorization.
source "$(dirname "$(readlink -f "$0")")/lib.sh"

server_prerequisites() {
    # https://manpages.debian.org/trixie/apt/apt-get.8.en.html
    root env DEBIAN_FRONTEND=noninteractive apt-get update
    root env DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates curl \
        cron nftables unattended-upgrades logrotate openssh-client sudo procps util-linux adduser
    mkdir -p "$HOME/server-stack" "$HOME/.local/state/cal-server" "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
}

server_compose() {
    # https://docs.docker.com/engine/install/debian/
    local key source_file
    key=$(mktemp); source_file=$(mktemp)
    curl -fsSL https://download.docker.com/linux/debian/gpg -o "$key"
    install_root_file "$key" /etc/apt/keyrings/docker.asc 644
    # The Debian stable cloud base supplies its actual codename, not a guessed release.
    . /etc/os-release
    cat > "$source_file" <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $VERSION_CODENAME
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
    install_root_file "$source_file" /etc/apt/sources.list.d/docker.sources 644
    rm "$key" "$source_file"
    root env DEBIAN_FRONTEND=noninteractive apt-get update
    root env DEBIAN_FRONTEND=noninteractive apt-get install -y docker-ce docker-ce-cli \
        containerd.io docker-buildx-plugin docker-compose-plugin
    root systemctl enable --now docker.service
    cd "$HOME/server-stack"
    # https://docs.docker.com/reference/compose-file/
    # https://hub.docker.com/_/caddy ; https://hub.docker.com/_/postgres
    # https://github.com/traefik/whoami
    cat > compose.yaml <<'COMPOSE'
name: cal-server
services:
  web:
    image: docker.io/traefik/whoami:v1.11.0
    restart: unless-stopped
  proxy:
    image: docker.io/library/caddy:2-alpine
    restart: unless-stopped
    ports:
      - "127.0.0.1:18081:80"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy-data:/data
      - caddy-config:/config
    depends_on:
      - web
  db:
    image: docker.io/library/postgres:17-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: cal
      POSTGRES_PASSWORD: disposable-database-password
      POSTGRES_DB: cal
    volumes:
      - database:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cal -d cal"]
      interval: 5s
      timeout: 3s
      retries: 30
volumes:
  database:
  caddy-data:
  caddy-config:
COMPOSE
    cat > Caddyfile <<'CADDY'
:80 {
    respond "Server setup"
}
CADDY
    # https://docs.docker.com/reference/cli/docker/compose/up/
    root docker compose up --detach --wait --wait-timeout 240
}

server_orchestrator() {
    # https://docs.k3s.io/quick-start
    # https://docs.k3s.io/installation/configuration
    # https://docs.k3s.io/cli/server
    # Root helper stdin carries sudo authentication; sh itself obtains the web script.
    root bash -o pipefail -c 'curl -sfL https://get.k3s.io | sh -s - server --disable traefik --disable servicelb --write-kubeconfig-mode 600 --kubelet-arg fail-swap-on=false'
    cat > "$HOME/server-stack/workload.yaml" <<'YAML'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cal-web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cal-web
  template:
    metadata:
      labels:
        app: cal-web
    spec:
      containers:
        - name: web
          image: docker.io/traefik/whoami:v1.11.0
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: 20m
              memory: 32Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: cal-web
spec:
  selector:
    app: cal-web
  ports:
    - port: 80
      targetPort: 80
YAML
    # https://kubernetes.io/docs/reference/kubectl/generated/kubectl_wait/
    # https://kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/
    # https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_status/
    root k3s kubectl wait --for=create node --all --timeout=300s
    root k3s kubectl wait --for=condition=Ready node --all --timeout=300s
    root k3s kubectl apply -f "$HOME/server-stack/workload.yaml"
    root k3s kubectl rollout status deployment/cal-web --timeout=300s
}

server_reverse_proxy() {
    # https://caddyserver.com/docs/quick-starts/reverse-proxy
    # https://caddyserver.com/docs/command-line#caddy-reload
    cd "$HOME/server-stack"
    # Truncate the existing bind-mounted inode; do not replace it with rename.
    cat > Caddyfile <<'CADDY'
:80 {
    encode gzip
    header X-Environment disposable-server
    reverse_proxy web:80
}
CADDY
    root docker compose exec -T proxy caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
    root docker compose exec -T proxy caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile
    curl --fail --max-time 30 http://127.0.0.1:18081/
}

server_database() {
    # https://hub.docker.com/_/postgres
    # https://www.postgresql.org/docs/current/app-psql.html
    cd "$HOME/server-stack"
    root docker compose exec -T db psql -U cal -d cal -v ON_ERROR_STOP=1 -c \
        "CREATE TABLE tasks (id integer PRIMARY KEY, title text NOT NULL); INSERT INTO tasks VALUES (1, 'Rotate application logs'), (2, 'Review backups');"
    root docker compose exec -T db psql -U cal -d cal -v ON_ERROR_STOP=1 -c 'TABLE tasks;'
}

server_binary_service() {
    # https://prometheus.io/docs/guides/node-exporter/
    # https://github.com/prometheus/node_exporter/releases/tag/v1.9.1
    local work
    work=$(mktemp -d)
    cd "$work"
    curl -fL --max-time 300 -o node_exporter-1.9.1.linux-amd64.tar.gz \
        https://github.com/prometheus/node_exporter/releases/download/v1.9.1/node_exporter-1.9.1.linux-amd64.tar.gz
    curl -fL --max-time 60 -o sha256sums.txt \
        https://github.com/prometheus/node_exporter/releases/download/v1.9.1/sha256sums.txt
    # https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html
    awk '$2 == "node_exporter-1.9.1.linux-amd64.tar.gz" {print}' sha256sums.txt > selected.sha256
    test -s selected.sha256
    sha256sum --check selected.sha256
    tar -xzf node_exporter-1.9.1.linux-amd64.tar.gz
    install_root_file node_exporter-1.9.1.linux-amd64/node_exporter /usr/local/bin/node_exporter 755
    # https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
    # https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
    cat > cal-node-exporter.service <<'UNIT'
[Unit]
Description=Local system metrics exporter
After=network.target
[Service]
DynamicUser=yes
ExecStart=/usr/local/bin/node_exporter --web.listen-address=127.0.0.1:9100
Restart=on-failure
[Install]
WantedBy=multi-user.target
UNIT
    install_root_file cal-node-exporter.service /etc/systemd/system/cal-node-exporter.service 644
    cp selected.sha256 "$HOME/.local/state/cal-server/node-exporter.sha256"
    cd "$HOME"
    rm -r "$work"
    root systemctl daemon-reload
    root systemctl enable --now cal-node-exporter.service
    root systemctl is-active --quiet cal-node-exporter.service
}

server_scheduled_jobs() {
    local work
    work=$(mktemp -d)
    # https://manpages.debian.org/trixie/cron/crontab.5.en.html
    cat > "$work/cal-maintenance" <<'CRON'
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
17 * * * * root /usr/bin/date -u >> /var/log/cal-maintenance.log
CRON
    install_root_file "$work/cal-maintenance" /etc/cron.d/cal-maintenance 644
    # https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
    # https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
    cat > "$work/cal-maintenance.service" <<'UNIT'
[Unit]
Description=Record a daily maintenance timestamp
[Service]
Type=oneshot
ExecStart=/usr/bin/date -u
StandardOutput=append:/var/log/cal-maintenance.log
UNIT
    cat > "$work/cal-maintenance.timer" <<'UNIT'
[Unit]
Description=Daily server maintenance reminder
[Timer]
OnCalendar=daily
Persistent=true
[Install]
WantedBy=timers.target
UNIT
    install_root_file "$work/cal-maintenance.service" /etc/systemd/system/cal-maintenance.service 644
    install_root_file "$work/cal-maintenance.timer" /etc/systemd/system/cal-maintenance.timer 644
    rm -r "$work"
    root systemctl daemon-reload
    root systemctl enable --now cron.service cal-maintenance.timer
    root systemctl start cal-maintenance.service
}

server_firewall() {
    local work
    work=$(mktemp -d)
    # https://wiki.nftables.org/wiki-nftables/index.php/Simple_ruleset_for_a_server
    # Own input table: do not flush Docker/K3s forwarding or NAT tables.
    cat > "$work/firewall.nft" <<'NFT'
table inet cal_filter {
    chain input {
        type filter hook input priority 0; policy drop;
        ct state established,related accept
        iifname "lo" accept
        meta l4proto { icmp, ipv6-icmp } accept
        udp sport 67 udp dport 68 accept
        udp sport 547 udp dport 546 accept
        ip saddr 10.42.0.0/16 accept
        tcp dport { 22, 6443 } accept
        counter drop
    }
}
NFT
    install_root_file "$work/firewall.nft" /etc/cal-firewall.nft 644
    cat > "$work/cal-firewall.service" <<'UNIT'
[Unit]
Description=Server input firewall
Before=docker.service k3s.service
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/sbin/nft -f /etc/cal-firewall.nft
[Install]
WantedBy=multi-user.target
UNIT
    install_root_file "$work/cal-firewall.service" /etc/systemd/system/cal-firewall.service 644
    rm -r "$work"
    root nft --check --file /etc/cal-firewall.nft
    root systemctl daemon-reload
    root systemctl enable --now cal-firewall.service
}

server_account() {
    # https://manpages.debian.org/trixie/adduser/adduser.8.en.html
    # https://man.openbsd.org/ssh-keygen
    # https://www.sudo.ws/docs/man/sudoers.man/
    # https://www.sudo.ws/docs/man/visudo.man/
    local policy
    root adduser --disabled-password --comment '' calops
    ssh-keygen -q -t ed25519 -N '' -C 'disposable-server' -f "$HOME/.ssh/calops"
    root install -d -m 700 -o calops -g calops /home/calops/.ssh
    root install -m 600 -o calops -g calops "$HOME/.ssh/calops.pub" /home/calops/.ssh/authorized_keys
    policy=$(mktemp)
    printf '%s\n' 'calops ALL=(root) NOPASSWD: /usr/bin/systemctl restart cal-node-exporter.service' > "$policy"
    root visudo -cf "$policy"
    install_root_file "$policy" /etc/sudoers.d/calops 440
    rm "$policy"
}

server_kernel_parameters() {
    # https://manpages.debian.org/trixie/procps/sysctl.8.en.html
    # https://docs.kernel.org/admin-guide/sysctl/vm.html
    # https://docs.kernel.org/networking/ip-sysctl.html
    local config
    config=$(mktemp)
    printf '%s\n' 'vm.swappiness = 10' 'net.ipv4.tcp_keepalive_time = 600' > "$config"
    install_root_file "$config" /etc/sysctl.d/90-cal-server.conf 644
    rm "$config"
    root sysctl -p /etc/sysctl.d/90-cal-server.conf
}

server_swap() {
    # https://manpages.debian.org/trixie/mount/swapon.8.en.html
    # https://manpages.debian.org/trixie/util-linux/mkswap.8.en.html
    # https://manpages.debian.org/trixie/mount/fstab.5.en.html
    # Fresh Debian cloud root filesystem must support a non-sparse swap file.
    local fstab
    root test ! -e /swap-cal
    root dd if=/dev/zero of=/swap-cal bs=1M count=512 status=none
    root chmod 600 /swap-cal
    root mkswap /swap-cal
    root swapon /swap-cal
    fstab=$(mktemp)
    cat /etc/fstab > "$fstab"
    printf '\n%s\n' '/swap-cal none swap sw 0 0' >> "$fstab"
    install_root_file "$fstab" /etc/fstab 644
    rm "$fstab"
    root systemctl daemon-reload
}

server_automatic_updates() {
    # https://manpages.debian.org/trixie/unattended-upgrades/unattended-upgrade.8.en.html
    # https://github.com/mvo5/unattended-upgrades/blob/master/data/50unattended-upgrades.Debian
    # Keep the package's Debian origin/security defaults; enable daily execution.
    local config
    config=$(mktemp)
    cat > "$config" <<'APT'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
Unattended-Upgrade::Automatic-Reboot "false";
APT
    install_root_file "$config" /etc/apt/apt.conf.d/20auto-upgrades 644
    rm "$config"
    root systemctl enable --now apt-daily.timer apt-daily-upgrade.timer
}

server_log_rotation() {
    # https://manpages.debian.org/trixie/logrotate/logrotate.8.en.html
    local config
    config=$(mktemp)
    cat > "$config" <<'ROTATE'
/var/log/cal-maintenance.log {
    weekly
    rotate 4
    compress
    missingok
    notifempty
    create 0640 root adm
}
ROTATE
    install_root_file "$config" /etc/logrotate.d/cal-maintenance 644
    rm "$config"
    root logrotate --force /etc/logrotate.d/cal-maintenance
    root systemctl enable --now logrotate.timer
}

actions() {
    cat <<'ACTIONS'
server_prerequisites 1200
server_compose 1800
server_orchestrator 1800
server_reverse_proxy 120
server_database 120
server_binary_service 600
server_scheduled_jobs 120
server_firewall 120
server_account 120
server_kernel_parameters 60
server_swap 180
server_automatic_updates 120
server_log_rotation 120
ACTIONS
}
actions_main "$@"
