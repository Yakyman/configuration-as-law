#!/usr/bin/env python3
# Installer UI lives only in memory; no installer transcript is retained.
import os,sys,socket,select,json,time
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'terminal-deps'))
import pyte
os.chdir(os.path.dirname(__file__))
screen=pyte.Screen(80,25); stream=pyte.ByteStream(screen)
s=socket.socket(socket.AF_UNIX)
for _ in range(120):
 try:s.connect('install.sock');break
 except OSError:time.sleep(1)
s.setblocking(False)
c=socket.socket(socket.AF_UNIX);c.bind('terminal.sock');c.listen()
while True:
 for sock in select.select([s,c],[],[])[0]:
  if sock is s:
   data=s.recv(65536)
   if not data:sys.exit()
   stream.feed(data)
  else:
   conn,_=c.accept();req=json.loads(conn.recv(65536))
   if req.get('send'):s.sendall(req['send'].encode())
   conn.sendall(('\n'.join(screen.display)).encode());conn.close()
