#!/bin/bash
# Server only. The pinned inputs that the lines of D-test name in the syntax of build/DECLARATION.md revision 11,
# made by the case party from the published upstream sources of PROGRAMS.md (never from the builder's folders):
#   pip      PyPI cowsay 6.1 wheel (checked against the SHA256 PyPI publishes)
#   npm      package-lock.json of cowsay@1.6.0, resolved by native npm in a node container
#   container  OCI archive of docker.io/library/alpine:3.20.3 (podman save --format oci-archive), its config digest
#   flatpak  bundles of runtime/org.freedesktop.Platform/x86_64/26.08 and app/io.mpv.Mpv/x86_64/stable from Flathub,
#            pulled without deployment in a Debian 13 container and exported by native `flatpak build-bundle`
# Output: $SERVER_DIR/inputs/ and inputs/manifest.tsv (KIND NAME FILE SHA256 EXTRA). Usage: make-inputs.sh [STEP...]
set -euo pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
. "$HERE/local.env"
OUT="$HOME/$SERVER_DIR/inputs"
mkdir -p "$OUT"
cd "$OUT"
log() { printf '%s %s\n' "$(date -u +%FT%TZ)" "$*"; }
man() { printf '%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$(sha256sum "$3" | cut -d' ' -f1)" "${4:-}" >> manifest.new; }
: > manifest.new
P=(--root "$OUT/podman/store" --runroot "$OUT/podman/run" --storage-driver vfs --cgroup-manager cgroupfs
   --events-backend file --tmpdir "$OUT/podman/tmp")
mkdir -p podman/tmp
export XDG_RUNTIME_DIR="$OUT/podman/xdg"; mkdir -p "$XDG_RUNTIME_DIR"; chmod 700 "$XDG_RUNTIME_DIR"
pod() { podman "${P[@]}" "$@"; }
steps=${*:-pip npm container flatpak}

for step in $steps; do
case $step in
pip)
  log "pip: cowsay 6.1 from PyPI"
  python3 -I - <<'PY'
import hashlib, json, urllib.request
info = json.load(urllib.request.urlopen('https://pypi.org/pypi/cowsay/6.1/json', timeout=60))
w = [u for u in info['urls'] if u['filename'].endswith('py3-none-any.whl')][0]
data = urllib.request.urlopen(w['url'], timeout=120).read()
assert hashlib.sha256(data).hexdigest() == w['digests']['sha256'], 'PyPI checksum differs'
open(w['filename'], 'wb').write(data)
print(w['url'], w['digests']['sha256'])
PY
  man pip cowsay cowsay-6.1-py3-none-any.whl 6.1 ;;
npm)
  log "npm: package-lock.json of cowsay@1.6.0"
  rm -rf npm-work; mkdir -p npm-work
  printf '{"name":"cases-cowsay","version":"1.0.0","private":true,"dependencies":{"cowsay":"1.6.0"}}\n' > npm-work/package.json
  pod pull -q docker.io/library/node:20-bookworm-slim >/dev/null
  pod run --rm --cgroups=disabled --network=slirp4netns -v "$OUT/npm-work:/w" -w /w docker.io/library/node:20-bookworm-slim \
    npm install --package-lock-only --ignore-scripts --no-audit --no-fund --lockfile-version 3
  cp npm-work/package-lock.json cowsay-package-lock.json
  man npm cowsay cowsay-package-lock.json 1.6.0 ;;
container)
  log "container: alpine 3.20.3"
  pod pull -q docker.io/library/alpine:3.20.3 >/dev/null
  id=$(pod image inspect --format '{{.Id}}' docker.io/library/alpine:3.20.3)
  rm -f alpine.oci.tar
  pod save --format oci-archive --output "$OUT/alpine.oci.tar" docker.io/library/alpine:3.20.3
  man container docker.io/library/alpine:3.20.3 alpine.oci.tar "$id" ;;
flatpak)
  log "flatpak: Platform 26.08 and io.mpv.Mpv stable from Flathub"
  mkdir -p fp
  cat > fp/inside.sh <<'SH'
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get -q update >/dev/null
apt-get -q -y install --no-install-recommends flatpak ostree ca-certificates >/dev/null
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user --noninteractive --no-deploy --no-related flathub runtime/org.freedesktop.Platform/x86_64/26.08
flatpak install --user --noninteractive --no-deploy --no-related flathub app/io.mpv.Mpv/x86_64/stable
R=$HOME/.local/share/flatpak/repo
for ref in runtime/org.freedesktop.Platform/x86_64/26.08 app/io.mpv.Mpv/x86_64/stable; do
  c=$(ostree --repo=$R rev-parse "flathub:$ref" 2>/dev/null || ostree --repo=$R rev-parse "$ref")
  echo "COMMIT $ref $c"
done
ostree --repo=$R refs
flatpak build-bundle --runtime $R /out/runtime.flatpak org.freedesktop.Platform 26.08 2>&1 || \
  flatpak build-bundle --runtime --from-commit="$(ostree --repo=$R rev-parse flathub:runtime/org.freedesktop.Platform/x86_64/26.08)" $R /out/runtime.flatpak org.freedesktop.Platform 26.08
flatpak build-bundle $R /out/mpv.flatpak io.mpv.Mpv stable 2>&1 || \
  flatpak build-bundle --from-commit="$(ostree --repo=$R rev-parse flathub:app/io.mpv.Mpv/x86_64/stable)" $R /out/mpv.flatpak io.mpv.Mpv stable
SH
  pod pull -q docker.io/library/debian:trixie >/dev/null
  pod run --rm --cgroups=disabled --network=slirp4netns -v "$OUT/fp:/out" docker.io/library/debian:trixie bash /out/inside.sh | tee fp/inside.out
  rc=$(grep '^COMMIT runtime/' fp/inside.out | cut -d' ' -f3); ac=$(grep '^COMMIT app/' fp/inside.out | cut -d' ' -f3)
  cp fp/runtime.flatpak runtime.flatpak; cp fp/mpv.flatpak mpv.flatpak
  man flatpak runtime/org.freedesktop.Platform/x86_64/26.08 runtime.flatpak "$rc"
  man flatpak app/io.mpv.Mpv/x86_64/stable mpv.flatpak "$ac" ;;
game)
  # OW-8 through the declaration (REVIEW.md R2): the bundles of the `linuxgsm` line, from the upstream archives of
  # PROGRAMS.md and the two default configurations of the published release (environment GAME_SOURCE: its archive)
  log "game: LinuxGSM 26.5.0 / 26.6.0 sources, ET 2.60b server archive, defaults of $(basename "${GAME_SOURCE:?}")"
  mkdir -p game
  for x in "linuxgsm-26.5.0.tar.gz https://codeload.github.com/GameServerManagers/LinuxGSM/tar.gz/50dc4e551b661b9d1fa39c291068a16a66056aff" \
           "linuxgsm-26.6.0.tar.gz https://codeload.github.com/GameServerManagers/LinuxGSM/tar.gz/9ca2e951c6e15d4db7184a60e1fd8a831b2cdb0f" \
           "wet-2.60b.tar.xz https://linuxgsm.download/WolfensteinEnemyTerritory/wet-2.60b-linux-i386-linuxgsm-20261101.tar.xz"; do
    set -- $x
    [ -s "game/$1" ] || curl -fsSL --retry 2 --max-time 600 -o "game/$1" "$2"
  done
  tar -xzf "$GAME_SOURCE" -C game game-common.cfg game-server.cfg
  python3 -I "$HERE/tools/make-game-bundle.py" game
  for r in 26.5.0 26.6.0; do man linuxgsm "$r" "game/linuxgsm-wet-$r.tar" "$r"; done ;;
*) echo "unknown step $step" >&2; exit 2 ;;
esac
done
# merge: replace the rows of the steps made now
touch manifest.tsv
cut -f1 manifest.new | sort -u > kinds.new
grep -v -F -f <(sed 's/$/\t/' kinds.new) manifest.tsv > manifest.keep || true
cat manifest.keep manifest.new > manifest.tsv
rm -f manifest.new manifest.keep kinds.new
log "manifest:"; cat manifest.tsv
# throw-away stores
pod system reset --force >/dev/null 2>&1 || true
rm -rf podman npm-work fp
log "INPUTS DONE"
