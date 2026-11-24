#!/bin/bash
# Checks that every program and package named in PROGRAMS.md exists at its source. Run on the server.
set -u
. "$(dirname "$0")/../local.env"
W=${1:-$HOME/$SERVER_DIR/verify}
mkdir -p "$W"; cd "$W" || exit 1
echo "== Debian trixie Release"
curl -fsS https://deb.debian.org/debian/dists/trixie/Release | grep -E '^(Version|Date|Suite|Codename):'
curl -fsS https://security.debian.org/debian-security/dists/trixie-security/Release | grep -E '^(Date|Suite):'
for comp in main; do
  curl -fsS -o Packages-main.xz https://deb.debian.org/debian/dists/trixie/main/binary-amd64/Packages.xz
done
xz -dkf Packages-main.xz
for p in ed tree hello python3 python3-pip python3-venv nodejs npm flatpak libfuse2t64 fuse3 curl wget gcc make libc6-dev git podman cron at bash perl-base firefox-esr chromium libreoffice-writer fonts-noto-cjk tmux jq bc bsdmainutils distro-info lib32gcc-s1 lib32stdc++6 libc6-i386 pigz unzip bzip2 openssh-server sudo nftables iproute2 kmod procps passwd uidmap slirp4netns systemd systemd-cron cowsay sl; do
  v=$(awk -v p="$p" '$1=="Package:"{n=$2} $1=="Version:" && n==p {print $2; exit}' Packages-main)
  printf '%-22s %s\n' "$p" "${v:-MISSING}"
done
echo "== PyPI"
for pv in cowsay/6.1 pyjokes/0.8.3; do curl -fsS -o /dev/null -w "%{http_code} $pv\n" https://pypi.org/pypi/$pv/json; done
echo "== npm"
for pv in cowsay/1.6.0 semver/7.6.3; do curl -fsS -o /dev/null -w "%{http_code} $pv\n" https://registry.npmjs.org/$pv; done
echo "== GitHub release assets"
for u in \
 https://github.com/BurntSushi/ripgrep/releases/download/14.1.1/ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz \
 https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-amd64 \
 https://github.com/neovim/neovim/releases/download/v0.10.4/nvim-linux-x86_64.appimage \
 https://github.com/neovim/neovim/releases/download/v0.9.5/nvim.appimage \
 https://raw.githubusercontent.com/docker-library/hello-world/522bcd2faf422c60b9d20e64d7cd6d56600aec97/hello.c \
 https://ftp.gnu.org/gnu/hello/hello-2.12.1.tar.gz \
 https://raw.githubusercontent.com/GameServerManagers/LinuxGSM/50dc4e551b661b9d1fa39c291068a16a66056aff/linuxgsm.sh ; do
  curl -fsSL -o /dev/null -w "%{http_code} %{size_download} $u\n" "$u" || echo "FAIL $u"
done
echo "== Flathub"
for a in io.mpv.Mpv org.gnome.Calculator net.sourceforge.ExtremeTuxRacer; do
  curl -fsS -o "flathub-$a.json" -w "%{http_code} $a\n" "https://flathub.org/api/v2/appstream/$a" || echo "FAIL $a"
  python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print("  runtime:", d.get("bundle",{}).get("runtime"))' "flathub-$a.json" 2>/dev/null
done
echo "== Docker Hub"
for r in library/alpine:3.20.3 library/busybox:1.36.1 library/hello-world:latest; do
  repo=${r%%:*}; tag=${r##*:}
  curl -fsS -o /dev/null -w "%{http_code} $r\n" "https://hub.docker.com/v2/repositories/$repo/tags/$tag" || echo "FAIL $r"
done
