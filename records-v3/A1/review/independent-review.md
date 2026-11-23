# Independent review of adjudication card 4 and the resolved sample

> **Supersession notice.** This file preserves the review chronologically. Its early H4 extent
> and negative-rule conclusions were superseded by later evidence. The current acceptance and
> remaining boundary findings are in `final-boundaries.md`; in particular, the Home
> aggregate remains confirmed, the outside-store aggregate is factual-unknown, and the six
> separate compiled-node outputs require downgrade because the runtime loads their copied union.

## Scope and conclusion

This review used (not published: outside selected checks and direct evidence), Sections 2–5 of `../../TEXT.md`, `../../SENTENCES.md`,
`../adjudication/HOLES.md`, `../adjudication/rows.tsv`, `../compare/joined.tsv`, the named raw
inventory, and the saved primary-source material under `(not published: adjudication scratch)`.

The code/cache collision in card 4 is **confirmed as a kind of case**. S2.2-10 requires recording
interpreter-executed code when it runs with the interpreter's rights, while S2.2-5 says that a
cache whose removal changes only speed need not be recorded. A compiled module that is actually
loaded, but whose removal causes the same source module to be loaded or compiled instead, meets
both descriptions. The text states no precedence.

The stated extent of 12 rows is not equally well established for every row. Four standalone
objects have direct saved evidence for both execution and source fallback, and one aggregate row
contains directly evidenced constituents of that kind. Seven are plausible instances of the same
generator pattern, but the saved record does not map each exact compiled store object to its
members, consumer, and corresponding source path. Conversely, six agreed standalone rows
elsewhere in the table are directly generated compiled-module outputs with separate source
outputs and should be included in the whole-table extent; a second aggregate contains the known
Home constituents.

## Existing card-4 rows

### Directly supported

- `guix-084d6fb332` and `guix-033f2e4eef`: the inventory identifies auto-compiled `.go` files for
  the retained `home.scm` and `config.scm` sources. The saved loader documentation says that a
  compiled file is preferred and that, when it is absent, the loader searches the fallback path
  and may create an auto-compiled file (`(not published: adjudication scratch)`, lines
  186–216). These are executed code under S2.2-10 and caches satisfying the removal description
  in S2.2-5.
- `guix-eaca1bed67`: `A1/in/raw/guix/system-boot.scm` puts the source `module-import` in
  `%load-path` and the exact compiled `module-import-compiled` in `%load-compiled-path`. The same
  saved loader documentation establishes source fallback.
- `guix-5e84abb70c`: the c1 record identifies the exact compiled activation-module path and the
  corresponding source modules as loadable in its absence. This is the same literal collision.
- `guix-25ad6943ae`: the Home aggregate contains two `module-import-compiled` objects and the
  corresponding source `module-import` objects
  (`../in/raw/guix/home-closure-outside-system-and-user.txt`). The group also contains ordinary
  MUST and NOT members, but its compiled-module constituents retain the card-4 collision. This is
  an affected aggregate row, not itself a speed-only cache when treated as one indivisible object.

### Likely, but not individually demonstrated by the saved record

The remaining seven current rows are `guix-4693999f1c`, `guix-a36c632a1b`, `guix-9b6df1084f`,
`guix-2b6eee2e59`, `guix-1823ef372b`, `guix-b54e286053`, and `guix-060983918a`. Their names match
the supported `module-import-compiled` pattern. However, `../compare/joined.tsv` records that c1
could not establish exact members and consumers for these objects; two rows have no c1 evidence
at all. The card's assertion that each has a retained source fallback therefore goes beyond the
exact-object evidence saved for these seven rows. They are likely card-4 instances, but not
confirmed to the same standard as the five rows above.

## Whole-table extent beyond the 12 rows

### Six additional confirmed row objects

`(not published: adjudication scratch)` gives a complete primary-source chain:

1. `scheme-node` creates a distinct source output and a distinct compiled output (lines 198–220).
2. `node-source+compiled` places both in a bundle as separate source and `site-ccache` links
   (lines 129–153).
3. `guix-command` adds the bundle's source directory to `%load-path` and its compiled directory to
   `%load-compiled-path` (lines 612–646).
4. The loader preferentially uses compiled modules and falls back when they are absent
   (`(not published: adjudication scratch)`, lines 120–125 and 186–216).

Accordingly, these six separately inventoried compiled outputs meet both S2.2-10 and S2.2-5:

- `guix-ba6bc2924d` — `guix-system-tests`
- `guix-8fd6717fba` — `guix-system`
- `guix-9e2b09e306` — `guix-packages-base`
- `guix-d6f4da0567` — `guix-extra`
- `guix-9849b393fe` — `guix-cli-core`
- `guix-0c0c8b4f78` — `guix-cli`

Both classifications called these rows MUST. That decision accounts for S2.2-10 but omits the
simultaneously applicable cache sentence. Removal of the compiled row object leaves its distinct
source output available and changes loading or compilation time rather than capability.

### Second affected aggregate

`guix-da5f01a3ef`, the aggregate for store objects outside the current system closure, is also an
affected aggregate. `../in/raw/guix/closure-comparison.json` explicitly places the two Home
`module-import-compiled` outputs and their source `module-import` partners outside the system
closure, so the aggregate contains known card-4 constituents. In addition,
`../in/raw/guix/store-outside-system-closure.txt` contains 18 actual
`module-import-compiled` outputs, but the saved record does not map those 18 exact outputs to
source partners and active loaders. Those additional constituents remain possible rather than
confirmed merely from their names. The exact Home paths are absent from the separately saved
`store-outside-system-closure.txt` enumeration despite the closure comparison and
`store-top-level.txt`; that record inconsistency should remain visible, but it does not erase the
explicit set-membership result in `../in/raw/guix/closure-comparison.json`.

### Rows that should not be added

- The `*-modules` bundle rows contain both source and compiled links as one inventoried object.
  Removing the row object removes both routes, so the computer does not merely do the same more
  slowly. They are MUST under S2.2-10/S2.2-2, without the S2.2-5 collision at row-object level.
- The individual `shepherd-*.go` rows are named compiled service definitions loaded through the
  service-manager configuration. The inventory contains related `.scm` objects, but the saved
  boot record invokes one exact configuration and does not establish that removal of a named
  `.go` causes runtime source lookup. Regenerability at build time is not enough: S2.2-5 defines a
  cache by removal behavior. These rows remain ordinary MUST code unless exact fallback is shown.
- `guix-b1ffaedde8` and `debian-desktop-32e4e6f22d` are shader caches, but no evidence shows code
  running with the host program's full rights as required by S2.2-10. Shader execution is limited
  to the graphics execution interface, so S2.2-10's “so that the code can do whatever the program
  can do” condition is not met.
- `debian-desktop-56f3219102` and the related mail-client startup cache do not have saved evidence
  of independently executable code with the host program's rights. Browser or extension code is
  also expressly addressed by S2.2-7 and S2.2-11 when confined to that program's interface. These
  rows do not extend card 4 on the current evidence; unknown unlisted contents remain an S3-2
  evidence issue rather than a confirmed definition collision.
- Compiled access-control policy caches are rules or values loaded by a policy tool, not code shown
  to execute with that tool's rights. They do not meet S2.2-10.

On the saved evidence, the transparent whole-table bound is therefore **19 affected rows**:
**10 confirmed standalone rows** (the two user cache rows, the two exactly mapped
`module-import-compiled` rows, and the six compiled-node outputs), **two aggregate rows containing
confirmed collision constituents**, and **seven unmatched `module-import-compiled` standalone
rows whose exact facts remain unconfirmed**. The definition collision is certain; the factual
status of seven of the 19 affected rows is not. Counting only standalone rows with exact mappings
gives 10. Counting aggregates that contain such constituents gives 12. Counting the seven likely
generator-pattern instances gives the full 19-row affected set.

## Literal-quote review of `resolved-sample.tsv`

The quoted sentence text is copied literally. The main problem is sufficiency: several notes make
claims that the single quoted sentence does not decide.

### Systematic issue: S2.2-2 used as a converse

S2.2-2 says: “if, after an object is removed, the computer stops doing something or something
becomes impossible on it, the object must be recorded.” It does not literally say that every
object whose removal changes nothing need not be recorded. The opening phrase “The test is
removal” suggests that intended use, but the stated conditional supplies only the MUST direction.
Therefore S2.2-2 alone is not a literal resolving quote for the NOT verdicts in these sampled rows:

`coreos-7b9cb61b42`, `debian-9e34733f17`, `debian-e64b8dac95`, `coreos-f75a178565`,
`arch-97fdaec6aa`, `coreos-a1d62e6d33`, `coreos-56b6b697cc`, `nixos-e4d952cbb3`,
`ubuntu-6759ca6559`, `debian-b314911515`, `guix-0abb5d3f0a`, `guix-68f88fa3ed`, and
`nixos-ed89bf30d9`.

This is a new definition candidate, not just a citation defect: S2.2-1 and S2.2-2 state sufficient
conditions for MUST, while the text does not state a general negative rule for an object outside
the listed exemptions. The factual corrections for individual rows may still be right, but their
quoted sentence does not by itself yield NOT under the required literal reading.

### Rows whose NOT verdict needs additional quoted exemptions

- `debian-desktop-2a6c5aa500`: S2.2-7 covers preferences, but the note also decides telemetry and
  session records under S2.2-6 and messages under S2.2-4. Those two sentences are necessary to
  support the all-NOT group result.
- `ubuntu-b20e807939`: S2.2-5 covers package lists, but the note classifies `extended_states` as
  program state under S2.5-1. The quote does not cover that member.
- `freebsd-b8875e4726`: S2.5-1 covers the state component under the task's outside-scope rule, but
  the repository catalogues are decided as cache under S2.2-5, which is not quoted.
- `ubuntu-869a3e13d4`: S2.2-5 covers package caches, but a recreated lock is justified by unchanged
  removal behavior, not by the cache sentence as quoted.

### Rows whose MUST quote does not identify the inventoried object

- `guix-30d7041bdd`: S2.2-9 requires recording programs, while the row object is a profile link
  tree. S2.2-2 is needed to connect removal of that tree to loss of program startability.
- `ubuntu-89ce5c5668` and `arch-89ce5c5668`: S2.2-9 says that a program which runs must be recorded,
  but the row objects are kernel threads. The note asserts that a thread is itself “a program”
  without a resolving sentence. S2.2-10 may support the underlying kernel code, but it is not the
  quoted sentence and does not decide whether each thread object is that code.

### Section 2.5 rows

For `guix-db686654db`, `freebsd-1fd72f4c9d`, `freebsd-b8875e4726`, and
`nixos-f0398dd524`, S2.5-1 does not literally say “program state need not be recorded.” It says how
to treat program state is not a condition of declarativeness. Under the explicit instruction in
(not published: outside selected checks and direct evidence), these are outside the definition and are not holes. The record should therefore be
read as an outside-scope disposition encoded as NOT for the table, rather than as a textual
need-not exemption granted by S2.5-1.

The remaining sampled quotes are adequate to identify at least the decisive member for a MUST
group, or all members for a simple NOT object, assuming the factual note is accepted. This review
does not independently validate every factual note.

## Final acceptance review

The mechanical counts in the final artifacts are reproducible. `resolved-audit.tsv` has 40 rows:
16 `SUPPORTED`, 17 `REFUTED`, 3 `FACT-WRONG`, and 4 `OUTSIDE`. The 17 refuted quotations resolve
to 12 NOT, 3 MUST, and 2 factual UNKNOWN. The input sample has the stated 17 original MUST and 23
original NOT verdicts. `hole-4-extent.tsv` has 19 screened rows: 10 confirmed standalone rows, 2
aggregate occurrences containing confirmed constituents, 6 factual-UNKNOWN candidates, and 1
`FACT-WRONG` instance. The last instance is properly excluded from both the confirmed and
unverified extents: the saved exact-artifact record establishes that it is an empty 96-byte NAR,
not compiled code. Thus the bounded result is exactly 12 confirmed row occurrences, six unresolved
candidates, and one screened false instance. The apt-cache group is also correctly changed to
`REFUTED`: S2.2-5 decides the cached package data, while S2.5-1 is needed for the lock member.

The use of S2.2-1 to dispose of the apparent negative-removal problem is acceptable and retracts
the new-hole candidate raised earlier in this review. Section 2.2 presents behavioural dependence
as the scope of what must be recorded and expressly calls removal “the test.” When the facts
establish no behavioural contribution and no explicit mandatory category applies, failure to
satisfy that scope supports NOT; a separate sentence saying “if not, need not” is unnecessary.
S2.2-2 remains insufficient as the original quotation by itself, so marking those quotations
`REFUTED` is correct. In `resolved-audit.tsv`, listing S2.2-2 again among the corrective sentences
for a NOT result is redundant; S2.2-1 plus the established absence of contribution does the
corrective work. The two cases where that absence is not established are correctly retained as
factual UNKNOWN under S3-2.

Two material issues prevent unconditional acceptance of `../RESULT.md` as written:

1. **Card 1 is not refuted by the quoted text.** The result chooses “the effect stays inside the
   program” as the meaning of S2.2-7's “in force only inside one program.” The sentence does not
   define that phrase, and S2.2-13 says a file read as values is a setting without defining where
   that setting is in force. The competing literal reading—configuration read and applied by one
   daemon is in force inside that daemon—remains possible even when the daemon changes the clock,
   network, files, or other processes. S2.2-2 then points the other way. Stating that external
   effects “invoke” S2.2-2 does not decide whether S2.2-7 simultaneously exempts the setting. The
   browser examples do not close this boundary; browser extensions can themselves have effects
   beyond presentation. On the fixed text, original Card 1 remains a confirmed collision or at
   minimum is not refuted, so the headline count of one confirmed hole is not secure.
2. **The second aggregate's evidence pointer is wrong or incomplete.** The
   `guix-da5f01a3ef` row in `hole-4-extent.tsv` says the outside-system group contains the two Home
   compiled outputs, but its `evidence` field cites only
   `../in/raw/guix/store-outside-system-closure.txt`; neither exact Home path occurs in that file.
   `../in/raw/guix/closure-comparison.json` does explicitly place both compiled outputs and their source
   partners outside the system closure, while `store-top-level.txt` contains the compiled paths.
   Thus the aggregate conclusion is supportable, but the row-level evidence boundary and the
   `../RESULT.md` sentence crediting `store-outside-system-closure.txt` do not support the stated
   overlap. The saved-record inconsistency must not be hidden.

There are also two smaller reproducibility/category limitations. `build_records.py` verifies the
two pre-existing sample files rather than generating them, and it generates `resolved-audit.tsv`
but not `agreed-audit.tsv`, `counts.json`, or `unknown-rows.tsv`; its hard-coded review overrides
reproduce the current categories but do not derive them from cited evidence. The statement that it
reproduces the samples' order is exact, but the broader suggestion that it reproduces all review
row records is unsupported. In addition, the two kernel-thread sample rows are plausibly program
state under S2.5-1 rather than MUST objects under S2.2-1/S2.2-2; the result gives no reason for
treating per-thread runtime instances differently from the runtime reflections assigned outside in
Card 5. Moving those two rows from `REFUTED/MUST` to `OUTSIDE` would change the category split to
15 refuted and 6 outside, without creating a new hole or changing the 24 challenged quotations.

Cards 2, 3, 5, 6, and 7 have adequate dispositions on their stated facts. Card 2's database/content
exception includes the explicit unchanged-capability condition; Card 3's cache exception likewise
requires unchanged operation apart from speed; Card 5 is expressly program/runtime-state
treatment outside the definition; S2.2-1 covers Card 6's later behaviour; and Card 7's future
logging switch is distinct from exempt past records.
