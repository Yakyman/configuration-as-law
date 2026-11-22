import socket,time,pathlib
root=pathlib.Path.home()/'VMs/cal-1122'
s=socket.socket(socket.AF_UNIX);s.connect(str(root/'install/guix/monitor.sock'))
def key(k):
 s.sendall(('sendkey '+k+'\n').encode());time.sleep(.04)
def text(t):
 mapping={'.':'dot',' ':'spc','/':'slash','-':'minus',';':'semicolon','>':'shift-dot','&':'shift-7',':':'shift-semicolon','=':'equal'}
 for c in t:
  key(mapping.get(c,'shift-'+c.lower() if c.isupper() else c))
key('ret');time.sleep(1)
text('mkdir -p /run/install-input; mount /dev/sr1 /run/install-input; bash /run/install-input/install.sh >/dev/ttyS0 2>&1')
key('ret')
