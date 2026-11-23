"""Read saved outputs only; does not inventory the controller."""
import collections,csv,json,pathlib,sys
out=pathlib.Path(sys.argv[1]);read=lambda p:list(csv.DictReader(p.open(),delimiter='\t'))
objects=read(out/'objects.tsv');cov=read(out/'coverage.tsv');files=read(out/'package-files.tsv');meta=json.loads((out/'metadata.json').read_text())
assert meta['duration']<1800;assert meta['filesystem_complete'];assert any(r['level']=='2' for r in objects)
assert all(float(r['duration'])>=0 and int(r['rows'])>=0 for r in cov)
assert all((out/r['stdout']).is_file() and (out/r['stderr']).is_file() for r in cov)
assert not any(r['name'].startswith(('/tmp/c1-collector','/run/c1-collector','/var/tmp/c1-collector')) for r in objects)
member_total=0;groups=0
for row in objects:
 if row['kind'].startswith('stored-'):
  members=json.loads(row['members']);rows=read(out/members['file']);assert len(rows)==members['count'];assert members['complete'];assert len({r['path'] for r in rows})==len(rows)
  assert all(pathlib.PurePosixPath(r['path']).parent==pathlib.PurePosixPath(row['name']) for r in rows)
  assert all(r['signature'] for r in rows);member_total+=len(rows);groups+=1
assert groups>0
for row in objects:
 if row['kind']=='package':assert json.loads(row['members'])['reason'] in ('explicit','dependency','unknown')
assert all(r['integrity'] in ('unchanged','changed','missing','unknown') for r in files)
if 'debian' in out.name:
 package=next(r for r in objects if r['kind']=='package' and r['name']=='dpkg:c1-fixture');assert json.loads(package['members'])['reason']=='explicit'
 f={r['path']:r['integrity'] for r in files if r['package']==package['id']}
 assert f['/usr/share/c1-fixture/unchanged']=='unchanged',f
 assert f['/usr/share/c1-fixture/changed']=='changed' and f['/usr/share/c1-fixture/missing']=='missing',f
 assert f['/etc/c1-fixture.conf']=='changed',f
 group=next(r for r in objects if r['name']=='/home/user/.config/c1-fixture' and r['kind'].startswith('stored-'))
 assert json.loads(group['members'])['count']==1201
 assert any(r['name']=='/home/user/.local/bin/c1-shebang' and r['kind'] in ('executable-code-outside-packages','code-ownership-unresolved') for r in objects)
 config=next(r for r in read(out/'configuration-origin.tsv') if r['path']=='/etc/c1-fixture-generated.conf');assert config['created']=='unknown';assert '.postinst' in config['package_script_mentions']
print(json.dumps({'passed':True,'duration':meta['duration'],'objects':len(objects),'groups':groups,'members':member_total,'package_files':len(files),'integrity':dict(collections.Counter(r['integrity'] for r in files)),'ownership_complete':meta['package_ownership_complete'],'failed_queries':sum(int(r['exit_status'])!=0 for r in cov)}))
