# RPM classification notes

Scope: 3,954 RPM inventory rows representing 1,977 named packages in two inventory contexts. Each input identifier is retained. Installation evidence establishes package presence; it is not used as proof that every package is executable. No object was removed and no machine probe was performed.

## Sources and method

The two RPM inventory outputs are `../in/raw/fedora/raw/004-packages-root-rpm.out` and `../in/raw/fedora/raw/039-packages-user-rpm.out`. Their names, versions and architectures were matched to public package descriptions. The supplied ownership and filesystem outputs are empty and were not used to infer payloads.

Public package descriptions: [https://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/repodata/400ba6e734c9d65d685823ab30724d33c1a11a2c370cd22477e2c843a75636f5-primary.xml.zst](https://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/repodata/400ba6e734c9d65d685823ab30724d33c1a11a2c370cd22477e2c843a75636f5-primary.xml.zst). Public payload listings: [https://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/repodata/b3d721ca63b972a2aa46803df239cbc337d948f9ce14743d4c49c7b156290aab-filelists.xml.zst](https://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/repodata/b3d721ca63b972a2aa46803df239cbc337d948f9ce14743d4c49c7b156290aab-filelists.xml.zst). Selected records were streamed without installing or executing packages. The saved source extraction is (not published: downloaded distribution package metadata). Public repository documentation establishes package purpose; it does not certify byte-for-byte identity with the inventoried versions.

The descriptions contain the following exact functional terms used in rule checks: "policy", "wallpaper", "directories", "Documentation", "Firmware", "font", "library", "metapackage", "module", "plugin", "programs", "data", "Translations". These short quotations refer to descriptions, not to the earlier inventory labels. Detailed functions are paraphrased in the output.

The implementation is `rpm-classify.py`, with individually reviewed cases in `rpm-special.py` and current-run corrections in `rpm-revisions.py`. Settled rows were appended and flushed individually. Later review corrections are retained in `part-fedora.rpm.correction-audit.tsv`; `part-fedora.rpm.corrections.tsv` supplies replacement rows. No earlier classification was consulted.

## Applicable sentences, quoted exactly

- **S2.2-1** Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.

- **S2.2-2** The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.

- **S2.2-4** content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;

- **S2.2-7** settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.

- **S2.2-9** a program that runs on the computer must be recorded regardless of how it was installed—including an application package (Flatpak), a program in the home directory, and a program in a container;

- **S2.2-10** code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.

- **S2.2-11** Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.

- **S2.2-12** This exemption covers only code that runs inside the executing program; a program that runs as its own process on the computer, including in a container, is a program and must be recorded.

- **S2.2-13** A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;

- **S2.2-15** accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;

- **S2.2-16** the boot order and device firmware must be recorded where the system is able to change them.

- **S3-2** If what the object does remains unknown, the case yields ?.

## Homogeneous rules and ten manually inspected rows per rule

### access

MUST (S2.2-1, S2.2-2, S2.2-15): documented access-control policies change which operations are permitted. Policy tools and libraries are separately classified as code.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-401aafc2c93db29a7f5d5188`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-39cf27cf6ac22aa82e3197e4`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-dad5194586ffa57ebd05f2bf`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-3d4376a27db4488991133c68`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-e81c2a9068cf6ee6c9da7cad`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-6106d7b48d4bf43f8eead688`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-690eb0c69aac5b3c98f0a0a8`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-acb236ec9892ce5f40c0f5c6`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-5f51df55119cfdaea7f025f8`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.
- `fedora-ee442f3e06d6d5aed46a8f1a`: Supplies access-control policy governing permitted system operations. Verified against the description and payload listing.

### art

NOT (S2.2-4): decorative pictures, icons, wallpapers, cursors and sounds lose their particular content on removal; the programs using them retain their operations.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-2d9f69baa45edd8c5d7a7e91`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-a18249c9d0fa708e1a1d6876`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-dac714d5ac6cb167e4a9910f`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-079731ebe92e3045b8360192`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-3268c5874ca30fd36dbc7144`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-b356fc11d9d7be7a4dd5483f`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-44a45b04d40a4002cfed09ad`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-c3cf87397d9c67b42cb8aa4a`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-0b9b7984a9eb8451ef2e6bc9`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.
- `fedora-62390e1a2474b226d6fa4743`: Supplies decorative images, icons, or sounds. Verified against the description and payload listing.

### directories

UNKNOWN (S3-2): documentation identifies directory ownership, but the inventory lacks occupancy and operative dependence on empty directories. No recursive removal is assumed. Packages containing scripts, system-account rules, essential compatibility paths or macros were separated.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-5e338f6bb866db8e2a41edeb`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-a72bbb3ac6e34b6db736c8d9`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-57a389ab36fffa295005c147`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-370f9670318663db7d7af56f`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-4f8074a48708dd529c75b65e`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-d39abe1ddedcb3a27506a9ef`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-041e3807da84dd9e46186c79`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-9053b3a7e45ae753a4a9e8d3`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-f531a43938c67a1109b6ed09`: Owns directories used by other packages. Verified against the description and payload listing.
- `fedora-8a6c610e96f3dbcc46ae487b`: Owns directories used by other packages. Verified against the description and payload listing.

### documents

NOT (S2.2-4): documentation and license payloads make only their document content unavailable. A documentation directory containing actual executable code is not classified by this rule.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-da3964ef0015cfae111f13df`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-b6269203e737dac13108c5ca`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-7b84a6c2dd78d79e9b065092`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-bb97dc4efa67462e903bb8f3`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-39013d59b6fb9efe514d7c81`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-bfe273ab545974dcd8ac0bf2`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-75345b8b036158dc98895e20`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-c479d4b18ce742f1c1b0b781`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-ffc8a677ec4afd093afcfa2f`: Supplies documentation or licensing text. Verified against the description and payload listing.
- `fedora-a33452db9baecef4fd4f3f12`: Supplies documentation or licensing text. Verified against the description and payload listing.

### firmware

MUST (S2.2-1, S2.2-2, S2.2-16): device firmware images and firmware-loading support enable device initialization or updates. Their removal prevents supplying that functionality. Guest firmware and uncertain BIOS deployment are separate cases.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-eaecd855d3b238f815d51e72`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-f733db428ec6a29ecb85d28e`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-f53e71d57d5f3afc074c36c2`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-03c77549892b6a8193035af4`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-1fef7c4b0de4ef9b38eeda7e`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-4aeb8ef58f03412cf56ccd3a`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-d175e0f65161fea9fcb47a66`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-ef952e201e9d3b706b3fe18e`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-661d2912f0d98de7b4160da2`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.
- `fedora-fbf97f188c89cc143ec3bd8a`: Supplies device firmware or firmware-loading support. Verified against the description and payload listing.

### fonts

NOT (S2.2-4): the payload provides typeface and glyph-shape content. Removing that content leaves rendering programs and algorithms available. Particular designs cease to be available. Operational character-processing rules are separate cases.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-a5b953eef1bebf50abae063b`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-cda4a44cc707192c93f66698`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-8c1cc1fbc16837c841d7b68c`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-14928d3664ea72ff24c8269f`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-3b918dfc4f83c367dcb026cf`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-2ec107617e982d64ea2a92da`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-da70b55dde55d6da634a2481`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-57e4db925137d63d11a40631`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-8c1bbecc2b543f8b3d3e1f83`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.
- `fedora-547407149020ad146ca7ed47`: Supplies typeface and glyph-shape content for text rendering. Verified against the description and payload listing.

### library

MUST (S2.2-1, S2.2-10): documented executable library routines run under the calling program authority. Library-looking names alone were insufficient; descriptions establish runtime-library functionality.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-edb09599722384f6bb836965`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-21e312548b0f8d7d4e2182be`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-f619198a4461ebe7240c5dd8`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-9a450a0179f3679402f3102c`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-55ce98be0c44a6502c367997`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-377d221dd0fcdb2297dc97b4`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-276bb55c296f439e02d1f675`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-2b10e107afcacf2988c7b2af`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-223761c229fbf1974686ac3c`: Supplies executable library routines used by other programs. Verified against the description and payload listing.
- `fedora-bcb572405c43442f9f518ea2`: Supplies executable library routines used by other programs. Verified against the description and payload listing.

### meta

NOT (S2.2-1, S2.2-2): dependency-selection packages lacking runtime payload leave separately installed dependencies available when the selected package is removed. Catalog descriptions, documentation, and licensing material add no runtime operation. An apparently similar package containing executable helper scripts was separated.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-138a10d5278297b267d354ee`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-be5599ad26429f507c08c013`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-8730ac5a39bf84af93b38e20`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-7ea45e943d0bb511c6ebe3b5`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-07515c2535408ee07c36d1f6`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-fca703a8f1ced7ff190c701b`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-438f4ce9019643929958b0b6`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-149f51b465b82779d0c664a1`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-6747d55fa0766abda60b7a7e`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.
- `fedora-9599a741b857ba787b4dec0a`: Selects dependencies without supplying executable runtime operations. Verified against the description and payload listing.

### module

MUST (S2.2-10): documented interpreter modules supply executable routines running with interpreter authority. The rule is not applied merely because a name has a language prefix; dependency-only extras were separated.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-27e2d2dc939310b3a9d142fc`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-d0d306da7b26b866dfc2f1c5`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-76997ee765a0cefaf538ea45`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-708c4c2d0a85f498e5b37957`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-49b7a78fbb82a92881309900`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-727574267f9860a5616d294a`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-f17c3f67492a6f5922f38468`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-e8fb5374118fc855a77c2f1d`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-3342f3d007a3e8507fea11c0`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.
- `fedora-23a9ae7dc603e18f4eac7ca9`: Supplies interpreter modules or executable language support. Verified against the description and payload listing.

### native

MUST (S2.2-1, S2.2-10): documented plugins, drivers, parsers, codecs and implementation modules supply executable operations within the calling program. Guest-confined firmware is separate. Host-side emulator device implementations are host code, not guest code.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-78a07f368dd66bf0c5c34f6e`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-ba44be2d1b32f9dbc8620e1d`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-92e7cb16325d58b3242234a9`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-8bb8455c1e98d47cd64570cd`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-1c67dbedae42aa60e8d74fb4`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-48d48c2d61923f8c709beb8f`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-bf034164763b7026389b7711`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-c5ea8e158aef9f1932ef4bd2`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-53d2dfb5c3c8dbec48863fec`: Supplies executable modules implementing program operations. Verified against the description and payload listing.
- `fedora-91dd7ff34401ed0f818e2a36`: Supplies executable modules implementing program operations. Verified against the description and payload listing.

### program

MUST (S2.2-9, S2.2-12): command-path payloads or documented standalone daemons/helpers establish executable programs. Their installation method does not change the explicit program requirement.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-2a4f52995c5b6597c9ae4da9`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-40f67601ab760fef41d8c68d`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-f0000db9d3e3bdff190dc1d0`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-e8070a5f3ff2f24403e24375`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-de5e84503da6254598d4ff6b`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-bb9c02d258f9dc2fc6500734`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-dcf5934f834be0b44aff15c8`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-fdb52d37ebe4e4ad86277d77`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-3013dd5332806971f55d351b`: Provides installed executable commands. Verified against the description and payload listing.
- `fedora-e915f0e88118eda90fbbc096`: Provides installed executable commands. Verified against the description and payload listing.

### tables

HOLE (S2.2-1, S2.2-2, S2.2-4): non-executable reference tables participate in lookup, validation, spelling, input, or processing. One reading treats losing these particular operations as lost capability; another treats the absent entries as unavailable database content. The text does not specify the boundary between an operation and a lookup of missing content. Each package purpose was checked independently before admission to this rule.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-ddf7aee0dfcb6861fd6c11a4`: Maps encoded characters to glyph identifiers for text rendering. Verified against the description and payload listing.
- `fedora-758ab1b54089d36f3f204298`: Supplies searchable application metadata and software-center icons. Verified against the description and payload listing.
- `fedora-3bee2fde6a0a4c7940913aa4`: Supplies a weather-location database. Verified against the description and payload listing.
- `fedora-ba642d8c7dc65763670a545f`: Supplies Australian English spelling dictionaries. Verified against the description and payload listing.
- `fedora-14c56b96b1d25a343c22e542`: Supplies American English spelling dictionaries. Verified against the description and payload listing.
- `fedora-b792b3d284c8bb4f1a50a00f`: Supplies language-tag and locale reference tables. Verified against the description and payload listing.
- `fedora-30e08c6eb3ac2e6152819be2`: Supplies input maps and language-specific text rendering tables. Verified against the description and payload listing.
- `fedora-d4649655477796f4959ebaf9`: Describes terminal capabilities for terminal-aware programs. Verified against the description and payload listing.
- `fedora-e13fc67638ebe9ce37446135`: Identifies domain suffix boundaries for cookie security decisions. Verified against the description and payload listing.
- `fedora-d2d21c3359edaae41805b76b`: Supplies XML schemas and catalogs used by XML processors. Verified against the description and payload listing.

### translations

NOT (S2.2-4): message catalogs and localized document content supply alternative strings or documents; their absence does not remove the program operations. Locale archives governing collation, parsing and conversion are separate MUST cases.

Manual checks of the documented purpose and relevant payload against the rule:

- `fedora-7dbeecbdde5eb164d415b5b4`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-61ac71638a43dd6e94f9bf51`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-338b8f40f8960cbf67b044bd`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-58e2a0e95887ed95992d1c20`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-382a4d8641dbb641d7c7f9d0`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-28e9960e5a220ec503448f10`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-7312414364c476331e693454`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-65e9be2f1322a296f55563cd`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-0932683cb5f85283b3295b76`: Supplies translated messages or localized document content. Verified against the description and payload listing.
- `fedora-07334ecf67889302253474d8`: Supplies translated messages or localized document content. Verified against the description and payload listing.

## Individual distinctions and supporting quotations

- [RPM manual](https://rpm.org/docs/4.20.x/man/rpm.8): "erase individual software packages". The object-removal reasoning removes the selected package, not separately inventoried dependencies. No dependency autoremove operation was assumed.
- [RPM removal implementation](https://raw.githubusercontent.com/rpm-software-management/rpm/master/lib/fsm.cc): `unlinkat(dirfd, path, AT_REMOVEDIR)`. A nonempty directory is not recursively deleted. Missing occupancy information therefore remains an evidence limitation for directory-only packages.
- [Locale documentation](https://man7.org/linux/man-pages/man7/locale.7.html): "This category governs the collation rules used for sorting and regular expressions". The locale archive supplies behavioral rules, unlike translation-only catalogs.
- [Shell extension documentation](https://gjs.guide/extensions/overview/anatomy.html): "The code in `extension.js` is executed in the same process as `gnome-shell`". The five installed extension packages contain this entry-point code, so S2.2-10 applies.
- [RPM keyring documentation](https://rpm.org/docs/4.20.x/man/rpmkeys.8): "Digital signatures cannot be verified without a public key." The imported-key pseudo-package is classified by signature verification, not by the package label.

The package rows represent individual packages, not directory-member groups. A package containing required code together with exempt documentation is MUST: recording the package records its required contribution. No package row was converted into a synthetic MIXED directory group.

Further individually checked distinctions include host daemons packaged as data, shell initialization and kernel-install scripts, account rules in directory packages, guest-only firmware, browser-only administrative pages, and default configurations shared across programs. Macro expansion and stylesheet execution rights remain UNKNOWN when the actual behavior is not established. HOLE is reserved for a textual boundary with established object function.

## Validation

Validated: input/output identifiers have the same set and count, each once; all decisions are allowed; all field word limits pass. Counts: MUST 3380, NOT 450, HOLE 80, UNKNOWN 44, MIXED 0.
