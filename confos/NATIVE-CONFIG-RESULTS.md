# Private39 native configuration-store experiment

The exact `patch-native-config-draft.py` policy was applied only to a separate
sealed39 source extraction. No main source/package/image, release40/41, declaration
grammar or recorder implementation changed. Guest3GiB/2vCPU, persistent unit8GiB
memory cap/100% CPU, one shared slot. Final unit exited0; guest and private tree
were removed after evidence collection. Shared worker usage then39G.

## Observed native results

Every command below ran as root in `confos-session (enforce)`, against existing
native ELF executables. Results were repeated after the successful apply/reboot.

| Command | Exit | Diagnostic / result |
|---|---:|---|
| `apt-mark hold cron` |100| No permission to lock `/var/lib/dpkg`; dpkg child failed. |
| `apt-mark auto cron` |100| Creating temporary `extended_states` file denied. |
| `apt-mark manual bash` |100| Same permission denial; bash initially auto. |
| `crontab -u user /tmp/native-config-request.cron` |1| Spool mkstemp Permission denied. |
| `crontab -u user -r` |1| Spool unlink Permission denied; existing table remains. |
| `dpkg --set-selections`, input `cron hold` |2| No permission to lock database directory. |
| `apt-mark showhold/showauto/showmanual` |0| Unchanged query outputs; no hold, bash auto, cron manual. |
| `crontab -u user -l` |0| Empty output for the comment-only packaged table; exact table bytes separately checked, unchanged. No active-job scheduling claim. |
| `dpkg --get-selections cron` |0| `cron install`. |

For every command the driver compared full membership, mode, uid/gid, symlink
targets and regular-file content hashes beneath `/var/lib/dpkg`, `/var/lib/apt`,
`/var/spool/cron`, plus declaration SHA256. Every before/after pair matched.
These are direct observed store invariants, not an inference from exit status.
Full exit/stdout/stderr and each pair of hashes: `native-config-private.log`.

The supported `apt-get install ed=1.21.1-1` still recorded an exact package line.
`/usr/bin/ed` remained absent before apply and status still named the old applied
identity. `confos apply` rebuilt/rebooted, reported the exact new identity and
`ed --version` succeeded; the mutation/query matrix passed again afterward.

- Initial identity: `b8c3cf857f60457ca70715b7ad91fd6ff911cad3b22df567ab9459eea5f07a9b`.
- Recorded/new applied identity: `18fe51d7e2e7b08b867f9e6cfafe7c9fdf5461f5227d86c977045a62b4d1eb72`.
- Final marker: `NATIVE CONFIG PRIVATE MUTATIONS QUERIES AND RECORDER APPLY PASS`.

## Fixture provenance, limitations and prior attempts

Ordinary file rows do not support `/var`. Two explicit **private runtime-package
fixtures**, both root-owned, supplied meaningful initial auto/removal state:

| Packaged contribution | Mode | SHA256 |
|---|---|---|
| `/var/lib/apt/extended_states`, bash Auto-Installed1 |0644| `646d7709b0d24d7bfcfb9b5aec7befa051b78171a14110bdfda7093fb2643d5a` |
| `/var/spool/cron/crontabs/user`, one identifying comment |0600| `4c155593b737d2e168c4e8876df5349821281db22629607ba10ce8d6d235c9c6` |

No ad-hoc guest write seeded these stores. Private runtime package checksum:
`cda2c6b8293fe5bebaac3fd7e62174c023dffaeb9c9047dcce269dc7ea132c26`.
The package, changed source, fixture inputs and exact patch are in the evidence.
This is not public file-row support or a new line kind. Holds/auto/manual/cron
requests still refuse; the experiment implements no recorder for them.

Earlier logs are preserved: first build rejected invalid `/var` file rows;
second probe incorrectly chose absent sed as the auto fixture; third incorrectly
required crontab to display its comment; fourth accepted too narrow a spelling
of the observed dpkg lock denial. None was reported as a policy success. Final
driver was fed explicitly on stdin as test data (R4), asserting the same kernel
confinement profile, to avoid repeatedly rebuilding for observation corrections.
The old recorded probe remains an unused fixture input in that private image.

Only the native host-session routes above were exercised. Although the same
rules were emitted into Flatpak policy, actual Flatpak app context and the
`/run/host`/`/proc/*/root` aliases were not exercised here. No blanket channel,
S8.3-7 completeness, production release or acceptance claim follows.

Evidence archive `native-config-evidence.tar.gz` SHA256:
`e04cd513deed9defeeb04e1c049122087edbd0efdd1b58c12636c9be71d4be29`.
It includes all failed attempts, passing log/serial, private runtime package,
fixture inputs, policy source and reproduction scripts. This evidence is separate
from the17-case pdb/gyp candidate and neither candidate was integrated into40/41.
