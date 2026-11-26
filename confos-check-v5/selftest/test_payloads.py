#!/usr/bin/env python3
"""Small host fixtures validate payload syntax/behavior, not OS enforcement."""
import os,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Payloads(unittest.TestCase):
    def test_compile_and_harmless_modes(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'selftest') as tmp:
            out=Path(tmp)
            for src,name in [('case-small.c','small'),('case-probe.c','probe')]:
                p=subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(ROOT/'payloads'/src),'-o',str(out/name)],capture_output=True,text=True)
                self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(subprocess.check_output([str(out/'small')],text=True),'case-small 1\n')
            self.assertEqual(subprocess.check_output([str(out/'probe'),'control'],text=True),'probe-control\n')
            self.assertEqual(subprocess.check_output([str(out/'probe'),'read',str(ROOT/'payloads/typed-input.sh')],text=True),'typed-ok\n')
            value=subprocess.check_output([str(out/'probe'),'values',str(ROOT/'payloads/values.txt')],text=True)
            self.assertIn('theme=plain',value)
            p=subprocess.run([str(out/'probe'),'read',str(out/'absent')],capture_output=True)
            self.assertNotEqual(p.returncode,0)
    def test_recipe_staged_build(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'selftest') as tmp:
            env=dict(os.environ,DESTDIR=tmp,CASE_VERSION='2',CASE_FETCH='wget',CASE_FETCH_STYLE='wget')
            p=subprocess.run(['sh','build.sh'],cwd=ROOT/'payloads',env=env,capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(subprocess.check_output([str(Path(tmp)/'usr/bin/case-small')],text=True),'case-small 2\n')
    def test_recipe_requires_destination(self):
        env=dict(os.environ);env.pop('DESTDIR',None)
        p=subprocess.run(['sh',str(ROOT/'payloads/build.sh')],env=env,capture_output=True)
        self.assertNotEqual(p.returncode,0)
if __name__=='__main__': unittest.main(verbosity=2)
