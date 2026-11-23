# Review of cards 1, 7 and 8

Scope: every row of (not published: outside selected checks and direct evidence) was searched by kind and name; stored groups were matched against their actual listed members, and subtree rows against their prefixes. Raw filesystem evidence is (not published: over 20 MB: raw trace, snapshot, index or operational log), six NUL-separated fields per entry (path, type, mode, uid, gid, link target). The full confirmed memberships, concrete source pairs and named regeneration evidence are in `code_extent.tsv`; uncertain memberships from the original card are separately in `code_unknown.tsv`. A directory group counts when a represented member contains a qualifying object; the group's own directory marker is not permission to count every object below `/`.

## Card 1 — CONFIRMED, narrowed: executable caches with source fallback

Regenerable editor and interpreter caches are both code executed with the program's rights and dispensable copies whose removal changes speed. The text provides both the cache exemption and the code requirement without stating which applies to their overlap.

S2.2-5: “cache: after it is removed, the computer does the same, only more slowly;”

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.2-13: “A file that a program executes as code counts as code even when it holds settings; a file that a program only reads as values counts as a setting;”

Refutation attempted: S2.2-13 expressly resolves code versus settings, but does not resolve code versus cache; S2.5-1 addresses treatment of state, not whether executable cache objects meet Section 2.2. Neither disposes of the collision between S2.2-5 and S2.2-10. This is two sentences colliding, not a missing object taxonomy.

Confirmed extent: **115 rows**, including two not assigned to card 1 in the adjudication: `4977b521c631e8b76eb7538b` `/home/user/Projects` and `lived-t59f3c9499d` `/var/lib/flatpak/runtime/org.gnome.Platform`. Compiled suffix alone is insufficient: the extent builder verifies that the corresponding `.py`, `.el` (or `.el.gz`), decoded `.lua`, or uncompiled zsh source exists in the raw inventory; native Emacs trampolines and the lazy.nvim generated package cache instead carry explicit named-consumer evidence. Unpaired compiled paths are saved separately in `code_unpaired.tsv` and cannot establish membership. The added runtime row contains standard-library Python bytecode with its source present. Both that row and its runtime ancestor use `unittest/__pycache__/result.cpython-313.opt-2.pyc` as witness, with (not published: external working record) present; this is interpreter library code with the standard import loader. Extent concerns represented objects, including code that can be started; it does not assert every compiled module ran during the inventory. The other 113 memberships were already assigned to card 1.

Examples: `dd743d5660f8360b1a7dd17e` `/home/user/.emacs.d/elpa/embark-consult-20260503.118` contains the Lisp source and its compiled `.elc`; `lived-tcf3018d0d8` `/home/user/.emacs.d/eln-cache/30.1-c7a97098` contains five native trampolines; `8116f43e8ff91b41a1de6d2b` `/home/user/.cache/nvim/luac` contains Lua bytecode whose encoded paths identify the source; `00be4be3f78767b555ebdc00` `/home/user/.local/state` contains the generated Lua package cache. Their named functions and consumers are recorded in `../adjudication/rows.tsv`; presence and source/compiled pairs are independently checked in the filesystem inventory.

The original **132** is not an exact verified extent: **19 original memberships are uncertain**, and **2 additional memberships** are present. The seven card examples were individually challenged: the three compiled editor examples and the generated Lua example survive; the Go shell-script cache, Cargo executable fixture and repository pathname do not supply sufficient evidence of the cache/removal/actual-consumer conjunction. The script and fixture can be started, but removing their paths need not merely slow that operation; re-downloading a package is not itself proof of S2.2-5. Repository deployment hard links do not show execution through the repository's hashed names. Those assertions are not established false, so the whole card is neither FACT-WRONG nor REFUTED.

The GL.default row `lived-ta0d1cc4da2` is additionally UNKNOWN, beyond the 19 uncertain original memberships: source pairs exist in its shipped license/source tree, but their existence does not establish runtime loader use or fallback. All source/documentation bytecode is excluded as a witness; the resulting uncertainty ledger has 20 rows.

Other excluded candidates: V8 cache rows do not establish rights of the particular execution context; generated dictionaries-common Lisp does not establish automatic fallback after deletion. The two `.oh-my-zsh` rows are also uncertain: the saved notes describe generating and sourcing `grep-alias`, but do not establish the startup branch that regenerates it if missing. Go `go-build` entries were searched across the whole table: `-d` files are build artifacts and the inventory does not show they are executing caches. Mesa shader-cache entries also fail to establish S2.2-10's ability to do whatever the executing program can do. Neither class becomes an additional confirmed hole merely because it contains compiled bytes. Unknown membership is not an additional textual gap.

## Card 7 — CONFIRMED: history stored as executable editor code

Saved editor history is explicitly exempt as a record of the past. When the editor restores it by executing Lisp or sourced commands with its own rights, the code requirement also applies and the text gives no precedence.

S2.2-6: “records of the past—logs, history;”

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.5-1: “How to treat data and program state, the remains of removed programs, user authority, generations and rollback, the transfer of accumulated state to another computer, when an edit of the declaration takes effect, and how to protect the declaration itself and secrets are questions of the design of a system built on the hypothesis, not conditions of declarativeness.”

Refutation attempted: S2.2-13 says files executed as code count as code even when they hold settings, but it does not withdraw the history exemption. S2.5-1 excludes design questions about treating program state; it does not decide the simultaneous recording obligations of history already executed as code. Two sentences collide.

Confirmed extent: **7 rows**, listed under card 7 in `code_extent.tsv`: `/home`, `/home/user`, `/home/user/.emacs.d`, `/home/user/.emacs.d/savefile`, `/home/user/.local`, `/home/user/.local/state`, and `/home/user/.local/state/nvim`. Examples are `99b8709d5a3af244262c5442` `/home/user/.emacs.d/savefile` (recentf and savehist), `00be4be3f78767b555ebdc00` `/home/user/.local/state` and `lived-tbba8c81784` `/home/user/.local/state/nvim` (sourced session). The raw inventory confirms all three named saved files; the consumer facts are recorded in the corresponding adjudication notes. These seven memberships overlap card 1 except savefile; unlike the earlier cards, overlap is retained.

## Card 8 — REFUTED: document type does not exempt executable behavior

S2.2-4: “content—documents, photographs, the contents of databases: after it is removed, the computer does and can do the same, and only the content itself is unavailable;”

S2.2-10: “code that another program executes must be recorded if the program runs it with the program’s own rights, so that the code can do whatever the program can do: scripts executed by an interpreter (python, bash), shell startup files, an editor configuration written in the editor’s programming language.”

S2.2-2: “The test is removal: if, after an object is removed, the computer stops doing something or something becomes impossible on it, the object must be recorded.”

The card's premise itself says the embedded macro builds a font sample with the office program's rights. S2.2-10 therefore requires that macro; S2.2-4 cannot exempt it, because removing the macro removes executable font-sample-building behavior, not merely the document's content. S2.2-4 exempts the notes and PDF members of `fd76e7d51f3623288353a7c8` `/home/user/Documents`; the same row is mixed because its macro member is required. Reading the word “documents” alone and discarding the rest of S2.2-4 creates the apparent contradiction. No claim is made that the raw inventory contains the document bytes; the refutation grants the card's own stated macro behavior.
