# Pair and term candidates — beyond the published plan

Attacker candidates, not independently accepted findings. Three candidates have proposed outcome 0 and one remains ?. Card count and combined outcome are assigned by integration and separate review.

## A regenerable executable cache is both optional and required

Type: COLLISION. Candidate outcome: 0.

Case: CPython loads the compiled module kept in __pycache__ while its unchanged source is also available. Deleting this compiled copy makes the interpreter recompile source and preserves the module's capabilities, at a loading cost. This is an ordinary documented executable cache, not a data file repurposed as code and not an installation-channel probe.

Primary sources: https://docs.python.org/3/tutorial/modules.html#compiled-python-files — “To speed up loading modules, Python caches the compiled version of each module”. https://docs.python.org/3/reference/import.html#loaders — “Module loaders provide the critical function of loading: module execution.”

Sentences:
- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

Why the text fails: The compiled file satisfies the cache exemption because source remains and reproduces the same computation. It also supplies executable Python module code with the interpreter's ordinary rights. The explicit code requirement and explicit cache exemption both classify the same object. No sentence states which wins for executable caches.

Strongest objection: S2.2-13 expressly prioritizes code over settings. Read literally, its priority concerns settings, not cache, so it does not remove the cache exemption; treating a source reference as also recording the compiled object raises the separate undefined recorded-object issue rather than supplying a priority rule.

Other objects in this gap: regenerable compiled Lisp caches; regenerable native-code caches for managed runtimes; generated executable build caches when actually executed with ordinary process authority. These analogues are breadth hints, not separately verified cases.

## A setting used by one program can also be a mandatory login rule

Type: TERM. Candidate outcome: 0.

Case: OpenSSH's PasswordAuthentication option is a keyword/value setting interpreted by sshd, and controls whether that program accepts password login. It does not set the password-login policy of other independent login programs.

Primary source: https://man.openbsd.org/sshd_config — “Specifies whether password authentication is allowed.” The same manual describes sshd reading its configuration as keyword/argument pairs.

Sentences:
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”

Why the text fails: S2.2-15 expressly requires the password-login permission rule. S2.2-7 exempts settings in force only inside one program, and this value governs sshd. The text does not say whether inside refers to which program evaluates the value or to every downstream effect of a successful login. Those readings decide this same setting differently.

Strongest objection: S2.2-15 names this rule explicitly, and could be read as overriding S2.2-7. It does not say that mandatory rules are excluded from one-program settings, while S2.2-13 positively classifies read-only values as settings; the text supplies no meaning of inside that selects the intended category. If an adjudicator finds the explicit enumeration decisive as a priority rule, reject the collision reading but retain the scope question only if another concrete case survives.

Other objects in this gap: sshd AllowUsers and forwarding controls; a Wi-Fi profile consumed by one supplicant; application-level authentication permissions. These share the program-scope boundary rather than creating separate cards.

## An editor is also a documented package manager

Type: COLLISION. Candidate outcome: 0.

Case: GNU Emacs edits files and includes package-install, which downloads and installs packages. The distinction changes whether a superuser change through this same program is breaking or a built-in-tool action subject to P4; no channel-closure claim is needed.

Primary source: https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Installation.html — “then downloads and installs it.” The documented command is M-x package-install.

Sentences:
- S3-6: “**Built-in tool.** A program of the system whose purpose, according to its documentation, includes changing what must be recorded: a package manager, including package managers of programming languages and of application packages; account and rights management; the service manager; network and firewall configuration.”
- S3-7: “General-purpose programs—an editor, file copying, link creation, the command shell—are not built-in tools: changing with them, through superuser privileges, what must be recorded is breaking.”
- S3-8: “If a program’s documentation does not state its purpose, the case yields ?; if it does and this indicator still does not decide whether the program is a built-in tool, the case is a counterexample to the definitions and yields 0.”
- S2.1-7: “**Breaking**—a change to what must be recorded, made past the declaration outside the built-in tools through the power of superuser privileges obtained by any means—in a full superuser session or through sudo: by writing directly to files, deleting, or disabling system mechanisms.”

Why the text fails: The inclusive documented-purpose test identifies a package manager as built-in. The explicit editor sentence says an editor is not built-in. Emacs satisfies both descriptions. Neither sentence says which category prevails for a program with both documented purposes.

Strongest objection: S3-7 may be read as applying only when Emacs edits rather than installs. Literally it classifies general-purpose programs, not invocations or subcommands, and S3-6 also classifies a program by included purposes; invocation-level classification would add a rule.

Other objects in this gap: development environments containing extension package managers; command shells containing documented module-package management. The editor example alone supports the card.

## Guest firmware crosses the guest exemption and the device rule

Type: TERM. Candidate outcome: ? pending independent selection.

Case: libvirt selects a guest firmware loader with a pflash backing image, and QEMU exposes bootindex to control guest device boot order. The firmware is guest-executed code and controls virtual rather than physical host devices.

Primary sources: https://libvirt.org/formatdomain.html#guest-firmware documents loader selection and pflash guest firmware. https://www.qemu.org/docs/master/system/bootindex.html — “The `bootindex` properties are used to determine the order in which firmware will consider devices for booting the guest OS.”

Sentences:
- S2.2-11: “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.”
- S2.2-16: “the boot order and device firmware must be recorded where the system is able to change them.”
- S2.1-3: “**In force**—for an object that must be recorded (Section 2.2): a program or code runs or can be started, a service is enabled, an account exists, a rule is applied, a saved network or a login key is available to the program that uses it, firmware or a boot order is set on the device.”

Why the text may fail: S2.2-11 exempts guest code. S2.2-16 requires firmware and boot order that the system can change, without restricting device to physical host hardware. A guest firmware image may satisfy both unless device is given an unstated physical-only boundary. The evidence establishes the overlap in terminology, not that the host and guest are one computer.

Strongest objection: S2.2-11 expressly exempts a guest system, so it may already decide every guest-owned object; S2.2-16 may be understood as host devices only. Neither scope restriction is explicit, but the guest exemption is a substantial refutation. Keep as a term-boundary candidate only; do not automatically promote it as a collision.

Other objects in this gap: guest option ROMs; virtual TPM firmware; guest boot-device priority.

## Rejected attacks

- General removal rule versus an ordinary log, photograph or browser theme: the explicit exemption already supplies the answer.
- Fail2Ban log versus firewall rule: different objects, so no direct opposite-decision pair.
- Editor configuration as both setting and code: S2.2-13 explicitly handles settings executed as code; do not duplicate the separately assigned data-as-code task.
- Guest page versus renderer process: distinguish the page from the host executable before claiming a collision.
- Every dynamic state change as a law violation: S2.5 excludes treatment of program state and data from definition; require a separately explicit mandatory object before promoting.
