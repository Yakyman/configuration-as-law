# Alma instrument preparation

2026-11-23 UTC. No inventory observation or object decision is made here.

Primary documentation consulted before rehearsal:

- https://help.gnome.org/system-admin-guide/dconf-profiles.html — a profile selects user and system databases; a profile reference establishes configured use, not historical reading.
- https://teams.pages.gitlab.gnome.org/websites/help.gnome.org/system-admin-guide/dconf-keyfiles.html — system databases use GVDB and correspond to `.d` keyfile directories.
- https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/automatically_installing_rhel/creating-kickstart-files — “all choices made during the installation are saved into a Kickstart file named `anaconda-ks.cfg`”. Generated directives can establish recorded values, but do not distinguish an installer default from human intent without a retained original recipe.
- https://docs.npmjs.com/files/package-lock.json.html — `integrity` identifies the archive artifact used at that package location. The shared npm adapter verifies retained artifact bytes before comparing full installed member hashes.
- https://docs.podman.io/en/latest/markdown/podman-images.1.html — `RepoDigests` records repository/digest names; neither that field nor image creation date identifies who pulled an image.

## Rehearsal 1 expectation (written before starting)

A fresh copy of the committed Alma installation should boot with one available slot. The unchanged nine ordinary actions should finish; the extended collector should finish with status 0. Current dconf compiled values, profiles and key semantics should be obtainable. A `/proc` map snapshot can identify currently mapped system databases; absence cannot disprove earlier use. Current installation directives and configuration contents should be obtainable where retained. Human intent and unlogged historical events cannot be reconstructed from current-state queries alone. Inventory and query stdout will be deleted unread; only diagnostics and numeric summaries retained. The harness waits for final assembly before collection.

Commands on the laboratory server, from the task root:

```sh
systemd-run --user --unit=s4-alma-rehearsal-1-start --working-directory="$PWD" --property=MemoryMax=2G --property=CPUQuota=100% python3 S4/rehearsal/alma/run.py
```

The copied laboratory runner acquires a numbered shared slot for the VM and creates `reh-s4-alma-1`; the harness destroys it in `finally`. `S4/rehearsal/alma/run.py` contains exact action staging and collector commands. It consumes unchanged (not published: record outside selected evidence), copied byte-for-byte from `check-inputs-v4/actions/alma.sh`, together with the shared action files.

## Added table

`alma-facts.tsv` columns: `object_id`, `path`, `fact`, `value`, `status`, `evidence`. Join `object_id` to `objects.tsv.id`; for a stored group, the attached path is an immediate child or a referenced related configuration source. `compiled-values` comes from a synthetic profile selecting exactly the existing system database; the command only dumps and never updates it. `key-semantics-schema-evidence` lists exact schema XML evidence references. `current-reader-snapshot` is limited to mapped system databases and the DCONF_PROFILE variable. Installer evidence omits secret directives and redacts credential arguments. Current policy and transaction summaries explicitly do not assert human intent or complete history.

Harness launch correction: the first unit had no working directory and exited before opening the script or creating a VM. The corrected unit sets the laboratory working directory explicitly; this is not a guest or fact-query attempt.

Before collection, the evidence plan adds three distinct historical routes: generated/original installation directives; retained journal/audit operation records; current package scriptlets and unit presets. Their presence can support a causal account; absent or insufficient records cannot establish unrecorded human intent. The audit query retains operation/result identifiers only; journal messages are restricted to relevant account, acquisition and configuration operations, with credential arguments redacted. Package scriptlets are published package text, not proof of past execution. The process evidence is capped at 1 MiB per maps/environment input and reports exceeded caps and inaccessible/exited processes explicitly. No other environment variable is emitted.

Pre-collection diagnostics: boot exit 0 in 16.425 seconds; unchanged ordinary actions exit 0 in 92.116 seconds, all nine action statuses zero (`S4/rehearsal/alma/actions.tsv`). The harness removed action logs from the clone and is waiting for the collector assembly gate. Action statuses/durations are diagnostic records, not object facts.

Missing-fact grouping counts for the two committed tables: npm original member integrity 50; installer choice/default distinction 8; unit disablement history 2; opaque store contents 2; key acquisition history 1; ALSA content/creator 1; persistent SELinux boolean creator 1; compiled dconf contents/use 1. Total 66 distinct Alma rows. These groups concern missing evidence only and assign no decisions.

## Rehearsal 1 result and next expectation

Collector exit 0, 186.034 seconds; destruction exit 0, 2.872 seconds. Diagnostic counters record 5 compiled database dumps, 358 current-content rows, three historical evidence routes, 3/3 completed opaque-store traversals (72,148 members), 24/24 decoded font caches, and 4,781/4,783 full digests. The inventory and throwaway clone are deleted; `S4/rehearsal/alma/.inventory-unread.diagnostics.json` is a numeric reducer output, not an inventory. Reads were limited to action statuses, coverage diagnostics, stderr and numeric summaries.

The lock-addressed npm adapter produced no package/member facts on this global installation. The next, distinct evidence route will use retained cache-index receipts and installed metadata to find exact-version archives, validate their integrity and compare full member bytes. This will be rehearsed on another fresh clone with unchanged ordinary actions. It does not rerun the same failed query shape or change the ordinary actions.

Before the second collection, current boot-environment bytes are added as bounded base64 (`current-content-base64`), and NetworkManager files receive a guest-side nonsecret field allowlist. The latter emits connection identity, Ethernet and IP routing fields only; it never saves the raw credential-bearing file. Expected result: these current values can be captured without inferring who chose them. The source amendment precedes the second collection gate. The npm fallback now includes installed metadata receipts and a cache-index route; a cache identity match alone is explicitly a comparison reference, not an installation receipt.

## Rehearsal 2 interrupted before extensions

The collector was terminated by signal 9 after 74.046 seconds, during the native package-digest stage and before the npm or Alma extension ran. The cause is not established: collector stderr was empty, the user-service journal showed a 729.4 MiB peak with no OOM entry, and kernel-journal access was unavailable. No source-stage fault is inferred from a signal. Destruction returned 0 in 2.840 seconds; clone and inventory absence were checked. Status and coverage are retained in `S4/rehearsal/alma/round2/`. This does not count as a failed query of the new npm evidence route because that route was never reached.

A fresh third rehearsal will preserve cgroup memory events before and after collection to distinguish a resource-limit kill from other causes. The expected result remains collector exit 0 with the changed npm reference queries and the added boot/network values. Ordinary actions remain unchanged. The common collector index may use a precomputed directory index with equivalent mapping output; that optimization will be staged before the gate.

## Final rehearsal result

Fresh rehearsal 3: boot exit 0 in 16.472 s; unchanged actions exit 0 in 112.360 s (all nine individual actions zero); collector exit 0 in 120.522 s; destruction exit 0 in 2.879 s. Evidence: `S4/rehearsal/alma/round3/status.tsv`, `actions.tsv`, `coverage.tsv`, and `.inventory-unread.diagnostics.json`. Every query named `s4-*` returned zero. Memory-limit event counters are all zero (`collector-after-memory.events`). No inventory was read; the collector's numeric reducer was inspected. Clone and inventory removal were verified after destruction.

The final numeric diagnostics report five compiled dconf database dumps, 358 current-text content rows and 444 Alma fact-table rows; 41 integrity-verified cached npm archives, 459 equal member hashes and 52 directory records; three complete opaque-store traversals with 72,148 members; 24/24 decoded font caches; and 4,790/4,793 requested full digests recorded. The npm fallback records equality to a cache identity reference, explicitly not proof of historical acquisition from that archive. A file without a usable full digest is left unknown, never treated as equal by prefix.

All source files used by Alma were byte-identical before and after the final run (`source-before.sha256`, `source-after.sha256`); only the unrelated Talos extension changed during that interval. The executed Alma extension SHA-256 is `2cdf9d5826fcc5b1286fe0d2b0724b17082aa770dc6bfa55caed2f5ae3489344`; common extension SHA-256 is `81e4a94efd3da2a7cb6cc2229f868e025c6b46ed3825786a2e2ff99e9ffdff78`.

Historical completeness remains unestablished after the three different retained-evidence channels: original/generated installation directives, retained journal/audit records, and package scriptlets/current presets. In particular, erased or unlogged acquisition, human choice, configuration creator and enablement history cannot be recovered by reading current state. The collector records available evidence and explicitly labels its limits; no case receives a decision from this preparation. Dconf reader evidence is a bounded current snapshot, not proof of all past use.

Exact final rehearsal invocation, after the unchanged ordinary actions and with a new empty output path:

```sh
LAB_ROOT=S4/lab-alma check-inputs-v4/supplement-1/step-4-instruments/S4/collect.sh --rehearsal reh-s4-alma-3 OUTPUT
```

For the separate authorized observation, after the inputs are committed and a fresh `d1b-alma` clone receives the same ordinary actions:

```sh
C1_INPUTS_COMMIT=INPUTS_COMMIT LAB_ROOT=LAB_ROOT check-inputs-v4/supplement-1/step-4-instruments/S4/collect.sh --observe d1b-alma D1b/raw/alma
```

`INPUTS_COMMIT` and `LAB_ROOT` are operator-supplied values, not machine-specific publication paths. This preparation does not run that command. Independent acceptance belongs to review RV-S4-P.
