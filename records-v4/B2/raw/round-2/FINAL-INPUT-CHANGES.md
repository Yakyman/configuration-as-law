# Final input changes from development

Recorded 2026-11-23 UTC before final machine observations. Development's frozen
source and raw outputs are preserved. These changes are included in the required
final rebuild and whole-suite validation, not reruns of the development phase.

- Native package-member receipt is unknown without original delivery evidence;
  matching consumes a single census snapshot. See RECEIPT-CORRECTION.md.
- S8.2-14 personal values that neither launch nor grant access classify as a
  program record even when entered by a person. Two pure fixtures were added.
- The received default file now has an actual recorded consumer: the source
  and its produced bytecode read `language=en` as a value and print it. The
  expected output fixes both the execution marker and the read default.
- The unsupported-algorithm diagnostic is printed on stdout by the transaction
  layer. The final detector inspects both stdout and stderr. Development's failed
  detector is retained; no runtime retry is used to relabel its raw assertion.
- Development's alternate-root native install lacked its root directory and
  failed with `error creating directory '.': No such file or directory`.
  Its no-bypass Boolean is not a policy refusal. The final fixture creates the
  destination before invoking the installer and reports the concrete package
  database state, content and declaration/report identity.
- Three independent validation branches run concurrently after both scratch
  recipes. All existing cases and child drivers remain unchanged. Their outputs
  join only after all branches finish. The final controller's cleanup is the
  authoritative whole-run cleanup record; a child may observe another branch's
  live guest. The complete example includes the six exact new object/unit rows
  exported from the target interpreter and is replayed on both independent builds.
