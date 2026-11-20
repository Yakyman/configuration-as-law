#!/usr/bin/env python3
"""Reproduce E6C's ID join, descriptive statistics and complete audit tables."""
import csv
import hashlib
import json
import shutil
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
E = ROOT
RAW = E / 'E6C-raw'
RAW.mkdir(exist_ok=True)
INPUTS = ['E/E6-c1-classes.tsv', 'E/E6-c2-classes.tsv',
          'E/E6-residual.tsv', 'E/E6-preclassified.tsv', 'E/raw-E6/holes.tsv']
# Freeze inputs on first run; later runs reproduce the same comparison.
for name in INPUTS:
    dst = RAW / 'inputs' / name
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dst)

def read(name):
    with (RAW / 'inputs' / name).open(newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def index(rows):
    out = {x['id']: dict(x, row=i) for i, x in enumerate(rows, 2)}
    assert len(out) == len(rows), 'duplicate ID'
    return out

def canonical(value):
    if value in ('recorded', 'recorded (works)'):
        return 'recorded'
    if value == 'derivative' or value.startswith('derivative of '):
        return 'derivative'
    assert value in ('data', 'hole-none', 'hole-two'), value
    return value

def dump(name, rows, columns=None):
    with (E / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=columns or list(rows[0]), delimiter='\t')
        w.writeheader()
        w.writerows(rows)

a = index(read('E/E6-c1-classes.tsv'))
b = index(read('E/E6-c2-classes.tsv'))
r = index(read('E/E6-residual.tsv'))
p = index(read('E/E6-preclassified.tsv'))
h = index(read('E/raw-E6/holes.tsv'))
assert a.keys() == b.keys() == r.keys()
assert not (r.keys() & p.keys())
assert h.keys() == {i for i, x in a.items() if x['class'].startswith('hole')}

REASONS = {
 'DECL': ('NEW', 'Package membership/provisioning is a proxy; §5 requires personal designation of the primary description. Text alone cannot establish that historical fact.'),
 'ACCT': ('O1; NEW', 'An account is a running component, but package scripts or package membership alone do not establish both declaration designation and the creator’s operational need.'),
 'BOOT': ('O1; O9', 'Boot artifact creation, later consumption and running-component granularity are not settled by the path or a generating-tool attribution.'),
 'COMP': ('O1; O9; NEW', 'The observed service/configuration can describe what runs or be generated state; §5 supplies no composition or designation test for this observation.'),
 'GRAN': ('O9; NEW', 'Kernel/manager runtime representation versus separately classified component is not determined at this observation’s granularity.'),
 'GROUP': ('O1; O2; NEW', 'The row combines members with potentially different authors, purposes or classes; no group-composition rule is stated.'),
 'CREATOR': ('O1; O2', 'Observed writer, later consumer and human-supplied settings do not establish a unique derivative/data assignment for every member.'),
 'SHARED': ('O1', 'P6 permits shared need, but does not establish the actual needed-by owner set from a log filename or writer list.'),
 'REFERENCE': ('O9; NEW', 'An absent-unit reference does not fix whether the object is a name, source dependency or manager state.'),
 'EVIDENCE': ('O1; O2; NEW', 'Saved path/type and an asserted writer do not establish all §5 premises: creation, operational need, personal authorship and declaration designation.'),
 'CENSUS': ('O1; O2; NEW', 'User-data names the account, but its designation as declaration is unproved. Creation for the person does not prove cloud-init needs the account for its own operation; the alleged two-class witness is unproved.'),
 'PS': ('O5; O9; NEW', 'Launching packaged ps does not establish execution within the shell or two incompatible consequences. Recorded status is a proxy; §5 gives no launch/creation boundary.'),
 'INPUTRC': ('O2', 'Human authorship and consumption are observed. Data wording supports B, but §5 does not decide whether interpreting these setting commands is code executed within a program; no contrary derivative assignment is demonstrated.'),
 'TWO': ('O1; O2', 'Human-specified settings and a program writer are alleged; that alone does not prove creation for that writer’s operation or two classes with different consequences.'),
 'UNIT': ('O9; NEW', 'Packaged fragment and generated drop-in are different constituents. §5 does not classify their composite; two constituent classes do not prove incompatible classes of one object.'),
 'OWNER': ('O1; NEW', 'Same derivative class, different owner strings (often program versus package naming). §5 does not identify these names or establish distinct lifecycle consequences; no aliases are silently merged.'),
 'CODE': ('O1; NEW', 'The text settles the derivative class if B’s within-program execution premise is true. Actual execution of every member and the exact owner are not established merely by that assertion; these are evidence/owner gaps, not a missing code-class rule.'),
}
CODE_IDS = {'alpine-ea05c8eb7f', 'ubuntu-211f893687', 'ubuntu-3543b3a205',
            'ubuntu-3787beb4db', 'ubuntu-2d36998dd6', 'ubuntu-c15063bcfe',
            'ubuntu-90017bfd94', 'ubuntu-0fbf442b3c'}
CODE_QUOTE = 'Code executed within a program is its derivative.'
ISSUES = {'boot-provenance':'BOOT', 'component-configuration':'COMP',
 'component-granularity':'GRAN', 'grouping-gap':'GROUP',
 'creator-consumer-boundary':'CREATOR', 'shared-owner-boundary':'SHARED',
 'reference-identity':'REFERENCE', 'settings-code-boundary':'INPUTRC',
 'evidence-gap':'EVIDENCE'}

def reason(i, x, y, z, owner_diff):
    if owner_diff:
        return 'OWNER'
    if i.endswith('-96a19ba1e6'):
        return 'CENSUS'
    if i.endswith('-d8ee8908a9'):
        return 'PS'
    if i == 'ubuntu-cbd353d9e3':
        return 'UNIT'
    if i == 'alpine-3e7f7f2c59':
        return 'INPUTRC'
    if i in CODE_IDS:
        return 'CODE'
    if y['class'] == 'hole-two':
        return 'TWO'
    if z['kind'] == 'account':
        return 'ACCT'
    return ISSUES.get(h.get(i, {}).get('issue_type'), 'EVIDENCE')

joined = []
for i, z in r.items():
    x, y = a[i], b[i]
    ac, bc = canonical(x['class']), canonical(y['class'])
    for item in (x, y):
        if item['class'].startswith('derivative of '):
            assert item['class'][len('derivative of '):] == item['program_if_derivative']
        if canonical(item['class']) == 'derivative':
            assert item['program_if_derivative']
    od = ac == bc == 'derivative' and x['program_if_derivative'] != y['program_if_derivative']
    hole = ac.startswith('hole') or bc.startswith('hole')
    key = reason(i, x, y, z, od) if hole or od else ''
    op, why = REASONS[key] if key else ('', '')
    joined.append(dict(id=i, machine=z['machine'], residual_row=z['row'],
      c1_row=x['row'], c2_row=y['row'], kind=z['kind'], path_or_name=z['path_or_name'],
      c1_raw_class=x['class'], c2_raw_class=y['class'], c1_class=ac, c2_class=bc,
      c1_owner=x['program_if_derivative'], c2_owner=y['program_if_derivative'],
      class_match=ac == bc, literal_class_match=x['class'] == y['class'], owner_difference=od,
      hole_union=hole, text_resolution=('class rule resolved conditional on execution premise; factual/owner assignment not resolved' if key=='CODE' else 'not resolved' if hole or od else 'no semantic disagreement'),
      section5_resolving_sentence=CODE_QUOTE if key=='CODE' else '',
      reason_code=key, open_problem=op, adjudication_reason=why,
      c1_reason=x['reason'], c2_reason=y['reason'], evidence=z['short_evidence']))

dump('E6C-joined.tsv', joined)
dump('E6C-disagreements.tsv', [x for x in joined if not x['class_match'] or x['owner_difference']])
dump('E6C-holes.tsv', [x for x in joined if x['hole_union']])
coverage = [dict(id=i, machine=x['machine'], preclassified_row=x['row'], kind=x['kind'],
                path_or_name=x['path_or_name'], class_proxy=x['class'],
                why='Outside both residual classification files; no independent double classification supplied',
                open_problem='NEW: procedure coverage', evidence=x['evidence']) for i, x in p.items()]
dump('E6C-coverage-gaps.tsv', coverage)

def stats(rows, mode='canonical'):
    if mode == 'canonical':
        pairs = [(x['c1_class'], x['c2_class']) for x in rows]
    elif mode == 'literal':
        pairs = [(x['c1_raw_class'], x['c2_raw_class']) for x in rows]
    else:
        pairs = [((x['c1_class'], x['c1_owner'] if x['c1_class']=='derivative' else ''),
                  (x['c2_class'], x['c2_owner'] if x['c2_class']=='derivative' else '')) for x in rows]
    n = len(pairs)
    ca, cb = Counter(x for x,y in pairs), Counter(y for x,y in pairs)
    m = sum(x == y for x,y in pairs)
    po = Fraction(m,n)
    pe = Fraction(sum(ca[c]*cb[c] for c in ca), n*n)
    k = (po-pe)/(1-pe)
    return dict(n=n, matches=m, agreement=float(po), pe=float(pe), kappa=float(k),
                agreement_exact=str(po), pe_exact=str(pe), kappa_exact=str(k))

summary = {}
for system in ('ubuntu','alpine','overall'):
    rows = [x for x in joined if system=='overall' or x['machine']==system]
    counts = {side:dict(Counter(x[side+'_class'] for x in rows)) for side in ('c1','c2')}
    summary[system] = dict(canonical=stats(rows), literal=stats(rows,'literal'),
       class_and_owner=stats(rows,'owner'), counts=counts,
       class_disagreements=sum(not x['class_match'] for x in rows),
       owner_differences=sum(x['owner_difference'] for x in rows),
       holes=sum(x['hole_union'] for x in rows),
       both_hole_none=sum(x['c1_class']==x['c2_class']=='hole-none' for x in rows),
       affirmative_class_disagreements=sum(not x['class_match'] and not x['hole_union'] for x in rows),
       coverage_gaps=sum(system=='overall' or x['machine']==system for x in coverage), outcome='?')
(E/'E6C-statistics.json').write_text(json.dumps(summary, indent=2)+'\n')
manifest = {name:hashlib.sha256((RAW/'inputs'/name).read_bytes()).hexdigest() for name in INPUTS}
(RAW/'input-sha256.json').write_text(json.dumps(manifest, indent=2)+'\n')
checks = dict(unique_ids=True, residual_join_exact=True, missing_c1_ids=[], missing_c2_ids=[],
    preclassified_residual_disjoint=True, original_holes_exact=True, all_derivative_owners_consistent=True,
    full_join_rows=len(joined), hole_rows=sum(x['hole_union'] for x in joined),
    disagreement_rows=sum(not x['class_match'] or x['owner_difference'] for x in joined),
    input_snapshot_matches_live={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in manifest.items() if (ROOT/name).exists()})
assert all(checks['input_snapshot_matches_live'].values()), 'inputs changed during comparison'
(E/'E6C-validation.json').write_text(json.dumps(checks, indent=2)+'\n')

def cell(x):
    return str(x).replace('|','\\|').replace('\n',' ')

def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(cell(v) for v in row)+' |' for row in rows])

out = ['''# E6C — Check 1 comparison of the additional E6 systems

**2026-11-19 — Ubuntu: `?`; Alpine: `?`; overall: `?`.** The paired residual classifications are insufficient to establish either success or the fixed failure condition. This is not a claim of agreement: 184 of 262 normalized decisions differ and 199 rows have at least one hole flag. Every differing decision involves a hole flag; none assigns two different affirmative §5 classes. The claimed no-class/two-class cases have unproved premises or unresolved object boundaries, as detailed below. No rule is added and no original classification is overwritten.

## Fixed criterion and its application

`PAPER.html:220`, §9.2, verbatim:

> An object is found on either machine that, under the definitions, belongs to no class or belongs to two classes with different consequences, or the two classifications assign the object to different classes and the text of the definitions does not resolve the disagreement.

The criterion has no agreement or kappa threshold. The observed low agreement therefore does not itself select `0`. Equally, missing provenance must not silently become a proven no-class witness. `E6.md` explicitly defines Classification 1’s `hole-none` as “not established by this first pass”, rather than proof of impossibility. Classification 2’s `hole-two` reasons are claims to audit, not evidence that both defining premises and different consequences hold. The files’ hole labels are measurement categories, not additional classes defined in §5. E6B requested stronger hole meanings (“fits no class” / “fits two classes with different consequences”); identical hole labels therefore need not express the same evidential claim on both sides. The metrics below measure label agreement, not equivalence of those claims.

- **No-class branch:** 15 rows have `hole-none` from both classifiers (Ubuntu 8, Alpine 7); the saved reasons describe unknown image-build provenance or mixed groups, not demonstrated exclusion from every class. All other Classification 1 hole-none rows likewise withhold a decision. No proved no-class witness is established here.
- **Two-class branch:** Classification 2 marks 12 rows hole-two (Ubuntu 7, Alpine 5). The complete audit below checks each. They invoke human input versus a program writer, launching versus creation, or mixed unit constituents. These do not establish both §5 predicates for one object and different consequences. No proved two-class witness is established here.
- **Disagreement branch:** no joined row has different affirmative class assignments (recorded/data/derivative). There are 184 differing decisions involving hole flags, plus 14 same-class owner-string differences; all remain visible. The former do not supply a second affirmative class, and the latter do not establish different classes or lifecycle consequences. Thus this evidence does not demonstrate this failure branch. This is an evidential conclusion, not a new exception to §9.2: a verified unresolvable class disagreement or no-class/two-class object would require `0` immediately, even with high aggregate agreement.
- **Success:** unavailable: unresolved premises, unresolved boundaries and incomplete independent coverage prevent `1`. `?` does not mean the definitions resolve all rows. Eight code rows have a direct class rule conditional on the asserted execution fact; their factual/owner gaps remain. Other retained holes and owner differences are marked **not resolved** below.

## Join, normalization and counts

Inputs are frozen under [E6C-raw/inputs](E6C-raw/inputs/); hashes: [input-sha256.json](E6C-raw/input-sha256.json). The TSV join uses `id`, never row position. Both files contain exactly the same 262 unique residual IDs: Ubuntu 197, Alpine 65. No duplicate, missing or extra residual ID occurs. Source line numbers in the tables include the header as line 1.

Format-only normalization: `recorded (works)` and `recorded` → `recorded`; `derivative of X` and `derivative` → `derivative`, retaining X in the separate owner field. This changes no classification rule and does not certify a package/provisioning proxy as a designated declaration. `hole-none` and `hole-two` remain separate categories. No owner aliases are merged.

Unweighted nominal Cohen’s κ is calculated on the five normalized decision labels, including hole flags: `p_o = matches/N`, `p_e = Σ n_A(c)n_B(c)/N²`, `κ = (p_o−p_e)/(1−p_e)`. Hole agreement is agreement about an unresolved decision, not successful object classification. Statistics describe the supplied residual only, not all objects on either VM.
''']
out.append(table(['System','Paired residual','Matching labels','Agreement','p_e','κ','Different labels','Owner-only differences','Hole union'],
  [(s,summary[s]['canonical']['n'],summary[s]['canonical']['matches'],
    f"{summary[s]['canonical']['agreement']:.6%}",f"{summary[s]['canonical']['pe']:.9f}",
    f"{summary[s]['canonical']['kappa']:.9f}",summary[s]['class_disagreements'],
    summary[s]['owner_differences'],summary[s]['holes']) for s in summary]))
out.append('\nClass counts, **residual only** (A = Classification 1; B = Classification 2):\n')
out.append(table(['System / classifier','recorded','derivative','data','hole-none','hole-two'],
 [(s+' / '+side,*[summary[s]['counts'][side].get(c,0) for c in ['recorded','derivative','data','hole-none','hole-two']])
  for s in ('ubuntu','alpine') for side in ('c1','c2')]))
out.append('''
Sensitivity to representation (not alternative substantive verdicts):
''')
out.append(table(['System','Literal class-string matches / N','Literal κ','Normalized class + exact derivative owner matches / N','Class + owner κ'],
 [(s,f"{summary[s]['literal']['matches']}/{summary[s]['literal']['n']}",f"{summary[s]['literal']['kappa']:.9f}",
   f"{summary[s]['class_and_owner']['matches']}/{summary[s]['class_and_owner']['n']}",f"{summary[s]['class_and_owner']['kappa']:.9f}") for s in summary]))
out.append('''
Literal mismatches include 62 rows with matching normalized classes (24 recorded, 38 derivative); these are label-format differences, of which 14 also have different owner strings. Both raw labels and both owner strings remain in [E6C-joined.tsv](E6C-joined.tsv), so no raw disagreement is lost. Exact rational statistics and confusion-table-reconstructible counts: [E6C-statistics.json](E6C-statistics.json).

## Text audit of all disagreements and holes

The following exact §5 sentences are relevant. They can settle a class rule while leaving factual premises unverified; this distinction is recorded explicitly for eight code rows below:

- **Q-D**, §5.1: “Declaration—a collection of files that a person has designated as the primary description of the computer.”
- **Q-R**, §5.1: “Running components—users and the rules under which they operate, programs, drivers, and services.”
- **Q-V**, §5.1: “Derivative—an object that a described program has created itself because the object is needed for the program's operation: saved Wi-Fi networks for a network management service, extensions for a browser, a cache, a log.”
- **Q-C**, §5.1: “Code executed within a program is its derivative.”
- **Q-A**, §5.1: “Data—what a person has created: photographs, documents, databases, and their own settings files, such as a text editor configuration.”
- **Q-P3**, §5.2: “Everything that is on the computer and is not recorded in the declaration is either a derivative of a recorded program or the person's data.”
- **Q-P5**, §5.2: “Any derivative and any data can be recorded in the declaration; they then become subject to it on the same terms as everything else recorded.”
- **Q-P6**, §5.2: “A derivative needed by several programs exists as long as at least one of them is present.”

Q-R settles that an account is a running component; it does not designate a declaration. Q-P3 addresses the unrecorded remainder, and Q-P5 allows recording data/derivatives, so an overlap involving “recorded” is not automatically a two-class witness with different consequences. Q-P6 permits shared owners, but does not infer their need from paths. No quote is treated as an observation of a creator’s intent.

### Audit of all 12 alleged two-class witnesses
''')
out.append(table(['ID (A/B source line)','Object','A → B','§5 resolves? / why; open problem'],
 [(f"{x['id']} ({x['c1_row']}/{x['c2_row']})",x['path_or_name'],x['c1_class']+' → '+x['c2_class'],
   'not resolved — '+x['adjudication_reason']+' ['+x['open_problem']+']')
  for x in joined if x['c2_class']=='hole-two']))
out.append('''
Evidence anchors: the two `census` accounts are named in `raw-E6/{ubuntu,alpine}/user-data:4`; the collector invokes ps in `src/collect.sh:23`; Ubuntu’s unit fragment/drop-in are saved in `raw-E6/ubuntu/unit-paths.txt:1346–1349` and `E6-residual.tsv:253`. Human specification or a generated constituent alone does not establish the two competing predicates. Ubuntu’s hostname, sudoers and SSH cases, and Alpine’s sudoers and SSH cases, retain their individual provenance pointers in the full table below and the joined TSV.

For the agreed hole-none account `alpine-c6df412fe9`, B additionally says the requester is off-machine and “not this computer’s person”. §5’s data sentence says “a person”; it supplies no on-machine-authorship requirement. That exclusion cannot be adopted as a rule. Actual authorship and designation still remain unestablished, so neither no-class proof nor a positive data assignment follows.

Additional boundary candidate `alpine-3e7f7f2c59`: `src/day-alpine.sh:13–14` and `raw-E6/alpine/day.log:31–34` show writing `.inputrc` and loading it with `bind -f`; the log reports vi editing mode. Q-A supports data. Whether those settings count as Q-C’s “code” is not defined by §5; §8 O2 explicitly identifies that boundary. A withholds assignment and B chooses data; these are not two observed affirmative assignments. We do not invent either a “settings are never code” rule or a “all interpreted settings are code” rule.

### Direct text rule for the eight code assertions

For each following disagreement, **the class rule is resolved conditional on B’s factual execution premise**, by the exact sentence: “Code executed within a program is its derivative.” No new rule is needed to derive the class on that premise. This is not certification that each asserted file was actually executed, that every grouped member fits, or that B’s exact owner set is correct. Those retained evidence/owner holes prevent a fully verified assignment. In particular, `bash -s` alone does not prove `.bash_logout` was executed. Original classifier labels and pre-adjudication agreement statistics remain unchanged.
''')
out.append(table(['ID / A,B line','Object','B’s execution assertion','§5 text ruling'],
 [(f"{x['id']} / {x['c1_row']},{x['c2_row']}",x['path_or_name'],x['c2_reason'],
   'Derivative if execution premise holds: “'+CODE_QUOTE+'”') for x in joined if x['reason_code']=='CODE']))
out.append('''
Logs/caches and shared owners: Q-V explicitly gives logs and caches as examples; Q-P6 explicitly permits shared need. Consequently lack of a sole owner is not a missing class rule. For `*-d6ce9987c3` (wtmp), `ubuntu-9c96b64591` (btmp), and `ubuntu-698c23461f` (lastlog), the unresolved question is the actual needed-by set and recorded program, not whether several owners are allowed. Likewise the log/cache assertions for `*-293699acd1`, `ubuntu-626ab0ebaf`, and `ubuntu-382c94b98b` have textual derivative support; their asserted provenance/need is not established by the example sentence alone. These distinctions do not turn a filename or a claimant’s reason into a verified observation.

### Complete residual-hole list (199 rows)

This is the union of both classifiers’ original hole flags: 141 Ubuntu, 58 Alpine. It includes all 184 differing normalized labels and the 15 matching hole-none decisions. A/B labels use `R`=recorded, `V`=derivative, `D`=data, `H0`=hole-none, `H2`=hole-two. Rows are linked by ID and exact residual/A/B source line; full verbatim reasons and evidence pointers are in [E6C-holes.tsv](E6C-holes.tsv). The eight CODE rows have the conditional class ruling above, retaining factual/owner holes; the other 191 rows are **not resolved**. No original hole flag is silently removed by an inferred rule. The code column refers to the explicit reason below, and the row retains B’s particular claim. `NEW` is a gap not named by O1–O9, not a newly adopted rule: declaration/proxy identification, observation composition/identity, or evidence/procedure coverage. O-tags are diagnostic mappings only; they are not decisions on open problems.
''')
out.append(table(['Reason code','O1–O9 or NEW','Why §5 alone does not resolve'],[(k,*v) for k,v in REASONS.items() if k!='OWNER']))
labels={'recorded':'R','derivative':'V','data':'D','hole-none':'H0','hole-two':'H2'}
for system in ('ubuntu','alpine'):
    out.append('\n#### '+system+'\n')
    out.append(table(['Residual / A / B line','ID','Object','A → B','Why code; O / NEW','B’s specific claim (unverified where disputed)'],
      [(f"{x['residual_row']}/{x['c1_row']}/{x['c2_row']}",x['id'],x['path_or_name'],
        labels[x['c1_class']]+' → '+labels[x['c2_class']], x['reason_code']+'; '+x['open_problem'],x['c2_reason'])
       for x in joined if x['machine']==system and x['hole_union']]))
out.append('''
### All 14 same-class owner differences

These are additional owner/identity uncertainties, outside the 199 hole-flag rows. Every row is derivative/derivative; §5 text resolution: **not resolved** (reason OWNER, O1 + NEW). Program names versus package names are retained exactly; a naming difference is not by itself evidence of incompatible P6 consequences.
''')
out.append(table(['ID / A,B line','Object','A owner','B owner'],
 [(f"{x['id']} / {x['c1_row']},{x['c2_row']}",x['path_or_name'],x['c1_owner'],x['c2_owner']) for x in joined if x['owner_difference']]))
out.append('''
## Coverage holes and limitations

1. **Independent classification coverage (NEW):** `E6-preclassified.tsv` contains another 1,238 Ubuntu and 473 Alpine rows. None appears in either supplied classification TSV. The second classification (E6B) covered only the residual by design, so this is not a failed residual join. It is a limitation of Check 1’s “each object ... twice, independently” requirement. Every omitted ID, source line, object, reason and NEW mapping is listed in [E6C-coverage-gaps.tsv](E6C-coverage-gaps.tsv). Full E6 totals remain Ubuntu 1,435, Alpine 538, overall 1,973. No preclassified row was copied into both sides to inflate agreement. Full-census agreement/κ is unavailable.
2. **Additional enumeration coverage (O9 + NEW):** E6 reports Alpine user-service probes with runtime-directory/dependency-tree errors, despite zero exit status (`raw-E6/alpine/openrc-user-status.txt`, `openrc-user-runlevels.txt`, `openrc-user-paths.txt`). Unloaded unit files/device bindings are raw-only; excluded filesystem areas and physical firmware/TPM are not fully inventoried. These gaps have no residual ID and are not included in the 199 count. They are stand/coverage limits, not proved no-class objects.
3. **Evidence asymmetry (O1/O2 + NEW):** Classification 2 sometimes infers a creator from a package role or script (and explicitly says “script not saved” for eight Ubuntu accounts), while Classification 1 withholds classification. Existing scripts or known writers are not observed designation or need. E6C does not obtain new VM traces or silently accept either threshold. Some missing premises may be recoverable; the report does not claim every uncertainty is an intrinsic defect in §5.
4. **Proxy and dependence:** E6 calls recorded status an operational package/provisioning proxy. Most rows have no demonstrated personally designated primary declaration. The two residual assignments were made separately and independently, and E6B forbade reading Classification 1’s file; E6C audits their outputs, not the classifiers’ complete cognitive independence. Both used the same collected/grouped inventory and can share errors. The E6 review is not another classification. P1/P4 nonconformity of an ordinary distribution is not substituted for a Check 1 definition counterexample.
5. **Sampling:** one short scripted headless session per VM, not 24 elapsed hours, one user and narrow workloads; differing service universes; overlapping grouped observations rather than independent physical objects. Residual selection and dominant hole labels affect κ; pooled κ is descriptive only. No statistical confidence or OS-quality claim is made.
6. **Resolution limits:** eight of 184 label disagreements have an explicit conditional code-class ruling, while factual/owner gaps remain; 176 label disagreements and all 14 owner differences are not resolved. The table retains all original flags, including 15 matching hole-none pairs. This does not assert that every missing fact needs a new definition, nor that any particular proposed rule is correct. There is no proven incompatible class pair and no proved exclusion from all classes in this audit; further evidence or independent affirmative classifications can change `?` under the same fixed criterion.

## Reproduction and verification

Run `python E6C-compare.py` in this directory. It reads frozen inputs, joins by ID, computes exact fractions, emits the complete row tables and verifies unique/full joins, original hole coverage, owner-field consistency and unchanged source hashes. Output evidence: [E6C-validation.json](E6C-validation.json), [E6C-statistics.json](E6C-statistics.json), [E6C-joined.tsv](E6C-joined.tsv), [E6C-disagreements.tsv](E6C-disagreements.tsv), [E6C-holes.tsv](E6C-holes.tsv). The disagreement file has 198 rows (184 different labels + 14 owner-only); the hole file has 199. Their union has 213 distinct residual IDs. No original E6 or PAPER file is changed.

An independent definition audit is retained in [E6C-definition-audit.md](E6C-definition-audit.md). An independent review (`E6C-review.md`, a working file) independently reproduced the calculations and, in its appended exact-§9.2 clarification, supports `? / ? / ?` and retracts its initial proposed Alpine `0`. The report also incorporates its distinction between a direct code-class rule and unverified execution/owner premises. The original review and correction are both retained; mechanical checks are not self-acceptance of the scientific conclusion.
''')
(E/'E6C-RESULT.md').write_text('\n\n'.join(out)+'\n')
print(json.dumps({'summary':summary,'validation':checks},indent=2))
