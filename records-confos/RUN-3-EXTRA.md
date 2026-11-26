# The second set on release 0.55: run-3-extra and run-3-radio

Written by the case party. Times in UTC, 2026-11-25. The cases beyond the plan (`CASES-EXTRA.md`); they are outside
`CASES.md` and outside the complete runs, and their rows are not observations of the check.

## What was run

- Release 0.55: `releases/confos-0.55-source.tar.gz`, SHA256
  `eb901118dc725dfbadfc46ee56069f4fa631903fdb08eec25bf763f6a12acdd1` (checked by the script before the runs).
- Order 6 of the party that directed the work, item 5, with `run/src16` (order 8): right after complete run 3, the second set as `READY.md`,
  section 7b, says. Programs: `run/src16`; before the runs `sha256sum -c src16.sha256` and `sha256sum -c
  src16x-extra.sha256`: every file OK (the second set as committed in `confos-check-extra/`, its eleven files
  unchanged; what it reads of the first set is the seventh freeze). Script: `scraps/f11/run3x.sh`.
- Both invocations with `CASES_DERIVE_RADIO=1` (every derivation by `derive-radio`, which differs from the frozen
  `derive` only in the three radio kinds and the kind `group`), declaration `declarations/D-test-noflatpak.spec`
  (`D-test` without its flatpak line: with that line mpv is already recorded and X-REC-FLATPAK could not show the
  recording), at most 5 machines; every machine stopped and every work folder removed at the end (08:13 UTC: no
  `qemu-system` process on the server, `run/work` empty).
- The X-REC cases: one for every recording tool that 0.55's `CHOICES.md` names. Its table of recording tools is the
  table of 0.52 with only the names of the evidence files changed (`records/` → `evidence/`), so the cases are the 17
  of `dev-15-extra`. `localectl set-locale` and `loginctl enable-linger` are “not built” in 0.55 too.

| run | time | cases |
|---|---|---|
| `run-3-extra` | 07:14:36–07:58:29 | X-REC-APT, -APT2, -PIP, -NPM, -FLATPAK, -PODMAN, -HOST, -TIME, -SYSCTL, -ENABLE, -UENABLE, -USER, -USERMOD, -NFT, -GROUP, -SUDO, -MODULE |
| `run-3-radio` (folder `runs/run-3-radio-extra`: `run-extra` adds `-extra` to a name that does not end with it) | 07:58:29–08:13:12 | X-WIFI, X-BT |

The folders are on the server and, without the raw inventories and comparisons, in `../runs/run-3-extra` and
`../runs/run-3-radio-extra`.

## The cases beyond the plan

For each case: performed or not, the outcome, one sentence, the evidence (relative to the run's folder). An X-REC row
is `fail` when one of its steps fails or one of the P1/P2 rows of its inventories after the application and after the
removal is `fail`, and `unobserved` when a step's effect has only objects whose route or probe was not taken ([x1]);
the sentence says which.

| Case | Run | Performed | Outcome | One sentence | Evidence |
|---|---|---|---|---|---|
| X-REC-APT | run-3-extra | yes | pass | `apt-get install -y hello` recorded `package hello 2.10-5` and nothing else; `hello --version` and `dpkg-query` held only after the application; `apt-get remove -y hello` restored the text and after its application nothing of it remained. | `X-REC-APT/X-REC-APT.outcome.txt`, `X-REC-APT/xrec-steps.json` |
| X-REC-APT2 | run-3-extra | yes | pass | The same with `apt install -y hello` and `apt purge -y hello`. | `X-REC-APT2/…` |
| X-REC-PIP | run-3-extra | yes | pass | `pip install --break-system-packages pyjokes==0.8.3` recorded `pip pyjokes 0.8.3 12836e61… recorded-inputs/…/pyjokes-0.8.3-py3-none-any.whl`; `pyjoke` ran only after the application; `pip uninstall -y pyjokes` removed the line and, after its application, the program. | `X-REC-PIP/…` |
| X-REC-NPM | run-3-extra | yes | pass | `npm install -g semver@7.6.3` recorded `npm semver 7.6.3 d05eee44… recorded-inputs/…/package-lock.json`; the module was loadable by `node` only after the application and not after the removal (`npm uninstall -g semver`) was applied. | `X-REC-NPM/…` |
| X-REC-FLATPAK | run-3-extra | yes | pass | `flatpak install -y --bundle /home/person/mpv.flatpak` recorded `flatpak app/io.mpv.Mpv/x86_64/stable 13baef0d… 66d65390… recorded-inputs/…`; `flatpak list --app --columns=application` and `flatpak info io.mpv.Mpv` held only after the application and not after the removal was applied. On 0.52 it was `fail` because the person's `flatpak list` was refused (`REQUESTS.md`, entry 17); repaired in the implementation. | `X-REC-FLATPAK/X-REC-FLATPAK.outcome.txt`, `X-REC-FLATPAK/xrec-steps.json` |
| X-REC-PODMAN | run-3-extra | yes | unobserved | `podman pull docker.io/library/busybox:1.36.1` recorded `container person docker.io/library/busybox:1.36.1 b116e155… 4c57ecd7… recorded-inputs/…`; `podman images` and `podman run --rm … true` held only after the application and not after `podman rmi …` was applied; step 3 now has no effect (on 0.52 root's podman queries failed there, entry 17; repaired in the implementation). `unobserved` only by step 5: two files under `/run/user/1000` (podman's `confos-podman-tmp/events/events.log` and crun's seccomp cache) whose routes `run-extra` did not try (`UNROUTED`), as in `dev-15c-extra`. That is the case party's program, not the implementation (below). The P1 and P2 rows pass. | `X-REC-PODMAN/X-REC-PODMAN.outcome.txt`, `X-REC-PODMAN/5-attempt-effect.tsv` |
| X-REC-HOST | run-3-extra | yes | pass | `hostnamectl set-hostname xrechost` replaced `setting hostname confos-test` by `setting hostname xrechost`; the name held only after the application; setting it back restored the text and the name. | `X-REC-HOST/…` |
| X-REC-TIME | run-3-extra | yes | pass | `timedatectl set-timezone UTC` replaced `setting timezone Etc/UTC` by `setting timezone UTC`; `/etc/timezone` read `UTC` only after the application, and not after the reverse request was applied. | `X-REC-TIME/…` |
| X-REC-SYSCTL | run-3-extra | yes | fail | `sysctl -w net.ipv4.ip_forward=1` recorded `setting sysctl:net.ipv4.ip_forward 1`; `sysctl -n` gave 1 only after the application and not after the removal request (`… =0`, recorded as `… 0`) was applied; the P1 rows pass; `fail` only through its two P2 rows, `MISSING setting sysctl:net.ipv4.ip_forward`, which is the case party's `inventory` (it takes no kernel parameter as a setting in force; as in `dev-14` and `dev-15-extra`). | `X-REC-SYSCTL/P2:X-REC-SYSCTL-applied.outcome.txt`, `X-REC-SYSCTL/inv-X-REC-SYSCTL-applied/compare.tsv` (server) |
| X-REC-ENABLE | run-3-extra | yes | pass | `systemctl enable cases-xrec` changed `service cases-xrec disabled /usr/bin/sleep 86412` to `… enabled …`; the process `sleep 86412` ran only after the application and not after `systemctl disable cases-xrec` was applied. | `X-REC-ENABLE/…` |
| X-REC-UENABLE | run-3-extra | yes | pass | `systemctl --user disable cases-tick.timer` changed the person's `user-unit … cases-tick.timer enabled …` line to `disabled`; `systemctl --user is-enabled` followed only after each application. | `X-REC-UENABLE/…` |
| X-REC-USER | run-3-extra | yes | pass | `useradd -m xrecuser` recorded `account xrecuser 1001 1001 - /bin/bash /home/xrecuser`; `getent passwd xrecuser` answered only after the application; `userdel xrecuser` restored the text and after its application the account was gone. | `X-REC-USER/…` |
| X-REC-USERMOD | run-3-extra | yes | pass | `usermod -s /bin/sh xrecmod` changed only the shell field of the account line; `/bin/sh` held only after the application, `/bin/bash` again after the reverse request was applied. | `X-REC-USERMOD/…` |
| X-REC-NFT | run-3-extra | yes | pass | `nft add rule inet confos input tcp dport 9998 accept` recorded `rule nft-5085132a61548392ac4e0953 'add rule inet confos input tcp dport 9998 accept'`; the rule was in `nft list ruleset` only after the application; `nft delete rule inet confos input handle 3` restored the text and removed the rule. | `X-REC-NFT/…` |
| X-REC-GROUP | run-3-extra | yes | pass | `groupadd xrecgroup` recorded `group xrecgroup 1001`; `getent group xrecgroup` answered only after the application; `groupdel xrecgroup` restored the text and after its application the group was gone. | `X-REC-GROUP/…` |
| X-REC-SUDO | run-3-extra | yes | pass | `printf 'person ALL=(root) NOPASSWD: /usr/bin/true\n' \| EDITOR='tee -a' visudo` recorded `file /etc/sudoers.d/confos-local 0440 0:0 4e3f22b2… recorded-inputs/visudo-4e3f22b2…`; `sudo -l -U person` showed the rule only after the application; `visudo --remove` restored the text and after its application the rule was gone. | `X-REC-SUDO/…` |
| X-REC-MODULE | run-3-extra | yes | fail | `modprobe dummy` recorded `setting module:dummy loaded`; `dummy` was in `/proc/modules` only after the application and not after `modprobe -r dummy` was applied; the P1 rows pass; `fail` only through its P2 row after the application, `MISSING setting module:dummy`, which is the case party's `inventory` (it takes no loaded module as a setting in force). | `X-REC-MODULE/P2:X-REC-MODULE-applied.outcome.txt`, `X-REC-MODULE/inv-X-REC-MODULE-applied/compare.tsv` (server) |
| X-WIFI | run-3-radio | yes | pass | The documented `nmcli` add request with the fixture's values wrote the line `network casesnet d2e8171f… recorded-inputs/network-d2e8171f….json` (“RECORDED …; run confos apply”); after its application the simulated client was connected; a new clean installation from the same declaration was connected with nothing typed; the removal request removed the line and, after its application, the connection. Its P2 rows fail: `MISSING network casesnet` and `MISSING radio-fixture lab` (the case party's programs, below). | `X-WIFI/X-WIFI.outcome.txt`, `X-WIFI/xradio-steps.json` |
| X-BT | run-3-radio | yes | pass | With the two reciprocal `bluetooth-pair` lines and the `radio-fixture` line applied, the simulated controllers were paired; a new clean installation from the same declaration was paired with nothing typed; removing the lines and applying left them unpaired. Its P2 rows fail on `MISSING` objects of the kinds `bluetooth-pair` and `radio-fixture` (the case party's programs, below). | `X-BT/X-BT.outcome.txt`, `X-BT/xradio-steps.json` |
| X-REC-LOCALE, X-REC-LINGER | — | no | fail | Not performed: 0.55's `CHOICES.md` has `localectl set-locale` “none: only the C locales exist without generated locale data, and sessions are started with a fixed locale \| refuses \| not built” and `loginctl enable-linger` “none: a user manager exists only through `user-unit` lines of the account \| refuses \| not built”; by the order, a case that cannot be performed because the implementation has no such tool is `fail`, with the builder's words. | `CHOICES.md` of 0.55, lines 44–45 |

In short: every one of the 17 recording requests was recorded as exactly the line the implementation documents and
nothing else, nothing of it was in force before `confos apply`, the application brought it in force, and every
removal request recorded the removal, which held only after its application. Since 0.52 the two failures of the
implementation (X-REC-FLATPAK, X-REC-PODMAN step 3; `REQUESTS.md`, entry 17) are gone. No row of these runs fails
because of the implementation; X-REC-LOCALE and X-REC-LINGER are `fail` because the implementation has no such tool.

Rows of the runs:

| run | X-* | P1 | P2 | UND | all |
|---|---|---|---|---|---|
| run-3-extra | pass 14, fail 2, unobserved 1 | pass 34 | pass 31, fail 3 | undecided 34 | 119 |
| run-3-radio (X-WIFI, X-BT) | pass 2 | pass 4 | fail 4 | undecided 4 | 14 |

The `UND` rows are `undecided` as everywhere: met against the reference installation, not under the derivation from
the declaration alone (D1, D3–D6).

The list for the builder: nothing. No row of these runs fails because of the implementation, and no `REQUESTS.md`
entry is written for them.

### Rows that are not `pass` because of the case party's programs

The second set is frozen; none of these was repaired.

- X-REC-PODMAN, step 5 (`unobserved`): `run-extra` judges the effect of a step as the frozen `run` judges an attempt
  ([x1]): objects whose route was not taken are `unobserved`, not `fail`. The two files under `/run/user/1000` appear
  after the inventory of step 4, where the case's probe `podman run --rm … true` runs as the person; no route of them
  was tried.
- X-REC-SYSCTL, X-REC-MODULE, P2 (`fail`): `inventory` takes no kernel parameter and no loaded module as a setting in
  force, while the probes (`sysctl -n`, `/proc/modules`) show the value. `inventory` is frozen, no case of `CASES.md`
  has such a line, and a copy that took every kernel parameter as a setting would change every other row.
- X-WIFI, X-BT, P2 (`fail`): `derive-radio` derives objects of the kinds `radio-fixture`, `network` and
  `bluetooth-pair`, which the frozen `inventory` does not observe in the form of these lines (it has no object of
  those kinds), so each such object is `MISSING`; the cases' own probes show them in force.
