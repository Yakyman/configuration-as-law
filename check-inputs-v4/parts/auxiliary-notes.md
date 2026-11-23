## Fedora and Mint source paths

The supplied previous-laboratory `install/` directory contains only the NixOS
and Guix recipe directories. The clean Fedora and Mint backings are actually
`C1/base/fedora.qcow2` and `C1/base/mint.qcow2` in that laboratory, both mode 0444.
Those are the existing immutable images used as backing files; they are never
modified. A new overlay holds laboratory SSH access. These auxiliary machines
are outside the checks. Their access scripts are recorded separately.
