# Check 4 — assessment c1

Recorded 2026-11-22 UTC. Gate commit: `43594a47b72707f836953b6b39d5849d5513f61a`.
Exact inputs, source passages, full indicator quotations, and common mapping are
in [SOURCES.md](SOURCES.md); input verification is in [raw/input-verification.tsv](raw/input-verification.tsv).
Each decision below concerns the selected configuration of the named system.
No claim is made about all possible configurations of that distribution.
“After application” follows S2.3-1 and S3-3: the last successfully applied
unchanged declaration remains in force during subsequent built-in-tool actions.

## nixos / P1

Demand — S2.3-4: “**P1. Completeness.** Everything that must be recorded under Section 2.2 and is in force on the computer is recorded.” Accounts exist in force (S2.1-3) and must be recorded (S2.2-15).
Mapping — S2.1-1–2 designate `configuration.nix` plus `hardware-configuration.nix` and their computed imports/defaults; application is `nixos-rebuild switch` (S2.1-5), with its completion message/status 0 as success (S3-3).
Tool — `useradd` is account management under S3-6, by its [own manual](https://raw.githubusercontent.com/shadow-maint/shadow/master/man/useradd.8.xml): “create a new user or update default new user information”; S3-7 does not exclude it and S3-8 leaves no undecided purpose.
Facts — The [selected-revision option documentation](https://raw.githubusercontent.com/NixOS/nixpkgs/94c3211b0ee8/nixos/modules/config/users-groups.nix) permits additions “with the ordinary `useradd` and `groupadd` commands.” `users.mutableUsers` defaults to true; activation merges account databases with generated entries (N2).
Record — [raw/inspect-nixos.txt](raw/inspect-nixos.txt) confirms the exact release, both input hashes, installed `useradd`, and `mutableUsers=true`; [raw/p2-nixos.txt](raw/p2-nixos.txt) records completed application. No user-addition probe was needed: N2 and useradd(8) establish the path.
Decision — **does not have**. A newly added account can exist outside the designated primary files after application; the mutable account database is not itself the designated declaration. Built-in account creation is not breaking (S2.1-7–8). This one documented path is sufficient.

## nixos / P2

Demand — S2.3-5: “**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.” For this account, required state includes its primary group (S2.1-4, S2.2-15).
Mapping — S2.1-1–2 designate the same two Nix files; `nixos-rebuild switch` applies them (S2.1-5), and its explicit completion plus status 0 fixes the declaration in force (S3-3). `isNormalUser=true` supplies group `users` by the documented default (S3-10, N2).
Tool — The [usermod manual](https://raw.githubusercontent.com/shadow-maint/shadow/master/man/usermod.8.xml) says “modify a user account”; thus this installed program is built-in under S3-6, including with root privileges (S2.3-7), without an S3-8 ambiguity.
Facts — [Option documentation](https://raw.githubusercontent.com/NixOS/nixpkgs/94c3211b0ee8/nixos/modules/config/users-groups.nix): “This automatically sets {option}`group` to `users`,”; [NixOS manual](https://nixos.org/manual/nixos/stable/): “Accounts can be modified using usermod.” Installed manual/evaluation: [raw/inspect-nixos.txt](raw/inspect-nixos.txt).
Record — Expected result preceded the single run in [raw/p2-plan.md](raw/p2-plan.md); [commands](raw/p2-nixos.sh) and [output](raw/p2-nixos.txt) show `APPLICATION_EXIT=0`, primary GID 100, `USERMOD_EXIT=0`, then GID 1, with both declaration hashes unchanged. Cleanup restored GID 100.
Decision — **does not have**. After the successful application, the account has group `wheel` rather than required `users`; no intervening application replaces the declaration in force. The change uses a documented built-in tool, not breaking. Later restoration does not erase the witnessed mismatch (S2.3-1, S3-3).

## nixos / P4

Demand — S2.3-6: “**P4. Law.** The system provides no path for changing, past the declaration, anything that must be recorded.” S2.3-7 explicitly includes privileged built-in tools.
Mapping — S2.1-1–2 designate the two selected Nix files; `nixos-rebuild switch` is application (S2.1-5), and its success message/status 0 is the completion report (S3-3).
Tool — The [usermod manual](https://raw.githubusercontent.com/shadow-maint/shadow/master/man/usermod.8.xml) says “The usermod command modifies the system account files.” Its account-management purpose decides it as built-in by S3-6; S3-7 and S3-8 supply no exemption or unresolved classification.
Facts — Primary group is an account/access property that must be recorded (S2.2-1–2, S2.2-15); the [NixOS manual](https://nixos.org/manual/nixos/stable/) states “Accounts can be modified using usermod.” N2 also documents imperative account creation.
Record — The same established fact in [raw/p2-nixos.txt](raw/p2-nixos.txt), not a second experiment, shows privileged `usermod -g wheel user` changes that property successfully while both declaration hashes stay unchanged after application.
Decision — **does not have**. A built-in account tool changes required account state past the declaration. S2.1-7 defines breaking outside built-in tools, so superuser execution does not exclude this counterexample. Documentation and the one shared record suffice.

## guix / P1

Demand — S2.3-4: “**P1. Completeness.** Everything that must be recorded under Section 2.2 and is in force on the computer is recorded.” An account exists in force (S2.1-3) and must be recorded (S2.2-15).
Mapping — S2.1-1–2 designate the selected `config.scm` operating-system expression with its imported/default definitions; `guix system reconfigure /etc/config.scm` applies it (S2.1-5), and normal successful completion/status 0 is the report (S3-3). The initial recipe uses `guix system init`.
Tool — [useradd(8)](https://raw.githubusercontent.com/shadow-maint/shadow/master/man/useradd.8.xml): “create a new user or update default new user information”; account management decides it as built-in under S3-6, without an S3-8 ambiguity. Guix's own account manual names it, and versioned package sources establish system inclusion (G3, G5).
Facts — [Guix 1.5.0 User Accounts](https://guix.gnu.org/manual/1.5.0/en/html_node/User-Accounts.html): “Thus, account or group creations or modifications made by directly invoking commands such as useradd are lost upon reconfiguration or reboot.” This documents additional accounts between applications, without additions to the primary operating-system file.
Record — G1, G3 and G5 in [SOURCES.md](SOURCES.md), with saved excerpts/source, establish the path. The clean clone's transport failed ([raw/new-guix.txt](raw/new-guix.txt), [raw/inspect-guix.txt](raw/inspect-guix.txt)); no guest account observation or account-addition experiment is claimed.
Decision — **does not have**. A documented additional account can be in force after completed application until the next reconfiguration/reboot, without being recorded in `config.scm`. Built-in creation is not breaking; later removal does not exclude the earlier state (S2.3-1, S3-3).

## guix / P2

Demand — S2.3-5: “**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.” The [selected account excerpt](raw/guix-declaration-account.txt) explicitly has `(group "users")`; this is required account state (S2.1-4, S2.2-15).
Mapping — S2.1-1–2 designate `config.scm` and its computed imports/defaults; `guix system reconfigure /etc/config.scm` is application (S2.1-5), with successful completion/status 0 as report (S3-3). [The manual](https://guix.gnu.org/manual/1.5.0/en/html_node/Invoking-guix-system.html) says “Build the operating system described in file, activate it, and switch to it”.
Tool — [The versioned usermod(8) manual](https://raw.githubusercontent.com/shadow-maint/shadow/4.13/man/usermod.8.xml) says “modify a user account”; `-g` specifies “The name or numerical ID of the user's new primary group.” Guix 1.5.0 includes shadow 4.13 (G5), so S3-6 decides this as built-in, not breaking or an S3-8 ambiguity.
Facts — [Guix's account manual](https://guix.gnu.org/manual/1.5.0/en/html_node/User-Accounts.html) establishes the declared account properties at completion, and says imperative modifications “are lost upon reconfiguration or reboot.” G3 plus G6 therefore permit a subsequent primary-group modification before the next application, outside the operating-system declaration.
Record — This is a documentation-based decision (G2–G3, G5–G6), not a successful experiment: the expected result in [raw/p2-plan.md](raw/p2-plan.md) was followed by [one attempted script](raw/p2-guix.sh), which failed at serial login ([raw/p2-guix.txt](raw/p2-guix.txt)). No actual Guix application exit or account change was observed.
Decision — **does not have**. The documented built-in modification path can leave the declared account's primary group different after completed application, while S3-3 still selects the last applied declaration. The documentation establishes the counterexample independently of the unavailable clean-clone transcript; the transport failure itself proves nothing about P2.

## guix / P4

Demand — S2.3-6: “**P4. Law.** The system provides no path for changing, past the declaration, anything that must be recorded.” S2.3-7 explicitly includes privileged built-in tools.
Mapping — S2.1-1–2 designate `config.scm` with its computed imports/defaults; `guix system reconfigure /etc/config.scm` applies it (S2.1-5), with successful completion/status 0 as the report (S3-3).
Tool — [useradd(8)](https://raw.githubusercontent.com/shadow-maint/shadow/master/man/useradd.8.xml): “create a new user or update default new user information”. Its purpose is account management, making it built-in by S3-6; G3 and G5 establish Guix integration. S3-7 does not exclude it, and S3-8 does not leave it undecided.
Facts — [Guix 1.5.0 User Accounts](https://guix.gnu.org/manual/1.5.0/en/html_node/User-Accounts.html) documents “account or group creations or modifications made by directly invoking commands such as useradd”. They are undone by later application/reboot, rather than being additions to the declaration. Accounts must be recorded (S2.2-15).
Record — G3, T1 and G5 in [SOURCES.md](SOURCES.md) establish this path without an experiment; failed clean-clone transport is separately recorded and supplies no property evidence. G4 also documents per-user package operations, but that additional path is unnecessary to the decision.
Decision — **does not have**. Guix provides a documented account-management path past its designated operating-system description. Its privileged execution remains built-in and is excluded from breaking by S2.1-7; restoring state at a later application does not remove this path.
