# X9 — Where 25 programs keep observed filesystem state

Outcome for O1, O2, P6 and the hypothesis: **?**. This is a descriptive corpus, not a classification or generation/archive test. Collection status: **? — unresolved trace attribution**, despite all 25 verified workloads.

**25/25 families have a verified scripted use with paired inventories and a trace.** 53 attempts are retained; 3 were not verified. Primary statistics use the highest verified complete attempt per family; every attempt remains in the path table.

Primary population is campaign B: all 25 first-use workloads on a second clean VM with persistent, per-run-verified runtime directories. Campaign A is retained as superseded evidence because its early GUI runtime directory disappeared. See campaign-A report and run log.

Frozen measurement/failure rules: protocol, preregistration hash, repairs/run log, independent review.

Clean Debian 12 VM on <HOST>, 4 GiB RAM/2 vCPU. All packages were installed before collection. GUI applications used Xvfb; ordinary programs shared one unprivileged home. The recorded environment sets MOZ_DISABLE_CONTENT_SANDBOX=1. PostgreSQL used its packaged account; Podman used guest root and the distribution default overlay storage driver (recorded in stdout). Each run has a script, strace -f with decoded file descriptors and file/write/process/mmap syscalls, and whole-root metadata inventories excluding /proc, /sys, /dev, /x9.

Primary provenance: OS, versions, mounts, provisioning, readiness and run order.

| Fixed metric | Observed value |
|---|---:|
| Distinct created paths, including unattributed | 2,058 |
| Exactly one observed creator / created paths | 2,053/2,058 (99.76%) |
| No / multiple observed creators | 5 / 0 |
| Exactly one observed mutator / created paths | 2,051/2,058 (99.66%) |
| No / multiple observed mutators of created paths | 5 / 2 |
| Mutated by exactly two / at least two / more than two families | 2 / 3 / 1 |
| Attributed mutation paths outside fixed XDG or /var/lib roots | 1,635 |
| All observed outside paths, including snapshot-only changes | 1,645 |

Numerators, denominators and run diagnostics: [analysis.json](raw-X9/analysis.json). Creator means observed creation during a script; mutator also includes later changes/deletions. Neither means semantic owner. A high creator fraction in a serialized sample does not show that a file has only one possible user.

| Program | Attempt | Attributed paths | Outside | Created / changed / deleted (all snapshot rows) | Evidence |
|---|---:|---:|---:|---|---|
| firefox | 3 | 195 | 0 | 197 / 2 / 0 | run.json, stdout.log |
| vim | 3 | 2 | 2 | 1 / 2 / 0 | run.json, stdout.log |
| emacs | 3 | 2 | 2 | 1 / 2 / 0 | run.json, stdout.log |
| nano | 3 | 1 | 1 | 1 / 4 / 2 | run.json, stdout.log |
| libreoffice | 3 | 40 | 1 | 39 / 4 / 0 | run.json, stdout.log |
| thunderbird | 3 | 77 | 59 | 78 / 2 / 0 | run.json, stdout.log |
| vlc | 3 | 2 | 0 | 2 / 1 / 0 | run.json, stdout.log |
| gimp | 3 | 65 | 0 | 65 / 1 / 0 | run.json, stdout.log |
| evince | 3 | 2 | 0 | 0 / 4 / 2 | run.json, stdout.log |
| git | 3 | 27 | 27 | 27 / 1 / 0 | run.json, stdout.log |
| ssh | 3 | 1 | 1 | 1 / 4 / 0 | run.json, stdout.log |
| sqlite | 3 | 1 | 1 | 1 / 1 / 0 | run.json, stdout.log |
| postgresql | 3 | 38 | 0 | 5 / 33 / 1 | run.json, stdout.log |
| podman | 3 | 21 | 4 | 15 / 7 / 0 | run.json, stdout.log |
| python | 3 | 1,490 | 1,490 | 1490 / 1 / 0 | run.json, stdout.log |
| node | 3 | 9 | 9 | 8 / 2 / 0 | run.json, stdout.log |
| gcc | 3 | 1 | 1 | 1 / 1 / 0 | run.json, stdout.log |
| go | 3 | 90 | 1 | 90 / 1 / 0 | run.json, stdout.log |
| rust | 3 | 25 | 25 | 25 / 1 / 0 | run.json, stdout.log |
| bash | 3 | 1 | 1 | 1 / 1 / 0 | run.json, stdout.log |
| curl | 3 | 2 | 2 | 2 / 2 / 0 | run.json, stdout.log |
| wget | 3 | 1 | 1 | 1 / 4 / 0 | run.json, stdout.log |
| make | 3 | 1 | 1 | 1 / 1 / 0 | run.json, stdout.log |
| tmux | 3 | 2 | 2 | 0 / 3 / 0 | run.json, stdout.log |
| gnupg | 3 | 5 | 5 | 7 / 2 / 0 | run.json, stdout.log |

Unverified attempts (retained; excluded from primary counts):
- vim attempt 1: exit 1, timeout False; run.json, stderr.log.
- gimp attempt 1: exit 1, timeout False; run.json, stderr.log.
- podman attempt 1: exit 125, timeout False; run.json, stderr.log.

Complete per-program path list: [X9-paths.tsv](X9-paths.tsv); compact examples for all 25: path guide. Filter primary_run=1 for the metric population. Unattributed rows retain background/uncertain snapshot changes; creator_supported distinguishes creation proof from later writes. Every row cites inventories and trace lines. caller_directed=yes marks only explicitly named outputs and does not classify them as data. Read-only and trace-only/transient paths are excluded from the persistent-file denominator; trace candidates retain the latter separately.

Observed shared mutation paths: shared.tsv. Read-only library use is excluded. The table does not establish that every listed program needs a path.

Shared paths: /home/subject/.local/share/recently-used.xbel (evince,gimp); /home/subject/work/shared.txt (emacs,vim); /run/user/1000/dconf/user (evince,firefox,libreoffice,thunderbird).

The largest contributor to the pooled outside count is python (1,490 paths). Python virtual-environment and bytecode products are included. The pooled metric weights files, not programs equally.

Coverage holes: Firefox has one literal ???() = ? at trace line 83271; its recorded syscall number does not recover the missing arguments/result. Podman has 86 unresolved namespace paths, 21 unresolved dirfd operations and 10 unsupported mount mappings; these counts can overlap. Parser diagnostics, including unresolved-or-nonfile descriptor events, are retained per run in [analysis.json](raw-X9/analysis.json). Unsupported mappings are left unresolved. Consequently the displayed fractions describe supported observations and are not certified complete ownership shares or numerical bounds.

GnuPG also created two persistent paths without a traced creator: ~/.gnupg/crls.d/DIR.txt and ~/.gnupg/private-keys-v1.d/<REDACTED-7>.key. The client trace, lines 643–657, shows an existing agent socket and IPC, consistent with daemon-mediated writes outside traced descendants. The exact creators remain unassigned; this is a concrete attribution hole, not a data/derivative rule.

All 50 primary inventories reported zero read errors. Runtime directories were checked before 24 runs; PostgreSQL had no exported runtime variable. Mechanical set arithmetic, primary selection, path-guide references and unchanged protocol hash passed validation. The independent assessment is in X9-REVIEW.md.

Limits: one distribution, one shared home, fixed sequential workloads; superseded retries are retained separately. The unit is pathname rather than inode identity; metadata snapshots detect surviving files, not all transient files or content changes. Helpers belong to run labels. Daemon-mediated activity outside traced descendants remains unattributed. Guest management SSH probes also generate background activity. Outside paths include requested documents/build products, temporary files and valid non-XDG locations; this is not a standards-violation count.

Concrete classification/need questions left open (paths and write evidence are in the TSV):

| Observed candidate | What this experiment cannot decide |
|---|---|
| /home/subject/work/shared.txt, written by Vim and Emacs | O2: the script requests a document; writer identity alone cannot classify it. |
| /home/subject/work/records.sqlite and /var/lib/postgresql/15/main | O2: database storage contains requested records alongside server-maintained structures; paths/writes do not supply a classification rule. |
| /home/subject/work/pyenv and /home/subject/work/rust-project/target | O1/O2: generated environment/build files do not reveal semantic ownership or future need. |
| recently-used.xbel and /run/user/1000/dconf/user | O1/P6: overlapping run labels establish writes, not which current or saved programs need these files. |

O1 remains open because observed writes do not show program need. O2 remains open where the same write mechanism produces requested documents/databases, generated code or program-maintained state. Shared writes are candidates for P6 study; no declaration, saved generation, uninstall or archive-setting transition occurred, so the fixed P6 failure condition was not exercised.

Campaign A: 214 copied files passed SHA256 verification; cleanup. Campaign B: 191 copied files passed SHA256 verification; cleanup. All raw attempts remain available. Reproduce derived outputs with python X/X9-analyze.py, then python X/X9-report.py and python X/X9-validate.py.
