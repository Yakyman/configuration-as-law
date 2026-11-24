# Gentoo rehearsal

Completed 2026-11-23 UTC. Instrument preparation only: no object was classified, and inventories were deleted unread. External acceptance remains RV-S4-P.

## Result

The second fresh four-slot Gentoo clone booted, attempted all nine unchanged ordinary actions, and the extended collector completed with status 0. Seven actions succeeded; browser extension and container execution failed. Thus the machine-level inventory fact G01 is obtainable, but successful completion of every ordinary action is not established.

| Phase | Exit | Seconds | Evidence |
|---|---:|---:|---|
| Fresh boot | 0 | 16.480 | `S4/rehearsal/gentoo/round2/status.tsv` |
| Ordinary action batch | 1 | 566.034 | same; individual `actions.tsv` |
| Extended collector | 0 | 116.237 | same |
| Destroy | 0 | 2.714 | same |

The browser action failed in 9 seconds: its diagnostic requires the environment variable `MOZ_REMOTE_ALLOW_SYSTEM_ACCESS=1`. The unchanged helper passes a command-line switch but not that environment variable. The container action failed in 258 seconds: `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?` The diagnostic proves endpoint unavailability at that command; it does not establish the daemon's underlying failure cause. Neither action was repaired or rerun on the clone. Sources: `round2/action-browser_extension.stderr`, `round2/action-container_run.stderr` and committed `check-inputs-v4/actions/gentoo.sh`, `gentoo-firefox-addon.py`.

Collector-owned numeric diagnostics (`round2/.inventory-unread.diagnostics.json`) report 32,756 objects, 1,193 level-one rows, 31,563 level-two rows, 109,382 package-file rows with 109,059 known integrity values, and 152,219 full digests from 152,220 requested. Traversal completeness is true; package-ownership completeness is false. One requested full digest remains unavailable; no path or reason is inferred from a numerical aggregate. The diagnostic index reports 657 active `/etc` members and two completed opaque-store traversals. These are instrument coverage counts, not decisions or universal completeness claims.

## Inputs, slots, and cleanup

Primary implementation: `check-inputs-v4/lab.sh` acquires the base metadata's four nonblocking shared slot locks before QEMU, assigning 4096 MiB and two CPUs per slot. Its durable user service waits up to 240 seconds for silent `exit 0`. The first slot preflight found ten free slots. Both fresh clones used the same read-only registered Gentoo backing image through (not published: record outside selected evidence); keys, installation inputs and shared slots were linked to existing laboratory inputs. The preflight is not an explanation of the first-night startup failure.

`round2/source-before.sha256` was captured before collection and `source-after.sha256` after destruction. Every listed staged wrapper, Python/Go source and compressed probe hash is identical. No ordinary-action source was modified. 

The finished marker was checked together with absence of `.inventory-unread` and (not published: record outside selected evidence); the earlier clone and inventory were also absent. Only numeric diagnostics, coverage, status, sanitized stderr and source hashes were copied locally. No object, member, raw stdout or fact table was opened or retained. Diagnostic reads included the browser/container failures and the numeric summary. Other retained query errors are available for external review, with exact statuses in `coverage.tsv`.

## History and expectation

`D1/in/FACTS.md` establishes that no first-night Gentoo inventory exists and the startup cause is unknown. Neither unknown-row table contains a Gentoo ID; G01 therefore has zero existing rows to match. `check-inputs-v4/READY.md` records an earlier successful collector and browser-action failure, but does not prove a fresh run. Before the first rehearsal, the written expectation was successful boot with four free slots, nine unchanged actions attempted, and collector completion, with browser success uncertain.

An initial host launcher used a relative Python path and exited before harness execution: no status file or clone existed. The absolute runtime argument fixed that control setup before the actual launch. Clone names used the required `reh-` prefix; no guard was weakened.

First actual rehearsal: boot 0/16.481 s. After fact queries, quadratic directory indexing consumed excessive CPU; the assembler stopped that exact collector with SIGTERM, yielding -15/460.573 s, then destruction 0/3.236 s. Evidence: `S4/rehearsal/gentoo/status.tsv` and `controller-stop.json`. The indexing repair made a single equivalent pass. The second fresh rehearsal tested that revised source; its successful status does not erase the first failure. Before second collection, the expectation of completion within the existing bound was recorded and source hashes captured.

Historical Portage reasons remain limited: `check-inputs-v4/collector/portage-reasons.py` marks selected atoms explicit only for unique installed matches; other historical reasons remain unknown because `--oneshot` may omit direct requests and current dependency edges do not establish history. `check-inputs-v4/collector/PACKAGES.md` documents CONTENTS full-MD5 and symlink-target checks. No historical reason was invented.

## Commands

From the laboratory root, with the published S4 collector staged and isolated lab initialized:

```sh
S4/lab-gentoo/lab.sh new reh-s4-gentoo-2 gentoo
# Stage the unchanged C1/actions directory and run its guest entry once:
bash gentoo.sh
# After actions, on the host:
LAB_ROOT=S4/lab-gentoo check-inputs-v4/supplement-1/step-4-instruments/S4/collect.sh --rehearsal reh-s4-gentoo-2 S4/rehearsal/gentoo/round2/.inventory-unread
S4/lab-gentoo/lab.sh destroy reh-s4-gentoo-2
```

The complete durable staging/action/collection/cleanup sequence is `S4/rehearsal/gentoo/run2.py`. Runtime laboratory paths are expanded to absolute paths. Observation commands are committed separately by the assembler; these rehearsals authorize no observation or object decision.
