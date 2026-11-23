#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive
printf 'deb https://deb.debian.org/debian trixie-backports main\n' > /etc/apt/sources.list.d/b1-backports.list
apt-get update
apt-get -y dist-upgrade
apt-get -y install python3 linux-image-7.3.4+deb13-amd64=7.3.4-1~bpo13+1
printf 'SETUP_COMPLETE\n'
