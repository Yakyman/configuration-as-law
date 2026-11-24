#!/usr/bin/env python3
"""Document observed handoff schemas and exact joins, without object decisions."""
import collections
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SYSTEMS = ('alma', 'void', 'gentoo', 'microos', 'talos')
csv.field_size_limit(536870912)

JOINS = {
 'objects.tsv': 'Find the unchanged raw ID in `id`. `members` is JSON; package rows carry `reason`, `manager`, and available reason-source/native-record fields. Unknown values remain unknown. A `members.file` entry names the separate member table.',
 'level-1.tsv': 'Same IDs and cells as the corresponding level-1 rows of objects.tsv.',
 'level-2.tsv': 'Same IDs and cells as the corresponding level-2 rows of objects.tsv.',
 'package-files.tsv': '`package` is the raw package object ID; `path` is the supplied file. `integrity` records unchanged, changed, missing or unknown, with its `rule` and saved query evidence. This is the recorded reference comparison; no inference is made for omitted or unknown rows.',
 'configuration-origin.tsv': 'Join an exact object/member path to `path`. The created field and causal limitations are explicit; modification times and script mentions do not supply a creation event.',
 'coverage.tsv': 'Match an evidence filename to `stdout`; retain query exit_status, duration, status and stderr. Exit zero alone does not assert a known value in every returned field.',
 'full-digests.tsv': 'Exact object/member path joins `path`; algorithm, digest, bytes, status and reason describe the complete bounded read, with no accepted digest for a failed read.',
 'object-fact-index.tsv': 'Raw ID joins `object_id`; `path`, `fact_file` and `join_column` identify the next lookup exactly.',
 'store-members.tsv': 'JSON `object_ids` contains raw IDs. `store` is the root; a parent member can join its child store path. Inner path metadata, target, prefix signature and persistence are retained independently.',
 'store-coverage.tsv': 'JSON `object_ids` or exact `store` joins the row. query_exit, traversal_complete, members and inner_opaque bound what was read.',
 'font-cache-sources.tsv': 'Exact cache member path joins `path`; evidence names saved fc-cat output identifying its source directories/fonts.',
 'font-source-packages.tsv': 'Exact source font path joins `path`; JSON package_ids joins raw package IDs and package-files.tsv.',
 'alma-facts.tsv': 'Raw ID joins `object_id`; distinguish each `fact` and `path`. value/status/evidence retain current bytes, directives, decoded values, selected operation extracts, source text and unknown fields.',
 'alma-key-events.tsv': 'Raw package ID joins object_id. key_id matches the literal RPM key component. Fingerprint, key source, import/success timestamps, preceding command, source file, log segment and line fields retain measured context. No transaction/PID correlation or acquisition-reason field is added.',
 'alma-key-event-coverage.tsv': 'The event source_file joins the queried source; query_exit_status/status and line/byte counts retain source coverage and bounds.',
 'npm-archive-sources.tsv': 'Exact package_root, or a component-delimited member beneath it, locates the archive source. lock/resolved/integrity/cache/status/evidence identify the reference and verification.',
 'npm-member-integrity.tsv': 'JSON object_ids contains raw IDs, or join exact member path. package_root joins npm-archive-sources.tsv. expected/actual/status retain the complete byte or target comparison.',
 'old-package-receipt-sources.tsv': 'source joins the source field of old-package-member-integrity.tsv; status and evidence distinguish the recorded manifest sources.',
 'old-package-member-integrity.tsv': 'JSON object_ids contains raw IDs, or use exact path. source links the manifest source. type/expected/actual/status/evidence retain comparisons; no-reference-found does not provide an original reference.',
 'void-configuration-facts.tsv': 'JSON object_ids contains raw IDs, or use exact path. content_base64 holds selected current bytes; historical_creator is separate and can remain unknown.',
 's4-microos-snapshot-files.tsv': 'Exact stored member path joins path. snapshot_root identifies that RPM database; package_path/package are its recorded names. algorithm/expected/observed/comparison and manifest/digest evidence retain that comparison.',
 's4-microos-snapshot-current.tsv': 'Exact snapshot member joins snapshot_path; current_path names the separately read live file. Both complete SHA256 values, comparison and evidence are retained.',
 's4-microos-sources.tsv': 'Join exact object/member path, or a source path selected by the unit table, to path. status/content_base64/evidence retain the bounded current source bytes.',
 's4-microos-unit-links.tsv': 'Exact member/link path joins path. target and error are current link observations.',
 's4-microos-unit-selected.tsv': 'Raw ID joins object_id. user/unit and properties_json identify current FragmentPath, drop-ins and source paths; query_exit/evidence retain the query result.',
 's4-microos-scriptlet-query.tsv': 'evidence points to the RPM installation script source output; query_exit is retained. Source text is not an execution event.',
 's4-microos-selinux-stores.tsv': 'Use the component-delimited store_root/policy directory containing the member. evidence names the native module format/checksum listing; query_exit retains failure.',
 's4-microos-solver-cache.tsv': 'Exact cache path joins path. content_status/query_exit/content_evidence describe the safe byte read and host decoder; digest_status/sha256/digest_evidence describe the complete digest.',
 'talos-image-sources.tsv': 'Exact image name joins image; resource_id and evidence identify the current workload configuration source. There is no historical pull-actor field.',
 'talos-expanded-members.tsv': 'JSON object_ids links raw IDs where supplied. For a directory row, exact name plus slash selects descendants; for an ordinary member group, use immediate parent equality. path/type/mode/owner/size/link_target/evidence describe listed members.',
 'talos-listing-coverage.tsv': 'Directory name joins directory; query_exit/status/members/evidence describe each separately bounded listing.',
 'talos-listing-boundaries.tsv': 'Exact path names an unexpanded boundary and reason. It does not assert an empty directory.',
 'talos-content.tsv': 'JSON object_ids or exact member path joins the row. status/bytes/sha256/prefix_hex/signature/query_exit/evidence/method/error_category/diagnostic describe the last accepted or failed bounded content method. No installed-image comparison field is present.',
 'talos-content-attempts.tsv': 'Same joins as talos-content.tsv; each implemented Read, Copy or refreshed-metadata Read attempt remains separately recorded.',
 'talos-mountinfo.tsv': 'Decode Linux path escapes, then find mountpoints equal to or component-delimited ancestors of the object/member path. Preserve stacked candidates, parent IDs and namespace limits; do not infer the covering mount from longest prefix alone.',
 'talos-mountinfo-coverage.tsv': 'query_exit/status/mounts/namespace/evidence qualify the exact API-daemon mountinfo parse; other workload namespaces are not supplied by this row.',
 'talos-fact-index.tsv': 'Raw ID joins object_id; members_file/members_join/content_file/content_join specify further lookups. backing/image_integrity retain references or explicit unknown fields.',
}


def scan(path):
    with path.open(newline='', encoding='utf-8') as source:
        reader = csv.DictReader(source, delimiter='\t')
        columns = reader.fieldnames or []
        counts = collections.defaultdict(collections.Counter)
        n = 0
        for row in reader:
            n += 1
            for key in ('status', 'integrity', 'comparison', 'persistence', 'historical_creator', 'query_exit', 'query_exit_status', 'exit_status', 'traversal_complete'):
                if key in row:
                    counts[key][row[key]] += 1
        return columns, n, {k: dict(v) for k, v in counts.items()}


def main():
    lines = ['# Handoff fact locations', '', '2026-11-23 UTC. All facts below come from the delivered handoff copies.', '',
             'An inventory ID is `d1b-MACHINE-RAW_ID`. Remove that exact machine prefix to obtain the unchanged collector ID, or use `D1b/in/object-id-map.tsv` (`id`, `machine`, `raw_id`). The handoff object, member, package and fact tables and the fixed matcher all use the unchanged raw ID. No content hash matching is implied.', '',
             '`members` cells and fields explicitly described as JSON must be JSON-decoded; a few inherited rows contain a JSON string holding another JSON value. Evidence paths are relative to the corresponding `D1b/handoff/MACHINE/` directory. Semicolon-separated evidence references retain each named output. For a raw query, `.sh` records its exact command, `.out` its output, and `.err` its error output; `coverage.tsv` records its exit/status and bound.', '',
             'Package installation reason is the `reason` field in the package object\'s decoded `members`, with the recorded source/native fields and evidence. `explicit`, `dependency`, and `unknown` are collector values. File comparisons are the `package-files.tsv` rows keyed by that raw package ID and exact path. Omitted file rows, unknown comparisons, and missing reason fields remain unrecorded facts.', '',
             'For every member group, decode `members.file` and read that exact `members/RAW_ID.tsv` file completely. Its columns are `path`, `type`, `mode`, `owner`, `size`, `mtime`, `executable`, `signature`, `persistence`. `members.count`, `members.complete`, metadata coverage and the underlying query qualify the list. The signature in this inherited table covers only a 4096-byte prefix. A group without an expanded table has only the bounded facts named in its row and the additional store/listing tables; it has no invented full member list.', '',
             'For stored paths on the SSH systems, the member row\'s `persistence` (or the individual object\'s decoded metadata) is the collector\'s recorded filesystem fact; inspect its saved scan evidence. Inner store members have a separate `persistence`. For Talos, use the recorded `backing` field and covering candidates in `talos-mountinfo.tsv`, with its namespace/status table and explicit unknown values. A current path, read-only flag or digest alone is not a persistence or historical-creator record.', '',
             'Every root TSV below is listed with its actual columns and row count. `fact-table-status.json` records numerical distributions of returned status fields, without filling missing values. `metadata.json`, `fact-summary.json` and `coverage.tsv` retain traversal bounds, query failures and numeric reductions. The handoff bytes remain the evidence.', '']
    summaries = {}
    for machine in SYSTEMS:
        folder = ROOT / 'D1b/handoff' / machine
        lines += ['## ' + machine, '', '`D1b/handoff/' + machine + '/`.', '']
        if not (folder / 'objects.tsv').is_file():
            lines += ['No delivered object inventory; no facts asserted for this machine.', '']
            continue
        lines += ['| Exact file | Rows | Columns | ID/path lookup and recorded fields |', '|---|---:|---|---|']
        summaries[machine] = {}
        for path in sorted(folder.glob('*.tsv')):
            columns, n, counts = scan(path)
            summaries[machine][path.name] = dict(rows=n, columns=columns, status_counts=counts)
            join = JOINS.get(path.name)
            if join is None:
                raise ValueError('Undocumented fact table: ' + path.name)
            link = f'`D1b/handoff/{machine}/{path.name}`'
            lines.append('| ' + link + ' | ' + str(n) + ' | ' + ', '.join('`' + c + '`' for c in columns) + ' | ' + join + ' |')
        lines += ['', f'Exact member files: `D1b/handoff/{machine}/members/RAW_ID.tsv`, reached through the object row\'s `members.file`. All files and every member row are retained. For groups whose collector row gives no member file, use its explicit inline members and the joins above; absent expansion stays absent.', '',
                  f'`D1b/handoff/{machine}/metadata.json` fields `utc`, `machine`, `system`, `duration`, `filesystem_complete`, `package_ownership_complete`, `gaps`, `ready_for_observation` are retained exactly. `ready_for_observation` is an inherited collector field, not a substituted operator outcome.', '',
                  f'`D1b/handoff/{machine}/fact-summary.json` retains the original numeric/boolean reductions and adapter status counters. The source query files under `D1b/handoff/{machine}/raw/` retain the actual output, stderr and exact commands referenced by each evidence cell.', '']
    (ROOT / 'D1b/in/FACTS.md').write_text('\n'.join(lines), encoding='utf-8')
    (ROOT / 'D1b/in/fact-table-status.json').write_text(json.dumps(summaries, indent=2) + '\n')
    print('Fact schemas documented for ' + str(len(summaries)) + ' delivered machines')


if __name__ == '__main__':
    main()
