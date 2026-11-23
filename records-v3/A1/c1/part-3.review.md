# Review of part 3 core subset

Scope: 124 rows covering accounts, the build-account group, loaded kernel modules, and processes. The review checked the rows and their generating script and notes against the input inventory, saved raw evidence, and the exact rules in Sections 2.2 and 3.

## Findings

1. **Resolved: evidence citation for `nixos-344126e1ba`.** The row now cites `../in/raw/nixos/process-executables.tsv`, which resolves PID 303 to `udevadm` and supports the claimed executable identity.

2. **Resolved: evidence citation for `nixos-791fcf298c`.** The row now cites `../in/raw/nixos/process-executables.tsv`, which resolves PID 785 to `systemd-executor` and supports the claimed executable identity.

3. **Resolved: function claim for `nixos-89ce5c5668`.** The row now makes the narrower claim that the observed kernel threads execute kernel code. This matches the process evidence and the S2.2-10 reasoning without assigning an unverified function to every member.

## Checks that passed

- All 124 scoped IDs occur once and correspond to the intended input kinds.
- Every decision uses an allowed output value and cites only S2.2 or the Section 3 recording indicator.
- `what_it_does` and `reason` satisfy the stated word limits.
- The notes contain ten manually checked IDs for each multi-row account, module, and native-process rule. The single grouped build-account row and the single kernel-thread row are handled individually.
- The account and loaded-module decisions have evidence adequate for their stated homogeneous rules. The native-process MUST rule follows directly from observed execution and S2.2-9/S2.2-12; the corrected executable citations support the two resolved identities.

Core review result after correction: **accepted**; no classification decision was modified by review.

# Review of part 3 unit subset

Scope: 150 rows covering singular and grouped system and user units. The review checked the unit result and notes against the input inventory, saved unit listings and path evidence, and the exact rules in Sections 2.2 and 3.

## Findings

1. **Resolved: `nixos-9994d7ebc4`.** The row now uses UNKNOWN with S3-1 and S3-2 and states that the omitted dependency relationships prevent establishing the retained references' operational effects.

2. **Resolved: `nixos-97fdaec6aa`.** The row now uses UNKNOWN with S3-1 and S3-2 for the same unestablished reference relationships and effects.

## Checks that passed

- The subset contains exactly 150 distinct IDs matching the four intended unit kinds.
- All `what_it_does` and `reason` fields satisfy the word limits, and all sentence citations stay within S2.2 and the Section 3 recording indicator.
- The 148 MUST decisions follow the documented operational semantics of loaded services, sockets, mounts, targets, slices, timers, paths, scopes, and device units, with relevant raw state cited.
- The notes supply ten manually checked IDs for the 139-row homogeneous singular-unit rule and separately reason through every grouped row.

Unit review result after correction: **accepted**; no classification decision was modified by review.

# Review of part 3 stored-object subset

Scope: 97 rows covering stored paths, two store groups, and the directory-only remainder. The review checked each result and its notes against the input inventory, saved raw evidence, cited documentation, and the exact rules in Sections 2.2 and 3.

## Findings

No unresolved findings remain after correction. `nixos-2527479582` now preserves factual uncertainty instead of applying the one-program exemption. `nixos-57da4d32dc` now has a complete twelve-member MIXED partition with catalog documentation and explicit UNKNOWN empty directories. `nixos-bfd49e603a`, `nixos-76634f69cd`, `nixos-0075a76d48`, and `nixos-b86fee9a16` now use exhaustive disjoint MIXED partitions rather than blanket UNKNOWN.

## Text-grounded checks

- `nixos-049151ab36` is a genuine HOLE on the fixed text. S2.2-4 expressly lists database contents among exempt content, while the documented store metadata is operational and removal disables store operations under S2.2-1 and S2.2-2. The text applies both outcomes and does not delimit operational database contents from exempt database contents.
- The two update-marker HOLE decisions similarly identify direct dual applicability: the objects are records of completed past updates under S2.2-6, while their timestamps control future conditions under S2.2-1.
- UNKNOWN is appropriate for individual members whose contents, targets, or consumers are missing; heterogeneous groups still require a MIXED partition when another member's decision is known.

## Structural checks that passed

- The subset contains exactly 97 distinct IDs matching the intended stored-object kinds.
- Every decision and basis uses the allowed vocabulary, every sentence citation stays within S2.2 or the Section 3 recording indicator, and all limited text fields satisfy their word limits.
- The subset is classified by explicit per-ID decisions rather than a scripted homogeneous rule, so the ten-manual-ID requirement does not apply.

Stored-object review result after correction: **accepted**; no classification decision was modified by review.

# Review of part 3 system-closure store subset

Scope: 618 rows covering individual store objects in the current system closure. The review checked the result and notes against the input inventory, saved raw evidence, cited primary documentation, and the exact rules in Sections 2.2 and 3.

## Finding

No unresolved findings remain after correction. For `nixos-7d271b79b7`, the notes now cite primary documentation that explicitly calls `/etc/services` a “services database file” and `/etc/protocols` a “protocol database file,” and documents the lookup functions that consume them. Combined with the package source tying those files to the classified object, this establishes both sides of the HOLE reasoning.

## Checks that passed

- The subset contains exactly 618 distinct IDs matching the intended input kind; decisions, citations, basis values, field shape, and word limits conform to the required schema.
- Each of the nine scripted homogeneous rules has ten manually inspected IDs in the notes, with rule-specific identity and function checks.
- The executable, library, unit-definition, unit-script, privilege-wrapper, PAM-policy, restart-trigger, and distinct documentation-output rules follow the cited functions and the literal S2.2 rules.
- UNKNOWN is used where only a store pathname is known and documentation cannot establish the generated artifact's actual contents or role.
- `nixos-531f170216`, `nixos-bb87ebc68c`, and `nixos-bfbcc6b6ea` are text-grounded HOLE cases: their cited sources explicitly call the objects databases, while their runtime values also determine behavior under S2.2-1 and S2.2-2.

Store-subset review result after correction: **accepted**; no classification decision was modified by review.
