KIT2: 2 of 2 late systems ready

Preparation started 2026-11-23T07:16Z. Both systems passed by 07:58:08Z;
final cleanup was verified at 08:00:39Z, within the 90-minute limit.
Readiness is an instrument result, not a hypothesis outcome. The original
[KIT report](KIT-READY.md) remains the historical five-of-seven snapshot.

| System | Ready | Work and evidence | Recorded choice | Failure and limitation |
|---|---|---|---|---|
| GNU Guix System 1.5.0 | yes | Reused the byte-identical original clean installation, registered its read-only base and serial metadata, restored the preceding recipe's passive initial serial login. Fresh boot/login returned 0; `lab.sh run` returned user 37 and root 0. [Record](parts/guix-kit2.md), [statuses](raw/guix-kit2/status.txt), [registration and reuse](raw/guix-kit2/reuse-status.txt), [cleanup](raw/guix-kit2/cleanup-status.txt). | Original user/password serial access retained under the task's explicit fallback; no successful SSH reconfiguration or lab-key installation claimed. [Choice](CHOICES.md), [recipe](install/guix/KIT2.md). | Earlier SSH reconfiguration timed out (124), guest-side reason unknown because output was discarded; not repeated. A new host-only relative service path error was corrected before a VM started. Native stop returned 1; forced stop and destroy returned 0, disposable absent. Smoke elapsed 07:22:00–07:24:29 UTC. |
| openSUSE MicroOS Snapshot20261121 | yes | Verified the vendor's same-release plain KVM/XEN image and configured first boot with Combustion. Registered the read-only base with SSH user `user`, lab key, q35 and UEFI metadata. Fresh shared-runner clone boot/login returned 0; ordinary scripts returned 0 and 37, privileged script 37, destroy 0. [Record](parts/microos-kit2.md), [first boot](raw/microos-kit2/attempt-6-status.log), [runner statuses](raw/microos-kit2/attempt-6-runner-status.log), [registration](raw/microos-kit2/registered-base.txt), [cleanup](raw/microos-kit2/cleanup-status.log). | Authorized vendor VM-image fallback, documented Combustion user creation with mounted `/home`, and preparation NICs matching the shared runner. [Choice and documentation passages](CHOICES.md), [active recipe](install/microos/kit2/attempt-6/), [recipe guide](install/microos/kit2/README.md). | The earlier DVD timeout (124) was not repeated. Earlier first-boot recipes failed to establish login; `useradd` status 6 justified removing an unnecessary supplementary group. The documented home mount was added; standalone access then passed, but its first runner clone returned 1. Matching the runner's two NIC inputs produced the final passing base. Internal causes beyond the documented status meaning remain unknown. Detailed attempt history and the first attempt's missing terminal status are retained in the record. Final runner validation elapsed 07:58:06–07:58:08 UTC; all disposable disks, FIFOs and VMs were cleaned. |

The shared runner modification is limited to metadata-gated passive serial
startup. Local/deployed hashes match and shell/Python syntax checks passed:
[runner integration](raw/kit2/runner-integration.json). The access details and
Guix shutdown limitation are documented in [LAB.md](LAB.md).

Both late systems are ready; none remains unfinished. Independent acceptance is
recorded in [KIT2-REVIEW.md](KIT2-REVIEW.md).

Only installation, boot/login and predetermined script exit statuses are tested.
Guest and installer output is discarded. No check-system contents or hypothesis
properties are observed. Concrete inputs still require the downstream
pre-observation repository commitment described in the original task.
