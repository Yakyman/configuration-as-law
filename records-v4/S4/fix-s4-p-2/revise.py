#!/usr/bin/env python3
"""Prepare round-two documentation and status corrections from saved records."""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'fix-s4-p-1'


def read(name):
    with (PRIOR / name).open(newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def write(name, fields, rows):
    with (HERE / name).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


status = read('tables/fact-status.tsv')
audit = []
for row in status:
    if row['status'] != 'not-obtainable':
        continue
    fact = row['fact_id']
    if fact in ('V09', 'M14'):
        row['status'] = 'not rehearsed'
        basis = 'No targeted consumer/use rehearsal was performed. The current-reader route used for A13 has not been tried here. Neither item 1 nor item 4 is established.'
    elif fact == 'V02':
        basis = ('Item 4: three distinct reference searches, not three nonzero exits. '
                 'Installed manifests, residual metadata and cached archive manifests did not supply an old reference for an unowned path. '
                 'parts/void.md sections Prior sources and expected results and Rehearsal 2 result and final source validation; '
                 'collector/extra_void.py collect(): .linux*.plist selection, cached .xbps manifest selection, and candidate comparisons; '
                 'rehearsal/void/round3/coverage.tsv lines 136-144: nine cache-manifest queries exit 0; '
                 'rehearsal/void/round3/fact-summary.json adapters.old-package: 6859 no-surviving-receipt and 22282 equal. '
                 'The part report attributes equal comparisons to already-owned paths. '
                 'Unavailable means these three routes failed to record the requested old reference; it does not mean no archive exists elsewhere.')
    else:
        row['status'] = 'attempt evidence incomplete'
        if fact.startswith('A'):
            basis = ('Current directives, retained history and scriptlets were queried (parts/alma.md; '
                     'collector/extra_alma.py; rehearsal/alma/round3/coverage.tsv). '
                     'The historical_evidence_routes=3 aggregate is not a per-fact record that each of three attempts failed to obtain this fact. '
                     'The saved reducers do not establish that all possible retained event sources are absent.')
        elif fact.startswith('V'):
            basis = ('Current sources/package records were read (parts/void.md; collector/extra_void.py). '
                     'The three documented old-package reference routes concern V02, not this history fact. '
                     'No three distinct fact-specific failures or proof of no retained queryable event source is saved.')
        elif fact.startswith('M'):
            basis = ('Current sources/scriptlets/boot bytes were read (parts/microos.md; collector/extra_microos.py; '
                     'rehearsal/microos/round-3/coverage.tsv). Rehearsals 1-3 repair unit selection, cache decoding and validate source; '
                     'they are not three distinct attempts on this historical fact. No query-impossibility premise is established.')
        else:
            basis = ('Current listing/content/mount/source records were queried (parts/talos.md; collector/extra_talos.py). '
                     'The three listing or content methods concern T02/T06, not three methods retrieving this original reference or creation event. '
                     'Absence of that field in these schemas does not establish that no query can supply it.')
        basis += ' Task item 4 remains incomplete; no new attempt is invented or run in this correction.'
    audit.append({'fact_id': fact, 'old_status': 'not-obtainable', 'status': row['status'], 'basis': basis})
    row['reason_or_limit'] = row['reason_or_limit'].replace('no-surviving-receipt', 'no-reference-found') + ' Status basis: checks/status-basis.tsv.'
    row['evidence'] += ';S4/fix-s4-p-2/checks/status-basis.tsv#' + fact
write('tables/fact-status.tsv', list(status[0]), status)
write('checks/status-basis.tsv', list(audit[0]), audit)

missing = read('tables/MISSING.tsv')
for row in missing:
    row['how_recorded_now'] = row['how_recorded_now'].replace('no-surviving-receipt', 'no-reference-found')
    if row['fact'].split(':')[0] in ('V09', 'M14'):
        row['how_recorded_now'] = ('No targeted choice-event or consumer/use rehearsal has been performed; current metadata/digests may be present. '
                                   'No claim of query impossibility is made; 1 RESULT-only ID, 0 IDs in fixed matching inputs')
write('tables/MISSING.tsv', list(missing[0]), missing)

doc = (PRIOR / 'COLLECT.md').read_text().replace('fix-s4-p-1', 'fix-s4-p-2')
doc = doc.replace('No surviving receipt is explicit.', 'Missing comparison references carry no-reference-found in the handoff copy.')
doc = doc.replace('The existing cache-only reference status literal is documented below.',
                  'The handoff status names the cache-identity reference source.')
doc = doc.replace('## Revision scope and unchanged status literals', '## Revision scope and observation handoff')
start = doc.index('Existing collector status literals such as ')
end = doc.index('V09/M14 list ', start)
doc = doc[:start] + '''The operator runs the committed handoff copier before giving an observation to deciding parties. It changes only explicitly named status cells and two diagnostic counter keys. All object IDs, levels, kinds, names, membership, content, digests, evidence references, query exits and raw evidence are preserved. The original collector output remains a separate frozen record. HANDOFF.md describes the neutral field meanings and exact delivery procedure. The mapping and operator audit remain outside the deciding parties' document set.

''' + doc[end:]
doc = doc.replace('A past choice with no retained event record has no retrospective query route in this instrument.',
                  'No targeted choice-event or consumer/use rehearsal has been performed for these two groups; no claim of query impossibility is made.')
(HERE / 'COLLECT.md').write_text(doc)

commands = (PRIOR / 'COMMANDS.md').read_text().replace('fix-s4-p-1', 'fix-s4-p-2')
commands += '''
Before classification handoff, create new neutral copies with the exact five commands in HANDOFF.md. Preserve D1b/raw as collected. Send D1b/handoff together with the document allowlist and unchanged matching output; withhold the originals and handoff audit reports during the independent decisions. A failed handoff is recorded and the partial copy is not delivered; it never triggers a new collection or repairs an observation failure.
'''
(HERE / 'COMMANDS.md').write_text(commands)

ready = (PRIOR / 'READY.md').read_text().replace('FX-S4-P-1', 'FX-S4-P-2').replace('fix-s4-p-1', 'fix-s4-p-2')
ready = ready.replace('Runtime remains `collect.sh` and `collector/`, unchanged.',
                      'Collector runtime remains `collect.sh` and `collector/`, unchanged. New `fix-s4-p-2/neutralize.py` and `neutral-literals.tsv` prepare a separate observation handoff; they do not collect facts.')
ready = ready.replace('Newly listed V09/M14 have no choice-history or complete consumer/use record emitted by this instrument and are excluded from the numerator.',
                      'V09/M14 are not rehearsed and remain excluded from the numerator.')
ready = ready.replace('**18 recordable, 12 partial, 15 not-obtainable** groups',
                      '**18 recordable, 12 partial, 1 not-obtainable, 12 attempt evidence incomplete, 2 not rehearsed** groups')
ready = ready.replace('defines these as record availability within the collection routes, not evidence-sufficiency rulings under the published text.',
                      'restores TASK-S4-P items 1/4 for not-obtainable. Only V02 retains that status; `fix-s4-p-2/checks/status-basis.tsv` audits all 15 formerly so labelled groups. The 12 incomplete groups lack documented fact-specific three-attempt exhaustion or an established no-query reason. These are preparation statuses, not rulings under the published text.')
ready = ready.replace('No new query or machine run was performed.',
                      'No new query or machine run was performed. Changed checks are local accounting and synthetic handoff tests only.')
ready = ready.replace('Readiness still requires a fresh-copy collector exit of zero and success of the prescribed actions.',
                      'The 4-of-5 system count retains the historical fresh-copy collector/action gate; it is not certification that item 4 is complete for every missing fact. Twelve fact groups have incomplete attempt evidence and two are not rehearsed. Independent acceptance and publication remain pending. Readiness still requires a fresh-copy collector exit of zero and success of the prescribed actions.')
ready = ready.replace('all twelve status rows passed', 'all twelve action-status rows passed (actions.tsv)')
needle = 'Source hashes and cleanup records remain beside them;'
ready = ready.replace(needle,
    'Individual action exits come from each system\'s `actions.tsv`, not the transport rows in `status.tsv`. Void\'s `action-language_install_node`, `action-language_npm_install` and `action-language_cowsay` rows in `status.tsv` have exit 1 because the harness reads absent stderr logs with `cat`; all twelve actual action rows have exit 0 (`rehearsal/void/run-round3.py:39-42`). ' + needle)
ready = ready.replace('A03/A04/A07/A09/A11 not-obtainable.', 'A03/A04/A07/A09/A11 attempt evidence incomplete.')
ready = ready.replace('V02/V03/V07/V09 not-obtainable.', 'V02 not-obtainable; V03/V07 attempt evidence incomplete; V09 not rehearsed.')
ready = ready.replace('M03/M05/M11/M14 not-obtainable.', 'M03/M05/M11 attempt evidence incomplete; M14 not rehearsed.')
ready = ready.replace('T03/T05 not-obtainable.', 'T03/T05 attempt evidence incomplete.')
ready = ready.replace('`fix-s4-p-2/records/void.md`', '`fix-s4-p-1/records/void.md`')
ready = ready.replace('the new observation and the matching output:',
                      'the neutral observation copy produced under `fix-s4-p-2/HANDOFF.md` and the unchanged matching output:')
ready = ready.replace('Full records are withheld from those parties during their work.',
                      'Full records, original unneutralized observations, mapping source and handoff audit reports are withheld from those parties during their work. Neutralization preserves every measured value and unknown/failure field; it changes only enumerated wording.')
ready = ready[:ready.index('Changed accounting checks:')] + '''Changed checks: `fix-s4-p-2/checks/accounting.json`, `fix-s4-p-2/checks/handoff-tests.json` and `fix-s4-p-2/raw/publication-verification.json`. All prior files except the requested active READY update retain their baseline hashes. Only status accounting, documentation, publication selection and the separate handoff copier changed; no collector runtime, matcher, action, installation or failure condition changed. These are mechanical preparation checks, not independent acceptance. Finding-by-finding responses: `FIX-S4-P-2.md`.
'''
(HERE / 'READY.md').write_text(ready)
print('Updated round-two status and documentation copies; frozen inputs unchanged.')
