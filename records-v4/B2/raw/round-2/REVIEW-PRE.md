# Round 2 review: bounded closure criteria

Recorded 2026-11-23 UTC. This is a pre-build review of the Round 2 plan and
existing recipe. It is not acceptance of an implementation.

## Common evidence threshold

A closed row needs all of the following: a mechanism; a fresh-image attempt to
get an uncovered object/effect through that mechanism which fails; an
independent census of the concrete object/effect before it is matched to a
declaration line; and exact evidence for the claimed owning line and required
state. A command refusal, declaration enumeration, or a matching pathname is
not enough.

The census must apply the first affirmative question rule in S8.2-6. In
particular, package membership and unchanged package content are decided first
(S8.2-7--8), then executable code (S8.2-9--10), then settings
(S8.2-11--14), and only then program records or material (S8.2-15). Missing
provenance or semantics is FACT_UNKNOWN, not coverage. Inputs and expected
results must be frozen before the first fresh-image observation (Section 9.1
and A.4.1).

## Owner-specific criteria

| Owner | Minimum mechanism and fresh-image attempt |
|---|---|
| C1.3 | Census the concrete products of alternate-root, alternate-database and package-extraction operations, including non-executable package content. Show each is absent or covered by an own, package, or derived line under S8.2-16. Refusal of the manager command alone is insufficient. |
| C6.5 | Create or observe a generated unit, user environment generator and loaded cron command. Trace each executable/generated contribution to its actual owning source line. Do not invent a separate mandatory row for a runtime activation edge. |
| C7.18 | Establish the real provenance of executable bytecode/JIT cache. If it is executable, treat it as code/program and show its own/package/derived coverage; call it a record only after the code question fails. |
| C7.19 | The S8.2-21 exemption requires both execution inside a recorded renderer/helper and inability of the web code to launch programs or change installed state/settings. A text-only rendering result does not establish those facts. |
| C7.21 | Test the actual WASI runtime and preopened host directory. Determine whether its module is confined under S8.2-21 or is an own-process program under S8.2-22; partial rights do not settle the question by themselves. |
| C7.25 | A listener is runtime-only under S8.2-5. Identify and cover its creating program or setting; prove required-state readback where a declaration line makes a relevant claim. Do not require a standalone port line. |
| C8.08 | Test an untouched package default before any preference classification. A personal values-only preference is a program record only if it neither launches nor grants access (S8.2-14); a computer-wide chosen value needs its own setting line. |
| M5.01 | Demonstrate the finite typed format against an independent census containing a no-code package, dependency-only package, untouched default, edited setting, installed/extracted code and generated unit. Delete an owning line and inspect residual package/derived contributions, checksum, permissions and required value. |
| M5.02 | Do not close. Round 2 expressly retains unrestricted algorithmic/semantic validation as unsupported. Tests of a chosen finite format cannot establish that universal requirement, and neither Section 8.5 nor finite examples do so. |

## Existing-recipe risks to resolve in evidence

`build/inventory.py` currently derives file claims from declaration rows before
walking files. It emits a deliberately incomplete census and records broad
unknown classes; it does not by itself establish package provenance, untouched
package defaults, generated-unit provenance, or semantic capability facts.
The existing `round2-selftest.py` is an execution-boundary suite whose
bytecode/browser/WASI/listener tests do not supply the above object census or
coverage proof. New Round 2 evidence must make these limitations explicit and
must not reuse a launcher refusal as proof of recorded-object coverage.

