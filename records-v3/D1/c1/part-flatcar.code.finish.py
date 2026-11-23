import csv,os,collections
from pathlib import Path
base=Path('D1/c1'); p=base/'part-flatcar.code.tsv'
rows=[r for r in csv.DictReader(open('D1/in/part-flatcar.tsv'),delimiter='\t') if r['kind']=='L2:executable-code-outside-packages']
old={r['id'] for r in csv.DictReader(open(p),delimiter='\t')}
grub='https://raw.githubusercontent.com/flatcar/scripts/main/build_library/grub_install.sh'
manual='https://www.gnu.org/software/grub/manual/grub/grub.html'
bash='https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files'
index='https://raw.githubusercontent.com/rhboot/grub2/master/grub-core/Makefile.am'
manual_decisions={
'core.img':('MUST','S2.2-9','Provides GRUB’s BIOS core bootloader.','The core image is bootloader program code; the program requirement applies regardless of installation location.'),
'boot.img':('MUST','S2.2-9','Provides BIOS first-stage bootloader code.','The first-stage boot image is a program used to start GRUB; S2.2-9 requires recording programs.'),
'mbr.bin':('HOLE','S2.2-1,S2.2-2,S2.2-6','Preserves a snapshot of patched MBR boot code for restoration.','Restoration uses saved boot code, while the snapshot records past bytes. The text does not define whether its records-of-the-past exemption includes functional recovery snapshots.'),
'grub.cfg.tar':('UNKNOWN','S2.2-10,S2.2-13,S3-2','Supplies build-time GRUB configuration archive; installed-copy consumers are unestablished.','The installer embeds this archive into bootloader images. No evidence establishes later consumption or functional dependence on this separate installed archive.'),
'grubx64.efi':('MUST','S2.2-9','Runs the EFI GRUB bootloader.','The EFI GRUB image is a bootloader program; S2.2-9 requires recording it.'),
'mmx64.efi':('MUST','S2.2-9','Runs MokManager for EFI machine-owner key management.','MokManager is an EFI program; S2.2-9 requires recording it.'),
'bootx64.efi':('MUST','S2.2-9','Runs shim as the default EFI bootloader.','Shim is a bootloader program; S2.2-9 requires recording it.'),
'pvboot-x86_64.elf':('MUST','S2.2-9','Runs the Xen paravirtualized GRUB bootloader.','The installed Xen bootloader is program code for this computer; S2.2-9 requires recording it.'),
'menu.lst':('MUST','S2.2-1,S2.2-2,S2.2-13','Selects the Xen GRUB bootloader for legacy chainloading.','Its kernel directive determines which bootloader starts; removal loses the configured chainloading behavior.'),
'00-prompt-command.sh':('MUST','S2.2-10,S2.2-13','Initializes Bash PROMPT_COMMAND during login shell startup.','This shell drop-in executes commands with Bash’s rights; code remains code when configuring a variable.'),
'gawk.sh':('MUST','S2.2-10','Defines shell functions for adjusting AWKPATH and AWKLIBPATH.','The shell executes startup function definitions with its own rights; S2.2-10 expressly includes shell startup files.'),
'gawk.csh':('MUST','S2.2-10','Defines shell helpers for adjusting AWKPATH and AWKLIBPATH.','The shell executes startup helper definitions with its own rights; S2.2-10 expressly includes shell startup files.')}
with open(p,'a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 for r in rows:
  if r['id'] in old:continue
  n=r['name']; leaf=n.rsplit('/',1)[1]; url=grub
  if n.endswith('.lst') and '/grub/' in n and leaf!='menu.lst':
   d,s,what,why='NOT','S2.2-7,S2.2-13','Supplies GRUB module discovery, selection, or dependency values.','These module-selection values configure only GRUB. S2.2-13 treats them as settings, and S2.2-7 explicitly exempts settings confined to one program.';url=index
  elif n.startswith('/etc/skel/'):
   d,s,what,why='UNKNOWN','S3-2','Provides a skeleton file copied into new account directories; actual commands unknown.','Inventory records the template pathname but not its contents; documentation explains copying, not whether this particular file contains behavior-changing commands.';url='https://man7.org/linux/man-pages/man8/useradd.8.html'
  elif n.startswith('/home/'):
   d,s,what,why='MUST','S2.2-10','Supplies Bash commands at shell startup or logout.','Bash executes this standard per-account shell file with its own rights; S2.2-10 expressly includes shell startup files.';url=bash
  elif leaf=='load.cfg':
   d,s,what,why='UNKNOWN','S2.2-10,S2.2-13,S3-2','Supplies build-time GRUB script; installed-copy consumers are unestablished.','The installer embeds this script into another object. No evidence establishes later execution or functional dependence on the separate installed source copy.'
  else:
   d,s,what,why=manual_decisions[leaf]
   if leaf.startswith('gawk.'):url='https://www.gnu.org/software/gawk/manual/html_node/Shell-Startup-Files.html'
   if leaf=='00-prompt-command.sh':url='https://raw.githubusercontent.com/gentoo/gentoo/master/app-shells/bash/files/profile.d/00-prompt-command.sh'
   if leaf=='menu.lst':url='https://raw.githubusercontent.com/flatcar/scripts/main/build_library/menu.lst'
  w.writerow([r['id'],d,s,what,'doc:'+url,why]);f.flush()
out=list(csv.DictReader(open(p),delimiter='\t'))
assert len(out)==len(rows)==466 and {x['id'] for x in out}=={x['id'] for x in rows}
assert len({x['id'] for x in out})==466
for x in out:
 assert x['decision'] in ['MUST','NOT','HOLE','UNKNOWN','MIXED']
 assert len(x['what_it_does'].split())<=15,(x['id'],'what')
 assert len(x['reason'].split())<=30,(x['id'],'reason')
print(collections.Counter(x['decision'] for x in out))
