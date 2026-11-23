## NixOS and GNU Guix System

The task expressly retains the previous installation recipes when releases match.
Both match: NixOS 26.05.14979.94c3211b0ee8 and Guix 1.5.0. Copies of their
previous verified images and clean installations are used. Their original
host-authored declarations are retained under `install/nixos/` and `install/guix/`.
Access declarations add the laboratory key, SSH and passwordless administrative
execution; these additions belong to the instrument.

NixOS official manual, https://nixos.org/manual/nixos/stable/:
“The minimal images will boot to a command line.” Manual installation requires
the supplied declaration. No desktop is chosen in the preserved recipe.

Guix manual source, https://codeberg.org/guix/guix/raw/tag/v1.5.0/doc/guix.texi,
section `operating-system` Reference, describes `sudoers-file`; OpenSSH service
reference describes `authorized-keys`. The preserved manual declaration supplies
the explicit base-services choice, rather than asserting a graphical installer default.
