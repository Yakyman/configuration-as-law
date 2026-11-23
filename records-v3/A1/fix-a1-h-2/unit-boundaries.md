# H1: the 21 units excluded under both recorded readings

Date: 2026-11-22 UTC. Review-2 finding 1 is accepted. This record supersedes the treatment of these 21 rows as READING-DEPENDENT in `A1/fix-a1-h-1/`, `../FIX-A1-H-1.md` and the previous `../QUESTIONS.md`. The prior round remains unchanged as a dated record. No other boundary or classification is revised.

For the managed-unit reading, the object is the managed service/mount/target with its state, not the settings in its backing fragment. The prior H1 argument applies only after substituting that file for the object; it supplies no H1 membership under the managed-unit reading (`../fix-a1-h-1/unit-boundaries.md`, Findings 1 and 2). This is a limit of that H1 claim, not a new exemption for services or a decision about their overall recording requirement.

For the backing-file reading, these exact 21 rows have saved disabled states in the matching manager scope. The saved primary manual defines disabled as containing installation instructions (`A1/fix-a1-h-1/raw/systemctl-v260.xml:1116-1117`); the unit manual assigns those instructions to systemctl rather than the runtime manager (`A1/fix-a1-h-1/raw/systemd.unit-v260.xml:2241-2246`). The file reading therefore fails the single-program premise used by this H1 claim. This evidence was already established in round 1; no new probe or lookup is needed. Per-row source paths, line numbers, states and both outcomes are in [reading-outcomes.tsv](reading-outcomes.tsv).

S2.2-7: “settings that are in force only inside one program, for example the home page, theme, and extensions of a web browser.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

Thus both recorded object readings exclude these rows from this H1 claim. `EXCLUDED-BOTH-READINGS` records that conjunction without choosing a reading, applying a multiple-reader label to the managed unit itself, assigning MUST/NOT, or asserting that every other possible wording question is resolved. The remaining 501 inventory-unit candidates retain the unresolved object reading; they are not factual unknowns or confirmed H1 members. The 76 stored unit files remain factual unknowns. No decision rule is added to the published text.

The new partition is 85 confirmed standalone + 29 confirmed constituent + 243 factual unknown + 501 reading-dependent + 21 excluded under both readings + 35 previous exclusions = 914 unique candidate rows. Established H1 membership remains 114. The 21 changed IDs occur in neither sample, so both audit results and sample selections remain unchanged. [Changes](changes.tsv) and [counts](counts.json) record this round's delta; the earlier 607 membership changes and 614 total changed records remain historical round-1 counts.

Run `/usr/bin/python3 -I A1/fix-a1-h-2/recompute.py` from the night folder. It reads round-1 records and the already saved evidence; it writes only into this new output directory. Only these 21 rows change in the extent, reader checks and whole-table index. It does not run the earlier recomputation or regenerate samples.
