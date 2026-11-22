#!/usr/bin/env python3
import socket,json,sys,os
from datetime import datetime,timezone
s=socket.socket(socket.AF_UNIX);s.connect(os.path.join(os.path.dirname(__file__),'terminal.sock'))
if len(sys.argv)>1:
 with open(os.path.join(os.path.dirname(__file__),'input-events.jsonl'),'a') as f:f.write(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'send':sys.argv[1]})+'\n')
s.sendall(json.dumps({'send':sys.argv[1] if len(sys.argv)>1 else ''}).encode());print(s.recv(65536).decode())
