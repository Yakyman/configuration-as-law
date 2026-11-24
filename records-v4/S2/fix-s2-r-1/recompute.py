"""Recompute only FX-S2-R-1 adjudication, evidence audit and accounting.

Run from the night folder. Frozen inputs are read only. No probe is run.
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path('S2/fix-s2-r-1')


def read(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write(name, rows):
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


rows = read('S2/adjudication/rows.tsv')
facts = read('S2/facts.tsv')
c1 = {r['object']: r for r in read('S2/c1/decisions.tsv')}
c2 = {r['object']: r for r in read('S2/c2/decisions.tsv')}
facts_by_id = defaultdict(dict)
for line, r in enumerate(facts, 2):
    facts_by_id[r['object']][r['fact']] = (line, r)

boot = 'void-386e90812bdecbec21d0785c'
container = 'developer-59a4ddfe60a8a1b18f6627c9'
hook = 'developer-3bcbeded8b7cf5aedc1382fb'
links = 'server-be5afc83ca654a448cd1fb60'
audit_ids = {r['object'] for r in rows if r['family'] in {'7', '8', '10', '12'}
             and r['verdict'] in {'AGREED', 'GAP'} and 'GAP' in r['c1']}

# Each UNKNOWN in each challenged shared-gap object is accounted for, without
# converting an unobserved fact into a known fact.
audit = []
for r in rows:
    oid, family = r['object'], r['family']
    if oid not in audit_ids:
        continue
    ff = facts_by_id[oid]
    for fact, (line, f) in ff.items():
        if not f['value'].startswith('UNKNOWN:'):
            continue
        if fact == 'primary_description_designation':
            sentences = 'S8.1-3;S8.2-1;S8.2-2;S8.2-19'
            reason = ('Whether a person designated a primary-description file determines what the declaration is, '
                      'not whether this object must be included. S8.2-1/-2 specify the obligation; S8.2-19 '
                      'permits voluntary recording of objects that need not be recorded. Neither alternative '
                      'decision depends on whether that obligation has already been fulfilled. No existing '
                      'declaration or successful application is asserted.')
            evidence = f'S2/facts.tsv:{line}; S2/c1/decisions.tsv and S2/c2/decisions.tsv, {oid}'
        elif fact == 'unchanged_since_receipt' and family == '7':
            sentences = 'S8.1-4;S8.1-6;S8.2-6;S8.2-7;S8.2-15'
            reason = ('The saved delivery is a project git clone, not an installer-managed package transaction. '
                      'The object is Git repository storage produced during that clone, not a file delivered '
                      'with the Git package. S8.2-7 requires receipt as part of an installed package before '
                      'unchangedness can decide its second branch. This branch is inapplicable under either '
                      'value of unchangedness here. Git reads these paths as repository data; no hook or '
                      'launch directive is assigned to them. The two S8.2-15 clauses remain the dispute. '
                      'This does not apply to the four Homebrew installation repositories.')
            evidence = '; '.join('S2/facts.tsv:'+str(ff[k][0]) for k in
                                 ['delivery', 'execution_content', 'launch_access', 'producer', fact])
        elif fact == 'unchanged_since_receipt' and family == '12':
            sentences = 'S8.1-4;S8.1-6;S8.2-6;S8.2-7;S8.2-9;S8.2-23'
            reason = ('The disputed command-bearing file is authored locally by the operator through a shell '
                      'heredoc (and a copy into cron.d for the cron case), not received with an installed '
                      'package. A package receipt comparison cannot decide S8.2-7 for this file; the '
                      'known producer and content settle that premise. The unknown comparison remains '
                      'unknown, without preventing the code-versus-values reading question. Group scope '
                      'and other members are discussed in FACT-AUDIT.md; this does not assert receipt '
                      'integrity for the whole directory.')
            evidence = '; '.join('S2/facts.tsv:'+str(ff[k][0]) for k in
                                 ['content', 'human_created_or_brought', 'producer', fact])
        elif oid == container and fact == 'unchanged_since_receipt':
            sentences = 'S8.1-4;S8.1-6;S8.2-7;S8.2-9;S8.2-11;S8.2-13'
            reason = ('Set aside c1\'s INSTALLED-OWN reading, consistently with the four image resolutions '
                      'in the frozen adjudication. The saved operation creates/starts a container; it '
                      'does not supply a received installer package for this stored container object. '
                      'Neither remaining reading (executable workload or saved service values) relies '
                      'on unchanged receipt. This audit does not reinstate the rejected installer reading.')
            evidence = 'S2/facts.tsv:19502,19519,19524,19525,19526; S2/adjudication/rows.tsv:51'
        elif oid == container and fact in {'execution_rights', 'host_change_capability'}:
            sentences = 'S8.2-9;S8.2-13;S8.2-21;S8.2-22'
            reason = ('The workload is running and has its own host-kernel process (S8.2-22), so on the '
                      'PROGRAM reading it is not code confined inside a recorded program under S8.2-21. '
                      'Exact UID, mounts and capabilities do not decide that established process boundary. '
                      'On the SETTING reading, operator-chosen service command, restart and port values '
                      'fall under S8.2-13 regardless of the workload\'s exact capabilities. Those unknown '
                      'capabilities cannot choose which of these two things the stored container denotes.')
            evidence = 'S2/facts.tsv:19495,19496,19498,19499,19503,19518,19519,19524'
        else:
            raise AssertionError((oid, fact))
        audit.append(dict(object=oid, family=family, fact=fact, saved_value=f['value'],
                          status='UNKNOWN, non-deciding for the stated alternatives', sentences=sentences,
                          evidence=evidence, reason=reason))
    r['reason'] += (' FX-S2-R-1: deciding-fact audit in S2/fix-s2-r-1/unknown-facts-audit.tsv '
                    f'and FACT-AUDIT.md, object {oid}; every saved UNKNOWN is addressed.')
    if oid == container:
        r['verdict'] = 'GAP'
        r['what_differs_in_the_declaration'] = 'nothing: PROGRAM-OWN and SETTING-OWN both require a line of its own'
        r['reason'] += (' The INSTALLED-OWN alternative is set aside consistently with the four images. '
                        'The remaining gap is PROGRAM-OWN for the executable workload (S8.2-9/-22) '
                        'versus SETTING-OWN for the persistent service values (S8.2-11/-13). '
                        'S8.2-6 fixes the order for a specified object; it does not specify which of '
                        'these referents the stored-container inventory object denotes. Both referents '
                        'and their behavior are established, not missing observations. See RESULT.md question 6.')
    if family == '12':
        r['reason'] += (' The code-versus-values question concerns the identified command-bearing member; '
                        'the full directory is not asserted to have a single category. See FACT-AUDIT.md.')

for r in rows:
    if r['object'] == boot:
        r['verdict'] = 'FACT-UNKNOWN'
        r['what_differs_in_the_declaration'] = 'undetermined for the six-member group; the two separate archive rows retain their stated difference'
        r['signs'] = 'n/a: group outcome ?; original answers preserved in signs.tsv'
        r['reason'] = ('FX-S2-R-1: the six-entry immediate-child group (S2/facts.tsv:18136) '
                       'includes the two separately counted archive witnesses and other boot members. '
                       'Their package/as-received status and human choices are not all established '
                       '(S2/facts.tsv:18065-18067,18137). Do not count the group as another complete-facts '
                       'counterexample. It is FACT-UNKNOWN, outcome ?. The two separate archives '
                       'void-0d4bff48fce03ced27aa83a4 and void-a6e5bb36a961f99d2e09e83e '
                       'remain GAP; family 4 remains 0.')


def outcome(r):
    if r['verdict'] == 'FACT-UNKNOWN' or (r['verdict'] == 'AGREED' and r['c1'].startswith('UNKNOWN')):
        return '?'
    if r['verdict'] == 'GAP' or (r['verdict'] == 'AGREED' and r['c1'].startswith('GAP')):
        return '0'
    return '1'


signs = []
for r in rows:
    oid = r['object']
    if outcome(r) != '0' and oid != boot:
        continue
    a, b = c1[oid], c2[oid]
    yesno = a['by_meaning'].split(':')[0] == b['by_meaning'].split(':')[0]
    second = a['without_forbidding'] == b['without_forbidding'] == 'yes'
    full = a['by_meaning'] == b['by_meaning']
    yn, fl = ('both signs' if yesno and second else 'not both'), ('both signs' if full and second else 'not both')
    signs.append(dict(scope='family' if oid != boot else 'excluded group', object=oid, family=r['family'],
                      outcome=outcome(r), c1_by_meaning=a['by_meaning'], c2_by_meaning=b['by_meaning'],
                      c1_without_forbidding=a['without_forbidding'], c2_without_forbidding=b['without_forbidding'],
                      yes_no_reading=yn, full_answer_reading=fl))
    if oid != boot:
        r['signs'] = f'yes/no reading: {yn}; full answer including line: {fl}; author choice pending'

sample = read('S2/sample-adjudication.tsv')
cup_ids = {'gaming-0b9c75abae9461b0be7b041d', 'gaming-7b8b804e906bab4f5a36ccf2'}
for r in sample:
    if r['id'] not in cup_ids:
        continue
    r['verdict'] = 'GAP'
    r['reason'] = ('The original agreement is INSTALLED-PACKAGE. The hard-link names created by '
                   'cups-daemon.postinst refer to unchanged packaged files: device/inode equality and '
                   'full package-integrity comparisons are saved in S2/a2/raw/evidence.txt:1-18; '
                   'the six-member group is enumerated in S2/a2/raw/facts.jsonl; the ln commands '
                   'are in S2/b2/raw/cups-daemon-postinst-backends.txt. S8.2-7 “Is the object a '
                   'package installed on the computer, or was it obtained as part of such a package '
                   'and does it remain as received?” Reading A takes the object to be the received '
                   'unchanged file, allowing INSTALLED-PACKAGE and its package line. Reading B takes '
                   'the object to be the additional name made on the computer, giving PROGRAM-DERIVED '
                   'and coverage by the installation/link-creation line under S8.2-9/-16. '
                   'No sentence chooses file identity over the created name. The original adjudication '
                   'chose A; that choice is withdrawn. S8.2-6 orders the questions but does not resolve '
                   'this reading of question 1. This is GAP on known facts, outcome 0, even though both '
                   'decisions require recording. See RESULT.md question 13. The group and its snmp '
                   'member overlap physically but remain two sampled agreements in the fixed sample.')

write('rows.tsv', rows)
write('sample-adjudication.tsv', sample)
write('unknown-facts-audit.tsv', audit)
write('signs.tsv', signs)
write('outcomes.tsv', [dict(object=r['object'], family=r['family'], outcome=outcome(r)) for r in rows])

family_outcomes = {}
for family in range(1, 16):
    counts = Counter(outcome(r) for r in rows if r['family'] == str(family))
    family_outcomes[str(family)] = {'rows': dict(counts), 'outcome': '0' if counts['0'] else '?' if counts['?'] else '1'}
a1 = {(r['source'],r['id']): r for r in read('S2/a1/sample.tsv')}
a2 = {(r['source'],r['id']): r for r in read('S2/a2/sample.tsv')}
assert a1.keys() == a2.keys() and len(a1) == 600
adjudicated = {(r['source'],r['id']):r for r in sample}
sample_outcomes = Counter()
sample_by_source = defaultdict(Counter)
for key, a in a1.items():
    b = a2[key]
    if key in adjudicated:
        verdict = adjudicated[key]['verdict']
        result = 'does_not_follow' if verdict == 'GAP' else 'fact_unknown' if verdict == 'FACT-UNKNOWN' else 'follows'
    else:
        result = 'follows' if a['finding'] == b['finding'] == 'FOLLOWS' else 'fact_unknown'
    sample_outcomes[result] += 1
    sample_by_source[key[0]][result] += 1
sample_outcome = '0' if sample_outcomes['does_not_follow'] else '?' if sample_outcomes['fact_unknown'] else '1'
summary = dict(object_outcomes=dict(Counter(outcome(r) for r in rows)), families=family_outcomes,
               sample=dict(outcome=sample_outcome, **sample_outcomes),
               sample_by_source=dict(sample_by_source),
               signs_yes_no=dict(Counter(s['yes_no_reading'] for s in signs if s['scope']=='family')),
               signs_full=dict(Counter(s['full_answer_reading'] for s in signs if s['scope']=='family')),
               audited_objects=len(audit_ids), audited_unknowns=len(audit))
(OUT/'raw/counts.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='families'}, indent=2))
