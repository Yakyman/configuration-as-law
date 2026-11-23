# Round 1 mechanism sources and integration questions

Recorded 2026-11-22 UTC, before guest tests. These are builder regression tests of a changed integration, not repeated hypothesis observations. Documentation answers the primitive semantics; tests below check that the recipe actually installs the intended policy.

- D-Bus policy: https://dbus.freedesktop.org/doc/dbus-daemon.1.html — “The last rule that matches the message determines whether it may be sent.” User-specific denial and root allow rules are installed for the supplied ordinary account; polkit additionally denies non-root administrative actions. Tests must return AccessDenied, not merely UnknownObject or missing hardware.
- systemd unit paths: https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html — “Unit files are loaded from a set of paths determined during compilation”. User managers are masked and their executable unreadable to callers; writable user search paths are therefore not honoured. Declared jobs use protected system units with explicit User=stand.
- systemd manager authorization: https://www.freedesktop.org/software/systemd/man/latest/org.freedesktop.systemd1.html — “PID 1 uses polkit to allow access to privileged operations for unprivileged processes.” Direct bus methods and transient-unit methods are included in the denial checks.
- sudo command/environment policy: https://www.sudo.ws/docs/man/1.9.14/sudoers.man.pdf — “If set, sudo will use this value in place of the user's PATH environment variable.” The allowlist grants only declaration dispatchers; Python isolated mode and a fixed subprocess environment prevent caller Python/module/bus variables from granting backend authority.
- nftables authorization: https://man7.org/linux/man-pages/man7/capabilities.7.html — CAP_NET_ADMIN includes “administration of IP firewall, masquerading, and accounting”. Native netlink and library tests run without this capability, and sudo cannot grant a generic client.

No documentation establishes this assembled testbed's end-to-end closure. Raw tests record implementation failures separately; a failure is not a definition-only impossibility argument.
