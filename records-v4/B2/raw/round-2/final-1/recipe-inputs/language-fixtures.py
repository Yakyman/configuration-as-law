#!/usr/bin/python3
"""Fetch fixed upstream development artifacts on the build server only."""
import base64,hashlib,json,pathlib,sys,urllib.request
P=pathlib.Path(sys.argv[1]);P.mkdir(parents=True,exist_ok=True)
def fetch(url):
    with urllib.request.urlopen(url,timeout=60) as r:return r.read()
ARTIFACTS={
 ('pip','python-dateutil','2.9.0.post0'):('https://files.pythonhosted.org/packages/ec/57/56b9bcc3c9c6a792fcbaf139543cee77261f3651ca9da0c93f5c1221264b/python_dateutil-2.9.0.post0-py2.py3-none-any.whl','a8b2bc7bffae282281c8140a97d3aa9c14da0b136dfe83f850eea9a5f7470427',None),
 ('pip','six','1.17.0'):('https://files.pythonhosted.org/packages/b7/ce/149a00dd41f10bc29e5921b496af8b574d8413afcd5e30dfa0ed46c2cc5e/six-1.17.0-py2.py3-none-any.whl','4721f391ed90541fddacab5acf947aa0d3dc7d27b2e1e8eda2be8970586c3274',None),
 ('npm','is-odd','3.0.1'):('https://registry.npmjs.org/is-odd/-/is-odd-3.0.1.tgz','13c23b3f1f3a5c146b8906e23c8e674f8e4a6ff44b77720e1d4bddb7b2caf312','090a6758fac3c263f5f923075d986d2ed26ff74ca2c957e5b86b17e62342564ae142d5374d01ec5163c6f7091d93d2e0779c8da4083d8d0128f7408169781630'),
 ('npm','is-number','6.0.0'):('https://registry.npmjs.org/is-number/-/is-number-6.0.0.tgz','62589f25115042c4d34863bc8e6ab4790a8920b811949c30e0ebc5733aca66cb','5aed551de20b04af0a016254022499417f781a6384e39460ebfe77f1f2b08a5a14bb6d4a9dc1246063eaa1bda8499e66513ef7bcb1ab1d08cac3728c3f07c3ce')}
def package(channel,n,v,deps):
    url,wanted,wanted512=ARTIFACTS[(channel,n,v)]
    filename=n+'-'+v+('.whl' if channel=='pip' else '.tgz');target=P/filename
    data=target.read_bytes() if target.exists() else fetch(url)
    if hashlib.sha256(data).hexdigest()!=wanted:raise ValueError('pinned artifact SHA256 mismatch')
    if wanted512 and hashlib.sha512(data).hexdigest()!=wanted512:raise ValueError('pinned artifact SHA512 mismatch')
    if not target.exists():target.write_bytes(data)
    return dict(name=n,version=v,source=url,sha256=wanted,archive=filename,dependencies=deps)
for channel,spec,code in [('pip',[('python-dateutil','2.9.0.post0',['six']),('six','1.17.0',[])],"from dateutil.parser import parse\nprint('PIP_POSITIVE '+str(parse('2026-11-22').year))\n"),('npm',[('is-odd','3.0.1',['is-number']),('is-number','6.0.0',[])],"console.log('NPM_POSITIVE '+require('is-odd')(3));\n")]:
    lock=dict(schema=1,channel=channel,project='development',packages=[package(channel,*s) for s in spec],entry_code=code,entry_sha256=hashlib.sha256(code.encode()).hexdigest())
    path=P/(channel+'.lock.json');content=json.dumps(lock,sort_keys=True)+'\n'
    if path.exists():
        if path.read_text()!=content:raise ValueError('cached lock differs from pinned recipe')
    else:path.write_text(content)
print('LANGUAGE_FIXTURES_READY')
