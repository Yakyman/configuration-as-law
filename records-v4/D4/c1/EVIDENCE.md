# Evidence and method

Assessment c1, 2026-11-23 UTC. C1/C2/C4 in the task correspond to P1/P2/P4 in S8.3-4–8. The decisions concern the systems, using the committed declarations; they do not claim that every possible configuration behaves identically. One documented ordinary path suffices for a negative decision.

## Input boundary

(not published: orchestration or scratch) identifies commit `3e0207b104f9718793c5b2678810936c7c3c14d2`, timestamp `2026-11-23T11:10:54Z`. The assessment accepts that gate as the supplied commitment record; this workspace does not expose a Git repository (`raw/inputs-commit.txt`). `raw/inputs-sha256.txt` identifies the allowed inputs read. No other assessment, prior-night directory, or previous assessment repository was read. References from the installation recipes into those directories were not followed.

NixOS input: `check-inputs-v4/install/recipes/nixos/configuration.nix.in`, with its hardware import and the successful access application described by `README.md.in` and `access.sh.in`. The explicit account `user` has `extraGroups = [ "wheel" ];`. The access script ends with `nixos-rebuild switch`; its recorded exit status in the supplied README is 0. The declaration is the designated configuration and its imports, not generated `/etc/passwd`, `/etc/group`, a profile manifest, or the whole package catalogue.

Guix input: `check-inputs-v4/install/recipes/guix/original-config.scm.in`, `original-install.sh.in`, and the active `KIT2.md.in`. The `user-account` named `user` has `(supplementary-groups '("wheel" "netdev"))`. The initial recipe applies the declaration with `guix system init` and boots the installed system. The failed SSH configuration is not the declaration of this installation. The designated primary text is `/etc/config.scm` with the Scheme definitions it uses; runtime account databases and automatically generated profiles are not additional designated declarations.

The report-of-success mapping is normal successful command completion (exit 0), not merely building a derivation or creating a profile. For the initial Guix installation, the inputs supply the clean-installation provenance; this assessment does not invent an observed application exit status. The counterexamples are documented possible changes *after* completed application, not alleged failures during application.

## N-D: NixOS declaration and application

Official NixOS 26.05 manual, [Changing the Configuration](https://nixos.org/manual/nixos/stable/#sec-changing-config), captured in `raw/nixos-changing-the-configuration.txt`:

> The file /etc/nixos/configuration.nix contains the current configuration of your machine.

It directs the administrator to run `nixos-rebuild switch` after edits, to build, select the boot default, and realise the configuration in the running system. This maps the text and its application under S8.1-1–3,13–14. The input's successful switch supplies the relevant application; a build-only invocation would not.

## N-I: NixOS installer and packages

Official [Package Management](https://nixos.org/manual/nixos/stable/#sec-package-management), captured in `raw/nixos-package-management.txt`:

> With the command nix-env, you can install and uninstall packages from the command line.

The manual describes package selection, root and per-user profiles, and uninstallation. Thus `nix-env` is an installer and built-in tool (S8.1-4,7); its selected package/output is the installed unit (S8.1-6), with unchanged contents covered by S8.2-7–8,16. `nixos-rebuild` is also a built-in configuration tool; the declarative package list is realised through it. Per-user profile generation is not a designation of that generated file as primary declaration (S8.1-2–3). No package-installation counterexample is needed for these decisions.

## N-U: NixOS ordinary account changes

Official [User Management](https://nixos.org/manual/nixos/stable/#sec-user-management), captured in `raw/nixos-user-management.txt`:

> NixOS supports both declarative and imperative styles of user management.

> In the imperative style, users and groups are managed by commands such as useradd, groupmod and so on.

> Accounts can be modified using usermod.

The same section documents `userdel` and distinguishes declarative accounts in `configuration.nix` from these imperative commands. The option documentation in the [selected release's users module](https://github.com/NixOS/nixpkgs/blob/94c3211b0ee8/nixos/modules/config/users-groups.nix), captured in `raw/nixos-users-options.txt`, sets `users.mutableUsers`' default to `true` and says:

> If set to `true`, you are free to add new users and groups to the system with the ordinary `useradd` and `groupadd` commands.

It describes merging the existing account databases at activation, not rewriting the primary Nix declaration. The committed top-level declaration does not select immutable accounts. The same source describes `extraGroups` as “The user's auxiliary groups.” These sources establish an ordinary account-management route supplied by NixOS, irrespective of whether one can configure a more restrictive variant.

## G-D: Guix declaration, application, installer, packages

Official release [Guix 1.5.0 reference manual source](https://codeberg.org/guix/guix/src/tag/v1.5.0/doc/guix.texi), nodes “Using the Configuration System”, “Invoking guix system”, and “Invoking guix package”; relevant source excerpts and full-source digest are in `raw/guix-manual-excerpts.txt`. The HTML manual endpoints returned HTTP 403; the release's official source was retrieved directly instead.

> The configuration is declarative.

The manual identifies a Scheme `operating-system` expression supplied in a file to `guix system`, specifies `init` as installing that configuration and `reconfigure` as building, activating and switching to it. This maps S8.1-1–3,13–14; normal completed activation/boot following `init`, or successful `reconfigure`, is application. Merely creating a derivation is not application.

> The @command{guix package} command is the tool that allows users to
> install, upgrade, and remove packages, as well as rolling back to
> previous configurations.

This exact source quotation retains Texinfo markup. `guix package` (including `install`/`remove` aliases) is an installer and built-in tool under S8.1-4,7, its selected package/output the unit under S8.1-6. The manual distinguishes user profiles from the operating-system package list. `guix system` is the built-in system-configuration tool. An automatically constructed profile is not a newly designated primary description under S8.1-2–3.

## G-U: Guix ordinary account changes

Same official release manual, node [User Accounts](https://guix.gnu.org/manual/en/html_node/User-Accounts.html), release-source excerpt in `raw/guix-manual-excerpts.txt`:

> When booting or upon completion of @command{guix system reconfigure},
> the system ensures that only the user accounts and groups specified in
> the @code{operating-system} declaration exist, and with the specified
> properties. Thus, account or group creations or modifications made by
> directly invoking commands such as @command{useradd} are lost upon
> reconfiguration or reboot.

The quotation joins the source sentence spacing but preserves its words and markup. The manual expressly recognises interim account/group changes and subsequent restoration. Restoration is evidence that those commands do not amend the designated declaration. It does not establish continuous conformity in the interval before reboot/reconfiguration. Its `supplementary-groups` field documentation says:

> Optionally, this can be defined as a list of group names that this
> account belongs to.

The official [1.5.0 system source](https://codeberg.org/guix/guix/src/tag/v1.5.0/gnu/system.scm) includes `shadow` in `%base-packages-utils` and that list in `%base-packages` (`raw/guix-base-packages.txt`). The [package definition](https://codeberg.org/guix/guix/src/tag/v1.5.0/gnu/packages/admin.scm) fixes Shadow 4.13 and describes its authentication and account-management tools (`raw/guix-shadow-package.txt`). This establishes that the account tools are supplied by the system, not added by an experiment.

## U-M: Account-tool semantics

Official Shadow usermod(8), [version 4.13](https://github.com/shadow-maint/shadow/blob/4.13/man/usermod.8.xml) for Guix and [version 4.19.4](https://github.com/shadow-maint/shadow/blob/4.19.4/man/usermod.8.xml) for NixOS, `DESCRIPTION` and `-G`, captured in `raw/shadow-4.13-usermod.txt` and `raw/shadow-4.19.4-usermod.txt`:

> The usermod command modifies the system account files.

> If the user is currently a member of a group which is not listed, the user will be removed from the group.

The latter is the documented `-G` operation without `-a`. These match the release package definitions: Guix 1.5.0 uses 4.13; the [selected NixOS release package definition](https://github.com/NixOS/nixpkgs/blob/94c3211b0ee8/pkgs/by-name/sh/shadow/package.nix) uses 4.19.4 (`raw/nixos-shadow-package.txt`). The NixOS manual independently documents `usermod` for account modification. Removing a declared auxiliary group is a concrete instance. An illustrative command is `usermod -G netdev user` on Guix (that group is already explicitly in the input); on NixOS the same documented operation replaces the auxiliary-group list with a list omitting `wheel`. These are documentation witnesses, not commands executed in this assessment; both omit `wheel`. No additional account or changed declaration is needed.

## Definition mapping and exclusion

An administrator-chosen new account or changed group membership is not an unchanged package component (S8.2-7), nor executable code (S8.2-9). It is an account/rights setting under S8.2-11–13 and must be recorded by S8.2-1,17. A manually chosen extra account is not a default created during installation, not generated by a line naming that account, and not supplied by a declared external account list (S8.2-17–18). Recording the account-management package does not record every later choice made through it.

Account existence and group-membership values give the in-force tests under S8.1-10–12. Commands typed by a person are actions under S8.2-4; the resulting account or membership is the assessed object. Shells, editors, copying and link-creation programs are excluded from built-in tools by S8.1-8; the shell does not change the classification of a documented `useradd` or `usermod` operation. The examples use those programs' account-management purpose, hence S8.1-7 applies.

Direct privileged editing/deletion of account files or disabling protective mechanisms outside the built-in tools would be breaking (S8.1-15–16), excluded from all decisions. Privilege alone does not make a built-in account operation breaking. There is no definition-mapping counterexample required to decide these six cases.

## Experimental discipline and laboratory record

All property facts above are established by official documentation, supplemented by official release source for package inclusion/defaults. No unresolved property fact required an experiment; no property-changing guest command was run. In particular, there is no claimed runtime observation of account creation or group removal, no reapplication trial, and no inference of continuous guarantee from a successful switch alone.

The runner's remote SHA256 matched the committed input (`raw/runner-check-fallback.txt`). The default SSH invocation failed before contacting the server; explicitly selecting the existing user SSH configuration succeeded without changing system files (`raw/runner-check.txt`). The supplied `lab.sh` creates durable, slot-locked VM services; no separate VM or altered runner was used.

NixOS: `lab.sh new d4c1-nixos nixos` returned 0; `lab.sh destroy d4c1-nixos` returned 0 (`raw/nixos-new.txt`, `raw/nixos-destroy.txt`). Guix: `lab.sh new d4c1-guix guix` returned 1 with a boot/login timeout (`raw/guix-new.txt`); no property observation was obtained from that clone. The first `destroy` returned 1 after shutdown timed out (`raw/guix-destroy.txt`); the documented fallback `kill` returned 0 and the second `destroy` returned 0 (`raw/guix-kill.txt`, `raw/guix-destroy-2.txt`). `raw/cleanup.txt` confirms both named disposable VM directories are absent. The transport failure does not turn documented system facts into unknown facts: Appendix A.4.5 accepts a source **or** a record. It does limit the claim: this is a documentation-based assessment, with a successful NixOS clone launch and an unsuccessful Guix clone launch, not six live demonstrations.

The dated raw lifecycle records are retained. Source downloads were temporary parsing inputs; the cited relevant excerpts, source URLs and release identities are retained rather than unrelated manual chapters. External adjudication/review remains separate; this assessment does not accept its own results on behalf of that role.
