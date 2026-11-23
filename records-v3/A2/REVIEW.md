# Independent review of A2 candidates

Role: review only. Recorded: 2026-11-22 04:42:32 UTC.

Judgments apply the literal text of Sections 2 and 3. They do not propose repairs or wording.

## PROPERTY-CANDIDATES.md

### P-C1. An editor can also be a package manager — RETAIN

The documented case is real: the GNU Emacs manual says, “This prompts for the name of a package with the ‘available’ status, then downloads and installs it.” The collision is at the program-classification level. S3-6 says, “**Built-in tool.** A program of the system whose purpose, according to its documentation, includes changing what must be recorded: a package manager, including package managers of programming languages and of application packages; account and rights management; the service manager; network and firewall configuration.” S3-7 says, “General-purpose programs—an editor, file copying, link creation, the command shell—are not built-in tools: changing with them, through superuser privileges, what must be recorded is breaking.” The unit in both sentences is a program, and neither gives priority when one documented program has both purposes. S3-8 expressly assigns 0 when documented purpose still does not decide the classification. The final card should make explicit that the installed package contains code executed with the editor's rights; installation of a merely inert or exempt in-program setting would not establish that the tool changes something that must be recorded.

### P-C2. Boot-order lines have no unambiguity test — RETAIN

The primary source documents a separate operation: “Explicitly set BootOrder (hex).” S2.2-16 says, “the boot order and device firmware must be recorded where the system is able to change them.” S3-9 covers only a line that installs something, while S3-10 says, “A line for an account, a service or a rule is unambiguous when every value of the object is either stated in the line or fixed by the system as a documented default.” The text separately enumerates “a rule” and “a boot order” in S2.1-3, so treating every prescribed state as a rule would erase a distinction the text itself makes. No unambiguity indicator covers the mandatory boot-order line. Broaden this card to the omitted mandatory-object categories only where a primary source establishes the object; do not create one card per category.

## ROOT-CANDIDATES.md

### R1. A package name does not say which objects count as recorded — REJECT

The source establishes package-installed `sysusers.d` configuration, but the proposed hole is resolved for the stated declaration. S2.1-4 says, “For a recorded object, its line states the required state; whether a recorded program is running at a given moment does not matter unless its line requires it.” A line that pins only a package and does not state the account's required state does not record the account; P1 therefore requires the account to be recorded. S3-9's content-identification test does not convert every effect of installed content into a separately recorded object. The candidate mistakes deterministic provenance for the text's stated-state relation.

### R2. In-force tests stop before shared settings — RETAIN

The systemd documentation says, “The /etc/localtime file configures the system-wide timezone of the local system that is used by applications for presentation to the user.” This is neither a setting in force only inside one program nor an object whose in-force condition S2.1-3 states. S2.2-1 requires recording whatever behavior depends on, but P1 in S2.3-4 applies to such an object only when it “is in force on the computer.” Calling every selected shared setting “a rule” is not supplied by the text; S2.1-3 separately lists rules alongside several other object categories. Retain as the general gap: Section 2.2 makes object types mandatory for which Section 2.1 supplies no in-force criterion. Merge later candidates that merely instantiate this same missing branch.

### R3. A remote account is usable locally without existing locally — RETAIN

The cited primary documentation states, “SSSD does not create user accounts on the local system. Instead, it uses the identities from the external data store and lets the users access the local system.” S2.1-3 says only, “an account exists,” and S2.2-15 says, “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded”. Neither sentence delimits which externally stored accounts count as existing or in force on the assessed computer. Recording “the account” cannot decide the prior scope question: all directory accounts, locally authorized accounts, resolvable accounts, and accounts that have actually logged in are different sets. Retain unless a later candidate establishes a broader computer-boundary term into which this should merge.

### R4. An interface can permit selected effects outside its program — REJECT

The primary source says that applications “can only access files and directories they've been given access to.” S2.2-10 requires recording code when “the program runs it with the program’s own rights, so that the code can do whatever the program can do”. The proposed guest cannot do whatever the host program can do. S2.2-11 then expressly covers “Code that the program confines to its own interface”. A capability-limited linked interface fits those literal conditions even if effects reach a selected host directory; the text never requires all effects to remain in private application storage.

### R5. Virtual firmware fits both the guest and firmware sentences — REJECT

S2.2-11 expressly says, “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.” The proposed OVMF code is guest-system code executing inside the virtual machine. S2.2-16's general firmware rule does not defeat that explicit exemption, and the source does not establish that the OVMF image is firmware “set on the device” under S2.1-3. This is a generic-rule versus explicit-exemption collision already decided by the exemption heading and example.

### R6. A login key can be present but require confirmation each time — RETAIN

The primary manual says, “Indicates that added identities should be subject to confirmation before being used for authentication.” S2.1-3 makes a login key in force when it “is available to the program that uses it”, but gives no criterion for availability subject to a pending per-use condition. The identity is loaded and requestable, yet it cannot be used for authentication until a separate confirmation succeeds; ordinary senses of “available” support both classifications. S2.5-1 permits a system to choose its authority and secret-protection design, but that does not supply the missing observable predicate needed to decide P1 for the chosen design. Retain as the general conditional-availability gap and merge locked-agent, absent-token, touch-required and similar credentials into it rather than making separate cards.

## PAIR-TERM-CANDIDATES.md

### A regenerable executable cache is both optional and required — RETAIN

This is a direct collision between two expressly classified properties of the same file, not merely the general removal rule against an exemption. The Python documentation says, “To speed up loading modules, Python caches the compiled version of each module”; the import documentation states that loading performs “module execution.” S2.2-5 says, “cache: after it is removed, the computer does the same, only more slowly;” S2.2-10 says code executed with the program's own rights “must be recorded”, and S2.2-13 says, “A file that a program executes as code counts as code even when it holds settings”. A current compiled module used by the loader fits both explicit categories, and the code-versus-setting priority in S2.2-13 says nothing about code that is also a cache. Retain only with a quotation that directly ties the compiled cache to loading or execution; the two current quotations are close but the final card should not make that factual link implicit.

### A setting used by one program can also be a mandatory login rule — REJECT

S2.2-15 names the exact case: “an account password need not be, but the rule that password login is allowed must be”. `PasswordAuthentication` is that rule. The broad setting exemption in S2.2-7 does not make the exact later classification undecidable; the explicit consequence fixes this otherwise boundary-prone case. S2.2-13 establishes that the file is read as values, but it does not say every setting is exempt.

### An editor is also a documented package manager — MERGE with P-C1

This is the same program, same source, same S3-6/S3-7 collision and same effect on the breaking classification as P-C1. Keep one card only.

### Guest firmware crosses the guest exemption and the device rule — REJECT

Same judgment as R5. S2.2-11 explicitly exempts “a guest system in a virtual machine”. The case establishes guest firmware and guest boot order, so treating the general device rule as an unresolved contrary answer would disregard the express guest exemption.

## TERMS.tsv consistency audit

- Row 61 should be `yes: S3-3`: after one success and during a later unreported application, the former remains “the declaration of the last application that the system has reported as successful”.
- Row 80 should not be a `no` on the stated facts. S3-3 orders by the successful applications as reported; different report order still produces a last reported success. A separate identity problem would need evidence that one report cannot be associated with its application.
- Row 81 should not be a `no`. At the one-hour point S3-4 keeps the previous declaration in force; if the system later reports that application as successful, S3-3 then identifies it as the last successfully reported application. The sentences decide each observation time without requiring a permanent cutoff.
- Row 82 is not a counterexample. S3-4 does not assert that a previous declaration must exist before a first application; a failed first attempt simply establishes no successfully applied declaration against which the post-application properties can be checked.
- Row 83 should be `yes: S2.1-4; S3-5`: S2.1-4 makes the required state line-specific. If a line requires a rule only until reboot, its absence after reboot is not “a state that then differs from the declaration reported as applied.”
- Rows 67 and 68 should not be promoted on the stated examples. A line can denote a required value through the fixed semantics of the declared system even when it does not spell the value out, so the declaration can still describe what is in force. A different system version or content would itself have to be recorded under P1 and pinned under S3-9; varying it while calling the full declaration the same assumes the nonconformance that the example is meant to prove.

## SWEEP-CANDIDATES.md

### A value read by one program can control work outside it — RETAIN

The Mozilla documentation says, “these are the settings that tell Firefox to open a PDF file with Acrobat Reader when you click on it.” S2.2-7 exempts “settings that are in force only inside one program”, while S2.2-1 requires whatever the computer's behavior depends on. The text supplies no criterion for whether “inside” tracks the sole program that reads the value or the boundary of the effects it controls. Here one reading makes the browser-owned value exempt and the other makes it mandatory because it starts a separate program. Retain as one scope-of-one-program term card; do not list each analogous directive as a separate finding.

### A Wi-Fi password and a raw key share one field — REJECT

The documentation's distinction supplies the answer rather than a hole: the property accepts either a passphrase or a 64-hexadecimal-character raw key. S2.2-14 exempts “the network password”; a raw cryptographic key is not a password merely because one field can represent either credential. The raw key therefore remains MUST under S2.2-1. S2.5-1 makes protection of the secret a design question, but it does not turn two documented credential types into one undefined type.

## Final artifact pass

The seven cards are distinct and defensible. Cards 1, 5 and 6 all involve P1, but they expose different failures: an omitted object category, the scope of account existence, and the threshold for conditional key availability. No merge is warranted. Three corrections remain before finalization:

1. Card 1 makes the factual claim that removal selects the UTC fallback but paraphrases rather than quotes its source. Add the exact primary-source passage, “If /etc/localtime is missing, the default "UTC" timezone is used.” This directly supports the removal case.
2. Card 4's only exact source quotation establishes downloading and installation, not the further claim that the installed package is executable Lisp run by Emacs. The following official-manual passage directly supports that link and should be quoted with its primary URL: “installing a package using ‘package-install’ takes care of placing the package's Lisp files in a directory where Emacs will find it, and also extends ‘load-path’ as needed”. Otherwise narrow the factual claim to what the quoted package-install page actually establishes.
3. The stated broad-to-narrow ranking is inconsistent with placing the missing unambiguity branch last. It affects boot order plus multiple express mandatory classes and is broader than the conditional-key case. A defensible breadth order is 1, 3, 7, 2, 5, 4, 6. Exact ordering among the middle four is judgmental, but card 7 should precede cards 5 and 6, and card 6 is the narrowest retained gap.

Source support for cards 2, 3, 5, 6 and 7 is adequate. The quotation checker passes all 36 controlling-text quotations. No card duplicates an excluded typed/piped-code, recorded-data-file, declaration-algorithm, Section 2.5 design, or launch-channel case.

## Completed verdict after corrections

`CARDS.md` is accepted: seven distinct findings, broad-to-narrow ordering is now defensible, the two missing primary-source quotations have been supplied, and all 36 controlling-text quotations pass. Add one blank line before the `## 6` heading so the Markdown boundary is unambiguous. The final GNU Emacs evidence is sufficient; the unquoted sentence about byte compilation and autoloads is unnecessary and may be removed, but it does not change the finding.

`SWEEP.tsv` exceeds the required breadth, but the following obvious cross-platform or umbrella aliases should be pruned before calling all 197 rows unique:

- `Calendar timer` and `Crontab scheduled task` are the same functional object: a time-scheduled task. Keep one.
- `Service activation definition` and `On-demand launchd service registration` are the same functional object: an activation-managed service definition. Keep one.
- `Application-private Registry preference` and `Application defaults-domain value` are the same functional object on two operating systems: a preference confined to one application. Keep one.
- `Application state-only file` is an umbrella that already contains the later concrete state rows for window layout, browser session, editor recovery and similar state. Remove the umbrella row.
- `Runtime sensitive-data permission grant` is an umbrella for later concrete Android permission rows, including screen capture and background location. Remove the umbrella or retain it and remove the covered examples.

`Login-triggered task` and `Per-user login agent` are close but can remain: one is a scheduled action at the login event and the other is a registered per-user managed service. The remaining rows represent different functions or materially different scopes rather than renamed OS equivalents. Pruning the five aliases above leaves a large margin over 150 and does not change any retained card or HOLE kind.
