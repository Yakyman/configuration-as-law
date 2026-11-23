import csv,collections
p='A1/c1/part-4.3.tsv';rs=list(csv.DictReader(open(p),delimiter='\t'));updates={}
def m(i,what,reason,url,s='S2.2-1,S2.2-2'):updates['guix-'+i]=dict(decision='MUST',sentences=s,what_it_does=what,reason=reason,basis='doc:'+url)
m('ea2b617ba5','Supplies the persistent system hostname.','The configured system identity affects network and application behavior beyond one program.','https://raw.githubusercontent.com/lfam/guix/master/gnu/system.scm')
m('1809ee6527','Supplies stable machine identity used for interprocess communication.','Cross-process identity and same-machine detection depend on this value.','https://dbus.freedesktop.org/doc/dbus-specification.html')
m('6b4026dd02','Exposes the current mount namespace through the conventional mount-table path.','Removing the alias prevents mount-table queries through this interface; it is an operational link.','https://man7.org/linux/man-pages/man5/proc_pid_mounts.5.html')
m('6a38277ef0','Identifies the operating system for applications and scripts.','Applications use identification fields to select system-specific behavior; they are not confined to one program.','https://man7.org/linux/man-pages/man5/os-release.5.html')
m('8c833da179','Supplies the timezone name to GLib and other applications.','Shared timezone lookup affects multiple applications; the source explicitly identifies its consumers.','https://raw.githubusercontent.com/lfam/guix/master/gnu/system.scm')
m('31edaf98e6','Seeds the kernel random generator during system boot.','Removing saved seed changes kernel initialization and credited entropy, affecting system-wide random generation.','https://raw.githubusercontent.com/lfam/guix/master/gnu/services/base.scm')
m('4d882498fa','Configures authentication modules and privilege-granting policy for applications.','Authentication policy controls login and privileges across applications; exact values are unnecessary to establish this role.','https://man7.org/linux/man-pages/man5/pam.d.5.html','S2.2-1,S2.2-15')
m('cafee5136d','Configures account creation and password-management policy defaults.','These defaults govern account operations and login policy, beyond one program interface.','https://man7.org/linux/man-pages/man5/login.defs.5.html','S2.2-1,S2.2-15')
m('d80ad67f85','Defines authorization rules for privileged system operations.','Policy determines which system actions callers may perform; executable rules also run with the authorization manager rights.','https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html','S2.2-1,S2.2-10,S2.2-15')
m('561d6a5935','Configures device naming, permissions, properties, and event actions.','Device rules change system device access and behavior across programs.','https://man7.org/linux/man-pages/man7/udev.7.html')
m('df290cde86','Configures message-bus access policies and service activation.','Bus policies and activation determine interprocess communication and available services.','https://dbus.freedesktop.org/doc/dbus-daemon.1.html')
m('cfe66bc678','Stores account passwords, lock status, and aging controls.','Passwords need not be recorded, but login restrictions require recording; operational account-policy role makes the file mandatory.','https://man7.org/linux/man-pages/man5/shadow.5.html','S2.2-1,S2.2-15')
updates['guix-451d25b3c7']=dict(decision='MIXED',sentences='S2.2-4,S2.2-10,S2.2-13',what_it_does='Provides editor load-path code and an Info documentation index.',reason='MUST: emacs-subdirs contains executable Lisp; NOT: info-dir contains the generated documentation menu.',basis='doc:https://raw.githubusercontent.com/lfam/guix/master/guix/profiles.scm')
for r in rs:
 if r['id'] in updates:r.update(updates[r['id']])
 assert len(r['what_it_does'].split())<=15
 assert len(r['reason'].split())<=30
with open(p,'w') as f:
 w=csv.DictWriter(f,fieldnames=rs[0],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rs)
print(collections.Counter(r['decision'] for r in rs))
