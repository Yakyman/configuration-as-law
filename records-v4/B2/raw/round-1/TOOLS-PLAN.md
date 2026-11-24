# Typed tool implementation and pre-run fixtures

Recorded 2026-11-23 UTC. This is an implementation plan, not successful VM evidence or a closure claim.

`v4_tools.py` accepts `TOOL add ROW.json` and `TOOL remove ID`. Supported kinds:

| Tool | Kind |
|---|---|
| useradd, usermod, userdel | account |
| groupadd, groupdel | group |
| systemctl | service, timer, socket |
| systemd-run | service, timer |
| crontab, at | timer |
| nft | rule |
| nmcli | wifi |
| bluetoothctl | bluetooth |

Deletion tools accept only `remove`. Other tools support removal of their kind,
including removal through the same frontend that added the row. Each adapter
checks row kind and managed status; the common validator checks all values and
factory protection. Deletion also requires an existing matching managed row.
The existing `crontab add` schedule specification still creates its paired
service/timer rows. Remove the timer first, then service through `systemctl`.
`systemctl --user add` and `systemd-run --user add-timer` remain available.
These are finite declared-state interfaces, not compatibility implementations of
every native command-line option.

Standalone group fixture:

```json
{"id":"test:group","type":"group","managed":true,"name":"testgroup","gid":1901,"members":[]}
```

Numeric IDs must be 1100 through 60000. Only empty independent groups are
supported. An independent group cannot conflict by name or numeric ID with any
account row. Account row semantics continue to declare their primary group.
Group readback compares name, GID and actual members. Group removal invokes the
native group deletion backend, with application rollback supplied by the common
transaction machinery. Independent inventory coverage remains a later-round
limitation; this does not change that census.

`apt`, `apt-get`, and `stand-pkg` accept `reinstall` and `downgrade` as exact
desired-state selection aliases for `install`, using an exact JSON artifact or
(for apt variants) a supported catalog package/version. No unavailable version
is implied. A downgrade requires an actually lower version fixture.

`v4-editor` is a document editor with the following operations:

- `read FILE` writes the exact document to stdout.
- `write FILE` replaces a document with stdin bytes.
- `append FILE` appends stdin bytes.
- `package-install ROW.json` installs the exact program/code artifact through `stand-pkg`.
- `package-remove ID` removes that artifact through `stand-pkg`.

Document editing preserves the invoking identity. The installation operations
reach the same privileged declaration broker as other installation tools,
including when the editor itself is invoked as actual root. The editor has no
extra sudo authorization and cannot make document editing privileged on behalf
of an ordinary user.

## Expected tests before observation

For each frontend at both identities (ordinary user invoking its allowed sudo
frontend, and actual root), add a valid row, require successful application,
inspect the designated declaration for the exact row and its successful report,
then inspect actual state and remove the row. Require declaration absence and
actual absence afterward. For userdel/groupdel prepare with their add counterpart.
For timers, prepare an existing declared service; remove the timer before service.
For sockets prepare the existing declared service. Use existing valid service,
account, nft, Wi-Fi saved and Bluetooth prepared fixtures. Radio profile success
is not evidence of connection or pairing.

Negative tests: supply an account row to nft; request deletion of an account via
nmcli; replace a factory row; request a group conflicting with an existing
account; attempt a nonempty independent group. Each must fail without a changed
declaration or actual setting. Record declaration digest before/after.

Editor test: write a document, append another line, read and compare exact bytes.
Install an artifact with executable bytes, verify declaration and on-disk hash,
run the declared entry, remove through editor and inspect absence. Repeat the
installer portion as actual root. Negative test: alter the artifact bytes without
changing the declared digest; require failed install and unchanged actual state.

Run these fixtures on a fresh VM and again after complete image rebuild. The
module's syntax or an isolated mocked dispatch check cannot substitute for those
VM tests.

## Explicit limitations

Native administrative executables remain at their existing canonical paths.
Their root invocation can bypass these public `/usr/local/bin` adapters. No
mandatory native-backend domain or root containment claim is made. Public tool
positive tests alone cannot close that bypass. The editor implementation is a
small supplied general-purpose editor; it does not establish that all installers
embedded in all supplied general-purpose software are covered. Existing native
rights tools without positive declared adapters remain unsupported.

## Guest executable suite

`build/v4-tools-selftest.py` is a root controller for a fresh guest. It logs all
generated input rows before running tests, then runs ordinary calls through
`runuser -u stand -- stand-shell -c` with shell-quoted argument vectors; actual
root calls are direct subprocesses. It exercises all typed adapters, enabled
service/timer/socket readback, account change, independent group lifecycle,
saved/prepared radio rows, negative kind/member/hash cases, both apt aliases,
and editor operations. Every mutation records exact changed/deleted declaration
rows, durable report identity, every-line observed-state digest and failures,
and concrete required-row observation. Deletion additionally checks concrete
absence. The suite checks final declaration restoration and every-line readback.

Direct root editor writing of a temporary `/etc/stand` marker is separately
classified as breaking and immediately cleaned up; its expected success is not
mistaken for a containment failure. The suite does not test native root bypasses
or hardware radio effects, and does not replace language/application suites.

The suite additionally invokes native `/usr/sbin/useradd` as actual root to create
`v4raw` (UID 1998, no home creation, nologin shell). Before invocation it logs the
required property and the architecture's predicted bypass separately. The
`boundary_result` logs account readback, absent declaration coverage and unchanged
last-success identity. Creating this unrecorded account is a failed built-in-tool
boundary (C10.1), not breaking. That boundary failure is reported independently
of the implemented-check exit status. Native deletion immediately cleans the
account and any remaining same-name group; cleanup failure fails the suite.
