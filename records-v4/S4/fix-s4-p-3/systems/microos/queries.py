# Targeted read-only query inputs. Output is transient inventory material.
UNITS='dbus-org.freedesktop.nm-dispatcher.service jeos-firstboot.service network.service NetworkManager-dispatcher.service NetworkManager-wait-online.service NetworkManager.service mdcheck_continue.timer'
FACTS={
'M03':('systemctl|preset|enable|disable|symlink', ['/etc/systemd/system'], 'NetworkManager|jeos-firstboot|mdcheck_continue|network.service'),
'M05':('sudoers|visudo|sudo-access', ['/etc/sudoers','/etc/sudoers.d','/usr/etc/sudoers'], 'sudoers|visudo'),
'M11':('grubenv|grub2-editenv|grub-editenv|saved_entry|next_entry', ['/boot/grub2/grubenv'], 'grubenv|editenv|saved_entry|next_entry'),
'M14':('ca-certificates|update-ca-certificates|trust anchor|p11-kit|openssl', ['/var/lib/ca-certificates/openssl','/etc/pki/trust'], 'ca-certificates|update-ca-certificates|p11-kit|trust anchor'),
}
def queries():
 import shlex
 result=[]
 for fact,(pattern,paths,source_pattern) in FACTS.items():
  result.append((fact,'journal',"journalctl --no-pager --all -o cat --grep="+shlex.quote(pattern)))
  audit='\n'.join('ausearch --input-logs --file '+shlex.quote(p)+' --interpret; printf "query_exit=%s\\n" "$?"' for p in paths)
  result.append((fact,'audit','command -v ausearch || exit 127\n'+audit))
  history="find /var/log/zypp /var/log/YaST2 /var/log/transactional-update /var/log/combustion /var/lib/combustion -type f -size -16M -exec grep -aEn -- "+shlex.quote(source_pattern)+" {} +"
  if fact=='M03': history+='\nsystemctl show '+UNITS+' -p Id -p UnitFileState -p UnitFilePreset\nrpm -q --scripts systemd NetworkManager mdadm jeos-firstboot'
  if fact=='M05': history+='\nrpm -q --scripts sudo\nrpm -V sudo\nfor p in /etc/sudoers /usr/etc/sudoers /etc/sudoers.d/*; do test ! -f "$p" || sha256sum "$p"; done'
  if fact=='M11': history+='\ncommand -v grub2-editenv >/dev/null && grub2-editenv /boot/grub2/grubenv list\nrpm -q --scripts grub2 grub2-x86_64-efi'
  if fact=='M14': history+='\ncommand -v trust >/dev/null && trust list\ncommand -v pkg-config >/dev/null && pkg-config --variable p11_trust_paths p11-kit-1\ncommand -v openssl >/dev/null && openssl version -d\nprintf "CURRENT_FD_BEGIN\\n"\nfor p in /proc/[0-9]*/fd/*; do t=$(readlink "$p") || continue; case "$t" in /var/lib/ca-certificates/openssl/*|/etc/ssl/certs/*|/etc/pki/trust/*) printf "%s\\t%s\\n" "$p" "$t";; esac; done\nprintf "CURRENT_FD_END\\nCURRENT_MAPS_BEGIN\\n"\ngrep -lE "p11-kit-trust|/var/lib/ca-certificates/openssl/|/etc/ssl/certs/|/etc/pki/trust/" /proc/[0-9]*/maps\nprintf "CURRENT_MAPS_END\\n"'
  result.append((fact,'installation-current',history))
 return result
