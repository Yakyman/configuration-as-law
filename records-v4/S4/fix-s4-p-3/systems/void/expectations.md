# Prior sources and expectations

2026-11-23 UTC. Written before the targeted queries. Rehearsal only.

- https://docs.voidlinux.org/config/services/logging.html: “The default installation comes with no syslog daemon.” This is a default, not proof that retained logs are absent on this installation.
- https://man.voidlinux.org/useradd.8: “The name of the user's login shell.” The shell option describes operation, not this machine's executed choice. Its description says command-line and system defaults supply account values; it does not identify this installation's inputs.
- https://man.voidlinux.org/xbps-install.1: “Default trusted keys directory.” This labels `/var/db/xbps/keys`. The environment section specifies CA certificate file/path overrides, so an installed default cannot establish all actual consumers.
- https://docs.openssl.org/3.0/man3/SSL_CTX_load_verify_locations/ documents trust-location loading. A process can read and close a certificate; a present library or empty descriptor snapshot cannot establish complete prior use.

Missing targets: V03 account shell, nine supplementary group memberships, two sudo-rule records; V07 default configuration, module configuration, sudo configuration, mount directory and XBPS trust-key creator; V09 `/etc/ssl/certs` trust-value choices and actual use. Original object counts are dependency counts only.

Expected route 01: targeted retained audit/syslog/installation event searches may find no events establishing all V03/V07/V09 targets. An absent event is unknown, not proof of no change.
Expected route 02: shell histories may be absent or omit target commands; timestamps/command text alone may not establish execution or completeness. Separate route from logging.
Expected route 03: installer artifacts, account backups and package installation scripts may provide source/defaults without evidence of who actually selected or executed them. This attempts V03/V07 by a source and installation-record route, separate from event logs and shell histories.
Expected route 04: current process descriptors and mapped files may show actual current readers of certificate paths. Even a positive result cannot establish all past consumers or trust choices. This is a targeted current-use route for V09.
Expected route 05: current process environments/arguments and CA policy files may reveal active overrides or configured references, but do not establish all actual use or choice events. This provides a third distinct V09 route beyond event logs and live open files (and a fourth beyond histories).

All routes are read-only, bounded, and run once after unchanged ordinary actions on a fresh disposable clone. They emit diagnostic counts only; no per-object inventory is retained or used for a decision. No experiment induces a new certificate use and misrepresents it as an earlier use. A command exit 0 means the diagnostic query completed, not that the complete missing fact was obtained.
