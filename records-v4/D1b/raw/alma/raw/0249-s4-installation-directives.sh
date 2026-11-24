for file in /root/anaconda-ks.cfg /root/original-ks.cfg; do
 if test -f "$file"; then
  printf 'FILE %s\n' "$file"
  awk '/^(network|bootloader|firewall|selinux|services|group|user|firstboot|keyboard|lang|timezone)( |$)/ { gsub(/--(password|rootpw|passphrase|wpakey)(=| )[[:graph:]]+/, "--credential=[REDACTED]"); print }' "$file"
 fi
done

