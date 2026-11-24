#!/usr/bin/python3
"""Guest assertion of actual native observations, independent of READY contents."""
import json
import subprocess
import sys

present = sys.argv[1] == 'present'
assert sys.argv[1] in ('present', 'absent')
def query(kind):
    output = subprocess.check_output(['sudo', '-n', 'confos', 'radio-inspect', kind], text=True)
    print(kind, output, flush=True)
    return json.loads(output)

wifi = query('wifi')
assert all(item['exit'] == 0 for item in wifi), wifi
link = wifi[1]['stdout']
assert ('Connected to ' in link) if present else ('Not connected.' in link)
assert 'type AP' in wifi[3]['stdout']
addresses = [address['local'] for interface in json.loads(wifi[2]['stdout'])
             for address in interface['addr_info'] if address['family'] == 'inet']
assert addresses == ([sys.argv[2]] if present else []), addresses
objects = query('bluetooth')
adapters = [ifaces['org.bluez.Adapter1']['Address'] for ifaces in objects.values()
            if 'org.bluez.Adapter1' in ifaces]
assert sorted(adapters) == ['00:AA:01:00:00:00', '00:AA:01:01:00:01']
pairs = [ifaces['org.bluez.Device1'] for ifaces in objects.values()
         if ifaces.get('org.bluez.Device1', {}).get('Paired')]
assert len(pairs) == (2 if present else 0), pairs
files = query('files')
info = [item for item in files if item['path'].startswith('/var/lib/bluetooth/')
        and item['path'].endswith('/info')]
assert len(info) == (2 if present else 0)
for item in info:
    immutable = '/usr/lib/confos/radio/bluez/'+item['path'].removeprefix('/var/lib/bluetooth/')
    expected = subprocess.check_output(['sudo', '-n', 'sha256sum', immutable], text=True).split()[0]
    assert item['sha256'] == expected, item
print('NATIVE RADIO INSPECTION PASS '+sys.argv[1], flush=True)
