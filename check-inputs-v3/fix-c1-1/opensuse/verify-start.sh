#!/bin/bash
set -euo pipefail
cd "${LAB_ROOT:?}"
d=fix-c1-1/opensuse
while systemctl --user is-active --quiet cal-fx1-opensuse-download; do sleep 5; done
iso=openSUSE-Tumbleweed-DVD-x86_64-Snapshot20261120-Media.iso
mkdir -m700 "$d/gnupg"
GNUPGHOME="$PWD/$d/gnupg"; export GNUPGHOME
curl -fLsS -o "$d/signing.key" https://download.opensuse.org/tumbleweed/repo/oss/repodata/repomd.xml.key
gpg --batch --import "$d/signing.key" >/dev/null 2>&1
gpg --batch --status-fd 1 --verify "images/$iso.sha256.asc" "images/$iso.sha256" 2>/dev/null > "$d/signature-status.txt"
(cd images; sha256sum -c "$iso.sha256") > "$d/checksum-status.txt"
printf 'verified_utc=%s\n' "$(date -u +%FT%TZ)" >> "$d/checksum-status.txt"
exec bash "$d/launch.sh"
