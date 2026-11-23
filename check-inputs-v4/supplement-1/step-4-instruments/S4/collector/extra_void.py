"""Supplement facts only; never changes object membership or assigns decisions."""
import base64
import collections
import gzip
import hashlib
import io
import json
import os
import plistlib
import re
import shlex
import tarfile


def _write(ctx, name, columns, rows):
    from main import write_tsv
    write_tsv(ctx.out / name, columns, rows)


def _ids(ctx, path):
    if not hasattr(ctx, '_s4_id_names'):
        ctx._s4_id_names = collections.defaultdict(list)
        ctx._s4_group_names = collections.defaultdict(list)
        for row in ctx.objects:
            ctx._s4_id_names[row[4]].append(row[0])
            if row[2] == 2: ctx._s4_group_names[row[4]].append(row[0])
    return list(dict.fromkeys(ctx._s4_id_names[path] + ctx._s4_group_names[os.path.dirname(path)]))


def _summary(ctx, name, counts):
    if not hasattr(ctx, 's4_summary'):
        ctx.s4_summary = {}
    ctx.s4_summary[name] = dict(counts)


def _npm_fallback(ctx):
    """Additional references for installs without lockfiles; preserve weaker provenance."""
    installed = sorted(p for p in ctx.entries if '/node_modules/' in p and p.endswith('/package.json') and p not in ctx.owned)
    records = {}
    index = []
    indexes = sorted(p for p,r in ctx.entries.items() if '/.npm/_cacache/index-v5/' in p and r.get('type') == 'file')
    for path,(blob,rc,ev) in ctx.safe_reads(indexes,1048576).items():
        if rc: continue
        for line in blob.splitlines():
            try:
                checksum, encoded = line.split(b'\t',1)
                if hashlib.sha1(encoded).hexdigest().encode() != checksum: continue
                record = json.loads(encoded)
                if isinstance(record,dict) and record.get('integrity'): index.append((record,ev))
            except (ValueError,TypeError): continue
    for path,(blob,rc,ev) in ctx.safe_reads(installed,1048576).items():
        if rc: continue
        try: meta = json.loads(blob)
        except ValueError: continue
        name, version = meta.get('name'), meta.get('version')
        if not isinstance(name,str) or not isinstance(version,str): continue
        reference = None
        if meta.get('_integrity'):
            reference = {'integrity':meta['_integrity'],'resolved':meta.get('_resolved',''),
                         '_s4_provenance':'installed-metadata-reference'}
        else:
            suffix = '/' + name + '/-/' + name.rsplit('/',1)[-1] + '-' + version + '.tgz'
            choices = [(record,ie) for record,ie in index if str(record.get('key','')).endswith(suffix)]
            unique = {record['integrity'] for record,ie in choices}
            if len(unique) == 1:
                record,ie = choices[-1]
                reference = {'integrity':record['integrity'],'resolved':record.get('key',''),
                             '_s4_provenance':'cache-identity-reference-not-install-receipt'}
                ev += ';' + ie
        if reference:
            reference['_s4_identity'] = [name,version]
            records[path] = ({'packages':{'.':reference}}, ev)
    return records


def collect_npm(ctx):
    """Verify lock-addressed cached archives, then full installed member bytes."""
    packages = {}
    sources = []
    pending = []
    roots = [u['home'].rstrip('/') + '/.npm/_cacache/content-v2' for u in ctx.users]
    counts = collections.Counter()
    locks = sorted(p for p in ctx.entries if p.endswith('/package-lock.json') and '/node_modules/' not in p)
    locks += sorted(p for p in ctx.entries if p.endswith('/node_modules/.package-lock.json'))
    seen = set()
    fallback = _npm_fallback(ctx)
    locks += sorted(fallback)
    for lock in locks:
        if lock in fallback:
            data, evidence = fallback[lock]
            blob, rc = json.dumps(data).encode(), 0
        else:
            blob, rc, evidence = ctx.safe_read(lock, 16777216)
        if rc:
            sources.append([lock, '', '', '', '', 'lock-unreadable', evidence]); continue
        try:
            data = json.loads(blob)
        except ValueError:
            sources.append([lock, '', '', '', '', 'lock-invalid', evidence]); continue
        root = os.path.dirname(lock)
        if os.path.basename(lock).startswith('.'):
            root = os.path.dirname(root)
        for relative, record in data.get('packages', {}).items():
            if not relative or not isinstance(record, dict) or record.get('link'):
                continue
            prefix = os.path.normpath(root + '/' + relative)
            if prefix in seen or (prefix not in ctx.entries and prefix + '/package.json' not in ctx.entries):
                continue
            seen.add(prefix)
            sri = record.get('integrity', '')
            expected_archive = None
            for token in sri.split():
                try:
                    alg, value = token.split('-', 1)
                    if alg not in ('sha512', 'sha256', 'sha1'): continue
                    raw = base64.b64decode(value, validate=True)
                    if len(raw) != hashlib.new(alg).digest_size: continue
                    expected_archive = alg, raw
                    break
                except (ValueError, TypeError):
                    continue
            if not expected_archive:
                sources.append([lock, prefix, record.get('resolved', ''), sri, '', 'no-supported-integrity', evidence]); continue
            alg, raw = expected_archive
            h = raw.hex()
            candidates = [p + '/' + alg + '/' + h[:2] + '/' + h[2:4] + '/' + h[4:] for p in roots]
            cache = next((p for p in candidates if p in ctx.entries), None)
            if cache is None:
                sources.append([lock, prefix, record.get('resolved', ''), sri, '', 'cache-absent', evidence]); continue
            archive, ar, ae = ctx.safe_read(cache, 16777216)
            if ar or hashlib.new(alg, archive).digest() != raw:
                sources.append([lock, prefix, record.get('resolved', ''), sri, cache, 'archive-unreadable-or-integrity-mismatch', evidence + ';' + ae]); continue
            identity = record.get('_s4_identity')
            if identity:
                try:
                    with tarfile.open(fileobj=io.BytesIO(archive),mode='r:*') as tf:
                        member = tf.getmember('package/package.json')
                        if not member.isfile() or member.size > 1048576: raise ValueError('metadata bound')
                        package_meta = json.load(tf.extractfile(member))
                        if [package_meta.get('name'), package_meta.get('version')] != identity: raise ValueError('identity mismatch')
                except (ValueError,KeyError,tarfile.TarError,OSError):
                    sources.append([lock,prefix,record.get('resolved',''),sri,cache,'archive-identity-unverified',evidence+';'+ae]);continue
            provenance = record.get('_s4_provenance','lock-receipt-reference')
            sources.append([lock, prefix, record.get('resolved', ''), sri, cache, 'verified-archive:' + provenance, evidence + ';' + ae])
            counts[provenance] += 1
            counts['verified_archives'] += 1
            try:
                with tarfile.open(fileobj=io.BytesIO(archive), mode='r:*') as tf:
                    total = 0
                    for member_number, member in enumerate(tf):
                        if member_number >= 100000: raise ValueError('member-limit')
                        bits = member.name.split('/')
                        if bits[0] != 'package' or '..' in bits or not bits[1:]: continue
                        path = prefix + '/' + '/'.join(bits[1:])
                        if member.isfile():
                            total += member.size
                            if total > 268435456: raise ValueError('expanded-byte-limit')
                            stream = tf.extractfile(member)
                            digest = hashlib.sha256()
                            for chunk in iter(lambda: stream.read(1048576), b''): digest.update(chunk)
                            pending.append((path, digest.hexdigest(), member.size, prefix, ae))
                        elif member.issym():
                            meta = ctx.entries.get(path, {})
                            status = 'equal' if meta.get('type') == 'symlink' and meta.get('target') == member.linkname else 'different-or-absent'
                            packages[path] = [json.dumps(_ids(ctx,path)), prefix, path, 'symlink', member.linkname, meta.get('target',''), status, ae]
            except (ValueError, tarfile.TarError, OSError) as exc:
                sources.append([lock, prefix, '', sri, cache, 'archive-parse-' + type(exc).__name__, ae])
                counts['archive_parse_failures'] += 1
    # Explicit per-file maximum covers entire file or refuses it; never prefix equality.
    answers = ctx.digests([(p, 'sha256') for p, d, n, root, ev in pending], max_bytes=1073741824)
    for path, expected, size, root, ev in pending:
        result = answers.get((path, 'sha256'), {})
        actual = result.get('digest', '')
        status = 'unknown'
        if result.get('status') == 'ok': status = 'equal' if actual == expected else 'different'
        elif result.get('status') == 'missing': status = 'absent'
        packages[path] = [json.dumps(_ids(ctx,path)), root, path, 'sha256', expected, actual, status, ev + ';' + result.get('evidence','')]
    for path, meta in ctx.entries.items():
        matching = [root for root in seen if path.startswith(root + '/') and path not in packages]
        if matching:
            root = max(matching, key=len)
            packages[path] = [json.dumps(_ids(ctx,path)), root, path, '', '', '',
                              'directory' if meta.get('type') == 'directory' else 'not-compared-to-archive', '']
    counts.update(r[6] for r in packages.values())
    _write(ctx, 'npm-archive-sources.tsv', ['lock','package_root','resolved','integrity','cache','status','evidence'], sources)
    _write(ctx, 'npm-member-integrity.tsv', ['object_ids','package_root','path','algorithm','expected','actual','status','evidence'], packages.values())
    _summary(ctx, 'npm', counts)


# Trusted reader source is transmitted to the guest, never loaded from an archive.
ARCHIVE_READER = r"""
import ctypes as C, sys
a=C.CDLL('libarchive.so.13')
a.archive_read_new.restype=C.c_void_p
a.archive_read_support_filter_all.argtypes=[C.c_void_p]
a.archive_read_support_format_tar.argtypes=[C.c_void_p]
a.archive_read_open_filename.argtypes=[C.c_void_p,C.c_char_p,C.c_size_t]
a.archive_read_next_header.argtypes=[C.c_void_p,C.POINTER(C.c_void_p)]
a.archive_entry_pathname.argtypes=[C.c_void_p]; a.archive_entry_pathname.restype=C.c_char_p
a.archive_read_data.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t];a.archive_read_data.restype=C.c_ssize_t
a.archive_read_free.argtypes=[C.c_void_p]
a.archive_error_string.argtypes=[C.c_void_p];a.archive_error_string.restype=C.c_char_p
h=a.archive_read_new()
try:
 a.archive_read_support_filter_all(h);a.archive_read_support_format_tar(h)
 if a.archive_read_open_filename(h,sys.argv[1].encode(),65536)!=0:raise RuntimeError(a.archive_error_string(h))
 entry=C.c_void_p();found=False
 for index in range(100000):
  status=a.archive_read_next_header(h,C.byref(entry))
  if status==1:break
  if status<0:raise RuntimeError(a.archive_error_string(h))
  name=a.archive_entry_pathname(entry)
  if name not in (b'files.plist',b'./files.plist'):continue
  chunks=[];total=0;buffer=C.create_string_buffer(65536)
  while True:
   size=a.archive_read_data(h,buffer,len(buffer))
   if size<0:raise RuntimeError(a.archive_error_string(h))
   if size==0:break
   total+=size
   if total>16777216:raise RuntimeError('metadata size cap')
   chunks.append(buffer.raw[:size])
  sys.stdout.buffer.write(b''.join(chunks));found=True;break
 if not found:raise RuntimeError('manifest not present within header bound')
finally:a.archive_read_free(h)
"""


def collect(ctx):
    """Record all surviving kernel receipt routes without fetching/reinstalling."""
    collect_npm(ctx)
    paths = sorted(p for p in ctx.entries if p.startswith('/var/db/xbps/.linux') and p.endswith('.plist'))
    archives = sorted(p for p in ctx.entries if p.startswith('/var/cache/xbps/') and p.endswith('.xbps') and '/linux' in p)
    receipts = []
    candidates = []
    counts = collections.Counter()
    for path in paths:
        blob, rc, ev = ctx.safe_read(path, 16777216)
        if rc:
            receipts.append([path, 'unreadable', ev]); continue
        try:
            if blob.startswith(b'\x1f\x8b'):
                with gzip.GzipFile(fileobj=io.BytesIO(blob)) as stream: blob = stream.read(67108865)
            if len(blob) > 67108864: raise ValueError('metadata-limit')
            obj = plistlib.loads(blob)
        except Exception:
            receipts.append([path, 'not-readable-plist', ev]); continue
        receipts.append([path, 'read', ev])
        if isinstance(obj,dict): candidates.append((path,obj,ev))
    for archive in archives:
        # tar reads data only; no archive pathname is extracted to disk.
        script = 'python3 - ' + shlex.quote(archive) + " <<'S4_ARCHIVE_READER'\n" + ARCHIVE_READER + '\nS4_ARCHIVE_READER\n'
        blob, rc, ev = ctx.query('s4-old-kernel-cache-manifest', script, timeout=90, max_bytes=67108864)
        if rc:
            receipts.append([archive, 'manifest-unreadable', ev]); continue
        try: obj = plistlib.loads(blob)
        except Exception:
            receipts.append([archive,'manifest-invalid',ev]); continue
        receipts.append([archive,'read',ev])
        if isinstance(obj,dict): candidates.append((archive,obj,ev))
    manifest = []
    for source, obj, ev in candidates:
        for kind in ('files','conf_files','links','dirs'):
            for item in obj.get(kind,[]):
                if not isinstance(item,dict): continue
                path = item.get('file','')
                if not path.startswith(('/usr/lib/modules/','/lib/modules/','/boot/')): continue
                from main import canonical
                manifest.append((source,canonical(ctx,path),kind,item.get('sha256',''),item.get('target',''),ev))
    jobs = [(p,'sha256') for s,p,k,d,t,e in manifest if re.fullmatch('[a-fA-F0-9]{64}',str(d))]
    answers = ctx.digests(jobs,max_bytes=1073741824)
    rows = []
    for source,path,kind,expected,target,ev in manifest:
        current = answers.get((path,'sha256'),{})
        actual = current.get('digest','')
        status = 'unknown'
        if kind == 'dirs': status = 'directory-receipt'
        elif kind == 'links':
            meta = ctx.entries.get(path,{})
            status = 'equal' if meta.get('type')=='symlink' and meta.get('target')==target else 'different-or-absent'
            actual = meta.get('target',''); expected = target
        elif current.get('status') == 'ok': status = 'equal' if actual==expected else 'different'
        elif current.get('status') == 'missing': status = 'absent'
        rows.append([json.dumps(_ids(ctx,path)),path,source,kind,expected,actual,status,ev+';'+current.get('evidence','')])
        counts[status] += 1
        if path not in ctx.owned: counts['unowned-with-receipt-' + status] += 1
    covered = {r[1] for r in rows}
    for path in sorted(ctx.entries):
        if path.startswith(('/usr/lib/modules/','/lib/modules/','/boot/')) and path not in covered:
            rows.append([json.dumps(_ids(ctx,path)),path,'','', '', '', 'no-surviving-receipt',''])
            counts['no-surviving-receipt'] += 1
    _write(ctx,'old-package-receipt-sources.tsv',['source','status','evidence'],receipts)
    _write(ctx,'old-package-member-integrity.tsv',['object_ids','path','source','type','expected','actual','status','evidence'],rows)
    _summary(ctx,'old-package',counts)

    configs = sorted(p for p,r in ctx.entries.items() if r.get('type') == 'file' and
                     p.startswith(('/etc/default/','/etc/modules-load.d/','/etc/sudoers.d/','/var/db/xbps/keys/')))
    contents = []
    for path,(blob,rc,ev) in ctx.safe_reads(configs,1048576).items():
        contents.append([json.dumps(_ids(ctx,path)),path,'ok' if rc==0 else 'unreadable',
                         base64.b64encode(blob).decode() if rc==0 else '',
                         'unknown: no creation event established by current file',ev])
    _write(ctx,'void-configuration-facts.tsv',['object_ids','path','status','content_base64','historical_creator','evidence'],contents)
