# Instrument workaround: type text on the guest's virtual console via QMP send-key, optional screendump.
# usage: qmpkeys.py QMP_SOCK [--text STRING] [--enter] [--dump FILE.ppm]
import socket,json,sys,time
args=sys.argv[1:];sock=args.pop(0)
s=socket.socket(socket.AF_UNIX);s.connect(sock);f=s.makefile('rw')
def cmd(c,a=None):
    m={'execute':c};
    if a is not None:m['arguments']=a
    f.write(json.dumps(m)+'\n');f.flush()
    while True:
        r=json.loads(f.readline())
        if 'return' in r or 'error' in r:return r
json.loads(f.readline());cmd('qmp_capabilities')
names={' ':'spc','\n':'ret','-':'minus','=':'equal','/':'slash','.':'dot',',':'comma',';':'semicolon',"'":'apostrophe','\\':'backslash','[':'bracket_left',']':'bracket_right','`':'grave_accent'}
shifted={'_':'minus','+':'equal','|':'backslash','>':'dot','<':'comma',':':'semicolon','"':'apostrophe','?':'slash','~':'grave_accent','!':'1','@':'2','#':'3','$':'4','%':'5','^':'6','&':'7','*':'8','(':'9',')':'0','{':'bracket_left','}':'bracket_right'}
def key(ch):
    if ch in shifted:ks=['shift',shifted[ch]]
    elif ch.isupper():ks=['shift',ch.lower()]
    elif ch in names:ks=[names[ch]]
    else:ks=[ch]
    r=cmd('send-key',{'keys':[{'type':'qcode','data':k} for k in ks]})
    if 'error' in r:print('ERR',ch,r,file=sys.stderr)
    time.sleep(0.03)
while args:
    a=args.pop(0)
    if a=='--text':
        for ch in args.pop(0):key(ch)
    elif a=='--textfile':
        for ch in open(args.pop(0)).read().rstrip('\n'):key(ch)
    elif a=='--enter':key('\n')
    elif a=='--sleep':time.sleep(float(args.pop(0)))
    elif a=='--dump':print(cmd('screendump',{'filename':args.pop(0)}))
