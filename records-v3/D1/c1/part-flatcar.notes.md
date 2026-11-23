# Flatcar c1 classification notes

Input: `../in/part-flatcar.tsv`. Output: `part-flatcar.tsv`.

All 1,827 input occurrences are retained exactly once. Decisions use only Section 2.2 and the first indicator of Section 3, together with object behavior established from the assigned inventory and public primary sources. No objects were removed. The inventory's earlier class-like wording was ignored. No other classification or earlier-night result was consulted.

The following sections contain all rules, their sentence derivations, ten hand-checked row IDs per homogeneous rule, individually considered exceptions, documentation quotations, and grouped-member mappings. For MIXED rows, numbers refer to one-based positions in the input members array; the complete mappings appear below. The small decision table remains within its field-length bounds.

Raw references use the inventory layout: `raw:raw/flatcar/raw/...` is relative to D1/in, `raw:flatcar/raw/...` is relative to D1/in/raw, and `raw:D1/in/raw/...` is relative to the night folder. Optional trailing line numbers identify exact inventory records.

Finished rows were appended and flushed. Factual corrections within this task were audited in the relevant subsection and `part-flatcar.integration-corrections.jsonl`; no previous-attempt output existed at task start.

Validation: `part-flatcar.verify.py` verifies exact header, UTF-8 decoding, input/output count and ID multiset equality, uniqueness, decision vocabulary, sentence IDs, field word limits, embedded delimiters, and raw-file references. `part-flatcar.done` contains the resulting counts. Stored-group verification additionally checks every MIXED row's complete, non-overlapping member-index coverage.




---

# c1 Flatcar: accounts, processes, interfaces, and authorization

Scope: 516 rows outside the stored-object, executable-candidate, and service-unit subsets. Read COMMON.md first, then TEXT.md Sections 2 and 3 and SENTENCES.md. Only the assigned input, its raw evidence, public documentation, and this task's c1 work products were consulted. No removal or machine modification was performed. Inventory category names do not determine decisions. Raw basis paths are relative to D1/in; an optional final colon gives the inventory line.

## Exact text used

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-2** If what the object does remains unknown, the case yields ?.

## Primary documentation and short supporting quotations

- https://man7.org/linux/man-pages/man5/group.5.html: “defines the groups on the system.” The fields distinguish group identity and supplementary membership, including empty membership lists.
- https://man7.org/linux/man-pages/man5/proc_pid_exe.5.html: “containing the actual pathname of the executed command.” The collector's readlink result identifies an executable only for the immediately preceding PID.
- https://www.kernel.org/doc/html/latest/kbuild/modules.html: “The kbuild system will build <module_name>.o from <module_name>.c”. Loaded kernel modules are native kernel code rather than preference values.
- https://docs.kernel.org/admin-guide/sysfs-rules.html: “it is retrieved by reading the “driver”-link and using only the last element of the target path”. Driver rows identify live discovery interfaces, not stored driver binary files.
- https://docs.kernel.org/driver-api/driver-model/binding.html: “Driver binding is the process of associating a device with a device driver that can control it.” The actual link targets identify the current driver associations.
- https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html: “Actions correspond to operations that clients can request the mechanism to carry out”; “the spawned programs will run as the unprivileged polkitd system user.” Actions register cross-program authorization; JavaScript rules can execute helpers with interpreter rights. The .example file is not a loaded .rules file.
- https://man.openbsd.org/sshd_config: “The file contains keyword-argument pairs, one per line.” Effective SSH values were read individually against the documented directive meanings. Authentication and session controls affect account access or session processes; protocol and display choices remain internal. Forwarding and exported PID metadata leave the scope of “only inside” unclear. The manually authored directive map records individual judgments, not a rule that all SSH settings share a classification.
- https://www.freedesktop.org/software/systemd/man/latest/networkctl.html: “Show a list of existing links and their status.” The rows represent network interfaces, including loopback, rather than saved Wi-Fi profiles.
- https://devmanual.gentoo.org/function-reference/install-functions/index.html: “This is accomplished by installing a hidden file prefixed with `.keep` to the directory in question.” Empty package placeholders are neither access rules nor saved networks.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html: “The main network file must have the extension `.network`; other extensions are ignored.” This directly excludes the inventoried empty .keep placeholder from network configuration.

## Homogeneous rules

All rule samples below were read by hand in the inventory and raw records, before final validation. The scripts preserve each input occurrence as a separate ID, including repeated accounts and groups.

1. **accounts**: passwd entries define accounts; S2.2-15 explicitly requires accounts. A non-login shell does not remove account identity. All 39 MUST.
2. **groups**: group entries define system identities used to assign process/file group ownership and supplementary membership. S2.2-1/2 require those capabilities. An empty supplementary list still defines a usable named group; no particular privilege is inferred from a group's name. All 67 MUST.
3. **identified-processes**: exactly one PID followed by one absolute executable path proves a running program. S2.2-9/12 explicitly require the program. All 18 MUST.
4. **unresolved-processes**: the named PID lacks an executable lookup. The raw shell command prints the PID before readlink and adds no newline on readlink failure. Later PIDs and paths concatenate onto that line; a later executable cannot be attributed to the first PID. Actual behavior of the named object remains unknown under S3-2. All 15 UNKNOWN. These are not directory groups, so a known later process does not justify MIXED for the unresolved named PID.
5. **modules**: raw /proc/modules records identify loaded native kernel modules. Native code executes with kernel rights; S2.2-10 requires it. All 73 MUST. Names such as mbcache do not turn implementing code into exempt cache content.
6. **driver-links**: each inventoried object is specifically a /sys/devices/.../driver symbolic link. Documentation establishes that it exposes driver identity, but no actual local consumer dependency is captured. All 29 UNKNOWN under S3-2: the evidence does not establish whether a link participates in operational selection or only supplies displayed information. Treating it as the underlying driver code or binding is unsupported. Calling it exempt content would also assume that its loss has no downstream behavioral effects. The ten checks establish the link type and identity-export role, not an unobserved dependency.
7. **polkit-actions**: pkaction lists registered operations whose identities let services request authorization. Removing the registration removes the action's authorization lookup capability (S2.2-1/2). These effects span requesting services and the authority, so S2.2-7's only-inside-one-program exemption does not apply. All 136 MUST. No particular authorization default is inferred from the action name.

### Ten hand checks: accounts

- flatcar-9446ea4c2ea6643ef119fe94 — `root`; `raw/flatcar/raw/001-accounts.out:1`. Matches the stated rule.
- flatcar-1573a97b22b14bf0bc661037 — `bin`; `raw/flatcar/raw/001-accounts.out:5`. Matches the stated rule.
- flatcar-32c2519983ce1a3a69e200f6 — `sync`; `raw/flatcar/raw/001-accounts.out:9`. Matches the stated rule.
- flatcar-1a79c863917a6387494f4291 — `operator`; `raw/flatcar/raw/001-accounts.out:14`. Matches the stated rule.
- flatcar-8a63d6c9caea3d68b0d56ad8 — `syslog`; `raw/flatcar/raw/001-accounts.out:18`. Matches the stated rule.
- flatcar-e638ed82a9c48805caa94e12 — `dhcp`; `raw/flatcar/raw/001-accounts.out:22`. Matches the stated rule.
- flatcar-426a551faa38f300d21d663b — `polkitd`; `raw/flatcar/raw/001-accounts.out:26`. Matches the stated rule.
- flatcar-3509f4eef5a197145d96425f — `systemd-bus-proxy`; `raw/flatcar/raw/001-accounts.out:31`. Matches the stated rule.
- flatcar-b0f90d7ad88193bbd94691bb — `pcap`; `raw/flatcar/raw/001-accounts.out:35`. Matches the stated rule.
- flatcar-b18c5de7a54360092dbeab4d — `systemd-timesync`; `raw/flatcar/raw/001-accounts.out:39`. Matches the stated rule.
### Ten hand checks: groups

- flatcar-3e7acd7861265a9c89184e3b — `root`; `raw/flatcar/raw/002-groups.out:1`. Matches the stated rule.
- flatcar-c23346b48a0e548523a60586 — `user`; `raw/flatcar/raw/002-groups.out:8`. Matches the stated rule.
- flatcar-6d011a00027adadf3a3b9238 — `lp`; `raw/flatcar/raw/002-groups.out:16`. Matches the stated rule.
- flatcar-5660feb17732bd3e2d11db19 — `man`; `raw/flatcar/raw/002-groups.out:23`. Matches the stated rule.
- flatcar-53bebc1021f83702f71d74a5 — `lock`; `raw/flatcar/raw/002-groups.out:30`. Matches the stated rule.
- flatcar-42b94f5513549dd2f613cc26 — `messagebus`; `raw/flatcar/raw/002-groups.out:38`. Matches the stated rule.
- flatcar-4f9bee274fd71767025c64e9-occurrence-2 — `docker`; `raw/flatcar/raw/002-groups.out:45`. Matches the stated rule.
- flatcar-99dccc2b5ae11e3bbbc90ae6-occurrence-2 — `systemd-journal`; `raw/flatcar/raw/002-groups.out:52`. Matches the stated rule.
- flatcar-4bd27d3eeee4cd8cf97317e1 — `nobody`; `raw/flatcar/raw/002-groups.out:60`. Matches the stated rule.
- flatcar-6785b86ec58d3f7dd6d1ba25 — `systemd-timesync`; `raw/flatcar/raw/002-groups.out:67`. Matches the stated rule.
### Ten hand checks: identified-processes

- flatcar-05ec3cc0e86008caa5e18ce4 — `1`; `raw/flatcar/raw/076-process.out:1`. Matches the stated rule.
- flatcar-b21bd699f15a45f57b4d2e38 — `1276`; `raw/flatcar/raw/076-process.out:5`. Matches the stated rule.
- flatcar-c492be43fae992e473e5ae06 — `1283`; `raw/flatcar/raw/076-process.out:7`. Matches the stated rule.
- flatcar-d0784996137a79baac0fb07a — `1489`; `raw/flatcar/raw/076-process.out:11`. Matches the stated rule.
- flatcar-7db8ca67487a94e2455688e4 — `1544`; `raw/flatcar/raw/076-process.out:14`. Matches the stated rule.
- flatcar-0566f60f749051d42469de83 — `1569`; `raw/flatcar/raw/076-process.out:16`. Matches the stated rule.
- flatcar-646408228193545da4978a72 — `2399`; `raw/flatcar/raw/076-process.out:22`. Matches the stated rule.
- flatcar-9a3a3290224c2b5a725051f3 — `2417`; `raw/flatcar/raw/076-process.out:25`. Matches the stated rule.
- flatcar-75981e3939136dbb4684104a — `2672`; `raw/flatcar/raw/076-process.out:28`. Matches the stated rule.
- flatcar-5e6b491559756a37c2018295 — `2728`; `raw/flatcar/raw/076-process.out:32`. Matches the stated rule.
### Ten hand checks: unresolved-processes

- flatcar-14525dd9e4b7bbef650b9011 — `10`; `raw/flatcar/raw/076-process.out:2`. Matches the stated rule.
- flatcar-7d6150870c0e19813dac4f59 — `13`; `raw/flatcar/raw/076-process.out:9`. Matches the stated rule.
- flatcar-06716a3aeb699bd0659be487 — `1340`; `raw/flatcar/raw/076-process.out:10`. Matches the stated rule.
- flatcar-255713f7d7e2d3ddbb53e53c — `155`; `raw/flatcar/raw/076-process.out:15`. Matches the stated rule.
- flatcar-284cd771182864c383eb7a85 — `157`; `raw/flatcar/raw/076-process.out:17`. Matches the stated rule.
- flatcar-5f92333a6fb6dc32157f880f — `162`; `raw/flatcar/raw/076-process.out:19`. Matches the stated rule.
- flatcar-ba8d8237dfa44ef3a053444c — `165`; `raw/flatcar/raw/076-process.out:21`. Matches the stated rule.
- flatcar-55032763f65826e491b088f3 — `25`; `raw/flatcar/raw/076-process.out:26`. Matches the stated rule.
- flatcar-8185176747a03f9fcad21155 — `27`; `raw/flatcar/raw/076-process.out:29`. Matches the stated rule.
- flatcar-06462aa9434fec4fc20c04f0 — `28`; `raw/flatcar/raw/076-process.out:33`. Matches the stated rule.
### Ten hand checks: modules

- flatcar-5eaca0ced48f94ffcbed0deb — `intel_rapl_msr`; `raw/flatcar/raw/077-module.out:1`. Matches the stated rule.
- flatcar-36406d293bdf3501bb2a7f14 — `button`; `raw/flatcar/raw/077-module.out:9`. Matches the stated rule.
- flatcar-8272c1b46581420bee9a9d4c — `vsock_loopback`; `raw/flatcar/raw/077-module.out:17`. Matches the stated rule.
- flatcar-901e010e05818ed12feccd40 — `jbd2`; `raw/flatcar/raw/077-module.out:25`. Matches the stated rule.
- flatcar-24ffceada3289c7b7fd77bd7 — `net_failover`; `raw/flatcar/raw/077-module.out:33`. Matches the stated rule.
- flatcar-a73e6cae3c32fc7b0d8bb647 — `libiscsi`; `raw/flatcar/raw/077-module.out:41`. Matches the stated rule.
- flatcar-a36013da02441d8736791940 — `virtiofs`; `raw/flatcar/raw/077-module.out:49`. Matches the stated rule.
- flatcar-7bffe09a57f3ae7ee671c05b — `lzo_compress`; `raw/flatcar/raw/077-module.out:57`. Matches the stated rule.
- flatcar-be299f225b12dc74402a0081 — `sd_mod`; `raw/flatcar/raw/077-module.out:65`. Matches the stated rule.
- flatcar-ddf5d2cb6c580613985a76c8 — `crc32c_intel`; `raw/flatcar/raw/077-module.out:73`. Matches the stated rule.
### Ten hand checks: driver-links

- flatcar-f680f2ced5cbbbb98c0f7e6e — `/sys/devices/pnp0/00:05/driver`; `raw/flatcar/raw/078-driver.out:1`. Matches the stated rule.
- flatcar-f0515208c7470ebde5ef43b0 — `/sys/devices/pnp0/00:04/00:04:0/driver`; `raw/flatcar/raw/078-driver.out:4`. Matches the stated rule.
- flatcar-1f9163a7e2f94b85174294f1 — `/sys/devices/pnp0/00:00/driver`; `raw/flatcar/raw/078-driver.out:7`. Matches the stated rule.
- flatcar-3d0421dd3fe9ece92d5747d4 — `/sys/devices/platform/serial8250/serial8250:0/serial8250:0.1/driver`; `raw/flatcar/raw/078-driver.out:10`. Matches the stated rule.
- flatcar-56a7db23ffbc04132a032ab1 — `/sys/devices/platform/serial8250/driver`; `raw/flatcar/raw/078-driver.out:13`. Matches the stated rule.
- flatcar-b605afe2f102578e85a9a076 — `/sys/devices/pci0000:00/0000:00:04.0/virtio1/driver`; `raw/flatcar/raw/078-driver.out:17`. Matches the stated rule.
- flatcar-d02f30a66be6bd18bdc29171 — `/sys/devices/pci0000:00/0000:00:03.0/driver`; `raw/flatcar/raw/078-driver.out:20`. Matches the stated rule.
- flatcar-bc8c732576c2b08f4d089545 — `/sys/devices/pci0000:00/0000:00:01.1/driver`; `raw/flatcar/raw/078-driver.out:23`. Matches the stated rule.
- flatcar-075f446569106f7b41ed3158 — `/sys/devices/pci0000:00/QEMU0002:00/driver`; `raw/flatcar/raw/078-driver.out:26`. Matches the stated rule.
- flatcar-130d22dd45e97d035accd37e — `/sys/devices/LNXSYSTM:00/LNXPWRBN:00/driver`; `raw/flatcar/raw/078-driver.out:29`. Matches the stated rule.
### Ten hand checks: polkit-actions

- flatcar-5a4e50a2a12a6cc490521db3 — `io.systemd.ask-password.ask`; `raw/flatcar/raw/087-polkit-actions.out:1`. Matches the stated rule.
- flatcar-3fa90bb13762f44ad1c2d65d — `io.systemd.namespace-resource.allocate-user-namespace`; `raw/flatcar/raw/087-polkit-actions.out:16`. Matches the stated rule.
- flatcar-6d11af61ff27b74dc904b558 — `org.freedesktop.import1.import`; `raw/flatcar/raw/087-polkit-actions.out:31`. Matches the stated rule.
- flatcar-43e25ae4565df96178e06f6f — `org.freedesktop.login1.inhibit-block-sleep`; `raw/flatcar/raw/087-polkit-actions.out:46`. Matches the stated rule.
- flatcar-d9f112c1bbb41a4935544988 — `org.freedesktop.login1.reboot-multiple-sessions`; `raw/flatcar/raw/087-polkit-actions.out:61`. Matches the stated rule.
- flatcar-ef3f0c180371837766138b64 — `org.freedesktop.machine1.inspect-images`; `raw/flatcar/raw/087-polkit-actions.out:76`. Matches the stated rule.
- flatcar-1dc7a7dfc25ef1671e233671 — `org.freedesktop.network1.set-default-route`; `raw/flatcar/raw/087-polkit-actions.out:91`. Matches the stated rule.
- flatcar-09fa3a869650fb7efc8aba7b — `org.freedesktop.realmd.deconfigure-realm`; `raw/flatcar/raw/087-polkit-actions.out:106`. Matches the stated rule.
- flatcar-975def8ff99e2d3e1c557d82 — `org.freedesktop.resolve1.set-llmnr`; `raw/flatcar/raw/087-polkit-actions.out:121`. Matches the stated rule.
- flatcar-d466d4b191cbefe0b38d2922 — `org.freedesktop.timesync1.set-runtime-servers`; `raw/flatcar/raw/087-polkit-actions.out:136`. Matches the stated rule.

## Individual remaining decisions

The eight ports and three links were checked individually against 079-port.out and 084-networkd.out. UDP receive endpoints and TCP listeners are open network endpoints under S2.2-15; local-only binding is not an exemption. Removing lo, eth0, or eth1 prevents traffic through that interface (S2.2-2). No assertion about a saved wireless network follows.

The single authorized_keys row is explicitly covered by S2.2-15. Four sudo permission lines all authorize execution as any account, including superuser; password prompting does not change the right's recording requirement.

Five loaded polkit scripts were read in 114, 115, 117, 118, and 119-access-rule outputs. Their actual JavaScript functions grant cross-service operations or select administrative identity; S2.2-10/13 apply to code, with S2.2-1 additionally establishing system effects. The 116 example has a non-loaded .example suffix and describes how to enable it; it is instructional content (S2.2-4). The three access-directory placeholders and network-directory placeholder are empty, as the corresponding raw files establish. Removing those files removes only their placeholder content, not a rule. No classification uses the misleading access-rule or saved-network inventory labels.

The system-image row represents the mounted operating-system image, rather than only the os-release text used to identify it. The /usr mounts and identified executable paths establish its role in supplying system programs (S2.2-1/2/9). It is not classified as if every file in the image were a program.

Each SSH directive was individually assigned in part-flatcar.ssh-map.tsv after reading its value in 085-ssh-access.out. That map records what the directive does and the applicable reasoning category; the script only joins these completed judgments to occurrence IDs. The table below records every individual directive occurrence and its resulting decision. Repeated AcceptEnv rows all select environment variables passed to separate session processes. Ten distinct repetitions were checked, listed after the table. The four HostKey occurrences select the SSH server's identity rather than keys authorizing login to an account, and were each reviewed. The rules are effective values exposed by sshd, not purported physical source lines; redundant source-line removal is not assumed to remove an effective value.

| ID | Directive or object | Decision |
| --- | --- | --- |
| flatcar-110d66925baf0a6a1a4bd6f7 | ssh-access:port | MUST |
| flatcar-0918da7edd64a48b206ff7dd | ssh-access:AddressFamily | MUST |
| flatcar-4ef274c21fc9bb60b53020d4 | ssh-access:listenaddress | MUST |
| flatcar-7f1d874c386f108a682a21b2 | ssh-access:listenaddress | MUST |
| flatcar-c188897f093c5117ff868a85 | ssh-access:UsePAM | MUST |
| flatcar-f56e165ce3982c8e4e92a18f | ssh-access:PAMServiceName | MUST |
| flatcar-c943ee7616e643f7ea270f07 | ssh-access:LoginGraceTime | NOT |
| flatcar-d9080f1b18cd7b9d52ee5bf4 | ssh-access:X11DisplayOffset | NOT |
| flatcar-86f401952aadcc05301211d3 | ssh-access:MaxAuthTries | NOT |
| flatcar-4e34a3c8592ce4ab88dea652 | ssh-access:MaxSessions | MUST |
| flatcar-213982f6b503a2e81751aafb | ssh-access:ClientAliveInterval | NOT |
| flatcar-227f50458b0ebd69dc62a385 | ssh-access:ClientAliveCountMax | NOT |
| flatcar-5b1b239bd3ddc18fe021389c | ssh-access:RequiredRSASize | NOT |
| flatcar-27deb26d2fe4af2f7297e996 | ssh-access:StreamLocalBindMask | MUST |
| flatcar-515a520bcf3a3b16d84f3a90 | ssh-access:UnusedConnectionTimeout | NOT |
| flatcar-1371df286070ed7f42e749cd | ssh-access:PermitRootLogin | MUST |
| flatcar-c2ecb15cf6b0b94511e9a53b | ssh-access:IgnoreRhosts | MUST |
| flatcar-611195fc9200fcb530a884d1 | ssh-access:IgnoreUserKnownHosts | MUST |
| flatcar-c3888d88a98301bd3b9b3d45 | ssh-access:HostbasedAuthentication | MUST |
| flatcar-d5eb749a8a3760e6fbca4b71 | ssh-access:HostbasedUsesNameFromPacketOnly | NOT |
| flatcar-4c7581a0eac8b63e8e6acd35 | ssh-access:PubkeyAuthentication | MUST |
| flatcar-00fadc015680822bdf525452 | ssh-access:KerberosAuthentication | MUST |
| flatcar-b861218844402b2dfa2ca967 | ssh-access:KerberosOrLocalPasswd | MUST |
| flatcar-5d80395a659e8419162b17af | ssh-access:KerberosTicketCleanup | MUST |
| flatcar-a2f43615467461d74cd71b86 | ssh-access:GSSAPIAuthentication | MUST |
| flatcar-9a331615508f9e7abf819565 | ssh-access:GSSAPICleanupCredentials | MUST |
| flatcar-fb371a938b48ad8f2110ae85 | ssh-access:GSSAPIDelegateCredentials | MUST |
| flatcar-e70e05e92622cbcc2e3b4494 | ssh-access:GSSAPIStrictAcceptorCheck | NOT |
| flatcar-a3eed61881b3e8fcdf504d50 | ssh-access:PasswordAuthentication | MUST |
| flatcar-e04ac31632b8fb0ca58fa72c | ssh-access:KbdInteractiveAuthentication | MUST |
| flatcar-e2a1ca84900130e6d25f5b4f | ssh-access:PrintMotd | NOT |
| flatcar-f10b6f542206d251faca0dda | ssh-access:PrintLastLog | NOT |
| flatcar-3879c5635f8487590fbc98a3 | ssh-access:X11Forwarding | HOLE |
| flatcar-bb00b6291ec9cf7304e52e97 | ssh-access:X11UseLocalhost | MUST |
| flatcar-499e4d5af6b36b88abad464a | ssh-access:PermitTTY | MUST |
| flatcar-939d7a7b0d01b67c8e427d2d | ssh-access:PermitUserRC | MUST |
| flatcar-5709df13d448daefda9ad39a | ssh-access:StrictModes | MUST |
| flatcar-f659cb06ab962a0351f51a9a | ssh-access:TCPKeepAlive | NOT |
| flatcar-944dcf74467877c671f6168f | ssh-access:PermitEmptyPasswords | MUST |
| flatcar-dea33bab44e30338b734f77e | ssh-access:Compression | NOT |
| flatcar-7cf14d58ec5443f0ebc93131 | ssh-access:GatewayPorts | MUST |
| flatcar-89948b47698319927d6ad711 | ssh-access:UseDNS | NOT |
| flatcar-89f4f8b56925831292371d1e | ssh-access:AllowTcpForwarding | HOLE |
| flatcar-d6632bedd852052ec33e4ed0 | ssh-access:AllowAgentForwarding | HOLE |
| flatcar-c60f2348aa07e08d10550467 | ssh-access:DisableForwarding | HOLE |
| flatcar-8da96f306d0863e6bc6f60ca | ssh-access:AllowStreamLocalForwarding | HOLE |
| flatcar-9e9c53cba1dcb223a5624b61 | ssh-access:StreamLocalBindUnlink | MUST |
| flatcar-71cf53f072fdfe8ca41a601d | ssh-access:FingerprintHash | NOT |
| flatcar-75c6a8db40c3f9b508e5f565 | ssh-access:ExposeAuthInfo | MUST |
| flatcar-f7c7fedce0e2f18bdceec831 | ssh-access:RefuseConnection | MUST |
| flatcar-27668ef22c0c53aded70245e | ssh-access:PidFile | HOLE |
| flatcar-9739dd9cd83e5be1fde79e66 | ssh-access:ModuliFile | NOT |
| flatcar-34324cc03d257717c37ae293 | ssh-access:XAuthLocation | MUST |
| flatcar-b0129c4b9296d9b55bc5be05 | ssh-access:Ciphers | NOT |
| flatcar-fde5c291e244abd227a76f90 | ssh-access:Macs | NOT |
| flatcar-62ffddc8f738797e215201aa | ssh-access:Banner | NOT |
| flatcar-01a4e12d4f4da587ea2a95fd | ssh-access:ForceCommand | MUST |
| flatcar-45ae9435aef1e87782ed21d2 | ssh-access:ChrootDirectory | MUST |
| flatcar-44c137335a4d9727246bae27 | ssh-access:TrustedUserCAKeys | MUST |
| flatcar-80e5d5c583b94f700cabd885 | ssh-access:SecurityKeyProvider | NOT |
| flatcar-04d20d905cf48789916d65e4 | ssh-access:AuthorizedPrincipalsFile | MUST |
| flatcar-55ce7a4c373a37e87f1c5ecb | ssh-access:VersionAddendum | NOT |
| flatcar-d34ed07eb863e12ae87f1da2 | ssh-access:AuthorizedKeysCommand | MUST |
| flatcar-5fbfdeb2e75c8a8fd2ae6155 | ssh-access:AuthorizedKeysCommandUser | MUST |
| flatcar-7b727b940ba1f23b98c0b1d0 | ssh-access:AuthorizedPrincipalsCommand | MUST |
| flatcar-19bb7a554c3539abcd522387 | ssh-access:AuthorizedPrincipalsCommandUser | MUST |
| flatcar-9192031ed725e81ab6233bef | ssh-access:HostKeyAgent | NOT |
| flatcar-4f36872050a8e8c8457d7318 | ssh-access:KexAlgorithms | NOT |
| flatcar-8b8029cbafe7ea635a895b25 | ssh-access:CASignatureAlgorithms | NOT |
| flatcar-4723118762625a26a2666dc7 | ssh-access:HostbasedAcceptedAlgorithms | NOT |
| flatcar-984aa056a7da603f21af6cec | ssh-access:HostKeyAlgorithms | NOT |
| flatcar-d5c88e5e30c0888a6ca38316 | ssh-access:PubkeyAcceptedAlgorithms | NOT |
| flatcar-f8b927b906391312b6e57dad | ssh-access:SshdSessionPath | MUST |
| flatcar-1f7fcb5f10b8cfb81a096d03 | ssh-access:SshdAuthPath | MUST |
| flatcar-0e07a161aa75165dc2ddddc1 | ssh-access:PerSourcePenaltyExemptList | NOT |
| flatcar-530f3664de581de1e24ccef1 | ssh-access:LogLevel | NOT |
| flatcar-a933383d00b0e173071825a6 | ssh-access:SyslogFacility | NOT |
| flatcar-a907f4e61106ab3b830ee0c4 | ssh-access:AuthorizedKeysFile | MUST |
| flatcar-4ffd82fa38286ea6436e1a9e | ssh-access:HostKey | NOT |
| flatcar-57f829c278e3a32ae67a5421 | ssh-access:HostKey | NOT |
| flatcar-c488b0dd3a035637e0c2c96d | ssh-access:HostKey | NOT |
| flatcar-155c77b5a3f4cbe62a885b35 | ssh-access:HostKey | NOT |
| flatcar-68459936ec84b76ae310f82e | ssh-access:AcceptEnv | MUST |
| flatcar-e11dc946353e182416f820ab | ssh-access:AcceptEnv | MUST |
| flatcar-14be86e4d58767a17ef66dae | ssh-access:AcceptEnv | MUST |
| flatcar-ccb3b228b9fb0eeab9b4df89 | ssh-access:AcceptEnv | MUST |
| flatcar-377df8f2ef3f7f8bff5c3d22 | ssh-access:AcceptEnv | MUST |
| flatcar-faa0d984fc169a0430fedf1e | ssh-access:AcceptEnv | MUST |
| flatcar-ef3905f9ec3722fbf9cde738 | ssh-access:AcceptEnv | MUST |
| flatcar-c7cd4ec65c79b30667e89512 | ssh-access:AcceptEnv | MUST |
| flatcar-e27b087e332cdbf4affe382e | ssh-access:AcceptEnv | MUST |
| flatcar-a062861c82d2d599a2dcc52d | ssh-access:AcceptEnv | MUST |
| flatcar-4f9c6b06d8f7ad5939457e11 | ssh-access:AcceptEnv | MUST |
| flatcar-fcc568ae504c7531844f5402 | ssh-access:AcceptEnv | MUST |
| flatcar-ae12a7d079de6a3b01101ee1 | ssh-access:AcceptEnv | MUST |
| flatcar-8f1e34c9370c68548ff0212b | ssh-access:AcceptEnv | MUST |
| flatcar-79aec2d054209a4bc4cb1de7 | ssh-access:AcceptEnv | MUST |
| flatcar-6e2defe63b0e0b3707d4af82 | ssh-access:AcceptEnv | MUST |
| flatcar-5e9df6cee09cb36ae89e4507 | ssh-access:AuthenticationMethods | MUST |
| flatcar-70171fb23917b95641bb05b4 | ssh-access:ChannelTimeout | NOT |
| flatcar-63f55f60c51fb4d3434fa466 | ssh-access:subsystem | MUST |
| flatcar-4584b62a420ca72191696ee8 | ssh-access:maxstartups | NOT |
| flatcar-ac8377323f0a629da39fb800 | ssh-access:persourcemaxstartups | NOT |
| flatcar-cde34ae0a06e9c836b514587 | ssh-access:persourcenetblocksize | NOT |
| flatcar-dcf198770a303b4980a2c3bd | ssh-access:PermitTunnel | MUST |
| flatcar-f2dc5fd0556d39a9179c707c | ssh-access:ipqos | NOT |
| flatcar-e6eae5d0a7cff82c1f261edf | ssh-access:rekeylimit | NOT |
| flatcar-092805b1287f27a3cbe629d2 | ssh-access:permitopen | HOLE |
| flatcar-b237c241469fe66ec2043c43 | ssh-access:permitlisten | MUST |
| flatcar-d25a28375ccd3d677307f4c4 | ssh-access:PermitUserEnvironment | MUST |
| flatcar-0bdf73041c7a3ae7fca3aeb0 | ssh-access:pubkeyauthoptions | NOT |
| flatcar-e797f025f554c660f5d426c4 | ssh-access:persourcepenalties | NOT |
| flatcar-480b364e0b40b0d8496c9960 | sudo-access:5 | MUST |
| flatcar-13853be1586d85a3431f6d8d | sudo-root:5 | MUST |
| flatcar-d0def0f9090d3e5e462a0e09 | sudo-root:6 | MUST |
| flatcar-eac163ea2bf938616e4c57fc | sudo-user:5 | MUST |
| flatcar-00a172f9be4f7fb57422e3c0 | /usr/share/polkit-1/rules.d/empower.rules | MUST |
| flatcar-d53111470b3a1e4a5d1bc7b1 | /usr/share/polkit-1/rules.d/systemd-networkd.rules | MUST |
| flatcar-787bb8e7cdfb15a85476f6a1 | /usr/share/polkit-1/rules.d/10-systemd-logind-root-ignore-inhibitors.rules.example | NOT |
| flatcar-15ba5068cd79ebbb2cbfa7c6 | /usr/share/polkit-1/rules.d/sssd-realmd.rules | MUST |
| flatcar-29b1443a7d9cde03252e5b0e | /usr/share/polkit-1/rules.d/sssd-pcsc.rules | MUST |
| flatcar-77c4aad4b1ed58435970beb1 | /usr/share/polkit-1/rules.d/50-default.rules | MUST |
| flatcar-2988e2c9c125829707f86771 | /etc/pam.d/.keep_sys-libs_pam-0 | NOT |
| flatcar-95a29987a00d50b5e0c6efdb | /etc/polkit-1/rules.d/.keep_sys-auth_polkit-0 | NOT |
| flatcar-37f513275dbc89536b67600d | /etc/sudoers.d/.keep_app-admin_sudo-0 | NOT |

Ten hand-checked AcceptEnv repetitions (variable names were inspected individually):

- flatcar-68459936ec84b76ae310f82e — AcceptEnv LANG. Passed to session processes, so S2.2-1/2 apply.
- flatcar-e11dc946353e182416f820ab — AcceptEnv LC_ALL. Passed to session processes, so S2.2-1/2 apply.
- flatcar-14be86e4d58767a17ef66dae — AcceptEnv LC_COLLATE. Passed to session processes, so S2.2-1/2 apply.
- flatcar-ccb3b228b9fb0eeab9b4df89 — AcceptEnv LC_CTYPE. Passed to session processes, so S2.2-1/2 apply.
- flatcar-377df8f2ef3f7f8bff5c3d22 — AcceptEnv LC_MESSAGES. Passed to session processes, so S2.2-1/2 apply.
- flatcar-faa0d984fc169a0430fedf1e — AcceptEnv LC_MONETARY. Passed to session processes, so S2.2-1/2 apply.
- flatcar-ef3905f9ec3722fbf9cde738 — AcceptEnv LC_NUMERIC. Passed to session processes, so S2.2-1/2 apply.
- flatcar-c7cd4ec65c79b30667e89512 — AcceptEnv LC_TIME. Passed to session processes, so S2.2-1/2 apply.
- flatcar-e27b087e332cdbf4affe382e — AcceptEnv LANGUAGE. Passed to session processes, so S2.2-1/2 apply.
- flatcar-a062861c82d2d599a2dcc52d — AcceptEnv LC_ADDRESS. Passed to session processes, so S2.2-1/2 apply.

## Review correction: driver-link evidence

The original 29 driver-link MUST decisions inferred an operational dependency from the availability of driver discovery. Review found that inference unsupported: the snapshot does not demonstrate actual consumers, and the links are not the binding or executing code. Each is now UNKNOWN pending evidence of its complete operational role. The exact IDs are all L1:driver input rows; the integration audit preserves each original decision. No new claim that the links are necessarily exempt informational content is made.


---

# Service and timer classification

Scope: 459 rows of kinds L1:user-service, L1:user-timer, L1:user-unit-file, L1:service, L1:timer and L1:unit-file. Only the assigned input, its raw inventory, COMMON.md, TEXT.md, SENTENCES.md and primary public documentation were consulted. No removal was performed. Inventory conclusions were ignored.

## Exact decisive text

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S3-2: “If what the object does remains unknown, the case yields ?.”

## Primary documentation

- https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html: “A unit configuration file whose name ends in ".service" encodes information about a process controlled and supervised by systemd.” Service units configure supervision of processes; they are not themselves executable programs.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html: “A unit configuration file whose name ends in ".timer" encodes information about a timer controlled and supervised by systemd, for timer-based activation.” The matching unit, normally a service, is activated when the timer elapses.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html: “Units can be aliased (have an alternative name), by creating a symlink from the new name to the existing name”. Such names supply activation entry points. Templates provide definitions for instances.
- https://www.freedesktop.org/software/systemd/man/latest/systemctl.html: “List units that systemd currently has in memory.” The list can contain references lacking definitions; list-unit-files instead lists installed definitions. Inactive is an activation state, not evidence that an installed definition is absent.

## Homogeneous rule R1

Apply MUST to an installed service/timer definition, loaded service, or timer activation entry. Each configures, names or schedules managed activation of a separate service process. Removal removes that managed activation capability, named entry point or schedule (S2.2-1, S2.2-2). Inactive, disabled and template entries still supply capabilities; the task asks whether objects must be recorded, not whether currently active.

These files are settings under S2.2-13, not code merely because an ExecStart value names code. S2.2-7 requires settings to be in force **only inside** one program. Supervision, process activation and the schedule of a separately executing service extend outside the manager. Therefore R1 does not invoke that exemption. Reading values in one parser alone does not establish that their force is only inside it. No precedence between sentences has been invented. A logging or cache-building service is neither its logs nor its cache.

The rule covers service definitions, aliases and timers as one homogeneous kind: controls of external service activation. The script varies the factual description for the documented mechanism without changing the decision rule. The raw inventory scripts confirm list-units, list-timers and list-unit-files as the source commands.

Ten hand checks against the actual cited raw lines and documented unit semantics:

| ID | Checked property |
| --- | --- |
| flatcar-36902b7d91efb89edf0757e2 | Loaded inactive user message-bus service; managed process remains available. |
| flatcar-905e902eefa63160a0ddd48c | Active exited user file-creation service; service activation has filesystem effects. |
| flatcar-2db3435e61f3b7410b61dfcc | User import-service alias; alternative service activation name. |
| flatcar-194640cbe88827831ab4807e | Disabled user p11-kit service definition; disabled is not absence. |
| flatcar-e2392fe58e7be6849e1a44d1 | Static password-request service template; defines parameterized activation. |
| flatcar-19a0e1d4f8287374c6f606d3 | Disabled user cleanup timer definition; supplies scheduling capability. |
| flatcar-c1b32845646e0963306d2ee5 | Running container runtime service; supervised external process. |
| flatcar-ed19a98eeeca14c92573cd16 | Exited linker-cache rebuild service; service is distinct from cache content. |
| flatcar-081049d311fe2c1986619bff | System virtual-terminal service alias template; named activation capability. |
| flatcar-35f9e9b83152b2aff0bca0de | Disabled filesystem-scrubbing timer definition; scheduling rather than file content. |

## Individual unresolved references

The following five service rows each report `not-found inactive dead`. Unlike installed definitions, these are unresolved manager references. No definition or dependency graph is supplied. The generic purpose of a similarly named upstream unit cannot establish what this absent local definition or live reference contributes. Public manager documentation establishes the reference status, but not the individual dependency effects. Each is UNKNOWN under S3-2, not a claim that absent services run or that absence is a textual hole.

- flatcar-f79b464b166dee8a6edf7235: missing plymouth-quit-wait definition; raw/flatcar/raw/073-service.out:46.
- flatcar-db3479ac6a4a75602d47f30f: missing plymouth-start definition; raw/flatcar/raw/073-service.out:47.
- flatcar-4ebcb6edd91450f4eb5aa735: missing syslog definition; raw/flatcar/raw/073-service.out:57.
- flatcar-88464f8a7422c36c077c2907: missing systemd-quotacheck definition; raw/flatcar/raw/073-service.out:93.
- flatcar-ee9d2efa3352fec63a32b097: missing systemd-tpm2-setup-early definition; raw/flatcar/raw/073-service.out:111.

## Validation

The append-only build script preserves prior completed rows and flushes each new row. It verifies exact assigned ID set and count, unique IDs, allowed decisions and field word limits. Result: 454 MUST, 5 UNKNOWN; total 459. No group rows occur in this subset; the members field contains one inventory line per object.


---

# Executable-candidate classification notes

Scope: 466 assigned rows. The inventory label is ignored. `../in/raw/flatcar/raw/113-code-candidates.sh` selects executable permissions, shebangs, or shell filenames. Its output contains paths, not file contents. Therefore the candidate list is not itself proof of executable code. Public primary documentation and program source identify the functions below. No objects were removed or executed.

## Deciding sentences (exact quotations)

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;

- **S3-2** If what the object does remains unknown, the case yields ?.

## Primary documentation

- https://www.gnu.org/software/grub/manual/grub/grub.html: “Everything else in GRUB resides in dynamically loadable modules.” The image-file discussion identifies `.mod` files as GRUB native modules. They are executable extensions, not merely files marked executable.
- https://raw.githubusercontent.com/rhboot/grub2/master/grub-core/kern/dl.c: `mod->init = (void (*) (grub_dl_t)) sym->st_value;`. Native module symbols are resolved and relocated into GRUB; their initialization code has GRUB's execution privileges.
- https://raw.githubusercontent.com/flatcar/scripts/main/build_library/grub_install.sh: “# Generate a memdisk containing the appropriately generated grub.cfg.” and “# boot.img gets manipulated by grub-bios-setup”. The installer copies/compresses module and list files, embeds load.cfg and grub.cfg.tar, generates core.img/EFI/Xen executables, copies shim and MokManager, and saves patched MBR bytes for restoration. Its target-specific layout matches the inventory. These are semantic identification sources, not proof that each optional module ran during inventory.
- https://raw.githubusercontent.com/rhboot/grub2/master/grub-core/Makefile.am: “# generate global module dependencies list”. The `.lst` rules generate name-to-module maps and module lists for commands, filesystems, partitions, terminals, device-tree drivers, video, cryptography, and dependencies. These are values, not native code.
- https://raw.githubusercontent.com/flatcar/scripts/main/build_library/menu.lst: `kernel  /xen/pvboot-x86_64.elf`. This command selects the Xen bootloader rather than an interface preference.
- https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files: “it reads and executes commands from”. The documented startup/logout paths establish execution by Bash; these files are specifically covered by S2.2-10.
- https://www.gnu.org/software/gawk/manual/html_node/Shell-Startup-Files.html: “containing functions to aid in manipulating the AWKPATH and AWKLIBPATH environment variables.” This identifies both shell drop-ins as executable shell definitions.
- https://raw.githubusercontent.com/gentoo/gentoo/master/app-shells/bash/files/profile.d/00-prompt-command.sh: `eval 'PROMPT_COMMAND=()'`. This drop-in executes code to initialize the prompt-command array, rather than supplying a passive setting.
- https://man7.org/linux/man-pages/man8/useradd.8.html: “create the new user's home directory and copy initial files.” The upstream useradd manual establishes the skeleton's copying role but does not reveal the actual contents of these three inventoried templates.

## Homogeneous rule M: native GRUB modules

Apply only to the 427 `.mod` files in the two installed GRUB platform directories. Documentation establishes that these are loadable native code, and the Flatcar installer specifically places compressed modules there. S2.2-10 requires code executed with its executing program's privileges. GRUB's native module loader supplies those privileges without interface confinement. The same rule covers filesystem, cryptographic, device, and utility modules; no claim that every module was loaded at inventory time is needed to decide the recording requirement. This classification addresses the inventoried computer, not a surrounding virtualization host.

Ten manually checked input rows (checked individual pathname, platform directory, membership record, presence in candidate output, and `.mod` semantic match):

- flatcar-7448f108721fc286a373fef3: `/boot/flatcar/grub/i386-pc/acpi.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-1c84704d39e7c2374054ce7b: `/boot/flatcar/grub/i386-pc/adler32.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-d18ed0114c49adbad77896d5: `/boot/flatcar/grub/i386-pc/affs.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-963a17b6f6604bdc51a9a125: `/boot/flatcar/grub/i386-pc/datehook.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-06f005b6405f60df4ac8a3d1: `/boot/flatcar/grub/i386-pc/gcry_whirlpool.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-a8ba5105a035f510e7ad2666: `/boot/flatcar/grub/i386-pc/luks2.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-17f994f3de9765795d080467: `/boot/flatcar/grub/i386-pc/pxe.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-7bc4d8cd80654c2d82ec3be2: `/boot/flatcar/grub/i386-pc/xnu.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-3845c4685cf7d3661ddec733: `/boot/flatcar/grub/x86_64-xen/gcry_serpent.mod` — native module in the documented installed module directory; rule M applies.
- flatcar-9c9c9b222a2f193273b2964a: `/boot/flatcar/grub/x86_64-xen/zstd.mod` — native module in the documented installed module directory; rule M applies.

## Homogeneous rule L: GRUB value lists

Apply only to 18 platform `.lst` rows, excluding the boot menu `menu.lst`. Their generation rules establish values rather than executable code (S2.2-13). These module-selection values configure only GRUB; S2.2-7 explicitly exempts settings confined to one program. The general capability rule does not defeat that explicit exemption. Decision: NOT.

Ten manually checked input rows (all nine list types on BIOS, plus the corresponding Xen command map):

- flatcar-e5869975107dd1606ec51809: `/boot/flatcar/grub/i386-pc/command.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-1d509ff72f6ebda06a74f24b: `/boot/flatcar/grub/i386-pc/crypto.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-a57831f044e17b543418e523: `/boot/flatcar/grub/i386-pc/fdt.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-7904e536689dfb4920c065e2: `/boot/flatcar/grub/i386-pc/fs.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-85dcb992af130d2188c69228: `/boot/flatcar/grub/i386-pc/moddep.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-0a3e3cfe3ac4624ab107909d: `/boot/flatcar/grub/i386-pc/partmap.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-0e6c4297e1c7ee27ea640213: `/boot/flatcar/grub/i386-pc/parttool.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-cbb532e843582afa0c475968: `/boot/flatcar/grub/i386-pc/terminal.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-772bb06922e0fe319ced9341: `/boot/flatcar/grub/i386-pc/video.lst` — list type individually matched to its upstream generation rule; rule L applies.
- flatcar-5c299521082131f80720b170: `/boot/flatcar/grub/x86_64-xen/command.lst` — list type individually matched to its upstream generation rule; rule L applies.

## Remaining rows: individual decisions

Each remaining row has an individual rationale and documentation URL in the TSV. No additional homogeneous rule is applied.

- flatcar-27a9bbed5ceb9ff7953cd293 (.bash_logout): MUST; S2.2-10.
- flatcar-198385181ff22d0d558e1c21 (.bash_profile): MUST; S2.2-10.
- flatcar-ea39cc839176e502604c2907 (.bashrc): MUST; S2.2-10.
- flatcar-37041f258c25177429d46e43 (load.cfg): UNKNOWN; S2.2-10,S2.2-13,S3-2.
- flatcar-334558d67d5b17a1a48f6580 (core.img): MUST; S2.2-9.
- flatcar-fdce05a11eb6580b746ee991 (boot.img): MUST; S2.2-9.
- flatcar-14a05bb2f57c924ebf089310 (mbr.bin): HOLE; S2.2-1,S2.2-2,S2.2-6.
- flatcar-13aed24415f036f8d1bd6cba (grub.cfg.tar): UNKNOWN; S2.2-10,S2.2-13,S3-2.
- flatcar-f0f44dff73a1ee2661dd6c9b (load.cfg): UNKNOWN; S2.2-10,S2.2-13,S3-2.
- flatcar-844d2924dea652c3192b9304 (load.cfg): UNKNOWN; S2.2-10,S2.2-13,S3-2.
- flatcar-b59146c6ef774b9d1e7896fc (grubx64.efi): MUST; S2.2-9.
- flatcar-a9f169a0287b9bcda5746db1 (mmx64.efi): MUST; S2.2-9.
- flatcar-a4945760c4931e2ae3f22053 (bootx64.efi): MUST; S2.2-9.
- flatcar-24dc8be7f77d9dae39bfed08 (pvboot-x86_64.elf): MUST; S2.2-9.
- flatcar-029508e7f993a11ad8cbd8d4 (menu.lst): MUST; S2.2-1,S2.2-2,S2.2-13.
- flatcar-39b74ce4ac43077561ded8b6 (00-prompt-command.sh): MUST; S2.2-10,S2.2-13.
- flatcar-3415242185dd23520c96ddd0 (gawk.csh): MUST; S2.2-10.
- flatcar-d7a371cb24bd93a5b6087625 (gawk.sh): MUST; S2.2-10.
- flatcar-e99d01540d33e0f07a650d86 (.bash_logout): UNKNOWN; S3-2.
- flatcar-20ac2453d5813a360f4d5a48 (.bash_profile): UNKNOWN; S3-2.
- flatcar-b7763493bf96dc9f0d8a962a (.bashrc): UNKNOWN; S3-2.

## Correction audit

Review rechecked five objects after the initial 466-row completion. Their initial decisions were MUST. For load.cfg (three rows) and grub.cfg.tar, the initial rationale incorrectly transferred the embedded copy's execution to the distinct stored source object. They are now UNKNOWN: build-time use is documented, but no captured evidence establishes later consumers of the installed copies. For mbr.bin, the initial removal rationale assumed recovery capability alone decided the case. It is now HOLE: the snapshot also records past bytes, and S2.2-6 does not delimit whether recovery snapshots qualify. This is a scope question about the explicit exemption, not an invented precedence rule.

Corrected IDs:

- flatcar-37041f258c25177429d46e43: MUST → UNKNOWN.
- flatcar-14a05bb2f57c924ebf089310: MUST → HOLE.
- flatcar-13aed24415f036f8d1bd6cba: MUST → UNKNOWN.
- flatcar-f0f44dff73a1ee2661dd6c9b: MUST → UNKNOWN.
- flatcar-844d2924dea652c3192b9304: MUST → UNKNOWN.

Additional exact sentence: S2.2-6: “records of the past—logs, history;”

## Validation

The finish script verifies 466 rows, equal input/output ID sets, uniqueness, permitted decisions, and field word limits. The correction script records the explicit five-row correction. Current totals: MUST 440; NOT 18; HOLE 1; UNKNOWN 7; MIXED 0. No group rows occur in this assigned kind.

## Rule L correction audit

The 18 list rows originally received HOLE, citing S2.2-1,S2.2-7,S2.2-13, because their internal settings affected bootloader capabilities. Review rejected that rationale: S2.2-7 already explicitly exempts settings confined to one program; general capability effects establish no additional ambiguity. All 18 now receive NOT under S2.2-7,S2.2-13. The ten individual checks above remain valid. Native modules and the five earlier individual corrections are unchanged.

- flatcar-e5869975107dd1606ec51809: HOLE → NOT.
- flatcar-1d509ff72f6ebda06a74f24b: HOLE → NOT.
- flatcar-a57831f044e17b543418e523: HOLE → NOT.
- flatcar-7904e536689dfb4920c065e2: HOLE → NOT.
- flatcar-85dcb992af130d2188c69228: HOLE → NOT.
- flatcar-0a3e3cfe3ac4624ab107909d: HOLE → NOT.
- flatcar-0e6c4297e1c7ee27ea640213: HOLE → NOT.
- flatcar-cbb532e843582afa0c475968: HOLE → NOT.
- flatcar-772bb06922e0fe319ced9341: HOLE → NOT.
- flatcar-5c299521082131f80720b170: HOLE → NOT.
- flatcar-6cf96cf62a5c025915a5304f: HOLE → NOT.
- flatcar-169971c66f71b58b99c4405f: HOLE → NOT.
- flatcar-835444a1e99d596b1bb77428: HOLE → NOT.
- flatcar-452c72fd408533fcf34dd6a6: HOLE → NOT.
- flatcar-77796baf3bc41ca5cf2c1fd9: HOLE → NOT.
- flatcar-87d65840836e70d225b4fbf3: HOLE → NOT.
- flatcar-974618a7c5fc08b7d44dc4e8: HOLE → NOT.
- flatcar-a38dc4a119724473b97a7092: HOLE → NOT.


---

# Stored objects: independent classification notes

Scope: only L2:stored-outside-packages rows. Inventory labels were disregarded. The raw filesystem snapshot stores path, type, mode, uid, gid, and link target in six NUL-delimited fields. It does not contain arbitrary file contents. Directories listed as members are considered with their contents; grouping never implies homogeneous membership. No objects were removed. UNKNOWN identifies unavailable actual consumers or contents, not a defect concerning system-design treatment of state.

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Rule U: udev link-stack entries
For each group strictly under /run/udev/links/, every member is the recorded priority/device association used when udev chooses the target of a device alias. Removing it eliminates that candidate during subsequent link updates. Device alias behavior is therefore dependent on these objects (S2.2-1, S2.2-2), and they are neither historical records nor a speed-only cache. MUST. This is runtime device-management state, not a user setting confined to an application.
Source: https://raw.githubusercontent.com/systemd/systemd/main/src/udev/udev-node.c
Exact quote: “This reads priority and device node from the symlink under /run/udev/links/ directory.”
The function stack_directory_find_prioritized_devnode selects among these candidates; link_search_and_update deletes the alias when no reference remains.
Hand-checked 10 groups against both raw type/target and the input members:
- flatcar-4c7805e498936e7ae1a37d41: /run/udev/links/cdrom; -100:/dev/sr0. All members are priority/device links; the multi-candidate group also fits.
- flatcar-bd0133edb221e27985df2227: /run/udev/links/disk\x2fby-designator\x2fesp; 0:/dev/vda1. All members are priority/device links; the multi-candidate group also fits.
- flatcar-10a0bb9519b190ffc2487d7d: /run/udev/links/disk\x2fby-id\x2fata-QEMU_DVD-ROM_QM00003; -100:/dev/sr0. All members are priority/device links; the multi-candidate group also fits.
- flatcar-8d598cebee188f04355c53a0: /run/udev/links/disk\x2fby-label\x2fEFI-SYSTEM; 0:/dev/vda1. All members are priority/device links; the multi-candidate group also fits.
- flatcar-bf1a27b86060d3ef4c7eb4fc: /run/udev/links/disk\x2fby-partlabel\x2froot-x86-64; 0:/dev/loop2p1, 0:/dev/loop7p1, 0:/dev/loop1p1, 0:/dev/loop3p1. All members are priority/device links; the multi-candidate group also fits.
- flatcar-5a6a824d018649210bec1e4f: /run/udev/links/disk\x2fby-path\x2fpci-0000:00:01.1-ata-2; -100:/dev/sr0. All members are priority/device links; the multi-candidate group also fits.
- flatcar-bd2da87ed0efb70dddab1085: /run/udev/links/disk\x2fby-uuid\x2f38565143-560c-4c39-8c57-658effcbfe8c; 0:/dev/loop1p2. All members are priority/device links; the multi-candidate group also fits.
- flatcar-bc6c22f3322ab9f6bac92165: /run/udev/links/input\x2fby-path\x2fplatform-i8042-serio-0-event-kbd; 0:/dev/input/event0. All members are priority/device links; the multi-candidate group also fits.
- flatcar-0d0039dc3b2bb330f490ad2a: /run/udev/links/mapper\x2floop1p1-45-verity; 0:/dev/dm-3. All members are priority/device links; the multi-candidate group also fits.
- flatcar-c189e7cb14a12c396c78de5f: /run/udev/links/rtc; -100:/dev/rtc0. All members are priority/device links; the multi-candidate group also fits.

## Rule K: empty-directory package markers
A group consisting entirely of .keep_* regular files contains package bookkeeping markers, not settings, executable code or device/access rules. Removing the marker alone leaves the directory and program functions intact. NOT (S2.2-2, S2.2-4).
Source: https://devmanual.gentoo.org/function-reference/install-functions/index.html
Exact quote: “This is accomplished by installing a hidden file prefixed with `.keep` to the directory in question.”
Hand-checked IDs below:
- flatcar-75eb1fe98f314da284effa3a: ["/etc/binfmt.d/.keep_sys-apps_systemd-0"]; raw records regular .keep files, with no other group members.
- flatcar-8a343b5a4d44aaa4822d1249: ["/etc/dbus-1/session.d/.keep_sys-apps_dbus-0"]; raw records regular .keep files, with no other group members.
- flatcar-c37ad6485aad0bfd3e16c136: ["/etc/dbus-1/system.d/.keep_sys-apps_dbus-0"]; raw records regular .keep files, with no other group members.
- flatcar-1a3c31d650cc1876ccc51362: ["/etc/kernel/install.d/.keep_sys-apps_systemd-0"]; raw records regular .keep files, with no other group members.
- flatcar-4aa44cbec033da59c6990315: ["/etc/lessfilter.d/.keep_sys-apps_less-0"]; raw records regular .keep files, with no other group members.
- flatcar-f69f27e0da9e77c1433fd5f1: ["/etc/modules-load.d/.keep_sys-apps_systemd-0"]; raw records regular .keep files, with no other group members.
- flatcar-0d03a9e02b07f43c129a7bb5: ["/etc/pam.d/.keep_sys-libs_pam-0"]; raw records regular .keep files, with no other group members.
- flatcar-e42a68dbfdaa8487079efbc9: ["/etc/polkit-1/rules.d/.keep_sys-auth_polkit-0"]; raw records regular .keep files, with no other group members.
- flatcar-cc0a6306432086897d0e99af: ["/etc/sasl2/.keep_dev-libs_cyrus-sasl-2"]; raw records regular .keep files, with no other group members.
- flatcar-2b3d55863d26e28bc1e9cdd3: ["/etc/security/.keep_sys-libs_pam-0"]; raw records regular .keep files, with no other group members.

### flatcar-01d1a51570df35156d65b6b7
Member numbers are one-based input-array positions. Behavioral trees are required; unused directory consumers are unestablished.
- 1: `/` — MUST
- 2: `/.systemd-etc-workdir` — MUST
- 3: `/boot` — MUST
- 4: `/etc` — MUST
- 5: `/home` — MUST
- 6: `/lost+found` — UNKNOWN
- 7: `/media` — UNKNOWN
- 8: `/mnt` — UNKNOWN
- 9: `/oem` — MUST
- 10: `/opt` — MUST
- 11: `/root` — UNKNOWN
- 12: `/run` — MUST
- 13: `/srv` — UNKNOWN
- 14: `/tmp` — MUST
- 15: `/var` — MUST

### flatcar-7955ed3fbebf581406d0ce57
Member numbers are one-based input-array positions. Account/code/system effects require recording; historical and display content do not; uncaptured settings remain unknown.
- 1: `/etc/.ignition-result.json` — NOT
- 2: `/etc/.pwd.lock` — UNKNOWN
- 3: `/etc/.systemd-confext` — MUST
- 4: `/etc/.updated` — UNKNOWN
- 5: `/etc/X11` — MUST
- 6: `/etc/audit` — MUST
- 7: `/etc/azure-ephemeral-disk-setup.conf` — UNKNOWN
- 8: `/etc/bash` — MUST
- 9: `/etc/bindresvport.blacklist` — UNKNOWN
- 10: `/etc/binfmt.d` — UNKNOWN
- 11: `/etc/cifs-utils` — UNKNOWN
- 12: `/etc/cni` — UNKNOWN
- 13: `/etc/conntrackd` — UNKNOWN
- 14: `/etc/coreos` — UNKNOWN
- 15: `/etc/credstore` — UNKNOWN
- 16: `/etc/credstore.encrypted` — UNKNOWN
- 17: `/etc/dbus-1` — MUST
- 18: `/etc/default` — MUST
- 19: `/etc/dracut.conf` — UNKNOWN
- 20: `/etc/e2scrub.conf` — UNKNOWN
- 21: `/etc/environment.d` — MUST
- 22: `/etc/ethertypes` — UNKNOWN
- 23: `/etc/extension-release.d` — MUST
- 24: `/etc/extensions` — MUST
- 25: `/etc/flatcar` — UNKNOWN
- 26: `/etc/group` — MUST
- 27: `/etc/group-` — NOT
- 28: `/etc/gshadow` — MUST
- 29: `/etc/gshadow-` — NOT
- 30: `/etc/hosts` — MUST
- 31: `/etc/idmapd.conf` — UNKNOWN
- 32: `/etc/init.d` — UNKNOWN
- 33: `/etc/iscsi` — UNKNOWN
- 34: `/etc/isns` — UNKNOWN
- 35: `/etc/issue` — NOT
- 36: `/etc/kernel` — MUST
- 37: `/etc/kexec.conf` — UNKNOWN
- 38: `/etc/keyutils` — UNKNOWN
- 39: `/etc/krb5.conf.example` — NOT
- 40: `/etc/ld.so.cache` — UNKNOWN
- 41: `/etc/ldap.conf.sudo` — UNKNOWN
- 42: `/etc/lessfilter.d` — UNKNOWN
- 43: `/etc/libaudit.conf` — UNKNOWN
- 44: `/etc/locale.conf` — MUST
- 45: `/etc/login.defs` — MUST
- 46: `/etc/logrotate.conf` — UNKNOWN
- 47: `/etc/logrotate.d` — UNKNOWN
- 48: `/etc/lvm` — UNKNOWN
- 49: `/etc/machine-id` — MUST
- 50: `/etc/mke2fs.conf` — UNKNOWN
- 51: `/etc/modules-load.d` — MUST
- 52: `/etc/motd` — NOT
- 53: `/etc/mtab` — UNKNOWN
- 54: `/etc/netconfig` — UNKNOWN
- 55: `/etc/nscd.conf` — UNKNOWN
- 56: `/etc/ntp.conf` — UNKNOWN
- 57: `/etc/nvme` — UNKNOWN
- 58: `/etc/openldap` — UNKNOWN
- 59: `/etc/pam.d` — UNKNOWN
- 60: `/etc/passwd` — MUST
- 61: `/etc/passwd-` — NOT
- 62: `/etc/pkcs11` — UNKNOWN
- 63: `/etc/polkit-1` — UNKNOWN
- 64: `/etc/profile.d` — MUST
- 65: `/etc/quotagrpadmins` — UNKNOWN
- 66: `/etc/quotatab` — UNKNOWN
- 67: `/etc/request-key.conf` — MUST
- 68: `/etc/request-key.d` — MUST
- 69: `/etc/resolv.conf` — MUST
- 70: `/etc/runlevels` — UNKNOWN
- 71: `/etc/sasl2` — UNKNOWN
- 72: `/etc/securetty` — MUST
- 73: `/etc/security` — MUST
- 74: `/etc/selinux` — MUST
- 75: `/etc/sestatus.conf` — UNKNOWN
- 76: `/etc/shadow` — UNKNOWN
- 77: `/etc/shadow-` — NOT
- 78: `/etc/skel` — MUST
- 79: `/etc/ssh` — MUST
- 80: `/etc/ssl` — MUST
- 81: `/etc/sssd` — MUST
- 82: `/etc/subgid` — MUST
- 83: `/etc/subgid-` — NOT
- 84: `/etc/subuid` — MUST
- 85: `/etc/subuid-` — NOT
- 86: `/etc/sudo_logsrvd.conf` — UNKNOWN
- 87: `/etc/sudoers.d` — MUST
- 88: `/etc/sudoers.dist` — UNKNOWN
- 89: `/etc/sysconfig` — UNKNOWN
- 90: `/etc/systemd` — MUST
- 91: `/etc/tcsd.conf` — UNKNOWN
- 92: `/etc/tmpfiles.d` — MUST
- 93: `/etc/tpm2-tss` — UNKNOWN
- 94: `/etc/udev` — MUST
- 95: `/etc/user` — UNKNOWN
- 96: `/etc/vim` — UNKNOWN
- 97: `/etc/warnquota.conf` — UNKNOWN
- 98: `/etc/whois.conf` — UNKNOWN
- 99: `/etc/wireguard` — UNKNOWN
- 100: `/etc/xattr.conf` — UNKNOWN
- 101: `/etc/xdg` — MUST

### flatcar-3e3328fa5aa3c0625e5e872a
Member numbers are one-based input-array positions. Marker is bookkeeping; audit rules alter kernel event collection.
- 1: `/etc/audit/rules.d/.keep_sys-process_audit-0` — NOT
- 2: `/etc/audit/rules.d/00-clear.rules` — MUST
- 3: `/etc/audit/rules.d/80-selinux.rules` — MUST
- 4: `/etc/audit/rules.d/99-default.rules` — MUST

### flatcar-bd2c4559f2056871a7ff8f03
Member numbers are one-based input-array positions. Bus rules govern multiple processes; marker-only subdirectories carry bookkeeping.
- 1: `/etc/dbus-1/session.conf` — MUST
- 2: `/etc/dbus-1/session.d` — NOT
- 3: `/etc/dbus-1/system.conf` — MUST
- 4: `/etc/dbus-1/system.d` — NOT

### flatcar-8ab92d58c9a88869f7e5408d
Member numbers are one-based input-array positions. Example is content; active-name configuration governs remote block-storage access.
- 1: `/etc/iscsi/initiatorname.iscsi.example` — NOT
- 2: `/etc/iscsi/iscsid.conf` — MUST

### flatcar-95f8a1273692407a1adfef04
Member numbers are one-based input-array positions. Marker is bookkeeping; rotation rules remove or rotate filesystem logs, beyond one program.
- 1: `/etc/logrotate.d/.keep_app-admin_logrotate-0` — NOT
- 2: `/etc/logrotate.d/iscsiuiolog` — MUST
- 3: `/etc/logrotate.d/qemu-guest-agent` — MUST
- 4: `/etc/logrotate.d/rsyncd` — MUST
- 5: `/etc/logrotate.d/sssd` — MUST

### flatcar-f9ff8d878016884d80dadb98
Member numbers are one-based input-array positions. Example is content; actual client defaults and their scope are unavailable.
- 1: `/etc/openldap/ldap.conf` — UNKNOWN
- 2: `/etc/openldap/ldap.conf.default` — NOT

### flatcar-67eb2395438dce162f6560f5
Member numbers are one-based input-array positions. Text mappings control security labels; compiled equivalents accelerate lookup.
- 1: `/etc/selinux/mcs/contexts/files/file_contexts` — MUST
- 2: `/etc/selinux/mcs/contexts/files/file_contexts.bin` — NOT
- 3: `/etc/selinux/mcs/contexts/files/file_contexts.homedirs` — MUST
- 4: `/etc/selinux/mcs/contexts/files/file_contexts.homedirs.bin` — NOT
- 5: `/etc/selinux/mcs/contexts/files/file_contexts.local` — MUST
- 6: `/etc/selinux/mcs/contexts/files/file_contexts.local.bin` — NOT
- 7: `/etc/selinux/mcs/contexts/files/file_contexts.subs_dist` — MUST
- 8: `/etc/selinux/mcs/contexts/files/media` — MUST

### flatcar-8e7f275dda3033c6764dbce1
Member numbers are one-based input-array positions. Text mappings control security labels; compiled equivalents accelerate lookup.
- 1: `/etc/selinux/mls/contexts/files/file_contexts` — MUST
- 2: `/etc/selinux/mls/contexts/files/file_contexts.bin` — NOT
- 3: `/etc/selinux/mls/contexts/files/file_contexts.homedirs` — MUST
- 4: `/etc/selinux/mls/contexts/files/file_contexts.homedirs.bin` — NOT
- 5: `/etc/selinux/mls/contexts/files/file_contexts.local` — MUST
- 6: `/etc/selinux/mls/contexts/files/file_contexts.local.bin` — NOT
- 7: `/etc/selinux/mls/contexts/files/file_contexts.subs_dist` — MUST
- 8: `/etc/selinux/mls/contexts/files/media` — MUST

### flatcar-fe7d9160ddf88a1ab47b648a
Member numbers are one-based input-array positions. Text mappings control security labels; compiled equivalents accelerate lookup.
- 1: `/etc/selinux/targeted/contexts/files/file_contexts` — MUST
- 2: `/etc/selinux/targeted/contexts/files/file_contexts.bin` — NOT
- 3: `/etc/selinux/targeted/contexts/files/file_contexts.homedirs` — MUST
- 4: `/etc/selinux/targeted/contexts/files/file_contexts.homedirs.bin` — NOT
- 5: `/etc/selinux/targeted/contexts/files/file_contexts.local` — MUST
- 6: `/etc/selinux/targeted/contexts/files/file_contexts.local.bin` — NOT
- 7: `/etc/selinux/targeted/contexts/files/file_contexts.subs_dist` — MUST
- 8: `/etc/selinux/targeted/contexts/files/media` — MUST

### flatcar-3546abab943996de0d498da5
Member numbers are one-based input-array positions. Marker is bookkeeping; binary policy controls system-wide access.
- 1: `/etc/selinux/mcs/policy/.keep_sec-policy_selinux-base-0` — NOT
- 2: `/etc/selinux/mcs/policy/policy.35` — MUST

### flatcar-2172ae44cbb0a923ab9ba6fb
Member numbers are one-based input-array positions. Marker is bookkeeping; binary policy controls system-wide access.
- 1: `/etc/selinux/mls/policy/.keep_sec-policy_selinux-base-0` — NOT
- 2: `/etc/selinux/mls/policy/policy.35` — MUST

### flatcar-19aaf19227695fbd77af5cca
Member numbers are one-based input-array positions. Marker is bookkeeping; binary policy controls system-wide access.
- 1: `/etc/selinux/targeted/policy/.keep_sec-policy_selinux-base-0` — NOT
- 2: `/etc/selinux/targeted/policy/policy.35` — MUST

### flatcar-fc09a47fdb5636cbf6b1fb22
Member numbers are one-based input-array positions. Client defaults remain inside SSH; host authentication and server access enable login.
- 1: `/etc/ssh/moduli` — MUST
- 2: `/etc/ssh/ssh_config` — NOT
- 3: `/etc/ssh/ssh_config.d` — NOT
- 4: `/etc/ssh/ssh_host_ecdsa_key` — MUST
- 5: `/etc/ssh/ssh_host_ecdsa_key.pub` — MUST
- 6: `/etc/ssh/ssh_host_ed25519_key` — MUST
- 7: `/etc/ssh/ssh_host_ed25519_key.pub` — MUST
- 8: `/etc/ssh/ssh_host_mldsa44_ed25519_key` — MUST
- 9: `/etc/ssh/ssh_host_mldsa44_ed25519_key.pub` — MUST
- 10: `/etc/ssh/ssh_host_rsa_key` — MUST
- 11: `/etc/ssh/ssh_host_rsa_key.pub` — MUST
- 12: `/etc/ssh/ssh_revoked_hosts` — MUST
- 13: `/etc/ssh/sshd_config` — MUST
- 14: `/etc/ssh/sshd_config.d` — MUST

### flatcar-b3531e524e85d4c2cc907fb8
Member numbers are one-based input-array positions. Markers/examples are content; SSSD configuration governs system identity and authentication.
- 1: `/etc/sssd/conf.d` — NOT
- 2: `/etc/sssd/pki` — NOT
- 3: `/etc/sssd/sssd-example.conf` — NOT
- 4: `/etc/sssd/sssd.conf` — MUST

### flatcar-1dbf7846e77a20c7624142e9
Member numbers are one-based input-array positions. Marker is bookkeeping; wants-directory links control service timer activation.
- 1: `/etc/systemd/system/.keep_sys-apps_systemd-0` — NOT
- 2: `/etc/systemd/system/timers.target.wants` — MUST

### flatcar-776158c873d0ec65315d36b4
Member numbers are one-based input-array positions. Hardware properties affect devices; markers are bookkeeping; uncaptured configuration values remain unknown.
- 1: `/etc/udev/hwdb.bin` — MUST
- 2: `/etc/udev/hwdb.d` — NOT
- 3: `/etc/udev/iocost.conf` — UNKNOWN
- 4: `/etc/udev/rules.d` — NOT
- 5: `/etc/udev/udev.conf` — UNKNOWN

### flatcar-68768e2b26f1fba2d8bcc15a
Member numbers are one-based input-array positions. Startup code and login keys require recording; empty home-directory dependency is unestablished.
- 1: `/home/core` — UNKNOWN
- 2: `/home/user` — MUST

### flatcar-47598385be793e3487e3ae2f
Member numbers are one-based input-array positions. Startup code and login keys are required; lock behavior is not established.
- 1: `/home/user/.authorized_keys.d.lock` — UNKNOWN
- 2: `/home/user/.bash_logout` — MUST
- 3: `/home/user/.bash_profile` — MUST
- 4: `/home/user/.bashrc` — MUST
- 5: `/home/user/.ssh` — MUST

### flatcar-7976e0ab6cbbb8450088916a
Member numbers are one-based input-array positions. Old copy records past authorization; current key files enable account login.
- 1: `/home/user/.ssh/.authorized_keys.d.old` — NOT
- 2: `/home/user/.ssh/authorized_keys` — MUST
- 3: `/home/user/.ssh/authorized_keys.d` — MUST

### flatcar-025b74d903a537ca1a129ee2
Member numbers are one-based input-array positions. Boot rules/extensions alter execution; release text identifies content.
- 1: `/oem/grub.cfg` — MUST
- 2: `/oem/oem-release` — NOT
- 3: `/oem/sysext` — MUST

### flatcar-8d354bdc3e8042522678923e
Member numbers are one-based input-array positions. Live endpoints/rules affect interprocess behavior; caches/content/history are exempt; other runtime uses are unestablished.
- 1: `/run/blkid` — NOT
- 2: `/run/containerd` — MUST
- 3: `/run/coreos` — NOT
- 4: `/run/credentials` — UNKNOWN
- 5: `/run/cryptsetup` — UNKNOWN
- 6: `/run/dbus` — MUST
- 7: `/run/docker` — MUST
- 8: `/run/docker.pid` — UNKNOWN
- 9: `/run/docker.sock` — MUST
- 10: `/run/faillock` — UNKNOWN
- 11: `/run/flatcar` — NOT
- 12: `/run/fsck` — UNKNOWN
- 13: `/run/ignition.env` — UNKNOWN
- 14: `/run/initramfs` — UNKNOWN
- 15: `/run/issue` — NOT
- 16: `/run/issue.d` — NOT
- 17: `/run/lock` — UNKNOWN
- 18: `/run/log` — NOT
- 19: `/run/lvm` — UNKNOWN
- 20: `/run/mdadm` — UNKNOWN
- 21: `/run/modprobe.d` — UNKNOWN
- 22: `/run/mount` — UNKNOWN
- 23: `/run/multipath` — UNKNOWN
- 24: `/run/nri` — MUST
- 25: `/run/nscd` — UNKNOWN
- 26: `/run/saslauthd` — UNKNOWN
- 27: `/run/ssh-unix-local` — MUST
- 28: `/run/sshd` — UNKNOWN
- 29: `/run/sssd` — UNKNOWN
- 30: `/run/sudo` — UNKNOWN
- 31: `/run/systemd` — MUST
- 32: `/run/tmpfiles.d` — MUST
- 33: `/run/tpm2-tss` — UNKNOWN
- 34: `/run/udev` — MUST
- 35: `/run/update-engine` — UNKNOWN
- 36: `/run/user` — MUST
- 37: `/run/utmp` — NOT
- 38: `/run/varlink` — MUST
- 39: `/run/xtables.lock` — UNKNOWN

### flatcar-0a2f5f184ea0098c30af81ef
Member numbers are one-based input-array positions. Sockets enable IPC; directory contents and actual database effects are not captured.
- 1: `/run/containerd/containerd.sock` — MUST
- 2: `/run/containerd/containerd.sock.ttrpc` — MUST
- 3: `/run/containerd/io.containerd.grpc.v1.cri` — UNKNOWN
- 4: `/run/containerd/io.containerd.mount-manager.v1.bolt` — UNKNOWN
- 5: `/run/containerd/io.containerd.runtime.v2.task` — UNKNOWN
- 6: `/run/containerd/io.containerd.sandbox.controller.v1.shim` — UNKNOWN

### flatcar-cc7f234ea5320af7c211fb4a
Member numbers are one-based input-array positions. IPC paths enable interprocess functions; empty plugin-directory dependence is unknown.
- 1: `/run/docker/libcontainerd` — MUST
- 2: `/run/docker/libnetwork` — MUST
- 3: `/run/docker/metrics.sock` — MUST
- 4: `/run/docker/plugins` — UNKNOWN

### flatcar-591f3f4c191b1e17b6e0632f
Member numbers are one-based input-array positions. Past logs are exempt; actual uses of other retained directories are unknown.
- 1: `/run/initramfs/cmdline.d` — UNKNOWN
- 2: `/run/initramfs/log` — NOT
- 3: `/run/initramfs/systemd` — UNKNOWN

### flatcar-7db1d507b1da0e5b91f46577
Member numbers are one-based input-array positions. Sockets and unit rules enable system behavior; identification content is exempt; other state consumers remain unknown.
- 1: `/run/systemd/ask-password` — UNKNOWN
- 2: `/run/systemd/coredump` — MUST
- 3: `/run/systemd/default-hostname` — NOT
- 4: `/run/systemd/dissect-root` — UNKNOWN
- 5: `/run/systemd/generator` — MUST
- 6: `/run/systemd/generator.late` — MUST
- 7: `/run/systemd/inaccessible` — MUST
- 8: `/run/systemd/inhibit` — UNKNOWN
- 9: `/run/systemd/io.systemd.AskPassword` — MUST
- 10: `/run/systemd/io.systemd.Credentials` — MUST
- 11: `/run/systemd/io.systemd.FactoryReset` — MUST
- 12: `/run/systemd/io.systemd.Hostname` — MUST
- 13: `/run/systemd/io.systemd.Import` — MUST
- 14: `/run/systemd/io.systemd.JournalAccess` — MUST
- 15: `/run/systemd/io.systemd.Login` — MUST
- 16: `/run/systemd/io.systemd.ManagedOOM` — MUST
- 17: `/run/systemd/io.systemd.Manager` — MUST
- 18: `/run/systemd/io.systemd.MountFileSystem` — MUST
- 19: `/run/systemd/io.systemd.MuteConsole` — MUST
- 20: `/run/systemd/io.systemd.NamespaceResource` — MUST
- 21: `/run/systemd/io.systemd.Repart` — MUST
- 22: `/run/systemd/io.systemd.sysext` — MUST
- 23: `/run/systemd/journal` — MUST
- 24: `/run/systemd/machine` — MUST
- 25: `/run/systemd/machines` — UNKNOWN
- 26: `/run/systemd/mount-rootfs` — UNKNOWN
- 27: `/run/systemd/netif` — MUST
- 28: `/run/systemd/network` — MUST
- 29: `/run/systemd/notify` — MUST
- 30: `/run/systemd/nspawn` — UNKNOWN
- 31: `/run/systemd/nsresource` — UNKNOWN
- 32: `/run/systemd/oom` — MUST
- 33: `/run/systemd/private` — MUST
- 34: `/run/systemd/propagate` — NOT
- 35: `/run/systemd/report` — MUST
- 36: `/run/systemd/resolve` — MUST
- 37: `/run/systemd/resolve.hook` — MUST
- 38: `/run/systemd/seats` — UNKNOWN
- 39: `/run/systemd/sessions` — UNKNOWN
- 40: `/run/systemd/show-status` — UNKNOWN
- 41: `/run/systemd/shutdown` — UNKNOWN
- 42: `/run/systemd/sysext` — UNKNOWN
- 43: `/run/systemd/system` — UNKNOWN
- 44: `/run/systemd/systemd-units-load` — UNKNOWN
- 45: `/run/systemd/timesync` — UNKNOWN
- 46: `/run/systemd/transient` — MUST
- 47: `/run/systemd/units` — UNKNOWN
- 48: `/run/systemd/userdb` — MUST
- 49: `/run/systemd/users` — UNKNOWN

### flatcar-27ab5a6b2bcd37afb4af1e52
Member numbers are one-based input-array positions. Sockets enable logging IPC; sequence/stream-state contents and consumers are not fully established.
- 1: `/run/systemd/journal/dev-log` — MUST
- 2: `/run/systemd/journal/flushed` — UNKNOWN
- 3: `/run/systemd/journal/io.systemd.journal` — MUST
- 4: `/run/systemd/journal/kernel-seqnum` — UNKNOWN
- 5: `/run/systemd/journal/seqnum` — UNKNOWN
- 6: `/run/systemd/journal/socket` — MUST
- 7: `/run/systemd/journal/stdout` — MUST
- 8: `/run/systemd/journal/streams` — UNKNOWN

### flatcar-96a67fde1ac33b125a79bea0
Member numbers are one-based input-array positions. IPC and current network state serve other programs; empty server-lease-directory use is unknown.
- 1: `/run/systemd/netif/dhcp-server-lease` — UNKNOWN
- 2: `/run/systemd/netif/io.systemd.Network` — MUST
- 3: `/run/systemd/netif/leases` — MUST
- 4: `/run/systemd/netif/links` — MUST
- 5: `/run/systemd/netif/state` — MUST

### flatcar-ace9f82cde7b45781f45ea71
Member numbers are one-based input-array positions. IPC and device metadata support system access; empty lock/rule-directory dependencies are unknown.
- 1: `/run/udev/control` — MUST
- 2: `/run/udev/data` — MUST
- 3: `/run/udev/io.systemd.Udev` — MUST
- 4: `/run/udev/links` — MUST
- 5: `/run/udev/links.lock` — UNKNOWN
- 6: `/run/udev/rules.d` — UNKNOWN
- 7: `/run/udev/tags` — MUST
- 8: `/run/udev/watch` — MUST

### flatcar-9b9193a7e1c17f5ead59b1aa
Member numbers are one-based input-array positions. Active IPC enables programs to communicate; empty users directory dependencies are not established.
- 1: `/run/user/1000` — MUST
- 2: `/run/user/500` — UNKNOWN

### flatcar-c0a30ba689b29442ff194133
Member numbers are one-based input-array positions. IPC/sandbox nodes affect other processes; release text is content; invocation consumer behavior remains unestablished.
- 1: `/run/user/1000/systemd/inaccessible` — MUST
- 2: `/run/user/1000/systemd/io.systemd.AskPassword` — MUST
- 3: `/run/user/1000/systemd/io.systemd.Import` — MUST
- 4: `/run/user/1000/systemd/io.systemd.JournalAccess` — MUST
- 5: `/run/user/1000/systemd/io.systemd.Manager` — MUST
- 6: `/run/user/1000/systemd/machine` — MUST
- 7: `/run/user/1000/systemd/notify` — MUST
- 8: `/run/user/1000/systemd/private` — MUST
- 9: `/run/user/1000/systemd/propagate` — NOT
- 10: `/run/user/1000/systemd/report` — MUST
- 11: `/run/user/1000/systemd/units` — UNKNOWN

### flatcar-e8bc19ab63b2f5950a9671af
Member numbers are one-based input-array positions. Private directories back process isolation; empty display-server directory consumers are unestablished.
- 1: `/tmp/.ICE-unix` — UNKNOWN
- 2: `/tmp/.X11-unix` — UNKNOWN
- 3: `/tmp/.XIM-unix` — UNKNOWN
- 4: `/tmp/.font-unix` — UNKNOWN
- 5: `/tmp/systemd-private-399ee384a85947e5802aa24624a28b03-polkit.service-b91ISC` — MUST
- 6: `/tmp/systemd-private-399ee384a85947e5802aa24624a28b03-systemd-logind.service-dAxW1L` — MUST

### flatcar-b5baa09f5c3f8794557bf857
Member numbers are one-based input-array positions. Runtime/service dependencies require recording; cache/log stores are exempt; remaining directory consumers are unestablished.
- 1: `/var/.updated` — UNKNOWN
- 2: `/var/cache` — NOT
- 3: `/var/db` — UNKNOWN
- 4: `/var/empty` — UNKNOWN
- 5: `/var/kubernetes` — UNKNOWN
- 6: `/var/lib` — MUST
- 7: `/var/lock` — MUST
- 8: `/var/log` — NOT
- 9: `/var/run` — MUST
- 10: `/var/spool` — UNKNOWN
- 11: `/var/tmp` — MUST

### flatcar-7a63c430cdc959f1b261bfa0
Member numbers are one-based input-array positions. Auxiliary linker cache only accelerates rebuilding; private directory dependency is unestablished.
- 1: `/var/cache/ldconfig` — NOT
- 2: `/var/cache/private` — UNKNOWN

### flatcar-f91c1f2c90de95c5b942a889
Member numbers are one-based input-array positions. Configuration/identity aliases serve programs; cache storage is exempt; actual state contents and other directory dependencies are unavailable.
- 1: `/var/lib/cache` — NOT
- 2: `/var/lib/containerd` — UNKNOWN
- 3: `/var/lib/dbus` — MUST
- 4: `/var/lib/docker` — UNKNOWN
- 5: `/var/lib/etcd` — UNKNOWN
- 6: `/var/lib/extensions.mutable` — MUST
- 7: `/var/lib/ip6tables` — UNKNOWN
- 8: `/var/lib/ipset` — UNKNOWN
- 9: `/var/lib/iptables` — UNKNOWN
- 10: `/var/lib/iscsi` — UNKNOWN
- 11: `/var/lib/isns` — UNKNOWN
- 12: `/var/lib/krb5kdc` — UNKNOWN
- 13: `/var/lib/lib` — UNKNOWN
- 14: `/var/lib/machines` — UNKNOWN
- 15: `/var/lib/misc` — UNKNOWN
- 16: `/var/lib/nfs` — UNKNOWN
- 17: `/var/lib/nftables` — UNKNOWN
- 18: `/var/lib/ntp` — UNKNOWN
- 19: `/var/lib/polkit-1` — UNKNOWN
- 20: `/var/lib/portables` — UNKNOWN
- 21: `/var/lib/private` — UNKNOWN
- 22: `/var/lib/sss` — UNKNOWN
- 23: `/var/lib/systemd` — UNKNOWN
- 24: `/var/lib/tpm` — UNKNOWN
- 25: `/var/lib/tpm2-tss` — UNKNOWN

### flatcar-ff709a51aa4d7980d98fc060
Member numbers are one-based input-array positions. Cache/history are exempt; other databases lack contents establishing their actual effects.
- 1: `/var/lib/docker/buildkit/cache.db` — NOT
- 2: `/var/lib/docker/buildkit/containerdmeta.db` — UNKNOWN
- 3: `/var/lib/docker/buildkit/executor` — UNKNOWN
- 4: `/var/lib/docker/buildkit/history.db` — NOT
- 5: `/var/lib/docker/buildkit/metadata_v2.db` — UNKNOWN
- 6: `/var/lib/docker/buildkit/snapshots.db` — UNKNOWN

### flatcar-186acdd6733c226cced3c6d3
Member numbers are one-based input-array positions. Block node provides storage access; volume database contents and actual effects remain unknown.
- 1: `/var/lib/docker/volumes/backingFsBlockDev` — MUST
- 2: `/var/lib/docker/volumes/metadata.db` — UNKNOWN

### flatcar-d11cff71d6ec6e8beafbf4e9
Member numbers are one-based input-array positions. Timing records both describe past events and affect future actions; remaining states have distinct functions.
- 1: `/var/lib/systemd/catalog` — NOT
- 2: `/var/lib/systemd/coredump` — NOT
- 3: `/var/lib/systemd/ephemeral-trees` — UNKNOWN
- 4: `/var/lib/systemd/linger` — UNKNOWN
- 5: `/var/lib/systemd/network` — UNKNOWN
- 6: `/var/lib/systemd/pstore` — NOT
- 7: `/var/lib/systemd/random-seed` — MUST
- 8: `/var/lib/systemd/timers` — HOLE
- 9: `/var/lib/systemd/timesync` — HOLE

### Correction flatcar-b63a60e710980988400f52f9
MUST → MIXED. Modules execute; separate memdisk/configuration inputs lack established later consumers.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/grub.cfg.tar` — UNKNOWN
- 2: `/boot/flatcar/grub/i386-pc` — MUST
- 3: `/boot/flatcar/grub/x86_64-efi` — UNKNOWN
- 4: `/boot/flatcar/grub/x86_64-xen` — MUST

### Correction flatcar-aa489ee21d27f0b113d367ca
MUST → MIXED. Code requires recording; indexes/history have exemption conflicts; construction inputs lack established later consumers.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/i386-pc/acpi.mod` — MUST
- 2: `/boot/flatcar/grub/i386-pc/adler32.mod` — MUST
- 3: `/boot/flatcar/grub/i386-pc/affs.mod` — MUST
- 4: `/boot/flatcar/grub/i386-pc/afs.mod` — MUST
- 5: `/boot/flatcar/grub/i386-pc/afsplitter.mod` — MUST
- 6: `/boot/flatcar/grub/i386-pc/ahci.mod` — MUST
- 7: `/boot/flatcar/grub/i386-pc/all_video.mod` — MUST
- 8: `/boot/flatcar/grub/i386-pc/aout.mod` — MUST
- 9: `/boot/flatcar/grub/i386-pc/appendedsig.mod` — MUST
- 10: `/boot/flatcar/grub/i386-pc/archelp.mod` — MUST
- 11: `/boot/flatcar/grub/i386-pc/asn1.mod` — MUST
- 12: `/boot/flatcar/grub/i386-pc/at_keyboard.mod` — MUST
- 13: `/boot/flatcar/grub/i386-pc/ata.mod` — MUST
- 14: `/boot/flatcar/grub/i386-pc/backtrace.mod` — MUST
- 15: `/boot/flatcar/grub/i386-pc/bfs.mod` — MUST
- 16: `/boot/flatcar/grub/i386-pc/bitmap.mod` — MUST
- 17: `/boot/flatcar/grub/i386-pc/bitmap_scale.mod` — MUST
- 18: `/boot/flatcar/grub/i386-pc/blocklist.mod` — MUST
- 19: `/boot/flatcar/grub/i386-pc/blscfg.mod` — MUST
- 20: `/boot/flatcar/grub/i386-pc/boot.img` — UNKNOWN
- 21: `/boot/flatcar/grub/i386-pc/boot.mod` — MUST
- 22: `/boot/flatcar/grub/i386-pc/bsd.mod` — MUST
- 23: `/boot/flatcar/grub/i386-pc/bufio.mod` — MUST
- 24: `/boot/flatcar/grub/i386-pc/cat.mod` — MUST
- 25: `/boot/flatcar/grub/i386-pc/cbfs.mod` — MUST
- 26: `/boot/flatcar/grub/i386-pc/cbls.mod` — MUST
- 27: `/boot/flatcar/grub/i386-pc/cbmemc.mod` — MUST
- 28: `/boot/flatcar/grub/i386-pc/cbtable.mod` — MUST
- 29: `/boot/flatcar/grub/i386-pc/cbtime.mod` — MUST
- 30: `/boot/flatcar/grub/i386-pc/chain.mod` — MUST
- 31: `/boot/flatcar/grub/i386-pc/cmosdump.mod` — MUST
- 32: `/boot/flatcar/grub/i386-pc/cmostest.mod` — MUST
- 33: `/boot/flatcar/grub/i386-pc/cmp.mod` — MUST
- 34: `/boot/flatcar/grub/i386-pc/command.lst` — HOLE
- 35: `/boot/flatcar/grub/i386-pc/core.img` — MUST
- 36: `/boot/flatcar/grub/i386-pc/cpio.mod` — MUST
- 37: `/boot/flatcar/grub/i386-pc/cpio_be.mod` — MUST
- 38: `/boot/flatcar/grub/i386-pc/cpuid.mod` — MUST
- 39: `/boot/flatcar/grub/i386-pc/crc64.mod` — MUST
- 40: `/boot/flatcar/grub/i386-pc/crypto.lst` — HOLE
- 41: `/boot/flatcar/grub/i386-pc/crypto.mod` — MUST
- 42: `/boot/flatcar/grub/i386-pc/cryptodisk.mod` — MUST
- 43: `/boot/flatcar/grub/i386-pc/cs5536.mod` — MUST
- 44: `/boot/flatcar/grub/i386-pc/date.mod` — MUST
- 45: `/boot/flatcar/grub/i386-pc/datehook.mod` — MUST
- 46: `/boot/flatcar/grub/i386-pc/datetime.mod` — MUST
- 47: `/boot/flatcar/grub/i386-pc/disk.mod` — MUST
- 48: `/boot/flatcar/grub/i386-pc/diskfilter.mod` — MUST
- 49: `/boot/flatcar/grub/i386-pc/div.mod` — MUST
- 50: `/boot/flatcar/grub/i386-pc/dm_nv.mod` — MUST
- 51: `/boot/flatcar/grub/i386-pc/drivemap.mod` — MUST
- 52: `/boot/flatcar/grub/i386-pc/efiemu.mod` — MUST
- 53: `/boot/flatcar/grub/i386-pc/ehci.mod` — MUST
- 54: `/boot/flatcar/grub/i386-pc/elf.mod` — MUST
- 55: `/boot/flatcar/grub/i386-pc/eval.mod` — MUST
- 56: `/boot/flatcar/grub/i386-pc/exfat.mod` — MUST
- 57: `/boot/flatcar/grub/i386-pc/ext2.mod` — MUST
- 58: `/boot/flatcar/grub/i386-pc/extcmd.mod` — MUST
- 59: `/boot/flatcar/grub/i386-pc/f2fs.mod` — MUST
- 60: `/boot/flatcar/grub/i386-pc/fdt.lst` — HOLE
- 61: `/boot/flatcar/grub/i386-pc/file.mod` — MUST
- 62: `/boot/flatcar/grub/i386-pc/font.mod` — MUST
- 63: `/boot/flatcar/grub/i386-pc/freedos.mod` — MUST
- 64: `/boot/flatcar/grub/i386-pc/fs.lst` — HOLE
- 65: `/boot/flatcar/grub/i386-pc/fshelp.mod` — MUST
- 66: `/boot/flatcar/grub/i386-pc/gcry_arcfour.mod` — MUST
- 67: `/boot/flatcar/grub/i386-pc/gcry_blowfish.mod` — MUST
- 68: `/boot/flatcar/grub/i386-pc/gcry_camellia.mod` — MUST
- 69: `/boot/flatcar/grub/i386-pc/gcry_cast5.mod` — MUST
- 70: `/boot/flatcar/grub/i386-pc/gcry_crc.mod` — MUST
- 71: `/boot/flatcar/grub/i386-pc/gcry_des.mod` — MUST
- 72: `/boot/flatcar/grub/i386-pc/gcry_dsa.mod` — MUST
- 73: `/boot/flatcar/grub/i386-pc/gcry_idea.mod` — MUST
- 74: `/boot/flatcar/grub/i386-pc/gcry_md4.mod` — MUST
- 75: `/boot/flatcar/grub/i386-pc/gcry_md5.mod` — MUST
- 76: `/boot/flatcar/grub/i386-pc/gcry_rfc2268.mod` — MUST
- 77: `/boot/flatcar/grub/i386-pc/gcry_rijndael.mod` — MUST
- 78: `/boot/flatcar/grub/i386-pc/gcry_rmd160.mod` — MUST
- 79: `/boot/flatcar/grub/i386-pc/gcry_rsa.mod` — MUST
- 80: `/boot/flatcar/grub/i386-pc/gcry_seed.mod` — MUST
- 81: `/boot/flatcar/grub/i386-pc/gcry_serpent.mod` — MUST
- 82: `/boot/flatcar/grub/i386-pc/gcry_sha1.mod` — MUST
- 83: `/boot/flatcar/grub/i386-pc/gcry_sha256.mod` — MUST
- 84: `/boot/flatcar/grub/i386-pc/gcry_sha512.mod` — MUST
- 85: `/boot/flatcar/grub/i386-pc/gcry_tiger.mod` — MUST
- 86: `/boot/flatcar/grub/i386-pc/gcry_twofish.mod` — MUST
- 87: `/boot/flatcar/grub/i386-pc/gcry_whirlpool.mod` — MUST
- 88: `/boot/flatcar/grub/i386-pc/gdb.mod` — MUST
- 89: `/boot/flatcar/grub/i386-pc/geli.mod` — MUST
- 90: `/boot/flatcar/grub/i386-pc/gettext.mod` — MUST
- 91: `/boot/flatcar/grub/i386-pc/gfxmenu.mod` — MUST
- 92: `/boot/flatcar/grub/i386-pc/gfxterm.mod` — MUST
- 93: `/boot/flatcar/grub/i386-pc/gfxterm_background.mod` — MUST
- 94: `/boot/flatcar/grub/i386-pc/gpt.mod` — MUST
- 95: `/boot/flatcar/grub/i386-pc/gptrepair.mod` — MUST
- 96: `/boot/flatcar/grub/i386-pc/gptsync.mod` — MUST
- 97: `/boot/flatcar/grub/i386-pc/gzio.mod` — MUST
- 98: `/boot/flatcar/grub/i386-pc/halt.mod` — MUST
- 99: `/boot/flatcar/grub/i386-pc/hashsum.mod` — MUST
- 100: `/boot/flatcar/grub/i386-pc/hdparm.mod` — MUST
- 101: `/boot/flatcar/grub/i386-pc/hello.mod` — MUST
- 102: `/boot/flatcar/grub/i386-pc/help.mod` — MUST
- 103: `/boot/flatcar/grub/i386-pc/hexdump.mod` — MUST
- 104: `/boot/flatcar/grub/i386-pc/hfs.mod` — MUST
- 105: `/boot/flatcar/grub/i386-pc/hfsplus.mod` — MUST
- 106: `/boot/flatcar/grub/i386-pc/hfspluscomp.mod` — MUST
- 107: `/boot/flatcar/grub/i386-pc/http.mod` — MUST
- 108: `/boot/flatcar/grub/i386-pc/increment.mod` — MUST
- 109: `/boot/flatcar/grub/i386-pc/iorw.mod` — MUST
- 110: `/boot/flatcar/grub/i386-pc/iso9660.mod` — MUST
- 111: `/boot/flatcar/grub/i386-pc/jfs.mod` — MUST
- 112: `/boot/flatcar/grub/i386-pc/jpeg.mod` — MUST
- 113: `/boot/flatcar/grub/i386-pc/json.mod` — MUST
- 114: `/boot/flatcar/grub/i386-pc/keylayouts.mod` — MUST
- 115: `/boot/flatcar/grub/i386-pc/keystatus.mod` — MUST
- 116: `/boot/flatcar/grub/i386-pc/ldm.mod` — MUST
- 117: `/boot/flatcar/grub/i386-pc/legacycfg.mod` — MUST
- 118: `/boot/flatcar/grub/i386-pc/linux.mod` — MUST
- 119: `/boot/flatcar/grub/i386-pc/load.cfg` — UNKNOWN
- 120: `/boot/flatcar/grub/i386-pc/loadenv.mod` — MUST
- 121: `/boot/flatcar/grub/i386-pc/loopback.mod` — MUST
- 122: `/boot/flatcar/grub/i386-pc/ls.mod` — MUST
- 123: `/boot/flatcar/grub/i386-pc/lsacpi.mod` — MUST
- 124: `/boot/flatcar/grub/i386-pc/lsapm.mod` — MUST
- 125: `/boot/flatcar/grub/i386-pc/lsmmap.mod` — MUST
- 126: `/boot/flatcar/grub/i386-pc/lspci.mod` — MUST
- 127: `/boot/flatcar/grub/i386-pc/luks.mod` — MUST
- 128: `/boot/flatcar/grub/i386-pc/luks2.mod` — MUST
- 129: `/boot/flatcar/grub/i386-pc/lvm.mod` — MUST
- 130: `/boot/flatcar/grub/i386-pc/lzopio.mod` — MUST
- 131: `/boot/flatcar/grub/i386-pc/macbless.mod` — MUST
- 132: `/boot/flatcar/grub/i386-pc/macho.mod` — MUST
- 133: `/boot/flatcar/grub/i386-pc/mbr.bin` — HOLE
- 134: `/boot/flatcar/grub/i386-pc/mda_text.mod` — MUST
- 135: `/boot/flatcar/grub/i386-pc/mdraid09.mod` — MUST
- 136: `/boot/flatcar/grub/i386-pc/mdraid09_be.mod` — MUST
- 137: `/boot/flatcar/grub/i386-pc/mdraid1x.mod` — MUST
- 138: `/boot/flatcar/grub/i386-pc/memrw.mod` — MUST
- 139: `/boot/flatcar/grub/i386-pc/minicmd.mod` — MUST
- 140: `/boot/flatcar/grub/i386-pc/minix.mod` — MUST
- 141: `/boot/flatcar/grub/i386-pc/minix2.mod` — MUST
- 142: `/boot/flatcar/grub/i386-pc/minix2_be.mod` — MUST
- 143: `/boot/flatcar/grub/i386-pc/minix3.mod` — MUST
- 144: `/boot/flatcar/grub/i386-pc/minix3_be.mod` — MUST
- 145: `/boot/flatcar/grub/i386-pc/minix_be.mod` — MUST
- 146: `/boot/flatcar/grub/i386-pc/mmap.mod` — MUST
- 147: `/boot/flatcar/grub/i386-pc/moddep.lst` — HOLE
- 148: `/boot/flatcar/grub/i386-pc/morse.mod` — MUST
- 149: `/boot/flatcar/grub/i386-pc/mpi.mod` — MUST
- 150: `/boot/flatcar/grub/i386-pc/msdospart.mod` — MUST
- 151: `/boot/flatcar/grub/i386-pc/multiboot.mod` — MUST
- 152: `/boot/flatcar/grub/i386-pc/multiboot2.mod` — MUST
- 153: `/boot/flatcar/grub/i386-pc/nativedisk.mod` — MUST
- 154: `/boot/flatcar/grub/i386-pc/net.mod` — MUST
- 155: `/boot/flatcar/grub/i386-pc/newc.mod` — MUST
- 156: `/boot/flatcar/grub/i386-pc/nilfs2.mod` — MUST
- 157: `/boot/flatcar/grub/i386-pc/ntfs.mod` — MUST
- 158: `/boot/flatcar/grub/i386-pc/ntfscomp.mod` — MUST
- 159: `/boot/flatcar/grub/i386-pc/ntldr.mod` — MUST
- 160: `/boot/flatcar/grub/i386-pc/odc.mod` — MUST
- 161: `/boot/flatcar/grub/i386-pc/offsetio.mod` — MUST
- 162: `/boot/flatcar/grub/i386-pc/ohci.mod` — MUST
- 163: `/boot/flatcar/grub/i386-pc/part_acorn.mod` — MUST
- 164: `/boot/flatcar/grub/i386-pc/part_amiga.mod` — MUST
- 165: `/boot/flatcar/grub/i386-pc/part_apple.mod` — MUST
- 166: `/boot/flatcar/grub/i386-pc/part_bsd.mod` — MUST
- 167: `/boot/flatcar/grub/i386-pc/part_dfly.mod` — MUST
- 168: `/boot/flatcar/grub/i386-pc/part_dvh.mod` — MUST
- 169: `/boot/flatcar/grub/i386-pc/part_msdos.mod` — MUST
- 170: `/boot/flatcar/grub/i386-pc/part_plan.mod` — MUST
- 171: `/boot/flatcar/grub/i386-pc/part_sun.mod` — MUST
- 172: `/boot/flatcar/grub/i386-pc/part_sunpc.mod` — MUST
- 173: `/boot/flatcar/grub/i386-pc/partmap.lst` — HOLE
- 174: `/boot/flatcar/grub/i386-pc/parttool.lst` — HOLE
- 175: `/boot/flatcar/grub/i386-pc/parttool.mod` — MUST
- 176: `/boot/flatcar/grub/i386-pc/password.mod` — MUST
- 177: `/boot/flatcar/grub/i386-pc/password_pbkdf2.mod` — MUST
- 178: `/boot/flatcar/grub/i386-pc/pata.mod` — MUST
- 179: `/boot/flatcar/grub/i386-pc/pbkdf2.mod` — MUST
- 180: `/boot/flatcar/grub/i386-pc/pci.mod` — MUST
- 181: `/boot/flatcar/grub/i386-pc/pcidump.mod` — MUST
- 182: `/boot/flatcar/grub/i386-pc/pgp.mod` — MUST
- 183: `/boot/flatcar/grub/i386-pc/pkcs1_v15.mod` — MUST
- 184: `/boot/flatcar/grub/i386-pc/plainmount.mod` — MUST
- 185: `/boot/flatcar/grub/i386-pc/plan9.mod` — MUST
- 186: `/boot/flatcar/grub/i386-pc/play.mod` — MUST
- 187: `/boot/flatcar/grub/i386-pc/png.mod` — MUST
- 188: `/boot/flatcar/grub/i386-pc/priority_queue.mod` — MUST
- 189: `/boot/flatcar/grub/i386-pc/probe.mod` — MUST
- 190: `/boot/flatcar/grub/i386-pc/procfs.mod` — MUST
- 191: `/boot/flatcar/grub/i386-pc/progress.mod` — MUST
- 192: `/boot/flatcar/grub/i386-pc/pxe.mod` — MUST
- 193: `/boot/flatcar/grub/i386-pc/pxechain.mod` — MUST
- 194: `/boot/flatcar/grub/i386-pc/raid5rec.mod` — MUST
- 195: `/boot/flatcar/grub/i386-pc/raid6rec.mod` — MUST
- 196: `/boot/flatcar/grub/i386-pc/random.mod` — MUST
- 197: `/boot/flatcar/grub/i386-pc/rdmsr.mod` — MUST
- 198: `/boot/flatcar/grub/i386-pc/reboot.mod` — MUST
- 199: `/boot/flatcar/grub/i386-pc/regexp.mod` — MUST
- 200: `/boot/flatcar/grub/i386-pc/reiserfs.mod` — MUST
- 201: `/boot/flatcar/grub/i386-pc/relocator.mod` — MUST
- 202: `/boot/flatcar/grub/i386-pc/romfs.mod` — MUST
- 203: `/boot/flatcar/grub/i386-pc/scsi.mod` — MUST
- 204: `/boot/flatcar/grub/i386-pc/search_fs_file.mod` — MUST
- 205: `/boot/flatcar/grub/i386-pc/search_label.mod` — MUST
- 206: `/boot/flatcar/grub/i386-pc/search_part_uuid.mod` — MUST
- 207: `/boot/flatcar/grub/i386-pc/sendkey.mod` — MUST
- 208: `/boot/flatcar/grub/i386-pc/setjmp.mod` — MUST
- 209: `/boot/flatcar/grub/i386-pc/setpci.mod` — MUST
- 210: `/boot/flatcar/grub/i386-pc/sfs.mod` — MUST
- 211: `/boot/flatcar/grub/i386-pc/sleep.mod` — MUST
- 212: `/boot/flatcar/grub/i386-pc/smbios.mod` — MUST
- 213: `/boot/flatcar/grub/i386-pc/spkmodem.mod` — MUST
- 214: `/boot/flatcar/grub/i386-pc/squash4.mod` — MUST
- 215: `/boot/flatcar/grub/i386-pc/syslinuxcfg.mod` — MUST
- 216: `/boot/flatcar/grub/i386-pc/terminal.lst` — HOLE
- 217: `/boot/flatcar/grub/i386-pc/terminfo.mod` — MUST
- 218: `/boot/flatcar/grub/i386-pc/testload.mod` — MUST
- 219: `/boot/flatcar/grub/i386-pc/testspeed.mod` — MUST
- 220: `/boot/flatcar/grub/i386-pc/tftp.mod` — MUST
- 221: `/boot/flatcar/grub/i386-pc/tga.mod` — MUST
- 222: `/boot/flatcar/grub/i386-pc/time.mod` — MUST
- 223: `/boot/flatcar/grub/i386-pc/tr.mod` — MUST
- 224: `/boot/flatcar/grub/i386-pc/trig.mod` — MUST
- 225: `/boot/flatcar/grub/i386-pc/true.mod` — MUST
- 226: `/boot/flatcar/grub/i386-pc/truecrypt.mod` — MUST
- 227: `/boot/flatcar/grub/i386-pc/udf.mod` — MUST
- 228: `/boot/flatcar/grub/i386-pc/ufs1.mod` — MUST
- 229: `/boot/flatcar/grub/i386-pc/ufs1_be.mod` — MUST
- 230: `/boot/flatcar/grub/i386-pc/ufs2.mod` — MUST
- 231: `/boot/flatcar/grub/i386-pc/uhci.mod` — MUST
- 232: `/boot/flatcar/grub/i386-pc/usb.mod` — MUST
- 233: `/boot/flatcar/grub/i386-pc/usb_keyboard.mod` — MUST
- 234: `/boot/flatcar/grub/i386-pc/usbms.mod` — MUST
- 235: `/boot/flatcar/grub/i386-pc/usbserial_common.mod` — MUST
- 236: `/boot/flatcar/grub/i386-pc/usbserial_ftdi.mod` — MUST
- 237: `/boot/flatcar/grub/i386-pc/usbserial_pl2303.mod` — MUST
- 238: `/boot/flatcar/grub/i386-pc/usbserial_usbdebug.mod` — MUST
- 239: `/boot/flatcar/grub/i386-pc/usbtest.mod` — MUST
- 240: `/boot/flatcar/grub/i386-pc/vbe.mod` — MUST
- 241: `/boot/flatcar/grub/i386-pc/version.mod` — MUST
- 242: `/boot/flatcar/grub/i386-pc/vga.mod` — MUST
- 243: `/boot/flatcar/grub/i386-pc/vga_text.mod` — MUST
- 244: `/boot/flatcar/grub/i386-pc/video.lst` — HOLE
- 245: `/boot/flatcar/grub/i386-pc/video.mod` — MUST
- 246: `/boot/flatcar/grub/i386-pc/video_bochs.mod` — MUST
- 247: `/boot/flatcar/grub/i386-pc/video_cirrus.mod` — MUST
- 248: `/boot/flatcar/grub/i386-pc/video_colors.mod` — MUST
- 249: `/boot/flatcar/grub/i386-pc/video_fb.mod` — MUST
- 250: `/boot/flatcar/grub/i386-pc/videoinfo.mod` — MUST
- 251: `/boot/flatcar/grub/i386-pc/videotest.mod` — MUST
- 252: `/boot/flatcar/grub/i386-pc/wrmsr.mod` — MUST
- 253: `/boot/flatcar/grub/i386-pc/xfs.mod` — MUST
- 254: `/boot/flatcar/grub/i386-pc/xnu.mod` — MUST
- 255: `/boot/flatcar/grub/i386-pc/xnu_uuid.mod` — MUST
- 256: `/boot/flatcar/grub/i386-pc/zfs.mod` — MUST
- 257: `/boot/flatcar/grub/i386-pc/zfscrypt.mod` — MUST
- 258: `/boot/flatcar/grub/i386-pc/zfsinfo.mod` — MUST
- 259: `/boot/flatcar/grub/i386-pc/zstd.mod` — MUST

### Correction flatcar-e202fef092ca215c5aa60869
MUST → MIXED. Code requires recording; indexes/history have exemption conflicts; construction inputs lack established later consumers.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/x86_64-xen/adler32.mod` — MUST
- 2: `/boot/flatcar/grub/x86_64-xen/affs.mod` — MUST
- 3: `/boot/flatcar/grub/x86_64-xen/afs.mod` — MUST
- 4: `/boot/flatcar/grub/x86_64-xen/afsplitter.mod` — MUST
- 5: `/boot/flatcar/grub/x86_64-xen/all_video.mod` — MUST
- 6: `/boot/flatcar/grub/x86_64-xen/appendedsig.mod` — MUST
- 7: `/boot/flatcar/grub/x86_64-xen/archelp.mod` — MUST
- 8: `/boot/flatcar/grub/x86_64-xen/asn1.mod` — MUST
- 9: `/boot/flatcar/grub/x86_64-xen/backtrace.mod` — MUST
- 10: `/boot/flatcar/grub/x86_64-xen/bfs.mod` — MUST
- 11: `/boot/flatcar/grub/x86_64-xen/bitmap.mod` — MUST
- 12: `/boot/flatcar/grub/x86_64-xen/bitmap_scale.mod` — MUST
- 13: `/boot/flatcar/grub/x86_64-xen/blocklist.mod` — MUST
- 14: `/boot/flatcar/grub/x86_64-xen/blscfg.mod` — MUST
- 15: `/boot/flatcar/grub/x86_64-xen/bufio.mod` — MUST
- 16: `/boot/flatcar/grub/x86_64-xen/cat.mod` — MUST
- 17: `/boot/flatcar/grub/x86_64-xen/cbfs.mod` — MUST
- 18: `/boot/flatcar/grub/x86_64-xen/cmp.mod` — MUST
- 19: `/boot/flatcar/grub/x86_64-xen/command.lst` — HOLE
- 20: `/boot/flatcar/grub/x86_64-xen/cpio.mod` — MUST
- 21: `/boot/flatcar/grub/x86_64-xen/cpio_be.mod` — MUST
- 22: `/boot/flatcar/grub/x86_64-xen/cpuid.mod` — MUST
- 23: `/boot/flatcar/grub/x86_64-xen/crc64.mod` — MUST
- 24: `/boot/flatcar/grub/x86_64-xen/crypto.lst` — HOLE
- 25: `/boot/flatcar/grub/x86_64-xen/crypto.mod` — MUST
- 26: `/boot/flatcar/grub/x86_64-xen/cryptodisk.mod` — MUST
- 27: `/boot/flatcar/grub/x86_64-xen/date.mod` — MUST
- 28: `/boot/flatcar/grub/x86_64-xen/datehook.mod` — MUST
- 29: `/boot/flatcar/grub/x86_64-xen/datetime.mod` — MUST
- 30: `/boot/flatcar/grub/x86_64-xen/disk.mod` — MUST
- 31: `/boot/flatcar/grub/x86_64-xen/diskfilter.mod` — MUST
- 32: `/boot/flatcar/grub/x86_64-xen/div.mod` — MUST
- 33: `/boot/flatcar/grub/x86_64-xen/dm_nv.mod` — MUST
- 34: `/boot/flatcar/grub/x86_64-xen/elf.mod` — MUST
- 35: `/boot/flatcar/grub/x86_64-xen/eval.mod` — MUST
- 36: `/boot/flatcar/grub/x86_64-xen/exfat.mod` — MUST
- 37: `/boot/flatcar/grub/x86_64-xen/ext2.mod` — MUST
- 38: `/boot/flatcar/grub/x86_64-xen/f2fs.mod` — MUST
- 39: `/boot/flatcar/grub/x86_64-xen/fdt.lst` — HOLE
- 40: `/boot/flatcar/grub/x86_64-xen/file.mod` — MUST
- 41: `/boot/flatcar/grub/x86_64-xen/font.mod` — MUST
- 42: `/boot/flatcar/grub/x86_64-xen/fs.lst` — HOLE
- 43: `/boot/flatcar/grub/x86_64-xen/fshelp.mod` — MUST
- 44: `/boot/flatcar/grub/x86_64-xen/gcry_arcfour.mod` — MUST
- 45: `/boot/flatcar/grub/x86_64-xen/gcry_blowfish.mod` — MUST
- 46: `/boot/flatcar/grub/x86_64-xen/gcry_camellia.mod` — MUST
- 47: `/boot/flatcar/grub/x86_64-xen/gcry_cast5.mod` — MUST
- 48: `/boot/flatcar/grub/x86_64-xen/gcry_crc.mod` — MUST
- 49: `/boot/flatcar/grub/x86_64-xen/gcry_des.mod` — MUST
- 50: `/boot/flatcar/grub/x86_64-xen/gcry_dsa.mod` — MUST
- 51: `/boot/flatcar/grub/x86_64-xen/gcry_idea.mod` — MUST
- 52: `/boot/flatcar/grub/x86_64-xen/gcry_md4.mod` — MUST
- 53: `/boot/flatcar/grub/x86_64-xen/gcry_md5.mod` — MUST
- 54: `/boot/flatcar/grub/x86_64-xen/gcry_rfc2268.mod` — MUST
- 55: `/boot/flatcar/grub/x86_64-xen/gcry_rijndael.mod` — MUST
- 56: `/boot/flatcar/grub/x86_64-xen/gcry_rmd160.mod` — MUST
- 57: `/boot/flatcar/grub/x86_64-xen/gcry_rsa.mod` — MUST
- 58: `/boot/flatcar/grub/x86_64-xen/gcry_seed.mod` — MUST
- 59: `/boot/flatcar/grub/x86_64-xen/gcry_serpent.mod` — MUST
- 60: `/boot/flatcar/grub/x86_64-xen/gcry_sha1.mod` — MUST
- 61: `/boot/flatcar/grub/x86_64-xen/gcry_sha256.mod` — MUST
- 62: `/boot/flatcar/grub/x86_64-xen/gcry_sha512.mod` — MUST
- 63: `/boot/flatcar/grub/x86_64-xen/gcry_tiger.mod` — MUST
- 64: `/boot/flatcar/grub/x86_64-xen/gcry_twofish.mod` — MUST
- 65: `/boot/flatcar/grub/x86_64-xen/gcry_whirlpool.mod` — MUST
- 66: `/boot/flatcar/grub/x86_64-xen/geli.mod` — MUST
- 67: `/boot/flatcar/grub/x86_64-xen/gettext.mod` — MUST
- 68: `/boot/flatcar/grub/x86_64-xen/gfxmenu.mod` — MUST
- 69: `/boot/flatcar/grub/x86_64-xen/gfxterm.mod` — MUST
- 70: `/boot/flatcar/grub/x86_64-xen/gfxterm_background.mod` — MUST
- 71: `/boot/flatcar/grub/x86_64-xen/gpt.mod` — MUST
- 72: `/boot/flatcar/grub/x86_64-xen/gptrepair.mod` — MUST
- 73: `/boot/flatcar/grub/x86_64-xen/gptsync.mod` — MUST
- 74: `/boot/flatcar/grub/x86_64-xen/gzio.mod` — MUST
- 75: `/boot/flatcar/grub/x86_64-xen/halt.mod` — MUST
- 76: `/boot/flatcar/grub/x86_64-xen/hashsum.mod` — MUST
- 77: `/boot/flatcar/grub/x86_64-xen/hello.mod` — MUST
- 78: `/boot/flatcar/grub/x86_64-xen/help.mod` — MUST
- 79: `/boot/flatcar/grub/x86_64-xen/hexdump.mod` — MUST
- 80: `/boot/flatcar/grub/x86_64-xen/hfs.mod` — MUST
- 81: `/boot/flatcar/grub/x86_64-xen/hfsplus.mod` — MUST
- 82: `/boot/flatcar/grub/x86_64-xen/hfspluscomp.mod` — MUST
- 83: `/boot/flatcar/grub/x86_64-xen/http.mod` — MUST
- 84: `/boot/flatcar/grub/x86_64-xen/increment.mod` — MUST
- 85: `/boot/flatcar/grub/x86_64-xen/iso9660.mod` — MUST
- 86: `/boot/flatcar/grub/x86_64-xen/jfs.mod` — MUST
- 87: `/boot/flatcar/grub/x86_64-xen/jpeg.mod` — MUST
- 88: `/boot/flatcar/grub/x86_64-xen/json.mod` — MUST
- 89: `/boot/flatcar/grub/x86_64-xen/keystatus.mod` — MUST
- 90: `/boot/flatcar/grub/x86_64-xen/ldm.mod` — MUST
- 91: `/boot/flatcar/grub/x86_64-xen/legacycfg.mod` — MUST
- 92: `/boot/flatcar/grub/x86_64-xen/linux.mod` — MUST
- 93: `/boot/flatcar/grub/x86_64-xen/load.cfg` — UNKNOWN
- 94: `/boot/flatcar/grub/x86_64-xen/loadenv.mod` — MUST
- 95: `/boot/flatcar/grub/x86_64-xen/loopback.mod` — MUST
- 96: `/boot/flatcar/grub/x86_64-xen/ls.mod` — MUST
- 97: `/boot/flatcar/grub/x86_64-xen/lsmmap.mod` — MUST
- 98: `/boot/flatcar/grub/x86_64-xen/lsxen.mod` — MUST
- 99: `/boot/flatcar/grub/x86_64-xen/luks.mod` — MUST
- 100: `/boot/flatcar/grub/x86_64-xen/luks2.mod` — MUST
- 101: `/boot/flatcar/grub/x86_64-xen/lvm.mod` — MUST
- 102: `/boot/flatcar/grub/x86_64-xen/lzopio.mod` — MUST
- 103: `/boot/flatcar/grub/x86_64-xen/macbless.mod` — MUST
- 104: `/boot/flatcar/grub/x86_64-xen/macho.mod` — MUST
- 105: `/boot/flatcar/grub/x86_64-xen/mdraid09.mod` — MUST
- 106: `/boot/flatcar/grub/x86_64-xen/mdraid09_be.mod` — MUST
- 107: `/boot/flatcar/grub/x86_64-xen/mdraid1x.mod` — MUST
- 108: `/boot/flatcar/grub/x86_64-xen/memrw.mod` — MUST
- 109: `/boot/flatcar/grub/x86_64-xen/minicmd.mod` — MUST
- 110: `/boot/flatcar/grub/x86_64-xen/minix.mod` — MUST
- 111: `/boot/flatcar/grub/x86_64-xen/minix2.mod` — MUST
- 112: `/boot/flatcar/grub/x86_64-xen/minix2_be.mod` — MUST
- 113: `/boot/flatcar/grub/x86_64-xen/minix3.mod` — MUST
- 114: `/boot/flatcar/grub/x86_64-xen/minix3_be.mod` — MUST
- 115: `/boot/flatcar/grub/x86_64-xen/minix_be.mod` — MUST
- 116: `/boot/flatcar/grub/x86_64-xen/moddep.lst` — HOLE
- 117: `/boot/flatcar/grub/x86_64-xen/mpi.mod` — MUST
- 118: `/boot/flatcar/grub/x86_64-xen/msdospart.mod` — MUST
- 119: `/boot/flatcar/grub/x86_64-xen/net.mod` — MUST
- 120: `/boot/flatcar/grub/x86_64-xen/newc.mod` — MUST
- 121: `/boot/flatcar/grub/x86_64-xen/nilfs2.mod` — MUST
- 122: `/boot/flatcar/grub/x86_64-xen/ntfs.mod` — MUST
- 123: `/boot/flatcar/grub/x86_64-xen/ntfscomp.mod` — MUST
- 124: `/boot/flatcar/grub/x86_64-xen/odc.mod` — MUST
- 125: `/boot/flatcar/grub/x86_64-xen/offsetio.mod` — MUST
- 126: `/boot/flatcar/grub/x86_64-xen/part_acorn.mod` — MUST
- 127: `/boot/flatcar/grub/x86_64-xen/part_amiga.mod` — MUST
- 128: `/boot/flatcar/grub/x86_64-xen/part_apple.mod` — MUST
- 129: `/boot/flatcar/grub/x86_64-xen/part_bsd.mod` — MUST
- 130: `/boot/flatcar/grub/x86_64-xen/part_dfly.mod` — MUST
- 131: `/boot/flatcar/grub/x86_64-xen/part_dvh.mod` — MUST
- 132: `/boot/flatcar/grub/x86_64-xen/part_msdos.mod` — MUST
- 133: `/boot/flatcar/grub/x86_64-xen/part_plan.mod` — MUST
- 134: `/boot/flatcar/grub/x86_64-xen/part_sun.mod` — MUST
- 135: `/boot/flatcar/grub/x86_64-xen/part_sunpc.mod` — MUST
- 136: `/boot/flatcar/grub/x86_64-xen/partmap.lst` — HOLE
- 137: `/boot/flatcar/grub/x86_64-xen/parttool.lst` — HOLE
- 138: `/boot/flatcar/grub/x86_64-xen/parttool.mod` — MUST
- 139: `/boot/flatcar/grub/x86_64-xen/password.mod` — MUST
- 140: `/boot/flatcar/grub/x86_64-xen/password_pbkdf2.mod` — MUST
- 141: `/boot/flatcar/grub/x86_64-xen/pbkdf2.mod` — MUST
- 142: `/boot/flatcar/grub/x86_64-xen/pgp.mod` — MUST
- 143: `/boot/flatcar/grub/x86_64-xen/pkcs1_v15.mod` — MUST
- 144: `/boot/flatcar/grub/x86_64-xen/plainmount.mod` — MUST
- 145: `/boot/flatcar/grub/x86_64-xen/png.mod` — MUST
- 146: `/boot/flatcar/grub/x86_64-xen/priority_queue.mod` — MUST
- 147: `/boot/flatcar/grub/x86_64-xen/probe.mod` — MUST
- 148: `/boot/flatcar/grub/x86_64-xen/procfs.mod` — MUST
- 149: `/boot/flatcar/grub/x86_64-xen/progress.mod` — MUST
- 150: `/boot/flatcar/grub/x86_64-xen/raid5rec.mod` — MUST
- 151: `/boot/flatcar/grub/x86_64-xen/raid6rec.mod` — MUST
- 152: `/boot/flatcar/grub/x86_64-xen/reboot.mod` — MUST
- 153: `/boot/flatcar/grub/x86_64-xen/regexp.mod` — MUST
- 154: `/boot/flatcar/grub/x86_64-xen/reiserfs.mod` — MUST
- 155: `/boot/flatcar/grub/x86_64-xen/relocator.mod` — MUST
- 156: `/boot/flatcar/grub/x86_64-xen/romfs.mod` — MUST
- 157: `/boot/flatcar/grub/x86_64-xen/scsi.mod` — MUST
- 158: `/boot/flatcar/grub/x86_64-xen/search_fs_file.mod` — MUST
- 159: `/boot/flatcar/grub/x86_64-xen/search_label.mod` — MUST
- 160: `/boot/flatcar/grub/x86_64-xen/search_part_uuid.mod` — MUST
- 161: `/boot/flatcar/grub/x86_64-xen/setjmp.mod` — MUST
- 162: `/boot/flatcar/grub/x86_64-xen/sfs.mod` — MUST
- 163: `/boot/flatcar/grub/x86_64-xen/sleep.mod` — MUST
- 164: `/boot/flatcar/grub/x86_64-xen/squash4.mod` — MUST
- 165: `/boot/flatcar/grub/x86_64-xen/syslinuxcfg.mod` — MUST
- 166: `/boot/flatcar/grub/x86_64-xen/terminal.lst` — HOLE
- 167: `/boot/flatcar/grub/x86_64-xen/testload.mod` — MUST
- 168: `/boot/flatcar/grub/x86_64-xen/testspeed.mod` — MUST
- 169: `/boot/flatcar/grub/x86_64-xen/tftp.mod` — MUST
- 170: `/boot/flatcar/grub/x86_64-xen/tga.mod` — MUST
- 171: `/boot/flatcar/grub/x86_64-xen/time.mod` — MUST
- 172: `/boot/flatcar/grub/x86_64-xen/tr.mod` — MUST
- 173: `/boot/flatcar/grub/x86_64-xen/trig.mod` — MUST
- 174: `/boot/flatcar/grub/x86_64-xen/true.mod` — MUST
- 175: `/boot/flatcar/grub/x86_64-xen/udf.mod` — MUST
- 176: `/boot/flatcar/grub/x86_64-xen/ufs1.mod` — MUST
- 177: `/boot/flatcar/grub/x86_64-xen/ufs1_be.mod` — MUST
- 178: `/boot/flatcar/grub/x86_64-xen/ufs2.mod` — MUST
- 179: `/boot/flatcar/grub/x86_64-xen/version.mod` — MUST
- 180: `/boot/flatcar/grub/x86_64-xen/video.lst` — HOLE
- 181: `/boot/flatcar/grub/x86_64-xen/video.mod` — MUST
- 182: `/boot/flatcar/grub/x86_64-xen/video_colors.mod` — MUST
- 183: `/boot/flatcar/grub/x86_64-xen/video_fb.mod` — MUST
- 184: `/boot/flatcar/grub/x86_64-xen/videoinfo.mod` — MUST
- 185: `/boot/flatcar/grub/x86_64-xen/videotest.mod` — MUST
- 186: `/boot/flatcar/grub/x86_64-xen/xfs.mod` — MUST
- 187: `/boot/flatcar/grub/x86_64-xen/xnu_uuid.mod` — MUST
- 188: `/boot/flatcar/grub/x86_64-xen/zfs.mod` — MUST
- 189: `/boot/flatcar/grub/x86_64-xen/zfscrypt.mod` — MUST
- 190: `/boot/flatcar/grub/x86_64-xen/zfsinfo.mod` — MUST
- 191: `/boot/flatcar/grub/x86_64-xen/zstd.mod` — MUST

### Correction flatcar-ea240c7b8257d2e5ce718e32
MUST → UNKNOWN. Inspected grub_install.sh: grub-mkimage consumes load.cfg with --config; the separately retained copy has no established runtime consumer.

### Correction flatcar-f4ec5e1afe79e8134ad617be
MUST → UNKNOWN. useradd documents copying templates, not executing them. The inventory has no contents of these templates.

### Correction flatcar-e20b758d51ecb8b4bc396bfb
UNKNOWN → MIXED. Kernel rules affect system auditing; plugin and daemon setting values remain unavailable.
Corrected complete member map (supersedes earlier map):
- 1: `/etc/audit/audisp-filter.conf` — UNKNOWN
- 2: `/etc/audit/audisp-remote.conf` — UNKNOWN
- 3: `/etc/audit/audit-stop.rules` — MUST
- 4: `/etc/audit/audit.rules` — MUST
- 5: `/etc/audit/auditd.conf` — UNKNOWN
- 6: `/etc/audit/plugins.d` — UNKNOWN
- 7: `/etc/audit/rules.d` — MUST

### Correction flatcar-6af53e326cce5228408a6307
UNKNOWN → MIXED. Policy trees supply system access controls; uncaptured selection and management values remain unknown.
Corrected complete member map (supersedes earlier map):
- 1: `/etc/selinux/config` — UNKNOWN
- 2: `/etc/selinux/mcs` — MUST
- 3: `/etc/selinux/mls` — MUST
- 4: `/etc/selinux/semanage.conf` — UNKNOWN
- 5: `/etc/selinux/targeted` — MUST

### Correction flatcar-73e390997be4f5bde0ca5a28
UNKNOWN → MIXED. Trust store serves multiple programs; marker is bookkeeping; cryptographic configuration values are uncaptured.
Corrected complete member map (supersedes earlier map):
- 1: `/etc/ssl/certs` — MUST
- 2: `/etc/ssl/fipsmodule.cnf` — UNKNOWN
- 3: `/etc/ssl/openssl.cnf` — UNKNOWN
- 4: `/etc/ssl/private` — NOT

### Correction flatcar-43d0c22d212a2cad83c0bab0
UNKNOWN → MIXED. Timer enablement affects execution; marker directories are bookkeeping; actual service-configuration values are uncaptured.
Corrected complete member map (supersedes earlier map):
- 1: `/etc/systemd/coredump.conf` — UNKNOWN
- 2: `/etc/systemd/journal-remote.conf` — UNKNOWN
- 3: `/etc/systemd/journal-upload.conf` — UNKNOWN
- 4: `/etc/systemd/journald.conf` — UNKNOWN
- 5: `/etc/systemd/logind.conf` — UNKNOWN
- 6: `/etc/systemd/network` — NOT
- 7: `/etc/systemd/networkd.conf` — UNKNOWN
- 8: `/etc/systemd/oomd.conf` — UNKNOWN
- 9: `/etc/systemd/pstore.conf` — UNKNOWN
- 10: `/etc/systemd/resolved.conf` — UNKNOWN
- 11: `/etc/systemd/sleep.conf` — UNKNOWN
- 12: `/etc/systemd/system` — MUST
- 13: `/etc/systemd/system.conf` — UNKNOWN
- 14: `/etc/systemd/timesyncd.conf` — UNKNOWN
- 15: `/etc/systemd/user` — NOT
- 16: `/etc/systemd/user.conf` — UNKNOWN

### Correction flatcar-7955ed3fbebf581406d0ce57
MIXED → MIXED. Account/code/system effects require recording; markers/history/content are exempt; other uncaptured effects remain unknown.
Corrected complete member map (supersedes earlier map):
- 1: `/etc/.ignition-result.json` — NOT
- 2: `/etc/.pwd.lock` — UNKNOWN
- 3: `/etc/.systemd-confext` — MUST
- 4: `/etc/.updated` — UNKNOWN
- 5: `/etc/X11` — MUST
- 6: `/etc/audit` — MUST
- 7: `/etc/azure-ephemeral-disk-setup.conf` — UNKNOWN
- 8: `/etc/bash` — MUST
- 9: `/etc/bindresvport.blacklist` — UNKNOWN
- 10: `/etc/binfmt.d` — NOT
- 11: `/etc/cifs-utils` — UNKNOWN
- 12: `/etc/cni` — UNKNOWN
- 13: `/etc/conntrackd` — UNKNOWN
- 14: `/etc/coreos` — UNKNOWN
- 15: `/etc/credstore` — UNKNOWN
- 16: `/etc/credstore.encrypted` — UNKNOWN
- 17: `/etc/dbus-1` — MUST
- 18: `/etc/default` — MUST
- 19: `/etc/dracut.conf` — UNKNOWN
- 20: `/etc/e2scrub.conf` — UNKNOWN
- 21: `/etc/environment.d` — MUST
- 22: `/etc/ethertypes` — UNKNOWN
- 23: `/etc/extension-release.d` — MUST
- 24: `/etc/extensions` — MUST
- 25: `/etc/flatcar` — UNKNOWN
- 26: `/etc/group` — MUST
- 27: `/etc/group-` — NOT
- 28: `/etc/gshadow` — MUST
- 29: `/etc/gshadow-` — NOT
- 30: `/etc/hosts` — MUST
- 31: `/etc/idmapd.conf` — UNKNOWN
- 32: `/etc/init.d` — UNKNOWN
- 33: `/etc/iscsi` — UNKNOWN
- 34: `/etc/isns` — UNKNOWN
- 35: `/etc/issue` — NOT
- 36: `/etc/kernel` — NOT
- 37: `/etc/kexec.conf` — UNKNOWN
- 38: `/etc/keyutils` — UNKNOWN
- 39: `/etc/krb5.conf.example` — NOT
- 40: `/etc/ld.so.cache` — UNKNOWN
- 41: `/etc/ldap.conf.sudo` — UNKNOWN
- 42: `/etc/lessfilter.d` — UNKNOWN
- 43: `/etc/libaudit.conf` — UNKNOWN
- 44: `/etc/locale.conf` — MUST
- 45: `/etc/login.defs` — MUST
- 46: `/etc/logrotate.conf` — UNKNOWN
- 47: `/etc/logrotate.d` — UNKNOWN
- 48: `/etc/lvm` — UNKNOWN
- 49: `/etc/machine-id` — MUST
- 50: `/etc/mke2fs.conf` — UNKNOWN
- 51: `/etc/modules-load.d` — NOT
- 52: `/etc/motd` — NOT
- 53: `/etc/mtab` — UNKNOWN
- 54: `/etc/netconfig` — UNKNOWN
- 55: `/etc/nscd.conf` — UNKNOWN
- 56: `/etc/ntp.conf` — UNKNOWN
- 57: `/etc/nvme` — UNKNOWN
- 58: `/etc/openldap` — UNKNOWN
- 59: `/etc/pam.d` — NOT
- 60: `/etc/passwd` — MUST
- 61: `/etc/passwd-` — NOT
- 62: `/etc/pkcs11` — NOT
- 63: `/etc/polkit-1` — NOT
- 64: `/etc/profile.d` — MUST
- 65: `/etc/quotagrpadmins` — UNKNOWN
- 66: `/etc/quotatab` — UNKNOWN
- 67: `/etc/request-key.conf` — MUST
- 68: `/etc/request-key.d` — MUST
- 69: `/etc/resolv.conf` — MUST
- 70: `/etc/runlevels` — UNKNOWN
- 71: `/etc/sasl2` — UNKNOWN
- 72: `/etc/securetty` — MUST
- 73: `/etc/security` — NOT
- 74: `/etc/selinux` — MUST
- 75: `/etc/sestatus.conf` — UNKNOWN
- 76: `/etc/shadow` — UNKNOWN
- 77: `/etc/shadow-` — NOT
- 78: `/etc/skel` — UNKNOWN
- 79: `/etc/ssh` — MUST
- 80: `/etc/ssl` — MUST
- 81: `/etc/sssd` — MUST
- 82: `/etc/subgid` — MUST
- 83: `/etc/subgid-` — NOT
- 84: `/etc/subuid` — MUST
- 85: `/etc/subuid-` — NOT
- 86: `/etc/sudo_logsrvd.conf` — UNKNOWN
- 87: `/etc/sudoers.d` — NOT
- 88: `/etc/sudoers.dist` — UNKNOWN
- 89: `/etc/sysconfig` — UNKNOWN
- 90: `/etc/systemd` — MUST
- 91: `/etc/tcsd.conf` — UNKNOWN
- 92: `/etc/tmpfiles.d` — NOT
- 93: `/etc/tpm2-tss` — UNKNOWN
- 94: `/etc/udev` — MUST
- 95: `/etc/user` — UNKNOWN
- 96: `/etc/vim` — UNKNOWN
- 97: `/etc/warnquota.conf` — UNKNOWN
- 98: `/etc/whois.conf` — UNKNOWN
- 99: `/etc/wireguard` — UNKNOWN
- 100: `/etc/xattr.conf` — UNKNOWN
- 101: `/etc/xdg` — NOT

## Documentation record and interpretation details

The following short quotations establish program roles. Row `basis` identifies either the raw member snapshot or the primary documentation used; this section supplies additional role documentation. UNKNOWN is not an inference that no public documentation exists: the documentation establishes the file format or generic facility, while the actual captured object's contents or consumer dependency remains unavailable. Empty directories are not equated with the programs whose names appear in their paths. No design question about retaining or migrating state is used as a HOLE.

- https://raw.githubusercontent.com/flatcar/scripts/main/build_library/grub_install.sh — “Generate a memdisk containing the appropriately generated grub.cfg.” The script embeds load.cfg and grub.cfg.tar into separate boot images. Its i386 branch also saves patched boot bytes. Therefore separately retained construction inputs are not assumed active merely from their names. In the corrected module groups: `.mod` and `core.img` MUST; `.lst` NOT (program-local values under S2.2-7 and S2.2-13); `mbr.bin` HOLE (past bytes versus restoration capability); `boot.img` and `load.cfg` UNKNOWN (installed-copy consumer unestablished). The source establishes image construction, not runtime use of every intermediate file.
- https://raw.githubusercontent.com/rhboot/grub2/master/docs/grub.texi — “a flexible and powerful boot loader program”. GRUB executable images and modules supply native boot functionality. Native code is not confined web-page/guest code under S2.2-11.
- https://raw.githubusercontent.com/shadow-maint/shadow/master/man/useradd.8.xml — “The files and directories contained in the skeleton directory”. The surrounding documentation specifies copying into new homes. Copying alone does not establish that these particular templates contain commands; their contents were not captured. This narrows the initial template decision to UNKNOWN.
- https://docs.kernel.org/filesystems/overlayfs.html — “the result of overlaying one filesystem on top of the other.” The recorded configuration work directory supports the overlay mount; this is filesystem behavior shared across programs.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-sysext.html — “systemd-sysext activates/deactivates system extension images.” Extension references and compatibility information select resources merged into system directories. The separately stored image group remains UNKNOWN where image and selection-marker contents are absent.
- https://dbus.freedesktop.org/doc/dbus-daemon.1.html — “Multiple programs connect to the message bus daemon and can exchange messages with one another.” Bus sockets and access/activation configuration serve interprocess behavior.
- https://raw.githubusercontent.com/linux-audit/audit-userspace/master/docs/audit.rules.7 — “a set of rules loaded in the kernel audit system”. Audit rule files have kernel effects; uncaptured plugin settings are not assumed equivalent to those rules.
- https://raw.githubusercontent.com/logrotate/logrotate/main/logrotate.8.in — “It allows automatic rotation, compression, removal, and mailing of log files.” Rotation configuration controls filesystem actions, unlike the logs themselves.
- https://raw.githubusercontent.com/SSSD/sssd/master/src/man/sssd.conf.5.xml — “the configuration file for SSSD”. Authentication/identity configuration affects account access. Empty state/IPC directories do not prove populated databases or active sockets.
- https://raw.githubusercontent.com/SELinuxProject/selinux/master/libselinux/man/man5/selabel_file.5 — “The file contexts backend maps from pathname/mode combinations into security contexts.” The three policy trees were inspected individually: contexts and user mappings affect labels/access; compiled `.bin` equivalents accelerate lookup; `.keep` files are markers. The mcs/mls/targeted counterpart groups were each checked against the raw member list; they were not inferred from a shared directory name alone.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html — “Unit configuration”. Its documented search paths include transient, generated and administrator units. Unit definitions, dependencies and enablement change processes/mounts beyond the manager interface.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html — “for socket-based activation”. Actual socket inodes and their observed aliases provide connection paths; they are not cached or historical descriptions of those paths.
- https://www.freedesktop.org/software/systemd/man/latest/varlinkctl.html — “Directory containing `AF_UNIX` entrypoint socket inodes (or symlinks to them)”. The registry files identify public IPC endpoints. All members of the two registry groups were verified as symlinks to recorded sockets.
- https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.exec.xml — “a new file system namespace will be set up for the executed processes”. Private temporary directories and inaccessible nodes implement cross-process filesystem separation. They are not merely presentation settings of one application.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html — “Networks are applied to links whenever the links appear.” Network rules, generated resolver configuration and shared interface status concern system connectivity outside the reader.
- https://www.freedesktop.org/software/systemd/man/latest/udev.html — “All device information udev processes is stored in the udev database and sent out to possible event subscribers.” Database entries and tags supply information to other programs. They are not assumed speed-only caches.
- https://raw.githubusercontent.com/systemd/systemd/v260/src/udev/udev-node.c — “With the new format, the devnode and priority can be obtained from symlink itself.” The matching version also implements the link-stack association behavior used for Rule U; raw symlinks use this priority:device format.
- https://raw.githubusercontent.com/systemd/systemd/v260/src/udev/udev-watch.c — `udev_watch_begin`. Device watches and their saved associations map notifications to affected devices. The raw group contains reciprocal watch/device symlinks.
- https://man.openbsd.org/sshd.8 — “The forked daemons handle key exchange, encryption, authentication, command execution, and data exchange.” Host authentication keys and server settings enable account login; client default settings are program-local values. Current authorized-key files are distinct from the named old directory.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html — “collects and stores logging data”. Journal files and conventional login/audit logs retain past events; live logging sockets are not historical records.
- https://www.freedesktop.org/software/systemd/man/latest/os-release.html — “contain operating system identification data.” Staged release files supply content, not executable commands. Extension compatibility metadata has a different selection role, covered separately.
- https://www.freedesktop.org/software/systemd/man/latest/machine-id.html — “This machine ID adheres to the same format and logic as the D-Bus machine ID.” The recorded D-Bus alias exposes shared identity to programs.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-tmpfiles.html — “creates, deletes, and cleans up files and directories”. The generated static-node rules affect system device availability.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html — “the time when the service unit was last triggered is stored on disk.” Persistent timers use this historical timestamp to determine catch-up activation. S2.2-1 requires behavioral dependencies while S2.2-6 exempts history; neither states precedence for a past-event record that drives future execution.
- https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html — “A file that is touched on each successful synchronization”. The synchronization marker informs dependent services, while the saved clock timestamp advances the next boot's clock. Their HOLE is the explicit history/behavior intersection, not a general objection to program state.
- https://raw.githubusercontent.com/containerd/containerd/main/docs/ops.md — “containerd is a high performance container runtime”. This establishes the runtime role, but does not reveal captured Bolt database entries; those groups remain UNKNOWN.
- https://docs.docker.com/engine/storage/drivers/overlayfs-driver/ — “OverlayFS storage driver”. Documented layer-storage roles cannot establish actual images or network/volume database contents in the inventory; empty directories and undecoded databases remain UNKNOWN.

## Per-row verification

The only bulk homogeneous decisions are Rule U and Rule K, each with ten named hand checks above. Other rows were inspected individually, including corresponding SELinux policy directories with separately enumerated memberships. The script is a transcription helper, not authority for inference from a path prefix. MIXED positions always refer to the input's one-based member array; complete mappings are recorded above. Correction sections supersede earlier mappings, preserving the audit of narrowed claims.

Validation passed: 386 exact unique assigned IDs; allowed decisions; 15/30-word limits; every MIXED member assigned exactly once. Counts: {'NOT': 41, 'MUST': 237, 'MIXED': 45, 'UNKNOWN': 60, 'HOLE': 3}.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/grub.cfg.tar` — UNKNOWN
- 2: `/boot/flatcar/grub/i386-pc` — MUST
- 3: `/boot/flatcar/grub/x86_64-efi` — UNKNOWN
- 4: `/boot/flatcar/grub/x86_64-xen` — MUST

### Correction flatcar-aa489ee21d27f0b113d367ca
MIXED → MIXED. Code requires recording; indexes are program-local values; saved boot bytes conflict with history exemption; construction-input consumers are unknown.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/i386-pc/acpi.mod` — MUST
- 2: `/boot/flatcar/grub/i386-pc/adler32.mod` — MUST
- 3: `/boot/flatcar/grub/i386-pc/affs.mod` — MUST
- 4: `/boot/flatcar/grub/i386-pc/afs.mod` — MUST
- 5: `/boot/flatcar/grub/i386-pc/afsplitter.mod` — MUST
- 6: `/boot/flatcar/grub/i386-pc/ahci.mod` — MUST
- 7: `/boot/flatcar/grub/i386-pc/all_video.mod` — MUST
- 8: `/boot/flatcar/grub/i386-pc/aout.mod` — MUST
- 9: `/boot/flatcar/grub/i386-pc/appendedsig.mod` — MUST
- 10: `/boot/flatcar/grub/i386-pc/archelp.mod` — MUST
- 11: `/boot/flatcar/grub/i386-pc/asn1.mod` — MUST
- 12: `/boot/flatcar/grub/i386-pc/at_keyboard.mod` — MUST
- 13: `/boot/flatcar/grub/i386-pc/ata.mod` — MUST
- 14: `/boot/flatcar/grub/i386-pc/backtrace.mod` — MUST
- 15: `/boot/flatcar/grub/i386-pc/bfs.mod` — MUST
- 16: `/boot/flatcar/grub/i386-pc/bitmap.mod` — MUST
- 17: `/boot/flatcar/grub/i386-pc/bitmap_scale.mod` — MUST
- 18: `/boot/flatcar/grub/i386-pc/blocklist.mod` — MUST
- 19: `/boot/flatcar/grub/i386-pc/blscfg.mod` — MUST
- 20: `/boot/flatcar/grub/i386-pc/boot.img` — UNKNOWN
- 21: `/boot/flatcar/grub/i386-pc/boot.mod` — MUST
- 22: `/boot/flatcar/grub/i386-pc/bsd.mod` — MUST
- 23: `/boot/flatcar/grub/i386-pc/bufio.mod` — MUST
- 24: `/boot/flatcar/grub/i386-pc/cat.mod` — MUST
- 25: `/boot/flatcar/grub/i386-pc/cbfs.mod` — MUST
- 26: `/boot/flatcar/grub/i386-pc/cbls.mod` — MUST
- 27: `/boot/flatcar/grub/i386-pc/cbmemc.mod` — MUST
- 28: `/boot/flatcar/grub/i386-pc/cbtable.mod` — MUST
- 29: `/boot/flatcar/grub/i386-pc/cbtime.mod` — MUST
- 30: `/boot/flatcar/grub/i386-pc/chain.mod` — MUST
- 31: `/boot/flatcar/grub/i386-pc/cmosdump.mod` — MUST
- 32: `/boot/flatcar/grub/i386-pc/cmostest.mod` — MUST
- 33: `/boot/flatcar/grub/i386-pc/cmp.mod` — MUST
- 34: `/boot/flatcar/grub/i386-pc/command.lst` — NOT
- 35: `/boot/flatcar/grub/i386-pc/core.img` — MUST
- 36: `/boot/flatcar/grub/i386-pc/cpio.mod` — MUST
- 37: `/boot/flatcar/grub/i386-pc/cpio_be.mod` — MUST
- 38: `/boot/flatcar/grub/i386-pc/cpuid.mod` — MUST
- 39: `/boot/flatcar/grub/i386-pc/crc64.mod` — MUST
- 40: `/boot/flatcar/grub/i386-pc/crypto.lst` — NOT
- 41: `/boot/flatcar/grub/i386-pc/crypto.mod` — MUST
- 42: `/boot/flatcar/grub/i386-pc/cryptodisk.mod` — MUST
- 43: `/boot/flatcar/grub/i386-pc/cs5536.mod` — MUST
- 44: `/boot/flatcar/grub/i386-pc/date.mod` — MUST
- 45: `/boot/flatcar/grub/i386-pc/datehook.mod` — MUST
- 46: `/boot/flatcar/grub/i386-pc/datetime.mod` — MUST
- 47: `/boot/flatcar/grub/i386-pc/disk.mod` — MUST
- 48: `/boot/flatcar/grub/i386-pc/diskfilter.mod` — MUST
- 49: `/boot/flatcar/grub/i386-pc/div.mod` — MUST
- 50: `/boot/flatcar/grub/i386-pc/dm_nv.mod` — MUST
- 51: `/boot/flatcar/grub/i386-pc/drivemap.mod` — MUST
- 52: `/boot/flatcar/grub/i386-pc/efiemu.mod` — MUST
- 53: `/boot/flatcar/grub/i386-pc/ehci.mod` — MUST
- 54: `/boot/flatcar/grub/i386-pc/elf.mod` — MUST
- 55: `/boot/flatcar/grub/i386-pc/eval.mod` — MUST
- 56: `/boot/flatcar/grub/i386-pc/exfat.mod` — MUST
- 57: `/boot/flatcar/grub/i386-pc/ext2.mod` — MUST
- 58: `/boot/flatcar/grub/i386-pc/extcmd.mod` — MUST
- 59: `/boot/flatcar/grub/i386-pc/f2fs.mod` — MUST
- 60: `/boot/flatcar/grub/i386-pc/fdt.lst` — NOT
- 61: `/boot/flatcar/grub/i386-pc/file.mod` — MUST
- 62: `/boot/flatcar/grub/i386-pc/font.mod` — MUST
- 63: `/boot/flatcar/grub/i386-pc/freedos.mod` — MUST
- 64: `/boot/flatcar/grub/i386-pc/fs.lst` — NOT
- 65: `/boot/flatcar/grub/i386-pc/fshelp.mod` — MUST
- 66: `/boot/flatcar/grub/i386-pc/gcry_arcfour.mod` — MUST
- 67: `/boot/flatcar/grub/i386-pc/gcry_blowfish.mod` — MUST
- 68: `/boot/flatcar/grub/i386-pc/gcry_camellia.mod` — MUST
- 69: `/boot/flatcar/grub/i386-pc/gcry_cast5.mod` — MUST
- 70: `/boot/flatcar/grub/i386-pc/gcry_crc.mod` — MUST
- 71: `/boot/flatcar/grub/i386-pc/gcry_des.mod` — MUST
- 72: `/boot/flatcar/grub/i386-pc/gcry_dsa.mod` — MUST
- 73: `/boot/flatcar/grub/i386-pc/gcry_idea.mod` — MUST
- 74: `/boot/flatcar/grub/i386-pc/gcry_md4.mod` — MUST
- 75: `/boot/flatcar/grub/i386-pc/gcry_md5.mod` — MUST
- 76: `/boot/flatcar/grub/i386-pc/gcry_rfc2268.mod` — MUST
- 77: `/boot/flatcar/grub/i386-pc/gcry_rijndael.mod` — MUST
- 78: `/boot/flatcar/grub/i386-pc/gcry_rmd160.mod` — MUST
- 79: `/boot/flatcar/grub/i386-pc/gcry_rsa.mod` — MUST
- 80: `/boot/flatcar/grub/i386-pc/gcry_seed.mod` — MUST
- 81: `/boot/flatcar/grub/i386-pc/gcry_serpent.mod` — MUST
- 82: `/boot/flatcar/grub/i386-pc/gcry_sha1.mod` — MUST
- 83: `/boot/flatcar/grub/i386-pc/gcry_sha256.mod` — MUST
- 84: `/boot/flatcar/grub/i386-pc/gcry_sha512.mod` — MUST
- 85: `/boot/flatcar/grub/i386-pc/gcry_tiger.mod` — MUST
- 86: `/boot/flatcar/grub/i386-pc/gcry_twofish.mod` — MUST
- 87: `/boot/flatcar/grub/i386-pc/gcry_whirlpool.mod` — MUST
- 88: `/boot/flatcar/grub/i386-pc/gdb.mod` — MUST
- 89: `/boot/flatcar/grub/i386-pc/geli.mod` — MUST
- 90: `/boot/flatcar/grub/i386-pc/gettext.mod` — MUST
- 91: `/boot/flatcar/grub/i386-pc/gfxmenu.mod` — MUST
- 92: `/boot/flatcar/grub/i386-pc/gfxterm.mod` — MUST
- 93: `/boot/flatcar/grub/i386-pc/gfxterm_background.mod` — MUST
- 94: `/boot/flatcar/grub/i386-pc/gpt.mod` — MUST
- 95: `/boot/flatcar/grub/i386-pc/gptrepair.mod` — MUST
- 96: `/boot/flatcar/grub/i386-pc/gptsync.mod` — MUST
- 97: `/boot/flatcar/grub/i386-pc/gzio.mod` — MUST
- 98: `/boot/flatcar/grub/i386-pc/halt.mod` — MUST
- 99: `/boot/flatcar/grub/i386-pc/hashsum.mod` — MUST
- 100: `/boot/flatcar/grub/i386-pc/hdparm.mod` — MUST
- 101: `/boot/flatcar/grub/i386-pc/hello.mod` — MUST
- 102: `/boot/flatcar/grub/i386-pc/help.mod` — MUST
- 103: `/boot/flatcar/grub/i386-pc/hexdump.mod` — MUST
- 104: `/boot/flatcar/grub/i386-pc/hfs.mod` — MUST
- 105: `/boot/flatcar/grub/i386-pc/hfsplus.mod` — MUST
- 106: `/boot/flatcar/grub/i386-pc/hfspluscomp.mod` — MUST
- 107: `/boot/flatcar/grub/i386-pc/http.mod` — MUST
- 108: `/boot/flatcar/grub/i386-pc/increment.mod` — MUST
- 109: `/boot/flatcar/grub/i386-pc/iorw.mod` — MUST
- 110: `/boot/flatcar/grub/i386-pc/iso9660.mod` — MUST
- 111: `/boot/flatcar/grub/i386-pc/jfs.mod` — MUST
- 112: `/boot/flatcar/grub/i386-pc/jpeg.mod` — MUST
- 113: `/boot/flatcar/grub/i386-pc/json.mod` — MUST
- 114: `/boot/flatcar/grub/i386-pc/keylayouts.mod` — MUST
- 115: `/boot/flatcar/grub/i386-pc/keystatus.mod` — MUST
- 116: `/boot/flatcar/grub/i386-pc/ldm.mod` — MUST
- 117: `/boot/flatcar/grub/i386-pc/legacycfg.mod` — MUST
- 118: `/boot/flatcar/grub/i386-pc/linux.mod` — MUST
- 119: `/boot/flatcar/grub/i386-pc/load.cfg` — UNKNOWN
- 120: `/boot/flatcar/grub/i386-pc/loadenv.mod` — MUST
- 121: `/boot/flatcar/grub/i386-pc/loopback.mod` — MUST
- 122: `/boot/flatcar/grub/i386-pc/ls.mod` — MUST
- 123: `/boot/flatcar/grub/i386-pc/lsacpi.mod` — MUST
- 124: `/boot/flatcar/grub/i386-pc/lsapm.mod` — MUST
- 125: `/boot/flatcar/grub/i386-pc/lsmmap.mod` — MUST
- 126: `/boot/flatcar/grub/i386-pc/lspci.mod` — MUST
- 127: `/boot/flatcar/grub/i386-pc/luks.mod` — MUST
- 128: `/boot/flatcar/grub/i386-pc/luks2.mod` — MUST
- 129: `/boot/flatcar/grub/i386-pc/lvm.mod` — MUST
- 130: `/boot/flatcar/grub/i386-pc/lzopio.mod` — MUST
- 131: `/boot/flatcar/grub/i386-pc/macbless.mod` — MUST
- 132: `/boot/flatcar/grub/i386-pc/macho.mod` — MUST
- 133: `/boot/flatcar/grub/i386-pc/mbr.bin` — HOLE
- 134: `/boot/flatcar/grub/i386-pc/mda_text.mod` — MUST
- 135: `/boot/flatcar/grub/i386-pc/mdraid09.mod` — MUST
- 136: `/boot/flatcar/grub/i386-pc/mdraid09_be.mod` — MUST
- 137: `/boot/flatcar/grub/i386-pc/mdraid1x.mod` — MUST
- 138: `/boot/flatcar/grub/i386-pc/memrw.mod` — MUST
- 139: `/boot/flatcar/grub/i386-pc/minicmd.mod` — MUST
- 140: `/boot/flatcar/grub/i386-pc/minix.mod` — MUST
- 141: `/boot/flatcar/grub/i386-pc/minix2.mod` — MUST
- 142: `/boot/flatcar/grub/i386-pc/minix2_be.mod` — MUST
- 143: `/boot/flatcar/grub/i386-pc/minix3.mod` — MUST
- 144: `/boot/flatcar/grub/i386-pc/minix3_be.mod` — MUST
- 145: `/boot/flatcar/grub/i386-pc/minix_be.mod` — MUST
- 146: `/boot/flatcar/grub/i386-pc/mmap.mod` — MUST
- 147: `/boot/flatcar/grub/i386-pc/moddep.lst` — NOT
- 148: `/boot/flatcar/grub/i386-pc/morse.mod` — MUST
- 149: `/boot/flatcar/grub/i386-pc/mpi.mod` — MUST
- 150: `/boot/flatcar/grub/i386-pc/msdospart.mod` — MUST
- 151: `/boot/flatcar/grub/i386-pc/multiboot.mod` — MUST
- 152: `/boot/flatcar/grub/i386-pc/multiboot2.mod` — MUST
- 153: `/boot/flatcar/grub/i386-pc/nativedisk.mod` — MUST
- 154: `/boot/flatcar/grub/i386-pc/net.mod` — MUST
- 155: `/boot/flatcar/grub/i386-pc/newc.mod` — MUST
- 156: `/boot/flatcar/grub/i386-pc/nilfs2.mod` — MUST
- 157: `/boot/flatcar/grub/i386-pc/ntfs.mod` — MUST
- 158: `/boot/flatcar/grub/i386-pc/ntfscomp.mod` — MUST
- 159: `/boot/flatcar/grub/i386-pc/ntldr.mod` — MUST
- 160: `/boot/flatcar/grub/i386-pc/odc.mod` — MUST
- 161: `/boot/flatcar/grub/i386-pc/offsetio.mod` — MUST
- 162: `/boot/flatcar/grub/i386-pc/ohci.mod` — MUST
- 163: `/boot/flatcar/grub/i386-pc/part_acorn.mod` — MUST
- 164: `/boot/flatcar/grub/i386-pc/part_amiga.mod` — MUST
- 165: `/boot/flatcar/grub/i386-pc/part_apple.mod` — MUST
- 166: `/boot/flatcar/grub/i386-pc/part_bsd.mod` — MUST
- 167: `/boot/flatcar/grub/i386-pc/part_dfly.mod` — MUST
- 168: `/boot/flatcar/grub/i386-pc/part_dvh.mod` — MUST
- 169: `/boot/flatcar/grub/i386-pc/part_msdos.mod` — MUST
- 170: `/boot/flatcar/grub/i386-pc/part_plan.mod` — MUST
- 171: `/boot/flatcar/grub/i386-pc/part_sun.mod` — MUST
- 172: `/boot/flatcar/grub/i386-pc/part_sunpc.mod` — MUST
- 173: `/boot/flatcar/grub/i386-pc/partmap.lst` — NOT
- 174: `/boot/flatcar/grub/i386-pc/parttool.lst` — NOT
- 175: `/boot/flatcar/grub/i386-pc/parttool.mod` — MUST
- 176: `/boot/flatcar/grub/i386-pc/password.mod` — MUST
- 177: `/boot/flatcar/grub/i386-pc/password_pbkdf2.mod` — MUST
- 178: `/boot/flatcar/grub/i386-pc/pata.mod` — MUST
- 179: `/boot/flatcar/grub/i386-pc/pbkdf2.mod` — MUST
- 180: `/boot/flatcar/grub/i386-pc/pci.mod` — MUST
- 181: `/boot/flatcar/grub/i386-pc/pcidump.mod` — MUST
- 182: `/boot/flatcar/grub/i386-pc/pgp.mod` — MUST
- 183: `/boot/flatcar/grub/i386-pc/pkcs1_v15.mod` — MUST
- 184: `/boot/flatcar/grub/i386-pc/plainmount.mod` — MUST
- 185: `/boot/flatcar/grub/i386-pc/plan9.mod` — MUST
- 186: `/boot/flatcar/grub/i386-pc/play.mod` — MUST
- 187: `/boot/flatcar/grub/i386-pc/png.mod` — MUST
- 188: `/boot/flatcar/grub/i386-pc/priority_queue.mod` — MUST
- 189: `/boot/flatcar/grub/i386-pc/probe.mod` — MUST
- 190: `/boot/flatcar/grub/i386-pc/procfs.mod` — MUST
- 191: `/boot/flatcar/grub/i386-pc/progress.mod` — MUST
- 192: `/boot/flatcar/grub/i386-pc/pxe.mod` — MUST
- 193: `/boot/flatcar/grub/i386-pc/pxechain.mod` — MUST
- 194: `/boot/flatcar/grub/i386-pc/raid5rec.mod` — MUST
- 195: `/boot/flatcar/grub/i386-pc/raid6rec.mod` — MUST
- 196: `/boot/flatcar/grub/i386-pc/random.mod` — MUST
- 197: `/boot/flatcar/grub/i386-pc/rdmsr.mod` — MUST
- 198: `/boot/flatcar/grub/i386-pc/reboot.mod` — MUST
- 199: `/boot/flatcar/grub/i386-pc/regexp.mod` — MUST
- 200: `/boot/flatcar/grub/i386-pc/reiserfs.mod` — MUST
- 201: `/boot/flatcar/grub/i386-pc/relocator.mod` — MUST
- 202: `/boot/flatcar/grub/i386-pc/romfs.mod` — MUST
- 203: `/boot/flatcar/grub/i386-pc/scsi.mod` — MUST
- 204: `/boot/flatcar/grub/i386-pc/search_fs_file.mod` — MUST
- 205: `/boot/flatcar/grub/i386-pc/search_label.mod` — MUST
- 206: `/boot/flatcar/grub/i386-pc/search_part_uuid.mod` — MUST
- 207: `/boot/flatcar/grub/i386-pc/sendkey.mod` — MUST
- 208: `/boot/flatcar/grub/i386-pc/setjmp.mod` — MUST
- 209: `/boot/flatcar/grub/i386-pc/setpci.mod` — MUST
- 210: `/boot/flatcar/grub/i386-pc/sfs.mod` — MUST
- 211: `/boot/flatcar/grub/i386-pc/sleep.mod` — MUST
- 212: `/boot/flatcar/grub/i386-pc/smbios.mod` — MUST
- 213: `/boot/flatcar/grub/i386-pc/spkmodem.mod` — MUST
- 214: `/boot/flatcar/grub/i386-pc/squash4.mod` — MUST
- 215: `/boot/flatcar/grub/i386-pc/syslinuxcfg.mod` — MUST
- 216: `/boot/flatcar/grub/i386-pc/terminal.lst` — NOT
- 217: `/boot/flatcar/grub/i386-pc/terminfo.mod` — MUST
- 218: `/boot/flatcar/grub/i386-pc/testload.mod` — MUST
- 219: `/boot/flatcar/grub/i386-pc/testspeed.mod` — MUST
- 220: `/boot/flatcar/grub/i386-pc/tftp.mod` — MUST
- 221: `/boot/flatcar/grub/i386-pc/tga.mod` — MUST
- 222: `/boot/flatcar/grub/i386-pc/time.mod` — MUST
- 223: `/boot/flatcar/grub/i386-pc/tr.mod` — MUST
- 224: `/boot/flatcar/grub/i386-pc/trig.mod` — MUST
- 225: `/boot/flatcar/grub/i386-pc/true.mod` — MUST
- 226: `/boot/flatcar/grub/i386-pc/truecrypt.mod` — MUST
- 227: `/boot/flatcar/grub/i386-pc/udf.mod` — MUST
- 228: `/boot/flatcar/grub/i386-pc/ufs1.mod` — MUST
- 229: `/boot/flatcar/grub/i386-pc/ufs1_be.mod` — MUST
- 230: `/boot/flatcar/grub/i386-pc/ufs2.mod` — MUST
- 231: `/boot/flatcar/grub/i386-pc/uhci.mod` — MUST
- 232: `/boot/flatcar/grub/i386-pc/usb.mod` — MUST
- 233: `/boot/flatcar/grub/i386-pc/usb_keyboard.mod` — MUST
- 234: `/boot/flatcar/grub/i386-pc/usbms.mod` — MUST
- 235: `/boot/flatcar/grub/i386-pc/usbserial_common.mod` — MUST
- 236: `/boot/flatcar/grub/i386-pc/usbserial_ftdi.mod` — MUST
- 237: `/boot/flatcar/grub/i386-pc/usbserial_pl2303.mod` — MUST
- 238: `/boot/flatcar/grub/i386-pc/usbserial_usbdebug.mod` — MUST
- 239: `/boot/flatcar/grub/i386-pc/usbtest.mod` — MUST
- 240: `/boot/flatcar/grub/i386-pc/vbe.mod` — MUST
- 241: `/boot/flatcar/grub/i386-pc/version.mod` — MUST
- 242: `/boot/flatcar/grub/i386-pc/vga.mod` — MUST
- 243: `/boot/flatcar/grub/i386-pc/vga_text.mod` — MUST
- 244: `/boot/flatcar/grub/i386-pc/video.lst` — NOT
- 245: `/boot/flatcar/grub/i386-pc/video.mod` — MUST
- 246: `/boot/flatcar/grub/i386-pc/video_bochs.mod` — MUST
- 247: `/boot/flatcar/grub/i386-pc/video_cirrus.mod` — MUST
- 248: `/boot/flatcar/grub/i386-pc/video_colors.mod` — MUST
- 249: `/boot/flatcar/grub/i386-pc/video_fb.mod` — MUST
- 250: `/boot/flatcar/grub/i386-pc/videoinfo.mod` — MUST
- 251: `/boot/flatcar/grub/i386-pc/videotest.mod` — MUST
- 252: `/boot/flatcar/grub/i386-pc/wrmsr.mod` — MUST
- 253: `/boot/flatcar/grub/i386-pc/xfs.mod` — MUST
- 254: `/boot/flatcar/grub/i386-pc/xnu.mod` — MUST
- 255: `/boot/flatcar/grub/i386-pc/xnu_uuid.mod` — MUST
- 256: `/boot/flatcar/grub/i386-pc/zfs.mod` — MUST
- 257: `/boot/flatcar/grub/i386-pc/zfscrypt.mod` — MUST
- 258: `/boot/flatcar/grub/i386-pc/zfsinfo.mod` — MUST
- 259: `/boot/flatcar/grub/i386-pc/zstd.mod` — MUST

### Correction flatcar-e202fef092ca215c5aa60869
MIXED → MIXED. Code requires recording; indexes are program-local values; saved boot bytes conflict with history exemption; construction-input consumers are unknown.
Corrected complete member map (supersedes earlier map):
- 1: `/boot/flatcar/grub/x86_64-xen/adler32.mod` — MUST
- 2: `/boot/flatcar/grub/x86_64-xen/affs.mod` — MUST
- 3: `/boot/flatcar/grub/x86_64-xen/afs.mod` — MUST
- 4: `/boot/flatcar/grub/x86_64-xen/afsplitter.mod` — MUST
- 5: `/boot/flatcar/grub/x86_64-xen/all_video.mod` — MUST
- 6: `/boot/flatcar/grub/x86_64-xen/appendedsig.mod` — MUST
- 7: `/boot/flatcar/grub/x86_64-xen/archelp.mod` — MUST
- 8: `/boot/flatcar/grub/x86_64-xen/asn1.mod` — MUST
- 9: `/boot/flatcar/grub/x86_64-xen/backtrace.mod` — MUST
- 10: `/boot/flatcar/grub/x86_64-xen/bfs.mod` — MUST
- 11: `/boot/flatcar/grub/x86_64-xen/bitmap.mod` — MUST
- 12: `/boot/flatcar/grub/x86_64-xen/bitmap_scale.mod` — MUST
- 13: `/boot/flatcar/grub/x86_64-xen/blocklist.mod` — MUST
- 14: `/boot/flatcar/grub/x86_64-xen/blscfg.mod` — MUST
- 15: `/boot/flatcar/grub/x86_64-xen/bufio.mod` — MUST
- 16: `/boot/flatcar/grub/x86_64-xen/cat.mod` — MUST
- 17: `/boot/flatcar/grub/x86_64-xen/cbfs.mod` — MUST
- 18: `/boot/flatcar/grub/x86_64-xen/cmp.mod` — MUST
- 19: `/boot/flatcar/grub/x86_64-xen/command.lst` — NOT
- 20: `/boot/flatcar/grub/x86_64-xen/cpio.mod` — MUST
- 21: `/boot/flatcar/grub/x86_64-xen/cpio_be.mod` — MUST
- 22: `/boot/flatcar/grub/x86_64-xen/cpuid.mod` — MUST
- 23: `/boot/flatcar/grub/x86_64-xen/crc64.mod` — MUST
- 24: `/boot/flatcar/grub/x86_64-xen/crypto.lst` — NOT
- 25: `/boot/flatcar/grub/x86_64-xen/crypto.mod` — MUST
- 26: `/boot/flatcar/grub/x86_64-xen/cryptodisk.mod` — MUST
- 27: `/boot/flatcar/grub/x86_64-xen/date.mod` — MUST
- 28: `/boot/flatcar/grub/x86_64-xen/datehook.mod` — MUST
- 29: `/boot/flatcar/grub/x86_64-xen/datetime.mod` — MUST
- 30: `/boot/flatcar/grub/x86_64-xen/disk.mod` — MUST
- 31: `/boot/flatcar/grub/x86_64-xen/diskfilter.mod` — MUST
- 32: `/boot/flatcar/grub/x86_64-xen/div.mod` — MUST
- 33: `/boot/flatcar/grub/x86_64-xen/dm_nv.mod` — MUST
- 34: `/boot/flatcar/grub/x86_64-xen/elf.mod` — MUST
- 35: `/boot/flatcar/grub/x86_64-xen/eval.mod` — MUST
- 36: `/boot/flatcar/grub/x86_64-xen/exfat.mod` — MUST
- 37: `/boot/flatcar/grub/x86_64-xen/ext2.mod` — MUST
- 38: `/boot/flatcar/grub/x86_64-xen/f2fs.mod` — MUST
- 39: `/boot/flatcar/grub/x86_64-xen/fdt.lst` — NOT
- 40: `/boot/flatcar/grub/x86_64-xen/file.mod` — MUST
- 41: `/boot/flatcar/grub/x86_64-xen/font.mod` — MUST
- 42: `/boot/flatcar/grub/x86_64-xen/fs.lst` — NOT
- 43: `/boot/flatcar/grub/x86_64-xen/fshelp.mod` — MUST
- 44: `/boot/flatcar/grub/x86_64-xen/gcry_arcfour.mod` — MUST
- 45: `/boot/flatcar/grub/x86_64-xen/gcry_blowfish.mod` — MUST
- 46: `/boot/flatcar/grub/x86_64-xen/gcry_camellia.mod` — MUST
- 47: `/boot/flatcar/grub/x86_64-xen/gcry_cast5.mod` — MUST
- 48: `/boot/flatcar/grub/x86_64-xen/gcry_crc.mod` — MUST
- 49: `/boot/flatcar/grub/x86_64-xen/gcry_des.mod` — MUST
- 50: `/boot/flatcar/grub/x86_64-xen/gcry_dsa.mod` — MUST
- 51: `/boot/flatcar/grub/x86_64-xen/gcry_idea.mod` — MUST
- 52: `/boot/flatcar/grub/x86_64-xen/gcry_md4.mod` — MUST
- 53: `/boot/flatcar/grub/x86_64-xen/gcry_md5.mod` — MUST
- 54: `/boot/flatcar/grub/x86_64-xen/gcry_rfc2268.mod` — MUST
- 55: `/boot/flatcar/grub/x86_64-xen/gcry_rijndael.mod` — MUST
- 56: `/boot/flatcar/grub/x86_64-xen/gcry_rmd160.mod` — MUST
- 57: `/boot/flatcar/grub/x86_64-xen/gcry_rsa.mod` — MUST
- 58: `/boot/flatcar/grub/x86_64-xen/gcry_seed.mod` — MUST
- 59: `/boot/flatcar/grub/x86_64-xen/gcry_serpent.mod` — MUST
- 60: `/boot/flatcar/grub/x86_64-xen/gcry_sha1.mod` — MUST
- 61: `/boot/flatcar/grub/x86_64-xen/gcry_sha256.mod` — MUST
- 62: `/boot/flatcar/grub/x86_64-xen/gcry_sha512.mod` — MUST
- 63: `/boot/flatcar/grub/x86_64-xen/gcry_tiger.mod` — MUST
- 64: `/boot/flatcar/grub/x86_64-xen/gcry_twofish.mod` — MUST
- 65: `/boot/flatcar/grub/x86_64-xen/gcry_whirlpool.mod` — MUST
- 66: `/boot/flatcar/grub/x86_64-xen/geli.mod` — MUST
- 67: `/boot/flatcar/grub/x86_64-xen/gettext.mod` — MUST
- 68: `/boot/flatcar/grub/x86_64-xen/gfxmenu.mod` — MUST
- 69: `/boot/flatcar/grub/x86_64-xen/gfxterm.mod` — MUST
- 70: `/boot/flatcar/grub/x86_64-xen/gfxterm_background.mod` — MUST
- 71: `/boot/flatcar/grub/x86_64-xen/gpt.mod` — MUST
- 72: `/boot/flatcar/grub/x86_64-xen/gptrepair.mod` — MUST
- 73: `/boot/flatcar/grub/x86_64-xen/gptsync.mod` — MUST
- 74: `/boot/flatcar/grub/x86_64-xen/gzio.mod` — MUST
- 75: `/boot/flatcar/grub/x86_64-xen/halt.mod` — MUST
- 76: `/boot/flatcar/grub/x86_64-xen/hashsum.mod` — MUST
- 77: `/boot/flatcar/grub/x86_64-xen/hello.mod` — MUST
- 78: `/boot/flatcar/grub/x86_64-xen/help.mod` — MUST
- 79: `/boot/flatcar/grub/x86_64-xen/hexdump.mod` — MUST
- 80: `/boot/flatcar/grub/x86_64-xen/hfs.mod` — MUST
- 81: `/boot/flatcar/grub/x86_64-xen/hfsplus.mod` — MUST
- 82: `/boot/flatcar/grub/x86_64-xen/hfspluscomp.mod` — MUST
- 83: `/boot/flatcar/grub/x86_64-xen/http.mod` — MUST
- 84: `/boot/flatcar/grub/x86_64-xen/increment.mod` — MUST
- 85: `/boot/flatcar/grub/x86_64-xen/iso9660.mod` — MUST
- 86: `/boot/flatcar/grub/x86_64-xen/jfs.mod` — MUST
- 87: `/boot/flatcar/grub/x86_64-xen/jpeg.mod` — MUST
- 88: `/boot/flatcar/grub/x86_64-xen/json.mod` — MUST
- 89: `/boot/flatcar/grub/x86_64-xen/keystatus.mod` — MUST
- 90: `/boot/flatcar/grub/x86_64-xen/ldm.mod` — MUST
- 91: `/boot/flatcar/grub/x86_64-xen/legacycfg.mod` — MUST
- 92: `/boot/flatcar/grub/x86_64-xen/linux.mod` — MUST
- 93: `/boot/flatcar/grub/x86_64-xen/load.cfg` — UNKNOWN
- 94: `/boot/flatcar/grub/x86_64-xen/loadenv.mod` — MUST
- 95: `/boot/flatcar/grub/x86_64-xen/loopback.mod` — MUST
- 96: `/boot/flatcar/grub/x86_64-xen/ls.mod` — MUST
- 97: `/boot/flatcar/grub/x86_64-xen/lsmmap.mod` — MUST
- 98: `/boot/flatcar/grub/x86_64-xen/lsxen.mod` — MUST
- 99: `/boot/flatcar/grub/x86_64-xen/luks.mod` — MUST
- 100: `/boot/flatcar/grub/x86_64-xen/luks2.mod` — MUST
- 101: `/boot/flatcar/grub/x86_64-xen/lvm.mod` — MUST
- 102: `/boot/flatcar/grub/x86_64-xen/lzopio.mod` — MUST
- 103: `/boot/flatcar/grub/x86_64-xen/macbless.mod` — MUST
- 104: `/boot/flatcar/grub/x86_64-xen/macho.mod` — MUST
- 105: `/boot/flatcar/grub/x86_64-xen/mdraid09.mod` — MUST
- 106: `/boot/flatcar/grub/x86_64-xen/mdraid09_be.mod` — MUST
- 107: `/boot/flatcar/grub/x86_64-xen/mdraid1x.mod` — MUST
- 108: `/boot/flatcar/grub/x86_64-xen/memrw.mod` — MUST
- 109: `/boot/flatcar/grub/x86_64-xen/minicmd.mod` — MUST
- 110: `/boot/flatcar/grub/x86_64-xen/minix.mod` — MUST
- 111: `/boot/flatcar/grub/x86_64-xen/minix2.mod` — MUST
- 112: `/boot/flatcar/grub/x86_64-xen/minix2_be.mod` — MUST
- 113: `/boot/flatcar/grub/x86_64-xen/minix3.mod` — MUST
- 114: `/boot/flatcar/grub/x86_64-xen/minix3_be.mod` — MUST
- 115: `/boot/flatcar/grub/x86_64-xen/minix_be.mod` — MUST
- 116: `/boot/flatcar/grub/x86_64-xen/moddep.lst` — NOT
- 117: `/boot/flatcar/grub/x86_64-xen/mpi.mod` — MUST
- 118: `/boot/flatcar/grub/x86_64-xen/msdospart.mod` — MUST
- 119: `/boot/flatcar/grub/x86_64-xen/net.mod` — MUST
- 120: `/boot/flatcar/grub/x86_64-xen/newc.mod` — MUST
- 121: `/boot/flatcar/grub/x86_64-xen/nilfs2.mod` — MUST
- 122: `/boot/flatcar/grub/x86_64-xen/ntfs.mod` — MUST
- 123: `/boot/flatcar/grub/x86_64-xen/ntfscomp.mod` — MUST
- 124: `/boot/flatcar/grub/x86_64-xen/odc.mod` — MUST
- 125: `/boot/flatcar/grub/x86_64-xen/offsetio.mod` — MUST
- 126: `/boot/flatcar/grub/x86_64-xen/part_acorn.mod` — MUST
- 127: `/boot/flatcar/grub/x86_64-xen/part_amiga.mod` — MUST
- 128: `/boot/flatcar/grub/x86_64-xen/part_apple.mod` — MUST
- 129: `/boot/flatcar/grub/x86_64-xen/part_bsd.mod` — MUST
- 130: `/boot/flatcar/grub/x86_64-xen/part_dfly.mod` — MUST
- 131: `/boot/flatcar/grub/x86_64-xen/part_dvh.mod` — MUST
- 132: `/boot/flatcar/grub/x86_64-xen/part_msdos.mod` — MUST
- 133: `/boot/flatcar/grub/x86_64-xen/part_plan.mod` — MUST
- 134: `/boot/flatcar/grub/x86_64-xen/part_sun.mod` — MUST
- 135: `/boot/flatcar/grub/x86_64-xen/part_sunpc.mod` — MUST
- 136: `/boot/flatcar/grub/x86_64-xen/partmap.lst` — NOT
- 137: `/boot/flatcar/grub/x86_64-xen/parttool.lst` — NOT
- 138: `/boot/flatcar/grub/x86_64-xen/parttool.mod` — MUST
- 139: `/boot/flatcar/grub/x86_64-xen/password.mod` — MUST
- 140: `/boot/flatcar/grub/x86_64-xen/password_pbkdf2.mod` — MUST
- 141: `/boot/flatcar/grub/x86_64-xen/pbkdf2.mod` — MUST
- 142: `/boot/flatcar/grub/x86_64-xen/pgp.mod` — MUST
- 143: `/boot/flatcar/grub/x86_64-xen/pkcs1_v15.mod` — MUST
- 144: `/boot/flatcar/grub/x86_64-xen/plainmount.mod` — MUST
- 145: `/boot/flatcar/grub/x86_64-xen/png.mod` — MUST
- 146: `/boot/flatcar/grub/x86_64-xen/priority_queue.mod` — MUST
- 147: `/boot/flatcar/grub/x86_64-xen/probe.mod` — MUST
- 148: `/boot/flatcar/grub/x86_64-xen/procfs.mod` — MUST
- 149: `/boot/flatcar/grub/x86_64-xen/progress.mod` — MUST
- 150: `/boot/flatcar/grub/x86_64-xen/raid5rec.mod` — MUST
- 151: `/boot/flatcar/grub/x86_64-xen/raid6rec.mod` — MUST
- 152: `/boot/flatcar/grub/x86_64-xen/reboot.mod` — MUST
- 153: `/boot/flatcar/grub/x86_64-xen/regexp.mod` — MUST
- 154: `/boot/flatcar/grub/x86_64-xen/reiserfs.mod` — MUST
- 155: `/boot/flatcar/grub/x86_64-xen/relocator.mod` — MUST
- 156: `/boot/flatcar/grub/x86_64-xen/romfs.mod` — MUST
- 157: `/boot/flatcar/grub/x86_64-xen/scsi.mod` — MUST
- 158: `/boot/flatcar/grub/x86_64-xen/search_fs_file.mod` — MUST
- 159: `/boot/flatcar/grub/x86_64-xen/search_label.mod` — MUST
- 160: `/boot/flatcar/grub/x86_64-xen/search_part_uuid.mod` — MUST
- 161: `/boot/flatcar/grub/x86_64-xen/setjmp.mod` — MUST
- 162: `/boot/flatcar/grub/x86_64-xen/sfs.mod` — MUST
- 163: `/boot/flatcar/grub/x86_64-xen/sleep.mod` — MUST
- 164: `/boot/flatcar/grub/x86_64-xen/squash4.mod` — MUST
- 165: `/boot/flatcar/grub/x86_64-xen/syslinuxcfg.mod` — MUST
- 166: `/boot/flatcar/grub/x86_64-xen/terminal.lst` — NOT
- 167: `/boot/flatcar/grub/x86_64-xen/testload.mod` — MUST
- 168: `/boot/flatcar/grub/x86_64-xen/testspeed.mod` — MUST
- 169: `/boot/flatcar/grub/x86_64-xen/tftp.mod` — MUST
- 170: `/boot/flatcar/grub/x86_64-xen/tga.mod` — MUST
- 171: `/boot/flatcar/grub/x86_64-xen/time.mod` — MUST
- 172: `/boot/flatcar/grub/x86_64-xen/tr.mod` — MUST
- 173: `/boot/flatcar/grub/x86_64-xen/trig.mod` — MUST
- 174: `/boot/flatcar/grub/x86_64-xen/true.mod` — MUST
- 175: `/boot/flatcar/grub/x86_64-xen/udf.mod` — MUST
- 176: `/boot/flatcar/grub/x86_64-xen/ufs1.mod` — MUST
- 177: `/boot/flatcar/grub/x86_64-xen/ufs1_be.mod` — MUST
- 178: `/boot/flatcar/grub/x86_64-xen/ufs2.mod` — MUST
- 179: `/boot/flatcar/grub/x86_64-xen/version.mod` — MUST
- 180: `/boot/flatcar/grub/x86_64-xen/video.lst` — NOT
- 181: `/boot/flatcar/grub/x86_64-xen/video.mod` — MUST
- 182: `/boot/flatcar/grub/x86_64-xen/video_colors.mod` — MUST
- 183: `/boot/flatcar/grub/x86_64-xen/video_fb.mod` — MUST
- 184: `/boot/flatcar/grub/x86_64-xen/videoinfo.mod` — MUST
- 185: `/boot/flatcar/grub/x86_64-xen/videotest.mod` — MUST
- 186: `/boot/flatcar/grub/x86_64-xen/xfs.mod` — MUST
- 187: `/boot/flatcar/grub/x86_64-xen/xnu_uuid.mod` — MUST
- 188: `/boot/flatcar/grub/x86_64-xen/zfs.mod` — MUST
- 189: `/boot/flatcar/grub/x86_64-xen/zfscrypt.mod` — MUST
- 190: `/boot/flatcar/grub/x86_64-xen/zfsinfo.mod` — MUST
- 191: `/boot/flatcar/grub/x86_64-xen/zstd.mod` — MUST
Corrected complete member map (supersedes earlier map):
- 1: `/etc/audit/audisp-filter.conf` — UNKNOWN
- 2: `/etc/audit/audisp-remote.conf` — UNKNOWN
- 3: `/etc/audit/audit-stop.rules` — MUST
- 4: `/etc/audit/audit.rules` — MUST
- 5: `/etc/audit/auditd.conf` — UNKNOWN
- 6: `/etc/audit/plugins.d` — UNKNOWN
- 7: `/etc/audit/rules.d` — MUST
Corrected complete member map (supersedes earlier map):
- 1: `/etc/selinux/config` — UNKNOWN
- 2: `/etc/selinux/mcs` — MUST
- 3: `/etc/selinux/mls` — MUST
- 4: `/etc/selinux/semanage.conf` — UNKNOWN
- 5: `/etc/selinux/targeted` — MUST
Corrected complete member map (supersedes earlier map):
- 1: `/etc/ssl/certs` — MUST
- 2: `/etc/ssl/fipsmodule.cnf` — UNKNOWN
- 3: `/etc/ssl/openssl.cnf` — UNKNOWN
- 4: `/etc/ssl/private` — NOT
Corrected complete member map (supersedes earlier map):
- 1: `/etc/systemd/coredump.conf` — UNKNOWN
- 2: `/etc/systemd/journal-remote.conf` — UNKNOWN
- 3: `/etc/systemd/journal-upload.conf` — UNKNOWN
- 4: `/etc/systemd/journald.conf` — UNKNOWN
- 5: `/etc/systemd/logind.conf` — UNKNOWN
- 6: `/etc/systemd/network` — NOT
- 7: `/etc/systemd/networkd.conf` — UNKNOWN
- 8: `/etc/systemd/oomd.conf` — UNKNOWN
- 9: `/etc/systemd/pstore.conf` — UNKNOWN
- 10: `/etc/systemd/resolved.conf` — UNKNOWN
- 11: `/etc/systemd/sleep.conf` — UNKNOWN
- 12: `/etc/systemd/system` — MUST
- 13: `/etc/systemd/system.conf` — UNKNOWN
- 14: `/etc/systemd/timesyncd.conf` — UNKNOWN
- 15: `/etc/systemd/user` — NOT
- 16: `/etc/systemd/user.conf` — UNKNOWN
Corrected complete member map (supersedes earlier map):
- 1: `/etc/.ignition-result.json` — NOT
- 2: `/etc/.pwd.lock` — UNKNOWN
- 3: `/etc/.systemd-confext` — MUST
- 4: `/etc/.updated` — UNKNOWN
- 5: `/etc/X11` — MUST
- 6: `/etc/audit` — MUST
- 7: `/etc/azure-ephemeral-disk-setup.conf` — UNKNOWN
- 8: `/etc/bash` — MUST
- 9: `/etc/bindresvport.blacklist` — UNKNOWN
- 10: `/etc/binfmt.d` — NOT
- 11: `/etc/cifs-utils` — UNKNOWN
- 12: `/etc/cni` — UNKNOWN
- 13: `/etc/conntrackd` — UNKNOWN
- 14: `/etc/coreos` — UNKNOWN
- 15: `/etc/credstore` — UNKNOWN
- 16: `/etc/credstore.encrypted` — UNKNOWN
- 17: `/etc/dbus-1` — MUST
- 18: `/etc/default` — MUST
- 19: `/etc/dracut.conf` — UNKNOWN
- 20: `/etc/e2scrub.conf` — UNKNOWN
- 21: `/etc/environment.d` — MUST
- 22: `/etc/ethertypes` — UNKNOWN
- 23: `/etc/extension-release.d` — MUST
- 24: `/etc/extensions` — MUST
- 25: `/etc/flatcar` — UNKNOWN
- 26: `/etc/group` — MUST
- 27: `/etc/group-` — NOT
- 28: `/etc/gshadow` — MUST
- 29: `/etc/gshadow-` — NOT
- 30: `/etc/hosts` — MUST
- 31: `/etc/idmapd.conf` — UNKNOWN
- 32: `/etc/init.d` — UNKNOWN
- 33: `/etc/iscsi` — UNKNOWN
- 34: `/etc/isns` — UNKNOWN
- 35: `/etc/issue` — NOT
- 36: `/etc/kernel` — NOT
- 37: `/etc/kexec.conf` — UNKNOWN
- 38: `/etc/keyutils` — UNKNOWN
- 39: `/etc/krb5.conf.example` — NOT
- 40: `/etc/ld.so.cache` — UNKNOWN
- 41: `/etc/ldap.conf.sudo` — UNKNOWN
- 42: `/etc/lessfilter.d` — UNKNOWN
- 43: `/etc/libaudit.conf` — UNKNOWN
- 44: `/etc/locale.conf` — MUST
- 45: `/etc/login.defs` — MUST
- 46: `/etc/logrotate.conf` — UNKNOWN
- 47: `/etc/logrotate.d` — UNKNOWN
- 48: `/etc/lvm` — UNKNOWN
- 49: `/etc/machine-id` — MUST
- 50: `/etc/mke2fs.conf` — UNKNOWN
- 51: `/etc/modules-load.d` — NOT
- 52: `/etc/motd` — NOT
- 53: `/etc/mtab` — UNKNOWN
- 54: `/etc/netconfig` — UNKNOWN
- 55: `/etc/nscd.conf` — UNKNOWN
- 56: `/etc/ntp.conf` — UNKNOWN
- 57: `/etc/nvme` — UNKNOWN
- 58: `/etc/openldap` — UNKNOWN
- 59: `/etc/pam.d` — NOT
- 60: `/etc/passwd` — MUST
- 61: `/etc/passwd-` — NOT
- 62: `/etc/pkcs11` — NOT
- 63: `/etc/polkit-1` — NOT
- 64: `/etc/profile.d` — MUST
- 65: `/etc/quotagrpadmins` — UNKNOWN
- 66: `/etc/quotatab` — UNKNOWN
- 67: `/etc/request-key.conf` — MUST
- 68: `/etc/request-key.d` — MUST
- 69: `/etc/resolv.conf` — MUST
- 70: `/etc/runlevels` — UNKNOWN
- 71: `/etc/sasl2` — UNKNOWN
- 72: `/etc/securetty` — MUST
- 73: `/etc/security` — NOT
- 74: `/etc/selinux` — MUST
- 75: `/etc/sestatus.conf` — UNKNOWN
- 76: `/etc/shadow` — UNKNOWN
- 77: `/etc/shadow-` — NOT
- 78: `/etc/skel` — UNKNOWN
- 79: `/etc/ssh` — MUST
- 80: `/etc/ssl` — MUST
- 81: `/etc/sssd` — MUST
- 82: `/etc/subgid` — MUST
- 83: `/etc/subgid-` — NOT
- 84: `/etc/subuid` — MUST
- 85: `/etc/subuid-` — NOT
- 86: `/etc/sudo_logsrvd.conf` — UNKNOWN
- 87: `/etc/sudoers.d` — NOT
- 88: `/etc/sudoers.dist` — UNKNOWN
- 89: `/etc/sysconfig` — UNKNOWN
- 90: `/etc/systemd` — MUST
- 91: `/etc/tcsd.conf` — UNKNOWN
- 92: `/etc/tmpfiles.d` — NOT
- 93: `/etc/tpm2-tss` — UNKNOWN
- 94: `/etc/udev` — MUST
- 95: `/etc/user` — UNKNOWN
- 96: `/etc/vim` — UNKNOWN
- 97: `/etc/warnquota.conf` — UNKNOWN
- 98: `/etc/whois.conf` — UNKNOWN
- 99: `/etc/wireguard` — UNKNOWN
- 100: `/etc/xattr.conf` — UNKNOWN
- 101: `/etc/xdg` — NOT

## Final review correction: GRUB indexes
The 18 `.lst` members in the BIOS and Xen groups are NOT under S2.2-7 and S2.2-13: they supply values only to GRUB. General capability dependence does not override the explicit program-local setting exemption. Earlier HOLE mappings for these indexes are superseded by the last corrected complete member maps. Native modules remain MUST, construction inputs UNKNOWN, and saved MBR bytes HOLE. Ancestor directory decisions remain unchanged because each affected directory still contains required native code.


---

# Review response and final verification

The separate review is recorded in `part-flatcar.review.md`. Its two material issue families were addressed: the 18 GRUB value-list rows are NOT under S2.2-7/13, with matching grouped-member corrections; the 29 driver-link rows are UNKNOWN under S3-2 because actual downstream dependencies remain unestablished. This avoids asserting either driver removal or absence of operational effects from a metadata link alone. Each change is preserved in `part-flatcar.integration-corrections.jsonl`.

Final verification passed: 1,827 rows, exact input/output ID multiset, each ID once, all five-word decisions valid, sentence references limited to S2.2 and S3-1/2, field word limits respected, and raw references resolved. All MIXED member mappings were checked for complete, non-overlapping coverage.

Counts: MUST 1549; NOT 106; HOLE 11; UNKNOWN 116; MIXED 45.
