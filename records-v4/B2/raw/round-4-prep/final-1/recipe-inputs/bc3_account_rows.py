"""Prospective account settings from caller-supplied bytes; never reads live state.

The caller supplies the complete candidate database snapshot before publication.
Rows belong to the filesystem's primary declaration, not stand.py's finite API.
No row here grants permission to publish or replaces a successful transaction.
"""
import base64
import hashlib

DATABASES = ('/etc/passwd', '/etc/group', '/etc/shadow', '/etc/gshadow',
             '/etc/subuid', '/etc/subgid')


def _entries(data, fields, path):
    """Preserve exact bytes separately; expose valid local semantic entries."""
    entries = []
    for number, line in enumerate(data.decode('utf-8', 'surrogateescape').splitlines(), 1):
        if not line or line.startswith('#'):
            continue
        values = line.split(':')
        # Compatibility/NIS records are explicitly represented by exact DB rows.
        if line.startswith(('+', '-')):
            continue
        if len(values) != fields:
            raise ValueError(f'{path}: malformed prospective line {number}')
        entries.append(values)
    return entries


def account_rows(snapshot):
    """Return deterministic own-line settings, including exact database contents.

    snapshot maps all present DATABASES paths to bytes. passwd and group are
    required, even if empty. Numeric groups are authoritative: native tools may
    publish passwd and group in separate renames. Missing primary-group names
    must not silently suppress an account row or invent a group.
    """
    if '/etc/passwd' not in snapshot or '/etc/group' not in snapshot:
        raise ValueError('complete prospective passwd/group snapshot required')
    for path, data in snapshot.items():
        if path not in DATABASES:
            raise ValueError('unexpected account database path')
        if not isinstance(data, bytes):
            raise TypeError('prospective database contents must be bytes')
    rows = []
    groups = []
    names = set()
    for name, password, gid, members in _entries(snapshot['/etc/group'], 4, '/etc/group'):
        if name in names:
            raise ValueError('duplicate prospective group name')
        names.add(name)
        numeric_gid = int(gid)
        if numeric_gid < 0:
            raise ValueError('negative prospective gid')
        member_names = sorted(set(members.split(','))) if members else []
        groups.append((name, numeric_gid, member_names))
        rows.append({'id': 'bc3:group:' + name, 'type': 'group',
                     'name': name, 'gid': numeric_gid, 'members': member_names,
                     'source': '/etc/group', 'recording': 'own'})
    names = set()
    for name, password, uid, gid, gecos, home, shell in _entries(snapshot['/etc/passwd'], 7, '/etc/passwd'):
        if name in names:
            raise ValueError('duplicate prospective account name')
        names.add(name)
        numeric_uid, numeric_gid = int(uid), int(gid)
        if numeric_uid < 0 or numeric_gid < 0:
            raise ValueError('negative prospective account identifier')
        memberships = sorted({g for _, g, members in groups if name in members} | {numeric_gid})
        group_names = sorted({gname for gname, g, members in groups
                              if g == numeric_gid or name in members})
        rows.append({'id': 'bc3:account:' + name, 'type': 'account',
                     'name': name, 'uid': numeric_uid, 'gid': numeric_gid,
                     'group_ids': memberships, 'groups': group_names,
                     'home': home, 'shell': shell, 'gecos': gecos,
                     'source': '/etc/passwd', 'recording': 'own'})
    rows.extend(database_rows(snapshot))
    return sorted(rows, key=lambda row: row['id'])


def database_rows(snapshot):
    """Exact own-line settings even when privileged breaking makes parsing fail.

    This helper does not validate semantic account syntax or block direct edits.
    Credentials require a declaration readable only by authorized principals.
    """
    rows = []
    for path in DATABASES:
        if path in snapshot:
            data = snapshot[path]
            if not isinstance(data, bytes):
                raise TypeError('prospective database contents must be bytes')
            rows.append({'id': 'bc3:account-database:' + path.rsplit('/', 1)[1],
                         'type': 'setting', 'path': path, 'recording': 'own',
                         'encoding': 'base64',
                         'value': base64.b64encode(data).decode('ascii'),
                         'sha256': hashlib.sha256(data).hexdigest()})
    return rows
