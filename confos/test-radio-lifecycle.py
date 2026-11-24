#!/usr/bin/python3
"""Local checks, no radio/device calls; native evidence is a separate VM run."""
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch
import radio_runtime
import radio_systemd

class Lifecycle(unittest.TestCase):
    def test_notify_after_record(self):
        with tempfile.TemporaryDirectory() as temp:
            ready=Path(temp)/'ready.json';endpoint=str(Path(temp)/'notify')
            with socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM) as listener:
                listener.bind(endpoint);listener.settimeout(1)
                runtime=radio_runtime.Supervisor({},'f'*64)
                with patch.object(radio_runtime,'READY',ready),patch.dict(os.environ,{'NOTIFY_SOCKET':endpoint}):
                    runtime.publish_ready()
                self.assertEqual(listener.recv(4096),b'READY=1')
                self.assertIn('f'*64,ready.read_text())
    def test_unit_dependencies_and_cleanup(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);units=root/'etc/confos/systemd-system';units.mkdir(parents=True)
            for name in ('confos-ready.service','confos-user-1000.service'):(units/name).write_text('[Service]\n')
            radio_systemd.configure(root)
            service=(units/'confos-radio.service').read_text()
            self.assertIn('Type=notify\nNotifyAccess=main\n',service)
            self.assertIn('KillMode=control-group\n',service)
            self.assertIn('ExecStopPost=/usr/bin/rm -f /run/confos-ready',service)
            for name in ('confos-ready.service','confos-user-1000.service'):
                text=(units/(name+'.d')/'90-radio.conf').read_text()
                self.assertIn('BindsTo=confos-radio.service\nAfter=confos-radio.service\n',text)
            with self.assertRaises(ValueError):radio_systemd.configure(root)

if __name__=='__main__':unittest.main(verbosity=2)
