import csv
rows=list(csv.DictReader(open('A1/in/part-4.tsv'),delimiter='\t'))
p='A1/c1/part-4.packages.tsv'
w=csv.writer(open(p,'w'),delimiter='\t',lineterminator='\n');w.writerow(['id','decision','sentences','what_it_does','basis','reason'])
def a(name,what,url,reason,s='S2.2-2,S2.2-10',d='MUST'):
 for r in rows:
  if '-'+name+'-' in r['name']:
   assert len(what.split())<=15 and len(reason.split())<=30
   w.writerow([r['id'],d,s,what,'doc:'+url,reason])
a('zbar-minimal','Decodes barcodes through native barcode-reader code.','https://zbar.sourceforge.net/api/','Removing the barcode library removes decoding code used with application rights.')
a('keybinder','Registers global keyboard shortcuts for GTK applications on X11.','https://github.com/kupferlauncher/keybinder','Native library code implements keyboard bindings with the calling application rights.')
a('libsrtp','Implements secure real-time transport encryption and authentication.','https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/telephony.scm','Native cryptographic protocol implementation executes with application rights.')
a('debianutils','Provides system utilities used by installation scripts and interactive users.','https://salsa.debian.org/debian/debianutils','Removing executable utilities removes available system operations.','S2.2-2,S2.2-9')
a('libmd','Implements BSD-compatible message-digest functions.','https://github.com/guillemj/libmd/blob/main/README','Native digest code runs with the rights of its caller.')
a('libxcrypt','Hashes passwords for authentication programs.','https://github.com/besser82/libxcrypt','This is executable password-hashing code, not exempt password material.')
a('python-minimal-wrapper','Provides unversioned Python command aliases and an executable configuration-query wrapper.','https://github.com/lfam/guix/blob/master/gnu/packages/python.scm','Removing wrappers prevents these command invocations; the shell wrapper also executes with interpreter rights.','S2.2-2,S2.2-10')
a('udftools','Creates and manages UDF filesystems and optical-media devices.','https://github.com/pali/udftools','Executable filesystem tools provide capabilities lost on removal.','S2.2-2,S2.2-9')
a('keyutils','Provides tools and library functions for kernel keyring management.','https://man7.org/linux/man-pages/man2/keyctl.2.html','Userspace code invokes kernel key management; removal removes these tools and library entry points.','S2.2-2,S2.2-9,S2.2-10')
a('iso-codes','Provides country, language, script, and currency names and translations.','https://salsa.debian.org/iso-codes-team/iso-codes','These lists and translations are reference content; their removal removes the names, not executable functionality.','S2.2-4','NOT')
a('libslirp','Implements user-mode networking for virtualizers, containers, and tools.','https://gitlab.com/qemu-project/libslirp/-/raw/master/README.md','Networking library runs in the host application with its rights; it is not confined guest code.')
a('glibc-utf8-locales','Supplies compiled UTF-8 locale definitions for application locale selection.','https://man7.org/linux/man-pages/man3/setlocale.3.html','Removing locale definitions makes those locales unavailable and changes shared character classification and formatting behavior.','S2.2-1,S2.2-2')
a('usb-modeswitch-data','Provides device switching configurations and automatic device-event rules.','https://www.draisberghof.de/usb_modeswitch/','Configuration and rules enable hardware mode changes; removing them prevents automatic supported-device switching.','S2.2-1,S2.2-2')
a('libnfs','Implements NFS client access in a native library.','https://github.com/sahlberg/libnfs','Native network-filesystem code runs with calling application rights.')
a('elfutils','Provides native ELF and debugging-data manipulation libraries.','https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/elf.scm','The default output contains executable native libraries; removing them breaks dependent object-file and debugging operations.')
a('cyrus-sasl','Implements pluggable authentication mechanisms for network applications.','https://www.cyrusimap.org/sasl/','Authentication implementation and plugins execute with application rights; they are not password content.')
a('libical','Implements iCalendar protocols and calendar-data processing.','https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/calendar.scm','This is executable calendar-processing library code, not calendar content.')
a('liburcu','Provides read-copy-update synchronization and concurrent data structures.','https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/datastructures.scm','Native synchronization code executes with the rights of applications using it.')
a('nilfs-utils','Creates, mounts, cleans, and manages NILFS filesystems and snapshots.','https://nilfs.sourceforge.io/en/manual.html','Executable filesystem management tools provide capabilities lost on removal.','S2.2-2,S2.2-9')
a('zix','Provides native data structures, allocation, threading, and filesystem utility code.','https://raw.githubusercontent.com/lfam/guix/master/gnu/packages/datastructures.scm','Native library code executes with calling application rights.')
a('bdb','Provides embedded key-value database storage and management functions.','https://www.oracle.com/database/technologies/related/berkeleydb.html','Database engine code executes with application rights; the exemption for database contents does not cover the engine.')
