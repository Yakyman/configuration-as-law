#!/bin/bash
set -uo pipefail
sudo() { command sudo -S -p "" "$@" <<< "<REDACTED>"; }
printf '\nACTION 01 BEGIN\n'
eval "$(printf %s c3VkbyBlbnYgREVCSUFOX0ZST05URU5EPW5vbmludGVyYWN0aXZlIGFwdC1nZXQgdXBkYXRlCg== | base64 -d)"
action_rc=$?
printf 'ACTION 01 EXIT %s\n' "$action_rc"
printf '\nACTION 02 BEGIN\n'
eval "$(printf %s c3VkbyBlbnYgREVCSUFOX0ZST05URU5EPW5vbmludGVyYWN0aXZlIGFwdC1nZXQgaW5zdGFsbCAteSBoZWxsbyBwb2RtYW4K | base64 -d)"
action_rc=$?
printf 'ACTION 02 EXIT %s\n' "$action_rc"
printf '\nACTION 03 BEGIN\n'
eval "$(printf %s ZmxhdHBhayAtLXVzZXIgcmVtb3RlLWFkZCAtLWlmLW5vdC1leGlzdHMgZmxhdGh1YiBodHRwczovL2ZsYXRodWIub3JnL3JlcG8vZmxhdGh1Yi5mbGF0cGFrcmVwbwo= | base64 -d)"
action_rc=$?
printf 'ACTION 03 EXIT %s\n' "$action_rc"
printf '\nACTION 04 BEGIN\n'
eval "$(printf %s ZmxhdHBhayAtLXVzZXIgaW5zdGFsbCAtLW5vbmludGVyYWN0aXZlIC15IGZsYXRodWIgb3JnLmdub21lLkNhbGN1bGF0b3IK | base64 -d)"
action_rc=$?
printf 'ACTION 04 EXIT %s\n' "$action_rc"
printf '\nACTION 05 BEGIN\n'
eval "$(printf %s c3VkbyBubWNsaSBjb25uZWN0aW9uIGFkZCB0eXBlIGV0aGVybmV0IGlmbmFtZSAnKicgODAyLTMtZXRoZXJuZXQubWFjLWFkZHJlc3MgNTI6NTQ6MDA6Y2E6MTA6MDIgY29uLW5hbWUgY2FsLXdpcmVkIGlwdjQubWV0aG9kIGF1dG8gaXB2NC5uZXZlci1kZWZhdWx0IHllcyBpcHY2Lm1ldGhvZCBkaXNhYmxlZAo= | base64 -d)"
action_rc=$?
printf 'ACTION 05 EXIT %s\n' "$action_rc"
printf '\nACTION 06 BEGIN\n'
eval "$(printf %s c3VkbyBubWNsaSBjb25uZWN0aW9uIHVwIGNhbC13aXJlZAo= | base64 -d)"
action_rc=$?
printf 'ACTION 06 EXIT %s\n' "$action_rc"
printf '\nACTION 07 BEGIN\n'
eval "$(printf %s c3VkbyBubWNsaSBjb25uZWN0aW9uIGFkZCB0eXBlIHdpZmkgaWZuYW1lICcqJyBjb24tbmFtZSBjYWwtdGVzdCBzc2lkIGNhbC10ZXN0IGNvbm5lY3Rpb24uYXV0b2Nvbm5lY3Qgbm8gaXB2NC5tZXRob2QgYXV0byBpcHY2Lm1ldGhvZCBkaXNhYmxlZAo= | base64 -d)"
action_rc=$?
printf 'ACTION 07 EXIT %s\n' "$action_rc"
printf '\nACTION 08 BEGIN\n'
eval "$(printf %s c3VkbyBubWNsaSBjb25uZWN0aW9uIG1vZGlmeSBjYWwtdGVzdCB3aWZpLXNlYy5rZXktbWdtdCB3cGEtcHNrIHdpZmktc2VjLnBzayBjYWwtdGVzdC1wYXNzcGhyYXNlCg== | base64 -d)"
action_rc=$?
printf 'ACTION 08 EXIT %s\n' "$action_rc"
printf '\nACTION 09 BEGIN\n'
eval "$(printf %s bWtkaXIgLXAgIiRIT01FLy5sb2NhbC9iaW4iICIkSE9NRS8uY29uZmlnL3N5c3RlbWQvdXNlciIK | base64 -d)"
action_rc=$?
printf 'ACTION 09 EXIT %s\n' "$action_rc"
printf '\nACTION 10 BEGIN\n'
eval "$(printf %s Y2F0ID4gIiRIT01FLy5sb2NhbC9iaW4vY2FsLXVzZXItc2NyaXB0IiA8PCdFT0YnCiMhL2Jpbi9zaApwcmludGYgJ29yZGluYXJ5LWFjdGlvblxuJyA+PiAiJEhPTUUvY2FsLXVzZXItc2NyaXB0LmxvZyIKRU9GCg== | base64 -d)"
action_rc=$?
printf 'ACTION 10 EXIT %s\n' "$action_rc"
printf '\nACTION 11 BEGIN\n'
eval "$(printf %s Y2htb2QgNzU1ICIkSE9NRS8ubG9jYWwvYmluL2NhbC11c2VyLXNjcmlwdCIK | base64 -d)"
action_rc=$?
printf 'ACTION 11 EXIT %s\n' "$action_rc"
printf '\nACTION 12 BEGIN\n'
eval "$(printf %s IiRIT01FLy5sb2NhbC9iaW4vY2FsLXVzZXItc2NyaXB0Igo= | base64 -d)"
action_rc=$?
printf 'ACTION 12 EXIT %s\n' "$action_rc"
printf '\nACTION 13 BEGIN\n'
eval "$(printf %s Y2F0ID4gIiRIT01FLy5jb25maWcvc3lzdGVtZC91c2VyL2NhbC11c2VyLXNjcmlwdC5zZXJ2aWNlIiA8PCdFT0YnCltVbml0XQpEZXNjcmlwdGlvbj1PcmRpbmFyeSB1c2VyIHNjcmlwdApbU2VydmljZV0KVHlwZT1vbmVzaG90CkV4ZWNTdGFydD0laC8ubG9jYWwvYmluL2NhbC11c2VyLXNjcmlwdApFT0YK | base64 -d)"
action_rc=$?
printf 'ACTION 13 EXIT %s\n' "$action_rc"
printf '\nACTION 14 BEGIN\n'
eval "$(printf %s Y2F0ID4gIiRIT01FLy5jb25maWcvc3lzdGVtZC91c2VyL2NhbC11c2VyLXNjcmlwdC50aW1lciIgPDwnRU9GJwpbVW5pdF0KRGVzY3JpcHRpb249T3JkaW5hcnkgdXNlciB0aW1lcgpbVGltZXJdCk9uQm9vdFNlYz0xMG1pbgpPblVuaXRBY3RpdmVTZWM9MWgKW0luc3RhbGxdCldhbnRlZEJ5PXRpbWVycy50YXJnZXQKRU9GCg== | base64 -d)"
action_rc=$?
printf 'ACTION 14 EXIT %s\n' "$action_rc"
printf '\nACTION 15 BEGIN\n'
eval "$(printf %s c3lzdGVtY3RsIC0tdXNlciBkYWVtb24tcmVsb2FkCg== | base64 -d)"
action_rc=$?
printf 'ACTION 15 EXIT %s\n' "$action_rc"
printf '\nACTION 16 BEGIN\n'
eval "$(printf %s c3lzdGVtY3RsIC0tdXNlciBlbmFibGUgLS1ub3cgY2FsLXVzZXItc2NyaXB0LnRpbWVyCg== | base64 -d)"
action_rc=$?
printf 'ACTION 16 EXIT %s\n' "$action_rc"
printf '\nACTION 17 BEGIN\n'
eval "$(printf %s cG9kbWFuIHJ1biAtLW5hbWUgY2FsLWNvbnRhaW5lciBkb2NrZXIuaW8vbGlicmFyeS9idXN5Ym94OjEuMzcuMCAvYmluL3NoIC1jICdwcmludGYgIm9yZGluYXJ5LWNvbnRhaW5lclxuIicK | base64 -d)"
action_rc=$?
printf 'ACTION 17 EXIT %s\n' "$action_rc"
