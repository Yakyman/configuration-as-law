rpm -qa 'gpg-pubkey*' --qf '%{NAME}-%{VERSION}-%{RELEASE}\t%{INSTALLTIME}\t%{SUMMARY}\n'
dnf -C history list

