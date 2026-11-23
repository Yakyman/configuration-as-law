# Gentoo collector repair contract

The Portage adapter invokes the installed manager's Python API without executing ebuilds or installing tools. It expands `selected` through `getSetAtoms` and matches installed versions/slots through `vartree.dbapi.match`. A selected atom with exactly one installed match is explicit. Ambiguous matches and nonselected packages remain unknown. The manager's `--oneshot` option permits direct installation without adding a selected record, so neither absence from selected nor a present dependency graph establishes the installation reason.

Sources: https://raw.githubusercontent.com/gentoo/portage/master/lib/portage/_sets/files.py (`WorldSelectedSet`: “Set of packages and subsets that were directly installed by the user”); https://raw.githubusercontent.com/gentoo/portage/master/lib/portage/_sets/__init__.py (`getSetAtoms` recursively expands referenced sets); https://dev.gentoo.org/~zmedico/portage/doc/man/emerge.1.html (`--oneshot` prevents adding requested packages to world).

The helper is `collector/portage-reasons.py`; the controller sends its source through the normal bounded transport. Query `package-reasons-portage` is limited to 120 seconds. Every returned package identifier remains in the unread collector output until numerical reduction and deletion.

An initial implementation proposed assigning dependency from current mandatory dependency edges. Independent review identified the historical-reason ambiguity, but the correction was deployed after the first repaired collection. FX1 counts therefore cannot certify reason coverage. That inference was removed for FX2; unknown facts are retained rather than filling the readiness threshold.

Portage `dir` records now establish ownership without entering the packaged-file integrity denominator. `sym` records compare their installation target with the safe filesystem probe's captured link target: equal is unchanged, unequal or replaced object type is changed, and failed/absent link evidence stays unknown. Source: the native CONTENTS parser in https://raw.githubusercontent.com/gentoo/portage/master/lib/portage/dbapi/vartree.py . Synthetic verification (`portage-adapter-test.txt`) covers ownership-preserving directory exclusion and unchanged/changed/unreadable symlink targets.

Synthetic selected-set verification (`test-portage-reasons.py`, `portage-reasons-test.txt`) also covers a uniquely selected installed package, ambiguous parallel versions/slots, an unrecorded direct request, and a possible dependency. Only the unique selection is explicit; the others remain unknown.
