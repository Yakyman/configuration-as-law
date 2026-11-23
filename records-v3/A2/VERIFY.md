CARDS: 7 confirmed of 7

# A2-V: verification of the A2 cards

Recorded 2026-11-22T05:05Z (UTC) by the verification. The verification took no part in A2. Read: TEXT.md Sections 2–5,
SENTENCES.md, A2/CARDS.md; SWEEP.tsv rows were opened only for the sample and to compare the HOLE rows with card 2.
Copies of the card sources fetched for this check are in `A2/raw/verify/src/`. In the table below, source passages are
in single quotes; text passages are in double quotes and are the exact sentences of SENTENCES.md.

## Card verdicts

| # | Title | Verdict | Sentence ID with quote / source | Reasoning |
|---|---|---|---|---|
| 1 | Shared settings have no test for being in force | CONFIRMED | S2.1-3 “a program or code runs or can be started, a service is enabled, an account exists, a rule is applied, a saved network or a login key is available to the program that uses it, firmware or a boot order is set on the device”. Source checked (localtime(5), systemd 248): 'configures the system-wide timezone of the local system'; 'If /etc/localtime is missing, the default "UTC" timezone is used.' | The timezone is used by many programs, so S2.2-7 does not exempt it and S2.2-1 requires it; it is none of the kinds listed in S2.1-3 (not literally a rule), so P1 cannot be evaluated for it. |
| 2 | A setting can belong to one program and act outside it | CONFIRMED | S2.2-7 “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser”. Source checked (Mozilla profile article, archived copy; the live page returned a client challenge): handlers.json, 'these are the settings that tell Firefox to open a PDF file with Acrobat Reader when you click on it.' | The preference is read only by Firefox but its effect is that another program starts; no sentence says whether "inside one program" means where a setting is read or where its effect lands. |
| 3 | An executable cache is both optional and required | CONFIRMED | S2.2-5 “cache: after it is removed, the computer does the same, only more slowly” against S2.2-10 “code that another program executes must be recorded if the program runs it with the program’s own rights”. Sources checked (Python tutorial 6.1.3; import reference 5.4.1 and 5.4.6): all three quoted passages found. | A .pyc file meets both sentences literally; S2.2-13 gives code priority only over settings, and no sentence orders the cache exemption against the code rule. |
| 4 | An editor can also be a package manager | CONFIRMED | S3-6 “A program of the system whose purpose, according to its documentation, includes changing what must be recorded” against S3-7 “General-purpose programs—an editor, file copying, link creation, the command shell—are not built-in tools”. Source checked (GNU Emacs manual, Package Installation and Lisp Libraries): 'then downloads and installs it'; 'takes care of placing the package's Lisp files in a directory where Emacs will find it'. | Both sentences classify the same program and neither prevails; S3-8 “if it does and this indicator still does not decide whether the program is a built-in tool, the case is a counterexample to the definitions and yields 0” assigns 0 rather than deciding, so it confirms the hole. |
| 5 | Boot-order lines have no unambiguity test | CONFIRMED | S3-9 “A line that installs something is unambiguous when it states the version and the source” and S3-10 “A line for an account, a service or a rule is unambiguous when every value of the object is either stated in the line or fixed by the system as a documented default”; S2.2-16 makes boot order mandatory. Source checked (efibootmgr README): '-o \| --bootorder XXXX,YYYY,ZZZZ,... Explicitly set BootOrder (hex).' | A boot-order line installs nothing and S2.1-3 lists a boot order separately from a rule, so neither branch of the indicator applies, while S2.4-2 and check 3 need the line to be judged unambiguous. |
| 6 | A remote account has no clear boundary of local existence | CONFIRMED | S2.3-4 “Everything that must be recorded under Section 2.2 and is in force on the computer is recorded”, with S2.1-3 “an account exists”. Sources checked: sssd.io introduction, 'Specific users and, or groups can be authorized to access the host'; RHEL 7 System-Level Authentication Guide (archived HTML copy; the PDF and live page returned 403), 'SSSD does not create user accounts on the local system.' | Accounts are mandatory (S2.2-15), but "an account exists" does not say whether existence in the directory, resolvability on the client or authorization on the client counts as being in force on this computer; S2.5-1 user authority concerns powers, not which accounts exist. |
| 7 | A key awaiting confirmation has no clear availability test | CONFIRMED | S2.1-3 “a saved network or a login key is available to the program that uses it”. Source checked (OpenBSD ssh-add(1), -c): 'Indicates that added identities should be subject to confirmation before being used for authentication.' | "Available" is not defined; a key the program can request but not use without approval fits it or not depending on the reading, and S2.5-1 frees the protection policy but not the in-force predicate that P1 uses. Not the same gap as card 6: a different predicate of S2.1-3 and a different object. |

No card was refuted: for each, the verification looked for a deciding sentence among S2.1-3/4, S2.2-1…16, S2.3-4…7,
S3-1…10 and S2.5-1…3 and found none that decides the case without an added word.

## Confirmed gaps in the verification's own words

1. **Shared settings.** A setting such as the system timezone is used by many programs, so the text requires it to be
   recorded. But the definition of "in force" names only programs, services, accounts, rules, networks, keys, firmware
   and boot order, so there is no way to say whether an unrecorded timezone is in force and therefore whether P1 fails.
2. **One-program settings.** The exemption for settings that act only inside one program does not say whether that
   means the program that reads the setting or the place where its effect appears. A browser preference that makes the
   browser start a different program is exempt under the first reading and mandatory under the second.
3. **Executable cache.** A compiled Python cache file is a cache, which need not be recorded, and also code run by the
   interpreter with its rights, which must be recorded. The text says code beats settings but never says whether code
   beats the cache exemption, so the file is both required and not required.
4. **Mixed-purpose program.** Emacs is an editor, which the text says is not a built-in tool, and its manual documents
   installing packages of code, which makes it one. The text has no rule for a program that matches both, and its own
   fallback simply declares such a case a counterexample.
5. **Boot-order line.** The test for an unambiguous line covers only lines that install something and lines for
   accounts, services and rules. A line that sets the boot order is none of these, so the text gives no way to decide
   whether it is unambiguous, although reproducibility depends on that.
6. **Remote account.** The text makes accounts mandatory and says an account is in force when it exists. For identities
   kept in a remote directory and served to the client, it does not say whether existing in the directory, being
   resolvable on the client or being allowed to log in to the client is what makes an account exist on this computer.
7. **Gated key.** A login key counts as in force when it is available to the program that uses it. A key held by an
   agent that asks a person to confirm each use can be requested but not used without approval, and the text does not
   say whether that is available.

## Sweep sample

Seed `20261122`; Python `random.seed(20261122)` then `random.sample` of 30 from the 179 rows of SWEEP.tsv whose
decision is MUST or NOT (file lines, header is line 1). Script: `raw/verify/sample_sweep.py`; output:
`raw/verify/sample.txt`.

Result: 30 rows checked. 21 rows: the cited sentences give the decision. 9 rows do not: 2 are still decided by another
sentence (lines 122, 139), 1 is outside the definition (line 38), 6 are instances of card 2 (lines 46, 106, 140, 142,
168, 170: new hole candidates that reduce to an already confirmed gap).

| Line | Type | Decision | Cited | Check |
|---|---|---|---|---|
| 6 | Unused factory configuration example | NOT | S2.2-4 | given, on the row's premise that no tool copies the file (the hierarchy spec: 'Software should not read configuration settings directly from /usr/share/factory/'); removal leaves only the file itself unavailable |
| 11 | Executable compatibility symlink | MUST | S2.2-1,2 | given: removal breaks commands called by that path |
| 17 | Service activation definition | MUST | S2.2-1,2 | given: removal makes the service impossible to start; S2.1-3 lists services among objects that must be recorded |
| 38 | File synchronization lock | MUST | S2.2-1,2 | NOT GIVEN as a decision of the definition — see candidate L38 |
| 46 | SysRq permitted-operation mask | MUST | S2.2-1,2 | NOT GIVEN — see candidate L46 |
| 61 | Browser extension confined to browser interface | NOT | S2.2-7,11 | given: extensions are the named example of S2.2-7 |
| 63 | Web browsing history | NOT | S2.2-6 | given: history is named |
| 70 | Dependency install-reason flag | NOT | S2.2-6 | given: the install reason is a stored record of how the package came to be installed |
| 80 | Shell logout cleanup file | MUST | S2.2-10 | given: code run by the shell with its rights |
| 84 | Shell file-creation umask | MUST | S2.2-1,2 | given: inherited by every child process, so not inside one program |
| 94 | Connection last-used timestamp | NOT | S2.2-6 | given: a record of a past activation; S2.2-6 exempts it although autoconnection reads it |
| 100 | Wi-Fi protected-management-frame requirement | MUST | S2.2-14 | given: part of the saved network, and S2.2-14 excepts only the password |
| 106 | DHCP client identifier | MUST | S2.2-1 | NOT GIVEN — see candidate L106 |
| 107 | Policy-routing selection rule | MUST | S2.2-1,2 | given: the rule is applied by the kernel to all traffic, so it is in force outside the program that stores it |
| 108 | Network address-translation policy | MUST | S2.2-1,2 | given: applied as kernel translation for all traffic |
| 110 | Container bind-mount mapping | MUST | S2.2-1,2 | given: the mount exists in the kernel for the container process, outside the runtime |
| 122 | Guest memory snapshot | NOT | S2.5-1 | NOT GIVEN by the cited sentence — see candidate L122 |
| 133 | Device visibility ruleset | MUST | S2.2-1,2 | given: applied by the kernel to devices of the jail |
| 139 | Mandatory multifactor-authentication sequence | MUST | S2.2-1,2 | NOT GIVEN by the cited sentences alone — see candidate L139 |
| 140 | SSH server identity key | MUST | S2.2-1,2 | NOT GIVEN — see candidate L140 |
| 142 | SSH agent forwarding permission | MUST | S2.2-1,2 | NOT GIVEN — see candidate L142 |
| 145 | Account expiration deadline | MUST | S2.2-15 | given: a value of the account (S3-10 treats such values as part of the account line) |
| 148 | System-wide Registry configuration value | MUST | S2.2-1,2 | given: system-wide, not inside one program |
| 158 | Global preferences domain value | MUST | S2.2-1 | given: read by all applications |
| 168 | Persistent boot order | MUST | S2.2-16 | NOT GIVEN — see candidate L168 |
| 170 | Firmware-setup next-boot flag | MUST | S2.2-1,2 | NOT GIVEN — see candidate L170 |
| 174 | Firmware search-path override | MUST | S2.2-1,2 | given: selects which firmware is set on the device, a mandatory kind under S2.2-16 |
| 175 | Device permission assignment rule | MUST | S2.2-1,2 | given: the permission is applied to the device node for all programs |
| 185 | System timezone selection | MUST | S2.2-1 | given as a recording class (its in-force status is card 1) |
| 189 | System collation-order setting | MUST | S2.2-1 | given: read by all programs |

### Rows where the cited sentences do not give the decision

| Line | Verdict | Sentence ID with quote | Reasoning |
|---|---|---|---|
| 38 | OUTSIDE | S2.5-1 “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.” | A lock file in the runtime directory is program state; S2.2-2 read alone gives MUST, but the treatment of program state is a design question, so MUST is not a decision of the definition. |
| 46 | DUPLICATE (card 2) | S2.2-7 “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser” | The mask is read only by the kernel and steers only the kernel's own reaction to a key; exempt if "inside" means where it is read, mandatory if it means where the effect lands. |
| 106 | DUPLICATE (card 2) | S2.2-7, as above | The identifier is read only by the network manager and only shapes the request it sends; same boundary. |
| 122 | REFUTED (not a hole) | S2.2-11 “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.” | S2.5-1 cited by the row makes the object a design question, not NOT; the decision NOT is given by S2.2-11, since the snapshot is the guest system's saved state. |
| 139 | REFUTED (not a hole) | S2.2-15 “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;” | S2.2-1/2 alone would leave the S2.2-7 question of card 2 open; the required method list states whether password login is allowed, so S2.2-15 decides MUST. |
| 140 | DUPLICATE (card 2) | S2.2-13 “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting” | The host key is read only by sshd as values, so it is a setting; whether it is "inside one program" (sshd) or acts outside (clients verify it) is the card 2 boundary. It is not a key used to log in to an account. |
| 142 | DUPLICATE (card 2) | S2.2-7, as above | The option is read only by sshd and only governs what sshd itself permits; same boundary. |
| 168 | DUPLICATE (card 2) | S2.2-16 “the boot order and device firmware must be recorded where the system is able to change them” | The source (bootctl(1)) documents 'Sets the default boot loader entry', a loader setting, not an order; without the word "default entry" added to S2.2-16 the row rests on S2.2-1/2 and the loader-only boundary that A2 itself marks HOLE for the boot menu timeout (line 171). |
| 170 | DUPLICATE (card 2) | S2.2-7, as above | The flag is neither the boot order nor device firmware; it is read only by the firmware and steers its own next boot; same boundary. |

Observation for the record: A2 marked as HOLE several settings read by one program (lines 33, 67, 74–78, 117–125, 171)
but marked as MUST other settings of the same shape (sample lines 46, 106, 140, 142, 168, 170). The sweep's count of 13
HOLE rows therefore understates how far card 2 reaches; the card itself stands as one gap.
