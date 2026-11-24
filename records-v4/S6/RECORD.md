STEP 6: case 1 1; 2a 1; 2b ?; 3 1; 4 1; the step ?

# Supplement 1, step 6: record of the second party (S6-O)

Recorded 2026-11-23, 18:01–18:25 UTC, by a party that prepared neither the image nor the cases. Checked by: review
RV-S6-O. Rules: `SUP1/step-6.md` (identical to the published `cases-6/criteria/step-6.md`, SHA-256 in the seal). Paths
are relative to this folder unless they start with `B2/`, `SUP1/` or (not published: record outside selected evidence) (night folder). “Laboratory” is the server
laboratory directory. The step-by-step log, with each expectation written before its run, is [LOG.md](LOG.md).

## 0. Before the first case

| Check | Result | Evidence |
|---|---|---|
| Gate (not published: orchestration or scratch): commit `c0de5e63d4cf0814608d543b6eb8942e2b08d386`, 18:00:34Z | remote `main` of the public repository = this commit; first attempt began 18:03:03Z | `raw/verify/published-vs-seal.txt` |
| CASES-6.md SHA-256 named by the gate `729f1b9d…8cc025` | equal (local, laboratory, public unauthenticated fetch) | `raw/verify/public-fetch.txt`, `raw/verify/server-checksums.txt` |
| COMPARE-6.md SHA-256 named by the gate `6ef2f674…38dc` | equal (local, laboratory, public) | same |
| Image SHA-256 at the top of CASES-6.md `1b581030…980eca` | equal; mode 0444 | `raw/verify/server-checksums.txt` |
| Seven declaration SHA-256 in the CASES-6 table | equal to seal, laboratory files, published files and to `sha256sum` inside every guest after staging | `raw/verify/inputs-seal.json`, `raw/case-*/*source-identities.stdout` |
| Laboratory seal: 181 files | 0 mismatches | `raw/verify/server-checksums.txt` |
| 89 published files under `step-6-cases/B2/` | 89 equal to the seal, 0 mismatches | `raw/verify/published-vs-seal.txt` |

No checksum differed, so the cases were run. Not part of the public commit: the runner `build/bc4-run-case.py`, the
collector `build/bc4-compare.py`, `lab.py` and the seal file itself (sealed locally only); the commands and the queries
are published as text in CASES-6.md and COMPARE-6.md. See QUESTIONS.md, item 2. The runner requires a publication
record; this party wrote it at the laboratory `raw/round-4-prep/publication.json` from the facts verified above (public
URL, commit, SHA-256 of the seal `42317d32…7840124`); copies with the owner name removed: `raw/case-*/publication.json`,
original checksums in `raw/publication-original.sha256`.

Each case was attempted once, by the CASES-6 commands, in the CASES-6 order, each service finished before the next
started. Nothing was repaired or repeated. All guests were destroyed by the runner (`raw/case-*/cleanup.json`:
`remaining_owned_guests: []`); `lab.py list` empty, no guest directory and no QEMU process left (`raw/cleanup-final.txt`).
Large outputs are zstd-compressed (`*.zst` (some matches not published: direct evidence at least 2 MB) (some matches not published: direct evidence at least 2 MB)); SHA-256 of every original: `raw/LARGE-ORIGINALS.sha256`.

How required values were compared with native observations: `tools/judge.py` (offline, on the saved collector
outputs). Its first run on case 1 reported 204 package mismatches that were an error of this reader (a line names a
multi-arch package `name:amd64`; `dpkg-query ${Package}` prints it without the qualifier). The reader was corrected to
strip the qualifier only when it equals the stated architecture and run again on the same saved files; no guest command
was repeated. Two lines cannot be decided by readback from inside a guest on any case: `boot` (`order: ["disk"]`,
`guest_can_change: false`) and `code-boundary` (a prose requirement; COMPARE-6 “Limits”). They are listed per case.

## Case 1 — reproducibility (Appendix A.4.4)

- **Commands.** `systemd-run --user --unit=bc4-second-case-1 … python3 build/bc4-run-case.py 1 --publication raw/round-4-prep/publication.json`
  (CASES-6); in each of two fresh guests `left`, `right`: `bc4_bundle.py apply …/case-1`, `cat complete-last-success.json`,
  `bc3-state.py export`, `bc4-compare.py snapshot --bundle …/case-1/declaration.json`; on the host
  `bc4-compare.py diff left right`. Exact argv/stdin/UTC: `raw/case-1/commands.json`. Service exit 0.
- **Expected** (written before the run, LOG.md): no difference in any stated value; every line fulfilled.
- **Observed.** Both guests `COMPLETE SUCCESS 8a98779d…` (`raw/case-1/{left,right}-apply.stdout`), 1,370 filesystem paths
  verified by the testbed. Independent readback: current `machine.jsonl` byte-identical to the requested one; all eight
  primary files byte-identical; every filesystem path with no declared-field difference (including stated timestamps,
  sizes, xattrs); all five filesystem declarations stable during readback; every line's stated values equal their native
  observations on both guests (`raw/case-1/judge-{left,right}-fulfil.json`: 0 mismatches) — except `boot` and
  `code-boundary`, not decidable by readback. Host VM argv of the two guests: identical except per-guest file paths and the
  forwarded host port; one disk drive, no boot option (`raw/case-1/{left,right}-qemu-argv.json`). For `code-boundary` the
  loaded kernel policy bytes, policy sources and launch table are identical on both guests (no difference in the pair diff).
- **Every difference found by the comparison** (`raw/case-1/pair-diff.stdout`, 8 entries; `raw/case-1/judge-pair.json`,
  `tools/detail.py`, `tools/sscheck.py`, `tools/reports.py`):
  1. `/evidence/commands`: 11 `ss -H -lnt`/`-lnu` outputs differ only in the order of their lines (same lines).
  2. `/rows/code-boundary/observed/kernel_profiles`: the 119 listed profiles are the same; only their listing order differs.
  3. `/evidence/last_success`: only `time_utc` (time of application).
  4–8. `/filesystems/{etc,home,shm,tmp,vartmp}/success_report`: only `utc_epoch` (time of application).
  None of them is a value stated by a line or a value listed by A.4.4 (file checksums/permissions, enablement and unit
  checksum, account tuple, effective rule text); the listener lines' stated value `listening` is equal on both.
- **Outcome: 1.** Nothing counts against the hypothesis: what is in force under the lines does not differ between the two
  installations. No argument for 0 was needed or written. Limits retained: `boot` `guest_can_change` and the
  `code-boundary` prose are not observed as such; their observable implementation (host argv, kernel policy bytes) is
  identical on both machines.

## Case 2a — a different order, identifiers stated

- **Commands.** `systemd-run --user --unit=bc4-second-case-2a … bc4-run-case.py 2a …`. Left: `stand-pkg install
  …/package-alpha.json`, then `…/package-beta.json`; right: beta, then alpha; both then `getent passwd bc4alpha bc4beta`,
  `id bc4alpha`, `id bc4beta`, `getent group bc4alpha bc4beta`, `bc4_bundle.py apply …/case-2a`, `cat
  complete-last-success.json`, `bc3-state.py export`, `bc4-compare.py snapshot …`; host `diff`. `raw/case-2a/commands.json`.
  Service exit 0.
- **Expected:** no difference; bc4alpha 2201/2201, bc4beta 2202/2202 on both.
- **Observed.** All four installs `SUCCESS` in the stated orders (`raw/case-2a/{left,right}-install-{1,2}.stdout`).
  Before the final application, identical on both: `bc4alpha:x:2201:2201:BC4 alpha account:/home/bc4alpha:/usr/sbin/nologin`,
  `bc4beta:x:2202:2202:BC4 beta account:/home/bc4beta:/usr/sbin/nologin`, each only in its own group
  (`raw/case-2a/*-accounts-before-final.stdout`). Final application `COMPLETE SUCCESS fdf0bc71…` on both; last applied
  complete hash `fdf0bc71…` on both (`*-last-applied.stdout.zst`), so the declaration last applied is byte-identical.
  Independent readback: account tuples as stated on both (name, UID, GID, groups, shell, home, GECOS); every line fulfilled
  (`raw/case-2a/judge-{left,right}-fulfil.json`: 0 mismatches except `boot`, `code-boundary`).
- **Every difference** (`raw/case-2a/pair-diff.stdout`, 8 entries): 6 `ss -H -lnt` outputs differ only in line order;
  kernel profile listing differs only in order (117 profiles, same set); `last_success.time_utc`; five
  `success_report.utc_epoch`. No difference in a stated value or in an account tuple.
- **Outcome: 1.** No argument for 0 needed or written.

## Case 2b — a different order, identifiers not stated

- **Command.** `python3 build/bc4-run-case.py 2b --publication raw/round-4-prep/publication.json` (no VM). Exit 0.
- **Expected:** not expressible; “?”.
- **Observed.** `raw/case-2b/not-expressible.json`: “Both the managed account row and the complete filesystem account
  database requirements state numeric identifiers. No omitted-identifier declaration is admitted.” Read in the source,
  without a probe: `B2/build/stand.py` line 94 reads `r['uid']` for every managed account and requires 1100–60000;
  line 118 `expected_account` requires `uid` and `gid`; `B2/build/bc3_account_rows.py` lines 61–72 emit numeric UID/GID
  for every account database entry.
- **Differences:** none (nothing performed).
- **Outcome: ?** — SUP1/step-6.md: “If the declaration format of the testbed does not admit a line without the identifier,
  2b is recorded as not expressible on this testbed.” and “A case that cannot be expressed or performed gives “?”.” The
  question about the readings of “unambiguous” (Section 8.4) was not reached; it stays open (QUESTIONS.md, item 1).

## Case 3 — removal of a program, a service and a rule (Appendix A.4.3)

- **Commands.** `systemd-run --user --unit=bc4-second-case-3 … bc4-run-case.py 3 …`. One fresh guest: apply
  `case-3-before`; snapshot; ordinary shell `/opt/stand/pkgs/dev-worker/bin/worker`; `systemctl show
  stand-development.service -p MainPID -p ActiveState -p UnitFileState -p FragmentPath`; `bc4-compare.py processes …`;
  apply `case-3-after`; `processes`; former-identity check; `systemctl is-enabled`; `systemctl show`; `nft list table
  inet stand`; `nft -j list table inet stand`; `stat` of the worker and of the unit file; ordinary-shell launch of the
  worker; snapshot `case-3-after`. `raw/case-3/commands.json`. Service exit 0. Removed lines: `dev-worker`,
  `dev-service`, `dev-rule` (`check-inputs-v4/supplement-1/step-6-cases/B2/cases-6/removed-lines.json`).
- **Expected:** nothing the removed lines contributed in force; remaining lines fulfilled.
- **Observed before.** `COMPLETE SUCCESS 8a98779d…`; service `ActiveState=active`, `UnitFileState=enabled`, MainPID 1534;
  one holder of the worker path, PID 1538, starttime 5173, state S, argv `/opt/stand/pkgs/dev-worker/bin/worker --wait`,
  exe under `/var/lib/stand/code-root/` (`raw/case-3/before-processes.stdout`); ordinary launch exit 0, prints
  `development-version-1`; the rule text with 17777 and the comment `dev-rule` present; kernel profiles
  `stand-run-458181eb…` (worker) and `stand-run-281b3a23…` (service) loaded; every line fulfilled
  (`raw/case-3/judge-before-fulfil.json`).
- **Observed after.** `COMPLETE SUCCESS 41299a86…` (`raw/case-3/removal-apply.stdout`). Former process 1538:
  `exists: false` (`raw/case-3/former-identities.stdout`); no holder of the worker path (`after-processes.stdout`);
  `is-enabled` → `not-found`, exit 4; `MainPID=0`, `ActiveState=inactive`, no FragmentPath; `nft list table inet stand`
  holds only the chain `input` (policy accept), no `17777`, no `dev-rule`, in text and JSON; `stat` of the worker and of
  the unit file: “No such file or directory”, exit 1; ordinary launch exit 127, “No such file or directory”. In the
  after-snapshot the launch table (before: two entries for the worker and the service), the loaded and exported kernel
  profiles (before: `stand-run-458181eb…`, `stand-run-281b3a23…`), the firewall chain text (before: contained 17777) and
  the declared filesystem paths (before: the unit file, its `multi-user.target.wants` link, its drop-in directory and
  file, its private tmp directory) no longer hold any of them (`tools/case3.py`, `tools/case3b.py`); the
  `/etc/apparmor.d/stand-*` policy sources and the objects ledger named none of them before or after; every remaining line fulfilled (`raw/case-3/judge-after-fulfil.json`: 0 mismatches except `boot`,
  `code-boundary`).
- **Differences / remaining contribution:** none observed.
- **Limit.** The worker ran from the code-root view `/var/lib/stand/code-root/opt/stand/pkgs/dev-worker/bin/worker`. The
  committed queries do not read that view after removal. The testbed's own verifier reported `code-boundary OK`, which
  includes an exact membership check of that view (`B2/build/codeboundary.py` lines 154–157, 207–208), but it is not an
  independent observation (QUESTIONS.md, item 3).
- **Outcome: 1.** No argument for 0 needed or written.

## Case 4 — the last owner

- **Commands.** `systemd-run --user --unit=bc4-second-case-4 … bc4-run-case.py 4 …`. One fresh guest; for each of
  `case-4-both`, `case-4-one`, `case-4-none`: apply; `bc4-compare.py package bc4-shared`, `… bc4-owner-a`,
  `… bc4-owner-b`, `cat /var/lib/stand/objects.json`; snapshot. `raw/case-4/commands.json`. Service exit 0.
- **Expected:** shared package stays after the first removal, covered by the remaining line; gone after the second.
- **Observed** (`raw/case-4/{both,one,none}-packages.stdout(.zst)`, `tools/case4.py`):

| Stage | Application | bc4-shared v1 | bc4-owner-a | bc4-owner-b | Lines fulfilled |
|---|---|---|---|---|---|
| both | `COMPLETE SUCCESS b7446497…` | installed; origins `bc4:owner-a`, `bc4:owner-b` | installed | installed | yes |
| one (owner-a removed) | `COMPLETE SUCCESS dbfd73cf…` | installed; origin `bc4:owner-b` only | no registration | installed; its required dependency bc4-shared v1 registered | yes |
| none (owner-b removed) | `COMPLETE SUCCESS 126c4c96…` | no registration | no registration | no registration | yes |

  In the last stage the objects ledger has no entry naming `bc4-` or `bc4:`. Required vs observed: 0 mismatches at each
  stage except `boot`, `code-boundary` (`raw/case-4/judge-{both,one,none}-fulfil.json`).
- **Differences / remaining contribution:** none. After the first removal the remaining line and the shared object it
  covers are in force as required (P2); after the second, nothing remains.
- **Outcome: 1.** No argument for 0 needed or written.

## The step

By SUP1/step-6.md: no case gives 0; case 2b gives “?”; so **the step: ?**. This step observes reproducibility and
removal only in these cases; its outcome is not the outcome of check 2 or check 3. No argument from the definitions
alone was written, because no case had an observation counting against the hypothesis; its absence is recorded here as
the task requires. No gap of the text was found by performing the cases; the open author reading for 2b is not decided.

## Comparison with the expected result of SUP1/step-6.md (not adjusted)

| Expected (step-6.md) | Observed | Met |
|---|---|---|
| case 1: no difference | no difference in any stated value; 8 differences only in listing order and application time | met |
| case 2a: no difference | no difference; accounts 2201/2202 identical in both orders | met |
| case 2b: identifiers differ, or the line not expressible | not expressible | met (second alternative) |
| case 3: nothing the removed lines contributed in force | nothing in force by every committed query | met |
| case 4: object stays after the first removal, covered by the remaining line, gone after the second | exactly so | met |
