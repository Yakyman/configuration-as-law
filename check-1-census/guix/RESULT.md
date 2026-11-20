# Check 1 — Guix System VM: comparison and outcome

Date: 2026-11-19. An independent definition audit was done as a separate step; independent verification was recorded in a separate working file (`REVIEW-V3.md`); the independent review included here is [REVIEW.md](REVIEW.md). No VM was started or modified for this comparison. All V3 writes are under W/.

**Guix: 0. Overall for the supplied W inputs: 0.** The sole VM in both input tables is `guix`; NixOS below is an evidence appendix from the earlier V census, not another paired sample in this calculation. No V outcome is imported.

## Fixed failure condition and application

The frozen [PAPER.html §9.2](../../first-paper/PAPER.html) says exactly:

> An object is found on either machine that, under the definitions, belongs to no class or belongs to two classes with different consequences, or the two classifications assign the object to different classes and the text of the definitions does not resolve the disagreement.

The wording “either machine” is retained; this census covers one Guix VM. No agreement threshold, new classification rule or change to the condition is used. §9.1 and the shared rules of the checks distinguish definition counterexamples from stand defects. A failed collector, missing provenance or heterogeneous directory group is not by itself a no-class object.

The concrete two-class case is the **persistent imperative package selection**, `guix-6633666c2c`: `/gnu/store/hmlgnj2qflvif6vvd60n4x9lblkcybsp-profile`, including its manifest. `guix-e495746cb2` is the generation-selector family for the same selection. Both original classifiers mark both rows `hole-two`. The [user-day log](raw/guix/day/user-day.log) records ordinary-user `guix install hello`, successful execution, and unchanged `/etc/config.scm` and `home.scm` hashes. The [generated manifest](raw/guix/configuration/home/guest/.guix-profile/manifest) persists `hello 2.12.2`; [profile links](raw/guix/guix-profiles.tsv) connect the selector to that output. This is one selection mechanism observed in two rows, not two independent replications.

The competing readings come directly from §5.1:

> Derivative—an object that a described program has created itself because the object is needed for the program's operation: saved Wi-Fi networks for a network management service, extensions for a browser, a cache, a log.

> Data—what a person has created: photographs, documents, databases, and their own settings files, such as a text editor configuration.

Guix generated operational profile state while persisting the person's package setting. The text does not distinguish program-mediated creation of personal settings from program-created operational state or prioritize either reading (O1/O2). The consequences differ: P6 states, “If the program is absent from the current generation, its derivative is moved to an archive.” It imposes no equivalent program-removal condition on data. **Not resolved:** this is the §9.2 two-classes-with-different-consequences case. It does not depend on a collector malfunction, on counting aliases again, or on proving that all 32 flagged rows are definition counterexamples. This interpretation is explicit and reviewable in the [definition audit](definition-audit.md).

Additional unresolved differences include whether declared skeleton bytes copied into home directories are themselves recorded, and whether internal threads/services are the recorded program or its derivatives. §5 supplies no explicit propagation or granularity rule. These are retained as recording-scope disagreements; no such rule is added to force agreement. Imperative hello is **not** proved classless merely because P4 forbids its installation path: §5 still defines an unrecorded change as a bypass. This census is not an implementation test of Guix compliance with P4.

## Counts and agreement

All 178 IDs occur exactly once in each classifier and in the residual inventory. Classes below are the original decisions, before adjudication. Format normalization is explicit: `recorded (works)` → `recorded`; `derivative of X` → `derivative`, retaining X as owner. `hole-none` and `hole-two` remain distinct response categories and count as matching decisions when both classifiers use the same label; matching holes do not mean successful classification. Literal and exact-owner diagnostics preserve the original differences.

For paired rows, pₒ = matches/n, pₑ = Σₖ n(A,k)n(C,k)/n² and κ = (pₒ − pₑ)/(1 − pₑ). No weighting or cutoff. The script computes pooled κ again, not as a mean; here pooled and Guix are identical. κ is null when n=0 or pₑ=1. The 965 shared automatic decisions are excluded from the agreement denominator because they were not classified independently twice.

| VM/scope | Pairs | Class matches/share | Class κ | Literal matches/share | Literal κ | Class+exact owner matches/share | Owner-sensitive κ |
|---|---:|---|---:|---|---:|---|---:|
| guix | 178 | 143/178 = 80.337079% | 0.633464729 | 4/178 = 2.247191% | 0.020369433 | 110/178 = 61.797753% | 0.365518687 |
| overall | 178 | 143/178 = 80.337079% | 0.633464729 | 4/178 = 2.247191% | 0.020369433 | 110/178 = 61.797753% | 0.365518687 |

| Class | Paired residual: classification 1 | Paired residual: classification 2 | Shared automatic | Full census: classification 1 | Full census: classification 2 |
|---|---:|---:|---:|---:|---:|
| recorded | 116 | 108 | 964 | 1080 | 1072 |
| derivative | 51 | 41 | 0 | 51 | 41 |
| data | 2 | 1 | 1 | 3 | 2 |
| hole-none | 7 | 2 | 0 | 7 | 2 |
| hole-two | 2 | 26 | 0 | 2 | 26 |

Residual totals: 178 each. Full-census totals: 1,143 each (965 automatic + 178 residual). These are overlapping observations across packages, processes, services and stored groups, not counts of distinct physical objects. Original automatic labels are operational proxies, not independently validated §5 judgments. Sources: [preclassified.tsv](preclassified.tsv), [residual.tsv](residual.tsv), [stats.json](raw/v3/stats.json).

## Every disagreement

- [joined.tsv](raw/v3/joined.tsv): every row, original class, owner and reason from both classifiers, inventory evidence, comparison flags and text decision.
- [disagreements.tsv](raw/v3/disagreements.tsv): all **35** normalized class disagreements; **4** resolved at the class level, **31** `not resolved`.
- [literal-disagreements.tsv](raw/v3/literal-disagreements.tsv): all **174** unequal original class strings, including notation differences.
- [owner-disagreements.tsv](raw/v3/owner-disagreements.tsv): all **33** exact-owner-string differences among class-agreeing derivatives. They mix spelling, program-family granularity and attribution. §5 provides no lexical alias table; no new class failures are inferred from these strings alone.
- [definition-audit.tsv](definition-audit.tsv): 71 decisions covering every class disagreement, matching hole and owner mismatch. Resolved rows quote the sentence; every other substantive case says `not resolved`. Original labels and agreement numbers are never rewritten after adjudication.

The four resolved rows are `guix-2cd84ac792` (Avahi log), `guix-b6a2c8e4dd` (D-Bus log), `guix-43c963f378` (Guix daemon log), and `guix-e684d315eb` (ntpd log). Classification 2's stated conflict is Shepherd versus daemon ownership. P6 explicitly says:

> A derivative needed by several programs exists as long as at least one of them is present.

This resolves the claim that different possible owners alone require two incompatible classes: all are derivative readings. It does not establish which programs actually need a log. That O1 evidence limitation and every original hole flag remain recorded. Captured [Shepherd sources](raw/guix/service-source-paths.txt) identify the log paths; the per-row audit cites the relevant evidence.

For copied skeleton settings P5 is conditional: “Any derivative and any data can be recorded in the declaration; they then become subject to it on the same terms as everything else recorded.” [Matching hashes](raw/guix/supplementary-provenance.txt) establish identical bytes, not a text-defined rule that every copied output is recorded; residence in a home does not establish person authorship. These disputes remain `not resolved`.

## Full hole register

**Classification 1: 9; classification 2: 28; union: 32 rows.** All original flags are retained, including resolved log cases. A=`classification 1`, C=`classification 2`; `none`/`two` abbreviate the submitted hole labels. Per-row original reasons and inventory evidence are in [holes.tsv](raw/v3/holes.tsv); the table below gives the audited reason and closest O1–O9 connection. O3 for copied/recorded representations is an analogy to recorded-data status, not a new rule. O6–O8 were not exercised.

| Row | Object | Hole flags | Why / disposition | Open problem |
|---|---|---|---|---|
| guix-0253fce5e2 | `/root/.bash_profile` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-0fbdac78d4 | `/gnu/store/cs56i9digj9qg1bd383cmxc6xrfpdn9n-hello-2.12.2` | C: none | Ordinary-user hello installation/execution is observed. Bypass means an unrecorded running-component change even if forbidden by P4, so forbidden does not mean no class. Whether package-manager output is needed for its operation (derivative) is unresolved by §5; no creator-only rule may be added. | O1,O5,O9 |
| guix-14d33b9392 | `/root/.zprofile` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-2cd84ac792 | `/var/log/avahi-daemon.log` | C: two | Resolved at derivative class: P6 allows multiple owners. Actual program need remains an O1 evidence question; original flag retained. | O1 |
| guix-351644c1fd | `/root/.ssh` | C: two | Manual bootstrap authorized_keys: personal setting versus unrecorded login rule/bypass; object/change boundary not resolved. Instrumentation. | O2,O4 |
| guix-3bc83b10e8 | `/root/.config/nano` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-43c963f378 | `/var/log/guix-daemon.log` | C: two | Resolved at derivative class: P6 allows multiple owners. Actual program need remains an O1 evidence question; original flag retained. | O1 |
| guix-451d25b3c7 | `user profile support outside current system closure` | C: two | Support output or static alias is associated with selection; not proved to store the selection itself. Do not duplicate the manifest case. | O1,O2 |
| guix-4e7a5a4664 | `/home/guest/.guix-profile` | C: two | Support output or static alias is associated with selection; not proved to store the selection itself. Do not duplicate the manifest case. | O1,O2 |
| guix-570c2a56ed | `/home/guest/.guile` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-64f62c6553 | `directory-only remainder` | A: none; C: none | Mixed-member group; different members/purposes do not prove two classes for one object. Not a standalone counterexample. | O1 |
| guix-6633666c2c | `/gnu/store/hmlgnj2qflvif6vvd60n4x9lblkcybsp-profile` | A: two; C: two | Generated personal selection fits operational-state and personal-settings readings; §5 gives no priority, P6 consequences differ. | O1,O2 |
| guix-6e81e82021 | `/home/guest/.config/nano` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-76634f69cd | `/boot/grub` | A: none | Mixed-member group; different members/purposes do not prove two classes for one object. Not a standalone counterexample. | O1 |
| guix-7bc12ec287 | `/home/guest/.config/xfce4` | A: none | Image/desktop history does not establish each member’s creator or purpose; absence of edits in this script is insufficient. | O1,O2 |
| guix-7f3f786b88 | `/home/guest/.config/glib-2.0` | A: none | Image/desktop history does not establish each member’s creator or purpose; absence of edits in this script is insufficient. | O1,O2 |
| guix-88a33ee425 | `/root/guix-home-config.scm` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-8bcc29aa90 | `/home/guest/guix-home-config.scm` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-9052456462 | `/home/guest/.Xdefaults` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-9969ba0797 | `/root/.config/gdb` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-a008390f8b | `/root/.Xdefaults` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-a9e486a84b | `/home/guest/.config/gdb` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-b6a2c8e4dd | `/var/log/dbus-daemon.log` | C: two | Resolved at derivative class: P6 allows multiple owners. Actual program need remains an O1 evidence question; original flag retained. | O1 |
| guix-bd5c3d6b7a | `/home/guest/.config/Thunar` | A: none | Image/desktop history does not establish each member’s creator or purpose; absence of edits in this script is insufficient. | O1,O2 |
| guix-c7553146ab | `/etc/guix` | A: none; C: two | Mixed-member group; different members/purposes do not prove two classes for one object. Not a standalone counterexample. | O1 |
| guix-cfe66bc678 | `/etc/shadow` | C: two | Declared account policy does not prove all mutable password fields recorded; ability to run passwd is not evidence of an edit. | O2,O3 |
| guix-d62cf2da81 | `/root/.guile` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-d68b8b54b5 | `/home/guest/.bash_profile` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-da5f01a3ef | `/gnu/store outside current system closure` | A: none; C: two | Mixed-member group; different members/purposes do not prove two classes for one object. Not a standalone counterexample. | O1,O9 |
| guix-dea3c6354f | `/home/guest/.zprofile` | C: two | Copied skeleton bytes match recorded defaults; §5 gives no propagation rule and home location does not prove personal authorship. | O1,O2,O3 |
| guix-e495746cb2 | `/var/guix/profiles/per-user/guest/guix-profile` | A: two; C: two | Generated personal selection fits operational-state and personal-settings readings; §5 gives no priority, P6 consequences differ. | O1,O2 |
| guix-e684d315eb | `/var/log/ntpd.log` | C: two | Resolved at derivative class: P6 allows multiple owners. Actual program need remains an O1 evidence question; original flag retained. | O1 |

## What lives outside configuration.nix on NixOS

This appendix uses saved observations from V, copied into W with a source/hash manifest. It adds no NixOS classifications or new experiment. The full original outside table is retained. “Outside the literal file” differs from “outside its transitive declaration”: §5 allows a declaration to comprise many files.

| Object | Observed boundary and evidence |
|---|---|
| Imported hardware file, generated `/etc` links/accounts, current system closure | Outside the literal file, indirectly described: configuration.nix imports hardware configuration; account definitions and 618 closure paths retain evaluated results/dependencies. Store outputs are not equivalent to conventional package counts. |
| Imperatively installed hello and user environment/manifest | User closure has 7 paths, 3 outside the system closure. day.log records user `nix-env`, successful hello, and unchanged hashes of both NixOS source files. |
| `~/.local/state/nix/profiles`, alias `~/.nix-profile` | Mutable persistent user selection, one logical mechanism: profile links, member manifest. |
| `.vimrc` and `Documents/day-note.md` | User setting (`set number`) and authored document: day.log. Data outside the declaration is expressly allowed. |
| Runtime identities, host keys, leases, service state and logs | `/etc/machine-id`, SSH host-key values, `/var/lib/dhcpcd`, `/var/lib/systemd`, journal/login records: member manifest. Values/contents are not enumerated in the configuration file. |
| Nix database, GC roots, socket, userpool, profiles/channel state | Mutable package-manager bookkeeping, distinct from declared system-generation targets: member manifest, profiles. |
| Other retained store paths | 4,347 paths outside system and user closures include build descriptions/inputs. They are not 4,347 demonstrated hidden running programs. |

Outside-file presence alone does not satisfy §9.2: permitted derivatives and data also live there. The corresponding Guix observations are separately retained in [guix-outside-declaration.tsv](guix-outside-declaration.tsv): system `config.scm`, applied `home.scm`, imperative profile selection and runtime state must not be conflated.

## Limitations and reproducibility

- One disposable Guix image and a short scripted CLI workload, not a full day or representative personal machine. The image auto-started Xfce; no interactive GUI workload was performed. A later read-only provenance capture supplements the frozen census. Method and timestamps: [METHOD.md](METHOD.md), [day log](raw/guix/day/user-day.log), [supplementary capture](raw/guix/supplementary-provenance.txt).
- Shared inventory and automatic preclassifier limit independence; agreeing classifiers can share errors. Closure membership is a recorded-membership proxy, and captured declarations do not establish a universal transitive-recording rule. Classes attach to inventory rows at different granularities; 34 structural groups and the large outside-closure store group are manifest-backed but heterogeneous. See [residual.tsv](residual.tsv), [directory manifest](raw/guix/directory-only-groups.json), [store remainder](raw/guix/store-outside-system-closure.txt).
- The walk covers `/etc`, `/var`, `/opt`, `/usr/local`, `/srv`, `/home`, `/root`, `/boot`, with Guix state. It does not exhaust `/usr`, `/proc`, `/sys`, `/dev`, `/run`, `/tmp`, firmware or TPM/off-disk state (O9); processes/modules are targeted observations, driver bindings raw-only. Interpreter membership does not establish its script arguments as declared. Collection is non-atomic and includes instrumentation. [METHOD.md](METHOD.md), [walk roots](raw/guix/walk-roots.txt).
- The booted Guix daemon may remain from a saved generation while its replacement is pending; current-closure absence is not proof that its service was undeclared. [Detailed service status](raw/guix/herd-all-service-status.txt), [closure comparison](raw/guix/closure-comparison.json).
- Initial missing-getent collection was corrected and rerun. Optional absent root-profile/mcron/user-Shepherd facilities are reported, not assumed successful. Validation records no final mandatory failures, four optional failures, 120-second dwell, 5,278 walked entries and 8,567 store top-level paths represented. No stand failure is counted as a definition failure. VM shutdown/runtime deletion were already verified in cleanup.
- No lifecycle deletion, rollback or transfer test is performed (O6–O8). P6 is used only to compare stated consequences. Some O1/O2/O3/O4/O5/O9 cases are evidence gaps or overlaps, not independently proved counterexamples. Independent acceptance is documented separately in REVIEW-V3.md.

Reproduce: `python compare.py` (the report renderer is not part of this repository). The script writes only to raw/v3; no VM or network is needed. Input hashes and frozen inputs preserve the comparison basis.
