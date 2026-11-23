# Lived-in Debian server repair result

2026-11-23 UTC. **Ready on FX1 (round 11).** The original thirteen activities
are unchanged and all succeeded. No action replacement was required.

| Evidence | FX1 |
|---|---:|
| Transport calls | 20/20 status 0 |
| Actions | 13/13 status 0 |
| Collector status | 0 |
| Collector duration | 33.241 seconds |
| Whole-run duration | 147.739 seconds |
| Second-level rows | 1249 |
| Reason known / packages | 359 / 392 (91.58%) |
| Integrity known / packaged files | 23314 / 25166 (92.64%) |
| Filesystem and reduction complete | 1 / 1 |
| Destroy status | 0 |

Evidence: `status.tsv`, `counts.tsv`, `diagnostics/fx1/coverage.tsv`.
`CLEANUP.tsv` certifies the clone and unread-output directory are absent.
Deployed source and helper hashes are in `fx1-deployed.sha256`.

The earlier integrity denominator included directory records. The shared
collector now retains directory ownership while excluding directories from
packaged-file integrity accounting. The shared filesystem helper also treats
the scripted K3s default image/runtime stores as opaque image boundaries, as
COLLECT.md documents. This system needed no additional private source edit.

Missing OpenRC, NetworkManager and Podman commands, and unavailable selected
user-manager buses, remain explicit query limitations named in COLLECT.md.
Thirty-three Python package reasons remain unknown; no native-package reason
was substituted for a language-manager reason. The numeric readiness fraction
still exceeds nine tenths. Read diagnostics and their disclosures are listed
individually in `DISCLOSURES-FRAGMENT.md`; successful action stderr was not read.

There was no additional fresh round after readiness was established.
