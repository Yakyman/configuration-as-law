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
