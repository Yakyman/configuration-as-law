# Object-sweep candidates and rejected attacks

Beyond the published plan. Documentation-only attacker sweep. This memo supplies candidate kinds to the final integration; it does not accept them as findings.

## 1. A value read by one program can control work outside it

Candidate type: TERM. The concrete object is Firefox handlers.json choosing an external PDF viewer. The browser reads a value, then another application opens the file. Source: https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data, Download actions; its quoted passage is saved under `browser` in SWEEP-SOURCES.md.

S2.2-1 “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-7 “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S2.2-13 “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

The text does not delimit whether inside one program means the location where a setting is interpreted or the reach of its effects. The first reading exempts the browser preference; the second requires it because it controls a separate process. The values/code distinction confirms that this is a setting but does not define that boundary. This is one gap kind, shared by the 12 corresponding one-program boundary rows, not 12 cards.

Strongest objection: the external effect means the setting is not only inside the browser, and the general rule decides MUST. That is a plausible reading, but the text does not state an effect-based criterion; the homepage example itself causes communication with external systems. Another objection is that every browser setting is exempt: the sentence exempts only settings with the inside-one-program qualification, so the browser label alone cannot decide it.

Related objects: package repository endpoints and update holds; package extraction exclusions and package trust settings; syslog delivery and log-rotation policies; virtual CPU and RAM settings; guest shared-directory settings; boot-menu timeout; desktop visibility settings.

Primary references for those analogues: SWEEP-SOURCES.md sections pacmanconf, bsdconfig, vm, bootctl, desktop. SWEEP.tsv gives the relevant directive or section for each HOLE row.

## 2. A Wi-Fi password and a raw key share one field

Candidate type: TERM, lower confidence. NetworkManager's psk property accepts a passphrase or the already derived 64-hexadecimal-character key. Source: https://networkmanager.dev/docs/api/latest/settings-802-11-wireless-security.html, psk property. The short existing source quotation establishes Wi-Fi security configuration; the property itself explicitly distinguishes the two representations.

S2.2-1 “Whatever the computer’s behaviour depends on—what it does and what can be done on it—must be recorded.”

S2.2-14 “a saved Wi-Fi network must be recorded; the network password need not be: when it changes, the computer does the same;”

S2.5-1 “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”

The text exempts a network password but does not delimit password against the binary secret derived from one. A literal technical distinction makes the raw key MUST under the behavioral rule, whereas a credential-purpose reading treats it as the exempt password. This is not an issue about how secrets are protected; it concerns which credential object must be recorded.

Strongest objection: password has its ordinary passphrase meaning, so the general rule directly decides MUST for a raw key. That is a substantial refutation; retain a card only if the final term analysis establishes that ordinary use does not decide it. Do not assert a collision merely because credentials can be represented differently.

## Rejected attacks retained as audit trail

- Registry configuration, installed-package ownership data and udev's live device database are MUST. Their behavior changes when removed, so the content-only condition does not apply.
- A repository metadata cache that cannot be reconstructed and whose loss disables installation is MUST. It fails the only-more-slowly condition; being called a cache is insufficient.
- Last-used network timestamps, install-reason history and boot-attempt history are NOT under the explicit past-record exemption. Their downstream influence alone does not remove that exemption.
- Dictionary values confined to one editor and certificate settings confined to one browser are NOT. They are values rather than full-rights code, and there is an express local-setting exemption.
- Ordinary temporary state, undo files, snapshots, entropy persistence and removed-program remnants are not holes: their treatment is outside the definition.
- Current CPU performance state affects behavior and is MUST under the first sentence. Inability to perform a meaningful removal is not needed to defeat the first sentence; any separate in-force vocabulary problem belongs in the term sweep.

## Initial catalogue check (before final integration)

194 functional types, 35 primary documentation URLs, 134 MUST / 45 NOT / 13 HOLE. The 13 HOLE rows represent at most two candidate kinds. Linux hierarchy/init/kernel/package/desktop/shell/editor/browser/container/VM/network/authentication/device/power/firmware/time/locale sources are included, with FreeBSD, OpenBSD, Windows, macOS and Android breadth. No duplicate names; package-payload alias and one insufficiently supported Windows access-token row were removed. All records use only documentation and reasoning.

Final disposition: candidate 1 retained as one TERM card; candidate 2 rejected and its raw-key row changed to MUST. Final integrated catalogue: 192 types, 38 source URLs, 134 MUST / 45 NOT / 13 HOLE; see README.md.
