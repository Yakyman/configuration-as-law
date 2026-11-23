# Documentation quotes used by assessment c2 (fetched 2026-11-22 UTC)

Quotes are verbatim from the pages as fetched (HTML tags stripped).

## NixOS (manual "Version 26.05", https://nixos.org/manual/nixos/stable/)

D-N1 — Changing the Configuration: "The file /etc/nixos/configuration.nix contains the current configuration of your
machine. Whenever you’ve changed something in that file, you should do # nixos-rebuild switch to build the new
configuration, make it the default configuration for booting, and try to realise the configuration in the running
system (e.g., by restarting system services)."

D-N2 — Package Management: "NixOS has two distinct styles of package management: Declarative, where you declare what
packages you want in your configuration.nix. Every time you run nixos-rebuild, NixOS will ensure that you get a
consistent set of binaries corresponding to your specification. Ad hoc, where you install, upgrade and uninstall
packages via the nix-env command. This style allows mixing packages from different Nixpkgs versions. It’s the only
choice for non-root users."

D-N3 — Ad-Hoc Package Management: "With the command nix-env, you can install and uninstall packages from the command
line. For instance, to install Mozilla Thunderbird: $ nix-env -iA nixos.thunderbird If you invoke this as root, the
package is installed in the Nix profile /nix/var/nix/profiles/default and visible to all users of the system;
otherwise, the package ends up in /nix/var/nix/profiles/per-user/username/profile and is not visible to other users."
… "Other packages in the profile are not affected; this is the crucial difference with the declarative style of
package management, where running nixos-rebuild switch causes all packages to be updated to their current versions in
the NixOS channel."

D-N4 — User Management: "NixOS supports both declarative and imperative styles of user management. In the declarative
style, users are specified in configuration.nix." … "In the imperative style, users and groups are managed by commands
such as useradd, groupmod and so on. For instance, to create a user account named alice: # useradd -m alice" … "A user
can be deleted using userdel: # userdel -r alice" … "Accounts can be modified using usermod. Unix groups can be managed
using groupadd, groupmod and groupdel." … "If you set users.mutableUsers to false, then the contents of /etc/passwd
and /etc/group will be congruent to your NixOS configuration. … Also, imperative commands for managing users and
groups, such as useradd, are no longer available."

D-N5 — Options, https://nixos.org/manual/nixos/stable/options , `users.mutableUsers`: "If set to true, you are free to
add new users and groups to the system with the ordinary useradd and groupadd commands. On system activation, the
existing contents of the /etc/passwd and /etc/group files will be merged with the contents generated from the
users.users and users.groups options. The initial password for a user will be set according to users.users, but
existing passwords will not be changed." … "Type: boolean Default:true"

D-N6 — What happens during a system switch?: "nixos-rebuild, like many deployment solutions, calls
switch-to-configuration … After calculating what should be done, the actions are carried out. … Inspect what changed
during these actions and print units that failed and that were newly started".

## Nix (reference manual 2.34.9, https://nix.dev/manual/nix/stable/)

D-X1 — command-ref/nix-env.html: "nix-env - manipulate or query Nix user environments".
D-X2 — command-ref/nix-shell.html: "nix-shell - start an interactive shell based on a Nix expression" … "The command
nix-shell will build the dependencies of the specified derivation, but not the derivation itself. It will then start an
interactive shell in which all environment variables defined by the derivation path have been set to their
corresponding values"; synopsis includes "{--packages | -p} {packages | expressions}".

## Shadow and systemd man pages

D-M1 — https://man7.org/linux/man-pages/man8/useradd.8.html: "useradd - create a new user or update default new user
information".
D-M2 — https://man7.org/linux/man-pages/man8/userdel.8.html: "userdel - delete a user account and related files" …
"The userdel command modifies the system account files, deleting all entries that refer to the user name LOGIN."
D-M3 — https://man7.org/linux/man-pages/man1/gpasswd.1.html: "gpasswd - administer /etc/group and /etc/gshadow" …
"The gpasswd command is used to administer /etc/group, and /etc/gshadow. Every group can have administrators, members
and a password."
D-M4 — https://www.freedesktop.org/software/systemd/man/latest/systemctl.html: "systemctl — Control the systemd system
and service manager".

## GNU Guix (manual 1.5.0, https://guix.gnu.org/manual/1.5.0/en/html_node/)

D-G1 — Invoking-guix-system.html, `reconfigure`: "Build the operating system described in file, activate it, and
switch to it." … "This effects all the configuration specified in file: user accounts, system services, global package
list, privileged programs, etc. The command starts system services specified in file that are not currently running;
if a service is currently running this command will arrange for it to be upgraded the next time it is stopped".

D-G2 — Invoking-guix-package.html: "The guix package command is the tool that allows users to install, upgrade, and
remove packages, as well as rolling back to previous configurations. These operations work on a user profile—a
directory of installed packages. Each user has a default profile in $HOME/.guix-profile. The command operates only on
the user’s own profile, and works with normal user privileges" … "guix install is an alias for guix package -i".

D-G3 — Features.html: "The guix package command is the central tool to manage packages (see Invoking guix package). It
operates on the per-user profiles, and can be used with normal user privileges."

D-G4 — Using-the-Configuration-System.html, Globally-Visible Packages: "The packages field lists packages that will be
globally visible on the system, for all user accounts—i.e., in every user’s PATH environment variable—in addition to
the per-user profiles (see Invoking guix package)."

D-G5 — User-Accounts.html (11.7): "User accounts and groups are entirely managed through the operating-system
declaration." … "When booting or upon completion of guix system reconfigure, the system ensures that only the user
accounts and groups specified in the operating-system declaration exist, and with the specified properties. Thus,
account or group creations or modifications made by directly invoking commands such as useradd are lost upon
reconfiguration or reboot. This ensures that the system remains exactly as declared."

D-G6 — Services.html: "On a running system, the herd command allows you to list the available services, show their
status, start and stop them, or do other specific operations" … "# herd stop nscd Service nscd has been stopped."

D-G7 — Base-Services.html, `agetty-configuration` `tty`: "This argument is optional, it will default to a reasonable
default serial port used by the kernel Linux." (used only for the instrument note).
