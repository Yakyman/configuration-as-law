#!/bin/sh
find /var/log/zypp /var/log/YaST2 /var/log/transactional-update /var/log/combustion /var/lib/combustion -type f -size -16M -exec grep -aEn -- 'grubenv|editenv|saved_entry|next_entry' {} +
command -v grub2-editenv >/dev/null && grub2-editenv /boot/grub2/grubenv list
rpm -q --scripts grub2 grub2-x86_64-efi
