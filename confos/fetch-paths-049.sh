#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
bash fetch-release.sh 0.49
python3 collect-evidence.py 0.49
for name in prepare-paths smoke updates recording-apt configuration-recording language-recording podman-recording flatpak-recording other-export runtime-source-package reader-inheritance source-modes inventory underived cleanup-paths;do
 python3 fetch-record.py "logs/$name-0.49.log" "records/$name-0.49.log"
done
for name in generated-root-0.49.json runtime-objects-0.49.json reader-inheritance-0.49.json;do
 python3 fetch-record.py "records/$name" "records/$name"
done
python3 fetch-record.py releases/inherited-0.49.sha256 releases/inherited-0.49.sha256
python3 check-fetched-release.py 0.49
python3 document-inventory.py 0.49
