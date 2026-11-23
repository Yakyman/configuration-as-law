"""Append manual decisions. Usage: python3 -I c2/scripts/part-2/append_manual.py c2/part-2.manual-N.txt (run from A1/).
Line format: key|decision|sentences|what_it_does|basis|reason ; key = row id, or kind:name.
Rows already present in c2/part-2.tsv are skipped. Checks lengths and vocabulary."""
import csv, os, sys
IN = 'in/part-2.tsv'; OUT = 'c2/part-2.tsv'
rows = [r for r in csv.reader(open(IN, encoding='utf-8'), delimiter='\t')][1:]
byid = {r[0]: r for r in rows}
bykey = {}
for r in rows:
    bykey.setdefault(r[3] + ':' + r[4], []).append(r[0])
done = set()
if os.path.exists(OUT):
    done = {l.split('\t', 1)[0] for l in open(OUT, encoding='utf-8')}
sent_ids = set()
for l in open('../SENTENCES.md', encoding='utf-8'):
    if l.startswith('- **S'):
        sent_ids.add(l.split('**')[1])
out = []; err = 0
for n, line in enumerate(open(sys.argv[1], encoding='utf-8'), 1):
    line = line.rstrip('\n')
    if not line.strip() or line.startswith('#'):
        continue
    f = line.split('|')
    if len(f) != 6:
        print('BAD FIELDS line', n, line[:80]); err += 1; continue
    key, dec, sen, what, basis, reason = [x.strip() for x in f]
    if key in byid:
        rid = key
    else:
        ids = bykey.get(key, [])
        if len(ids) != 1:
            print('KEY?', n, key, ids); err += 1; continue
        rid = ids[0]
    if dec not in ('MUST', 'NOT', 'HOLE', 'UNKNOWN', 'MIXED'):
        print('DEC?', n, dec); err += 1; continue
    for s in sen.split(','):
        if s not in sent_ids:
            print('SENT?', n, s); err += 1
    if len(what.split()) > 15:
        print('WHAT>15', n, rid, len(what.split())); err += 1
    if len(reason.split()) > 30:
        print('REASON>30', n, rid, len(reason.split())); err += 1
    if not (basis in ('evidence', 'none') or basis.startswith('raw:') or basis.startswith('doc:')):
        print('BASIS?', n, basis); err += 1
    if rid in done:
        continue
    out.append('\t'.join([rid, dec, sen, what, basis, reason]))
    done.add(rid)
if err:
    sys.exit('errors: %d (nothing written)' % err)
with open(OUT, 'a', encoding='utf-8') as fh:
    for o in out:
        fh.write(o + '\n')
print('appended', len(out))
