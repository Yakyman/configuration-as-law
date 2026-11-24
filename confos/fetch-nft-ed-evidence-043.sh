#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
bash fetch-release.sh 0.43
python3 collect-evidence.py 0.43
for name in prepare-nft-ed-0.43 nft-ed-0.43 smoke-0.43 updates-0.43 runtime-source-package-0.43 \
 reader-inheritance-0.43 source-modes-0.43 inventory-0.43 underived-0.43;do
 python3 fetch-record.py "logs/$name.log" "records/$name.log"
done
for cycle in {1..10};do
 python3 fetch-record.py "logs/nft-ed-043-$cycle.serial" "records/nft-ed-043-$cycle.serial"
done
for name in generated-root-0.43.json runtime-objects-0.43.json reader-inheritance-0.43.json nft-ed-043-fixture.conf;do
 python3 fetch-record.py "records/$name" "records/$name"
done
python3 fetch-record.py releases/inherited-0.43.sha256 releases/inherited-0.43.sha256
python3 check-fetched-release.py 0.43
python3 document-inventory.py 0.43
