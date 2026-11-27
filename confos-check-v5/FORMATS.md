# Checking formats and primitive operations

2026-11-26 UTC. UTF-8 JSON; shell entry points print JSON to stdout. Malformed
or duplicate records are errors. No Python evaluation or shell evaluation of a
JSON object is allowed. Platform-specific parsing/commands are in adapter.py.

## Declaration and derivation

`derive --declaration FILE [--fixture-packages DIRECTORY]` accepts
`{"schema":1,"lines":[...]}`. Each line has a unique `id`.

- `file`: path, text, mode (four octal digits), uid, gid. Derive exact content hash.
- `object`: explicit `object` with kind, id and value map. Only fields named by
  the declaration are promised; omitted account IDs do not become promises.
- `package`: name, version, source_sha256, recipe_sha256, archive,
  archive_sha256. The package reader checks the archive and obtains its contents
  without reading a machine. Test tar readers are fixture-only, not confpkg.
- `open-folder`: path and scope (`execute`). Resolved containment, not prefix
  matching; executable material does not exempt arbitrary computer settings.
- `external-accounts`: exact named source; source provenance is observed at
  actual account lookups. A fabricated list cannot satisfy this line.
- `binding`: a named slot filled from the release/interface before a run. It
  always emits an underived error until resolved. It is not a native line.

Result: `objects` (kind, id, value, owners), `errors`, `openings`, semantic
`declaration_sha256`. Shared contributions retain all owners; conflicting
requirements stop derivation. Native-byte law identities are separate from
semantic hashes. Build outputs whose exact bytes are not promised may differ
between independent builds; local package-content hashes still identify what
actually runs. Source and recipe identity are always compared when named.

## Independent inventory

`inventory --fixture-root TREE [--force FILE]` is the runnable fixture entry.
It scans ordinary files without following symlinks; it is not a disk mount tool.
Native image/filesystem and live capture are adapter bindings (A05/A10).

An inventory has `objects`, `errors` and `coverage`. Every object is
`{"kind":KIND,"id":ID,"value":{...}}`. Stored files record mode/uid/gid and
sha256; symlinks their target. Processes and ports carry actual `exe_sha256`
and `exe_evidence` obtained through the process's namespace root, not just an
executable pathname or an ownership ledger. Settings record native effective
values, independently read from files, kernel interfaces or actual tool queries.

Required coverage keys: stored, process, port, account, group, access, service,
network, saved-network, mount, module, sysctl, locale, time, hostname, wifi,
bluetooth. Each is `{"status":"complete","evidence":"RELATIVE-EVIDENCE"}`;
`not-applicable` additionally requires an absence reason and independent probe.
A missing query, unreadable file, partial scan or unstable snapshot is an error.
Do not replace failures with empty lists. Inactive generations require separate
classification and review evidence; do not silently discard them.

Personal material/program records need `classification`, `origin_evidence`,
`route_evidence` and nonempty `routes`. Each route names kind direct/data/values,
observed, executed, and any installation/configuration effect. A direct execution
cannot be excused merely because the file resides in home. Data routes and
value readers follow review R4/R5; execution by a personally recorded reader
follows Q4/R10 and is tested separately. Opened material needs resolved_path
and actual route evidence. No blanket home, tmp, cache or log exemption exists.

## Native binding (release 0.66)

`bindings/release-0.66.json` maps every binding slot of the semantic declarations
to native lines and input files, or to `unsupported` with the documented reason.
`bindings/commands-0.66.json` holds tokens, typed preludes, the command of every
variant, probes (exit 0 present, 1 absent, other unobservable), X-REC requests,
removal/change targets and the files of the case-controlled server. BINDING.md
describes each operation; adapter_native.py and adapter_disk.py implement them.

## Comparison

`compare --derived FILE --inventory FILE` outputs outcome and issues:
UNRECORDED, MISSING, DIFFERS, UNVERIFIED, UNDERIVED, UNDECIDED. UNDECIDED is given
only to an object classified `inactive-generation`, `system-store` or
`kernel-automatic` that names its question (QUESTIONS 9, 10) and that the derivation
does not expect; it makes the outcome undecided when nothing fails and nothing is
unobserved. Objects of the system partition: `system-archive` (id
`/system/packages/FILE`, value name, version, recipe_sha256, sources), `release-tree`
(id the release, value manifest: SHA-256 of the sorted lines `path NUL kind NUL
sha256-or-target NUL x-or-dash` of `recipes/`, `files/`, `tools/`), `release-source` (id
the file name, value sha256), `system-store` (the selected generation, `boot.cfg`,
`state/applied`, other entries). Those a line brings are derived and compared like any
object; a missing one is MISSING when the stored capture is complete. A concrete violation fails;
missing/underived evidence cannot pass. Fixtures exercise both directions of
process attribution, data routes, folder boundaries, missing probes and shared
ownership. An inventory after apply creates P1/P2/UND companion rows; other
checkpoints create P1/UND. Before-reboot pipeline inventories are evidence only.

## Scenario requests, captures and checks

`plans.json` is generated from casedefs.py. Each case has id, statement labels,
purpose, kind, steps, optional variants and origins (stand IDs). Each step has
unique name, request and checks. `{"ref":"step.field"}` refers to an earlier
capture; unknown references never coerce to an empty value.

Requests use the following operation vocabulary. These are adapter method
contracts, not shell command names. Native command text must be recorded with
each performed operation and frozen in the binding addendum before run 1.

| Operation | Input / required raw capture |
|---|---|
| fresh, fresh-from-law, two-clean-builds, clone-disposable | Named semantic declaration/source lock; source hash, build command/output, image identity, boot identity and clean provenance. Two-clean-builds must have separate build logs and roots. A clone is allowed only for explicitly disposable breaking, never REPRO. |
| command | user/root role, shell text and variant; actual command, returncode/stdout/stderr, start/end time. No host fallback. A timeout is a capture failure, not a refusal. |
| put-material | Named local source and guest target; bytes/hash and result of transfer. Material setup does not itself record a program. |
| edit, split-declaration, record-if-refused, record-removal-if-refused, record-radio-if-needed | Native candidate bytes before/after and exact intended semantic delta; never advance committed state. Refusal branch writes explicit intended lines by the person. |
| read-law | candidate or committed, raw externally read bytes, native sha256, parsed semantic declaration; candidate also expected_status. Committed read must identify boot-selected generation. |
| apply, start-apply, finish-apply | Actual command output and exit, old/new boot IDs, exact final status; asynchronous handle for interrupted install. The completion must agree with candidate hash. |
| apply-cut | Watch exact reported success, cut power then boot; record status and cut timestamps and transport evidence. cut_after_success must be computed from recorded times, never asserted by the guest. |
| restart, boot, read-boot | Native boot/stop commands, old/new boot identity. Restart is not merely a disconnected SSH session. |
| network | Host-side QMP link down/up on owned machine, reply and transfer progress; source server throttling is fixture-controlled. |
| inventory | Independent whole stored/live capture in the format above, including raw query outputs and coverage evidence. |
| query | Subject from plans.json; raw underlying observations plus value. Values such as absence are computed from successful probes, never from missing tools. Cross-machine equality and candidate deltas must retain both operands for independent checking. |
| prepare-change, prepare-removal, prepare-shared, select-update-start | Explicit prerequisite lines/application and payloads; raw preparation evidence, not a waived precondition. No assertion is satisfied by naming the requested change. |
| tool-request | Native installation/configuration tool, user/root, exact request and returncode/output; independently read candidate/active state after it. |
| container, guest-system | Real guest facility; actual commands, observed namespace/process/host boundary, not host-side simulation. |
| external-server | Case-controlled account source state and actual lookup traffic; no invented account database result. |
| radio-request | Actual connect/pair command; preserve credentials only in private evidence and publish redacted command/output with hashes. |
| raw-root-write, review-event | Disposable guest raw write and observed effect; later independent review decision and its evidence. No automatic exclusion of root mutations. |
| derive-inputs | Host derivation before machine access; actual allowed input list and access-isolation evidence. No implementation reference installation may supply expected values. |

Checks support eq/ne/match/not-match/contains/gt/in. Missing fields are unobserved.
A check with `alternative` and a question ID can report undecided when only that
reading holds. Each failure remains even if a later check succeeds. The engine
stops dependent steps after failed prerequisites and emits unobserved rows for
them, including all checkpoint companions.

Transcript fixtures have `events: [{request: EXACT_REQUEST, reply: RAW_CAPTURE}]`;
`unavailable: REASON` replaces reply for missing facilities. Mismatched requests,
unused events and missing captures are errors. This proves checker behavior only.
`availability: unsupported` in a raw response requires documented reason and is
unobserved, distinct from a tool's actual refusal. No fixture is an OS observation.

## Reports, privacy and publication

One row per case summary and per check, with the four outcomes. JSON evidence
keeps actual commands and outputs; report.md includes counts and reasons.
`request_entries` emits one entry for every fail/unobserved row. A final hypothesis
0 requires the argument/review of the plan; the engine's operational 0 only means
some check failed. Logic rows, raw text outcomes and strict-plan review R8/D1–D6
outcomes are kept distinct. No final acceptance is performed by these programs.

Machine-specific transport, credentials, paths, addresses and radio endpoints
belong only in unpublished local.env. Exported raw evidence must be checked and
redacted before publication. The portable declarations and scripts
contain only symbolic binding tokens and synthetic guest paths.

Relational query values are computed in core.evaluate_query, ignoring a bare
adapter `value`: equality needs left/right operands and their evidence; exact
request deltas need before/after line sets and frozen expected additions/removals;
system update needs old/new source identities for a frozen set of actual system
components; independent builds need distinct work/log identities with matching
release source and evidence of clean, non-cloned builds. apply-cut ordering is
computed in engine.py from captured monotonic timestamps. StandTransport provides
executable SSH user/root commands, exact status parsing and verified candidate
writes against the stand; it is not selected by the part-1 CLI. Disk/lifecycle
bindings remain explicitly unavailable until the new interface is read.
