# Void rehearsal preparation

2026-11-23 UTC. Rounds 1 and 2 existed before this continuation; both clones
were destroyed successfully. Only their numeric statuses and counts were read.
Round 2 failed the language program, user service, network connection and
container actions. No failure text was read; their precise causes are not
established by the exit statuses alone.

Before round 3, source review identified a service startup race: newly enabled
services may not yet have a supervisor when `sv` is called. The runsvdir manual
states “At least every five seconds runsvdir checks” its directory; the sv manual
lists an uncontrolled directory as an error. Bounded FIFO readiness waits were
added before `sv`, and a bounded Docker API readiness wait before container run.
These are synchronization repairs to the same actions, not replacements.
Sources: https://man.voidlinux.org/runsvdir.8 ; https://man.voidlinux.org/sv.8 ;
https://docs.docker.com/reference/cli/docker/info/ .

Expected before round 3: new supervisor readiness removes the identified race;
all nine actions must still return zero. Three fixed numeric substep labels
identify whether installing Node.js, installing cowsay, or invoking cowsay
fails; no command output is inspected. Collector completion must remain below
1800 seconds with level-2 rows and more than 90 percent package reason and
integrity coverage. Twenty consecutive transport calls must complete normally.

Round 3: the Node.js installation returned zero; npm installation returned 1
in less than one recorded second. Its precise error remains unknown because
output was deleted unread. The three supervisor waits returned 124. Source
review found that runsv creates `supervise` with mode 0700; an unprivileged FIFO
check cannot inspect a root-owned supervisor directory. The round-4 wait uses
`sudo -n test -p` through the existing root helper. Source:
https://raw.githubusercontent.com/void-linux/runit/master/src/runsv.c
(`mkdir("supervise", 0700)` and `fifo_make("supervise/ok",0600)`).

Expected before round 4: the permission-correct readiness check allows the same
user-service, network and container actions to proceed. The npm failure is not
presumed repaired. The collector guard is repaired centrally to permit read-only
QEMU metadata access to a running overlay; round 3's exit 1 is retained as a
failed collector rehearsal, not collection evidence. Round 4 is the last allowed
round; any remaining failure will be reported without a fifth attempt.

Round 4 briefly overlapped a fifth system part because its launch crossed a
scheduling hold message. The controller and virtual machine were frozen using
host service controls, both status 0, pending completion of another part. No
clone was replaced and no additional round was started. This scheduling pause
can inflate wall-clock duration; elapsed times are retained without subtraction.

## Final result

Round 4 completed with seven of nine ordinary actions returning zero. The npm
installation still returned 1; the network action returned 8. These failures'
exact guest messages remain unknown because all output was deleted unread.
The user-service and container actions returned zero after synchronization and
permission repairs. Twenty consecutive transport calls returned zero in every
round. Both final clones were destroyed successfully; no fifth round was run.

The round-3 and round-4 collector exited 1 before any query in 0.064 seconds.
The host service launch omitted both a working directory and LAB_ROOT; unlike
lifecycle calls using absolute paths, the collector defaults LAB_ROOT to the
current directory. Thus these launches supplied the wrong laboratory root.
This host-launch defect is corrected centrally for subsequent systems; Void's
four-round limit prevents another run. Neither final attempt supplies inventory
counts. The last successful collector was round 2: 54.206 seconds, 696 level-2
rows, 339 of 501 package reasons known and 345 of 501 with any known integrity.
Neither ratio exceeds 90 percent. Zero packages had all file integrity facts
known. Void is not ready.

No guest content was seen by accident during this continuation. Rehearsal
output was deleted unread; only status/duration/byte/count records were copied.
