# Void kit readiness

System: void (20250202 x86_64 glibc base).
Image verified: yes (SHA256 and minisign, both exit 0).
Clean installation boots: yes (shared runner new/start exit 0).
Lab run works: yes (ordinary and root scripts returned their requested status 37).
Elapsed: approximately 9 minutes, 2026-11-23T05:47Z–05:56Z.
Backing: `void/clean-fixed.qcow2`, read-only; registered as `C1/base/void.qcow2`.

The original live medium's void-installer performed a Local installation. Only instrument access was added. A root smoke failure (exit 1) was corrected by sorting the dedicated NOPASSWD sudoers rule after the installer-provided wheel rule. The corrected recipe uses `zz-lab` from the start. No diagnostic text, inventory, or machine contents were retrieved. See `C1/raw/void/timeline.log`, `C1/install/void/`, and `C1/parts/void-choices.md`.

Post-review recipe correction (2026-11-23 UTC): the reusable launcher now tries
all twelve shared locks before reporting no free slot. The successful recorded
installation held slot 5 throughout; it was not rerun. The verification key is
now pinned to its pre-cutoff upstream revision, and the pinned bytes match the
originally verified key; see `raw/void/key-provenance.txt`.
