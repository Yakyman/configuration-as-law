cat /etc/os-release; printf "\nMOUNTS\n"; findmnt -rn -o TARGET,OPTIONS /usr
