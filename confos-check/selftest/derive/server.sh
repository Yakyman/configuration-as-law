#!/bin/bash
# Self-test of `derive`, run on the server inside the case party's folder (copied there by run.sh).
# An experiment: derive from a declaration, install the same packages in a stock Debian 13 machine, read its disk
# from outside, and compare object by object. Exit status 0 only if every check passes.
set -u
TOP=$(cd "$(dirname "$0")/.." && pwd)        # the derive folder on the server
. "$TOP/local.env"
export STRIP="$TOP"
cd "$TOP"
W=work                                        # throw-away tree of this run (relative to TOP)
R=results
rm -rf "$W" "$R"
mkdir -p "$W" "$R"
DERIVE="python3 -I $TOP/derive"
CHECK="python3 -I $TOP/selftest/check.py"
STATUS=0
QPID=""
note() { printf '\n== %s\n' "$*"; }
result() {
  if [ "$1" -eq 0 ]; then s="STEP $2: PASS"; else s="STEP $2: FAIL"; STATUS=1; fi
  echo "$s"; echo "$s" >> "$TOP/$R/steps.txt"
}

cleanup() {
  if [ -n "$QPID" ] && kill -0 "$QPID" 2>/dev/null; then kill "$QPID" 2>/dev/null; sleep 2; kill -9 "$QPID" 2>/dev/null; fi
  if [ -f "$W/qemu.pid" ]; then kill "$(cat "$W/qemu.pid")" 2>/dev/null; fi
  rm -rf "$TOP/$W"
}
trap cleanup EXIT

echo "derive self-test, $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "derive sha256 $(sha256sum "$TOP/derive" | cut -d' ' -f1)"
echo "check.py sha256 $(sha256sum "$TOP/selftest/check.py" | cut -d' ' -f1)"
echo "declaration:"; sed 's/^/  | /' selftest/decl/test.conf

note "1. derive from the declaration alone (empty cache, then again from the cache)"
$DERIVE --declaration selftest/decl/test.conf --cache "$W/cache" --out "$R/derived.jsonl"; rc=$?
echo "derive exit status $rc"; [ $rc -eq 0 ]; result $? "1a derive exits 0"
$CHECK lines "$R/derived.jsonl" selftest/decl/test.conf; result $? "1b every line has derived objects"
$DERIVE --declaration selftest/decl/test.conf --cache "$W/cache" --out "$W/derived-again.jsonl"; rc=$?
$CHECK same "$R/derived.jsonl" "$W/derived-again.jsonl"; result $? "1c a second derivation is identical"
cp "$W/cache/derive-reads.log" "$R/derive-reads.log"

note "2. the same packages installed in a stock Debian 13 machine; its disk read from outside"
IMG="$HOME/$STOCK_IMAGE"
echo "stock image sha512 matches local.env: $( [ "$(sha512sum "$IMG" | cut -d' ' -f1)" = "$STOCK_IMAGE_SHA512" ] && echo yes || echo NO)"
qemu-img create -q -f qcow2 -b "$IMG" -F qcow2 "$W/overlay.qcow2" 8G
ssh-keygen -q -t ed25519 -N '' -C derive-selftest -f "$W/key"
printf 'instance-id: derive-selftest\nlocal-hostname: derive-selftest\n' > "$W/meta-data"
{ printf '#cloud-config\nusers:\n  - name: probe\n    shell: /bin/bash\n    sudo: "ALL=(ALL) NOPASSWD:ALL"\n'
  printf '    ssh_authorized_keys:\n      - %s\n' "$(cat "$W/key.pub")"; } > "$W/user-data"
cloud-localds "$W/seed.img" "$W/user-data" "$W/meta-data"
PORT=""
# a free common slot is waited for (at most CASES_SLOT_WAIT seconds, default 7200)
WAITED=0
while [ -z "$PORT" ] && [ "$WAITED" -le "${CASES_SLOT_WAIT:-7200}" ]; do
for N in 1 2 3 4 5 6; do
  P=$((24410 + N))
  ss -ltn | grep -q ":$P " && continue
  flock -n "$HOME/$SLOTS_DIR/slot-$N.lock" qemu-system-x86_64 -name derive-selftest -machine q35,accel=kvm \
    -cpu host -smp 2 -m 2048 -drive "file=$W/overlay.qcow2,if=virtio,format=qcow2" \
    -drive "file=$W/seed.img,if=virtio,format=raw" -netdev "user,id=n,hostfwd=tcp:127.0.0.1:$P-:22" \
    -device virtio-net-pci,netdev=n -display none -serial "file:$W/serial.log" -pidfile "$W/qemu.pid" &
  QPID=$!
  sleep 3
  if kill -0 "$QPID" 2>/dev/null; then PORT=$P; echo "machine started in slot $N"; break; fi
  QPID=""
done
[ -n "$PORT" ] || { sleep 30; WAITED=$((WAITED + 30)); }
done
[ -n "$PORT" ] || { echo "no free slot"; result 1 "2a machine started"; exit 1; }
SSH="ssh -i $W/key -p $PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=5"
up=1
for i in $(seq 1 60); do $SSH probe@127.0.0.1 true 2>/dev/null && { up=0; break; }; sleep 5; done
result $up "2a machine reachable over ssh"
if [ $up -eq 0 ]; then
  scp -q -i "$W/key" -P "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR \
    selftest/guest.sh probe@127.0.0.1:guest.sh
  ED_URL=$(grep -o '"url": "[^"]*ed_1.21.1-1[^"]*"' "$R/derived.jsonl" | head -1 | cut -d'"' -f4)
  TREE_URL=$(grep -o '"url": "[^"]*tree_2.2.1-1[^"]*"' "$R/derived.jsonl" | head -1 | cut -d'"' -f4)
  $SSH probe@127.0.0.1 bash guest.sh "$ED_URL" "$TREE_URL"; result $? "2b ed and tree installed in the machine"
  $SSH probe@127.0.0.1 sudo poweroff 2>/dev/null
  for i in $(seq 1 60); do kill -0 "$QPID" 2>/dev/null || break; sleep 2; done
  if kill -0 "$QPID" 2>/dev/null; then echo "machine did not stop; power cut"; kill "$(cat "$W/qemu.pid")"; sleep 3; fi
  QPID=""
  echo "machine stopped; reading its disk read-only from outside"
  virt-ls --format=qcow2 -a "$W/overlay.qcow2" --csv -lR --uids --checksum=sha256 / > "$W/listing.csv" 2> "$W/virt-ls.err"
  rc=$?; echo "virt-ls exit status $rc, $(wc -l < "$W/listing.csv") lines"; [ $rc -eq 0 ] || head -5 "$W/virt-ls.err"
  $CHECK disk "$R/derived.jsonl" "$W/listing.csv" ed tree; result $? "2c every derived object of ed and tree is on the disk as derived"
fi

note "3. what derive read (derive-reads.log of both runs of step 1)"
$CHECK reads "$R/derived.jsonl" "$R/derive-reads.log" selftest/decl/test.conf "$W/cache" ed tree
result $? "3 derive read only the declaration, its source, the two named packages and the snapshot indexes"

note "4. a dependency that no line names"
$CHECK underived "$R/derived.jsonl" "$R/derive-reads.log" ed tree
result $? "4 the unnamed dependency is underived and not read"

note "5. guard: a disk image is refused"
$DERIVE --declaration "$W/overlay.qcow2" --cache "$W/cache-guard" --out "$W/guard.jsonl" 2>&1; rc=$?
echo "derive on a qcow2 disk: exit status $rc"
ln -s overlay.qcow2 "$W/declaration-without-suffix"
$DERIVE --declaration "$W/declaration-without-suffix" --cache "$W/cache-guard" --out "$W/guard.jsonl" 2>&1; rc2=$?
echo "derive on a qcow2 disk without suffix (by its magic): exit status $rc2"
[ $rc -eq 2 ] && [ $rc2 -eq 2 ] && [ ! -e "$W/guard.jsonl" ] && [ ! -e "$W/cache-guard/derive-reads.log" ]
result $? "5 disk images refused before anything is read"

note "6. unknown kind"
$DERIVE --declaration selftest/decl/unknown.conf --cache "$W/cache-unknown" --out "$R/unknown.jsonl" 2>&1; rc=$?
echo "exit status $rc"; sed 's/^/  /' "$R/unknown.jsonl"
[ $rc -eq 2 ] && grep -q '"kind": "error"' "$R/unknown.jsonl"; result $? "6 unknown kind gives an error object and exit 2"

note "7. the base: components of the published component lock of the snapshot the declaration names"
# The base line names the published release (published/VERSION); the snapshot line names an archive state.
# T2 (newest state) must give the lock components/T2.txt (= components.txt); T0 must give components/T0.txt,
# whose versions differ, so a derivation that ignores the snapshot fails 7d.
V=$(cat published/VERSION)
mkdir -p "$W/decl-base"
printf 'base %s\nsnapshot 20261123T000000Z\n' "$V" > "$W/decl-base/t2.conf"
printf 'base %s\nsnapshot 20260801T000000Z\n' "$V" > "$W/decl-base/t0.conf"
$DERIVE --declaration "$W/decl-base/t2.conf" --components published/components.txt --cache "$W/cache-base" \
  --out "$R/base.jsonl"; rc=$?
echo "derive exit status $rc"; [ $rc -eq 0 ]; result $? "7a derive of the base at T2 exits 0"
$CHECK base "$R/base.jsonl" published/components/20261123T000000Z.txt; result $? "7b every T2 component derived at its locked version"
$DERIVE --declaration "$W/decl-base/t0.conf" --components published/components.txt --cache "$W/cache-base" \
  --out "$R/base-t0.jsonl"; rc=$?
echo "derive exit status $rc"; [ $rc -eq 0 ]; result $? "7c derive of the base at T0 exits 0"
$CHECK base "$R/base-t0.jsonl" published/components/20260801T000000Z.txt; result $? "7d every T0 component derived at its locked version"

note "8. the kinds of DECLARATION.md revisions 6-18: one line each, small source files beside the declaration"
D8="$W/decl-r11"; mkdir -p "$D8"
for n in w.whl lock.json a.flatpak img.appimage s.c oci.tar unit.timer game.tar; do printf 'content of %s\n' "$n" > "$D8/$n"; done
h() { sha256sum "$D8/$1" | cut -d' ' -f1; }
C=13baef0d642fdf97a1c8b542288453e27b2335ec29e54c5cb29c0a2df509b5bc
I=63b790fccc9078ab8bb913d94a5d869e19fca9b77712b315da3fa45bb8f14636
{ echo "pip Cow_Say 6.1 $(h w.whl) w.whl"; echo "npm cowsay 1.6.0 $(h lock.json) lock.json"
  echo "flatpak app/io.mpv.Mpv/x86_64/stable $C $(h a.flatpak) a.flatpak"
  echo "appimage /home/user/bin/nvim 0755 $(h img.appimage) img.appimage"
  echo "compile /home/user/bin/hello 0755 $(h s.c) s.c -O2"
  echo "container u docker.io/library/alpine:3.20.3 $I $(h oci.tar) oci.tar"
  echo "user-unit u cases-tick.timer enabled $(h unit.timer) unit.timer"
  echo "user-unit u cases-tick.service disabled $(h unit.timer) unit.timer"
  echo "linuxgsm user /home/user/game 26.5.0 $(h game.tar) game.tar"
  echo "pip bad 1.0 0000000000000000000000000000000000000000000000000000000000000000 w.whl"; } > "$D8/declaration.conf"
$DERIVE --declaration "$D8/declaration.conf" --cache "$W/cache-r11" --out "$R/r11.jsonl"; rc=$?
echo "derive exit status $rc (2 expected: the last line's checksum is wrong)"; sed 's/^/  /' "$R/r11.jsonl" | cut -c1-220
python3 -I - "$R/r11.jsonl" "$I" <<'PY'; result $? "8 each new kind gives the objects of what its line states, a wrong checksum an error"
import json, sys
objs = [json.loads(l) for l in open(sys.argv[1])]
have = {(o['kind'], o['id']) for o in objs if o.get('value') is not None}
want = {('language-package', 'pip:*/cow-say'), ('language-package', 'npm:*/cowsay'), ('flatpak', '*/io.mpv.Mpv/*'),
        ('file', '/home/user/bin/nvim'), ('file', '/home/user/bin/hello'), ('container', 'u/image/' + sys.argv[2]),
        ('unit', 'user/*/cases-tick.timer'), ('unit', 'user/*/cases-tick.service'), ('dir', '/home/user/game')}
errs = [o for o in objs if o['kind'] == 'error']
ok = want <= have and len(errs) == 1 and 'sha256' in errs[0]['error']
nv = next(o for o in objs if o['id'] == '/home/user/bin/nvim')
ok = ok and 'sha256' in (nv.get('underived_fields') or {}) and nv['value'].get('mode') == '0755'
print('missing:', sorted(want - have), 'errors:', [e['error'] for e in errs])
sys.exit(0 if ok else 1)
PY

note "9. a component shipped by the release itself (packages/ beside components.txt) and a file line with UID:GID"
R9="$W/rel9"; mkdir -p "$R9/packages" "$R9/pkg/DEBIAN" "$R9/pkg/etc/cases9" "$W/decl9"
printf 'Package: cases-runtime9\nVersion: 9.0\nArchitecture: all\nMaintainer: case party <cases@invalid>\nDescription: test\n' > "$R9/pkg/DEBIAN/control"
printf 'default\n' > "$R9/pkg/etc/cases9/default.conf"
dpkg-deb --root-owner-group -b "$R9/pkg" "$R9/packages/cases-runtime9_9.0_all.deb" >/dev/null
sha256sum "$R9/packages/cases-runtime9_9.0_all.deb" | cut -d' ' -f1 > "$R9/packages/cases-runtime9_9.0_all.deb.sha256"
printf 'cases-runtime9=9.0\n' > "$R9/components.txt"; printf '9.9\n' > "$R9/VERSION"
printf 'mine\n' > "$W/decl9/mine.txt"
printf 'base 9.9\nsnapshot 20261123T000000Z\nfile /home/user/mine.txt 0644 1000:1000 %s mine.txt\n' "$(sha256sum "$W/decl9/mine.txt" | cut -d' ' -f1)" > "$W/decl9/declaration.conf"
$DERIVE --declaration "$W/decl9/declaration.conf" --components "$R9/components.txt" --cache "$W/cache9" --out "$R/r9.jsonl"; rc=$?
echo "derive exit status $rc"
python3 -I - "$R/r9.jsonl" <<'PY'; result $? "9 the release's own package derived from packages/, the stated owner derived"
import json, sys
objs = {(o['kind'], o['id']): o for o in map(json.loads, open(sys.argv[1]))}
pk = objs.get(('package', 'cases-runtime9:all'))
f = objs.get(('file', '/etc/cases9/default.conf'))
mine = objs.get(('file', '/home/user/mine.txt'))
ok = bool(pk and pk['value'] and pk['value']['url'].startswith('release:packages/') and f and f.get('value')
          and mine and mine['value'].get('uid') == 1000 and mine['value'].get('gid') == 1000
          and not mine.get('underived_fields'))
print('package', bool(pk and pk.get('value')), 'file of it', bool(f and f.get('value')), 'owner', mine and mine.get('value'))
sys.exit(0 if ok else 1)
PY

note "10. reader overrides of the release's own component (build/INTERFACE.md revision 29; builder's entry 49)"
# In the T2 base derivation (7a): for every record of /usr/lib/confos/reader-overrides/manifest.json of the
# component confos-code-readers whose package is a component of the lock, the target is derived with the mode and
# raw SHA256 of the record; for a record whose package is not selected, the target is not taken from the record.
python3 -I selftest/check-overrides.py "$R/base.jsonl" published; result $? "10 targets of selected packages derived from the override manifest"

note "summary"
cat "$R/steps.txt"
if [ $STATUS -eq 0 ]; then echo "SELFTEST derive: PASS"; else echo "SELFTEST derive: FAIL"; fi
exit $STATUS
