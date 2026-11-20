# X4 — mechanical search of the written definitions

2026-11-19, corrected by FX-X4-1. **Classification: 0, same witness as Check 1
(A/RESULT.md), §9.2 disagreement branch; not counted separately.**
**Strict logical contradiction: ?** after adding the omitted P3/P4 effective-launch
check: conditional conflicts are established, but their required contexts or
semantic boundaries are not resolved by the paper and evidence. No open problem
is decided; this is not an impossibility proof.

Protocol: X4-PROTOCOL.md, frozen before installation/search,
SHA-256 `c234983d552dac7149fd0700c15ee35929a6db4630c67917ed548b32d966608d`.
Authoritative run: [run-006/summary.json](raw-X4/fix-001/run-006/summary.json).
Original run and instrument corrections remain in change log.
Finding dispositions and new evidence: FIX-X4-1.md.

## What was measured

[X4-model.py](X4-model.py) uses Z3 5.4.1, installed as `z3-solver==5.4.1.0`
in a dedicated venv. It searches one target object, two possible owner programs,
root and one ordinary person, root/personal declarations, a current and a saved
generation, plus an inclusion before/after pair and a feasible bypass-launch
attempt with a free effective-launch outcome. Root/personal ownership and
designation are fixed role assignments by construction; the declarations form
one logical description. Entry conflicts, program/person roles, need, human
creation, manual intent and what counts as running are inputs, not inferred facts.
The paper provides no executable criterion for these roles.

Each unordered property pair A/B uses a common input context c and free outcomes o:

`exists o: Base(c,o) & A(c,o)` AND `exists o: Base(c,o) & B(c,o)` AND
`NOT exists o: Base(c,o) & A(c,o) & B(c,o)`.

SAT therefore means both properties can be met separately but not together at
that context. Each SAT pair has fixed-context `-left`, `-right` SAT models and a
`-joint` UNSAT core. Outcome variables are projected out of the initial search;
their values appear only in the separate models. All queries have replayable
SMT-LIB beside their JSON trace in [queries/](raw-X4/fix-001/run-006/queries/).

**226 solver calls: 104 SAT, 122 UNSAT, no unknown/timeouts.** These include
105 pair searches (21 pairs × five explicitly labelled interpretations),
three provenance/class overlaps, six class-obligation conflict searches,
one synthetic no-class search, two epistemic completions, replay traces,
and targeted/control cases. The 105 pair searches produced 19 SAT entries:
five each of P3/P4, P3/P6 and P4/P6, one P2/P6, two P4/P7, and one deliberately
overstrong P5/P7 control. Counts are queries, not numbers of real counterexamples.

## Translation and boundaries

Exact original sentences and line numbers are preserved in
source-sentences.json and
paper-lines.txt; their source is the hashed
[paper snapshot](../../first-paper/PAPER.html). Independent translation audits:
semantics, model audit.

| Concept/property | Encoded obligation or predicate | Deliberately unresolved |
|---|---|---|
| Recorded | Explicit membership in root or personal declaration | Installed/package-owned is not recorded; current entries and attempted new entries are separate snapshots. |
| Derivative, line133 | Described-at-creation program created x for its operation, **or** x was executed internally | Internal execution is historical provenance; shell launching is not automatically internal execution (O5). Need is an input (O1). |
| Data, line134 | Person-created provenance | No exclusive-class or data nondeletion rule. Class status after inclusion is open (O2/O3). |
| P1, line140 | Runs without explicit bypass ⇒ recorded | No automatic equation of installed, internal code and independently running component (O9). |
| P2, line141 | Recorded ⇒ present; also after inclusion | Present does not mean active or unarchived. Bypass/P2 interaction remains O4. |
| P3, line142 | Present and unrecorded ⇒ data or derivative with recorded owner; derivative cannot be independent authority | Whether historical recording counts is exposed by a sensitivity query. Direct derivative-of eligibility and broader shared-needer eligibility are tested separately; P6 protects both. |
| P4, lines143/227 | Implicit bypass denied; explicit bypass allowed; applicable line takes effect for a feasible attempted launch | Person-root versus autonomous program-root is an input (O4); permission is not observed execution. |
| P5, line144 | Inclusion is possible for derivative/data; taking inclusion records it | A limited availability proxy and transition, not a proof of a complete implementation or every user's admission right. |
| P6, lines145/238 | Current/saved owner preserves x; no current owner archives it; any current shared needer protects access; completed archive disposition follows explicit policy | Archive step is an event, not absence. Missing policy is free (O6); completed deletion is gated by no current/saved owner. Recorded derivative lifecycle is omitted from the partial translation and tested separately, not declared exempt. |
| P7, lines146/243 | Personal admission obeys root conflict, Unix entry permission and chosen list mode; manual root retains authority | Execution-scoped Unix permission and unrestricted root-program privilege are separate conditional readings. Root and personal declarations are fixed roles, not a parsed policy language. |

The model is target-local: it does not enforce all seven properties recursively
on every owner, or prove reachable machine states. There is at most one list
mode per situation. O7/O8 have no settled compatibility/transfer obligation to
encode. O9 and action identity remain inputs. Negative synthetic facts are
explicit constructions, never substitutes for unknown observations.

FX-X4-1 adds P4's positive effect: for a feasible attempted bypass launch with an
applicable permitting line, `launch_effective=1`, hence `present=1`. Both are
outcomes, not preset input facts. P1 covers this effective launch too. The
queried state includes its launch effect; this is a local feasibility test, not
a full temporal trace. A permitting line without an attempt does not force
execution. Declaration membership and provenance remain independent inputs:
§5.3 line150 says the permitting line “does not enumerate what has actually been
launched under that permission”; a separate entry may nevertheless record x.
No new class, bypass exemption from P3, or rule resolving O5 is introduced.

## Class and no-class results

| Search | Mechanical result | Evidence and outcome |
|---|---|---|
| Recorded + derivative; recorded + data | Both provenance overlaps SAT; only recorded/derivative has an opposing-duty witness when lifecycle retention is added | No full real inclusion/removal match found. Membership after inclusion and lifecycle priority remain holes: **?** for strict conflict. |
| Derivative + data | SAT. The data definition adds no opposite archival or deletion duty; class-duty conflict search UNSAT in both tested profiles | E1 editor settings and E2 Nix profile are existing unresolved independent classification disagreements: **0 for classification**, not proof of opposite duties. |
| None of recorded/derivative/data | SAT for a present synthetic object with all three predicates false | E3 user-profile `hello` is only a partial match; no observed source establishes all negative predicates: **?** for a real no-class object. |
| Unknown internal execution of person-created settings | Both completions SAT | Saved code alone does not establish a runtime load; the model preserves that uncertainty. |

Trace files: [overlap derivative/data](raw-X4/fix-001/run-006/queries/overlap-derivative-data.json),
[recorded/derivative conflict](raw-X4/fix-001/run-006/queries/class-conflict-retain_recorded_derivative-recorded-derivative.json),
[synthetic no-class](raw-X4/fix-001/run-006/queries/no-class-closed-predicates.json),
[editor completion 0](raw-X4/fix-001/run-006/queries/epistemic-editor-code-0.json),
[editor completion 1](raw-X4/fix-001/run-006/queries/epistemic-editor-code-1.json).

E1 is the personal editor configuration from the personal-machine census (path not published): frozen classifiers say `hole-two`
and `data` for the same row. E2 is `/home/census/.local/state/nix/profiles/profile`:
classifiers disagree about generated operational state versus personal settings.
The paper itself says: “A rule is needed that resolves such cases unambiguously”
(O2, line201). This supplies the frozen §9.2 failure branch without claiming that
static source proves runtime execution. Exact source rows, copied excerpts,
SHA-256 hashes, and the distinction between observed and inferred facts are in
X4-EVIDENCE.md and its manifest.
This reuses the census evidence; X4 did not conduct a new independent census.

## Conditional conflicting obligations: minimal traces

All unlisted input flags in the canonical traces are explicitly false synthetic
facts. Each linked joint trace has matching `-left.json`, `-right.json` and SMT-LIB
files; these show satisfiability on each side and the combined UNSAT core.

| Case and minimal input | Opposing outcomes and exact paper sentences | Real object match; interpretation |
|---|---|---|
| **C1 P2/P6:** x explicitly recorded; historically described p created/needed x; no current/saved owner; archive setting delete; disposition completed; derivative lifecycle retained after inclusion | P2: `present=1`; P6: `deleted=1`, hence `present=0`. “Everything explicitly recorded in the declaration is present on the computer” (141). “Any derivative and any data can be recorded in the declaration; they then become subject to it on the same terms as everything else recorded” (144). “Whether to keep the archive indefinitely or delete it is a setting recorded in the declaration” (145). [Joint trace](raw-X4/fix-001/run-006/queries/canonical-recorded-delete-joint.json). | **No full match found.** E6 Chromium state was not individually recorded and a base browser remained. Conditional on lifecycle retention/priority after P5 and completed disposition; related to O3, which explicitly names data. **?**. |
| **C2 P4/P7, ordinary person:** running-component change bypasses declaration; Unix permits; no lists or explicit exception; ordinary user | P4 `change_allowed=0`; execution-scoped P7 `change_allowed=1`. “A bypass is possible only explicitly” (143). “By default, the user's permissions are determined by ordinary Unix permissions” (146); §9.6 fails if “in the absence of lists, the user cannot do what ordinary Unix permissions allow” (243). [Joint trace](raw-X4/fix-001/run-006/queries/canonical-ordinary-unix-joint.json). | **Partial:** E4 `/home/alice/downloaded` is Unix-executable, denied without exception, succeeds after exception. Whether copied `hello` is a distinct unrecorded component, and P7's execution versus declaration-admission scope, remain unsettled. Stand failure is not property-inherent proof. **?**. |
| **C3 P4/P7, root program:** autonomous root program changes a component without declaration write, manual action or permitting line | P4 `change_allowed=0`; root-executor reading of P7 `change_allowed=1`. “A program, including one running with root privileges, changes the system only by writing to the declaration” (143). “Root's own privileges are not restricted, and the system does not take them away from the person” (146). [Joint trace](raw-X4/fix-001/run-006/queries/canonical-root-program-joint.json). | **Partial:** E5 `/usr/local/root-program-probe` and managed root-worker logs record UID/process behavior, not human intent. O4 explicitly leaves the distinction open. Manual person-root is separately SAT with both properties. **?**. |
| **C4 P3/P6:** unrecorded, non-person-created historical derivative; no currently recorded owner; no current/saved owner; explicit keep-archive policy | Current-only P3 eligibility forces `present=0`; P6 keep requires `present=1`. “Everything that is on the computer and is not recorded in the declaration is either a derivative of a recorded program or the person's data” (142). Archive-setting sentence at145 and fate-setting failure at238. [Joint trace](raw-X4/fix-001/run-006/queries/canonical-historic-archive-joint.json). | **No full match found.** E6 does not establish absence of all owners. With historical recording admitted for P3, the same context is [SAT](raw-X4/fix-001/run-006/queries/canonical-historic-archive-historical-scope.json). The paper does not specify this temporal scope; no reading selected. **?**. |
| **C5 P3/P4:** feasible attempted bypass launch; applicable permitting line; x unrecorded, not person-created, no creator/internal-code derivative predicates | P3 forces `present=0`; P4's effective-launch duty forces `launch_effective=1`, hence `present=1`. P3 line142; P4 line143; §9.3 line227: “explicit permission through a line in the declaration does not take effect”; §5.3 line150 separates permission from enumeration. [Joint trace](raw-X4/fix-001/run-006/queries/canonical-permitted-bypass-no-class-joint.json). | **No full match found.** E4 has permission followed by successful shell launch, but its negative class facts and unrecorded identity are unresolved. O5 explicitly leaves the shell-launch derivative boundary open. **?**, detailed below. |
| **C6 P4/P6:** feasible attempted permitted launch of an unrecorded historical derivative; no current/saved owner; delete policy and completed disposition in the same queried state | P4 requires effective launch/presence; P6 requires deletion/absence (143/227 versus145/238). [Joint trace](raw-X4/fix-001/run-006/queries/canonical-permitted-launch-completed-delete-joint.json). | **No full match found.** The state projection aligns launch effect and completed deletion; the paper does not require simultaneity or persistent presence after execution. [Deletion not completed](raw-X4/fix-001/run-006/queries/canonical-permitted-launch-delete-not-completed.json) and [keep policy](raw-X4/fix-001/run-006/queries/canonical-permitted-launch-keep-archive.json) are SAT. Conditional timing result, **?**; not a property-inherent failure. |

A second P3/P6 sensitivity keeps a *different* recorded needing program current.
P6 protects the shared derivative even though that program did not create it.
Whether this also satisfies P3's “derivative of” relation is unspecified:
[direct-origin eligibility](raw-X4/fix-001/run-006/queries/canonical-shared-needer-direct-origin-eligibility.json)
is UNSAT; [broader shared-needer eligibility](raw-X4/fix-001/run-006/queries/canonical-shared-needer-broad-eligibility-BRANCH.json)
is SAT. This is a further ownership-scope hole under C4, with no complete real
match established; neither eligibility rule is declared the paper's decision.

**New hole H-X4-temporal (not assigned to O1–O9):** does P3's “recorded program”
(line142) include programs recorded only in earlier generations? Line133 says
“a described program has created”; line145 retains derivatives through saved
generations and possible indefinite archives. These sentences do not settle
the temporal scope of P3. O6 concerns missing archive instructions, whereas C4
has an explicit keep setting. The current-only and historical queries expose
this hole; neither becomes a classification rule.

The class-overlap and no-class sentences are lines133–134 and P3 line142:
“Code executed within a program is its derivative”; “Data—what a person has
created”; and the P3 remainder requirement quoted above. Their traces and
real-object matches are given in the preceding table (E1–E3). The old fixed-run
[P1](raw-X4/fix-001/run-006/queries/explicit-bypass-none-P1.json) and
[P3](raw-X4/fix-001/run-006/queries/explicit-bypass-none-P3.json) checks did not test P4's
positive duty. Their earlier dismissal of the bypass issue, also present in
the historical evidence note, is withdrawn by this correction.

C5 now has SAT left/right and UNSAT joint traces with **identical inputs and
free outcomes**. P3 alone keeps x absent and unlaunched; P4 alone makes it
present and launched. Thus the opposing duties are mechanical evidence, not
merely a P1 exception. What is missing is an established no-class context:
O5 (line204) asks, “Does a program launched by another program, such as a shell,
become its derivative?” Line133 says, “Code executed within a program is its
derivative.” E4 is a shell launch of a person-copied executable whose original
`hello` is already recorded. Neither its lack of person-created data provenance
nor its distinct unrecorded program identity is established. E3 likewise lacks
complete declaration/need/provenance negatives. This invokes O5 and missing
facts, **not O4 as an exception to P3**. Exact copied evidence, including the
original declaration entry and shell commands, is in the
fix evidence manifest.

The same C5 attempt is jointly SAT when x is
[data](raw-X4/fix-001/run-006/queries/canonical-permitted-bypass-data-completion.json),
a [recorded-owner derivative](raw-X4/fix-001/run-006/queries/canonical-permitted-bypass-derivative-completion.json),
or [separately recorded](raw-X4/fix-001/run-006/queries/canonical-permitted-bypass-separately-recorded.json).
[No attempt](raw-X4/fix-001/run-006/queries/canonical-permitted-bypass-no-attempt.json)
and [no permission](raw-X4/fix-001/run-006/queries/canonical-bypass-no-permission.json)
also avoid the conflict. These are sensitivity completions, not classifications
of E4. Frozen protocol therefore gives **?** for strict contradiction: the
negative class context is stipulated synthetically, not established without
resolving the open boundary. It is not evidence of consistency either.

## All 21 pairs, controls, and acceptance limits

[Full generated matrix](raw-X4/fix-001/run-006/pair-matrix.md) lists every pair in all five
profiles. SAT is a conflict in that encoding; UNSAT is absence of such a local
conflict, **1 only within the stated partial encoding and bound**. The exceptional
pairs are P2/P6, P3/P4, P3/P6, P4/P6, P4/P7 and the P5/P7 control. All other 15 pairs are UNSAT
in all five profiles. This does not establish full joint consistency, modal
feasibility, arbitrary owner/generation counts, or implementation feasibility.

Two deliberately stronger readings demonstrate how to manufacture a conflict;
neither is counted as a paper counterexample. Requiring P5 to admit every
personal route conflicts with P7, while inclusion through another authorized
route remains possible ([control](raw-X4/fix-001/run-006/queries/canonical-overstrong-personal-joint.json)).
Immediate archive deletion while a saved owner exists conflicts with §9.5's
explicit protection ([control](raw-X4/fix-001/run-006/queries/BRANCH-immediate-delete-saved-internal-P6-conflict.json));
the paper does not license ignoring that protection. Neither control has a
claimed real-object match.

Positive checks include a jointly satisfiable P1–P7 context, true/compatible
conflict controls, explicit bypass permission, manual-root compatibility,
saved-owner preservation, shared needing-but-noncreating owner protection,
kept archive compatibility with P2, and successful inclusion. With no archive
setting and no owners, both present and absent completions are SAT: an O6 hole,
not a default deletion rule. Results and expectations are saved in
results.jsonl.

The original acceptance X4-REVIEW.md applies to
run-004 and was challenged by REVIEW-X4.md; it does not accept
this correction. FX-X4-1 uses a separate independent semantic audit and an
independent reviewer. Current review and replay status are
**ACCEPT**, X4-FIX-1-REVIEW.md; **226/226** stored queries
replayed without mismatch (record).
Final preservation and cleanup checks are in FIX-X4-1.md.
Commands, installation log, package hash, input snapshots,
and retained earlier run are under [raw-X4/](raw-X4/). No system package,
service, VM or external publication was changed.

Reproduce in a new venv with [X4-requirements.txt](X4-requirements.txt), then:

```sh
python -m venv X/X4-venv
X/X4-venv/bin/python -m pip install --no-cache-dir -r X/X4-requirements.txt
X/X4-venv/bin/python X/X4-model.py --out X/raw-X4/reproduction-NEW
```

Use a fresh output directory; previous evidence is never overwritten. The
script checks the frozen protocol hash. The disposable venv and downloaded
wheel are removed after review; their versions/hash and all model evidence remain.
