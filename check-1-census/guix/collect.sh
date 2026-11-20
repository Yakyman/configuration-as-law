#!/usr/bin/env bash
# Guest root only. Every command records status; mandatory failures cause exit 1 after tar.
set -u
export LC_ALL=C
OUT=/tmp/w1-census
CENSUS_USER=${CENSUS_USER:-guest}
mkdir -p "$OUT"
exec 2>"$OUT/collector-errors.txt"
failed=0
run() {
  local requirement=$1 name=$2 rc
  shift 2
  "$@" >"$OUT/$name" 2>"$OUT/$name.stderr"; rc=$?
  printf '%s\t%s\t%s\n' "$requirement" "$name" "$rc" >>"$OUT/command-status.tsv"
  if [ "$rc" -ne 0 ] && [ "$requirement" = mandatory ]; then failed=1; fi
  return 0
}
printf 'requirement\toutput\texit_code\n' >"$OUT/command-status.tsv"
run mandatory time.txt date -u --iso-8601=seconds
run mandatory os-release cat /etc/os-release
run mandatory uname.txt uname -a
run optional uptime.txt uptime
run mandatory mounts.txt findmnt -rn -o TARGET,SOURCE,FSTYPE,OPTIONS
GETENT=$(command -v getent || true)
if [ -z "$GETENT" ]; then
  for p in /gnu/store/*glibc*/bin/getent; do
    [ ! -x "$p" ] || { GETENT=$p; break; }
  done
fi
printf '%s\n' "$GETENT" > "$OUT/getent-path.txt"
run mandatory nsswitch.txt cat /etc/nsswitch.conf
run mandatory accounts.txt "$GETENT" passwd
run mandatory groups.txt "$GETENT" group
run mandatory processes.txt ps -ww -eo pid,ppid,user,comm,args
for p in /proc/[0-9]*; do
  printf '%s\t%s\t%s\n' "${p##*/}" "$(cat "$p/comm" 2>/dev/null)" "$(readlink "$p/exe" 2>/dev/null)"
done >"$OUT/process-executables.tsv"
for p in /bin /sbin /lib /lib64 /home /root /usr/local /opt /srv; do
  [ ! -L "$p" ] || printf '%s\t%s\n' "$p" "$(readlink -f "$p")"
done >"$OUT/path-aliases.tsv"
run mandatory modules.txt lsmod
while read -r m rest; do
  [ "$m" = Module ] && continue
  p=$(modinfo -n "$m" 2>/dev/null)
  printf '%s\t%s\n' "$m" "$(readlink -f "$p")"
done <"$OUT/modules.txt" >"$OUT/module-files.tsv"
run mandatory device-drivers.tsv find /sys/devices -name driver -type l -printf '%p\t%l\n'
echo guix >"$OUT/package-manager.txt"
printf '%s\n' "$CENSUS_USER" >"$OUT/census-user.txt"
home=$("$GETENT" passwd "$CENSUS_USER" | cut -d: -f6)
run mandatory guix-version.txt guix --version
run optional guix-channels.scm guix describe --format=channels
run optional guix-system-description.txt guix system describe
run mandatory current-system.txt readlink -f /run/current-system
run mandatory system-closure.txt guix gc --requisites "$(readlink -f /run/current-system)"
run mandatory system-generations.txt guix system list-generations
run mandatory system-profile.txt guix package -p /run/current-system/profile -I
run optional root-profile.txt guix package -I
run mandatory user-profile.txt su - "$CENSUS_USER" -c 'guix package -I'
run mandatory user-closure.txt guix gc --requisites "$(readlink -f "$home/.guix-profile")"
run mandatory user-generations.txt su - "$CENSUS_USER" -c 'guix package --list-generations'
run optional root-generations.txt guix package --list-generations
run mandatory store-top-level.txt find /gnu/store -mindepth 1 -maxdepth 1 -printf '%p\n'
run mandatory guix-profiles.tsv find /var/guix/profiles "$home" /root -maxdepth 5 -type l -printf '%p\t%l\n'
run mandatory system-config.txt cat /run/current-system/configuration.scm
run mandatory root-config.txt cat /etc/config.scm
run mandatory herd-status.txt herd status
run optional herd-detailed-status.txt herd status root
run optional herd-log.txt herd log
run optional mcron-schedule.txt herd schedule mcron
run optional shepherd-timer-log-cleanup.txt herd status log-cleanup
run optional shepherd-timer-log-rotation.txt herd status log-rotation
run optional user-herd-status.txt su - "$CENSUS_USER" -c 'herd status'
run optional user-mcron-schedule.txt su - "$CENSUS_USER" -c 'herd schedule mcron'
# Resolve and snapshot generated config files; avoid copying the whole closure.
mkdir -p "$OUT/configuration"
for p in /etc/config.scm /run/current-system/configuration.scm /run/current-system/parameters /run/current-system/activate /run/current-system/profile/manifest "$home/.guix-profile/manifest" /root/.guix-profile/manifest /run/current-system/shepherd.conf /etc/shepherd.scm /etc/mcron /etc/guix /etc/skel /etc/passwd /etc/group "$home/.guix-home" "$home/.config/guix/home.scm" "$home/home.scm"; do
  if [ -e "$p" ]; then
    printf '%s\t%s\n' "$p" "$(readlink -f "$p")" >>"$OUT/configuration-paths.tsv"
    case "$p" in
      "$home/.guix-home") run optional home-closure.txt guix gc --requisites "$(readlink -f "$p")"
        run optional home-profile.txt guix package -p "$p/profile" -I
        run optional home-generations.txt su - "$CENSUS_USER" -c 'guix home list-generations'
        run optional home-description.txt su - "$CENSUS_USER" -c 'guix home describe' ;;
      *) cp -LR --parents "$p" "$OUT/configuration/" ;;
    esac
  fi
done
# Small synthetic-user settings: provenance evidence for Home/skel versus day edits.
for p in "$home/.bashrc" "$home/.bash_profile" "$home/.profile" "$home/.vimrc" "$home/home.scm" "$home/.config/w1/declared-note" /etc/skel/.bashrc /etc/skel/.bash_profile /etc/skel/.profile; do
  if [ -f "$p" ]; then
    printf '\n### %s -> %s\n' "$p" "$(readlink -f "$p")"
    sha256sum "$p"
    cat "$p"
  fi
done >"$OUT/user-settings.txt"
# Guix 1.5 keeps Shepherd configuration in a store path referenced by boot;
# it is not /run/current-system/shepherd.conf. Retain exact closure source paths.
grep -E '/gnu/store/.*-shepherd.*\.(scm|conf)$' "$OUT/system-closure.txt" | sort -u >"$OUT/service-source-paths.txt"
while read -r p; do [ ! -f "$p" ] || cp --parents "$p" "$OUT/configuration/"; done <"$OUT/service-source-paths.txt"
cp -L /run/current-system/boot "$OUT/system-boot.scm"
# Runtime timer details are included among service status records.
awk '$1 == "+" || $1 == "*" || $1 == "-" { print $2 }' "$OUT/herd-status.txt" | while read -r service; do
  printf '\n### %s\n' "$service"
  herd status "$service"
done >"$OUT/herd-all-service-status.txt" 2>"$OUT/herd-all-service-status.stderr"
run optional log-files.tsv find /var/log -maxdepth 3 -type f -printf '%p\t%s\n'
# Activation references generated account/service setup source files.
if [ -e /run/current-system/activate ]; then
  grep -oE '/gnu/store/[^" ]+\.scm' /run/current-system/activate | sort -u >"$OUT/activation-source-paths.txt"
  while read -r p; do [ ! -f "$p" ] || cp --parents "$p" "$OUT/configuration/"; done <"$OUT/activation-source-paths.txt"
fi
for p in /var/log/messages /var/log/shepherd.log /var/log/guix-daemon.log; do
  [ ! -f "$p" ] || { printf '\n### %s\n' "$p"; tail -n 250 "$p"; }
done >"$OUT/log-tail.txt"
printf '%s\n' /etc /var /opt /usr/local /srv /home /root /boot /var/guix >"$OUT/walk-roots.txt"
findmnt -rn -o TARGET,FSTYPE | awk '$1 ~ /^\/(etc|var|opt|usr\/local|srv|home|root|boot)\// && $2 !~ /^(proc|sysfs|devtmpfs|devpts|cgroup2?)$/ {print $1}' >>"$OUT/walk-roots.txt"
: >"$OUT/files-unsorted.tsv"
while read -r root; do
  [ -e "$root" ] || continue
  [ ! -L "$root" ] || root=$(readlink -f "$root")
  find "$root" -xdev -printf '%y\t%p\t%l\t%s\n' >>"$OUT/files-unsorted.tsv" 2>>"$OUT/walk-errors.txt"
  rc=$?; printf 'mandatory\twalk:%s\t%s\n' "$root" "$rc" >>"$OUT/command-status.tsv"
  [ "$rc" -eq 0 ] || failed=1
done <"$OUT/walk-roots.txt"
sort -u "$OUT/files-unsorted.tsv" >"$OUT/files.tsv"
unlink "$OUT/files-unsorted.tsv"
date -u --iso-8601=seconds >"$OUT/end-time.txt"
printf '%s\n' "$failed" >"$OUT/mandatory-failure.txt"
tar -C /tmp -czf /tmp/w1-census.tar.gz w1-census || exit 1
exit "$failed"
