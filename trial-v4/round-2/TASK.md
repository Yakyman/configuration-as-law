# TASK — draft classification under a rule text (second text)

Work folder: `trial-v4/round-2/` (all paths below are relative to it unless
absolute). Write only inside this folder. No sudo, no installs, no virtual machines, no graphical programs, nothing
public.

## What this is

`PAGE.md` is a short rule text in Russian that says which objects of a computer must be recorded in the computer's
declaration. Every sentence has an ID (D1, I1, R1, Q1, L1, U1, …). The text is FIXED. Your job is to find out, object
by object, whether this text is enough to decide. You are not asked to like the text, to improve it or to repair it.

- Read the text literally and strictly. Do not be generous to it: when a sentence fits a case only after you add a
  word to it, it does not fit.
- Never invent a rule to decide a case. If the text does not decide a case, say so; if it decides a case both ways,
  say so. Do not propose a fix.
- The order of the four questions Q1–Q4 is part of the text (R6): the first question answered «yes» decides.
- That existing distributions do something in different ways is not a gap of the text.

## Independence

This is a clean-room classification. Read ONLY:

- this folder;
- the raw inventory files that the `evidence` column points to, under
  `records-v3/D1/in/raw/`,
  `records-v3/A1/in/raw/`,
  (not published: unreduced inventory) and
  `records-v3/A3R/in/raw/`;
- public documentation on the web (cite the URL).

Do NOT read anything else under `<HOME>/Projects/` (in particular no other file or folder of `night-1122`, of
`cal-paper/v2`, `v3`, `v4` — including `v4/dryrun/` — of `configuration-as-law`, no `izr-definition.md`), nothing
under `(not published: tooling configuration)` or `(not published: tooling configuration)`. Earlier classifications of these same objects exist there
under older, different rule texts; seeing them would spoil this run. The same restriction binds every part of this
work.

## Input

Three tables, tab-separated, UTF-8, one object per row, header `id part machine kind name members evidence`:

- `in/rows-d1.tsv` — 1843 objects from clean installations of Fedora, openSUSE Tumbleweed, Linux Mint, Flatcar;
- `in/rows-a1.tsv` — 1084 objects from clean installations of an earlier round (CoreOS, Guix, NixOS, Debian and others);
- `in/rows-a3r.tsv` — 2010 objects outside system packages from a lived-in Debian desktop.

The objects were found on real machines by an inventory tool. `evidence` quotes the inventory or names a raw file. A
row whose `kind` ends in `:subtree` or whose `members` is greater than 1 is a group of stored objects under one
directory. Some long fields are cut (marked «cut here»); the full value is in the raw file named in `evidence`.
Wording inside `kind` or `evidence` that sounds like a class («recorded», «closure», «works», «evidence») comes from
the inventory tool of an older definition: ignore it and decide only by `PAGE.md`.

`CASES.md` holds fifteen separately described cases.

## What to decide for every row

1. `kind` — what the object is by the text:
   `INSTALLED` (установленное that is not itself executed code: a package, or a non-code part received in a package, Q1),
   `PROGRAM` (Q2),
   `SETTING` (Q3, Q3a, Q3b),
   `PROGRAM_RECORD` (запись программы, Q3b or Q4),
   `MATERIAL` (материал, Q4),
   `RUNTIME` (exists only while the computer runs and is not a separate object, R5; name in `reason` the program or
   setting it belongs to and give that object's `record`),
   `ACTION` (a person's action, R4),
   `NONE` (cannot be said).
2. `record` — `YES` (must be recorded by a line of its own), `COVERED` (needs no line of its own because a line named
   in L1, L2 or L3 covers it), `NO` (need not be recorded), `NA`.
3. `status`:
   - `DECIDED` — the text decides, and decides one way;
   - `NOT_DECIDED` — the text does not allow deciding what the object is or whether it must be recorded;
   - `TWO_WAYS` — the text allows deciding both ways and no sentence says which prevails;
   - `FACT_UNKNOWN` — a fact about the object cannot be established from the evidence, the raw inventory files and
     public documentation, AND the decision depends on that fact. If every possible value of the unknown fact gives
     the same `record`, the row is `DECIDED`: say so in `reason`. Do not guess;
   - `MIXED` — a group row whose members get different decisions (say which members get which).

You may decide a homogeneous kind of objects with one written rule applied by a script — but the rule must itself
follow from cited sentences of `PAGE.md`, you state it in `out/RULES.md`, and you check by hand 10 rows per rule
(list their ids in `out/RULES.md`) that the rule fits them. Everything that is not homogeneous is decided row by row.

## Output

For each input table `in/rows-<set>.tsv` write `out/rows-<set>.tsv`, tab-separated, UTF-8, header exactly:

`id	kind	record	status	sentences	what_it_does	basis	reason`

- `sentences`: IDs from `PAGE.md` that decide the case, comma-separated; for `NOT_DECIDED` and `TWO_WAYS` the
  sentences that come closest or that conflict;
- `what_it_does`: at most 15 words;
- `basis`: `evidence`, `raw:<file>`, `doc:<url>` or `none`;
- `reason`: at most 30 words; for `NOT_DECIDED` say exactly what the text lacks, for `TWO_WAYS` name the two
  readings. No tabs or line breaks inside a field.

One output row per input row: the same ids, nothing skipped, nothing added. Append finished rows as you go, so that an
interruption loses nothing; if an output file already holds rows from an earlier attempt, keep them and continue with
the ids that are still missing.

Also write:

- `out/CASES-ANSWERS.md` — for each of the fifteen cases of `CASES.md`: `kind`, `record`, `status`, sentences and at
  most 60 words of reasoning. If a case holds several situations, answer each.
- `out/HOLES.md` — every `NOT_DECIDED` and `TWO_WAYS` row grouped into kinds of gap. For each kind: one sentence
  saying what the text lacks or which two readings exist; the sentence IDs involved; the number of rows per table;
  three example ids. No fixes. If there is none, say so.
- `out/UNKNOWN.md` — the `FACT_UNKNOWN` rows grouped by the kind of missing fact, with row counts per table and
  three example ids per group.
- `out/SUMMARY.md` — counts per table and per status, counts per `kind` and `record`, the number of script rules.
- `out/DONE` — written last, holding the row counts per status, after a script has verified that the ids of each
  output table equal the ids of its input table (same set, same count, each once) and that every `kind`, `record`
  and `status` is one of the allowed words.

## Limits

- The work may be divided into at most 2 parallel parts, each under these same instructions and the same reading
  restriction; each part writes to `out/rows-<set>.<k>.tsv` and the parts are merged. A part is not divided further.

Final report: the counts per status for each table, and nothing else.
