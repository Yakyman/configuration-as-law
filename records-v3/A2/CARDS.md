CARDS: 7

Exploratory attack beyond the published plan. Outcome: 0 for the retained textual counterexamples; this is not a result of a published machine check. Ordered by the breadth of real objects and routine use affected. Independent selection and rejected attacks are recorded in REVIEW.md.

## 1. Shared settings have no test for being in force

Type: MISSING

Case: A non-UTC system timezone is selected through /etc/localtime and used by several applications. Its removal changes time presentation to the documented UTC fallback. This is an effective shared setting, not accumulated application data.

Primary evidence: [systemd localtime documentation](https://www.freedesktop.org/software/systemd/man/248/localtime.html): “file configures the system-wide timezone of the local system”; “If /etc/localtime is missing, the default "UTC" timezone is used.”

Sentences involved:

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.1-3: “**In force**—for an object that must be recorded (Section 2.2): a program or code runs or can be started, a service is enabled, an account exists, a rule is applied, a saved network or a login key is available to the program that uses it, firmware or a boot order is set on the device.”
- S2.1-4: “For a recorded object, its line states the required state; whether a recorded program is running at a given moment does not matter unless its line requires it.”
- S2.3-4: “**P1. Completeness.** Everything that must be recorded under Section 2.2 and is in force on the computer is recorded.”

Why the text fails: The behavior rule requires the shared timezone setting, and the one-program exemption does not cover it. The in-force definition gives tests for programs, services, accounts, rules, networks, keys, firmware and boot order, but none for a shared setting as such. P1 needs an in-force decision even when the setting has been omitted from the declaration. The text never identifies all such settings as rules or supplies a general test for the remaining mandatory types.

Strongest objection and reply: S2.1-4 lets a recorded object’s line state its required state, and S2.1-3 could be invoked by calling the timezone a rule. The first cannot classify an omitted object, which has no line; the second requires an unstated inclusion of shared settings in the rule category. This is a missing applicability predicate, not a demand for a particular storage or state-management design.

Other objects in the same gap: System-wide locale selection; shared resolver settings; mounted-filesystem mappings; device settings outside the listed firmware category. Sources for these type families are indexed in SWEEP.tsv.

## 2. A setting can belong to one program and act outside it

Type: TERM

Case: Firefox handlers.json selects a separate application to open a downloaded PDF. Firefox interprets the preference as values; the selected application is another program whose own presence can already be recorded. The question is whether the preference itself must be recorded.

Primary evidence: [Firefox profile documentation](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data), Download actions: “these are the settings that tell Firefox to open a PDF file with Acrobat Reader when you click on it.”

Sentences involved:

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-9: “a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S3-1: “**Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.”
- S3-2: “If what the object does remains unknown, the case yields ?.”

Why the text fails: If inside one program refers to where the setting is interpreted and enforced, this preference is exempt. If it refers to the reach of the resulting action, launching another program puts the preference outside the exemption. The text gives no criterion for choosing between those boundaries. Documentation already establishes the action, so the unknown-function outcome does not answer the classification question.

Strongest objection and reply: S2.2-1 could decide MUST because the preference affects another program. But S2.2-7 exempts some behavior-affecting settings and does not state whether program ownership or downstream effects determine its boundary; even its home-page example can initiate external communication. S2.2-9 decides the external executable, a different object, and S2.2-13 confirms that the preference is a setting without deciding its scope.

Other objects in the same gap: Package repository and extraction preferences; log-delivery and rotation settings; virtual-machine resource and shared-directory settings. The corresponding HOLE rows in SWEEP.tsv are instances of this single boundary.

## 3. An executable cache is both optional and required

Type: COLLISION

Case: CPython imports a current .pyc module cache while the unchanged source remains available. Removing this compiled copy causes source recompilation and preserves the computation at additional loading cost; the cached module executes with the interpreter’s ordinary authority. The object is deliberately compiled code, not data repurposed as code.

Primary evidence: [Python module tutorial](https://docs.python.org/3/tutorial/modules.html#compiled-python-files): “To speed up loading modules, Python caches the compiled version of each module”. [Python import specification](https://docs.python.org/3/reference/import.html#cached-bytecode-invalidation): “Before Python loads cached bytecode from a .pyc file”; its Loaders section states: “Module loaders provide the critical function of loading: module execution.”

Sentences involved:

- S2.2-3: “The following need not be recorded:”
- S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

Why the text fails: The same compiled file meets the semantic cache exemption and the explicit requirement for code executed with its interpreter’s rights. This is an overlap of two explicitly classified kinds, not just the general removal rule opposed to an exception. No sentence gives either classification priority for executable caches.

Strongest objection and reply: S2.2-13 is the closest priority rule: executed files count as code even when they hold settings. Its words address settings, not caches, so they establish the code classification without withdrawing the separate cache exemption. Recording the source or the cache voluntarily does not answer whether this object must be recorded.

Other objects in the same gap: Regenerable compiled Lisp caches; runtime-generated native-code caches executed with the runtime’s rights. These are the same code/cache overlap, not additional findings.

## 4. An editor can also be a package manager

Type: COLLISION

Case: GNU Emacs edits files and offers package-install to download and install Emacs Lisp packages. Those packages contain executable Lisp run by the editor, so this documented purpose includes changing code that must be recorded. No installation or privileged bypass was attempted.

Primary evidence: [GNU Emacs package installation manual](https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Installation.html): “then downloads and installs it.” The [GNU Emacs manual, Lisp Libraries](https://www.gnu.org/software/emacs/manual/pdf/emacs.pdf) says package-install “takes care of placing the package’s Lisp files in a directory where Emacs will find it”.

Sentences involved:

- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S3-6: “**Built-in tool.** A program of the system whose purpose, according to its documentation, includes changing what must be recorded: a package manager, including package managers of programming languages and of application packages; account and rights management; the service manager; network and firewall configuration.”
- S3-7: “General-purpose programs—an editor, file copying, link creation, the command shell—are not built-in tools: changing with them, through superuser privileges, what must be recorded is breaking.”
- S3-8: “If a program’s documentation does not state its purpose, the case yields ?; if it does and this indicator still does not decide whether the program is a built-in tool, the case is a counterexample to the definitions and yields 0.”
- S2.1-7: “**Breaking**—a change to what must be recorded, made past the declaration outside the built-in tools through the power of superuser privileges obtained by any means—in a full superuser session or through sudo: by writing directly to files, deleting, or disabling system mechanisms.”
- S2.3-7: “The built-in tools, including those executed with superuser privileges, change it only through the declaration: an installer does not install a program past the declaration but adds it to the declaration.”

Why the text fails: The documented-purpose test includes this program because it installs packages of executable code. The next sentence excludes an editor from built-in tools. Both classify programs, and neither gives priority when one program satisfies both descriptions. The conflict changes whether privileged changes are breaking or remain subject to P4.

Strongest objection and reply: S3-7 could be applied only when the editor edits, with S3-6 applied when it installs. Literally S3-7 classifies programs, while S3-6 asks whether their purpose includes the relevant activity; neither switches the classification unit to a command or invocation. S3-8 supplies a failure outcome for an undecided documented purpose, not a precedence rule.

Other objects in the same gap: Editors and development environments with integrated code-package managers; multi-call executables combining account-management tools with editors and shells. This is one mixed-purpose-program gap.

## 5. Boot-order lines have no unambiguity test

Type: MISSING

Case: A declaration sets firmware BootOrder to an ordered list of already existing boot entries. This changes a mandatory object without installing anything, creating an account or enabling a service. The line’s values are known; the missing item is the applicability of the Section 3 indicator.

Primary evidence: [efibootmgr primary documentation](https://github.com/rhboot/efibootmgr), --bootorder: “Explicitly set BootOrder (hex).” The documented independent operation establishes the concrete case.

Sentences involved:

- S2.2-16: “the boot order and device firmware must be recorded where the system is able to change them.”
- S2.1-3: “**In force**—for an object that must be recorded (Section 2.2): a program or code runs or can be started, a service is enabled, an account exists, a rule is applied, a saved network or a login key is available to the program that uses it, firmware or a boot order is set on the device.”
- S3-9: “**Unambiguous line.** A line that installs something is unambiguous when it states the version and the source so that the content to be installed is uniquely determined, for example by a checksum.”
- S3-10: “A line for an account, a service or a rule is unambiguous when every value of the object is either stated in the line or fixed by the system as a documented default.”
- S2.4-2: “**Reproducibility.** The same declaration on another computer yields exactly the result described in it, provided the description is unambiguous.”

Why the text fails: Boot order is explicitly mandatory where changeable. The unambiguity indicator covers installations and lines for accounts, services or rules. It provides no branch for this boot-order line, although Reproducibility depends on an unambiguous description. The same omission applies to mandatory non-installation object types not identified as one of those three classes.

Strongest objection and reply: S3-10 would apply if any prescribed setting were called a rule. S2.1-3 separately lists a rule and a boot order, and no sentence includes every non-installation object in the rule category. S2.5-3 permits different declaration forms; it does not expand this indicator’s object classes.

Other objects in the same gap: Saved-network selections and login-key selections that configure existing objects without installing content; their mandatory classes are explicit in S2.2-14 and S2.2-15. This is one omitted indicator branch, not one card per type.

## 6. A remote account has no clear boundary of local existence

Type: TERM

Case: An SSSD client retrieves identities from a remote directory and permits those identities to access the client without creating local user accounts. A directory can contain identities that are resolvable but not authorized on that client, as well as identities that are authorized but have never logged in.

Primary evidence: [System-Level Authentication Guide, section 7.1.1](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/pdf/system-level_authentication_guide/Red_Hat_Enterprise_Linux-7-System-Level_Authentication_Guide-en-US.pdf): “SSSD does not create user accounts on the local system.” [SSSD introduction, Access control](https://sssd.io/docs/introduction.html): “Specific users and, or groups can be authorized to access the host”. These sources distinguish stored identity, retrieval and local authorization.

Sentences involved:

- S2.1-1: “**Declaration**—a collection of files that a person has designated as the primary description of the computer.”
- S2.1-3: “**In force**—for an object that must be recorded (Section 2.2): a program or code runs or can be started, a service is enabled, an account exists, a rule is applied, a saved network or a login key is available to the program that uses it, firmware or a boot order is set on the device.”
- S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”
- S2.3-4: “**P1. Completeness.** Everything that must be recorded under Section 2.2 and is in force on the computer is recorded.”
- S2.4-1: “**Understanding.** If there was no breaking, what is in force on the computer can be read from the declaration alone, without inspecting the computer.”

Why the text fails: Accounts are explicitly mandatory, but their in-force test says only that an account exists. The text does not say whether existence in a remote directory, local resolvability, local authorization or local materialization makes that account in force on this computer. Those tests select different sets of accounts for P1. Knowing the directory and client behavior therefore does not supply the missing scope criterion.

Strongest objection and reply: S2.2-15 clearly says accounts must be recorded. That fixes the object class but not which externally stored accounts are in force on the assessed computer, the further condition imposed by S2.3-4. S2.5-1 leaves the design of user authority and state handling free; the case holds those policies fixed and asks which existing identities the definition counts.

Other objects in the same gap: Directory-backed NSS identities; domain accounts used for local login; centrally managed identities exposed to several clients. These are the same remote-existence boundary.

## 7. A key awaiting confirmation has no clear availability test

Type: TERM

Case: An SSH identity is loaded into a reachable ssh-agent with per-use confirmation enabled. The program can request a signature, but authentication cannot use the key until confirmation succeeds; no request is currently being approved. Its location and authorization policy are fully known.

Primary evidence: [OpenSSH ssh-add manual, -c](https://man.openbsd.org/ssh-add): “Indicates that added identities should be subject to confirmation before being used for authentication.” The manual separately documents listing represented identities, confirmation, locking and testing usability.

Sentences involved:

- S2.1-3: “**In force**—for an object that must be recorded (Section 2.2): a program or code runs or can be started, a service is enabled, an account exists, a rule is applied, a saved network or a login key is available to the program that uses it, firmware or a boot order is set on the device.”
- S2.1-4: “For a recorded object, its line states the required state; whether a recorded program is running at a given moment does not matter unless its line requires it.”
- S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”
- S2.3-4: “**P1. Completeness.** Everything that must be recorded under Section 2.2 and is in force on the computer is recorded.”
- S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”

Why the text fails: The login key is a mandatory type, but it is in force only when available to the program that uses it. Present and requestable, usable after a further authorization event, and usable immediately are different states of this real key. The text does not say which of them counts as available. An omitted key therefore has no determined P1 status during the interval before confirmation.

Strongest objection and reply: S2.5-1 leaves user authority and secret protection to system design, and S2.1-3 might use available in the broad sense of requestable under the chosen policy. The case does not challenge that policy: it asks for the observable in-force classification after the policy is fixed. S2.1-4 cannot supply the missing criterion for an omitted object, because it applies to a recorded object’s line.

Other objects in the same gap: Keys in locked agents; token-backed keys awaiting touch or PIN; identities whose hardware token is temporarily absent. These are availability boundaries, not separate policies or findings.

