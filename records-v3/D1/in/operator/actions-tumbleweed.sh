#!/bin/bash
set -uo pipefail
as_root() { printf '%s\n' <REDACTED> | sudo -S -- "$@"; }
printf '\nACTION 01 BEGIN\n'
eval "$(printf %s YXNfcm9vdCB6eXBwZXIgLS1ub24taW50ZXJhY3RpdmUgaW5zdGFsbCBoZWxsbyBwb2RtYW4gZmxhdHBhawo= | base64 -d)"
action_rc=$?
printf 'ACTION 01 EXIT %s\n' "$action_rc"
printf '\nACTION 02 BEGIN\n'
eval "$(printf %s ZmxhdHBhayAtLXVzZXIgcmVtb3RlLWFkZCAtLWlmLW5vdC1leGlzdHMgZmxhdGh1YiBodHRwczovL2RsLmZsYXRodWIub3JnL3JlcG8vZmxhdGh1Yi5mbGF0cGFrcmVwbwo= | base64 -d)"
action_rc=$?
printf 'ACTION 02 EXIT %s\n' "$action_rc"
printf '\nACTION 03 BEGIN\n'
eval "$(printf %s ZmxhdHBhayAtLXVzZXIgaW5zdGFsbCAtLW5vbmludGVyYWN0aXZlIC15IGZsYXRodWIgb3JnLmdub21lLkNhbGN1bGF0b3IK | base64 -d)"
action_rc=$?
printf 'ACTION 03 EXIT %s\n' "$action_rc"
printf '\nACTION 04 BEGIN\n'
eval "$(printf %s YXNfcm9vdCBubWNsaSBjb25uZWN0aW9uIGFkZCB0eXBlIGV0aGVybmV0IGNvbi1uYW1lIGNhbC1zZWNvbmRhcnkgaWZuYW1lICcqJyA4MDItMy1ldGhlcm5ldC5tYWMtYWRkcmVzcyA1Mjo1NDowMDpjYToxMDowMiBpcHY0Lm1ldGhvZCBhdXRvIGlwdjQubmV2ZXItZGVmYXVsdCB5ZXMgaXB2Ni5tZXRob2QgZGlzYWJsZWQK | base64 -d)"
action_rc=$?
printf 'ACTION 04 EXIT %s\n' "$action_rc"
printf '\nACTION 05 BEGIN\n'
eval "$(printf %s YXNfcm9vdCBubWNsaSAtLXdhaXQgNjAgY29ubmVjdGlvbiB1cCBjYWwtc2Vjb25kYXJ5Cg== | base64 -d)"
action_rc=$?
printf 'ACTION 05 EXIT %s\n' "$action_rc"
printf '\nACTION 06 BEGIN\n'
eval "$(printf %s YXNfcm9vdCBubWNsaSBjb25uZWN0aW9uIGFkZCB0eXBlIHdpZmkgY29uLW5hbWUgY2FsLXRlc3QgaWZuYW1lICcqJyBzc2lkIGNhbC10ZXN0IGNvbm5lY3Rpb24uYXV0b2Nvbm5lY3Qgbm8gd2lmaS1zZWMua2V5LW1nbXQgd3BhLXBzayB3aWZpLXNlYy5wc2sgY2FsLXRlc3QtcGFzc3dvcmQK | base64 -d)"
action_rc=$?
printf 'ACTION 06 EXIT %s\n' "$action_rc"
printf '\nACTION 07 BEGIN\n'
eval "$(printf %s bWtkaXIgLXAgIiRIT01FLy5sb2NhbC9iaW4iICIkSE9NRS8uY29uZmlnL3N5c3RlbWQvdXNlciIK | base64 -d)"
action_rc=$?
printf 'ACTION 07 EXIT %s\n' "$action_rc"
printf '\nACTION 08 BEGIN\n'
eval "$(printf %s Y2F0ID4gIiRIT01FLy5sb2NhbC9iaW4vY2FsLWhlbGxvIiA8PCdTQ1JJUFQnCiMhL2Jpbi9zaApwcmludGYgJyVzXG4nICdjYWwtdGVzdCcgPj4gIiRIT01FL2NhbC10ZXN0LmxvZyIKU0NSSVBUCg== | base64 -d)"
action_rc=$?
printf 'ACTION 08 EXIT %s\n' "$action_rc"
printf '\nACTION 09 BEGIN\n'
eval "$(printf %s Y2htb2QgNzU1ICIkSE9NRS8ubG9jYWwvYmluL2NhbC1oZWxsbyIK | base64 -d)"
action_rc=$?
printf 'ACTION 09 EXIT %s\n' "$action_rc"
printf '\nACTION 10 BEGIN\n'
eval "$(printf %s IiRIT01FLy5sb2NhbC9iaW4vY2FsLWhlbGxvIgo= | base64 -d)"
action_rc=$?
printf 'ACTION 10 EXIT %s\n' "$action_rc"
printf '\nACTION 11 BEGIN\n'
eval "$(printf %s Y2F0ID4gIiRIT01FLy5jb25maWcvc3lzdGVtZC91c2VyL2NhbC1oZWxsby5zZXJ2aWNlIiA8PCdVTklUJwpbVW5pdF0KRGVzY3JpcHRpb249V3JpdGUgdGhlIGxhYm9yYXRvcnkgZ3JlZXRpbmcKW1NlcnZpY2VdClR5cGU9b25lc2hvdApFeGVjU3RhcnQ9JWgvLmxvY2FsL2Jpbi9jYWwtaGVsbG8KVU5JVAo= | base64 -d)"
action_rc=$?
printf 'ACTION 11 EXIT %s\n' "$action_rc"
printf '\nACTION 12 BEGIN\n'
eval "$(printf %s Y2F0ID4gIiRIT01FLy5jb25maWcvc3lzdGVtZC91c2VyL2NhbC1oZWxsby50aW1lciIgPDwnVU5JVCcKW1VuaXRdCkRlc2NyaXB0aW9uPVNjaGVkdWxlIHRoZSBsYWJvcmF0b3J5IGdyZWV0aW5nCltUaW1lcl0KT25Cb290U2VjPTVtaW4KT25Vbml0QWN0aXZlU2VjPTFoCltJbnN0YWxsXQpXYW50ZWRCeT10aW1lcnMudGFyZ2V0ClVOSVQK | base64 -d)"
action_rc=$?
printf 'ACTION 12 EXIT %s\n' "$action_rc"
printf '\nACTION 13 BEGIN\n'
eval "$(printf %s c3lzdGVtY3RsIC0tdXNlciBkYWVtb24tcmVsb2FkCg== | base64 -d)"
action_rc=$?
printf 'ACTION 13 EXIT %s\n' "$action_rc"
printf '\nACTION 14 BEGIN\n'
eval "$(printf %s c3lzdGVtY3RsIC0tdXNlciBlbmFibGUgLS1ub3cgY2FsLWhlbGxvLnRpbWVyCg== | base64 -d)"
action_rc=$?
printf 'ACTION 14 EXIT %s\n' "$action_rc"
printf '\nACTION 15 BEGIN\n'
eval "$(printf %s cG9kbWFuIHJ1biAtLW5hbWUgY2FsLWNvbnRhaW5lciBkb2NrZXIuaW8vbGlicmFyeS9hbHBpbmU6My4yMiAvYmluL2VjaG8gY2FsLXRlc3QK | base64 -d)"
action_rc=$?
printf 'ACTION 15 EXIT %s\n' "$action_rc"
