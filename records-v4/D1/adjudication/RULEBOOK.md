# Adjudication rulebook for D1 (internal working rules of the adjudication)

Applies to every part of the adjudication of `D1/compare/to-adjudicate.tsv`. Read (not published: orchestration or scratch), `TEXT.md`
Sections 8.1–8.2, 9.2, Appendix A.4.1 and `SENTENCES.md` first. Times UTC, English, no personal names, no host
names, no home paths of the host, no personal provenance; the classifications are "c1" and "c2".

## Verdicts

- `RESOLVED:<WORD>` — WORD one of INSTALLED-OWN, INSTALLED-PACKAGE, INSTALLED-DERIVED, PROGRAM-OWN, PROGRAM-DERIVED,
  SETTING-OWN, SETTING-DEFAULT, RECORD, MATERIAL, RUNTIME, ACTION. Needs: the sentence ID (or IDs, comma-separated)
  that decides, the exact quote (whole sentence or its deciding part, copied from `SENTENCES.md`; the quote check
  ignores `*` and whitespace; parts may be joined with ` [...] `), and `erred` = c1, c2, both or none.
- `UNKNOWN` — the decision depends on a fact that neither the inventory, the facts files nor public documentation
  establishes; the note names the fact. A classification's UNKNOWN is NOT accepted just because it says so: first try
  to establish the fact from the inventory (`D1/in/FACTS.md` says where each fact is).
- `GAP` — no sentence decides, or two sentences decide oppositely and neither the order of the four questions nor any
  sentence says which prevails. Use one of the hole slugs below; if a row is a gap of a new kind, invent a short
  slug and describe it in the part's `HOLES-NEW.md` (2 sentences + sentence IDs + the two decisions + example ids).
- MIXED rows (members of a directory with different decisions): decide each member class in the note; the verdict is
  GAP only if some member is a gap (hole = that gap); otherwise if some member is UNKNOWN the verdict is UNKNOWN;
  otherwise RESOLVED with the word of the members if they share one, else `RESOLVED:MIXED` is NOT allowed — use the
  word of the largest member class and list the others in the note (the note must say "members:" with the classes).

Strictness: if a sentence fits only after adding a word, it does not fit. Do not call a gap what a sentence plainly
decides. What Section 8.5 puts outside the definition (storage of records and material, generations and rollback,
etc.) is not a gap. That systems differ is not a gap.

## Established reading of the text (apply consistently)

1. Q1 (S8.2-7): a package file that remains as received is an installed object, covered by the package line
   (S8.2-16 "the line of the package as part of which it was obtained"). "Remains as received" must be shown by
   the inventory: `package-files.tsv` integrity `unchanged`, or a full digest equal to the manager record, or for a
   symlink the target equal to the manager's link record; for a directory, presence in the manager's file list with
   the recorded mode. A prefix signature alone is not integrity, except when the file is no longer than the prefix
   (then it is the full sha256). npm/pip files: ctime equal to the install moment with an unchanged RECORD digest
   (pip) is acceptable only if the inventory shows it; otherwise UNKNOWN.
2. A package with reason `dependency` → INSTALLED-DERIVED (S8.2-16 "a package installed as a dependency of a
   recorded package"); reason `explicit` → INSTALLED-OWN; a package under another package's own `node_modules`
   is a dependency of that package; a package whose files belong to a native package (manager's own manifest) is
   part of that package → INSTALLED-PACKAGE.
3. Q2 (S8.2-9): code the computer executes. Compiled bytecode (.pyc) built by the system from package sources →
   PROGRAM-DERIVED (S8.2-10 + S8.2-16 "a compiled copy"). A script written by a person → PROGRAM-OWN. Shell start
   files copied from /etc/skel by useradd (code Bash executes, S8.2-23) → PROGRAM-DERIVED only if the copy source is a
   package file and the copy is shown unchanged; otherwise UNKNOWN (fact: copy unchanged).
4. Q3 (S8.2-11..14): a value chosen by a person that the computer as a whole obeys → SETTING-OWN (S8.2-17 first
   clause). A setting value obtained with a package and remaining as received is an installed object by Q1 (order).
5. Q4 (S8.2-15): written by a program as it ran (log, cache, history, working state, PID files, lock files, program
   databases, browser profile state) → RECORD; created or brought by a person (downloads, directories made by the
   person) → MATERIAL.
6. S8.2-5: what exists only while the computer runs (on tmpfs `/run`, `/tmp` if tmpfs, `/dev`, `/proc`, `/sys`, a
   process, an open port, live netfilter state) → RUNTIME, when the inventory shows the backing is runtime
   (persistence `runtime`, or a documented tmpfs mount captured in the inventory). If backing is unknown, the fact
   is missing → UNKNOWN (name it), unless documentation of the system states the path is always tmpfs — cite it.
7. A directory not in any package manifest, created by an installer or a program as it ran → RECORD (S8.2-15).

## Known gap kinds (hole slugs)

- `default-at-install` — a value created during a package's installation by a script/preset/sysusers/alternatives,
  not shipped in the package, chosen by no person (system accounts/groups created by package scripts, preset
  enablement links, default alternatives links). Q3 (S8.2-11) requires "a value chosen by a person", so by the
  order it would be a program record (S8.2-15); but S8.2-13 lists services and accounts as settings and S8.2-17
  covers "a default value obtained with a package or created during its installation" by the package line.
  SETTING-DEFAULT vs RECORD.
- `generated-list` — non-code data the system generated from installed packages (MIME database, icon/font caches,
  compiled schemas, module dependency lists, ld.so.cache, hwdb, generated man-page links): by the order Q4 makes it a
  program record (S8.2-15 "cache"), while S8.2-16 names "a generated list" among what is installed, recorded by the
  derived line. RECORD vs INSTALLED-DERIVED.
- `old-version-leftover` — files kept from an earlier version of a package that is still installed in a newer version
  (e.g. old kernel modules kept by preserve). Q1 asks whether the object was obtained as part of "a package installed
  on the computer"; the text does not say whether an earlier version of an installed package is that package.
  INSTALLED-PACKAGE vs PROGRAM-OWN/RECORD (Q2/Q4).
- `archive-of-code` — a stored archive or image whose contents are executed but which is itself only unpacked or
  loaded (initramfs, boot images built by tools): S8.2-9/S8.2-23 do not say whether an archive of code is code.
  PROGRAM-DERIVED vs RECORD.

## Output of a part

(not published: record outside selected evidence) with header `id	verdict	sentence_id	quote	erred	hole	note`, one row per input
row of the part, `note` ≤ 30 words. Facts used must be cited in the note (file name relative to (not published: record outside selected evidence))
or in `parts/<part>.facts.md`. Scripts go to (not published: record outside selected evidence), raw outputs to `D1/adjudication/raw/`.
Run `/usr/bin/python3 -I (not published: orchestration or scratch) D1/adjudication/parts/<part>.tsv` until 0 quotes are missing.
Python: write scripts to files and run them with `/usr/bin/python3 -I <file>` (code on stdin is blocked).
