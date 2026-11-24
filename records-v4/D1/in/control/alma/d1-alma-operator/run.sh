#!/bin/bash
cd /tmp/d1-alma-operator/actions
bash alma.sh
rc=$?
printf '%s\n' "$rc" > /tmp/d1-alma-operator/action-exit
