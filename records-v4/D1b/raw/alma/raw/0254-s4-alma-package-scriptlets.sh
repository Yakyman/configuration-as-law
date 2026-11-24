rpm -qa --qf '%{NAME}\n' | LC_ALL=C sort -u | while IFS= read -r package; do
 case "$package" in setup|systemd|NetworkManager|firewalld|alsa-utils|selinux-policy*|rpm|gdm|dconf) printf 'PACKAGE %s\n' "$package"; rpm -q --scripts "$package" ;; esac
done

