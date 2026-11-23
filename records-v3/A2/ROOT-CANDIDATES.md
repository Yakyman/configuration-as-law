# Additional candidates for adversarial review

Exploratory attack beyond the published plan. These are candidates, not accepted cards.

## R1. A package name does not say which objects count as recorded

Type: TERM. Concrete case: a pinned package contains a sysusers.d file that creates an account. The declaration records the package but does not separately mention that account. Primary source: https://www.freedesktop.org/software/systemd/man/latest/sysusers.d.html — “Packages should install their configuration files in /usr/lib/sysusers.d.” The same document describes account creation at package installation or boot time and automatic UID allocation.

Relevant sentences: S2.1-1, S2.1-4, S2.2-15, S2.3-4, S3-9, S2.4-4. The account is mandatory; the question is whether the package reference records it indirectly and whether the package line covers it after an explicit account line is removed. S3-9 fixes installed content, not the recording relation between a package and objects produced by its contents. Strongest objection: S2.5-3 allows a computing declaration, so ordinary evaluation can yield an account. Reply: this case is a package list, not an algorithm receiving computer state; allowing forms does not specify which package effects count as recorded. Review must decide if ordinary meaning of a primary description plus required state already disposes of this.

## R2. In-force tests stop before shared settings

Type: MISSING. Concrete case: the non-UTC system-wide timezone selected by /etc/localtime is used by several applications. Primary source: https://www.freedesktop.org/software/systemd/man/248/localtime.html — “The /etc/localtime file configures the system-wide timezone of the local system”. The document also specifies the UTC fallback when the file is absent.

Relevant sentences: S2.2-1, S2.2-2, S2.2-7, S2.1-3, S2.1-4, S2.3-4. The shared timezone affects behavior and is not a setting confined to one program. It is not among the categories with a stated in-force test. For an omitted object P1 needs that test before an object's declaration line can supply it. Strongest objection: S2.1-3 says a rule is applied; a timezone might be called a rule. Reply: the text neither defines rule nor says all shared settings are rules. This may merge with the missing unambiguity branch if the underlying gap is the same undefined breadth of rule.

## R3. A remote account is usable locally without existing locally

Type: TERM. Concrete case: an SSSD client authenticates an account from an external directory without creating a local account. Primary source: https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/pdf/system-level_authentication_guide/Red_Hat_Enterprise_Linux-7-System-Level_Authentication_Guide-en-US.pdf — “SSSD does not create user accounts on the local system.” The same source says the external identities allow local access. Supporting primary documentation: https://sssd.io/docs/introduction.html.

Relevant sentences: S2.1-1, S2.1-3, S2.2-15, S2.3-4, S2.4-1. The account exists in the directory and is usable on the client; the text does not delimit where an account must exist for it to be in force on the computer. The question is scope of existence, not how to transfer/cache data or how to grant authority. Strongest objection: S2.2-15 unconditionally requires accounts, so simply record it. Reply: that resolves mandatory type, but not which directory accounts are in force on this computer for P1 (all existing, resolvable, authorized, or locally materialized). Review should reject if ordinary account existence plus on-the-computer is sufficient.

## R4. An interface can permit selected effects outside its program

Type: TERM. Concrete case: an in-process Wasmtime guest is given access to one host directory through WASI but not the host's other files. Primary source: https://docs.wasmtime.dev/security.html — “applications can only access files and directories they've been given access to.” The same page says all external interaction occurs through linked interfaces and there is no raw system-call access.

Relevant sentences: S2.2-1, S2.2-10, S2.2-11, S2.2-12. The guest lacks the host's full rights yet can change host files through an API. The text gives no criterion whether confinement to its own interface means API mediation, restricted authority, or effects remaining within the application. Strongest objection: S2.2-11's VM example already permits virtual disks and external I/O; WASI clearly fits mediated interface. Reply for review: if any mediated restricted API suffices, is that rule already in the words or an added definition? Reject if the literal confinement condition unambiguously fits. This is ordinary code classified by its rights, not a file misread as data or a launch-channel feasibility issue.

## R5. Virtual firmware fits both the guest and firmware sentences

Type: COLLISION or TERM pending review. Concrete case: an OVMF image selected as guest firmware by libvirt runs within QEMU and can be replaced through its host loader configuration. Primary source: https://libvirt.org/formatdomain.html — “Booting via a guest firmware is available for hypervisors supporting full virtualization.” The document specifies a loader path and pflash type. QEMU boot-order documentation: https://www.qemu.org/docs/master/system/bootindex.html.

Relevant sentences: S2.2-11, S2.2-12, S2.2-16. Confined guest firmware is code in a virtual machine, while firmware is expressly mandatory wherever the system can change it. Strongest objection: S2.2-16 means firmware of physical devices on the assessed computer, not firmware of a guest. Reply: neither physical devices nor that scope restriction appears in the sentence. Do not retain as an independent card if this is just an instance of a wider computer/device boundary already recorded.

## Rejected leads

- A program failing after application is not a definition contradiction: P2 can simply fail, and implementations can refuse unsatisfiable declarations.
- General behavior-versus-log, content, or password exceptions are not automatically collisions: the exemption heading is a textual priority clue.
- Redundant objects do not alone refute removal: S2.2-2 is a sufficient test, while S2.2-1 can still apply.
- Removing a live file but leaving mapped pages does not establish unavoidable Removal failure: implementations may stop the process before reporting success.
- Different installed permissions under identical archive bytes collide with Section 4's comparison only after additional assumptions; that is not a direct contradiction between Sections 2 and 3.

## R6. A login key can be present but require confirmation each time

Type: TERM. Concrete case: an SSH key identity has been loaded into a reachable ssh-agent with the per-use confirmation constraint, and no authentication request is currently being approved. Primary source: https://man.openbsd.org/ssh-add — “Indicates that added identities should be subject to confirmation before being used for authentication.” The manual distinguishes listing represented identities, locking the agent, testing usability, and approving use.

Relevant sentences: S2.1-3, S2.1-4, S2.2-15, S2.3-4. A key is expressly mandatory, but in force depends on being available to the using program. The text does not say whether present and requestable counts as available while the required confirmation is still absent, or whether successful current use is necessary. The issue is classification of an existing mandatory credential, not how to protect the secret or which authority a user should possess. Strongest objection: S2.1-3's ordinary available means accessible subject to normal authorization; S2.5-1 excludes secrets and user authority. Reply for review: authority/protection policy is held fixed, yet the time at which its key becomes in force still changes P1's verdict; recording its required state under S2.1-4 cannot decide the status of an omitted key. Reject if ordinary availability alone decisively includes this known case.
