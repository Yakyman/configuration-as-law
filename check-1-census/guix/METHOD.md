# W1 Guix census method — 2026-11-19

Official source research and the collector/reducer adaptation were done as two
separate steps.
The first manual classification is classification 1. The second, independent classification
(W2) and the comparison (W3) are separate steps; W1 does not read those
outputs.

Fixed definitions and failure condition: PAPER.html §5 and §9.2. No new precedence
rule is introduced after observing objects. A stand defect or missing provenance
is reported as insufficient evidence, not a definition-level counterexample.

The workload follows V1's short scripted CLI day, not 24 hours: ordinary-user
`guix install`, a user setting, documents, a root service change through saved
`config.scm`, then at least 120 seconds of service operation. The Guix system
closure is an operational recorded-membership proxy, not proof of the paper's
person-designated primary declaration. All automatic counts retain this caveat.

VM work occurs on <HOST> under <WORKDIR>/W1, without host sudo. Each VM has
4 GiB and 2 vCPUs. Long-lived download/VM/workload jobs use user systemd units.
Other work is limited to reading inputs and writing the records in W/.

The initial official image's GUI/console is accessed with QEMU HMP sendkey only
for bootstrap; a read-only 9p share supplies the public key and workload scripts.
The private key remains in the disposable server tree and is deleted at cleanup.
A root authorized_keys file is instrumentation, recorded separately from the
service declaration. Host port 22841 binds to loopback only.

The collector maps systemd facilities to Shepherd status and mcron schedules,
records every command status, and preserves optional facility failures rather
than treating them as absence. It walks the V1 roots (/etc, /var, /opt,
/usr/local, /srv, /home, /root, /boot), with /var/guix included and deduplicated.
Symlinked roots are resolved; descendant symlinks are not followed. The current
system closure, user package closure, Home closure, and other store objects are
kept separate. A full /gnu/store file walk is unnecessary for this membership
proxy; retained top-level paths are saved. /proc, /sys, /dev, /run, /tmp are not
general walk roots; processes/modules/driver bindings provide targeted coverage.
Firmware, arbitrary unowned files elsewhere, and complete runtime transient state
remain outside this census. Counts are overlapping grouped observations, not
counts of disjoint physical objects. Structural directories and builder accounts
may be grouped only with a complete member manifest and no silent truncation.

Observed timing: system reconfigure began at 08:50:00 UTC; stock `current-guix`
reconstructed the pinned channel d58da8a56b75af73a7b5466f7ef8a81679713aa3.
Initial Git pack processing dominated the wait; the source was not replaced and
no authentication bypass was used. The unprivileged Home/install/settings/document
script ran concurrently during that preparation, 08:53:50–08:54:13 UTC. Reconfigure
completed at 09:06:15 UTC. The final service dwell starts after successful SSH
activation. No claim is made that the short scripted workload lasted a full day.

The official image auto-started an Xfce desktop. The user work itself was CLI;
startup-generated desktop state is nevertheless included in the census. Three
console logins and the read-only 9p mount are disclosed instrumentation. A temporary
root tail of the bootstrap log to the serial port was stopped before final collection.

## Final collector correction and provenance

The first collector failed because getent was absent from PATH, which also left
the user home path empty. It was present at
/gnu/store/yj053cys0724p7vs9kir808x7fivz17m-glibc-2.41/bin/getent.
The final collector discovers that binary and records its path; nsswitch.txt
confirms passwd/group use files. The day was not repeated: only inventory was
rerun, 09:09:35–09:09:39 UTC, after the completed 120-second dwell.
raw/first-collection.tar.gz and first-collection-command-status.tsv preserve the
failed attempt; raw/final-collection.tar.gz preserves the successful census.
raw/first-day-driver-status.txt remains 1 because that original driver stopped
at its first collection error. Final command-status.tsv/mandatory-failure.txt
are authoritative for the corrected census. This is a stand defect, not a
hypothesis counterexample.

Guix 1.5's generated Shepherd configuration is a store path referenced from boot,
not /run/current-system/shepherd.conf. The collector captures 55 closure source
files, activation sources, runtime service detail and timer schedules.
The initial unsupported `herd status --verbose` probe was replaced with `herd
status root`; detail for every observed service is also retained.
Optional final failures report no root package profile, no mcron service, and no
user Shepherd socket. System Shepherd timers log-cleanup/log-rotation were
captured separately; these failures do not mean that the system has no timers.

A supplementary read-only capture at 09:11:36 UTC verifies default home files
against /etc/skel, /etc/hosts and sudoers against current-system outputs, and
system/Home/user profile boundaries. It is later than the frozen census; no
workload configuration was changed between them. Raw manifest, source and hash
comparisons are in supplementary-provenance.txt. The original image autologin
and its defaults must not be confused with the manually applied home.scm.

## Reduction and first classification

Initial reduction yielded 169 rows (raw/initial-residual.tsv). Before assigning
classes, operational directories under /var/db and /var/run and the two user
profile families under /var/guix/profiles were separated. The user package output,
profile/manifest, and two generated support paths were also separated. Final
residual: 178 rows. All 5278 walked entries and all 8567 top-level store paths
remain represented with full manifests; no object was truncated. Directory-only
structural groups (34 groups) remain one manifest-backed observation; ten build
accounts remain one family. This refines inventory grouping, not §5 definitions.

The first judgments are explicitly encoded in classify-c1.py and
c1-classes.tsv, separate from preclass.py. Automatic recorded labels use only
current system closure/executable/module membership and are unvalidated proxies.
Manual recorded judgments use captured evaluated declarations, service sources,
Home source/closure, or byte-identical skeleton/current-system copies. They remain
first interpretations of transitive description; they do not establish P1/P4 or
a general person-designation rule for package/store metadata. Interpreter-path
membership also does not prove that every script argument is declared.

The proposed definition ambiguity is the persistent imperative user package
selection, represented by one store profile/manifest and its generation-selector
family. The static ~/.guix-profile indirection is classified as Guix bookkeeping;
it is not counted as another independent counterexample. Seven hole-none labels
express provenance or grouping gaps only. No second classifier's output was read.

## Cleanup

The guest was powered off through `herd power-off root` at 09:12:38 UTC after a
`poweroff` convenience-command probe was unavailable. No forced VM termination
was needed. MainPID=0 and the closed forwarded port were verified before deletion.
The 3.7 GiB W1 runtime tree, including both disks, downloaded image, share and
server SSH key, was deleted by 09:12:59 UTC. See raw/guix/shutdown-verification.txt
and cleanup.txt. A failed, non-running first driver status is retained as evidence;
no W1 VM or background workload remains.
