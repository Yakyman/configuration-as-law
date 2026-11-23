# Guix instrument access

The release and original clean installation are reused as explicitly requested.
The preserved base-system declaration is the exact prior input, not an inferred
inventory. Only access declarations are added in `C1/install/guix/config.scm`.

Primary documentation: GNU Guix manual, SSH Services and operating-system
reference, https://guix.gnu.org/manual/en/html_node/SSH-Services.html and
https://guix.gnu.org/manual/en/html_node/operating_002dsystem-Reference.html ;
saved source `C1/raw/guix/manual.texi`.

- OpenSSH `authorized-keys` has an empty-list default: “This is the list of authorized keys.” The declared file-like public key authorizes the lab user.
- `sudoers-file`: “The contents of the /etc/sudoers file as a file-like object”. The declaration supplies a passwordless wheel rule for the instrument.

These are explicit instrument-access changes, not claims that the installer has
no default. Initial serial access exists in the previous recipe; it is used
only to apply the known declaration. The intended final instrument uses SSH; its preparation did not complete.

Host-only declaration review: the tagged 1.5.0 `(gnu)` composite module includes
`(guix gexp)` in its publicly re-exported module interfaces. Thus the existing
`(use-modules (gnu))` import supplies `plain-file`; no additional import is
required. Evidence: `C1/raw/guix/gnu-module-excerpt.scm`, source
https://git.savannah.gnu.org/cgit/guix.git/plain/gnu.scm?h=v1.5.0 .

Recovery-only inputs are recorded in `install/guix/README.md`: a Debian helper,
the known original partition target, temporary helper CA certificates, and the
official `https://ci.guix.gnu.org` substitute source. These do not replace the
original installed-system declaration. All failed recovery candidates were
removed after the final timeout; no SSH-enabled Guix base is registered.
