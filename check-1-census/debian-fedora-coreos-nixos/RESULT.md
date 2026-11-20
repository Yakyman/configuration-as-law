# FV1 — Check 1: corrected clean-VM census

Date: 2026-11-19T08:36:58.915806+00:00. Fix round for REVIEW.md; dispositions and independent review status: FIX-1.md. No VM was started: this round changes adjudication and reporting, not collection or the two submitted classifications.

**Outcomes: Fedora CoreOS 0; Debian 0; NixOS 0; overall 0**, under the unresolved-disagreement branch of §9.2. Evidence-only gaps give **?** for the affected case and do not establish a failure. Counts of textual issue types are diagnostic, not a count of proved counterexamples.

## Fixed condition and application

The frozen [PAPER.html](../../first-paper/PAPER.html), §9.2, says exactly:

> An object is found on either machine that, under the definitions, belongs to no class or belongs to two classes with different consequences, or the two classifications assign the object to different classes and the text of the definitions does not resolve the disagreement.

The original two-machine wording is unchanged; the census covers three VMs. No rule requiring execution to be observed within the census window, no class priority, and no package-membership definition of recorded status is introduced.

| VM | Row / object | Submitted classification 1 / classification 2 | Assessment under the fixed condition |
|---|---|---|---|
| CoreOS | `coreos-89ce5c5668`: kernel threads | derivative of Linux kernel / recorded | **not resolved**, §9.2 third clause: code within the kernel versus a component of the kernel; §5 supplies no component granularity or class priority (O1/O9). This replaces the evidence-limited LVM witness. |
| Debian | `debian-89ce5c5668`: kernel threads | derivative of Linux kernel / recorded | **not resolved**, the same textual disagreement (O1/O9). Used instead of making the netplan attribution decisive. |
| NixOS | `nixos-ea3d75074e`: user Nix profile; alias `nixos-0ae3a1e7df` | hole-two / derivative of nix | **not resolved**, §9.2 third clause: operational profile state versus a person's persisted package choice (O1/O2); profile and alias are one logical example. |
| NixOS | `nixos-d2fde56a38`: hello outside the system closure | hole-none / hole-none | **First clause assessed; retained hole, not an independently proved no-class object.** Bypass denotes a change; P3 adds no class for its resulting object. Installer output versus program need and launch versus creation remain undecided (O1/O4/O5/O9). NixOS 0 already follows from the preceding disagreement. |

Kernel-thread observations, including PID 2 (`kthreadd`), are in [CoreOS processes](raw/coreos/processes.txt), [Debian processes](raw/debian/processes.txt) and the corresponding `process-executables.tsv` files. The submitted explanations and exact PID sets are preserved in [joined.tsv](raw/fv1-comparison/joined.tsv). The third-clause assessment concerns the unresolved component/code distinction in the submitted classifications; it does **not** establish that the kernel was person-designated as recorded. That designation remains unestablished, consistently with the count convention below. The row is not used as proof of dual membership or an implementation impossibility.

Secondary evidence-limited rows: `coreos-1ba388a08e` (`/etc/lvm`) remains `creator-consumer+evidence-gap`, not the decisive CoreOS witness. [unowned-groups.json](raw/coreos/unowned-groups.json) records the 485-byte `system.devices`; [unit-paths.txt](raw/coreos/unit-paths.txt):671 names the service and console.log:1484 records its completion, but no unit body or write trace was saved. Debian `debian-bbe4c8f871` (`/etc/netplan`) remains a textual creator/consumer candidate with an attribution limitation: [unowned-groups.json](raw/debian/unowned-groups.json) records the 483-byte YAML; journal-tail.txt:7 says `Nov 19 06:30:32 v1-debian systemd-networkd[445]: ens3: Configuring with /run/systemd/network/10-netplan-ens3.network.` The link from `50-cloud-init.yaml` to that `.network` file is **inferred, not logged**. Neither secondary row is needed for these outcomes.

Relevant §5.1 text:

> Derivative—an object that a described program has created itself because the object is needed for the program's operation: saved Wi-Fi networks for a network management service, extensions for a browser, a cache, a log.

> Code executed within a program is its derivative.

> Data—what a person has created: photographs, documents, databases, and their own settings files, such as a text editor configuration.

> Bypass—a change to running components that is not recorded in the declaration.

P3 says: “Everything that is on the computer and is not recorded in the declaration is either a derivative of a recorded program or the person's data.” P6 requires a derivative to move to an archive if its program is absent from the current generation; data has no corresponding obligation. These sentences supply no priority resolving the settings/profile disputes.

For the first-clause candidate, [day.log](raw/nixos/day.log):23–29 records the ordinary user's `nix-env` installation and successful execution of hello; configuration hashes before and after are equal. [user-closure-outside-system.txt](raw/nixos/user-closure-outside-system.txt):3 identifies the concrete hello store path; the other two entries are the user environment and manifest, not additional proved no-class objects. Both classifiers give definitional reasons, not just missing provenance. Nevertheless their agreement does not establish exclusion from every class: §5 leaves the installer-need and launching/creation boundaries open. The recorded action is a bypass in the descriptive sense, not evidence that this non-root action is an **explicit permitted bypass** under P4. No fourth class, installer exception or proof of P4 impossibility is inferred. The hole remains even though there is no inter-classifier disagreement.

The earlier A3 semantic review gave CoreOS **?**, Debian **?**, NixOS **0** on the earlier evidence-limited witnesses. Its historical assessment is preserved. This round replaces those witnesses; it does not claim that A3 approved the replacements or that the missing designation/provenance has been supplied.

## Complete comparison and decisions

All 398 residual IDs pair exactly. The 2,652 shared automatic decisions are excluded from agreement/kappa. Counts are grouped observations at overlapping inventory levels, not disjoint physical objects.

- [joined.tsv](raw/fv1-comparison/joined.tsv): all 398 original labels, owners, reasons, evidence pointers and corrected decisions.
- [disagreements.tsv](raw/fv1-comparison/disagreements.tsv): 146 five-category disagreements; **0 resolved, 146 not resolved**.
- [literal-disagreements.tsv](raw/fv1-comparison/literal-disagreements.tsv): 381 unequal label strings, including notation differences.
- [owner-disagreements.tsv](raw/fv1-comparison/owner-disagreements.tsv): 70 same-category derivative owner mismatches; spelling/abstraction differences are not automatically semantic contradictions.
- [frozen adjudications](compare-adjudications.tsv): 232 decisions covering category disagreements, owner mismatches and all original hole flags.
- [agreed-holes.tsv](raw/fv1-comparison/agreed-holes.tsv): all 16 rows with matching hole labels; agreement never exempts a row from the first clause.

`coreos-661587021d` (`.bashrc`) and `nixos-dfc5f24c51` (`.vimrc`) are restored to **not resolved** (O2). Person authorship is observed; the definitions do not give priority over the competing code reading. Absence of a captured execution does not resolve that textual disagreement. Neither actual execution nor proved two-class membership is asserted. The earlier observation-window resolution is withdrawn.

The split below is computed from the existing `issue_type` annotations, with those two rows restored to `definition-boundary`. “Text boundary” means the recorded issue concerns the wording, not that every factual premise or recorded designation is independently proved. Evidence/grouping gaps alone yield **?**; mixed cases require both kinds of uncertainty to be addressed before use as failure witnesses.

| VM | Text boundaries | Evidence/designation/grouping gaps | Mixed creator/consumer + evidence | Total |
|---|---|---|---|---|
| coreos | 2 | 77 | 1 | 80 |
| debian | 7 | 40 | 2 | 49 |
| nixos | 12 | 5 | 0 | 17 |
| overall | 21 | 122 | 3 | 146 |

The previous 144 unresolved rows comprised 19 text boundaries, 122 evidence/designation/grouping gaps and 3 mixed cases. Restoring the settings holes produces **21 / 122 / 3**, total 146. Exact issue-type counts follow; the split is not a classification rule.

| Issue type | coreos | debian | nixos | overall |
|---|---|---|---|---|
| creator-consumer+evidence-gap | 1 | 2 | 0 | 3 |
| definition-boundary | 2 | 2 | 5 | 9 |
| designation+evidence-gap | 66 | 4 | 1 | 71 |
| evidence-gap | 1 | 25 | 1 | 27 |
| execution+evidence-gap | 5 | 8 | 0 | 13 |
| grouping+evidence-gap | 0 | 0 | 1 | 1 |
| grouping-gap | 3 | 0 | 2 | 5 |
| representation+evidence-gap | 2 | 3 | 0 | 5 |
| representation-boundary | 0 | 5 | 7 | 12 |

O-numbers identify the closest open problem. O3 on generated representations is an analogy, not an account-database definition. O6–O8 were not exercised.

## Agreement and submitted class counts

Normalization changes notation only: `recorded (works)` = `recorded`; `derivative of X` becomes `derivative` with X retained as owner. Five-category agreement compares recorded, derivative, data, hole-none and hole-two. The owner-sensitive diagnostic retains exact owner strings with no alias merging.

For each scope, pₒ = matching pairs/n; pₑ = Σₖ n(A,k)n(C,k)/n²; κ = (pₒ−pₑ)/(1−pₑ). No threshold or weighting is used; pooled κ is recomputed. Empty vectors or pₑ=1 give null κ.

**One convention throughout:** all tables count submitted labels and operational proxies, not verified §5 membership. Package/image membership does not establish person designation for either automatic or residual rows. Accordingly **recorded status on Debian/CoreOS is unestablished**, and the pooled recorded total is not an established census of recorded objects. The 71 `designation+evidence-gap` disagreements remain unresolved for the same reason. NixOS has stronger source/import/closure evidence, but its submitted labels are not silently accepted as adjudicated classes. This convention changes no original label and supplies no classification rule.

| VM | n | Five-class matches / share | κ | Literal matches / share | Literal κ | Class+owner matches / share | Class+owner κ |
|---|---|---|---|---|---|---|---|
| coreos | 125 | 45 / 36.000000% | 0.223602484 | 3 / 2.400000% | 0.004893964 | 30 / 24.000000% | 0.205153949 |
| debian | 151 | 102 / 67.549669% | 0.467582932 | 13 / 8.609272% | 0.053678474 | 72 / 47.682119% | 0.430949769 |
| nixos | 122 | 105 / 86.065574% | 0.741911399 | 1 / 0.819672% | 0.007129405 | 80 / 65.573770% | 0.491817911 |
| overall | 398 | 252 / 63.316583% | 0.454804751 | 17 / 4.271357% | 0.025306122 | 182 / 45.728643% | 0.375486721 |

Residual class counts. Each cell is **classification 1 / classification 2**; these are the submitted decisions, not post-adjudication replacements.

| Class | coreos | debian | nixos | overall |
|---|---|---|---|---|
| recorded | 2 / 71 † | 25 / 30 † | 64 / 70 | 91 / 171 † |
| derivative | 47 / 49 | 73 / 101 | 48 / 49 | 168 / 199 |
| data | 1 / 0 | 1 / 1 | 1 / 0 | 3 / 1 |
| hole-none | 75 / 4 | 52 / 15 | 7 / 2 | 134 / 21 |
| hole-two | 0 / 1 | 0 / 4 | 2 / 1 | 2 / 6 |

Full-census **submitted-label/proxy totals**: shared automatic preclassification plus residual labels. Of the 2,652 automatic rows, 2,649 carry the recorded proxy and 3 data. Recorded membership is unestablished for Debian/CoreOS (and therefore the pooled total); † marks those counts explicitly. The shared rows are excluded from agreement.

| Class | coreos | debian | nixos | overall |
|---|---|---|---|---|
| recorded | 1098 / 1167 † | 712 / 717 † | 930 / 936 | 2740 / 2820 † |
| derivative | 47 / 49 | 73 / 101 | 48 / 49 | 168 / 199 |
| data | 2 / 1 | 2 / 2 | 2 / 1 | 6 / 4 |
| hole-none | 75 / 4 | 52 / 15 | 7 / 2 | 134 / 21 |
| hole-two | 0 / 1 | 0 / 4 | 2 / 1 | 2 / 6 |

| VM | Classification 1 holes | Classification 2 holes | Union holes |
|---|---|---|---|
| coreos | 75 | 5 | 77 |
| debian | 52 | 19 | 59 |
| nixos | 9 | 3 | 11 |
| overall | 136 | 27 | 147 |

## What is outside configuration.nix on NixOS

The complete original inventory is [nixos-outside-configuration.tsv](nixos-outside-configuration.tsv). Literal-file absence differs from absence from the transitive declaration; §5 permits a declaration consisting of many files.

| Object | Observation and evidence |
|---|---|
| Imported hardware configuration, current system closure, generated `/etc` links and accounts | Outside the literal file but indirectly declared: explicit import in [configuration.nix](raw/nixos/nixos-configuration/configuration.nix), 618 paths in [system-closure.txt](raw/nixos/system-closure.txt), generated definitions in [account-definitions.txt](raw/nixos/account-definitions.txt). 618 store outputs are not 618 dpkg/RPM-equivalent packages. |
| User-installed hello and profile environment/manifest | Seven paths in [user-closure.txt](raw/nixos/user-closure.txt), three absent from the system closure: hello, user environment and manifest, listed in [user-closure-outside-system.txt](raw/nixos/user-closure-outside-system.txt). Installation and execution left both NixOS source-file hashes unchanged in [day.log](raw/nixos/day.log). |
| User profile links and selection | `~/.local/state/nix/profiles`, alias `~/.nix-profile`; [unowned-groups.json](raw/nixos/unowned-groups.json) and [nix-profiles.tsv](raw/nixos/nix-profiles.tsv). Same logical selection, not two independent examples. |
| Personal setting and document | `.vimrc` containing `set number`; `Documents/day-note.md`; authored in [day.log](raw/nixos/day.log), entries retained in [files.tsv](raw/nixos/files.tsv). |
| Runtime identity, credentials, leases, logs and service state | `/etc/machine-id`, SSH host-key values, `/var/lib/dhcpcd`, `/var/lib/systemd`, journals and login records; [unowned-groups.json](raw/nixos/unowned-groups.json). Generated values are not enumerated in the source configuration. |
| Mutable Nix operation and channel state | `/nix/var/nix/db`, gcroots, daemon socket, userpool, profiles and root channel bookkeeping; [unowned-groups.json](raw/nixos/unowned-groups.json), [nix-profiles.tsv](raw/nixos/nix-profiles.tsv). System profile targets and mutable link state are distinct. |
| Other retained Nix store objects | 4,347 additional paths outside both system and user closures in [store-outside-system-closure.txt](raw/nixos/store-outside-system-closure.txt), including build descriptions/inputs. They are not 4,347 demonstrated hidden running programs. |

Being outside configuration.nix alone is not a §9.2 failure, since derivatives and data are expressly allowed. This census does not prove or disprove NixOS compliance with P4.

## Limitations and reproducibility

- The short scripted CLI “day” lasted minutes, not 24 hours: one user, one extra program per VM, no GUI or long-lived workload. These are disposable clean images, not representative personal machines. Collection method and exclusions: [METHOD.md](METHOD.md).
- Package/image membership is an operational recorded proxy, not evidence of person designation under §5. This matters especially for Debian/CoreOS. NixOS source imports and closures provide a stronger declaration trace. Neither classifier's provenance assertions are silently promoted to observed write traces.
- Inventory rows mix packages, processes, account identities and directory groups; observations can overlap. Directory-only rows and Nix store groups can be heterogeneous. Per-row `member_count`/raw manifests preserve detail, but heterogeneous membership does not prove one object belongs to two classes.
- General walks omit `/proc`, `/sys`, `/dev`, `/run`, `/tmp`, some `/usr` objects and the full CoreOS backing store; targeted facilities cover only part of these. Firmware/TPM state is not inventoried (O9). Device-driver bindings and inactive-unit listings remain raw-only. Collection is not atomic and includes the collector's processes.
- CoreOS escaped unit names have a metadata matching defect; earlier provisioning failures and collection retries are stand defects, not hypothesis failures. The two classifiers share the same reduced inventory and automatic preclassifier; their independence does not exclude correlated errors.
- Original `hole-none` sometimes means missing evidence, not a demonstrated empty class set. Original hole flags, including the two restored settings holes, remain visible below. Owner names differ in abstraction and spelling; the owner-sensitive statistic is conservative and not proof of 70 distinct ownership disputes.
- Definitions, original classifications, raw census evidence and old frozen outputs are unchanged. Current adjudications and reporting are corrected; previous versions are preserved in before/. New input hashes are in [metrics.json](raw/fv1-comparison/metrics.json); verification: validation.json.
- The earlier definition-review.md addendum's settings resolution is superseded by FV1 and REVIEW.md. Independent fix review and its disposition are recorded in FIX-1.md. Local mechanical checks do not substitute for independent acceptance.

Reproduce into a **new** comparison directory; existing comparison outputs are rejected:

```sh
python compare.py --output raw/fv1-reproduction
```

The comparison freezes its inputs, validates duplicate/missing IDs, class/owner consistency, adjudication coverage and exact §5 resolving quotations, and preserves fractional κ. The report renderer that produced this text is not part of this repository.

## Full list of flagged holes

All **147** rows marked as a hole by either original classifier appear below, including the restored settings holes. `A` means classification 1, `C` classification 2; `none`/`two` abbreviate their submitted hole labels. The reason is FV1's assessment of the flag, not a new class. Original reasons and per-row raw-evidence pointers are preserved in [the complete hole TSV](raw/fv1-comparison/holes.tsv). Row IDs join directly to [residual.tsv](residual.tsv). O1–O9 mappings are diagnostic references, not added classification rules.

| Row / VM | Object | Flagged by | Why / assessment | Open problem |
|---|---|---|---|---|
| coreos-0075a76d48 | /etc/ssh | A: none | The row groups structural or heterogeneous entries; a single class is not established. A mixed inventory group is not proof that one object has two classes. | O1 |
| coreos-016dfe226d | avahi-autoipd | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-03b6505825 | rpcuser | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-09d09204d8 | /etc/sudoers.d | A: none | Seeded authorization values and generated/copied files are distinct levels; §5 does not state that inclusion of a value records every resulting file. | O1;O3 |
| coreos-0ac5a10e67 | coreos-platform-chrony-config.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-0b2fc8af1f | tcpdump | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-0ef3eb01b3 | /var/home/census/.bash_logout | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| coreos-14dc4e5831 | core | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-1525133242 | systemd-timesync | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-167f3063ff | coreos-populate-lvmdevices.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-195a1b489c | systemd-oom | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-1af8deec0e | /etc/modprobe.d | A: none | Deployed-image content is claimed recorded, while provenance/designation or generated origin is disputed; §5 does not equate image membership with person designation. | O1;O3 |
| coreos-1ba388a08e | /etc/lvm | C: none | Creation and consumption are attributed to different programs; §5 does not say whether indirect setup need suffices. Mixed contents or image-build provenance add uncertainty. | O1 |
| coreos-1bebb37879 | kube | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-1f9ebd3eec | polkitd | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-23a9706caf | /boot/grub2 | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| coreos-245a92fd3e | etcd | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-28c046fc91 | dnsmasq | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-2d7adb8ef6 | /var/roothome | A: none | Deployed-image content is claimed recorded, while provenance/designation or generated origin is disputed; §5 does not equate image membership with person designation. | O1;O3 |
| coreos-3620611c7e | /boot/boot | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| coreos-37c52140e1 | sssd | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-3d437d2b28 | halt | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-4900fca16b | daemon | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-4c29fefef0 | dbus | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-4c9f8adea6 | coreos-warn-invalid-mounts.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-4d882498fa | /etc/pam.d | A: none | Deployed-image content is claimed recorded, while provenance/designation or generated origin is disputed; §5 does not equate image membership with person designation. | O1;O3 |
| coreos-54ef0687f4 | systemd-resolve | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-55e4967557 | lp | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-5ab2e196c7 | dockerroot | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-64c4ab9fc8 | nfsnobody | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-64f62c6553 | directory-only remainder | A: none | The row groups structural or heterogeneous entries; a single class is not established. A mixed inventory group is not proof that one object has two classes. | O1 |
| coreos-661587021d | /var/home/census/.bashrc | C: two | Person-authored setting meets the data wording; the competing code-within-a-program reading has no boundary or priority in §5. Absence of an execution trace during the census does not resolve that textual dispute. Keep the O2 hole without claiming observed execution or proved two-class membership. | O2 |
| coreos-688f82dd27 | adm | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-70c3717c60 | ftp | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-75de6dcfcb | coreos-update-ca-trust.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-788a40727c | rpc | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-79d1cbcc95 | ignition-delete-config.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-7b28a710b2 | coreos-ignition-write-issues.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-7b9cb61b42 | /boot/coreos | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| coreos-832595bcce | zincati | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-839c0c17a5 | systemd-bus-proxy | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-83bc7a060a | clevis | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-842ef8c3bd | coreos-ignition-firstboot-complete.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-84b24ebf2a | /etc/security | A: none | Deployed-image content is claimed recorded, while provenance/designation or generated origin is disputed; §5 does not equate image membership with person designation. | O1;O3 |
| coreos-86d74136ea | chronyd.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-8d1e409524 | bin | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-8e4a0f0c6a | games | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-95ac45c046 | /var/home/core/.bash_logout | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| coreos-9a8b0774fb | coreos-ignition-delete-config.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-9ac48a93f2 | coreos-printk-quiet.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-9b11573e98 | bootloader-update.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-9b47a2a2ff | systemd-fsck@dev-disk-by\x2duuid-b1dba14c\x2d5e68\x2d439d\x2db965\x2d5427e22d7535.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-9b7b30cbba | /var/home/core/.bash_profile | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| coreos-9faaf00905 | coreos-warn-misplaced-network.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-a2044ac6f8 | ceph | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-a464712e08 | shutdown | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-ab8c35e257 | sync | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-af2a58bec6 | nobody | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-b2b64aaca8 | /var/home/census/.ssh | A: none | Seeded authorization values and generated/copied files are distinct levels; §5 does not state that inclusion of a value records every resulting file. | O1;O3 |
| coreos-b86fee9a16 | /etc/systemd | A: none | The row groups structural or heterogeneous entries; a single class is not established. A mixed inventory group is not proof that one object has two classes. | O1 |
| coreos-ba123e6f1b | /etc/containers | A: none | Deployed-image content is claimed recorded, while provenance/designation or generated origin is disputed; §5 does not equate image membership with person designation. | O1;O3 |
| coreos-be57689b36 | /var/home/census/.bash_profile | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| coreos-be7c5e2840 | operator | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-bee4a827f4 | cockpit-ws | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-bf56b0bc9b | /etc/sysconfig | A: none | Deployed-image content is claimed recorded, while provenance/designation or generated origin is disputed; §5 does not equate image membership with person designation. | O1;O3 |
| coreos-c1cb4d2cb3 | coreos-check-ssh-keys.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-ca040c10df | systemd-repart.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-cbaf0b4232 | root | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-cc3f68da69 | /boot/.root_uuid | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| coreos-cc70cd5e32 | /var/home/core/.bashrc | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| coreos-cff9eec648 | tss | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-dbea3590f8 | sshd | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-e7927b082e | systemd-coredump | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-eb57ff0e5c | unpackaged *.socket | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| coreos-ecfab3dd45 | mail | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-ee17e5a4df | systemd-network | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| coreos-f3d59b813f | chrony | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| debian-0075a76d48 | /etc/ssh | A: none; C: none | Creation and consumption are attributed to different programs; §5 does not say whether indirect setup need suffices. Mixed contents or image-build provenance add uncertainty. | O1 |
| debian-0306bdd9a9 | /etc/ssl | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-0326839754 | /etc/ca-certificates.conf.dpkg-old | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-0758efc3b0 | systemd-growfs@-.service | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
| debian-09d09204d8 | /etc/sudoers.d | A: none | Seeded authorization values and generated/copied files are distinct levels; §5 does not state that inclusion of a value records every resulting file. | O1;O3 |
| debian-0b2fc8af1f | tcpdump | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| debian-0fbf442b3c | /root/.profile | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| debian-1af8deec0e | /etc/modprobe.d | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-20302e112e | /etc/sgml | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-211f893687 | /etc/grub.d | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| debian-228a030233 | /etc/default | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| debian-2adfd50853 | /etc/gshadow | C: two | Recorded account entries and generated database representation are different inventory levels; §5 does not propagate class membership from entries to the whole file. | O1;O3 |
| debian-2d36998dd6 | /home/census/.bashrc | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| debian-2dfb100dfa | /etc/python3 | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-34803cf70a | /etc/cloud | C: none | Creation and consumption are attributed to different programs; §5 does not say whether indirect setup need suffices. Mixed contents or image-build provenance add uncertainty. | O1 |
| debian-351644c1fd | /root/.ssh | A: none | Seeded authorization values and generated/copied files are distinct levels; §5 does not state that inclusion of a value records every resulting file. | O1;O3 |
| debian-3543b3a205 | /etc/profile | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| debian-3787beb4db | /home/census/.bash_logout | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| debian-384e8d981f | /etc/apparmor.d | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-413e0b552f | /etc/inputrc | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-493d4cfdb1 | /etc/passwd | C: two | Recorded account entries and generated database representation are different inventory levels; §5 does not propagate class membership from entries to the whole file. | O1;O3 |
| debian-4cce813fe8 | /etc/fstab | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-4d882498fa | /etc/pam.d | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-5b5a9c277e | /etc/shells | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-5bf2e2415a | /boot/efi | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-5cad41b508 | /etc/hosts | C: none | Creation and consumption are attributed to different programs; §5 does not say whether indirect setup need suffices. Mixed contents or image-build provenance add uncertainty. | O1 |
| debian-5deb3892cc | /etc/environment | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-5f65179c45 | /etc/nsswitch.conf | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-64f62c6553 | directory-only remainder | A: none; C: none | The row groups structural or heterogeneous entries; a single class is not established. A mixed inventory group is not proof that one object has two classes. | O1 |
| debian-66fa11f56b | /etc/xml | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-6f021dad80 | /etc/networks | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-72dead8488 | /etc/cloud-release | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-76634f69cd | /boot/grub | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-7740cdd4af | /etc/dpkg | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-84b24ebf2a | /etc/security | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-8c833da179 | /etc/timezone | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-90017bfd94 | /root/.bashrc | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| debian-966442e2a8 | /etc/localtime | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-97fc2dd36c | /usr/local/man | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-98e3025b9e | /var/spool/mail | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-9cf6463675 | /etc/ca-certificates.conf | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-9e65e302c3 | /etc/modules | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-a0ea4d1be3 | uuidd | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| debian-a349a8354f | /etc/kernel-img.conf | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-a763d184b3 | /etc/group | C: two | Recorded account entries and generated database representation are different inventory levels; §5 does not propagate class membership from entries to the whole file. | O1;O3 |
| debian-b86fee9a16 | /etc/systemd | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-b8a8c42f35 | /etc/hosts.deny | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-bbe4c8f871 | /etc/netplan | C: none | cloud-init creates network configuration consumed by netplan/networkd; §5 does not decide whether this satisfies the creator’s own operational need. | O1 |
| debian-c15063bcfe | /home/census/.profile | A: none | The code clause requires code executed within a program; copied-file provenance or a shell-file name alone does not prove this premise or exclude authored data. | O1;O2 |
| debian-c3a3dd6c9b | /home/census/.ssh | A: none | Seeded authorization values and generated/copied files are distinct levels; §5 does not state that inclusion of a value records every resulting file. | O1;O3 |
| debian-ce45570012 | /etc/apt | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-cf102b2bab | /etc/locale.gen | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-cfe66bc678 | /etc/shadow | C: two | Recorded account entries and generated database representation are different inventory levels; §5 does not propagate class membership from entries to the whole file. | O1;O3 |
| debian-d47133480a | /etc/hosts.allow | A: none; C: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-dbea3590f8 | sshd | A: none | Account exists, but creator/need or person-designated declaration membership is disputed; image/package provenance alone is not the designation required by §5. | O1 |
| debian-e2573a99e5 | /etc/runit | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-f3f8b50a94 | /etc/initramfs-tools | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-f4c9cf7ef7 | /etc/tmpfiles.d | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| debian-fb657bdf06 | /etc/motd | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| nixos-0075a76d48 | /etc/ssh | A: none | The row groups structural or heterogeneous entries; a single class is not established. A mixed inventory group is not proof that one object has two classes. | O1 |
| nixos-09d9e916a6 | /etc/sudoers | A: none | Declared content and generated live output are both described in the evidence; §5/P5 does not specify whether representation inherits recorded status or loses derivative origin. | O1;O3 |
| nixos-0ae3a1e7df | /home/census/.nix-profile | A: two | Nix-generated profile also encodes the personal package-selection setting; §5 does not settle that boundary. Profile and alias are one logical example. | O1;O2 |
| nixos-56394eddb3 | /etc/nixos | C: none | §5 identifies these files as the declaration but does not thereby classify the declaration’s own authored/generated files as recorded objects; no self-inclusion rule is given. | O1;O3 |
| nixos-64f62c6553 | directory-only remainder | A: none | The row groups structural or heterogeneous entries; a single class is not established. A mixed inventory group is not proof that one object has two classes. | O1 |
| nixos-bfd49e603a | /nix/store outside current system closure | A: none | Retained store paths mix build descriptions, inputs and outputs; store location does not establish a single creator, need or running-component status. | O1;O9 |
| nixos-c093c82f20 | /etc/NIXOS | A: none | Creator, program need or declaration designation is not established by the saved provenance; the definition cannot supply those facts. | O1 |
| nixos-d2fde56a38 | user profile closure outside current system closure | A: none; C: none | First clause of §9.2 assessed: hello is installed and launched outside the system closure; both classifiers mark hole-none. §5.1 defines Bypass as a change, not a class of resulting objects; P3 offers only derivative or data for the unrecorded remainder. Installer output versus program need (O1) and launch versus creation (O5) are undecided. Retain the no-class candidate as a hole (O4/O5); agreement alone does not prove all classes excluded, and the three-path group is not one no-class object. No claim of P4 impossibility. | O1;O4;O5;O9 |
| nixos-dfc5f24c51 | /home/census/.vimrc | C: two | Person-authored setting meets the data wording; the competing code-within-a-program reading has no boundary or priority in §5. Absence of an execution trace during the census does not resolve that textual dispute. Keep the O2 hole without claiming observed execution or proved two-class membership. | O2 |
| nixos-ea3d75074e | /home/census/.local/state/nix | A: two | Nix-generated profile also encodes the personal package-selection setting; §5 does not settle that boundary. Profile and alias are one logical example. | O1;O2 |
| nixos-eb57ff0e5c | unpackaged *.socket | A: none | Unit provenance or generated/masked status does not establish declaration designation and unique owner; inactive references must not be assumed to run. | O1;O9 |
