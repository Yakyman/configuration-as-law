"""Private36 assembly adapter. Draft for later numbered-release review."""
import shlex
from pathlib import Path
import radio_declaration

KINDS={'radio-fixture','network','bluetooth-pair'}
EXTRA={'iputils-ping':'3:20240905-3','python3-dbus':'1.4.0-1','python3-gi':'3.50.0-4+b1'}

def install(root,rows,declaration):
    radio_rows=[row for row in rows if row[0] in KINDS]
    result=radio_declaration.derive('\n'.join(shlex.join(row) for row in radio_rows),declaration.parent)
    packages={}
    for paragraph in (root/'var/lib/dpkg/status').read_text().split('\n\n'):
        fields=dict(line.split(': ',1) for line in paragraph.splitlines() if ': ' in line and not line.startswith(' '))
        if 'Package' in fields: packages[fields['Package']]=fields.get('Version')
    required=dict(result['required_packages'])
    if result['plan']['network']: required['iputils-ping']=EXTRA['iputils-ping']
    if result['plan']['fixture'] and result['plan']['fixture']['bluetooth']:
        required.update({k:EXTRA[k] for k in ('python3-dbus','python3-gi')})
    for name,version in required.items():
        if packages.get(name)!=version: raise ValueError('radio requires exact resolved package '+name+'='+version)
    for path,entry in result['files'].items():
        target=root/path.lstrip('/')
        if target.exists() or target.is_symlink(): raise ValueError('radio output ownership conflict: '+path)
        for parent in target.parents:
            if parent==root: break
            if parent.is_symlink(): raise ValueError('radio output ancestor is a symlink')
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(entry['data']);target.chmod(entry['mode'])
