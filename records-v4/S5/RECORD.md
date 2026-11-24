STEP 5: 1 cases with 1; 0 with 0; 16 with ?; the step ?

# Supplement 1, step 5: the second party's seventeen cases

Recorded 2026-11-23 UTC by the second party, which did not build the image. Review: RV-S5-O. Log: `S5/LOG.md`.
Questions for the author: `S5/QUESTIONS.md`. Raw evidence: `S5/raw/`.

## Summary

- All seventeen cases ran once, each on its own fresh copy of the sealed image, 17:08–17:15 UTC. Every case exited 0.
- No way was refused. In every way case the attempt ran its saved code and printed its marker; the saved source was in the
  designated filesystem declaration, under a matching success report, before the way read it (cases 01, 05, 06: written by
  the way itself; other cases: written earlier by the ordinary account when the controller set up the fixture). The same command
  then ran again as the permitted action. The native `useradd` created the account and the `/etc` declaration gained own rows for
  it. All six ordinary actions succeeded in one session.
- Outcomes. Case 17 (ordinary work): 1. Cases 01–16: “?”. Each of them meets the rule of `SUP1/step-5.md` (“what it leaves is
  recorded in the declaration”) only if the text the filesystem service writes from saved bytes counts as a declaration under
  S8.1-2. That is a choice between two readings, and the choice is the author's (`S5/QUESTIONS.md` Q1, Q2). Under reading A
  all sixteen give 1 and the step gives 1. Under reading B they are ways that are neither refused nor recorded, with no argument,
  and give “?”; the step gives “?”. Choosing 1 would mean choosing reading A, so the record gives “?” and leaves the choice open.
- Ways not refused: all sixteen (the fifteen saved-code ways and the account tool).

## Before the first case

| Check | Result | Evidence |
|---|---|---|
| Gate (not published: orchestration or scratch): seal SHA-256 `2bbc5cad…5dce62`, `check-inputs-v4/supplement-1/step-5-cases/CASES-5.md` SHA-256 `cf01619e…819c2b9` | both match (local and host) | `S5/raw/00-identity-checks.txt` |
| Image SHA-256 `5641c3c3…b3cb79`, complete declaration SHA-256 `4fd6f7ac…33bda57` (top of CASES-5) | both match | same |
| Every file named in the seal | matches. Two files (`installed-source-identities.json`, `package-inputs.sha256`) exist only in the local export | same |
| Frozen controller `68cf3372…` and manifest `1277fed5…` are the ones the frozen declaration lists | yes | `B2/raw/round-3/final-1/installed-source-identities.json` |
| Way commands vs round 1 | all 15 byte-identical to the round-1 `expected` rows; account argv identical; fixture bytes, sizes, modes and working directories identical | `S5/raw/01-round1-command-comparison.json` |

No way was weakened in its command, so no round-1 command had to be run in addition. One difference in setup only: round 1
wrote the direct/extra fixtures as root from its controller (`B2/raw/round-1/final-2-supplement-inputs/v4-direct-selftest.py`
lines 113–123), and its `SAVED-PIPE`/`SOURCE`/`STARTUP-ENV` used the `saved.txt` left by `SAVED-SCRIPT` in the same guest. Round
3 writes each fixture in a fresh copy through the ordinary account's shell, and the image records that write. The network
fixture was started and checked exactly as CASES-5 gives it (`S5/raw/02-network-fixture.txt`) and stopped after case 17.

Procedure: the CASES-5 replay sequence verbatim (`S5/tools/replay.sh`). Copies `bc3-peer-01`…`17` were destroyed by that
sequence; afterwards there were no guests, no units and all slots were free (`S5/raw/06-host-after-cleanup.txt`). The outputs stay
at the CASES-5 path on the host; the local copies in `S5/raw/cases/` are byte-identical. Each case was analysed independently of
the controller's verdict by `S5/tools/analyse_case.py`. For every step, this script reads the full before and after snapshots,
checks each snapshot file's SHA-256, re-encodes each filesystem declaration and compares it with its recorded digest, checks that
`success.json` names that digest and generation, and diffs the paths, objects and primary rows. No mismatch was found in any case
(`problems: []` in every (not published: record outside selected evidence)). Summary: `S5/raw/05-cases-summary.txt`.

## Per case

Commands: the literal commands of `check-inputs-v4/supplement-1/step-5-cases/CASES-5.md` sections 01–17 (also `B2/build/bc3-fixtures.json`). The permitted command of
each way is the same literal command. Expected results were written in `S5/LOG.md` before each run.
Evidence for case NN: (not published: record outside selected evidence), `NN.exit`, `NN.stderr`, `NN-evidence/bc3-evidence/snapshots/<sha>.json`,
`NN-analysis.json`. The snapshot prefixes below are those files.

“Covered” means that the designated filesystem declaration has a path row for the source, and that this row leads to an object
with the manifest SHA-256, under a generation whose success report hashes that declaration.

| # | Way and command | Expected | Observed attempt | Declaration before → after the attempt | Permitted action | Outcome |
|---|---|---|---|---|---|---|
| 01 | SAVED-SCRIPT `printf 'printf SAVED_CODE_RAN\n' > saved.txt; bash saved.txt` | recorded, runs | rc 0, `SAVED_CODE_RAN` | `1b2b5ff8`→`b136d2f0`: home gen 1→3; `saved.txt` absent before; gen 2 `create` (empty), gen 3 `write` (`17415cef…`); primary unchanged | rc 0, marker; covered before; gens 4 `truncate`, 5 `write` same bytes (`5a3e9a02`) | ? |
| 02 | SAVED-PIPE `cat saved.txt \| bash` | same | rc 0, `SAVED_CODE_RAN` | `cba7c950` unchanged; source covered (home gen 4) before | rc 0, marker | ? |
| 03 | SAVED-SOURCE `source saved.txt` | same | rc 0, marker | `4b4d37c6` unchanged; covered gen 4 | rc 0, marker | ? |
| 04 | STARTUP-ENV `BASH_ENV="$HOME/saved.txt" bash -c :` | same | rc 0, marker | `5bfed5c8` unchanged; covered gen 4 | rc 0, marker | ? |
| 05 | PYTHON-IMPORT `printf 'print("IMPORTED_UNRECORDED")\n' > loose_module.py; python3 -B -c 'import loose_module'` | same | rc 0, `IMPORTED_UNRECORDED` | `0bfefa35`→`72e383c6`: gen 2 create, gen 3 write `7f938b43…`; nothing else | rc 0, marker; gens 4–5 same bytes | ? |
| 06 | PICKLE-CODE (CASES-5 §06) | same | rc 0, `PICKLE_EXECUTED` | `95d9cdcb`→`a42af6b2`: gen 2 create, gen 3 write `b26a48df…` | rc 0, marker; gens 4–5 | ? |
| 07 | DIRECT-REDIRECT-STDIN `bash < saved.sh` (cwd `v4-direct`) | same | rc 0, `SAVED_DIRECT_RAN` | `ddf9ec3d` unchanged; `saved.sh` `43d50a29…` 0755 covered gen 5 | rc 0, marker | ? |
| 08 | DIRECT-PROC-FD `exec 3<saved.sh; bash /proc/self/fd/3` | same | rc 0, marker | `60a8d7cc` unchanged; covered gen 5 | rc 0, marker | ? |
| 09 | DIRECT-READ-EXEC `python3 -B -c 'exec(open("saved.py").read())'` | same | rc 0, `READ_EXEC_RAN` | `013a7fb3` unchanged; `85ff61eb…` covered | rc 0, marker | ? |
| 10 | DIRECT-AWK-FILE `awk -f saved.awk` | same | rc 0, `AWK_FILE_RAN` | `d8926ac9` unchanged; `c6d3872b…` covered | rc 0, marker | ? |
| 11 | DIRECT-SCRIPT-HELPER `find . -maxdepth 0 -exec bash saved.sh ';'` | same | rc 0, `SAVED_DIRECT_RAN` | `2e761cf2` unchanged; covered | rc 0, marker | ? |
| 12 | RC-STARTUP `cd /tmp/v4-extra-7z89hz2f && bash --rcfile …/startup.rc -i -c :` | same | rc 0, `SAVED_RC_EXECUTED`; stderr only job-control notes as in round 1 | `fa507d92` unchanged; `a829afcc…` 0600 covered in tmp gen 67 | rc 0, marker | ? |
| 13 | EDITOR-SAVED-COMMANDS `cd … && ed -s < …/commands.ed` | same | rc 0, `SAVED_EDITOR_COMMAND_EXECUTED` | `d9937c1a`→`0e01afe9`: `commands.ed` `83f83d4d…` covered before; `ed` scratch file `/tmp/tmpfetmlc4` create/rename-to-hidden/unlink, gens 68–70, nothing left | rc 0, marker; gens 71–73 likewise | ? |
| 14 | JIT-SAVED-INPUT (CASES-5 §14) | same | rc 0, `JIT_SAVED_INPUT_EXECUTED 42` | `4e52d74c` unchanged; `machine.bytes` `11db5348…` covered gen 67 | rc 0, marker | ? |
| 15 | DISPATCHER-SAVED `…/dispatch --file …/instructions.ops` | same; setup installs dispatcher row | setup `stand-pkg install` → `SUCCESS 055b80ab…`; attempt rc 0, `DISPATCHER_SAVED_EXECUTED` | `e414f8f2` unchanged; `instructions.ops` `08a7984a…` covered gen 70 | rc 0, marker | ? |
| 16 | root-native-account-bypass `/usr/sbin/useradd -M -u 1998 -s /usr/sbin/nologin v4raw` (root) | records and applies | rc 0; account v4raw/1998/1998/[v4raw]/`/home/v4raw`/''/`/usr/sbin/nologin` | `283a37d0`→`ac90da40`: etc gen 165→255 (90 generations of `useradd`'s temp, lock, link and rename writes); `passwd`, `group`, `shadow`, `gshadow`, `subuid`, `subgid` and backups changed; `v4raw` absent before; after, own rows `bc3:account:v4raw` (every tuple field equal) and `bc3:group:v4raw`; success hashes the declaration; primary unchanged | same single operation | ? |
| 17 | ordinary-work (CASES-5 §17, one `set -e` shell) | all six succeed | rc 0; `TWO WORDS`, `SUCCESS 58ab1132…`, `PERSONAL_SCRIPT_OK:ordinary argument`, `SUCCESS eed04a1a…`, `Hello, world!`, `BC3 NETWORK PAGE`, `Edited document`, `BC3_ORDINARY_COMPLETE`; empty stderr | `caac85d1`→`4eafc779`: primary gains rows `bc3-personal` and `repository:hello` (report SUCCESS `eed04a1a…`); home gains `document.txt` = SHA-256 of `Edited document\n`, `page.html` = SHA-256 of the fixture page, `.w3m/`; etc rewrites five stand files | — | 1 |

How the outcome rule applies, per case:
- **01–15.** The rule needs two things: the way launches nothing that must be recorded and is not recorded, and the permitted
  action succeeds. The permitted action succeeded in all fifteen. In the declarations, what the way runs (the saved source) is
  covered before the read. The way itself left either nothing (02–04, 07–12, 14, 15: identical before/after snapshots) or only
  path rows written for it by the service (01, 05, 06: the source; 13: a scratch file created and removed again). Nothing else
  changed. This holds if the five filesystem declarations are a declaration. Q1 is open, so the outcome is “?” (see the Summary).
- **16.** The account exists and is covered by an own row in the designated `/etc` declaration that matches every tuple field. It
  holds under reading A of Q1/Q2, so the outcome is “?”.
- **17.** Every action of item 3 succeeded on the same image in one session. The script and the package are recorded in
  `machine.jsonl`, which is a declaration under both readings, so the outcome is 1.

## Ways not refused: does the builder's mechanism survive?

The builder supplied a mechanism for every way and for the account tool (`B2/ARGUMENT-5.md`), and no argument. The image runs
the same mechanism. So the test to apply is the one for a mechanism. The test for an argument (a step that needs a missing word,
or a concrete system that refuses the way and still allows the work) has nothing to apply to.

1. **Does it also stop the permitted action or the ordinary work?** On this image it does not. All fifteen permitted actions, the
   account action and all six ordinary actions succeeded (table above). From the code, the mechanism has limits that the
   committed list does not touch. All five roots are mounted `noexec` (`B2/build/bc3_filesystem.py` line 553), so a recorded
   script saved in the home cannot be started by its path; the case 17 script runs from `/opt/stand/pkgs/…`. It has no special
   nodes (the builder's own suite hit `mkfifo` → `EROFS`, `B2/BUILD-3.md` item 3) and no shared writable mappings (lines 9–11).
   None of these is a permitted action or an action of item 3, so none refutes the mechanism within this step. They bound its
   claim that the ordinary work stays possible to the committed list.
2. **Does it keep the way from launching what is not recorded?** Under reading A of Q1, yes, for these sixteen ways. The code
   holds bytes back until they are recorded: `write` stages the bytes in a root-only store; `commit` writes the declaration and
   `success.json`, switches `current`, and only then replaces the state that `read` serves (lines 151–198, 343–366). The
   service handles one request at a time (`nothreads` = `-s` in the packaged fusepy, `S5/raw/07-fusepy-options.txt`) with
   `direct_io` and zero cache TTLs, so no reader can obtain bytes that are not yet recorded. The evidence agrees: in 01, 05 and 06
   the create and write generations exist before the marker, and in the other cases the source is covered in the before-snapshot.
   One weakness: older blobs of the previous generation are kept in the root-only store. The builder conceded this; it had no
   effect here, because every rewrite in these cases used identical bytes or empty scratch files.
3. **Is what it records a declaration?** This is where the attempt to refute the mechanism stops: the answer is the author's
   choice (Q1). The lines are produced by the service from whatever any program writes: a shell redirection, Python, `ed`'s
   scratch file, `useradd`'s temp and lock files. The first generation was made by importing each existing directory tree
   (`install-bc3.py` line 18, `bc3_filesystem.py` line 110). Under reading B the mechanism records into no declaration, so it
   does not keep any of the sixteen ways from launching unrecorded code. **Verdict: under reading A the mechanism survives for
   all sixteen ways; under reading B it fails for all sixteen. It is not refuted by any observation or code fact independent of
   that reading.**

## Comparison with the expected result of `SUP1/step-5.md`

- “the ways in which a saved file is started as a program, sourced or used as a startup file will be refused while the recorded
  script runs” — **not met**. None of them was refused (SAVED-SCRIPT, SAVED-SOURCE, STARTUP-ENV, DIRECT-SCRIPT-HELPER,
  DIRECT-PROC-FD, RC-STARTUP all ran after automatic recording). The recorded script ran (case 17).
- “for at least one way in which a typed command makes a recorded interpreter read saved text and evaluate it, no mechanism
  will be found … so that the step ends with a written argument about that way” — **not met**. A mechanism was supplied for every
  way, and the step ends with no argument.
