# S6-O log (second party, supplement 1, step 6)

Times UTC. Paths relative to this folder unless stated. “Laboratory” = the server laboratory directory
`VMs/cal-1123/stand/` relative to the server account's initial directory.

## 18:01–18:05 Verification before any case

- Gate (not published: orchestration or scratch): commit `c0de5e63d4cf0814608d543b6eb8942e2b08d386`, 2026-11-23T18:00:34Z, names
  CASES-6.md sha256 `729f1b9d…8cc025` and COMPARE-6.md sha256 `6ef2f674…38dc`.
- Local `check-inputs-v4/supplement-1/step-6-cases/B2/CASES-6.md` and `check-inputs-v4/supplement-1/step-6-cases/B2/COMPARE-6.md`: both equal the gate (sha256sum at 18:01).
- Image at top of CASES-6.md `1b581030…980eca`: laboratory `base/stand.qcow2` equals it, mode 0444
  (`raw/verify/server-checksums.txt`).
- Laboratory seal `raw/round-4-prep/inputs-seal.json` (sha256 `42317d32…7840124`, copy `raw/verify/inputs-seal.json`):
  181 sealed files, 0 mismatches on the laboratory (`raw/verify/server-checksums.txt`); every declaration SHA-256 in the
  CASES-6 table equals its seal entry.
- Public record: remote `main` = `c0de5e63…`; the 89 files of the commit under `step-6-cases/B2/` equal the sealed bytes,
  0 mismatches; local B2 copies equal the seal (`raw/verify/published-vs-seal.txt`). Unauthenticated public fetch of
  CASES-6.md and COMPARE-6.md at that commit returns the gate checksums (`raw/verify/public-fetch.txt`).
- Not in the public commit (sealed locally only): the runner `build/bc4-run-case.py`, the collector
  `build/bc4-compare.py`, `lab.py`, the seal file itself and 88 other recipe/records files. The commands and queries are
  published as prose in CASES-6.md and COMPARE-6.md. Recorded as a question; it is not a checksum difference, so the
  cases are run.
- Decision: no checksum differs → the cases are run.

## 18:03 Case 1 — expected observation (written before the run)

Publication record placed at laboratory `raw/round-4-prep/publication.json` (keys public_record_url, commit
c0de5e63…, inputs_seal_sha256 42317d32…). Expected (SUP1/step-6.md): both fresh guests (left, right) report a complete
successful application of case-1 (sha256 8a98779d…); both snapshots show current machine bytes identical to the
requested ones and every declared value equal to its native observation; the host `diff` of the two snapshots shows no
difference in any declared value under any line (program file checksums/permissions, unit enablement/checksums, account
tuples, rule text). Differences only in undeclared diagnostics (PIDs, nft handles, profile listing order) may appear and
are recorded. Command: CASES-6 `systemd-run --user --unit=bc4-second-case-1 … python3 build/bc4-run-case.py 1 --publication raw/round-4-prep/publication.json`.

## 18:03–18:06 Case 1 — observed (service exit 0, Result=success)

Both guests: `COMPLETE SUCCESS 8a98779d…` (raw/case-1/{left,right}-apply.stdout); all collectors exit 0; no
failure.json; cleanup: no remaining guests. Required vs observed (tools/judge.py fulfil): 0 mismatches on each guest,
apart from 2 lines the collector cannot decide from inside the guest (boot, code-boundary) — raw/case-1/judge-*-fulfil.json.
First reader run reported 204 dpkg mismatches: an artefact of my reader (multi-arch qualifier `:amd64` in the line name,
absent from dpkg-query ${Package}); fixed in the reader and rerun on the same saved files — no guest command repeated.
Pair diff: 8 differences (raw/case-1/pair-diff.stdout, judge-pair.json, tools/detail.py, tools/sscheck.py): 11 ss
outputs differ only in line order; kernel profile listing differs only in order (same 119 lines); last-success and five
filesystem success reports differ only in application time. Host VM argv identical apart from per-guest paths and the
forwarded host port (raw/case-1/{left,right}-qemu-argv.json).

## 18:08 Case 2a — expected observation (written before the run)

Expected (SUP1/step-6.md): no difference. Concretely: left installs alpha then beta, right beta then alpha, each
install succeeds; pre-final diagnostics may show the account tuples; the final application of case-2a (sha256 fdf0bc71…)
reports COMPLETE SUCCESS on both; the last-applied complete hash equals fdf0bc71… on both; bc4alpha = UID/GID 2201,
bc4beta = UID/GID 2202, own primary group only, /usr/sbin/nologin, /home/NAME, GECOS as stated, on both; every line
fulfilled; pair diff shows no difference in any stated value. Command: CASES-6 `systemd-run --user --unit=bc4-second-case-2a … bc4-run-case.py 2a …`.

## 18:08–18:14 Case 2a — observed (service exit 0, Result=success)

Order (raw/case-2a/commands.json): left alpha→beta, right beta→alpha; all four installs `SUCCESS`. Pre-final
diagnostics identical on both: bc4alpha 2201/2201, bc4beta 2202/2202, own group only, nologin, /home/NAME, stated GECOS.
Final application `COMPLETE SUCCESS fdf0bc71…` on both; last-applied complete hash fdf0bc71… on both. Required vs
observed: 0 mismatches apart from boot and code-boundary (undecidable by guest readback). Pair diff: 8 differences — 6 ss
outputs differ only in line order, kernel profile listing only in order (117 lines), last-success `time_utc` and five
success reports `utc_epoch` (tools/reports.py). No guest destroyed late; no remaining guests.

## 18:14 Case 2b — expected observation (written before the run)

Expected (SUP1/step-6.md, CASES-6): no installation, no VM; the runner writes `not-expressible.json` stating that the
declaration format admits no account line without a numeric identifier; the case gives “?” (“A case that cannot be
expressed or performed gives “?”.”). Command: CASES-6 `python3 build/bc4-run-case.py 2b --publication raw/round-4-prep/publication.json`.

## 18:14 Case 2b — observed

Runner exit 0, no VM; `raw/case-2b/not-expressible.json` as expected. Source read (no probe): `B2/build/stand.py` line
94 accesses `r['uid']` for every managed account and requires 1100–60000; line 118 `expected_account` requires `uid`
and `gid`; `bc3_account_rows.py` lines 61–72 emit numeric uid/gid for every account database entry.

## 18:14 Case 3 — expected observation (written before the run)

Expected (SUP1/step-6.md): nothing the removed lines contributed is in force. Concretely: before — case-3-before
COMPLETE SUCCESS; stand-development.service active/enabled with a running worker (`--wait`) process; the ordinary-shell
launch of the worker succeeds (exit 0). After the single application of case-3-after (sha256 41299a86…): COMPLETE
SUCCESS; former worker PID either gone or not the same starttime, or a zombie — not running; no holder of the worker path;
`systemctl is-enabled` not `enabled` (not-found or disabled), unit inactive, unit file absent (stat fails); nft table has
no rule with comment dev-rule and no `tcp dport 17777 drop` text; worker `stat` fails; ordinary-shell launch fails
(non-zero, not found or denied); every remaining line fulfilled. Command: CASES-6 `systemd-run --user --unit=bc4-second-case-3 … bc4-run-case.py 3 …`.

## 18:14–18:17 Case 3 — observed (service exit 0, Result=success)

Before: COMPLETE SUCCESS 8a98779d…; service active/enabled, MainPID 1534; worker holder PID 1538 starttime 5173, argv
`… --wait`, exe under /var/lib/stand/code-root/; ordinary launch exit 0, output `development-version-1`. Removal:
COMPLETE SUCCESS 41299a86…. After: former identity 1538 `exists: false`; no holder of the worker path;
`is-enabled` → `not-found` (exit 4); MainPID 0, inactive, no FragmentPath; nft table holds only the chain, no 17777, no
dev-rule; stat of worker and unit file: No such file (exit 1); ordinary launch exit 127 `No such file or directory`;
launch table, kernel profiles stand-run-458181eb…/281b3a23… (worker, service) and filesystem declared paths no longer
hold the removed names (tools/case3.py, tools/case3b.py). Required vs observed before and after: 0 mismatches apart from
boot and code-boundary. Limit: the committed queries do not read /var/lib/stand/code-root after removal; the testbed's
own verifier (code-boundary OK, which includes exact code-root membership, B2/build/codeboundary.py lines 154–157, 207–208)
is not an independent observation.

## 18:18 Case 4 — expected observation (written before the run)

Expected (SUP1/step-6.md): stage both — COMPLETE SUCCESS b7446497…; bc4-shared v1 registered with origins from both
owners; bc4-owner-a and bc4-owner-b registered. Stage one (owner-a removed) — COMPLETE SUCCESS dbfd73cf…; owner-a not
registered; owner-b registered and its line fulfilled; bc4-shared still registered, origin only owner-b. Stage none —
COMPLETE SUCCESS 126c4c96…; no registration of bc4-shared, owner-a or owner-b; remaining lines fulfilled.
Command: CASES-6 `systemd-run --user --unit=bc4-second-case-4 … bc4-run-case.py 4 …`.

## 18:18–18:22 Case 4 — observed (service exit 0, Result=success)

both: COMPLETE SUCCESS b7446497…; bc4-shared v1 origins bc4:owner-a and bc4:owner-b; both owners registered.
one: COMPLETE SUCCESS dbfd73cf…; bc4-shared v1 origin bc4:owner-b only; owner-a not registered; owner-b registered.
none: COMPLETE SUCCESS 126c4c96…; no registration of bc4-shared, owner-a, owner-b; ledger names no `bc4-`/`bc4:`.
Required vs observed at each stage: 0 mismatches apart from boot and code-boundary (raw/case-4/judge-*-fulfil.json,
tools/case4.py). Staged inputs in every guest equal their sealed hashes (raw/case-*/*source-identities.stdout).

## 18:23–18:25 Closing

Server: `lab.py list` empty, no bc4-second guest directory, no QEMU process; the four services inactive, exit 0
(raw/cleanup-final.txt). Laboratory evidence kept in `raw/round-4-second-party/` (CASES-6 “Records”). Local copies: the
owner name removed from five publication.json copies (raw/publication-original.sha256); 22 files over 1 MB zstd-compressed
after recording their SHA-256 (raw/LARGE-ORIGINALS.sha256); file names in this log ending in `.stdout` for those
files now end in `.stdout.zst`. Result: RECORD.md; questions: QUESTIONS.md.
