# BC4 independent acceptance review

Status: accepted for the bounded BC4 scope. The implementation, corrected clean builds, complete runtime regression, rebooted two-build combined comparison, documentation and cleanup satisfy the stated acceptance requirements.

Recorded 2026-11-22 UTC. Scope: C2.1–C2.6, C3.1–C3.5, C9.1–C9.6 and the ordinary-work paths in Section 4.3. The review read the governing text and sentence identifiers, TASK-B2, B1 channel dispositions, the preceding testbed reports, the BC4 plan and static review, the amended channel modules, integration points, fixture producers, four BC4 self-tests and the final saved evidence. The review started no VM or probe.

## Resolved findings and preserved failures

The review found concrete defects during development and withheld acceptance until they were corrected and exercised in clean rebuilt images.

1. Initial application removal omitted generic AppImage dispatch, the non-entry execution negative used a fabricated path, and the OCI removal case covered only an already completed process. The corrected implementation dispatches AppImage removal, attempts an actual recorded non-entry native file, and removes a live OCI holder.
2. The first holder fixture did not prove descendant revocation. The corrected holder forks a surviving child, emits separate readiness markers, and the test observes distinct parent and child PIDs in the exact profile. Successful removal is reported only after both profile process lists are empty; the former entry, retained archive and restart then refuse.
3. The initial language suite lacked a positive native-extension case. The final deterministic wheel contains the recorded CPython `_bz2` extension, verifies that it loaded from the managed project, round-trips `abc`, and refuses after removal.
4. Development runs exposed an unusable updated-system entry and two ordinary-work helper-boundary failures. Fixed native arguments make the updated GNU ed entry usable. The compiler profile now admits the recorded GCC helper closure, while the public restricted-editor entry maps directly to the recorded editor with fixed arguments. Focused development evidence and the final clean-image suites cover the corrected paths.
5. Per-component exports did not establish that one complete declaration containing all new rows applies reproducibly to independent builds. The final procedure now mandates exact assembly followed by `combined-selftest.py --reboot`; HOWTO and CHANNEL-PATHS state this sequence. The final comparison uses the updated factory produced by the base transaction rather than appending rows to a stale factory.
6. The first final two-build comparison found a real nondeterministic initramfs: the two hashes were `d13d3daec8efe41bb1fd322f0ff1cd234fcd78f2a007632e184fc19e2083ae10` and `c557fc22a4ac5237c8c0572b633075d6883ee86c749e93b64d82b29fd4e47db6`. The base manifests and complete declarations consequently differed in one of 557 rows, the controller exited 1, and the combined stage did not run. This failure is preserved under `rebuild-attempt-1/`. Supplying the pinned source date to the existing reproducible initramfs mode corrected the recipe. A subsequent host-observation placement error returned 126 and is preserved under `rebuild-attempt-2/`; moving that observation inside the existing privileged build step corrected the host recipe without changing installed policy.

None of these failed observations is counted as a pass. The final recipe and complete runtime chain were rerun after the last correction.

## Final build identity

Two complete recipe executions succeeded from the same pinned inputs. The retained primary image SHA-256 is `6626fded301318907dc841d6dc5118e2eea36d075d2d1824f6a4f289f38e7fc1`; the independent peer SHA-256 is `62adffae74c1d95b0fc289c418420457d75c38306e1a456c8cc494950cf8b0eb`. Their 56 regular recipe-file hashes are identical. Both builds emitted the same complete factory SHA-256 `0cccc17c3d5ef98f37b90ecff4665711b4a99e2cd79571dd3688f124a4395b27`, base-manifest SHA-256 `389ef31925caf6029db0629fcc5073d5a2b45520113c45820a14480a1e9da1fc`, and initramfs SHA-256 `668563d9966420710c09b8826e1ccbcc9112ccbcc449782994cdb0b5321c4aac`.

The exported final factory has 553 rows, including 434 package rows and 31,247 base-file entries. All 24 installed implementation and self-test sources checked by `factory-info.json` equal the published recipe sources. This connects the reviewed source, installed tests, retained image, factory export and runtime results.

## Language channels: C2.1–C2.6

The corrected-image language suite ran in a fresh disposable VM. Its suite, whole-declaration verification, exact export and destruction all exited zero. The saved stream contains 79 named result assertions, no false result and an empty failure list.

Pip and npm admission embeds and re-derives complete exact locks and archives, checks supported dependency edges, refuses mutable/source/hook forms, and launches only fixed recorded entries in immutable roots. Exact pip/npm projects install and run through ordinary and privileged frontends. Omitted dependencies, changed hashes, alternate indexes and registries, VCS/local direct inputs, editable/link/workspace/global/prefix forms, raw interpreters and caller arguments refuse. Lifecycle metadata remains inert; wheel `.pth` and source-backend inputs refuse without executing their markers. Managed files resist writes, and copied or removed entries do not launch.

The native wheel loads `_bz2` from its managed project and emits `NATIVE_POSITIVE abc`; removal withdraws that entry. A separately recorded entry cannot load a mutable shared object. These mechanisms and results support the bounded `CLOSED` dispositions for C2.1–C2.6.

## Application channels: C3.1–C3.5 and C9.1–C9.6

The corrected-image application suite ran in a fresh disposable VM. Its suite, whole-declaration verification, exact export, helper observation and destruction all exited zero. The saved stream contains 131 named result assertions, no false result and an empty failure list. Both Flatpak helper paths are absent, the helper unit links to `/dev/null`, and its enabled state is `masked`.

The fixtures contain genuine OSTree/Flatpak objects, an official Type-2 AppImage runtime followed by a SquashFS payload, and OCI layout/index/manifest/config/layer objects. Exact source hashes, parsers, reconstructed rows and positive entries pass; checksum, permission, entrypoint and installed-payload tampering refuse. This validates finite format parsing and the prototype's extracted immutable runtime, not every upstream runtime implementation.

Pinned Flatpak import and its one entry work through both authorities. System/user/alternate-root/remotes/bundles, runtime changes, overrides, alternate commands, development mode, absolute frontend and helper routes refuse. The exact AppImage imports and its extracted recorded entry runs; direct downloaded execution, FUSE mode, copied extraction, self-update and unpinned manager forms refuse with generation unchanged. Removal withdraws both entries.

The OCI image and separate application row install, verify and run. The program observes only its image root, cannot create a network socket or writable output, and cannot execute the recorded non-entry native file. Tags, alternate roots, binds, overlays, exec/package-install, build/load/import/commit, privilege, host namespaces, devices, hooks and manager API forms refuse. Present `bwrap` is not an ordinary entry and refuses; absent alternate runtimes are recorded as absent.

For lifecycle removal, distinct holder parent and child processes are observed in the exact profile and both are absent before removal succeeds. Former launch, retained archive and restart refuse; the image then removes and final verification passes. These mechanisms and results support bounded `CLOSED` dispositions for C3.1–C3.5 and C9.1–C9.6.

## System and ordinary work

The corrected-image system suite contains 32 named result assertions, no false result and an empty failure list. The repository example installs a relocated immutable `hello` closure and launches it. It is explicitly a repository-install example rather than a live base-root package transaction. Separately, a trusted catalog created by real old/new package transactions changes actual package state from ed 1.19-1 to 1.21.1-1, verifies the complete package map and affected root state, and launches the updated `/usr/bin/ed` with fixed `--version` arguments. Tampered catalog application restores the preceding declaration; removal restores 1.19-1; reapplication and final factory restoration pass.

The corrected-image ordinary suite contains 59 named result assertions, no false result and an empty failure list. Actual HTTP response bytes are recorded, remain inert, import, and then run only at the managed entry. Exact C source builds under the recorded compiler policy, remains inert until a separate import, and then emits `BUILT_SOURCE_OK`. The scheduled service actually runs that program; alternate user-manager, transient and cron forms refuse. The restricted editor saves `Edited document`, while shell escape and command-output read refuse; the fixed text browser renders its recorded page.

Wi-Fi and Bluetooth evidence covers saved/prepared profile state only. It explicitly records no hardware test and `paired:false`; it does not claim connection or pairing. All added ordinary rows remove, old launches refuse, and final verification passes. Deliberately loading the parser and compiler policies in complain mode causes actual `code-boundary` verification failures; applying the declaration restores enforcing kernel policy and final verification.

Across these four corrected-image component suites, all 301 named assertions pass.

## Regression and independent comparison

The complete preceding regression chain was rerun against the corrected image. The transaction suite has 35 passing named assertions covering ten injected failures, two stalls, supervisor death, removal, descendants and shared ownership. The delayed boot test admitted no ordinary session before replay readiness, and all nine immediate-success add/change/remove power cuts replayed the reported generation. D01–D10, their peer checks and three cut checks exited zero. BC1 has 166 passing named assertions; BC2 has 133. All disposable regression VMs were destroyed.

The inventory result remains honest: `complete:false`, `p1:"?"`, 31,441 covered, 40,588 unknown and 1,264 unrecorded observations. It is bounded inventory evidence, not complete P1.

The corrected independent prior comparison applies identical complete declaration bytes and reports all 557 actual rows equal. This resolves the preserved initramfs failure without weakening the comparison or excluding the differing file.

Assembly emits exactly 19 new channel/ordinary rows and a complete 572-row declaration. Its channel machine SHA-256 is `60c73154a1e6ce8efc317f51e92bf579ba8f567954965407f20f17025ffa051f`; the combined machine SHA-256 is `29680919714eefb4c7fab885ddaed7ca482db9973280f27169f7e186cf65b257`. Fresh guests from both independent images apply those exact bytes. On each side all 572 rows verify before reboot, all eleven recorded channel entries launch with their expected output, scheduled execution emits `BUILT_SOURCE_OK`, and the declaration hash and all 572 rows verify again after reboot. Both snapshots contain all 572 successful rows; installed `stand-compare` reports all 572 actual observations equal. Recipe inputs compare equal, both combined VMs are destroyed, and `summary.json` reports `suite_exit:0` with no owned VM remaining.

The final cleanup record preserves the primary image unchanged with mode 0444 and the recorded SHA-256, reports no owned VM or QEMU process, removes the temporary independent build root and export archive, and records the validation service as successfully completed. BUILD-4 reports 17 closures in this round and 78 of 88 total; STAND contains exactly 78 `CLOSED` and 10 `NOT CLOSED` rows while retaining `STAND: partial`. SELFTEST, HOWTO and CHANNEL-PATHS describe the completed mandatory combined sequence and its limits consistently.

## Disposition and limits

The implementation and final evidence support all 17 requested bounded closures: C2.1–C2.6, C3.1–C3.5 and C9.1–C9.6. The Section 4.3 repository/base-update, download/import, fixed build/import, jobs/schedule, headless document/browser and saved-radio paths also have positive, refusal, removal and readback evidence appropriate to their stated finite scope.

`STAND: partial` remains required. The result does not establish universal package- or application-format coverage, every upstream runtime, hardware radio connection/pairing, complete P1 inventory, or the open M1.02/M2.02/M3.02/M5.01/M5.02 obligations. No reviewed obstacle is shown by a definition-only argument to occur in every possible system. The overall hypothesis outcome therefore remains `?`.

Final bounded BC4 acceptance outcome: `1`.
