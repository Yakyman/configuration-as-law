#!/bin/bash
# Reads the trixie point-release version at several snapshot.debian.org timestamps. Run on the server.
set -u
for ts in 20260601T000000Z 20260801T000000Z 20260901T000000Z 20261001T000000Z 20261101T000000Z 20261115T000000Z 20261122T000000Z 20261123T000000Z; do
  v=$(curl -fsSL --max-time 90 "https://snapshot.debian.org/archive/debian/$ts/dists/trixie/Release" | awk '/^Version:/{print $2} /^Date:/{sub(/^Date: /,""); d=$0} END{print d}' | tr '\n' ' ')
  echo "$ts $v"
done
