BUILD 3: 0 of 15 ways refused with their permitted action working; account tool closed; ordinary work done

Recorded 2026-11-23 UTC. The header counts literal refusals: **zero commands were denied**. All fifteen nevertheless met the committed **automatic-recording alternative**: they executed successfully after their saved input was recorded by the system. Every same-code, same-command permitted counterpart succeeded. The native root account operation and all ordinary work also succeeded on the same final image. These are builder observations, not the second party's one-attempt results or separate acceptance. The hypothesis/step outcome remains `?` pending those proceedings and the stated interpretation/implementation limits.

**Whole-suite status: finished with an incomplete carried code/lifecycle suite.** The final image was rebuilt from scratch and all seventeen targeted builder cases finished. The validation controller ended at **16:56:44 UTC with exit 1**, preserving the FIFO setup failure. The other carried lanes and combined replay/reboot completed. The original code/lifecycle log has 73 passes and 60 absent observations; a separate continuation has 59 passes, with FIFO still unavailable. The [full evidence audit](raw/round-3/regression-audit.json) reports no inconsistencies and retains that missing suffix, nineteen historical false observations and seven historical untested observations. This is not a full-suite pass.

## One recipe, one image, one description

The recipe is [build/](build), with the added dependencies in `bootstrap.sh`, modules installed by `build.py`, and [install-bc3.py](build/install-bc3.py) invoked before factory capture. The general mechanism is [bc3_filesystem.py](build/bc3_filesystem.py), using the existing kernel FUSE interface at `/home/stand`, `/tmp`, `/var/tmp`, `/dev/shm` and `/etc`. No command wrapper was added for any of the fifteen inputs or for native useradd.

For each mutation the service constructs intended namespace/inode/content requirements, writes immutable content, a durable declaration and a matching successful-application identity, atomically selects that generation, and only then completes the mutation. Serialized read callbacks obtain the selected bytes. Exact same-path rewrites remain possible. The service records optional material too, as allowed by S8.2-19: “What need not be recorded may also be recorded in the declaration.” This is an implementation choice, not an added rule requiring every document to be classified as installed code. Account rows are derived from prospective database content by [bc3_account_rows.py](build/bc3_account_rows.py).

The primary designation `/etc/stand/bc3-primary.json` names the original `/var/lib/stand/current/machine.jsonl` plus five `/var/lib/stand-fs/KEY/current/declaration.json` files. The complete export also includes the original referenced `base-files.json` and the designation itself: eight exact files in one canonical bundle. Audit logs are evidence, not the declaration. The account/filesystem declaration has its own exact desired-state rows and successful-generation identity; a command log alone would not suffice.

- Retained server image: `VMs/cal-1123/stand/base/stand.qcow2`, relative to the server account's initial directory; mode `0444`; SHA-256 `5641c3c34e08dba60ae7f97511fae33d4dde48dba0ef5d93db93ab6faeb3cb79`.
- Complete frozen-image declaration: (not published: direct evidence at least 2 MB), SHA-256 `4fd6f7acbc4e9d110dbd3513b4b42aace2b775d99f9f90341f86fb64e33bda57`. It was extracted read-only from the unbooted frozen disk; [identity.json](raw/round-3/final-1/offline-declaration/identity.json) binds each constituent file.
- Recipe inputs: [frozen hashes](raw/round-3/final-1/input-sha256.json), [source snapshot](raw/round-3/final-1/recipe-inputs), [actual 118-package manifest](raw/round-3/final-1/package-inputs.sha256). The [package delta](raw/round-3/final-1/package-inputs.json) adds only libfuse2t64 and python3-fusepy to the inherited manifest, with no inherited package changes.
- All six installed BC3 runtime/controller/fixture files have matching local-source and frozen-declaration hashes: [installed identities](raw/round-3/final-1/installed-source-identities.json).

## Fifteen ways and their paired permitted actions

For **every row below**, the attempt returned zero, produced the listed marker and had exact path/inode/content-hash coverage with a matching successful filesystem generation. The permitted action then repeated the **same literal original command** with the **same saved bytes**, already covered before invocation, and produced that marker again. Inline write-and-execute commands additionally have a successful write audit, so a failed overwrite followed by execution of an old file cannot pass. There was no literal denied command in any row.

Exact commands, working directories, source bytes/hashes and original Round 1 evidence are fixed in (not published: record outside this collection) and [bc3-fixtures.json](build/bc3-fixtures.json). Evidence below is under `raw/round-3/final-1-validation/`; line numbers refer to [cases.jsonl](raw/round-3/final-1-validation/cases.jsonl). Each before/after record names a SHA-256-verified full snapshot in `cases-evidence/bc3-evidence/snapshots/`. Read the attempt and permitted records together, including `coverage`, `inline_write_verified`, `audit`, stdout/stderr and generation reports.

| Way | Mechanism on the exact saved input | Attempt and permitted observation | Evidence lines: attempt / permitted |
|---|---|---|---|
| SAVED-SCRIPT | Record the original write to `saved.txt` before Bash reads it | Recorded and ran; same command ran again: `SAVED_CODE_RAN` | 2 / 4 |
| SAVED-PIPE | Record `saved.txt` at saving; cat reads the declared bytes into the pipe | Recorded and ran; same command ran again: `SAVED_CODE_RAN` | 8 / 10 |
| SAVED-SOURCE | Record `saved.txt` before the current shell sources it | Recorded and ran; same command ran again: `SAVED_CODE_RAN` | 14 / 16 |
| STARTUP-ENV | Record `saved.txt` before BASH_ENV startup evaluation | Recorded and ran; same command ran again: `SAVED_CODE_RAN` | 20 / 22 |
| PYTHON-IMPORT | Record each original `loose_module.py` write before import | Recorded and ran; same command ran again: `IMPORTED_UNRECORDED` | 24 / 26 |
| PICKLE-CODE | Record the original serialized-file write before pickle.load | Recorded and ran; same command ran again: `PICKLE_EXECUTED` | 28 / 30 |
| DIRECT-REDIRECT-STDIN | Record `saved.sh` before redirection opens it | Recorded and ran; same command ran again: `SAVED_DIRECT_RAN` | 34 / 36 |
| DIRECT-PROC-FD | Record `saved.sh`; the descriptor resolves its declared inode | Recorded and ran; same command ran again: `SAVED_DIRECT_RAN` | 40 / 42 |
| DIRECT-READ-EXEC | Record `saved.py` before open/read/exec | Recorded and ran; same command ran again: `READ_EXEC_RAN` | 46 / 48 |
| DIRECT-AWK-FILE | Record `saved.awk` before awk -f reads it | Recorded and ran; same command ran again: `AWK_FILE_RAN` | 52 / 54 |
| DIRECT-SCRIPT-HELPER | Record `saved.sh` before find starts Bash on it | Recorded and ran; same command ran again: `SAVED_DIRECT_RAN` | 58 / 60 |
| RC-STARTUP | Record `startup.rc` before explicit startup processing | Recorded and ran; same command ran again: `SAVED_RC_EXECUTED` | 64 / 66 |
| EDITOR-SAVED-COMMANDS | Record `commands.ed` before editor redirection and shell escape | Recorded and ran; same command ran again: `SAVED_EDITOR_COMMAND_EXECUTED` | 70 / 72 |
| JIT-SAVED-INPUT | Record `machine.bytes` before Python reads and executes its six bytes | Recorded and ran; same command ran again: `JIT_SAVED_INPUT_EXECUTED 42` | 76 / 78 |
| DISPATCHER-SAVED | Record `instructions.ops` before the unchanged recorded dispatcher reads it | Recorded and ran; same command ran again: `DISPATCHER_SAVED_EXECUTED` | 85 / 87 |

The ordering claim rests on the prospective publication code and mounted-operation audit, not merely a matching post-execution hash. [Internal source review](raw/round-3/parts/final-source-review.md) checked all fifteen original commands and the native account argv against Round 1. The [offline case audit](raw/round-3/final-cases-audit.json) checks saved evidence consistency and explicitly lists the observational limits. Neither is the required external acceptance.

## Native account tool

The exact original command, run as actual root, was `/usr/sbin/useradd -M -u 1998 -s /usr/sbin/nologin v4raw`. It returned zero. Actual and declared tuples agree: name `v4raw`, uid/gid `1998`, groups `["v4raw"]`, home `/home/v4raw`, empty gecos and shell `/usr/sbin/nologin`. The `/etc` declaration changed and its success hash matches. Own semantic account/group/settings rows are made from candidate passwd/group/shadow bytes before each filesystem publication; this is not a post-execution hook or an argv-specific wrapper.

Evidence: `cases.jsonl` lines 88–89, with the referenced before/after snapshots and audit changes. The same operation both records and applies the change; it is not repeated against an already existing account. Direct privileged editing outside built-in tools remains possible and is not forbidden under a redefinition of breaking. This finite native operation does not prove every possible account-database transaction or continuous whole-system P1/P2.

## Ordinary work in one session

`cases.jsonl` lines 92–93 preserve the complete single `set -e` Bash session and result. It executed free commands, a function, arguments, a pipeline and redirection; installed and ran its own exact recorded script with an argument; installed hello through the package manager; connected over the virtual Ethernet TCP/HTTP path; opened that page with the recorded w3m browser; and created then edited and read a document. Script/package declaration rows and saved document requirements appear in its exported snapshots. The fixed host HTTP fixture and exact commands are in CASES-5.

Observed output, omitting only the two separately retained SUCCESS generation hashes:

```text
TWO WORDS
PERSONAL_SCRIPT_OK:ordinary argument
Hello, world!
BC3 NETWORK PAGE
Edited document
BC3_ORDINARY_COMPLETE
```

All seventeen cases ran in the same builder guest on the frozen image. Filesystem readback afterwards checked 1,379 declared paths with no mismatch: [cases-filesystem-verify.jsonl](raw/round-3/final-1-validation/cases-filesystem-verify.jsonl). The second party's protocol instead requires a fresh copy for each of its seventeen single attempts; its ordinary-work case still uses one session.

## What failed, and what is not claimed

1. The historical executable/native-mapping gate missed all fifteen saved-input routes in Round 1. Existing-kernel source assessments explain why read data are not native execution events; see `raw/round-3/parts/`. Blanket read denial would also deny permitted material reads. Read-time notification without versioned mutation handling misses mmap/in-place changes. Immutable-at-path protection would prevent the original rewrite-and-run commands. These are documented rejected mechanisms, not invented records of new VM trials. No closure is claimed by banning their permitted action.
2. The first new scratch build failed during factory capture with a systemd/DBus timeout: [development-1/build.log](raw/round-3/development-1/build.log). No image or case pass came from it. The filesystem had expensive whole-state work on ordinary lookup/close; indexed namespace bookkeeping removed that work. The successful development-2 build and seventeen-case run are retained separately. This was an integration failure, not a failed permitted-action case followed by disguised command-specific patches.
3. The unchanged carried code/lifecycle suite stopped at `round2-selftest.py:176`: `os.mkfifo` returned `EROFS` because the filesystem does not implement special nodes. Its first 73 observations passed; the original controller returned 1 and its remaining 60 observations were absent. A separately fixed [continuation](raw/round-3/parts/round2-continuation.md) ran the 59 still-available suffix observations once on a fresh copy of the same image, with unchanged commands and separately labelled setup; all 59 passed. FIFO was not retried and remains unavailable. The [continuation audit](raw/round-3/continuation-audit.json) verifies 132 distinct observations plus that unavailable case. This does not turn the aborted original suite into a complete pass or alter the seventeen committed inputs. Evidence: `raw/round-3/final-1-validation/carried-suite/regressions/round2.jsonl` and `raw/round-3/final-1-continuation/`.
4. The mechanism is finite: shared writable mappings, special nodes, full ACL handling, arbitrary writable mounts and general direct native/shebang execution in the noexec mediated roots are not established. The committed ways all use explicit admitted consumers; the ordinary personal script runs from its recorded package path. Retained previous-generation blobs are not necessarily covered by the current declaration, and root read/execute is not automatically breaking. Whole-system completeness and every recovery/concurrency transition remain unproved.
5. [ARGUMENT-5.md](ARGUMENT-5.md) gives a concrete stronger mechanism for each of the fifteen ways, with sentence IDs/exact quotes and strongest objections. It does not claim an impossibility theorem. [QUESTIONS-5.md](QUESTIONS-5.md) records both readings of saving/running saved text at repeatedly typed commands, prospective recording and retained copies. No authorial reading is selected.

## Full rebuild, records and handoff

The final scratch recipe and independent peer scratch recipe both completed. The rebuilt-image validation finished in `raw/round-3/final-1-validation/`; [SELFTEST.md](SELFTEST.md) records every stage, retained false/untested observations and the failed original code/lifecycle scenario. The separate continuation does not replace that scenario's original log. The inherited peer comparison has 563 matching original-machine reader rows; combined replay has 584 matching rows, complete readback before/after reboot on both sides and 24 successful event observations. These comparisons do not compare all five new filesystem declarations or assert byte equality of the complete BC3 bundle.

[Final host readback](raw/round-3/final-host-readback.json), at **16:59:01 UTC**, confirms unchanged image/declaration identities, all 77 frozen recipe files unchanged, no owned disposable guests or peer image, and no active validation, continuation or network-fixture service. The combined replay inputs are retained under `final-1-validation/complete-example/`, with a relocation record. No other variant in the historical 88-row table is reclassified by this bounded round. Updated operating and scope records are [STAND.md](STAND.md), [SELFTEST.md](SELFTEST.md), [HOWTO.md](HOWTO.md) and [ROUNDS.md](ROUNDS.md).

[Export verification](raw/round-3/final-export-verification.json) checked all 489 listed final-build, validation, continuation and controller evidence files against their server SHA-256 identities: no missing or mismatched file. The [final evidence review](raw/round-3/parts/regression-final-review.md) and [report consistency review](raw/round-3/parts/report-internal-review.md) are internal checks only; neither substitutes for the two separate parties required by the task.

(not published: record outside this collection) has the final image and complete-declaration SHA-256 at its top, exact standalone commands for all seventeen cases, observations and fresh-copy setup/cleanup. It and its input identities are locally frozen by [inputs-seal.json](raw/round-3/inputs-seal.json). **Public commitment is pending:** repository metadata in this working copy is empty and read-only, and no public destination has been supplied. This is not represented as a commit or a published check. The records operator must publish the unchanged sealed package before the second party's first attempt; the inputs and commands must not change afterwards. No independent attempt was performed by the builder.
