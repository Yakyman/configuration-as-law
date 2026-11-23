# Independent review of cards 1–4

Review date: 2026-11-22 UTC. Inputs: (not published: outside selected checks and direct evidence), `../../TEXT.md` Sections 2–5, `../../SENTENCES.md`, `../adjudication/HOLES.md`, `../adjudication/rows.tsv`, and the entire `../compare/joined.tsv`. No machine or removal probe was added.

## Final judgments

Card 1 is **CONFIRMED in a substantially narrower extent: one inventory row**. Card 2's claimed unconditional collision is **REFUTED**; six original examples have independent MUST reasons and the remaining example is UNKNOWN because exact package facts are incomplete, not a confirmed counterexample. Cards 3 and 4 are **REFUTED**. No entire card is classified OUTSIDE or FACT-WRONG.

Revision note, 2026-11-22 UTC: an earlier working assessment compared package payloads without consistently testing the package's dependency metadata. That assessment was withdrawn: the final enumeration below treats inventory packages as whole objects, including operational metadata and maintainer scripts. No earlier working extent is the final result.

## Deciding sentences

- S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”
- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”
- S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”
- S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”
- S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”
- S2.2-15: “accounts, the right to become superuser, the keys used to log in to an account, firewall rules, and ports open for connection must be recorded; an account password need not be, but the rule that password login is allowed must be;”
- S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”
- S3-2: “If what the object does remains unknown, the case yields ?.”

## Confirmed hole: Shared presentation content versus loss of capability

Removing the emoji font can mean either that its particular artwork is unavailable or that the computer can no longer render those emoji in that form. The text does not distinguish these descriptions when the drawing programs remain available and the object is shared among programs.

**Type:** one missing boundary, not two colliding unconditional rules. **Sentences:** S2.2-2, S2.2-4, S2.2-7 and S2.2-13, quoted above. S2.2-4 contains a substantive condition after the colon; database or artwork labels alone do not exempt an object. S2.2-13 makes values settings but does not state that settings and content are disjoint; S2.2-7 supplies no exemption for a shared setting.

**Actual row:** `mint-854622d42bc8ca5d899db0ff` — `root:fonts-noto-color-emoji`, version `2.047-0ubuntu0.24.04.1`, kind `L1:package:dpkg-query`. **Established extent:** one row, on Mint. Its payload file list ((not published: adjudication scratch)) contains `NotoColorEmoji.ttf` and two documentation files, with no fontconfig rules or executables. The exact installed-version binary package control archive was read independently: (not published: downloaded distribution package metadata) records its source URL, version, absence of maintainer scripts/triggers, and absence of Depends, Pre-Depends, Recommends, Suggests, Conflicts, Breaks, Replaces, Provides, Essential and Protected fields. The installed-package dependency search found no reverse dependency or recommendation naming it in the fetched metadata. This defeats the operational-package-metadata refutation that eliminated the other established matches.

The attempted literal refutation treats any inability to display the deleted content as satisfying S2.2-2. But then displaying a deleted document is also impossible, although S2.2-4 expressly exempts documents: its qualification about content must make a distinction. The text gives no corresponding criterion for the shared emoji artwork. This is a classification question, not the S2.5-1 design question of how to preserve or transfer data. No rule for resolving it has been added.

## Whole-table extent and uncertainty

The full table was searched by kinds and names, including font, theme, lang, l10n, common, data, dictionary, terminfo, colour, wallpaper, artwork, sound, branding, locale, zone, database, CMap and transport/reference names. `cards14_scan.py`, `cards14_extra.py`, and the dependency audit scripts preserve that work. Existing payload lists were read alongside inventory versions. A package name alone was never sufficient for confirmation.

`cards-1-4-extent.tsv` enumerates 602 matching rows, including 28 matches outside the original cards. The final counts are:

| Machine | Independent MUST reason | Confirmed | UNKNOWN facts |
|---|---:|---:|---:|
| Fedora | 250 | 0 | 0 |
| Tumbleweed | 242 | 0 | 0 |
| Mint | 88 | 1 | 19 |
| Flatcar | 1 | 0 | 1 |
| Talos | 0 | 0 | 0 |
| Total | 581 | 1 | 20 |

By original card: card 1 has 405 MUST rows, one confirmed row and seven UNKNOWN rows; card 2 has 148 MUST rows and 13 UNKNOWN rows. All 28 additional whole-table matches have independent MUST reasons. These are inventory rows, retaining root/user duplicates as separate objects.

The 20 UNKNOWN entries are **not confirmed members** of the hole and are not claimed to be resolved merely because an earlier label existed. For most, metadata matching the exact installed version was unavailable; for fonts-ubuntu, mint-translations and mint-l-icons, another version of an installed consumer has a reverse dependency but the exact consumer binary URL returned 404. For Flatcar `/etc/udev`, the inventory gives names/metadata rather than the contents of `hwdb.bin`, which can contain operational device rules as well as descriptive data. The table states each unresolved factual condition. The confirmed extent is exactly the one established row above; the unresolved factual candidates are explicitly separate.

Primary metadata evidence: (not published: adjudication scratch); (not published: downloaded distribution package metadata) (exact installed versions from the public 20261120 repository; URL in `tw-primary-source.txt`); the `mint-*-metadata.json` and `mint-*-versions.json` extracts of Ubuntu noble, updates/security and the Mint zena repository. Public package headers and controls are retained as selected operational fields only in `cards14-raw/*-header.json` and `*-control.json`. The [RPM tag reference](https://rpm.org/docs/4.20.x/manual/tags.html) identifies the header fields inspected. Exact-version comparison and forward/reverse installed-package searches are implemented in `cards14_finalextent.py`; `cards14_finish.py` applies the separately checked control/script results.

**Why metadata decides many supposedly data-only packages:** installed dependencies and recommendations change package-manager selection and retention; maintainer scripts execute code with the manager's rights. S2.2-1 or S2.2-10 applies independently of the payload-content question, exactly as for card 3. Examples of further decisive evidence are the installed recommendation of Fedora qt6-qttranslations by qt6-qtbase-gui, and Tumbleweed desktop-translations' Supplements relationship to the installed yast2-control-center. Mint ncurses-base has Essential: yes, governing whether the package manager permits its removal. This does not rely on hypothetical absent future consumers.

## Each original example of cards 1 and 2

S2.2-1 decides every MUST entry below; S3-2 decides the unavailable-fact entry. The exact dependency, script, trust or transport fact is given for each object.

| Source card | Id and name | Decision and independent fact |
|---|---|---|
| 1 | fedora-825992c02de7410b9de93d54 — root:abattis-cantarell-vf-fonts | MUST: Whole package has operational requirement(s): fontpackages-filesystem; (not published: adjudication scratch) |
| 1 | tumbleweed-25d4e59fef6a08262890c4c4 — root:google-roboto-fonts | MUST: Whole package has operational requirement(s): /bin/sh, /bin/sh, aaa_base, coreutils, coreutils, perl; cards14-raw/tw-primary-selected.json |
| 1 | fedora-f6384d9de305cf7440d4a349 — user:gnulib-l10n | MUST: Installed reverse requirements depend on package metadata: coreutils-common; (not published: adjudication scratch) |
| 1 | tumbleweed-d8620423f05d02d99e676201 — user:libKF6Baloo6-lang | MUST: Whole package has operational requirement(s): libKF6Baloo6; cards14-raw/tw-primary-selected.json |
| 1 | mint-f029447dfa5b81e83920cfc2 — root:cinnamon-l10n | MUST: Installed reverse requirements depend on package metadata: cinnamon-control-center, nemo, nemo-fileroller; cards14-raw/mint-*-metadata.json and mint-*-versions.json |
| 1 | fedora-e94d6040fe6b71468614c285 — user:adwaita-icon-theme-legacy | MUST: Whole package has operational requirement(s): /bin/sh; (not published: adjudication scratch) |
| 1 | tumbleweed-819b570cdea5ea55df85afe1 — user:gtk4-metatheme-breeze6 | MUST: Whole package has operational requirement(s): metatheme-breeze6-common; cards14-raw/tw-primary-selected.json |
| 2 | fedora-1616320aeaca00e35b428e9b — user:ncurses-base | MUST: Installed reverse requirements depend on package metadata: ncurses-libs; (not published: adjudication scratch) |
| 2 | tumbleweed-eaa3bb18d4c9f9d9e224e05d — user:terminfo | MUST: Whole package has operational requirement(s): terminfo-base; cards14-raw/tw-primary-selected.json |
| 2 | mint-cef67297df4b26083898d0be — root:libdrm-common | UNKNOWN: Exact installed-version metadata not found; cannot rule out operational package dependencies. |
| 2 | tumbleweed-856378d1c349da9571edbf48 — root:poppler-data | MUST: Installed reverse requirements depend on package metadata: libpoppler166; cards14-raw/tw-primary-selected.json |
| 2 | tumbleweed-cb6bae922bf2ef3c7006b5b6 — root:mobile-broadband-provider-info | MUST: Whole package has operational requirement(s): /usr/bin/pkg-config; cards14-raw/tw-primary-selected.json |
| 2 | mint-ef80a80feb7709633f6d40e4 — root:libtirpc-common | MUST: Operational trust or transport settings independently satisfy S2.2-1. |
| 2 | tumbleweed-d8740b0efbb387551a5f8266 — user:gpg-pubkey | MUST: Operational trust or transport settings independently satisfy S2.2-1. |

Card 2 does not establish the claimed unconditional clash: S2.2-4 expressly requires the computer to retain its behaviour, and the whole-package examples mostly have operational metadata independent of any reference values. The sole unresolved original example, libdrm-common, remains a factual question about that actual package rather than evidence that an unconditional database exemption overrides S2.2-1.

## Card 3: REFUTED

S2.2-1 directly includes behaviour of the package manager. A later run is something the computer does, and S2.2-2 says after removal, not immediately after removal. The card's own established premise is that dependency metadata changes later installation/retention/upgrade decisions; no timing amendment is needed to apply the sentence. It is not enough to call the README content while ignoring the package object's dependency metadata.

| Original example | Why S2.2-1 decides MUST |
|---|---|
| tumbleweed-8ffe304c89c8c7e36f097d58 — root:patterns-fonts-fonts | Its dependencies select font packages; that selection is computer behaviour. |
| tumbleweed-aac6aa8494b1f3e8c0028242 — user:grub2 | Its dependency constraints select boot-loader packages. |
| tumbleweed-f461fea1b1631f3f7d3a0c18 — root:kernel-firmware-all | Its dependency constraints select firmware subpackages. |
| mint-10d2b7fe70e9862d28583c28 — root:xserver-xorg-video-all | Its dependency constraints select X video-driver packages. |
| mint-7588ce4f54fd792c9bd42dd5 — root:libtag1v5:amd64 | Its dependency relationship controls retention/selection of the implementation package. |
| fedora-acb86505aa1316e17254882c — user:passwdqc | Its requirements select pam_passwdqc and passwdqc-utils despite having no payload files. |

Evidence: the card and corresponding `../adjudication/rows.tsv` notes establish these dependency effects; Fedora requirements are additionally saved in (not published: adjudication scratch). [Debian Policy §7](https://www.debian.org/doc/debian-policy/ch-relationships.html) specifies how dependency fields constrain package relationships. This conclusion does not depend on whether a future autoremove happens automatically: the constraints already affect what the package manager may do.

## Card 4: REFUTED

The proposed alternative replaces the actual words in force with read. S2.2-7 never says that every setting read by one program is exempt; the card's premise that its effect reaches other programs contradicts the exemption's only inside condition. S2.2-1 therefore decides these external effects without choosing between two permitted readings of the sentence.

| Original example | Literal decision and evidence |
|---|---|
| flatcar-939d7a7b0d01b67c8e427d2d — ssh-access:PermitUserRC | MUST: controls running a separate login-session script. Effective value yes in `D1/in/raw/flatcar/raw/085-ssh-access.out:36`. |
| flatcar-fcc568ae504c7531844f5402 — ssh-access:AcceptEnv | MUST: affects the environment inherited by session programs, not only sshd. Effective accepted locale variables at lines 83–98 of that inventory file. |
| flatcar-f7c7fedce0e2f18bdceec831 — ssh-access:RefuseConnection | MUST: controls whether users can establish sessions. Effective no at line 50; a default-valued policy still determines behaviour under S2.2-1. |
| flatcar-04d20d905cf48789916d65e4 — ssh-access:AuthorizedPrincipalsFile | MUST: chooses whether certificate logins require principals named in a file, an account-access effect; effective none at line 61. S2.2-1, reinforced by S2.2-15 for login keys. |
| fedora-8daf8a09379a987250afb6d4 — user:NetworkManager-config-connectivity-fedora | MUST: configures connectivity checking that is exposed to other clients and used in route selection; the saved payload is a conf.d drop-in. |
| tumbleweed-398f3c80654469a71f15a2fe — user:sddm-branding-openSUSE | MUST: the compositor command starts another program; the fact that the same file also selects a greeter look does not erase this effect. |
| tumbleweed-cdd698ee2b182cf9d748a45a — user:rpm-plugin-selinux | MUST: enabling file labelling determines installed-file security contexts used outside rpm. |

Primary semantics: [sshd_config](https://man.openbsd.org/sshd_config) describes the accepted variables being copied into the session environment and the other options' session/access effects. [NetworkManager.conf](https://networkmanager.dev/docs/api/latest/NetworkManager.conf.html) describes the connectivity mechanism and route effects. The display-manager and rpm macro payloads and their facts are saved in (not published: adjudication scratch) and identified by the corresponding names in (not published: adjudication scratch). S2.5-1 does not remove the classification of access or program-starting settings; it assigns user-authority design to the system.
