# E6C — Check 1 comparison of the additional E6 systems

**2026-11-19 — Ubuntu: `?`; Alpine: `?`; overall: `?`.** The paired residual classifications are insufficient to establish either success or the fixed failure condition. This is not a claim of agreement: 184 of 262 normalized decisions differ and 199 rows have at least one hole flag. Every differing decision involves a hole flag; none assigns two different affirmative §5 classes. The claimed no-class/two-class cases have unproved premises or unresolved object boundaries, as detailed below. No rule is added and no original classification is overwritten.

## Fixed criterion and its application

`PAPER.html:220`, §9.2, verbatim:

> An object is found on either machine that, under the definitions, belongs to no class or belongs to two classes with different consequences, or the two classifications assign the object to different classes and the text of the definitions does not resolve the disagreement.

The criterion has no agreement or kappa threshold. The observed low agreement therefore does not itself select `0`. Equally, missing provenance must not silently become a proven no-class witness. `E6.md` explicitly defines Classification 1’s `hole-none` as “not established by this first pass”, rather than proof of impossibility. Classification 2’s `hole-two` reasons are claims to audit, not evidence that both defining premises and different consequences hold. The files’ hole labels are measurement categories, not additional classes defined in §5. E6B requested stronger hole meanings (“fits no class” / “fits two classes with different consequences”); identical hole labels therefore need not express the same evidential claim on both sides. The metrics below measure label agreement, not equivalence of those claims.

- **No-class branch:** 15 rows have `hole-none` from both classifiers (Ubuntu 8, Alpine 7); the saved reasons describe unknown image-build provenance or mixed groups, not demonstrated exclusion from every class. All other Classification 1 hole-none rows likewise withhold a decision. No proved no-class witness is established here.
- **Two-class branch:** Classification 2 marks 12 rows hole-two (Ubuntu 7, Alpine 5). The complete audit below checks each. They invoke human input versus a program writer, launching versus creation, or mixed unit constituents. These do not establish both §5 predicates for one object and different consequences. No proved two-class witness is established here.
- **Disagreement branch:** no joined row has different affirmative class assignments (recorded/data/derivative). There are 184 differing decisions involving hole flags, plus 14 same-class owner-string differences; all remain visible. The former do not supply a second affirmative class, and the latter do not establish different classes or lifecycle consequences. Thus this evidence does not demonstrate this failure branch. This is an evidential conclusion, not a new exception to §9.2: a verified unresolvable class disagreement or no-class/two-class object would require `0` immediately, even with high aggregate agreement.
- **Success:** unavailable: unresolved premises, unresolved boundaries and incomplete independent coverage prevent `1`. `?` does not mean the definitions resolve all rows. Eight code rows have a direct class rule conditional on the asserted execution fact; their factual/owner gaps remain. Other retained holes and owner differences are marked **not resolved** below.

## Join, normalization and counts

Inputs are frozen under [E6C-raw/inputs](E6C-raw/inputs/); hashes: [input-sha256.json](E6C-raw/input-sha256.json). The TSV join uses `id`, never row position. Both files contain exactly the same 262 unique residual IDs: Ubuntu 197, Alpine 65. No duplicate, missing or extra residual ID occurs. Source line numbers in the tables include the header as line 1.

Format-only normalization: `recorded (works)` and `recorded` → `recorded`; `derivative of X` and `derivative` → `derivative`, retaining X in the separate owner field. This changes no classification rule and does not certify a package/provisioning proxy as a designated declaration. `hole-none` and `hole-two` remain separate categories. No owner aliases are merged.

Unweighted nominal Cohen’s κ is calculated on the five normalized decision labels, including hole flags: `p_o = matches/N`, `p_e = Σ n_A(c)n_B(c)/N²`, `κ = (p_o−p_e)/(1−p_e)`. Hole agreement is agreement about an unresolved decision, not successful object classification. Statistics describe the supplied residual only, not all objects on either VM.


| System | Paired residual | Matching labels | Agreement | p_e | κ | Different labels | Owner-only differences | Hole union |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ubuntu | 197 | 64 | 32.487310% | 0.170037878 | 0.186556970 | 133 | 10 | 141 |
| alpine | 65 | 14 | 21.538462% | 0.157633136 | 0.068558584 | 51 | 4 | 58 |
| overall | 262 | 78 | 29.770992% | 0.165360410 | 0.158570855 | 184 | 14 | 199 |


Class counts, **residual only** (A = Classification 1; B = Classification 2):


| System / classifier | recorded | derivative | data | hole-none | hole-two |
| --- | --- | --- | --- | --- | --- |
| ubuntu / c1 | 26 | 31 | 1 | 139 | 0 |
| ubuntu / c2 | 25 | 156 | 1 | 8 | 7 |
| alpine / c1 | 2 | 7 | 0 | 56 | 0 |
| alpine / c2 | 18 | 34 | 1 | 7 | 5 |


Sensitivity to representation (not alternative substantive verdicts):


| System | Literal class-string matches / N | Literal κ | Normalized class + exact derivative owner matches / N | Class + owner κ |
| --- | --- | --- | --- | --- |
| ubuntu | 9/197 | 0.017508489 | 54/197 | 0.238456964 |
| alpine | 7/65 | 0.016436212 | 10/65 | 0.054732946 |
| overall | 16/262 | 0.019249205 | 64/262 | 0.194772135 |


Literal mismatches include 62 rows with matching normalized classes (24 recorded, 38 derivative); these are label-format differences, of which 14 also have different owner strings. Both raw labels and both owner strings remain in [E6C-joined.tsv](E6C-joined.tsv), so no raw disagreement is lost. Exact rational statistics and confusion-table-reconstructible counts: [E6C-statistics.json](E6C-statistics.json).

## Text audit of all disagreements and holes

The following exact §5 sentences are relevant. They can settle a class rule while leaving factual premises unverified; this distinction is recorded explicitly for eight code rows below:

- **Q-D**, §5.1: “Declaration—a collection of files that a person has designated as the primary description of the computer.”
- **Q-R**, §5.1: “Running components—users and the rules under which they operate, programs, drivers, and services.”
- **Q-V**, §5.1: “Derivative—an object that a described program has created itself because the object is needed for the program's operation: saved Wi-Fi networks for a network management service, extensions for a browser, a cache, a log.”
- **Q-C**, §5.1: “Code executed within a program is its derivative.”
- **Q-A**, §5.1: “Data—what a person has created: photographs, documents, databases, and their own settings files, such as a text editor configuration.”
- **Q-P3**, §5.2: “Everything that is on the computer and is not recorded in the declaration is either a derivative of a recorded program or the person's data.”
- **Q-P5**, §5.2: “Any derivative and any data can be recorded in the declaration; they then become subject to it on the same terms as everything else recorded.”
- **Q-P6**, §5.2: “A derivative needed by several programs exists as long as at least one of them is present.”

Q-R settles that an account is a running component; it does not designate a declaration. Q-P3 addresses the unrecorded remainder, and Q-P5 allows recording data/derivatives, so an overlap involving “recorded” is not automatically a two-class witness with different consequences. Q-P6 permits shared owners, but does not infer their need from paths. No quote is treated as an observation of a creator’s intent.

### Audit of all 12 alleged two-class witnesses


| ID (A/B source line) | Object | A → B | §5 resolves? / why; open problem |
| --- | --- | --- | --- |
| alpine-96a19ba1e6 (4/4) | census | recorded → hole-two | not resolved — User-data names the account, but its designation as declaration is unproved. Creation for the person does not prove cloud-init needs the account for its own operation; the alleged two-class witness is unproved. [O1; O2; NEW] |
| alpine-d8ee8908a9 (26/26) | ps | recorded → hole-two | not resolved — Launching packaged ps does not establish execution within the shell or two incompatible consequences. Recorded status is a proxy; §5 gives no launch/creation boundary. [O5; O9; NEW] |
| alpine-09d09204d8 (50/50) | /etc/sudoers.d | hole-none → hole-two | not resolved — Human-specified settings and a program writer are alleged; that alone does not prove creation for that writer’s operation or two classes with different consequences. [O1; O2] |
| alpine-c3a3dd6c9b (53/53) | /home/census/.ssh | hole-none → hole-two | not resolved — Human-specified settings and a program writer are alleged; that alone does not prove creation for that writer’s operation or two classes with different consequences. [O1; O2] |
| alpine-351644c1fd (55/55) | /root/.ssh | hole-none → hole-two | not resolved — Human-specified settings and a program writer are alleged; that alone does not prove creation for that writer’s operation or two classes with different consequences. [O1; O2] |
| ubuntu-96a19ba1e6 (70/70) | census | recorded → hole-two | not resolved — User-data names the account, but its designation as declaration is unproved. Creation for the person does not prove cloud-init needs the account for its own operation; the alleged two-class witness is unproved. [O1; O2; NEW] |
| ubuntu-d8ee8908a9 (101/101) | ps | recorded → hole-two | not resolved — Launching packaged ps does not establish execution within the shell or two incompatible consequences. Recorded status is a proxy; §5 gives no launch/creation boundary. [O5; O9; NEW] |
| ubuntu-ea2b617ba5 (130/130) | /etc/hostname | hole-none → hole-two | not resolved — Human-specified settings and a program writer are alleged; that alone does not prove creation for that writer’s operation or two classes with different consequences. [O1; O2] |
| ubuntu-09d09204d8 (177/177) | /etc/sudoers.d | hole-none → hole-two | not resolved — Human-specified settings and a program writer are alleged; that alone does not prove creation for that writer’s operation or two classes with different consequences. [O1; O2] |
| ubuntu-c3a3dd6c9b (192/192) | /home/census/.ssh | hole-none → hole-two | not resolved — Human-specified settings and a program writer are alleged; that alone does not prove creation for that writer’s operation or two classes with different consequences. [O1; O2] |
| ubuntu-351644c1fd (196/196) | /root/.ssh | hole-none → hole-two | not resolved — Human-specified settings and a program writer are alleged; that alone does not prove creation for that writer’s operation or two classes with different consequences. [O1; O2] |
| ubuntu-cbd353d9e3 (253/253) | systemd-networkd-wait-online.service | hole-none → hole-two | not resolved — Packaged fragment and generated drop-in are different constituents. §5 does not classify their composite; two constituent classes do not prove incompatible classes of one object. [O9; NEW] |


Evidence anchors: the two `census` accounts are named in `raw-E6/{ubuntu,alpine}/user-data:4`; the collector invokes ps in `src/collect.sh:23`; Ubuntu’s unit fragment/drop-in are saved in `raw-E6/ubuntu/unit-paths.txt:1346–1349` and `E6-residual.tsv:253`. Human specification or a generated constituent alone does not establish the two competing predicates. Ubuntu’s hostname, sudoers and SSH cases, and Alpine’s sudoers and SSH cases, retain their individual provenance pointers in the full table below and the joined TSV.

For the agreed hole-none account `alpine-c6df412fe9`, B additionally says the requester is off-machine and “not this computer’s person”. §5’s data sentence says “a person”; it supplies no on-machine-authorship requirement. That exclusion cannot be adopted as a rule. Actual authorship and designation still remain unestablished, so neither no-class proof nor a positive data assignment follows.

Additional boundary candidate `alpine-3e7f7f2c59`: `src/day-alpine.sh:13–14` and `raw-E6/alpine/day.log:31–34` show writing `.inputrc` and loading it with `bind -f`; the log reports vi editing mode. Q-A supports data. Whether those settings count as Q-C’s “code” is not defined by §5; §8 O2 explicitly identifies that boundary. A withholds assignment and B chooses data; these are not two observed affirmative assignments. We do not invent either a “settings are never code” rule or a “all interpreted settings are code” rule.

### Direct text rule for the eight code assertions

For each following disagreement, **the class rule is resolved conditional on B’s factual execution premise**, by the exact sentence: “Code executed within a program is its derivative.” No new rule is needed to derive the class on that premise. This is not certification that each asserted file was actually executed, that every grouped member fits, or that B’s exact owner set is correct. Those retained evidence/owner holes prevent a fully verified assignment. In particular, `bash -s` alone does not prove `.bash_logout` was executed. Original classifier labels and pre-adjudication agreement statistics remain unchanged.


| ID / A,B line | Object | B’s execution assertion | §5 text ruling |
| --- | --- | --- | --- |
| alpine-ea05c8eb7f / 44,44 | /etc/profile.d | 50-cloud-init-locale.sh written by cloud-init (cloud-init.log); code run by sh, shared | Derivative if execution premise holds: “Code executed within a program is its derivative.” |
| ubuntu-211f893687 / 127,127 | /etc/grub.d | script executed within grub-mkconfig: code executed within a program (5.1) | Derivative if execution premise holds: “Code executed within a program is its derivative.” |
| ubuntu-3543b3a205 / 154,154 | /etc/profile | copied from /usr/share/base-files/profile; code run by sh | Derivative if execution premise holds: “Code executed within a program is its derivative.” |
| ubuntu-3787beb4db / 187,187 | /home/census/.bash_logout | copied from /etc/skel by useradd, not person-written; code executed within the shell (5.1) | Derivative if execution premise holds: “Code executed within a program is its derivative.” |
| ubuntu-2d36998dd6 / 188,188 | /home/census/.bashrc | copied from /etc/skel by useradd, not person-written; code executed within the shell (5.1) | Derivative if execution premise holds: “Code executed within a program is its derivative.” |
| ubuntu-c15063bcfe / 191,191 | /home/census/.profile | copied from /etc/skel by useradd, not person-written; code executed within the shell (5.1) | Derivative if execution premise holds: “Code executed within a program is its derivative.” |
| ubuntu-90017bfd94 / 194,194 | /root/.bashrc | copied from /usr/share/base-files dot files, not person-written; code executed within the shell | Derivative if execution premise holds: “Code executed within a program is its derivative.” |
| ubuntu-0fbf442b3c / 195,195 | /root/.profile | copied from /usr/share/base-files dot files, not person-written; code executed within the shell | Derivative if execution premise holds: “Code executed within a program is its derivative.” |


Logs/caches and shared owners: Q-V explicitly gives logs and caches as examples; Q-P6 explicitly permits shared need. Consequently lack of a sole owner is not a missing class rule. For `*-d6ce9987c3` (wtmp), `ubuntu-9c96b64591` (btmp), and `ubuntu-698c23461f` (lastlog), the unresolved question is the actual needed-by set and recorded program, not whether several owners are allowed. Likewise the log/cache assertions for `*-293699acd1`, `ubuntu-626ab0ebaf`, and `ubuntu-382c94b98b` have textual derivative support; their asserted provenance/need is not established by the example sentence alone. These distinctions do not turn a filename or a claimant’s reason into a verified observation.

### Complete residual-hole list (199 rows)

This is the union of both classifiers’ original hole flags: 141 Ubuntu, 58 Alpine. It includes all 184 differing normalized labels and the 15 matching hole-none decisions. A/B labels use `R`=recorded, `V`=derivative, `D`=data, `H0`=hole-none, `H2`=hole-two. Rows are linked by ID and exact residual/A/B source line; full verbatim reasons and evidence pointers are in [E6C-holes.tsv](E6C-holes.tsv). The eight CODE rows have the conditional class ruling above, retaining factual/owner holes; the other 191 rows are **not resolved**. No original hole flag is silently removed by an inferred rule. The code column refers to the explicit reason below, and the row retains B’s particular claim. `NEW` is a gap not named by O1–O9, not a newly adopted rule: declaration/proxy identification, observation composition/identity, or evidence/procedure coverage. O-tags are diagnostic mappings only; they are not decisions on open problems.


| Reason code | O1–O9 or NEW | Why §5 alone does not resolve |
| --- | --- | --- |
| DECL | NEW | Package membership/provisioning is a proxy; §5 requires personal designation of the primary description. Text alone cannot establish that historical fact. |
| ACCT | O1; NEW | An account is a running component, but package scripts or package membership alone do not establish both declaration designation and the creator’s operational need. |
| BOOT | O1; O9 | Boot artifact creation, later consumption and running-component granularity are not settled by the path or a generating-tool attribution. |
| COMP | O1; O9; NEW | The observed service/configuration can describe what runs or be generated state; §5 supplies no composition or designation test for this observation. |
| GRAN | O9; NEW | Kernel/manager runtime representation versus separately classified component is not determined at this observation’s granularity. |
| GROUP | O1; O2; NEW | The row combines members with potentially different authors, purposes or classes; no group-composition rule is stated. |
| CREATOR | O1; O2 | Observed writer, later consumer and human-supplied settings do not establish a unique derivative/data assignment for every member. |
| SHARED | O1 | P6 permits shared need, but does not establish the actual needed-by owner set from a log filename or writer list. |
| REFERENCE | O9; NEW | An absent-unit reference does not fix whether the object is a name, source dependency or manager state. |
| EVIDENCE | O1; O2; NEW | Saved path/type and an asserted writer do not establish all §5 premises: creation, operational need, personal authorship and declaration designation. |
| CENSUS | O1; O2; NEW | User-data names the account, but its designation as declaration is unproved. Creation for the person does not prove cloud-init needs the account for its own operation; the alleged two-class witness is unproved. |
| PS | O5; O9; NEW | Launching packaged ps does not establish execution within the shell or two incompatible consequences. Recorded status is a proxy; §5 gives no launch/creation boundary. |
| INPUTRC | O2 | Human authorship and consumption are observed. Data wording supports B, but §5 does not decide whether interpreting these setting commands is code executed within a program; no contrary derivative assignment is demonstrated. |
| TWO | O1; O2 | Human-specified settings and a program writer are alleged; that alone does not prove creation for that writer’s operation or two classes with different consequences. |
| UNIT | O9; NEW | Packaged fragment and generated drop-in are different constituents. §5 does not classify their composite; two constituent classes do not prove incompatible classes of one object. |
| CODE | O1; NEW | The text settles the derivative class if B’s within-program execution premise is true. Actual execution of every member and the exact owner are not established merely by that assertion; these are evidence/owner gaps, not a missing code-class rule. |


#### ubuntu


| Residual / A / B line | ID | Object | A → B | Why code; O / NEW | B’s specific claim (unverified where disputed) |
| --- | --- | --- | --- | --- | --- |
| 70/70/70 | ubuntu-96a19ba1e6 | census | R → H2 | CENSUS; O1; O2; NEW | person-specified user (user-data) created by cloud-init useradd: data vs derivative (O2); a user also falls under P1 |
| 72/72/72 | ubuntu-27d89cb149 | dhcpcd | H0 → V | ACCT; O1; NEW | not in any package-owned definition nor cloud-init; system user of installed dhcpcd-base (script not saved); P1 tension |
| 76/76/76 | ubuntu-6f28118711 | landscape | H0 → V | ACCT; O1; NEW | not in any package-owned definition nor cloud-init; system user of installed landscape-common (script not saved); P1 tension |
| 85/85/85 | ubuntu-8ea6eb1441 | pollinate | H0 → V | ACCT; O1; NEW | not in any package-owned definition nor cloud-init; system user of installed pollinate (script not saved); P1 tension |
| 88/88/88 | ubuntu-dbea3590f8 | sshd | H0 → V | ACCT; O1; NEW | not in any package-owned definition nor cloud-init; system user of installed openssh-server (script not saved); P1 tension |
| 91/91/91 | ubuntu-48ebc93776 | syslog | H0 → V | ACCT; O1; NEW | not in any package-owned definition nor cloud-init; system user of installed rsyslog (script not saved); P1 tension |
| 95/95/95 | ubuntu-0b2fc8af1f | tcpdump | H0 → V | ACCT; O1; NEW | not in any package-owned definition nor cloud-init; system user of installed tcpdump (script not saved); P1 tension |
| 96/96/96 | ubuntu-cff9eec648 | tss | H0 → V | ACCT; O1; NEW | not in any package-owned definition nor cloud-init; system user of installed tpm-udev (script not saved); P1 tension |
| 98/98/98 | ubuntu-a0ea4d1be3 | uuidd | H0 → V | ACCT; O1; NEW | not in any package-owned definition nor cloud-init; system user of installed uuid-runtime (script not saved); P1 tension |
| 100/100/100 | ubuntu-89ce5c5668 | kernel threads | H0 → R | GRAN; O9; NEW | the recorded kernel (linux-image-6.8.0-147-generic) running its own code |
| 101/101/101 | ubuntu-d8ee8908a9 | ps | R → H2 | PS; O5; O9; NEW | recorded program launched by the collector shell: recorded vs derivative of launcher, O5 left open |
| 102/102/102 | ubuntu-5bf2e2415a | /boot/efi | H0 → V | BOOT; O1; O9 | EFI loaders installed by grub-install/shim; code run at boot |
| 103/103/103 | ubuntu-76634f69cd | /boot/grub | H0 → V | BOOT; O1; O9 | modules, fonts, grub.cfg, grubenv generated by grub-install/update-grub |
| 104/104/104 | ubuntu-6759ca6559 | /boot/initrd.img | H0 → V | BOOT; O1; O9 | symlink made by linux-update-symlinks on kernel install |
| 105/105/105 | ubuntu-b22d4fd11a | /boot/initrd.img-6.8.0-147-generic | H0 → V | BOOT; O1; O9 | generated by update-initramfs; code run at boot (P1 tension) |
| 106/106/106 | ubuntu-184ea03842 | /boot/initrd.img.old | H0 → V | BOOT; O1; O9 | symlink made by linux-update-symlinks on kernel install |
| 107/107/107 | ubuntu-28ea033f07 | /boot/vmlinuz | H0 → V | BOOT; O1; O9 | symlink made by linux-update-symlinks on kernel install |
| 108/108/108 | ubuntu-93fe6af096 | /boot/vmlinuz.old | H0 → V | BOOT; O1; O9 | symlink made by linux-update-symlinks on kernel install |
| 109/109/109 | ubuntu-fefd90f542 | /etc/.pwd.lock | H0 → V | EVIDENCE; O1; O2; NEW | lock file of the shadow tools |
| 110/110/110 | ubuntu-917d8d1269 | /etc/.resolv.conf.systemd-resolved.bak | H0 → V | EVIDENCE; O1; O2; NEW | backup made by systemd-resolved install |
| 111/111/111 | ubuntu-5932b79e41 | /etc/.updated | H0 → V | EVIDENCE; O1; O2; NEW | stamp of systemd-update-done |
| 112/112/112 | ubuntu-809cb439ce | /etc/alternatives | H0 → V | EVIDENCE; O1; O2; NEW | update-alternatives links set by package scripts; select which binary runs |
| 113/113/113 | ubuntu-384e8d981f | /etc/apparmor.d | H0 → V | EVIDENCE; O1; O2; NEW | local/ stubs and tunables made by dh_apparmor postinst snippets |
| 114/114/114 | ubuntu-ce45570012 | /etc/apt | H0 → V | EVIDENCE; O1; O2; NEW | ubuntu.sources by cloud-init (log), auto-upgrades files via ucf (ucf cache); sources.list writer not in evidence |
| 115/115/115 | ubuntu-9cf6463675 | /etc/ca-certificates.conf | H0 → V | EVIDENCE; O1; O2; NEW | generated by ca-certificates postinst |
| 116/116/116 | ubuntu-0326839754 | /etc/ca-certificates.conf.dpkg-old | H0 → V | EVIDENCE; O1; O2; NEW | old copy kept during config update |
| 117/117/117 | ubuntu-34803cf70a | /etc/cloud | H0 → H0 | GROUP; O1; O2; NEW | build.info written by image build, no recorded writer (90_dpkg.cfg is cloud-init debconf) |
| 118/118/118 | ubuntu-2a3c514663 | /etc/console-setup | H0 → V | EVIDENCE; O1; O2; NEW | cached fonts/keymaps written by setupcon |
| 119/119/119 | ubuntu-f3d3ee3907 | /etc/crypttab | H0 → V | EVIDENCE; O1; O2; NEW | created by cryptsetup install when missing |
| 120/120/120 | ubuntu-228a030233 | /etc/default | H0 → V | EVIDENCE; O1; O2; NEW | package-generated defaults (grub, sysstat via ucf cache); grub.d cfg is code sourced by grub-mkconfig |
| 121/121/121 | ubuntu-7740cdd4af | /etc/dpkg | H0 → V | EVIDENCE; O1; O2; NEW | origins/default link made by base-files postinst |
| 122/122/122 | ubuntu-9e9990f42c | /etc/ec2_version | H0 → H0 | EVIDENCE; O1; O2; NEW | version stamp written by image build; no recorded writer |
| 123/123/123 | ubuntu-5deb3892cc | /etc/environment | H0 → H0 | EVIDENCE; O1; O2; NEW | no package owns it, no saved script or cloud-init log writes it |
| 124/124/124 | ubuntu-4cce813fe8 | /etc/fstab | H0 → H0 | EVIDENCE; O1; O2; NEW | written by image build (cloudimg-rootfs label); no recorded writer; drives mounts |
| 125/125/125 | ubuntu-a763d184b3 | /etc/group | H0 → V | EVIDENCE; O1; O2; NEW | account database the shadow tools keep; census line saved like a Wi-Fi network (5.1) |
| 126/126/126 | ubuntu-d3bb1c2fce | /etc/group- | H0 → V | EVIDENCE; O1; O2; NEW | backup the shadow tools write when editing the database |
| 127/127/127 | ubuntu-211f893687 | /etc/grub.d | H0 → V | CODE; O1; NEW | script executed within grub-mkconfig: code executed within a program (5.1) |
| 128/128/128 | ubuntu-2adfd50853 | /etc/gshadow | H0 → V | EVIDENCE; O1; O2; NEW | account database the shadow tools keep; census line saved like a Wi-Fi network (5.1) |
| 129/129/129 | ubuntu-42b0af3cd4 | /etc/gshadow- | H0 → V | EVIDENCE; O1; O2; NEW | backup the shadow tools write when editing the database |
| 130/130/130 | ubuntu-ea2b617ba5 | /etc/hostname | H0 → H2 | TWO; O1; O2 | person-specified hostname (user-data) written by cloud-init for the system: data vs derivative (O2) |
| 131/131/131 | ubuntu-5cad41b508 | /etc/hosts | H0 → H0 | EVIDENCE; O1; O2; NEW | no package owns it, cloud-init did not write it (log): image build |
| 132/132/132 | ubuntu-d47133480a | /etc/hosts.allow | H0 → V | EVIDENCE; O1; O2; NEW | created by libwrap0 install when missing |
| 133/133/133 | ubuntu-b8a8c42f35 | /etc/hosts.deny | H0 → V | EVIDENCE; O1; O2; NEW | created by libwrap0 install when missing |
| 134/134/134 | ubuntu-f3f8b50a94 | /etc/initramfs-tools | H0 → V | EVIDENCE; O1; O2; NEW | modules copied from /usr/share/initramfs-tools/modules by postinst |
| 135/135/135 | ubuntu-413e0b552f | /etc/inputrc | H0 → V | EVIDENCE; O1; O2; NEW | copied from /usr/share/readline/inputrc by postinst |
| 136/136/136 | ubuntu-9da5575867 | /etc/iscsi | H0 → V | EVIDENCE; O1; O2; NEW | initiatorname generated by open-iscsi |
| 138/138/138 | ubuntu-d59101ffe2 | /etc/locale.conf | H0 → H0 | EVIDENCE; O1; O2; NEW | no package owns it, no saved script or cloud-init log writes it |
| 139/139/139 | ubuntu-cf102b2bab | /etc/locale.gen | H0 → V | EVIDENCE; O1; O2; NEW | generated by locales configuration |
| 140/140/140 | ubuntu-966442e2a8 | /etc/localtime | H0 → V | EVIDENCE; O1; O2; NEW | link set by tzdata configuration |
| 141/141/141 | ubuntu-1809ee6527 | /etc/machine-id | H0 → V | EVIDENCE; O1; O2; NEW | generated by systemd-machine-id-setup |
| 142/142/142 | ubuntu-6245454f68 | /etc/mdadm | H0 → V | EVIDENCE; O1; O2; NEW | mdadm.conf generated by mdadm postinst (mkconf) |
| 143/143/143 | ubuntu-9e65e302c3 | /etc/modules | H0 → V | EVIDENCE; O1; O2; NEW | created by kmod install when missing |
| 144/144/144 | ubuntu-6b4026dd02 | /etc/mtab | H0 → V | EVIDENCE; O1; O2; NEW | link to /proc/self/mounts made by systemd-tmpfiles |
| 145/145/145 | ubuntu-966a04ec60 | /etc/multipath | H0 → V | EVIDENCE; O1; O2; NEW | bindings file written by multipathd |
| 146/146/146 | ubuntu-bbe4c8f871 | /etc/netplan | H0 → V | EVIDENCE; O1; O2; NEW | 50-cloud-init.yaml rendered by cloud-init from datasource network config |
| 147/147/147 | ubuntu-6f021dad80 | /etc/networks | H0 → V | EVIDENCE; O1; O2; NEW | copied from /usr/share/base-files/networks by postinst |
| 148/148/148 | ubuntu-a8d7f506ac | /etc/newt | H0 → V | EVIDENCE; O1; O2; NEW | update-alternatives link |
| 149/149/149 | ubuntu-5f65179c45 | /etc/nsswitch.conf | H0 → V | EVIDENCE; O1; O2; NEW | installed by base-files postinst |
| 150/150/150 | ubuntu-361c854675 | /etc/overlayroot.local.conf | H0 → H0 | EVIDENCE; O1; O2; NEW | not in overlayroot package (only overlayroot.conf), no saved script or cloud-init writes it |
| 151/151/151 | ubuntu-4d882498fa | /etc/pam.d | H0 → V | EVIDENCE; O1; O2; NEW | common-* generated by pam-auth-update |
| 152/152/152 | ubuntu-493d4cfdb1 | /etc/passwd | H0 → V | EVIDENCE; O1; O2; NEW | account database the shadow tools keep; census line saved like a Wi-Fi network (5.1) |
| 153/153/153 | ubuntu-c169edc1ca | /etc/passwd- | H0 → V | EVIDENCE; O1; O2; NEW | backup the shadow tools write when editing the database |
| 154/154/154 | ubuntu-3543b3a205 | /etc/profile | H0 → V | CODE; O1; NEW | copied from /usr/share/base-files/profile; code run by sh |
| 155/155/155 | ubuntu-2dfb100dfa | /etc/python3 | H0 → V | EVIDENCE; O1; O2; NEW | debian_config written by python3 postinst |
| 156/156/156 | ubuntu-5ecd8ad6ee | /etc/rc0.d | H0 → V | EVIDENCE; O1; O2; NEW | update-rc.d links set by package scripts; state what starts (P3 tension) |
| 157/157/157 | ubuntu-2e520cea02 | /etc/rc1.d | H0 → V | EVIDENCE; O1; O2; NEW | update-rc.d links set by package scripts; state what starts (P3 tension) |
| 158/158/158 | ubuntu-31b4602da2 | /etc/rc2.d | H0 → V | EVIDENCE; O1; O2; NEW | update-rc.d links set by package scripts; state what starts (P3 tension) |
| 159/159/159 | ubuntu-78bcc39697 | /etc/rc3.d | H0 → V | EVIDENCE; O1; O2; NEW | update-rc.d links set by package scripts; state what starts (P3 tension) |
| 160/160/160 | ubuntu-8e766b28b8 | /etc/rc4.d | H0 → V | EVIDENCE; O1; O2; NEW | update-rc.d links set by package scripts; state what starts (P3 tension) |
| 161/161/161 | ubuntu-f032939066 | /etc/rc5.d | H0 → V | EVIDENCE; O1; O2; NEW | update-rc.d links set by package scripts; state what starts (P3 tension) |
| 162/162/162 | ubuntu-b1fb6e4c19 | /etc/rc6.d | H0 → V | EVIDENCE; O1; O2; NEW | update-rc.d links set by package scripts; state what starts (P3 tension) |
| 163/163/163 | ubuntu-4311df43fb | /etc/rcS.d | H0 → V | EVIDENCE; O1; O2; NEW | update-rc.d links set by package scripts; state what starts (P3 tension) |
| 164/164/164 | ubuntu-cee61291d2 | /etc/resolv.conf | H0 → V | EVIDENCE; O1; O2; NEW | link to stub-resolv.conf made by systemd-resolved |
| 165/165/165 | ubuntu-d7ce6674a9 | /etc/rsyslog.d | H0 → V | EVIDENCE; O1; O2; NEW | 50-default.conf via ucf (ucf cache) |
| 166/166/166 | ubuntu-84b24ebf2a | /etc/security | H0 → V | EVIDENCE; O1; O2; NEW | opasswd password-history store of pam_unix/pam_pwhistory |
| 167/167/167 | ubuntu-20302e112e | /etc/sgml | H0 → V | EVIDENCE; O1; O2; NEW | catalog link made by update-catalog |
| 168/168/168 | ubuntu-cfe66bc678 | /etc/shadow | H0 → V | EVIDENCE; O1; O2; NEW | account database the shadow tools keep; census line saved like a Wi-Fi network (5.1) |
| 169/169/169 | ubuntu-9ed4eb3a99 | /etc/shadow- | H0 → V | EVIDENCE; O1; O2; NEW | backup the shadow tools write when editing the database |
| 170/170/170 | ubuntu-5b5a9c277e | /etc/shells | H0 → V | EVIDENCE; O1; O2; NEW | maintained by add-shell (shells.state) |
| 171/171/171 | ubuntu-0075a76d48 | /etc/ssh | H0 → V | CREATOR; O1; O2 | host keys by cloud-init ssh-keygen (log); sshd_config via ucf (ucf cache) |
| 172/172/172 | ubuntu-0306bdd9a9 | /etc/ssl | H0 → V | EVIDENCE; O1; O2; NEW | bundle and hash links by update-ca-certificates |
| 173/173/173 | ubuntu-f18cbc897b | /etc/subgid | H0 → V | EVIDENCE; O1; O2; NEW | subordinate id ranges allocated by useradd (and backups) |
| 174/174/174 | ubuntu-c1ef82d842 | /etc/subgid- | H0 → V | EVIDENCE; O1; O2; NEW | subordinate id ranges allocated by useradd (and backups) |
| 175/175/175 | ubuntu-f17149d114 | /etc/subuid | H0 → V | EVIDENCE; O1; O2; NEW | subordinate id ranges allocated by useradd (and backups) |
| 176/176/176 | ubuntu-a2bc9043e2 | /etc/subuid- | H0 → V | EVIDENCE; O1; O2; NEW | subordinate id ranges allocated by useradd (and backups) |
| 177/177/177 | ubuntu-09d09204d8 | /etc/sudoers.d | H0 → H2 | TWO; O1; O2 | person-specified sudo rule (user-data) written by cloud-init for sudo: data vs derivative (O2) |
| 178/178/178 | ubuntu-7ab5b73f41 | /etc/sysctl.d | H0 → H0 | EVIDENCE; O1; O2; NEW | 99-cloudimg-ipv6.conf written by image build; no recorded writer |
| 179/179/179 | ubuntu-b86fee9a16 | /etc/systemd | H0 → V | COMP; O1; O9; NEW | enable links by deb-systemd-helper/systemctl; state what starts (P3 tension) |
| 180/180/180 | ubuntu-8c833da179 | /etc/timezone | H0 → V | EVIDENCE; O1; O2; NEW | written by tzdata configuration |
| 181/181/181 | ubuntu-f4c9cf7ef7 | /etc/tmpfiles.d | H0 → V | EVIDENCE; O1; O2; NEW | screen-cleanup.conf created by screen postinst |
| 182/182/182 | ubuntu-8eb611608b | /etc/ufw | H0 → V | EVIDENCE; O1; O2; NEW | rules via ucf (ucf cache), ufw.conf/user rules by ufw postinst |
| 183/183/183 | ubuntu-a9c2b32744 | /etc/update-motd.d | H0 → V | EVIDENCE; O1; O2; NEW | link made by landscape-common postinst |
| 184/184/184 | ubuntu-1ef4d5e9cf | /etc/vconsole.conf | H0 → V | EVIDENCE; O1; O2; NEW | link to default/keyboard |
| 185/185/185 | ubuntu-de7f67781f | /etc/vtrgb | H0 → V | EVIDENCE; O1; O2; NEW | update-alternatives link |
| 186/186/186 | ubuntu-66fa11f56b | /etc/xml | H0 → V | EVIDENCE; O1; O2; NEW | catalogs maintained by update-xmlcatalog |
| 187/187/187 | ubuntu-3787beb4db | /home/census/.bash_logout | H0 → V | CODE; O1; NEW | copied from /etc/skel by useradd, not person-written; code executed within the shell (5.1) |
| 188/188/188 | ubuntu-2d36998dd6 | /home/census/.bashrc | H0 → V | CODE; O1; NEW | copied from /etc/skel by useradd, not person-written; code executed within the shell (5.1) |
| 189/189/189 | ubuntu-d48a9a03d6 | /home/census/.cache/motd.legal-displayed | H0 → V | EVIDENCE; O1; O2; NEW | marker the login motd writes once the notice was shown |
| 191/191/191 | ubuntu-c15063bcfe | /home/census/.profile | H0 → V | CODE; O1; NEW | copied from /etc/skel by useradd, not person-written; code executed within the shell (5.1) |
| 192/192/192 | ubuntu-c3a3dd6c9b | /home/census/.ssh | H0 → H2 | TWO; O1; O2 | person's key in person's settings file, written by cloud-init: data vs derivative (O2) |
| 194/194/194 | ubuntu-90017bfd94 | /root/.bashrc | H0 → V | CODE; O1; NEW | copied from /usr/share/base-files dot files, not person-written; code executed within the shell |
| 195/195/195 | ubuntu-0fbf442b3c | /root/.profile | H0 → V | CODE; O1; NEW | copied from /usr/share/base-files dot files, not person-written; code executed within the shell |
| 196/196/196 | ubuntu-351644c1fd | /root/.ssh | H0 → H2 | TWO; O1; O2 | person's key written by cloud-init into root's authorized_keys: data vs derivative (O2) |
| 197/197/197 | ubuntu-97fc2dd36c | /usr/local/man | H0 → V | EVIDENCE; O1; O2; NEW | compat link made by base-files postinst |
| 198/198/198 | ubuntu-1711d3c8c4 | /var/.updated | H0 → V | EVIDENCE; O1; O2; NEW | stamp of systemd-update-done |
| 201/201/201 | ubuntu-68207b149d | /var/cache/debconf | H0 → V | GROUP; O1; O2; NEW | debconf database |
| 204/204/204 | ubuntu-382c94b98b | /var/cache/motd-news | H0 → V | EVIDENCE; O1; O2; NEW | cache |
| 208/208/208 | ubuntu-11311dcdf3 | /var/lib/PackageKit | H0 → V | EVIDENCE; O1; O2; NEW | transaction db |
| 209/209/209 | ubuntu-b5a8d76ff6 | /var/lib/app-info | H0 → V | EVIDENCE; O1; O2; NEW | compat link |
| 210/210/210 | ubuntu-b20e807939 | /var/lib/apt | H0 → V | GROUP; O1; O2; NEW | lists and extended_states (person's install saved like Wi-Fi) |
| 211/211/211 | ubuntu-995a8560ba | /var/lib/cloud | H0 → V | GROUP; O1; O2; NEW | cloud-init own state incl. saved copy of person's cloud-config (saved-Wi-Fi pattern, 5.1) |
| 213/213/213 | ubuntu-7c99ede366 | /var/lib/dbus | H0 → V | EVIDENCE; O1; O2; NEW | machine-id link |
| 214/214/214 | ubuntu-3cce15cf49 | /var/lib/dpkg | H0 → V | GROUP; O1; O2; NEW | package database |
| 215/215/215 | ubuntu-9bc7e83653 | /var/lib/grub | H0 → V | EVIDENCE; O1; O2; NEW | ucf copy of previous config |
| 218/218/218 | ubuntu-b56df50fe2 | /var/lib/pam | H0 → V | EVIDENCE; O1; O2; NEW | pam-auth-update state |
| 221/221/221 | ubuntu-1108460cc8 | /var/lib/shells.state | H0 → V | EVIDENCE; O1; O2; NEW | add-shell state |
| 222/222/222 | ubuntu-4541ba09cc | /var/lib/snapd | H0 → V | GROUP; O1; O2; NEW | snapd state |
| 223/223/223 | ubuntu-8f8e5e285e | /var/lib/swcatalog | H0 → V | EVIDENCE; O1; O2; NEW | catalog links |
| 224/224/224 | ubuntu-57da4d32dc | /var/lib/systemd | H0 → V | COMP; O1; O9; NEW | catalog, timer stamps, deb-systemd-helper state |
| 225/225/225 | ubuntu-1955be13dd | /var/lib/ubuntu-advantage | H0 → V | EVIDENCE; O1; O2; NEW | state |
| 227/227/227 | ubuntu-eaf0301642 | /var/lib/ucf | H0 → V | GROUP; O1; O2; NEW | ucf registry and cache |
| 231/231/231 | ubuntu-d01c2fc3c7 | /var/log/README | H0 → V | EVIDENCE; O1; O2; NEW | link to systemd README made by systemd-tmpfiles |
| 236/236/236 | ubuntu-9c96b64591 | /var/log/btmp | H0 → V | SHARED; O1 | log (5.1 example) |
| 239/239/239 | ubuntu-293699acd1 | /var/log/dmesg | H0 → V | EVIDENCE; O1; O2; NEW | log (5.1 example) |
| 240/240/240 | ubuntu-626ab0ebaf | /var/log/dmesg.0 | H0 → V | EVIDENCE; O1; O2; NEW | log (5.1 example) |
| 245/245/245 | ubuntu-698c23461f | /var/log/lastlog | H0 → V | SHARED; O1 | log (5.1 example) |
| 249/249/249 | ubuntu-d6ce9987c3 | /var/log/wtmp | H0 → V | SHARED; O1 | log (5.1 example) |
| 250/250/250 | ubuntu-98e3025b9e | /var/spool/mail | H0 → V | EVIDENCE; O1; O2; NEW | compat link to ../mail made by base-files postinst |
| 251/251/251 | ubuntu-64f62c6553 | directory-only remainder | H0 → V | GROUP; O1; O2; NEW | 24 empty dirs made by package scripts, systemd, useradd, mkfs |
| 252/252/252 | ubuntu-96787848d5 | netplan-ovs-cleanup.service | H0 → V | COMP; O1; O9; NEW | unit generated into /run by netplan generator; an unrecorded service (P1 tension) |
| 253/253/253 | ubuntu-cbd353d9e3 | systemd-networkd-wait-online.service | H0 → H2 | UNIT; O9; NEW | packaged fragment (recorded) plus generated netplan drop-in (derivative) in one running unit |
| 254/254/254 | ubuntu-a3f2270221 | unpackaged *.device | H0 → V | GRAN; O9; NEW | device units systemd creates from udev at runtime |
| 255/255/255 | ubuntu-18fb2985ed | unpackaged *.mount | H0 → V | GRAN; O9; NEW | mount units from fstab generator and runtime mounts |
| 256/256/256 | ubuntu-9994d7ebc4 | unpackaged *.not-found | H0 → V | REFERENCE; O9; NEW | entries in systemd reference graph for absent units |
| 257/257/257 | ubuntu-0ff15b2741 | unpackaged *.scope | H0 → V | GRAN; O9; NEW | runtime scopes made by systemd/logind |
| 258/258/258 | ubuntu-253d752b01 | unpackaged *.slice | H0 → V | GRAN; O9; NEW | runtime slices made by systemd |
| 259/259/259 | ubuntu-88335c6c87 | unpackaged *.device | H0 → V | GRAN; O9; NEW | device units systemd creates from udev at runtime (user manager) |
| 260/260/260 | ubuntu-565df89b5f | unpackaged *.mount | H0 → V | GRAN; O9; NEW | mount units from fstab generator and runtime mounts (user manager) |
| 261/261/261 | ubuntu-97fdaec6aa | unpackaged *.not-found | H0 → V | REFERENCE; O9; NEW | entries in systemd reference graph for absent units (user manager) |
| 262/262/262 | ubuntu-3bc8c8458c | unpackaged *.scope | H0 → V | GRAN; O9; NEW | runtime scopes made by systemd/logind (user manager) |
| 263/263/263 | ubuntu-b855166ba5 | unpackaged *.slice | H0 → V | GRAN; O9; NEW | runtime slices made by systemd (user manager) |


#### alpine


| Residual / A / B line | ID | Object | A → B | Why code; O / NEW | B’s specific claim (unverified where disputed) |
| --- | --- | --- | --- | --- | --- |
| 2/2/2 | alpine-c6df412fe9 | alpine | H0 → H0 | ACCT; O1; NEW | present in image before first boot; no recorded program or cloud-init log creates it; requester off-machine, not this computer's person |
| 3/3/3 | alpine-8d1e409524 | bin | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 4/4/4 | alpine-96a19ba1e6 | census | R → H2 | CENSUS; O1; O2; NEW | person-specified user (user-data) created by cloud-init useradd for the person, not for cloud-init: data vs derivative (O2); a user also falls under P1 |
| 5/5/5 | alpine-f3d59b813f | chrony | H0 → V | ACCT; O1; NEW | created by chrony pre-install adduser (apk-scripts.tar.gz); running user outside declaration (P1 tension) |
| 6/6/6 | alpine-62764f769d | cron | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 7/7/7 | alpine-4900fca16b | daemon | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 8/8/8 | alpine-27d89cb149 | dhcpcd | H0 → V | ACCT; O1; NEW | created by dhcpcd pre-install adduser (apk-scripts.tar.gz); P1 tension |
| 9/9/9 | alpine-70c3717c60 | ftp | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 10/10/10 | alpine-8e4a0f0c6a | games | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 11/11/11 | alpine-6a022e8f54 | guest | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 12/12/12 | alpine-3d437d2b28 | halt | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 13/13/13 | alpine-577b91e134 | klogd | H0 → V | ACCT; O1; NEW | created by busybox post-install adduser (apk-scripts.tar.gz); P1 tension |
| 14/14/14 | alpine-55e4967557 | lp | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 15/15/15 | alpine-ecfab3dd45 | mail | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 16/16/16 | alpine-625113a2f2 | news | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 17/17/17 | alpine-af2a58bec6 | nobody | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 18/18/18 | alpine-429764e391 | ntp | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 19/19/19 | alpine-cbaf0b4232 | root | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 20/20/20 | alpine-a464712e08 | shutdown | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 21/21/21 | alpine-dbea3590f8 | sshd | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 22/22/22 | alpine-ab8c35e257 | sync | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 23/23/23 | alpine-736d2abbd6 | uucp | H0 → R | ACCT; O1; NEW | defined in package-owned /etc/passwd (alpine-baselayout-data, apk-owner-probes.txt); no apk script or cloud-init creates it |
| 24/24/24 | alpine-ae28c2e9a3 | cloud-getty | H0 → H0 | COMP; O1; O9; NEW | started service; /etc/init.d/cloud-getty owned by no package, not written by cloud-init: image build; unrecorded running component |
| 25/25/25 | alpine-89ce5c5668 | kernel threads | H0 → R | GRAN; O9; NEW | the recorded kernel (linux-virt in world) running its own code |
| 26/26/26 | alpine-d8ee8908a9 | ps | R → H2 | PS; O5; O9; NEW | recorded program launched by the collector shell: recorded vs derivative of launcher, O5 left open |
| 27/27/27 | alpine-3620611c7e | /boot/boot | H0 → V | BOOT; O1; O9 | ln -sf . /boot/boot in mkinitfs trigger (apk-scripts.tar.gz) |
| 28/28/28 | alpine-8809189527 | /boot/extlinux.conf | H0 → V | BOOT; O1; O9 | generated by update-extlinux, syslinux trigger |
| 29/29/29 | alpine-e950c1ebc9 | /boot/initramfs-virt | H0 → V | BOOT; O1; O9 | generated by mkinitfs trigger; code run at boot (P1 tension) |
| 30/30/30 | alpine-d30c6fa9e6 | /boot/ldlinux.c32 | H0 → V | BOOT; O1; O9 | bootloader file installed from syslinux by extlinux/update-extlinux |
| 31/31/31 | alpine-7738a30df8 | /boot/ldlinux.sys | H0 → V | BOOT; O1; O9 | bootloader file installed from syslinux by extlinux/update-extlinux |
| 32/32/32 | alpine-4339436a65 | /boot/libcom32.c32 | H0 → V | BOOT; O1; O9 | bootloader file installed from syslinux by extlinux/update-extlinux |
| 33/33/33 | alpine-5037f0ff69 | /boot/libutil.c32 | H0 → V | BOOT; O1; O9 | bootloader file installed from syslinux by extlinux/update-extlinux |
| 34/34/34 | alpine-fe806c5e93 | /boot/mboot.c32 | H0 → V | BOOT; O1; O9 | bootloader file installed from syslinux by extlinux/update-extlinux |
| 35/35/35 | alpine-f4d63dd583 | /boot/menu.c32 | H0 → V | BOOT; O1; O9 | bootloader file installed from syslinux by extlinux/update-extlinux |
| 36/36/36 | alpine-68e4895187 | /boot/vesamenu.c32 | H0 → V | BOOT; O1; O9 | bootloader file installed from syslinux by extlinux/update-extlinux |
| 37/37/37 | alpine-1dc18c9809 | /etc/apk | H0 → V | GROUP; O1; O2; NEW | apk own state: arch, repositories, world (person-requested names saved by apk, like saved Wi-Fi in 5.1) |
| 38/38/38 | alpine-a483762de6 | /etc/conf.d | H0 → H0 | COMP; O1; O9; NEW | cloud-getty config; no package owns it, cloud-init did not write it: image build |
| 39/39/39 | alpine-8aab7ad250 | /etc/doas.d | H0 → H0 | EVIDENCE; O1; O2; NEW | wheel.conf: no package owns it, no saved script or cloud-init writes it: image build |
| 40/40/40 | alpine-d3bb1c2fce | /etc/group- | H0 → V | EVIDENCE; O1; O2; NEW | backup the shadow tools write when editing /etc/group |
| 41/41/41 | alpine-3d987624ee | /etc/init.d | H0 → H0 | EVIDENCE; O1; O2; NEW | cloud-getty service script: no package owns it, cloud-init did not write it: image build |
| 42/42/42 | alpine-46b7935e7d | /etc/mkinitfs | H0 → H0 | EVIDENCE; O1; O2; NEW | features.d settings written by image build, not by mkinitfs; no recorded writer |
| 43/43/43 | alpine-c169edc1ca | /etc/passwd- | H0 → V | EVIDENCE; O1; O2; NEW | backup the shadow tools write when editing /etc/passwd |
| 44/44/44 | alpine-ea05c8eb7f | /etc/profile.d | H0 → V | CODE; O1; NEW | 50-cloud-init-locale.sh written by cloud-init (cloud-init.log); code run by sh, shared |
| 45/45/45 | alpine-cee61291d2 | /etc/resolv.conf | H0 → V | EVIDENCE; O1; O2; NEW | written by dhcpcd from DHCP lease |
| 46/46/46 | alpine-312e18febb | /etc/runlevels | H0 → V | COMP; O1; O9; NEW | rc-update links = openrc own store of enabled services; states what runs (P3 sentence 2 tension) |
| 47/47/47 | alpine-9ed4eb3a99 | /etc/shadow- | H0 → V | EVIDENCE; O1; O2; NEW | backup the shadow tools write when editing /etc/shadow |
| 48/48/48 | alpine-0075a76d48 | /etc/ssh | H0 → V | CREATOR; O1; O2 | host keys via ssh-keygen and sshd_config.d/50-cloud-init.conf written by cloud-init (cloud-init.log); used by openssh |
| 49/49/49 | alpine-13c9d923d8 | /etc/sudoers.apk-new | H0 → V | EVIDENCE; O1; O2; NEW | apk writes .apk-new when a modified config file conflicts on install |
| 50/50/50 | alpine-09d09204d8 | /etc/sudoers.d | H0 → H2 | TWO; O1; O2 | person-specified sudo rule (user-data) written by cloud-init for sudo: data vs derivative (O2) |
| 51/51/51 | alpine-561d6a5935 | /etc/udev | H0 → V | EVIDENCE; O1; O2; NEW | 70-persistent-net.rules written by cloud-init (cloud-init.log) |
| 52/52/52 | alpine-3e7f7f2c59 | /home/census/.inputrc | H0 → D | INPUTRC; O2 | settings file the person wrote during the day (day.log printf) |
| 53/53/53 | alpine-c3a3dd6c9b | /home/census/.ssh | H0 → H2 | TWO; O1; O2 | person's key in person's settings file, written by cloud-init: own settings (data) vs program-written (derivative), O2 |
| 54/54/54 | alpine-783adc95a0 | /lib/apk | H0 → V | GROUP; O1; O2; NEW | apk installed-package database |
| 55/55/55 | alpine-351644c1fd | /root/.ssh | H0 → H2 | TWO; O1; O2 | person's key written by cloud-init into root's authorized_keys: data vs derivative (O2) |
| 57/57/57 | alpine-995a8560ba | /var/lib/cloud | H0 → V | GROUP; O1; O2; NEW | cloud-init own state incl. saved copy of person's cloud-config (saved-Wi-Fi pattern, 5.1) |
| 63/63/63 | alpine-293699acd1 | /var/log/dmesg | H0 → V | EVIDENCE; O1; O2; NEW | log of kernel messages saved at boot |
| 65/65/65 | alpine-d6ce9987c3 | /var/log/wtmp | H0 → V | SHARED; O1 | login accounting log, shared derivative |
| 66/66/66 | alpine-64f62c6553 | directory-only remainder | H0 → H0 | GROUP; O1; O2; NEW | /home/alpine made at image build (same as account alpine); /home/census by useradd |


### All 14 same-class owner differences

These are additional owner/identity uncertainties, outside the 199 hole-flag rows. Every row is derivative/derivative; §5 text resolution: **not resolved** (reason OWNER, O1 + NEW). Program names versus package names are retained exactly; a naming difference is not by itself evidence of incompatible P6 consequences.


| ID / A,B line | Object | A owner | B owner |
| --- | --- | --- | --- |
| alpine-f2fcdd0583 / 56,56 | /var/cache/apk | apk | apk-tools |
| alpine-4156dc1632 / 59,59 | /var/log/acpid.log | acpid | busybox (acpid) |
| alpine-336e9af6dd / 60,60 | /var/log/apk.log | apk | apk-tools |
| alpine-91a21a61f1 / 64,64 | /var/log/messages | BusyBox syslogd | busybox (syslogd) |
| ubuntu-f2368b74f2 / 137,137 | /etc/ld.so.cache | ldconfig | libc-bin |
| ubuntu-2b7dd179b7 / 202,202 | /var/cache/ldconfig | ldconfig | libc-bin |
| ubuntu-9102b10f3d / 207,207 | /var/cache/swcatalog | AppStream | appstream |
| ubuntu-4214fb28d3 / 216,216 | /var/lib/landscape | landscape | landscape-common |
| ubuntu-baa3fc0dda / 226,226 | /var/lib/ubuntu-release-upgrader | ubuntu-release-upgrader | ubuntu-release-upgrader-core |
| ubuntu-5c70f19bc7 / 228,228 | /var/lib/update-manager | update-manager | update-manager-core |
| ubuntu-7622d0fa6a / 229,229 | /var/lib/update-notifier | update-notifier | update-notifier-common |
| ubuntu-5ce874f910 / 232,232 | /var/log/alternatives.log | update-alternatives | dpkg |
| ubuntu-e6b33c3854 / 242,242 | /var/log/journal | systemd-journald | systemd (journald) |
| ubuntu-eba2994ac6 / 244,244 | /var/log/landscape | landscape | landscape-common |


## Coverage holes and limitations

1. **Independent classification coverage (NEW):** `E6-preclassified.tsv` contains another 1,238 Ubuntu and 473 Alpine rows. None appears in either supplied classification TSV. The second classification (E6B) covered only the residual by design, so this is not a failed residual join. It is a limitation of Check 1’s “each object ... twice, independently” requirement. Every omitted ID, source line, object, reason and NEW mapping is listed in [E6C-coverage-gaps.tsv](E6C-coverage-gaps.tsv). Full E6 totals remain Ubuntu 1,435, Alpine 538, overall 1,973. No preclassified row was copied into both sides to inflate agreement. Full-census agreement/κ is unavailable.
2. **Additional enumeration coverage (O9 + NEW):** E6 reports Alpine user-service probes with runtime-directory/dependency-tree errors, despite zero exit status (`raw-E6/alpine/openrc-user-status.txt`, `openrc-user-runlevels.txt`, `openrc-user-paths.txt`). Unloaded unit files/device bindings are raw-only; excluded filesystem areas and physical firmware/TPM are not fully inventoried. These gaps have no residual ID and are not included in the 199 count. They are stand/coverage limits, not proved no-class objects.
3. **Evidence asymmetry (O1/O2 + NEW):** Classification 2 sometimes infers a creator from a package role or script (and explicitly says “script not saved” for eight Ubuntu accounts), while Classification 1 withholds classification. Existing scripts or known writers are not observed designation or need. E6C does not obtain new VM traces or silently accept either threshold. Some missing premises may be recoverable; the report does not claim every uncertainty is an intrinsic defect in §5.
4. **Proxy and dependence:** E6 calls recorded status an operational package/provisioning proxy. Most rows have no demonstrated personally designated primary declaration. The two residual assignments were made separately and independently, and E6B forbade reading Classification 1’s file; E6C audits their outputs, not the classifiers’ complete cognitive independence. Both used the same collected/grouped inventory and can share errors. The E6 review is not another classification. P1/P4 nonconformity of an ordinary distribution is not substituted for a Check 1 definition counterexample.
5. **Sampling:** one short scripted headless session per VM, not 24 elapsed hours, one user and narrow workloads; differing service universes; overlapping grouped observations rather than independent physical objects. Residual selection and dominant hole labels affect κ; pooled κ is descriptive only. No statistical confidence or OS-quality claim is made.
6. **Resolution limits:** eight of 184 label disagreements have an explicit conditional code-class ruling, while factual/owner gaps remain; 176 label disagreements and all 14 owner differences are not resolved. The table retains all original flags, including 15 matching hole-none pairs. This does not assert that every missing fact needs a new definition, nor that any particular proposed rule is correct. There is no proven incompatible class pair and no proved exclusion from all classes in this audit; further evidence or independent affirmative classifications can change `?` under the same fixed criterion.

## Reproduction and verification

Run `python E6C-compare.py` in this directory. It reads frozen inputs, joins by ID, computes exact fractions, emits the complete row tables and verifies unique/full joins, original hole coverage, owner-field consistency and unchanged source hashes. Output evidence: [E6C-validation.json](E6C-validation.json), [E6C-statistics.json](E6C-statistics.json), [E6C-joined.tsv](E6C-joined.tsv), [E6C-disagreements.tsv](E6C-disagreements.tsv), [E6C-holes.tsv](E6C-holes.tsv). The disagreement file has 198 rows (184 different labels + 14 owner-only); the hole file has 199. Their union has 213 distinct residual IDs. No original E6 or PAPER file is changed.

An independent definition audit is retained in [E6C-definition-audit.md](E6C-definition-audit.md). An independent review (`E6C-review.md`, a working file) independently reproduced the calculations and, in its appended exact-§9.2 clarification, supports `? / ? / ?` and retracts its initial proposed Alpine `0`. The report also incorporates its distinction between a direct code-class rule and unverified execution/owner premises. The original review and correction are both retained; mechanical checks are not self-acceptance of the scientific conclusion.

