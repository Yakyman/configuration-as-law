VERDICT: DISAGREE

Second review of the inputs of step 2 of Supplement 1, `SUP1/step-2.md`, after `SUP1/REVIEW-STEP2.md`. It checks the file against `SUP1/SUPPLEMENT-1.md` (step 2 and the rules line), `PROTOCOL.md` Sections 2–4, `TEXT.md` Section 9.2 with Appendix A.4.1, `SENTENCES.md`, and the first line of `W0/RESULT.md`. Reviewed 2026-11-23 UTC. Paths are relative to the night folder.

Checked, with no problem found:

- All nine findings of `SUP1/REVIEW-STEP2.md` are carried out word for word. Findings 1 (both places), 2, 3, 4, 5, 6, 7, 8 and 9 each appear in `SUP1/step-2.md` exactly as their minimal fixes state.
- The quotation in the last sentence of part 2, “must this be in the declaration, if the declaration describes everything installed and every setting”, matches `PROTOCOL.md` Section 2 exactly. The second question, which is not quoted, keeps the words of the second sign.
- The family outcome rule matches Appendix A.4.1. “Two readings … counts as receiving two decisions” matches Section 9.2 (“allows deciding both ways”). “A deciding fact remains unknown gives “?”” matches Section 9.6.
- Sample of six claims, each confirmed:
  - The SHA-256 of `D1/compare/joined.tsv` is `a0921b41…216d` and that of `A3/compare/joined.tsv` is `b23d7175…05c4`. Both are as stated.
  - (not published: orchestration or scratch) has `SEED, SIZE = 20261123, 300`.
  - The interpreter is Python 3.14.10.
  - `D1/adjudication/HOLES.md` has cards 1–5, `A3/adjudication/HOLES.md` has cards 1–7, and `B1/fix-b1-1/GAPS.md` has three gap sections plus one section of cited text. Their titles match families 1–15.
  - Card 2 of `A3/adjudication/HOLES.md` reads “Neither needs a line, so the declarations do not differ”. This supports the expectation for family 7.
- Nothing in the file goes beyond its task. It contains no personal name, host name or home path.

1. **Gaps are weighted although the calibration of `PROTOCOL.md` Section 4 did not pass.**
   Where: `SUP1/step-2.md`, “Rules of Supplement 1”, together with the last sentence of part 2 of “What is done”.
   Evidence: `PROTOCOL.md` Section 2: “Every gap that is found additionally receives one of two weights”, which are gap in the wording and gap in the idea. Section 4: “Before any new object is weighted, the procedure of Section 3 is applied to these cases. If even one of them receives a different decision, weighting does not begin”. `W0/RESULT.md`, first line: “CALIBRATION: FAILED 2 of 8”. The last sentence of part 2 only collects answers, and on its own it does not contradict Section 4. However, the rules line then puts every gap found into the wording list or the idea list by the two signs of Section 2. That is weighting new objects, which Section 4 forbids now. `SUPPLEMENT-1.md` requires the two lists and also says “It does not change `PROTOCOL.md`”. Choosing between these two published requirements belongs to the author ((not published: orchestration or scratch): “A question only the author can decide … is never decided by you”). The step file decides it silently.
   Minimal fix: replace the rules paragraph with: “**Rules of Supplement 1.** Each case is attempted once. Every gap found is reported together with both parties' answers to the two questions of part 2, and the answers are published. Section 4 of `PROTOCOL.md` says that weighting does not begin if one of its cases receives a different decision, and its calibration did not pass (`W0/RESULT.md`: “CALIBRATION: FAILED 2 of 8”). Whether the two lists required by Supplement 1, gaps in the wording and gaps in the idea, are nevertheless made by the signs of Section 2 of `PROTOCOL.md` is recorded before the work as a question for the author. Until the author answers, no gap is put into either list. The lists do not affect the outcome.”

2. **Sampled agreements that turn out to be gaps never get the two questions, so they would fall to the idea list by default.**
   Where: `SUP1/step-2.md`, “What is done”, part 4; “Rules of Supplement 1”.
   Evidence: part 2 asks the two questions of `PROTOCOL.md` Section 2 only “for each example object”. The rules line sends a gap to the wording list “only when both signs are established, otherwise to the list of gaps in the idea”. A gap found in the sample (“counted in the same way”) has no answers. So it is placed in the idea list without any party being asked about it.
   Minimal fix: at the end of part 4, add: “For each sampled agreement that goes to adjudication, each party also answers, separately, the two questions of part 2.”

3. **The expected result is written as statements of fact, not as an expectation.**
   Where: `SUP1/step-2.md`, paragraph “Expected result”.
   Evidence: Only the bold label marks the paragraph as an expectation. The sentences themselves state results in the present tense: “families 2, 3, 4, 5, 11 and 12 still receive two decisions or none. Family 1 receives one decision. Family 7 receives two decisions …”. Quoted without the label, each one reads as an outcome. The paragraph also never says that it decides nothing. In particular, “At most 20 of the 600” could be read as a tolerance, but the outcome rule for the sample gives 0 for any agreement that does not follow from a sentence.
   Minimal fix: after the bold label, replace the text with: “It is expected that, with complete facts, families 2, 3, 4, 5, 11 and 12 will still receive two decisions or none; that family 1 will receive one decision; that family 7 will receive two decisions under which the declaration is the same; and that at most 20 of the 600 sampled agreements will not follow from a sentence. This expectation decides no outcome and is not a threshold.”

4. **The reference to `SENTENCES.md` points to the wrong folder.**
   Where: `SUP1/step-2.md`, line 3: “Sentence numbers refer to `SENTENCES.md` in this folder.”
   Evidence: `SUP1/` has no `SENTENCES.md`. The file is at the top of the night folder (`SENTENCES.md`). The night folder is also the base of the file's other paths ((not published: record outside selected evidence), (not published: record outside selected evidence), (not published: record outside selected evidence), (not published: record outside selected evidence)).
   Minimal fix: replace that sentence with: “Sentence numbers refer to `SENTENCES.md` in the night folder; all paths are relative to that folder.”
