BUILD 2: 0 variants closed in this round, 2 of 88 closed in all

Recorded 2026-11-23 UTC. Scope: exactly the nine Round 2 owners in
[ROUNDS.md](ROUNDS.md). Outcome: `?`. The complete final run finished at 14:38:29 UTC after two
independent scratch builds. All nine Round 2 owners remain NOT CLOSED.
The [independent final review](raw/round-2/REVIEW-FINAL.md) preserves the two
previous closures; finite classifier and installer fixtures establish no new one.

## Built

- An independent census, completed before declaration matching, with an ordered
  four-question classifier. Required state and verified provenance identify an
  own, package or derived covering line. Missing facts remain `FACT_UNKNOWN`.
- Exact native package identities and a protected finite-installer receipt
  database for no-code packages, no-file dependency registrations and received
  defaults. Native package membership alone does not establish unchanged bytes.
- Validated copy and target-interpreter bytecode derivations, source-bound
  generated units, and an own-line chosen kernel setting with native readback.
  Existing file permissions, package databases, systemd and kernel interfaces
  provide realization and observations; no command-specific denial patch was added.
- Runtime processes, listeners and mounts remain diagnostic objects without a
  mandatory standalone line. Proven creator information can follow a covered
  program; absent creation provenance is explicitly unknown.
- Complete recipe deployment, fresh-machine object tests, retained full
  regression tests, and a complete example containing the six new object/unit
  rows alongside the existing channel rows.

The [mechanism and conservative interpretation](STAND.md),
[operation instructions](HOWTO.md), [validation ledger](SELFTEST.md) and
[nine-owner evidence map](raw/round-2/COVERAGE.md) distinguish implementation
success from variant closure. Other rounds retain their assigned scope.

## Fresh-machine evidence

The (not published: orchestration or scratch),
[final source changes](raw/round-2/FINAL-INPUT-CHANGES.md),
[source review](raw/round-2/REVIEW-FINAL-SOURCE.md) and
[82 frozen input hashes](raw/round-2/final-1-source-sha256.json) precede the
final machine observations. The [source comparison](raw/round-2/final-1-source-provenance.json)
records five new recipe files, six changed recipe files and 59 unchanged recipe
files; all carried self-test sources are unchanged. These are builder self-tests; no input-commit
prerequisite for the published hypothesis checks is claimed.

The primary scratch recipe passed at 13:01:34–13:03:07 UTC and the independent
peer recipe passed at 13:03:08–13:04:43 UTC. Final evidence is saved
under `raw/round-2/final-1/`. All 40 controller steps and all three lanes exited
zero. Their completion does not erase the retained boundary failures.

| Self-test | Result | Evidence under `raw/round-2/final-1/` |
|---|---|---|
| Ordered rules and concrete objects | 37/37 pure cases; 49/52 machine assertions pass, three actual boundary failures; 2/2 reboot assertions pass | `objects.jsonl`, `objects-reboot.jsonl`, `objects-evidence/round2-evidence/` |
| Independent census and every-line readback | Five internally consistent censuses, explicitly incomplete; all 553 final declared rows read back cleanly | Five census exports under `objects-evidence/round2-evidence/`; `objects-verify.log` |
| Carried shell, freezer, tools and supplements | Shell 22/28, reboot 1/1, freezer 9/9, tools 85/86, direct supplement 12/17, extra supplement 12/16; all required supported-operation assertions pass and all 16 prior boundary failures recur | `shell.jsonl`, `shell-reboot.jsonl`, `gate.jsonl`, `tools.jsonl`, `supplement-direct.jsonl`, `supplement-extra.jsonl` and their readbacks |
| Complete carried channel/regression chain | Language 79, applications 131, system 32, ordinary work 59, transaction 35, authority/frontend 166 and code/lifecycle 133 assertions pass; all nine power cuts and original D01–D10 complete | `carried-suite/`, `carried-suite/regressions/`, `regressions-console.jsonl` |
| Independent builds and complete example | Separate 557-row comparison passes; combined 578-row replay/reboot passes on both builds, 24/24 event assertions plus exact-declaration/schedule checks, every row equal | `carried-suite/regressions/independent-stand-compare.jsonl`, `complete-example.json`, `combined/` |
| Cleanup and evidence audit | No owned guest or peer remains; all eight offline audit sections validate with no missing/invalid evidence | `summary.json`, `steps.json`; [host readback](raw/round-2/adoption.json), [audit](raw/round-2/audit-final-1.json) |

The retained image is mode 0444, SHA-256
`6f7185e7590547a4fba9bfe8f4061306d6611e8cd6058111ead59d558af9451c`.
All 82 source files still match the frozen inputs. The complete 578-row
(not published: record outside selected evidence) has SHA-256
`5df1087f7a88b0af51ee358846a5f95a3877be583fb5ff79eb3e296b36d3828b`
for `machine.jsonl`; further identities are in [SELFTEST.md](SELFTEST.md).
The [reviewed audit correction](raw/round-2/REVIEW-AUDIT.md) preserves exact
systemd dependency membership while allowing printed token order to vary;
it changes no guest source or raw observation.

## What was tried and failed

The development scratch build completed. Its object suite had 52 assertions:
49 passes, two actual saved-code boundary failures and one faulty diagnostic
detector. Removal and reboot passed, with 553 final declaration rows verified;
the disposable guest was deleted. Evidence:
[object log](raw/round-2/development-1/objects.jsonl),
[reboot](raw/round-2/development-1/objects-reboot.jsonl),
[controller and cleanup](raw/round-2/development-1/summary.json).

The unsupported-algorithm operation correctly refused on stdout, while the
development detector checked stderr. Its failed raw assertion is preserved;
the final detector inspects both streams. The development alternate-root
installation failed because the test had not created its root directory.
That setup failure is not a successful policy refusal. The final fixture
creates the directory and inspects the actual database, file and report.

The [receipt correction](raw/round-2/RECEIPT-CORRECTION.md) removes an overclaim:
capturing a file alongside current package membership does not prove it remains
as received. No successful development count substitutes for final validation.

The final object observations retain three actual boundary failures: saved
bytecode, extracted code, and privileged native installation into an alternate
root/database. The latter reports `install ok installed 1`, reads back the
installed non-code file, and leaves the declaration/report unchanged. Its final
fixture is a successful bypass, not the development setup error. The received
default has now been consumed by recorded bytecode with output
`DEFAULT-LANGUAGE:en`; false derivation and unsupported-algorithm refusals passed.
See the final [object log](raw/round-2/final-1/objects.jsonl) and
[independent object review](raw/round-2/REVIEW-OBJECTS.md). The final audit retains
all three failures and the 16 carried boundary failures separately from passes.

Executable browser/WASI capability fixtures are unavailable. A passive browser
render does not demonstrate internal-code confinement. Listener creation
provenance and arbitrary configuration semantics remain unknown. The format
explicitly refuses unrestricted algorithms, so M5.02 remains open. These are
implementation limits, not added hypothesis rules or definition-only failures.

Direct privileged byte/mode edits are labelled breaking and tested only for
readback sensitivity. An actual privileged built-in installer bypass remains
a built-in-tool failure. Supported changes still use declaration transactions;
ordinary commands, document work and recorded script execution remain available.
