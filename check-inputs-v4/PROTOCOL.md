# Order of the checks of version 4: what counts, how gaps are weighted, and what is done beyond the plan

This page is fixed before the first observation and is not changed after publication.

## 1. What is already fixed

The four checks of version 4 and their failure conditions are set out in Section 9 of the fourth paper
(`fourth-paper/paper4-en.md`). The outcome of each check is determined by them alone. This page neither changes
nor relaxes them: any object for which the text of Sections 8.1 and 8.2 does not allow deciding, or allows
deciding both ways, gives check 1 the outcome 0, whatever weight it is assigned below.

## 2. The weight of a gap

Every gap that is found additionally receives one of two weights.

- **Gap in the wording.** By the meaning of the definition there is an answer and only one, but the words of the
  text do not give it. There are two signs, and both are required. First: two parties, asked separately “must
  this be in the declaration, if the declaration describes everything installed and every setting”, give the
  same answer. Second: a system can meet this requirement without forbidding any ordinary action from the list
  in Section 9.2.
- **Gap in the idea.** Everything else: the parties differ on the meaning as well, or the agreed requirement
  cannot be met without forbidding an ordinary action.

The weight does not affect the outcome of a check. It determines what is corrected in the next version as a
word and what as the definition itself. Both lists are published in full.

## 3. Procedure of weighting

- A gap is accepted only for an object of a real inventory taken after the actions fixed in the check inputs.
  Invented cases are not accepted.
- One party puts the gap forward. A second party, without seeing its arguments, decides the same object by the
  text and names the sentence that decides it. If a sentence is named and it decides the object unambiguously,
  there is no gap. A third party adjudicates the dispute. All three decisions are published.
- The parties answering the question about the meaning do not see each other's answers.

## 4. Cases with a decision known in advance

Before any new object is weighted, the procedure of Section 3 is applied to these cases. If even one of them
receives a different decision, weighting does not begin, and the discrepancy is published.

| No. | Case | Expected decision |
|---|---|---|
| 1 | A font, icons and a theme obtained with a package | No gap under version 4: an installed object (question 1). Under version 3 this was a gap in the wording. |
| 2 | An installed package that contains only dependencies | No gap under version 4: an installed object. Under version 3, a gap in the wording. |
| 3 | A compiled copy of code that a program builds itself | No gap under version 4: covered by the line of the original package. Under version 3, a gap in the wording. |
| 4 | A browser extension that a person installed in their own profile | No gap: an installed object with a line of its own. |
| 5 | A game downloaded and installed by a game store | No gap in the definition: a program, which must be recorded. By what means a system ensures this is not part of the definition (Section 8.5) and is checked on the testbed. |
| 6 | The command `curl … \| bash` typed by a person | No gap: a command is the person's action. What the script has left on the computer is decided for each object it has left. |
| 7 | A personal setting of a program, for example an editor theme | No gap: a program record, which need not be recorded. |
| 8 | An object that the system itself creates anew after removal, under the text of version 3 | A gap in the idea of version 3: the removal test gave no answer for it, and the criterion had to be replaced. |

## 5. What is done beyond the plan

These investigations are not part of the outcomes of the four checks and are reported separately.

- Contradictions within the text of Sections 8.1–8.3: every pair of sentences.
- Inventories of lived-in disposable machines of three kinds: a developer's workstation; a gaming computer with
  a game store; a server with containers. The actions on each are fixed in the inputs before the first
  inventory.
- The installation and configuration channels of the fourth paper (Section 4.5): where, by the text of
  version 4, what each of the 88 channels leaves belongs.

## 6. What will not be done

The text of version 4 is not edited until the checks are finished. The cases of Section 4 and the procedure of
Section 3 are not changed after publication. The search does not stop at the first gap found: all the machines
and all the investigations listed above are checked.
