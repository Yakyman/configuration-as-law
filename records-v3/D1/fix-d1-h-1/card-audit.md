# Independent card reasoning audit

Recorded 2026-11-22 UTC. This is a bounded reasoning audit for findings 2, 3, 4 and 6, not final acceptance. No probes or frozen-input changes. Read the named task, text and sentence index, original result/review, hole cards, selected joined/adjudication records, and saved review evidence. No files in the unlisted adjudication work folder were read. Earlier review references to that folder are not fresh verification of their underlying facts.

## Literal sentences

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.2-11: “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.”

S2.2-12: “This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

S2.2-16: “the boot order and device firmware must be recorded where the system is able to change them.”

S3-2: “If what the object does remains unknown, the case yields ?.”

## Findings 2 and 3: package metadata and card 3

**Finding 2 is valid against the blanket metadata inference.** A dependency field naming an executable is not evidence that the package contains or runs that executable. A forward requirement and an installed reverse requirement are different relations, and neither alone establishes a positive removal test without choosing how later package-manager actions enter the comparison. Actual executable payload or documented script execution can give an independent reason under S2.2-9/10, but the existence of a requirement on `/bin/sh` does not prove that reason.

For example, `tumbleweed-25d4e59fef6a08262890c4c4` (`root:google-roboto-fonts`) is described in its adjudication note as font files and metadata/licences, no code. Its metadata-based refutation in `../review/cards-1-4.md` therefore does not refute the presentation-content question. Card 1 remains CONFIRMED; the one-row extent must be recomputed rather than retained.

For card 2, `mint-cef67297df4b26083898d0be` (`root:libdrm-common`) has an established GPU-name-table role in `../adjudication/rows.tsv`. Absence of exact dependency metadata cannot alone convert this known role into unknown behavior under S3-2 once metadata is no longer an independent deciding rule. Card 2's unconditional database exemption argument is too strong: S2.2-4 includes a behavior-preservation condition. Nevertheless, its descriptive lookup-data examples retain the content/capability boundary problem of card 1. A whole-card REFUTED disposition based on metadata is unsupported. Trust-policy and transport-policy objects may have independent behavioral reasons; they cannot make all descriptive tables resolved by association.

**Finding 3 is valid.** The note for `tumbleweed-8ffe304c89c8c7e36f097d58` (`root:patterns-fonts-fonts`) says its dependencies steer later package-manager runs. `mint-7588ce4f54fd792c9bd42dd5` (`root:libtag1v5:amd64`) carries documentation and dependency selection; `fedora-acb86505aa1316e17254882c` (`user:passwdqc`) owns no files and requires other packages. S2.2-1 can be read to include their selection behavior, while the designated removal test in S2.2-2 does not specify whether to include a later package-manager action. No sentence chooses that scope. Card 3 stays CONFIRMED, not REFUTED merely because the text lacks the word immediate. The 127 original card-3 rows are a source population, not a newly verified whole-table extent.

## Finding 4: absent hardware

**Finding 4 is valid.** `fedora-eaecd855d3b238f815d51e72` (`root:alsa-sof-firmware`) and `fedora-369a1218fca1b15b045403ef` (`user:alsa-sof-firmware`) have notes establishing device-firmware-only files and absent sound hardware. `../review/card5-challenge.md` itself identifies both scopes: capabilities on fixed observed hardware, or capabilities after a hardware addition. These are competing scopes of the text, not unknown facts about the firmware's role. S2.2-16 likewise leaves whether a stored image for an absent device is covered unresolved. Card 5 is CONFIRMED at least for those two rows; remove them from the previous explicit UNKNOWN set. This alone changes 114 to 112, before any other corrected dispositions. The previous 56 metadata exclusions must also be reconsidered.

No physical attachment probe is needed to prove what the text does not specify. Conversely, a package's name alone is insufficient to add it to a precise extent. Packages containing separately established host code can still be decided by that code. The Xen boot-module sample must use the same unresolved scope, not silently select the fixed-environment reading.

## Card 7 after removal of the metadata shortcut

The proposed universal collision has factual weaknesses independent of metadata. In the saved `D1/review/raw/cockpit-development.html` around line 933, the bridge is server-side and services requests from the front end: its rights are not the browser's rights. This addresses `fedora-d23b5ec58a99a2d5dd98c6d0` (`root:cockpit-storaged`) and `fedora-d1549cca8e2e2802d54afae6` (`user:cockpit-system`).

For `tumbleweed-458bd2d25764f4b4b0aa2150` (`user:libreoffice-filters-optional`), the saved `D1/review/raw/libreoffice-xslt.cxx:328`–334 forbids writes, directory creation and network operations while allowing local-file reads. That contradicts the proposed unrestricted-rights premise. For `tumbleweed-58bfaed75b767465bff8e84a` (`user:augeas-lenses`), the adjudication note itself says no I/O primitives. Selecting transformations is not evidence that lens code can do whatever the executing program can do.

For `tumbleweed-b8d3bce61d0c4d8c4fd618cc` (`user:plasma6-theme-openSUSE`) and `tumbleweed-c225ad126cda23f96aa4609e` (`user:plasma6-sddm-theme-openSUSE`), generic QML documentation (`D1/review/raw/qt-untrusted.html:201`) says that QML has no separate privacy domains. It does not establish the exact operations available to these installed scripts or prove every payload member is unrestricted. The source card's conflation of an API with confinement is not enough to demonstrate a collision; equally, removing the metadata shortcut leaves the previous all-14-MUST conclusion unsupported. FACT-WRONG for the asserted universal collision must not be presented as a complete literal classification of those fourteen packages. Residual package/execution facts require explicit uncertainty or separate evidence, not an invented choice.

## Finding 6: guest ROMs and card 8

**The inconsistency finding is valid; confirmation is not its only permitted correction.** The finding itself offers dropping the metadata ground everywhere as an alternative. Taking that alternative avoids deriving MUST for guest-ROM packages solely from reverse requirements.

The notes for `fedora-21a722be1d318ec0f86e5189` (`user:ipxe-roms-qemu`) and `fedora-d42127df5b3b98e4059e07bb` (`user:seavgabios-bin`) establish execution inside guests; their root duplicates are `fedora-616e68aeb7dec8d6385fe655` and `fedora-5b4329ab9922a63ad2aeff1f`. S2.2-11 expressly exempts that execution context, and S2.2-12 expressly calls it an exemption. Requiring guest code to make that guest work does not itself invalidate the named exemption; otherwise the explicit guest-system example would exempt nothing.

The package claim must remain distinct. `fedora-729138f682023c574071c098` (`root:seabios-bin`) has both images and QEMU firmware descriptors in its permitted adjudication note. This disproves its code-only package premise. For OVMF, the prior report's more specific descriptor claim is supported there only by an unlisted folder; this audit does not independently re-establish it. Card 8's pure-guest-code collision can be REFUTED without metadata, while descriptor-bearing packages need an independently sourced whole-package decision. A FACT-WRONG code-only premise is not proof that every package has been decided MUST.

## Handoff limits

This memo establishes reasoning and named counterexamples, not a new exhaustive extent. Source populations are 413/161/127/58/14/8 for cards 1/2/3/5/7/8 respectively, from a fresh read of `../adjudication/rows.tsv`. Exact corrected extent lists must search all `../compare/joined.tsv`, separate demonstrated payload/code decisions from metadata-only decisions, and preserve unknown facts without converting textual ambiguity to S3-2. No claim of final acceptance is made.
