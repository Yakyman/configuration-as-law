# Independent round 3 review

Reviewed at 2026-11-22T10:14:18Z. This review covers the final recipe source, the retained rebuilt image, both independent build records, the complete round-3 evidence, the earlier-round regressions, and the claimed BC3 variant dispositions. It does not treat builder summaries as evidence when the corresponding raw output is absent.

## Decision

Accept the bounded round-3 result with **6 variants newly CLOSED and 61 CLOSED in total of 88**. The accepted new closures are **C1.6, C6.6, M2.01, M3.01, M4.03, and M4.04**. The testbed remains **partial**. In-scope variants **M1.02, M2.02, M3.02, M5.01, M5.02, and C9.6** remain **NOT CLOSED**. M1.01, M4.01, and M4.02 retain their earlier closures.

The first line of `../../BUILD-3.md` should therefore be `BUILD 3: 6 variants closed in this round, 61 closed in total of 88`. This count starts from the 55 accepted closures at the end of round 2 and adds only the six variants listed above.

## Source and mechanism review

The application transaction has a coherent durable authority order. A worker freezes the candidate, records its identity in `pending.json`, activates it, and completes every-line readback before exiting. The supervisor then selects and syncs the realized generation, atomically writes `last-success.json`, clears and syncs the pending journal, publishes the volatile readiness marker, and only then forwards `SUCCESS` to stdout. Recovery treats the durable success report as authoritative and the pending candidate as the possible live source. This makes a crash before the report restore the preceding declaration and a crash after the report replay the reported declaration.

Worker process-group ownership, process-start identity checks, the root-owned test setting, and the independent timer cover worker silence and supervisor death without relying on the applying process to remain alive. Recovery quiesces the union of target and candidate sockets, timers, and services; removes candidate-only contributions; rewrites target files, accounts, rules, and policy; then starts admitted sockets, timers, and services in that topological order. Existing identities must be deleted successfully; an absent identity is the only ignored deletion case. These details address the concrete inverse-operation failures retained in `ITERATIONS.md`.

The boot gate is also coherent for the observed system. `/run/stand-ready` is volatile and appears only after replay readback. PAM account admission and the ordinary launcher require it, while instantiated getty, serial-getty, logind, and user-session units both require and follow replay. SSH may listen early because that endpoint is itself part of replay readback, but no tested login session passed before readiness.

Removal uses the existing manager and process mechanisms rather than command-specific cleanup. Sockets and timers are withdrawn before services; manager cgroups and the code boundary revoke living holders and descendants; managed files, generated input-root copies, profiles, unit files, socket paths, and owned rules are replaced from the remaining declaration. The admitted job grammar permits only services, nonpersistent timers targeting declared services, and fixed Unix sockets targeting declared services. Other directives, dependency hooks, restart policy, user managers, transient jobs, cron/at routes, and direct manager mutation were already tested as refusals. Exact duplicate claims are admitted only when their required state is equal, so removing one owner preserves the contribution and removing the last owner revokes it.

`stand-inventory` is useful but deliberately incomplete. It enumerates filesystem trees including shared memory, accounts and groups, rights and configured login keys, system and reachable user-manager units, scheduled-manager configuration, kernel-visible keys, mounts, rules, listeners, saved networks, processes, namespaces, executable mappings, and accessible boot state before matching objects to declaration lines. Its summary nevertheless reports `complete:false` and `p1:"?"`; unknown file semantics, alternate managers and namespaces, resident modifications, inaccessible keys, and external firmware remain unresolved. This is the correct reason to leave M5.01 and M5.02 open.

## Evidence review

The two final build logs each report a complete 494-line, 28,840-file factory built from separate recipe roots. `final-provenance.json` records equal corrected recipe trees, distinct independently built image hashes, and installed hashes equal to the source for the image inputs. The later controller-only getty-instance correction is explicitly outside the image input closure and both its at-build and corrected hashes are retained. The local recipe checksum list verifies in full. `cleanup-final.json` records no remaining disposable VMs or source/builder disks and retains only the required final image, inputs, and evidence.

The final guest suite in `rebuilt/round3.jsonl` has 35 result rows and all pass. The ten injected failure checkpoints restore the previous generation, durable report, exact snapshot values, readiness marker, and absence of candidate-only files, account, unit, and rule. The two eight-second worker stalls restore in 27.277 and 27.407 seconds under the documented 60-second test deadline. Killing only the supervisor at the files checkpoint triggers independent recovery in 29.138 seconds, with the worker dead and no pending journal.

Removal evidence is substantive rather than a refusal-only result. The service had a manager relay, worker, and forked descendant; the recorded socket started the stopped service; and all captured holders were gone after removal. The original file, retained copy, generated snapshot, cache copy, socket path, units, and rule were absent or inactive, and launcher, manager, retained-container-name, and socket reconnection attempts failed. Shared-ownership tests retained exact program, service, timer, socket, account, and rule state after one owner was removed, then revoked all six contribution kinds after the last owner was removed.

All nine power-cut trials pass: three additions, three changes, and three removals were cut 0.213–0.482 ms after the first received success record. Each new boot selected the exact reported generation, retained the matching durable report, had no pending journal, and passed complete declaration readback. The delayed replay test made 167 pre-ready ordinary login attempts with zero successes and observed no premature operator session.

The main controller preserves exit 1 because its first auxiliary boot query used the invalid uninstantiated name `getty@.service`. That is an observation-harness defect, not a hidden pass. The original failure remains in `rebuilt/boot-order.jsonl`; a prerecord-backed fresh-VM correction checks PAM/readiness and both `Requires` and `After` for four instantiated session units, with all five assertions passing in `rebuilt/boot-order-corrected.log`. The aggregate result may include that correction but must not relabel the original controller exit as zero.

The external-root planting test reports every planted program/code-like/unsuffixed/container-tree file, service, timer, socket, cron entry, account, group, privilege rule, login key, firewall rule, listener, network, and boot file, then explicitly reports incomplete semantic coverage. The ordinary inventory invocation independently returns uncovered and unknown objects. This proves bounded detection, not P1 completeness.

The original D01–D10 regression exits zero; its two declarations are byte-equal, all 498 comparison values are equal, and all three boot recovery cases report verification. BC1 has 160 passing tests and no failures. BC2 has 129 passing result rows, three passing assertions, and a passing summary. For the two independent recipe builds, the complete applied declaration files are byte-identical, the exported snapshot hashes match, and the installed `stand-compare` emits 498 rows with every row equal and both sides `ok:true`.

## Variant assessment

| Variant | Review disposition | Grounds |
|---|---|---|
| C1.6 | **CLOSED** | The active declaration alone generates launch membership and the immutable input-root copy. Removal deletes the original and generated snapshot, while retained home/cache copies and earlier-generation routes remain nonstartable. T04 attempts all four locations; earlier loader/direct-entry regressions still pass. |
| C6.6 | **CLOSED** | The finite admitted activation graph is fully enumerated. Positive socket and timer activation precede removal; removal stops socket, timer, service, and descendants; post-removal service/timer/socket manager requests and socket connection fail. Unsupported independent manager routes continue to refuse in regressions. |
| M2.01 | **CLOSED** | Exact generations, selector, realization, and success report have explicit sync ordering. Nine immediate report-triggered cuts replay the exact reported generation, and the session gate prevents entry before replay readback completes. This closure is for durable exact generation and boot selection; it does not imply M2.02. |
| M3.01 | **CLOSED** | Failures during inert preparation and freezing cannot become a success report or live declaration. The preparation and frozen checkpoints restore exact prior state and remove candidate-only generation effects; the remaining phase injections provide supporting inverse-operation coverage. |
| M4.03 | **CLOSED** | The admitted service/timer/socket graph and nft rule backend have finite schemas. Positive activation, ordered quiescing, descendant removal, rule replacement, post-removal reactivation attempts, and earlier refusals for restart/dependency/alternate-manager edges cover that finite mechanism. C9.6 remains separate and open. |
| M4.04 | **CLOSED** | T05 supplies two explicit equal owners for program bytes/launch membership, service, timer, socket, account, and rule. Removing one preserves exact required state; removing the last removes the object, activation, descendants, identity, and rule. Conflicting shared claims are rejected at admission. |

## Variants that remain open

- **M1.02:** serialization and finite readback do not represent or verify every live cross-resource or device effect.
- **M2.02:** nine finite cuts do not establish complete replay of every runtime and hardware state, especially actual radio state.
- **M3.02:** the journal's total deadline is not an enforced end-to-end recovery deadline. Recovery itself can fail or stall, and the independent recovery unit can run beyond the remaining allowance.
- **M5.01:** the inventory exposes many unknowns and cannot classify all code, rights, managers, namespaces, keys, or firmware state.
- **M5.02:** the declaration language and verifier do not implement unrestricted algorithmic requirements or decide their semantic effects.
- **C9.6:** a frontend refusal and container-tree file census do not realize and then revoke a declared container name, daemon graph, image layers, and retained restart state.

These are implementation and evidence limits. The records contain no grounds for concluding that the same obstacles belong to every possible system. The overall testbed remains partial, and the round does not supply a definition-only hypothesis verdict.
