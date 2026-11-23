# Accounts, loaded modules, and observed processes

Only `../in/part-2.tsv`, the relevant `A1/in/raw/debian/` inventory files, the fixed text, and the public sources below supplied evidence. No removal was performed. Inventory classification language was disregarded. Decisions concern the object represented by each row, not the text file reporting it.

## Rule A: accounts

All 27 account rows are account definitions confirmed by the seven fields in `accounts.txt`. S2.2-15 explicitly requires accounts, without limiting this to interactive accounts. Apply MUST to each account row. No account passwords are classified by this rule.

Documentation: https://man7.org/linux/man-pages/man5/passwd.5.html — “The /etc/passwd file is a text file that describes user login accounts for the system.”

Ten manual checks against the account records:

- debian-205e945769: UID 42, noninteractive account.
- debian-3fa3a857d8: UID 34, noninteractive account.
- debian-8d1e409524: UID 2, noninteractive account.
- debian-96a19ba1e6: UID 1000, interactive shell.
- debian-4900fca16b: UID 1, noninteractive account.
- debian-8e4a0f0c6a: UID 5, noninteractive account.
- debian-707e10c2e4: UID 39, noninteractive account.
- debian-3413994e24: UID 38, noninteractive account.
- debian-55e4967557: UID 7, noninteractive account.
- debian-cbaf0b4232: UID 0, privileged account.

Each record is an account, so the explicit sentence fits regardless of shell or UID.

## Rule K: loaded kernel modules

All 52 module rows are observed loaded modules in `modules.txt`, with corresponding module file paths in the input. They execute native code in kernel space, with the kernel's privileges, rather than in an interface restricting their capabilities. Apply MUST using S2.2-10. This is a code rule, not an inference that every module's removal prevents boot; redundant implementations do not override the explicit code requirement.

Documentation: https://man7.org/linux/man-pages/man2/init_module.2.html — “init_module() loads an ELF image into kernel space”. The same description states that loading runs the module's initialization function. https://docs.kernel.org/kbuild/modules.html — “after linking, will result in the kernel module <module_name>.ko.”

Ten manual checks against `modules.txt` and the input file paths:

- debian-ddb5a87d9a: aesni_intel, loaded, native crypto module path.
- debian-0074a80686: ata_generic, loaded, ATA driver module path.
- debian-4ef0af6396: ata_piix, loaded, ATA driver module path.
- debian-4fb00be8be: autofs4, loaded, filesystem module path.
- debian-d8aafdbe20: binfmt_misc, loaded, binary-format module path.
- debian-70a3c6eeb0: button, loaded, ACPI driver module path.
- debian-3b459c779e: cdrom, loaded, CD-ROM driver module path.
- debian-37eece24d6: configfs, loaded, filesystem module path.
- debian-3817fdb2ed: crc32_pclmul, loaded, native crypto module path.
- debian-ec81aeacb8: crc32c_intel, loaded, native crypto module path.

Each checked object is loaded kernel code. The inventory usage count is not a permissions boundary or an exemption.

## Rule P: observed executable processes

Apply MUST under S2.2-9 and S2.2-12 to the 14 executable process rows. `processes.txt` directly reports running commands; `process-executables.tsv` resolves executables where available. No assertion that a process is a saved setting is needed. The row for `ps` is observed in the process listing even though the executable-resolution snapshot missed this short-lived process.

Ten manual checks against both process inventories:

- debian-ce95966cbb: PID 805 executes bash.
- debian-670c720118: PID 501 executes the system bus daemon.
- debian-0605c303f7: PID 523 executes Python for the upgrade shutdown helper.
- debian-add864bf46: PID 804 executes sudo.
- debian-aee2bf821c: PID 286 runs device management; executable resolution names udevadm.
- debian-42c14762fe: PIDs 1, 579, 580 resolve to the service manager executable.
- debian-7b2f0c0e4f: PID 260 executes the journal daemon, not the journal records.
- debian-a7da54431d: PID 504 executes the login manager.
- debian-ca73c5eaa2: PID 445 executes the network manager.
- debian-b66da72753: PID 417 executes the resolver daemon.

Every checked row is an observed separate executable process, so the explicit program requirement applies without further assumptions about its individual configuration.

## Individual case: kernel threads

`debian-89ce5c5668` groups observed kernel threads. `processes.txt` identifies kernel task names and `process-executables.tsv` has no userspace executable for them. This is kernel code running with kernel privileges, meeting S2.2-10; the group is homogeneous at that decisive boundary. No claim that each thread is a separate installed userspace program is made.

Documentation: https://docs.kernel.org/driver-api/basics.html — “This helper function creates and names a kernel thread.” The kthread_create_on_node description explains that waking the task runs its supplied function. All listed members have the same MUST decision.

## Application and scope

`part-2.core.py` applies these three rules and the single kernel-thread case, appending only missing IDs to `part-2.tsv` and flushing each row. Raw paths in the basis field are relative to `A1/in/raw/`. Public documentation supplements the inventories; the inventories establish that these specific objects exist or execute.

## Exact deciding text

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.

- **S3-2** If what the object does remains unknown, the case yields ?.

