# Development self-test plan

Recorded 2026-11-22T05:39Z UTC, before development property self-tests. Factory installation is still being debugged; integration-01.log is a failed installation (generated unit identifier), not a check observation or a property claim.

Sources consulted first: research/DESIGN-NOTE.md, research/FAPOLICYD.md and research/policy.md. These establish file-trust, fsync, unit/cgroup, readback and API primitives, but cannot answer whether this newly written composition implements them. Tests below ask those integration questions, once per listed question. Any failed installation or altered implementation retest must be labelled as development with its exact change, not silently replace evidence. No actual-check programs are selected or inspected.

| ID | Item | Development question and expected result | Command/script planned |
|---|---|---|---|
| D01 | 1,3 | Factory declaration has a row for its base, every captured account and enabled/running service/timer, sudo/login/password/port/boot; readback passes per row | stand-verify; stand-compare --snapshot |
| D02 | 2,3 | Add the builder's native greeting artifact, service and drop rule through the broker; exact bytes, enabled/active service and effective nft text match | selftest.py add |
| D03 | 2 | Invalid payload checksum refuses in preparation and leaves previous declaration/state unchanged | selftest.py invalid |
| D04 | 4 | Custom file-trust policy denies an undeclared copy of the development ELF and the direct dynamic-loader route; declared original runs | selftest.py admission |
| D05 | 4 | Provided management frontend refuses an unsupported mutation under ordinary uid and sudo; direct original backend remains a known architectural gap, not root breaking | selftest.py frontends |
| D06 | 5 | Removing development program/service/rule stops its managed cgroup, removes activation and rule, and denies former executable/copy; surviving base files remain | selftest.py remove |
| D07 | 2 | One development add, change and removal each survive a power cut immediately after stdout SUCCESS; boot verify matches reported declaration | powercut.py; three distinct development transitions, not the actual check's nine trials |
| D08 | 6 | Browser renders a local static page; ed changes a text document while file policy stays enabled | selftest.py work |
| D09 | 6 | Wi-Fi saved profile is accepted/read back by NetworkManager; Bluetooth local prepare path is written but pairing is not claimed without hardware | selftest.py radio |
| D10 | 7 | Same explicit declaration on two clean factory overlays produces identical per-line observations, with full file checksums/modes and service/account/rule fields | selftest.py reproducibility |

Known from documentation/source, no duplicate probes: Python and shell non-file code, custom dispatch, unrestricted systemctl/D-Bus/netlink root backends, global anonymous-memory/injection controls, general whole-state rollback, and unimplemented package channels remain open. No new experiment is needed to rediscover stock interpreter behavior already reported by B1. System-wide update and actual radios must be demonstrated or explicitly missing. No hypothesis outcome 0 is inferred from an implementation defect.

Amendment before formal self-tests, 2026-11-22 UTC: the fapolicyd integration did not converge and blocked management access (integration-03/04). Final bounded D04 expectation uses kernel noexec bind mounts on writable directories: direct ELF execution and the dynamic-loader route from the user's home should fail; interpreter reads are explicitly not covered. D08 checks stand-noexec remains active. D10 uses the deterministic `add` operation on two independent clean overlays and compares their saved snapshots. No whole-channel closure follows from these finite examples.
D08 also updates the same builder artifact to version 3 through the ordinary user's stand-pkg frontend and verifies it. This tests the frontend translation path; it is not a system/base update. D06 records the former managed service PID and tests its absence after removal.
