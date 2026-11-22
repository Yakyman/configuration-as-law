#!/bin/sh
set -eu
cd "${CAL_LAB_ROOT:-$HOME/VMs/cal-1122}"
xorriso -osirrox on -indev images/guix.iso -extract /gnu/store/pbpfl2ll5qz36bqfnl3g3vvag764714h-linux-libre-6.17.12/bzImage install/guix/bzImage -extract /gnu/store/lwalc924v2jaa3r029qk19v6685d6snn-raw-initrd/initrd.cpio.gz install/guix/initrd
xorriso -as mkisofs -o install/guix/input.iso -graft-points config.scm=install/guix/config.scm install.sh=install/guix/install.sh
qemu-img create -f qcow2 C1/base/guix.qcow2 32G
