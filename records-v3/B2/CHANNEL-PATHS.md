# Declaration paths for the installation channels

This is the command and format reference for assembling the Check 2 declaration. It describes the finite supported paths; it is not a Check 2 result or an acceptance report. Fresh-image outcomes belong to [SELFTEST.md](SELFTEST.md) and [raw/round-4/](raw/round-4).

The exact emitted rows are exported in example/channels/machine.jsonl (not published: outside selected checks and direct evidence), selected by the `id` column below; the complete replayable directory is example/combined/ (not published: external working record). The complete declaration also needs the factory rows and their referenced manifests. An import request or package lock is input to a tool; it is **not** the emitted declaration row. Do not replace exported payloads or hashes with the abbreviated descriptions in this document. The exported artifacts are development inputs for assembling the separate published check.

`example/` is the artifact catalogue. Apply example/factory/ (not published: external working record) for the complete factory declaration or example/combined/ (not published: external working record) for the complete channel example. `example/channels/` contains only the additional rows. The top-level `machine.jsonl` and `base-files.json` retain convenient copies of the factory files; submit a complete leaf directory to `stand-apply`.

## Calling convention

From the retained server build root described in [HOWTO.md](HOWTO.md), create one disposable VM:

```sh
python3 lab.py new channel-demo stand
request() { printf '%s\t' "$@"; printf '\n'; }
```

Pipe each `request` below to `python3 lab.py run channel-demo`. `broker TOOL ...` uses the ordinary account's declared sudo grant. `run PATH` selects an exact recorded launch entry; it does not interpret shell syntax. All examples use the synthetic guest account, not a host account. For an explicit root-frontend repeat, run the same frontend via `python3 lab.py run channel-demo --root`, for example:

```sh
printf '/usr/local/bin/apt-get install hello=2.10-5\n' | python3 lab.py run channel-demo --root
```

Verification and cleanup:

```sh
request broker stand-verify | python3 lab.py run channel-demo
python3 lab.py destroy channel-demo
```

## Exact row identities and input formats

| Channel | Emitted row IDs | Exact input in the image / required state |
|---|---|---|
| Distribution package | `repository:hello` | `/usr/local/share/stand/system/catalog.json`, `installs.hello`: Debian hello 2.10-5, archive SHA256/source, all relocated payload files and exact transitive dependency states referencing factory package lines. |
| Base update | `system:base-state`, with rewritten factory base/package file requirements | Same catalog, `updates.ed.row`: real ed 1.19-1 → 1.21.1-1 state; exact complete package version map, changed file payloads and required absences. The returned whole declaration includes revised factory requirements. |
| pip project | `language:pip:development` | `/usr/local/share/stand/language/pip.lock.json`: project entry, exact python-dateutil 2.9.0.post0 and six 1.17.0 archives and dependency edges. Full lock and archives become required files. |
| Native pip wheel | `language:pip:native-development` | `/usr/local/share/stand/language/pip-native.lock.json`: deterministic stand-native 1.0 wheel containing the exact base CPython `_bz2` extension, complete wheel/hash and recorded entry. The entry requires the module to load from the managed project path. |
| npm project | `language:npm:development` | `/usr/local/share/stand/language/npm.lock.json`: project entry, exact is-odd 3.0.1 and is-number 6.0.0 archives and dependency edges. Full lock and archives become required files. |
| Flatpak | `round4-flatpak` | `/usr/local/share/stand/channels/flatpak.json`: artifact SHA256, exact app/runtime OSTree commits, names, entry and permissions. Full emitted row embeds the artifact and all installed payloads. |
| AppImage | `round4-appimage` | `/usr/local/share/stand/channels/appimage.json`: image SHA256, Type-2 runtime SHA256, SquashFS offset, AppRun entry and permissions. Runtime is not executed during import. |
| OCI image/container | `round4-oci-image`, `round4-oci` | `/usr/local/share/stand/channels/oci.json`: exact manifest digest and archive SHA256; image row owns the layout; container row requires the image row and exact configuration. |
| Direct file import | `import:downloaded` | Download specification described below: exact bytes/version/source, installed into a broker-owned path. The original file remains inert. |
| Recorded source and built result | `source:source-example`, `import:source-example-built` | Source specification below; fixed compiler takes recorded source, writes an inert result and generates its exact import specification. |
| User service | `dev-worker`, `dev-service` | `/usr/local/share/stand/dev/worker-1.json`, `service.json`: exact program payload and unit text/hash; service runs the recorded worker with fixed `--wait`. |
| User timer | `round4-user-timer` | Exact timer text below, with enabled and active requirements and its SHA256. |
| Scheduled command | `schedule:scheduled-example:service`, `schedule:scheduled-example:timer` | Schedule specification below is translated into exact protected service/timer rows. |
| Saved Wi-Fi | `dev-wifi` | `/usr/local/share/stand/dev/wifi.json`: explicit SSID, UUID, autoconnect false, state saved. |
| Bluetooth | `dev-bluetooth` | `/usr/local/share/stand/dev/bluetooth.json`: synthetic adapter/device addresses, name, trusted false, state prepared; this is not a successful pairing. |

To extract an exact emitted line from the record folder, use any ID from the table as the argument. This preserves the exported line bytes:

```sh
python3 - repository:hello <<'PYTHON'
import json,sys
from pathlib import Path
for line in Path('(not published: direct evidence over 2 MB)').read_text().splitlines(keepends=True):
    if json.loads(line)['id'] == sys.argv[1]:
        sys.stdout.write(line)
        break
else:
    raise SystemExit('requested channel row is absent')
PYTHON
```

Both language adapters accept one whole-project lock. Its exact schema is `schema:1`, `channel:"pip"` or `"npm"`, `project`, `packages`, `entry_code`, `entry_sha256`. Every package contains `name`, `version`, `sha256`, `source`, `archive`, and `dependencies`. Archives must be alongside the lock. Entry code is itself recorded. Archive-derived names, versions and dependency edges must agree. Source builds, editable installations, npm links and lifecycle commands refuse; no implicit build backend or install hook runs. Separate admitted code uses the common importer and boundary.

All three application formats require permissions exactly `{"network":false,"devices":false,"host_files":false,"writable_root":false,"extra_arguments":false}`. Supported entries are static native ELF64. Flatpak accepts the recorded app/runtime repository contents; AppImage imports its AppDir; OCI accepts one uncompressed layer. OCI configuration fixes image digest, entrypoint, UID/GID 1000, read-only root, network `none`, and empty mounts/capabilities/hooks. Unsupported formats/options refuse. These are implementation restrictions, not additions to the hypothesis.

## Package and application commands

```sh
request broker apt-get install hello=2.10-5 | python3 lab.py run channel-demo
request run /opt/stand/pkgs/repository-hello/usr/bin/hello | python3 lab.py run channel-demo
request broker apt-get upgrade --stand-catalog ed | python3 lab.py run channel-demo
request run /usr/bin/ed | python3 lab.py run channel-demo

request broker pip install --stand-lock /usr/local/share/stand/language/pip.lock.json | python3 lab.py run channel-demo
request run /opt/stand/pkgs/pip-development/main.py | python3 lab.py run channel-demo
request broker pip install --stand-lock /usr/local/share/stand/language/pip-native.lock.json | python3 lab.py run channel-demo
request run /opt/stand/pkgs/pip-native-development/main.py | python3 lab.py run channel-demo
request broker npm install --stand-lock /usr/local/share/stand/language/npm.lock.json | python3 lab.py run channel-demo
request run /opt/stand/pkgs/npm-development/main.js | python3 lab.py run channel-demo

request broker flatpak install /usr/local/share/stand/channels/flatpak.json | python3 lab.py run channel-demo
request broker flatpak run round4-flatpak | python3 lab.py run channel-demo
request broker stand-appimage install /usr/local/share/stand/channels/appimage.json | python3 lab.py run channel-demo
request broker stand-appimage run round4-appimage | python3 lab.py run channel-demo
request broker podman install /usr/local/share/stand/channels/oci.json | python3 lab.py run channel-demo
request broker podman run round4-oci | python3 lab.py run channel-demo
```

The ordinary launch entries are `/opt/stand/pkgs/round4-flatpak/app/files/bin/probe`, `/opt/stand/pkgs/round4-appimage/AppRun`, and `/opt/stand/pkgs/round4-oci/bin/probe`. Application-manager `run ID` selects these recorded entries; it does not accept arbitrary program arguments. The base update's `ed` launch has recorded fixed `--version` arguments and empty input; document editing uses the separate data tool below.

Removal examples:

```sh
request broker pip remove language:pip:development | python3 lab.py run channel-demo
request broker npm remove language:npm:development | python3 lab.py run channel-demo
request broker flatpak remove round4-flatpak | python3 lab.py run channel-demo
request broker stand-appimage remove round4-appimage | python3 lab.py run channel-demo
request broker podman remove round4-oci | python3 lab.py run channel-demo
request broker podman remove round4-oci-image | python3 lab.py run channel-demo
request broker apt-get remove repository:hello | python3 lab.py run channel-demo
request broker apt-get remove system:base-state | python3 lab.py run channel-demo
```

## Direct download, source and build import

The supplied development exercise in [build/round4-selftest.py](build/round4-selftest.py) serves the exact development worker bytes over local HTTP, retrieves them with ordinary recorded curl, and writes them as inert guest data. The temporary HTTP port is allocated by that test and is not a fixed deployment requirement. Check 2 must freeze its own download URL and content before execution.

To replay the exact exported development import without choosing new bytes, reconstruct its artifact and input specification from the emitted row (from the record folder):

```sh
python3 - <<'PYTHON'
import base64,json
from pathlib import Path
rows=map(json.loads,Path('(not published: direct evidence over 2 MB)').read_text().splitlines())
row=next(r for r in rows if r['id']=='import:downloaded')
f=row['files'][0]
Path('downloaded-program').write_bytes(base64.b64decode(f['content_b64'],validate=True))
Path('download.json').write_text(json.dumps({'id':'downloaded','version':row['version'],'source':row['source'],'sha256':f['sha256'],'path':'/home/stand/downloaded-program'})+'\n')
PYTHON
```

Transfer these two files to the server build root, then send their exact bytes through the ordinary data writer:

```sh
{ printf 'run\t/usr/bin/dd\t/home/stand/downloaded-program\n'; cat downloaded-program; } | python3 lab.py run channel-demo
{ printf 'run\t/usr/bin/dd\t/home/stand/download.json\n'; cat download.json; } | python3 lab.py run channel-demo
```

This reproduces the exact import input; the separate `DOWNLOAD` self-test supplies the actual ordinary HTTP transport observation.

For an existing downloaded file `/home/stand/downloaded-program`, write (not published: external working record) as JSON containing `id:"downloaded"`, `version:"1"`, `source` identifying the frozen download, its exact `sha256`, and `path:"/home/stand/downloaded-program"`. For a script also state the supported fixed `interpreter`; native ELF imports omit it. `sha256` must be computed from the actual file, never substituted with a label. The emitted `import:downloaded` row includes the full content and its required broker-owned destination.

```sh
request run /home/stand/downloaded-program | python3 lab.py run channel-demo
# Expected refusal before import.
request broker stand-import install /home/stand/download.json | python3 lab.py run channel-demo
request run /opt/stand/pkgs/downloaded/bin/program | python3 lab.py run channel-demo
```

To reproduce the supplied recorded-source example, write these literal bytes through the document tool:

```sh
printf 'run\t/usr/bin/dd\t/home/stand/source.c\n#include <stdio.h>\nint main(void){puts("BUILT_SOURCE_OK");return 0;}\n' | python3 lab.py run channel-demo
```

Write the complete source request with the checksum computed from those exact bytes:

```sh
printf 'run\t/usr/bin/dd\t/home/stand/source.json\n%s\n' '{"id":"source-example","version":"1","source":"builder-source:ordinary-c","path":"/home/stand/source.c","sha256":"9f52d7174b89b3b17bf8cee3804fd24330bd832082b03a38cc726df6b0147fed"}' | python3 lab.py run channel-demo
```

The source request has no interpreter. The exact emitted source and import rows are included in the channel export. Build output remains inert until its separate import succeeds:

```sh
request broker stand-import source /home/stand/source.json | python3 lab.py run channel-demo
request broker stand-build build source:source-example | python3 lab.py run channel-demo
request run /home/stand/source-example.built | python3 lab.py run channel-demo
# Expected refusal: compiled output is still inert.
request broker stand-import install /home/stand/source-example.built.json | python3 lab.py run channel-demo
request run /opt/stand/pkgs/source-example-built/bin/program | python3 lab.py run channel-demo
```

`stand-build` produces the exact `.built.json` specification itself. The source, compiler and permitted compiler inputs are recorded; fixed compilation has no caller flags or executable plugins. The resulting import carries the actual compiled content checksum.

## User services, timers and scheduled commands

Create `timer.json` and `schedule.json` using the exact instructions below before submitting their add commands. The program must precede its service, and the service must precede its timer.

```sh
request broker stand-pkg install /usr/local/share/stand/dev/worker-1.json | python3 lab.py run channel-demo
request broker systemctl --user add /usr/local/share/stand/dev/service.json | python3 lab.py run channel-demo
request broker systemd-run --user add-timer /home/stand/timer.json | python3 lab.py run channel-demo
request broker crontab add /home/stand/schedule.json | python3 lab.py run channel-demo
```

`timer.json` is the exported row `round4-user-timer`: type timer, managed true, unit `stand-user-example.timer`, enabled `enabled`, active true, exact `unit_text` below and its computed `unit_sha256`:

```ini
[Unit]
Description=Declared user timer
[Timer]
OnBootSec=1h
OnUnitActiveSec=1h
Unit=stand-development.service
Persistent=false
[Install]
WantedBy=timers.target
```

The trailing newline belongs to `unit_text`. To transfer the exact exported timer row into its ordinary data file (run from the record folder, then send `timer.json` from the server build root):

```sh
python3 - <<'PYTHON' > timer.json
import json
from pathlib import Path
for line in Path('(not published: direct evidence over 2 MB)').read_text().splitlines():
    row=json.loads(line)
    if row['id']=='round4-user-timer':
        print(json.dumps(row,separators=(',',':')))
        break
else:
    raise SystemExit('exact timer export is missing')
PYTHON
{ printf 'run\t/usr/bin/dd\t/home/stand/timer.json\n'; cat timer.json; } | python3 lab.py run channel-demo
```

Create `schedule.json` through the same ordinary document writer:

```sh
printf 'run\t/usr/bin/dd\t/home/stand/schedule.json\n%s\n' '{"id":"scheduled-example","command":"/opt/stand/pkgs/source-example-built/bin/program","on_boot":"1s","interval":"1min"}' | python3 lab.py run channel-demo
```

The schedule request is exactly:

```json
{"id":"scheduled-example","command":"/opt/stand/pkgs/source-example-built/bin/program","on_boot":"1s","interval":"1min"}
```

The source-built program must already be recorded. User jobs are implemented as protected system units whose fixed launcher drops to the ordinary identity before workload execution. Arbitrary user-manager, unit-hook, cron and transient-command paths refuse; they are not alternative installation channels outside the declaration.

## Browser, documents and saved radio state

```sh
printf 'run\t/usr/bin/dd\t/home/stand/document.txt\nFirst document\n' | python3 lab.py run channel-demo
printf 'run\t/usr/bin/red\tdocument.txt\n1c\nEdited document\n.\nw\nq\n' | python3 lab.py run channel-demo
request run /usr/bin/cat /home/stand/document.txt | python3 lab.py run channel-demo
printf 'run\t/usr/bin/dd\t/home/stand/page.html\n<html><body>Ordinary browser works</body></html>\n' | python3 lab.py run channel-demo
request run /usr/bin/w3m /home/stand/page.html | python3 lab.py run channel-demo
request broker nmcli add /usr/local/share/stand/dev/wifi.json | python3 lab.py run channel-demo
request broker bluetoothctl add /usr/local/share/stand/dev/bluetooth.json | python3 lab.py run channel-demo
```

The restricted headless editor changes and saves individual lines; the literal writer also supports whole-document replacement; browser operation is passive text output with fixed configuration and no page-code execution. Their programs/configuration belong to factory rows; the document and page contents remain data.

An explicit Bluetooth pairing requirement line, distinct from the prepared VM fixture, is:

```json
{"id":"development-pairing","type":"bluetooth","managed":true,"adapter":"<MAC>","address":"<MAC>","name":"development-peer","trusted":false,"state":"paired"}
```

Write that JSON to (not published: external working record) with the literal writer, then submit `request broker bluetoothctl add /home/stand/pairing.json | python3 lab.py run channel-demo`. The example addresses are synthetic and must be replaced with the intended hardware addresses before hardware use. This line is **not tested on hardware** and is not part of the successfully applied VM profile fixture.

Wi-Fi connection requires the same line with `state:"connected"` and actual hardware/network values. Bluetooth pairing requires `state:"paired"`, actual adapter/device addresses and an explicit trusted value; its apply path calls the pairing backend and reads actual paired/trusted state. The provided `prepared` example does not assert a bond. **Wi-Fi connection and Bluetooth pairing: not tested on hardware.** Do not present synthetic saved/prepared profiles as hardware success.

## Refusal coverage and exact suite commands

The complete attempts are executable records in [language-selftest.py](build/language-selftest.py), [app-selftest.py](build/app-selftest.py), [system-selftest.py](build/system-selftest.py), and [round4-selftest.py](build/round4-selftest.py). They include alternate roots, mutable package inputs, hooks/backends, incorrect checksums, Flatpak permission/runtime options, AppImage direct/extracted paths, OCI overlays/binds/exec/build/load/privileged/API routes, and removal. Their expected outcomes precede execution; only saved result rows establish outcomes.

On the server, the one-shot driver creates a separate fresh VM per suite:

```sh
python3 build/round4-driver.py fresh-label
# Full prior-suite and independent-rebuild validation, using an actual separate build root:
python3 build/round4-driver.py full-label --regressions --peer-root ../independent-build
```

The second path must identify an already rebuilt independent image. Omitting it does not establish independent reproducibility. The complete combined declaration must be exported after all intended rows are applied, including factory changes induced by the base update; appending only the update request to the original factory would be incorrect.

The complete validation requires the following post-driver stages after a successful `full-label` run:

```sh
python3 build/assemble-channel-examples.py raw/round-4/full-label channel-example
python3 build/combined-selftest.py combined-label channel-example/combined --peer-root ../independent-build --reboot
```

Both build roots must have the same final recipe files and their separately rebuilt images. Both driver summaries must report zero, and the combined evidence must contain equal every-line observations after reboot. The assembly refuses failed or missing channel exports.
