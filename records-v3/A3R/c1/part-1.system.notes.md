# Classification c1: system subset

Only the authorized input, raw inventory, fixed text, build description and cited public documentation were consulted. No objects were removed.

## Exact text

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.
- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.
- **S2.2-3** The following need not be recorded:
- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;
- **S2.2-5** cache: after it is removed, the computer does the same, only more slowly;
- **S2.2-6** records of the past—logs, history;
- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.
- **S2.2-8** Consequences of this rule that we fix explicitly:
- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;
- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.
- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.
- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.
- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;
- **S2.2-14** a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;
- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;
- **S2.2-16** the boot order and device firmware must be recorded where the system is able to change them.
- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.
- **S3-2** If what the object does remains unknown, the case yields ?.

## Homogeneous rules and manual checks

Each rule below was checked against the displayed raw entries for its first ten listed IDs. Functions, not inventory class labels, determine the decisions.

### accounts

Scope: account. 40 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 66251b78bb6f912aa915abb1, 0500fe8692cdec2d97e72891, 1a8c96d4c282ed70c6167e58, cd80c580185f4091df737c0c, 40e833964547387f3ca4e553, c2b55ec7fb85f936e32f588e, a634e1780bab80e03cbf0e39, 855811c08518bf800c8dd897, 3d2875b6496538d42abc46ba, 3de43376d6f23e3efccd5496.

### groups

Scope: group. 68 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 424cb5f40e407805606b43e3, 9a4c7a2ea9898d9ae38b5554, ca43ae86e803e0ce5b114acb, 275846cd06c295d42d5542fa, cd5cf2d139b549e5462d19b9, 233837b04ee105ad3015470e, d05c192167c5d3fe22d5bcb2, 5af62d641728cadffc3d9ac4, e55ba3e907101bc803a424b4, 2f8d930a409d1f2bdd2c5fa3.

### services

Scope: service, user-service. 19 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 47c7815588e844c881916f82, 3c4f4e65c757b551ff3b1f81, dcac5914e520f17b298b681f, a315658eb8bf9e7eb6a1b6ea, 2a46a74df2451e259b6ed3b0, 4dc126c54aec97463c351c86, 5bcd72a57568d62e4b8eeaa5, 6c6b38144ff0ac1886377992, d59d14dc3535bec649909ff1, 1413205ac7d1d69a837dabb3.

### absent-services

Scope: service, user-service. 19 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: d6bc83a7f2ca4f16f6e78efe, 06fa1242840b189689061719, 90f390ddf29b7369718d4977, fa69fb560b4500fad1f08784, 2f5b18f25d55cf29bd04e4f1, f2aee53f185b859565fdfdc8, 3f1c73b48d9806792c04fcb4, 2dddfe42afbabcf835c845c8, 1fe8a1baafff2cd597376eb3, 978e06a6ed01dcd129258630.

### units

Scope: unit-file, user-unit-file. 55 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 531cdbe55af3004b2739cb22, df6003b998e902e368f48f0c, 6c8613682668a234b62b9293, 502b5f821f78dc4db11523ce, e5550072d851d99906872129, e1e0b163b302a8cbbcc9d7e0, 5ec94a501ed23615be676ed4, c448e0f072952ad51da0e28e, de9bc02887c53b50e0a1898f, cae5392ebf5125dba2b23e25.

### processes

Scope: process. 66 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: a54331f4416f0d3975046f6e, 4d26d5704cf52e5ae4acbf8c, ac12bb908cb86db7ea204809, 47402393f7377f308ce3da35, 2d208f9f569bf7cab0a7cb42, 69554e1c931ffa3c34beb96b, a2c934737dae951e4e69f2ef, a38a087a068b5823d770620c, d22f66dc0415311f8a7c34b5, 4eb464269c6a97375189523e.

### unresolved-processes

Scope: process. 22 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 1c460643fdd8cfbbd196d5c8, 8b1dbd0e6a04dda53f042fdf, 42c8a140e560dc29380e1d8c, 9dfd7d2fb9793e2b0f9e0450, 1de8c224f0b98ee3c699a8f1, 870b4f98bda38de1efeebee1, 7f68c5deb8bee8904640065d, 5170ad8d1f6cab983ec4aac9, a56cebd347b0e2d321707d00, 405fd3b1305197a3b82e9395.

### drivers

Scope: driver. 35 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 362aac25bc3ff6a3adf0a0e5, d12eacb0fc0b883b38c28c81, 31489a1bb2b9bcbc9d50becb, ec02f88264ac6f14cb3c7b48, 516af3b20d07477d0880f173, 7285a2d79b6340611118e1b8, 4a16f044d2a204288036ee84, 21d0a8ca78fa8dab4685b518, 325f463f0ee4c170dfda2160, 4d95912dea3aba87d392ee89.

### ports

Scope: port. 30 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 50569e2b739a95c2d9211520, a10944ac5db4979488d11d44, 818e748f0a25d4ce6b7e112b, 90015923ad530f453981f9d7, c130018c3b73f5cd5e761ce1, f63fd0600c18846258c07f68, f4bbb25a9e6780d70e006fe9, 2b4d1a3fdb18bd8257283ff6, 4e2a49e1518a7ae42fd035da, b12b144e402737d5b7dbfd69.

### firewall-rules

Scope: firewall-rule. 21 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 82cf95c36b73b53f28b0a694, 00e4bb96eba524c41611dcf9, 32d581eebb12d54853ebf91c, e649b8e7c3e336831c4836f6, 38a2815ee993ffdf0b64293f, b64534a87c0760c3621f0857, bbdc0f43e0cc8d2c12d255c1, 47921eae029fa610270e94f1, 85ec649d68b7beab063b6b99, 46a718f82a4f2bc6ba44ef0b.

### polkit

Scope: polkit-actions. 219 rows. The corresponding TSV reason is the rule applied by `classify_system.py`.

Manual checks: 3e209d6e565fbc2a96423ca5, 93664169da2a08543bebc9fd, 92b43c33b616c9da07700acf, cbc914d3e7e1602d9b6053f5, b3b783db0a8964cfae6d3e79, f086f19d5724019e2120e18e, d88942a7193718431a649c09, f467c8cc721d8153af82e90f, 2ba592b30a400e0fe5514afa, 9689bca4147eb2173056832e.

## Sources

- https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html : “Actions correspond to operations that clients can request the mechanism to carry out”. Policies span client, authority and service processes.
- https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html : “A unit file is a plain text ini-style file”. Service units arrange external program activation, rather than settings confined to systemd’s interface.
- https://docs.kernel.org/driver-api/driver-model/binding.html : “Driver binding is the process of associating a device with a device driver that can control it.” Rows identify the binding, not ordinary stored symlink files.
- https://www.man7.org/linux/man-pages/man5/group.5.html : “The /etc/group file is a text file that defines the groups on the system.” Group records define usable named credentials, including empty groups.
- https://netfilter.org/projects/nftables/manpage.html : “nft - Administration tool of the nftables framework for packet filtering and classification”.
- https://man.openbsd.org/sshd_config : “The file contains keyword-argument pairs, one per line.” These are values, not executable code.
- https://docs.podman.io/en/latest/markdown/podman-run.1.html : “Run a process in a new container.” The same documentation specifies automatic image pulling when absent.

## Process evidence defect

`../in/raw/lived/raw/076-process.sh` prints the PID and a tab before `readlink`; a failed readlink emits no newline. Several raw lines therefore concatenate unresolved PIDs before another PID and its executable. The row name is the first PID. Those rows are UNKNOWN, not assigned the last PID’s executable. Public program documentation cannot recover which program an unidentified PID ran.

## Individually considered remaining rows

SSH values were considered individually using https://manpages.debian.org/trixie/openssh-server/sshd_config.5.en.html and the corresponding keywords in https://man.openbsd.org/sshd_config. The sources define each directive. Quote: “Specifies what environment variables sent by the client will be copied into the session”. No actual account password is included.

- b8093dd460d9b0712167e99d: MUST; Schedules the development cleanup service. Removing the active timer stops the scheduled cleanup action.
- ce9cf885ee9d5f0106f81e49: UNKNOWN; Lists a timer without an activation time or target service. The listing supplies no activation or target, and the related service is absent; existence and function of this timer remain unestablished.
- 6545c01a63ed249cce38d052: MUST; Contains the identified packet-filtering chains and their policies. The table holds firewall policy definitions, including default chain verdicts; these firewall rules are explicitly required.
- 717eb2770380a84a60c5c313: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- dda59fbc8826d393f7d01a10: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 35cb6ad5449614d23bebe242: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 48c1fa93a17da9d38e506def: MUST; Contains the identified packet-filtering chains and their policies. The table holds firewall policy definitions, including default chain verdicts; these firewall rules are explicitly required.
- a09dad130a88e21ac58d25ca: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 42fee34c37890e2ec7bad698: MUST; Contains the identified packet-filtering chains and their policies. The table holds firewall policy definitions, including default chain verdicts; these firewall rules are explicitly required.
- a1543f91747b9c5a83532869: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- ea5d40a2dff60d224d49f01a: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- dd09d750d72e29a6802c0993: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 68e163de5be454c2c0f3b7ff: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 402a14bcdc254a1331a2d91c: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 45fa13af9c9c2849fefd5d4a: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 2714f30ffdeaf1632792f969: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- c170614338f39c0ff9dbc556: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 339a64d45b4a268c2b7939fe: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- c8c7f72048df6524167e19e5: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- baf66f3a90895b339239008f: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- e68b62bdcfb24cc617e6993a: MUST; Defines packet-processing chain hooks, default verdicts, or referenced rule targets. The chain supplies firewall policy or rule execution structure; removing it removes that firewall definition.
- 29b72142ba82d7d23e0e9bbd: MUST; Defines a system network interface or tunnel connection profile. The profile configures network connectivity for other programs; removal loses that saved connection capability.
- 45494a3628cd9f2a6a155e72: MUST; Defines a system network interface or tunnel connection profile. The profile configures network connectivity for other programs; removal loses that saved connection capability.
- 44bcf67fcda29b9fa6d3de74: MUST; Defines a system network interface or tunnel connection profile. The profile configures network connectivity for other programs; removal loses that saved connection capability.
- ad5b73353f54e5a01ea55bb9: MUST; Defines a system network interface or tunnel connection profile. The profile configures network connectivity for other programs; removal loses that saved connection capability.
- 37e697762632a2f0de4384fd: MUST; Stores a saved Wi-Fi connection profile. Saved Wi-Fi networks are explicitly required; this row identifies the network profile, not its password.
- 65df70aaa862229cd4fd3618: MUST; Stores a saved Wi-Fi connection profile. Saved Wi-Fi networks are explicitly required; this row identifies the network profile, not its password.
- fbc43cf4d2bace79f0e65a70: MUST; Provides an operating-system network communication interface. Removing the interface prevents traffic through it, affecting communication by multiple programs.
- 62d714301de740e46b1a3024: MUST; Provides an operating-system network communication interface. Removing the interface prevents traffic through it, affecting communication by multiple programs.
- 91ecf17e0567fccc77b8e076: MUST; Provides an operating-system network communication interface. Removing the interface prevents traffic through it, affecting communication by multiple programs.
- 204facdaa40276808ea45ed2: MUST; Provides an operating-system network communication interface. Removing the interface prevents traffic through it, affecting communication by multiple programs.
- de63db4254e7f1cbf407dffd: MUST; Provides an operating-system network communication interface. Removing the interface prevents traffic through it, affecting communication by multiple programs.
- d1e8812964d588e2a21c6235: MUST; Selects SSH listening port. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 737f1902f893bea8c97a1782: MUST; Selects SSH IPv4 or IPv6 listening. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 7e4c1ea41e01e76ab786bf0a: MUST; Selects SSH listening address. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 9570234ba746fde9faa9eeb9: MUST; Selects SSH listening address. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 5f8fcf77e7c5041de9f3e517: MUST; Enables PAM account and session checks. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 4725e095d352bc5ed4c1212b: MUST; Selects PAM service configuration. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 70af2f25c61976b23e86474e: HOLE; Limits time available for login. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- a92608a203e2973dcfaed75e: MUST; Selects initial X11 proxy display number. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 73b70232c07e15bee2c93628: HOLE; Limits authentication attempts. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- e8ddd511263a12c14f4e5efe: HOLE; Limits concurrent login sessions. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- d29f710b6352ad934c568a48: HOLE; Schedules SSH client liveness probes. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 8ffdf2c6cb34aa995b80a0b8: HOLE; Limits unanswered client liveness probes. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 64c3eeeb56074c666b06d5da: HOLE; Sets minimum accepted RSA key size. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- fc175f3fe8e9bfeb82bd30b7: MUST; Sets permissions on forwarded Unix sockets. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 846b368c9c7eb3b2cc9bafda: HOLE; Limits time retaining connections without channels. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 5dfdf1d7b9c621a510a827ea: MUST; Controls remote login to the superuser account. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- ca5a9ae631db41881a734b4e: MUST; Controls rhosts authentication source. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d12c24ce799f60fedc128ce0: MUST; Controls user hostbased authentication sources. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 2b243d7d1c8afe48dcd5638d: MUST; Controls hostbased account authentication. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 63f63d2dbbcced0b61b17eb8: HOLE; Selects hostbased authentication hostname source. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- d858b7eb5b5db644a78163d0: MUST; Controls public-key account login. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- c820f0571c36594777b32e84: MUST; Controls Kerberos account login. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 753c27cfe7d736e997bdfae4: MUST; Controls password fallback for Kerberos authentication. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- c462b75395e079a1aca2a05a: MUST; Removes session Kerberos tickets at logout. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- c8d97c4e5a2cc2c9113c1511: MUST; Controls GSSAPI account login. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- bbad5c6166456c8edcbaefd6: MUST; Cleans session GSSAPI credentials at logout. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 999504031457ae948155b61a: HOLE; Controls GSSAPI key exchange. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 4df184f1d0b6c034f26d0ce0: HOLE; Controls server principal checks for GSSAPI. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 19dab249d75fc4989eb0155c: MUST; Updates stored GSSAPI credentials on rekey. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 64c1378303db60df30dc481f: HOLE; Selects GSSAPI key-exchange algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- ef20600433d5240311ab31ed: MUST; Controls password account login. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 17944940865f95039d032349: MUST; Controls keyboard-interactive account login. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 0fa4588a2dad34f680665277: NOT; Controls login message display. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 92e6c624ab79089f59bfa9ac: NOT; Controls display of previous login. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 82afb2db4ffd5e38b0ec4ecd: MUST; Controls X11 access forwarding. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 975a5aa0f2ba4519ff6f9882: MUST; Controls X11 forwarding socket binding. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d6235a098bb82243371dc8d0: MUST; Controls pseudo-terminal allocation. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- c30c19e8bcd5ed9c4c5321d4: MUST; Controls execution of user session startup code. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 4b2c2f0ad8ab9f74f3a65c6e: MUST; Checks login-file ownership and permissions. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 7f4432571561605278bf1b19: HOLE; Controls transport keepalive probes. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- c8a680baaf352c8e605fb03e: MUST; Controls login with empty passwords. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 0d65c285875796e9bbf21830: NOT; Controls SSH transport compression. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 74999b1091594f23c49d1e14: MUST; Controls externally reachable forwarding sockets. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- ba7e43ae48e7b7e88b3ea292: HOLE; Controls client hostname resolution. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 83bfbe2fd66f60bcc74b2389: MUST; Controls TCP forwarding capability. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 6e5a986502606af48e9fae01: MUST; Controls forwarding access to authentication agents. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 63d8ebafc9125aab5fdb691d: MUST; Controls all SSH forwarding capabilities. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 30fc0b2ef1da93db06446a63: MUST; Controls Unix-socket forwarding capability. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- b264b65fcfc3d225ca4cd1e5: MUST; Controls removal of existing forwarding socket paths. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 8933d62da3bbf94c46748f84: NOT; Selects displayed key fingerprint hash. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 9a64547fcefb3cbdbd52c4f3: MUST; Exports authentication information to login sessions. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 7d7819fbc923d0351a4b6ae9: MUST; Controls refusal of SSH connections. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 5910743adb18dff8d270113c: NOT; Controls distribution identification in server banner. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 21f275a8d1b48381331c9b31: MUST; Selects daemon process identification file. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- cfd777570548528d1120f2ef: HOLE; Selects Diffie-Hellman parameter source. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- acdf33b140bddd83baac8d1a: MUST; Selects external X11 authorization helper. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 602b5e23a1883323cc8e5024: HOLE; Selects transport encryption algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 3eb0197357b7f632c0d5a684: HOLE; Selects transport integrity algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 1a2131e708503d3c6e9975f5: NOT; Selects authentication banner text. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- eaf28940b541c88787e98e69: MUST; Controls forced session command. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 02d364605368ce2e87933c14: MUST; Controls session filesystem confinement. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 6fa7d4f75e0e35c7fade8b0d: MUST; Selects trusted login certificate authorities. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d5a6e136b887d644ed5b86d1: MUST; Selects revoked login key list. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- adbbb49cf85548a7b0d4bd2f: HOLE; Selects security-key middleware. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 8f4b98737822decc4aa358e4: MUST; Selects accepted login certificate principals. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 6e3034df678eb731d614f899: NOT; Selects server version text suffix. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 761bef463139fca352f38ab7: MUST; Selects external login-key lookup command. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 51f5f81517f1036aaf862727: MUST; Selects account for login-key lookup command. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- b1656b52f6546343f81d2b33: MUST; Selects external login-principal lookup command. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d6c8aa3105290ac72af083e5: MUST; Selects account for login-principal lookup command. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- bd2987e4902c8af01f2225cf: HOLE; Selects agent for server host-key signing. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- d807dfa19b8414477670f600: HOLE; Selects SSH key-exchange algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 69e2f73b55483fea06b9b8c0: HOLE; Selects accepted certificate signature algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 151593c72142893b3c097bdf: HOLE; Selects hostbased authentication signature algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- a1a8b86c2f09f76c21f4cfd6: HOLE; Selects server host-key signature algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 30303d540f77779033bc6b7a: HOLE; Selects accepted account public-key algorithms. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 17e46fc45310b9c16b42f4fa: MUST; Selects external session executable. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 8ec96424e643f241a4f7de9b: MUST; Selects external authentication executable. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- f448ba068075fa4146ab2811: HOLE; Exempts sources from connection penalties. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- f4d118580a3e7aa82d912ac9: NOT; Selects diagnostic verbosity. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 11e920923f03575bac9def2f: NOT; Selects diagnostic logging facility. This value controls presentation, diagnostics, or transport processing inside SSH; the single-program setting exemption applies.
- 5d8da4c7ed8f79839659f3c3: MUST; Selects authorized account login-key files. This governs explicitly required account access, superuser login, login keys, or open ports; it is not a password value.
- 837ebb63632431b7c3f91ae6: MUST; Selects server identity key. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 84c1f410613424a2c2846127: MUST; Selects server identity key. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 8fe45bad30e49b61dfc9f9ca: MUST; Selects server identity key. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- ea3c0282d2d33f7f8f77e5eb: MUST; Controls environment passed to session programs. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d962db55ec61443e174b4687: MUST; Controls environment passed to session programs. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- dea39dc9c5f82815409c5d3d: MUST; Controls environment passed to session programs. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 23220e1a88cbb25f827b3335: MUST; Controls environment passed to session programs. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- e1182fe531b91f83ddde87ef: MUST; Selects allowed account authentication combinations. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d913ea330d8c4a39a5ea3001: HOLE; Sets idle SSH channel expiry. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 60d688cfe3148facddc7533d: MUST; Selects external file-transfer subsystem executable. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 4229ee629e74a8e9a246fbc8: HOLE; Limits unauthenticated connections. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 9526c25b3b6c490a157fe0b6: HOLE; Limits unauthenticated connections per source. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 363323f681d7fb46cf88fb80: HOLE; Groups connection sources for limits. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 3bf694aa7045763042ac1ed1: MUST; Controls tunnel-device forwarding capability. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- d2badf806ff0685bfd641d10: MUST; Sets network packet traffic class. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 3306995d71cfd7876d4d337b: HOLE; Sets encrypted transport rekey thresholds. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 1f489f4744d29ff82a43c9ab: MUST; Restricts destinations for TCP forwarding. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- fcbb738fa454383ee9ee8f48: MUST; Restricts listeners for TCP forwarding. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- 072198f6e5546f574cdee23d: MUST; Controls environment passed from account files. The setting governs external login sessions, programs, credentials, devices, or network access; its force extends beyond SSH’s internal interface.
- ff18237bd8a718c081eded14: HOLE; Controls additional public-key authentication requirements. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- b3bc32c5ee21a357406dd84d: HOLE; Sets per-source connection penalties. It controls SSH internally but also determines connection availability; the text does not define whether that effect is confined inside one program.
- 1c014e18a421906ec23c7c86: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 659db790fbad407e7b491b05: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 3c8fbdb169ca038e2f7a8f7a: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 0e7b4eb5eb41a5b6d4329b4e: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 976a51452aa5aaabce9936bc: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 275587ed29b693da11e27dee: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 81efdb137b7129e363e54bc8: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- c97d9f250787c54baa1e0b72: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- 70217070f9a3640192bf6d15: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- be195af2e23105d0bdf5c1e2: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- cd7cb3b2f25e9f09baa807d1: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- 6b15c08f7bc1a541a005da17: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- b1e3831b876984497b7e8d93: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- b8b01cfc68bab1c959788e4e: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- d5004a94c316645f5bf68e8a: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 0ec69b7d8b30779dc1e36f2f: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 9a6877ef4dd6c4c7bffb594f: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- 5d27dbfeaaba365841790985: MUST; Runs or retains a launchable server program in a container. Container programs are explicitly required; stopped retained containers still provide the program’s launch capability.
- d15f6d19976fd46865b5f935: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- 51e0bcb301dea3bd5c64a3ac: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- cbaf6f16dab7fb21b548717b: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- 390e9a29d1bd114fae135522: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- e05bb8e86e06116fe843be06: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- ad5ed316ad45d6f4424c5073: MUST; Supplies executable server or interpreter files for container processes. The image supplies runnable programs; container installation does not exempt programs. Evidence does not establish this exact image as disposable cache only.
- 2775edcfb0f82fc878c68705: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- b84b415e1bf50514c55e592f: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 3e893bb18da6831140bf5cbf: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 64a3574bd2259c1ed1eca376: MUST; Runs a scheduled shell command measuring document storage usage. Removal stops the scheduled command; its shell executes with account rights.
- 5a58baf83824f5a7aa6fd323: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 1c0d2cf76eb8c9c39f062ad7: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- bc748d9e22c3fa931e8e0921: NOT; Contains explanatory comments without active access rules. The complete raw file contains comments only; removal loses documentation, not an active access policy.
- 1d6abde9e70de201cd9f22cb: MUST; Executes authorization rules granting or checking cross-program privileges. The rules change which clients can invoke privileged mechanisms; their effects cross process and account boundaries.
- 725c897e37fdd876f805fa42: MUST; Grants commands the authority to run under another account. The evidence grants superuser command execution, explicitly required by the text.
- 8def8d3af86de559a85b09c5: NOT; Contains explanatory comments without active access rules. The complete raw file contains comments only; removal loses documentation, not an active access policy.
- ce36426d9bc200cddc900200: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 274f9cc66dc198a1cc2ba58d: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- e581cb6387cbf187f0923388: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 67912141d193bf207cf5489b: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 68492d8fadb2a3e81c76739f: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 12166c7ff3c49a8165a055c8: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 10a6f930fb268691b4f8dc71: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 5854afeab0e7e2fb6f6530cb: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 35c07ada63f572ae967d102b: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- dc9cd820c00dfebfa30c73e7: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- c4591b600526302f419d3f8f: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- ebbae05e7033f89e3b498f7d: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- fbe7c34a8b7d57b6d64cccc7: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 0f12515b4d2daa1f7c3adace: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- ecee78bff19a51e9d1e52526: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- a11b005c0e40b20d598aa237: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 1c3f3e73a9b7512cd3491b21: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- aefa03a23283acd5ff4e35ff: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 1407f5dd4ec885764ba87d8d: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 021870f6557c1dbd60610edf: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 837b226662b3921cf5c07a59: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- cc9f0e00b416491cdc788c92: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- e612a7941991dfb21f7d0d4b: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- d2cc6a2e5c6ac97274cf0c4f: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 9824b0d6f5397a64a7646653: MUST; Selects authentication, account, password-management, or session modules. The active module stack governs account access or external session behavior; removal changes those operating-system capabilities.
- 9a3b6e231bc7eba3365b24bd: MUST; Executes authorization rules granting or checking cross-program privileges. The rules change which clients can invoke privileged mechanisms; their effects cross process and account boundaries.
- 4b8a98d8f999fea37b32bde2: MUST; Executes authorization rules granting or checking cross-program privileges. The rules change which clients can invoke privileged mechanisms; their effects cross process and account boundaries.
- fa6d95b263e511ca146e966d: MUST; Executes authorization rules granting or checking cross-program privileges. The rules change which clients can invoke privileged mechanisms; their effects cross process and account boundaries.
- 5b0117625a58399aae82e9bb: MUST; Executes authorization rules granting or checking cross-program privileges. The rules change which clients can invoke privileged mechanisms; their effects cross process and account boundaries.
- b28703b0cdea90b900c8cad7: MUST; Authorizes public keys to log in to the account. Keys used to log in to an account are explicitly required.
- 5cc49500f354bc1cf21844ee: MUST; Stores a saved Wi-Fi connection profile. Saved Wi-Fi networks are explicitly required; this row identifies the network profile, not its password.
- 3ab18b850bed1101d762fa08: MUST; Stores a saved Wi-Fi connection profile. Saved Wi-Fi networks are explicitly required; this row identifies the network profile, not its password.
- d9012fa4771e4e4686e9c967: MUST; Defines a system network interface or tunnel connection profile. The profile configures network connectivity for other programs; removal loses that saved connection capability.

## Additional homogeneous rule checks

PAM stacks: S2.2-1 and S2.2-2 require active authentication/account/session module stacks because they control access and credentials outside their reader. Manual inspection covered the first ten listed entries and raw content: ce36426d9bc200cddc900200, 274f9cc66dc198a1cc2ba58d, e581cb6387cbf187f0923388, 67912141d193bf207cf5489b, 68492d8fadb2a3e81c76739f, 12166c7ff3c49a8165a055c8, 10a6f930fb268691b4f8dc71, 5854afeab0e7e2fb6f6530cb, 35c07ada63f572ae967d102b, dc9cd820c00dfebfa30c73e7.

Firewall chains: S2.2-15 requires firewall policy; chain hooks, default verdicts and referenced chain targets implement that policy. Manual inspection covered the first ten listed entries and raw content: 717eb2770380a84a60c5c313, dda59fbc8826d393f7d01a10, 35cb6ad5449614d23bebe242, a09dad130a88e21ac58d25ca, a1543f91747b9c5a83532869, ea5d40a2dff60d224d49f01a, dd09d750d72e29a6802c0993, 68e163de5be454c2c0f3b7ff, 402a14bcdc254a1331a2d91c, 45fa13af9c9c2849fefd5d4a.

Container images: S2.2-9 and S2.2-12 require programs packaged in container images. Inventory confirms executable server/interpreter images, without establishing cache-only removal behavior. Manual inspection covered the first ten listed entries and raw content: c97d9f250787c54baa1e0b72, 70217070f9a3640192bf6d15, be195af2e23105d0bdf5c1e2, cd7cb3b2f25e9f09baa807d1, 6b15c08f7bc1a541a005da17, b1e3831b876984497b7e8d93, d15f6d19976fd46865b5f935, 51e0bcb301dea3bd5c64a3ac, cbaf6f16dab7fb21b548717b, 390e9a29d1bd114fae135522.

All remaining small categories (fewer than ten cases), individual SSH directives, and non-PAM access files were considered row by row. TSV decisions were appended and flushed; no previous rows were replaced. Verification: 797 unique subset IDs, exact set equality, valid labels, function/reason word bounds.
