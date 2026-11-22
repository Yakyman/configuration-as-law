import socket,sys,time
s=socket.socket(socket.AF_UNIX);s.connect('C1/install/mint/monitor.sock');s.recv(4096)
for key in sys.argv[1:]:
 s.sendall(('sendkey '+key+'\n').encode());time.sleep(.5);s.recv(4096)
