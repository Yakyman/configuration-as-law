#!/bin/bash
set -euo pipefail
export TZ=UTC
# Run from the laboratory root on the server.
mkdir -p images C1/fedora/gnupg
chmod 700 C1/fedora/gnupg
cd images
curl -fL --retry 2 -O https://download.fedoraproject.org/pub/fedora/linux/releases/45/Workstation/x86_64/iso/Fedora-Workstation-Live-45-1.4.x86_64.iso
curl -fLsS -O https://dl.fedoraproject.org/pub/fedora/linux/releases/45/Workstation/x86_64/iso/Fedora-Workstation-45-1.4-x86_64-CHECKSUM
curl -fLsS -O https://fedoraproject.org/fedora.gpg
gpgv --homedir ../C1/fedora/gnupg --keyring ./fedora.gpg --output ../C1/fedora/checksums Fedora-Workstation-45-1.4-x86_64-CHECKSUM 2> ../C1/fedora/signature.log
sha256sum -c ../C1/fedora/checksums > ../C1/fedora/checksum.log
