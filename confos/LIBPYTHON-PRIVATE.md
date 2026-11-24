# Shared CPython reader repair, 2026-11-24 UTC

Outcome: `?`. Released44's recorded embedding probe executes saved files through
the unmodified libpython3.13 package. This is an implementation failure, not an
impossibility proof (records/embedded-python-private).

The existing patched python executable is a static build. The separate Debian
shared library is selected by embedded programs and does not contain that repair.
Build the exact authenticated Debian3.13.5+security source with the same existing
file-descriptor checks and shared-library configuration; compare ABI and run the
same embedding probe against the candidate before any canonical integration.

References read before building:
- [CPython configure](https://docs.python.org/3.13/using/configure.html#cmdoption-enable-shared):
  --enable-shared builds the shared library, which is disabled by default.
- [CPython file execution API](https://docs.python.org/3.13/c-api/veryhigh.html#c.PyRun_SimpleFileExFlags):
  PyRun_SimpleFileExFlags reads and executes its FILE input. The existing probe
  uses that native API directly, not a typed expression that copies file bytes.

Recipe: build-libpython-private.sh. It builds only the shared-library target,
keeps source/configure/build output under interpreter-inputs/libpython-private,
and changes no release component. Source, patch, recipe, original/candidate
symbols, dynamic dependencies and guest tests must be retained before cleanup.
No compatibility or enforcement success is claimed from compilation alone.
