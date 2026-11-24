# Evidence for the final boundary checks

Accessed 2026-11-23 UTC. These support rejected candidates or boundary examinations, not a report of experiments.

- CAP: https://man7.org/linux/man-pages/man7/capabilities.7.html
  Passage: “units, known as capabilities, which can be independently enabled and disabled.” Under CAP_DAC_OVERRIDE: “Bypass file read, write, and execute permission checks.” The preceding definition connects these units to privileges traditionally associated with superuser.
- SUDO: https://www.sudo.ws/docs/man/1.9.14/sudoers.man.pdf
  Passage: “the default file mode is 0440 (readable by owner and group, writable by none).” This makes the capability-dependent direct append case concrete; file ownership alone supplies no write bit.
- PODMAN: https://docs.podman.io/en/stable/markdown/podman-create.1.html
  Passage: “Creates a writable container layer over the specified image”. The user-namespace and capability sections describe rootless mappings and namespace capabilities; rootless status does not mean that namespace-governed file writes use no privilege.
- PLSOURCE: https://www.postgresql.org/docs/18/catalog-pg-proc.html
  Passage: “For all other currently-known language types, prosrc contains the function's source text.” The catalog separately stores names, ownership and other metadata.
- PLPOWER: https://www.postgresql.org/docs/18/plpython.html
  Passage: “it will be able to do anything that could be done by a user logged in as the database administrator.” This supports considering non-exempt stored code, not merely restricted SQLite triggers.
- NFSROOT: https://docs.kernel.org/admin-guide/nfs/nfsroot.html
  Passage: “Name of the directory on the server to mount as root.” This is the documented root-dir parameter of a diskless client's NFS root filesystem.
