# SPDX-License-Identifier: MIT
"""Fixture tests of the native 0.70 binding. No virtual machine, no network, no system run."""
import importlib.machinery, json, os, shlex, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import adapter_native as N
from adapter import Unavailable
from core import derive, evaluate_query
import core

# The release tree is optional: tests that need it skip without it.
TREE = Path(os.environ.get('CONFOS_RELEASE_TREE', HERE.parent / 'build'))
# Only a tree of the bound release counts (the builder's working tree moves on).
if not (TREE / 'declarations/base.conf').is_file() or 'base 0.70' not in (TREE / 'declarations/base.conf').read_text():
    TREE = HERE / 'no-release-tree'
# Private copies of the update-state trees and the source archive (read now: loading the
# release's own confos program below replaces the environment of this process).
UPDATE_TREES = {st: os.environ.get('CONFOS_TREE_' + st) for st in ('T1', 'T2')}
UPDATE_SOURCES = os.environ.get('CONFOS_SOURCES')
PRIVATE = {'@SERVER@': 'http://10.0.2.2:8000', '@KEY_TYPE@': 'ssh-ed25519', '@KEY@': 'AAAAC3NzaC1lZDI1NTE5AAAAIFAKEFAKEFAKE'}


def bindings():
    return N.Bindings(PRIVATE, HERE)


class FakeGuest:
    """Replies by exact command text; records every call. Unknown commands are errors."""
    def __init__(self, replies):
        self.replies, self.calls = replies, []
    def run(self, role, text, stdin=None, timeout=120, env=None, tty=False):
        self.calls.append((role, text, stdin))
        for pattern, reply in self.replies:
            if pattern(role, text):
                r = reply(role, text, stdin) if callable(reply) else dict(reply)
                return dict({'command': text, 'role': role, 'stdout': '', 'stderr': '', 'returncode': 0}, **r)
        raise AssertionError('unexpected guest command: %s %r' % (role, text[:120]))


class Render(unittest.TestCase):
    def test_d_test_renders_every_slot(self):
        b = bindings()
        decl = b.render(json.loads((HERE / 'declarations/D-test.json').read_text()))
        lines = decl.lines()
        self.assertEqual(lines[0], 'base 0.70')
        self.assertIn('open /home/user/control', lines)
        self.assertIn('package case-probe 1 case-probe-1.recipe', lines)
        self.assertIn('setting hostname case-test', lines)
        self.assertTrue(any(l.startswith('authorized-key root ssh-ed25519 ') for l in lines))
        self.assertTrue(any(l.startswith('file /home/user/bin/cases-report.sh 0755 1000:1000 ') for l in lines))
        for rel in ('case-probe-1.recipe', 'case-probe.c', 'case-small-1.recipe', 'case-small.c', 'case-rule.sudoers', 'files/script'):
            self.assertIn(rel, decl.inputs)
        self.assertNotIn('@', decl.files[N.MAIN].decode().replace('@SERVER', ''))

    def test_unsupported_slot_and_token_are_unavailable(self):
        b = bindings()
        for name in ('D-latest', 'D-radio', 'D-external-accounts', 'D-shared'):
            with self.assertRaises(Unavailable):
                b.render(json.loads((HERE / ('declarations/%s.json' % name)).read_text()))
        with self.assertRaises(Unavailable):
            b.expand('@SERVICE_TOOL@ enable x')
        with self.assertRaises(Unavailable):
            b.expand('@NO_SUCH_TOKEN@')
        with self.assertRaises(Unavailable):
            N.Bindings({}, HERE).expand('@KEY@')

    def test_order_items_reverse_line_order(self):
        b = bindings()
        d = json.loads((HERE / 'declarations/D-accounts-open.json').read_text())
        ab, ba = b.render(d, ['a', 'b']).lines(), b.render(d, ['b', 'a']).lines()
        la, lb = (b.expand('account case-%s auto auto - /bin/bash @HOME_ROOT@/case-%s' % (x, x))[0] for x in 'ab')
        self.assertLess(ab.index(la), ab.index(lb))
        self.assertGreater(ba.index(la), ba.index(lb))
        self.assertTrue(la.endswith('/case-a'))

    def test_prelude_is_typed_text(self):
        text = bindings().shell('@FETCH@ @PAYLOAD_URL@ @HOME@/brought')
        self.assertTrue(text.startswith('case_fetch() { curl -fsSL -o "$2" -- "$1"; }; case_fetch '))
        self.assertIn('http://10.0.2.2:8000/payload /home/user/brought', text)

    def test_variant_tables(self):
        b = bindings()
        with self.assertRaises(Unavailable):
            b.variant('G-SERVICE', 'at')
        with self.assertRaises(Unavailable):
            b.variant('G-RIGHTS', 'direct root write is W5-BREAK')
        v = b.variant('G-SCRIPT', 'shell filename')
        self.assertEqual(v['steps']['attempt']['command'], 'bash @TARGET@/case-input')
        self.assertEqual(b.variant('G-SHELL', None), {})


class Identity(unittest.TestCase):
    def test_one_and_several_files(self):
        one = N.NativeDecl({N.MAIN: b'base 0.70\n'})
        self.assertEqual(one.identity, N.sha(b'base 0.70\n'))
        two = N.NativeDecl({N.MAIN: b'base 0.70\ninclude p.conf\n', 'p.conf': b'package bash 5.3\n'})
        want = N.hashlib.sha256((N.MAIN + '\0' + N.sha(b'base 0.70\ninclude p.conf\n') + '\n' +
                                 'p.conf\0' + N.sha(b'package bash 5.3\n') + '\n').encode()).hexdigest()
        self.assertEqual(two.identity, want)
        self.assertEqual(two.order, [N.MAIN, 'p.conf'])
        with self.assertRaises(ValueError):
            N.NativeDecl({N.MAIN: b'base 0.70 a b c\n'})
        with self.assertRaises(ValueError):
            N.NativeDecl({N.MAIN: b'include ../x.conf\n'})

    def test_identity_agrees_with_release_parser(self):
        src = TREE / 'files/confos/confos'
        if not src.is_file():
            self.skipTest('release tree not beside the set')
        loader = importlib.machinery.SourceFileLoader('release_confos', str(src))
        mod = loader.load_module()
        b = bindings()
        decl = b.render(json.loads((HERE / 'declarations/D-test.json').read_text()))
        split = N.NativeDecl({N.MAIN: b'base 0.70\ninclude programs.conf\n' + b'\n'.join(
            l.encode() for l in decl.lines() if not l.startswith(('package', 'base'))) + b'\n',
            'programs.conf': b'\n'.join(l.encode() for l in decl.lines() if l.startswith('package')) + b'\n'}, decl.inputs)
        for d in (decl, split):
            with tempfile.TemporaryDirectory() as t:
                for rel, data in {**d.files, **d.inputs}.items():
                    p = Path(t) / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
                theirs = mod.Declaration(Path(t) / N.MAIN, tree=str(TREE))
                self.assertEqual(theirs.identity, d.identity)
                self.assertEqual([canon for canon in d.lines()], [N.canon(r) for _, _, r in theirs.rows])


class Semantic(unittest.TestCase):
    def test_semantic_objects_and_derive(self):
        b = bindings()
        decl = b.render(json.loads((HERE / 'declarations/D-test.json').read_text()))
        if not (TREE / 'recipes').is_dir():
            self.skipTest('release tree not available')
        sem = N.semantic_from_native(decl, TREE, {}, b.release['layout'], b.release['derivation'])
        kinds = {(l['object']['kind'], l['object']['id']) for l in sem['lines'] if l['kind'] == 'object'}
        self.assertIn(('account', 'user'), kinds)
        self.assertIn(('hostname', 'hostname'), kinds)
        self.assertIn(('file', '/home/user/.bashrc'), kinds)
        self.assertIn(('dir', '/home/user'), kinds)
        self.assertIn(('dir', '/data/home/user'), kinds)
        self.assertIn(('access', '/etc/sudoers.d/case-rule'), kinds)
        self.assertIn(('account', 'root'), kinds)
        pk = [l for l in sem['lines'] if l['kind'] == 'package']
        self.assertEqual(len(pk), 64)
        self.assertTrue(all('/etc/passwd' in l['overlay'] for l in pk))
        out = derive(sem, None)
        self.assertTrue(any('package reader unavailable' in e['reason'] for e in out['errors']))

    def test_overlay_reader_keeps_presence_only(self):
        r = N.overlay_reader(lambda line: [{'kind': 'file', 'id': '/etc/network.conf', 'value': {'sha256': 'x'}},
                                           {'kind': 'file', 'id': '/usr/bin/a', 'value': {'sha256': 'y'}}], [])
        got = r({'overlay': ['/etc/network.conf']})
        self.assertEqual(got[0]['value'], {})
        self.assertEqual(got[1]['value'], {'sha256': 'y'})

    def test_missing_recipe_is_underived(self):
        sem = N.semantic_from_native(N.NativeDecl({N.MAIN: b'base 0.70\npackage nothing 1\n'}), None, {})
        self.assertEqual(derive(sem, None)['errors'][0]['line'], N.MAIN + ':2')


def guest_with_candidate(files):
    """A fake guest that keeps the candidate folder: tar in, sha256sum and tar out."""
    import tarfile, io
    store = dict(files)
    def write(role, text, stdin):
        path = shlex.split(text.split('&&')[-1])[-1]
        store[path] = stdin
        return {}
    def untar(role, text, stdin):
        with tarfile.open(fileobj=io.BytesIO(stdin), mode='r:') as t:
            for m in t:
                if m.isreg():
                    store[N.CANDIDATE_DIR + '/' + m.name] = t.extractfile(m).read()
        return {}
    def names(text):
        return shlex.split(text.split('--', 1)[1].split('|')[0])
    def sums(role, text, stdin):
        return {'stdout': ''.join(N.sha(store[N.CANDIDATE_DIR + '/' + n]) + '  ' + n + '\n'
                                  for n in names(text) if N.CANDIDATE_DIR + '/' + n in store)}
    def tarout(role, text, stdin):
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode='w') as t:
            for n in names(text):
                data = store.get(N.CANDIDATE_DIR + '/' + n)
                if data is None:
                    return {'returncode': 2, 'stderr': 'tar: %s: Cannot stat' % n}
                ti = tarfile.TarInfo(n); ti.size = len(data); t.addfile(ti, io.BytesIO(data))
        return {'stdout': N.base64.b64encode(buf.getvalue()).decode()}
    def rd(role, text, stdin):
        path = shlex.split(text)[-1]
        if path not in store:
            return {'returncode': 1, 'stderr': 'No such file'}
        if text.startswith('sha256sum'):
            return {'stdout': N.sha(store[path]) + '  ' + path + '\n'}
        return {'stdout': N.base64.b64encode(store[path]).decode()}
    return FakeGuest([(lambda r, t: 'tar -x' in t, untar),
                      (lambda r, t: 'sha256sum --' in t, sums),
                      (lambda r, t: 'tar -c --' in t, tarout),
                      (lambda r, t: 'cat >' in t, write),
                      (lambda r, t: t.startswith(('sha256sum', 'base64')), rd),
                      (lambda r, t: True, {'returncode': 0})]), store


class Edits(unittest.TestCase):
    def native(self, case_id='OW-8', variant=None):
        from casedefs import BY_ID
        b = bindings()
        g, store = guest_with_candidate({})
        work = tempfile.TemporaryDirectory()
        self.addCleanup(work.cleanup)
        n = N.Native({'work': work.name}, b, BY_ID[case_id], variant, guest=g)
        n.candidate = b.render(json.loads((HERE / 'declarations/D-test.json').read_text()))
        return n, store

    def test_replace_package_and_read_back(self):
        n, store = self.native()
        r = n.op_edit({'op': 'edit', 'action': 'replace', 'line': {'kind': 'package', 'name': 'case-small', 'binding': 'small-v2'}})
        self.assertIn('package case-small 2 case-small-2.recipe', r['after_lines'])
        self.assertNotIn('package case-small 1 case-small-1.recipe', r['after_lines'])
        self.assertIn('/data/confos/case-small-2.recipe', store)
        law = n.op_read_law({'op': 'read-law', 'scope': 'candidate'})
        self.assertEqual(law['sha256'], n.candidate.identity)
        self.assertEqual(law['expected_status'], 'APPLIED ' + n.candidate.identity)

    def test_remove_missing_line_is_error(self):
        n, _ = self.native()
        with self.assertRaises(ValueError):
            n.op_edit({'op': 'edit', 'action': 'remove', 'line': {'kind': 'package', 'name': 'case-owner-a'}})

    def test_xrec_record_delta_is_exact(self):
        n, _ = self.native('X-REC-HOST')
        n.xrec_before = n.candidate
        w, added, removed = n._record(n.b.cmd['xrec']['hostname']['record_add'])
        self.assertEqual(added, ['setting hostname case-rec'])
        self.assertEqual(removed, ['setting hostname case-test'])
        q = n.q_request_delta_valid({'target': 'hostname'})
        self.assertTrue(evaluate_query('request-delta-valid', q)['value'])

    def test_split_declaration(self):
        n, _ = self.native('W1d-MULTI')
        r = n.op_split_declaration({'op': 'split-declaration', 'files': ['main', 'programs']})
        self.assertEqual(r['file_count'], 2)
        self.assertEqual(sorted(n.candidate.lines()), sorted(n.before_split.lines()))


LIVE = '''P 1 4194560 0 aa /usr/sbin/confos-init -
P 2 2129984 0 - - -
P 300 4194560 1000 bb /usr/bin/case-probe Y2FzZS1wcm9iZSBsaXN0ZW4gNzA3Mg==
S 300 socket:[555]
N tcp 0100007F:1BB0 0A 555
A root:x:0:0:root:/root:/bin/bash
A user:x:1000:1000:user:/home/user:/bin/bash
G root:x:0:
G users:x:999:user
R /etc/sudoers.d/case-rule cc
K user ssh-ed25519 AAAA
V eyJjYXNlLXNlcnZpY2UiOiB7InN0YXRlIjogImVuYWJsZWQiLCAiYXJndiI6IFsiL3Vzci9iaW4vY2FzZS1wcm9iZSJdfX0=
W -
I 2: eth0    inet 10.0.2.15/24 scope global eth0
I 1: lo    inet 127.0.0.1/8 scope host lo
I 2: eth0    inet6 fe80::1/64 scope link
T4 default via 10.0.2.2 dev eth0
T4 10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15
M 20 1 0:1 / / ro,relatime - squashfs /dev/loop0 ro
M 21 20 0:2 / /home rw,nosuid,nodev,noexec,relatime - ext4 /dev/vda3 rw
M 22 20 0:3 / /tmp rw,nosuid,nodev,noexec - tmpfs tmpfs rw
D-ABSENT /proc/modules
Y net.ipv4.ip_forward 0
L LANG=C.UTF-8
Z ../usr/share/zoneinfo/Etc/GMT-3 Etc/GMT-3
H case-test case-test
FW table inet confos {
FW 	chain input {
FW 		type filter hook input priority filter; policy accept;
FW 		tcp dport 22 accept
FW 	}
FW }
FW-END
X-ABSENT ieee80211
X-ABSENT bluetooth
F /tmp/x 644 1000 1000 f 3
END'''


class Live(unittest.TestCase):
    def test_parse_live(self):
        live = N.parse_live(LIVE, {'returncode': 0})
        by = {(o['kind'], o['id']): o for o in live['objects']}
        self.assertEqual(by[('process', 'kthread:2')]['value']['exe_sha256'], '@KERNEL@')
        self.assertEqual(by[('port', 'tcp:0100007F:1BB0')]['value']['exe_sha256'], 'bb')
        self.assertEqual(by[('account', 'user')]['value']['groups'], ['users'])
        self.assertEqual(by[('network', '10.0.2.15/24')]['value'], {'gateway': '10.0.2.2'})
        self.assertIn(('network-link-local', 'eth0 fe80::1/64'), by)
        self.assertEqual(by[('mount', '/home')]['value']['noexec'], True)
        self.assertEqual(by[('time', 'timezone')]['value']['zone'], 'Etc/GMT-3')
        self.assertEqual(live['coverage']['module']['status'], 'not-applicable')
        self.assertEqual(live['coverage']['wifi']['status'], 'not-applicable')
        self.assertEqual(live['coverage']['saved-network']['status'], 'not-applicable')
        self.assertIn(('firewall-rule', 'tcp dport 22 accept'), by)
        self.assertEqual(live['coverage']['firewall-rule']['status'], 'complete')
        self.assertEqual([o['id'] for o in live['objects'] if o['kind'] == 'firewall-rule'], ['tcp dport 22 accept'])
        failed = N.parse_live(LIVE.replace('FW-END', 'FW-ERROR refused'), {'returncode': 0})
        self.assertIn('firewall-rule', [e.get('kind') for e in failed['errors']])

    def test_incomplete_capture_is_unavailable(self):
        with self.assertRaises(Unavailable):
            N.parse_live(LIVE.rsplit('\n', 1)[0], {'returncode': 0})

    def test_classify_material_and_noexec(self):
        live = N.parse_live(LIVE, {'returncode': 0})
        stored = [{'kind': 'file', 'id': '/data/home/user/case-input', 'value': {}},
                  {'kind': 'file', 'id': '/data/home/user/other', 'value': {}},
                  {'kind': 'file', 'id': '/usr/bin/bash', 'value': {}}]
        live['objects'].append({'kind': 'mount', 'id': '/data', 'value': {'noexec': True}})
        mat = {'/home/user/case-input': {'origin': 'payloads/unrecorded.sh', 'routes': [{'kind': 'direct', 'observed': True, 'executed': False}]}}
        out = {o['id']: o for o in N.classify(stored, mat, live)}
        self.assertEqual(out['/data/home/user/case-input']['routes'][0]['executed'], False)
        self.assertEqual(out['/data/home/user/other']['classification'], 'material')
        self.assertNotIn('classification', out['/usr/bin/bash'])
        self.assertEqual(out['/tmp/x']['classification'], 'material')

    def test_classify_opened_folder(self):
        live = N.parse_live(LIVE, {'returncode': 0})
        live['objects'] += [{'kind': 'mount', 'id': '/data', 'value': {'noexec': True}},
                            {'kind': 'mount', 'id': '/home/user/opened', 'value': {'noexec': False}}]
        stored = [{'kind': 'file', 'id': '/data/home/user/opened/script', 'value': {}},
                  {'kind': 'file', 'id': '/data/home/user/opened-sibling/script', 'value': {}}]
        mat = {p: {'origin': 'boundary-fixture', 'routes': [{'kind': 'direct', 'observed': True, 'executed': True}]}
               for p in ('/home/user/opened/script', '/home/user/opened-sibling/script')}
        out = {o['id']: o for o in N.classify(stored, mat, live)}
        o = out['/data/home/user/opened/script']
        self.assertEqual((o['classification'], o['value']['resolved_path']), ('opened-material', '/home/user/opened/script'))
        self.assertEqual(out['/data/home/user/opened-sibling/script']['classification'], 'material')
        exp = {'objects': [], 'errors': [], 'openings': ['/home/user/opened']}
        issues = core.compare(exp, {'objects': [x for x in out.values() if x['id'].startswith('/data/')]})
        self.assertNotIn(['file', '/data/home/user/opened/script'], [i['object'] for i in issues])
        self.assertIn(['file', '/data/home/user/opened-sibling/script'], [i['object'] for i in issues])


class Commands(unittest.TestCase):
    def test_every_variant_bound_or_reasoned(self):
        plans = json.loads((HERE / 'plans.json').read_text())
        cmd = json.loads((HERE / 'bindings/commands-0.70.json').read_text())
        b = bindings()
        for c in plans:
            for v in c.get('variants', []):
                entry = cmd['variants'][c['id']][v]
                if 'unsupported' in entry or 'covered_by' in entry:
                    self.assertTrue(entry.get('unsupported', entry.get('covered_by')))
                    continue
                for step in entry.get('steps', {}).values():
                    b.shell(step['command'], dict(entry.get('tokens', {}), **{'@MARKER@': '/tmp/m', '@CHILD_PATHS@': ''}))
                if 'effect' in entry:
                    b.shell(entry['effect'])
        for x in cmd['xrec'].values():
            if 'unsupported' in x:
                continue
            for k in ('add', 'remove', 'effect'):
                if x.get(k):
                    b.shell(x[k])



class EngineWiring(unittest.TestCase):
    """G-SHELL through engine.execute with a stubbed machine: wiring only, not a system result."""
    def test_g_shell_pass_and_planted_object_fails(self):
        from casedefs import BY_ID
        from core import derive as core_derive
        from engine import execute
        b = bindings()
        case = BY_ID['G-SHELL']
        rows0 = None
        for planted in (False, True):
            g = FakeGuest([(lambda r, t: 'printf shell-ok' in t, {'stdout': 'shell-ok'}),
                           (lambda r, t: t == 'sync', {})])
            work = tempfile.TemporaryDirectory(); self.addCleanup(work.cleanup)
            tree = TREE
            if not (tree / 'recipes').is_dir():
                self.skipTest('release tree not beside the set')
            n = N.Native({'work': work.name, 'tree': str(tree)}, b, case, None, guest=g)
            decl = b.render(json.loads((HERE / 'declarations/D-test.json').read_text()))
            reader = lambda line: []
            def fresh(request, n=n, decl=decl):
                n.candidate = decl; n.disk = '/nonexistent.raw'
                return {'returncode': 0, 'boot_id': 'b1', 'status': 'APPLIED ' + decl.identity}
            def law(request, n=n, decl=decl):
                return {'scope': 'committed', 'sha256': decl.identity, 'declaration': n._semantic(decl), 'lines': decl.lines()}
            def inventory(request, n=n, decl=decl, planted=planted):
                objs = core_derive(n._semantic(decl), reader)['objects']
                objs = [{'kind': o['kind'], 'id': o['id'], 'value': o.get('value', {})} for o in objs]
                if planted:
                    objs.append({'kind': 'file', 'id': '/usr/bin/planted', 'value': {'sha256': 'ee'}})
                from core import COVERAGE
                return {'objects': objs, 'errors': [], 'coverage': {k: {'status': 'complete', 'evidence': 'fixture'} for k in COVERAGE}}
            n.op_fresh, n.op_read_law, n.op_inventory = fresh, law, inventory
            rows, ev = execute(case, n, reader)
            got = {(r['check'], r['part']): r['outcome'] for r in rows}
            self.assertEqual(got[('shell:2', 'case')], 'pass')
            self.assertEqual(got[('final', 'P1')], 'fail' if planted else 'pass')
            self.assertEqual(got[('case-result', 'case-summary')], 'fail' if planted else 'pass')

    def test_without_recipes_checkpoint_is_unobserved(self):
        sem = N.semantic_from_native(N.NativeDecl({N.MAIN: b'base 0.70\npackage bash 5.3\n'}), None, {})
        from core import derive, compare, outcome, COVERAGE
        inv = {'objects': [], 'errors': [], 'coverage': {k: {'status': 'complete', 'evidence': 'x'} for k in COVERAGE}}
        issues = compare(derive(sem, None), inv)
        self.assertIn(('UNDERIVED', ['line', N.MAIN + ':2']), [(i['status'], i['object']) for i in issues])


class Routes(unittest.TestCase):
    def test_route_kinds(self):
        f = '/home/user/case-input'
        self.assertEqual(N.route_kind('cat %s | /bin/sh' % f, f), 'data')
        self.assertEqual(N.route_kind('/bin/sh -c "$(cat %s)"' % f, f), 'data')
        self.assertEqual(N.route_kind('sh %s' % f, f), 'direct')
        self.assertEqual(N.route_kind('%s' % f, f), 'direct')
        self.assertEqual(N.route_kind('/bin/sh < %s' % f, f), 'direct')
        self.assertEqual(N.route_kind('case-probe read %s' % f, f), 'data')
        self.assertIsNone(N.route_kind('true', f))

    def test_rule_derived_by_statement(self):
        sem = N.semantic_from_native(N.NativeDecl({N.MAIN: b"base 0.70\nrule case-ssh 'add rule inet confos input tcp dport 22 accept'\n"}), None, {})
        objs = [x['object'] for x in (sem if isinstance(sem, list) else sem['lines']) if x.get('kind') == 'object' and x['object']['kind'] == 'firewall-rule']
        self.assertEqual(objs, [{'kind': 'firewall-rule', 'id': 'tcp dport 22 accept', 'value': {}}])


class FinalComparison(unittest.TestCase):
    """The final comparison can pass: what the lines bring onto the system partition (the
    archive of a named package, the tree and the sources of the release named by `base`,
    the generation in force) is derived and compared; only what no line names stays
    undecided (QUESTIONS Q-GENERATION), one state per kind of such object."""

    def setUp(self):
        import adapter_disk
        self.AD = adapter_disk
        t = tempfile.TemporaryDirectory(); self.addCleanup(t.cleanup)
        self.tree = Path(t.name) / 'tree'
        self.src = b'source archive bytes'
        for rel, data, x in (('recipes/demo.recipe', b'name: demo\nsource: demo-1.tar.gz %s\nsource: tools %s\n'
                              % (N.sha(self.src).encode(), b'0' * 64), False),
                             ('files/base-files/etc/os-release', b'VERSION_ID="0.70"\n', False),
                             ('files/confos/confos', b'VERSION = "0.70"\n', True),
                             ('tools/confpkg', b'#!/usr/bin/python3\n', True)):
            f = self.tree / rel; f.parent.mkdir(parents=True, exist_ok=True); f.write_bytes(data)
            f.chmod(0o755 if x else 0o644)
        self.src = b'source archive bytes'
        (self.tree / 'sources.tsv').write_text('demo\t1\thttps://example.org/demo-1.tar.gz\t%s\tMIT\tnote\n' % N.sha(self.src))
        self.recipe = b'name: demo\nversion: 1\nsource: demo-1.tar.gz %s\nbuild:\ntrue\n' % N.sha(self.src).encode()
        self.decl = N.NativeDecl({N.MAIN: b'base 0.70\npackage demo 1 demo-1.recipe\n'},
                                 {'demo-1.recipe': self.recipe, 'demo-1.tar.gz': self.src})
        self.gid = self.decl.identity
        self.manifest = self.AD.tree_manifest_local(str(self.tree))['manifest']

    def expected(self):
        sem = N.semantic_from_native(self.decl, None, {}, [], None, trees={'0.70': str(self.tree)})
        return derive(sem, lambda line: [])

    def disk_info(self):
        pairs = [['demo-1.tar.gz', N.sha(self.src)]]
        return {'selected': self.gid, 'state_applied': self.gid + '\n', 'errors': [],
                'boot_cfg': 'linux /generations/%s/vmlinuz confos.generation=%s\n' % (self.gid, self.gid),
                'generations': {self.gid: {'declaration_files': {N.MAIN: self.gid}, 'kernel_sha256': 'k',
                                           'initramfs_sha256': 'i', 'root_sqfs_sha256': 'r',
                                           'root': {'objects': [], 'errors': []}}},
                'system_root_meta': None, 'data': {'objects': [], 'errors': []},
                'system_store': {'packages': {'demo-1.confpkg': 'a' * 64},
                                 'archives': {'demo-1.confpkg': {'name': 'demo', 'version': '1',
                                                                 'recipe_sha256': N.sha(self.recipe), 'sources': pairs}},
                                 'trees': [{'path': '/tree', 'manifest': self.manifest, 'files': 3, 'version_id': '0.70'}],
                                 'sources': {'demo-1.tar.gz': N.sha(self.src)}, 'other_entries': []}}

    def compare(self, info):
        inv = self.AD.inventory_from_disk(info)
        exp = self.expected()
        objs = inv['objects'] + [{'kind': 'package', 'id': 'demo', 'value': {
            'version': '1', 'recipe_sha256': N.sha(self.recipe), 'source_sha256': [['demo-1.tar.gz', N.sha(self.src)]]}},
            # the live capture of the release defaults (INTERFACE 5), as on a running system
            {'kind': 'hostname', 'id': 'hostname', 'value': {'name': 'confos'}},
            {'kind': 'time', 'id': 'timezone', 'value': {'zone': 'Etc/UTC'}},
            {'kind': 'locale', 'id': 'LANG', 'value': {'value': 'C.UTF-8'}}]
        cov = {k: {'status': 'complete', 'evidence': 'fixture'} for k in core.COVERAGE}
        issues = core.compare(exp, {'objects': objs, 'errors': inv['errors'], 'coverage': cov})
        return core.outcome(issues), issues

    def test_derived_store_objects(self):
        keys = {(o['kind'], o['id']) for o in self.expected()['objects']}
        for k in (('system-archive', '/system/packages/demo-1.confpkg'), ('release-tree', '0.70'),
                  ('release-source', 'demo-1.tar.gz'), ('system-store', '/system/generations/' + self.gid),
                  ('system-store', '/system/boot.cfg'), ('system-store', '/system/state/applied')):
            self.assertIn(k, keys)

    def test_ordinary_state_passes(self):
        out, issues = self.compare(self.disk_info())
        self.assertEqual((out, issues), ('pass', []))

    def test_each_remaining_kind_is_undecided(self):
        def gen_before(i):
            i['generations']['b' * 64] = {'declaration_files': {}, 'kernel_sha256': 'k', 'initramfs_sha256': 'i',
                                          'root_sqfs_sha256': 'r', 'root': {'objects': [], 'errors': []}}
        def archive(i):
            i['system_store']['packages']['old-1.confpkg'] = 'b' * 64
        def tree(i):
            i['system_store']['trees'].append({'path': '/trees/0.65', 'release': '0.65', 'manifest': 'm', 'files': 3})
        def source(i):
            i['system_store']['sources']['old-1.tar.gz'] = 'c' * 64
        for name, change, key in (('generation before', gen_before, ['generation', 'b' * 64]),
                                  ('archive no line names', archive, ['system-archive', '/system/packages/old-1.confpkg']),
                                  ('tree of a release no line names', tree, ['release-tree', '0.65']),
                                  ('source no line names', source, ['release-source', 'old-1.tar.gz'])):
            with self.subTest(name):
                info = self.disk_info(); change(info)
                out, issues = self.compare(info)
                self.assertEqual(out, 'undecided')
                self.assertEqual([(i['status'], i['object']) for i in issues], [('UNDECIDED', key)])

    def test_what_a_line_brings_is_decided(self):
        info = self.disk_info(); info['system_store']['sources']['demo-1.tar.gz'] = 'd' * 64
        self.assertEqual(self.compare(info)[0], 'fail')
        info = self.disk_info(); del info['system_store']['packages']['demo-1.confpkg']
        self.assertEqual(self.compare(info)[0], 'fail')
        info = self.disk_info(); info['system_store']['trees'][0]['manifest'] = 'e' * 64
        self.assertEqual(self.compare(info)[0], 'fail')
        info = self.disk_info(); info['state_applied'] = 'f' * 64 + '\n'
        self.assertEqual(self.compare(info)[0], 'fail')


class UpdateStates(unittest.TestCase):
    """INTERFACE 9 bindings: the edit of an update state and the raw operands of the
    components query (the trees are private copies; without them the edit test skips)."""

    def test_slots_bound(self):
        b = bindings()
        for st in ('T1', 'T2'):
            s = b.slot(st)
            self.assertTrue(s['native'][0].startswith('base 0.70.'))
            self.assertEqual(len(s['native'][0].split()), 4)
            self.assertIn('base-files', s['replaces']['packages'])
            self.assertTrue(s['tree_input']['files'])
        self.assertEqual(b.slot('system-update-state-T0')['native'], ['base 0.70'])

    def test_edit_and_components(self):
        trees, src = dict(UPDATE_TREES), UPDATE_SOURCES
        if not all(trees.values()) or not src:
            self.skipTest('update trees (CONFOS_TREE_T1/T2) and sources (CONFOS_SOURCES) not given')
        from casedefs import BY_ID
        b = bindings(); b.local = {'update_trees': trees, 'sources': src}
        g, store = guest_with_candidate({})
        versions = {'tzdata': '2025b', 'base-files': '0.70', 'confos': '0.70', 'file': '5.46'}
        def passport(role, text, stdin):
            name = text.split('/')[-1][:-len('.passport')]
            return {'stdout': 'confpkg 1\nname %s\nversion %s\nsource %s.tar sha256 %s\nrecipe %s.recipe sha256 %s\nbuilt-with bash-5.3\n'
                              % (name, versions[name], name, 'a' * 64, name, 'b' * 64)}
        g.replies.insert(0, (lambda r, t: t.startswith('cat /usr/lib/confpkg/'), passport))
        work = tempfile.TemporaryDirectory(); self.addCleanup(work.cleanup)
        n = N.Native({'work': work.name}, b, BY_ID['OW-2'], None, guest=g)
        n.candidate = b.render(json.loads((HERE / 'declarations/D-test.json').read_text()))
        r = n.op_edit({'op': 'edit', 'action': 'replace', 'line': {'kind': 'base', 'binding': 'T1'}})
        self.assertIn(b.slot('T1')['native'][0], r['after_lines'])
        self.assertNotIn('base 0.70', r['after_lines'])
        self.assertIn('package tzdata 2026f', r['after_lines'])
        self.assertNotIn('package tzdata 2025b', r['after_lines'])
        self.assertIn(N.CANDIDATE_DIR + '/rel-0.70.1/tools/confpkg', store)
        self.assertIn(N.CANDIDATE_DIR + '/tzdata2026f.tar.gz', store)
        versions.update({'tzdata': '2026f', 'base-files': '0.70.1', 'confos': '0.70.1'})
        n.q_system_source_state = lambda req: {'value': 'T1'}
        q = n.q_system_components_changed({'subject': 'system-components-changed'})
        self.assertTrue(evaluate_query('system-components-changed', q)['value'])
        n.before_components['values'] = dict(q['after_components'])
        self.assertFalse(evaluate_query('system-components-changed', n.q_system_components_changed({}))['value'])
        r2 = n.op_edit({'op': 'edit', 'action': 'replace', 'line': {'kind': 'base', 'binding': 'T2'}})
        self.assertEqual(r2['removed_inputs'] if 'removed_inputs' in r2 else n.stale_inputs, ['rel-0.70.1', 'tzdata2026f.tar.gz'])


if __name__ == '__main__':
    unittest.main()
