#!/usr/bin/python3
"""Pure lifecycle/validation checks; deliberately never invokes native setup."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import radio_runtime as runtime
import radio_declaration as declaration

class Tests(unittest.TestCase):
    def test_exact_public_inputs_render(self):
        root=Path(__file__).parent/'radio-public-fixture'
        result=declaration.derive((root/'radio-draft.conf').read_text(),root)
        self.assertEqual(len(result['plan']['bonds']),2)
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)
            for path,entry in result['files'].items():
                out=target/Path(path).relative_to(declaration.PREFIX)
                out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(entry['data']);out.chmod(entry['mode'])
            # Only fake immutable storage metadata; native functions remain uncalled.
            with patch.object(runtime,'IMMUTABLE',target),patch.object(runtime.os,'statvfs',return_value=SimpleNamespace(f_flag=runtime.os.ST_RDONLY)),patch.object(Path,'stat',return_value=SimpleNamespace(st_uid=0,st_mode=0o100600)):
                plan,digest=runtime.load_plan()
            self.assertEqual(plan,result['plan'])
            self.assertEqual(len(digest),64)
    def test_writable_inputs_refused(self):
        with patch.object(runtime.os,'statvfs',return_value=SimpleNamespace(f_flag=0)):
            with self.assertRaisesRegex(ValueError,'read-only'): runtime.load_plan()
    def test_unowned_runtime_not_cleaned(self):
        s=runtime.Supervisor({'fixture':None,'network':None,'bonds':[]},'a'*64)
        with patch.object(runtime.READY.__class__,'unlink') as unlink:
            s.cleanup()
        unlink.assert_not_called()
    def test_client_status_requires_correct_radio(self):
        s=runtime.Supervisor({'network':{'address':'192.0.2.2/24'}},'a'*64)
        good='wpa_state=COMPLETED\nkey_mgmt=WPA2-PSK\npairwise_cipher=CCMP\ngroup_cipher=CCMP\nip_address=192.0.2.2\nid=0\nbssid=02:00:00:00:00:00\n'
        for text,expect in ((good,True),(good.replace('id=0','id=1'),False),(good.replace('00:00:00\n','00:00:01\n'),False),(good.replace('WPA2-PSK','NONE'),False)):
            with patch.object(runtime,'command',return_value=SimpleNamespace(stdout=text)):
                self.assertEqual(s.wifi_connected(),expect)
    def test_failure_revokes_owned_ready_and_keys(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'runtime';root.mkdir();ready=root/'ready.json';ready.write_text('ready')
            (root/'bluez').mkdir();(root/'bluez'/'key').write_text('test')
            s=runtime.Supervisor({},'a'*64);s.owned_run=True;s.failure=True
            with patch.object(runtime,'RUN',root),patch.object(runtime,'READY',ready):s.cleanup()
            self.assertFalse(ready.exists());self.assertFalse((root/'bluez').exists())
            self.assertFalse(root.exists()) # diagnostics streamed; no keys/control mount retained

if __name__=='__main__':unittest.main(verbosity=2)
