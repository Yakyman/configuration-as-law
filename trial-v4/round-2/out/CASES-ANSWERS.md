# Fifteen cases under PAGE.md

`COVERED` denotes the availability of the covering line specified by L1–L3, not a claim that an unseen declaration already contains it. Package selection/dependency provenance is a factual question. Q1 takes precedence over Q2, including for package contents that happen to be executable.

## 1. Administrator-modified service configuration

Both the boot-module list and time-server value: **SETTING / YES / DECIDED**. Sentences: R6, Q3, Q3a, R1, L2, U4.

The administrator chose system-service parameters. A single reader does not make them private application preferences. They are read as values, and the stated modifications exclude unchanged package defaults.

## 2. Compiled Python or Guile copy

Both copies: **PROGRAM / COVERED / DECIDED**. Sentences: R6, Q2, U4, R1, L1.

The program executes the generated copy. It was not received unchanged in the package, so Q2 applies. Its source came with a package; the source/package line covers the automatically compiled result.

## 3. Emacs savehist

**PROGRAM / YES / DECIDED**. Sentences: R6, Q2, U4, R1, L1.

The case expressly states that Emacs executes this file as Lisp. Its historical data origin does not reach Q4 after Q2 succeeds. Session history is not reconstructible from the Emacs package line; no other generating declaration line is given. Ordinary Emacs Lisp has the editor’s ability to launch programs and change files; U2 does not exempt it.

## 4. Package-helper enablement marker

**PROGRAM_RECORD / NO / DECIDED**. Sentences: R6, Q3, Q3a, Q4, R2.

The marker records a past installation event. It is not the chosen service activation value, even though a later installer consults it. Reading working state to decide subsequent behavior does not by itself meet Q3's human-choice condition.

## 5. Browser extension installed in a profile

**INSTALLED / YES / DECIDED**. Sentences: I1, I2, I3, R6, Q1, R1, L1.

The browser's extension installer installs and removes the extension as a unit. The person selected this extension, rather than an unspecified dependency. Q1 decides before executable-code distinctions; the extension package needs its own line.

Documentation: [Firefox extension installation and removal](https://support.mozilla.org/en-US/kb/disable-or-remove-add-ons).

## 6. Installed emoji-font package

**INSTALLED / NA / FACT_UNKNOWN**. Sentences: I2, R6, Q1, R1, L1.

Q1 expressly includes font packages. The case does not say whether this package was selected independently or obtained as a dependency of a recorded package. The first requires its own line; the second can be COVERED. Sharing the font among programs does not create a gap.

## 7. Installed reference-table package

**INSTALLED / NA / FACT_UNKNOWN**. Sentences: I2, R6, Q1, R1, L1.

Q1 expressly includes reference tables. A package must be recorded, but independent selection versus dependency provenance is absent: YES or COVERED. Its lack of executable code does not change the kind.

## 8. Installed dependency-only package

**INSTALLED / NA / FACT_UNKNOWN**. Sentences: I2, R6, Q1, R1, L1.

Q1 expressly includes a package containing only dependencies. Whether this metapackage itself was independently selected or obtained through another package is unstated, so its own-line requirement is unknown. Packages it obtains as dependencies can be covered by its line.

## 9. Unusable firmware and Xen boot files

Both: **INSTALLED / COVERED / DECIDED**. Sentences: R6, Q1, R1, L1, U1.

Both objects were received as package parts. The described absence of matching hardware does not alter them. Q1 succeeds first, regardless of whether Q2 would fail under U1; their containing package lines cover them.

## 10. Generated runtime service objects

File regenerated in `/run`: **RUNTIME / NO / DECIDED**. Sentences: R5, Q2, Q3a, L1, L2.

It belongs to the service-manager generator, whose own record is NA because package/source provenance is unstated. Its volatile output needs no separate line regardless of that provenance.

User service generated from an autostart shortcut: **NONE / NA / FACT_UNKNOWN**. Sentences: R5, Q3a, Q3b, L2.

The case does not state whether this second output is volatile or a persistent service definition, nor whether the shortcut is an installer default. Volatile output is RUNTIME/NO, belonging to the shortcut setting (record YES or COVERED); persistent service/default provenance can require YES or COVERED.

## 11. Typed terminal commands

`ls | grep foo`, `python -c "print(1)"`, and `curl https://example.org/install.sh | bash`: each **ACTION / NO / DECIDED**. Sentences: R4, R2.

Each described object is a command typed by a person. R4 explicitly treats it as an action. Separately stored files or lasting changes produced by executing a command would be different objects, not the typed command being classified here.

## 12. External declaration sources

Organization account source: **SETTING / COVERED / DECIDED**. Sentences: Q3a, R1, L3.

The account-setting line explicitly names its source. L3 makes the named source recorded; individual entries need not have separate lines. R3 excludes treating the remote server itself as a local object.

Scripts selected from project directory D: **PROGRAM / COVERED / DECIDED**. Sentences: Q2, R1, L3.

The scripts line names D as its source. L3 makes that source recorded through the line; D need not have a separate declaration line. The case calls these objects scripts, rather than unspecified project data.

## 13. Root Emacs installing extensions

Executable extensions installed as packages: **INSTALLED / YES / DECIDED**. Sentences: I1, I2, I3, T1, T2, R6, Q1, R1, L1, B1.

Emacs counts as an installer in its package-install part. Selected extension packages require lines; dependencies can be covered by those lines. Superuser execution does not bypass the stated system-tool exception. The situation therefore does not establish B1 breakage merely because an editor performs installation.

Documentation: [Emacs package installation](https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Installation.html), [package deletion](https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Menu.html).

## 14. Personal remote SSH key

Stored private key: **MATERIAL / NO / DECIDED**. Sentences: R6, Q4, R2.

The case expressly limits its purpose to entering other machines. Q4 names personal remote-entry keys as material. It does not authorize entry into this computer under Q3a.

Loaded agent copy: **RUNTIME / NO / DECIDED**. Sentences: R5, Q2, L1.

The loaded copy belongs to ssh-agent (PROGRAM; creator record NA because package/source provenance is unstated). It is transient agent memory, with no separate line. Requiring confirmation does not change the stored original key into a local-entry credential.

## 15. WebAssembly with one shared directory

**PROGRAM / NA / FACT_UNKNOWN**. Sentences: Q2, U2, U3, R1, L1.

Execution is established. The accessible directory's contents and write permissions are not: the module might change installed code or settings there, defeating U2, or have no such capability. The Wasmtime host process alone does not establish that the module has an independent process. Coverage provenance is also unstated.

Documentation: [Wasmtime filesystem capabilities](https://docs.wasmtime.dev/cli-options.html), [Wasmtime security](https://docs.wasmtime.dev/security.html).
