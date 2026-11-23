find / \( -path /proc -o -path /sys -o -path /dev \) -prune -o -printf '%p\0%y\0%m\0%U\0%G\0%l\0'
