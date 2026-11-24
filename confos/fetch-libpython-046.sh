#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
bash fetch-release.sh 0.46
python3 collect-evidence.py 0.46
for name in prepare-libpython libpython smoke updates runtime-source-package reader-inheritance source-modes inventory underived;do
 python3 fetch-record.py "logs/$name-0.46.log" "records/$name-0.46.log"
done
for name in generated-root-0.46.json runtime-objects-0.46.json reader-inheritance-0.46.json;do
 python3 fetch-record.py "records/$name" "records/$name"
done
python3 fetch-record.py releases/inherited-0.46.sha256 releases/inherited-0.46.sha256
python3 check-fetched-release.py 0.46
python3 document-inventory.py 0.46
