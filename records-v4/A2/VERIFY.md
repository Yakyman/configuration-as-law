CARDS: 0 confirmed of 0

# A2-V — verification of the A2 cards and of the pair sweep

Verification of `A2/CARDS.md` against `TEXT.md` Section 8 and `SENTENCES.md`. The verification took no part in A2.
Working files: `verify/completeness.py` and `verify/completeness.txt` (completeness), `verify/sample.py` and
`verify/sample.txt` (sample), `verify/sources.md` (documentation passages fetched for this verification).

## Cards

`CARDS.md` has the first line `CARDS: 0` and contains no card. There is nothing to confirm or refute.

| Card | Title | Verdict | Sentence ID with quote or source | Reasoning |
|---|---|---|---|---|
| — | (no cards) | — | — | CARDS.md states that no examined candidate passed the filter. |

## Confirmed gaps in the verification's own wording

None: there is no card. The new candidate N1 found in the sample check (below) is stated there.

## Sample of the pair sweep

### Completeness of the table

- `PAIR_SENTENCES.tsv` lists 39 sentences (S8.1-1 … S8.1-16, S8.2-1 … S8.2-23). `PAIRS.tsv` has 741 rows, which is
  39 × 38 / 2; 741 distinct unordered pairs, no duplicates, no missing pair, no pair outside the list
  (`verify/completeness.txt`). Results: 713 “consistent”, 28 “settled by the order”, 0 “collision”.
- Measured against TASK-A2 (the deciding sentences of Section 8.2 and the definitions of Section 8.1 they rely on), the
  table is complete.
- Measured against PROTOCOL.md Section 5 (every pair of sentences of Sections 8.1–8.3), it is not: the 8 sentences of
  Section 8.3 are not in the pair table, so 340 pairs (8 × 39 cross pairs and 28 pairs inside Section 8.3) are not
  rows of `PAIRS.tsv`. `PROPERTIES.tsv` examines Section 8.3 in 28 grouped rows that cite S8.3-1, S8.3-4, S8.3-5,
  S8.3-6, S8.3-7 and S8.3-8; S8.3-2 and S8.3-3 are cited nowhere. Which of the two scopes applies is not decided here.
- The 741 rows use 14 distinct witness objects; 399 rows use the same unchanged gawk package. As `README.md` says, a
  “consistent” row means consistent on its stated witness, not that no object makes the pair collide.

### Sample

Seed 20261123, Python `random.Random(seed).sample` over all 741 eligible rows (every row is “consistent” or “settled
by the order”), 30 rows, sorted by file line (line 1 = header). All 30 drawn rows are “consistent”.

| File line | Pair | Witness | Check |
|---|---|---|---|
| 32 | S8.1-1 × S8.2-16 | gawk package | Holds: the definition of the declaration and the package-line rule give no opposite answer. |
| 48 | S8.1-2 × S8.1-11 | gawk package | Holds: direction of conformity and service/account in-force test do not meet on this or any object. |
| 53 | S8.1-2 × S8.1-16 | gawk package | Holds: no breaking is involved. |
| 56 | S8.1-2 × S8.2-3 | gawk package | Holds. |
| 64 | S8.1-2 × S8.2-11 | gawk package | Holds: Q1 places the packaged shell file before Q3 is asked. |
| 77 | S8.1-3 × S8.1-4 | gawk package | Holds: different subjects (declaration files, installer). |
| 92 | S8.1-3 × S8.2-3 | gawk package | Holds: no opposite answer on the witness. |
| 105 | S8.1-3 × S8.2-16 | gawk package | Holds. |
| 115 | S8.1-4 × S8.1-7 | Emacs package menu | Holds: S8.1-7 lists an installer among built-in tools. |
| 165 | S8.1-5 × S8.2-7 | Emacs package menu | Holds: the extension is what the built-in installer installs as a whole, so Q1 answers yes. |
| 179 | S8.1-5 × S8.2-21 | Emacs package menu | Holds on the witness (Emacs Lisp can launch programs, so S8.2-21 does not apply). The same pair on a browser extension leads to candidate N1 below. |
| 192 | S8.1-6 × S8.2-1 | gawk package | Holds. |
| 280 | S8.1-9 × S8.1-12 | gawk package | Holds: presence test and line-stated state do not conflict. |
| 290 | S8.1-9 × S8.2-6 | gawk package | Holds. |
| 336 | S8.1-10 × S8.2-23 | authorized_keys entry | Holds: sshd reads the file as values. |
| 352 | S8.1-11 × S8.2-11 | authorized_keys entry | Holds. |
| 388 | S8.1-12 × S8.2-20 | SQLite table records | Holds. |
| 399 | S8.1-13 × S8.2-5 | systemd unit enabled/running | Holds: the process follows its unit; application concerns the required state. |
| 436 | S8.1-14 × S8.2-17 | gawk package | Holds. |
| 479 | S8.1-16 × S8.2-13 | authorized_keys entry | Holds: no superuser power, so no breaking; S8.2-13 names means of login as a setting. |
| 484 | S8.1-16 × S8.2-18 | SSH default host key | Holds. |
| 507 | S8.2-1 × S8.2-19 | gawk package | Holds: optional extra recording does not oppose a duty. |
| 554 | S8.2-4 × S8.2-6 | Emacs package menu | Holds: the typed command is an action, the extension an object placed by Q1. |
| 575 | S8.2-5 × S8.2-9 | Bash history re-executed by fc | Holds: the history file outlives the process; Section 8.6 reasons the same way. |
| 580 | S8.2-5 × S8.2-14 | systemd unit | Holds. |
| 591 | S8.2-6 × S8.2-8 | gawk package | Holds. |
| 670 | S8.2-11 × S8.2-17 | gawk package | Holds. |
| 672 | S8.2-11 × S8.2-19 | gawk package | Holds. |
| 678 | S8.2-12 × S8.2-14 | authorized_keys entry | Holds: both make the entry a setting. |
| 692 | S8.2-13 × S8.2-18 | SSH default host key | Holds: no external list is involved. |

Result: 30 of 30 sampled dispositions hold on their stated witnesses. No sampled pair is itself a collision.

### New candidate N1 (reached from line 179; the colliding pair is line 509, outside the random sample)

| Candidate | Title | Verdict | Sentence ID with quote or source | Reasoning |
|---|---|---|---|---|
| N1 | Must restricted code installed inside a recorded program be recorded? | CONFIRMED (collision) | S8.2-1 “Everything that is installed and every setting must be recorded.” against S8.2-21 “Code that runs inside a recorded program and cannot itself launch programs or change what is installed and the computer’s settings—a web page in a browser, a guest system in a virtual machine—need not be recorded.” | For an installed browser extension both sentences apply literally and prescribe opposite duties; no sentence says which prevails. |

The object: the Dark Reader extension for Firefox, listed on addons.mozilla.org. Its Firefox manifest requests only
alarms, contextMenus, storage, tabs, theme and all-URL access, with no optional permissions (verify/sources.md WX6).
Launching a native program needs the nativeMessaging permission and a native application the browser does not install
(WX1); uninstalling another add-on needs the management permission (WX2); opening a downloaded file with its application
needs downloads.open (WX3). The browser keeps installed add-ons and uninstalls one by its ID (WX4); an extension is a
collection of files packaged for installation, with scripts that respond to browser events (WX5).

Placement by the text: Firefox counts as an installer in its add-on part (S8.1-5), the extension is a package
(S8.1-6), and Q1 answers yes (S8.2-7), so it is an installed object, and S8.2-1 requires it to be recorded. Its scripts run
inside the recorded browser and cannot launch programs or change what is installed or the computer's settings, so
S8.2-21 says it need not be recorded.

Closest sentences and why they do not decide:
- S8.2-6 orders the four questions, which decide what an object is. S8.2-21 assigns no kind and the case's kind is not
  disputed (installed object). The order does not say whether S8.2-1 or S8.2-21 governs the duty to record.
- S8.2-19 “What need not be recorded may also be recorded in the declaration.” This permits recording but does not
  say whether recording is required.
- A2 (REVIEW.md, “Restricted interpreted code”) settles the same pair on the gawk join.awk function by an “ordinary
  specific-exception reading”. No sentence of Sections 8.1–8.3 says that a clarification prevails over S8.2-1. That
  priority rule is added to the text, which (not published: orchestration) forbids, so the A2 rejection does not stand.
- Section 8.6, which is reasoning, not part of the definition, reads the opposite way for exactly this object:
  quote: “An installer built into the browser installs and removes it as a whole: an installed object, recorded.”
  That the A2 reading and the authors' own table disagree shows that Sections 8.1–8.3 do not settle the case.
- Section 8.5 puts outside the definition “how it adds to the declaration what has been installed by a program that
  itself downloads other programs”, that is, the mechanism, not whether the object must be recorded. Not OUTSIDE.

Different declarations: under S8.2-1 every such extension needs a line (or a covering line), and an extension the user
adds through the add-on manager without one breaks P1; under S8.2-21 the declaration may omit it and P1 holds.

The gap in the verification's own words: An extension that the browser installs as a whole is an installed object, and
the rule says that everything installed must be recorded. The same extension is code running inside a recorded program
with no power to launch programs or to change installation or computer settings, and a clarification says that such code
need not be recorded, and no sentence says which of the two prevails.

Other objects in the same gap: other extensions of the same browsers without the permissions named above; the gawk
join.awk function and other restricted interpreted code that Q2 makes a program (S8.2-10: a program belongs to what is
installed); stored SQLite trigger code; PAC scripts (all examined by A2 and rejected on the same specific-exception
reasoning).
