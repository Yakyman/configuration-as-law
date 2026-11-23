#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p downloads raw keys base
url=https://cloud.debian.org/images/cloud/trixie/20261116-2664/debian-13-generic-amd64-20261116-2664.qcow2
digest=e53a93ef33f828ceed0e7278c2cc2753bdc7d5098fbfae15bd64b6d878db350ea3744247763a1c8ecb6b4019a0f623c38caf6038ad6f9c357fb4e01493ddf1a3
if [ ! -f downloads/source.qcow2 ]; then
  curl --fail --location --retry 3 --output downloads/source.qcow2.part "$url"
  mv downloads/source.qcow2.part downloads/source.qcow2
fi
printf '%s  downloads/source.qcow2\n' "$digest" | sha512sum -c -
chmod 444 downloads/source.qcow2
if [ ! -f keys/guest ]; then ssh-keygen -q -t ed25519 -N '' -C disposable-management -f keys/guest; fi
