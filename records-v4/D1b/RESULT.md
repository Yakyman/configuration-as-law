STEP 4: alma ?; void 0B; gentoo 0B; microos ?B; talos 0B; together 0B

2026-11-23 UTC. Compilation for S4-H; independent acceptance belongs to review RV-S4-H.

The outcomes apply only to the objects selected for this step. They follow the committed “What counts against the hypothesis” and “Outcome” rules in `SUP1/step-4.md`, using every verdict in `D1b/adjudication/rows.tsv` unchanged. A row absent from that adjudication keeps its matching c1/c2 decision from `D1b/compare/joined.tsv`. `UNKNOWN` means a deciding fact is missing; it is not a gap. A resolved `MIXED` row retains the member decisions established by adjudication and is not counted as a gap.

Reading A in `check-inputs-v4/QUESTIONS.md` treats existing second-level rows as an obtained level; reading B requires the whole level. The suffix B marks reading B in the first line, including its combined outcome. AlmaLinux has no delivered second level, so its ? does not depend on choosing A or B. Under either reading the combined outcome is 0: Appendix A.4.1 combines by 0 first, then ?, then 1. No outcome of the first night is changed, and no outcome for the unselected new objects is claimed.

## Per-machine outcomes and inventory coverage

| Machine | Original inventory (L1 / L2) | Delivered new inventory | Objects decided in this step | First-night unmatched | A | B | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| alma | 5,711 (4,026 / 1,685) | 0 | 0 | 66 | ? | ? | No delivered inventory; the committed handoff failed, so there is no object decision on which to claim 1. |
| void | 3,279 (1,211 / 2,068) | 3,279 | 1,143 | 1 | 0 | 0 | One GAP object (card 2) gives 0; 1,076 other selected objects remain fact-unknown. |
| gentoo | 32,775 (1,210 / 31,565) | 32,775 | 32,775 | 0 | 0 | 0 | 24 GAP objects (cards 1 and 2) give 0; 30,075 other objects remain fact-unknown. |
| microos | 6,567 (1,464 / 5,103) | 6,567 | 747 | 7 | ? | ? | No GAP verdict; 37 selected objects remain fact-unknown, preventing 1 even under A. |
| talos | 278 (225 / 53) | 278 | 43 | 0 | 0 | 0 | 12 GAP objects (card 1) give 0; 17 other selected objects remain fact-unknown. |
| together | 48,610 | 42,899 | 34,708 | 74 | 0 | 0 | At least one machine gives 0 under each reading. |

Counts and coverage: `D1b/in/READY.md`; selection and unmatched objects: `D1b/in/match/`; decisions: `D1b/compare/joined.tsv` joined by id to `D1b/adjudication/rows.tsv`. “Decided in this step” means assessed rows, including UNKNOWN and GAP, not only resolved rows. The original inventory total includes the 5,711 undelivered AlmaLinux objects.

| Machine | Was the second level obtained? |
| --- | --- |
| alma | Raw level obtained only in part: filesystem_complete=true, package_ownership_complete=false, unresolved ownership and atomic images/stores. None delivered: copier failed with `_csv.Error: field larger than field limit (131072)`; no repair or rerun. |
| void | Part only: implemented traversal complete, package ownership incomplete; 15 atomic image rows, 72,162 members in three stores, without complete payload receipts or creator events. |
| gentoo | Part only: implemented traversal complete, package ownership incomplete; npm per-file provenance unresolved, no complete adapter for the discovered Go manager; 11 atomic images and 530 members in two stores. Eight ordinary actions passed; browser_extension failed once. |
| microos | Part only despite both completeness flags: 20 image rows and `/.snapshots/2/snapshot` remain unexpanded; `/etc` has 2,219 recorded descendants; inner store tables are header-only. |
| talos | Part only: filesystem_complete=false, depth/count bounds and 18 retained boundaries; 8,503 members in 1,219 directory listings; 5,932/5,963 bounded content reads succeeded. The literal package_ownership_complete=true flag does not remove the explicit coverage limits. |

## Counts after compilation

From `D1b/compare/STATS.md`: **34,708** objects, all with a valid decision from both parties; **5,074 / 34,708 = 14.62%** matching decision labels; **Cohen’s kappa = 0.08855**. These are the original comparison measures, before adjudication, not a recomputation from the final outcomes. The 30,024 adjudicated rows comprise 29,634 differing decision labels plus 390 matching MIXED labels.

| Adjudication verdict | alma | void | gentoo | microos | talos | Total |
| --- | --- | --- | --- | --- | --- | --- |
| GAP | 0 | 1 | 24 | 0 | 12 | 37 |
| UNKNOWN | 0 | 7 | 29,288 | 13 | 17 | 29,325 |
| RESOLVED:INSTALLED-OWN | 0 | 0 | 1 | 0 | 0 | 1 |
| RESOLVED:INSTALLED-PACKAGE | 0 | 0 | 178 | 1 | 10 | 189 |
| RESOLVED:PROGRAM-OWN | 0 | 0 | 8 | 0 | 0 | 8 |
| RESOLVED:SETTING-OWN | 0 | 10 | 14 | 0 | 0 | 24 |
| RESOLVED:RECORD | 0 | 2 | 28 | 0 | 1 | 31 |
| RESOLVED:RUNTIME | 0 | 0 | 33 | 0 | 2 | 35 |
| RESOLVED:MIXED | 0 | 3 | 371 | 0 | 0 | 374 |
| Total | 0 | 23 | 29,945 | 14 | 42 | 30,024 |

Source: `D1b/adjudication/rows.tsv`, grouped by its literal `verdict` and the machine in `D1b/compare/joined.tsv`. No other adjudication verdict occurs. There are 662 resolved adjudication rows, 29,325 UNKNOWN verdicts, and 37 GAP verdicts. The 4,684 rows outside adjudication comprise 2,804 resolved matching rows and 1,880 matching UNKNOWN rows.

| Machine | Resolved rows (including member decisions) | Fact-unknown rows | GAP rows | All assessed rows |
| --- | --- | --- | --- | --- |
| alma | 0 | 0 | 0 | 0 |
| void | 66 | 1,076 | 1 | 1,143 |
| gentoo | 2,676 | 30,075 | 24 | 32,775 |
| microos | 710 | 37 | 0 | 747 |
| talos | 14 | 17 | 12 | 43 |
| Total | 3,466 | 31,205 | 37 | 34,708 |

The counts are inventory objects, not the number of files inside grouped objects. The 74 unmatched first-night objects receive no decision here and are not added to the 31,205 fact-unknown assessed objects. There is no pair of matching GAP labels and no additional gap found by both parties outside the 37 GAP verdicts; matching MIXED rows were also adjudicated.

### Fact-unknown objects by kind

| Kind | alma | void | gentoo | microos | talos | Total |
| --- | --- | --- | --- | --- | --- | --- |
| L1:account | 0 | 1 | 18 | 2 | 0 | 21 |
| L1:group | 0 | 0 | 37 | 20 | 0 | 57 |
| L1:openrc-runlevel | 0 | 0 | 5 | 0 | 0 | 5 |
| L1:openrc-service | 0 | 0 | 7 | 0 | 0 | 7 |
| L1:package | 0 | 0 | 375 | 0 | 0 | 375 |
| L1:sudo-access | 0 | 0 | 5 | 0 | 0 | 5 |
| L1:unit-file | 0 | 0 | 0 | 4 | 0 | 4 |
| L1:user-unit-file | 0 | 0 | 0 | 1 | 0 | 1 |
| L2:code-ownership-unresolved | 0 | 0 | 1,363 | 0 | 0 | 1,363 |
| L2:image | 0 | 0 | 3 | 0 | 0 | 3 |
| L2:image-container-store | 0 | 1 | 0 | 0 | 0 | 1 |
| L2:opaque-directory | 0 | 0 | 0 | 0 | 3 | 3 |
| L2:snapshot | 0 | 0 | 0 | 1 | 0 | 1 |
| L2:stored-outside-packages | 0 | 0 | 0 | 9 | 0 | 9 |
| L2:stored-ownership-unknown | 0 | 0 | 0 | 0 | 14 | 14 |
| L2:stored-ownership-unresolved | 0 | 1,074 | 28,262 | 0 | 0 | 29,336 |
| Total | 0 | 1,076 | 30,075 | 37 | 17 | 31,205 |

### Fact-unknown objects by missing fact

These are disjoint reporting groups of the same 31,205 rows. Each group preserves the missing fact stated in the adjudication note, or both original reasons where matching UNKNOWN rows were not adjudicated. Several grouped objects lack more than one fact; a group naming several facts counts each affected object once. The example id locates the saved note/reasons in `D1b/adjudication/rows.tsv` and `D1b/compare/joined.tsv`; the selection column makes the grouping reproducible without guessing new facts.

| Group | Missing fact | Rows | Selection | Example id |
| --- | --- | --- | --- | --- |
| G1 | Whether a package was explicitly selected or installed as a dependency. | 375 | gentoo; L1:package | d1b-gentoo-4fdc4b1911980b52450bbf10 |
| G2 | How the repository tree was acquired and which source obtained its code/data; matching UNKNOWN reasons also leave interpreter availability or execution as code unrecorded. | 29,307 | gentoo; names under /var/db/repos, excluding the two profile-chain rows | d1b-gentoo-d1a1869b5087cbcc4f6df688 |
| G3 | Whether these profile values belong to the selected, obeyed profile chain. | 2 | gentoo; two notes beginning Profile values | d1b-gentoo-d4bcdd8be82152fedbb1c210 |
| G4 | Original package-member comparison, including directory integrity; some grouped rows also lack the creator of unowned links. | 228 | gentoo; notes containing CONTENTS directories, plus /usr/bin | d1b-gentoo-c182f830d8ab49985277b6d4 |
| G5 | Account/group creation event: installation default or a person’s choice. | 55 | gentoo; L1:account or L1:group | d1b-gentoo-e272e21fd7b107c7d58b9c76 |
| G6 | Whether each effective privilege value is an installation default or a later personal choice. | 5 | gentoo; L1:sudo-access | d1b-gentoo-6f51347974368c552609ddb2 |
| G7 | Whether a package script or a person created the runlevel links; script source alone does not establish execution. | 12 | gentoo; L1:openrc-service or L1:openrc-runlevel | d1b-gentoo-8430e5795c0707e38860524b |
| G8 | Unidentified pip response body: data/index page or archive of code. | 19 | gentoo; UNKNOWN names under /home/user/.cache/pip/http-v2 | d1b-gentoo-9bd07964b6ec0095829c01df |
| G9 | Browser payload contents, source of compiled script caches, or whether saved values launch something or grant access. | 4 | gentoo; four browser cache/profile/store rows identified by notes | d1b-gentoo-74cb2b959ad9f0180a56d987 |
| G10 | Whether the system built/copied the code from a source or a person supplied it (own versus derived coverage). | 8 | gentoo; remaining L2:code-ownership-unresolved or L2:image | d1b-gentoo-cefb08f95822c620fa8edafe |
| G11 | Creation or selection history together with original package metadata, comparison or link target. | 10 | gentoo; remaining matching UNKNOWN rows | d1b-gentoo-ed2a8894895ef7eb91e9dcbc |
| G12 | Who wrote the saved nftables ruleset and whether the service loads it. | 1 | gentoo; /var/lib/nftables | d1b-gentoo-508d38e17d282cec0debe751 |
| G13 | Creator, acquisition or derivation event for remaining directories, boot/GRUB groups, settings, keys, selection links and saved state. | 49 | gentoo; remaining UNKNOWN rows; all notes explicitly leave those events unrecorded | d1b-gentoo-0d021149a1badb08ee1d1fba |
| V1 | Original old-kernel package provenance and reference comparison: whether the members remain as received. | 1,068 | void; matching UNKNOWN notes about original package provenance | d1b-void-5933a7ab38ed2c6e261307b0 |
| V2 | Origin of root’s /bin/sh value: an earlier base-files default or a person’s choice. | 1 | void; L1:account | d1b-void-14aecb121740cea2d41bda86 |
| V3 | Integrity comparison for installed application/runtime files and repository objects. | 1 | void; L2:image-container-store | d1b-void-a1dbd2aa543dcaa9fc26e311 |
| V4 | Reference for old kernel files, initramfs builder and GRUB directory creator. | 1 | void; /boot | d1b-void-e2eaf799995627549514724b |
| V5 | Creation/choice event: installation default, program output or a person’s value. | 3 | void; /etc/default, /etc/modules-load.d, /etc/sudoers.d | d1b-void-f94480229ceee52dfca25523 |
| V6 | How the trusted signing key arrived: image-builder copy or confirmed import. | 1 | void; /var/db/xbps/keys | d1b-void-1aba5ad464188d286f2c87e5 |
| V7 | Creator and package provenance of the persistent /mnt/lab directory. | 1 | void; /mnt | d1b-void-88bc9ff6f55f73bba3cf61e9 |
| M1 | Account/group creation event: installation default or a person’s choice. | 22 | microos; L1:account or L1:group | d1b-microos-62e69634eb677cc7b715d241 |
| M2 | Alias-link creation event: package preset or a person. | 5 | microos; L1:unit-file or L1:user-unit-file | d1b-microos-d6842be9fe6a468b5f044b0e |
| M3 | Original package comparison and creator of the /etc snapshot subvolume. | 1 | microos; L2:snapshot | d1b-microos-8c0d934f64bedecf0619f2f0 |
| M4 | Original comparison/receipt for snapshot files and directory members; some unowned members also lack creator history. | 6 | microos; snapshot audit, crypto-policies, lvm, selinux, ssl and zypp groups | d1b-microos-51818afdedac382f2e76ff2d |
| M5 | Whether a digest-less audit rule is unchanged package content, generated at installation or chosen later. | 1 | microos; snapshot etc/audit/rules.d | d1b-microos-eaa172a157463a1f87fcf619 |
| M6 | Whether changed policy was chosen, generated at installation or saved as historical policy. | 1 | microos; snapshot etc/selinux/targeted/policy | d1b-microos-64b79fd5387353990e4c8ed9 |
| M7 | Creators of grubenv and four unowned directories. | 1 | microos; /boot/grub2 | d1b-microos-d54eadcb6b1b99287fccaf2c |
| T1 | Comparison with the installed-image reference; some members also lack overlay-layer or boot-writer provenance. | 15 | talos; UNKNOWN rows other than the two stores below | d1b-talos-dd2b8a1e4f21f9f8653c0906 |
| T2 | Who pulled the snapshot code and the source line that obtained it. | 1 | talos; note beginning Blobs are JSON | d1b-talos-3da20a4239d2bce2616f4852 |
| T3 | Creators or contents of keys/certificates and pod directories, including failed content reads. | 1 | talos; note beginning State files | d1b-talos-d66a06c314cf71400cf92874 |

## Gap cards

The following two cards reproduce the adjudication’s gap outcomes from `D1b/adjudication/HOLES.md` and the `hole` column of `rows.tsv`; they are not a new adjudication. Exact object names and original decisions come from `D1b/compare/joined.tsv`. Neither card is placed in a wording-gap list or an idea-gap list. That choice remains the author’s question under `SUP1/step-4.md`; it cannot change these outcomes.

For the side-by-side answers, Q1 asks whether the object must be in a declaration describing everything installed and every setting; Q2 asks whether a system can meet that requirement without forbidding any ordinary action in Section 9.2. These are the two questions referenced by step 4 through `PROTOCOL.md` Section 2; no weighting is performed here. “Not supplied” is a missing answer, not “no”, agreement, or a reason to alter a GAP verdict.

### Gap 1. Container images: is the image engine an installer?

A container engine downloads an image whole, runs containers from it and removes the image whole, but the text does not settle whether that engine counts as an installer. The image therefore has two decisions: a package at question 1 or a program at question 2.

- S8.1-4 «Installer—a program of the system whose purpose, according to its documentation, includes installing and removing programs: the system package manager, package managers of programming languages and of application packages.»
- S8.1-6 «Package—what an installer installs and removes as a whole; in a system that is installed and updated as an image, the image is a package.»
- S8.2-7 «Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?»
- S8.2-9 «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»
- S8.2-22 «A program that runs as its own process on the computer, including in a container, is a program.»
- S8.2-16 «What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.»

| Reading / decision in the adjudication card | What the declaration records |
| --- | --- |
| Question 1: INSTALLED-OWN | A package line for the image; its unchanged layers and files are covered by that package line. |
| Question 2: PROGRAM-OWN | A code line for the image; that line provides no package coverage for its contents. Both readings require recording the image, but the kind of line and coverage of contents differ. |

The card’s alternative decisions are preserved as written. The parties’ original labels were c1 UNKNOWN and c2 GAP-TWO on all 13 rows; the adjudication states that the installer question remains even with acquisition history known. The c2 answers below separately retain its proposed derived coverage for Talos; they are published answers, not replacements for the card’s alternatives.

| alma | void | gentoo | microos | talos | Total |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0 | 12 | 13 |

| Example id (all affected rows) | Name | c1 | c2 |
| --- | --- | --- | --- |
| d1b-gentoo-f23478e06580c65ea0aab234 | sha256:a7dbc319b1438115a207e11930dc4bb3e643dcb3ec0bdd694bb36cd8fad289ec | UNKNOWN | GAP-TWO |
| d1b-talos-a17c1f63854bee1c87899ea5 | registry.k8s.io/kube-apiserver:v1.37.1 | UNKNOWN | GAP-TWO |
| d1b-talos-a3943a08f9a984711a8f2f6c | registry.k8s.io/kube-apiserver@sha256:e190f914a6cc21cab9268485d1ae7282fdeab1315ac64b668aa42d732fd1061d | UNKNOWN | GAP-TWO |
| d1b-talos-a50f0524d2017d10970b75e0 | registry.k8s.io/kube-controller-manager:v1.37.1 | UNKNOWN | GAP-TWO |
| d1b-talos-fb4c72097532b2a6e5ee7f0d | registry.k8s.io/kube-controller-manager@sha256:d470c1b85aebb466e971c06239cc6a31a4ac337a78600cef80375a79a1be1641 | UNKNOWN | GAP-TWO |
| d1b-talos-e634add8a1918968c654058e | registry.k8s.io/kube-scheduler:v1.37.1 | UNKNOWN | GAP-TWO |
| d1b-talos-368fc0eb6b7bf8eeefa09780 | registry.k8s.io/kube-scheduler@sha256:b6e2474a6c20309f0df1e7337364281fda95c6a0722259ba7f032a1e177d3f29 | UNKNOWN | GAP-TWO |
| d1b-talos-1de301bc31af36a197dad392 | registry.k8s.io/pause:3.10.2 | UNKNOWN | GAP-TWO |
| d1b-talos-bf9ff0c5e4f144ed63716c37 | registry.k8s.io/pause@sha256:f548e0e8e3dc1896ca956272154dde3314e8cc4fde0a57577ee9fa1c63f5baf4 | UNKNOWN | GAP-TWO |
| d1b-talos-765c2ea628f6919041741da8 | sha256:336e72df967a8c1b1a6b2746476baa9ced7ef89f031726ed3f925cfd2727e16a | UNKNOWN | GAP-TWO |
| d1b-talos-b2e3362f68a9561179bc10f4 | sha256:45eb9287e2328469fbc59ec896f82b013cb462514dacf586034b22d1931e4d16 | UNKNOWN | GAP-TWO |
| d1b-talos-54682459121f4a9fb9974687 | sha256:4a83b15d3ecfe0d916b2d0a7991bc2854a629b8097017c2ee1ff65b30ae4c07c | UNKNOWN | GAP-TWO |
| d1b-talos-ce3033b2816e6818ada2774f | sha256:82ae6c548117fbd112a45e1ae093211fdb53dda179b5b6f8f2d881dd463a572a | UNKNOWN | GAP-TWO |

Answers: `D1b/c1/meaning-gentoo.tsv`, `D1b/c1/meaning-talos.tsv` (both header-only), `D1b/c2/meaning-gentoo.tsv`, and `D1b/c2/meaning-talos.tsv`. The following groups exhaust all 13 ids above; c2’s answer and reason are reproduced verbatim.

Objects: `d1b-gentoo-f23478e06580c65ea0aab234`.

| Question / reason | c1 | c2 |
| --- | --- | --- |
| Q1 | Not supplied | yes: own line |
| Q2 | Not supplied | yes |
| Reason | Not supplied | image a person pulled to run a container must be declared under either reading; a container tool can add it to the declaration, so running a container stays allowed |

Objects: `d1b-talos-a17c1f63854bee1c87899ea5`, `d1b-talos-a3943a08f9a984711a8f2f6c`, `d1b-talos-a50f0524d2017d10970b75e0`, `d1b-talos-fb4c72097532b2a6e5ee7f0d`, `d1b-talos-e634add8a1918968c654058e`, `d1b-talos-368fc0eb6b7bf8eeefa09780`, `d1b-talos-765c2ea628f6919041741da8`, `d1b-talos-b2e3362f68a9561179bc10f4`, `d1b-talos-ce3033b2816e6818ada2774f`.

| Question / reason | c1 | c2 |
| --- | --- | --- |
| Q1 | Not supplied | yes: covered by the control-plane configuration line from which the system obtained it |
| Q2 | Not supplied | yes |
| Reason | Not supplied | The system obtains it itself from the control-plane configuration; an installer recording pulled images in the declaration does not forbid running a container. |

Objects: `d1b-talos-1de301bc31af36a197dad392`, `d1b-talos-bf9ff0c5e4f144ed63716c37`, `d1b-talos-54682459121f4a9fb9974687`.

| Question / reason | c1 | c2 |
| --- | --- | --- |
| Q1 | Not supplied | yes: covered by the line of the Talos image, whose containerd default sandbox image the system pulled |
| Q2 | Not supplied | yes |
| Reason | Not supplied | The system obtains it itself from a built-in default of a recorded package; recording pulled images in the declaration does not forbid running a container. |

### Gap 2. A stored archive of code that nothing executes as it is

An archive contains code that can run on the computer, but no program executes the archive itself: programs only store or unpack it. The text does not settle whether the archive itself counts as executable code at question 2 or as a cache or downloaded material at question 4.

- S8.2-6 «What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order.»
- S8.2-9 «Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?»
- S8.2-10 «Then it is a program, whoever wrote it and wherever it came from; a program belongs to what is installed.»
- S8.2-15 «Otherwise: if a program recorded the object as it ran, it is a program record—a log, cache, history, working state; if a person created or brought the object, it is material—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines.»
- S8.2-23 «A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code.»
- S8.2-1 «Everything that is installed and every setting must be recorded.»
- S8.2-2 «The rest need not be recorded.»
- S8.2-16 «What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package.»

| Reading / decision in the adjudication card | What differs in the declaration |
| --- | --- |
| Question 2: PROGRAM | The archive belongs to what is installed and must have a line of its own or a line from which the system obtained it. |
| Question 4: RECORD or MATERIAL | A program’s cache or a person’s downloaded material need not be recorded; the declaration may omit it. |

| alma | void | gentoo | microos | talos | Total |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 23 | 0 | 0 | 24 |

All 24 affected inventory rows are listed below, including the adjudication’s member-level explanation. A store or directory can have otherwise resolved members alongside the archive gap; the GAP verdict on the whole inventory row stands. In particular, the Gentoo container store has matching MIXED labels, but its GAP verdict is retained.

| Example id (all affected rows) | Name | c1 | c2 | Archive/member identified by adjudication |
| --- | --- | --- | --- | --- |
| d1b-gentoo-c303bfa08eaf41759cb7b68b | /var/lib/containerd | MIXED | MIXED | Layer blob 68fe9bff (busybox tar+gzip, registry manifest): archive-of-code gap; snapshot 1 busybox ELF: PROGRAM-OWN; snapshot 2, databases, uuid: RECORD; .keep: package file. |
| d1b-gentoo-a24a1afb129438e4f35877b6 | /home/user/.cache/pip/http-v2/0/e/6/9/9 | MIXED | RECORD | Body sha256 equals PyPI file mozsystemmonitor-1.0.1-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-921ab470fae1e8cda098a3f9 | /home/user/.cache/pip/http-v2/1/3/8/4/e | MIXED | RECORD | Body sha256 equals PyPI file jinxed-2.1.1-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-ed731cb35dde90d690d1a36d | /home/user/.cache/pip/http-v2/1/b/2/b/c | MIXED | RECORD | Body sha256 equals PyPI file mozfile-3.0.0-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-ad430b0e40c6598dfabc0c7a | /home/user/.cache/pip/http-v2/3/0/9/6/6 | MIXED | RECORD | Body sha256 equals PyPI file distro-1.9.0-py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-da3e7e6876b12be4334bb664 | /home/user/.cache/pip/http-v2/4/0/0/d/b | MIXED | RECORD | Body sha256 equals PyPI file six-1.17.0-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-42bf344cdf5b59bdfa2b3628 | /home/user/.cache/pip/http-v2/4/3/3/f/c | MIXED | RECORD | Body sha256 equals PyPI file mozdevice-4.3.0-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-d5b2438fa52b9dfd988169e4 | /home/user/.cache/pip/http-v2/5/c/5/4/9 | MIXED | RECORD | Body sha256 equals PyPI file mozprocess-1.4.0-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-5ac0eff595ce87e7dfe6758e | /home/user/.cache/pip/http-v2/6/f/5/8/3 | MIXED | RECORD | Body sha256 equals PyPI file setuptools-84.2.1-py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-d2266c02251d6ae8b474df5d | /home/user/.cache/pip/http-v2/7/a/a/5/8 | MIXED | RECORD | Body sha256 equals PyPI file wcwidth-0.9.5-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-cc202aa713e48384198883e7 | /home/user/.cache/pip/http-v2/9/8/f/8/d | MIXED | RECORD | Body sha256 equals PyPI file mozinfo-1.2.3-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-16f595323c4eeca610dcb101 | /home/user/.cache/pip/http-v2/a/1/d/8/d | MIXED | RECORD | Body sha256 equals PyPI file blessed-1.53.0-py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-44108c7746b93d50a56171c1 | /home/user/.cache/pip/http-v2/a/9/b/b/0 | MIXED | RECORD | Body sha256 equals PyPI file mozlog-8.1.0-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-2d00df66cca725b39281bc5a | /home/user/.cache/pip/http-v2/b/3/3/1/0 | MIXED | RECORD | Body sha256 equals PyPI file cowsay-6.1-py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-733705351271d9cca4e9ccc7 | /home/user/.cache/pip/http-v2/b/5/0/1/6 | MIXED | RECORD | Body sha256 equals PyPI file psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-44cbfcf5493841c61b3d2c5f | /home/user/.cache/pip/http-v2/b/7/7/0/d | MIXED | RECORD | Body sha256 equals PyPI file mozprofile-3.0.0.tar.gz (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-25e272c8d45e3a071fd81ab7 | /home/user/.cache/pip/http-v2/c/1/b/4/7 | MIXED | RECORD | Body sha256 equals PyPI file mozterm-1.0.0-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-0b4e0862363bb1a427a11316 | /home/user/.cache/pip/http-v2/d/3/b/a/7 | MIXED | RECORD | Body sha256 equals PyPI file mozversion-2.4.0-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-214917654452c16f0c398112 | /home/user/.cache/pip/http-v2/e/f/b/1/7 | MIXED | RECORD | Body sha256 equals PyPI file marionette_driver-3.7.1-py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-7433e84c2536a9f7f3a56ab0 | /home/user/.cache/pip/http-v2/f/5/9/6/b | MIXED | RECORD | Body sha256 equals PyPI file mozrunner-8.4.0-py2.py3-none-any.whl (archive of Python code): archive-of-code gap; metadata member: RECORD, pip cache. |
| d1b-gentoo-2546496f6d830f0509d2db6c | /home/user/.cache/pip/wheels/40/8f/0b/d808189c2e26aa4a5f606f2921820952459398a6f69f10925d | MIXED | RECORD | mozprofile-3.0.0 wheel pip built (sha256 equals log line "Created wheel", full-digests.tsv): archive-of-code gap; origin.json: RECORD. |
| d1b-gentoo-d366c590629c496123b00a73 | /home/user/Downloads | UNKNOWN | MATERIAL | clearurls.xpi (downloaded extension archive of code): archive-of-code gap; clearurls-source.json written by the person's script: MATERIAL. |
| d1b-gentoo-b92d06df7c2cb763db610d04 | /var/cache/distfiles | MIXED | RECORD | Source and binary archives (go-bootstrap linux-amd64, rust x86_64 binaries, Python sdists): archive-of-code gap; .layout.conf, .mirror-cache.json: RECORD. |
| d1b-void-0c614b583829bd40eb38d058 | /var/lib/docker | UNKNOWN | MIXED | Layer blob 68fe9bff (busybox tar+gzip): archive-of-code gap; snapshot ELF: PROGRAM-OWN; container config: SETTING-OWN; logs, databases, generated files: RECORD. |

Answers: the corresponding ids are absent from both parties’ `meaning-gentoo.tsv` and `meaning-void.tsv`. All c1 `meaning-*.tsv` files, including both Gentoo part files, are header-only. c2’s other answers must not be borrowed for these objects.

| Question / reason | c1 (all 24 objects) | c2 (all 24 objects) |
| --- | --- | --- |
| Q1 | Not supplied | Not supplied |
| Q2 | Not supplied | Not supplied |
| Reason | Not supplied | Not supplied |

Across the supplied answer files, c2 has 7,437 Gentoo rows, 12 Talos rows and one Void row; its AlmaLinux and MicroOS files are header-only. Only the 13 card-1 ids intersect the final GAP ids. The remaining 7,436 Gentoo answers and the one Void answer belong to objects not adjudicated GAP, and are not counted as extra gaps or as answers to card 2. The task’s request for both parties’ answers therefore has an input omission: 37 c1 answer rows and 24 c2 answer rows for adjudicated gaps are absent. This compilation records the absence and supplies no answer on either party’s behalf.

## Comparison with the committed expected result

The three clauses below are copied from the “Expected result, written before the work” paragraph of `SUP1/step-4.md`. The expectation is not an outcome threshold and is not adjusted after seeing the results.

| Committed expectation, clause by clause | Met or not met | Evidence and limit |
| --- | --- | --- |
| an inventory of Gentoo will be obtained | Met | `D1b/in/READY.md`: 32,775 delivered Gentoo objects, 1,210 at level one and 31,565 at level two; all assessed here. Coverage remains partial as reported above. |
| at least half of the 937 objects will receive a decision once their fact is known | Met | MicroOS alone provides 710 resolved matched rows out of its 754 members of the original 937 (747 matched, 37 still UNKNOWN, 7 unmatched). Thus at least 710/937 = 75.77% have a resolved decision, already exceeding the required 469, without counting any of the additional 1,069 Void objects or the extra AlmaLinux object. Sources: `SUP1/step-4.md`, `D1b/in/match/matched-microos.tsv`, `D1b/compare/joined.tsv`, `D1b/adjudication/rows.tsv`. This is a sufficient lower bound, not a claim that exactly 710 of all 937 resolved. |
| at least one kind of object not met in the first night — among what a system that builds its programs from source leaves on the disk — will receive two decisions or none | Not met as a demonstrated full claim | The two-decisions part is observed: card 2 includes Gentoo’s Portage source/bootstrap/binary download cache `/var/cache/distfiles` (`d1b-gentoo-b92d06df7c2cb763db610d04`) and its locally built mozprofile wheel (`d1b-gentoo-2546496f6d830f0509d2db6c`). But the supplied sources establish the first Gentoo inventory, not that the archive-of-code kind was absent from every first-night inventory. Novelty of the kind is not established here; a new machine or object id is not evidence of a previously unseen kind. This evidential limit does not change any GAP verdict or outcome. |

## Questions for the author

1. Does downloading and removing container images make Docker or containerd an installer in the sense of S8.1-4? If so the image is a package; if not the other decision in card 1 treats it as a program, with different coverage of its contents.
2. Is an archive that only stores executable code itself code that the computer can execute under S8.2-9? Card 2 records the choice between mandatory program recording and optional recording of a cache or downloaded material; the question order does not choose between those readings.
3. Does a second level count as obtained when only part was inventoried, or only when the whole level was obtained? These are readings A and B in `check-inputs-v4/QUESTIONS.md`; both outcomes are reported and neither reading is selected as the author’s answer.
4. Should these gaps be put into the two lists required by Supplement 1, and should the missing answers first be obtained from the parties? As `SUP1/step-4.md` requires, neither gap is assigned to either list; the missing c1 and c2 answers are shown above.

## First-night objects without a match

These are the exact `first_id` values in (not published: record outside selected evidence) (the rows for that machine in (not published: record outside selected evidence); the nested files also contain the other machines’ unmatched input ids). None receives a decision in this step. Matching records identify 1,933 matched first-night objects and 74 unmatched out of the committed 2,007.

### alma: 66 unmatched

| First-night id | Name | Recorded match status |
| --- | --- | --- |
| alma-0775bdced8f5e336e1899de5 | /home/user/.local/lib/node_modules/cowsay/node_modules/emoji-regex | no-candidate |
| alma-0992221176232280ccdcc0b9 | /home/user/.local/lib/node_modules/cowsay/node_modules/p-locate | no-candidate |
| alma-0c99474b7568b9110f088ac0 | /home/user/.local/share/flatpak | no-candidate |
| alma-0dfae747e06c5824e8c27deb | /home/user/.local/lib/node_modules/cowsay/node_modules/color-convert | no-candidate |
| alma-1270e6e8c836b299ab4094f3 | /home/user/.local/lib/node_modules/cowsay/node_modules/ansi-regex | no-candidate |
| alma-15147e7885ba0fa16cd90853 | rpmdb-rebuild.service | no-candidate |
| alma-158635226420b9a1ec41f618 | /home/user/.local/lib/node_modules/cowsay/node_modules/find-up | no-candidate |
| alma-1c92207b67b0c7ebbce8f988 | /home/user/.local/lib/node_modules/cowsay/node_modules/yargs | no-candidate |
| alma-2378d6f274fb58e64d1821e4 | /home/user/.local/lib/node_modules/cowsay/node_modules/locate-path | no-candidate |
| alma-2692e186951aa3010b5e5bf6 | /home/user/.local/lib/node_modules/cowsay/node_modules/yargs/node_modules/ansi-regex | no-candidate |
| alma-333afdbdbc9a48e0c6d1708e | /home/user/.local/lib/node_modules/cowsay/node_modules/which-module | no-candidate |
| alma-377dda98f5174997e505b29e | /home/user/.local/lib/node_modules/cowsay/node_modules/strip-final-newline | no-candidate |
| alma-37e64d66a42b19ce6becc67d | /home/user/.local/lib/node_modules/cowsay/node_modules/yargs/node_modules/strip-ansi | no-candidate |
| alma-37fe49b20f1540f9b29bd9cd | /home/user/.local/lib/node_modules/cowsay/node_modules/emoji-regex/es2015 | no-candidate |
| alma-3e7e56118eb7c2717607f633 | /home/user/.local/lib/node_modules/cowsay/node_modules/p-try | no-candidate |
| alma-45c2eda7aec0104a163bbc43 | /home/user/.local/lib/node_modules/cowsay/node_modules/wrap-ansi/node_modules/strip-ansi | no-candidate |
| alma-47ca636a891ff9c67eec35fd | /home/user/.local/lib/node_modules/cowsay/node_modules/cliui/node_modules/string-width | no-candidate |
| alma-514d98f76b08abf8d7841b6e | /etc/NetworkManager/system-connections/ens3.nmconnection | no-candidate |
| alma-5451c1a600f09bd58868c590 | /home/user/.local/lib/node_modules/cowsay/build | no-candidate |
| alma-54ed698dbfa0fda9b8ea59df | /home/user/.local/lib/node_modules/cowsay/node_modules/wrap-ansi/node_modules/string-width | no-candidate |
| alma-5979198b1523e9e8195df68e | rpmdb-migrate.service | no-candidate |
| alma-5bafee22bc69b6fb7e9b4c37 | /boot/loader/entries | no-candidate |
| alma-61c67b50804440435a6bc944 | rpm:gpg-pubkey@c2a1e572-668fe8ef.(none) | no-candidate |
| alma-6417296a51f56e3cd1211479 | /var/lib/selinux/targeted/active | no-candidate |
| alma-642d8bf8a1aa6fa3d5888a6c | /home/user/.local/lib/node_modules/cowsay/node_modules/cliui/node_modules/is-fullwidth-code-point | no-candidate |
| alma-6691ba0f4bbca15e1f342cbb | /home/user/.local/lib/node_modules/cowsay/node_modules/is-fullwidth-code-point | no-candidate |
| alma-692bae3e82cf4ace35cbce54 | /etc/NetworkManager/system-connections | no-candidate |
| alma-75895161584b9b74153015d4 | /home/user/.local/lib/node_modules/cowsay/node_modules/yargs/locales | no-candidate |
| alma-79608afad4f605639b600ea2 | /home/user/.local/lib/node_modules/cowsay/node_modules/wrap-ansi/index.js | no-candidate |
| alma-7b4695c1bfab97c08acbf770 | /home/user/.local/lib/node_modules/cowsay/node_modules/get-caller-file | no-candidate |
| alma-7c249b4e85c8b62b8d4190ea | /home/user/.local/lib/node_modules/cowsay/node_modules/ansi-styles | no-candidate |
| alma-7ca071d35467ab8f64e2a5d7 | /home/user/.local/lib/node_modules/cowsay/node_modules/cliui/node_modules/strip-ansi | no-candidate |
| alma-88fd59e42e3ab26eeba64167 | /home/user/.local/lib/node_modules/cowsay/node_modules/yargs-parser/lib | no-candidate |
| alma-894535cc1ce55c243421555b | /etc/kernel | no-candidate |
| alma-89a3c5f249697f9f1ac2abcc | /home/user/.local/lib/node_modules/cowsay/node_modules/get-stdin | no-candidate |
| alma-930b9792c746a9bafad93f57 | /home/user/.local/lib/node_modules/cowsay/cli.js | no-candidate |
| alma-949842d9eda0bd8dd6461c9d | /home/user/.local/lib/node_modules/cowsay/node_modules/color-name | no-candidate |
| alma-9dfea5a57bc86f405e3ae0c3 | /home/user/.local/lib/node_modules/cowsay/node_modules/p-limit | no-candidate |
| alma-9e19a4736dd6e6f38c7196ed | /home/user/.local/lib/node_modules/cowsay/node_modules/set-blocking | no-candidate |
| alma-9fb5386f2fe6a4a2a188166a | /var/lib/containers/storage | no-candidate |
| alma-a1172fe717274bcb3a77b0f1 | /home/user/.local/lib/node_modules/cowsay/node_modules/camelcase | no-candidate |
| alma-a1c5c6d8831220ffd972ccaa | /home/user/.local/lib/node_modules/cowsay/node_modules/y18n | no-candidate |
| alma-a1fce78f8bf1996a3571087b | /home/user/.local/lib/node_modules/cowsay/node_modules/path-exists | no-candidate |
| alma-a21b5980f2d69a44b6509823 | /home/user/.local/lib/node_modules/cowsay/node_modules/cliui | no-candidate |
| alma-ad9fb12eeb027086dae92d57 | /boot/grub2 | no-candidate |
| alma-af27daed7a703d9138e44c5a | /home/user/.local/lib/node_modules/cowsay | no-candidate |
| alma-b548a7ed608da24a4e5d58d1 | /home/user/.local/lib/node_modules/cowsay/node_modules/wrap-ansi/node_modules/is-fullwidth-code-point | no-candidate |
| alma-babf6a10543af22e535e0c4e | /etc/sysconfig | no-candidate |
| alma-bb5cfd1cad56acbe5768e45f | /home/user/.local/lib/node_modules/cowsay/node_modules/yargs/node_modules/is-fullwidth-code-point | no-candidate |
| alma-bde72c953d9e249b906620c5 | /home/user/.local/lib/node_modules/cowsay/node_modules/require-directory | no-candidate |
| alma-c299a482078fc5b7cb4b8229 | /home/user/.local/lib/node_modules/cowsay/cows | no-candidate |
| alma-c2ca5831f857c8ba99cdfc0e | ens3:<REDACTED>:802-3-ethernet:ens3 | no-candidate |
| alma-c3d63fb0d3d8e06ed8a8e0b5 | /etc/alsa | no-candidate |
| alma-c83f99622553a56e7b5bad36 | /home/user/.local/lib/node_modules/cowsay/node_modules/yargs-parser | no-candidate |
| alma-caff428f8364f0a663721a85 | /etc/dconf/db | no-candidate |
| alma-d30cd481688f21f09a67fed5 | /home/user/.local/lib/node_modules/cowsay/node_modules/strip-ansi | no-candidate |
| alma-da78eefbf5cf48a9769ecc39 | /home/user/.local/lib/node_modules/cowsay/node_modules/yargs/node_modules/string-width | no-candidate |
| alma-dab39645202d97d80dcf72f3 | /etc/firewalld/zones | no-candidate |
| alma-e1590b8c27669a2d935f3869 | /home/user/.local/lib/node_modules/cowsay/node_modules/decamelize | no-candidate |
| alma-e3ac89b4136be2f8fd8390d5 | /home/user/.local/lib/node_modules/cowsay/node_modules/cliui/node_modules/ansi-regex | no-candidate |
| alma-e7f55306c21a5def7ee20b22 | /home/user/.local/lib/node_modules/cowsay/node_modules/wrap-ansi | no-candidate |
| alma-e91f48a4f4dac062b5c8f92e | /home/user/.local/lib/node_modules/cowsay/node_modules/yargs/build/lib | no-candidate |
| alma-f0fd38e1a214fd214a189218 | /home/user/.local/lib/node_modules/cowsay/node_modules/string-width | no-candidate |
| alma-f7ee01c83482561a2cf042b9 | /home/user/.local/lib/node_modules/cowsay/node_modules/require-main-filename | no-candidate |
| alma-f926f4778984e259b5281388 | /home/user/.local/lib/node_modules/cowsay/node_modules/wrap-ansi/node_modules/ansi-regex | no-candidate |
| alma-fdecadc52ade076bcda7a8eb | /home/user/.local/lib/node_modules/cowsay/lib | no-candidate |

### void: 1 unmatched

| First-night id | Name | Recorded match status |
| --- | --- | --- |
| void-5a19bc168ee39041e66bc22a | (ALL | ambiguous-new-key |

### gentoo: 0 unmatched

None.

### microos: 7 unmatched

| First-night id | Name | Recorded match status |
| --- | --- | --- |
| microos-14b49eb5b4dbb9b8e9701af7 | (ALL) | ambiguous-first-night-key |
| microos-2651ae8b3936cafe8ab643b8 | (ALL) | ambiguous-first-night-key |
| microos-58a5bf771842e6e74625f86c | Defaults!/usr/sbin/visudo | ambiguous-first-night-key |
| microos-68691ac08ba5b8bb07517ff3 | secure_path=/usr/local/sbin\\:/usr/local/bin\\:/usr/sbin\\:/usr/bin\\:/sbin\\:/bin, | ambiguous-first-night-key |
| microos-8db6691105c8ac421e0e73b7 | secure_path=/usr/local/sbin\\:/usr/local/bin\\:/usr/sbin\\:/usr/bin\\:/sbin\\:/bin, | ambiguous-first-night-key |
| microos-c2cb0aae2410f18e15023fe3 | (ALL) | ambiguous-first-night-key |
| microos-faa9663df42f9349b7627ba9 | Defaults!/usr/sbin/visudo | ambiguous-first-night-key |

### talos: 0 unmatched

None.

## Mechanical checks

The compilation joins every adjudication row to exactly one assessed object, retains all 30,024 verdicts, checks the matched-id selection for each non-Gentoo machine, and checks that the machine-specific match tables agree with the nested outputs after filtering unmatched rows to their machine. The unknown-by-kind and unknown-by-missing-fact totals both equal 31,205; the gap cards cover all 37 GAP ids exactly once. These are compilation checks, not independent acceptance by RV-S4-H.

Quote validation: `/usr/bin/python3 -I (not published: orchestration or scratch) D1b/RESULT.md` — passed: 14 quotations checked; 0 not found in `TEXT.md`.
