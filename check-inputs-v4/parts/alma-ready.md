# AlmaLinux readiness

- Release: AlmaLinux 10.3, latest stable major/minor at 2026-11-23T01:19:00Z; release evidence in `C1/parts/alma-release.tsv` and `C1/raw/alma/sources.txt`.
- Image verified: yes. Pinned SHA256 matches; CHECKSUM signature verified against the official AlmaLinux 10 fingerprint. Evidence: `C1/raw/alma/verification.txt`, `CHECKSUM`, `signing-key.asc`.
- Clean installation boots: yes. Unattended default-environment installation powered off with exit status 0; disposable overlay boot and SSH login returned 0.
- `lab.sh run` works: yes. Script `exit 37` returned 37; root script `exit 0` returned 0. Only exit statuses retained.
- Time: installation 2026-11-23T05:51:21Z–05:57:03Z (5m42s); boot, login, transport, shutdown and deletion finished at 05:57:25Z (6m04s total from installer start). Image acquisition through cleanup took 9m45s (05:47:40Z–05:57:25Z, host image creation timestamp in attempts.txt); source research preceded this interval.
- Backing: host-relative `install/alma/base.qcow2`, mode 0444; registry `C1/base/alma.qcow2` and `C1/base/alma.json`.
- Failures: initial image download exited 92 near completion; HTTP/1.1 resume succeeded. An initial premature host launcher failed before boot; explicit service queue replaced it. No installation failure. See `C1/raw/alma/attempts.txt`.
- Cleanup: disposable VM stopped and destroyed, both statuses 0; extracted installer kernel/initramfs removed. Evidence: `C1/raw/alma/status.txt` and exact `C1/install/alma/finish.sh`.
- No packages, services, accounts, processes or files of the check machine were inspected. No check outcome was assessed. Readiness remains subject to independent review.
