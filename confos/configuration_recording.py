"""Explicit configuration recording; no native commands or applied-state writes.

Recording dispatch precedes read-only query escalation and requires root authority.
"""
import fcntl
import os
from pathlib import Path
import re
import shlex
import tempfile

import recording

LOCK = Path('/run/confos-apply.lock')
TOOLS = {'hostnamectl', 'timedatectl', 'sysctl', 'systemctl', 'useradd', 'usermod', 'userdel',
         'groupadd', 'groupdel', 'modprobe'}


def authority(euid, uid, environment):
    if euid != 0 or uid != 0:
        raise ValueError('permission denied: this account may not change /state/declaration.conf; use an authorized root invocation')
    # Defense in depth: the installed query helper is automatically escalated.
    command = environment.get('SUDO_COMMAND', '')
    if command.split(' ', 1)[0] == '/usr/lib/confos/systemctl-query':
        raise ValueError('read-only query escalation does not authorize recording')


def caller(rows, environment):
    """Resolve user scope only from a consistent declared sudo origin."""
    uid, name = environment.get('SUDO_UID'), environment.get('SUDO_USER')
    if uid is None or name is None or not re.fullmatch('[0-9]+', uid):
        raise ValueError('--user requires an explicit sudo invocation by a declared ordinary account')
    matches = [r for r in rows if r[0] == 'account' and r[1] == name and int(r[2]) == int(uid)]
    if len(matches) != 1 or not 1 <= int(uid) <= 4294967294 or int(uid) == 42:
        raise ValueError('sudo origin does not identify a declared ordinary account')
    if 'SUDO_GID' in environment:
        gid = environment['SUDO_GID']
        if not re.fullmatch('[0-9]+', gid) or int(gid) != int(matches[0][3]):
            raise ValueError('sudo origin group conflicts with the declared account')
    return name


def request(tool, arguments):
    """Return exact requested settings, or a unit state and scope; reject options."""
    args = list(arguments)
    if tool in ('useradd', 'usermod', 'userdel'):
        fields = {}
        options = {'-u': 2, '-g': 3, '-G': 4, '-s': 5, '-d': 6}
        create_home = False
        append_groups = False
        if args[:1] == ['-aG']:
            args[:1] = ['-a', '-G']
        while args and args[0].startswith('-'):
            option = args.pop(0)
            if option == '-a' and tool == 'usermod' and not append_groups:
                append_groups = True
                continue
            if option == '-m' and tool == 'useradd' and not create_home:
                create_home = True
                continue
            if tool == 'userdel' or option not in options or len(args) < 2 or options[option] in fields:
                raise ValueError('unsupported or duplicate account option')
            fields[options[option]] = args.pop(0)
        if len(args) != 1 or not re.fullmatch('[a-z_][a-z0-9_-]*', args[0]):
            raise ValueError('account request needs one exact name after its options')
        if append_groups and 4 not in fields:
            raise ValueError('usermod -a requires -G GROUPS')
        if tool == 'usermod' and not fields:
            raise ValueError('usermod requires an explicit supported field change')
        for index in (2, 3):
            if index in fields and (not re.fullmatch('[0-9]+', fields[index]) or
                    not 0 <= int(fields[index]) <= 4294967294 or
                    (index == 2 and int(fields[index]) in (0, 42))):
                raise ValueError('account recording requires UID 1..4294967294 except 42 and GID 0..4294967294')
        if 4 in fields:
            groups = fields[4].split(',') if fields[4] else []
            if len(groups) != len(set(groups)) or any(not re.fullmatch('[a-z_][a-z0-9_-]*', group) for group in groups):
                raise ValueError('supplementary groups require distinct names; use an empty value for none')
            fields[4] = ','.join(groups) or '-'
        return 'account', (tool, args[0], fields, append_groups)
    if tool in ('groupadd', 'groupdel'):
        gid = None
        if tool == 'groupadd' and len(args) == 3 and args[0] in ('-g', '--gid'):
            gid = args[1]
            args = args[2:]
        if len(args) != 1 or not re.fullmatch('[a-z_][a-z0-9_-]*', args[0]):
            raise ValueError('supported request: groupadd [-g GID] NAME; groupdel NAME')
        if gid is not None and (not re.fullmatch('[0-9]+', gid) or not 1 <= int(gid) <= 4294967294):
            raise ValueError('group recording requires GID 1..4294967294')
        return 'group', (tool, args[0], gid)
    if tool == 'modprobe':
        remove = args[:1] in (['-r'], ['--remove'])
        names = args[1:] if remove else args
        if len(names) != 1 or not re.fullmatch('[a-z0-9][a-z0-9_-]*', names[0]):
            raise ValueError('supported request: modprobe NAME; modprobe -r NAME (no options or module parameters)')
        return 'module', (remove, names[0].replace('-', '_'))
    if tool in ('hostnamectl', 'timedatectl'):
        operation, key = ('set-hostname', 'hostname') if tool == 'hostnamectl' else ('set-timezone', 'timezone')
        if len(args) != 2 or args[0] != operation:
            raise ValueError('supported request: '+operation+' VALUE')
        value = args[1]
        if key == 'hostname' and not re.fullmatch('[A-Za-z0-9][A-Za-z0-9.-]{0,63}', value):
            raise ValueError('unsupported hostname')
        if key == 'timezone' and value not in ('UTC', 'Etc/UTC'):
            raise ValueError('supported timezones: UTC, Etc/UTC')
        return 'settings', {key: value}
    if tool == 'sysctl':
        if len(args) < 2 or args[0] != '-w':
            raise ValueError('supported request: -w KEY=VALUE...')
        settings = {}
        for token in args[1:]:
            key, separator, value = token.partition('=')
            if not separator or not re.fullmatch(r'[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*', key) or not value or any(ord(c) < 32 or ord(c) == 127 for c in value):
                raise ValueError('unsupported sysctl assignment')
            key = 'sysctl:'+key
            if key in settings:
                raise ValueError('duplicate sysctl assignment')
            settings[key] = value
        return 'settings', settings
    if tool == 'systemctl':
        user = False
        if args and args[0] == '--user':
            user = True
            args.pop(0)
        if len(args) < 2 or args[0] not in ('enable', 'disable'):
            raise ValueError('supported request: [--user] enable/disable NAME...')
        operation, *names = args
        pattern = r'[A-Za-z0-9][A-Za-z0-9_.-]*\.(?:service|timer)' if user else r'[A-Za-z0-9_-]+'
        if len(names) != len(set(names)) or any(not re.fullmatch(pattern, name) for name in names):
            raise ValueError('use distinct exact declared unit names; options and aliases are unsupported')
        return 'units', (user, 'enabled' if operation == 'enable' else 'disabled', names)
    raise ValueError('no implemented configuration recording mapping for '+tool)


def spans(line):
    """Shell token spans, so a changed field keeps all surrounding source text."""
    positions = []
    i = 0
    while i < len(line):
        if line[i].isspace():
            i += 1
            continue
        if line[i] == '#':
            break
        start, quote = i, None
        while i < len(line):
            char = line[i]
            if quote is None and (char.isspace() or char == '#'):
                break
            if char == '\\' and quote != "'":
                i += 2
                continue
            if char in ("'", '"'):
                if quote is None:
                    quote = char
                elif quote == char:
                    quote = None
            i += 1
        positions.append((start, i))
    return positions


def validate(rows):
    """Relevant semantic checks that assemble.parse defers until assembly."""
    import assemble
    assemble.declared_hostname(rows)
    assemble.validate_accounts(rows)
    assemble.declared_modules(rows)
    accounts = {r[1]: r for r in rows if r[0] == 'account'}
    # A `group` line may stand anywhere: a tool appends it after the account lines.
    groups = {'root', 'wheel', 'nogroup'} | {row[1] for row in rows if row[0] == 'group'}
    for row in rows:
        if row[0] == 'account':
            groups.add(row[1])
            if row[4] != '-' and any(group not in groups for group in row[4].split(',')):
                raise ValueError('unknown or forward supplementary group reference')
        elif row[0] == 'setting':
            name, value = row[1:]
            if name == 'hostname' or (name == 'timezone' and value in ('UTC', 'Etc/UTC')) or name.startswith('module:'):
                continue
            if not (name.startswith('sysctl:') and re.fullmatch('[A-Za-z0-9_.]+', name[7:]) and '\n' not in value):
                raise ValueError('unsupported setting '+name)
        elif row[0] == 'service':
            if not re.fullmatch('[A-Za-z0-9_-]+', row[1]) or row[2] not in ('enabled', 'disabled') or not row[3].startswith('/'):
                raise ValueError('invalid declared service')
        elif row[0] == 'user-unit':
            if row[1] not in accounts or int(accounts[row[1]][2]) == 0 or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*\.(service|timer)', row[2]) or row[3] not in ('enabled', 'disabled'):
                raise ValueError('invalid declared user-unit')


def account_dependents(rows, account):
    """Declared references only; never inspect home contents or installed users."""
    _, name, uid, gid, _, _, home = account
    dependent = []
    for row in rows:
        if row[0] in ('authorized-key', 'container', 'user-unit', 'linuxgsm') and row[1] == name:
            dependent.append(row[0])
        elif row[0] == 'account' and row[1] != name and name in row[4].split(','):
            dependent.append('supplementary group')
        elif row[0] in ('file', 'compile', 'appimage'):
            if row[1] == home or row[1].startswith(home+'/'):
                dependent.append('home path')
            # assemble.parse places the optional owner last; raw rows put it third.
            if row[0] == 'file' and len(row) == 6:
                owner = row[3] if re.fullmatch('[0-9]+:[0-9]+', row[3]) else row[-1]
                if re.fullmatch('[0-9]+:[0-9]+', owner):
                    owner_uid, owner_gid = owner.split(':')
                    if int(owner_uid) == int(uid) or int(owner_gid) == int(gid):
                        dependent.append('numeric file owner')
    return dependent


def edit_account(original, rows, data):
    operation, name, fields, append_groups = data
    fields = dict(fields)
    if name in ('root', '_apt', 'wheel', 'nogroup'):
        raise ValueError('reserved account name')
    existing = next((row for row in rows if row[:2] == ['account', name]), None)
    if operation == 'useradd':
        if existing is not None:
            defaults = {index: existing[index] for index in range(2, 7)}
        else:
            used = {int(row[index]) for row in rows if row[0] == 'account' for index in (2, 3)}
            uid = 1000
            while uid in used:
                uid += 1
            defaults = {2: str(uid), 3: fields.get(2, str(uid)), 4: '-', 5: '/bin/bash', 6: '/home/'+name}
        fields = defaults | fields
        candidate_row = ['account', name, *[fields[index] for index in range(2, 7)]]
        if existing is not None:
            if existing == candidate_row:
                return original
            raise ValueError('account already exists with different fields')
        if any(row[0] == 'account' and row[6] == candidate_row[6] for row in rows):
            raise ValueError('account home is already declared')
        output = original.decode()
        if output and not output.endswith('\n'):
            output += '\n'
        output += shlex.join(candidate_row)+'\n'
    elif existing is None:
        if operation == 'userdel':
            # Orphan named references cannot make a removal idempotently succeed.
            if any(row[0] in ('authorized-key', 'container', 'user-unit', 'linuxgsm') and row[1] == name or
                   row[0] == 'account' and name in row[4].split(',') for row in rows):
                raise ValueError('account still has declared references')
            return original
        raise ValueError('usermod needs an existing declared account')
    else:
        if append_groups:
            groups = [] if existing[4] == '-' else existing[4].split(',')
            for group in ([] if fields[4] == '-' else fields[4].split(',')):
                if group not in groups:
                    groups.append(group)
            fields[4] = ','.join(groups) or '-'
        changes_identity = any(index in fields and fields[index] != existing[index] for index in (2, 3, 6))
        if (operation == 'userdel' or changes_identity) and account_dependents(rows, existing):
            raise ValueError('account has dependent declaration rows; edit those explicitly first')
        if operation == 'usermod':
            for row in rows:
                if row[0] == 'account' and row[1] != name:
                    if 6 in fields and fields[6] != existing[6] and row[6] == fields[6]:
                        raise ValueError('account home is already declared')
        output = []
        for line in original.decode().splitlines(keepends=True):
            if shlex.split(line, comments=True)[:2] != ['account', name]:
                output.append(line)
                continue
            positions = spans(line)
            if operation == 'userdel':
                # Keep the inline comment as a comment-only line.
                suffix = line[positions[-1][1]:]
                if '#' in suffix:
                    output.append(suffix)
                continue
            for index, value in sorted(fields.items(), reverse=True):
                if value != existing[index]:
                    start, end = positions[index]
                    line = line[:start]+shlex.quote(value)+line[end:]
            output.append(line)
        output = ''.join(output)
    candidate = output.encode()
    validate([row for line in output.splitlines() if (row := shlex.split(line, comments=True))])
    return candidate


def remove_lines(original, identity):
    """Drop every line whose first tokens equal identity; keep an inline comment as its own line."""
    output = []
    for line in original.decode('utf-8').splitlines(keepends=True):
        row = shlex.split(line, comments=True)
        if row[:len(identity)] != list(identity):
            output.append(line)
            continue
        suffix = line[spans(line)[-1][1]:]
        if '#' in suffix:
            output.append(suffix.lstrip())
    return ''.join(output)


def append_line(original, row):
    output = original.decode('utf-8')
    if output and not output.endswith('\n'):
        output += '\n'
    return output+shlex.join(row)+'\n'


def edit_group(original, rows, data):
    """groupadd NAME -> `group NAME GID`; groupdel NAME removes that line."""
    tool, name, gid = data
    if name in ('root', '_apt', 'wheel', 'nogroup'):
        raise ValueError('reserved group name')
    existing = next((row for row in rows if row[:2] == ['group', name]), None)
    if tool == 'groupadd':
        if any(row[:2] == ['account', name] for row in rows):
            raise ValueError('an account line already provides this group name')
        if existing is not None:
            if gid in (None, existing[2]):
                return original
            raise ValueError('group already exists with a different GID')
        if gid is None:
            # Deterministic default, like the account default: the first unused number from 1000.
            used = {int(row[index]) for row in rows if row[0] == 'account' for index in (2, 3)}
            used |= {int(row[2]) for row in rows if row[0] == 'group'}
            number = 1000
            while number in used:
                number += 1
            gid = str(number)
        output = append_line(original, ['group', name, gid])
    else:
        if existing is None:
            if any(row[:2] == ['account', name] for row in rows):
                raise ValueError('this group belongs to an account line; use userdel')
            return original
        if any(row[0] == 'account' and name in row[4].split(',') for row in rows):
            raise ValueError('group is a supplementary group of a declared account; edit that account first')
        output = remove_lines(original, ('group', name))
    validate([row for line in output.splitlines() if (row := shlex.split(line, comments=True))])
    return output.encode('utf-8')


def edit_module(original, rows, data):
    """modprobe NAME -> `setting module:NAME loaded`; modprobe -r NAME removes that line."""
    remove, name = data
    key = 'module:'+name
    existing = [row for row in rows if row[0] == 'setting' and row[1].replace('-', '_') == key]
    if remove:
        if not existing:
            return original
        output = original.decode('utf-8')
        for row in existing:
            output = remove_lines(output.encode('utf-8'), ('setting', row[1]))
    else:
        if existing:
            return original
        # Refuse here what the application would refuse: a name that is no module file
        # of the installed kernel (built-in code and unknown names have no line).
        if not any(path.name.split('.ko')[0].replace('-', '_') == name
                   for path in Path('/usr/lib/modules').rglob('*.ko*')):
            raise ValueError('not a loadable module of the installed kernel: '+name)
        output = append_line(original, ['setting', key, 'loaded'])
    validate([row for line in output.splitlines() if (row := shlex.split(line, comments=True))])
    return output.encode('utf-8')


def edit(original, rows, tool, arguments, environment):
    validate(rows)
    kind, data = request(tool, arguments)
    if kind == 'account':
        return edit_account(original, rows, data)
    if kind == 'group':
        return edit_group(original, rows, data)
    if kind == 'module':
        return edit_module(original, rows, data)
    replacements = {}
    additions = {}
    if kind == 'settings':
        additions = dict(data)
        for row in rows:
            if row[0] == 'setting' and row[1] in data:
                replacements[tuple(row[:2])] = (2, data[row[1]])
                additions.pop(row[1])
    else:
        user, state, names = data
        owner = caller(rows, environment) if user else None
        for name in names:
            identity = ('user-unit', owner, name) if user else ('service', name)
            if not any(tuple(row[:len(identity)]) == identity for row in rows):
                raise ValueError('request needs an existing declaration line: '+name)
            replacements[identity] = (3 if user else 2, state)
    output = []
    for line in original.decode('utf-8').splitlines(keepends=True):
        row = shlex.split(line, comments=True)
        identity = tuple(row[:3] if row and row[0] == 'user-unit' else row[:2])
        if identity in replacements:
            index, value = replacements[identity]
            if row[index] != value:
                start, end = spans(line)[index]
                line = line[:start]+shlex.quote(value)+line[end:]
        output.append(line)
    for name, value in additions.items():
        if output and not output[-1].endswith('\n'):
            output[-1] += '\n'
        output.append(shlex.join(['setting', name, value])+'\n')
    candidate = ''.join(output).encode('utf-8')
    candidate_rows = [shlex.split(line, comments=True) for line in candidate.decode().splitlines()]
    validate([row for row in candidate_rows if row])
    return candidate


def record(tool, arguments):
    """Root-only durable recording, sharing the apply/installer transaction lock."""
    authority(os.geteuid(), os.getuid(), os.environ)
    request(tool, arguments)
    import assemble
    with LOCK.open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        path = recording.DECLARATION
        if path.is_symlink() or not path.is_file():
            raise ValueError('declaration must be a regular primary text file')
        original = path.read_bytes()
        with tempfile.TemporaryDirectory(prefix='confos-config-record-', dir=LOCK.parent) as temporary:
            captured = Path(temporary)/'declaration.conf'
            captured.write_bytes(original)
            rows, _ = assemble.parse(captured)
            candidate = edit(original, rows, tool, arguments, os.environ)
            captured.write_bytes(candidate)
            candidate_rows, _ = assemble.parse(captured)
            validate(candidate_rows)
            recording.commit(path, original, candidate)
