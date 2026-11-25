#!/bin/bash
# Test of derive-radio (the cases beyond the plan, not the frozen set), on the server: (1) derive-radio is what
# tools/make-derive-radio.py writes from the frozen `derive`; (2) the radio lines of the published fixture of the
# given release alone: the four radio objects must be derived and no `error` object may appear; (3) a wrong checksum
# must give one error object; (4) [x2] the line `group xrecgroup 1001` alone: one group object, no error object.
# usage: bash selftest/extra/test-derive-radio.sh SOURCE_TAR   (from the copy of cases/ on the server)
set -u
C=$(cd "$(dirname "$0")/../.." && pwd)
TAR=$1
. "$C/local.env"
T=$HOME/$SERVER_DIR/tmp-extra-radio
rm -rf "$T" && mkdir -p "$T/gen" "$T/dr/ok" "$T/dr/bad" "$T/dr/grp"
fail=0
cp "$C/derive" "$T/gen/derive"
python3 -I "$C/tools/make-derive-radio.py" "$T/gen" > /dev/null
if cmp -s "$T/gen/derive-radio" "$C/derive-radio"; then echo "ok: derive-radio is the program's output"
else echo "FAIL: derive-radio differs from the output of tools/make-derive-radio.py"; fail=1; fi
tar -xzf "$TAR" -C "$T" radio-public-fixture
F=$T/radio-public-fixture
cp "$F/fixture.json" "$F/client.json" "$F/00AA01000000.info" "$F/00AA01010001.info" "$T/dr/ok/"
cp "$F/fixture.json" "$T/dr/bad/"
s() { sha256sum "$F/$1" | cut -c1-64; }
printf '%s\n' "radio-fixture lab $(s fixture.json) fixture.json" "network saved $(s client.json) client.json" \
  "bluetooth-pair 00:AA:01:00:00:00 00:AA:01:01:00:01 $(s 00AA01000000.info) 00AA01000000.info" \
  "bluetooth-pair 00:AA:01:01:00:01 00:AA:01:00:00:00 $(s 00AA01010001.info) 00AA01010001.info" > "$T/dr/ok/declaration.conf"
printf '%s\n' "radio-fixture lab $(printf '0%.0s' $(seq 64)) fixture.json" > "$T/dr/bad/declaration.conf"
for c in ok bad; do
  python3 -I "$C/derive-radio" --declaration "$T/dr/$c" --cache "$T/dr/cache" --out "$T/dr/$c.jsonl" > "$T/dr/$c.log" 2>&1
  echo "$c: exit $?"
  grep -o '"kind": "[a-z-]*", "id": "[^"]*"' "$T/dr/$c.jsonl"
done
n=$(grep -c '"kind": "\(radio-fixture\|network\|bluetooth-pair\)"' "$T/dr/ok.jsonl")
e=$(grep -c '"kind": "error"' "$T/dr/ok.jsonl")
eb=$(grep -c '"kind": "error"' "$T/dr/bad.jsonl")
echo "ok: radio objects $n (want 4), errors $e (want 0); bad: errors $eb (want 1)"
[ "$n" = 4 ] && [ "$e" = 0 ] && [ "$eb" = 1 ] || fail=1
printf '%s\n' "group xrecgroup 1001" > "$T/dr/grp/declaration.conf"
python3 -I "$C/derive-radio" --declaration "$T/dr/grp" --cache "$T/dr/cache" --out "$T/dr/grp.jsonl" > "$T/dr/grp.log" 2>&1
echo "grp: exit $?"
ng=$(grep -c '"id": "xrecgroup", "kind": "group"' "$T/dr/grp.jsonl")
eg=$(grep -c '"kind": "error"' "$T/dr/grp.jsonl")
echo "grp: group objects $ng (want 1), errors $eg (want 0)"
[ "$ng" = 1 ] && [ "$eg" = 0 ] || fail=1
rm -rf "$T"
[ $fail = 0 ] && echo "RESULT: PASS" || echo "RESULT: FAIL"
exit $fail
