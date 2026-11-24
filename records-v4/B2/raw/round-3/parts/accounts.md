# Account tool: source analysis and integration boundary

Recorded 2026-11-23 UTC. This is component analysis, not a machine observation or acceptance.
No guest probe was run for this component. No existing recipe source was changed.

## Exact case

The committed original command, run with effective UID 0, is:

```sh
/usr/sbin/useradd -M -u 1998 -s /usr/sbin/nologin v4raw
```

Source: (not published: direct evidence at least 2 MB), records
`root-native-account-bypass`, phases `expected` and `boundary_result`;
implementation: `B2/build/v4-tools-selftest.py`, lines 183–230.
The original result was exit 0, account tuple
`{"name":"v4raw","uid":1998,"gid":1998,"groups":["v4raw"],"shell":"/usr/sbin/nologin","home":"/home/v4raw","gecos":""}`,
no covering account row, unchanged declaration and successful application identity.
This is a built-in-tool bypass; it is not breaking.

The paired permitted action is the same native account change being written into
the declaration by the tool and applied. Refusal of native useradd alone does not
pass this case. A separately successful JSON frontend is not this permitted action.

## Existing integration

`B2/build/v4_tools.py` accepts only the typed frontend interface
`useradd add ROW.json`, which calls `stand.candidate_edit`.
`B2/build/stand.py` has the common locked candidate/application supervisor;
`run()` explicitly resolves account backends to `/usr/sbin/…`.
`activate()` invokes native groupadd, useradd and usermod when realizing rows.
`B2/build/install-v4-tools.py` intentionally leaves native paths available.
Consequently replacing only the frontend cannot close this case.

## Existing facilities considered before a probe

Primary implementation sources inspected on 2026-11-23 UTC:

- https://raw.githubusercontent.com/shadow-maint/shadow/master/src/useradd.c
  `run_parts` for `useradd-pre.d` precedes the duplicate-account lookup.
  `close_files()` commits the database updates before the `useradd-post.d` hook.
  Exact source comment: “This causes any modified entries to be written out.”
- https://raw.githubusercontent.com/shadow-maint/shadow/master/lib/commonio.c
  `commonio_close()` writes a temporary database, flushes and synchronizes it,
  then publishes it. Exact statement: `if (rename(tmpf, db->filename) != 0)`.

These upstream sources establish the facility design; they are not evidence of
the version installed in the final guest. No unverified version equivalence is
claimed.

Two integration approaches are rejected from their documented ordering, not
reported as executed failures:

1. A post-hook snapshots account state and adds rows afterward. The account already
   exists before the hook; this leaves an uncovered interval. It also derives the
   declaration from already active machine state. A final clean readback does not
   establish absence of the interval.
2. A pre-hook calls the existing broker to apply the desired account row. The native
   parent then checks whether the account exists, finds the newly applied account,
   and fails. The original native operation does not complete successfully. Merely
   suppressing its duplicate error would be a command-specific workaround.

Neither requires an experimental probe to discover the ordering. Neither is a
claim that two mechanisms have failed on the final machine.

## Concrete general mechanism for a different implementation

This is a mechanism proposal, not a definitions-only impossibility argument and
not an implemented closure:

1. Account tools retain their ordinary argument processing and root invocation.
   Their common account-database write API creates an explicit transaction object
   holding prospective passwd, shadow, group, gshadow and subordinate-ID changes.
   Pending entries are not published as live account databases.
2. Before the first live database publication, the common API passes the intended
   complete account/group/settings delta and its base-generation identity to the
   declaration supervisor. The supervisor builds designated primary declaration
   rows from that intended delta, rather than from active account state.
3. The supervisor validates the whole proposed declaration and applies it through
   the common account backend with transaction identity authenticated by a private
   descriptor. This identity separates realization from a new user request and
   prevents recursive submission. A plain environment flag is insufficient.
4. The account state, declaration generation and success identity share one
   publication boundary. A concrete design is a generation store containing both
   declaration and account databases, with all account readers resolving the same
   generation pointer, and a single atomic generation switch. Native NSS lookup,
   authentication and services must consume that generation consistently; merely
   replacing passwd and then group is not this design. Recovery selects the last
   committed generation before admitting ordinary execution.
5. Only after publication does the native tool return success. Deletion and
   modification use the same transaction API. Direct privileged file edits remain
   available as breaking, as the task requires.

The critical engineering work is shared database/NSS and transaction integration,
not an argv wrapper. The existing testbed uses separate live files and a separate
success report, so it does not currently implement this mechanism. A frozen shell
alone cannot prove continuous P1/P2 for root callers or independent account readers.

## Definition constraints and strongest objection

S8.1-2: “The computer is brought into conformity with this text, rather than the text being compiled from the computer.”

S8.1-11: “A service is in force if it is enabled; an account, if it exists.”

S8.3-7: “Its tools for installation and configuration record changes in the declaration even when they run with superuser privileges: an installer does not install a program past the declaration but adds it to the declaration.”

These require intended account state to drive realization; they do not prohibit
an account transaction API. The strongest objection to the proposed implementation
is incomplete mediation: a remaining tool, reader, cached NSS entry or direct
backend publication can expose inconsistent generation state. This is an
implementation obligation, not a deduction that every possible system fails.
The definitions alone therefore do not establish outcome 0 for this account case.

## Replay and required observations

On a fresh image copy, verify the name/group and UID 1998 are absent. Save the exact
current declaration and success report. Run the original command above as actual
root. Save exit status, stdout and stderr. Observe `getent passwd v4raw`,
`getent group v4raw`, the complete declaration, and its success identity. A pass
requires the command's successful change, exact account tuple and system-created
covering row in the successful declaration. Final-only observation cannot prove
transactional continuous consistency; any closure statement must state its scope.

The native cleanup in the original case is `/usr/sbin/userdel v4raw`, followed by
`/usr/sbin/groupdel v4raw` only if that group remains. A fresh-copy case can instead
retain evidence and discard the copy, avoiding cleanup being confused with the
permitted action. Do not replace the native attempted command with a broker command.

## Prospective filesystem integration draft

The integration direction subsequently selected by the builder uses a writable
filesystem that records prospective contents before exposure. A pure helper is
provided in `B2/build/bc3_account_rows.py`; no existing recipe file was changed by
this component. It accepts a complete caller-supplied prospective account database
snapshot and never reads live account state. `account_rows()` emits exact semantic
account/group rows and own-line database settings; `database_rows()` retains exact
database settings even if intentional privileged breaking makes semantic parsing
impossible. Those rows belong to the additional primary filesystem declaration,
not the finite `stand.py` JSON API. Credentials require restricted declaration
access. Numeric primary groups remain represented during native passwd-before-group
publication; no nonexistent group name is invented.

This helper alone does not close the case. Integration must supply the correct
prospective bytes for rename, writes, truncation, unlink and other mutations; replace
stale semantic rows; publish declaration and live state coherently; and persist the
same authoritative generation for reboot. Exact bytes of passwd/group are recorded
as settings with their own lines, not merely as an installed package's edited files.
No claim is made that file hashing alone supplies these account-setting lines.
Static Python syntax parsing completed successfully. No guest probe has been run.
