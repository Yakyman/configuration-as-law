# Review notes: first 150 D1 sample rows

Every sampled ID was matched, without its source prefix, to `D1/in/raw/alma/objects.tsv`. The two submitted sentence sets were read but not used as proof. All member files were opened and every immediate member checked. No recursive group membership was invented. All references below are relative to `D1/in/raw/alma/` unless already prefixed D1.

## Literal rules and evidence

- Dependency packages: S8.2-7 and S8.2-8 decide the kind; S8.2-16 explicitly permits dependency coverage. The retained reason is dependency, including weak dependency. This tests the permissible recording route, not whether an existing declaration actually covers it.
- Nested packages: Exact native manifests establish package provenance for both metadata and actual content; all observed non-directory content paths were joined and are unchanged. native_package_ids alone is not used as containment proof. Question one decides because these are installed packages. S8.2-16 permits their native package line.
- Unchanged files and module groups: S8.2-7/8/16. Exact manifest integrity is unchanged. Module paths require the observed `/lib` symlink target `usr/lib` in `raw/0004-filesystem.out`; this is an observed alias, not guessed path equivalence.
- Policy actions: decoded retained metadata contains the exact action ID inside an unchanged package policy. S8.2-6 prevents replacing the first question with the later access-setting question.
- Processes, sysfs representations, live firewall rules, service-manager state, and runtime storage: S8.2-5 precedes the four questions. A missing executable name does not alter RUNTIME, because all possible creator identities give that label. Creator decisions are inherited rather than independently reconstructed here.
- Records: S8.2-15, after earlier questions, covers metadata/indexing directory objects, databases and logs. An immediate child directory is not silently expanded into its descendants. Four groups include actual opaque HTTP body files; their contents were not captured, so question two cannot be excluded from mode bits or names. These are FACT-UNKNOWN, not a text gap.

## Public documentation consulted

- https://docs.kernel.org/filesystems/sysfs.html : “sysfs is a RAM-based filesystem initially based on ramfs.” The captured query scripts list sysfs directories, not stored module binaries.
- https://docs.npmjs.com/cli/commands/npm-cache/ : “npm stores cache data in an opaque directory within the configured `cache`, named `_cacache`.” This identifies cache layout but does not prove opaque payload executability.
- https://pip.pypa.io/en/stable/topics/caching/ : “This cache functions like a web browser cache.” Its HTTP-response section and version-23.3 http-v2 description identify the layout; exact response contents remain unavailable.
- https://github.com/linux-audit/audit-userspace/blob/master/init.d/auditd.conf : “log_file = /var/log/audit/audit.log”. Retained members identify the log, not executable material.

`D1/in/control/alma/actions-logs/language_program.log` documents successful npm installation during the captured cache creation interval. No actual payload contents were inferred from that temporal correspondence.

## Manual checks per homogeneous rule

The source rows, member lists and relevant integrity joins were visually inspected before applying these rules. Lists below contain ten IDs or the whole rule when smaller.

- record-storage (16 rows): alma-01de2c17810a6d073ff215fc, alma-0f156edc538beaea8c740182, alma-101389cda3334da6ae1e6ca5, alma-13f3fc49e00d758f4a5b3ae2, alma-2503dc1730804dfecdb8d724, alma-3024b0bcc6b970629f803919, alma-41801e6cef6462af10fd155e, alma-478ebf23ffd2e516cfe11715, alma-53242fc87d6f5938c40b3e59, alma-6990321f35168eb2d918e4a0.
- nested-package (8 rows): alma-05f12d6e97997e01922d0833, alma-0a3c0cb2e5f459afec3b2ec3, alma-18466927543ce3a9e55f5fb4, alma-4aefc3250e442ed14a62023a, alma-7d57df7e0a621edccaf53809, alma-b09169804cf04fd2c02f24b0, alma-b2720b1428432d6396daa4f3, alma-c143577a24fffcf97c95151b.
- process (35 rows): alma-0a918c668b0167bf55e9aaba, alma-13aae0946baee1216b63e8b8, alma-17dc5d05010cd38bc6147a35, alma-26b86e2f3303a5cc0035fbe0, alma-2970be5f381a594f0deafffd, alma-2a64c73852e86ee645103163, alma-2b06c2daf4512007ce015a28, alma-31186e612073f58471ddec1e, alma-343ce46096a566b3f528e7cf, alma-37bdaa3a5b9589af91f9024a.
- polkit-action (12 rows): alma-0acd26fa018532bc4a6f2064, alma-54c5af42a3d2c905f7c6004d, alma-558b34faf2fde0918cb659fb, alma-64e4644617a89ddf03479a6e, alma-68780174c4eb5adf8e6521e0, alma-72ccd610cffd729eddae5fcb, alma-765fb469f2c1589991951b7a, alma-827ef66badc098d9ff74242d, alma-8827d8dd38847521e9b6c92f, alma-8d8442547e17685de4ec7e4f.
- opaque-http-body (4 rows): alma-0c65c3ff2333b5855dfa1218, alma-287954d7986f9463a1d03ac8, alma-69ab72dbf21ea1a6fe95344f, alma-93b0c210150c3de57fd663ee.
- dependency-package (29 rows): alma-0cb8eddde2f81bbeb26486f3, alma-10dcd106eefbef34437deae0, alma-1bfafdd6cecc1e9bda6b8b11, alma-27ee1e0d6b9dd79a85d6cc98, alma-34fdfeaf02f683e0a873994c, alma-362d8b22811d67f387668648, alma-451b73bda6e9ec1e1993f101, alma-480b66331b1031699e8809ca, alma-4ab6262626392d9ea31211a9, alma-4ba55e154ebd36ebd7c59c7e.
- firewall-runtime (11 rows): alma-0e25ced4c49af895d97d8395, alma-35f8d5c315f1ca762266035f, alma-3fd8d3c9097ecb66887bc6fd, alma-4b704a9c35400d77f231dc4a, alma-4bc08978550dfb230ce88537, alma-55d70bc0461faa64054ebe2d, alma-5c5bc064a48c070f46e70809, alma-7db6ed317d0ea1114a73fb9b, alma-8b307c05c48e0e2e713f1095, alma-ad706c157d772a8ef7ffd2cd.
- unchanged-module-group (10 rows): alma-14e8523f696dece93c71875e, alma-2c69f9f6fafd998cba3030a0, alma-33f2e2681995f2d97cb54985, alma-4613a5495334c5c10b6514a1, alma-4834f327863f488c9aeba5ae, alma-5be068306ffd78eb4cb14dbd, alma-637f6f7ed994901421759e05, alma-adcd6702b6cbc7d4117364c9, alma-c6f5e6073176d49555554cf0, alma-c79c577d10d15ad870640881.
- runtime-storage (5 rows): alma-26a23d2104fea49b1b65e6d3, alma-4b3adac5114a229206208282, alma-61f1eb28c19ef6c2bb547ac2, alma-7259977fddd8433ef380c0d0, alma-abc3e1d04735ab930a624c37.
- sysfs-runtime (9 rows): alma-2bb1108e03ebe00cdf704c7b, alma-50320d745aaabc5c80816c24, alma-5275383f5b310111ab62ad56, alma-5660c4c30d837dee812b6b99, alma-669ee8a57ffcb189f4fc6a62, alma-7fdd8e19483c3efb80b2ea63, alma-8ce82676283d422a5f1bef63, alma-a16100128ec51ea7dc23723e, alma-b6ff3049c9ce8031728f801f.
- unchanged-file (10 rows): alma-373e9de16f80c625b9e46618, alma-395e07fd1415587cadf07f46, alma-47ec2773ac48666c737c809c, alma-5df11c8303826fc728ff82e1, alma-65016f8ffa60e856f3fdd110, alma-72edf6df1bee60a1fcddb1e9, alma-7a25e6159de02325790f9f3e, alma-7bab9b79374b165df6b32709, alma-a00051bc3715e31b63bab9f7, alma-ab3fa6646241566543c5bab4.
- service (1 rows): alma-4129e3f409a79b3d38a21046.

## Per-row evidence index

| ID | Rule | Evidence |
|---|---|---|
| alma-01de2c17810a6d073ff215fc | record-storage | raw/0004-filesystem.out;members/01de2c17810a6d073ff215fc.tsv |
| alma-05f12d6e97997e01922d0833 | nested-package | raw/0005-metadata-read-0.out;package-files.tsv;native_package_ids=61ede02194b62207f7338ffc;content_root=/usr/lib/python3.12/site-packages/procfs;verified_content_files=9 |
| alma-0a3c0cb2e5f459afec3b2ec3 | nested-package | raw/0007-metadata-read-128.out;package-files.tsv;native_package_ids=b13ee5598b7640875532d838;content_root=/usr/lib/node_modules_22/npm/node_modules/spdx-license-ids;verified_content_files=3 |
| alma-0a918c668b0167bf55e9aaba | process | raw/0211-process-executables.out |
| alma-0acd26fa018532bc4a6f2064 | polkit-action | D1/in/raw/alma/raw/0226-metadata-read-0.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.NetworkManager.policy |
| alma-0c65c3ff2333b5855dfa1218 | opaque-http-body | raw/0004-filesystem.out;members/0c65c3ff2333b5855dfa1218.tsv |
| alma-0cb8eddde2f81bbeb26486f3 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-0e25ced4c49af895d97d8395 | firewall-runtime | raw/0202-firewall-nft.out |
| alma-0f156edc538beaea8c740182 | record-storage | raw/0004-filesystem.out;members/0f156edc538beaea8c740182.tsv |
| alma-101389cda3334da6ae1e6ca5 | record-storage | raw/0004-filesystem.out;members/101389cda3334da6ae1e6ca5.tsv |
| alma-10dcd106eefbef34437deae0 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-13aae0946baee1216b63e8b8 | process | raw/0211-process-executables.out |
| alma-13f3fc49e00d758f4a5b3ae2 | record-storage | raw/0004-filesystem.out;members/13f3fc49e00d758f4a5b3ae2.tsv |
| alma-14e8523f696dece93c71875e | unchanged-module-group | raw/0004-filesystem.out;members/14e8523f696dece93c71875e.tsv;package-files.tsv;raw/0004-filesystem.out:lib-symlink |
| alma-17dc5d05010cd38bc6147a35 | process | raw/0211-process-executables.out |
| alma-18466927543ce3a9e55f5fb4 | nested-package | raw/0005-metadata-read-0.out;package-files.tsv;native_package_ids=ad24d9eca67b506611e6a2ec;content_root=/usr/lib/python3.12/site-packages/argcomplete;verified_content_files=38 |
| alma-1bfafdd6cecc1e9bda6b8b11 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-2503dc1730804dfecdb8d724 | record-storage | raw/0004-filesystem.out;members/2503dc1730804dfecdb8d724.tsv |
| alma-26a23d2104fea49b1b65e6d3 | runtime-storage | raw/0004-filesystem.out;members/26a23d2104fea49b1b65e6d3.tsv |
| alma-26b86e2f3303a5cc0035fbe0 | process | raw/0211-process-executables.out |
| alma-27ee1e0d6b9dd79a85d6cc98 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-287954d7986f9463a1d03ac8 | opaque-http-body | raw/0004-filesystem.out;members/287954d7986f9463a1d03ac8.tsv |
| alma-2970be5f381a594f0deafffd | process | raw/0211-process-executables.out |
| alma-2a64c73852e86ee645103163 | process | raw/0211-process-executables.out |
| alma-2b06c2daf4512007ce015a28 | process | raw/0211-process-executables.out |
| alma-2bb1108e03ebe00cdf704c7b | sysfs-runtime | raw/0213-driver-names.out |
| alma-2c69f9f6fafd998cba3030a0 | unchanged-module-group | raw/0004-filesystem.out;members/2c69f9f6fafd998cba3030a0.tsv;package-files.tsv;raw/0004-filesystem.out:lib-symlink |
| alma-3024b0bcc6b970629f803919 | record-storage | raw/0004-filesystem.out;members/3024b0bcc6b970629f803919.tsv |
| alma-31186e612073f58471ddec1e | process | raw/0211-process-executables.out |
| alma-33f2e2681995f2d97cb54985 | unchanged-module-group | raw/0004-filesystem.out;members/33f2e2681995f2d97cb54985.tsv;package-files.tsv;raw/0004-filesystem.out:lib-symlink |
| alma-343ce46096a566b3f528e7cf | process | raw/0211-process-executables.out |
| alma-34fdfeaf02f683e0a873994c | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-35f8d5c315f1ca762266035f | firewall-runtime | raw/0202-firewall-nft.out |
| alma-362d8b22811d67f387668648 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-373e9de16f80c625b9e46618 | unchanged-file | raw/0197-unit-file.out;package-files.tsv:/usr/lib/systemd/system/pam_namespace.service |
| alma-37bdaa3a5b9589af91f9024a | process | raw/0211-process-executables.out |
| alma-395e07fd1415587cadf07f46 | unchanged-file | raw/0197-unit-file.out;package-files.tsv:/usr/lib/systemd/system/alsa-state.service |
| alma-3fd8d3c9097ecb66887bc6fd | firewall-runtime | raw/0202-firewall-nft.out |
| alma-40588903b264086789da29df | process | raw/0211-process-executables.out |
| alma-4129e3f409a79b3d38a21046 | service | raw/0195-service.out |
| alma-41801e6cef6462af10fd155e | record-storage | raw/0004-filesystem.out;members/41801e6cef6462af10fd155e.tsv |
| alma-451b73bda6e9ec1e1993f101 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-4613a5495334c5c10b6514a1 | unchanged-module-group | raw/0004-filesystem.out;members/4613a5495334c5c10b6514a1.tsv;package-files.tsv;raw/0004-filesystem.out:lib-symlink |
| alma-478ebf23ffd2e516cfe11715 | record-storage | raw/0004-filesystem.out;members/478ebf23ffd2e516cfe11715.tsv |
| alma-47ec2773ac48666c737c809c | unchanged-file | raw/0227-metadata-read-64.out;package-files.tsv:/usr/share/polkit-1/rules.d/org.gtk.vfs.file-operations.rules |
| alma-480b66331b1031699e8809ca | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-4834f327863f488c9aeba5ae | unchanged-module-group | raw/0004-filesystem.out;members/4834f327863f488c9aeba5ae.tsv;package-files.tsv;raw/0004-filesystem.out:lib-symlink |
| alma-4ab6262626392d9ea31211a9 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-4aefc3250e442ed14a62023a | nested-package | raw/0005-metadata-read-0.out;package-files.tsv;native_package_ids=b13ee5598b7640875532d838;content_root=/usr/lib/node_modules_22/npm/node_modules/@npmcli/node-gyp;verified_content_files=3 |
| alma-4b3adac5114a229206208282 | runtime-storage | raw/0004-filesystem.out;members/4b3adac5114a229206208282.tsv |
| alma-4b704a9c35400d77f231dc4a | firewall-runtime | raw/0202-firewall-nft.out |
| alma-4ba55e154ebd36ebd7c59c7e | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-4bc08978550dfb230ce88537 | firewall-runtime | raw/0202-firewall-nft.out |
| alma-50320d745aaabc5c80816c24 | sysfs-runtime | raw/0212-module-names.out |
| alma-50cdb3c2f82816995ee05ab6 | process | raw/0211-process-executables.out |
| alma-516bfde517ca31f89c40ca56 | process | raw/0211-process-executables.out |
| alma-5275383f5b310111ab62ad56 | sysfs-runtime | raw/0213-driver-names.out |
| alma-53242fc87d6f5938c40b3e59 | record-storage | raw/0004-filesystem.out;members/53242fc87d6f5938c40b3e59.tsv |
| alma-5324453d4a584a24e98f5d11 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-54c5af42a3d2c905f7c6004d | polkit-action | D1/in/raw/alma/raw/0227-metadata-read-64.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.UDisks2.policy |
| alma-558b34faf2fde0918cb659fb | polkit-action | D1/in/raw/alma/raw/0226-metadata-read-0.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.login1.policy |
| alma-55d70bc0461faa64054ebe2d | firewall-runtime | raw/0202-firewall-nft.out |
| alma-5660c4c30d837dee812b6b99 | sysfs-runtime | raw/0212-module-names.out |
| alma-58b59741d4332defdf1becbe | process | raw/0211-process-executables.out |
| alma-59e5ea936409b25aedce2bff | process | raw/0211-process-executables.out |
| alma-59e5fcaa01866bcc95ab6a12 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-59ecc0d8d9700d4501f70e2d | process | raw/0211-process-executables.out |
| alma-5afa4c0a0dce696bd17e557b | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-5be068306ffd78eb4cb14dbd | unchanged-module-group | raw/0004-filesystem.out;members/5be068306ffd78eb4cb14dbd.tsv;package-files.tsv;raw/0004-filesystem.out:lib-symlink |
| alma-5c5bc064a48c070f46e70809 | firewall-runtime | raw/0202-firewall-nft.out |
| alma-5df11c8303826fc728ff82e1 | unchanged-file | raw/0197-unit-file.out;package-files.tsv:/usr/lib/systemd/system/plymouth-switch-root.service |
| alma-60e08319af1d7795779b5085 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-61f1eb28c19ef6c2bb547ac2 | runtime-storage | raw/0004-filesystem.out;members/61f1eb28c19ef6c2bb547ac2.tsv |
| alma-637f6f7ed994901421759e05 | unchanged-module-group | raw/0004-filesystem.out;members/637f6f7ed994901421759e05.tsv;package-files.tsv;raw/0004-filesystem.out:lib-symlink |
| alma-64e4644617a89ddf03479a6e | polkit-action | D1/in/raw/alma/raw/0227-metadata-read-64.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.Flatpak.policy |
| alma-65016f8ffa60e856f3fdd110 | unchanged-file | raw/0222-user-user-unit-file.out;package-files.tsv:/usr/lib/systemd/user/gvfs-goa-volume-monitor.service |
| alma-6556f3ed91286ed746142ca7 | process | raw/0211-process-executables.out |
| alma-669e1f296de8f9812d1df6a5 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-669ee8a57ffcb189f4fc6a62 | sysfs-runtime | raw/0213-driver-names.out |
| alma-68780174c4eb5adf8e6521e0 | polkit-action | D1/in/raw/alma/raw/0227-metadata-read-64.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.UDisks2.policy |
| alma-690a01a2c11370ab1950bb3e | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-6990321f35168eb2d918e4a0 | record-storage | raw/0004-filesystem.out;members/6990321f35168eb2d918e4a0.tsv |
| alma-69ab72dbf21ea1a6fe95344f | opaque-http-body | raw/0004-filesystem.out;members/69ab72dbf21ea1a6fe95344f.tsv |
| alma-70af800627e9295909f8d27d | process | raw/0211-process-executables.out |
| alma-7259977fddd8433ef380c0d0 | runtime-storage | raw/0004-filesystem.out;members/7259977fddd8433ef380c0d0.tsv |
| alma-72ccd610cffd729eddae5fcb | polkit-action | D1/in/raw/alma/raw/0226-metadata-read-0.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.color.policy |
| alma-72edf6df1bee60a1fcddb1e9 | unchanged-file | raw/0226-metadata-read-0.out;package-files.tsv:/usr/share/polkit-1/actions/org.gnome.displaymanager.policy |
| alma-765fb469f2c1589991951b7a | polkit-action | D1/in/raw/alma/raw/0226-metadata-read-0.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.login1.policy |
| alma-7665e078531e0c636508e68b | process | raw/0211-process-executables.out |
| alma-7a25e6159de02325790f9f3e | unchanged-file | raw/0222-user-user-unit-file.out;package-files.tsv:/usr/lib/systemd/user/gvfs-daemon.service |
| alma-7b7495ff9dca1cc4ca1dc8f3 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-7bab9b79374b165df6b32709 | unchanged-file | raw/0226-metadata-read-0.out;package-files.tsv:/etc/sudoers |
| alma-7d57df7e0a621edccaf53809 | nested-package | raw/0005-metadata-read-0.out;package-files.tsv;native_package_ids=b3424c7b994bde3ef591023b;content_root=/usr/lib/python3.12/site-packages/pip;verified_content_files=1516 |
| alma-7db6ed317d0ea1114a73fb9b | firewall-runtime | raw/0202-firewall-nft.out |
| alma-7fd63132f984280ac5e8c41f | process | raw/0211-process-executables.out |
| alma-7fdd8e19483c3efb80b2ea63 | sysfs-runtime | raw/0213-driver-names.out |
| alma-8060b967d9eb2930f9490644 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-81455ab0dd570d9690c7cac1 | process | raw/0211-process-executables.out |
| alma-827ef66badc098d9ff74242d | polkit-action | D1/in/raw/alma/raw/0226-metadata-read-0.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.realmd.policy |
| alma-83cd539cb9921006f73b68c4 | process | raw/0211-process-executables.out |
| alma-842e90f811296c469f9e7e42 | record-storage | raw/0004-filesystem.out;members/842e90f811296c469f9e7e42.tsv |
| alma-84576be3461a2f4ce3a9e7cc | process | raw/0211-process-executables.out |
| alma-86ef4ebd8dadcd5f8390b8d7 | record-storage | raw/0004-filesystem.out;members/86ef4ebd8dadcd5f8390b8d7.tsv |
| alma-871fe0e2123dc22fa1b88891 | process | raw/0211-process-executables.out |
| alma-8827d8dd38847521e9b6c92f | polkit-action | D1/in/raw/alma/raw/0226-metadata-read-0.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.RealtimeKit1.policy |
| alma-89d630bdae35ffa1ee64747c | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-8a396153ab43de44f0991aaa | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-8b307c05c48e0e2e713f1095 | firewall-runtime | raw/0202-firewall-nft.out |
| alma-8c3e6dc7c00e5d9a7a14ec57 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-8ce82676283d422a5f1bef63 | sysfs-runtime | raw/0213-driver-names.out |
| alma-8d8442547e17685de4ec7e4f | polkit-action | D1/in/raw/alma/raw/0226-metadata-read-0.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.login1.policy |
| alma-8e1b4083c283f77fd8d14f59 | polkit-action | D1/in/raw/alma/raw/0226-metadata-read-0.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.login1.policy |
| alma-915d71ea44dace54b9c1ab40 | process | raw/0211-process-executables.out |
| alma-93b0c210150c3de57fd663ee | opaque-http-body | raw/0004-filesystem.out;members/93b0c210150c3de57fd663ee.tsv |
| alma-94f4998a75c73edda740d33f | process | raw/0211-process-executables.out |
| alma-9be63c40a4c1f219d92bfb62 | process | raw/0211-process-executables.out |
| alma-9d92996e420528ec6fc03120 | process | raw/0211-process-executables.out |
| alma-a00051bc3715e31b63bab9f7 | unchanged-file | raw/0222-user-user-unit-file.out;package-files.tsv:/usr/lib/systemd/user/systemd-exit.service |
| alma-a0f2c61fece75d15549cb871 | record-storage | raw/0004-filesystem.out;members/a0f2c61fece75d15549cb871.tsv |
| alma-a16100128ec51ea7dc23723e | sysfs-runtime | raw/0212-module-names.out |
| alma-a3df55613b9b6fe93d4161c1 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-a66a23b94257ba50639f9301 | process | raw/0211-process-executables.out |
| alma-a85c6909db6ca17bf43919da | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-a8c51a4676cdbeecd80ab527 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-a9afa405bcccdc0b5daffff7 | polkit-action | D1/in/raw/alma/raw/0226-metadata-read-0.out;package-files.tsv:/usr/share/polkit-1/actions/org.freedesktop.packagekit.policy |
| alma-a9c9a3ce44ebc606ea42ab1a | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-a9fd489a97922ef08fa8ed54 | process | raw/0211-process-executables.out |
| alma-ab3fa6646241566543c5bab4 | unchanged-file | raw/0197-unit-file.out;package-files.tsv:/usr/lib/systemd/system/systemd-suspend.service |
| alma-abc3e1d04735ab930a624c37 | runtime-storage | raw/0004-filesystem.out;members/abc3e1d04735ab930a624c37.tsv |
| alma-ad706c157d772a8ef7ffd2cd | firewall-runtime | raw/0202-firewall-nft.out |
| alma-adc78e1a50ece6d5b9aa9a52 | firewall-runtime | raw/0202-firewall-nft.out |
| alma-adcd6702b6cbc7d4117364c9 | unchanged-module-group | raw/0004-filesystem.out;members/adcd6702b6cbc7d4117364c9.tsv;package-files.tsv;raw/0004-filesystem.out:lib-symlink |
| alma-add3f7dde4ebc6e17d3abff2 | record-storage | raw/0004-filesystem.out;members/add3f7dde4ebc6e17d3abff2.tsv |
| alma-aea6e209d3434b24e1ff4aec | process | raw/0211-process-executables.out |
| alma-aecf2979c59cb0e19cba8beb | process | raw/0211-process-executables.out |
| alma-b09169804cf04fd2c02f24b0 | nested-package | raw/0006-metadata-read-64.out;package-files.tsv;native_package_ids=b13ee5598b7640875532d838;content_root=/usr/lib/node_modules_22/npm/node_modules/just-diff;verified_content_files=5 |
| alma-b1647b3f75fa0fe1bf000d84 | record-storage | raw/0004-filesystem.out;members/b1647b3f75fa0fe1bf000d84.tsv |
| alma-b2720b1428432d6396daa4f3 | nested-package | raw/0005-metadata-read-0.out;package-files.tsv;native_package_ids=b13ee5598b7640875532d838;content_root=/usr/lib/node_modules_22/npm/node_modules/@npmcli/git;verified_content_files=15 |
| alma-b5f888f751f7e06fb4014915 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-b6ff3049c9ce8031728f801f | sysfs-runtime | raw/0212-module-names.out |
| alma-b9b2006342aa12ca6ae12828 | process | raw/0211-process-executables.out |
| alma-babd26103390768dd5892c68 | record-storage | raw/0004-filesystem.out;members/babd26103390768dd5892c68.tsv |
| alma-badb537899cf1278ef4527d0 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-c143577a24fffcf97c95151b | nested-package | raw/0006-metadata-read-64.out;package-files.tsv;native_package_ids=b13ee5598b7640875532d838;content_root=/usr/lib/node_modules_22/npm/node_modules/ini;verified_content_files=3 |
| alma-c3369970a0b4daec453bddda | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-c51f9717fc41685e5b7cc171 | dependency-package | raw/0015-packages-rpm.out;raw/0016-package-reasons-dnf.out;raw/0017-metadata-read-0.out;raw/0018-package-selected-groups-dnf.out |
| alma-c6f5e6073176d49555554cf0 | unchanged-module-group | raw/0004-filesystem.out;members/c6f5e6073176d49555554cf0.tsv;package-files.tsv;raw/0004-filesystem.out:lib-symlink |
| alma-c79c577d10d15ad870640881 | unchanged-module-group | raw/0004-filesystem.out;members/c79c577d10d15ad870640881.tsv;package-files.tsv;raw/0004-filesystem.out:lib-symlink |
| alma-cd17d7baa722be8f2b1b47b1 | process | raw/0211-process-executables.out |
| alma-cd50d3a56025fd5b1023e76b | process | raw/0211-process-executables.out |

Counts: {'FOLLOWS': 146, 'FACT-UNKNOWN': 4}

## Nested-package follow-up verification

The filesystem traversal was joined against exact native manifest paths for every observed non-directory child under each package content root. No content path was absent, changed, or unknown. The three Python distributions have unavailable RECORD files, but their native RPM manifests contain both distribution metadata and actual module code. The mapping is checked against those native package contents, not inferred solely from metadata ownership.

| Sample ID | Content suffix under site-packages or npm/node_modules | Non-directory content files | Native package ID |
|---|---|---:|---|
| alma-05f12d6e97997e01922d0833 | procfs | 9 | 61ede02194b62207f7338ffc |
| alma-18466927543ce3a9e55f5fb4 | argcomplete | 38 | ad24d9eca67b506611e6a2ec |
| alma-7d57df7e0a621edccaf53809 | pip | 1516 | b3424c7b994bde3ef591023b |
| alma-0a3c0cb2e5f459afec3b2ec3 | spdx-license-ids | 3 | b13ee5598b7640875532d838 |
| alma-4aefc3250e442ed14a62023a | @npmcli/node-gyp | 3 | b13ee5598b7640875532d838 |
| alma-b09169804cf04fd2c02f24b0 | just-diff | 5 | b13ee5598b7640875532d838 |
| alma-b2720b1428432d6396daa4f3 | @npmcli/git | 15 | b13ee5598b7640875532d838 |
| alma-c143577a24fffcf97c95151b | ini | 3 | b13ee5598b7640875532d838 |

The Python native packages have respectively 16, 50, and 1531 total manifest files, all unchanged, including command entry points outside site-packages. Thus all eight recording routes remain supported. Evidence: (not published: over 20 MB), (not published: over 20 MB), and the native package records in `D1/in/raw/alma/objects.tsv`.
