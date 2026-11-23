#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get -y -t trixie-backports install linux-image-7.3.4+deb13-amd64=7.3.4-1~bpo13+1
printf 'BACKPORT_SETUP_COMPLETE\n'
