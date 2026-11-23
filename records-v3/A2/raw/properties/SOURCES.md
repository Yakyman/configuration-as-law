# Primary-source extracts for the property and indicator sweep

Retrieved: 2026-11-22 04:39:07 UTC.
These are bounded extracts and factual paraphrases, not machine observations.

## E1: An editor with package-management functions

URL: https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Installation.html
Exact passage: “This prompts for the name of a package with the ‘available’ status, then downloads and installs it.”
Context: the preceding sentence identifies the command as `M-x package-install`; the same page documents package upgrade, dependency installation and activation in later editor sessions. Access through indexed primary-source content succeeded; direct page opens timed out.

## E2: Boot-order configuration

URL: https://github.com/rhboot/efibootmgr
Exact passage: “Explicitly set BootOrder (hex).”
Context: the option is `-o | --bootorder XXXX,YYYY,ZZZZ,...`; this changes an ordered firmware boot selection, without installing content or creating an account or service.

## E3: Multi-purpose executable

URL: https://busybox.net/about.html
Exact passage: “BusyBox combines tiny versions of many common UNIX utilities into a single small executable.”
URL: https://busybox.net/downloads/BusyBox.html
Exact passage: “Add a user”
Context: this is the `adduser` command description. The same documented executable includes `cp`, `sh`, `vi`, `ip` and other applets. This is supporting breadth, not a separate gap.

## E4: Saved-network representation

URL: https://networkmanager.dev/docs/api/latest/nm-settings-keyfile.html
Exact passage: “NetworkManager is based on the concept of connection profiles that contain network configuration”
Context: profiles contain separate connection, wireless and IP configuration sections and can be saved in keyfiles. This is supporting breadth for the missing unambiguity branches.

## E5: Service state

URL: https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
Exact passage: “Check whether any of the specified units are active (i.e. running).”
Context: `is-active` tests activity, while the separate `is-enabled` interface tests enablement. The documentation distinguishes runtime activity and enablement. This supports scrutiny of service removal and state; it does not establish an unavoidable failure.
