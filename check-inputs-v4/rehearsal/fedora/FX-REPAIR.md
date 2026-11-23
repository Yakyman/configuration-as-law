# Fedora instrument repair

2026-11-23 UTC. Final continuation status: NOT READY after all four fresh rounds (11–14). Reason coverage is 1679/2248 (74.69%), below the required strictly greater than 90%.

- The prior collector startup failure was repaired centrally: host laboratory
  root, static helper and transport separation are present in all continued runs.
- The prior Homebrew action returned 56 before any meaningful duration; prior
  stderr was unavailable, so its exact cause remains unknown. The same installer
  is now downloaded with bounded retries into a temporary output file, avoiding
  partial stdout concatenation, then run unattended and cleaned up. All 13 actions
  passed in each completed continued round. No workload program was replaced.
- File accounting now retains directory ownership outside the file denominator
  and verifies native symlink targets. Fedora's retained file integrity ratio
  exceeds 90 percent in each completed continued round.
- Install reason coverage remains below 90 percent. DNF group/external/absent and
  language records without own-manager provenance remain unknown; native parent
  reasons are not transferred. The records truthfully retain this failure.
- Source review found a Homebrew discovery blind spot. The independently
  reviewed `homebrew-discovery.patch` adds command-v discovery only and records
  an explicit unsupported-adapter gap. It infers no package, reason, file or
  integrity fact. Rounds 3 and 4 retains `collector:unsupported-brew-adapter=1`.

Evidence: `status.tsv`, `counts.tsv`, `query-limitations.tsv`, the per-round
source/staged checksums, `FX-NOTES.md`, `FX-DISCLOSURES.md`, and
`HOMEBREW-REVIEW.md`. Collected outputs remain unread and deleted. The final
Homebrew discovery revision was not retroactively rehearsed on earlier systems.

Review finding 2's historical Fedora mismatch is addressed by retaining every
continued round and selecting the latest final round for the lead's regenerated
READY/disclosure inputs. The original historical numeric records remain intact.
No claim is made here that aggregate input manifests have already been rebuilt.

Final round: all 13 actions and 20 transport calls passed; collector status 0, L2=6870, file integrity 164540/169962 (96.81%), total duration 297.981 seconds. Six optional query failures have named limitations. Cleanup is certified in `cleanup-status.tsv`. Remaining deficiencies are conservative unknown reasons and the explicit unsupported Homebrew adapter; neither is concealed by invented facts.
