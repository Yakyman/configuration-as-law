import socket,json,time,sys,base64
sock=socket.socket(socket.AF_UNIX);sock.connect('C1/vms/c1-mint-actions/qmp.sock')
f=sock.makefile('rwb',buffering=0)
def cmd(obj):
 f.write(json.dumps(obj).encode()+b'\n')
 while True:
  r=json.loads(f.readline())
  if 'return' in r:return r
  if 'error' in r:raise RuntimeError(r)
f.readline();cmd({'execute':'qmp_capabilities'})
def key(k):
 cmd({'execute':'human-monitor-command','arguments':{'command-line':'sendkey '+k}});time.sleep(.06)
def text(t):
 m={' ':'spc','-':'minus','=':'equal','/':'slash','+':'shift-equal','.':'dot','|':'shift-backslash','\n':'ret'}
 for c in t:key(m.get(c,'shift-'+c.lower() if c.isupper() else c))
key('ctrl-alt-f2');time.sleep(1);text('user\n');time.sleep(1);text('cal-test\n');time.sleep(1)
script=open('C1/install/mint/enable-serial.sh','rb').read()
text('echo '+base64.b64encode(script).decode()+' | base64 -d | bash\n')
