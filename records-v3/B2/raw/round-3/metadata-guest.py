import hashlib,json,pathlib
p=pathlib.Path('/etc/stand/factory')
files=sorted(x for x in p.iterdir() if x.is_file())
info={'factory_generation':hashlib.sha256(b''.join(x.name.encode()+bytes([0])+x.read_bytes() for x in files)).hexdigest(),'factory_lines':len((p/'machine.jsonl').read_text().splitlines()),'base_file_entries':len(json.loads((p/'base-files.json').read_text())),'installed_hashes':{}}
for n in ['stand.py','transactions.py','inventory.py','round3-selftest.py','round3-inventory-test.py']:
 info['installed_hashes'][n]=hashlib.sha256((pathlib.Path('/usr/local/lib/stand')/n).read_bytes()).hexdigest()
print(json.dumps(info,indent=2))
