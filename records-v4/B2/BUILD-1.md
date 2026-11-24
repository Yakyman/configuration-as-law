BUILD 1: 2 variants closed in this round, 2 of 88 closed in all

Recorded 2026-11-23 UTC. Scope: exactly Round 1's 65 variants in
[ROUNDS.md](ROUNDS.md). This is a partial implementation and builder self-test,
not acceptance of the complete testbed or a published hypothesis check.
Outcome: `?`. The rebuilt full run and independent review completed. C5.4 and C10.4 are CLOSED; the other 86 variants remain NOT CLOSED.

## Built

- Ordinary Bash login with free commands, arguments, pipelines and redirection;
  writable documents; an exactly recorded personal script. Existing AppArmor
  native execution/mapping rules are inherited by ordinary descendants.
- Common declaration transactions for typed account/group, service/timer/socket,
  rule and saved radio-profile tools, package reinstall/downgrade aliases, and
  the installer part of the supplied document editor. Tests use ordinary Bash
  and actual root and inspect exact rows, durable reports, state and removal.
- A general cgroup v2 freezer gate around application. It preserves original
  cgroup ancestry, waits for kernel acknowledgement, and restores callers only
  after the durable report or successful recovery. It replaces the failed
  SIGSTOP design without an editor-specific execution workaround.
- Complete scratch recipe, separate v4 tests, explicit compatibility adapter
  for carried tests, and frozen source/evidence snapshots. No historical
  version 3 closure is silently inherited.

Mechanisms and strict reading are in [STAND.md](STAND.md); operational commands
are in [HOWTO.md](HOWTO.md). The [coverage map](raw/round-1/COVERAGE.md)
records each Round 1 variant's actual attempt and limit. Variants owned by other
rounds remain assigned there without a Round 1 gap analysis.

## Closed variants

| Variant | General mechanism | Attempt and observed refusal |
|---|---|---|
| C5.4 | Root-owned, exactly declared native files; inherited AppArmor/Unix write restrictions; authorized replacement goes through the common declaration transaction | `recorded-native-overwrite` attempts ordinary replacement of the installed worker. It returns permission denied; SHA-256, mode 0755, UID/GID 0, covering row and successful report remain unchanged. |
| C10.4 | The supplied general-purpose editor preserves caller identity for document operations and routes its documented installer through the common package broker, including actual root invocation | Ordinary and root document write/append/read and exact install/run/remove pass; bad-hash installation refuses and preserves the previous declaration/report and 553 clean readback rows. Direct privileged general editing remains permitted breaking. |

These are bounded claims about the recorded-file mechanism and supplied editor,
not every foreign editor/plugin or process race. [Component review](raw/round-1/REVIEW-FINAL2-TOOLS.md)
accepted them conditionally; the [final review](raw/round-1/REVIEW-FINAL.md)
accepted both after the whole rebuilt suite and independent replay completed.

## Fresh-machine evidence

The final recipe adds nine files and changes nine carried files; all original
carried self-test sources remain unchanged. The
[source comparison](raw/round-1/final-2-source-provenance.json) and
[frozen recipe hashes](raw/round-1/final-2-source-sha256.json) identify every file.
The final primary recipe rebuilt from scratch at 09:34:50–09:36:22 UTC, after
the general freezer correction. The independent peer recipe rebuilt at
10:32:19–10:33:50 UTC from the same frozen inputs.

| Final rebuilt-image observation | Result | Evidence |
|---|---|---|
| Actual Bash, document/browser work, recorded personal script, native refusals and saved-input attempts | 28 Boolean assertions: 22 pass, six saved-code boundary failures | [shell](raw/round-1/final-2/shell.jsonl) |
| Unsaved HTTP pipe execution followed by reboot | Executed contribution absent after reboot; one assertion passes | [reboot](raw/round-1/final-2/shell-reboot.jsonl) |
| General application freezer and nested broker/editor callers | 9/9 pass | [gate](raw/round-1/final-2/gate.jsonl) |
| Ordinary and actual-root typed tools and editor installer | 85/85 implementation assertions pass; one separate native-root account bypass fails the boundary; final 553/553 readback clean | (not published: direct evidence at least 2 MB), [readback](raw/round-1/final-2/tools-verify.log) |
| Supplemental direct Bash input paths | 17 Boolean assertions: 12 pass, five saved-code failures | [direct](raw/round-1/final-2/supplement/direct.jsonl) |
| Supplemental startup, editor, JIT, dispatcher and memory paths | 16 Boolean assertions: 12 pass, four saved-code failures; runtime and unavailable observations remain separate | [extra](raw/round-1/final-2/supplement/extra.jsonl) |
| Supplemental reboot continuity | All 553 readback rows and the success report remain byte-identical | [reboot comparison](raw/round-1/final-2/supplement/reboot.json) |

These new and supplemental logs contain 157 Boolean observations: 141 pass and
16 retain real boundary failures. This accounting does not turn finite passes
into whole-variant closure. The complete carried controller exited zero at
12:15:26 UTC: language 79/79, application/container 131/131, system 32/32,
ordinary work 59/59, transaction 35/35, power cuts 9/9, authority/frontend
166/166 and code/lifecycle 133/133. Boot admission refused all 205 pre-readiness
ordinary attempts. The original D01–D10 controller exited zero. The independent
build comparison reports identical declaration bytes and all 557 actual rows
equal. See [carried evidence](raw/round-1/final-2/carried-suite).

The final primary image is read-only mode 0444 with SHA-256
`3ad3bbaa805b65fb0f65487d15ca77a3702df04298fdfec3b5efeb254520ec21`.
The complete combined declaration has 572 rows and SHA-256
`7a5c9116f501dc280e1681970d1489c97b009509cc14e0c4048a82123d3b7284`.
Combined replay completed at 12:23:04 UTC: all 24 assertions pass, eleven
ordinary channel launches and the scheduled command succeed on each image,
all 572 rows verify before/after each reboot and compare equal, and exact
declaration bytes survive both reboots. The main controller reports all
22 steps successful, no owned guest and no temporary peer remaining.
The independent peer image SHA-256 was
`b07ba3412ad2c975287e352247e1da2c666a058ddab24197df30816c1517afa3`
before deletion. The different disk hashes are not claimed to be bit-for-bit
image reproducibility; exact declaration bytes and observed values are compared.
Final evidence validation, image adoption and separate review follow below.

## Failed attempts and limits

The first candidate's editor application completed, but its unconfined caller
remained stopped after the confined child exited. The preserved
[process evidence](raw/round-1/final-1/editor-stall-process.txt) and
[interruption](raw/round-1/final-1/interruption.json) prompted the
[general freezer correction](raw/round-1/FREEZER-CORRECTION.md). The incomplete
candidate is not a whole-suite pass. The earlier development run was explicitly
interrupted when the complete candidate superseded it; its source and partial
outputs remain preserved.

Saved uncovered script, sourced, piped, imported, serialized, startup, editor,
JIT and custom-dispatch inputs can still execute. Exact marker outputs and
unchanged declaration/report identities are retained, not converted into
successful refusals. Canonical native root account administration also bypasses
the declaration: that is a built-in-tool failure, not breaking. Direct root
general editing is separately classified as breaking and was not blocked.

Native mapping/overwrite refusals do not establish a saved-input boundary.
Unavailable tool paths remain UNTESTED. Runtime-only memory restrictions do not
become invented declaration requirements. The freezer supports normal cgroups;
threaded source cgroups refuse. Its identity checks cannot make the kernel's
numeric-PID migration API atomic. No universal concurrency closure is claimed.

The earlier supplement's FFI failure label was corrected by an
[offline exact-line audit](raw/round-1/supplement-marker-audit.json): a traceback
echoed source containing the marker, while actual mapping was denied. The raw
record and executed payload are preserved. Final-2 uses the corrected detector
as part of the mandatory rebuilt-image validation.

The [independent final review](raw/round-1/REVIEW-FINAL.md) accepts the two
bounded closures and the complete evidence. The
[strict metrics](raw/round-1/metrics.json) retain all 16 true failures and confirm
carried/combined assertion consistency. The final parser fixes only source-defined
transport/phase differences; [its audit](raw/round-1/PARSER-FINAL-AUDIT.md) records
the rejected earlier validation and the exact correction. No guest run was repeated
for these host-side parser fixes.

Publication and retained-image adoption are recorded in
[publication.json](raw/round-1/publication.json),
[export-verification.json](raw/round-1/export-verification.json),
[acceptance.json](raw/round-1/acceptance.json) and
[adoption.json](raw/round-1/adoption.json). Final host cleanup is recorded in
[host-cleanup.json](raw/round-1/host-cleanup.json).
