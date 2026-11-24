# Independent adversarial review

This review applies the fixed text literally. It accepts a card only when a documented real object produces different required declarations or different property applicability, not merely two possible names. Cases expressly delegated to design by Section 8.5 are excluded. Cases sharing one missing criterion are merged.

## Final scope candidate: remote files in an NFS root

**Verdict: reject under the declaration-difference filter.**

The real situation is a diskless Linux client whose root filesystem is mounted from NFS. The kernel documentation calls the machine using the filesystem the “client,” calls the NFS machine the “server,” and defines `<root-dir>` as the “Name of the directory on the server to mount as root.” Source: https://docs.kernel.org/admin-guide/nfs/nfsroot.html. Consider an executable file in that root directory which the client has not yet executed or otherwise copied into local memory.

S8.2-3 says that the recording rule applies to “objects that are on the computer,” but the text does not define whether `on` means physically stored by that computer or present in its mounted filesystem namespace. The primary source makes both descriptions true: the bytes remain in a directory on the server, while that directory is the client's root filesystem.

At the scope-label level, the readings appear to produce opposite recording duties:

- Under physical presence, the unexecuted file remains on the server and is outside S8.2-3 on the client. It need not be recorded in the client's declaration.
- Under namespace presence, the file is on the client because it is in the client's mounted root. S8.2-9 then answers yes because the client can execute it, and S8.2-10 makes it a program belonging to what is installed, which must count as recorded under S8.2-1 and S8.2-16.

The strongest scope objection is that mounting the directory “as root” makes ordinary software usage decisive: programs in the root filesystem are normally described as being on the client, regardless of storage hardware. That is a natural reading but not a textual criterion. The same documentation expressly locates the directory on the server, and no sentence says that namespace accessibility is sufficient for S8.2-3.

S8.1-9 does not resolve the scope gate. It says when a program is in force if it runs or can be started; it does not say that everything startable is therefore on the computer. S8.2-9 likewise classifies an object only after S8.2-3 has put it within the rule's scope. S8.2-5 excludes a runtime mount point as a separate object and assigns it to its creating setting or program, but the persistent files in the server directory are not mount points and do not exist only while the client runs.

The strict card filter nevertheless requires a different complete declaration or property judgment, and the candidate does not establish one. Both readings require the client declaration to record the NFS root as a filesystem setting under S8.2-13 and S8.2-17. That line necessarily identifies the root source and required mount state. Under the namespace-presence reading, the same line can record an executable under S8.2-16 as “a line from which the system itself built or obtained it.” If the line takes the server directory's entries as an external set, S8.2-18 also makes the named source what counts as recorded. The physical-presence reading needs the NFS setting line but places the executable outside scope. The resulting declaration can therefore be identical, and P1 can hold under both readings.

The fact that mounting attaches a namespace without fetching untouched file bytes does not restore the card. Treating “obtained” as requiring a local byte copy would add a criterion that S8.2-16 does not state. Treating a directory tree as outside S8.2-18 because it is not called a list would add another uncertain premise. No supplied complete declaration forces an own line for the remote executable under the namespace reading while avoiding the already mandatory NFS-source line.

The term “on the computer” remains linguistically open for this situation, but on the documented object it changes only the route by which the same declaration is assessed. It does not meet the required declaration-difference or property-difference threshold and is rejected.

## Strongest candidate after final recheck

### 1. Privilege domain in a rootless user namespace

**Verdict: reject.**

The refined real object is `/etc/sudoers` in a writable rootless container root filesystem. The documented default mode is 0440, readable by owner and group but writable by neither. Source: https://www.sudo.ws/docs/man/1.9.14/sudoers.man.pdf. Container UID 0 retains namespace `CAP_DAC_OVERRIDE` and appends an access-rule entry through shell redirection. The capability is necessary to bypass the file's write-permission bits; ordinary file ownership does not suffice.

The changed file is no longer unchanged package content for Q1. It is read as policy values rather than executed code, so Q2 does not apply. It is an access rule under S8.2-13 and, independently, a value granting access under S8.2-14, so it is a setting that requires its own line under S8.2-17. The shell is a general-purpose program outside the built-in tools under S8.1-8. The case therefore supplies a concrete direct setting change past the declaration.

The privilege evidence resolves rather than opens S8.1-15. `capabilities(7)` says that effective UID 0 is “referred to as superuser or root” and that Linux capabilities are distinct units of “privileges traditionally associated with superuser.” It defines `CAP_DAC_OVERRIDE` as the capability to bypass file read, write, and execute permission checks. Source: https://www.man7.org/linux/man-pages/man7/capabilities.7.html. The user-namespace documentation says that a process can have UID 0 and full privileges inside its user namespace while being unprivileged outside, and that a capability in a user namespace permits privileged operations on resources governed by that namespace. Source: https://www.man7.org/linux/man-pages/man7/user_namespaces.7.html.

The direct append is therefore made through a privilege traditionally associated with superuser, by a process that is UID 0 in the governing namespace, against a resource governed there. It meets S8.1-15 without any additional premise. The state is breaking and S8.3-1 excludes it from P1 and P4.

The proposed contrary reading counts only privilege in the initial user namespace. S8.1-15 contains no “host,” “global,” or “initial user namespace” qualification. Adding one would violate the literal-reading rule. The fact that the process lacks power over resources outside its namespace does not negate the superuser privilege actually used on this file. Namespace-local accounts, mounts, network settings, and other capability-mediated changes share the same resolution and do not create separate cards.

This is the candidate's strongest self-refutation and is sufficient to reject it.

## Rejected candidate cards

### Derivation relation in S8.2-16

**Verdict: reject after recheck.** The proposed Python bytecode cache does not produce different complete declarations. The personal `.py` source is itself executable code under S8.2-9. If it can launch programs or change installed objects or settings, S8.2-21 does not exempt it, so its own mandatory line covers the compiled `.pyc` under the narrow reading. If the source cannot do those things, both the source and equivalent bytecode fall within the same S8.2-21 recording exception. The compiler-line and source-line readings therefore do not establish a declaration difference for this witness.

A compiler can create real output code from source typed on standard input. The compiler documentation states that `-o` places the primary executable or object output in a file and that `-x` supplies the input language; the compiler driver's `-` input rule identifies this case as “input is from standard input.” Sources: https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html and https://gcc.gnu.org/pipermail/gcc-patches/2025-November/700204.html. S8.2-4 would make the typed command a person's action rather than an object. This still does not preserve the broad tool-provenance reading. Section 8.6 expressly says that executable program history “was not built from what is recorded” and therefore needs its own line. Because the program that recorded that history can itself be recorded, the example rejects the proposition that a recorded generating tool alone makes its generated code built from a recorded line. The ordinary narrow reading of S8.2-16 and the text's own worked example agree. No derivation card survives.

### Restricted interpreted code, including the GNU `join.awk` function

**Verdict: reject.** A nonpackaged copy executed by a recorded `gawk` interpreter is code under S8.2-9 and a program under S8.2-10. The documented function only concatenates array elements and separator strings; it does not launch a program or change what is installed or a computer setting. Source: https://www.gnu.org/software/gawk/manual/html_node/Join-Function.html.

S8.2-21 is an explicit, narrower recording exception: qualifying code inside a recorded program “need not be recorded.” S8.2-6 says the ordered questions decide **what an object is** and that clarifications do not change that order. It therefore preserves the Q2 category, but it does not turn the general recording consequence of S8.2-10 into an exception to the explicit recording exception. The ordinary specific-exception reading already settles the duty: the function is a program that need not be recorded. There are no opposite required declarations.

The same reasoning rejects a separate card for PAC functions or other sandboxed code unless the code itself has the forbidden capability. Disagreement over indirect influence is not enough when the concrete function merely returns a value.

### Mixed SQLite database and object granularity

**Verdict: reject on the supplied witness.** The sources establish that trigger SQL is stored in the database schema and that a trigger normally shares a database with its table. They do not establish opposite recording duties. A normal SQLite trigger does not itself launch programs or change what is installed or computer settings, so even if its stored SQL is isolated as Q2 code, S8.2-21 permits omission. Treating the whole database file as the object also does not make the ordinary table records mandatory on the supplied facts. The proposed whole-file versus trigger-entry boundary therefore changes names or extent without demonstrating a required declaration difference.

The SSH `Match exec` example does not rescue this card. The documented configuration value causes the SSH client to execute a command under the user's shell, which makes the launching value a setting under S8.2-14. The source does not show that the whole configuration file is executed as code rather than read as values. No accepted card follows from the file boundary alone.

An untrusted PostgreSQL PL/Python function is a stronger restricted-code witness but still does not establish the object-unit card. The catalog documentation states that `pg_proc.prosrc` contains the function's source text, while the same catalog row contains invocation data, settings, and access privileges. Source: https://www.postgresql.org/docs/16/catalog-pg-proc.html. The PL/Python documentation states that untrusted function code can do anything available to the database administrator, so S8.2-21 does not exempt that source text. Source: https://www.postgresql.org/docs/17/plpython.html.

The physical relation file, however, is read as database values; the language handler later executes the extracted `prosrc` value. S8.2-23 directly says that a file a program only reads as values does not count as code. Thus the executable source value is Q2 code and must be recorded, while the containing binary relation file does not become code as a whole. Treating the entire relation as executed would contradict the documented consumption mode and S8.2-23 rather than expose two unresolved units. The required extent is the stored function source, not every ordinary catalog field or the whole relation file.

### Modified package coverage

**Verdict: reject as a separate card.** S8.2-7 conditions the Q1 installed-object category on an object remaining as received. S8.2-16 does not repeat that condition when it says that what is installed may be recorded by the line of the package as part of which it was obtained. The literal result is broad package-line coverage after modification. Importing the earlier condition into S8.2-16 would add text rather than expose two equally stated rules. Any information-content concern belongs to the Understanding issue below, not a second recording-line card.

### Service enablement

**Verdict: reject.** The service-manager documentation expressly labels a static unit “not enabled.” Source: https://www.freedesktop.org/software/systemd/man/258/systemctl.html. That direct implementation meaning supplies a determinate S8.1-11 result. Eligibility for dependency or socket activation is a different fact, not an equally stated definition of enabled. S8.1-12 also lets a line state the required service state. The candidate does not produce opposite declarations or an unavoidable P2 result.

### Temporal executable capability during suspension

**Verdict: reject.** The kernel documentation establishes that user-space code cannot execute during a sleep state. Source: https://docs.kernel.org/admin-guide/pm/sleep-states.html. It does not establish that a recorded program ceases to be one that “can be started” in the dispositional sense used by S8.1-9 and S8.2-9. Ordinary resumption is part of the computer's ability to start it. The immediate-start reading is possible only by adding a time horizon absent from the sentence, and it produces no separate declaration. This is too weak for a card.

### Generated SSH host key and Understanding

**Verdict: reject as an intrinsic contradiction.** The sources establish real installation-time generation and random key bytes. They do not establish the candidate's crucial classification. S8.2-11 requires a value chosen by a person for Q3. The random private-key bytes are not person-chosen. The `HostKey` path is the service parameter; the random file contents are distinct key material produced by a program. Calling the bytes themselves a service parameter skips that distinction.

Even if package coverage is assumed, S8.4's claim that the declaration shows “how it is configured” admits the ordinary reading that a line shows the specified generative configuration rather than every generated secret byte. The competing concrete-value reading exposes an implication ambiguity in the Understanding consequence, but the supplied case does not make Sections 8.1–8.3 require both disclosure and nondisclosure, nor does it force incompatible declarations. The Reproducibility sentence promises the result described by the line, so it also does not require identical random bytes.

The modified-package and environmental-default examples share this information-content issue and do not become additional cards.

### Remaining property-pair candidates

**Verdict: reject as recorded in the candidate table.** Enabled-but-stopped services, built-in service-manager changes, persistent program records, optional exact recording, external lists, non-atomic application changes, and source variation either satisfy both properties under a coherent line, demonstrate only that an existing implementation is nonconforming, or fall under an express exception. Section 8.5 expressly removes storage and removal of program records and material, enforcement mechanism, declaration protection, and edit-effect timing from the definition. None yields an additional contradiction.

## Consolidated result

No card survives the strict filter. The NFS-root scope term is linguistically open, but the mandatory NFS-source setting line can also cover namespace-visible remote files under S8.2-16 or S8.2-18, so no different complete declaration or property judgment is forced. The namespace-privilege candidate fails because its operation demonstrably uses a capability defined as a unit of superuser privilege. The derivation candidate fails because its original source is mandatory code under the same conditions as its output, while Section 8.6 rejects tool-only provenance. The remaining candidates either have an explicit deciding sentence, change only a name, lack opposite declarations, fall outside the definition, or show only a nonconforming implementation.
