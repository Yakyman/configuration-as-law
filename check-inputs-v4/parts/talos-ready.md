# Talos readiness

Image verified: yes. ISO/client SHA256 and Sigstore bundles verify; installed factory payload is pinned to a verified signed digest. See `raw/talos/verification.log`, `container-signature.log`, and `installer-digest.txt`.

Clean installation boots: yes. The second installation used a fresh blank disk. Disk-only API login, bootstrap, shutdown and read-only base registration succeeded. See `raw/talos/install-status.json`.

`lab.sh run` works: yes. A disposable clone booted, authenticated with the generated certificate, returned requested exit 37, shut down and was destroyed (all expected statuses). See `raw/talos/smoke.json`.

Time: first installation attempt began 05:59:38 UTC; final smoke/cleanup completed 06:14:19 UTC (14m41s across attempts). The successful digest-pinned attempt ran 06:09:01–06:13:19 UTC (4m18s), followed by the clone test. Earlier image verification is recorded separately.

Failures: the first attempt used the generated version tag and had no automatic reboot. It was stopped without acceptance. The replacement pins the verified payload digest and explicitly performs a graceful shutdown followed by a disk-only boot. One initial disk-login attempt returned 1 before the successful readiness retry. No installer or guest diagnostic output was retained. Exact first-attempt inputs remain under `install/talos/attempt1/`.

Backing: `install/talos/base.qcow2`, mode 0444. Talos uses its API certificate instead of an SSH key because it has no shell. No inventory or property assessment was performed.

After a host interpreter-handling correction, a Python-shebang script also authenticated with discarded API output and returned 37; its clone stopped and was destroyed at 06:35:26 UTC. This additional runner validation is recorded in `raw/talos/interpreter-smoke.json`; it changes no backing-machine content.
