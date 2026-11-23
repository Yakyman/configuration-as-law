# Void repair summary

2026-11-23 UTC. Final status: **not ready**, following independent-review invalidation below.

| Defect | Repair | Evidence |
|---|---|---|
| Prior collector exited before queries | Shared host runner now supplies its laboratory root and separate stderr transport | Continued-round collector statuses and coverage under `diagnostics/` |
| Installed symlink integrity was discarded despite an XBPS target record | XBPS adapter compares the literal captured link target with the installation manifest, without following it | `collector/packages.py`, `xbps`; source excerpt `rehearsal/void/sources/xbps-manifest-excerpt.c` |
| Node loader requires newer C++ ABI | Language action explicitly updates libstdc++ with Node | `actions/void.sh`; `diagnostics/fx1/action-language_program.stderr` |
| Next Node startup requires SQLite session symbol | Language action explicitly updates sqlite as well | `actions/void.sh`; `diagnostics/fx2/action-language_program.stderr` |
| Earlier network action returned 8 | No new repair inferred; continued rounds 1 and 2 returned zero with the existing synchronization and service handover | `status.tsv`, rounds 11–12 |

The then-tested shared repairs inherited native-owned language package reasons and excluded
actual directories from the packaged-file denominator while retaining their
ownership. Numeric counts preserve the earlier failed rounds. No collected
object contents were read. All permitted diagnostic exposures are listed in
`FX-DISCLOSURES.md`; no ordinary action has been replaced.

Review findings relevant to Void: the latest completed continuation round must
be selected in regenerated READY and DISCLOSURES, and checksum manifests rebuilt
after writers stop. The historical release-evidence finding is handled by the
lead's document repair and does not require another guest probe.

Historical pre-review assessment (invalidated): **ready**, continued round 4 (status/count identifier 14). All nine actions
and 20/20 transport calls passed. Collector 0, 27.682 s, L2=2068; reason 530/546;
file integrity 37652/37931; whole 365.953 s; destruction 0. `FX-RESULT.json` is a
numeric summary derived solely from retained status/count records.

Remaining named limits: unavailable manager interfaces return 127; unsupported
npm per-file provenance and some Python request records remain explicit gaps.
The pre-review acceptance claim based on these thresholds is invalidated below. The historical network failure cause remains unresolved;
all four continued network actions passed without a new network-specific repair.

The final dependency fix is the consistent XBPS system update before tree,
followed by the selected installs. The final cowsay command uses npm's local
prefix form to preserve project-lock request/dependency records. Both exact
changes and their reasons are disclosed in `FX-DISCLOSURES.md`.

## Independent-review invalidation

The review rejected inferring a separate Python/npm package object's installation
reason from its native parent. That inheritance has been removed from the shared
collector. The original round 14 status/count evidence remains unchanged and the
old 530/546 reason count is historical, not accepted for final readiness.

Using only retained counts, conservatively remove all formerly known Python/npm
reasons: 530 - (40 npm dependency + 146 npm explicit + 2 Python explicit) = 342,
out of 546 packages (62.64%). This is a conservative numerical provenance bound,
not a new inventory or an exact recalculation of the repaired collector. More
than 90 percent known reasons is no longer certified. Final Void status is
**not ready**. All four new rounds are exhausted; a fifth is not permitted.

Nine actions, 20/20 transport calls, collector exit 0, L2 count 2068, measured
37652/37931 file integrity (99.26%), run duration and cleanup evidence remain
valid. No raw collection artifact was reopened for this correction.
