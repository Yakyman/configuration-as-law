#!/bin/bash
# Common replay sequence of B2/CASES-5.md, verbatim, with the two parameters as arguments.
cd "$HOME/VMs/cal-1123/stand" || exit 1
(
bc3_case_number=$1
bc3_case_id=$2
bc3_vm="bc3-peer-$bc3_case_number"
if test -e "raw/round-3/second-party/$bc3_case_number.jsonl"; then
    printf 'Case output already exists; do not repeat the attempt.\n' >&2
    exit 1
fi
python3 lab.py new "$bc3_vm" stand || exit 1
if printf 'python3 -B /usr/local/lib/stand/bc3-selftest.py --case %s\n' "$bc3_case_id" | python3 lab.py run "$bc3_vm" --root > "raw/round-3/second-party/$bc3_case_number.jsonl" 2> "raw/round-3/second-party/$bc3_case_number.stderr"; then
    bc3_case_status=0
else
    bc3_case_status=$?
fi
printf '%s\n' "$bc3_case_status" > "raw/round-3/second-party/$bc3_case_number.exit"
if ! python3 lab.py copy-out "$bc3_vm" /var/lib/stand/bc3-evidence "raw/round-3/second-party/$bc3_case_number-evidence"; then
    printf 'Evidence export failed; retain the failure in the record.\n' >&2
fi
python3 lab.py destroy "$bc3_vm"
)
