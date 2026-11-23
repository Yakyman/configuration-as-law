# Guix readiness

- Ready: no.
- Image verified: yes. Stable release 1.5.0 matches the preceding laboratory; its verified ISO, signature and original clean installation were copied. The original backing remains read-only.
- Clean installation boots: yes. The copied original logged in successfully through its existing serial instrument on two disposable copies (status 0). This does not establish successful boot of the later SSH-enabled candidates.
- Final `lab.sh run` works: no. Instrument access could not be completed within the bounded preparation attempts; no successful final SSH script run is claimed.
- Time spent: 2026-11-23T05:58:41Z–07:11:15Z, 1 hour 12 minutes 34 seconds including cleanup. Preparation paused at 06:54:28Z after 55 minutes 47 seconds, then returned at 06:55:20Z after the other systems reached their final phase. The final 900-second application ended with timeout status 124 at 07:10:34Z.

Two serial access applications returned status 1 with output discarded; two subsequent serial logins failed before applying the declaration. Offline mount and execution input repairs followed the exact prior partition recipe and official chroot manual. Static review found that generated profile sourcing was unsafe with nounset enabled. The corrected operation disables nounset while sourcing that profile. Its initial 300-second and final 900-second application attempts both returned timeout status 124. The runtime reason for noncompletion is unknown: no guest output, inventory or property observations were retained. No final SSH smoke test followed the incomplete application.

Cleanup completed with status 0. All failed candidate and helper disks were removed; the failed Guix base registry is absent, and no disposable Guix smoke VM remains. The original verified read-only installation, ISO/signature/key, exact recipes and exit-status records are retained. Records: `C1/raw/guix/attempts.md`, `recovery-attempt7.txt`, `final-cleanup.txt`, and the earlier individual status files. No assessment of Guix against the check properties was performed.
