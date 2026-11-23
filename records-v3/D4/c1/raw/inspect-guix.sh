#!/bin/sh
export LC_ALL=C
printf 'UTC='; date -u +%FT%TZ
guix --version | head -1
sha256sum /etc/config.scm
command -v guix useradd usermod
printf 'account uid/gid/shell: '; getent passwd user | cut -d: -f1,3,4,7
getent group users wheel | cut -d: -f1,3
MANWIDTH=80 man usermod | col -b | sed -n '/^NAME/,/^OPTIONS/p'
MANWIDTH=80 man usermod | col -b | sed -n '/-g, --gid/,/-G, --groups/p'
