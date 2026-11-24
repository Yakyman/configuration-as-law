# Code-candidate subset: independent classification notes

Scope: 619 input rows. The inventory label was not used as a class. All objects have persistent filesystem metadata. None joins to an installed per-file manifest in (not published: over 20 MB). A missing match is not a proof of non-package origin: `A3/in/raw/developer/metadata.json` records incomplete ownership, unavailable adapters, and missing language-package file provenance. Installation reason is consulted in package object metadata but cannot determine the origin or integrity of an individual file absent a manifest. Prefix signatures do not prove unchanged package bytes. No experiment was performed.

## Exact deciding text

- S8.2-6: "What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order."
- S8.2-7: "Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?"
- S8.2-9: "Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?"
- S8.2-15: "Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines."
- S8.2-16: "What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package."
- S8.2-20: "A file containing code that cannot be executed on this computer is not a program."
- S8.2-23: "A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code."

## Homogeneous rules

R1, registry: the 76 `.npm` binary response caches are RECORD. The documented purpose is data caching, not executable package payload. Package metadata downloaded from a registry is not itself an installed package. S8.2-23 distinguishes data from code even though the inventory marks a shebang; S8.2-15 therefore applies. The file permission is non-executable in all 76 rows. Official documentation, https://bun.sh/docs/pm/cli/install: "Bun uses a binary format for caching npm registry responses." This establishes the function; the inventory establishes the stored instances and persistence.

R2, payload: 467 files in package-manager/distribution payload trees lack a per-file package provenance and integrity record. UNKNOWN follows from the missing first-question facts, not from their directory names or permissions. The rule applies to an evidentially homogeneous deficiency, not a claim that all these objects contain code. An unchanged received file answers question one; a modified or independently supplied file requires later questions and a different label. Native reason facts cannot cure missing file provenance. Even foreign-architecture executables and non-code maps can be installed objects if unchanged package parts. Names alone cannot demonstrate their unmodified status. Documentation establishes functions but cannot establish these machine-specific facts.

R3, project: 68 project-tree files lack recorded supply/generation lineage. UNKNOWN records missing package origin or whether system derivation supplies coverage under S8.2-16. Project location does not prove material, and a script marker does not establish compatibility of a fixture. A general-purpose checkout or copy is not automatically an installer. No declaration-source or build-origin relation for these individual files is present in the supplied evidence. These missing facts change the result; this is not a textual gap.

Official context checked: https://github.com/JuliaLang/juliaup describes "Julia installer and version manager"; its add/remove operations establish installer purpose, not per-file integrity. https://git-scm.com/docs/git-init states "The sample hooks are all disabled by default." Disabled hook automation does not prove code cannot be executed manually; nor does a matching filename establish this particular copy's origin. Therefore Git sample hooks were not automatically labeled records or assigned derived coverage.

## Hand checks

For each listed row, the input metadata, path role, size, shebang/executable flags, persistence and absent manifest match were individually inspected. R1 checks confirm documented binary manifest-cache names. R2 deliberately includes data maps, archived fixtures, libraries and a foreign-platform executable to check that permissions do not replace question one. R3 includes scripts, hook samples, a tiny shell fixture and vendor code to check provenance rather than infer it from the project directory.

R1: developer-caf849f32050f8f8d12ca9c9, developer-1351463a6c67a00b6ee824ce, developer-4d82397294549802f9a0a5d6, developer-13f3e979b7195c668b372e8e, developer-704817ab60b35f13c0e2005e, developer-da2f14a256b5b59480761bc6, developer-6a6f2d7a3174a472748920b6, developer-e59844a05db92d3fa2608cb5, developer-af3b6882902935de10d39fb1, developer-cbfa619e0e3a123f9def8ee1.

R2: developer-2b53d455423cfccaa4ae8081, developer-695307ca85aebccd79b75006, developer-3e0790e8049f62cc71573ccc, developer-372014b2910fad6fad91da8e, developer-ed2ac74ec772f402f717c2df, developer-95586c676e3caba1d88defbc, developer-b965a1722c56137354b94d1e, developer-b288f685882c7c05021a4cd0, developer-48981bee5071dfce5d670349, developer-e0df0b0557ce677d8b3377f1.

R3: developer-9c4f107f9425a7455cd22c18, developer-8e112490c91a0cf94ff6eb1a, developer-5b44798ac7cac25ba65ace08, developer-f5570a6f0e6ae6957e5d423e, developer-4bfe0e664e563e64a225a044, developer-dd8872530d8a274849e8595e, developer-cca6f855eac328e8e043ca40, developer-e30974b2a09f5aa1302aaa27, developer-2c0fd3c3d00e154b409fc979, developer-6be81830b9c95010f8cbead7.

## Eight individual decisions

The two shell startup files differ from the untouched-base signatures and sizes. Both are shell code, but the recorded changes have no author or generator provenance; own versus derived remains unknown. Their initial and final metadata are in the respective `raw/0004-filesystem.out` files and creation provenance remains unknown in `configuration-origin.tsv`.

The runtime executable and two Python-tool executables have neither a manifest match nor full installation digest; installation origin and integrity remain unknown. The project-summary script is executable but the inventory does not preserve its source or creation method. The hook-manager command wrapper might be generated or received; its wrapper creation provenance is absent. The compiler runtime library lacks a current manifest match despite the compiler runtime package being present; package presence alone does not establish that this file remains as received.

Checks: 619 unique output IDs, exactly the subset IDs; 543 UNKNOWN and 76 RECORD. All output descriptions and reasons satisfy the word limits. Output is appended and flushed row by row; restarting the script preserves existing rows.
