import ast,hashlib,json,pathlib
P=pathlib.Path
d=json.loads(P('B2/build/bc3-fixtures.json').read_text())
source=P('B2/build/bc3-selftest.py').read_text();tree=ast.parse(source)
ordinary=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='ordinary_work')
command=next(ast.literal_eval(n.value) for n in ast.walk(ordinary) if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='command' for x in n.targets))
head='''# Supplement 1, step 5: frozen second-party cases

Final image SHA-256: `PENDING_FINAL_IMAGE_SHA256`
Final complete declaration SHA-256: `PENDING_FINAL_DECLARATION_SHA256`

Recorded 2026-11-23 UTC. **DRAFT — not sealed and not permission to begin the
second-party attempts.** The builder must replace both placeholders and seal the
image, declaration bundle, controller, fixture manifest and this document in the
public records before any second-party attempt. A local working-tree file is not
by itself evidence of that public commitment. After that commitment none of these
inputs or commands changes. Current publication is pending; repository metadata
is unavailable to this working copy.

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
printf '<html><body>BC3 NETWORK PAGE</body></html>\\n' > raw/round-3/network/index.html
systemd-run --user --collect --unit=bc3-case-network --property=WorkingDirectory="$PWD" python3 -m http.server 18753 --bind 127.0.0.1 --directory raw/round-3/network
```

The guest reaches that host server through its virtual Ethernet interface at
`http://10.0.2.2:18753/index.html`. This is an actual network TCP/HTTP connection.
Stop the service only after the ordinary-work case has finished:

```sh
systemctl --user stop bc3-case-network.service
```

## Replay every case on its own fresh copy

Run the following sequence separately for each of the seventeen IDs listed below.
Choose its listed number for `bc3_case_number` and its exact ID for `bc3_case_id`.
The root controller invokes each tested ordinary command as the ordinary account
through `stand-shell`; only the native account operation intentionally runs as
root. Do not run the displayed raw commands a second time after the controller:
they describe the single attempt already performed by it.

```sh
bc3_case_number=01
bc3_case_id=SAVED-SCRIPT
bc3_vm="bc3-peer-$bc3_case_number"
python3 lab.py new "$bc3_vm" stand
printf 'python3 -B /usr/local/lib/stand/bc3-selftest.py --case %s\\n' "$bc3_case_id" | python3 lab.py run "$bc3_vm" --root > "raw/round-3/second-party/$bc3_case_number.jsonl" 2> "raw/round-3/second-party/$bc3_case_number.stderr"
bc3_case_status=$?
printf '%s\\n' "$bc3_case_status" > "raw/round-3/second-party/$bc3_case_number.exit"
python3 lab.py copy-out "$bc3_vm" /var/lib/stand/bc3-evidence "raw/round-3/second-party/$bc3_case_number-evidence"
python3 lab.py destroy "$bc3_vm"
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
paths and SHA-256. The export preserves the corresponding basenames. Verify each
referenced file digest. Snapshots contain the main declaration plus all filesystem
primary texts and successful-generation identities; no command log is substituted
for them. Keep all stdout/stderr, failures, audit events and exported snapshots.

The following commands are literal original inputs, including their quoting,
trailing spaces and supplemental temporary directory. Direct cases have the
original controller's working directory applied separately. Their original
command strings are also exact in the fixture manifest.
'''
out=[head]
for i,c in enumerate(d['cases'],1):
 out.append(f"\n## {i:02d}. {c['id']}\n\nWorking directory: `{c['cwd']}`. Marker: `{c['marker']}`.\n\nAttempt command:\n\n```sh\n{c['command']}\n```\n\nPermitted command, after exact source coverage is verified:\n\n```sh\n{c['command']}\n```\n\n")
 for path in c['files']:
  f=next(f for f in d['files'] if f['path']==path)
  out.append(f"Source `{path}`: {f['bytes']} bytes; mode `{f['mode']:04o}`; SHA-256 `{f['sha256']}`. Base64: `{f['content_b64']}`.\n\n")
 out.append('Setup and observation: run the common replay sequence with this case ID. ')
 if c['inline_writes']:out.append('The attempt itself writes the source using the original command; the permitted command repeats that write, which must succeed and appear in the audit.\n')
 else:out.append('The controller creates the listed source with the ordinary account before the attempt and verifies exact bytes.\n')
 if c['id']=='DISPATCHER-SAVED':out.append('The controller first writes the original complete dispatcher row to `/tmp/v4-extra-7z89hz2f/dispatcher.json` and executes `stand-pkg install /tmp/v4-extra-7z89hz2f/dispatcher.json`, as in the original setup. Its exact row is in the fixture manifest; installation failure fails setup.\n')
out.append('''
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
printf "PERSONAL_SCRIPT_OK:%s\\n" "$1"
```

The complete personal row and its exact path/mode/hash are constructed visibly in
the frozen controller's `ordinary_work` function. It is an own script recorded by
`stand-pkg` before it runs. The complete one-session shell command is:

```sh
'''+command+'''```

Observe exit 0, all six expected outputs (`TWO WORDS`,
`PERSONAL_SCRIPT_OK:ordinary argument`, `Hello, world!`, `BC3 NETWORK PAGE`,
`Edited document`, `BC3_ORDINARY_COMPLETE`), and exact final document bytes
`Edited document\\n`. The package manager must install the catalog program, the
script must have its declared bytes, the HTTP page must be fetched over the guest
network and opened by the browser, and the document must be created then edited.
All occur in one shell session on the same fresh image. Preserve the declaration
snapshots and filesystem audit evidence for the full operation.

## Input identities to seal

The following source hashes describe this draft and must be recomputed if the
builder changes either source before final sealing. They must match the installed
image before second-party execution; they must not be silently updated afterwards.

''')
for p in ['B2/build/bc3-selftest.py','B2/build/bc3-fixtures.json']:
 out.append(f"- `{p}`: `{hashlib.sha256(P(p).read_bytes()).hexdigest()}`\n")
P('B2/CASES-5.md').write_text(''.join(out))
