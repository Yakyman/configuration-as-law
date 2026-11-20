#!/usr/bin/env bash
# Executed with guest root only; no host root operations.
set -u
export LC_ALL=C
OUT=/tmp/v1-census
mkdir -p "$OUT"
exec 2>"$OUT/collector-errors.txt"
date -u --iso-8601=seconds > "$OUT/time.txt"
cat /etc/os-release > "$OUT/os-release"
uname -a > "$OUT/uname.txt"
uptime > "$OUT/uptime.txt"
findmnt -rn -o TARGET,SOURCE,FSTYPE,OPTIONS > "$OUT/mounts.txt"
for p in /bin /sbin /lib /lib64 /home /root /usr/local /opt /srv; do
  [ -L "$p" ] && printf '%s\t%s\n' "$p" "$(readlink -f "$p")"
done > "$OUT/path-aliases.tsv"
getent passwd > "$OUT/accounts.txt"
getent group > "$OUT/groups.txt"
for f in /usr/share/base-passwd/passwd.master /usr/lib/passwd /usr/lib/sysusers.d/*.conf /etc/sysusers.d/*.conf /nix/store/*-users-groups.json; do
  [ -f "$f" ] || continue
  printf '\n### %s\n' "$f"
  cat "$f"
done > "$OUT/account-definitions.txt"
ps -ww -eo pid,ppid,user,comm,args > "$OUT/processes.txt"
for p in /proc/[0-9]*; do
  printf '%s\t%s\t%s\n' "${p##*/}" "$(cat "$p/comm" 2>/dev/null)" "$(readlink "$p/exe" 2>/dev/null)"
done > "$OUT/process-executables.tsv"
lsmod > "$OUT/modules.txt"
while read -r m rest; do
  [ "$m" = Module ] && continue
  p=$(modinfo -n "$m" 2>/dev/null)
  printf '%s\t%s\n' "$m" "$(readlink -f "$p")"
done < "$OUT/modules.txt" > "$OUT/module-files.tsv"
systemctl list-units --all --no-pager --plain > "$OUT/units.txt"
systemctl list-unit-files --no-pager --no-legend > "$OUT/unit-files.txt"
systemctl list-timers --all --no-pager > "$OUT/timers.txt"
systemctl list-units --all --no-pager --no-legend --plain | awk '{print $1}' | xargs -r -d '\n' systemctl show -p Id -p FragmentPath -p SourcePath -p DropInPaths -- > "$OUT/unit-paths.txt"
uid=$(id -u census)
loginctl show-user census -p Linger -p State > "$OUT/user-manager-state.txt"
for spec in 'list-units --all --plain' 'list-unit-files' 'list-timers --all'; do
  name=${spec%% *}
  runuser -u census -- env XDG_RUNTIME_DIR="/run/user/$uid" systemctl --user $spec --no-pager > "$OUT/user-$name.txt"
done
runuser -u census -- env XDG_RUNTIME_DIR="/run/user/$uid" bash -c 'systemctl --user list-units --all --no-pager --no-legend --plain | awk "{print \$1}" | xargs -r -d "\n" systemctl --user show -p Id -p FragmentPath -p SourcePath -p DropInPaths --' > "$OUT/user-unit-paths.txt"
sed -n -e 's/^FragmentPath=//p' -e 's/^DropInPaths=//p' "$OUT/unit-paths.txt" "$OUT/user-unit-paths.txt" | tr ' ' '\n' | sort -u | while read -r p; do
  [ -n "$p" ] && printf '%s\t%s\n' "$p" "$(readlink -f "$p")"
done > "$OUT/unit-realpaths.tsv"
if command -v dpkg-query >/dev/null; then
  echo dpkg > "$OUT/package-manager.txt"
  dpkg-query -W -f='${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' > "$OUT/packages.tsv"
  dpkg-query -L $(dpkg-query -W -f='${binary:Package}\n') | sort -u > "$OUT/package-files.txt"
  dpkg-query -W -f='${binary:Package}\n${Conffiles}\n' > "$OUT/conffiles.txt"
elif command -v rpm >/dev/null; then
  echo rpm-ostree > "$OUT/package-manager.txt"
  rpm -qa --qf '%{NAME}\t%{VERSION}-%{RELEASE}\t%{ARCH}\n' | sort > "$OUT/packages.tsv"
  rpm -qal | sort -u > "$OUT/package-files.txt"
  rpm-ostree status --json > "$OUT/rpm-ostree-status.json"
  ostree admin status > "$OUT/ostree-status.txt"
elif command -v nix-store >/dev/null; then
  echo nix > "$OUT/package-manager.txt"
  nix-store -qR /run/current-system | sort > "$OUT/system-closure.txt"
  nix-env -q --installed --out-path > "$OUT/root-profile.txt"
  runuser -u census -- nix-env -q --installed --out-path > "$OUT/user-profile.txt"
  nix-store -qR /home/census/.nix-profile | sort > "$OUT/user-closure.txt"
  find /nix/var/nix/profiles /home/census -maxdepth 4 -type l -printf '%p\t%l\n' > "$OUT/nix-profiles.tsv"
  find /nix/store -mindepth 1 -maxdepth 1 -printf '%p\n' | sort > "$OUT/store-top-level.txt"
  find /nix/store -type f -o -type l | sort > "$OUT/package-files.txt"
  cp "$OUT/store-top-level.txt" "$OUT/packages.tsv"
  cp -a /etc/nixos "$OUT/nixos-configuration"
  readlink -f /run/current-system > "$OUT/current-system.txt"
fi
# Include directory entries and symlinks; do not follow symlinks or cross mountpoints.
# Include local descendant mounts separately (e.g. /boot/efi).
printf '%s\n' /etc /var /opt /usr/local /srv /home /root /boot /nix/var > "$OUT/walk-roots.txt"
findmnt -rn -o TARGET,FSTYPE | awk '$1 ~ /^\/(etc|var|opt|usr\/local|srv|home|root|boot|nix\/var)\// && $2 !~ /^(proc|sysfs|devtmpfs|devpts|cgroup2?)$/ {print $1}' >> "$OUT/walk-roots.txt"
while read -r root; do
  [ -e "$root" ] || continue
  if [ -L "$root" ]; then root=$(readlink -f "$root"); fi
  find "$root" -xdev -printf '%y\t%p\t%l\t%s\n'
done < "$OUT/walk-roots.txt" | sort -u > "$OUT/files.tsv"
find /sys/devices -name driver -type l -printf '%p\t%l\n' > "$OUT/device-drivers.tsv"
journalctl -b --no-pager -n 250 > "$OUT/journal-tail.txt"
date -u --iso-8601=seconds > "$OUT/end-time.txt"
tar -C /tmp -czf /tmp/v1-census.tar.gz v1-census
