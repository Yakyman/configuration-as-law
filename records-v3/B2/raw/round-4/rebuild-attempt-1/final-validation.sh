#!/bin/bash
set -eu
while systemctl --user is-active --quiet bc4-final-build-a || systemctl --user is-active --quiet bc4-final-build-b; do sleep 5; done
test "$(systemctl --user show bc4-final-build-a --property=Result --value)" = success
test "$(systemctl --user show bc4-final-build-b --property=Result --value)" = success
python3 build/round4-driver.py rebuilt --regressions --peer-root ../round-4-peer > raw/final-suite-console.jsonl 2>&1
python3 build/assemble-channel-examples.py raw/round-4/rebuilt channel-example > raw/assembly-final.json 2>&1
python3 build/combined-selftest.py combined channel-example/combined --peer-root ../round-4-peer --reboot > raw/combined-final-console.jsonl 2>&1
