# Native version resolution diagnostic, 2026-11-24 UTC

On released46, `package libreoffice-writer 4:25.2.3-2+deb13u9` failed assembly
against the committed T2 archives, which also contain u12. The package still
exists. Original output: records/lo-macro-private-build-failure.

Native simulation with all base component versions fixed:
- Default solver: exit100.
- Solver3 with strict pinning: exit100.
- Solver3 with `--no-strict-pinning`: exit0,276 packages, every explicit package
  and version preserved. Commands: records/lo-solver-private.

References read before the native comparison:
- Worker /usr/share/doc/apt/examples/configure-index exposes
  apt::solver::strict-pinning and apt::solver.
- [APT solver author](https://blog.jak-linux.org/2024/05/14/solver3/):
  disabling strict pinning permits other available dependency versions when
  satisfying an explicitly requested package release.

Candidate policy: preserve default successful resolutions. If that native
simulation fails, retry through the native all-version solver, using the same
explicit version arguments. Assert every explicit request is selected exactly,
and use the same solver for download. Do not alter the declaration, loosen its
versions, change snapshot sources or add a strict dependency-line requirement.
The guest install/document/removal test is required before publishing the repair.
