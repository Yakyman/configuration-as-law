runuser -u user -- env HOME=/home/user XDG_RUNTIME_DIR=/run/user/1000 sh -c 'command -v rpm >/dev/null 2>&1 || exit 127; rpm -qa --qf '"'"'%{NAME}\t%{VERSION}-%{RELEASE}\t%{ARCH}\n'"'"''
