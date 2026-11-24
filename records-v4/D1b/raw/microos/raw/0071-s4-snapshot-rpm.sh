rpm --root /.snapshots/2/snapshot -qa --qf '[%{=NAME}@%{=VERSION}-%{=RELEASE}.%{=ARCH}\t%{FILENAMES}\t%{FILESIZES}\t%{FILEDIGESTS}\t%{=FILEDIGESTALGO}\t%{FILEMODES}\t%{FILELINKTOS}\n]'
