# A minimal declaration for testing the runner's ConfOS path only (run --declaration). Not the test declaration of
# the cases: outcomes of a run with it are development results of the runner, never observations of the check.
base
archive-state 20261123T000000Z
account person uid=1000 gid=1000 groups=wheel shell=/bin/bash home=/home/person
authorized-key person @PERSON_KEY@
package procps
package coreutils
package dpkg
script /home/person/bin/cases-report.sh 2fb12358ed0c2cf3ef02685dc629f046b5b40f32e1ff52ba03cdd854ea58c1d4
