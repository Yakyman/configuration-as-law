# External-root diagnostic only. Expected: capture effective capabilities and the failed credential call.
import pathlib,subprocess,sys,time
P=pathlib.Path
s=P('/tmp/session.c').read_text().replace('#include <linux/landlock.h>','#include <linux/landlock.h>\n#include <linux/capability.h>')
s=s.replace('if(setresuid(1000,1000,1000))fail("drop uid");','struct __user_cap_header_struct h={.version=_LINUX_CAPABILITY_VERSION_3,.pid=0};struct __user_cap_data_struct c[2];syscall(SYS_capget,&h,c);dprintf(2,"DROP pid=%d uid=%d euid=%d gid=%d caps=%08x%08x secure=%d seccomp=%d nnp=%d\\n",getpid(),getuid(),geteuid(),getgid(),c[1].effective,c[0].effective,prctl(PR_GET_SECUREBITS),prctl(PR_GET_SECCOMP),prctl(PR_GET_NO_NEW_PRIVS,0,0,0,0));if(setresuid(1000,1000,1000))fail("drop uid");')
P('/tmp/service-diag.c').write_text(s)
subprocess.run(['/usr/bin/gcc','-O2','-static','/tmp/service-diag.c','-o','/usr/local/lib/stand/service-launch.new'],check=True)
P('/usr/local/lib/stand/service-launch.new').replace('/usr/local/lib/stand/service-launch')
sys.path.insert(0,'/usr/local/lib/stand');import stand,codeboundary
stand.POLICY=codeboundary
new=P('/var/lib/stand/dev-add');old=stand.current_dir()
stand.activate(stand.load(new),new,stand.load(old),old)
time.sleep(2)
subprocess.run(['/usr/bin/journalctl','-u','stand-development','--no-pager','-n','10'])
subprocess.run(['/usr/bin/systemctl','show','stand-development.service','-p','CapabilityBoundingSet','-p','User','-p','SystemCallFilter','-p','SecureBits'])
