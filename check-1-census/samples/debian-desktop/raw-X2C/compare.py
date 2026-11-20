#!/usr/bin/env python3
"""Reproduce X2C join, metrics and exhaustive row adjudication from frozen inputs."""
import csv
import hashlib
import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / 'inputs'

def read(name):
    with (INPUT / name).open(newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    assert len(rows) == len({r['id'] for r in rows}), ('duplicate IDs', name)
    return {r['id']: dict(r, source_row=i) for i, r in enumerate(rows, 2)}

a = read('X2-c1-classes.tsv')
b = read('X2-c2-classes.tsv')
r = read('X2-residual.tsv')
h = read('X2-hole-register.tsv')
ids = sorted(set(a) | set(b) | set(r))
integrity = {
    'c1_rows': len(a), 'c2_rows': len(b), 'residual_rows': len(r),
    'duplicates': 0,
    'missing_c1': sorted(set(ids)-set(a)),
    'missing_c2': sorted(set(ids)-set(b)),
    'missing_inventory': sorted(set(ids)-set(r)),
    'missing_hole_register': sorted(set(ids)-set(h)),
}
(BASE / 'join-integrity.json').write_text(json.dumps(integrity, indent=2)+'\n')
assert all(not integrity[k] for k in integrity if k.startswith('missing_'))

def generic(label):
    return 'derivative' if label.startswith('derivative of ') else label

stats = {}
for machine in sorted({x['machine'] for x in r.values()}):
    group = [i for i in ids if r[i]['machine'] == machine]
    n = len(group)
    ca = Counter(a[i]['class'] for i in group)
    cb = Counter(b[i]['class'] for i in group)
    matches = sum(a[i]['class'] == b[i]['class'] for i in group)
    cross = sum(v*cb[k] for k,v in ca.items())
    po, pe = Fraction(matches,n), Fraction(cross,n*n)
    kappa = (po-pe)/(1-pe) if pe != 1 else None
    stats[machine] = dict(n=n, matches=matches, disagreements=n-matches,
        different_affirmative_class_pairs=sum(a[i]['class'] != b[i]['class'] and not a[i]['class'].startswith('hole-') and not b[i]['class'].startswith('hole-') for i in group),
        agreement_fraction=str(po), agreement=float(po),
        expected_agreement_fraction=str(pe), expected_agreement=float(pe),
        kappa_fraction=str(kappa), kappa=float(kappa) if kappa is not None else None,
        c1_counts=dict(ca), c2_counts=dict(cb),
        c1_generic_counts=dict(Counter(generic(a[i]['class']) for i in group)),
        c2_generic_counts=dict(Counter(generic(b[i]['class']) for i in group)),
        hole_union=sum(a[i]['class'].startswith('hole-') or b[i]['class'].startswith('hole-') for i in group),
        pair_counts=[dict(c1=x, c2=y, count=v) for (x,y),v in sorted(Counter(
            (generic(a[i]['class']), generic(b[i]['class'])) for i in group).items())])

SCRIPTS = {'fb87e8bdd4','09fa2e5ce3','f5e686458b','2438267eef','d54b59c426'}
QUOTES = {
    'Q1': 'Declaration—a collection of files that a person has designated as the primary description of the computer.',
    'Q2': "Derivative—an object that a described program has created itself because the object is needed for the program's operation: saved Wi-Fi networks for a network management service, extensions for a browser, a cache, a log.",
    'Q3': 'Code executed within a program is its derivative.',
    'Q4': 'Data—what a person has created: photographs, documents, databases, and their own settings files, such as a text editor configuration.',
    'Q5': 'Everything that is on the computer and is not recorded in the declaration is either a derivative of a recorded program or the person\'s data.',
    'Q6': 'A derivative exists as long as its program is present in the current generation or in one of the saved generations.',
    'Q7': 'If the program is absent from the current generation, its derivative is moved to an archive.',
}
rows = []
for ident in sorted(ids, key=lambda i:r[i]['source_row']):
    x,y,obs,old = a[ident],b[ident],r[ident],h[ident]
    suffix = ident.rsplit('-',1)[1]
    disagree = x['class'] != y['class']
    hole = x['class'].startswith('hole-') or y['class'].startswith('hole-')
    topics = set(t for t in old['topic'].split(',') if t.startswith('O'))
    topics.update(re.findall(r'\bO[1-9]\b', x['reason']+' '+y['reason']))
    quote_ids = ['Q1','Q2']
    if suffix in SCRIPTS:
        status = 'candidate definition boundary; instrumentation authorship/designation gap'
        why = 'Individual executor-authored source is executed/sourced by bash. Code-within-program is explicit, but the person-created data premise and described/recorded bash are not established. §5 gives no delegation-of-authorship rule. Competing data/derivative readings would differ under P6, but two applicable classes are not demonstrated.'
        topics.add('NEW')
        quote_ids = ['Q3','Q4','Q6','Q7']
    elif suffix == 'efc18859d4':
        status = 'agreed data; not a submitted hole'
        why = 'Both label retained, unexecuted source copy as data; agreement is not independent proof of all premises.'
        quote_ids = ['Q4']
    elif suffix == 'f05cbeb21e':
        status = 'unresolved definition disagreement; copy boundary; designation gap'
        why = 'For member d00001-001, byte-identical authored content versus CUPS-created operational copy: §5 gives no copy/creation priority. Other spool members are not this counterexample. Missing described-owner evidence remains separate.'
        topics.update(['O1','O2','NEW'])
        quote_ids = ['Q1','Q2','Q4','Q6','Q7']
    elif suffix == 'a8b44f743e':
        status = 'mixed-group; authorship/intent evidence gap'
        why = 'Personal research outputs and generated logs coexist; §5 does not assign the whole mixed group one class or resolve mediated creation. A group mixture is not proof of double membership of one file.'
        topics.update(['O1','O2','NEW'])
        quote_ids = ['Q1','Q2','Q4']
    elif old['status'] in ('reference-not-object','observation-race'):
        status = old['status']
        why = old['reason']+' Text cannot supply missing observational evidence.'
        topics.add('NEW')
    elif suffix in {'688808b26c','de9a685076','bf374a250d','b86fee9a16','57da4d32dc'}:
        status = 'mixed-group; designation gap'
        why = 'Different members have different roles; directory mixture is not demonstrated same-object double membership. §5 supplies no whole-group priority; recorded-owner evidence is absent.'
        topics.add('NEW')
        quote_ids = ['Q1','Q2','Q4']
    elif suffix == '351644c1fd':
        status = 'candidate settings/data boundary; authorship/designation gap'
        why = 'Root access key/policy combines supplied key material with cloud-init disable-root output. §5 does not decide personal setting versus operational derivative from this provenance; person authorship and described-owner status are not established.'
        topics.update(['O1','O2','O4','NEW'])
        quote_ids = ['Q1','Q2','Q4']
    elif suffix == '96d642d273':
        status = 'candidate definition boundary; designation gap'
        why = 'Personal color-scheme setting is in dconf operational database; data versus derivative boundary has no priority in §5; described-owner premise remains unevidenced.'
        topics.add('NEW')
        quote_ids = ['Q1','Q2','Q4','Q6','Q7']
    elif y['class'] == 'recorded (works)':
        status = 'designation evidence gap; unsupported recorded inference'
        why = 'Being a running-component kind or being manually provisioned does not establish recording in person-designated files. Q1 rejects that inference but cannot establish a unique alternative class. P1/P4 are requirements, not observations.'
        topics.add('NEW')
        quote_ids = ['Q1','Q5']
    elif y['class'].startswith('derivative of '):
        status = 'described-owner/intent evidence gap'
        why = 'Producer/path/package evidence does not establish the described/recorded owner required by Q2/Q5. Text constrains the claim but cannot supply designation, provenance or intent; no unique class is established.'
        topics.add('NEW')
        quote_ids = ['Q1','Q2','Q5']
    elif y['class'] == 'data':
        status = 'mediated authorship/intent evidence gap'
        why = 'Requested setting or tool-generated research output may express a person\'s intent, but §5 supplies no general rule equating all script-generated outputs with person-created data, or excluding operational derivatives.'
        topics.update(['O1','O2','NEW'])
        quote_ids = ['Q1','Q2','Q4']
    elif y['class'] == 'hole-two':
        status = 'candidate definition boundary; designation gap'
        why = 'Running-component kind is not itself a recorded class; program-generated origin does not establish described-owner status. Claimed component/derivative overlap remains unproved; §5 does not settle the row\'s final class.'
        topics.add('NEW')
        quote_ids = ['Q1','Q2','Q3','Q5']
    else:
        status = 'provenance/designation evidence gap'
        why = 'Both submit hole-none; missing creator/designation evidence does not prove that no class exists. Text cannot supply the absent factual premises.'
        topics.add('NEW')
    rows.append(dict(id=ident,machine=obs['machine'],residual_row=obs['source_row'],
        c1_row=x['source_row'],c2_row=y['source_row'],kind=obs['kind'],path_or_name=obs['path_or_name'],
        c1_class=x['class'],c2_class=y['class'],identical_class=not disagree,
        any_submitted_hole=hole,c1_program=x['program_if_derivative'],c2_program=y['program_if_derivative'],
        c1_reason=x['reason'],c2_reason=y['reason'],
        text_resolution='not resolved' if disagree else 'not applicable: identical submitted class',
        section5_quotes=' | '.join(f'{q}: {QUOTES[q]}' for q in quote_ids),
        adjudication_status=status,why=why,topic=','.join(sorted(topics)),
        original_c1_status=old['status'],evidence=obs['short_evidence']))

def write(name, selected):
    with (BASE/name).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),delimiter='\t')
        writer.writeheader(); writer.writerows(selected)

write('joined.tsv',rows)
write('disagreements.tsv',[x for x in rows if not x['identical_class']])
write('holes.tsv',[x for x in rows if x['any_submitted_hole']])
stats['adjudication_counts'] = dict(Counter(x['adjudication_status'] for x in rows))
(BASE/'statistics.json').write_text(json.dumps(stats,indent=2)+'\n')
(BASE/'section5-quotes.json').write_text(json.dumps(QUOTES,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({m:{k:v for k,v in s.items() if k not in ('c1_counts','c2_counts','pair_counts')} for m,s in stats.items() if m != 'adjudication_counts'},indent=2))
