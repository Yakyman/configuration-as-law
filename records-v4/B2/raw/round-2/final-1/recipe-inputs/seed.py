#!/usr/bin/env python3
"""Create disposable bootstrap credentials; no private key enters the guest."""
import json, pathlib, subprocess
r=pathlib.Path(__file__).resolve().parent.parent
pub=(r/'keys/guest.pub').read_text().strip()
data={'users':[{'name':'stand','uid':1000,'shell':'/bin/bash','groups':['sudo'],
               'sudo':['ALL=(ALL) NOPASSWD:ALL'],'lock_passwd':True,'ssh_authorized_keys':[pub]}],
      'disable_root':True,'ssh_pwauth':False,'manage_etc_hosts':False}
(r/'build/user-data').write_text('#cloud-config\n'+json.dumps(data)+'\n')
(r/'build/meta-data').write_text('instance-id: stand-bootstrap\nlocal-hostname: stand\n')
subprocess.run(['cloud-localds',str(r/'build/seed.iso'),str(r/'build/user-data'),str(r/'build/meta-data')],check=True)
