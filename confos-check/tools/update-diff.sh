#!/bin/bash
# For the update case: versions of chosen packages at T0, T1, T2 (snapshot.debian.org, trixie main amd64).
set -u
. "$(dirname "$0")/../local.env"
W=$HOME/$SERVER_DIR/verify/updates; mkdir -p "$W"; cd "$W" || exit 1
for ts in 20260801T000000Z 20261001T000000Z 20261123T000000Z; do
  [ -s "Packages-$ts" ] || { curl -fsSL --max-time 300 -o "Packages-$ts.xz" "https://snapshot.debian.org/archive/debian/$ts/dists/trixie/main/binary-amd64/Packages.xz" && xz -dc "Packages-$ts.xz" > "Packages-$ts"; }
done
printf '%-22s %-28s %-28s %-28s\n' package T0=20260801 T1=20261001 T2=20261123
for p in "$@"; do
  row="$p"
  for ts in 20260801T000000Z 20261001T000000Z 20261123T000000Z; do
    v=$(awk -v p="$p" '$1=="Package:"{n=$2} $1=="Version:" && n==p {print $2; exit}' "Packages-$ts")
    row="$row ${v:--}"
  done
  printf '%-22s %-28s %-28s %-28s\n' $row
done
echo "changed T0->T1: $(join -j1 <(awk '$1=="Package:"{n=$2} $1=="Version:"{print n, $2}' Packages-20260801T000000Z | sort -u) <(awk '$1=="Package:"{n=$2} $1=="Version:"{print n, $2}' Packages-20261001T000000Z | sort -u) | awk '$2!=$3' | wc -l) packages"
echo "changed T1->T2: $(join -j1 <(awk '$1=="Package:"{n=$2} $1=="Version:"{print n, $2}' Packages-20261001T000000Z | sort -u) <(awk '$1=="Package:"{n=$2} $1=="Version:"{print n, $2}' Packages-20261123T000000Z | sort -u) | awk '$2!=$3' | wc -l) packages"
