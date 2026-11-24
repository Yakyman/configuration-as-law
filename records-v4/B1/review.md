# Independent review of B1

Scope: 88 rows in `part-install/part.tsv`, `part-config/part.tsv`, and `raw/root-part.tsv`, with their source and gap files. The rows were checked against (not published: orchestration or scratch), `SENTENCES.md`, Sections 8, 9.3, and A.4.3, and `PROTOCOL.md`. No row was changed.

## Must-fix findings

1. **C1.3 maps the alternate database twice and inconsistently.** Leaf a includes the database at `--dbpath` but classifies all of a as an installed object; leaf b names the same database and classifies it as a program record. Resolution: make the payload and database distinct objects; Q1 applies only to the package payload, while the generated database reaches Q4.

2. **C2.1, C2.2, C2.3, and C2.5 send executable archives/caches to Q4 without testing Q2.** C7.09 and R06 establish that code in a suitable ZIP archive can execute directly. A wheel cache, retained wheel, or generated wheel therefore cannot be classified categorically as a program record or material. Resolution: split HTTP/cache metadata from each archive; a loadable archive containing executable modules is a program at Q2, while a format that cannot execute proceeds to Q3/Q4. C2.2 must also split the cache from `package-lock.json`, which are separate objects with potentially different origins.

3. **C2.6 gives the wrong Q4 origin to the path-only `.pth` file.** The leaf says it is locally supplied, but the kind says program-created program record. Resolution: after Q1 and Q2 fail, decide Q3 from the actual value: an executable `import` line is already Q2; a value that itself selects a launch/access path is Q3; otherwise a person-created or person-brought path-only file is material at Q4. This factual split does not establish another textual gap.

4. **C3.1 groups repository configuration and refs as one Q4 object.** This conflicts with C3.2, where chosen remote URL/policy values are correctly treated as settings. Resolution: classify each object separately: chosen persistent remote/policy values reach Q3 and need their own line; generated refs and transaction state can reach Q4 when they are only installer records.

5. **C4.3 overuses `FACT_UNKNOWN` for the documented updater branch.** The row already establishes a dedicated updater whose purpose is to replace an executable. That is enough for `[BUILTIN]` under S8.1-7; removal documentation is needed only to call it an installer under S8.1-4. Resolution: retain `[GENERAL]` for ordinary download/copy/sync and `[BUILTIN]` for the updater, and reserve unknown status for additional outputs that are actually unspecified.

6. **The C5 compiler/build routes are too broadly `[GENERAL]`.** Under the literal definitions, generating or copying executable output changes what is installed, and the documented purpose of a compiler/build/install tool includes that operation. The explicit general-purpose exclusions cover copying, link creation, shell, and editor operations, not the specialized compiler/build operation. Resolution: in C5.1, C5.2, C5.3, and the corresponding compiler operation in C5.5, mark compiler/build/output-generation functionality `[BUILTIN]`; keep shell, manual copying, and manual link creation `[GENERAL]`. CMake install lacks the removal fact required for `[INSTALLER]`, but that does not prevent `[BUILTIN]`.

7. **C6.3 contradicts itself about transient service parameters.** The kind cell puts registration and properties wholly under S8.2-5, while the record cell requires an own line for the chosen parameters. Resolution: separate the transient unit/process/relationship, which follows its creator under S8.2-5, from any person-chosen service parameter that the computer obeys, which is a Q3 setting with an own line.

8. **C6.5 omits the extra saved code named by the variant.** The row covers the generator and cron command text but not the file/code that the command loads. Resolution: add each retained loaded input as its own object and test Q1 before Q2; if the actual target is not supplied, the row cannot be fully `DECIDED` for that branch.

9. **C8.05 treats a transient shell snippet as a second persistent program and misroutes configuration.** Git reads the stored value, then supplies a shell snippet at runtime; that transient snippet falls under S8.2-5 rather than receiving another S8.2-16 line. The retained launch-selector value remains the Q3 object. Git is a general-purpose program and S8.1-8 supplies no configuration-function exception, so its configuration command is `[GENERAL]`, not `[BUILTIN]`. The retained Makefile recipe remains a separate Q2 program.

10. **C8.07 applies Q1 to generated extension registration.** Registration/default permission state created during installation is not thereby “obtained as part of” the package and unchanged as received. S8.2-17 instead presupposes that an installation-created default is a setting covered by the package line. Resolution: keep the extension bundle at Q1; send registration/default permission values to Q3, package-covered when created as installation defaults and own-line when later chosen. The present sources also do not document the asserted registration artifact, so either add direct documentation or state only the documented preference/permission object.

11. **C7.19 invents a persistent cache object from a sandbox source.** R13 supports confinement, but it does not establish that a saved web-code cache entry exists, what its bytes are, or that the saved entry itself is executable code. Resolution: keep in-memory web code under S8.2-5 and apply S8.2-21 only to code whose inability to launch programs or change installed objects/settings is established; remove the cache object or provide direct cache/execution evidence and classify that concrete object.

12. **The law cells in both part files do not quote S8.3-6 exactly.** The numbered sentence begins “P4. Law.”; the part rows quote only the remainder. Several cells also paraphrase the imported A.4.3 success/removal rule rather than identifying the quoted source passage. Resolution: use the complete numbered sentence text when claiming an exact sentence quotation, and label Section 9.3/A.4.3 quotations separately from local IDs.

## Status and gap conclusions

- **C8.08 is the only supported textual gap.** The stored theme value reaches Q4, while the home-page value has two literal S8.2-14 outcomes because the text does not define whether automatic navigation “launches something.” The gap file states the two recording consequences correctly. The factual source should establish actual home-page opening behavior, not merely that preferences are stored.
- **The twelve M rows may remain `FACT_UNKNOWN`.** They name cross-channel obligations, not a concrete acting tool or post-operation inventory; their example artifacts are expressly representative rather than asserted facts. Missing artifact identity, provenance, chosen value, and actor are facts, so this is not a gap. Section 8.5 excludes choosing the enforcement/storage mechanism; it does not turn unspecified actual artifacts into decided objects. Any claim about how a system must implement atomicity, admission, or prevention should therefore be marked outside the definition, while object classification remains fact-unknown.
- The runtime-first treatment in C7.03-C7.05 and C7.15-C7.16 correctly applies S8.2-5 before Q1-Q4. C7.19 may use S8.2-21 only for the expressly confined code, while each renderer/helper process executable still requires its own Q1/Q2 decision under S8.2-22.

## Disposition after revision

Reviewed `CHANNELS-V4.tsv` and `GAPS.md` after the corrections. The table has 88 rows and eight fields per row; its reported distribution is 60 `DECIDED`, 27 `FACT_UNKNOWN`, one `TWO_WAYS`, and no `NOT_DECIDED`.

Earlier findings 1-10 and 12 are resolved: C1.3 now separates the database; C2.1/C2.2/C2.3/C2.5 split executable archives from non-code records and use fact-unknown where compatibility is absent; C2.6 now applies the S8.2-14 “otherwise” branch without inventing program origin; C3.1 separates refs and chosen repository policy; C4.3 distinguishes the built-in updater from general download/copy; C5.1-C5.3 and C5.5 use the specialized built-in route; C6.3 no longer invents a persistent parent for transient properties; C6.5 includes the unidentified loaded input and is fact-unknown; C8.05 treats the extracted snippet as runtime and uses the general route; C8.07 separates the installed bundle, launch setting, and generated metadata with direct evidence; and the law cells quote the complete numbered sentences. C7.19 now has direct evidence for the cache object and code reuse, resolving the evidence portion of finding 11.

Two concrete corrections remain before acceptance:

1. **C5.4 still routes compiler/linker output as `[GENERAL]`.** It is the same specialized executable-producing functionality as C5.1-C5.3 and C5.5 and therefore is `[BUILTIN]` under the adopted literal resolution. Manual copying remains `[GENERAL]`; privileged direct overwrite outside built-in tools is `[BREAKING]`.
2. **C7.19 has not established the whole S8.2-21 capability condition.** The saved confinement excerpt establishes that sandboxed code cannot make persistent changes, but S8.2-21 additionally requires that the code cannot itself launch programs. The cache and execution evidence establishes Q2, not that second exemption fact. Add direct evidence or an explicit fixed premise covering inability to launch programs; otherwise the cache program's recording duty remains `FACT_UNKNOWN`.

`GAPS.md` is accepted: C8.08 remains the sole textual gap, documents actual home-page opening behavior, gives both literal S8.2-14 readings, and keeps enforcement mechanism outside the result. The twelve M rows remain defensible as `FACT_UNKNOWN` and add no gap.

### Final acceptance

The two remaining corrections were applied and verified. C5.4 now separates specialized compiler/linker replacement (`[BUILTIN]`), manual replacement (`[GENERAL]`), and privileged outside-tool bypass (`[BREAKING]`). C7.19 keeps the documented saved cache entry at Q2 but makes the S8.2-21 recording exemption `FACT_UNKNOWN` because inability to launch programs is not established. This is the required distinction between a known program object and an unknown exemption fact.

C7.24 was also rechecked after its input premise was restored: the saved instruction file reaches Q2 because the fixed variant says the dispatcher executes it with its own rights; non-file instruction storage follows S8.2-5; unidentified persistent outputs and documented tool purpose remain fact-unknown. This is consistent with the ordered questions and does not add a gap.

`CHANNELS-V4.tsv` and `GAPS.md` are accepted. Final verified distribution: 59 `DECIDED`, 28 `FACT_UNKNOWN`, one `TWO_WAYS`, zero `NOT_DECIDED`; 88 rows total. The sole textual gap remains C8.08.
