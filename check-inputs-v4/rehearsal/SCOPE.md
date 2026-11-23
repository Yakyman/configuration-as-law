# Rehearsal continuation and acceptance

Recorded 2026-11-23 UTC. Existing per-system rounds and running durable services
are continued without resetting the four-round limit. Only their numerical
reductions are read. No classification or property assessment is performed.

Expected before remaining runs: all fixed actions return zero unattended;
twenty consecutive transport calls return zero; the collector completes within
1800 seconds, each query succeeds or has a named limitation, level 2 has rows
where available, and known reason and integrity facts exceed nine tenths of
packages. Unknown facts are not reclassified to satisfy the threshold.
The current package integrity counters report both any known file and all
listed files known; a high any-known count alone cannot certify full package
integrity. Directory/symlink verification and unsupported managers remain gaps.

Collector output is parsed only by the numerical reducer and then deleted.
A nonzero collector exit makes all its counts partial, even when individual
files exist. Historical rounds lacking a reduction-complete counter must be
read with the collector exit status in their status table; this applies to
AlmaLinux rounds 1–2, Void rounds 1–2 and Mint rounds 1–2. They are not accepted
as complete inventories. New rounds explicitly count successful collector exit
and complete artifact presence. Missing rows never imply zero or success.

The controller now verifies that the target disk is a qcow2 overlay whose
backing resolves to the registered read-only base. A fresh name is required.
A failed create is cleaned up only if its previously absent clone directory
now contains metadata. Successful clones are destroyed; failed graceful
shutdown uses kill followed by destroy, with both statuses retained.

New action batches run in a detached guest session with nohup/setsid, allowing
network reconfiguration to interrupt an SSH connection without killing the
batch. The ordinary action scripts and their per-action limits are unchanged
by this launch mechanism. References: POSIX nohup utility specification,
https://pubs.opengroup.org/onlinepubs/9799919799/utilities/nohup.html ; util-linux
setsid source/manual, https://github.com/util-linux/util-linux/blob/master/sys-utils/setsid.1.adoc .

No account quota/reset tool is exposed in this task environment. No quota or
reset time is assumed. Host work is limited to scripts, metadata and documents;
all guests run on the laboratory server under the existing slot mechanism.
