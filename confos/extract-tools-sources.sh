#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p interpreter-inputs/tools/trees
for spec in 'dash dash_0.5.12-12.dsc' 'mawk mawk_1.3.4.20250131-1.dsc' 'gawk gawk_5.2.1-2.dsc' 'sed sed_4.9-2+deb13u1.dsc' 'make make-dfsg_4.4.1-2.dsc'; do
    read -r name dsc <<<"$spec"
    test -d "interpreter-inputs/tools/trees/$name" || dpkg-source --no-check -x "interpreter-inputs/tools/$dsc" "interpreter-inputs/tools/trees/$name"
done
