# Fedora continued rehearsal preparation

2026-11-23 UTC. No new virtual machine is launched until the lead releases the
check-1/check-4 ordering gate. Four fresh continued rounds are available.

The prior round 2 record has twelve of thirteen actions zero; Homebrew's action
returned 56 within its first recorded second. No action stderr was retained in
that pass. Therefore its precise cause is unknown. curl's official manual calls
56 “Failure in receiving network data.” Source: https://curl.se/docs/manpage.html
(exit codes). The installer download is the first network call in that action.

Repair: retain the same Homebrew installer, prefix, and hello package; download
the installer with three bounded `--retry-all-errors` retries into `--output`
a temporary file, then execute it and remove it on success or process exit.
The curl manual explains that an output file is reset before retries whereas
redirected stdout can duplicate partial data. No download error is suppressed,
no shell is run from an empty download, and no package/action is replaced.
Sources: https://curl.se/docs/manpage.html#--retry-all-errors ;
https://docs.brew.sh/Installation (noninteractive installation).

The prior known-reason count 1679/2248 and known-file count 141282/211683 did not
meet acceptance. Shared collector repairs now distinguish non-file directories,
verify symlink targets, and reconcile native-owned language package reasons.
DNF group/external/absent reasons still remain unknown; the first new numerical
reason counters will show which limitation remains. No Fedora-specific
collector change is made here.

Expected before continued round 1: bounded download retries remove a transient
receive failure if that caused the old status 56. All thirteen actions must end 0;
collector 0, only named query limitations, nonzero L2, both known fact ratios over
90 percent, whole run under 1800 seconds and twenty transport calls 0. Diagnostic
stderr and coverage may be read only after being saved under `diagnostics/` and
listed in `FX-DISCLOSURES.md`; collected content remains unread and deleted.

2026-11-23 09:48 UTC: the ordering gate was released. Continued round 1 starts
on a fresh clone under a durable driver capped at 4 GiB, 256 tasks and 2100
seconds. The VM separately holds its registered laboratory slot. Source and
staged action/library/harness/collector hashes are saved in `fx1-source.sha 256`
and `fx1-staged.sha 256`; the two sets match.

Continued round 1 completed: actions 13/13, transport 20/20, collector 0 in 144.971s,
L2=6870, file integrity 164540/169962 (96.81%), reasons 1679/2248 (74.69%),
whole 308.750s, destroy 0. The file threshold now passes; the reason threshold
still fails. Retained numerical reason counts show 334 native RPM group reasons,
2 unknown RPM reasons,77 RubyGems unknown,78 npm unknown and 78 Python unknown.
Native parent reason inheritance is absent. Optional interface failures match
COLLECT.md: missing selected-group history/OpenRC tools (127) and an unavailable
user-session bus (1), with precise stderr preserved and disclosed.

No action replacement is indicated. The collector's missing own-manager reason
evidence was reported to the lead before any shared collector change; this
system part does not edit shared collection code.

Before continued round 2: the lead confirms that group selections and native
parent-package provenance must not be converted to individual install reasons.
No documented missing source has been established that resolves these unknowns.
The user requires fresh rehearsals until readiness or four continued rounds;
therefore proceed with the same repaired instruments and disclose the expected
persistent reason failure, without altering the workload to manufacture facts.
Expected: all actions and transport remain zero; collection succeeds within the
bound with positive L2 and high file integrity, but reason coverage may remain
below 90 percent. This is the mandated fresh round, not a claimed new reason fix.

Continued round 2: all 13 actions 0; transport 20/20; collector 0 in 145.872 seconds;
L2=6870; file integrity 164540/169962; reasons 1679/2248; whole 309.793 seconds;
destroy 0. The same factual reason limitation persists.

Before round 3, source review found that Homebrew was absent from manager
discovery despite being in the fixed action list. A bounded discovery-only patch
adds `brew` to command-v checks, includes its documented Linux prefix, user
`.linuxbrew/bin` and scanned custom `/bin/brew` directories, and records an
explicit unsupported-adapter gap that clears ownership completeness. No brew
package, ownership, reason or integrity fact is invented. Source:
https://docs.brew.sh/Installation . Exact diff: `homebrew-discovery.patch`.
The patch is applied only after round 2 cleanup and awaits independent source
review before deployment/round 3. The expected reason limitation remains; the
new expectation is explicit Homebrew coverage incompleteness in collector gaps.

Independent source review accepted the Homebrew discovery-only patch before
round 3 (`HOMEBREW-REVIEW.md`). The host collector also emits the numerical
`collector:unsupported-brew-adapter` count from its in-memory explicit gap list;
it emits no manager inventory content. This preserves a concrete coverage-gap
count after raw metadata deletion. Both packages.py and main.py were deployed
together; round3 source/staged hashes match. This new revision is not claimed
to have been rehearsed retroactively on any earlier completed system.

Continued round 3: actions13/13, transport20/20, collector0 in144.696seconds,
L2=6870, reason1679/2248, file integrity164540/169962, whole299.280seconds,
destroy0. The new unsupported-Homebrew counter is1 (aggregate gaps164): the
previous discovery blind spot is now explicitly represented, not silently
accepted as complete coverage. No package facts were added or inferred.

Before continued round 4: no further justified reason repair is available.
Expect the same failed reason threshold with working actions, transport and
collector; this is the final fresh round required by the user's four-round
limit. The independently reviewed Homebrew discovery revision is unchanged.
The collector source/staged hashes will again be retained before launching.

At10:13UTC the lead deployed a later harness stderr-retention repair for timed-out
partial action batches. Fedora round4 was already running the prior loaded
harness and retains its own pre-launch hash evidence. It is not attributed to
that later harness revision; its completed action statuses are unchanged.

Continued round 4 (final): actions 13/13, transport 20/20, collector 0 in 144.851 seconds, L2=6870, reason 1679/2248, file integrity 164540/169962, whole 297.981 seconds, destroy 0. Unsupported Homebrew adapter count remains 1. All four rounds are exhausted; final status is NOT READY because reason coverage is 74.69%. Six optional query failures are documented limitations. `cleanup-status.tsv` confirms all four clones, transient unread folders and durable drivers are absent/inactive. No fifth round was launched.
