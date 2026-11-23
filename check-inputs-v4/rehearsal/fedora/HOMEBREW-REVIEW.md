# Homebrew discovery source review

2026-11-23 UTC. Independent source review: ACCEPTED.

Discovery uses only shell `command -v`, checks the documented Linux prefix,
per-user candidate prefixes and scanned `/bin/brew` parent directories, and
never executes Homebrew or formula code. A detected command adds only the
explicit unsupported-adapter/ownership-incomplete gap; it creates no package,
reason, manifest or integrity fact. Documentation states bounded discovery and
non-inference. The reviewed patch is `homebrew-discovery.patch`.

This accepts the source repair for deployment in continued round 3; it does not
accept Fedora readiness or infer any result from the unrehearsed revision.
