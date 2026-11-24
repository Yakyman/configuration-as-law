# D1 questions for the author

Recorded 2026-11-23 UTC during FX-D1-H-1. These questions record unresolved readings; they do not amend the published text or postpone reporting a gap.

## A stored archive whose contents are executed

For the generated initramfs archives in `D1/fix-d1-h-1/raw/card4-extent.tsv`, does executing the extracted contents count as executing the stored archive as code under S8.2-9/23?

- Reading 1: extraction reads the archive as values; only the extracted files are executed. The generated archive reaches S8.2-15 as a program record and need not be recorded.
- Reading 2: the stored executable contents are code the computer can execute through the extraction and boot path. The archive is a program under S8.2-9/10, with recording by its source line under S8.2-16.

The documented mechanism holds under both readings; the text does not select the boundary. The case remains a confirmed gap and yields 0 under Section 9.2. No wording change is proposed.

## A generated list: classification or recording-line example

Recorded 2026-11-23 UTC during FX-D1-H-2. For the data-list members in `D1/fix-d1-h-2/raw/card2-extent.tsv`, how do S8.2-15 and S8.2-16 apply together?

- Reading 1: the four questions classify the object first; S8.2-16 supplies a recording line only for an object already classified as installed. A non-code generated cache reaches Q4 and may be omitted under S8.2-2.
- Reading 2: S8.2-16's generated-list example identifies a generated list as what is installed, so S8.2-1 requires its recording through the source-line option, despite Q4's record decision.

S8.2-6 orders the four questions and says the clarifications do not change that order; S8.2-16 is in a separate recording-line paragraph. No explicit priority between the competing readings is supplied. The card remains CONFIRMED, without choosing a reading or extending it to objects whose relevant source/use facts are unknown.

## An installed XPI: package classification and recording exemption

Recorded 2026-11-23 UTC during FX-D1-H-2. For the two installed XPI rows in `D1/fix-d1-h-2/raw/card5-extent.tsv`, does the archive/content boundary also determine the reach of S8.2-21?

- Reading 1: separate the archive/package from its qualifying contained code. Q1 and S8.2-1 require recording the installed package.
- Reading 2: the executable contents make the stored XPI itself qualifying code running inside the recorded browser. S8.2-21 permits omission while Q1 and S8.2-1 still require recording the installed package.

Q1's precedence settles classification, not this competing recording obligation. This depends on the same unresolved archive/content boundary as card 4, and remains a separate confirmed recording conflict. No author choice is inferred and no wording change is proposed.
