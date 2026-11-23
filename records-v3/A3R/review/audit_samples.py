"""Reproduce the fixed samples and write their reviewed decisions (no new probes)."""
import csv
import json
import random
import re
from pathlib import Path

csv.field_size_limit(10000000)
base = Path('A3R/review')
joined = list(csv.DictReader(open('A3R/compare/joined.tsv'), delimiter='\t'))
adjudicated = list(csv.DictReader(open('A3R/adjudication/rows.tsv'), delimiter='\t'))
adj_ids = {r['id'] for r in adjudicated}
sentences = {}
for line in open('SENTENCES.md'):
    match = re.match(r'- \*\*(S[\d.]+-\d+)\*\* (.*)', line)
    if match:
        sentences[match[1]] = match[2].replace('**', '')

plugins = {2, 8, 13, 14, 19, 22, 26, 31, 37}
metadata = {4, 15, 16}
manifest_scripts = {1, 3, 18, 20, 28, 30, 32, 34}
state = {9, 24, 29, 40}
all_results = []
for sample, count, seed, pool in [
    ('resolved', 40, 2026112201,
     [r for r in adjudicated if r['verdict'].startswith('RESOLVED:')]),
    ('agreed', 60, 2026112202,
     [r for r in joined if r['same'] == 'yes' and r['id'] not in adj_ids]),
]:
    selected = json.loads((base / f'{sample}_sample.json').read_text())
    expected = random.Random(seed).sample(sorted(pool, key=lambda r: r['id']), count)
    assert [r['id'] for r in selected] == [r['id'] for r in expected]
    for r in selected:
        n = r['sample_order']
        candidate = 'no'
        status = 'SUPPORTED'
        decision = r.get('adjudication_verdict', r['c1_decision'])
        ids = r.get('adjudication_sentence_id', r['c1_sentences'])
        note = ''
        if sample == 'resolved':
            if n in plugins:
                candidate, status = 'yes', 'REFUTED'
                ids = 'S2.2-10,S2.2-4,S2.2-7'
                note = ('Quoted code rule alone does not decide MIXED. Script members MUST; '
                        'README/document content NOT by S2.2-4; editor preference values NOT by S2.2-7. '
                        'The additional literal exemptions resolve the candidate.')
            elif n in metadata:
                candidate, status, decision, ids = 'yes', 'REFUTED', 'UNKNOWN', 'S3-2'
                note = ('Loss of metadata retrieval is established, but a non-content operational '
                        'dependency for this particular copy is not. S3-2 decides ?; no demonstrated '
                        'textual hole. Saved fields and version-specific documentation: sample_sources.md.')
            elif n == 12:
                candidate, status, decision, ids = 'yes', 'REFUTED', 'UNKNOWN', 'S2.2-10,S3-2'
                note = ('Four shell scripts MUST. The manifest reader/effect is not established; '
                        'one reported reader does not prove an internal preference. Whole-row MIXED '
                        'is unsupported; unresolved member yields ? under S3-2.')
            elif n == 38:
                candidate, status, decision, ids = 'yes', 'FACT-WRONG', 'NOT unsupported', 'S2.2-13,S3-2'
                note = ('Fontmap is token-parsed, while cidfmap is executed through the resource-map '
                        'loader; both are not values-only tables. S2.2-13 supplies the distinction. '
                        'Local content/rights still need facts; see sample_sources.md.')
            elif n in manifest_scripts:
                note = ('Saved manifest contains named shell-script dispatch operations; removal '
                        'loses those operations, so the quoted S2.2-2 applies. Counting readers or '
                        'assuming that every import fails is unnecessary. Exact saved fields: settings_cards.md.')
            elif n in state:
                note = ('S2.5-1 puts treatment of these identified bookkeeping/staging records outside '
                        'the definition. NOT is retained only as the adjudication coding of that scope '
                        'exclusion, not as a new blanket exemption for operative settings.')
            elif r['kind'] == 'group':
                note = ('Removing the named group removes named group selection/assignment and its '
                        'membership definition; S2.2-2 applies without assuming it owns active files.')
            elif n == 5:
                note = 'The members are icon images; only their visual content becomes unavailable, S2.2-4.'
            elif n == 6:
                note = ('Code/program members satisfy S2.2-9/10; browser dashboard code is confined '
                        'under S2.2-11; collector preferences and documentation satisfy S2.2-7/4.')
            elif n in {7, 23, 39}:
                note = ('The manifest has no shell commands and configures the containing runtime '
                        'component; S2.2-7 applies to the program-local values, not to the code package.')
            elif n == 11:
                note = ('Active PDF.ppd governs printer processing across cupsd/filters (S2.2-2); '
                        'PDF.ppd.O is its historical copy (S2.2-6).')
            elif n == 17:
                note = 'The auto-update flag controls the man-db trigger for its own index, S2.2-7.'
            elif n == 25:
                note = ('Both members are Makefiles containing build recipes interpreted with process '
                        'rights, S2.2-13/10; target-platform naming does not turn commands into content.')
            elif n == 27:
                note = ('The executable subtree represents test_run.sh and bootstrap scripts; '
                        'nonmember documents cannot make that row MIXED. S2.2-10 decides MUST.')
            else:
                raise AssertionError((sample, n))
        else:
            if n == 7:
                candidate, status, decision, ids = 'yes', 'OUTSIDE', 'OUTSIDE', 'S2.5-1'
                note = ('The member is a transient udev symlink arbitration record, program state. '
                        'Neither cited positive rule addresses the explicit design-scope exclusion; '
                        'S2.5-1 applies. This is not a hole or an operative persistent access policy.')
            elif n in {11, 19, 24, 38, 44, 58}:
                note = ('Go action indexes/build outputs are regenerable caches under S2.2-5. '
                        'Inventoried artifacts do not establish executing code with process rights; '
                        'no confirmed collision follows merely from compiled output. See sample_sources.md.')
            elif n in {42, 57, 60}:
                note = ('Regenerable shader cache, S2.2-5. No evidence that GPU cache code can do '
                        'whatever the host program can do; S2.2-10 is not inferred from compiled bytes.')
            elif n in {37, 53}:
                note = 'Only icon lookup cache is represented; images remain available through slower lookup, S2.2-5.'
            elif n == 48:
                note = ('The four named preference/color files are settings/content, not commands. '
                        'c1 cites S2.2-7/13; c2 cites S2.2-4 for content and absent consumers. '
                        'NOT is supported, though absence alone is not the converse of S2.2-2.')
            elif n == 54:
                note = ('The key supplies tunnel authentication identity; this operation depends on '
                        'it, S2.2-1/2. Protecting the secret is a separate S2.5 design question.')
            elif r['kind'] in {'package:npm', 'python-distribution', 'executable-code-outside-packages'}:
                note = ('Identified module/library/script is executable with its consumer process rights, '
                        'S2.2-10. The row represents code, not its separately inventoried description. '
                        'Native libraries need not be mislabeled interpreters for the rule to apply.')
            elif r['kind'] in {'user-unit-file', 'user-service'}:
                note = ('Unit/service governs independently startable service or scheduled process; '
                        'removal loses that capability, S2.2-1/2. Disabled is not the same as unstartable.')
            elif r['kind'] == 'polkit-actions':
                note = ('Action definition controls authorization across a client and privileged service; '
                        'S2.2-1/2 applies. No extension of S2.2-15 to every right is needed.')
            elif r['kind'] == 'access-rule':
                note = 'PAM session stack governs external account/session operations; S2.2-1/2 applies.'
            elif r['kind'] == 'group':
                note = 'Named input-device group/membership governs system credentials and device access, S2.2-1/2.'
            elif r['kind'] == 'driver':
                note = 'Driver binding supplies device control; removing the binding loses that function, S2.2-1/2.'
            else:
                raise AssertionError((sample, n, r['kind']))
        quoted_exact = ''
        if sample == 'resolved':
            quoted_exact = str(r['adjudication_quote'].replace('**', '') in sentences.values()).lower()
        quotes = ' | '.join(sentences[i] for i in ids.split(','))
        all_results.append([sample, n, seed, r['id'], r['kind'], r['name'],
                            candidate, status, decision, ids, quoted_exact, note, quotes])

with (base / 'sample_audit.tsv').open('w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['sample', 'order', 'seed', 'id', 'kind', 'name', 'candidate',
                     'candidate_verdict', 'review_decision', 'sentence_ids',
                     'original_quote_is_full_sentence', 'reason', 'exact_sentences'])
    writer.writerows(all_results)
print('Reproduced 40/1348 resolved and 60/3202 agreed rows; 100 audit records written.')
