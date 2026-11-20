# X2C — Check 1 comparison, 2026-11-19

**Outcome: `?` for `debian-desktop`; `?` overall for the supplied X2 census.**
Only one system occurs in these inputs. No second-machine result is inferred.
No no-class object, two applicable classes with different consequences, or pair
of different affirmative §5 class assignments is established. Declaration,
provenance and authorship gaps prevent a pass or a demonstrated counterexample.
The low agreement and 234 submitted hole labels do not themselves establish `0`.

Executor: the producer of classification 1. Independent textual check: a separate step of the same executor.
Independent review:
review record. This report is the comparison,
not the second classifier's acceptance of the first classifier's work. Original classifications are preserved.

## Fixed condition and measurements

[PAPER.html §9.2](../../../first-paper/PAPER.html), unchanged:

> An object is found on either machine that, under the definitions, belongs to no
> class or belongs to two classes with different consequences, or the two
> classifications assign the object to different classes and the text of the
> definitions does not resolve the disagreement.

Join is by full `id`; system comes from `X2-residual.tsv`, not inferred from row
position. Both submissions and the inventory have **235 unique IDs**, with
**0 duplicates, 0 missing classifications, 0 extra/unmatched IDs**.
[Join audit](raw-X2C/join-integrity.json); frozen inputs and hashes.

| System | Paired rows | Same class | Different class | Agreement | Cohen's κ | Outcome |
|---|---:|---:|---:|---:|---:|:---:|
| debian-desktop | 235 | 17 | 218 | 17/235 = 7.234043% | 0.0374823861 | **?** |
| Overall, one supplied system | 235 | 17 | 218 | 7.234043% | 0.0374823861 | **?** |

These are **submitted-label** statistics, including `hole-none` and `hole-two`
as distinct categories, not agreement on 235 successfully classified objects.
Exact `class` strings are compared; reasons and candidate-owner columns are not
part of class equality. Collapsing `derivative of <program>` to `derivative`
does not change these numbers: classification 1 assigned no derivative labels. No labels
were changed after adjudication and no proxy rows were added to the denominator.

For unweighted Cohen's κ, `p_o=17/235`; marginal cross-product is
`223×7 + 11×39 + 1×10 = 2000`, so `p_e=2000/235²=80/2209` and
`κ=(p_o−p_e)/(1−p_e)=399/10645`. [Computed statistics](raw-X2C/statistics.json).

| Submitted class | Classification 1 | Classification 2 |
|---|---:|---:|
| recorded (works) | 0 | 27 |
| derivative of a program | 0 | 152 |
| data | 1 | 10 |
| hole-none | 223 | 7 |
| hole-two | 11 | 39 |
| Total | 235 | 235 |

| Classification 1 → classification 2 | Rows | Text-only adjudication |
|---|---:|---|
| hole-none → derivative | 151 | not resolved; described-owner/provenance/intent premises missing, including two absent-unit reference families |
| hole-none → hole-two | 30 | not resolved; candidate overlaps and mixed groups, not 30 proven double memberships |
| hole-none → recorded (works) | 27 | not resolved; running-component kind does not establish recording in a designated declaration |
| hole-none → data | 8 | not resolved; settings/authorship and program-mediated output boundary |
| hole-two → data | 1 | not resolved; mixed research evidence directory, row 161 |
| hole-two → derivative | 1 | not resolved; CUPS spool copy, row 218 |
| hole-none → hole-none | 7 | identical submitted evidence-gap labels |
| hole-two → hole-two | 9 | identical hole labels: five scripts, dconf, three mixed directories |
| data → data | 1 | retained unexecuted source copy, row 212 |

## Every disagreement and every hole

The following are integral row-level appendices to this result:

- [All 235 joined rows](raw-X2C/joined.tsv).
- [All 218 disagreements](raw-X2C/disagreements.tsv): each has both original
  classes/reasons, source row numbers, object, evidence, exact relevant §5
  quotations, `text_resolution`, adjudication reason and O1–O9/NEW tags.
- [All 234 rows with a hole in either submission](raw-X2C/holes.tsv): same
  complete columns, including all agreed holes. Classification 1 has 234 holes, classification 2
  has 46; their intersection is 46 and union is 234. The only non-hole row is
  `debian-desktop-efc18859d4`, retained failed-install source copy, data/data.

**All 218 submitted-decision disagreements remain “not resolved” by §5 alone.** This means the
text does not select a unique supported class for the supplied observation;
it does not mean 218 demonstrated definition counterexamples. In particular,
text can reject an unsupported inference without supplying the missing facts.
Every differing pair contains a `hole-*` label; **zero pairs assign different
affirmative classes** (`recorded`, `derivative`, `data`). `hole-none` mostly means
“not established” in classification 1's explicit reasons, not “proved to belong to no class”;
`hole-two` flags candidates, not proof of two memberships. These are measurement
labels, not extra §5 classes. Consequently the unresolved-label count cannot be
substituted for §9.2's different-class-assignment limb. The candidate holes below
also fail to establish the factual premises of its no-class/two-class limbs.
Under §9.1, insufficient evidence yields `?`. No precedence, directory rule,
declaration designation, or new class is introduced here.

The quotation constraining the 27 `recorded (works)` claims is:

> Declaration—a collection of files that a person has designated as the primary description of the computer.

For derivative claims the relevant sentence is:

> Derivative—an object that a described program has created itself because the object is needed for the program's operation: saved Wi-Fi networks for a network management service, extensions for a browser, a cache, a log.

Package membership, a producer's name, or being a running component does not
prove the required designation or described-owner premise. These quotes limit
what can be concluded; they cannot recover missing designation/creator/intent
evidence. P1/P4 requirements are not observations that Debian actually records
the object. Original qualification,
original per-row status, [§5 quote catalogue](raw-X2C/section5-quotes.json).

`NEW` in the appendices denotes an issue not specifically covered by O1–O9,
principally missing declaration/designation evidence or an observation defect;
it does **not** amend §8 or designate a new theoretical counterexample. O1 marks
creator/need evidence, O2 data/derivative boundaries, O4 root/manual provenance,
O5 launching/code boundaries and O9 observation/component scope. Topics can
overlap. This comparison establishes no O3 or O6–O8 result.

## Candidate definition holes and their evidential limits

Row numbers below are physical TSV lines, counting the header as line 1; IDs
are authoritative. All suffixes have prefix `debian-desktop-`.

| Row | ID suffix | Individual object | Classes | Issue |
|---:|---|---|---|---|
| 156 | fb87e8bdd4 | `/home/census/X2-complete-workload.sh` | hole-two / hole-two | O2,O5,NEW |
| 157 | 09fa2e5ce3 | `/home/census/X2-day.sh` | hole-two / hole-two | O2,O5,NEW |
| 158 | f5e686458b | `/home/census/X2-desktop-env.sh` | hole-two / hole-two | O2,O5,NEW |
| 159 | 2438267eef | `/home/census/X2-final-apps.sh` | hole-two / hole-two | O2,O5,NEW |
| 160 | d54b59c426 | `/home/census/X2-repair-desktop.sh` | hole-two / hole-two | O2,O5,NEW |

These are individual files, not mixtures of files. Both classifiers propose
data and code-executed-within-bash readings for the deliberately authored sources.
Those submissions are not proof of the person-created premise. §5.1 says, exactly:

> Code executed within a program is its derivative.

> Data—what a person has created: photographs, documents, databases, and their own settings files, such as a text editor configuration.

§5 does not say which reading takes precedence for authored executable source.
Applying P6 to the derivative reading has consequences absent from the data
reading:

> A derivative exists as long as its program is present in the current generation or in one of the saved generations.

> If the program is absent from the current generation, its derivative is moved to an archive.

Agreement on `hole-two` is not success, but the conditional contrast above is
also not proof of two applicable classes. O2 identifies person-authored executed
configuration as an unresolved boundary; the present evidence must still establish
its premises. No package database is retrospectively designated as a declaration.

Evidence: X2-day launch log,
observed processes,
census processes,
complete-workload source,
final-apps source, repair-desktop source
(each sources `X2-desktop-env.sh` at line 3), and the
[saved individual inventory members](raw-X2C/decisive-evidence.json).
**Authorship limitation:** these are executor-authored instrumentation for the
person's requested experiment, not evidenced human-authored user files. Both
submissions assume that deliberate research source is the person's data. §5
does not say whether executor production establishes person creation; this
comparison neither invents that rule nor its opposite. The person-created data
premise and a described/recorded bash remain unestablished. Hence these are
candidate O2/O5 cases with NEW evidence gaps, not demonstrated counterexamples.

Additional explicit disagreement: **row 218, `f05cbeb21e`, `/var/spool/cups`**,
specifically `d00001-001`, is hole-two versus derivative of CUPS (O1,O2,NEW).
The saved copy check records a byte-identical
138-byte copy of authored content; job submission
records `X2-Local-1`. §5 supplies no priority between the authored-document
reading and the operational-copy reading: **not resolved**. This is concrete
copy-boundary evidence, but the missing described-CUPS premise remains; the
person-authorship premise is also not independently established by byte identity.
It is therefore not promoted to a proven double class or a `0` verdict.

Other holes are fully enumerated in the appendix, with these distinctions:

| Rows / ID suffixes | Why retained; evidential status | Topic |
|---|---|---|
| 133 / 96d642d273 | Personal dark-mode choice stored in dconf database; candidate boundary, described owner missing | O1,O2,NEW |
| 52,135,137 / 688808b26c,de9a685076,bf374a250d | CUPS/Geany/Firefox mixed groups; different members are not proof of double classification of one member | O1/O2,NEW |
| 161 / a8b44f743e | Research screenshots/reports/logs group: hole-two versus data; no whole-group rule in §5 | O1,O2,NEW |
| 33,34 / 015af60fe8,377e7f2465 | Flatpak Calculator/container BusyBox processes: launch/component boundary, declaration premise missing | O5,O9,NEW |
| 140,142 / 7a6e20a2b1,90c74ccf60 | Podman/Flatpak stores: code plus manager state, not a proven uniform class | O1,O5,O9,NEW |
| 46,49,50,58,66,78,220 / ce45570012,34803cf70a,72dead8488,4cce813fe8,5cad41b508,1af8deec0e,64f62c6553 | Seven agreed hole-none labels: creator/designation or mixed-skeleton evidence missing, not proven absence of all classes | O1/O2,NEW |
| 225,234 / 9994d7ebc4,97fdaec6aa | `not-found` unit references do not establish present objects | O9,NEW |
| 36 / d8ee8908a9 | Collector `ps` vanished before executable resolution: observation race | O9,NEW |

## Coverage and reproducibility

The census is one disposable Debian 12/GNOME VM after a compressed scripted day,
not two real personal machines or 24 elapsed hours. The 235 rows are residual,
overlapping grouped observations. The **1,721 automatic proxy rows** (1,718
recorded proxies and 3 data proxies) did not receive the two supplied independent
classifications; no full-census agreement statistic is available. In particular,
the project proxy contains a venv and the Documents proxy includes an office lock
file. Those proxy limitations are recorded in X2-HOLES, not silently
converted to new residual rows or corrected classes.

The non-atomic inventory omits general `/run /tmp /proc /sys /dev`, unowned
`/usr` outside `/usr/local`, firmware and external hardware; some unit/driver/group
coverage is raw-only. Both classifiers may share errors. Independence of the
original classifications follows their submitted protocol statements, not an
audit of all prior exposure of the classifiers. Same hole labels may hide different reasons.
These limits prevent a whole-machine pass (`1`). The observed candidate boundaries
lack the evidence needed to establish a §9.2 failure; §9.1 therefore yields `?`.
Collection summary, frozen protocol.

Reproduce the join, metrics and row appendices with
`python raw-X2C/compare.py`. The script reads only the
snapshots and writes only X2C derived files. No source classification, definition,
protocol or failure condition was edited.

Independent review rejected the draft's `0` inference from executor-authored
scripts. The dated pre-review draft
is retained for audit; it is superseded by this result. The correction concerns
evidence sufficiency, not a change to §5, §9.2 or either submitted classification.
