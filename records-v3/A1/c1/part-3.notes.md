# Part 3 classification notes

# Part 3: accounts, modules, and processes

The classification uses only Section 2.2 and the recording indicator of Section 3. Inventory class labels are not used as decisions. The raw account database, loaded-module table, and process listing establish the relevant functions. No objects were removed. No other classification was consulted.

## Homogeneous rule A: operating-system accounts

Apply MUST with S2.2-15 to each account row verified in `../in/raw/nixos/accounts.txt`. The script does not infer a requirement from account names, privileges, or login shell. An account with a nologin shell remains an account. The grouped build identities are separately checked against `../in/raw/nixos/nix-builder-accounts.txt`: all 32 members are accounts and receive MUST.

Ten manually checked rows, with the raw UID confirming each identity:

- nixos-96a19ba1e6: UID 1000.
- nixos-27d89cb149: UID 999.
- nixos-9911292f99: UID 4.
- nixos-af2a58bec6: UID 65534.
- nixos-26ad58fd4b: UID 998.
- nixos-cbaf0b4232: UID 0.
- nixos-dbea3590f8: UID 997.
- nixos-e7927b082e: UID 151.
- nixos-ee17e5a4df: UID 152.
- nixos-195a1b489c: UID 996.

## Homogeneous rule K: loaded kernel modules

Apply MUST with S2.2-10 to every module listed as loaded in `../in/raw/nixos/modules.txt`, with its module pathname supplied by the input evidence. These are executable code loaded into the kernel, with the kernel's rights. They are not settings read as values or code confined to an application interface. The decision does not depend on whether a module has a current consumer or on its particular algorithm. In particular, `mbcache` is executable module code, not the cache contents exempted by S2.2-5.

Primary documentation: [init_module(2)](https://man7.org/linux/man-pages/man2/init_module.2.html): “init_module() loads an ELF image into kernel space”. The same description states that the kernel relocates the image and executes its initialization function. This establishes the execution mechanism for all rows in this rule.

Ten manually checked module rows, matching names, loaded entries, and `.ko.xz` evidence paths:

- nixos-7fdc5c58fa: 8021q, loaded, kernel/net/8021q.
- nixos-ddb5a87d9a: aesni_intel, loaded, kernel/arch/x86/crypto.
- nixos-770d8f08e0: af_packet, loaded, kernel/net/packet.
- nixos-0074a80686: ata_generic, loaded, kernel/drivers/ata.
- nixos-4ef0af6396: ata_piix, loaded, kernel/drivers/ata.
- nixos-b30af9d5d4: atkbd, loaded, kernel/drivers/input/keyboard.
- nixos-4fb00be8be: autofs4, loaded, kernel/fs/autofs.
- nixos-13fab1e09e: bochs, loaded, kernel/drivers/gpu/drm/tiny.
- nixos-70a3c6eeb0: button, loaded, kernel/drivers/acpi.
- nixos-519f0efa4c: ccp, loaded, kernel/drivers/crypto/ccp.

## Homogeneous rule P: observed native program processes

Apply MUST with S2.2-9 and S2.2-12 to the 18 process rows other than the kernel-thread group. The recorded PID and command in `../in/raw/nixos/processes.txt` establish that the program runs. `process-executables.tsv` additionally resolves executable paths except for the short-lived ps command, which the process listing itself observes. Multiple PIDs of the same executable receive the same requirement. The classification concerns the observed running programs, not a requirement to record individual PIDs or transient runtime state.

Ten manually checked rows:

- nixos-ab5afd3d29: PID 707, sshd listener command.
- nixos-68eab14191: PIDs 858 and 861, sshd-session processes.
- nixos-4bb4fc6dbf: PID 607, nsncd executable.
- nixos-8d6e82c019: PID 591, dbus-broker command.
- nixos-18a2277378: PID 544, dbus-broker-launch command.
- nixos-d59e2c228f: PID 669, dhcpcd manager command.
- nixos-bc78e20612: PID 864, bash command.
- nixos-c21d9ccbf0: PID 862, sudo command.
- nixos-344126e1ba: PID 303, udev daemon command, executable resolves to udevadm.
- nixos-02bf374b35: PIDs 1 and 783, system and user service managers.

## Individual group decision: kernel threads

nixos-89ce5c5668 is MUST. The raw process table lists kernel threads, including kthreadd, workers, softirq handlers, migration, memory reclaim, filesystem journaling, and device tasks. Each executes kernel code. The decision applies to the executing kernel code, not recording every transient thread identifier.

Primary documentation: [Workqueue](https://docs.kernel.org/core-api/workqueue.html): “special purpose threads, called [k]workers, execute the functions off of the queue”. This supports the worker members; the raw table identifies the remaining kernel tasks. The code is not confined to an application's interface. S2.2-1 and S2.2-10 require it.

## Exact deciding sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.

- **S3-2** If what the object does remains unknown, the case yields ?.


# Part 3 store-object classification notes

Scope: 618 system-closure-store-object rows. Only the specified input, its raw files, the fixed text and public primary documentation were consulted. No object was removed. Store-closure membership and inventory category wording are not recording rules.

## Governing sentences

S2.2-1: Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

S2.2-2: The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

S2.2-4: content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;

S2.2-7: settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.

S2.2-9: a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

S2.2-10: code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

S2.2-13: A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;

S2.2-15: accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

S2.2-16: the boot order and device firmware must be recorded where the system is able to change them.

S3-2: If what the object does remains unknown, the case yields ?.

## Homogeneous rules and hand checks

The following ten rows per rule were inspected against their inventory identities and the cited role documentation before the rule was accepted. The table records the checked fit; it is not a random mechanical existence check.

### documentation

Only distinct outputs ending -man, -doc, or -info. S2.2-4 exempts their readable documentation content; this does not exempt the corresponding program.

| Checked ID | Inspected identity | Why the rule fits |
|---|---|---|
| nixos-0d8e6571b3 | which-2.23-man | Supplies documentation for reading. |
| nixos-5bf964ab26 | sudo-1.9.17p2-man | Supplies documentation for reading. |
| nixos-4f49e33ff9 | iptables-1.8.13-man | Supplies documentation for reading. |
| nixos-7dd7c9efac | nano-9.3-doc | Supplies documentation for reading. |
| nixos-321145bd6c | lvm2-2.03.39-man | Supplies documentation for reading. |
| nixos-6cdc5ec8ec | linux-pam-1.7.2-man | Supplies documentation for reading. |
| nixos-abd9fea7bd | coreutils-full-9.11-info | Supplies documentation for reading. |
| nixos-d4f60c813a | bash-interactive-5.3p9-man | Supplies documentation for reading. |
| nixos-7f9811b4a3 | bash-interactive-5.3p9-info | Supplies documentation for reading. |
| nixos-6eb8c633bc | gzip-1.14-man | Supplies documentation for reading. |

### service-unit

Only generated unit definitions, excluding unit-script objects. Documentation establishes control of processes, sockets, devices, mounts, targets, timers and resources. Their effects extend to externally running processes and system resources; S2.2-1 and S2.2-2 apply rather than the single-program setting exemption.

| Checked ID | Inspected identity | Why the rule fits |
|---|---|---|
| nixos-84a041f075 | unit-sshd.service | Defines service, activation, scheduling, mount, or resource-management behavior. |
| nixos-67ab60209c | unit--.slice | Defines service, activation, scheduling, mount, or resource-management behavior. |
| nixos-5d5dfe50ce | unit-nix-optimise.service | Defines service, activation, scheduling, mount, or resource-management behavior. |
| nixos-804b8a2412 | unit-dbus-broker.service | Defines service, activation, scheduling, mount, or resource-management behavior. |
| nixos-84ec399df1 | unit-systemd-journald-audit.socket | Defines service, activation, scheduling, mount, or resource-management behavior. |
| nixos-7908efe09e | unit-systemd-backlight-.service | Defines service, activation, scheduling, mount, or resource-management behavior. |
| nixos-fa7ae4e8c6 | unit-systemd-timedated.service | Defines service, activation, scheduling, mount, or resource-management behavior. |
| nixos-802525fc67 | unit-container-getty-.service | Defines service, activation, scheduling, mount, or resource-management behavior. |
| nixos-5c12609b17 | unit-systemd-udevd.service | Defines service, activation, scheduling, mount, or resource-management behavior. |
| nixos-90d3fb15bc | unit-systemd-random-seed.service | Defines service, activation, scheduling, mount, or resource-management behavior. |

### documented-code-package

An explicit source metadata or project-documentation match establishes executable/library functionality. Data-only packages are excluded. S2.2-9 covers commands and S2.2-10 covers libraries; removing the object removes that functionality. Bare store membership alone is not used.

| Checked ID | Inspected identity | Why the rule fits |
|---|---|---|
| nixos-97cb111da6 | util-linux-minimal-2.42.4-mount | Provides executable or library code for util-linux-minimal. |
| nixos-ee2071e7d0 | jq-1.8.2 | Provides executable or library code for jq. |
| nixos-47026fe15e | libnftnl-1.3.1 | Provides executable or library code for libnftnl. |
| nixos-62e70fa96f | gnutls-3.8.13 | Provides executable or library code for gnutls. |
| nixos-99cc8e5ca6 | time-1.10 | Provides executable or library code for time. |
| nixos-4d03e8f157 | btrfs-progs-6.19.1 | Provides executable or library code for btrfs-progs. |
| nixos-5c799eca7b | hostname-debian-3.25 | Provides executable or library code for hostname-debian. |
| nixos-e295f3d815 | nsncd-1.5.3 | Provides executable or library code for nsncd. |
| nixos-8bc1905df8 | tpm2-tss-4.2.1 | Provides executable or library code for tpm2-tss. |
| nixos-11713daf6a | lzo-2.10 | Provides executable or library code for lzo. |

### library-output

Only distinct outputs ending -lib or -libgcc. These hold library code, executed by dependent programs without a separate confinement boundary. S2.2-10 and S2.2-2 require it.

| Checked ID | Inspected identity | Why the rule fits |
|---|---|---|
| nixos-0d64f91110 | libpwquality-1.4.5-lib | Provides library code executed by dependent programs. |
| nixos-5a2531bde3 | gcc-15.3.0-libgcc | Provides library code executed by dependent programs. |
| nixos-54d61dcad8 | gdbm-1.26-lib | Provides library code executed by dependent programs. |
| nixos-963ce26d5e | xgcc-15.3.0-libgcc | Provides library code executed by dependent programs. |
| nixos-e57a025c09 | keyutils-1.6.3-lib | Provides library code executed by dependent programs. |
| nixos-22749f918d | lvm2-2.03.39-lib | Provides library code executed by dependent programs. |
| nixos-f23d011fb5 | iptables-1.8.13-lib | Provides library code executed by dependent programs. |
| nixos-9418d6d5a3 | libarchive-3.8.9-lib | Provides library code executed by dependent programs. |
| nixos-dfc66d3944 | oniguruma-6.9.10-lib | Provides library code executed by dependent programs. |
| nixos-cb7aedf0be | protobuf-c-1.5.2-lib | Provides library code executed by dependent programs. |

### binary-output

Only distinct outputs ending -bin. The documented output convention places user-facing executables here. S2.2-9 requires those programs; S2.2-2 supplies the command-removal reasoning.

| Checked ID | Inspected identity | Why the rule fits |
|---|---|---|
| nixos-cd8ff5ee21 | e2fsprogs-1.47.4-bin | Provides executable commands. |
| nixos-100eaba827 | acl-2.4.0-bin | Provides executable commands. |
| nixos-28e58212d6 | bzip2-1.0.8-bin | Provides executable commands. |
| nixos-3b5785dadd | glibc-2.42-103-bin | Provides executable commands. |
| nixos-84bb7a78bc | xz-5.8.4-bin | Provides executable commands. |
| nixos-351c7742a8 | jq-1.8.2-bin | Provides executable commands. |
| nixos-3f7bbab591 | fuse-2.9.9-bin | Provides executable commands. |
| nixos-0abffcaf9c | attr-2.6.0-bin | Provides executable commands. |
| nixos-83c0c46eff | util-linux-minimal-2.42.4-bin | Provides executable commands. |
| nixos-acf6a7c2ef | fontconfig-2.17.1-bin | Provides executable commands. |

### restart-trigger

Only X-Restart-Triggers objects generated by systemd-lib. Their documented source supplies change-sensitive restart inputs. These determine restarting external services, so S2.2-1 and S2.2-2 require them.

| Checked ID | Inspected identity | Why the rule fits |
|---|---|---|
| nixos-a738960c81 | X-Restart-Triggers-reload-systemd-vconsole-setup | Determines whether configuration changes restart a service. |
| nixos-12077741ee | X-Restart-Triggers-resolvconf | Determines whether configuration changes restart a service. |
| nixos-ed89bf30d9 | X-Restart-Triggers-systemd-tmpfiles-resetup | Determines whether configuration changes restart a service. |
| nixos-37c734ac44 | X-Restart-Triggers-dhcpcd | Determines whether configuration changes restart a service. |
| nixos-99dc8e74de | X-Restart-Triggers-nix-daemon | Determines whether configuration changes restart a service. |
| nixos-203b47af8c | X-Restart-Triggers-dbus-broker | Determines whether configuration changes restart a service. |
| nixos-d5d37251d4 | X-Restart-Triggers-systemd-journald | Determines whether configuration changes restart a service. |
| nixos-aca93a4a49 | X-Restart-Triggers-systemd-sysctl | Determines whether configuration changes restart a service. |
| nixos-29ffe395d2 | X-Restart-Triggers-systemd-udevd | Determines whether configuration changes restart a service. |
| nixos-cf6b4465c0 | X-Restart-Triggers-sshd | Determines whether configuration changes restart a service. |

### security-wrapper

Only security-wrapper executable outputs. The wrapper source copies a compiled program into the privilege-wrapper directory and assigns configured rights. S2.2-9 and S2.2-15 require these executable privilege transitions.

| Checked ID | Inspected identity | Why the rule fits |
|---|---|---|
| nixos-46e14aa296 | security-wrapper-umount-x86_64-unknown-linux-musl | Executes a wrapped command with configured privilege transitions. |
| nixos-3f893f9f19 | security-wrapper-newgidmap-x86_64-unknown-linux-musl | Executes a wrapped command with configured privilege transitions. |
| nixos-6adfe77407 | security-wrapper-sg-x86_64-unknown-linux-musl | Executes a wrapped command with configured privilege transitions. |
| nixos-a3d9e0fb4c | security-wrapper-newuidmap-x86_64-unknown-linux-musl | Executes a wrapped command with configured privilege transitions. |
| nixos-fe7b152818 | security-wrapper-fusermount-x86_64-unknown-linux-musl | Executes a wrapped command with configured privilege transitions. |
| nixos-14a3d88be8 | security-wrapper-fusermount3-x86_64-unknown-linux-musl | Executes a wrapped command with configured privilege transitions. |
| nixos-3a64aeff99 | security-wrapper-newgrp-x86_64-unknown-linux-musl | Executes a wrapped command with configured privilege transitions. |
| nixos-4a7c5519f7 | security-wrapper-chsh-x86_64-unknown-linux-musl | Executes a wrapped command with configured privilege transitions. |
| nixos-6e9470a3a6 | security-wrapper-sudo-x86_64-unknown-linux-musl | Executes a wrapped command with configured privilege transitions. |
| nixos-7f7cfc2b40 | security-wrapper-mount-x86_64-unknown-linux-musl | Executes a wrapped command with configured privilege transitions. |

### pam-policy

Only named PAM service policy objects. PAM reads these when privilege-granting applications authenticate or establish sessions. These account/access rules fall directly under S2.2-15, irrespective of storage location.

| Checked ID | Inspected identity | Why the rule fits |
|---|---|---|
| nixos-b5a6c72599 | usermod.pam | Controls authentication, account access, and session establishment. |
| nixos-068402b5f0 | groupadd.pam | Controls authentication, account access, and session establishment. |
| nixos-538a27c54d | runuser-l.pam | Controls authentication, account access, and session establishment. |
| nixos-1866031379 | login.pam | Controls authentication, account access, and session establishment. |
| nixos-70030c0912 | groupmems.pam | Controls authentication, account access, and session establishment. |
| nixos-e224f7015d | sudo.pam | Controls authentication, account access, and session establishment. |
| nixos-74d41420f4 | chfn.pam | Controls authentication, account access, and session establishment. |
| nixos-7478014d7a | other.pam | Controls authentication, account access, and session establishment. |
| nixos-9b832188b2 | chsh.pam | Controls authentication, account access, and session establishment. |
| nixos-b862214766 | sshd.pam | Controls authentication, account access, and session establishment. |

### unit-script

Only generated unit-script outputs. systemd-lib creates executable shell scripts for service lifecycle hooks. S2.2-10 requires this code running under the service shell’s rights.

| Checked ID | Inspected identity | Why the rule fits |
|---|---|---|
| nixos-76aab70b52 | unit-script-nixos-activation-start | Executes service lifecycle actions as shell code. |
| nixos-884611d475 | unit-script-sleep-actions-start | Executes service lifecycle actions as shell code. |
| nixos-566881f135 | unit-script-post-boot-start | Executes service lifecycle actions as shell code. |
| nixos-76b7740691 | unit-script-linger-users-start | Executes service lifecycle actions as shell code. |
| nixos-2f63f83cb7 | unit-script-suid-sgid-wrappers-start | Executes service lifecycle actions as shell code. |
| nixos-66c9f81b32 | unit-script-network-local-commands-start | Executes service lifecycle actions as shell code. |
| nixos-c9275ff52c | unit-script-resolvconf-start | Executes service lifecycle actions as shell code. |
| nixos-bc9429aec4 | unit-script-sleep-actions-pre-stop | Executes service lifecycle actions as shell code. |
| nixos-231a055875 | unit-script-nix-gc-start | Executes service lifecycle actions as shell code. |
| nixos-0e91f5020a | unit-script-sshd-keygen-start | Executes service lifecycle actions as shell code. |

## Individual decisions and uncertainty

All rows outside those rules were inspected individually. Known source definitions and activation references are used only when they identify the actual generated role. Where the inventory supplies only a store pathname, a general manual describes possible behavior but cannot reveal whether this artifact contains operative values, code, an empty configuration, or another generated form. Such cases remain UNKNOWN rather than receiving a decision guessed from the filename.

The four HOLE cases are runtime databases. One reading exempts their contents as databases under S2.2-4; another treats the computations and decisions they enable as behavior under S2.2-1 and S2.2-2. The text does not specify how to distinguish unavailability of those contents from loss of the behavior calculated using them. This is a recording-boundary question, not a question about transferring accumulated program state.

| ID | Decision | Specific evidence limitation or determination |
|---|---|---|
| nixos-a332c16c0a | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-44be4b8c59 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-bd414d6b6a | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-7660afd089 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-e78f81d36e | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-903eca0ec8 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-e3ea449be8 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-70bca474fd | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-675aa31b3c | MUST | Removing trust anchors prevents certificate authentication; they are neither account passwords nor merely displayed content. |
| nixos-90649e5e3f | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-d3ac6fc3e9 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-04fa78880b | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-83c75ec418 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-532c5e327b | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-4d1b734b98 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-de918b3443 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-12f051d142 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-423c077ce2 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-1522395a0a | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-9e62fba385 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-aae336be17 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-8734c912f5 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-e9323e3380 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-1be18f5c7f | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-055cb95e1b | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-35f4a744de | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-6cbae59fe8 | NOT | These settings apply only inside the editor. |
| nixos-7bd272c10e | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-531f170216 | HOLE | Runtime database values determine behavior, yet database contents are exempt; text does not define the boundary between functional data and content. |
| nixos-7a3f657b52 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-ccf3cec10c | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-7200207b9e | NOT | Removing this manual removes readable content without removing the documented programs. |
| nixos-ff0dd3211c | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-14f4c5ce4d | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-1048e8b309 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-62040b99d6 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-a11c785693 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-98f239d59a | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-d5f22d1be4 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-3f6895f897 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-4671ebd9e3 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-1a22421eb6 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-9acf2b1c3d | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-72469a9c87 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-baa8d74997 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-656ead75a2 | MUST | Dependent programs execute these arithmetic routines with their own rights. |
| nixos-62d60967b5 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-210907cb54 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-e4d952cbb3 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-18c1434e8d | MUST | Removing the bootloader removes the configured path for starting the operating system. |
| nixos-5b690b3aad | MUST | Switch inhibitors are consumed before activation and control whether the system can switch. |
| nixos-5bcb04cfbe | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-c2b79babba | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-da434bd078 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-4970bcb341 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-127a576660 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-cdf87f0ae8 | MUST | Activation installs this tree as system configuration; removing it prevents the configured system setup. |
| nixos-1f1dff2e93 | MUST | Activation explicitly selects these firmware files for device loading. |
| nixos-9621a0acf4 | MUST | The generated environment influences executable generators and their system unit output. |
| nixos-99f150a190 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-491ab1a91a | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-e581313b72 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-2009ac3ba5 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-b157b75a6a | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-bda7e60399 | NOT | Removing this manual removes readable content without removing the documented programs. |
| nixos-fef9f6bfda | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-49da4872c3 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-9da30b3745 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-7584680ee6 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-ab9bd639f0 | MUST | Dependent programs execute these arithmetic routines with their own rights. |
| nixos-7ca87583cd | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-21f1027cff | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-83e205b21f | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-191bc7ac6b | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-610d1475a9 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-d04cb0cca1 | NOT | Removing this manual removes readable content without removing the documented programs. |
| nixos-b52f86e9a7 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-ac13fdc155 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-a02f6abea1 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-1f30ba48f1 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-506b53909b | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-3a466539a8 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-9c6b9f1065 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-24e0252547 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-41c14bc4fd | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-6cad6264ed | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-bb87ebc68c | HOLE | Runtime database values determine behavior, yet database contents are exempt; text does not define the boundary between functional data and content. |
| nixos-e436f23378 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-16e3948c30 | MUST | Bootloader generation consumes these settings; they determine boot entries and installation behavior. |
| nixos-bfbcc6b6ea | HOLE | Runtime database values determine behavior, yet database contents are exempt; text does not define the boundary between functional data and content. |
| nixos-ca3dfbaa85 | MUST | Removing trust anchors prevents certificate authentication; they are neither account passwords nor merely displayed content. |
| nixos-07617dcb2e | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-87d05f8af5 | MUST | This system directory is selected by the active system profile and supplies activation behavior. |
| nixos-c26a05fe8a | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-ed0e17634b | NOT | Removing theme sounds removes their content, not the ability to play sound. |
| nixos-802135b776 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-bb50160728 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-0b51cdd610 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-9dd4ab5eba | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-ea9ab21cec | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-2dde8220ff | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-424668c6bd | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-cac26cf14a | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-58a9b537e0 | MUST | The policy grants or denies superuser privileges, explicitly requiring recording. |
| nixos-5ce23ca370 | MUST | Activation consumes this account description; accounts and account rights must be recorded. |
| nixos-8eee3b9cfb | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-08ed819db8 | NOT | Removing the message removes only displayed content; login functionality remains. |
| nixos-5d2dacac8b | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-8d44cbf2f9 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-41576835a4 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-f317491007 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-11897673e1 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-6a2a4480be | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-99c79c8a9b | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-ddd3228d87 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-6676689071 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-195e0d56cd | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-d6de619cbb | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-fdf182202d | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-2e25b73de0 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-ad04588be7 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-e85650147f | MUST | Applications execute these HTTP server routines with their own rights. |
| nixos-d95b8332ad | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-d389910157 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-f49423c31c | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-bad4ffa911 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-5215be070f | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-28de4add81 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-ba6bd26979 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-7d271b79b7 | HOLE | Runtime database values determine behavior, yet database contents are exempt; text does not define the boundary between functional data and content. |
| nixos-d42821389f | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-07aece8fce | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-454fcd56c4 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-6fd6f32bb8 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-ee908f90c5 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-9cc8609d9d | NOT | Removing an image removes only that displayed content. |
| nixos-310b3fdb04 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-f08c36d455 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-590839ea05 | MUST | Executable code supplies this operation and runs with the executing program’s rights. |
| nixos-b5e79c0be1 | MUST | Documentation specifies a sourced shell script; executable settings count as code. |
| nixos-b2175cf642 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-43cb8d5075 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-795f11ad62 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-6103a770a6 | NOT | Theme assets supply presentation content; removal makes only those assets unavailable. |
| nixos-dfca77b396 | MUST | Login keys are explicitly required to be recorded. |
| nixos-bd2cb91707 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |
| nixos-b3bf4f119b | MUST | The switch-check program opens this comparison input; removing it prevents the specified comparison, rather than merely hiding content. |
| nixos-b9f001fe55 | UNKNOWN | Inventory records only a store pathname. General documentation does not establish this generated object’s contents, active values, or actual execution role. |

## Primary documentation passages

URLs identify program role or format. Public definitions establish roles, not exact reproduction of the installed binary. Package metadata excerpts below were fetched from the primary packaging repository. The raw inventory supplies the installed object identity.

- https://docs.kernel.org/admin-guide/README.html
  > Linux kernel release 6.x

- https://gmplib.org/manual/Introduction-to-GMP
  > GNU MP is a portable library written in C for arbitrary precision arithmetic

- https://man.archlinux.org/man/resolvconf.conf.5.en
  > The resolvconf.conf file is a shell script that is sourced by resolvconf(8)

- https://man7.org/linux/man-pages/man5/pam.conf.5.html
  > When a PAM aware privilege granting application is started, it activates its attachment to the PAM-API.

- https://man7.org/linux/man-pages/man5/sudoers.5.html
  > The sudoers policy plugin determines a user's sudo privileges.

- https://nixos.org/manual/nixpkgs/stable/#multiple-output-file-type-groups
  > is meant for user-facing binaries, typically residing in `bin/`.

- https://raw.githubusercontent.com/GNOME/libxml2/master/README.md
  > libxml2 is an XML toolkit implemented in C

- https://raw.githubusercontent.com/NixOS/nix/master/README.md
  > Nix is a powerful package manager for Linux and other Unix systems

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/lib/systemd-lib.nix
  > name = "unit-script-${scriptName}";

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/security/wrappers/default.nix
  > cp ${securityWrapper source}/bin/security-wrapper "$wrapperDir/${program}"

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/au/audit/package.nix
  > Audit Library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-c-auth/package.nix
  > C99 library implementation of AWS client-side authentication

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-c-cal/package.nix
  > AWS Crypto Abstraction Layer

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-c-common/package.nix
  > AWS SDK for C common core

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-c-compression/package.nix
  > C99 implementation of huffman encoding/decoding

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-c-event-stream/package.nix
  > C99 implementation of the vnd.amazon.eventstream content-type

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-c-http/package.nix
  > C99 implementation of the HTTP/1.1 and HTTP/2 specifications

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-c-io/package.nix
  > AWS SDK for C module for IO and TLS

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-c-mqtt/package.nix
  > C99 implementation of the MQTT 3.1.1 specification

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-c-s3/package.nix
  > C99 library implementation for communicating with the S3 service

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-c-sdkutils/package.nix
  > AWS SDK utility library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-checksums/package.nix
  > HW accelerated CRC32c and CRC32

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/aw/aws-crt-cpp/package.nix
  > C++ wrapper around the aws-c-* libraries

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ba/bash-completion/package.nix
  > Programmable completion for the bash shell

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/bc/bcache-tools/package.nix
  > User-space tools required for bcache (Linux block layer cache)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/bi/bind/package.nix
  > Domain name server

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/bo/boehmgc/package.nix
  > conservative garbage collector for C and C++

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/br/brotli/package.nix
  > General-purpose lossless compression library with CLI

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/bt/btrfs-progs/package.nix
  > Utilities for the btrfs filesystem

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/bu/busybox/package.nix
  > Tiny versions of common UNIX utilities in a single small executable

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/bz/bzip2/package.nix
  > High-quality data compression program

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ca/cacert/package.nix
  > Bundle of X.509 certificates of public Certificate Authorities (CA)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/co/coreutils/package.nix
  > GNU Core Utilities

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/cp/cpio/package.nix
  > Program to create or extract from cpio archives

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/cr/cracklib/package.nix
  > Password checking library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/cr/cryptsetup/package.nix
  > LUKS for dm-crypt

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/cy/cyrus_sasl/package.nix
  > Library for adding authentication support to connection-based protocols

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/da/dash/package.nix
  > POSIX-compliant implementation of /bin/sh that aims to be as small as possible

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/db/dbus-broker/package.nix
  > C-Util Project is a collection of utility libraries for the C11 language

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/db/dbus/package.nix
  > Simple interprocess messaging system

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/dh/dhcpcd/package.nix
  > Client for the Dynamic Host Configuration Protocol (DHCP)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/di/diffutils/package.nix
  > Commands for showing the differences between files (diff, cmp, etc.)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/dn/dns-root-data/package.nix
  > DNS root data including root hints and DNSSEC root trust anchor + key

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/do/dosfstools/package.nix
  > Utilities for creating and checking FAT and VFAT file systems

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/e2/e2fsprogs/package.nix
  > Tools for creating and checking ext2/ext3/ext4 filesystems

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ed/ed/package.nix
  > GNU implementation of the standard Unix editor

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ed/editline/package.nix
  > Readline() replacement for UNIX without termcap (ncurses)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/el/elfutils/package.nix
  > Set of utilities to handle ELF objects

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ex/expat/package.nix
  > Stream-oriented XML parser library written in C

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/fi/file/package.nix
  > Program that shows the type of files

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/fi/findutils/package.nix
  > GNU Find Utilities, the basic directory searching utilities of the GNU operating system

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/fr/freetype/package.nix
  > Font rendering engine

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/fs/fstrm/package.nix
  > Frame Streams implementation in C

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/gd/gdbm/package.nix
  > GNU dbm key/value database library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/gl/glib/package.nix
  > C library of programming buildings blocks

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/gn/gnugrep/package.nix
  > GNU implementation of the Unix grep command

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/gn/gnupatch/package.nix
  > GNU Patch, a program to apply differences to files

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/gn/gnused/package.nix
  > GNU sed, a batch stream editor

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/gn/gnutar/package.nix
  > GNU implementation of the `tar` archiver

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/gn/gnutls/package.nix
  > GNU Transport Layer Security Library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/gp/gpm/package.nix
  > Daemon that provides mouse support on the Linux console

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/gr/groff/package.nix
  > GNU Troff, a typesetting package that reads plain text and produces formatted output

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/gz/gzip/package.nix
  > GNU zip compression program

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/hi/hicolor-icon-theme/package.nix
  > Default fallback theme used by implementations of the icon theme specification

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ho/hostname-debian/package.nix
  > Utility to set/show the host name or domain name

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/hw/hwloc/package.nix
  > Portable abstraction of hierarchical architectures for high-performance computing

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ia/iana-etc/package.nix
  > IANA protocol and port number assignments (/etc/protocols and /etc/services)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ip/iproute2/package.nix
  > Collection of utilities for controlling TCP/IP networking and traffic control in Linux

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ip/iptables/package.nix
  > Program to configure the Linux IP packet filtering ruleset

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/je/jemalloc/package.nix
  > General purpose malloc(3) implementation

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/jq/jq/package.nix
  > Lightweight and flexible command-line JSON processor

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/kb/kbd/package.nix
  > Linux keyboard tools and keyboard maps

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ke/kexec-tools/package.nix
  > Tools related to the kexec Linux feature

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ke/keyutils/package.nix
  > Tools used to control the Linux kernel key management system

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/kr/krb5/package.nix
  > MIT Kerberos 5

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/le/less/package.nix
  > More advanced file pager than 'more'

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libaio/package.nix
  > Library for asynchronous I/O in Linux

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libapparmor/package.nix
  > Mandatory access control system - core library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libarchive/package.nix
  > Multi-format archive and compression library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libassuan/package.nix
  > IPC library used by GnuPG and related software

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libblake3/package.nix
  > Official C implementation of BLAKE3

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libbpf/package.nix
  > Library for loading eBPF programs and reading and manipulating eBPF objects from user-space

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libbsd/package.nix
  > Common functions found on BSD systems

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libcap/package.nix
  > Library for working with POSIX capabilities

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libcap_ng/package.nix
  > Library for working with POSIX capabilities

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libcbor/package.nix
  > CBOR protocol implementation for C and others

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libcpuid/package.nix
  > Small C library for CPU detection and feature extraction

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libedit/package.nix
  > Port of the NetBSD Editline library (libedit)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libevent/package.nix
  > Event notification library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libffiReal/package.nix
  > Foreign function call interface library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libgcrypt/package.nix
  > General-purpose cryptographic library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libgit2/package.nix
  > Linkable library implementation of Git that you can use in your application

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libgpg-error/package.nix
  > Small library that defines common error values for all GnuPG components

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libice/package.nix
  > Inter-Client Exchange Library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libksba/package.nix
  > CMS and X.509 access library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libmd/package.nix
  > Message Digest functions from BSD systems

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libmnl/package.nix
  > Minimalistic user-space library oriented to Netlink developers

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libnetfilter_conntrack/package.nix
  > Userspace library providing an API to the in-kernel connection tracking state table

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libnfnetlink/package.nix
  > Low-level library for netfilter related kernel/userspace communication

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libnftnl/package.nix
  > Userspace library providing a low-level netlink API to the in-kernel nf_tables subsystem

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libnl/package.nix
  > Linux Netlink interface library suite

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libpcap/package.nix
  > Packet Capture Library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libpipeline/package.nix
  > C library for manipulating pipelines of subprocesses in a flexible and convenient way

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libpng/package.nix
  > Official reference implementation for the PNG file format

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libpsl/package.nix
  > C library for the Publix Suffix List

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libpwquality/package.nix
  > Password quality checking and random password generation library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libseccomp/package.nix
  > High level library for the Linux Kernel seccomp filter

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libselinux/package.nix
  > SELinux core library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libsm/package.nix
  > X Session Management Library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libsodium/package.nix
  > Modern and easy-to-use crypto library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libssh2/package.nix
  > Client-side C library implementing the SSH2 protocol

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libtasn1/package.nix
  > ASN.1 library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libtool_2/package.nix
  > GNU Libtool, a generic library support script

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libtpms/package.nix
  > Library for software emulation of a Trusted Platform Module (TPM 1.2 and TPM 2.0)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/liburcu/package.nix
  > Userspace RCU (read-copy-update) library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libusb1/package.nix
  > Cross-platform user-mode USB device library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libuv/package.nix
  > Multi-platform support library with a focus on asynchronous I/O

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libx11/package.nix
  > Core X11 protocol client library (aka \

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libxau/package.nix
  > Functions for handling Xauthority files and entries.

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libxcb/package.nix
  > C interface to the X Window System protocol

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libxdmcp/package.nix
  > X Display Manager Control Protocol library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libxext/package.nix
  > Xlib-based library for common extensions to the X11 protocol

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libxmu/package.nix
  > X miscellaneous utility routines library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/libxt/package.nix
  > X Toolkit Intrinsics library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/li/linux-pam/package.nix
  > Pluggable Authentication Modules, a flexible mechanism for authenticating user

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ll/llhttp/package.nix
  > Port of http_parser to llparse

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/lo/logrotate/package.nix
  > Rotates and compresses system logs

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/lo/lowdown/package.nix
  > Simple markdown translator

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/lz/lz4/package.nix
  > Extremely fast compression algorithm

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/lz/lzo/package.nix
  > Real-time data (de)compression library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ma/mailcap/package.nix
  > Helper application and MIME type associations for file types

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ma/man-db/package.nix
  > Implementation of the standard Unix documentation system accessed using the man command

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/md/mdadm4/package.nix
  > Programs for managing RAID arrays under Linux

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/mk/mkpasswd/package.nix
  > Overfeatured front-end to crypt, from the Debian whois package

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/mp/mpdecimal/package.nix
  > Library for arbitrary precision decimal floating point arithmetic

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/na/nano/package.nix
  > Small, user-friendly console text editor

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ng/nghttp2/package.nix
  > HTTP/2 C library and tools

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ng/nghttp3/package.nix
  > Implementation of HTTP/3 mapping over QUIC and QPACK in C

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ng/ngtcp2/package.nix
  > Implementation of the QUIC protocol (RFC9000)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ni/nix-bash-completions/package.nix
  > Bash completions for Nix, NixOS, and NixOps

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ni/nixos-rebuild-ng/package.nix
  > Rebuild your NixOS configuration and switch to it, on local hosts and remote

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/np/npth/package.nix
  > New GNU Portable Threads Library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ns/nsncd/package.nix
  > Name service non-caching daemon

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/on/onetbb/package.nix
  > oneAPI Threading Building Blocks

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/on/oniguruma/package.nix
  > Regular expressions library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/op/openldap/package.nix
  > Open source implementation of the Lightweight Directory Access Protocol

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/op/openresolv/package.nix
  > Program to manage /etc/resolv.conf

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/p1/p11-kit/package.nix
  > Library for loading and sharing PKCS#11 modules

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/pc/pcre2/package.nix
  > Perl Compatible Regular Expressions

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/pc/pcsclite/package.nix
  > Middleware to access a smart card using SCard API (PC/SC)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/po/popt/package.nix
  > Command line option parsing library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/pu/publicsuffix-list/package.nix
  > Cross-vendor public domain suffix database

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/qr/qrencode/package.nix
  > C library and command line tool for encoding data in a QR Code symbol

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/rs/rsync/package.nix
  > Fast incremental file transfer utility

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/s2/s2n-tls/package.nix
  > C99 implementation of the TLS/SSL protocols

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/sh/shadow/package.nix
  > Suite containing authentication-related tools such as passwd and su

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/sh/shared-mime-info/package.nix
  > Database of common MIME types

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/so/sound-theme-freedesktop/package.nix
  > Freedesktop reference sound theme

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/st/strace/package.nix
  > System call tracer for Linux

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/su/sudo/package.nix
  > Command to run commands as root

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/tc/tcb/package.nix
  > Alternative password shadowing scheme

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ti/time/package.nix
  > Tool that runs programs and summarizes the system resources they use

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/tp/tpm2-tss/package.nix
  > OSS implementation of the TCG TPM2 Software Stack (TSS2)

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/tz/tzdata/package.nix
  > Database of current and historical time zones

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/un/unbound/package.nix
  > Validating, recursive, and caching DNS resolver

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/ut/util-linux/package.nix
  > Set of system utilities for Linux

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/w3/w3m/package.nix
  > Text-mode web browser

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/wh/which/package.nix
  > Shows the full path of (shell) commands

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/xa/xauth/package.nix
  > X authority file utility

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/xx/xxhash/package.nix
  > Extremely fast hash algorithm

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/xz/xz/package.nix
  > General-purpose data compression software, successor of LZMA

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/by-name/zs/zstd/package.nix
  > Zstandard real-time compression algorithm

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/acl/default.nix
  > Library and tools for manipulating access control lists

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/attr/default.nix
  > Library and tools for manipulating extended attributes

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/fontconfig/default.nix
  > Library for font customization and configuration

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/glibc/default.nix
  > GNU C Library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/libidn2/default.nix
  > Free software implementation of IDNA2008 and TR46

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/libunistring/default.nix
  > Unicode string library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/libxcrypt/default.nix
  > Extended crypt library for descrypt, md5crypt, bcrypt, and others

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/ncurses/default.nix
  > Free software emulation of curses in SVR4 and more

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/readline/8.3.nix
  > Library for interactive line editing

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/sqlite/default.nix
  > Self-contained, serverless, zero-configuration, transactional SQL database engine

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/libraries/zlib/default.nix
  > Lossless data-compression library

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/os-specific/linux/iputils/default.nix
  > Set of small useful utilities for Linux networking

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/os-specific/linux/kmod/default.nix
  > Tools for loading and managing Linux kernel modules

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/os-specific/linux/procps-ng/default.nix
  > Utilities that give information about processes using the /proc filesystem

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/os-specific/linux/systemd/default.nix
  > System and service manager for Linux

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/shells/bash/5.nix
  > GNU Bourne-Again Shell, the de facto standard shell on Linux

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/tools/security/gnupg/24.nix
  > Modern release of the GNU Privacy Guard, a GPL OpenPGP implementation

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/tools/text/gawk/default.nix
  > GNU implementation of the Awk programming language

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/top-level/perl-packages.nix
  > Module for reading .ini-style configuration files

- https://raw.githubusercontent.com/Perl/perl5/blead/pod/perlintro.pod
  > This document is intended to give you a quick overview of the Perl programming language

- https://raw.githubusercontent.com/Yubico/libfido2/main/README.adoc
  > provides library functionality and command-line tools to communicate with a FIDO device over USB or NFC

- https://raw.githubusercontent.com/c-util/c-dvar/main/README.md
  > The c-dvar project implements the D-Bus Variant Type-System.

- https://raw.githubusercontent.com/c-util/c-ini/main/README.md
  > The c-ini project implements APIs to deal with ini-files.

- https://raw.githubusercontent.com/c-util/c-rbtree/main/README.md
  > The c-rbtree project implements an intrusive collection based on red-black trees in ISO-C11.

- https://raw.githubusercontent.com/c-util/c-shquote/main/README.md
  > To use c-shquote, include c-shquote.h and link to the libcshquote.so library.

- https://raw.githubusercontent.com/c-util/c-utf8/main/README.md
  > The c-utf8 project implements utility functions around handling UTF-8 in standard ISO C11.

- https://raw.githubusercontent.com/curl/curl/master/README.md
  > libcurl is the library curl is using to do its job.

- https://raw.githubusercontent.com/json-c/json-c/master/README.md
  > JSON-C - A JSON implementation in C

- https://raw.githubusercontent.com/libfuse/libfuse/master/README.md
  > libfuse provides functions to mount the file system, unmount it, read requests from the kernel, and send responses back.

- https://raw.githubusercontent.com/libressl/portable/master/README.md
  > LibreSSL provides much of the OpenSSL 1.1 API.

- https://raw.githubusercontent.com/openssh/openssh-portable/master/README
  > This is the port of OpenBSD's excellent OpenSSH[0] to Linux and other Unices.

- https://raw.githubusercontent.com/openssl/openssl/master/README.md
  > The protocol implementations are based on a full-strength general purpose cryptographic library, which can also be used stand-alone.

- https://raw.githubusercontent.com/python/cpython/main/README.rst
  > Installable Python kits, and information about using Python, are available at

- https://raw.githubusercontent.com/unicode-org/icu/main/README.md
  > International Components for Unicode

- https://sourceware.org/lvm2/
  > LVM2 refers to the userspace toolset that provide logical volume management facilities on linux.

- https://www.boost.org/
  > Boost C++ Homepage Libraries

- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html
  > A unit file is a plain text ini-style file that encodes information about a service

- https://www.gnu.org/s/grub/
  > GNU GRUB is a Multiboot boot loader.

- https://www.gnu.org/software/libmicrohttpd/
  > GNU libmicrohttpd is a small C library that makes it easy to run an HTTP server as part of another application.

- https://www.lysator.liu.se/~nisse/nettle/
  > Nettle is a cryptographic library

- https://www.oracle.com/database/technologies/related/berkeleydb.html
  > Berkeley DB is a family of embedded key-value database libraries

## Additional source observations

- https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/lib/systemd-lib.nix generates restart inputs with `pkgs.writeText "X-Restart-Triggers-${name}"`.
- https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/system/activation/switchable-system.nix defines `pkgs.writers.writeJSON "switch-inhibitors" config.system.switch.inhibitors` and the constant `pkgs.writeText "empty-inhibitors" "{}"`. The constant is an operational comparison input, not a user document.
- https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/misc/documentation.nix defines `pkgs.writeShellScriptBin "nixos-help"`. The helper is executable even though it opens documentation.
- https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/services/networking/dhcpcd.nix defines `pkgs.writeShellScript "migrate-dhcpcd"` as a service pre-start command.
- A1/in/raw/nixos/activation-script.txt directly sources the mount and support scripts, executes the account-update and configuration-installation scripts, and consumes the account description and firmware path.

## Verification

The final subset has 618 unique IDs, exactly matching the selected input kind. Every decision is allowed; the header and six-field shape are exact. Word limits were checked mechanically. Counts are provided in the subset result notification.

## Review clarification: protocol and service mapping databases

For `nixos-7d271b79b7`, the package source identifies the installed protocol and service mapping files. Additional primary documentation establishes their database role explicitly:

- [getservent(3)](https://man7.org/linux/man-pages/man3/getservent.3.html), FILES: `/etc/services` — “services database file”. Its description says name and port lookup functions return entries from that database.
- [getprotoent(3)](https://man7.org/linux/man-pages/man3/getprotoent.3.html), FILES: `/etc/protocols` — “protocol database file”. Its description says name and protocol-number lookups return entries from that database.

Thus the row's database characterization is documented, not inferred merely from the package name. The HOLE remains the two readings already stated: operational mappings affect behavior under S2.2-1/2, while S2.2-4 explicitly names database contents among exempt content.


# Part 3 stored-object decisions

All 97 rows were decided individually. The writing script contains one explicit decision per ID; it does not classify rows by a homogeneous rule. Therefore the ten-sample requirement for scripted homogeneous classification does not apply. No files were removed or experiments run.

The inventory sometimes reports members=1 for a whole directory. Its full saved inventory was consulted; a directory with missing target contents is not presumed homogeneous. UNKNOWN denotes missing operational evidence, not a claimed defect in the text. Questions about state-management design were not independently treated as holes.

## Exact deciding sentences

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;

- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;

- **S2.2-6** records of the past—logs, history;

- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.

- **S3-2** If what the object does remains unknown, the case yields ?.

## Raw evidence

`../in/raw/nixos/unowned-groups.json` establishes each stored file type, target, size, and enumerated directory membership. `../in/raw/nixos/directory-only-groups.json` lists directory remainder members. `../in/raw/nixos/day.log` demonstrates hello execution through its user profile and writes the editor command `set number` and an ordinary work note. `../in/raw/nixos/user-profile.txt` and `user-closure-outside-system.txt` identify the installed hello environment. `../in/raw/nixos/root-profile.txt` supplies no installed packages. `A1/in/raw/nixos/nixos-configuration/configuration.nix` specifies boot, accounts, login keys, services, and privilege policy. `../in/raw/nixos/store-outside-system-closure.txt` supplies names, not the contents or consumer of every store object.

## Public documentation

The following short quotations establish functions independently of inventory classification language. URL citations supplement raw identity evidence; they do not prove absent local settings.

- Boot image: https://www.gnu.org/software/grub/manual/grub/html_node/Simple-configuration.html — “Set a background image for use with the ‘gfxterm’ graphical terminal.”
- Boot fonts: https://www.gnu.org/software/grub/manual/grub/grub.html — “Fonts are loaded with the “loadfont” command in GRUB”.
- Shell initialization: https://man7.org/linux/man-pages/man1/bash.1.html — “executes commands from the file /etc/profile, if that file exists.”
- DHCP hooks: https://manpages.debian.org/testing/dhcpcd-base/dhcpcd-run-hooks.8.en.html — “run any system and user defined hook scripts.”
- Binary registration: https://www.freedesktop.org/software/systemd/man/latest/binfmt.d.html — “register in the kernel additional binary formats for executables.”
- Service environment: https://www.freedesktop.org/software/systemd/man/latest/environment.d.html — “environment variable assignments passed to services started by the systemd user instance.”
- Filesystems: https://man7.org/linux/man-pages/man5/fstab.5.html — “The file fstab contains descriptive information about the filesystems the system can mount.”
- Account creation: https://man7.org/linux/man-pages/man8/useradd.8.html — “useradd - create a new user or update default new user information”.
- Address ordering: https://man7.org/linux/man-pages/man5/gai.conf.5.html — “these answers must be sorted so that the answer with the highest success rate is first in the list.”
- Groups: https://man7.org/linux/man-pages/man5/group.5.html — “The /etc/group file is a text file that defines the groups on the system.”
- Resolver: https://man7.org/linux/man-pages/man5/host.conf.5.html — “The file /etc/host.conf contains configuration information specific to the resolver library.”
- Host name: https://www.freedesktop.org/software/systemd/man/latest/hostname.html — “The `/etc/hostname` file configures the name of the local system.”
- Host mapping: https://man7.org/linux/man-pages/man5/hosts.5.html — “This file is a simple text file that associates IP addresses with hostnames”.
- Shared input: https://man7.org/linux/man-pages/man3/readline.3.html — “Other lines denote key bindings and variable settings.”
- Login banner: https://man7.org/linux/man-pages/man5/issue.5.html — “a message or system identification to be printed before the login prompt.”
- Locale: https://www.freedesktop.org/software/systemd/man/latest/locale.conf.html — “The locale settings configured in `/etc/locale.conf` are system-wide and are inherited by every service or user”.
- Login defaults: https://man7.org/linux/man-pages/man5/login.defs.5.html — “The /etc/login.defs file defines the site-specific configuration for the shadow password suite.”
- Machine identity: https://www.freedesktop.org/software/systemd/man/latest/machine-id.html — “The `/etc/machine-id` file contains the unique machine ID of the local system that is set during installation or boot.”
- Manual settings: https://man7.org/linux/man-pages/man5/manpath.5.html — “The manpath configuration file is used by the manual page utilities to assess users' manpaths at run time”.
- Kernel module settings: https://man7.org/linux/man-pages/man5/modprobe.d.5.html — “modprobe.d - Configuration directory for modprobe”.
- Boot modules: https://www.freedesktop.org/software/systemd/man/latest/modules-load.d.html — “contain kernel modules to load during boot in a static list.”
- Editor settings: https://www.nano-editor.org/dist/latest/nanorc.5.html — “The nanorc files contain the default settings for nano”.
- Shared name-service policy: https://www.man7.org/linux/man-pages/man5/nsswitch.conf.5.html — “sources from which to obtain name-service information”; netgroup: “Network-wide list of hosts and users, used for access rules.”
- Name-service cache configuration: https://man7.org/linux/man-pages/man5/nscd.conf.5.html — “The file /etc/nscd.conf is read from nscd(8) at startup.”
- Session environment: https://man7.org/linux/man-pages/man5/pam_env.conf.5.html — “When someone logs in, these files are read and the environment variables are set according.”
- Authentication: https://man7.org/linux/man-pages/man5/pam.d.5.html — “When a PAM aware privilege granting application is started, it activates its attachment to the PAM-API.”
- Accounts: https://man7.org/linux/man-pages/man5/passwd.5.html — “The /etc/passwd file is a text file that describes user login accounts for the system.”
- Certificate trust: https://docs.openssl.org/3.0/man3/SSL_CTX_load_verify_locations/ — “The certificates available via CAfile, CApath and CAstore are trusted.”
- Protocol lookup: https://man7.org/linux/man-pages/man5/protocols.5.html — “This file is a plain ASCII file, describing the various DARPA internet protocols that are available from the TCP/IP subsystem.”
- DNS lookup: https://man7.org/linux/man-pages/man5/resolv.conf.5.html — “The resolver is a set of routines in the C library that provide access to the Internet Domain Name System (DNS).”
- Resolver generator configuration: https://man.netbsd.org/NetBSD-6.0.3/resolvconf.conf.5 — “resolvconf.conf file is a shell script that is sourced by resolvconf(8)”.
- RPC lookup: https://man7.org/linux/man-pages/man5/rpc.5.html — “The rpc file contains user readable names that can be used in place of RPC program numbers.”
- Service lookup: https://man7.org/linux/man-pages/man5/services.5.html — “providing a mapping between human-friendly textual names for internet services, and their underlying assigned port numbers and protocol types.”
- Environment script: https://wiki.nixos.org/wiki/NixOS_system_configuration — “source /etc/set-environment”.
- Password policy: https://man7.org/linux/man-pages/man5/shadow.5.html — “If the password field begins with an exclamation mark !, the password is locked.”
- Login shells: https://man7.org/linux/man-pages/man5/shells.5.html — “This file is consulted by chsh(1) and available to be queried by other programs.”
- Subordinate groups: https://man7.org/linux/man-pages/man5/subgid.5.html — “Subgid authorizes a group id to map ranges of group ids from its namespace into child namespaces.”
- Subordinate users: https://man7.org/linux/man-pages/man5/subuid.5.html — “Subuid authorizes a user id to map ranges of user ids from its namespace into child namespaces.”
- Kernel parameters: https://www.freedesktop.org/software/systemd/man/latest/sysctl.d.html — “Configure kernel parameters at boot”.
- Terminal descriptions: https://man7.org/linux/man-pages/man5/termcap.5.html — “new programs should use the terminfo(5) database and associated libraries.”
- Runtime file rules: https://www.freedesktop.org/software/systemd/man/latest/tmpfiles.d.html — “Configuration for creation, deletion, and cleaning of files and directories”.
- Device rules: https://www.freedesktop.org/software/systemd/man/latest/udev.html — “udev supplies the system software with device events, manages permissions of device nodes”.
- Console: https://www.freedesktop.org/software/systemd/man/latest/vconsole.conf.html — “The `/etc/vconsole.conf` file configures the virtual console, i.e. keyboard mapping and console font.”
- Timezone: https://man7.org/linux/man-pages/man5/tzfile.5.html — “The timezone information files used by tzset(3) are typically found under a directory with a name like /usr/share/zoneinfo.”
- Profile selection: https://nix.dev/manual/nix/2.28/package-management/profiles — “The solution Nix uses is to create directory trees of symlinks to activated packages.”
- Channels: https://nix.dev/manual/nix/2.28/command-ref/nix-channel — “Channels are a mechanism for referencing remote Nix expressions and conveniently retrieving their latest version.”
- Daemon access: https://nix.dev/manual/nix/2.28/command-ref/nix-daemon — “It runs build tasks and other operations on the Nix store on behalf of unprivileged users.”
- Store database: https://nix.dev/manual/nix/2.28/store/types/local-store — “Nix's store metadata is in `/tmp/root/nix/var/nix/db`.”
- Collection roots: https://nix.dev/manual/nix/2.28/package-management/garbage-collector-roots — “the garbage collector will not remove `/nix/store/d718ef...-foo` or any of its dependencies.”
- Cache lookup: https://nix.dev/manual/nix/2.34/command-ref/conf-file.html?highlight=allowed-user — “Set to `0` to force updating the lookup cache.”
- Update markers: https://www.freedesktop.org/software/systemd/man/latest/systemd-update-done.service.html — “use the `ConditionNeedsUpdate=`”; “according to the modification times of the files described above.”
- Lingering: https://www.freedesktop.org/software/systemd/man/latest/loginctl.html — “a user manager is spawned for the user at boot and kept around after logouts.”
- Timer state: https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html — “If true, the time when the service unit was last triggered is stored on disk.”
- Random seed: https://www.freedesktop.org/software/systemd/man/latest/systemd-random-seed.service.html — “loads an on-disk random seed into the kernel entropy pool during boot and saves it at shutdown.”
- Clock state: https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html — “uses this to possibly advance the system realtime clock on subsequent reboots”.
- Last login: https://man7.org/linux/man-pages/man8/lastlog2.8.html — “lastlog2 - displays date of last login for all users or a specific one”.
- Journal: https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — “journalctl is used to print the log entries stored in the journal”.
- Login history: https://man7.org/linux/man-pages/man5/utmp.5.html — “utmp, wtmp - login records”.
- Runtime compatibility: https://man7.org/linux/man-pages/man7/hier.7.html — “Once this purpose was served by /var/run and programs may continue to use it.”

## Mixed group and limits

`nixos-57da4d32dc` retains MIXED with the following complete partition. Paths below are relative to the group's directory. Each of the twelve inventoried members appears once; the account-specific lingering filename is described without publishing an account name.

| Member | Decision | Evidence and reason |
| --- | --- | --- |
| Group directory itself | MUST | Removing the containing directory makes the known required descendants unavailable. |
| `catalog` directory | NOT | Container of the catalog content described below. |
| `coredump` directory | UNKNOWN | Empty in the inventory; no saved permissions, local retention settings, or actual use establish this directory's removal effects. |
| `ephemeral-trees` directory | UNKNOWN | Empty in the inventory; no saved permissions or local consumers establish this directory's removal effects. |
| `linger` directory | MUST | Makes the known user-lingering marker available to the login manager. |
| `timers` directory | HOLE | Contains the operational history stamp described below. |
| `timesync` directory | MUST | Makes the stored clock file available. |
| `catalog/database` | NOT | A message catalog of descriptive strings; removing it loses explanatory content rather than journaling capability. |
| Account-specific file in `linger` | MUST | Enables continued user services according to loginctl documentation. |
| `random-seed` | MUST | Feeds the kernel entropy pool according to random-seed service documentation. |
| `timers/stamp-fstrim.timer` | HOLE | Records a previous invocation but controls future scheduling: S2.2-1 versus S2.2-6. |
| `timesync/clock` | MUST | Advances boot time according to timesyncd service documentation. |

Additional catalog evidence: https://www.freedesktop.org/software/systemd/man/latest/journalctl.html describes `--list-catalog` contents as “message IDs, plus their short description strings.” The same page's `--root` option explicitly maps `--update-catalog` to `var/lib/systemd/catalog/database`; `--update-catalog` rebuilds the binary index from installed catalog files. This establishes the content function of the inventoried database. Unknown empty-directory members are now explicit rather than silently inherited from absent content.

Review correction for `nixos-2527479582`: the documentation identifies multiple manual-page utilities; no local contents or consumer evidence establish the literal one-program condition. The decision is UNKNOWN under S3-1/S3-2. This corrects an unsupported exemption inference, not the fixed text.


For single files containing both mandatory and exempt fields, MUST means the object cannot be omitted wholesale, not that every password byte must be recorded. Thus the shadow-file decision retains S2.2-15's explicit password exemption. A group uses MIXED when its members receive different decisions, including explicitly identified UNKNOWN members. Missing knowledge is retained at member level when other members have established decisions.

The update-marker holes and timer hole concern dual applicability of a stated history exemption and a documented behavioral dependency, not an objection that the text leaves state-transfer design unspecified.

## Reviewed heterogeneous-group partitions

These partitions replace the original whole-group UNKNOWN results. The classification does not require every member's function to be known before MIXED is usable. UNKNOWN is one of the allowed member decisions. A disjoint named subset followed by its explicit complement exhausts the saved group.

- `nixos-bfd49e603a` (4347 members): NOT applies to `/nix/store/wsm1x62rvhk30y7mqy1mp4yj8hhgglz1-nixos-rebuild.8.scd` and `/nix/store/yyrh92g94j8ljs6jaylqb8s7lkh6kggi-nixos-version.8`, which are the named manual-page documents. UNKNOWN applies to all 4345 other paths in `../in/raw/nixos/store-outside-system-closure.txt`; their names alone do not establish all contents, execution boundaries, and consumers. No hello path from `user-closure-outside-system.txt` appears in this particular saved listing; the two inventories must not be silently conflated.
- `nixos-76634f69cd` (338 members, paths relative to `/boot/grub`): MUST applies to the 274 `i386-pc/*.mod` loadable GRUB modules and the containing `i386-pc` and group directories (276 members). NOT applies to `fonts/unicode.pf2`, the 43 `locale/*.mo` translation catalogs, and their `fonts` and `locale` directories (46 members). UNKNOWN applies to all remaining 16 inventoried members; saved contents and consumers do not establish their individual local roles. The module functions, command implementations, filesystem drivers, and loader support run within the bootloader's authority; they are not documents.
- `nixos-0075a76d48` (11 members, paths relative to `/etc/ssh`): MUST applies to the account-specific authorized-key file, its `authorized_keys.d` directory, and the group directory (3 members), because removing them removes login-key availability. UNKNOWN applies to the two private host-key files, two public host-key files, and the `moduli`, `ssh_config`, `ssh_known_hosts`, and `sshd_config` links (8 members). This retains uncertainty about their particular local consumers, policy contents, and effects rather than assuming they are exempt.
- `nixos-b86fee9a16` (21 members, paths relative to `/etc/systemd`): MUST applies to `system-environment-generators/env-generator`, its `system-environment-generators` directory, and the group directory (3 members). UNKNOWN applies to all other 18 members: the two preset directories, two preset links, eight `.conf` links, `generator-environment.json`, and the five service/generator/shutdown-tree links. The actual preset and daemon settings and the target tree members were not saved. The known generator is executed by the manager and exports environment to services.

Additional primary documentation:

- https://www.gnu.org/software/grub/manual/grub/grub.html — “Modules can be loaded via the `insmod` (see insmod) command.”
- https://www.gnu.org/software/gettext/manual/gettext.html — “messages are converted to UTF-8 encoding before being stored in a MO file”.
- https://man.openbsd.org/sshd — “`AuthorizedKeysFile` specifies the files containing public keys for public key authentication”.
- https://www.freedesktop.org/software/systemd/man/254/systemd.environment-generator.html — “Generators are small executables”; “before starting any units.”


# Unit classification notes

Scope: 150 rows of kinds system-unit, system-units, user-unit, user-units from `../in/part-3.tsv`. No other classification was consulted. No objects were removed and no probes were run.

## Deciding sentences

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S3-2: “If what the object does remains unknown, the case yields ?.”

## Homogeneous rule U

A loaded unit definition that controls process execution, service activation, filesystem mounting, cross-process dependencies or process resource grouping is MUST under S2.2-1 and S2.2-2. Removing its contribution removes the named management, activation, scheduling, mounting or ordering capability. Units are read as values; this does not make them code under S2.2-13, nor does it make their effects internal to one program under S2.2-7. Their effects reach independently executing processes, shared filesystem interfaces or system resources. A unit need not be currently active to provide a capability. A service that writes logs or maintains caches is not itself a log or cache.

This one rule covers the 139 singular loaded-unit rows; descriptions are taken from the inventory, with explicit documentation for three custom hooks below. The script formats each type's operational description and reasoning; it does not classify from an inventory label. Ten manually checked rows spanning its mechanisms:

| ID | Observed object | Check |
|---|---|---|
| nixos-002aa91047 | Root slice | Active resource hierarchy; slice documentation establishes cross-process resource management. |
| nixos-77462850bc | Basic system target | Loaded boot synchronization and grouping unit; target documentation establishes dependent-unit ordering. |
| nixos-0384997ab4 | System message-bus service | Active running separate bus process; service management has external IPC effects. |
| nixos-06be1b0d47 | Message-bus socket | Active running socket; socket documentation establishes IPC and process activation. |
| nixos-16081f0750 | Huge-pages mount | Active mounted kernel filesystem; removing mounting capability affects filesystem access. |
| nixos-f5fee7c08e | Filesystem trim timer | Active waiting scheduled discard service; timer documentation establishes timed activation. |
| nixos-46b677ba51 | Console password path watcher | Active waiting path unit; path documentation establishes event-triggered activation. |
| nixos-feed84b43d | Emergency shell service | Inactive but loaded shell-launch definition; availability is a capability, independent of current execution. |
| nixos-05069d5c04 | Boot/shutdown accounting service | Unit executes accounting writer; it is not the historical records that writer produces. |
| nixos-f5943b1625 | User temporary-file cleanup timer | Active user timer schedules another process; user scope does not confine effects to a program interface. |

The observed state and description for each checked row are in `../in/raw/nixos/units.txt` or `../in/raw/nixos/user-list-units.txt`. Fragment and drop-in paths are corroborated by `../in/raw/nixos/unit-paths.txt`, `../in/raw/nixos/user-unit-paths.txt`, and `../in/raw/nixos/unit-realpaths.tsv`.

## Documentation supporting unit semantics

Short exact excerpts, each from the linked primary documentation:

- [Service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html): “encodes information about a process controlled and supervised by systemd.”
- [Socket](https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html): “Socket units may be used to implement on-demand starting of services, as well as parallelized starting of services.”
- [Mount](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html): “encodes information about a file system mount point controlled and supervised by systemd.” Runtime mounts are also monitored and listed as mount units.
- [Target](https://www.freedesktop.org/software/systemd/man/latest/systemd.target.html): “Target units are used to group units and to set synchronization points for ordering dependencies with other unit files.”
- [Slice](https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html): “A slice unit is a concept for hierarchically managing resources of a group of processes.”
- [Timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html): “By default, a service by the same name as the timer (except for the suffix) is activated.”
- [Path](https://www.freedesktop.org/software/systemd/man/latest/systemd.path.html): “For each path file, a matching unit file must exist, describing the unit to activate when the path changes.”
- [Scope](https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html): “Scope units manage a set of system processes.” They manage externally created processes and resource organization.
- [Device](https://www.freedesktop.org/software/systemd/man/latest/systemd.device.html): “This may be used to define dependencies between devices and other units.” These units are dynamically generated; mounts and sockets acquire dependencies on relevant devices.
- [Unit listing](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html): “List units that systemd currently has in memory.” Such references need not be installed definitions; the LOAD column distinguishes loaded and not-found.

## Custom definitions checked separately

- `nixos-afcf4a91ee`: [user configuration source](https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/config/users-groups.nix), exact identifiers `systemd.services.linger-users`, `disable-linger`, `enable-linger`. The service changes persistent user-manager execution. MUST under rule U.
- `nixos-189b4753ff`: [network configuration source](https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/tasks/network-interfaces.nix), “Run any user-specified commands.” The source links `network-local-commands` to network initialization and DNS configuration. MUST under rule U.
- `nixos-9f30203d50`: [power management source](https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/modules/config/power-management.nix), “Service executed after boot, and stopped during shutdown”. This is the boot/shutdown command-hook service. MUST under rule U; no claim that particular optional power commands are configured.

## Group rows decided individually

The members field says 1 for these inventory group rows, but the evidence explicitly enumerates multiple names. Decisions below apply to every named member, not merely one sample.

- `nixos-a3f2270221`: all listed device units expose kernel devices as dependency/activation units. MUST: device-dependent activation is behavior. This decision concerns the logical units, not a requirement to change hardware.
- `nixos-88335c6c87`: same mechanism for every listed user-visible device unit. MUST: device-dependent activation is behavior.
- `nixos-18fb2985ed`: root, store, key and runtime-directory mounts. All MUST because removing mounts removes the corresponding filesystem access capability.
- `nixos-565df89b5f`: every listed root, shared kernel-interface, store, credential, key, runtime and wrapper mount supplies filesystem access. All MUST.
- `nixos-0ff15b2741`: both listed scopes manage existing system or session processes. All MUST for lifecycle/resource-management behavior.
- `nixos-3bc8c8458c`: the initial-process scope manages an existing process group. MUST for lifecycle/resource-management behavior.
- `nixos-253d752b01`: all four slices group service instances or user processes for resource management. All MUST.
- `nixos-b855166ba5`: root slice provides the resource hierarchy. MUST.
- `nixos-eb57ff0e5c`: local SSH socket is loaded, active and listening according to the raw listing. MUST because removal removes that connection/activation path.
- `nixos-9994d7ebc4`: every member is explicitly not-found and inactive in the raw listing, with no loaded definition. UNKNOWN under S3-2: the inventory contains retained unit references, and absence of a definition does not establish their operational dependency effects. Neither stored unit-path metadata nor public documentation establishes which dependency relationships retain these particular references.
- `nixos-97fdaec6aa`: the sole block-device target reference is not-found and inactive. UNKNOWN under S3-2: its reference relationships and effects are not recorded. The missing definition alone cannot establish that the observed in-memory object does nothing.

These two decisions were corrected after review of the object boundary. [Unit listing documentation](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) expressly includes references in the in-memory listing; its definition of not-found establishes only that the unit file does not exist. [Dependency documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) distinguishes weak Wants dependencies from stronger Requires dependencies: “this unit will not be started” can follow failure of an ordered requirement. The raw inventories omit those dependency relationships. The uncertainty is factual, not a proposed change to the hypothesis.

## Verification

`part-3.units.build.py` preserves existing output rows and appends each missing row with a flush. It verifies exactly 150 distinct input IDs equal exactly 150 distinct output IDs and checks the decision vocabulary. Results: MUST 148, NOT 0, HOLE 0, UNKNOWN 2, MIXED 0.


## Mechanical verification

Input and output ids have the same set and count, with each id occurring once. All decisions, sentence references, field counts, and word limits were checked by `part-3.verify.py`.
