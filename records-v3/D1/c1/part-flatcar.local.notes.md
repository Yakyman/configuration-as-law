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
