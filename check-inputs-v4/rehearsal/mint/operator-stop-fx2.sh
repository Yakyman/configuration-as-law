(
job_session=$(cat "$HOME/.cal-rehearsal-actions/job.sid")
case "$job_session" in *[!0-9]*|"") exit 65;; esac
sudo -n pkill -TERM -s "$job_session" || :
sleep 3
sudo -n pkill -KILL -s "$job_session" || :
for attempt in 1 2 3 4 5; do
 if sudo -n sh -c 'pgrep -s "$1" >/dev/null; result=$?; case "$result" in 0) exit 10;; 1) exit 11;; *) exit 70;; esac' sh "$job_session"; then
  check_status=0
 else
  check_status=$?
 fi
 case "$check_status" in
  11) exit 0;;
  10) sleep 1;;
  *) echo "action session check failed" >&2; exit 70;;
 esac
done
echo "action session remains after termination" >&2
exit 70

) && printf "%s\n" 143 > "$HOME/.cal-rehearsal-actions/done"
