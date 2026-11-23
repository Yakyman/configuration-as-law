Gentoo: ready

Image verified: yes. Clean installation boots: yes. lab.sh run: yes.
Time: 59 minutes 44 seconds (2026-11-23T05:46:56Z–2026-11-23T06:46:40Z).

The plain amd64 OpenRC stage3 image and signed DIGESTS verified; the fixed source snapshot also verified. The source-only installation completed, final repository pin/update returned 0, and the powered-off backing image is read-only at `install/gentoo.qcow2`. A fresh clone booted and logged in; user and root scripts each returned their requested status 37. The corrected instrument stop and destroy each returned 0. Disposable clones, bootstrap and duplicate target disks were removed; verified images, exact recipes and the immutable clean base remain.

Failures and corrections: see `C1/raw/gentoo/installer-statuses.tsv`. The initial generic chroot failure was not diagnosed through guest output; adding the documented dracut configuration preceded successful source installation. Finalization needed explicit creation of the instrument sudoers directory. QMP ACPI shutdown timed out; the lab instrument now invokes root SSH poweroff and its fresh retry passed. These are laboratory preparation outcomes, not outcomes of the checks.

Evidence: `C1/raw/gentoo/verification.txt`, `C1/raw/gentoo/digests-signature.txt`, `C1/raw/gentoo/portage-verification.txt`, `C1/raw/gentoo/source-and-pin-exit-statuses.txt`, `C1/raw/gentoo/installer-statuses.tsv`, `C1/raw/gentoo/stop-retry-status.txt`, `C1/raw/gentoo/cleanup-status.txt`. No guest inventory or property assessment was performed. Independent review is separate.
