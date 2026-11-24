#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
bash fetch-release.sh 0.45
python3 collect-evidence.py 0.45
for name in prepare-radio-recording radio-recording smoke updates runtime-source-package reader-inheritance source-modes inventory underived;do
 python3 fetch-record.py "logs/$name-0.45.log" "records/$name-0.45.log"
done
for name in generated-root-0.45.json runtime-objects-0.45.json reader-inheritance-0.45.json;do
 python3 fetch-record.py "records/$name" "records/$name"
done
python3 fetch-record.py releases/inherited-0.45.sha256 releases/inherited-0.45.sha256
python3 check-fetched-release.py 0.45
python3 document-inventory.py 0.45
