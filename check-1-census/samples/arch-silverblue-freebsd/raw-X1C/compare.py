#!/usr/bin/env python3
"""Reproduce X1C counts and preserve the two supplied classifications unchanged.

The family notes document the text review, not a third classification rule.
Run from any directory. Inputs are the dated copies beside this script.
"""
import collections
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / 'inputs' / 'X'


def read(name):
    with (INPUT / name).open(newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    ids = [r['id'] for r in rows]
    assert len(ids) == len(set(ids)), (name, 'duplicate IDs')
    return rows, {r['id']: (i + 2, r) for i, r in enumerate(rows)}


residual, ri = read('X1-residual.tsv')
c1, ai = read('X1-c1-classes.tsv')
c2, ci = read('X1-c2-classes.tsv')
source_holes, hi = read('X1-holes.tsv')
assert set(ri) == set(ai) == set(ci)
assert set(hi) == {r['id'] for r in c1 if r['class'].startswith('hole-')}

QUOTES = {
    'declaration': 'Declaration—a collection of files that a person has designated as the primary description of the computer.',
    'derivative': "Derivative—an object that a described program has created itself because the object is needed for the program's operation: saved Wi-Fi networks for a network management service, extensions for a browser, a cache, a log.",
    'code': 'Code executed within a program is its derivative.',
    'data': 'Data—what a person has created: photographs, documents, databases, and their own settings files, such as a text editor configuration.',
    'p1': 'Everything that runs on the computer is recorded in the declaration.',
    'p3': "Everything that is on the computer and is not recorded in the declaration is either a derivative of a recorded program or the person's data.",
    'p5': 'Any derivative and any data can be recorded in the declaration; they then become subject to it on the same terms as everything else recorded.',
    'p6': 'If the program is absent from the current generation, its derivative is moved to an archive.',
}

O2 = {'arch-3e7f7f2c59', 'silverblue-661587021d', 'freebsd-72a7d6a331'}
EVIDENCE = {
    'arch-3e7f7f2c59': 'raw-X1/arch/setting-day.log:5-10; X1-arch-setting.sh:7-8',
    'silverblue-661587021d': 'raw-X1/silverblue/day.log (printf EDITOR=vi); raw-X1/silverblue/day-after.log (rcfile and Executed personal setting EDITOR=vi)',
    'freebsd-72a7d6a331': 'raw-X1/freebsd/day.log (printf set number); X1-freebsd-day.sh; raw-X1/freebsd/setting-verification-tty.txt (set number? -> number)',
}


def review(r, a, b):
    rid, reason = r['id'], b['reason']
    if rid in O2:
        return ('executed-personal-setting', 'O2,NEW', 'code,data,p3,p6',
                'Personal setting authorship and interpreter use are evidenced. Section 5 supplies both the data wording and the internal-code derivative wording, but no priority or exclusion resolving these submitted decisions. Recorded-parent designation is also unestablished. No two proved classes are asserted; this is an unresolved classification disagreement under the third disjunct of section 9.2.')
    if b['class'] == 'recorded (works)':
        return ('recorded-proxy-vs-evidence-hole', 'NEW', 'declaration,p1,p5',
                'The cited package/base/image/definition membership is not evidence that a person designated the primary description. Section 5 rejects treating that proxy alone as proof, but supplies neither the missing designation fact nor a unique class for this object. A required or permitted recording is not evidence of actual recording.')
    if b['class'].startswith('derivative of '):
        return ('derivative-claim-vs-evidence-hole', 'O1,NEW', 'declaration,derivative,p3',
                'The proposed creator/need is retained in the Classification 2 reason. Section 5 requires a described/recorded parent; its designation is unestablished. The text does not establish the missing fact or a unique alternative class. No owner is inferred from package name or directory.')
    if b['class'] == 'hole-two':
        if reason.startswith('mixed:'):
            return ('mixed-group', 'O1,NEW', 'derivative,p3,p5',
                    'Different members or derivative owners in one inventory group do not prove one object has two classes with different consequences. Section 5 has no rule assigning one class to this heterogeneous row; group-wide provenance and designation remain missing. Retain as a grouping/evidence hole, without inventing a majority or precedence rule.')
        if rid == 'silverblue-e0b055c77d':
            return ('installed-programs-and-derivatives', 'O1,O5,O9,NEW', 'declaration,derivative,p1,p3',
                    'The group contains installed Flatpak objects/programs. Creation by Flatpak and the P1 requirement do not establish actual declaration membership. Section 5 does not resolve the running/installed or program/derivative boundary for the group; no two proved classes are asserted.')
        return ('person-rule-and-running-component', 'O2,O4,NEW', 'declaration,data,p1,p5',
                'Classification 2 invokes person-made data and the P1 requirement to record a running-component rule. P1 does not prove actual recording and P5 does not impose exclusive classes. Section 5 does not select a unique class for the supplied instrumentation/authentication row. No proved two-class counterexample is inferred from the hole-two label.')
    if b['class'] == 'hole-none':
        if r['kind'] == 'stored-directory-skeleton' or reason.startswith('mixed:'):
            return ('agreed-hole-mixed-group', 'O1,NEW', 'derivative,p3',
                    'The shared hole-none label covers different member provenance or owners. The group is not proof of a single no-class object; no group-wide predicate is established.')
        if 'copied from skel' in reason:
            return ('agreed-hole-inherited-settings', 'O1,O2,NEW', 'derivative,data,p3',
                    'Classification 1 records unknown provenance/designation; Classification 2 excludes copied settings from data and derivatives. Section 5 supplies no copying/authorship precedence and the creator/need predicates are not fully established. Matching annotations do not prove matching interpretations or no-class status.')
        if 'creator !=' in reason or 'for other' in reason:
            return ('agreed-hole-creator-consumer', 'O1,NEW', 'derivative,data,p3',
                    'The suggested producer differs from the consumer. Program identity, need and eligible recorded parent are not established sufficiently to exclude all classes. Retain both reasons without turning a causal guess into a definition counterexample.')
        return ('agreed-hole-provenance', 'O1,NEW', 'declaration,derivative,data,p3',
                'Classification 1 records absent evidence; Classification 2 makes a no-class/provenance claim. The captures do not establish every exclusion needed to prove no class. Preserve the hole even though the labels match.')
    assert a['class'] == b['class'] == 'data'
    return ('agreed-personal-data', '', 'data', 'Both classify the authored, unexecuted .nanorc as data; no hole or disagreement.')


joined = []
for r in residual:
    rid = r['id']
    an, a = ai[rid]
    bn, b = ci[rid]
    family, tags, qkeys, why = review(r, a, b)
    same = a['class'] == b['class']
    hole = a['class'].startswith('hole-') or b['class'].startswith('hole-')
    resolved = family in {'recorded-proxy-vs-evidence-hole', 'derivative-claim-vs-evidence-hole',
                          'person-rule-and-running-component', 'installed-programs-and-derivatives'}
    resolution = ('not applicable: identical labels' if same else
                  'resolved: unsupported assertion rejected; evidence hole retained' if resolved else 'not resolved')
    if resolved:
        why = 'Text resolves the asserted support only; no replacement class is assigned. ' + why
    joined.append({
        'id': rid, 'system': r['system'], 'residual_line': ri[rid][0],
        'c1_line': an, 'c2_line': bn, 'kind': r['kind'], 'path_or_name': r['path_or_name'],
        'c1_class': a['class'], 'c2_class': b['class'],
        'c1_program': a['program_if_derivative'], 'c2_program': b['program_if_derivative'],
        'identical_class': int(same), 'any_hole': int(hole),
        'c1_reason': a['reason'], 'c2_reason': b['reason'],
        'c1_open_problem': hi[rid][1]['open_problem'] if rid in hi else '',
        'review_open_problem': tags, 'review_family': family,
        'section5_resolution': resolution,
        'resolution_quote': ' '.join(QUOTES[k] for k in qkeys.split(',')) if resolved else ('not resolved' if not same else ''),
        'relevant_section5_sentences': ' '.join(QUOTES[k] for k in qkeys.split(',')),
        'review_why': why, 'decisive_section9_2_witness': int(rid in O2),
        'source_evidence': r['short_evidence'], 'additional_evidence': EVIDENCE.get(rid, ''),
    })


def write_tsv(name, rows):
    with (HERE / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(joined[0]), delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


write_tsv('joined.tsv', joined)
write_tsv('disagreements.tsv', [r for r in joined if not r['identical_class']])
write_tsv('holes.tsv', [r for r in joined if r['any_hole']])


def rational(x):
    return {'exact': str(x), 'decimal': float(x)}


def metrics(rows):
    n = len(rows)
    ac = collections.Counter(r['c1_class'] for r in rows)
    bc = collections.Counter(r['c2_class'] for r in rows)
    matches = sum(r['identical_class'] for r in rows)
    po = Fraction(matches, n)
    pe = sum((Fraction(ac[c] * bc[c], n*n) for c in ac.keys() | bc.keys()), Fraction())
    kap = (po - pe) / (1 - pe) if pe != 1 else None
    matrix = collections.Counter((r['c1_class'], r['c2_class']) for r in rows)
    return {'n': n, 'matches': matches, 'disagreements': n-matches,
            'agreement': rational(po), 'expected_agreement': rational(pe),
            'kappa': rational(kap) if kap is not None else None,
            'c1_counts': dict(sorted(ac.items())), 'c2_counts': dict(sorted(bc.items())),
            'confusion': [{'c1': a, 'c2': b, 'n': v} for (a,b),v in sorted(matrix.items())],
            'hole_union': sum(r['any_hole'] for r in rows),
            'hole_both': sum(r['c1_class'].startswith('hole-') and r['c2_class'].startswith('hole-') for r in rows),
            'section5_resolutions': dict(collections.Counter(r['section5_resolution'] for r in rows if not r['identical_class'])),
            'review_families': dict(sorted(collections.Counter(r['review_family'] for r in rows).items()))}


result = {s: metrics([r for r in joined if r['system'] == s]) for s in ('arch', 'silverblue', 'freebsd')}
result['overall'] = metrics(joined)
(HERE / 'metrics.json').write_text(json.dumps(result, indent=2) + '\n')
(HERE / 'section5-quotes.json').write_text(json.dumps(QUOTES, indent=2, ensure_ascii=False) + '\n')
manifest_path = HERE / 'input-manifest.json'  # present only in the original working tree
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {'files': []}
original_root = HERE.parents[1]
changed = [r['source'] for r in manifest['files']
           if hashlib.sha256((original_root/r['source']).read_bytes()).hexdigest() != r['sha256']]
assert not changed, changed
validation = {'input_ids_equal': True, 'duplicates': 0, 'missing_or_extra_ids': 0,
              'joined_rows': len(joined), 'disagreement_rows': sum(not r['identical_class'] for r in joined),
              'hole_rows': sum(r['any_hole'] for r in joined), 'original_inputs_changed': changed,
              'row_numbers_include_header': True, 'class_labels_preserved': True,
              'derivative_program_fields_match': all(r['c2_class'] == 'derivative of '+r['c2_program'] for r in joined if r['c2_class'].startswith('derivative of '))}
(HERE / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
print(json.dumps({s: {k: v for k,v in m.items() if k in ('n','matches','disagreements','agreement','kappa','hole_union','review_families')} for s,m in result.items()}, indent=2))
