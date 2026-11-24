#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
bash fetch-release.sh 0.44
python3 collect-evidence.py 0.44
for name in prepare-tools-0.44 tools-0.44 smoke-0.44 updates-0.44 runtime-source-package-0.44 \
 reader-inheritance-0.44 source-modes-0.44 inventory-0.44 underived-0.44 visudo-editor-0.44;do
 python3 fetch-record.py "logs/$name.log" "records/$name.log"
done
for cycle in {1..10};do
 python3 fetch-record.py "logs/tools-044-$cycle.serial" "records/tools-044-$cycle.serial"
done
for name in generated-root-0.44.json runtime-objects-0.44.json reader-inheritance-0.44.json tools-044-fixture.conf;do
 python3 fetch-record.py "records/$name" "records/$name"
done
python3 fetch-record.py releases/inherited-0.44.sha256 releases/inherited-0.44.sha256
python3 check-fetched-release.py 0.44
python3 document-inventory.py 0.44
