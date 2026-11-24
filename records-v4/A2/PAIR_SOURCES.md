# Primary evidence for the pair sweep

Accessed 2026-11-23 UTC. Witnesses are documented real object types in the stated conditions, not observations of an inventory or claims of a conforming distribution. A conditional state (such as a separately downloaded file or an unavailable compatible interpreter) is stated in the object column, never silently inferred about a machine. Other source identifiers resolve in TERM_SOURCES.md and property_sources.md.

- PAIR1: https://packages.debian.org/bookworm/amd64/gawk/filelist
  Passage: `/usr/bin/gawk`; `/etc/profile.d/gawk.sh`; `/usr/share/awk/join.awk`.
- PAIR2: https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Menu.html
  Passage: “Download and install all packages marked with i, and their dependencies”. The same package-menu documentation supplies the deletion passage in TERM_SOURCES.md.
- PAIR3: https://www.gnu.org/software/coreutils/manual/coreutils.html
  Passage: “install copies files while setting their file mode bits and, if possible, their owner and group.”
- PAIR4: https://man.openbsd.org/sshd.8
  Passage: “AuthorizedKeysFile specifies the files containing public keys for public key authentication”.
- PAIR5: https://www.gnu.org/software/bash/manual/html_node/Bash-History-Builtins.html
  Passage: “fc re-executes command after replacing each instance of pat in the selected command with rep.”
- PAIR6: https://peps.python.org/pep-3147/
  Passage: “pyc files are not compatible across Python major releases.”
- PAIR7: https://specifications.freedesktop.org/desktop-entry/latest-single/
  Passage: “The Exec key must contain a command line.”
- PAIR8: https://www.gnu.org/software/gawk/manual/html_node/Join-Function.html
  Passage: “join.awk --- join an array into a string”. The full published function concatenates array entries and returns the resulting string; it contains no process-launch, file-writing or configuration operation.
- PAIR9: https://www.gnu.org/software/gawk/manual/html_node/Options.html
  Passage: “Disable the system() function, input redirections with getline, output redirections with print and printf, and dynamic extensions.” This documents the additional sandbox execution boundary; the pure join function also demonstrates that interpreter process rights and operations in the code are distinct facts.
- PAIR10: https://sssd.io/docs/quick-start.html
  Passage: “Now restart SSSD and test looking up a user.” The LDAP example configures `id_provider = ldap`; its source is set using `ldap_uri`.
