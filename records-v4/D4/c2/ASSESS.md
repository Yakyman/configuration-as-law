# Check 4 — assessment c2 of NixOS and GNU Guix System

Inputs: (not published: orchestration or scratch) (commit 3e0207b1…, 2026-11-23T11:10:54Z) and `check-inputs-v4/inputs-check-4.md`. The laboratory runner has
SHA256 `3402697b…` (`lab.sh`), matching the committed inputs. Clean installations: `lab.sh new d4c2-nixos nixos`
(11:13:20–11:13:44Z, status 0, `raw/new-nixos.txt`) and `lab.sh new d4c2-guix guix` (11:13:44–11:17:42Z, status 0,
`raw/new-guix.txt`). Both were destroyed with status 0 (`raw/destroy-nixos.txt`, `raw/destroy-guix.txt`).
Releases observed: NixOS `26.05.14979.94c3211b0ee8 (Yarara)` (`raw/e-n2.out`) and `guix (GNU Guix) 1.5.0`
(`raw/e-g2.out`). Expected results were written before each run; see `EXPERIMENTS.md`.

The properties are P1, P2 and P4 of Section 8.3 (the task calls them C1, C2 and C4). The text reads them strictly. A
property counts as "has" only if nothing found shows a way of the kind it excludes. One established counterexample
gives "does not have".

## Documentation sources (quoted verbatim)

NixOS manual, stable, "Version 26.05", https://nixos.org/manual/nixos/stable/ :
- N-D1 (#sec-changing-config): "The file `/etc/nixos/configuration.nix` contains the current configuration of your machine."
- N-D2 (#sec-ad-hoc-packages): "With the command `nix-env`, you can install and uninstall packages from the command line."
  … "If you invoke this as root, the package is installed in the Nix profile `/nix/var/nix/profiles/default`" (the
  sentence continues: visible to all users). Also: "Other packages in the profile are _not_ affected; this is the crucial
  difference with the declarative style of package management".
- N-D3 (#sec-user-management): "In the imperative style, users and groups are managed by commands such as `useradd`,
  `groupmod` and so on."

Manual pages installed with the exact release (`raw/doc-nixos-local.out`, `raw/doc-nixos-local-2.out`):
- N-D4 nixos-rebuild(8), switch: "Build and activate the new configuration, and make it the boot default."
- N-D5 configuration.nix(5), `users.mutableUsers`: "If set to ‘true’, you are free to add new users and groups to the
  system with the ordinary ‘useradd’ and ‘groupadd’ commands. On system activation, the existing contents of the
  ‘/etc/passwd’ and ‘/etc/group’ files will be merged with the contents generated from the ‘users.users’ and
  ‘users.groups’ options. The initial password for a user will be set according to ‘users.users’, but existing
  passwords will not be changed." "Default: true". The installed declaration does not set this option
  (`check-inputs-v4/install/recipes/nixos/configuration.nix.in`).
- N-D6 configuration.nix(5), `environment.systemPackages`: "The set of packages that appear in /run/current-system/sw.
  … (The latter is the main difference with installing them in the default profile, /nix/var/nix/profiles/default."
- N-D7 configuration.nix(5), `users.users.<name>.initialPassword`: "Specifies the initial password for the user, i.e.
  the password assigned if the user does not already exist. If users.mutableUsers is true, the password can be changed
  subsequently using the passwd command."
- N-D8 nix-env(1): "nix-env - manipulate or query Nix user environments"; it lists `--install` and `--uninstall` as
  operations. nix-env --install(1): "nix-env --install - add packages to user environment".

GNU Guix Reference Manual, "Version 1.5.0", https://guix.gnu.org/manual/1.5.0/en/html_node/ (saved under `raw/docs-guix/`):
- G-D1 (Using-the-Configuration-System.html): "The packages field lists packages that will be globally visible on the
  system, for all user accounts—i.e., in every user’s PATH environment variable—in addition to the per-user profiles
  (see Invoking guix package)."
- G-D2 (Invoking-guix-package.html): "The guix package command is the tool that allows users to install, upgrade, and
  remove packages, as well as rolling back to previous configurations. These operations work on a user profile—a
  directory of installed packages." "Each user has a default profile in $HOME/.guix-profile." "guix install is an alias
  for guix package -i".
- G-D3 (User-Accounts.html): "User accounts and groups are entirely managed through the operating-system declaration."
  "When booting or upon completion of guix system reconfigure, the system ensures that only the user accounts and
  groups specified in the operating-system declaration exist, and with the specified properties." "Thus, account or
  group creations or modifications made by directly invoking commands such as useradd are lost upon reconfiguration or
  reboot." Field `password`: "You would normally leave this field to #f, initialize user passwords as root with the
  passwd command, and then let users change it with passwd. Passwords set with passwd are of course preserved across
  reboot and reconfiguration. If you do want to set an initial password for an account, then this field must contain
  the encrypted password, as a string."
- G-D4 (Invoking-guix-system.html): "reconfigure Build the operating system described in file, activate it, and switch
  to it". "This effects all the configuration specified in file: user accounts, system services, global package list,
  privileged programs, etc. The command starts system services specified in file that are not currently running; if a
  service is currently running this command will arrange for it to be upgraded the next time it is stopped". "init
  Populate the given directory with all the files necessary to run the operating system specified in file."

shadow-utils 4.19.0, gpasswd(1), https://man7.org/linux/man-pages/man1/gpasswd.1.html (`raw/docs-shadow/`):
- S-D1: "gpasswd - administer /etc/group and /etc/gshadow". "The gpasswd command is used to administer /etc/group, and
  /etc/gshadow. Every group can have administrators, members and a password." "-d, --delete user Remove the user from
  the named group."

## Mapping of notions (Section 8.1), shared by the cases of each system

NixOS:
- Declaration (S8.1-1–S8.1-3): `/etc/nixos/configuration.nix` with its import `./hardware-configuration.nix` (N-D1; the
  installation recipe designates these files). Profile manifests that `nix-env` writes are not a declaration: S8.1-2
  requires that the computer be brought into conformity with the text, "rather than the text being compiled from the
  computer".
- Installers (S8.1-4): `nix-env` (N-D2, N-D8: install and uninstall) and `nixos-rebuild`, which installs and removes the
  system's packages through the declaration. Packages (S8.1-6): store outputs that `nix-env` adds to or removes from a
  profile as a whole.
- Built-in tools (S8.1-7): `nix-env` and `nixos-rebuild` (installers); `useradd`, `groupmod` (N-D3, N-D5) and `gpasswd`
  (S-D1), for account and rights management; `systemctl`, the service manager. All four account programs are present
  on the installation (`raw/doc-nixos-local.out`).
- Application (S8.1-13) and its report of success (S8.1-14): `nixos-rebuild switch` (N-D4). Success is exit status 0
  with "Done. The new configuration is …" (`raw/e-n2.out`). At installation the application is `nixos-install`.
  `nixos-rebuild boot` and `test` were examined: when they take effect is placed outside the definition by S8.5 ("when
  an edit takes effect", "generations and rollback"), so they are not recorded as counterexamples.
- Breaking (S8.1-15): changes made with superuser power outside these tools, for example a direct write to
  `/etc/group` or the deletion of store paths.

Guix System:
- Declaration: the `operating-system` declaration `/etc/config.scm`, applied at installation by `guix system init`
  (G-D4; `raw/e-g2.out` shows that file). A user profile's manifest generated by `guix package` is excluded by S8.1-2,
  as on NixOS.
- Installers: `guix package` with its aliases `guix install` and `guix remove` (G-D2), and `guix system` through the
  declaration. Packages: store items that `guix package` installs into or removes from a profile as a whole.
- Built-in tools: `guix package` and `guix system`; `useradd` (G-D3) and `gpasswd` (S-D1;
  `/run/current-system/profile/bin/gpasswd`, `raw/e-g2.out`) for accounts and rights; `herd`, the service manager
  (G-D4).
- Application and report: `guix system reconfigure FILE` ("activate it, and switch to it", G-D4), with `guix system
  init` at installation; success is completion with exit status 0. Activation at boot re-establishes the declared
  accounts (G-D3).
- Breaking: as for NixOS.

No notion was found that the definitions cannot map, so no mapping counterexample is recorded.

## nixos × P1 Completeness

**Demand.** S8.3-4, with S8.3-1, S8.2-1, S8.2-7/8, S8.2-10, S8.2-13, S8.2-16 and S8.2-17. At any moment after a
completed application, with no breaking, every package or program on the machine and every setting in force must have
a line in `configuration.nix`. Accounts count as settings (S8.2-13); an account is in force when it exists (S8.1-11).

**Facts.** N-D2: `nix-env`, invoked as root, installs a package into `/nix/var/nix/profiles/default`, visible to all
users. N-D6 contrasts this with `environment.systemPackages`. N-D5: by default (`true`, not overridden in the
installation's declaration), accounts can be added with `useradd`, and activation merges them rather than removing
them.

**Decision: does not have.** A package that `nix-env -i` installs as root is a package on the computer (S8.2-7), so it
is in force (S8.1-9). No line of `configuration.nix` names it, and it was not built from a recorded line (S8.2-16).
The typed command is not a line of the declaration (S8.2-4). Using `nix-env` is not breaking, because it is a built-in
tool (S8.1-7, S8.1-15). An account added with `useradd` is a second, independent counterexample. Its existence is
established by N-D5; it is a setting in force (S8.1-11) without a line (S8.2-17). Either one is enough. No experiment
was needed, because the documentation establishes the fact.

## nixos × P2 Guarantee

**Demand.** S8.3-5 with S8.3-1, S8.1-10, S8.1-11, S8.1-12, S8.1-15 and S8.1-16. At any moment after a completed
application, with no breaking, each recorded line must be in force as it requires. The case uses the line
`users.users.user.extraGroups = [ "wheel" ];`, which requires the account to be a member of `wheel`; membership is a
right, so it is a setting (S8.2-13).

**Facts.** E-N2 (`raw/e-n2.sh`, `raw/e-n2.out`):
- `nixos-rebuild switch` returned status 0 with "Done. The new configuration is …", and `id -nG user` gave
  `users wheel`.
- `gpasswd -d user wheel` returned status 0; afterwards `id -nG user` gave `users`, while the declaration line was
  unchanged (count 1).
- A second `nixos-rebuild switch` returned status 0 and `users wheel` was restored.

N-D7 was examined: an `initialPassword` line requires only an initial password (S8.1-12), so it is not used as a
counterexample.

**Decision: does not have.** After a completed application, the built-in rights-management tool `gpasswd` (S-D1,
S8.1-7) took the recorded line out of force. This was not breaking, because S8.1-15 excludes changes made with built-in
tools. S8.3-1 covers "any moment after a completed application", and no word limits it to the moment right after the
application, so this moment counts. The state right after each application did satisfy the line (both `id` results
show `wheel`).

## nixos × P4 Law

**Demand.** S8.3-6, S8.3-7 and S8.3-8, with S8.1-4, S8.1-7 and S8.1-15. NixOS must provide no ordinary way to change
what is installed or settings past `configuration.nix`. Its installers and configuration tools, even when run as root,
must record changes in that file, so that a change past it is possible only by breaking.

**Facts.** N-D2: "With the command `nix-env`, you can install and uninstall packages from the command line"; run as
root, it installs into `/nix/var/nix/profiles/default`, and the manual sets this against "the declarative style". N-D8
describes `nix-env --install` as "add packages to user environment", that is, to a profile, not to the declaration.
N-D3 and N-D5 call `useradd`/`groupadd` the "ordinary" commands of the "imperative style", and the default is `true`.

**Decision: does not have.** `nix-env` is an installer (S8.1-4) and a built-in tool, documented as an ordinary way to
install. It installs past the declaration and writes nothing into `configuration.nix`. That contradicts S8.3-7 ("an
installer does not install a program past the declaration but adds it to the declaration") and S8.3-8. `useradd` is a
second example, for settings. Both are established by the documentation, so no experiment was needed.

## guix × P1 Completeness

**Demand.** S8.3-4 with S8.3-1, S8.2-1, S8.2-7/8, S8.2-10, S8.2-13, S8.2-16 and S8.2-17. At any moment after a
completed application, with no breaking, every package or program on the machine and every setting in force must have
a line in `/etc/config.scm`.

**Facts.** G-D1: the declaration's `packages` field is global "in addition to the per-user profiles". G-D2:
`guix package` (or `guix install`) installs packages into a user profile, `$HOME/.guix-profile`. G-D3: account changes
made with commands such as `useradd` remain in effect until the next reconfiguration or reboot ("are lost upon
reconfiguration or reboot").

**Decision: does not have.** A package installed with `guix install` is a package on the computer (S8.2-7), and its
programs can be started (S8.1-9). No line of `/etc/config.scm` records it, and it was not built from a recorded line
(S8.2-16). `guix package` is a built-in tool, so its use is not breaking (S8.1-15). Accounts created with `useradd`
between applications are a second counterexample (G-D3, S8.1-11). The documentation establishes the facts, so no
experiment was needed.

## guix × P2 Guarantee

**Demand.** S8.3-5 with S8.3-1, S8.1-10, S8.1-11, S8.1-12, S8.1-15 and S8.1-16. Here the recorded line is
`(supplementary-groups '("wheel" "netdev"))` of the account `user`, which requires membership of `wheel` and `netdev`.

**Facts.** E-G2 (`raw/e-g2.sh`, `raw/e-g2.out`). Version 1.5.0; `/etc/config.scm` line 20 holds the line above.
`id -nG user` gave `users wheel netdev`. `gpasswd -d user wheel` returned status 0, and afterwards gave `users netdev`.
Membership was then restored with `gpasswd -a`. G-D3 states the general rule: changes made with `useradd`-family
commands persist until reconfiguration or reboot. The completed application was the installation's `guix system init`
and the activation at boot; no reconfigure was run. The password line was examined (G-D3: "initial password") and is
not used as a counterexample (S8.1-12).

**Decision: does not have.** After a completed application, the built-in tool `gpasswd` took a recorded line out of
force without breaking (S8.1-7, S8.1-15). S8.3-1 covers "any moment after a completed application". G-D3 confirms such
states last until the next reconfiguration or reboot. The state right after activation satisfied the line, since the
first `id` result showed `wheel`.

## guix × P4 Law

**Demand.** S8.3-6, S8.3-7 and S8.3-8, with S8.1-4, S8.1-7 and S8.1-15. Guix must provide no ordinary way to change
what is installed or settings past `/etc/config.scm`. Its installers and configuration tools must add changes to that
file.

**Facts.** G-D2: "The guix package command is the tool that allows users to install, upgrade, and remove packages …
These operations work on a user profile", and `guix install` is an alias for `guix package -i`. G-D1 places per-user
profiles beside the declaration's `packages` field. G-D3 names `useradd`, whose changes take effect until
reconfiguration or reboot.

**Decision: does not have.** `guix package` is an installer (S8.1-4) and a built-in tool, documented as the ordinary
way to install. It installs into a profile, past the declaration, and writes nothing into `/etc/config.scm`. That
contradicts S8.3-7 and S8.3-8. `useradd` is a second example, for settings. The documentation establishes this, so no
experiment was needed.
