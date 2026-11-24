# SELinux module member groups

2026-11-23 UTC. Scope: the 441 input groups beneath the snapshot's `etc/selinux/targeted/active/modules/100/`. No earlier classification was consulted.

## Rule

Read each exact `members.file` completely. All 441 complete groups have exactly three persistent files: `cil`, `hll`, and `lang_ext`. For every one of the 1,323 files, the snapshot RPM manifest associates its exact path with `<REDACTED>`, and its complete SHA256 equals the package reference. Apply question 1 to every member: INSTALLED-PACKAGE. All members agree, so the group has that decision. This does not depend on deciding whether SELinux policy is code or setting values, because the first question has already answered yes.

The script `part-microos.selinux.rule.py` implements these predicates, appends missing rows with flushing, and verifies the subset IDs, counts, decisions and field word limits.

Exact deciding sentences:

- S8.2-6: What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.
- S8.2-7: Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?
- S8.2-8: Then it is **an installed object**, whether it contains programs or not: fonts, icons, translations, lookup tables, firmware, default setting values, a package containing only dependencies.
- S8.2-16: What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.

## Evidence

All paths below are relative to `D1b/handoff/microos/`.

- `members/<raw-id>.tsv`: all 441 lists read completely; all 1,323 members persistent.
- `s4-microos-snapshot-files.tsv`: exact path joins, all 1,323 comparisons equal, nonempty complete SHA256, manifest exit 0. Underlying manifest `raw/0062-s4-snapshot-rpm.out` comes from RPM queried with `--root /.snapshots/1/snapshot`, as its matching `.sh` confirms. Digest evidence is `raw/0067-package-digests-8000.out`.
- `s4-microos-snapshot-current.tsv`: all 1,323 exact snapshot paths also equal their current counterparts. This corroborates bytes; it is not substituted for package provenance or persistence.
- `s4-microos-sources.tsv`: every one of the 441 `lang_ext` source reads is successful and decodes to `pp`.
- `s4-microos-selinux-stores.tsv` and `raw/0157-s4-selinux-modules.out`: native successful module listing identifies all 441 names at priority 100 with format `pp`. The matching `.sh` selects the snapshot store explicitly.
- `objects.tsv` records `rpm:<REDACTED>` as dependency, with its reason provenance. That concerns recording the package; it does not change the coverage of its unchanged supplied members by that package's line.

The primary [semodule manual](https://raw.githubusercontent.com/SELinuxProject/selinux/master/policycoreutils/semodule/semodule.8) identifies semodule as the manager of policy modules. Its exact description of `--extract` is: “Extract a module from the store as an HLL or CIL file to the current directory.” The manual identifies `--list-modules` as the installed-module listing and explains the alternate store root. These establish the objects' function; RPM provenance decides their classification. No installation event is inferred from scriptlet source, modification time, or merely being in a module store.

## Ten hand checks

For each listed group, inspected all three member rows, their persistence, exact snapshot RPM association and equal digests, equal current comparisons, native module entry, and decoded `pp` format marker. Each has the identical three-member structure and unchanged package relationship required by the rule.

| ID | Module |
|---|---|
| d1b-microos-10ad322ddd5480af8a4acfcf | abrt |
| d1b-microos-1f0f8bfe337b17611ec151f5 | account-utils |
| d1b-microos-11d32a4f9a9e8cb6b66b6e82 | chrome |
| d1b-microos-1999f2fe39864a3414623d4c | fail2ban |
| d1b-microos-dde4e165d81bbb477f107045 | ipsec |
| d1b-microos-618d956842d35100ba22b451 | mcelog |
| d1b-microos-634bd6a3d36f23d37707724a | opensm |
| d1b-microos-2bd33ed4e926e1154b3ebec8 | rdisc |
| d1b-microos-6032d5e70393a32b728f5521 | slpd |
| d1b-microos-30b7ff007ddf6050b055b60e | zosremote |

Result: 441 INSTALLED-PACKAGE; no gaps in this subset.
