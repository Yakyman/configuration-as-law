# Part 4 classification c1

Decisions use only Section 2.2 and the first indicator of Section 3. Closure membership and inventory classification vocabulary are not decision rules. No removal experiment was performed. The scripts append completed rows and preserve existing IDs.

## Evidence limitations and independence

Only the assigned input and its raw inventory were consulted. A structural inspection of the allowed raw `../in/raw/guix/group-members.json` unexpectedly exposed embedded legacy classification fields before their presence was known. Those fields were disregarded; that file was excluded from further reading. Member inspection instead uses `unowned-groups.json`. No other classification folder was consulted. Some paths named in the inventory, especially `configuration/gnu/store/`, are absent from the supplied files; a path reference alone is not evidence of its contents.

## Homogeneous rules for accounts, modules, processes, and services

R1: A row established as an operating-system account is MUST under S2.2-15. Account identity, not successful interactive login, is the criterion. Applied to 11 account rows. Ten manually checked rows in `../in/raw/guix/accounts.txt`: guix-ebda0cbba2, guix-c23681be3a, guix-27d89cb149, guix-e9ecf34b23, guix-6a022e8f54, guix-9911292f99, guix-af2a58bec6, guix-829a5eaf21, guix-1f9ebd3eec, guix-cbaf0b4232. Each has an account record with UID and GID; the records include ordinary, root, and non-login service accounts. The remaining account was inspected in the same file. The build-user row was separately checked: `../in/raw/guix/guix-builder-accounts.txt` contains ten accounts, all MUST by the same explicit sentence.

R2: A loaded kernel module is executable code running with the kernel's rights, so MUST under S2.2-10. This applies even when its current use counter is zero. Ten manually checked module records and their `.ko.zst` locations: guix-7fdc5c58fa (8021q), guix-ecd1d0957d (9p), guix-cd486effed (9pnet), guix-96c2a6c092 (9pnet_virtio), guix-ddb5a87d9a (aesni_intel), guix-baeebd18d2 (ahci), guix-13fab1e09e (bochs), guix-519f0efa4c (ccp), guix-145a20b523 (cfg80211), guix-3cd1d09ac0 (dm_crypt). Each is present in `modules.txt` with size and use information; their functions are kernel code, not values read by an application. This is the only functional property necessary for this decision.

Primary source: https://github.com/torvalds/linux/blob/master/kernel/module/Kconfig states: “Kernel modules are small pieces of compiled code which can be inserted in the running kernel”. The loaded-module inventory supplies the local observations.

R3: An executable observed as an operating-system process is MUST under S2.2-9 and S2.2-12. Grouped instances of the same executable have the same decision. Ten manually checked process-to-executable entries in `process-executables.tsv`, also matched to `processes.txt`: guix-c260909efc (PID 138), guix-d4c0f6937e (237), guix-8dd6185781 (189), guix-3d247384aa (310), guix-06cf17ff41 (377), guix-83de6c2f7f (192), guix-270c5e4acc (342), guix-92bd9a5073 (368), guix-63186abb2b (416), guix-a53c13b3d7 (370). These include daemons, desktop programs, and a launcher; their application-specific purposes do not alter the explicit process criterion. The process-table observation of `ps` also establishes a running program despite its short lifetime.

The kernel-thread group was decided separately: the captured process table lists kernel workers and memory, scheduling, and device threads. Their removal prevents kernel work (S2.2-1, S2.2-2). Primary documentation https://docs.kernel.org/core-api/workqueue.html says: “An independent thread serves as the asynchronous execution context.” The same page describes worker execution of queued kernel functions. The decision concerns the functioning execution contexts, not a requirement to preserve historical process identifiers.

R4: A Shepherd service implemented by executable lifecycle procedures is MUST under S2.2-10: the service manager executes those procedures with its own rights. A service is not its logs or cached data. Startup and shutdown procedures qualify even for one-shot, dependency-only, or currently idle services. The two rows directly describing the service-manager process and an accepted SSH process instead also satisfy R3, independently of their definitions. Primary manual https://www.gnu.org/software/shepherd/manual/shepherd.pdf states: “The configuration file contains Scheme code that uses the programming interface of the (shepherd service) module”. This passage was available through the indexed manual; direct page retrieval timed out.

Ten manually checked services in `../in/raw/guix/herd-all-service-status.txt`: guix-c7e5f38d94 (daemon PID 192), guix-a5fb612d86, guix-99b95ecba6, guix-d968cf24a8, guix-9eb7d7527b, guix-8199876f9a, guix-d5354a6cef (six console-font services, enabled with running value #t and their terminal dependencies), guix-a6ab41631c (system bus PID 138), guix-028034d635 (login daemon PID 189), guix-881cf8472f (pseudoterminal filesystem service, enabled with root-filesystem/device dependencies). Service provenance supplies matching Scheme definition names. Public source https://raw.githubusercontent.com/lfam/guix/master/gnu/services/base.scm was additionally inspected for lifecycle implementation, especially console fonts, filesystem services, virtual terminals, and entropy seeding; selected source evidence is retained in `part-4.service-source.txt`. The console-font procedure invokes setfont, filesystem services mount/unmount, and kernel-terminal procedures write kernel settings, establishing that these are not confined application-interface code.

These four rules are implemented in `part-4.parent.py` and `part-4.services.py`. Descriptions of individual service functions were checked against captured command lines, dependency/status details, and source, rather than inferred from closure membership. Additional subpart rules and their manual checks follow below; companion evidence notes supply detailed documentary excerpts and individual boundary cases.

## Exact definition sentences used by these rules

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S3-1** **Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information about what the object does, established by documentation, by observation, or by removal: in a disputed case, the object is removed on a disposable copy of the machine, and what stopped working is recorded.

- **S3-2** If what the object does remains unknown, the case yields ?.

## Store-object rules and manual checks

The two store-object segments used the following documented rules. Supplemental package evidence resolves 21 initially unknown rows; the second locale row confirms an already mandatory object. Final decisions are in `part-4.tsv`, rather than intermediate segment counts.

## Scripted rule P: documented executable package outputs

Match an inventory package name, including a documented inherited variant, to its package definition and synopsis. A documented executable program or native/interpreter library is MUST under S2.2-1/2/9/10: removal removes its installed executable capability. The criterion is executable function, not dependency-closure membership. Data-only packages, headers, fonts, certificates, schemas, aggregate profiles, and bare generated names are excluded and considered individually. A package output is a single input object when `members=1`; incidental manuals do not make it a group row.

The extraction helper finds package definitions and inherited synopses. (not published: downloaded distribution package metadata) retains neutral documentary observations, including URL and original synopsis. Current source and an older source mirror establish functional identity, not exact file lists or version equivalence. Functional descriptions in the result are paraphrases. Retrieval failures and missing generated bodies do not become evidence of executable function.

Ten manually checked applications of P:

| ID | Inspection |
|---|---|
| guix-0d48c6bf44 | Chromaprint is an audio-fingerprinting library, not stored fingerprint content. |
| guix-18b042cc42 | The session locker is an executable program, not a lock-state value. |
| guix-c8d1d95195 | The syscall-filter interface is executable library code, not a saved filter policy. |
| guix-689f8cdd35 | The HTTP library supplies networking routines. |
| guix-d385fad5dd | The Scheme JSON module is executable parsing/serialization code. |
| guix-72b5be6d4c | Multiple-precision arithmetic is implemented by library routines. |
| guix-472ca4444d | The RAID package supplies management commands, not merely array metadata. |
| guix-cab4c5bf44 | Asynchronous-I/O support is a library interface. |
| guix-6e3094f6d6 | The transfer package supplies executable networking operations. |
| guix-97eae529eb | The compression package is a program, not already-compressed user content. |


## Scripted rule C: identified interpreter and service code

Observed `primitive-load` calls establish activation code. Service provenance includes actual Scheme service expressions; the documented service language and executable source capability establish MUST under S2.2-2/10/13. Compiled service objects are directly loaded into the service manager and likewise MUST. Being generated, or called a configuration, is not an exemption. Initial uncertainty about source versus compiled loading was resolved using the capability test: recognizable executable service source can be loaded independently even when the normal boot path uses its compiled counterpart.

Ten manually checked applications of C:

| ID | Inspection |
|---|---|
| guix-4a1178fa90 | Exact activation path occurs in the saved activation script’s primitive-load list. |
| guix-196447bb11 | Same observed activation loading mechanism. |
| guix-7c626a4b70 | Same observed activation loading mechanism. |
| guix-99564c37c5 | Same observed activation loading mechanism. |
| guix-0d20337c18 | Same observed activation loading mechanism. |
| guix-928bb56800 | Same observed activation loading mechanism. |
| guix-f83a146d79 | Same observed activation loading mechanism. |
| guix-2de6dc679f | Saved boot code creates runtime state and launches the service manager. |
| guix-5782dfe617 | Provenance supplies a Scheme service expression for the time service. |
| guix-da1388031e | Compiled service-definition artifact fits the documented direct compiled loading mechanism. |



## Scripted rule U: unresolved generated-object role

Where the only surviving evidence identifies a generated store object, but neither captured contents, consuming references, nor retrieved documentation establishes its function, assign UNKNOWN under S3-1/2. This rule is about insufficient evidence, not an exemption and not a textual hole. Searches used the exact store path against the allowed inventory and configuration captures. Name resemblance alone cannot identify arbitrary generated content. Configuration roles established through a standard destination or a live command were decided separately; exact setting values are unnecessary when the established role decides the class.

Ten manually checked applications of U:

| ID | Inspection |
|---|---|
| guix-2a85615a21 | Module-import object lacks captured module bodies or a proven consuming reference. |
| guix-a1c1e67353 | Another module-import object with the same missing evidence. |
| guix-2917f3f574 | Module-import directory contents and distinct use were not captured. |
| guix-7526df5a8f | Additional module-import directory lacks captured module bodies and a proven consumer. |
| guix-3cc7726cb4 | Additional module-import directory lacks captured module bodies and a proven consumer. |
| guix-f3ca6aa7c1 | Artwork checkout name does not establish whether this checkout contains only visual content. |
| guix-4693999f1c | Compiled module aggregate lacks the relevant module contents or proven load reference. |
| guix-a36c632a1b | A second compiled aggregate has the same evidence limitation. |
| guix-9b6df1084f | A third compiled aggregate has the same evidence limitation. |
| guix-5d1d3b6b13 | Skeleton directory destination is known, but full content and executable portions are not. |


## Rules and manual checks

**P: executable software outputs.** A documented native executable, driver, runtime library, or interpreter module is MUST under S2.2-1, S2.2-2, S2.2-9 and S2.2-10. Removing the entire output prevents invoking its code or dependent operations. This rule is applied only to identified software outputs, not documentation, images, generated settings, protocol descriptions, or caches. Package names are matched to their own definitions or documented minimal variants; an inventory closure label is never the basis. The following ten rows were individually read against their package descriptions and checked as software rather than assets:

- guix-5e69024ed7: video capture utilities.
- guix-c451c2dd83: executable widget toolkit routines.
- guix-b087324c7e: account authentication commands.
- guix-f0f9aee420: Perl socket encryption module.
- guix-a5258762b5: desktop event playback library.
- guix-be089e96b2: color-management service.
- guix-47c22e3cb7: XML parsing library.
- guix-cd4404b821: executable audio plugins.
- guix-49b16208f4: network commands.
- guix-94e54f1dfa: desktop helper library.

**A: directly evaluated activation actions.** A file explicitly listed in `configuration/run/current-system/activate` and passed to `primitive-load` is MUST under S2.2-10 and S2.2-13. The saved expression uses `(primitive-load action)` inside `save-module-excursion`; the rule concerns executable action files, not values-only settings. Nine assigned rows match. Ten manual checks, including one additional input row solely to check the rule, were: guix-360efff222, guix-54c3549e3c, guix-ed7d9f5fc5, guix-7db6ef3aab, guix-4dbd370b6f, guix-51a7118274, guix-12c0b22b0a, guix-3eaf0083db, guix-c862ad9abd, guix-4a1178fa90. Each exact store path appears in that action list; the last row belongs to the other slice and is not output here.

**G: directly loaded compiled service definitions.** These are MUST under S2.2-2 and S2.2-10. The pinned generator loads the compiled file directly, so deleting it prevents service registration; this is not merely a slower module-cache miss. Ten manually checked definitions: guix-218dace6bc (time), guix-9250837ddd (discovery), guix-0d9b370edb (remote login), guix-e9ff5d3e91 (logging), guix-584e17b8e9 (timer), guix-b0e790d9d9 (console font), guix-06f908f7b3 (shared-memory mount), guix-b8b2e33f43 (console font), guix-80821e9370 (store mount), guix-9f4c6e2fbf (devices). The source file/service identity and compiled-name transformation were checked.

**S: executable Scheme service definitions.** These are MUST under S2.2-2, S2.2-10 and S2.2-13. Raw `../in/raw/guix/service-provenance.tsv` records an actual service constructor expression for the source file; the public generator establishes that its body defines service procedures. The conclusion is about interpreter-executable capability, not a claim that normal boot chooses the source instead of its compiled counterpart. Ten manual checks against the source expressions: guix-7d2ba848d0 (console font), guix-d83bcfd4e4 (random seed), guix-f3806e7f4d (control-group mount), guix-e1e9bab070 (loopback), guix-5dec5147fc (remote login), guix-1e02d84784 (terminal), guix-ef2b10eb77 (terminal), guix-8de9a639ef (system naming), guix-e5e5836647 (console font), guix-e6bdf0fcbb (runtime mount).

**M: identified package-management module nodes.** Public `guix/self.scm` explicitly constructs these names with `scheme-node`, producing executable Scheme modules, source trees, or bundles linking both source and compiled trees. Those identified code objects are MUST under S2.2-2 and S2.2-10. The rule does not extend to arbitrary unreferenced `module-import` basenames. Ten manually checked nodes: guix-40ac3ffda1 (base packages bundle), guix-c9c3fe4c21 (CLI bundle), guix-403ebb9bec (CLI core source), guix-1d030f4b23 (module bundle), guix-b1cda82d20 (system test bundle), guix-9e2b09e306 (base packages), guix-d6f4da0567 (additional modules), guix-9849b393fe (CLI core), guix-3321d7b173 (base package source), guix-0c0c8b4f78 (CLI). Source and bundle identity was read from generator structure, rather than inferred from the closure inventory.

All other rows were considered individually; the explicit row-by-row decisions are retained in the generation scripts and final TSV.


## Scripted rule

Only log rows were classified by a homogeneous rule: an inventoried service, build, display, or login log records past events and is NOT under S2.2-6, "records of the past—logs, history;". This rule applies to the 12 rows under the system log directory and the rotated resize log. Hand checks of ten input rows and corresponding group membership:

- guix-a4963ec3b5: display server log.
- guix-2cd84ac792: service-discovery daemon log.
- guix-b6a2c8e4dd: message-bus daemon log.
- guix-5ba0b35443: debug log.
- guix-985ad63959: build derivation logs, including compressed build records.
- guix-43c963f378: package-store daemon log.
- guix-698c23461f: last-login history.
- guix-91a21a61f1: system message log.
- guix-e684d315eb: clock synchronization log.
- guix-4ac29aa55a: authentication log.

All other rows were decided individually. The assignment script serializes explicit row decisions, rather than applying inferred classes to unseen rows. Small repeated decisions (two debugger files, two interpreter files, two editor option files, two compiled caches) were checked individually against each inventory row.


## Supplemental native-code checks

## Manual checks

The following ten representative native-code rows were checked against their own package source rather than assumed from a library-shaped name: guix-9230f521b9 (barcode decoding), guix-22c51eb1c5 (key bindings), guix-96a7070d1a (secure transport), guix-525e566986 (digests), guix-191f4a26d4 (password hashing), guix-35b0a2de06 (networking), guix-ff5349cd06 (NFS), guix-d13a209977 (calendar processing), guix-b44271a638 (synchronization), guix-ebe1a53639 (data structures). The common conclusion follows from S2.2-10, "code that another program executes must be recorded if the program runs it with the program’s own rights". Utility, wrapper, locale, ISO-content, and device-rule rows were checked separately.

Raw source fetches for some large modules returned connection resets. Where necessary, the public source was read through the repository contents API or rendered source page. Only role evidence was extracted. No software was installed, built, or executed.

## Companion evidence and final boundary cases

- [First store-object evidence](part-4.1.notes.md) gives the source URLs and documentary excerpts supporting its rules and individual decisions. The paired boot compiled-module object is HOLE because source fallback satisfies the cache exemption while interpreter execution satisfies the code requirement.
- [Second store-object evidence](part-4.2.notes.md) documents the second paired module-cache case, directly loaded compiled services, shared-library configuration, and daemon-setting scope ambiguities.
- [Stored-object evidence](part-4.3.notes.md) gives individual stored-object reasoning and explicit member mappings for both MIXED groups. Home compiled-support members lack captured source-fallback pairing and are not assumed to match the two inspected system pairs.
- [Supplemental package evidence](part-4.packages.notes.md) supplies primary documentation for the additional native libraries, command wrappers, utilities, locale definitions, device-switch rules, and ISO reference content.

The metadata files retain documentary identities and source descriptions for inventory-relevant packages. No unrelated classification was used. The mechanical checks below validate the files; they do not constitute independent acceptance of the classification.

## Additional evidence boundary

For guix-0abb5d3f0a, the upstream topology repository (https://github.com/alsa-project/alsa-topology-conf) says: “Use 'make firmware' to compile and install the topology files to the /lib/firmware tree.” This establishes the upstream source format and intended compilation route. The captured inventory does not establish the particular output's compiled firmware, source members, or consuming device/build path, so its removal-relevant function remains UNKNOWN rather than assuming a device effect from the package label.

## Final mechanical verification

`part-4.validate.py` merged all completed segments and the supplemental package evidence, then reread the delivered TSV. Input and output each contain exactly 1,143 distinct IDs, with the same set and each ID occurring once. The header, six fields, UTF-8 decoding, permitted decisions, 15-word descriptions, 30-word reasons, and cited raw-file existence passed. No input row was skipped or added. `part-4.done` contains the final decision counts: MUST 998, NOT 42, HOLE 13, UNKNOWN 88, MIXED 2.
