# Talos collector operational review

Recorded 2026-11-22T08:05:47Z.

Verdict: **the exact Talos collector cannot reasonably be expected to finish
tonight; ending the whole collector attempt is justified.** Talos should then be
reported as inventory unavailable, with a header-only part table. This is an
operational finding, not an object classification or a hypothesis outcome.

## Evidence

The selected (not published: outside selected checks and direct evidence) first saves a recursive
root listing (lines 87–90). For every listed regular path, it then starts
`talosctl read`, reads the first two bytes, drains the entire remaining stream in
one-megabyte blocks, and waits for exit (lines 93–103). There is no per-read
timeout, size bound, pseudo-filesystem exclusion, or checkpoint. `objects.tsv`,
`coverage.tsv`, and `limitations.json` are written only after every read finishes
(lines 109–113).

The saved listing has 145,301 lines and 25,244,948 bytes. Applying the collector's
own regular-path test to it yields 114,323 reads, including 359 paths ending in
`/pagemap`. The first such path is `/proc/1/pagemap`. See
`talos/listing-operational-counts.json`.

The contemporaneous process record shows the collector still reading
`/proc/1/pagemap` after 1,112 seconds. That one child had already transferred
more than 137 GB without reaching end of file. See
`talos/host-read-observation.json`.

The kernel's primary pagemap documentation states that the interface contains
one 64-bit value for each virtual page and advises efficient readers to skip
unmapped regions rather than read every entry:
<https://kernel.org/doc/html/latest/admin-guide/mm/pagemap.html>. The committed
collector does not skip unmapped regions. Hundreds of additional pagemap paths
and more than 113,000 other reads remain. The current read has no finite bound
enforced by the collector, and its observed duration and transfer volume already
exclude credible completion tonight.

## Required handling

End the entire Talos collector process tree rather than only the current read.
Allowing the parent to continue after selectively killing one path would change
the behavior of the committed collector. Do not modify, repair, resume, or rerun
the adapter, and do not construct an object table from partial API files held
before the unfinished loop.

Preserve the saved recursive listing, the two operational evidence files, the
collector and lifecycle logs, and the partial raw directory. Then destroy the
fresh VM through the selected runner. Because the exact adapter never reached
its output-writing section, generate `../part-talos.tsv` with only the required
header. `../READY.md` should state that the one committed attempt was terminated
after an unbounded full read of `/proc/1/pagemap` transferred more than 137 GB
for over 1,112 seconds, with 358 further pagemap paths and the remainder of
114,323 regular-path reads still pending. It should record this as the reason no
Talos inventory was obtained and as a deviation from completed execution of the
committed input.

This handling follows the one-attempt rule and the instruction to record exactly
why work that is impossible tonight could not finish, while preserving cleanup.
No live query or guest probe was performed for this review.
