# D1 questions for the author

Recorded 2026-11-23 UTC during FX-D1-H-1. These questions record unresolved readings; they do not amend the published text or postpone reporting a gap.

## A stored archive whose contents are executed

For the generated initramfs archives in `D1/fix-d1-h-1/raw/card4-extent.tsv`, does executing the extracted contents count as executing the stored archive as code under S8.2-9/23?

- Reading 1: extraction reads the archive as values; only the extracted files are executed. The generated archive reaches S8.2-15 as a program record and need not be recorded.
- Reading 2: the stored executable contents are code the computer can execute through the extraction and boot path. The archive is a program under S8.2-9/10, with recording by its source line under S8.2-16.

The documented mechanism holds under both readings; the text does not select the boundary. The case remains a confirmed gap and yields 0 under Section 9.2. No wording change is proposed.
