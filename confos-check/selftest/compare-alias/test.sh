#!/bin/bash
# Test of compare, derived mode: a `service` line matched to its running process, a rule given as nft text matched
# to the rule nft prints in its chain; an extra rule is UNRECORDED, a service not running is MISSING.
# Extended 2026-11-24: a service seen only by command line is UNVERIFIED, a rule read through the firewall
# fallback (`via`) is matched, the same rule with a comment added by the system is DIFFERS (Q7), and derived
# release objects are not compared. Objects placed by the system's convention (pip, npm, flatpak, container, user
# unit) are matched by name: a match is compared on what the line states, no match is MISSING.
cd "$(dirname "$0")" || exit 2
../../compare --inventory inv --derived derived.jsonl --declaration decl.conf --decide /dev/null --out compare.tsv
if cmp -s compare.tsv expected.tsv; then echo "RESULT: PASS"; else echo "RESULT: FAIL"; diff expected.tsv compare.tsv; exit 1; fi
