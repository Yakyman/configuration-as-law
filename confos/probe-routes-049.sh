#!/bin/bash
# Builder probe on a copy of the pristine 0.49 disk: the routes and attempts of the
# search's last valid catalogue (release 0.32, search/REQUESTS.md entry 1) that no
# later builder gate names — route 111 (APT_CONFIG hook), attempts 202 (apt-mark
# hold as root) and 234 (root crontab for the account) — with the 0.49 command
# paths, and three queries the case party's probes used. Prints what happened;
# the lines starting RESULT are the findings. Not an acceptance.
set -uo pipefail
cd "$(dirname "$0")"
exec >logs/routes-0.49.log 2>&1
source slots.sh
image=images/routes-049.qcow2
trap 'confos_stop_reserved; rm -f "$image"' EXIT
test ! -e "$image" || exit 1
cp --reflink=auto images/confos-0.49-clean.qcow2 "$image"
confos_reserve_guest
guest(){ ssh -F /dev/null -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=3 -o ServerAliveInterval=2 -o ServerAliveCountMax=3 -i private/login -p 22467 user@127.0.0.1 "$@"; }
expected=$(sha256sum examples/development.conf | cut -d' ' -f1)
confos_boot_reserved "$image" 22467 3072 logs/routes-049.serial
for attempt in {1..120};do
 if [ "$(guest 'confos status' 2>/dev/null || true)" = "APPLIED $expected" ];then break;fi
 sleep 2
done
test "$(guest 'confos status')" = "APPLIED $expected" || { echo 'NOT READY';exit 1; }
run(){ echo "=== $1";shift;guest "$@";echo "--- exit $?"; }
before=$(guest 'sha256sum /state/declaration.conf /var/lib/dpkg/status 2>&1')
run 'route 111 by name' 'mkdir -p r111/l/partial r111/c/archives/partial && cd r111 && printf '"'"'APT::Update::Pre-Invoke {"touch /tmp/mark-111";};\nDir::State::Lists "/home/user/r111/l";\nDir::Cache "/home/user/r111/c";\nDebug::NoLocking "true";\n'"'"' > a.conf && APT_CONFIG=/home/user/r111/a.conf apt-get update; ls -la /tmp/mark-111'
run 'route 111 by full path' 'cd r111 && APT_CONFIG=/home/user/r111/a.conf /usr/bin/apt-get update; ls -la /tmp/mark-111'
run 'route 111 by full path as root' 'cd r111 && sudo -n env APT_CONFIG=/home/user/r111/a.conf /usr/bin/apt-get update; ls -la /tmp/mark-111'
if guest 'test -e /tmp/mark-111';then echo 'RESULT route 111: RAN';else echo 'RESULT route 111: refused, no mark';fi
run 'attempt 202' 'sudo -n apt-mark hold cron; sudo -n apt-mark showhold; sudo -n /usr/bin/apt-mark hold cron; apt-mark showhold'
if [ -n "$(guest 'apt-mark showhold 2>/dev/null; sudo -n apt-mark showhold 2>/dev/null')" ];then echo 'RESULT attempt 202: a hold is in force';else echo 'RESULT attempt 202: no hold in force';fi
run 'attempt 234' 'printf "* * * * * /bin/touch /tmp/mark-234\n" > ct && sudo -n crontab -u user ct; sudo -n crontab -u user -l; crontab ct; crontab -l'
echo 'waiting 70 s for a cron run'
sleep 70
if guest 'test -e /tmp/mark-234';then echo 'RESULT attempt 234: RAN';else echo 'RESULT attempt 234: no crontab ran';fi
run 'query timedatectl --value' 'timedatectl show -p Timezone --value; timedatectl show -p Timezone'
run 'query systemctl is-enabled of a declared service' 'systemctl is-enabled sleeper; confos services'
run 'query full-path refusals' '/usr/bin/apt-get --version; /usr/sbin/sysctl -n kernel.ostype; sysctl -n kernel.ostype; /usr/bin/hostnamectl --static; hostnamectl --static; sudo -n /usr/sbin/visudo -c'
after=$(guest 'sha256sum /state/declaration.conf /var/lib/dpkg/status 2>&1')
if [ "$before" = "$after" ];then echo 'RESULT declaration text and package status unchanged';else echo 'RESULT CHANGED';printf '%s\n%s\n' "$before" "$after";fi
echo 'ROUTES PROBE END'
