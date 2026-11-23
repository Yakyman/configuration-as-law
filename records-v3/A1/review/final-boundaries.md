# Final boundary review

## H1 in the 40-row resolved sample

Three sampled rows intersect H1.

- `nixos-6cad6264ed` is a direct H1 instance on the adjudicated facts. Its generated
  `ssh_config` is applied by the SSH client, so S2.2-7 can exempt it as a setting in force inside
  that program. Its connection and authentication choices also change what can be done beyond the
  client, so S2.2-1 and S2.2-2 require it. The current `SUPPORTED/NOT` disposition therefore does
  not survive H1. This is the same boundary c2 originally identified; the saved module source also
  establishes that the generated object contains operative client options rather than being an
  empty marker.
- `coreos-4d2a7c7537` contains service enablement directories and links applied by the service
  manager. As settings of that manager, they meet the S2.2-7 side of H1; because they select which
  other services start, they also meet S2.2-1 and S2.2-2. The current `SUPPORTED/MUST` disposition
  states only the second side of the collision. This is an aggregate occurrence: the whole row is
  required, but it contains affected setting constituents.
- `debian-c366c1919d` contains `ssh_config`, so its note's constituent-level NOT decision has the
  same H1 defect as the separate NixOS row. The aggregate row remains MUST independently because
  it also contains `sshd_config`, including the password-login rule covered by S2.2-15. It is
  therefore an H1 aggregate occurrence without changing the row's overall MUST result.

The specifically requested comparison cases do not add H1 occurrences. `coreos-d33aabe318`
records `iscsid.conf` as read by both `iscsid` and `iscsiadm`; the one-program condition is not met
on that saved fact. `ubuntu-a8d7f506ac` is a palette shared by multiple Newt applications, so it is
likewise outside S2.2-7's one-program exemption and remains MUST. The same reasoning preserves the
MUST results for the sampled `fstab`, CA directory, and GSS mechanism table, each of which has
multiple established consumers. The Thunderbird row establishes application preferences,
content, records, and state, but no cross-program effect needed for H1.

The two kernel-thread rows are consistently OUTSIDE under S2.5-1: they inventory runtime program
state rather than the kernel code or a recorded setting. With those moves alone, before accounting
for the H1 changes above, the resolved-sample status split becomes 16 supported, 15 refuted, 3
fact-wrong, and 6 outside.

## H4 aggregate membership

`guix-da5f01a3ef` should not be counted as a confirmed constituent occurrence. Its row evidence is
the exact 7,684-member `store-outside-system-closure.txt` list. Set comparison of the saved raw
inventories gives an exact identity:

`store-outside-system-closure = store-top-level − system-closure − user-closure − home-closure`.

The list has no overlap with any of the three closures. In particular, it excludes all 17 Home
paths outside the system closure, including the two confirmed Home compiled outputs and their
source partners, as well as the four user-only paths. The raw files and
`../in/raw/guix/closure-comparison.json` have the same capture timestamp, so the discrepancy is not explained by
a later Home generation. The comparison file correctly says that the Home paths are semantically
outside the system closure; it does not establish membership in this deliberately disjoint row.

The exact row list does contain 18 other `module-import-compiled` paths. Their source partners and
active fallback loaders remain unmapped. The correct bounded H4 status for `guix-da5f01a3ef` is
therefore factual-unknown, based on those 18 possible constituents, rather than
confirmed-constituent based on the excluded Home paths. This leaves 10 confirmed standalone H4
rows plus the confirmed Home aggregate `guix-25ad6943ae`: 11 confirmed row occurrences, six
standalone factual-unknown candidates, one factual-unknown outside-store aggregate, and one
fact-wrong empty output in the screened extent.

## H1 full-extent boundary check

The full-table method is appropriate as a bounded row-coverage scan. Persistent native unit files
with nonempty fragment paths are value-parsed settings applied by the service manager to other
processes, mounts, dependencies, timers, and resource controls. They are H1 instances even when
inactive, because startability remains a capability. Store unit outputs and the two unit-tree rows
are likewise valid row occurrences; counting them separately from the corresponding loaded-unit
rows is acceptable so long as the result remains explicitly row coverage rather than a count of
distinct settings.

The regenerated extent corrects the earlier name-only exclusions: related service units are now
distinguished from their child login/firewall mechanisms, sockets are factual-unknown unless their
endpoint type is established, the five proved multi-reader sysctl rows are excluded, the two
preset rows are unknown, and the three skeleton rows are unknown because S2.2-10 may decide copied
startup code. Those corrections are sound.

The earlier 731-row draft included two overconfident classes:

1. Nine confirmed loaded-unit rows have generated or transient fragments under `/run`:
   `arch-c5c3eb977b`, `silverblue-dc8fe5998a`, `ubuntu-96787848d5`,
   `debian-desktop-96787848d5`, `debian-desktop-0758efc3b0`,
   `debian-desktop-53d095e912`, `debian-desktop-fdb6cb41a8`,
   `debian-desktop-ba3d3e02a2`, and `debian-desktop-7218a536a4`. A nonempty fragment proves a
   file, but these files are generator output or transient manager state. S2.5-1 or the applicable
   source object must decide their treatment; persistence of an ordinary unit definition cannot
   be inferred. The `/run/current-system/sw/...` fragment for `nixos-9ffeccd130` is a path into the
   persistent system profile and does not have this defect.
2. `ubuntu-7ab5b73f41` establishes that `systemd-sysctl` applies the IPv6 values, but does not
   establish that procps `sysctl --system` is absent. Unlike the five excluded CoreOS/NixOS rows,
   a second reader is unproved rather than proved. The one-program premise is therefore factual-
   unknown, not confirmed.

Those ten downgrades are reflected in the final bound of 721 confirmed row occurrences. It is not
an exact complete extent: the 158 rows labelled factual-unknown
remain open, including sockets whose endpoint types are not captured. Correctly resolving those
facts can move the bound in either direction.

The revised agreed-sample audit is internally sound: 48 supported rows, 10 `CONFIRMED:H1`, and 2
factual-unknown rows. Its ten H1 cases consist of eight persistent file-backed unit definitions,
one stored native unit file, and the `newsyslog` values file. None depends on the sysctl,
transient-fragment, skeleton, or endpoint-name boundary problems above.

## H4 compiled-node execution boundary

The six extra compiled-node outputs currently marked `CONFIRMED-STANDALONE` do not satisfy H4's
execution premise for those exact row objects. `scheme-node` creates distinct source and compiled
outputs, and `node-source+compiled` creates an intermediate bundle whose FHS paths are symlinks to
those outputs. But `built-modules` then passes the bundles through `directory-union` with
`#:copy? #t`, expressly making regular files in the final output. `guix-command` adds that final
module union, rather than the six separate compiled outputs, to `%load-path` and
`%load-compiled-path`.

The compiled bytes can therefore execute from the copied union while the six exact store objects
remain build inputs. Removing one of those six objects does not trigger source fallback in the
already-built runtime union. Generic loader fallback cannot supply the missing same-object
premise. The following rows should be `FACT-WRONG` as H4 collision instances:
`guix-ba6bc2924d`, `guix-8fd6717fba`, `guix-9e2b09e306`, `guix-d6f4da0567`,
`guix-9849b393fe`, and `guix-0c0c8b4f78`.

The evidence supports a bounded H4 extent of **5 confirmed row occurrences**: two user
auto-compilation caches, two directly captured compiled module-import rows, and the Home aggregate
containing the direct imports. Seven rows remain factual-unknown: six unmatched module-import
rows and the outside-store aggregate. Seven candidates are fact-wrong for H4: the verified empty
output and the six copied-node inputs. The current `../RESULT.md` count of 11 confirmed H4 row
occurrences, its six-node table entry, and the corresponding extent rows require correction.
The headline finding of two confirmed hole types remains valid because the directly evidenced H4
instances are unaffected.

## Final acceptance

The regenerated records resolve the compiled-node defect above. H4 now has 5 confirmed row
occurrences (4 standalone and 1 constituent-containing aggregate), 7 factual-unknown candidates,
and 7 fact-wrong candidates; the extent TSV has the same 5/7/7 partition across all 19 screened
rows. The six copied-node inputs are absent from the confirmed examples and are identified as
fact-wrong with the exact-object reason. H1 remains at 721 confirmed rows and 158 factual-unknown
candidates with the stated 683/38 and by-kind breakdowns. The resolved and agreed sample counts
remain consistent with their audit records. No material contradiction remains in the final
`../RESULT.md` or the two extent records reviewed here.
