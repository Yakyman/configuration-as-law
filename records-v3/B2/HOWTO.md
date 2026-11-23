# Stand operation

Run the commands below **on the VM server**, from the laboratory root into the retained testbed directory. No host sudo is used. Guest sudo belongs to the synthetic `stand` account and grants only declaration frontends, recorded in `sudo:stand`. The lab `--root` option uses a separate host-held SSH credential; it is external fixture/operator access and is never an ordinary-user bypass test. This is a partial testbed; read [STAND.md](STAND.md) before interpreting observations.

```sh
cd stand/round-4
```

## Create, run, and destroy

```sh
python3 lab.py new example stand
printf 'run\t/usr/bin/cat\t/etc/os-release\n' | python3 lab.py run example
printf 'broker\tstand-verify\n' | python3 lab.py run example
printf '%s\n' 'id' 'stand-verify' | python3 lab.py run example --root
python3 lab.py stop example
python3 lab.py start example
python3 lab.py kill example
python3 lab.py start example
python3 lab.py destroy example
```

An ordinary session reads one tab-delimited request: `run<TAB>PATH` or `broker<TAB>TOOL<TAB>ARG...`. Data-tool requests may include separately tab-delimited value arguments. The host's `printf` above supplies actual tabs. Spaces are literal characters within a field. No quoting, expansion, pipelines, redirects, shell functions or command substitutions are interpreted in the guest interface. A new request requires a new `lab.py run` call. Subsequent stdin belongs to a data tool; sealed recorded programs and scripts receive empty stdin and accept no caller arguments.

The `broker` action invokes the named declaration frontend through the account's restricted sudo grant. Free text such as `sudo -n sh` is refused; it is not guest shell syntax. `--root` explicitly selects external operator fixture access and accepts shell scripts. It does not represent the ordinary account's granted right.

`kill` is the hard power cut; `stop` asks for graceful shutdown. `start` waits for SSH **and completed declaration replay**. The SSH listener can start before replay because its listening endpoint is itself verified. A requisite PAM account check prevents both ordinary and operator login sessions until replay writes `/run/stand-ready`; the ordinary launcher checks that marker too. Getty, logind and user-session services require replay. A replay failure leaves entry closed. The wrapper refuses an unsafe VM name or unsupported system name. `new` creates a clean independent overlay of the read-only base and starts it. `list` reports retained VMs. Destroy disposable VMs after use.

## Apply a complete declaration

Create a fresh example VM. This operator fixture copies the complete factory declaration and adds the supplied development program's complete line:

```sh
python3 lab.py new example stand
python3 lab.py run example --root <<'GUEST'
set -eu
cp -a /etc/stand/factory /var/lib/stand/example-declaration
cat /usr/local/share/stand/dev/worker-1.json >> /var/lib/stand/example-declaration/machine.jsonl
stand-apply /var/lib/stand/example-declaration
stand-verify
GUEST
```

Success is printed as `SUCCESS <generation-sha256>` and has exit status 0. A rejected application returns nonzero; a separate worker performs application under a supervisor. Failed or stalled workers are killed and the previous durable declaration is reactivated and verified. An independent systemd timer recovers an abandoned supervisor. General recovery failure and arbitrary device effects remain unproved; read BUILD-3.md. The selected directory is `/var/lib/stand/current`; `/var/lib/stand/last-success.json` is the authoritative durable local success report. Stdout forwards that record. On crash, replay selects the reported generation and uses the pending candidate as the possible prior live state, removing candidate-only contributions. Pending state never overrides a newer success report.

Ordinary installation, update, native launch and removal use separate requests. Run this example on a fresh VM, or remove the development line installed above before its install step:

```sh
printf 'broker\tstand-pkg\tinstall\t/usr/local/share/stand/dev/worker-1.json\n' | python3 lab.py run example
printf 'run\t/opt/stand/pkgs/dev-worker/bin/worker\n' | python3 lab.py run example
printf 'broker\tstand-pkg\tupdate\t/usr/local/share/stand/dev/worker-2.json\n' | python3 lab.py run example
printf 'run\t/opt/stand/pkgs/dev-worker/bin/worker\n' | python3 lab.py run example
printf 'broker\tstand-pkg\tremove\tdev-worker\n' | python3 lab.py run example
```

The document writer accepts exactly one destination path. After the request's first newline, all remaining stdin bytes replace the document verbatim until EOF. The launcher invokes recorded `/usr/bin/dd` with fixed `of=PATH` and `status=none`; extra arguments and user-selected options are refused. Display the result with `cat`. This creates a plain document and an HTML document, then displays the HTML with the browser's fixed dump/configuration options:

```sh
printf 'run\t/usr/bin/dd\t/home/stand/document.txt\nA document\n' | python3 lab.py run example
printf 'run\t/usr/bin/cat\t/home/stand/document.txt\n' | python3 lab.py run example
printf 'run\t/usr/bin/dd\t/home/stand/page.html\n<html><body>Browser content</body></html>\n' | python3 lab.py run example
printf 'run\t/usr/bin/w3m\t/home/stand/page.html\n' | python3 lab.py run example
```

The headless editor is `/usr/bin/red`, launched with fixed `--restricted --script` options and one document basename in the ordinary home directory. It supports line editing and save commands; shell escapes and reads from commands refuse. For example, `printf 'run\t/usr/bin/red\tdocument.txt\n1c\nEdited document\n.\nw\nq\n' | python3 lab.py run example` replaces the first line and saves. Whole-document replacement remains available through the literal writer. The supplied text browser does not execute webpage JavaScript. Generic interpreter sessions, host JIT execution and arbitrary executable editor/project settings are unavailable.

## Declare and run a script

This external operator fixture creates a complete candidate line in the ordinary account's work directory. It does not execute the candidate script. The ordinary account then admits the line through the broker and runs its declared entrypoint:

```sh
python3 lab.py run example --root <<'GUEST'
set -eu
/usr/bin/python3 -I - <<'SCRIPT'
import base64, hashlib, json, os, pathlib
content = b"print('RECORDED_OK')\n"
path = '/opt/stand/pkgs/personal-script/hello.py'
row = {
    'id': 'personal-script', 'type': 'code', 'managed': True,
    'version': '1', 'source': 'local:hello.py',
    'files': [{
        'path': path, 'kind': 'file', 'mode': 420, 'uid': 0, 'gid': 0,
        'sha256': hashlib.sha256(content).hexdigest(),
        'content_b64': base64.b64encode(content).decode()
    }],
    'entrypoints': [{'path': path, 'interpreter': '/usr/bin/python3.13'}]
}
candidate = pathlib.Path('/home/stand/personal-script.json')
candidate.write_text(json.dumps(row) + '\n')
os.chown(candidate, 1000, 1000)
SCRIPT
GUEST
printf 'broker\tstand-line\tadd\t/home/stand/personal-script.json\n' | python3 lab.py run example
printf 'run\t/opt/stand/pkgs/personal-script/hello.py\n' | python3 lab.py run example
printf 'broker\tstand-line\tremove\tpersonal-script\n' | python3 lab.py run example
```

The expected script output is `RECORDED_OK`. Its interpreter and script must be recorded immutable files. The runner checks their hashes, supplies fixed interpreter options and environment, and supplies neither caller arguments nor input code. Scripts see the declaration-derived immutable filesystem snapshot at `/var/lib/stand/code-root`, with exact membership checked by verification, further restricted by Landlock. They cannot read mutable documents, project files, imports or settings outside that snapshot. Editing a script requires a new declaration application before running the new bytes. Data tools use a separate domain to retain ordinary document access.

AppArmor gates executable files and mappings. The inherited syscall filter refuses executable anonymous memory, writable/executable transitions, executable memory files, process injection and restricted IPC. Managed services use the same sealed boundary: the generated override starts a fixed privileged setup program in the manager-owned service cgroup, enters the declared profile and snapshot, and drops supplementary groups and identity to UID/GID 1000 before executing the workload. The manager defers no_new_privs to the fixed launcher, which locks it after the drop and clears inheritable, permitted, effective and ambient capabilities; verification checks those runtime values and the enforcing profile. This setup privilege is not a root shell or a root workload grant. Code changes stop managed sockets, timers and services before replacing the closure, revoke ordinary workload holders, then restart candidate jobs. Removal withdraws snapshot names and profiles.

Supported line types, fixed defaults and limits are in STAND.md. [CHANNEL-PATHS.md](CHANNEL-PATHS.md) gives the exact package, base-update, language, application, import/build and user-job paths. The pinned base transition is `apt-get upgrade --stand-catalog ed`; it updates actual root files and dpkg state through the declaration. For saved/prepared radio paths:

```sh
printf 'broker\tnmcli\tadd\t/usr/local/share/stand/dev/wifi.json\n' | python3 lab.py run example
printf 'broker\tbluetoothctl\tadd\t/usr/local/share/stand/dev/bluetooth.json\n' | python3 lab.py run example
```

These save an open Wi-Fi profile and prepare an **unpaired** Bluetooth profile. Changing state to `connected`/`paired` invokes the hardware backend; those operations are not tested on hardware. A prepared profile is not a successful pairing.

## Cut power at the observed success marker

The ordinary `kill`/`start` commands above are manual cuts. The following driver performs three adds, three changes and three removals of the development fixture, killing QEMU immediately when it receives each success marker. It records the marker-to-signal delay, requires the booted selected generation to equal the reported generation, then verifies every line. These are development fixtures, not the published check inputs. The independent boot-admission test delays replay and attempts both kinds of SSH login before readiness.

```sh
python3 lab.py new cut-example stand
python3 build/round3-cut.py cut-example > raw/manual-powercut.log 2>&1
python3 lab.py destroy cut-example
```

## Compare independent clean instances

Create two overlays, apply the byte-identical fixture declaration in each, collect actual observations, and compare with the implementation of `stand-compare`:

```sh
python3 lab.py new compare-a stand
python3 lab.py new compare-b stand
for vm in compare-a compare-b; do
  python3 lab.py run "$vm" --root <<'GUEST'
set -eu
cp -a /etc/stand/factory /var/lib/stand/comparison
cat /usr/local/share/stand/dev/worker-1.json >> /var/lib/stand/comparison/machine.jsonl
stand-apply /var/lib/stand/comparison
stand-compare --snapshot /var/lib/stand/snapshot.json
GUEST
  python3 lab.py copy-out "$vm" /var/lib/stand/snapshot.json "raw/$vm"
done
python3 - <<'PY'
import base64,pathlib,subprocess
script='set -eu\n'
for name in ('compare-a','compare-b'):
    data=base64.b64encode(pathlib.Path('raw',name,'snapshot.json').read_bytes()).decode()
    script += "printf '%s' '"+data+"' | base64 -d > /var/lib/stand/"+name+".json\n"
script += 'stand-compare /var/lib/stand/compare-a.json /var/lib/stand/compare-b.json\n'
with open('raw/manual-compare.jsonl','wb') as out:
    subprocess.run(['python3','lab.py','run','compare-a','--root'],input=script.encode(),stdout=out,check=True)
PY
python3 lab.py destroy compare-a
python3 lab.py destroy compare-b
```

Each output row contains both observations; exit 0 means their collected values match. The manual example creates clean disks from one image. BC3 additionally builds two images independently from the pinned source and recipe, using the same explicit package-cache and laboratory key inputs, then compares their complete declaration bytes and observations. Invoke `python3 build/round4-driver.py rebuilt --regressions --peer-root ../round-4-peer` after both builds; evidence is under `raw/round-4/rebuilt/`. Do not substitute another overlay for the second recipe execution.

## Rebuild the image from scratch

Copy all files of `B2/build/` into this directory's `build/` before rebuilding. Required server programs are Python, QEMU/KVM, cloud-localds, ssh/scp, curl, flock, ssh-keygen and a user systemd manager. Keep `downloads/packages/*.deb` and (not published: external working record): the recipe checks every cached input before installing it. The matching published manifest is `build/packages.sha256`. A first build without that cache resolves repository packages and freezes a new cache; it cannot promise this build's exact package set.

Remove all disposable instances first; the recipe refuses to replace a base with existing VM directories. The driver must finish and destroy its disposable VMs before rebuilding. For an existing base use `--replace`; omit that flag when no base exists. Long-running VM processes belong to user services and hold a shared slot lock.

```sh
python3 lab.py list
# Destroy each disposable VM listed, then:
systemd-run --user --unit=stand-rebuild --collect \
  --property=MemoryMax=1G --property=CPUQuota=100% \
  --property="StandardOutput=append:$PWD/raw/rebuild-console.log" \
  --property="StandardError=append:$PWD/raw/rebuild-console.log" \
  /usr/bin/python3 "$PWD/build/build.py" --server --replace
systemctl --user status stand-rebuild.service
```

The round-4 recipe retains its image at `round-4/base/stand.qcow2`, relative to the original stand directory; an already-running earlier-round VM keeps its old backing image. The recipe downloads and verifies the pinned cloud input, creates a fresh builder disk, installs cached packages, deploys the new implementation, captures/applies the factory, stops the guest, converts to one standalone `base/stand.qcow2`, and removes source/seed/builder disks. Logs are in `raw/recipe.log`; the image's own guest key remains server-local under `keys/`. The public example declaration contains only its public key.

Bootstrap fixes `SOURCE_DATE_EPOCH=1794787200` (the pinned cloud-source date, 2026-11-16 00:00 UTC) before package hooks run, so mkinitramfs uses its reproducible archive/compression mode. The recipe prints complete factory and initramfs hashes before freezing the image; compare these across independent builds before running the full suite. The first round-4 comparison exposed a differing generated initramfs, preserved in [rebuild-attempt-1](raw/round-4/rebuild-attempt-1); [build-factory-comparison.json](raw/round-4/build-factory-comparison.json) records identical hashes after the correction.

The first stage of the complete round suite is `python3 build/round4-driver.py rebuilt --regressions --peer-root ../round-4-peer`. It runs all four BC4 suites, then BC3, its inventory and nine-cut tests, the entire original development suite and BC1/BC2 on fresh overlays. The phase name is single-use. Both build roots must contain independent completed builds of the same final recipe. To prepare the second root before building, copy `build/`, the verified `downloads/packages/` and (not published: external working record), and `keys/` into `../round-4-peer/`; run its `build/build.py --server` under its own user service exactly as above. Never copy the finished image as a substitute. Review both complete recipe logs and the comparison result.

After that first stage succeeds, assembly and the combined-declaration comparison are mandatory. Run all three commands in order under a user service for a sustained validation run:

```sh
python3 build/round4-driver.py rebuilt --regressions --peer-root ../round-4-peer
python3 build/assemble-channel-examples.py raw/round-4/rebuilt channel-example
python3 build/combined-selftest.py combined channel-example/combined --peer-root ../round-4-peer --reboot
```

The assembly reads exact successful exports, carries the updated factory rows and manifests, and produces 19 additional channel/ordinary rows plus the complete replayable declaration. The last command applies identical bytes on fresh guests of the two independent builds, launches every channel, verifies scheduled execution, reboots and verifies again, and invokes installed `stand-compare` for every row. Both final summaries must report `suite_exit:0`; the first-stage summary alone does not establish new-channel coexistence or comparison. `channel-example/` is a fresh output directory; copy its factory, channels, combined and provenance artifacts into the published `B2/example/` layout described by CHANNEL-PATHS.

All created VMs are destroyed at driver exit. Omitting `--regressions` is only for channel integration debugging. Preserve failed logs and record the implementation correction before another run. The original development suite remains available as `python3 build/development.py`.

## Inventory and test-only failure settings

```sh
printf 'broker\tstand-inventory\n' | python3 lab.py run example > raw/inventory.jsonl
```

The independent census prints one JSON object per observed object followed by a summary. Exact matching lines are listed in `lines`; `unrecorded`, `mismatch` and `unknown` never count as covered. Exit 1 indicates uncovered candidates or mismatches, exit 2 unresolved coverage. This finite implementation does not certify universal P1: its summary explicitly reports `complete:false` and `p1:"?"`. `stand-verify` answers line readback; inventory adds the separate extra-object census. See `INVENTORY-3.md` for readers and unresolved boundaries.

Only external operator root can create `/run/stand-test.json`, owned by root and not group/world writable. The default worker cancellation time is 3300 seconds within a 3600-second total interval. For the shortened test use `{"stall_at":"files","timeout_seconds":8,"deadline_seconds":60}`: restoration must finish before 60 seconds. `{"fail_at":"accounts"}` injects an explicit failure. Supported checkpoints are `prepare`, `frozen`, `quiesce`, `files`, `accounts`, `rules`, `policy`, `jobs`, `readback`, `commit-ready`. The file is never part of an ordinary declaration and must be removed after a test; the helper does this in `finally`. Recovery itself is not yet guaranteed to finish by the total deadline under every failure, so M3.02 remains open. Test settings are absent from the delivered image.

Managed sockets have type `socket`, an exact `stand-*.socket` unit and inline `unit_text`/hash, with explicit enabled/active state. Allowed Socket values are `ListenStream=/run/stand-sockets/NAME.sock`, a declared `Service`, `Accept=no`, `RemoveOnStop=yes`, `SocketMode=0600`; the install target is `sockets.target`. Other activation directives refuse. The service still uses the common sealed workload boundary.

## Broker behavior

`stand-apply`, `stand-line`, `stand-pkg`, `stand-verify`, `stand-inventory`, `stand-compare` and every installed mutating frontend acquire one nonblocking application lock. A competing call returns nonzero with `REFUSED application in progress`. A supported apply emits `SUCCESS` only after every candidate line passes readback. An ordinary snapshot is streamed rather than written with root authority:

```sh
printf 'broker\tstand-compare\t--snapshot\t-\n' | python3 lab.py run example > raw/ordinary-snapshot.json
```

Public package/application/language-manager paths invoke the broker; remaining original administrative backends are root-only. User systemd managers, cron and at are unavailable as scheduling interfaces. A declared user job requires `User=stand` in its submitted unit. `systemctl --user add`, `systemd-run --user add-timer`, and `crontab add` submit the documented exact service/timer/schedule specifications. The generated service override performs only the privileged boundary setup described above; the workload runs as the ordinary account. Required unit defaults are documented in STAND.md and enforced by `guard.py`. Timers may name only a declared managed service. Arbitrary root units, hooks, privilege writes, mutable code ownership and extra activation directives refuse. This is an implementation admission limit, not a new hypothesis rule.

Historical round-3 rebuilt-image evidence is in `B2/raw/round-3/rebuilt/` in the publication folder. Its image SHA-256 was `f12284a70a76d80caf281400a5de002bad6eb6a2d6bd035af8b2f7fe0c35d29b`; `raw/round-3/cleanup-final.json` records its identity after those runs. `BUILD-3.md` records that result, including the preserved host-inspection error and its corrected observation. The current round-4 image SHA-256 is `6626fded301318907dc841d6dc5118e2eea36d075d2d1824f6a4f289f38e7fc1`; both clean rebuilds and their exact source hashes are recorded in [final-build-provenance.json](raw/round-4/final-build-provenance.json).

Round-4 package inputs also include the checksummed language archives, exact system-update artifacts and AppImage runtime in `downloads/language/`, `downloads/system/`, and `downloads/channels/`. Copy those verified caches when preparing the independent root. The recipe generates native-wheel and application-format development fixtures from its exact base inputs before capture. Channel imports never run package hooks or an AppImage runtime. See [CHANNEL-PATHS.md](CHANNEL-PATHS.md) for the complete emitted rows and combined declaration.
