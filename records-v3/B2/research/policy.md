# Declaration-derived file access policy

Implementation: `../build/policy.py`. Validation to date: Python AST parsing only.
No daemon was installed or run during this component task. Integration and
acceptance remain the builder's and independent reviewer's work.

## Interfaces and bootstrap

`install_policy()` replaces the prototype's complete ruleset and sets
`permissive=0`, `trust=file`, `integrity=sha256`, and explicit filesystem watching.
It removes alternate trust fragments and legacy rules which might shadow the
owned compiled rules. It checks configuration syntax but does not start or reload
the daemon, and returns `active_policy_acknowledged=False`.

`stage_trust(rows, declaration_dir)` reads `base`, `program`, and `code` rows,
accepting `type` or `kind` for the row discriminator. Each row uses either inline
`files` or `files_manifest`, a JSON list in a file inside the declaration directory.
Regular files require path, SHA256, mode, uid, gid; symlink records contribute no
trust. Each regular file is opened with O_NOFOLLOW, hashed, and checked for
permissions, ownership and concurrent metadata changes. Duplicates must agree.
Trust paths currently reject whitespace, percent signs and lengths above 500
bytes. This is an explicit prototype limitation, not a claim about the hypothesis.

The bootstrap sequence is `install_policy`, `stage_trust`, daemon startup, then
`refresh_trust`. The base manifest must include the broker and this module. Stage
alone is never evidence of enforcement. The caller must serialize applications
and prevent concurrent filesystem mutation; this helper supplies no global lock.

`refresh_trust(rows, declaration_dir)` requires an active daemon, stages the trust
file, requests update, then waits for exact database path/size/hash equality. It
checks trust consistency and active service status again. Failure, service death,
or timeout raises an exception. Its returned evidence explicitly includes
`reload_acknowledged=False`; callers must preserve this limitation in reports.

## Policy scope and unresolved limits

Trusted files may execute; all other execution is denied. Opens of untrusted ELF,
shared libraries, recognized shell/Python source and Python bytecode are denied.
Other opens are allowed for ordinary data work. No broad trusted-shell allow rule
exists. Rules do not distinguish root, so built-in tools through sudo face the same
rules. There is no promise to resist deliberate privileged destruction of policy.

Recognized script files are denied even when an editor wants to read them as data.
Conversely, code encoded in ordinary text, interpreter arguments/stdin, generated
memory, alternate MIME types, or unobserved filesystems is not comprehensively
controlled by these rules. Browser script execution is not closed by this module.
JSON passed to the broker on stdin is not classified as a source file.

There is an additional integration obstacle: denying untrusted source/ELF opens
can also deny the broker's own reads while hashing newly materialized files.
The module adds no broad root or interpreter exception to hide this issue. The
builder must test the declared installation path and report failure if this
prevents application. A unique trusted native broker or another general mechanism
would require separate implementation and validation; none is claimed here.

The update API does not acknowledge cache invalidation. Polling the persisted
database proves its contents, not that every concurrent permission decision has
crossed a reload boundary. This component therefore does not establish the
synchronous enforcement boundary required for success-report and removal claims.
No sleep duration or check-trustdb success is presented as proof of that boundary.

## Primary sources

- The upstream [CLI manual](https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd-cli.8)
  describes update as: “Notifies fapolicyd to perform an update of the trust database.”
  It separately describes consistency checking and dumping persisted entries.
- The [versioned CLI source](https://github.com/linux-application-whitelisting/fapolicyd/blob/v1.3.3/src/cli/fapolicyd-cli.c)
  shows `do_reload` writing the request FIFO and returning without waiting for
  completion; `do_dump_db` opens LMDB read-only and prints source/path/size/hash.
  This supports the limited synchronization claim and the dump parser.
- The [trust-file manual](https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.trust.5)
  states: “Each non-comment line contains a full path, size in bytes, and a valid SHA256 hash.”
  The implementation uses version 2 with restricted paths for compatibility.
- The [rules manual](https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.rules.5)
  states: “They are evaluated from top to bottom with the first rule to match”.
  It defines execute/open permissions, object trust, and magic-based MIME types.
- The [configuration manual](https://github.com/linux-application-whitelisting/fapolicyd/blob/main/doc/fapolicyd.conf.5)
  documents the file trust backend, SHA256 integrity, and watched filesystem
  configuration. Target-version configuration parsing is required in the guest.
