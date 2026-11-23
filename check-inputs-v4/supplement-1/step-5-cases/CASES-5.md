# Supplement 1, step 5: frozen second-party cases

Final image SHA-256: `5641c3c34e08dba60ae7f97511fae33d4dde48dba0ef5d93db93ab6faeb3cb79`
Final complete declaration SHA-256: `4fd6f7acbc4e9d110dbd3513b4b42aace2b775d99f9f90341f86fb64e33bda57`

Recorded 2026-11-23 UTC. **INPUTS FIXED — PUBLIC COMMITMENT PENDING.**
These image, declaration, source and command identities are locally frozen in
`raw/round-3/inputs-seal.json`. They must be committed to the public records before
any second-party attempt. This local seal is not evidence of that publication.
No case may start until the publication record identifies this unchanged seal.
The available working copy has empty read-only repository metadata and no supplied
public destination; publication requires the records operator. None of these
inputs or commands may change after that commitment.

The complete declaration identity above covers the designated primary declaration
and all five filesystem declarations, not merely machine.jsonl. The sealed bundle
and its identity manifest accompany the final image in the build report. Verify
those recorded hashes before starting. A mismatch means do not run the cases.

## Requirements and fixed host setup

Use the retained server laboratory directory `VMs/cal-1123/stand/`, relative to
the server account's initial directory. It contains `lab.py`, `base/stand.qcow2`,
`base/stand.json` and the existing laboratory keys. The base image is read-only;
`lab.py new NAME stand` creates a new disposable overlay and boots it under a
shared slot lock. No host sudo is needed. The controller and fixture manifest
are installed at `/usr/local/lib/stand/bc3-selftest.py` and
`/usr/local/lib/stand/bc3-fixtures.json` in the image.

The exact fixture manifest is [bc3-fixtures.json](build/bc3-fixtures.json).
It contains all fifteen original commands, their working directories, every
source's base64 bytes, byte count, mode and SHA-256, the exact account argv, the
recorded dispatcher's complete declaration row, and original evidence paths.
The standalone controller is [bc3-selftest.py](build/bc3-selftest.py).

Start the fixed network fixture once on the host:

```sh
cd VMs/cal-1123/stand
mkdir -p raw/round-3/network raw/round-3/second-party
printf '<html><body>BC3 NETWORK PAGE</body></html>\n' > raw/round-3/network/index.html
systemd-run --user --collect --unit=bc3-case-network --property=WorkingDirectory="$PWD" python3 -m http.server 18753 --bind 127.0.0.1 --directory raw/round-3/network
```

The guest reaches that host server through its virtual Ethernet interface at
`http://10.0.2.2:18753/index.html`. This is an actual network TCP/HTTP connection.
Before starting any case, verify this service is active and serves the exact page:

```sh
systemctl --user is-active bc3-case-network.service
curl -fsS http://127.0.0.1:18753/index.html
```

These are fixture-readiness checks, not case attempts. If the port is occupied or
the fixture is unavailable, resolve that setup failure before starting the cases.
Stop the service only after the ordinary-work case has finished:

```sh
systemctl --user stop bc3-case-network.service
```

## Replay every case on its own fresh copy

Run the following sequence separately for each of the seventeen IDs listed below.
Choose its listed number for `bc3_case_number` and its exact ID for `bc3_case_id`.
The root controller invokes each tested ordinary command as the ordinary account
through `stand-shell`; only the native account operation intentionally runs as
root. The controller deliberately labels its summary `builder self-test only`
and `hypothesis_outcome: "?"` even when invoked by the second party: those fixed
labels do not determine the independently reviewed case outcome. Do not run the displayed raw commands a second time after the controller:
they describe the single attempt already performed by it.

```sh
(
bc3_case_number=01
bc3_case_id=SAVED-SCRIPT
bc3_vm="bc3-peer-$bc3_case_number"
if test -e "raw/round-3/second-party/$bc3_case_number.jsonl"; then
    printf 'Case output already exists; do not repeat the attempt.\n' >&2
    exit 1
fi
python3 lab.py new "$bc3_vm" stand || exit 1
if printf 'python3 -B /usr/local/lib/stand/bc3-selftest.py --case %s\n' "$bc3_case_id" | python3 lab.py run "$bc3_vm" --root > "raw/round-3/second-party/$bc3_case_number.jsonl" 2> "raw/round-3/second-party/$bc3_case_number.stderr"; then
    bc3_case_status=0
else
    bc3_case_status=$?
fi
printf '%s\n' "$bc3_case_status" > "raw/round-3/second-party/$bc3_case_number.exit"
if ! python3 lab.py copy-out "$bc3_vm" /var/lib/stand/bc3-evidence "raw/round-3/second-party/$bc3_case_number-evidence"; then
    printf 'Evidence export failed; retain the failure in the record.\n' >&2
fi
python3 lab.py destroy "$bc3_vm"
)
```

Record errors and still export evidence and destroy the disposable VM. Do not
retry a failed case. All second-party case attempts occur once on the sealed
image. Builder development observations are separate. The second party performs;
a further party reviews the observations. Controller success is not independent
acceptance of the mechanism or of the hypothesis.

## What must be observed

Each saved-code case has one attempt followed by one permitted action in the same
fresh copy. The controller writes fixtures through ordinary commands, using exact
bytes from the manifest. In this image, saving those bytes is itself routed through
the prospective declaration filesystem, so it may record them before the attempt.
This is the explicitly allowed automatic-recording branch, not a claim that a
marker was suppressed. It must preserve the same code and route.

Observe `fixture_result`, `attempt_result`, `case_result` and the final `summary`.
For a refusal, the effect must be absent, an actual policy refusal must be present,
and the subsequent permitted action must work. For automatic recording, the exact
saved source must have a covering path/inode/hash requirement in the designated
filesystem declaration, with a matching successful generation report. The source
must be recorded before exposure/use by the mechanism. A matching hash after the
fact or the marker alone does not establish this ordering. Audit changes and the
reviewed prospective publication code supply the additional evidence. Inline
write+execute cases also require a successful source write audit and no writer
error; reading an old file after a failed write does not pass.

Before the permitted command, `coverage` must already show exact source coverage.
The same literal command then succeeds with the expected marker, and exact coverage
still holds. The audit and immutable generation success reports must agree.
Full snapshots are in `bc3-evidence/snapshots/<sha>.json`; JSONL gives their guest
paths and SHA-256. The exported path is `raw/round-3/second-party/NN-evidence/bc3-evidence/snapshots/<sha>.json`,
where `NN` is the case number. Verify each referenced file digest. Snapshots contain the main declaration plus all filesystem
primary texts and successful-generation identities; no command log is substituted
for them. Keep all stdout/stderr, failures, audit events and exported snapshots.

The following commands are literal original inputs, including their quoting,
trailing spaces and supplemental temporary directory. Direct cases have the
original controller's working directory applied separately. Their original
command strings are also exact in the fixture manifest.

## 01. SAVED-SCRIPT

Working directory: `/home/stand`. Marker: `SAVED_CODE_RAN`.

Attempt command:

```sh
printf 'printf SAVED_CODE_RAN\n' > saved.txt; bash saved.txt
```

Permitted command, after exact source coverage is verified:

```sh
printf 'printf SAVED_CODE_RAN\n' > saved.txt; bash saved.txt
```

Source `/home/stand/saved.txt`: 22 bytes; mode `0644`; SHA-256 `17415ceff55ee272ac1df03cebd32d979e47bc8727836ab76f55a56c8521009d`. Base64: `cHJpbnRmIFNBVkVEX0NPREVfUkFOCg==`.

Setup and observation: run the common replay sequence with this case ID. The attempt itself writes the source using the original command; the permitted command repeats that write, which must succeed and appear in the audit.

## 02. SAVED-PIPE

Working directory: `/home/stand`. Marker: `SAVED_CODE_RAN`.

Attempt command:

```sh
cat saved.txt | bash
```

Permitted command, after exact source coverage is verified:

```sh
cat saved.txt | bash
```

Source `/home/stand/saved.txt`: 22 bytes; mode `0644`; SHA-256 `17415ceff55ee272ac1df03cebd32d979e47bc8727836ab76f55a56c8521009d`. Base64: `cHJpbnRmIFNBVkVEX0NPREVfUkFOCg==`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 03. SAVED-SOURCE

Working directory: `/home/stand`. Marker: `SAVED_CODE_RAN`.

Attempt command:

```sh
source saved.txt
```

Permitted command, after exact source coverage is verified:

```sh
source saved.txt
```

Source `/home/stand/saved.txt`: 22 bytes; mode `0644`; SHA-256 `17415ceff55ee272ac1df03cebd32d979e47bc8727836ab76f55a56c8521009d`. Base64: `cHJpbnRmIFNBVkVEX0NPREVfUkFOCg==`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 04. STARTUP-ENV

Working directory: `/home/stand`. Marker: `SAVED_CODE_RAN`.

Attempt command:

```sh
BASH_ENV="$HOME/saved.txt" bash -c :
```

Permitted command, after exact source coverage is verified:

```sh
BASH_ENV="$HOME/saved.txt" bash -c :
```

Source `/home/stand/saved.txt`: 22 bytes; mode `0644`; SHA-256 `17415ceff55ee272ac1df03cebd32d979e47bc8727836ab76f55a56c8521009d`. Base64: `cHJpbnRmIFNBVkVEX0NPREVfUkFOCg==`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 05. PYTHON-IMPORT

Working directory: `/home/stand`. Marker: `IMPORTED_UNRECORDED`.

Attempt command:

```sh
printf 'print("IMPORTED_UNRECORDED")\n' > loose_module.py; python3 -B -c 'import loose_module'
```

Permitted command, after exact source coverage is verified:

```sh
printf 'print("IMPORTED_UNRECORDED")\n' > loose_module.py; python3 -B -c 'import loose_module'
```

Source `/home/stand/loose_module.py`: 29 bytes; mode `0644`; SHA-256 `7f938b43be066efce524423ea6484377bb4dd1e40fbc217e0cc4b3df9072c045`. Base64: `cHJpbnQoIklNUE9SVEVEX1VOUkVDT1JERUQiKQo=`.

Setup and observation: run the common replay sequence with this case ID. The attempt itself writes the source using the original command; the permitted command repeats that write, which must succeed and appear in the audit.

## 06. PICKLE-CODE

Working directory: `/home/stand`. Marker: `PICKLE_EXECUTED`.

Attempt command:

```sh
python3 -B -c 'import pickle; p=b"cbuiltins\nprint\n(S\x27PICKLE_EXECUTED\x27\ntR."; open("serialized","wb").write(p); pickle.load(open("serialized","rb"))' 
```

Permitted command, after exact source coverage is verified:

```sh
python3 -B -c 'import pickle; p=b"cbuiltins\nprint\n(S\x27PICKLE_EXECUTED\x27\ntR."; open("serialized","wb").write(p); pickle.load(open("serialized","rb"))' 
```

Source `/home/stand/serialized`: 39 bytes; mode `0644`; SHA-256 `b26a48df0be6ba31e0b3db37a9a5ae0289f337bffd329fbe7ad72aa3390aaaa3`. Base64: `Y2J1aWx0aW5zCnByaW50CihTJ1BJQ0tMRV9FWEVDVVRFRCcKdFIu`.

Setup and observation: run the common replay sequence with this case ID. The attempt itself writes the source using the original command; the permitted command repeats that write, which must succeed and appear in the audit.

## 07. DIRECT-REDIRECT-STDIN

Working directory: `/home/stand/v4-direct`. Marker: `SAVED_DIRECT_RAN`.

Attempt command:

```sh
bash < saved.sh
```

Permitted command, after exact source coverage is verified:

```sh
bash < saved.sh
```

Source `/home/stand/v4-direct/saved.sh`: 40 bytes; mode `0755`; SHA-256 `43d50a29262f6b0a31a30fc85806697adb289ad85bd98591fcce61ab7fc5bb2a`. Base64: `IyEvdXNyL2Jpbi9iYXNoCnByaW50ZiBTQVZFRF9ESVJFQ1RfUkFOCg==`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 08. DIRECT-PROC-FD

Working directory: `/home/stand/v4-direct`. Marker: `SAVED_DIRECT_RAN`.

Attempt command:

```sh
exec 3<saved.sh; bash /proc/self/fd/3
```

Permitted command, after exact source coverage is verified:

```sh
exec 3<saved.sh; bash /proc/self/fd/3
```

Source `/home/stand/v4-direct/saved.sh`: 40 bytes; mode `0755`; SHA-256 `43d50a29262f6b0a31a30fc85806697adb289ad85bd98591fcce61ab7fc5bb2a`. Base64: `IyEvdXNyL2Jpbi9iYXNoCnByaW50ZiBTQVZFRF9ESVJFQ1RfUkFOCg==`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 09. DIRECT-READ-EXEC

Working directory: `/home/stand/v4-direct`. Marker: `READ_EXEC_RAN`.

Attempt command:

```sh
python3 -B -c 'exec(open("saved.py").read())'
```

Permitted command, after exact source coverage is verified:

```sh
python3 -B -c 'exec(open("saved.py").read())'
```

Source `/home/stand/v4-direct/saved.py`: 23 bytes; mode `0644`; SHA-256 `85ff61eb43326de0b088852d16f37bc1bb299afd847569111a2c2f350087999e`. Base64: `cHJpbnQoIlJFQURfRVhFQ19SQU4iKQo=`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 10. DIRECT-AWK-FILE

Working directory: `/home/stand/v4-direct`. Marker: `AWK_FILE_RAN`.

Attempt command:

```sh
awk -f saved.awk
```

Permitted command, after exact source coverage is verified:

```sh
awk -f saved.awk
```

Source `/home/stand/v4-direct/saved.awk`: 31 bytes; mode `0644`; SHA-256 `c6d3872bf43cbf05e2c48b2f496dcea1f5d36ccc7af58d0f125ed45441dc5889`. Base64: `QkVHSU4geyBwcmludCAiQVdLX0ZJTEVfUkFOIiB9Cg==`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 11. DIRECT-SCRIPT-HELPER

Working directory: `/home/stand/v4-direct`. Marker: `SAVED_DIRECT_RAN`.

Attempt command:

```sh
find . -maxdepth 0 -exec bash saved.sh ';'
```

Permitted command, after exact source coverage is verified:

```sh
find . -maxdepth 0 -exec bash saved.sh ';'
```

Source `/home/stand/v4-direct/saved.sh`: 40 bytes; mode `0755`; SHA-256 `43d50a29262f6b0a31a30fc85806697adb289ad85bd98591fcce61ab7fc5bb2a`. Base64: `IyEvdXNyL2Jpbi9iYXNoCnByaW50ZiBTQVZFRF9ESVJFQ1RfUkFOCg==`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 12. RC-STARTUP

Working directory: `/home/stand`. Marker: `SAVED_RC_EXECUTED`.

Attempt command:

```sh
cd /tmp/v4-extra-7z89hz2f && bash --rcfile /tmp/v4-extra-7z89hz2f/startup.rc -i -c :
```

Permitted command, after exact source coverage is verified:

```sh
cd /tmp/v4-extra-7z89hz2f && bash --rcfile /tmp/v4-extra-7z89hz2f/startup.rc -i -c :
```

Source `/tmp/v4-extra-7z89hz2f/startup.rc`: 29 bytes; mode `0600`; SHA-256 `a829afcc91f6bf36347cde073a527ce259b35e1b74d7f4b2ac997445294ea28e`. Base64: `cHJpbnRmICJTQVZFRF9SQ19FWEVDVVRFRFxuIgo=`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 13. EDITOR-SAVED-COMMANDS

Working directory: `/home/stand`. Marker: `SAVED_EDITOR_COMMAND_EXECUTED`.

Attempt command:

```sh
cd /tmp/v4-extra-7z89hz2f && ed -s < /tmp/v4-extra-7z89hz2f/commands.ed
```

Permitted command, after exact source coverage is verified:

```sh
cd /tmp/v4-extra-7z89hz2f && ed -s < /tmp/v4-extra-7z89hz2f/commands.ed
```

Source `/tmp/v4-extra-7z89hz2f/commands.ed`: 44 bytes; mode `0600`; SHA-256 `83f83d4ddda12cb3ec60bdc2cef97c112835dd31900571ad4fc819a6ecb09174`. Base64: `IXByaW50ZiAiU0FWRURfRURJVE9SX0NPTU1BTkRfRVhFQ1VURURcbiIKcQo=`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 14. JIT-SAVED-INPUT

Working directory: `/home/stand`. Marker: `JIT_SAVED_INPUT_EXECUTED 42`.

Attempt command:

```sh
cd /tmp/v4-extra-7z89hz2f && python3 -B -c 'import ctypes,mmap
b=open('"'"'/tmp/v4-extra-7z89hz2f/machine.bytes'"'"',"rb").read()
m=mmap.mmap(-1,4096,prot=mmap.PROT_READ|mmap.PROT_WRITE|mmap.PROT_EXEC)
m.write(b)
f=ctypes.CFUNCTYPE(ctypes.c_int)(ctypes.addressof(ctypes.c_char.from_buffer(m)))
print("JIT_SAVED_INPUT_EXECUTED",f())
'
```

Permitted command, after exact source coverage is verified:

```sh
cd /tmp/v4-extra-7z89hz2f && python3 -B -c 'import ctypes,mmap
b=open('"'"'/tmp/v4-extra-7z89hz2f/machine.bytes'"'"',"rb").read()
m=mmap.mmap(-1,4096,prot=mmap.PROT_READ|mmap.PROT_WRITE|mmap.PROT_EXEC)
m.write(b)
f=ctypes.CFUNCTYPE(ctypes.c_int)(ctypes.addressof(ctypes.c_char.from_buffer(m)))
print("JIT_SAVED_INPUT_EXECUTED",f())
'
```

Source `/tmp/v4-extra-7z89hz2f/machine.bytes`: 6 bytes; mode `0600`; SHA-256 `11db5348e275fb704be582e8005ee7d604f7f17b154d6cc644d240eef29d456a`. Base64: `uCoAAADD`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.

## 15. DISPATCHER-SAVED

Working directory: `/home/stand`. Marker: `DISPATCHER_SAVED_EXECUTED`.

Attempt command:

```sh
/opt/stand/pkgs/v4-extra-dispatch/bin/dispatch --file /tmp/v4-extra-7z89hz2f/instructions.ops
```

Permitted command, after exact source coverage is verified:

```sh
/opt/stand/pkgs/v4-extra-dispatch/bin/dispatch --file /tmp/v4-extra-7z89hz2f/instructions.ops
```

Source `/tmp/v4-extra-7z89hz2f/instructions.ops`: 32 bytes; mode `0600`; SHA-256 `08a7984a7805319b3b105b98c2da1d9efdfdf841c166266b74b8a803923be3ef`. Base64: `UFJJTlQgRElTUEFUQ0hFUl9TQVZFRF9FWEVDVVRFRAo=`.

Setup and observation: run the common replay sequence with this case ID. The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.
The controller first writes the original complete dispatcher row to `/tmp/v4-extra-7z89hz2f/dispatcher.json` and executes `stand-pkg install /tmp/v4-extra-7z89hz2f/dispatcher.json`, as in the original setup. Its exact row is in the fixture manifest; installation failure fails setup.

## 16. root-native-account-bypass

Run the common replay sequence with this exact ID. The fresh image must not
already contain `v4raw`. The root attempt and permitted tool action are the same
single native operation, which must both record and apply the requested change:

```sh
/usr/sbin/useradd -M -u 1998 -s /usr/sbin/nologin v4raw
```

Observe exit 0 and exactly this account tuple: name `v4raw`, uid 1998, gid 1998,
groups `["v4raw"]`, home `/home/v4raw`, empty GECOS, shell `/usr/sbin/nologin`.
The `/etc` filesystem primary declaration must change and contain an own-line
account row matching every tuple field, as well as the exact account database
requirements. Its successful-generation digest must match. A successful native
command with an unchanged declaration or a mismatching tuple fails. No reset is
needed: destroy the entire disposable copy after exporting its evidence. Do not
use a broker alias in place of the literal native command.

## 17. ordinary-work

Run the common replay sequence with this exact ID while the host HTTP fixture is
running. The controller prepares `/tmp/bc3-personal.json` as an exact declaration
request for the following saved script, then one ordinary shell process performs
all six ordinary activities. Script bytes:

```sh
#!/usr/bin/bash
printf "PERSONAL_SCRIPT_OK:%s\n" "$1"
```

The complete personal row and its exact path/mode/hash are constructed visibly in
the frozen controller's `ordinary_work` function. It is an own script recorded by
`stand-pkg` before it runs. The complete one-session shell command is:

```sh
set -e
message='two words'; f() { printf '%s\n' "$1"; }; f "$message" | tr a-z A-Z > document.txt; cat < document.txt
stand-pkg install /tmp/bc3-personal.json
/opt/stand/pkgs/bc3-personal/bin/personal 'ordinary argument'
apt install hello=2.10-5
/opt/stand/pkgs/repository-hello/usr/bin/hello
curl -fsS http://10.0.2.2:18753/index.html > page.html
w3m -dump -config /etc/stand/w3m.conf http://10.0.2.2:18753/index.html
printf '1c\nEdited document\n.\nw\nq\n' | ed -s document.txt
cat document.txt
printf 'BC3_ORDINARY_COMPLETE\n'
```

Observe exit 0, all six expected outputs (`TWO WORDS`,
`PERSONAL_SCRIPT_OK:ordinary argument`, `Hello, world!`, `BC3 NETWORK PAGE`,
`Edited document`, `BC3_ORDINARY_COMPLETE`), and exact final document bytes
`Edited document\n`. The package manager must install the catalog program, the
script must have its declared bytes, the HTTP page must be fetched over the guest
network and opened by the browser, and the document must be created then edited.
All occur in one shell session on the same fresh image. Preserve the declaration
snapshots and filesystem audit evidence for the full operation.

## Fixed source identities

The following source hashes match the frozen image declaration, as recorded in
`raw/round-3/final-1/installed-source-identities.json`. They must match the installed
image before second-party execution and must not be silently updated afterwards.

- `B2/build/bc3-selftest.py`: `68cf337210fd012fc75e008c09c36af49f1a825a9fc491b500f6003a8412ec97`
- `B2/build/bc3-fixtures.json`: `1277fed54a24d19f04e566e88033fedf73a374be55b13745b8d9b4129c4e4aa1`
