# Sources and mapping

Recorded 2026-11-22 UTC. Assessment c1 used only COMMON.md, TEXT.md,
SENTENCES.md, GATES/INPUTS-4-PUSHED, the selected C1 inputs and runner
documentation, official documentation, and its own clean clones. The gate names
commit `43594a47b72707f836953b6b39d5849d5513f61a`; hashes are checked in
`raw/input-verification.tsv` and `raw/server-runner.sha256`.

## Declaration and application

S2.1-1: “**Declaration**—a collection of files that a person has designated as the primary description of the computer.”
S2.1-2: “There may be many files; together they form one description and one source of truth about the system.”
S2.1-5: “**Application of the declaration**—an action of the system that brings the computer into conformity with the declaration.”
S3-3: “**Declaration in force and completed application.** The declaration in force is the declaration of the last application that the system has reported as successful; that report completes the application.”

NixOS: the designated files are the selected `configuration.nix` and
`hardware-configuration.nix`, interpreted with their imports and system defaults;
Guix: the selected `config.scm` operating-system expression with its imports and
defaults. Computed descriptions are permitted by S2.5-3. The mutable account
databases and per-user package profiles are not additional designated primary
files. Recording a package-manager/account-manager program does not itself
record every future package/account it can create.

The selected installation recipes invoke `nixos-install --no-root-passwd` and
`guix system init /mnt/etc/config.scm /mnt`, respectively. Their installed-system
application interfaces are `nixos-rebuild switch` and
`guix system reconfigure /etc/config.scm`. These build and activate the description;
normal exit status 0 is the command's machine-readable success report. NixOS also
prints “Done. The new configuration is” followed by its store path. Experiment
outputs retain the actual report and status rather than inferring success from a
boot or a package build. Failure would leave the prior declaration in force under
S3-4. No channel updates, declaration edits, or alternate installation inputs are
used.

## Official sources

N1. [NixOS 26.05 manual](https://nixos.org/manual/nixos/stable/), Installation,
Package Management, and User Management; `raw/nixos-manual.txt`.
Quotes: “specifies the intended configuration of the system.”;
“install, upgrade and uninstall packages via the nix-env command.”;
“Accounts can be modified using usermod.”
The manual distinguishes declarative packages from ad-hoc `nix-env` operations
and describes imperative user creation, modification and deletion.

N2. [Option documentation at the selected Nixpkgs revision](https://raw.githubusercontent.com/NixOS/nixpkgs/94c3211b0ee8/nixos/modules/config/users-groups.nix),
`raw/nixos-user-default.txt`.
Quotes: “This automatically sets {option}`group` to `users`,”;
“The user's primary group.”; “with the ordinary `useradd` and `groupadd` commands.”
The `isNormalUser` option sets the primary group to `users`; `mutableUsers`
defaults to true, permits additional users/groups and merges existing account
files with generated entries during activation. The clean NixOS evaluation
confirms both values (`raw/inspect-nixos.txt`). These are documented defaults,
not an invented interpretation of the line (S3-10).

G1. [Guix 1.5.0 Using the Configuration System](https://guix.gnu.org/manual/1.5.0/en/html_node/Using-the-Configuration-System.html),
`raw/guix-config.txt`: “The operating system is configured by providing an operating-system declaration in a file”.

G2. [Guix 1.5.0 Invoking guix system](https://guix.gnu.org/manual/1.5.0/en/html_node/Invoking-guix-system.html),
`raw/guix-system.txt`: “Build the operating system described in file, activate it, and switch to it”.
This describes `reconfigure`; the same section documents system deployment,
account/service activation, and system-generation creation.

G3. [Guix 1.5.0 User Accounts](https://guix.gnu.org/manual/1.5.0/en/html_node/User-Accounts.html),
`raw/guix-accounts.txt`: “Thus, account or group creations or modifications made by directly invoking commands such as useradd are lost upon reconfiguration or reboot.”
This explicitly establishes that imperative account modifications are possible
between applications; restoring the declaration on a later reconfiguration or
boot does not exclude that path after the previous completed application.

G4. [Guix 1.5.0 Invoking guix package](https://guix.gnu.org/manual/1.5.0/en/html_node/Invoking-guix-package.html),
`raw/guix-package.txt`: “The command operates only on the user’s own profile, and works with normal user privileges”.
This is an additional documented package-management path, not an additional
experiment or case. The account path alone suffices for the negative assessment.

T1. [Upstream useradd(8)](https://raw.githubusercontent.com/shadow-maint/shadow/master/man/useradd.8.xml),
`raw/useradd.txt`: “create a new user or update default new user information”.
T2. [Upstream usermod(8)](https://raw.githubusercontent.com/shadow-maint/shadow/master/man/usermod.8.xml),
`raw/usermod.txt`: “modify a user account”; “The usermod command modifies the system account files.”
NixOS installed `usermod(8)` excerpts are also retained with clean-installation inspection;
`-g` changes the primary group to an existing group. The online upstream page is
not assumed to establish the installed version by itself.

## Built-in-tool indicator

S3-6: “**Built-in tool.** A program of the system whose purpose, according to its documentation, includes changing what must be recorded: a package manager, including package managers of programming languages and of application packages; account and rights management; the service manager; network and firewall configuration.”
S3-7: “General-purpose programs—an editor, file copying, link creation, the command shell—are not built-in tools: changing with them, through superuser privileges, what must be recorded is breaking.”
S3-8: “If a program’s documentation does not state its purpose, the case yields ?; if it does and this indicator still does not decide whether the program is a built-in tool, the case is a counterexample to the definitions and yields 0.”

For each system, `useradd` and `usermod` are built-in under S3-6: their own
manuals explicitly document account management. NixOS clean-system inspection
locates them as system programs; Guix versioned sources establish inclusion (G5–G6). NixOS also documents `nix-env` as a package
manager; Guix documents `guix package` as its package-management interface.
`nixos-rebuild` and `guix system` are documented system-configuration application
tools that change packages/accounts/services, also falling under S3-6. The shell
is explicitly excluded by S3-7; it invokes the account tools and performs reads,
not direct account-file edits. `getent`, `sha256sum`, `date`, and text filters are
read-only evidence instruments, not paths changing an assessed object.
No relied-upon changing tool has a stated purpose left unclassified by S3-6–S3-8;
there is no such indicator counterexample to silently decide. This is not an
exhaustive census of the programs shipped by either distribution.

## Scope of the temporal counterexample

S2.3-1: “The properties concern the computer after a completed application of the declaration, provided there was no breaking.”
S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”
S2.1-4: “For a recorded object, its line states the required state; whether a recorded program is running at a given moment does not matter unless its line requires it.”

An account's primary group is an account property and affects group access
rights (S2.2-1, S2.2-2, S2.2-15). P2 is tested after a successful application and
before any later application: S3-3 continues to identify that declaration as in
force. There is no premise restricting P2 to the instant of the report. A
successful `usermod` invocation is not a successful application of the unchanged
declaration: it intentionally changes the account away from the specified group.
Superuser execution of a documented account tool is included by S2.3-7 and is
not the outside-built-in-tool breaking of S2.1-7. No password, removed-program
remnant, rollback, declaration edit timing or other S2.5 design question supplies
the counterexample. One counterexample suffices; no universal `has` claim or
power-cut experiment is needed.

## Guix transport limit and versioned source confirmation

The clean Guix clone was created with the selected `new d4c1-guix guix`
command. Startup reported a login timeout. The normal read-only `run` failed
inside the serial wrapper with a shell syntax error before the script ran;
the one planned root P2 attempt then failed at login. Therefore no Guix
`APPLICATION_EXIT`, account change, or declaration hash was observed. The
planned expected result is not counted as an experimental result. The missing
fact is the exact clean clone's application transcript, not the documented
existence of the imperative account path. G3 establishes that path independently.

G5. [Guix v1.5.0 system package defaults](https://codeberg.org/guix/guix/raw/tag/v1.5.0/gnu/system.scm),
`raw/guix-base-packages-source.txt`, defines `%base-packages` including
`%base-packages-utils`, which contains `shadow`.
[Guix v1.5.0 shadow package definition](https://codeberg.org/guix/guix/raw/tag/v1.5.0/gnu/packages/admin.scm),
`raw/guix-shadow-source.txt`, selects version 4.13 and describes tools including
`useradd`; its installation removes the duplicate `groups` utility, not
`usermod`. These primary sources confirm distribution integration in the absence
of a usable guest command record. The selected operating-system input does not
override the default package list.

G6. [shadow 4.13 usermod(8)](https://raw.githubusercontent.com/shadow-maint/shadow/4.13/man/usermod.8.xml),
`raw/guix-usermod-4.13.txt`: “modify a user account”; the `-g` option specifies
“The name or numerical ID of the user's new primary group.” and “The group must exist.”
Together G3, G5 and G6 establish a built-in account modification path on the
selected Guix System. G3 says these modifications disappear at the next
reconfiguration/reboot, so they may exist after the preceding completed
application. Its statement that application establishes the declared accounts
supplies the temporal starting point. The selected `config.scm` explicitly
requires `(group "users")` (exact selected-input excerpt:
[raw/guix-declaration-account.txt](raw/guix-declaration-account.txt)); a different primary group therefore violates its
recorded state. This is a documentation-based counterexample, not a claim that
the attempted Guix script succeeded. The failure of transport is not converted
into a property failure or a definitional counterexample (Section 4.1).

