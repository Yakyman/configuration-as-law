# Alma rehearsal repair plan

2026-11-23 UTC. Four fresh-clone rounds are available for FX-C1-REH-1.
The shared repaired harness must be ready before the first round starts.

Primary sources consulted before execution:
- https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/cli/commands/repoquery.py supports the `reason` query tag and translates escaped tabs/newlines.
- https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/package.py obtains installed package reason from its history record.
- https://dnf.readthedocs.io/en/latest/command_ref.html documents distinct user, dependency and group marks. A group mark is not silently recoded as user or dependency.
- https://rpm.org/docs/latest/man/rpm.8 documents package query format; RPM file modes and digest algorithm are manager records.
- `actions/ordinary.md`, `actions/alma.sh`, `actions/ordinary.sh` cite the prescribed ordinary-action tools and interfaces.

Expected before the first fresh clone: all nine prescribed actions return zero;
20 consecutive empty scripts return zero; bootstrap and native package queries
return zero; the repaired filesystem helper completes or identifies an explicit
instrument limitation. Numerical reductions must show L2 rows, known reasons
for more than 90% of packages and known integrity for more than 90% of packaged
regular files. No inventory or raw query stdout will be read. Only retained
stderr and coverage diagnostics may inform repairs. Every clone is destroyed.

Existing historical records already show successful Alma actions and transport,
but incomplete filesystem traversal and insufficient fact coverage. They do
not establish which package manager accounts for unknown reason facts.

## FX2 expected result, recorded before execution

FX1 established that every action and transport passed, integrity coverage is
98.84%, and native DNF group reasons account for most unknown package reasons.
The rebuilt helper emits filesystem failure diagnostics to stderr; FX2 should
identify the traversal defect without exposing raw inventory. Group reasons
remain unknown; expected reason coverage still fails unless a documented
manager record supplies a justified binary distinction.

The DNF command reference describes history userinstalled as including groups,
but current implementation differs: `dnf/db/history.py`, `user_installed`,
returns true for USER or UNKNOWN, not GROUP. UNKNOWN is treated as user-installed
on the stated guess that it was installed via RPM. The collector does not turn
that heuristic into a known installation fact.
Sources: https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/db/history.py
and https://raw.githubusercontent.com/rpm-software-management/dnf/master/dnf/cli/commands/repoquery.py .

## FX3 expected result, recorded before execution

The rebuilt helper handles the documented document-portal virtual alias
boundary explicitly. The selected-group adapter now seeks positive native
USER-selected group/environment linkage before expanding installed members.
Expected: collector exits zero if the only prior traversal error was the
portal boundary, and reason coverage rises if GROUP packages have the recorded
selection linkage. Missing linkage remains unknown; no threshold is forced.
The same nine actions and twenty transport calls must pass again on a fresh
clone; raw inventories remain unread.

FX3 pre-collector correction: independent source review rejected translating
selected-group membership into individual historical package selection.
The mapping was removed and deployed while the fresh clone was still executing
its actions, before collector startup. Native GROUP remains unknown; positive
group/environment linkage is retained only as provenance. The expected reason
coverage therefore remains below threshold. The portal repair remains the
functional change under rehearsal.

## FX4 expected result, recorded before execution

The local and deployed main controller, package adapters, selected-group helper
and FX runner hashes match (`fx4-local.sha256`, `fx4-deployed.sha256`). The
controller calls in-memory rehearsal counting unconditionally at finish;
its old conditional instrumentation guard is absent. Expect retained L2 and
package-fact counts, collector zero with the portal boundary, all nine actions
zero and twenty transports zero. Native GROUP remains unknown, so package
reason coverage is expected to remain below 90%. This is the fourth and final
fresh repair round; its exact readiness status will be reported.
