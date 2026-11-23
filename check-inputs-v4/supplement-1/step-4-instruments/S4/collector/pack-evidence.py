import pathlib,subprocess,tarfile,json,hashlib
root=pathlib.Path(__file__).resolve().parent.parent
# Copy the syscall trace from the authorized guest before destroying it.
p=subprocess.run([str(root/'lab.sh'),'run','col-debian','--root'],input=b'head -c 1048576 /tmp/c1-tests/trace.log\n',stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
(root/'probe-trace.log').write_bytes(p.stdout)
files=['debian-full','debian-final','rpm-final','rpm-readonly','transport-controls','debian-validation.json','rpm-validation.json','guest-tests.log','guest-tests-v2.log','seed-fixture.log','rpm-readonly.log','transport-tests.log','parser-tests-final.log','probe-trace.log','collector/probe-build.json']
(root/'earlier-run-summary.json').write_text(json.dumps({'debian':json.loads((root/'debian-full-v2/metadata.json').read_text()),'rpm':json.loads((root/'rpm-full/metadata.json').read_text())},indent=2)+'\n');files.append('earlier-run-summary.json')
with tarfile.open(root/'evidence.tar.gz','w:gz') as tf:
 for name in files:tf.add(root/name,arcname=name)
print(hashlib.sha256((root/'evidence.tar.gz').read_bytes()).hexdigest())
