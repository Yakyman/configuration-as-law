#!/bin/bash
# The failure reported for 0.43: a declaration that names another export of the pinned
# Flatpak runtime and application commits could not be built
# (`ValueError: Flatpak reader bundle checksum mismatch`). Build such a declaration with
# the case party's own exported bundles and check that every reader replacement is
# in place. Build only; no machine is started.
set -euo pipefail
cd "$(dirname "$0")"
exec >logs/other-export-0.49.log 2>&1
fixture=other-export-049
image=images/other-export-049.qcow2
test ! -e "$fixture" && test ! -e "$image"
mkdir "$fixture"
trap 'rm -f "$image"; rm -rf "${image%.qcow2}.work" "$fixture"' EXIT
cp ../cases/inputs/runtime.flatpak ../cases/inputs/mpv.flatpak examples/recorded.sh "$fixture/"
ours_runtime=$(sha256sum flatpak-inputs/runtime.flatpak | cut -d' ' -f1)
ours_app=$(sha256sum flatpak-inputs/mpv.flatpak | cut -d' ' -f1)
runtime=$(sha256sum "$fixture/runtime.flatpak" | cut -d' ' -f1)
app=$(sha256sum "$fixture/mpv.flatpak" | cut -d' ' -f1)
echo "runtime export: ours $ours_runtime, other $runtime"
echo "application export: ours $ours_app, other $app"
test "$runtime" != "$ours_runtime"
test "$app" != "$ours_app"
cp examples/development.conf "$fixture/declaration.conf"
printf 'package flatpak 1.16.6-1~deb13u3\npackage gpg 2.4.7-21+deb13u1+b5\npackage gpg-agent 2.4.7-21+deb13u1+b5\n' >>"$fixture/declaration.conf"
printf 'flatpak runtime/org.freedesktop.Platform/x86_64/26.08 df26daaf9d07610b4a72cc4585566194051275ac68396597b06474396f66427c %s runtime.flatpak\n' "$runtime" >>"$fixture/declaration.conf"
printf 'flatpak app/io.mpv.Mpv/x86_64/stable 13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc %s mpv.flatpak\n' "$app" >>"$fixture/declaration.conf"
bash build.sh "$fixture/declaration.conf" "$image"
python3 check-other-export-049.py "${image%.qcow2}.work/root"
python3 compare-native-entries.py "${image%.qcow2}.work"
echo 'OTHER EXPORT OF THE PINNED FLATPAK COMMITS BUILDS; READER REPLACEMENTS IN PLACE PASS'
