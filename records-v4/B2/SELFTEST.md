# Round 3 — Supplement 1, step 5 single image

Recorded 2026-11-23 UTC. The final image was rebuilt from scratch, and its
seventeen targeted builder cases finished at **15:13:26 UTC**: **15 automatically
recorded saved-code executions, 15 same-code/same-command permitted successes,
native root account change recorded and applied, ordinary work done in one
session**. Literal denied commands: **0**. The validation controller finished at
**16:56:44 UTC with exit 1**: the carried code/lifecycle scenario stopped at FIFO
creation. Its 59 still-available suffix observations passed in a separate fresh
guest; FIFO remains unavailable and the original suite remains incomplete.
These are builder self-tests; the separate performance and review are
pending. Hypothesis/step outcome: `?`.

The image SHA-256 is
`5641c3c34e08dba60ae7f97511fae33d4dde48dba0ef5d93db93ab6faeb3cb79`.
Its complete frozen-disk declaration SHA-256 is
`4fd6f7acbc4e9d110dbd3513b4b42aace2b775d99f9f90341f86fb64e33bda57`.
[BUILD-3.md](BUILD-3.md) gives per-way mechanism and evidence, limitations and
handoff. (not published: record outside this collection) fixes all seventeen second-party commands and
observations on fresh copies; [inputs-seal.json](raw/round-3/inputs-seal.json)
freezes the inputs locally. Public commitment remains pending and must precede
those independent attempts. No second-party attempt has been performed here.

## Round 3 targeted validation

Evidence paths below are relative to `raw/round-3/`.

| Stage | Observed result | Evidence |
|---|---|---|
| Initial integration build | Failed factory capture with systemd/DBus timeout; no case result | `development-1/build.log`, `development-1/build-result.json` |
| Development scratch rebuild | Completed; all 17 builder cases pass | `development-2/`, `development-2-validation/cases.jsonl` |
| Final scratch rebuild | Completed; final image read-only | `final-1/build.log`, `final-1/build-result.json`, `final-1/image.json` |
| Independent peer scratch rebuild | Completed before full-suite lanes | `final-1-validation/peer-build.log` |
| Fifteen exact original ways and permitted counterparts | 15 recorded attempts and 15 permitted successes; 0 literal denials | `final-1-validation/cases.jsonl`, all case_result records through line 87 |
| Native root account tool | Exact original argv; full expected tuple equals its own declaration row | `final-1-validation/cases.jsonl`, lines 88–89 |
| Ordinary session | Every required action succeeds in one shell session | `final-1-validation/cases.jsonl`, lines 92–93 |
| Filesystem readback | 1,379 paths; zero mismatches | `final-1-validation/cases-filesystem-verify.jsonl` |
| Case evidence consistency | 112 snapshot references, 24 unique snapshots, no inconsistencies; explicit observational limits | `final-cases-audit.json` |
| Frozen-disk description | Eight exact constituent files; read-only extraction without boot | `final-1/offline-declaration/identity.json` |
| Installed source identity | Six local BC3 source/fixture files match frozen declaration hashes | `final-1/installed-source-identities.json` |

The complete filesystem declarations, successful-generation reports and original
machine rows referenced by case observations are exported in
`final-1-validation/cases-evidence/bc3-evidence/snapshots/`. The offline case audit
checks their hashes and exact recorded fixture identities, including successful
inline writes and pre-permitted coverage. It cannot infer prepublication ordering
from post-state hashes alone. The source reviews in `parts/` are internal
engineering checks, not independent acceptance of the builder's implementation.

## Round 3 whole-suite ledger

The source-frozen controller finished its component, channel, transaction,
power-cut, independent-build comparison and combined replay/reboot stages. The
component and channel lanes exited 0; the regression lane and parent exited 1.
The [offline full evidence audit](raw/round-3/regression-audit.json) exited 2
(`incomplete`): no malformed or inconsistent evidence, and precisely the original
60-observation code/lifecycle suffix absent. All nineteen historical false
observations and seven historical untested observations remain in that audit.

All evidence paths in this table are relative to `raw/round-3/final-1-validation/`
unless prefixed by (not published: record outside this collection). Counts exclude summary records and do not add nested
assertions to their enclosing observations.

| Stage | Observed result | Evidence |
|---|---|---|
| Controller | Finished 16:56:44 UTC, exit 1; component/channel lanes 0, regression lane 1 | `summary.json`, `steps.json`, `whole-suite-ledger.json` |
| Ordered object suite | 37 pure cases and 49 required machine observations pass; 3 historical false observations retained; 2 reboot observations pass | `objects.jsonl`, `objects-reboot.jsonl`, `objects-evidence/` |
| Ordinary shell and unsaved execution | 22/28 observations pass; 6 historical false observations retained; reboot absence passes | `shell.jsonl`, `shell-reboot.jsonl` |
| General freezer | 9/9 observations pass | `gate.jsonl` |
| Tools at ordinary/root authority | 85 passes, 1 historical false observation retained | `tools.jsonl` |
| Supplemental saved-input paths | Direct 12/17, extra 12/16; 9 historical false observations retained | `supplement-direct.jsonl`, `supplement-extra.jsonl` |
| Component readback | Every requested original-machine readback clean, before/after reboot where specified | `*-verify.log`, `*-before-verify.log` |
| Language, application, system and ordinary channels | 79, 131, 32 and 59 observations pass; all four channel readbacks clean | `carried-suite/` |
| Authority/frontends and transactions | 166 and 35 observations pass | `carried-suite/regressions/round1.jsonl`, `round3.jsonl` in the same directory |
| Power cuts and boot admission | All 9 cut/result pairs and the boot-gate observation pass | `carried-suite/regressions/powercuts.jsonl`, `boot-order.jsonl` in the same directory |
| Code/lifecycle original run | 73 passes; FIFO creation fails; 60 suffix observations absent | `carried-suite/regressions/round2.jsonl` |
| Separate code/lifecycle continuation | 59/59 available suffix observations pass; 4 setup operations excluded; FIFO remains unavailable | (not published: record outside this collection), (not published: record outside this collection) |
| Native D01–D10 | All scenario/peer controller exits 0; D10 has 563 matching reader rows | `carried-suite/regressions/original/` |
| Independent peer comparison | 563 matching original-machine reader rows and identical exported machine declarations | `carried-suite/regressions/independent-stand-compare.jsonl`, `peer-a/`, `peer-b/` in the same directory |
| Combined replay and reboot | Exit 0, 24 event observations pass; 584 matching reader rows; both sides' exact/readback/schedule checks pass before/after reboot as specified | `combined/`, `complete-example/`, `complete-example.json` |
| Cleanup and retained identities | No owned disposable guests or peer image; no active owned validation/network service; image and declaration hashes unchanged; all 77 recipe files unchanged | (not published: record outside this collection) |
| Evidence export | All 489 listed final-build, validation, continuation and controller files match server sizes and SHA-256 identities | (not published: record outside this collection), (not published: record outside this collection) |

The complete older suites inspect their original declaration schema. Historical
saved-code negative assertions expect marker suppression and omit the new
filesystem primary files; their raw false observations are preserved. The
seventeen-case controller separately checks the committed automatic-recording
branch. No assertion is silently rewritten and no other table variant is closed
by this bounded result. Inherited peer/combined comparisons cover the original
machine declaration and readers, not byte equality of all five new filesystem
declarations or of the complete BC3 bundle.

## Carried FIFO limit and separate continuation

The original code/lifecycle scenario failed while creating its named FIFO at
`round2-selftest.py:176`, before SEALED-FIFO could produce an observation. Its
73 preceding observations passed; the 60-observation suffix was absent and the
original controller returned 1. This is a concrete filesystem compatibility defect,
not a successful refusal or an argument from the definitions.

The [fixed continuation plan](raw/round-3/parts/round2-continuation.md) preserves
the exact 59 remaining available observations and their commands. It ran once on
a fresh copy of the unchanged image, finished at **16:50:14 UTC**, and passed all
59; its guest was destroyed at **16:50:16 UTC**. Four necessary setup operations
are labelled separately and are not counted twice. SEALED-FIFO is explicitly
NOT-TESTED because its original setup failed; it was not retried. The
[offline continuation audit](raw/round-3/continuation-audit.json) verifies exact
sources, identities and the 132 distinct observed results plus one unavailable
FIFO case, with no inconsistencies. The primary audit keeps the original missing
suffix and failed controller; these separate results are not merged into that log.
The complete original 133-observation suite remains incomplete.

# Historical Round 2 self-test record

# Round 2 — ordered recorded-object coverage

Recorded 2026-11-23 UTC. **Final validation completed at 14:38:29 UTC.**
Both scratch recipes, all three complete test lanes, combined replay/reboot and
cleanup finished. All 40 controller steps exited zero. The
[independent final review](raw/round-2/REVIEW-FINAL.md) preserves C5.4 and C10.4;
all nine Round 2 owners remain NOT CLOSED: **2 CLOSED / 86 NOT CLOSED**.
The hypothesis outcome is `?`. Earlier Round 1 evidence is retained below.

Scope and inputs: [round plan](ROUNDS.md), (not published: orchestration or scratch),
[final changes](raw/round-2/FINAL-INPUT-CHANGES.md),
[source review](raw/round-2/REVIEW-FINAL-SOURCE.md) and
[82 frozen files](raw/round-2/final-1-source-sha256.json).
The inputs identify builder checks, not a claimed committed-input published check.

## Round 2 validation ledger

All paths in the evidence column are relative to `raw/round-2/final-1/`.
Object exports are in `objects-evidence/round2-evidence/`.

| Stage | Result | Evidence |
|---|---|---|
| Complete primary scratch recipe | Exit 0, 13:01:34–13:03:07 UTC | `build.log`, `recipe.log`, `image.json` |
| Independent peer scratch recipe | Exit 0, 13:03:08–13:04:43 UTC | `peer-build.log`, `peer-image.json` |
| Ordered classifier and concrete object suite | 37/37 pure cases; 49 required machine passes and three genuine boundary failures | `objects.jsonl`; exported `rule-cases.json`, `results.json`, exact fixture rows and five censuses |
| Object removal, reboot and every-line readback | 2/2 reboot assertions; all 553 final rows clean; residual chosen-setting observation retained | `objects-reboot.jsonl`, `objects-before-verify.log`, `objects-verify.log`; exported `removed.jsonl`, `residual-setting.json` |
| Ordinary shell and unsaved execution | 22/28 shell assertions, six retained boundary failures; post-reboot absence passes | `shell.jsonl`, `shell-reboot.jsonl`, `shell-verify.log` |
| General cgroup freezer | 9/9 assertions and complete final readback pass | `gate.jsonl`, `gate-verify.log` |
| Tools and editor at ordinary/root authority | 85 required passes, one retained boundary failure; all 553 final rows clean | `tools.jsonl`, `tools-verify.log` |
| Supplemental ordinary command paths | Direct 12/17 and extra 12/16; nine retained boundary failures; before/after reboot readback passes | `supplement-direct.jsonl`, `supplement-extra.jsonl`, `supplement-before-verify.log`, `supplement-verify.log` |
| Whole channel/regression chain | Language 79, applications 131, system 32, ordinary 59, transaction 35, authority/frontend 166, code/lifecycle 133 assertions pass; all nine power cuts and D01–D10 complete | `carried-suite/`, `carried-suite/regressions/`, `regressions-console.jsonl` |
| Independent recipe comparison | Same complete declaration bytes; every one of 557 observed rows equal | `carried-suite/regressions/independent-stand-compare.jsonl`, `carried-suite/regressions/peer-a/`, `carried-suite/regressions/peer-b/` |
| Complete six-new-row example | 24/24 event assertions, four exact-declaration and two schedule checks pass; all 578 rows verify before/after each reboot and compare equal | `complete-example.json`, `combined/`, `combined-console.jsonl` |
| Controller and cleanup | All 40 steps and three lanes exit 0; no owned guest or temporary peer | `summary.json`, `steps.json`, `whole-suite-ledger.json` |

The [offline audit](raw/round-2/audit-final-1.json) validates all eight sections,
including exact result/file inventories, every-line readback and source identity.
It preserves 19 false observations: three new object failures and 16 carried
boundary failures. Its 13 not-tested/availability records include the channel
controller's administrative `--regressions not requested` entry: the complete
regression chain ran in its separate concurrent lane. These are record counts,
not thirteen distinct missing capabilities. No missing audit section is accepted.
The [audit correction](raw/round-2/AUDIT-TRANSPORT.md) and
[separate review](raw/round-2/REVIEW-AUDIT.md) concern only systemd dependency-token
ordering and relative audit paths; no frozen recipe or machine evidence changed.

The three lanes joined before evidence assembly. Child summaries are retained
unchanged, including another lane's then-live guest names. Final cleanup is
established by the controller and the [host readback](raw/round-2/adoption.json):
the service is inactive with success status, no VM or peer remains, and all 82
recipe/controller files still match their frozen hashes.

## Round 2 image and declaration identities

The retained primary image is mode 0444, SHA-256
`6f7185e7590547a4fba9bfe8f4061306d6611e8cd6058111ead59d558af9451c`.
The independently built peer image was SHA-256
`01d37f6a9981e327107c3b3b6f967adb9ef28a504f99017973c5aa3326053a3c`
before deletion. Disk-image equality is not claimed.

The (not published: record outside selected evidence) has 553 rows, 434 native package rows and
31,261 base-file requirements. Its `machine.jsonl` SHA-256 is
`d046ab7b0e47dd88d0b49b83c34f14f4dcb2195a93aaf13df349c166bf218815`.
The (not published: record outside selected evidence) has 578 rows and SHA-256
`5df1087f7a88b0af51ee358846a5f95a3877be583fb5ff79eb3e296b36d3828b`.
It adds `v4:objects`, `v4:meta`, `v4:noncode`, `v4:printk`,
`v4:unit-source` and `v4:generated-unit` to the complete carried assembly.

## Interpretation of the new observations

The object log has the fixed 52 machine results: 49 required passes and three
actual failures, `UNRECORDED-BYTECODE`, `EXTRACTED-CODE` and `ALTERNATE-DATABASE`.
The native alternate-root/database install exits zero, reports
`install ok installed 1`, leaves its non-code file present, and does not change
the declaration/report. Native privileged installer operations are not breaking.
Direct privileged byte/mode edits outside the tools are breaking and are used
only to check reader sensitivity. A `required:false` flag permits observation
to continue; it does not turn a failed boundary into a pass.

The recorded bytecode consumes the received default and prints
`RECORDED-BYTECODE` and `DEFAULT-LANGUAGE:en`. False derivation and unsupported
algorithm requests refuse explicitly. No-code/meta/dependency registrations,
own settings, generated units, exact readback, removal and material/value work
pass within the finite supported format. One explicit UNTESTED availability
record covers executable browser/WASI confinement, the two families C7.19/C7.21.
Pure rule cases establish decisions from supplied facts, not those facts on a
real machine. See [object review](raw/round-2/REVIEW-OBJECTS.md) and the
[nine-owner evidence map](raw/round-2/COVERAGE.md).

The initial v4 census reports 497 covered, 61 unrecorded, 58 diagnostic and
65,096 FACT_UNKNOWN objects. All five censuses are explicitly incomplete and
have failed observed coverage; they do not establish P1. Census precedes
matching, and unknown receipt or semantic facts never become coverage. Runtime
diagnostics have no compulsory separate rows. An unapplied candidate without
owners checks inventory sensitivity, not application success. Explicitly
restoring the prior chosen value before removing its row does not establish
automatic restoration; the residual observation remains visible and uncovered.

Development completed at 13:00:39 UTC with no remaining guest. Its 52 object
assertions included two saved-code boundary failures and one diagnostic-detector
failure; both reboot assertions passed. The corrected receipt semantics, actual
default consumer, alternate-root fixture and diagnostic detector were validated
only by the new final rebuild. Original development outputs are preserved in
[development-1](raw/round-2/development-1).

---

# Round 1 — ordinary shell and declaration-writing tools

Recorded 2026-11-23 UTC. **Final-2 validation completed at 12:23:04 UTC.**
Both full recipes, all component and carried suites, combined replay/reboot and
supplemental observations completed. The main controller's 22 steps exited zero;
no owned guest or temporary peer remains. New and supplemental logs retain
157 Boolean observations: 141 passes and 16 genuine boundary failures.
[Independent final review](raw/round-1/REVIEW-FINAL.md) accepts C5.4 and C10.4:
2 CLOSED / 86 NOT CLOSED in the current version.
Outcome remains `?`; no implementation failure here is a definition-only
impossibility argument.

Scope is exactly the 65 Round 1 owners in [ROUNDS.md](ROUNDS.md).
The (not published: orchestration or scratch), [tool expectations](raw/round-1/TOOLS-PLAN.md)
and [supplement plan](raw/round-1/SUPPLEMENT-PLAN.md) fix the builder checks.
The [coverage map](raw/round-1/COVERAGE.md) distinguishes test families and limits.

## Final-2 validation ledger

| Required stage | Status / counts | Evidence |
|---|---|---|
| Frozen inputs and complete primary recipe rebuild | Recipe exited 0, 09:34:50–09:36:22 UTC; 65 frozen recipe files | [input hashes](raw/round-1/final-2/input-sha256.json), [build log](raw/round-1/final-2/build.log), [recipe log](raw/round-1/final-2/recipe.log), [image identity](raw/round-1/final-2/image.json) |
| Ordinary login/Bash, material work and recorded personal script | 28 Boolean assertions: 22 pass, six genuine saved-input boundary failures | [login](raw/round-1/final-2/login.log), [shell](raw/round-1/final-2/shell.jsonl) |
| Actual unsaved HTTP pipe execution and post-reboot absence | Executed payload and live process observed; no saved payload found; one post-reboot absence assertion passes | [shell](raw/round-1/final-2/shell.jsonl), [post-reboot](raw/round-1/final-2/shell-reboot.jsonl), [readback](raw/round-1/final-2/shell-verify.log) |
| General cgroup freezer and retained subprocess callers | 9/9 assertions passed on rebuilt image | [gate](raw/round-1/final-2/gate.jsonl), [readback](raw/round-1/final-2/gate-verify.log) |
| Typed tool add/change/remove, exact state, ordinary and actual root; editor | 85/85 implementation assertions passed; one genuine native-root account boundary failure; 553/553 final readback | (not published: direct evidence at least 2 MB), [readback](raw/round-1/final-2/tools-verify.log), (not published: record outside selected evidence) |
| Independent complete peer rebuild | Recipe exited 0 at 10:33:50 UTC; independent 557-row and combined 572-row comparisons pass | [peer build](raw/round-1/final-2/peer-build.log), [peer image](raw/round-1/final-2/peer-image.json) |
| Whole carried channel/regression sequence | Controller exited 0 at 12:15:26 UTC; language 79, applications 131, system 32, ordinary 59, transaction 35, power cuts 9, authority/frontend 166 and code/lifecycle 133 assertions pass | [controller output](raw/round-1/final-2/regressions-console.jsonl), [suite evidence](raw/round-1/final-2/carried-suite) |
| Complete declaration assembly and replay on both builds, with reboot | 24/24 assertions pass; all 572 rows verify before/after each reboot and compare equal | [assembly](raw/round-1/final-2/assemble.log), [combined controller](raw/round-1/final-2/combined-console.jsonl), [combined evidence](raw/round-1/final-2/combined) |
| Supplement actual Bash routes, exact markers, reboot/readback | Completed; 17 direct assertions (5 saved-input failures), 16 extra boolean assertions (4 saved-input failures); full reboot readback passed | [supplement input hashes](raw/round-1/final-2/supplement/input-sha256.json), [direct](raw/round-1/final-2/supplement/direct.jsonl), [extra](raw/round-1/final-2/supplement/extra.jsonl), [reboot](raw/round-1/final-2/supplement/reboot.json), [summary](raw/round-1/final-2/supplement/summary.json) |
| Controller completion and owned-VM/peer cleanup | All 22 steps exit 0; no owned VM or temporary peer remains | [main steps](raw/round-1/final-2/steps.json), [main summary](raw/round-1/final-2/summary.json) |

The primary image was rebuilt after the general freezer correction; final-1
observations do not substitute for final-2 results. [Strict saved-evidence validation](raw/round-1/metrics.json) confirms all expected
records, exact file inventories, declaration readbacks and controller consistency.
The [final review](raw/round-1/REVIEW-FINAL.md) accepts the bounded result.

## Image and declaration identities

Both scratch builds use the same 65 frozen recipe files. The retained primary
image is mode 0444, SHA-256
`3ad3bbaa805b65fb0f65487d15ca77a3702df04298fdfec3b5efeb254520ec21`.
The independent peer image was SHA-256
`b07ba3412ad2c975287e352247e1da2c666a058ddab24197df30816c1517afa3`
before deletion. Disk-image equality is not claimed.

The factory has 553 declaration rows, 434 package rows and 31,256 base-file
requirements. Its `machine.jsonl` SHA-256 is
`c45b095cb0db71285b7de413549cde93c0c4c2e45b5a9bfa2526d0e31798cd53`.
The complete combined declaration has 572 rows and SHA-256
`7a5c9116f501dc280e1681970d1489c97b009509cc14e0c4048a82123d3b7284`.
See (not published: record outside selected evidence), (not published: record outside selected evidence),
[primary identity](raw/round-1/final-2/image.json) and
[peer identity](raw/round-1/final-2/peer-image.json).

The independent inventory visibility fixture exits zero and surfaces its planted
objects. Its census reports 31,450 covered, 1,264 unrecorded and 40,597 unknown
objects, `complete:false` and `p1:"?"`; this is not complete P1 evidence.
(not published: over 20 MB).

## What a pass means

The carried boot gate refused all 205 ordinary attempts before readiness and
admitted no premature operator session. The original D01–D10 controller exited
zero and cleaned up its guests. The separate comparison across independent full
recipe builds reports identical declaration bytes and all 557 observed rows
equal. The complete channel assembly contains 572 declaration rows: the
553-row factory plus 19 exact exported channel rows. Eleven ordinary channel
launches and the scheduled command succeed on each build. The complete
572-row declaration verifies before and after both reboots, preserves exact
declaration bytes, and compares equal for every actual row.

The shell suite executes actual ordinary Bash commands. The tool suite records
exact declaration diffs, durable success identity, every-line readback and
concrete removal, separately at ordinary and actual root authority. The gate
suite requires kernel `cgroup.events` acknowledgement, a stopped heartbeat
through realization, refusal of new entry while pending, restoration to original
cgroups and disappearance of private freezer children/journal. Its
`NESTED-BROKER-CALLER` and `NESTED-EDITOR-CALLER` tests retain an ordinary Python
parent across add/remove and inspect actual state between operations.

Read every result row, not only controller exits:

- An **implementation pass** means its specified supported operation and
  readback completed. It does not erase failed required-boundary attempts.
- Shell probes marked `requirement:false` retain genuine saved-code boundary
  failures while allowing remaining implementation checks to run. That flag is
  an exit-status convention, not an exemption from the hypothesis.
- The native-root account test has a separate `boundary_result`. A built-in
  native tool creating an uncovered account is a built-in-tool bypass, not
  breaking; its public typed adapter's success does not close that path.
- Runtime-only memory observations have no mandatory standalone line. A runtime
  memfd/injection restriction is neither a successful saved-code boundary proof
  nor an invented hypothesis requirement. Saved input is checked separately.
- Missing tools/facilities are **UNTESTED**, not successful refusals. Saved Wi-Fi
  and prepared Bluetooth values are not evidence of actual radio work.
- Carried broker calls adapted by `v4-suite-adapter.py` become Bash commands.
  Carried `run` requests remain sealed launcher calls inside Bash. Their refusal
  is compatibility evidence, not proof about arbitrary Bash interpreter input.
- Root editing around built-in tools is recorded separately as breaking; the
  general editor's documented installer still must declare/apply its changes.

Count true property failures separately from implemented-check failures,
untested families and accepted runtime observations. A finite attempt does not
close every path in its variant. Final closure needs a mechanism, a concrete
failed bypass and independent review.

## Retained earlier candidate failures and corrections

**Final-1 was incomplete.** Its editor transaction completed successfully, but
the ordinary caller stalled and timed out. Process evidence showed the
unconfined `runuser` parent stopped, the editor child exited, no pending/paused
journal and a durable success report. The SIGSTOP pause interacted with caller
job control; resuming only the ordinary confined child was insufficient.
[General correction record](raw/round-1/FREEZER-CORRECTION.md) and
[stall review](raw/round-1/REVIEW-EDITOR-STALL.md) preserve the observation and
superseded source hypothesis. The implementation now uses private cgroup v2
freezer children beneath original cgroups; the editor itself keeps its ordinary
subprocess call. The final-2 gate and tool suites validated this correction on
the rebuilt image; the complete carried and combined sequences also passed.

Final-1 supplements remain evidence for that earlier image, not acceptance of
the corrected one. The [direct log](raw/round-1/final-1/supplement/direct.jsonl)
contains 17 assertions and five genuine saved-code failures. The
[extra log](raw/round-1/final-1/supplement/extra.jsonl) initially labelled five
failures; [offline marker audit](raw/round-1/supplement-marker-audit.json)
confirmed four real execution effects and one detector error. `SAVED-FFI`
matched source echoed in a Python traceback: stdout was empty and `CDLL` failed
to map the library. It was a denied mapping, **not an executed FFI effect**.
The original payloads/logs remain preserved; no probe was repeated to make this
correction. The corrected future detector is not retroactive runtime evidence.
[Supplement evidence review](raw/round-1/REVIEW-SUPPLEMENT-EVIDENCE.md) records the
finite outcomes, unavailable cases and earlier reboot continuity. The final-2
supplement repeats these fixed inputs as part of mandatory rebuilt-image
validation, with the corrected exact-line detector. It confirms nine genuine
saved-input failures, refuses the FFI mapping, and preserves all 553 readback
rows and the success report across reboot. See the
[final-2 supplement review](raw/round-1/REVIEW-FINAL2-SUPPLEMENT.md).

## Recipe and run commands

Run only on the server, from `VMs/cal-1123/stand/` relative to its account's
initial directory. The complete image recipe is:

```sh
python3 build/build.py --server --replace
```

The main controller invokes that recipe itself, records input/image hashes,
creates independent fresh guests and a peer build, runs the new suites, then
runs the full carried and combined sequences. Do not separately rebuild again
between a controller's frozen-image identity and its validation. For the
preplanned final-2 phase, the long controller ran under a user service. The
executed service record is retained with its output; the equivalent invocation
below documents the mechanics and must not be repeated under a consumed name:

```sh
systemd-run --user --collect --unit=cal-1123-stand-round1-final2 \
  --working-directory="$PWD" python3 tools/round1.py final-2
```

After the main phase rebuild completes and its image identity is recorded, the
supplement controller uses that same image on another fresh overlay:

```sh
systemd-run --user --collect --unit=cal-1123-stand-supplement-final2 \
  --working-directory="$PWD" python3 tools/supplement1.py final-2
```

These are the planned commands, not instructions to rerun an already consumed
phase. Both controllers refuse existing evidence directories. Preserve failed
phases; do not delete logs to permit a repeat. `lab.py` defaults to ordinary
Bash input. `STAND_LEGACY=1` is explicit compatibility opt-in, set by the main
controller only for unchanged structured suites. Temporary guests and the peer
build must be removed, with cleanup recorded. These builder self-tests do not
constitute published checks with committed pre-observation inputs.

## Publication and retained testbed

[Publication manifest](raw/round-1/publication.json) and
[archive verification](raw/round-1/export-verification.json) identify all exported
files and their verified hashes. Frozen recipe and supplemental inputs preserve
exact bytes. The accepted final host parser is SHA-256
`df131f96cae4dc61cf4c10b6ddf196472051fdedd51cc10478fd353efbdcc9a4`;
[parser audit](raw/round-1/PARSER-FINAL-AUDIT.md) and
[validation output](raw/round-1/metrics-validation.log) preserve its strict result.
The earlier archive was unaccepted and replaced after this host-only correction.
No guest experiment was repeated for packaging or parser changes.

The [acceptance record](raw/round-1/acceptance.json) binds the exact image,
recipe manifest, publication, archive, metrics and independent review.
[Adoption](raw/round-1/adoption.json) and
[host cleanup](raw/round-1/host-cleanup.json) record the retained recipe/image,
complete examples, absence of owned guests, and removal of temporary peer,
candidate duplicate, staging copies, old backup and transfer archive.
The current declaration examples are under `example/round-1/`; the historical
Round 0 examples below remain unchanged.

## Historical Round 0 — retained baseline record

The remainder preserves the completed Round 0 record. Its dates, counts,
images, interface limits and disposition refer **only to that past baseline**.
Words such as “current,” “tonight” and “new” below have that historical meaning;
they are not final-2 status claims.

### Round 0 — unchanged carried testbed

Recorded 2026-11-23 UTC. **Round 0 passed: both builds and every carried controller exited 0.** Execution ran from 05:58:10 to 08:10:18 UTC; the final host cleanup inspection was at 08:11:04 UTC. This is the builder's baseline reproduction, not published Check 2/3 and not acceptance of a version 4 testbed. Overall hypothesis outcome remains `?`. No new system mechanism was built. [Final controller record](raw/round-0/summary.json).

The (not published: orchestration or scratch) fixes the scope. [round0.py](tools/round0.py) executes the carried recipe twice, runs the full unchanged final-night regression controller, assembles its complete declaration and runs the unchanged combined test on both builds with reboot. Assertions, fixtures and expectations are unchanged. Only the shared VM lock namespace in `build/lab.py` was relocated to this night's directory; [recipe-provenance.json](raw/round-0/recipe-provenance.json) records all 56 original and deployed recipe hashes. The [provenance notes](raw/round-0/PROVENANCE.md) distinguish source inventories from deployed inputs.

#### Builds and evidence boundary

Both independent recipe executions exited zero. Primary: 05:58:10–06:00:07 UTC; peer: 06:00:07–06:02:23 UTC. Their recipe inputs match. Image SHA-256 values are recorded in [build-identities.json](raw/round-0/build-identities.json):

- Primary: `c61702a6d01bc6c02ac1cb760bc1dd8475a7a1b6a8136bcbe3142b4405fe221c`.
- Peer: `cbc4ed1361acb33fba2c0b59c2f15b856798ec3b448f26a16c27212f5c317484`.

Both builds emitted the same **552-row factory**, with 434 package rows and 31,247 base-file entries. Their factory, base-manifest and initramfs digests match each other. The prior final review reports 553 factory rows and a different factory digest, while its base-manifest and initramfs digests match tonight's. **FACT_UNKNOWN: which historical factory row/value changed.** The named historical reports do not contain the full old export needed to identify it. Exact digests and this limitation are retained in [PROVENANCE.md](raw/round-0/PROVENANCE.md); the current export is analyzed in [factory-analysis.json](raw/round-0/factory-analysis.json). No cause is inferred and no exact old-factory reproduction is claimed. Both new builds' agreement is a separate comparison from agreement with the old report.

#### Observations

| Scope | Observed result | Saved evidence |
|---|---|---|
| Full recipe, twice | Both executions exit 0; independently created images, matching recipe inputs | [primary-build.log](raw/round-0/primary-build.log), [peer-build.log](raw/round-0/peer-build.log), [steps.json](raw/round-0/steps.json) |
| Language paths | 79/79 assertions pass | [language.jsonl](raw/round-0/round-4/baseline/language.jsonl) |
| Application/container paths | 131/131 assertions pass | [applications.jsonl](raw/round-0/round-4/baseline/applications.jsonl) |
| System update and restoration | 32/32 assertions pass | [system.jsonl](raw/round-0/round-4/baseline/system.jsonl) |
| Ordinary work, jobs, removal and policy restoration | 59/59 assertions pass | [ordinary.jsonl](raw/round-0/round-4/baseline/ordinary.jsonl) |
| Transaction, stalls, watchdog, removal and shared contributions | 35/35 assertions pass | [round3.jsonl](raw/round-0/round-4/baseline/regressions/round3.jsonl) |
| Boot admission | 176 ordinary attempts before observed readiness; zero successes, no premature operator session; PAM/readiness inspection passes | [regression controller](raw/round-0/round-4/baseline/regressions-console.jsonl), [boot-order.jsonl](raw/round-0/round-4/baseline/regressions/boot-order.jsonl), [attempts](raw/round-0/round-4/baseline/regressions/boot-attempts.json) |
| Nine success-triggered hard cuts | All nine add/change/remove cut-and-readback cases pass | [powercuts.jsonl](raw/round-0/round-4/baseline/regressions/powercuts.jsonl) |
| Independent inventory visibility fixture | All planted objects surfaced; exit 0. Census reports 31,439 covered, 1,266 unrecorded and 40,588 unknown objects, `complete:false`, `p1:"?"` | (not published: over 20 MB), [regression controller](raw/round-0/round-4/baseline/regressions-console.jsonl) |
| Original D01–D10 suite | Exit 0; all three earlier cuts verified; D10 declaration bytes equal and all 556 actual rows equal on two clean overlays of the primary image | [original-console.log](raw/round-0/round-4/baseline/regressions/original-console.log), [D07.log](raw/round-0/round-4/baseline/regressions/original/D07.log), [D10 summary](raw/round-0/round-4/baseline/regressions/original/D10-summary.log), (not published: over 20 MB) |
| BC1 authority and frontend regression | 166/166 assertions pass; guest suite exits 0 | [round1.jsonl](raw/round-0/round-4/baseline/regressions/round1.jsonl), [regression controller](raw/round-0/round-4/baseline/regressions-console.jsonl) |
| BC2 code-boundary and lifecycle regression | 133/133 assertions pass; guest suite exits 0 | [round2.jsonl](raw/round-0/round-4/baseline/regressions/round2.jsonl), [regression controller](raw/round-0/round-4/baseline/regressions-console.jsonl) |
| Comparison across independent full builds | Complete declaration bytes equal; all 556 actual rows equal; both regression controllers exit 0 | (not published: over 20 MB), (not published: over 20 MB), [regression summary](raw/round-0/round-4/baseline/regressions/summary.json), [full controller summary](raw/round-0/round-4/baseline/summary.json) |
| Complete channel-example assembly | Exact 19 exported channel rows; complete combined declaration has 571 rows with all 31,247 base-file requirements inline | [assembly.log](raw/round-0/assembly.log), (not published: over 20 MB), [example hashes](example/provenance.json) |
| Combined declaration on both independent builds, with reboot | Exit 0; all 24 controller assertions pass. Eleven ordinary channel launches and the scheduled command succeed on each build. All 571 rows verify before and after reboot; exact declaration bytes survive both reboots; all 571 actual rows compare equal | [combined summary](raw/round-0/round-4/combined/summary.json), [controller assertions](raw/round-0/round-4/combined/events.jsonl), (not published: over 20 MB), [first reboot readback](raw/round-0/round-4/combined/a-reboot-verify.jsonl), [second reboot readback](raw/round-0/round-4/combined/b-reboot-verify.jsonl), [first schedule](raw/round-0/round-4/combined/a-schedule.jsonl), [second schedule](raw/round-0/round-4/combined/b-schedule.jsonl) |
| Cleanup and retained testbed | No owned QEMU process or VM entry remains; temporary peer removed. Only `base/stand.qcow2` remains as a disk image, read-only mode 0444 with its original rebuilt digest. Recipe, verified inputs, private laboratory access keys and evidence remain for reuse | [cleanup.json](raw/round-0/cleanup.json), [host-cleanup.json](raw/round-0/host-cleanup.json) |

The four channel suites total 301 passing assertions. The original D10 overlay comparison is separate from the later comparisons across independent full builds. Inventory objects were planted through external root access as a visibility fixture; they are not ordinary-path property failures. Every planned stage completed; none was skipped or rerun.

#### Publication

All new evidence is under [raw/round-0/](raw/round-0). The [publication manifest](raw/round-0/publication.json) lists the 199 exported evidence/example files and their SHA-256 digests. No text normalization was needed: all 199 files, including the complete declarations, retain their server bytes. The original server logs remain there as well. No previous-night raw log, private access key or image is included in the laptop publication. Temporary transfer archives were removed after extraction.

#### Limits and disposition

Passing unchanged refusal tests does not establish the v4 command shell or privileged declaration-writing behavior. The carried interface still refuses free shell commands. Saved Wi-Fi and prepared Bluetooth profiles are not actual connection/pairing evidence. The independent census remains a bounded visibility test; it cannot prove complete P1. Transaction recovery tests do not establish general device recovery. The inherited one-hour bound is an engineering setting, not a condition added to the hypothesis.

At the end of Round 0, the previous-night table had 78 CLOSED / 10 NOT CLOSED, and all 88 v4 variants were NOT VALIDATED. [V4-DIFF.md](V4-DIFF.md) states the changed criteria, [ROUNDS.md](ROUNDS.md) assigns the remaining work, and [STAND.md](STAND.md) stays partial. The separate assessment is [REVIEW.md](REVIEW.md).
