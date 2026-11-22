import socket,time,pathlib,re
root=pathlib.Path.cwd()
s=socket.socket(socket.AF_UNIX);s.settimeout(1)
for _ in range(120):
 try:
  s.connect(str(root/'C1/fix-c1-1/nixos/serial.sock'));break
 except FileNotFoundError:time.sleep(1)
else:raise RuntimeError('Installer socket did not appear')
deadline=time.monotonic()+240
buf=b''
while time.monotonic()<deadline:
 s.sendall(b'\r')
 try:buf+=s.recv(65536)
 except TimeoutError:pass
 clean=re.sub(rb'\x1b\[[0-9;?]*[a-zA-Z]',b'',buf)
 if re.search(rb'[$#]\s*$',clean):break
 time.sleep(1)
else:raise RuntimeError('Installer shell readiness timeout')
command=b'sudo mkdir -p /run/install-input /run/install-output; sudo mount -t 9p -o trans=virtio,version=9p2000.L input /run/install-input; sudo mount -t 9p -o trans=virtio,version=9p2000.L output /run/install-output; sudo bash /run/install-input/install.sh\n'
for i in range(0,len(command),8):
 s.sendall(command[i:i+8]);time.sleep(.01)
deadline=time.monotonic()+2400
while time.monotonic()<deadline:
 try:
  if not s.recv(65536):break
 except TimeoutError:pass
s.close()
