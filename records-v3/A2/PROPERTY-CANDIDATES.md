# Property and indicator candidates

This is an exploratory attack beyond the published plan. Recorded: 2026-11-22 04:39:07 UTC.
Candidate outcomes refer to the textual cases, not to a testbed or the published checks. Both await independent review.

## P-C1. An editor can also be a package manager

Type: COLLISION. Candidate outcome: 0.

Case: GNU Emacs is an editor whose documented package-install command downloads and installs packages inside that same application. Primary source: https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Installation.html — “This prompts for the name of a package with the ‘available’ status, then downloads and installs it.” No installation was attempted: the case is classification of the documented program itself, before deciding whether any action is breaking.

Sentences involved:
- S3-6: “**Built-in tool.** A program of the system whose purpose, according to its documentation, includes changing what must be recorded: a package manager, including package managers of programming languages and of application packages; account and rights management; the service manager; network and firewall configuration.”
- S3-7: “General-purpose programs—an editor, file copying, link creation, the command shell—are not built-in tools: changing with them, through superuser privileges, what must be recorded is breaking.”
- S3-8: “If a program’s documentation does not state its purpose, the case yields ?; if it does and this indicator still does not decide whether the program is a built-in tool, the case is a counterexample to the definitions and yields 0.”
- S2.1-7: “**Breaking**—a change to what must be recorded, made past the declaration outside the built-in tools through the power of superuser privileges obtained by any means—in a full superuser session or through sudo: by writing directly to files, deleting, or disabling system mechanisms.”
- S2.3-7: “The built-in tools, including those executed with superuser privileges, change it only through the declaration: an installer does not install a program past the declaration but adds it to the declaration.”

Why the text fails: The documentation gives the editor a purpose that includes installing packages, so the positive definition includes it. The next sentence excludes an editor from built-in tools. Neither sentence makes classification depend on which command inside a program is being used or gives precedence to one classification. This changes whether privileged changes are excluded as breaking or remain subject to P4.

Strongest objection: S3-7 explicitly names editors, so one could let that exclusion prevail, or classify only the package-install function as the tool. S3-6 says that a program whose purpose includes the relevant activity qualifies; it does not exclude editors or replace the unit of classification with a function. S3-8 supplies outcome 0 when documented purpose still leaves classification undecided, not a priority rule.

Other objects in the same gap: BusyBox builds combining account-management applets with shell, copying and editor applets; other editors with integrated package managers. BusyBox source and exact excerpts are in `raw/properties/SOURCES.md`, E3.

## P-C2. Boot-order lines have no unambiguity test

Type: MISSING. Candidate outcome: 0.

Case: A declaration line sets firmware BootOrder to an ordered list of existing boot entries, without installing anything. Primary source: https://github.com/rhboot/efibootmgr — “Explicitly set BootOrder (hex).” The documented `--bootorder` option establishes that this is a real independently changeable object.

Sentences involved:
- S2.2-16: “the boot order and device firmware must be recorded where the system is able to change them.”
- S2.1-3: “**In force**—for an object that must be recorded (Section 2.2): a program or code runs or can be started, a service is enabled, an account exists, a rule is applied, a saved network or a login key is available to the program that uses it, firmware or a boot order is set on the device.”
- S3-9: “**Unambiguous line.** A line that installs something is unambiguous when it states the version and the source so that the content to be installed is uniquely determined, for example by a checksum.”
- S3-10: “A line for an account, a service or a rule is unambiguous when every value of the object is either stated in the line or fixed by the system as a documented default.”
- S2.4-2: “**Reproducibility.** The same declaration on another computer yields exactly the result described in it, provided the description is unambiguous.”

Why the text fails: Boot order is explicitly required when changeable. The unambiguity indicator covers lines that install something and lines for accounts, services or rules. An ordered firmware selection is not identified as any of those classes, so the indicator supplies no test for this mandatory object's line. Reproducibility still depends on whether that description is unambiguous.

Strongest objection: One could call any prescribed setting a rule and apply S3-10. The text separately names boot order and rules in S2.1-3 and never says that every non-installation object is a rule, so that generalization adds a category inclusion. S2.5-3 permits any declaration form; it does not expand the indicator to additional object types. If independent review accepts the broad ordinary reading of rule, merge this with the undefined scope of rule rather than retain a separate card.

Other objects in the same gap: saved Wi-Fi profiles, login-key selections, device settings that configure existing objects without installing content. These are breadth examples for one missing indicator branch, not independent cards.
