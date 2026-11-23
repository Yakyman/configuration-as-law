import urllib.request,concurrent.futures,json
paths=['gnu/services/base.scm','gnu/services/desktop.scm','gnu/services/xorg.scm','gnu/services/ssh.scm','gnu/services/dbus.scm','gnu/system.scm','gnu/system/pam.scm','guix/profiles.scm','gnu/services/shepherd.scm','gnu/system/shadow.scm','gnu/services/networking.scm','guix/self.scm']
base='https://raw.githubusercontent.com/Millak/guix/master/'
def f(p):
 try:return p,urllib.request.urlopen(base+p,timeout=20).read().decode()
 except:return p,''
d=dict(concurrent.futures.ThreadPoolExecutor(4).map(f,paths));json.dump(d,open('A1/c1/part-4.2-generated-docs.json','w'))
print([(p,len(t)) for p,t in d.items()])
