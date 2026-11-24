# Beyond-plan property candidates

This examination does not assign a published-check outcome or a weight. PROPERTIES.tsv records all fifteen pairs among the three properties and three consequences, plus ten qualifier and grouped checks. Consequence identifiers are local and mapped in consequence_ids.md. Primary passages are recorded in property_sources.md.

## C-PROP-1 — A package line does not reveal the identity its installer generates

Type: CONFLICT (coverage versus the asserted Understanding consequence; not an impossibility proof for every implementation).

Case: The openssh-server package's configure script generates the server's default Ed25519 host key when it is absent. Its post-installation source invokes ssh-keygen with no preselected key value (PS1); the service uses the host key as its own identity parameter (PS2); the key-generation implementation fills its seed with random bytes (PS3). Thus ordinary installation can yield a concrete configured service identity that a package-only declaration does not contain. This is not a client private key used to log in to another machine, nor a request to specify how secrets must be protected.

Sources and exact passages:

- https://sources.debian.org/src/openssh/1:9.2p1-2%2Bdeb12u7/debian/openssh-server.postinst/ — `ssh-keygen -q -f "$file" -N '' "$@"`; the create_keys function includes `/etc/ssh/ssh_host_ed25519_key` and is called in the configure branch. Full context and remaining short quotations: PS1.
- https://man.openbsd.org/sshd_config.5#HostKey — “Specifies a file containing a private host key used by SSH.”
- https://raw.githubusercontent.com/openssh/openssh-portable/V_9_2_P1/ed25519.c — `randombytes(sk,32);`

Sentences:

- S8.2-13: “Settings are services and their parameters, the network, including saved networks, devices and filesystems, time and language, accounts, rights, access rules and what is permitted as a means of login to this computer.”
- S8.2-17: “A setting is recorded by a line of its own; a default value obtained with a package or created during its installation is covered by the line of the package.”
- S8.1-12: “The required state of a recorded object is stated by its line.”
- S8.3-4: “**P1. Completeness.** Everything that is installed and every setting, when in force on the computer, are recorded.”
- S8.3-5: “**P2. Guarantee.** Everything recorded in the declaration is in force on the computer as its line requires.”
- S8.4-1: “**Understanding.** The declaration alone, without inspecting the computer, shows what is installed on it and how it is configured.”
- S8.4-2: “For a line that takes a list from outside the declaration, the declaration shows which source determines the list.”

Why the text fails here (four sentences): S8.2-17 permits the package line to cover an installation-created default service parameter without putting its actual value in the declaration. For the generated SSH identity, the package description and generation code do not determine the random seed or resulting key. P1 and P2 can therefore be met at the level of the permitted covering line without the declaration showing this concrete configuration as S8.4-1 says. The text gives a source-only qualification for external lists but no corresponding qualification for locally generated default values, leaving open whether Understanding means concrete configuration or only the generative instruction.

Strongest objection: S8.3-5 might be read to require every concrete value to be written into the declaration. Literally, however, it requires what the line requires, while S8.1-12 lets that line state the required state and S8.2-17 expressly permits package coverage. The alternative objection is that knowing 'generate a host identity' already shows how the machine is configured; this supplies the second reading, but does not reveal which host identity is actually in use. This candidate is a defect in the claimed consequence of the permissive recording rules; a stronger declaration can avoid the situation.

Question order: The newly generated key is not unchanged package-shipped content and is not executable code; as a service parameter it reaches the setting rule. Even if it were classified as an installed object derived from the package, S8.2-16 would still allow generative coverage, so question priority cannot provide its missing value. Neither classification adds the random seed or resulting identity to the text.

Non-breaking reachability: The documented package installation creates the key through its own installer script; there is no privileged direct edit past the declaration. The example does not claim that the existing distribution globally satisfies P4, only that the documented operation is permitted by the coverage rule and is outside S8.1-15's definition of breaking.

Difference between readings: A package-only declaration is complete and describes a generation procedure; whether it also satisfies Understanding depends on whether that consequence promises the concrete generated identity.

Other objects in the same gap: Other automatically generated SSH host-key types; locally generated default service credentials. These are category extensions, not additional independently accepted cards.

## Temporal executable capability — merge into a term card if retained

PS7 establishes a real reachable state: in normal system sleep, user-space code cannot execute. S8.1-9 tests whether a program runs or can be started, S8.3-1 applies at any moment, and S8.3-5 requires recorded objects to be in force. Immediate ability and ability after resuming give different P2 answers; question 2 contains the same temporal uncertainty rather than resolving it. Strongest objection: 'can be started' naturally includes ordinary resumption; the text does not state how far future enabling conditions may be assumed. Record this as a boundary of that term, not a claim that ordinary suspension makes the hypothesis impossible.

## Candidates rejected after attempted refutation

- Removal of program records or material: Section 8.5 excludes their removal; persistent journal retention PS5 cannot become a card.
- Random generated values versus Reproducibility: S8.4-3 promises the result described; a generative requirement can be reproduced without identical bytes.
- Disabled service versus P2: S8.1-12 and the words 'as its line requires' give the closest direct reading for a deliberately disabled state; do not infer an unavoidable contradiction from enablement vocabulary alone.
- An unprivileged configuration tool bypasses a declaration: this violates an implementation's P4, not the consistency of P1/P2/P4.
- Source lists vary or are unavailable: source variation is explicitly qualified by S8.4-2 and S8.4-4; unavailability would need a specified line requirement and a separate concrete contradiction argument.
- Optional exact recording of mutable logs: this adds a requirement under P2; nothing forces a declaration simultaneously to require frozen bytes and continuing writes to those same bytes.
- Non-atomic changes or interrupted application: an ordinary implementation's transition does not show that the definitions require that transition; Section 8.5 excludes when an edit takes effect.
