# X1C — Check 1: comparison of the two classifications

**2026-11-19. Outcome: Arch 0; Silverblue 0; FreeBSD 0; overall 0.**
Each system has an authored, interpreter-used personal setting for which the
submitted classifications diverge on the data/derivative boundary and §5 does
not resolve the disagreement. This applies the third disjunct of §9.2. It does
not infer failure from a low agreement score or from the mere presence of a
`hole-none`/`hole-two` annotation.

Executor: the producer of classification 1. The numerical audit and the text review were separate
steps of the same executor.
The source classifications and frozen X1 protocol were not edited. Inputs,
hashes and capture time: input manifest.

## Counts and agreement

Join is by exact **id**, with system and object identity from
X1-residual.tsv. All three tables have 510 unique IDs;
duplicates, missing IDs and extra IDs: **0**. Source line numbers below include
the header. Every disagreement and hole retains both original reasons and its
source line numbers in the linked ledgers.

| System | Paired rows | Identical classes | Agreement | Cohen's κ | Disagreements | Rows with either rater's hole | Outcome |
|---|---:|---:|---:|---:|---:|---:|:---:|
| Arch | 84 | 20 | 23.809524% | 0.018440752 | 64 | 83 | **0** |
| Silverblue | 133 | 13 | 9.774436% | 0 | 120 | 133 | **0** |
| FreeBSD | 293 | 33 | 11.262799% | 0 | 260 | 293 | **0** |
| Pooled | 510 | 66 | 12.941176% | 0.002515297 | 444 | 509 | **0** |

The raw `class` strings are compared without changing any decision. Each
`derivative of <program>` is a distinct category, and `hole-none` and `hole-two`
remain distinct annotations. For N paired rows, `p_o = matches/N`,
`p_e = Σ_c(n_A,c × n_B,c)/N²`, and `κ = (p_o − p_e)/(1 − p_e)`.
Calculations use exact rational arithmetic before display rounding.
The expected agreements are Arch `1579/7056`, Silverblue `13/133`, FreeBSD
`33/293`, pooled `33089/260100`. Exact κ is Arch `101/5477`, pooled
`571/227011`. Zero κ for Silverblue and FreeBSD is defined: classification 1 uses only
`hole-none` there, so observed and expected agreement coincide, with `p_e < 1`.
Pooled κ is calculated from pooled marginals, not an average of system κ values.
See [metrics and full confusion matrices](raw-X1C/metrics.json) and
[reproduction script](raw-X1C/compare.py).

| System / classifier | recorded (works) | derivative¹ | data | hole-none | hole-two |
|---|---:|---:|---:|---:|---:|
| Arch / classification 1 | 0 | 0 | 1 | 83 | 0 |
| Arch / classification 2 | 25 | 35 | 2 | 19 | 3 |
| Silverblue / classification 1 | 0 | 0 | 0 | 133 | 0 |
| Silverblue / classification 2 | 60 | 53 | 1 | 13 | 6 |
| FreeBSD / classification 1 | 0 | 0 | 0 | 293 | 0 |
| FreeBSD / classification 2 | 228 | 25 | 1 | 33 | 6 |
| Total / classification 1 | 0 | 0 | 1 | 509 | 0 |
| Total / classification 2 | 313 | 113 | 4 | 65 | 15 |

¹ Owners collapsed only for this display. Collapsing them for the calculation
also leaves agreement/κ unchanged here because classification 1 has no derivative labels.
All derivative suffixes match the supplied `program_if_derivative` fields.
Of 66 matches, **65 are shared hole-none annotations** and only one is shared
data: Arch `arch-7fa8a1d5c0`, `.nanorc`. Both raters mark a hole on 80 rows
(Arch 22, Silverblue 19, FreeBSD 39); the hole union is 509, not 589.

## Every disagreement: what §5 resolves

The complete [444-row disagreement ledger](raw-X1C/disagreements.tsv) is an
integral part of this report. Each row contains id, system, object, source lines,
both classes/owners/reasons, §5 resolution, verbatim supporting sentences or
**“not resolved”**, hole reason, O1–O9/NEW tags and evidence references.
The [510-row join](raw-X1C/joined.tsv) also retains every agreement.

“Resolved” below means **§5 rejects the stated support for an assertion**. It
does not mean that X1C supplies a new class or fills in missing empirical facts.
In particular, rejecting a package-membership proxy as proof of a declaration
leaves an evidence hole; it does not prove that the object belongs to no class.

| Disagreement family (classification 1 → classification 2) | Arch | Silverblue | FreeBSD | §5 text decision |
|---|---:|---:|---:|---|
| hole-none → recorded (works) | 25 | 60 | 228 | Unsupported recorded assertion rejected by Q1; hole retained |
| hole-none → derivative of program | 35 | 53 | 25 | Unsupported eligible-parent assertion rejected by Q1–Q3; hole retained |
| hole-none → hole-two: person-made rule needs recording | 2 | 3 | 4 | “Needs recording” is not evidence of recording: Q1, Q5, Q6; hole retained |
| hole-none → hole-two: installed Flatpak programs | 0 | 1 | 0 | Recorded parent and program need unestablished: Q1–Q3; hole retained |
| hole-none → hole-two: heterogeneous group | 1 | 2 | 2 | **not resolved** at grouped-row granularity; grouping hole |
| hole-none → data: executed personal setting | 1 | 1 | 1 | **not resolved**, Q3–Q4 do not select a unique result; O2 |
| Total | 64 | 120 | 260 | 436 unsupported assertions text-resolved; 8 not resolved |

The exact §5 sentences used are also stored in
[section5-quotes.json](raw-X1C/section5-quotes.json):

- **Q1, §5.1:** “Declaration—a collection of files that a person has designated as the primary description of the computer.”
- **Q2, §5.1:** “Derivative—an object that a described program has created itself because the object is needed for the program's operation: saved Wi-Fi networks for a network management service, extensions for a browser, a cache, a log.”
- **Q3, §5.2 P3:** “Everything that is on the computer and is not recorded in the declaration is either a derivative of a recorded program or the person's data.”
- **Q4, §5.1 (two sentences):** “Code executed within a program is its derivative.” / “Data—what a person has created: photographs, documents, databases, and their own settings files, such as a text editor configuration.”
- **Q5, §5.2 P1:** “Everything that runs on the computer is recorded in the declaration.”
- **Q6, §5.2 P5:** “Any derivative and any data can be recorded in the declaration; they then become subject to it on the same terms as everything else recorded.”

These sentences provide no authority to designate package databases, sysusers,
tmpfiles, base archives or deployment manifests on the person's behalf. They
also do not turn a requirement to record a component into a fact that it was
recorded. No file-location, package-owner, majority-of-members, authorship
precedence or program-identity rule is added. The original labels remain intact
for all measurements.

## Application of §9.2

The fixed failure condition, verbatim from [PAPER.html](../../../first-paper/PAPER.html), is:

> An object is found on either machine that, under the definitions, belongs to no class or belongs to two classes with different consequences, or the two classifications assign the object to different classes and the text of the definitions does not resolve the disagreement.

| System / outcome | Row id; source TSV line | Object | Evidence | §5 decision |
|---|---|---|---|---|
| Arch **0** | `arch-3e7f7f2c59`; 55 | `/home/census/.inputrc` | setting script, lines 7–8, writes `set completion-ignore-case on`; log shows Bash `bind -f` applies it and `bind -v` reports it on | **not resolved**, O2 |
| Silverblue **0** | `silverblue-661587021d`; 468 | `/var/home/census/.bashrc` | day.log appends `export EDITOR=vi`; day-after.log runs Bash with that rcfile and prints `Executed personal setting EDITOR=vi` | **not resolved**, O2 |
| FreeBSD **0** | `freebsd-72a7d6a331`; 325 | `/home/census/.exrc` | day script, line 9, writes `set number`; day.log and TTY verification show creation and `set number?` returning `number` | **not resolved**, O2 |

On each row, classification 1 records an unresolved data/internal-code-derivative boundary
and missing recorded-parent designation; classification 2 selects data solely from
personal authorship. The substantive disagreement is whether the personal-data
sentence settles the class despite the internal-code sentence. **Q4 contains
both statements and no precedence or exclusion.** Arch's inputrc is an
interpreted Readline setting applied through Bash, not evidence that it is a
shell script; §5 provides no parsing-versus-execution rule that would resolve
the submitted disagreement. Silverblue sources shell code; FreeBSD applies vi/ex
configuration commands. The observations are present, rather than missing files
or a failed settings test.

The competing readings have different lifecycle implications: §5.2 P6 says,
“If the program is absent from the current generation, its derivative is moved
to an archive.” It does not give that program-dependent lifecycle to personal
data. Section 8 O2 describes the same settings/execution boundary as open, but
is used here only to name the hole, not to supply a resolution.

The outcome uses the **unresolved-disagreement disjunct**, not a claim that two
fully established classes have been proved despite the missing recorded parent.
It does not depend on declaring any of the other 506 hole rows a definition
counterexample. A missing designation alone would leave insufficient data;
it does not supply the absent §5 rule for these observed authored settings.
One such unresolved substantive disagreement on each system suffices for 0;
there is no agreement/κ threshold in §9.2. Overall is 0 because the failure
condition is existential, not decided by averaging system scores.

## Every hole

The complete [509-row hole ledger](raw-X1C/holes.tsv), including agreements on
holes, gives **row/id, why, O1–O9 or NEW**, both original reasons, the original
Classification 1 tags separately from X1C's tags, and evidence. `NEW` identifies missing
designation, program-identity/causal provenance, or mixed-group measurement
issues not themselves settled by O1–O9. It names an observed issue; it proposes
no new definition. Multiple tags are nonexclusive. O6–O8 are not tested here;
P5 is relevant to some claims but actual recorded-data status is not established
sufficiently to claim an O3 counterexample.

| Hole family | Rows | Why / mapping |
|---|---:|---|
| Recorded proxy versus evidence hole | 313 | Person's designation unestablished; **NEW** |
| Claimed derivative versus evidence hole | 113 | Eligible recorded parent and creator/need; **O1, NEW** |
| Personal rule versus running-component requirement | 9 | No proof of actual recording, instrumentation/authorship boundary; **O2, O4, NEW** |
| Installed programs / Flatpak | 1 | Need, eligible parent, launching/running scope; **O1, O5, O9, NEW** |
| Executed personal settings | 3 | Data versus internal-code derivative; **O2, NEW** (also missing parent designation) |
| Heterogeneous groups with differing annotations | 5 | Different members/owners do not prove two classes for one object; **O1, NEW** |
| Shared hole-none: heterogeneous groups | 9 | Same grouping limitation despite matching labels; **O1, NEW** |
| Shared hole-none: inherited settings | 15 | Copying versus personal creation and program need; **O1, O2, NEW** |
| Shared hole-none: creator/consumer claims | 17 | Creator versus consumer, program identity and need unproved; **O1, NEW** |
| Shared hole-none: remaining provenance | 24 | Installer/base/instrumentation or creator/designation exclusions unproved; **O1, NEW** |
| Total | **509** | Unique row union |

The five unresolved aggregate annotations are listed explicitly so they cannot
be mistaken for the three decisive settings cases:

| Row id; source line | Object | Why §5 does not resolve the row |
|---|---|---|
| `arch-57da4d32dc`; 64 | `/var/lib/systemd` | Operational state plus `linger/census` |
| `silverblue-b86fee9a16`; 462 | `/etc/systemd` | Classification 2 names systemd and uresourced derivatives of different owners |
| `silverblue-57da4d32dc`; 480 | `/var/lib/systemd` | Timer state plus a person-enabled linger rule |
| `freebsd-0075a76d48`; 315 | `/etc/ssh` | Base-member files plus generated host keys |
| `freebsd-0306bdd9a9`; 316 | `/etc/ssl` | Base members plus generated certificate hash links |

These are **not resolved by §5 at aggregate-row granularity**. `hole-none` and
`hole-two` here are competing annotations, not two substantive §5 classes.
Different members or owners in a directory group do not establish that one
object has two classes with different consequences. These grouping/evidence
holes do not independently establish 0. No regrouping or new classifications
were introduced after observing the results.

## Limitations and verification

- Agreement describes only the **510 paired residual rows**. The 2,876
  automatically preclassified observations (2,873 recorded proxies and three
  authored-document groups) did not receive these two independent row decisions
  and are excluded, not counted as agreements. The fourth data row in classification 1's
  combined summary is residual `.nanorc`. Native inventories overlap across
  packages, paths, services and processes; these are not disjoint object counts.
- The supplied labels have different semantics: classification 1 explicitly uses
  `hole-none` for an evidence gap, while classification 2 often claims no class fits.
  Thus even agreement on 65 hole annotations does not prove agreement on the
  underlying predicates. No after-adjudication agreement score is substituted
  for the measured independent labels.
- Classification 2 uses package/image proxies, external (non-guest)/upstream
  tmpfiles observations and, for some Silverblue symlinks, expressly says
  “not in raw evidence.” Those claims cannot establish the guest's designated
  declaration. The reasons remain visible in the ledgers. See
  classifier source.
- X1 supplies three disposable VMs and short scripted CLI workloads with at
  least 120 seconds of service activity, not two lived-in personal machines or
  full days/GUI workloads. Shared source material and proxy assumptions limit
  independence; X1C compares the supplied independently produced files and does
  not certify their isolation. The findings do not estimate prevalence on other
  machines.
- As documented in X1-SUMMARY.md, root-walk scope omits general
  `/run`, `/tmp`, `/proc`, `/sys`, `/dev`, other unowned `/usr`, Arch `/efi`, full
  OSTree stores, firmware and off-disk state (**O9**). Some device bindings and
  inactive units remain raw-only. FreeBSD release membership predates p4;
  process races and heterogeneous groups remain. A successful exhaustive census
  cannot be claimed. These limitations do not resolve the three observed O2
  disagreements.
- [Validation](raw-X1C/validation.json) verifies exact ID coverage, source
  preservation and complete disagreement/hole exports; report checks
  verify original reasons/line references and exact §5 quotations. Numerical
  results were independently recomputed by a separate read-only check. A separate
  text reviewer agreed on the 436/8 adjudication partition and 0/0/0/0 outcomes
  (audit record). The final independent review
  accepted the report.
  No VMs, installs or system changes were needed for X1C.
