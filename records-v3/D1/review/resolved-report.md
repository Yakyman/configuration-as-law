# Review of the 40-row resolved sample

Seed: `2026112201`. Selection: `random.Random(2026112201).sample(eligible, 40)`, where eligible rows are `RESOLVED:` verdicts from `../adjudication/rows.tsv` in source order, read with tab delimiter and `csv.QUOTE_NONE`. Population: 888. Draw order and row-by-row reasoning are preserved in `resolved-sample.tsv`.

## Counts and limits

21 classifications upheld; 9 NOT classifications corrected to MUST by package metadata (candidates REFUTED by S2.2-1); 7 program-state cases are OUTSIDE by S2.5-1 rather than literal proofs of NOT; 3 resolutions are not established by the saved evidence and remain UNKNOWN under S3-2. No confirmed new textual holes. Original sample verdicts: {'RESOLVED:NOT': 28, 'RESOLVED:MUST': 12}.

The seven OUTSIDE rows concern runtime bookkeeping and one PrivateTmp directory. S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.” These are design questions excluded by the task instructions. The published sentence does not itself say that every program-state object need not be recorded; the original NOT labels should not be mistaken for such a rule.

## Candidates investigated

- FACT-WRONG factual premise, UNKNOWN object: `tumbleweed-e0e07676a2b45150a7303e31`, PID 12. `D1/in/raw/tumbleweed/raw/076-process.out:5` has PID 12 followed by PID 1210 and `/usr/bin/startplasma-wayland`. `076-process.sh` prints no newline after a failed executable-link lookup. Therefore the executable belongs to 1210; neither the file nor the script establishes the identity of PID 12. The text would decide known running program/code, but the facts needed to use it for this named object are missing.
- UNKNOWN factual premise: `flatcar-42cb73fd18430fd11f5d305f`, `/etc/selinux/targeted/contexts`; `flatcar-8e7f275dda3033c6764dbce1`, `/etc/selinux/mls/contexts/files`. `../in/raw/flatcar/raw/105-filesystem.out` inventories file metadata and names, not active policy or contents. The adjudication asserts operational use for both policy trees without a saved consumer/configuration observation establishing it. These are missing facts, not demonstrated contradictions of the text. If a consumer uses these mappings for system labels, S2.2-2 decides MUST; if not, that premise fails. Neither possibility needs a new textual rule.

S3-2: “If what the object does remains unknown, the case yields ?.”

## Evidence used for upheld rows

- (not published: adjudication scratch): exact file lists for rdma-core-common, kf6-filesystem, gnome-shell-common, liblangtag-data and microcode_ctl; (not published: adjudication scratch): dependency facts.
- (not published: adjudication scratch), `pix-data.txt`, `nautilus-data.txt`, `linux-headers-6.14.0-37-generic.txt`: package contents.
- (not published: adjudication scratch): package file lists for the Tumbleweed cases.
- Per-row raw inventory references and adjudication notes are in the TSV. No removal experiment was added. Negative removal conclusions are limited to the inventoried machine and its established available consumers; they do not make claims about hypothetical replacement hardware or installing a new consumer.

## Ordered ids

1. `flatcar-302977ff198a4e4b1a4e712d` — /run/udev/links/disk\\x2fby-uuid\\x2f38b84d8c-3de4-4017-8500-20fce9fab9ca
2. `flatcar-db094f84370913cb34fb0235` — /tmp/systemd-private-399ee384a85947e5802aa24624a28b03-polkit.service-b91ISC
3. `tumbleweed-1a2ff00a85c08b7185dc99db` — root:man-pages
4. `fedora-3f32895ef5232a9ecb90302a` — user:rdma-core-common
5. `tumbleweed-7ed90aaf19bee32844bb8824` — opt-relabel.service
6. `mint-488c9c6152f9a5f984d35271` — root:libreoffice-uiconfig-common
7. `flatcar-42cb73fd18430fd11f5d305f` — /etc/selinux/targeted/contexts
8. `flatcar-8d4ffd8cb5ebb190b7e002eb` — /run/udev/links/disk\\x2fby-diskseq\\x2f49
9. `flatcar-0a71ed851814e0fb697f33f3` — /run/udev/links/disk\\x2fby-id\\x2fdm-name-loop3p1-49-verity
10. `mint-18e93d819fb4b35150631865` — bluetooth
11. `tumbleweed-fb68f8c55638ce0185db1206` — user:displaymanager-sysconfig
12. `fedora-041e3807da84dd9e46186c79` — root:kf6-filesystem
13. `flatcar-148193fc319dd99b4186c9e5` — /boot/boot
14. `flatcar-2a8ca562df17fe66a53a012d` — /boot/flatcar/grub/x86_64-xen/macbless.mod
15. `flatcar-86b4b62afd038f8594ff2eb3` — /boot/flatcar/grub/x86_64-xen/search_label.mod
16. `fedora-cc58d5899acb1d4197b6bca4` — root:gnome-shell-common
17. `flatcar-0578cc5491998eeb2acff972` — /boot/flatcar/grub/x86_64-xen/reiserfs.mod
18. `flatcar-da06825ad4492564f1dfb14d` — /boot/flatcar/grub/x86_64-xen/afsplitter.mod
19. `mint-799ef1effb65ec56ca44deb1` — root:nautilus-data
20. `mint-11ea76b71b17cb2a11ce5b11` — root:pix-data
21. `fedora-2e21e6fd047c2a682612c2e0` — user:liblangtag-data
22. `flatcar-09e1b0c16fe478d53732fd21` — /boot/flatcar/grub/x86_64-xen/gcry_md5.mod
23. `tumbleweed-a37f16df0ff2b0a685408d5f` — root:system-group-kvm
24. `mint-a546e0583fc7d7668009b889` — root:linux-headers-6.14.0-37-generic
25. `flatcar-c2de399b8f804cb2d72c2d04` — pcap
26. `flatcar-921afd9765e4af8a8b661d5e` — /run/udev/links/disk\\x2fby-path\\x2fvirtio-pci-0000:00:05.0-part2
27. `flatcar-697c018a7eec871e90bb01f3` — /boot/flatcar/grub/x86_64-xen/part_bsd.mod
28. `flatcar-c14413689e4e173b4bd79592` — /boot/flatcar/grub/x86_64-xen/backtrace.mod
29. `fedora-19ba884b9098cd28a76920a5` — user:microcode_ctl
30. `flatcar-8e7f275dda3033c6764dbce1` — /etc/selinux/mls/contexts/files
31. `tumbleweed-e0e07676a2b45150a7303e31` — 12
32. `tumbleweed-974c6a6e6058683d4f9f985d` — user:yast2-control-center
33. `mint-515f025ca06639e16393a1d3` — backup
34. `flatcar-3ec540466dde50c24e4e6a58` — /sys/devices/pnp0/00:01/driver
35. `flatcar-439542c6589752b405f1a8b6` — /boot/flatcar/grub/x86_64-xen/gzio.mod
36. `mint-57580dfdf8374b94021919bb` — proxy
37. `flatcar-51df5301055ea57aa8b1dc51` — /run/udev/links/disk\\x2fby-path\\x2fpci-0000:00:05.0-part\\x2fby-partlabel\\x2fROOT
38. `fedora-dc2a0270f8795e7197c59f1e` — user:gnome-shell-common
39. `flatcar-0d0039dc3b2bb330f490ad2a` — /run/udev/links/mapper\\x2floop1p1-45-verity
40. `flatcar-586c641c1b9388b446605f5e` — /boot/flatcar/grub/x86_64-xen/newc.mod

## Package-metadata consistency audit

Nine originally upheld NOT package cases are corrected to MUST: sample indices 3, 4, 6, 11, 12, 19, 20, 21 and 23. The exact dependencies, installed versions and saved sources are recorded per row in the revised TSV. Each package is an inventory object whose own requirements or relationship to installed dependent packages controls package-manager behavior; looking only at documents, directories, inactive templates or program-local values omitted this operative metadata. This is the same literal criterion used to refute the dependency-metapackage card.

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

The corrected candidates are REFUTED, not confirmed holes. The remaining sampled NOT package, microcode_ctl, has no own requirements/recommendations or identified installed reverse dependent in the saved Fedora metadata; its documented inapplicability under this hypervisor remains the decision basis. No dependency function was inferred merely from empty directory ownership.
