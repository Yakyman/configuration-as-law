CALIBRATION: FAILED 2 of 8

Comparison written 2026-11-23 06:02 UTC by the third party of the weighting. Sources: `PROTOCOL.md` (Sections 2–4),
`W0/CASES.md`, `W0/m1/cases.tsv` (party 1, 11 rows), `W0/m2/cases.tsv` (party 2, 11 rows), `TEXT.md` Section 8 with
`SENTENCES.md` (version 4), `night-1122/TEXT.md` Sections 2 and 3 with `night-1122/SENTENCES.md` (version 3).
“v4” and “v3” below are the two texts. In the columns of the parties, `no`, `none-decides` and `two-ways` are the
values of the column `gap` of their files.

## 1. The table

| Case | Expected decision (`PROTOCOL.md`, Section 4) | Obtained by party 1 | Obtained by party 2 | Obtained weight | Verdict | The differing part |
|---|---|---|---|---|---|---|
| 1. A font, icons and a theme obtained with a package | “No gap under version 4: an installed object (question 1). Under version 3 this was a gap in the wording.” | v4: `no`; installed object by question 1 (S8.2-7, S8.2-8); must be recorded, covered by the line of the package (S8.2-16); decided for objects that remain as received. v3: gap, `none-decides` (S2.2-1, S2.2-2, S2.2-4); meaning: yes, must be in the declaration, the package may represent them; can be met: yes. | v4: `no`; installed object by question 1; must be recorded, covered by the line of the package or a line of its own. v3: gap, `two-ways` (S2.2-2 against S2.2-4); meaning: yes, covered by the line of that package; can be met: yes. | v3: gap in the wording (same answer; both say it can be met). | SAME | — |
| 2. An installed package that contains only dependencies | “No gap under version 4: an installed object. Under version 3, a gap in the wording.” | v4: `no`; installed object by question 1; must be recorded, by a line of its own or as a dependency of a recorded package (which of the two is a fact of the inventory). v3: gap, `none-decides` (S2.2-1 to S2.2-7); meaning: yes, by its own entry or by the recorded package that requires it; can be met: yes. | v4: `no`; installed object by question 1; must be recorded, by a line of its own or as a dependency of a recorded package. v3: gap, `none-decides` (S2.2-1, S2.2-2); meaning: yes, by a line of its own or as a dependency of a recorded package; can be met: yes. | v3: gap in the wording (same answer; both say it can be met). | SAME | — |
| 3. A compiled copy of code that a program builds itself | “No gap under version 4: covered by the line of the original package. Under version 3, a gap in the wording.” | v4: `no`; program by question 2 (S8.2-9, S8.2-10); must be recorded; covered by the line from which the system built it, or a line of its own if no such line exists (a fact). v3: `no`, status FACT_UNKNOWN (how the copy is executed and what its deletion changes are not given); no answer to the two signs. | v4: `no`; program by question 2; must be recorded; covered by the line of the code from which it was built (S8.2-16). v3: gap, `two-ways` (S2.2-5 against S2.2-10); meaning: yes, covered by the line of the code it was compiled from, not by a line of its own; can be met: yes. | v3: the parties differ on the gap; third party: gap (Section 3.1 below). Weight: gap in the idea, because only one party answered the question about the meaning. | DIFFERENT | Version 3, the weight: expected a gap in the wording, obtained a gap in the idea. Party 1 also obtained no gap under version 3. |
| 4. A browser extension that a person installed in their own profile | “No gap: an installed object with a line of its own.” | v4: `no`; a package installed by the installer built into the browser (S8.1-5, S8.1-6), installed object by question 1; must be recorded, by a line of its own unless a line obtains it as S8.2-16 says. | v4: gap, `two-ways` (S8.1-5, S8.1-6, S8.2-7 against S8.2-9, S8.2-21): installed object with a line of its own if the part of the browser that installs extensions is an installer; need not be recorded if it is not. Meaning: yes, by a line of its own; can be met: yes. | v4: the parties differ on the gap; third party: the gap stands (Section 3.2 below). Weight: gap in the idea, because only one party answered the question about the meaning. | DIFFERENT | Gap or no gap under version 4: expected no gap, obtained a gap. With it, “must be recorded” is not decided by the text. |
| 5. A game downloaded and installed by a game store | “No gap in the definition: a program, which must be recorded. By what means a system ensures this is not part of the definition (Section 8.5) and is checked on the testbed.” | v4: `no`; a package installed as a whole by the store (S8.1-5, S8.1-6), installed object by question 1; must be recorded, by a line of its own unless covered by a line from which the system obtains it. | v4: `no`; installed object by question 1 (the store is an installer by S8.1-4 or S8.1-5, on the documentation fact that it installs and removes games); must be recorded by a line of its own; it is also code (question 2), but question 1 comes first. | none (no gap) | SAME | — (name of the kind only, see Section 4) |
| 6. The command `curl … \| bash` typed by a person | “No gap: a command is the person's action. What the script has left on the computer is decided for each object it has left.” | v4: `no`; S8.2-4: not an object, the person's action; the decision concerns the command, not what was downloaded or installed. | v4: `no`; S8.2-4: not an object, nothing to record for the command itself; what it leaves is decided separately, object by object. | none (no gap) | SAME | — |
| 7. A personal setting of a program, for example an editor theme | “No gap: a program record, which need not be recorded.” | v4: `no`; S8.2-14: a record of that program, need not be recorded (S8.2-2); a value that launches something or grants access, or a file executed as code, is decided otherwise (facts). | v4: `no`; S8.2-14: a record of that program, need not be recorded; if the value is in a file the editor executes as code, S8.2-23 makes it code (a fact about the file). | none (no gap) | SAME | — |
| 8. An object that the system itself creates anew after removal (version 3) | “A gap in the idea of version 3: the removal test gave no answer for it, and the criterion had to be replaced.” | v3: `no`, status FACT_UNKNOWN (what the object does, what is lost before it is recreated, whether recreation changes only speed); no answer to the two signs. | v3: gap, `two-ways` (S2.2-1 against S2.2-2); meaning: yes, covered by the line of the program or setting that creates it, no line of its own; can be met: yes. | v3: the parties differ on the gap; third party: gap (Section 3.3 below). Weight: gap in the idea, because only one party answered the question about the meaning. | SAME | — (the match of the weight is formal, see Section 4) |

## 2. The discrepancies

**Case 3.** Under version 4 both parties obtained the expected decision: no gap, and the copy must be recorded. Under
version 3 the expected decision is a gap in the wording. Party 2 found the gap (S2.2-5 against S2.2-10); party 1 found
no gap, held that the decision depends on facts the case does not give, and so did not answer the two questions of
the weight. With one answer instead of two, the first sign of a gap in the wording is not met, and by the rule the
gap is a gap in the idea. The only answers given, those of party 2, were “yes, covered by the line of the code it was
compiled from” and “it can be met”.

**Case 4.** The expected decision is no gap: an installed object with a line of its own. Party 1 obtained exactly
this. Party 2 obtained a gap: S8.1-4 defines an installer by “installing and removing programs”, the text does not
say whether an extension, which gets only the permissions the browser grants it, is a program, and if the browser is
not an installer here, S8.2-21 says the extension need not be recorded. The third party found no sentence of
Sections 8.1 and 8.2 that settles which of the two holds, so the gap stands. On the question about the meaning
party 2 gave the expected answer: it must be in the declaration by a line of its own.

## 3. The decisions of the third party where the parties differ

The parties differ on “gap or no gap” in three rows. Section 3 of `PROTOCOL.md`: “If a sentence is named and it
decides the object unambiguously, there is no gap. A third party adjudicates the dispute.”

### 3.1. Case 3, version 3: gap

- S2.2-5 (in the list opened by S2.2-3 “The following need not be recorded:”): “cache: after it is removed, the
  computer does the same, only more slowly;”
- S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights,
  so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell
  startup files, an editor configuration written in the editor’s programming language.”

For a compiled copy that a program runs with its own rights and builds again when the copy is removed, both sentences
fit and give opposite decisions; no sentence of Sections 2 and 3 gives one of them precedence. Party 1 named no
sentence that decides the object. Its row states both rules side by side (“Code running as a program or with the
executing program's own rights must be recorded; … a cache whose removal changes only speed need not be”) and asks
for the facts; when both facts hold, both decisions stand, so the facts do not remove the conflict. For a compiled
copy of code that the program confines to its own interface (S2.2-11) there is no conflict; the gap concerns the
first kind.

The verdict of case 3 does not depend on this decision: with “no gap under version 3” the case differs from the
expected decision as well.

### 3.2. Case 4, version 4: the gap stands

The sentences named by party 1 (S8.1-5, S8.1-6, S8.2-7, S8.2-8, S8.2-16) decide the case only if the part of the
browser that installs extensions is an installer.

- S8.1-4: “**Installer**—a program of the system whose purpose, according to its documentation, includes installing
  and removing programs: the system package manager, package managers of programming languages and of application
  packages.”
- S8.1-5: “A general-purpose program with a built-in installer counts as an installer in that part of its
  functionality.”
- S8.2-9: “Is the object code that the computer executes or can execute: on its own, at a person’s command, or
  through another program with that program’s rights?”
- S8.2-21: “Code that runs inside a recorded program and cannot itself launch programs or change what is installed
  and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.”

Neither S8.1-4 nor S8.1-5 says that an extension is among the “programs” whose installation makes a program an
installer. The only test of a program in the text is S8.2-9, and the text does not say whether code to which a
browser grants part of its rights is executed “with that program’s rights”. Under one reading the extension is a
package, question 1 is answered “yes”, and it must be recorded by a line of its own. Under the other the browser is
not an installer in this part, questions 1 and 2 are answered “no”, and S8.2-21 says the extension need not be
recorded. S8.2-6 fixes the order of the questions, not the answer to question 1. A choice between two readings of
the text is not made here.

Section 8.6 of `TEXT.md` states the first reading (“An installer built into the browser installs and removes it as a
whole: an installed object, recorded.”). It is outside Sections 8.1 and 8.2, by which check 1 decides
(`PROTOCOL.md`, Section 1), and it says of itself: “This is our reasoning, not a check; the check is described in
Section 9.”

The verdict of case 4 depends on this decision: with the dispute decided for party 1 the case would be SAME.

### 3.3. Case 8, version 3: gap

- S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something
  becomes impossible on it, the object must be recorded.”
- S3-1: “**Whether an object must be recorded.** The decision is made from the text of Section 2.2 and information
  about what the object does, established by documentation, by observation, or by removal: in a disputed case, the
  object is removed on a disposable copy of the machine, and what stopped working is recorded.”

For an object that the system creates anew after removal, neither sentence says whether the computer is observed
before or after the object exists again, and the two moments can give different answers. When nothing stops, S2.2-2
gives no decision at all: it says only when an object must be recorded, and the list S2.2-4 to S2.2-7 of what need
not be recorded names no such kind of object (S2.2-5 fits only those whose removal makes the computer slower and
nothing else). Party 1 named no sentence that decides the object: its row says that such an object “has no
unconditional recording decision”. The facts it asks for (“what is lost before it is recreated”) already assume the
moment of observation that the text does not fix.

The verdict of case 8 depends on this decision: with “no gap under version 3” the case would be DIFFERENT.

## 4. Notes on the cases with the verdict SAME

- **Case 5, the name of the kind.** The expected decision says “a program”; both parties say “installed object”
  (question 1 comes before question 2). The answers to “gap or no gap” and to “must it be recorded” are the same,
  and S8.2-10 says: “a program belongs to what is installed”. Noted; not a different decision.
- **Case 3, version 4, the line.** The expected decision names the line of the original package. Party 2 names the
  same line. Party 1 names it on the condition that such a line exists, and a line of its own otherwise. Party 2 put
  a question about the words “the system itself built” of S8.2-16 into `W0/m2/QUESTIONS.md`; under both of its
  readings the copy must be recorded. “Gap or no gap” and “must it be recorded” are the same for both parties.
- **Case 8, the weight.** The weight “gap in the idea” was obtained only because party 1, having found no gap, gave
  no answer to the question about the meaning. It was not obtained from a difference in the meaning or from a
  requirement that cannot be met: the one party that answered said “yes, covered by the line of the program or
  setting that creates it” and “it can be met”. The same rule, applied in the same way, gives the weight of case 3.
- **Cases 1, 2 and 7, conditions.** Both parties decided cases 1 and 2 for objects that remain as received and named
  the facts of the inventory on which the choice of the line depends; both decided case 7 for a value that the
  program only reads. These conditions do not change “gap or no gap” or “must it be recorded”.

## 5. What the first line depends on

Case 3 has the verdict DIFFERENT under either decision of Section 3.1, so the calibration has failed whatever the
third party decided. The number of differing cases depends on Sections 3.2 and 3.3: it is 2 as decided here, and
would be between 1 and 3 under other decisions of the two disputes.

Two questions that only the author can decide are written in `W0/QUESTIONS.md`.
