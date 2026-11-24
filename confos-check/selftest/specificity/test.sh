#!/bin/bash
# [n2-7]: a test that the programs do not accuse a correct state, next to the planted-object tests.
# Runs ON THE SERVER from a copy of cases/ (lib/remote.sh specificity does it from the laptop):
#   selftest/specificity/test.sh RELEASE-SOURCE.tar.gz
# On a clean installation of the given release built from D-test (run, case P4-T-SPEC): an application of the unchanged
# declaration, `mkdir ~/p`, a saved text document, an archive of sources downloaded into the home directory, and the
# two refused attempts of P4-BT-5 — no row of P1, P2 or P4 may be `fail`. In the same run the planted test P4-T-PLANT
# (a file and a process planted by the attempt) must still be `fail` with both in its effect, and P4-T-CODE (a saved
# script and a copied program) must be `fail` exactly when a direct route executes one of them.
# [n3-A] (the four questions of S8.2-6 for the writable area): P4-T-PLANT's file is a module in the
# person's pip store (question 1); P4-T-CODE adds a saved .js file (question 2 where Node runs it); P4-T-Q1 (a Python package unpacked into the person's pip store) and P4-T-Q3 (a user unit put in force)
# must be `fail` through question 1 and question 3; P4-T-WORK (gpg writes its working folder ~/.gnupg) must not.
set -u
cd "$(dirname "$0")/../.."
. ./local.env
SRC=${1:?release source archive}
NAME=spec-$(date -u +%Y%m%dT%H%M%SZ)
echo "specificity test, start $(date -u +%FT%TZ), release $(basename "$SRC") sha256 $(sha256sum "$SRC" | cut -c1-64)"
./run --source "$SRC" --name "$NAME" --only P4-T-SPEC,P4-T-PLANT,P4-T-CODE,P4-T-Q1,P4-T-Q3,P4-T-WORK --max-vms "${SPEC_MAX_VMS:-3}"
RUNDIR="$HOME/$SERVER_DIR/runs/$NAME"
echo "-- results.tsv"
cat "$RUNDIR/results.tsv"
python3 -I selftest/specificity/check.py "$RUNDIR"
status=$?
echo "end $(date -u +%FT%TZ)"
if [ "$status" = 0 ]; then echo "SPECIFICITY TEST PASS"; else echo "SPECIFICITY TEST FAIL"; fi
exit "$status"
