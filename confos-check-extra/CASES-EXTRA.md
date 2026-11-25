# Cases beyond the plan

Three things that the text of the hypothesis and the plan name are exercised by no case of `CASES.md`. They are
written here, performed by `run-extra` (which loads the frozen `run` unchanged) into `runs/<name>-extra/`, and reported apart from the rows of Table 9.
They are not part of a complete run, and the frozen programs of a complete run do not read this file or
`casedefs_extra.py`. Notation, the semantic line specs and the decisions common to all cases are those of `CASES.md`;
the builder's format of each line is filled in by `adapter.py` from `build/DECLARATION.md` and `build/INTERFACE.md`.

Outcomes as in `CASES.md`: `pass`, `fail`, `unobserved` (the case could not be performed; the reason and the output are
in the evidence), `undecided` (with the question of `QUESTIONS.md`).

## The form performed on release 0.43 (development run dev-14-extra, 2026-11-24)

The tables further below are the first form, written before the implementation recorded anything. On 0.43 the
cases use the command forms that the implementation documents as recording (`build/CHOICES.md`, table “S8.3-7
recording choice”; `build/INTERFACE.md`, revisions 34–43; `build/CONFIGURATION-RECORDING-DRAFT.md`), so that a
refusal of a form the builder never offered is not what a case shows. `casedefs_extra.py` holds them as data. Step 2
is strict: every line the request adds or removes must match one pattern of the case, and each pattern exactly one
line. For a setting that `D-test` did not record before, the removal request records its former value, and that one
line may stay after step 5 (`restore_ok`). Every request runs as root through `sudo -n` (`build/INTERFACE.md`,
“Privilege”); `systemctl --user` keeps the origin of the person (`SUDO_USER`), as the builder requires.

| ID | Request (step 1) | Line that must be added (and taken out) | Probe | Removal request (step 5) |
|---|---|---|---|---|
| X-REC-APT | `apt-get install -y hello` | `package hello VERSION` | `U: hello --version`; `dpkg-query` status `ii` | `apt-get remove -y hello` |
| X-REC-APT2 | `apt install -y hello` | the same | the same | `apt purge -y hello` |
| X-REC-PIP | `pip install --break-system-packages pyjokes==0.8.3` | `pip pyjokes 0.8.3 SHA256 SOURCE` | `U: pyjoke`; `U: python3 -m pip show pyjokes` | `pip uninstall -y pyjokes` |
| X-REC-NPM | `npm install -g semver@7.6.3` | `npm semver 7.6.3 SHA256 LOCK` | `U: semver 1.2.3`; `npm ls -g` | `npm uninstall -g semver` |
| X-REC-FLATPAK | `flatpak install -y --bundle /home/person/mpv.flatpak` (the bundle put in the home first; the runtime line recorded and applied before) | `flatpak app/io.mpv.Mpv/x86_64/stable COMMIT SHA256 SOURCE` | `R: flatpak list --system --app`; `U: flatpak info io.mpv.Mpv` | `flatpak uninstall -y io.mpv.Mpv` |
| X-REC-PODMAN | `podman pull docker.io/library/busybox:1.36.1` | `container person docker.io/library/busybox:1.36.1 CONFIG ARCHIVE SOURCE` | `U: podman image exists …` | `podman rmi docker.io/library/busybox:1.36.1` |
| X-REC-HOST | `hostnamectl set-hostname xrechost` | `setting hostname xrechost` (out: `setting hostname confos-test`) | `U: hostnamectl --static`, `U: hostname` | `hostnamectl set-hostname` the former value |
| X-REC-TIME | `timedatectl set-timezone UTC` (the documented values are `UTC` and `Etc/UTC`; `D-test` has `Etc/UTC`) | `setting timezone UTC` (out: `Etc/UTC`) | `U: timedatectl show -p Timezone --value` | `timedatectl set-timezone` the former value |
| X-REC-SYSCTL | `sysctl -w net.ipv4.ip_forward=1` | `setting sysctl:net.ipv4.ip_forward 1` | `U: sysctl -n net.ipv4.ip_forward` | `sysctl -w net.ipv4.ip_forward=` the former value |
| X-REC-ENABLE | `systemctl enable cases-xrec` (setup: `service cases-xrec disabled /usr/bin/sleep 86412`) | `service cases-xrec enabled …` (out: `… disabled …`) | `U: ps` shows `sleep 86412`; `R: systemctl is-enabled` | `systemctl disable cases-xrec` |
| X-REC-UENABLE | `systemctl --user disable cases-tick.timer` (the person's recorded timer of `D-test`) | `user-unit person cases-tick.timer disabled …` (out: `… enabled …`) | `U: systemctl --user is-enabled` prints `disabled` | `systemctl --user enable cases-tick.timer` |
| X-REC-USER | `useradd -m xrecuser` | `account xrecuser 1001 1001 - /bin/bash HOME` with HOME `/home/` followed by the name (the documented defaults) | `U: getent passwd xrecuser` | `userdel xrecuser` |
| X-REC-USERMOD | `usermod -s /bin/sh xrecmod` (setup: the account `xrecmod` 1500) | `account xrecmod … /bin/sh …` (out: `… /bin/bash …`) | `U: getent passwd xrecmod` | `usermod -s /bin/bash xrecmod` |
| X-REC-NFT | `nft add rule inet confos input tcp dport 9998 accept` | `rule NAME … tcp dport 9998 accept` | `R: nft list ruleset` | `nft delete rule inet confos input handle H` (H read with `nft -a list ruleset` after the application) |

Not performed on 0.43: X-REC-LOCALE, X-REC-GROUP, X-REC-SUDO, X-REC-MODULE, X-REC-LINGER. `build/CHOICES.md` names
`localectl`, `groupadd`, `modprobe` and `loginctl` among the tools with “no current request mapping”, and `visudo`
records from release 0.44 only; the order of the development run names the tools that record.

On 0.52 (`dev-15-extra`, 2026-11-25) also performed, as `build/CHOICES.md` of 0.52 names them as recording:
X-REC-SUDO (`visudo`, from 0.44), X-REC-GROUP (`groupadd`, from 0.50) and X-REC-MODULE (`modprobe`, from 0.50), in
the form of the table below. Still not performed: X-REC-LOCALE and X-REC-LINGER (`localectl`, `loginctl`: “refuses”,
“not built” in 0.52's `CHOICES.md`).

**X-WIFI, X-BT on 0.43.** The simulated radios are the implementation's own (`build/DECLARATION.md`, revision 40):
the packages of the release's `radio-public-fixture/packages.conf` that `D-test` does not record, and the row
`radio-fixture lab …` with its file, both added and applied in step 1 (the fixture is in force when `sudo confos
radio-inspect wifi` shows `type AP`, or `… bluetooth` shows the second controller). Step 2: the person first tries
the built-in tools (`nmcli`, `iwctl`, `wpa_cli`, `connmanctl`; `bluetoothctl pair`), and the evidence keeps their
answer; the implementation documents that network and pairing requests are not recorded yet and that the rows are
written by hand, so the person writes `network saved …` (X-WIFI) or the two reciprocal `bluetooth-pair …` rows
(X-BT), with the release's files. Connected: `radio-inspect wifi` shows `Connected to 02:00:00:00:00:00 (on wlan1)`;
paired: `radio-inspect bluetooth` shows `"Paired": 1`. Stored: `/usr/lib/confos/radio/wpa.conf`, or
`/usr/lib/confos/radio/bluez/ADAPTER/PEER/info`; if it is not observed after the application, the case is
`unobserved` (otherwise its absence after the removal would show nothing). Steps 4 and 5 as below.

**The declaration of the development run.** Release 0.43 does not build `D-test` (`Flatpak reader bundle checksum
mismatch`: it accepts only the builder's own export of the runtime commit that `D-test` names, `DEV-14.md`). The cases
beyond the plan were therefore performed from `declarations/D-test-noflatpak.spec` (`D-test` without its flatpak
line), and X-REC-FLATPAK uses the builder's two exported bundles (read from the builder's folder on the server).

## X-REC — a tool of installation or configuration records the change in the declaration

Source: S8.3-7, “Its tools for installation and configuration record changes in the declaration even when they run
with superuser privileges: an installer does not install a program past the declaration but adds it to the
declaration.”

Every X-REC case has the same steps. `FRESH xrec-<id>`; `DECL?` (`DECL0`, the text read from outside, and the
identity of `confos status`); `INV <ID>-pre`; then:

1. **Request.** `R: CMD-ADD` — the person asks the tool, with superuser privileges, for a thing that no line of
   `DECL0` records. Kept: exit status, stdout, stderr.
2. **The line.** `DECL?` read from outside the machine (the disk image with libguestfs, read-only). Required: the
   declaration text differs from `DECL0` by lines that record exactly the requested thing (the semantic line `LINE`
   below, parsed by `adapter.py`), and by nothing else. The evidence names the program that wrote the text: the
   command of step 1, its output (for `apt-get`, `RECORDED SHA256; run confos apply`, `build/INTERFACE.md`), and the
   process and executable of the tool that ran (`/proc/PID/exe` of the tool's process, taken while it runs, when it
   runs long enough; otherwise the path the shell resolved, `R: command -v TOOL` and `readlink -f`).
3. **Nothing past the declaration before the application.** `INV <ID>-rec`; `CMP <ID>-rec` against the declaration in
   force (the one `confos status` names, which is still `DECL0` until the application); and `compare --baseline` of
   `INV <ID>-rec` against `INV <ID>-pre`, as for a P4 attempt. Required: the attempt effect is empty: no object of
   the requested thing is in force, and no recorded thing changed. The probes `PROBE` are taken too and must not hold.
4. **The application.** The application that `build/INTERFACE.md` documents for a recorded request (`APPLY`, unless
   the tool itself applies and documents that). Required: `applied` for the new text; then `PROBE` holds, `CMP <ID>`
   of `INV <ID>` against the derivation of the new text has no `UNRECORDED`, `MISSING`, `DIFFERS` or `UNVERIFIED`
   line (the same rules as the P2 and P1 rows of `CASES.md`).
5. **Removal request.** `R: CMD-REMOVE` to the same tool. `DECL?`: the line of step 2 is gone and the text equals
   `DECL0` up to the order of lines; `INV <ID>-unrec` and the attempt effect against `INV <ID>` as in step 3:
   nothing changed before the application.
6. **The application of the removal.** `APPLY`; required: `applied`; `PROBE` does not hold; the objects that step 4
   brought in force and that `DECL0` does not cover are not in force (the rule of `REM-1`); `CMP <ID>-removed` clean.

Outcome: `pass` when steps 1–6 hold. `fail` when the tool refuses the request (step 1 exits non-zero or prints a
refusal, and the text is unchanged), when it installs or changes past the declaration (step 3 or step 5 has an
effect), when the line is not written or something else is written (step 2, step 5), or when the application does not
bring the recorded state (steps 4 and 6). A refusal is `fail` here and not met as in R3 of the review: S8.3-7 asks
that the tool record the change, not that it refuse it. `unobserved` when a step could not be performed for a reason
outside the implementation (a machine that did not start, a network fetch of the case's own host that failed). The
evidence keeps the outcome of every step separately, so that a tool that records but whose application fails is
told apart from a tool that refuses.

### Installers

The thing requested is the one the P4 case of the same channel tries to install past the declaration, so that the
same package is first refused (P4) and then recorded (X-REC).

| ID | Channel | `CMD-ADD` | `LINE` | `PROBE` | `CMD-REMOVE` |
|---|---|---|---|---|---|
| X-REC-APT | system package manager | `apt-get install -y hello` | `package hello` (the version the archive state of the declaration gives) | `U: hello --version`; `dpkg-query -W hello` | `apt-get remove -y hello` |
| X-REC-APT2 | system package manager, `apt` | `apt install -y hello` | as X-REC-APT | same | `apt purge -y hello` |
| X-REC-PIP | pip | `pip install --break-system-packages pyjokes==0.8.3` | `pip pyjokes==0.8.3` | `U: pyjoke`; `R: pip show pyjokes` | `pip uninstall -y --break-system-packages pyjokes` |
| X-REC-NPM | npm | `npm install -g semver@7.6.3` | `npm semver@7.6.3` | `U: semver 1.2.3` | `npm uninstall -g semver` |
| X-REC-FLATPAK | Flatpak | `flatpak install --system -y flathub net.sourceforge.ExtremeTuxRacer` | `flatpak net.sourceforge.ExtremeTuxRacer flathub` | `R: flatpak list --system --app`; `U: flatpak run --command=true net.sourceforge.ExtremeTuxRacer` | `flatpak uninstall --system -y net.sourceforge.ExtremeTuxRacer` |
| X-REC-PODMAN | containers | `podman pull docker.io/library/busybox:1.36.1` | `container-image docker.io/library/busybox@DIGEST` (the digest the registry gives for the tag; `tools/make-inputs.sh` pins it) | `R: podman image exists docker.io/library/busybox:1.36.1` | `podman rmi docker.io/library/busybox:1.36.1` |

The command of each row is given as the person types it, with superuser privileges by the documented means
(`R:`). If `build/INTERFACE.md` documents a different form of request for the same tool (for example a required
option), the adapter uses that form and the evidence keeps both.

### Configuration tools

The tools of the P4-BT cases, with the same values; for each the line is the semantic setting line that `adapter.py`
renders in the builder's format. A tool that `build/INTERFACE.md` does not name as recording is performed all the
same (S8.3-7 names “its tools for installation and configuration”, not some of them); the evidence says whether the
builder names it.

| ID | Tool | `CMD-ADD` | `LINE` | `PROBE` | `CMD-REMOVE` |
|---|---|---|---|---|---|
| X-REC-HOST | `hostnamectl` | `hostnamectl set-hostname xrechost` | `setting hostname xrechost` | `hostnamectl --static` prints `xrechost` | `hostnamectl set-hostname` back to the value of `DECL0` (the line returns to its former value) |
| X-REC-TIME | `timedatectl` | `timedatectl set-timezone Asia/Tokyo` | `setting timezone Asia/Tokyo` | `timedatectl show -p Timezone --value` | `timedatectl set-timezone` back to the value of `DECL0` |
| X-REC-LOCALE | `localectl` | `localectl set-locale LANG=C.UTF-8` | `setting locale LANG=C.UTF-8` | `localectl status` | `localectl set-locale` back |
| X-REC-ENABLE | `systemctl enable` | `systemctl enable --now cases-xrec.service`, where `cases-xrec.service` is a unit that a recorded line of `D-test` installs and does not enable (`service NAME TEXT` without `enabled`, added to `DECL0` by the case before step 1 and applied) | `service cases-xrec.service TEXT enabled` | `systemctl is-enabled`, `is-active` | `systemctl disable --now cases-xrec.service` |
| X-REC-USER | `useradd` | `useradd -m xrecuser` | `account xrecuser` | `getent passwd xrecuser` | `userdel -r xrecuser` |
| X-REC-GROUP | `groupadd` | `groupadd xrecgroup` | `group xrecgroup GID` (the documented default GID) | `U: getent group xrecgroup` | `groupdel xrecgroup` |
| X-REC-NFT | `nft` | `nft add table inet xrec; nft add chain inet xrec c '{ type filter hook input priority 0; }'; nft add rule inet xrec c tcp dport 9998 accept` | `firewall 'tcp dport 9998 accept'` | `nft list ruleset` has the rule | `nft delete table inet xrec` |
| X-REC-SYSCTL | `sysctl` | `sysctl -w net.ipv4.ip_forward=1` | `setting sysctl net.ipv4.ip_forward=1` | `sysctl -n net.ipv4.ip_forward` prints 1 | `sysctl -w net.ipv4.ip_forward=` the value of `DECL0` |
| X-REC-SUDO | `visudo` | `EDITOR='tee -a' visudo` with `person ALL=(root) NOPASSWD: /usr/bin/true` on stdin | `sudo 'person ALL=(root) NOPASSWD: /usr/bin/true'` | `sudo -l -U person` | `visudo` removing the same line |
| X-REC-MODULE | `modprobe` | `modprobe dummy` | `setting module:dummy loaded` (loaded at every start after the application) | `U: grep -w ^dummy /proc/modules` | `modprobe -r dummy` |
| X-REC-LINGER | `loginctl` | `loginctl enable-linger person` | `setting linger person` | `loginctl show-user person -p Linger` | `loginctl disable-linger person` |

For a tool whose change is a value of an existing line (hostname, timezone, locale, sysctl), step 2 requires that the
line now states the new value and step 5 that it states the former value again; “the text equals `DECL0` up to the
order of lines” is required after step 5.

## X-WIFI — connecting to a Wi-Fi network, on simulated radios

Source: plan Section 9.3, ordinary work, “connecting to a Wi-Fi network”; S8.2-13, “Settings are services and their
parameters, the network, including saved networks, …”. OW-10 (real hardware) stays as it is; this case uses
simulated radios inside the guest and is reported apart.

The fixture is part of the declaration, so that a clean installation has it too: `module mac80211_hwsim radios=2`
(the module of the Debian kernel, `kernel/drivers/net/wireless/virtual/mac80211_hwsim.ko.xz`); `package hostapd`
(Debian 13: 2:2.10-24), `package iw`; a file line for `/etc/hostapd/cases-ap.conf` (interface: the first simulated
radio; `ssid=cases-net`, WPA2-PSK with the passphrase `cases-passphrase-1`, channel 1, `hw_mode=g`) and a `service`
line that runs `hostapd /etc/hostapd/cases-ap.conf`, enabled. The client is the second radio, with whatever
connection manager the release has (`nmcli`, `iwctl` or `wpa_cli`; the adapter takes the one `build/INTERFACE.md`
documents and records which).

| ID | Steps | Observed by | pass when |
|---|---|---|---|
| X-WIFI-1 | `FRESH xwifi1` from `D-test` plus the fixture lines; `APPLY`; check the fixture: `R: iw dev` lists two simulated interfaces and the access point is up (`R: iw dev AP-IF info` shows type AP, `ssid cases-net`) | `iw dev`; `iw dev AP-IF info` | the fixture is in force; otherwise the case is `unobserved` with the output |
| X-WIFI-2 | the person connects with the built-in tool: `R: nmcli device wifi connect cases-net password cases-passphrase-1 ifname CLIENT-IF` (or the documented equivalent); `DECL?`; if the tool did not write a line, the person writes it: `L+ wifi cases-net PSK CLIENT-IF` (the saved network), `APPLY` | `R: iw dev CLIENT-IF link` shows `Connected to` the access point's address and `SSID: cases-net`; `DECL?` has the line of the saved network | connected, and a line of the declaration records the saved network (written by the tool or by the person; the evidence says which) |
| X-WIFI-3 | `INV X-WIFI-3`; `CMP` | the saved network on the machine (the connection manager's stored profile, `nmcli -t connection show`) | the saved network follows from the line; no `UNRECORDED` saved network or profile (S8.2-13) |
| X-WIFI-4 | `FRESH-BUILD xwifi4` from the declaration in force after X-WIFI-2 (a new independent clean installation); boot until `APPLIED`; nothing typed in the guest | `R: iw dev CLIENT-IF link` within 120 s of the report of success | connected to `cases-net` without anything typed |
| X-WIFI-5 | on xwifi4: `L-` the line of the saved network (or the removal request of the tool, if the tool records); `APPLY` | `R: iw dev CLIENT-IF link` (`Not connected.`); the stored profile absent; `INV X-WIFI-5`; `CMP` | not connected, no saved network in force or stored, and nothing of the line remains (the rule of `REM-1`) |

Outcome of the case: `pass` when X-WIFI-2 … X-WIFI-5 hold; `fail` when one of them does not hold although the
fixture of X-WIFI-1 is in force; `unobserved` when the fixture cannot be made (the module is absent from the release's
kernel, the declaration format has no line for a kernel module parameter or a file, or `hostapd` does not start on a
simulated radio), with the command and output.

## X-BT — pairing a Bluetooth device, on a simulated controller pair

Source: plan Section 9.3, ordinary work, “pairing a Bluetooth device”; S8.2-13, “devices”. OW-11 (real hardware)
stays as it is.

The fixture: `module hci_vhci` (the module of the Debian kernel, `kernel/drivers/bluetooth/hci_vhci.ko.xz`);
`package bluez` (5.82-1.1), `package bluez-test-tools` (5.82-1.1, which ships `/usr/bin/btvirt`); a `service` line
that runs `btvirt -l2` (two virtual controllers over `hci_vhci`), enabled, and `bluetooth.service` enabled. One
controller is the person's (`hci0`), the other acts as the device (`hci1`, discoverable and pairable, with a
NoInputNoOutput agent: `btmgmt --index 1 power on; btmgmt --index 1 connectable on; btmgmt --index 1 bondable on;
btmgmt --index 1 discov yes`, made a recorded service of the fixture so that a clean installation has it too).

| ID | Steps | Observed by | pass when |
|---|---|---|---|
| X-BT-1 | `FRESH xbt1` from `D-test` plus the fixture lines; `APPLY` | `R: btmgmt info` lists two controllers; the address `ADDR1` of `hci1` | two controllers; otherwise `unobserved` with the output |
| X-BT-2 | the person pairs with the built-in tool: `R: bluetoothctl --timeout 60` with `select ADDR0`, `scan on`, `pair ADDR1`, `trust ADDR1`; `DECL?`; if the tool did not write a line, the person writes it: `L+ bt-pairing ADDR0 ADDR1` (with the link key that the line format requires), `APPLY` | `R: bluetoothctl info ADDR1` shows `Paired: yes`; `DECL?` has the line of the pairing | paired, and a line records the pairing (by the tool or by the person; the evidence says which) |
| X-BT-3 | `INV X-BT-3`; `CMP` | the stored pairing (`/var/lib/bluetooth/ADDR0/ADDR1/info`) | it follows from the line; no `UNRECORDED` pairing |
| X-BT-4 | `FRESH-BUILD xbt4` from the declaration in force after X-BT-2; boot until `APPLIED`; nothing typed | `R: bluetoothctl info ADDR1` | `Paired: yes`. The controller addresses of `btvirt` must be the same on both installations for the pairing to refer to the same device; if they are not (the addresses are made at random by `btvirt`), the row is `unobserved: the simulated device has another address on the clean installation`, with both addresses |
| X-BT-5 | on xbt4: `L-` the line of the pairing (or the removal request of the tool); `APPLY` | `R: bluetoothctl info ADDR1` (`Paired: no` or the device unknown); the stored pairing absent; `INV X-BT-5`; `CMP` | not paired, nothing of the line in force or stored |

Outcome of the case: as X-WIFI.

## Repairs of the programs of these cases

- **[x1] 2026-11-25 02:05 UTC, `run-extra`: the effect of an X-REC step counted every object as a failure.** Wrong:
  steps 3, 5 and 6 appended any non-empty effect (`N-attempt-effect.tsv`) to the failures, also objects whose route
  was not taken (`UNROUTED`, `UNPROBED`) and objects decided both ways or only by Q11/Q12 (`BOTHWAYS`, `QUESTION`);
  the frozen `run` judges the effect of an attempt otherwise (`p4_decide`, [n3-B]). Seen in `dev-15-extra` on 0.52:
  step 5 of X-REC-PODMAN failed on two files under `/run/user/1000` (podman's `events.log` and crun's seccomp
  cache, which is written when a container runs) that appeared after the inventory of step 4, where the case's
  probe `podman run --rm … true` runs as the person, and whose routes were not tried. Now `judge_effect`: objects that follow from no line → fail; only `UNROUTED`/`UNPROBED`
  → unobserved; only `BOTHWAYS`/`QUESTION` → undecided. Test: `selftest/extra/check-judge-effect.py RUN_EXTRA
  selftest/extra/fixture` with the effects recorded in `dev-15-extra` (X-REC-PODMAN steps 3 and 5) and `dev-16-new`
  (P4-S-054): FAIL on the `run-extra` of `dev-15-extra`, PASS after the repair.
- **[x2] 2026-11-25 03:25 UTC, `derive-radio` (`tools/make-derive-radio.py`): the kind `group` was unknown.** Wrong:
  release 0.50 adds the line `group NAME GID` (`build/DECLARATION.md`, revision 50), which `groupadd` records; the
  frozen `derive`, and so `derive-radio`, stopped on it (`derive: ERROR declaration.conf:49 group xrecgroup: unknown
  kind 'group'`, `runs/dev-15-extra/X-REC-GROUP/0043.err`), so in `dev-15-extra` on 0.52 the P1 and P2 rows of
  X-REC-GROUP and its step 5 were `unobserved`, although every probe of the case held. Now `derive-radio` derives
  the group NAME with its GID (the password field is underived; its members follow from the account lines that name
  it, as in the frozen `derive`). The frozen `derive` does not change. Test: `selftest/extra/test-derive-radio.sh
  SOURCE_TAR`, check 4 (the line `group xrecgroup 1001` alone: one group object, no error): FAIL with the
  `derive-radio` of the second-set freeze of 02:32 UTC, PASS after the repair (`scraps/f8/test-x2.txt`). X-REC-GROUP
  performed again as `dev-15g-extra` with `CASES_DERIVE_RADIO=1`.
