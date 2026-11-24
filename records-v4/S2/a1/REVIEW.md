# Review of the sampled agreements

The 600 rows in `sample.tsv` preserve every sampled ID, source and agreed decision. The source order is D1 followed by A3, each in its original order. The findings test the agreed labels against the ordered questions and recording routes, independently of the two cited sentence sets. They do not audit the earlier classifications' unsupplied reasons or actual declaration completeness.

The detailed evidence maps and rule checks are retained in `raw/d1-first-notes.md`, `raw/d1-second-notes.md`, `raw/a3-first-notes.md`, `raw/a3-first-evidence.md`, `raw/a3-second-notes.md` and `raw/a3-second-evidence.tsv`. Those references resolve to the permitted inventories and public primary documentation. No other party's work or earlier classification or adjudication was consulted.

## Review decisions

- S8.2-5 directly determines RUNTIME for an observed process even when its executable identity is unavailable. The classification template explicitly requires a decision when every possible value of an unknown fact gives the same decision. Missing creator identity does not turn this agreed label into FACT-UNKNOWN.
- S8.2-16 identifies the recording route. Current declaration contents are unnecessary to classify an installed dependency; requiring them would introduce a separate property-completeness check.
- Stored groups cover their enumerated immediate members, as specified in both inventory fact indexes. A child directory is not silently replaced with all its descendants. Cache index metadata and directory structures are distinguished from opaque payload files whose execution capabilities remain unknown.
- Package contents were checked against retained ownership and integrity records. Observed filesystem aliases resolved the module paths. The CUPS backend aliases have the same observed device/inode as unchanged package files. Nested language-package checks extend beyond metadata to their program contents.
- The two filesystem exceptions to the collector's persistence label were checked using retained filesystem magic and primary kernel definitions: RPC pipefs and NSFS are live kernel filesystems. `raw/review_checks.py` verifies the exact magic for every immediate member of these two groups.
- The bytecode review checked matching installed source files and the generating package scripts. The six Void groups have the explicit Python and pip post-install compilation selections in the decoded package database, installed state, and corresponding unchanged source files. All three Lutris groups have the matching package compilation script, successful setup log and unchanged source files. This evidence does not depend solely on timestamps or filename suffixes.
- The Netplan group remains FACT-UNKNOWN. Its sources belong to `netplan.io` (original ID `328ea3408632a89a16aca3df`), while the retained `py3compile -p python3-netplan:amd64` script belongs to `python3-netplan` (original ID `2d8da38c92da3435c54439be`). The two retained package lists cover different source directories. The available script therefore does not establish generation of this sampled group. Evidence: `A3/in/raw/server/raw/0007-metadata-read-128.out`, `0013-metadata-read-512.out`, `0112-metadata-read-256.out`, and (not published: direct evidence at least 2 MB).
- K3s extraction provenance is supported by the installation log and primary documentation. The three sampled executable files lack received-content integrity evidence needed to decide the earlier package question. Their findings do not deny the documented extraction mechanism.

## Unresolved facts

The sixteen FACT-UNKNOWN rows comprise six HTTP-response payload groups, three npm content-cache payload groups, three compressed updater archives, three extracted K3s executables, and the Netplan bytecode group. Their short reasons identify the missing facts. These are not findings of a wording gap. No sampled agreement was assigned DOES-NOT-FOLLOW.

## Final checks

`raw/review_checks.py` independently joins all 600 IDs to the original inventories, checks the preserved decisions, validates every sentence ID and the thirty-word reason limit, checks all 133 package reason/provenance predicates, opens all 148 immediate member lists, verifies 56 runtime groups and both pseudo-filesystem exceptions, and checks corresponding unchanged sources for all ten bytecode groups. The Netplan source match is explicitly insufficient to establish its generation route.

The final table has exactly the requested six-column header, 600 unique source/ID pairs, 300 rows per source and no missing sample rows. `raw/validation.json` records the checks and counts; `DONE` contains the three finding counts.
