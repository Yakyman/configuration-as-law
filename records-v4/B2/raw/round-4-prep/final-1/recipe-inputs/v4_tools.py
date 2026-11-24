"""Typed configuration adapters. All writes use the common declaration transaction."""
import json
import pathlib

KINDS = {
    'useradd': {'account'}, 'usermod': {'account'}, 'userdel': {'account'},
    'groupadd': {'group'}, 'groupdel': {'group'},
    'systemctl': {'service', 'timer', 'socket'},
    'systemd-run': {'service', 'timer'}, 'crontab': {'timer'}, 'at': {'timer'},
    'nft': {'rule'}, 'nmcli': {'wifi'}, 'bluetoothctl': {'bluetooth'},
}

def dispatch(name, args):
    import stand
    import bc4_packages
    result = bc4_packages.dispatch(name, args)
    if result is not None:
        return result
    if name not in KINDS or len(args) != 2 or args[0] not in ('add', 'remove'):
        return None
    operation, value = args
    rows = stand.load(stand.current_dir())
    if operation == 'add':
        row = json.loads(pathlib.Path(value).read_text())
        # The older crontab command accepts a schedule specification and emits
        # a service plus timer. Keep that documented API intact.
        if name == 'crontab' and isinstance(row, dict) and 'type' not in row:
            return None
        if not isinstance(row, dict) or row.get('type') not in KINDS[name] or row.get('managed') is not True:
            raise ValueError('REFUSED managed row of the tool kind required')
        if name in ('userdel', 'groupdel'):
            raise ValueError('REFUSED deletion tool accepts remove only')
        current = next((r for r in rows if r['id'] == row.get('id')), None)
        if current and (current['type'] not in KINDS[name] or not current.get('managed')):
            raise ValueError('REFUSED incompatible replacement')
        return stand.candidate_edit(add=row)
    current = next((r for r in rows if r['id'] == value), None)
    if current is None or current['type'] not in KINDS[name] or not current.get('managed'):
        raise ValueError('REFUSED existing managed row of the tool kind required')
    return stand.candidate_edit(remove=value)
