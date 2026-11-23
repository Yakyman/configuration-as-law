"""Additional evidence only. Original levels and row columns remain unchanged."""
import collections
import importlib
import json
import os
import shlex
from main import PROBE, write_tsv


def diagnostics(ctx):
    """Persist only numerical reductions, so rehearsal inventories can be deleted."""
    counts = collections.Counter({'objects': len(ctx.objects), 'level1': sum(r[2] == 1 for r in ctx.objects),
                                  'level2': sum(r[2] == 2 for r in ctx.objects),
                                  'filesystem_complete': int(ctx.filesystem_complete),
                                  'package_ownership_complete': int(ctx.package_ownership_complete)})
    counts.update(ctx.scan_counts)
    counts['package_files'] = len(ctx.package_files)
    counts['package_integrity_known'] = sum(r['integrity'] != 'unknown' for r in ctx.package_files)
    result = {'counts': dict(counts), 'adapters': getattr(ctx, 's4_summary', {})}
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    (ctx.out/'fact-summary.json').write_text(payload)
    if ctx.args.mode == 'rehearsal':
        ctx.out.with_name(ctx.out.name + '.diagnostics.json').write_text(payload)


def stores(ctx):
    from main import PROBE
    roots = sorted(p for p,r in ctx.entries.items() if r.get('atomic') == 'image-container-store')
    rows, coverage = [], []
    for root in roots:
        data, rc, ev = ctx.query('s4-store-members', PROBE+' scan '+shlex.quote(root)+' expand', 240, max_bytes=268435456)
        records, summary = [], {}
        for line in data.splitlines():
            try: item = json.loads(line)
            except ValueError: continue
            if item.get('path'): records.append(item)
            elif item.get('summary'): summary = item
        complete = rc == 0 and summary.get('complete') is True
        # This is an inner evidence table, not a new set of classified objects.
        ids = [obj[0] for obj in ctx.objects if obj[2] == 2 and obj[4] == root]
        for record in records:
            rows.append([json.dumps(ids), root, record['path'], record.get('type','unknown'),
                         record.get('mode','unknown'), record.get('uid','unknown'),record.get('gid','unknown'),
                         record.get('size','unknown'),record.get('target',''),record.get('signature','unknown'),
                         record.get('persistence','unknown'),record.get('atomic',''),ev])
        opaque = sum(bool(r.get('atomic')) and r['path'] != root for r in records)
        coverage.append([json.dumps(ids),root,rc,int(complete),len(records),opaque,ev])
        ctx.scan_counts['s4:store-roots'] += 1
        ctx.scan_counts['s4:store-traversals-complete'] += int(complete)
        ctx.scan_counts['s4:store-members'] += len(records)
        ctx.scan_counts['s4:store-inner-opaque'] += opaque
    write_tsv(ctx.out/'store-members.tsv', ['object_ids','store','path','type','mode','uid','gid','size','target','prefix_signature','persistence','opaque_kind','evidence'], rows)
    write_tsv(ctx.out/'store-coverage.tsv', ['object_ids','store','query_exit','traversal_complete','members','inner_opaque','evidence'], coverage)


def full_digests(ctx):
    paths = sorted(p for p,r in ctx.entries.items() if r.get('type') == 'file' and not r.get('atomic') and p not in ctx.owned)
    result = ctx.digests([(p,'sha256') for p in paths],1073741824)
    rows=[]
    for path in paths:
        item=result.get((path,'sha256'),{})
        rows.append([path,'sha256',item.get('digest',''),item.get('bytes',''),item.get('status','unknown'),item.get('reason','no-complete-response'),item.get('evidence','')])
    write_tsv(ctx.out/'full-digests.tsv',['path','algorithm','digest','bytes','status','reason','evidence'],rows)
    ctx.scan_counts['s4:full-digest-requested'] += len(paths)
    ctx.scan_counts['s4:full-digest-known'] += sum(row[4]=='ok' for row in rows)
    ctx.scan_counts['s4:active-etc-members'] += sum(p.startswith('/etc/') for p in ctx.entries)


def font_caches(ctx):
    rows=[]
    paths=sorted(p for p,r in ctx.entries.items() if r.get('type')=='file' and
                 (p.startswith(('/var/cache/fontconfig/','/usr/lib/fontconfig/cache/')) or '/.cache/fontconfig/' in p) and '.cache-' in p)
    for path in paths:
        data,rc,ev=ctx.query('s4-fontconfig-cache', 'command -v fc-cat >/dev/null || exit 127; fc-cat -v '+shlex.quote(path),60)
        rows.append([path,rc,ev])
    write_tsv(ctx.out/'font-cache-sources.tsv',['path','query_exit','evidence'],rows)
    # Preserve exact per-file owner identities for sources named by the decoder.
    owned=[[path,json.dumps(sorted(ids))] for path,ids in sorted(ctx.owned.items())
           if '/fonts/' in path or path.endswith(('.otf','.ttf','.ttc','.pcf','.pcf.gz','.pfa','.pfb'))]
    write_tsv(ctx.out/'font-source-packages.tsv',['path','package_ids'],owned)
    ctx.scan_counts['s4:font-cache-decoded']+=sum(r[1]==0 for r in rows)
    ctx.scan_counts['s4:font-cache-requested']+=len(rows)


def index(ctx):
    rows=[]
    members=collections.defaultdict(list)
    for path in ctx.entries:
        if path not in ctx.owned: members[os.path.dirname(path)].append(path)
    for obj in ctx.objects:
        if obj[2] != 2: continue
        facts=json.loads(obj[5]);paths=[obj[4]]
        if isinstance(facts,dict) and facts.get('file'):
            # Use the already collected in-memory records, not a second filesystem query.
            paths += members[obj[4]]
        for path in sorted(set(paths)):
            rows.append([obj[0],path,'full-digests.tsv','path'])
    write_tsv(ctx.out/'object-fact-index.tsv',['object_id','path','fact_file','join_column'],rows)


def collect(ctx):
    full_digests(ctx)
    stores(ctx)
    system=ctx.meta['system']
    if system in ('alma','void','microos'):
        importlib.import_module('extra_'+system).collect(ctx)
    if system=='alma':
        from extra_void import collect_npm
        collect_npm(ctx)
    font_caches(ctx)
    index(ctx)
