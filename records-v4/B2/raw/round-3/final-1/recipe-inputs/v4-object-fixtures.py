#!/usr/bin/python3 -B
"""Exact finite object fixtures; generated on the target interpreter version."""
import base64,hashlib,json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import recorded_objects

def file(path,content,mode=0o644):
    return {'path':path,'kind':'file','mode':mode,'uid':0,'gid':0,'sha256':hashlib.sha256(content).hexdigest(),'content_b64':base64.b64encode(content).decode()}

def rows():
    root='/opt/stand/pkgs/v4-objects/'
    source=root+'source.py'
    payload=(b'from pathlib import Path\nprint("RECORDED-BYTECODE")\n'
             b'print("DEFAULT-LANGUAGE:" + Path("/opt/stand/pkgs/v4-objects/default.conf").read_text().strip().split("=", 1)[1])\n')
    config=file(root+'default.conf',b'language=en\n')
    copied=file(root+'copy.py',payload)
    bytecode=file(root+'source.pyc',recorded_objects.derived_bytes(source,payload,'python-bytecode'))
    return [
        {'id':'v4:objects','type':'program','managed':True,'version':'1','source':'fixture:round-2',
         'package_identity':{'backend':'stand','name':'v4-objects','version':'1'},
         'files':[file(source,payload),copied,bytecode,config],
         'default_settings':[{'path':config['path']}],
         'derivations':[{'path':copied['path'],'source_path':source,'algorithm':'copy'},
                        {'path':bytecode['path'],'source_path':source,'algorithm':'python-bytecode'}]},
        {'id':'v4:meta','type':'program','managed':True,'version':'1','source':'fixture:round-2',
         'package_identity':{'backend':'stand','name':'v4-meta','version':'1'},'files':[],
         'package_dependencies':[{'backend':'stand','name':'v4-dependency','version':'1'}]},
        {'id':'v4:noncode','type':'program','managed':True,'version':'1','source':'fixture:round-2',
         'package_identity':{'backend':'stand','name':'v4-noncode','version':'1'},
         'files':[file('/opt/stand/pkgs/v4-noncode/lookup.txt',b'alpha=1\nbeta=2\n')]},
        {'id':'v4:printk','type':'setting','managed':True,'reader':'sysctl','name':'kernel.printk','value':'4 4 1 7'}]
def generated_unit(executable_path):
    text=('[Unit]\nDescription=Recorded source fixture\n[Service]\nType=simple\nUser=stand\nExecStart='+executable_path+
          '\nRestart=no\nKillMode=control-group\nTimeoutStopSec=5\nMemoryDenyWriteExecute=yes\nNoNewPrivileges=yes\nProtectSystem=strict\nPrivateTmp=yes\n[Install]\nWantedBy=multi-user.target\n')
    source='/opt/stand/pkgs/v4-unit/source.service'
    return [
        {'id':'v4:unit-source','type':'program','managed':True,'version':'1','source':'fixture:round-2',
         'package_identity':{'backend':'stand','name':'v4-unit-source','version':'1'},'files':[file(source,text.encode())]},
        {'id':'v4:generated-unit','type':'service','managed':True,'unit':'stand-v4-generated.service',
         'unit_text':text,'unit_sha256':hashlib.sha256(text.encode()).hexdigest(),'enabled':'disabled','active':False,
         'derived_from':{'line':'v4:unit-source','source_path':source,'algorithm':'copy'}}]

if __name__=='__main__':print(json.dumps(rows(),sort_keys=True))
