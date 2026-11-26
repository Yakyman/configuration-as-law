#!/usr/bin/env python3
import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class EntryPoints(unittest.TestCase):
    def call(self,*args):
        return subprocess.run([sys.executable,'-B',*args],cwd=ROOT,capture_output=True,text=True)
    def test_fixture_pass(self):
        p=self.call('run','--case','G-SHELL','--fixture','fixtures/shell-pass.json')
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertTrue(json.loads(p.stdout)['fixture'])
    def test_fixture_fail(self):
        p=self.call('run','--case','G-SHELL','--fixture','fixtures/shell-fail.json')
        self.assertEqual(p.returncode,1,p.stderr)
        data=json.loads(p.stdout);self.assertTrue(data['requests'])
        self.assertTrue(any(r['part']=='UND' and r['outcome']=='unobserved' for r in data['rows']))
    def test_no_accidental_live_run(self):
        p=self.call('run','--case','G-SHELL')
        self.assertEqual(p.returncode,2);self.assertIn('no release interface bound',p.stderr)
    def test_derive_compare_cli(self):
        p=self.call('derive','--declaration','fixtures/empty-declaration.json');self.assertEqual(p.returncode,0,p.stderr)
        with tempfile.TemporaryDirectory(dir=ROOT/'selftest') as d:
            f=Path(d)/'derived.json';f.write_text(p.stdout)
            p=self.call('compare','--derived',str(f),'--inventory','fixtures/empty-inventory.json')
            self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout)['outcome'],'pass')
    def test_unbound_derivation_nonzero(self):
        p=self.call('derive','--declaration','declarations/D-test.json')
        self.assertEqual(p.returncode,2);self.assertTrue(json.loads(p.stdout)['errors'])
if __name__=='__main__': unittest.main(verbosity=2)
