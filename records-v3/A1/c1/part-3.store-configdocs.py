import urllib.request,concurrent.futures,json
from bs4 import BeautifulSoup
sources={}
for n in ['tmpfiles.d','sysctl.d','systemd-system.conf','timesyncd.conf','coredump.conf','journald.conf','oomd.conf','logind.conf','systemd-sleep.conf','systemd.preset','systemd.generator','systemd.environment-generator','environment.d','vconsole.conf','locale.conf','os-release','hwdb','udev','systemd-halt']:
 sources[n]='https://www.freedesktop.org/software/systemd/man/latest/'+n+'.html'
for n,sec in [('hosts',5),('nsswitch.conf',5),('gai.conf',5),('host.conf',5),('fstab',5),('shells',5),('issue',5),('netgroup',5),('modprobe.d',5),('pam.conf',5)]:sources[n]=f'https://man7.org/linux/man-pages/man{sec}/{n}.{sec}.html'
sources.update({'nanorc':'https://www.nano-editor.org/dist/latest/nanorc.5.html','fontconfig':'https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html','ssh_config':'https://man.openbsd.org/ssh_config','sshd_config':'https://man.openbsd.org/sshd_config','sudoers':'https://www.sudo.ws/docs/man/sudoers.man/','nix.conf':'https://nix.dev/manual/nix/latest/command-ref/conf-file.html','nix-registry':'https://nix.dev/manual/nix/latest/command-ref/new-cli/nix3-registry.html','dhcpcd.conf':'https://man.archlinux.org/man/dhcpcd.conf.5.en','resolvconf.conf':'https://man.archlinux.org/man/resolvconf.conf.5.en','logrotate':'https://man7.org/linux/man-pages/man8/logrotate.8.html'})
def get(kv):
 k,u=kv
 try:
  s=BeautifulSoup(urllib.request.urlopen(u,timeout=6).read(),'html.parser').get_text(' ',strip=True)
  i=s.lower().find('description');return k,{'url':u,'excerpt':s[i:i+700]}
 except Exception as e:return k,{'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:d=dict(ex.map(get,sources.items()))
json.dump(d,open('A1/c1/part-3.store-configdocs.json','w'),indent=2)
for k,v in d.items():print(k,':',v.get('excerpt',v.get('error'))[:500])
