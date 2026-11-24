import csv,json,collections
from pathlib import Path
BASE=Path('D1b/handoff/microos')
ROWS=list(csv.DictReader(open('D1b/in/part-microos.tsv'),delimiter='\t'))
OUT=Path('D1b/c1/part-microos.tsv')
FIELDS=['id','decision','sentences','what_it_does','basis','reason']
def append(i,decision,sentences,what,basis,reason):
    old=list(csv.DictReader(open(OUT),delimiter='\t')) if OUT.exists() else []
    if ROWS[i]['id'] in {r['id'] for r in old}:return
    assert len(what.split())<=15 and len(reason.split())<=30
    with OUT.open('a') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n')
        if not old and OUT.stat().st_size==0:w.writerow(FIELDS)
        w.writerow([ROWS[i]['id'],decision,sentences,what,basis,reason]);f.flush()
if __name__=='__main__':
    for i in range(22):
        r=ROWS[i]
        append(i,'UNKNOWN','S8.2-11,S8.2-12,S8.2-13,S8.2-17',('System account ' if i<2 else 'Access-control group ')+r['name'],'raw:D1b/handoff/microos/configuration-origin.tsv','Account databases lack creation history: whether this value was created during package installation or chosen subsequently determines default versus own-line coverage.')
    descriptions=['System-wide interactive shell startup code','GRUB menu header generator','Linux boot entry generator','Xen boot entry generator','Other-operating-system boot entry generator','UEFI next-boot entry generator','Login shell initialization code','C-shell GLib command completion code','Shell GLib command completion code','Ignition early-boot provisioning executable']
    for i,what in zip(range(283,293),descriptions):
        append(i,'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16',what,'raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','Snapshot RPM manifest identifies the supplying package; complete digest equals its original digest. Question one precedes executability; the supplying package line covers this file.')
    append(268,'UNKNOWN','S8.2-11,S8.2-13,S8.2-17','Sudo authorization to run commands as any user and group','raw:D1b/handoff/microos/raw/0042-sudo-root.out','Effective authorization is known; its supplying rule and installation history are not. Those facts distinguish a package default from an independently chosen access setting.')
    append(293,'UNKNOWN','S8.2-7,S8.2-11,S8.2-15','Persistent system configuration directory','raw:D1b/handoff/microos/raw/0004-filesystem.out','Directory metadata establish persistence, not original package contents or historical creator. No complete expansion accompanies this object; its snapshot label supplies neither fact.')
    append(294,'MIXED','S8.2-7,S8.2-8,S8.2-15,S8.2-16','Snapshot audit configuration and directories','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','audit-stop.rules,auditd.conf: INSTALLED-PACKAGE (equal digests); audit.rules,audit.rules.prev,plugins.d,rules.d: UNKNOWN (missing original contents, directory comparison or historical creator).')
    append(295,'UNKNOWN','S8.2-7,S8.2-11,S8.2-15,S8.2-17','Snapshot audit rule file','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','RPM lists this file without a usable original digest. Whether received unchanged, generated during installation, or chosen later is not established.')
    append(296,'UNKNOWN','S8.2-7,S8.2-11,S8.2-15,S8.2-17','Snapshot cryptographic policy selection and supporting directories','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','config has no usable original digest or creation event; directory entries have membership only. Installation source cannot establish whether current objects remain as received.')
    append(297,'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Snapshot GRUB menu generation scripts and documentation','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','All seventeen members match their supplying RPM package digests. Question one decides each member before code or material distinctions.')
    append(298,'MIXED','S8.2-7,S8.2-8,S8.2-15,S8.2-16','Snapshot logical volume configuration and supporting directories','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','lvm.conf,lvmlocal.conf: INSTALLED-PACKAGE (equal digests); archive,backup,cache,profile: UNKNOWN (directory membership alone does not establish unchanged receipt or subsequent creator).')
    append(299,'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Snapshot shell initialization scripts for gawk and GLib tools','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','All four members match gawk or glib2-tools package digests. Their supplying package lines cover them before the executable-code question.')
    append(300,'MIXED','S8.2-7,S8.2-8,S8.2-11,S8.2-15,S8.2-16','Snapshot SELinux configuration, markers and store directories','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','fixfiles_exclude_dirs,semanage.conf: INSTALLED-PACKAGE (equal digests); .autorelabel,.relabelled,config,final,selinux_modules_migrated-targeted,targeted: UNKNOWN (missing receipt comparison or historical origin).')
    append(742,'UNKNOWN','S8.2-7,S8.2-11,S8.2-13,S8.2-15,S8.2-17','Snapshot compiled SELinux access policy','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','Policy differs from the supplied package. Whether its values were chosen, generated during installation, or merely saved as historical policy is not established.')
    append(743,'MIXED','S8.2-7,S8.2-8,S8.2-15,S8.2-16','Snapshot TLS trust links and OpenSSL configuration','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','ct_log_list.cnf,openssl-orig.cnf,openssl.cnf: INSTALLED-PACKAGE (equal digests); ca-bundle.pem,certs,private: UNKNOWN (unrecorded link origin or directory integrity).')
    append(744,'MIXED','S8.2-7,S8.2-8,S8.2-15,S8.2-16','Snapshot package-manager configuration and supporting directories','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','needreboot,systemCheck,zypp.conf.README,zypper.conf: INSTALLED-PACKAGE (equal digests); credentials.d,multiversion.d,needreboot.d,repos.d,services.d,systemCheck.d,vars.d,vendors.d,zypp.conf.d: UNKNOWN (directory membership does not establish unchanged receipt).')
    append(745,'INSTALLED-PACKAGE','S8.2-6,S8.2-7,S8.2-8,S8.2-16','Snapshot Ignition initramfs provisioning module files','raw:D1b/handoff/microos/s4-microos-snapshot-files.tsv','All eighteen members match ignition package digests. Its package line covers code, service definitions, and configuration alike under question one.')
    append(746,'UNKNOWN','S8.2-7,S8.2-11,S8.2-15','GRUB environment block and boot-support directories','raw:D1b/handoff/microos/s4-microos-sources.tsv','grubenv is blank; directory metadata show persistence. Original package receipt and historical creators are missing, preventing distinction between obtained files, program records, and supplied material.')
