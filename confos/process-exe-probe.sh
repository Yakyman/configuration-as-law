#!/bin/bash
# Guest part of test-queries-055.sh. Run as the ordinary account; it uses `sudo -n`.
#   process-exe-probe.sh readable|unreadable   the whole probe
#   process-exe-probe.sh scan                  (as root) every process whose executable cannot be read
#   process-exe-probe.sh find NAME             (as root) newest process with that command nameset -u
mode=$1
if [ "$mode" = scan ]; then
    for d in /proc/[0-9]*; do
        p=${d#/proc/}
        rest=$(sed 's/^.*) //' "$d/stat" 2>/dev/null) || continue
        set -- $rest
        state=${1:-}; parent=${2:-}
        # kernel threads execute no file
        if [ "$p" = 2 ] || [ "$parent" = 2 ]; then continue; fi
        if [ -z "$(readlink "$d/exe" 2>/dev/null)" ] && [ -d "$d" ]; then
            printf 'UNREADABLE pid=%s state=%s label=%s args=[%s]\n' "$p" "$state" \
                "$(cat "$d/attr/current" 2>/dev/null)" "$(tr '\0' ' ' <"$d/cmdline" 2>/dev/null)"
        fi
    done
    exit 0
fi
if [ "$mode" = find ]; then
    found=
    for d in /proc/[0-9]*; do
        if [ "$(cat "$d/comm" 2>/dev/null)" = "$2" ]; then
            p=${d#/proc/}
            if [ -z "$found" ] || [ "$p" -gt "$found" ]; then found=$p; fi
        fi
    done
    echo "$found"
    exit 0
fi
self=/usr/local/bin/process-exe-probe.sh
export XDG_RUNTIME_DIR=/run/user/$(id -u)
bad=0
check() {  # check TEXT STATUS: a requirement of the repaired release
    if [ "$2" = 0 ]; then echo "OK   $1"; else echo "FAIL $1"; bad=$((bad+1)); fi
}
echo '== processes whose executable root cannot read, before the application starts'
sudo -n "$self" scan | tee /tmp/exe-before
echo '== the recorded application, started as the case starts it'
( timeout -s KILL 40 flatpak run io.mpv.Mpv --idle=yes --vo=null --ao=null >/tmp/exe-mpv.out 2>&1 & )
started=$SECONDS
pid=
while [ -z "$pid" ] && [ $((SECONDS-started)) -lt 30 ]; do
    sleep 2
    pid=$(sudo -n "$self" find mpv)
done
echo "mpv pid=[$pid] label=[$(sudo -n cat "/proc/$pid/attr/current" 2>&1)]"
first=$(sudo -n readlink "/proc/$pid/exe" 2>&1)
echo "sudo -n readlink /proc/$pid/exe -> [$first] status $?"
# The path is the one of the application's own mount namespace; through the process's
# root it is the file of the recorded application in the immutable store.
inside=$(sudo -n sha256sum "/proc/$pid/root$first" 2>&1 | cut -d' ' -f1)
stored=$(sha256sum "/usr/lib/confos/flatpak/app/io.mpv.Mpv/x86_64/stable/active/files${first#/app}" 2>&1 | cut -d' ' -f1)
echo "checksum through /proc/$pid/root$first: [$inside]"
echo "checksum of the stored file of the recorded application: [$stored]"
echo '== after the front process was killed by its timeout'
while [ $((SECONDS-started)) -lt 46 ]; do sleep 2; done
cat /tmp/exe-mpv.out
pid2=$(sudo -n "$self" find mpv)
echo "mpv pid=[$pid2]"
second=$(sudo -n readlink "/proc/$pid2/exe" 2>&1)
echo "sudo -n readlink /proc/$pid2/exe -> [$second] status $?"
sudo -n "$self" scan | tee /tmp/exe-after
echo '== queries'
list=$(flatpak list --app --columns=application 2>&1); list_status=$?
echo "flatpak list --app --columns=application -> status $list_status: [$list]"
all=$(sudo -n flatpak list --all --columns=application,version,origin,installation,active,branch,arch 2>&1); all_status=$?
echo "sudo -n flatpak list --all --columns=… -> status $all_status:"; echo "$all"
ps=$(sudo -n podman ps -a --format json 2>&1); ps_status=$?
echo "sudo -n podman ps -a --format json -> status $ps_status: [$ps]"
images=$(sudo -n podman images --format json 2>&1); images_status=$?
echo "sudo -n podman images --format json -> status $images_status: [$images]"
plain=$(flatpak list 2>&1); plain_status=$?
echo "flatpak list -> status $plain_status"
refused=$(flatpak list --installation=other 2>&1); refused_status=$?
echo "flatpak list --installation=other -> status $refused_status: [$refused]"
# The account ends its own process; the superuser of a session has no capability to signal it.
[ -n "$pid2" ] && kill -KILL "$pid2"
if [ "$mode" = unreadable ]; then
    # control on a release before the repair: the report must be reproduced
    if [ -n "$pid" ] && [ "${first#/}" = "$first" ] && [ -n "$pid2" ] && [ "${second#/}" = "$second" ] && grep -q 'mpv' /tmp/exe-after; then
        echo 'CONTROL REPRODUCED: root cannot read the executable of the recorded application'; exit 0
    fi
    echo 'CONTROL NOT REPRODUCED'; exit 1
fi
[ -n "$pid" ]; check 'the recorded application runs' $?
[ "${first#/}" != "$first" ]; check "root reads the executable of the running application: $first" $?
[ ${#inside} = 64 ] && [ "$inside" = "$stored" ]; check 'that path, through the root of the process, is the stored file of the recorded application' $?
[ -n "$pid2" ] && [ "${second#/}" != "$second" ]; check "the same after the front process was killed (process $pid2): $second" $?
[ ! -s /tmp/exe-before ]; check 'no process with an unreadable executable before' $?
[ ! -s /tmp/exe-after ]; check 'no process with an unreadable executable after' $?
[ "$list_status" = 0 ] && [ "$list" = io.mpv.Mpv ]; check 'flatpak list --app --columns=application names the recorded application' $?
[ "$all_status" = 0 ] && printf '%s\n' "$all" | grep -q '^io.mpv.Mpv'; check 'flatpak list --all with columns answers for root' $?
[ "$ps_status" = 0 ] && [ "$ps" = '[]' ]; check "root's podman ps -a --format json is an empty list" $?
[ "$images_status" = 0 ] && [ "$images" = '[]' ]; check "root's podman images --format json is an empty list" $?
[ "$plain_status" = 0 ]; check 'plain flatpak list still answers' $?
[ "$refused_status" != 0 ]; check 'an option that names another installation is refused' $?
if [ "$bad" = 0 ]; then echo 'PROCESS EXE PROBE PASS'; exit 0; fi
echo "PROCESS EXE PROBE FAIL ($bad)"; exit 1
