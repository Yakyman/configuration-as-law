#!/usr/bin/env python3
"""Writes cases/derive-radio: a copy of the frozen `derive` that also knows the two radio kinds of
build/DECLARATION.md (revision 40, unchanged in 0.49): `radio-fixture NAME SHA256 RELATIVE_JSON` and
`bluetooth-pair ADAPTER PEER SHA256 RELATIVE_INFO`. Every other kind is byte-identical. Used only for the P1, P2 and
UND rows of X-WIFI and X-BT (order 3, item 4); not part of the frozen set. [x2] It also knows `group NAME GID`
(DECLARATION.md revision 50, from 0.50), for the rows of X-REC-GROUP."""
import pathlib
import sys

here = pathlib.Path(sys.argv[1])
src = (here / 'derive').read_text()

NEW = '''

def kind_radio_fixture(d, line, fdir, f, opts):
    # [radio, outside the frozen set] DECLARATION.md revision 40: “radio-fixture NAME SHA256 RELATIVE_JSON — two
    # hwsim radios/AP and a native btvirt controller pair with fixed identities”
    if not need(d, line, f, 4, 'radio-fixture NAME SHA256 RELATIVE_JSON'):
        return
    _, name, checksum, source = f
    size = check_source(d, line, fdir, source, checksum)
    if size is None:
        return
    d.emit('radio-fixture', name, line, {'name': name, 'sha256': checksum.lower(), 'size': size, 'source': source},
           underived_fields={'path': 'the line does not state where the fixture configuration is placed',
                             'devices': 'the line does not state the names of the simulated radios and controllers'})


def kind_bluetooth_pair(d, line, fdir, f, opts):
    # [radio, outside the frozen set] DECLARATION.md revision 40: “bluetooth-pair ADAPTER PEER SHA256 RELATIVE_INFO —
    # exact native BlueZ bond/key input”
    if not need(d, line, f, 5, 'bluetooth-pair ADAPTER PEER SHA256 RELATIVE_INFO'):
        return
    _, adapter, peer, checksum, source = f
    size = check_source(d, line, fdir, source, checksum)
    if size is None:
        return
    d.emit('bluetooth-pair', f'{adapter}/{peer}', line,
           {'adapter': adapter, 'peer': peer, 'sha256': checksum.lower(), 'size': size, 'source': source},
           underived_fields={'path': 'the line does not state where the bond is stored'})


def kind_group(d, line, fdir, f, opts):
    # [x2, outside the frozen set] DECLARATION.md revision 50: “group NAME GID — From 0.50. A group of its own; GID
    # 1..4294967294, used by no account and no other group; usable in GROUPS of any account line”. Its members follow
    # from the account lines that name it (kind_account: members_include).
    if not need(d, line, f, 3, 'group NAME GID'):
        return
    _, name, gid = f
    if not gid.isdigit() or not 1 <= int(gid) <= 4294967294:
        d.error(line, 'GID must be a number 1..4294967294')
        return
    d.emit('group', name, line, {'name': name, 'gid': int(gid)},
           underived_fields={'password': 'the group line does not state the password field'})
'''

anchor = "\n\nLOCATION = ("
assert src.count(anchor) == 1
src = src.replace(anchor, NEW + anchor, 1)
kinds_anchor = "    'network': kind_network,\n}"
assert src.count(kinds_anchor) == 1
src = src.replace(kinds_anchor, "    'network': kind_network,\n    'radio-fixture': kind_radio_fixture,\n"
                  "    'bluetooth-pair': kind_bluetooth_pair,\n    'group': kind_group,\n}", 1)
out = here / 'derive-radio'
out.write_text(src)
out.chmod(0o755)
print(f'wrote {out}')
