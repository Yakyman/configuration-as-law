#!/bin/bash
# Runs inside the stock Debian 13 guest: install ed and tree at the versions of the self-test declaration with the
# guest's own apt; if the guest's archive does not have these versions, fetch the very same files from
# snapshot.debian.org inside the guest and install them with dpkg -i.
# Usage: guest.sh ED_URL TREE_URL
set -u
cloud-init status --wait >/dev/null 2>&1 || true
export DEBIAN_FRONTEND=noninteractive
echo "guest: dpkg-query before:"; dpkg-query -W ed tree 2>&1 | sed 's/^/  /'
if sudo -E apt-get update -q >/tmp/apt-update.log 2>&1 &&
   sudo -E apt-get install -y -q --no-install-recommends ed=1.21.1-1 tree=2.2.1-1 >/tmp/apt-install.log 2>&1; then
  echo "guest: installed with the guest's apt from its own archive"
  tail -n 3 /tmp/apt-install.log | sed 's/^/  /'
  sha256sum /var/cache/apt/archives/ed_1.21.1-1_*.deb /var/cache/apt/archives/tree_2.2.1-1_*.deb 2>/dev/null |
    sed 's/^/  deb in guest cache: /'
else
  echo "guest: apt could not install these versions; fetching the same files from the snapshot inside the guest"
  tail -n 5 /tmp/apt-install.log 2>/dev/null | sed 's/^/  /'
  mkdir -p /tmp/debs
  for u in "$@"; do
    curl -fsSL -o "/tmp/debs/$(basename "$u")" "$u" || wget -q -O "/tmp/debs/$(basename "$u")" "$u" || exit 3
  done
  sha256sum /tmp/debs/*.deb | sed 's/^/  deb fetched in guest: /'
  sudo dpkg -i /tmp/debs/*.deb || exit 4
fi
echo "guest: dpkg-query after:"; dpkg-query -W ed tree | sed 's/^/  /'
sync
