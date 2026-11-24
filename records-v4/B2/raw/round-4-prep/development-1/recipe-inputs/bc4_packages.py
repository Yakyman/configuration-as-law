"""Atomic multi-row package artifacts using the existing declaration row types.

An artifact contains an exact registered package row and exact contributed rows.
The package records their IDs; all content still passes the ordinary admission,
activation and readback path. No account identifier is allocated or defaulted.
"""
import json
import pathlib
import shutil
import tempfile

FORMAT = 'stand-package-bundle-v1'
FIELD = 'package_contribution_ids'


def validate_declaration(rows):
    by_id = {r['id']: r for r in rows}
    for package in rows:
        if FIELD not in package:
            continue
        ids = package[FIELD]
        if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
            raise ValueError('package contributions require a list of line IDs')
        if any(i not in by_id for i in ids):
            raise ValueError('package contribution line missing')
        validate_artifact(dict(format=FORMAT, package=package, rows=[by_id[i] for i in ids]))


def validate_artifact(artifact):
    if set(artifact) != {'format', 'package', 'rows'} or artifact['format'] != FORMAT:
        raise ValueError('invalid exact package bundle')
    package = artifact['package']
    rows = artifact['rows']
    if not isinstance(package, dict) or not isinstance(rows, list):
        raise ValueError('package object and contribution list required')
    identity = package.get('package_identity', {})
    if package.get('type') not in ('program', 'code') or package.get('managed') is not True or identity.get('backend') != 'stand':
        raise ValueError('managed exact stand package required')
    ids = [r['id'] for r in rows]
    if not rows or len(set(ids)) != len(ids) or package['id'] in ids or package.get(FIELD) != ids:
        raise ValueError('exact unique contribution IDs required')
    if any(not r.get('managed') or FIELD in r for r in rows):
        raise ValueError('managed non-nested contributions required')
    return [package] + rows


def dispatch(name, args):
    import stand
    if name not in ('stand-pkg', 'apt', 'apt-get') or len(args) != 2:
        return None
    operation, value = args
    if operation in ('install', 'update'):
        path = pathlib.Path(value)
        if not path.is_file():
            return None
        artifact = json.loads(path.read_text())
        if not isinstance(artifact, dict) or artifact.get('format') != FORMAT:
            return None
        adds = validate_artifact(artifact)
        with stand.transaction():
            current = stand.load(stand.current_dir())
            old = next((r for r in current if r['id'] == adds[0]['id']), None)
            if old and old.get(FIELD) != adds[0][FIELD]:
                raise ValueError('bundle update requires identical contribution IDs')
            owners = {r['id']: r for r in current}
            for r in adds:
                existing = owners.get(r['id'])
                if existing and not old:
                    raise ValueError('bundle cannot adopt existing declaration lines')
                if existing and not existing.get('managed'):
                    raise ValueError('bundle cannot replace factory declaration lines')
            return stand.candidate_edit_unlocked(adds=adds)
    if operation != 'remove':
        return None
    with stand.transaction():
        directory = stand.current_dir()
        rows = stand.load(directory)
        package = next((r for r in rows if r['id'] == value), None)
        if package is None or FIELD not in package:
            return None
        if not package.get('managed'):
            raise ValueError('factory package removal unsupported')
        removed = set(package[FIELD]) | {package['id']}
        # A contribution shared by another exact bundle remains recorded.
        retained = {i for r in rows if r['id'] != value for i in r.get(FIELD, [])}
        removed -= retained
        with tempfile.TemporaryDirectory(prefix='package-remove-', dir=stand.ROOT) as temporary:
            for source in directory.iterdir():
                shutil.copyfile(source, pathlib.Path(temporary) / source.name)
            stand.atomic(pathlib.Path(temporary) / 'machine.jsonl', ''.join(
                stand.canonical(r) + '\n' for r in rows if r['id'] not in removed))
            return stand.apply(temporary)
