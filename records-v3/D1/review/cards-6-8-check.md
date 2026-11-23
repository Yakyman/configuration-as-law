# Independent challenge of cards 6–8 review

Reviewed 2026-11-22 UTC. Sources: `../../TEXT.md`, `../../SENTENCES.md`, `cards-5-8.md`, matching `../adjudication/rows.tsv` notes, package entries in (not published: adjudication scratch), and the saved primary sources in `raw/sources.json`.

## Card 6: refutation withstands challenge on the stated facts

S2.2-1: “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

The card establishes that the generated units, autologin drop-ins, enablement links, mount units, static-node configuration and resolver files are operational inputs. Each therefore meets S2.2-1. Recreating an input later does not contradict its current role. S2.2-2 states a sufficient positive removal test; it does not say that every negative or temporary result overrides S2.2-1.

The strongest challenge is that a generated input might be a cache. But the adjudication notes establish regeneration at boot, manager reload or service activation, rather than a slower fallback with unchanged behaviour after every removal. Automatic regeneration alone does not establish the explicit cache condition. The draft correctly avoids claiming that all derived objects must be recorded and confines its conclusion to the stated operational inputs. S2.5-3 concerns how to express the declaration; it supports dismissal of a representation question, but is not itself the reason these objects are MUST.

No confirmed gap is established by card 6. This conclusion does not independently establish every regeneration timing detail; none is necessary to the literal S2.2-1 refutation on the card's accepted dependency premise.

## Card 7: proposed collision fails, but two examples retain factual uncertainty

The Cockpit evidence establishes separate browser and bridge components. Rights of the bridge cannot simply be attributed to the browser-executed page. The XSLT evidence is stronger still: `D1/review/raw/libreoffice-xslt.cxx`, lines 323–338, forbids file writes, directory creation and network access, permits local reads, and applies the transform only after security preferences are installed. This contradicts the claim that the filter can do whatever the office program can do. The Augeas documentation and adjudication's own no-I/O-primitives note likewise do not establish unrestricted host-program operations.

For the two theme packages, the cited Qt passage is limited: it states that code can access all data in its scope. It does not prove arbitrary operating-system access, and it does not prove confinement to the executing program's interface. Treating absence of privacy domains as proof of S2.2-10 would stretch that evidence. Conversely, treating use of a scripting API as proof of S2.2-11 would stretch it too. The draft expressly preserves this uncertainty; that caveat is necessary.

S3-2: “If what the object does remains unknown, the case yields ?.”

Thus FACT-WRONG is defensible for the card's asserted factual collision, but not as a statement that every package member now has a complete resolved classification. The theme execution contexts remain factual UNKNOWN unless additional evidence establishes the relevant rights/confinement predicate. A genuine unresolved subcase must not disappear from the outcome accounting merely because this particular collision argument is rejected.

## Card 8: guest-code refutation holds; whole-package NOT is overbroad

S2.2-11: “Code that the program confines to its own interface—a web page in a browser, a guest system in a virtual machine—need not be recorded, but the program itself must be.”

S2.2-12 explicitly calls this an exemption, so the guest-only executable images and option ROMs are exempt despite being needed for particular guest operations. This refutes the proposed generic S2.2-2 collision.

However, the actual package payloads are larger than executable guest images. `seabios-bin` contains `/usr/share/qemu/firmware/80-seabios-default.json` and `80-seabios-microvm.json`. `edk2-ovmf` contains numerous firmware-selection descriptors under `/usr/share/qemu/firmware/` too. Their presence is explicit in (not published: adjudication scratch). They are host-read values, not guest-executed code, so S2.2-11 alone cannot decide them.

The draft says SeaBIOS descriptors are confined to one program but supplies no evidence establishing that confinement. A host VM manager may read a descriptor to configure a separate emulator process; if established, that effect is not confined inside the reading program, on the same reasoning used for card 4. A whole-package NOT also requires accounting for the OVMF descriptors omitted from its example explanation. The existing file lists establish the potential subcase, not its precise active consumers.

Conclusion: keep the guest-code collision REFUTED, but do not present both whole-package NOT verdicts as fully proved by the cited evidence. Classify the host-descriptor subcase only when its effects are established; otherwise S3-2 supplies UNKNOWN. This factual qualification does not itself confirm a new textual hole.
