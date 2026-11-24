# Final integration source review

Recorded 2026-11-23 UTC. Internal engineering review only; this does not accept the published cases or replace their second-party execution and separate review.

Scope: source inspection without guest probes. The reviewer did not implement the filesystem daemon, installer, state reader or case controller. The reviewer authored the account extraction helper; that helper is expressly excluded from independent acceptance here.

Disposition: no blocking defect found for executing the bounded seventeen-case builder suite on the final scratch image. This is not a universal P1/P2/P4 verdict.

## Findings

- Native account integration reads candidate immutable database blobs before generation publication. It derives account/group rows and exact database-setting rows before creating the generation declaration and success report. It does not snapshot already published live account state.
- The declaration and report become authoritative through one current-generation pointer. Filesystem callbacks are serialized; the in-memory state changes before the mutation callback returns. On an uncertain post-switch exception the daemon refuses further service pending restart. This is coherent for the bounded callback execution path; it does not establish universal kernel-cache, concurrent-observer or crash behavior.
- Native useradd is invoked directly with the original argv and effective root credentials. Its case requires exit zero, the exact expected account tuple, a matching prospective account row under a correctly identified filesystem success report, and a changed declaration. Refusal alone cannot pass the account case.
- An offline comparison confirmed exact equality of all fifteen saved-input command strings and the native-account argument list with command fields in their respective original Round-1 logs. There are fifteen way fixtures plus account and ordinary work, totaling seventeen.
- Each way checks executed marker or explicit refusal, exact saved-byte coverage and the same command with pre-recorded bytes. Inline-writing cases also require successful write audit entries; stale fixture execution following a failed write does not pass.
- Ordinary work uses one shell invocation with errexit, pipeline/redirection, declared personal script, package installation and execution, network request, browser rendering, and document editing. Required output markers and final document bytes are checked.
- Installation designates all five filesystem declarations alongside the original primary file. Account mode is enabled only for the /etc mount. Unit startup order and explicit mount readiness reduce accidental use of underlying trees; /etc is initially started last after units and enablement links are written.

## Material limits retained

- This review does not independently accept the account parsing helper. Its author should not be listed as its independent validator.
- The state reader validates declared reachable paths, mode/owner/group, file hashes and symlink targets, with a generation stability check. It does not independently recompute semantic account rows, compare every timestamp, inspect open-unlinked inodes or prove there are no undeclared reachable extras. Report its checked-path count accurately, not as a complete independent semantic census.
- Account case observations occur before and after invocation. Temporal ordering relies on source and transaction evidence; a passing final account tuple alone does not prove the absence of every possible transient inconsistency.
- The daemon is a bounded filesystem, not full POSIX support. Writable mmap, special nodes, ACL handling and other unsupported operations are not established. Five mounts do not establish mediation of all possible writes throughout the entire operating system.
- Installed native executables remain subject to existing boundaries. The fifteen ways may be closed by automatic recording; they are not necessarily execution refusals. Report that distinction beside any required header wording.
- No second-party published-case observation was performed by this review. Any source changes after the identities below require targeted reconsideration.

## Source identities

| Source under B2/build/ | SHA-256 |
|---|---|
| bc3_filesystem.py | `6a339ad7fba6bbfe39af2b54795238764452fb606cead5d92e83e834f1200326` |
| install-bc3.py | `f39794bbbc10409f7b1045a2cd0e6a8d56ea9025c88a9ee48d5469d6d41e447e` |
| bc3-state.py | `537663db5eeede204e28a7294d9862b015a265318cc03642afbe74908378d1a6` |
| bc3-selftest.py | `68cf337210fd012fc75e008c09c36af49f1a825a9fc491b500f6003a8412ec97` |
| bc3-fixtures.json | `1277fed54a24d19f04e566e88033fedf73a374be55b13745b8d9b4129c4e4aa1` |
| bc3-ready.py | `9b9cd54b35c4044a8a7f382736b35918fbb63822d30faf5b8ba63362681e590a` |
