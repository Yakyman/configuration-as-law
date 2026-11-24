#!/usr/bin/env python3
"""Assemble the operator record from saved results; no guest commands."""
import collections
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'D1b/in'
SYSTEMS = ('alma', 'void', 'gentoo', 'microos', 'talos')
RELEASES = {'alma': 'AlmaLinux 10.3', 'void': 'Void Linux 20250202, x86-64 glibc, runit',
            'gentoo': 'Gentoo 20261122T164601Z', 'microos': 'openSUSE MicroOS Snapshot20261121', 'talos': 'Talos Linux 1.14.6'}
RAW_COUNTS = {'alma': (5711, 4026, 1685), 'void': (3279, 1211, 2068), 'gentoo': (32775, 1210, 31565),
              'microos': (6567, 1464, 5103), 'talos': (278, 225, 53)}
LIFECYCLE = {'alma': 'new 0 / 16.425 s; collector 0 / 124.580 s; destroy 0 / 2.850 s',
             'void': 'new 0 / 16.224 s; collector 0 / 78.865 s; destroy 0 / 3.840 s',
             'gentoo': 'new 0 / 16 s; collector 0 / 100.624 s; destroy 0 / 2.644 s',
             'microos': 'new 0 / 24 s; collector 0 / 84 s; destroy 0 / 1 s',
             'talos': 'new 0 / 8 s; collector 0 / 203 s; destroy 0 / 47 s'}
LIMITS = {
 'alma': 'Raw level two was obtained in part: filesystem_complete=true, package_ownership_complete=false, with atomic images/stores and unresolved ownership. No level-two rows were delivered because the handoff failed.',
 'void': 'Level two obtained in part: filesystem_complete=true describes the implemented traversal; package_ownership_complete=false. Fifteen image rows remain atomic. Three store traversals recorded 72,162 inner members with zero inner opaque rows, without complete payload receipts or creator events.',
 'gentoo': 'Level two obtained in part: filesystem_complete=true but package_ownership_complete=false. npm per-file provenance is unresolved; a discovered Go manager has no complete adapter. Eleven image rows remain atomic. Two store traversals recorded 530 members with zero inner opaque rows.',
 'microos': 'Level two obtained in part despite filesystem_complete=true and package_ownership_complete=true: 20 image rows and /.snapshots/2/snapshot retain expanded=false. /etc has expanded=true and 2,219 recorded descendants. Inner store tables are header-only.',
 'talos': 'Level two obtained in part: filesystem_complete=false, original depth/count bounds and 18 extended workload-or-pseudo boundaries remain. The literal package_ownership_complete=true field does not override the explicit metadata limit on complete ownership/level-two coverage. Extended listings contain 8,503 members across 1,219 directories; 5,932 of 5,963 bounded content reads succeeded, with 31 not-found results.'}
ACTION_FILES = {'alma': 'operator/alma/action-evidence/actions-status.tsv',
                'void': 'operator/void/actions/actions-status.tsv',
                'gentoo': 'operator/gentoo/actions/actions-status.tsv'}
# Each entry describes measured fields and their limits, not whether an object is decided.
FACTS = {
 'A01': ('source references only', '41 verified npm archives; no per-object acquisition-event field.', 'npm-archive-sources.tsv'),
 'A02': ('current sources recorded', '19 installer-directive rows and current values, including nine nonsecret network-profile rows.', 'alma-facts.tsv'),
 'A03': ('source/history extracts only', 'Directives, 19 retained-event evidence rows and 19 scriptlet rows; no complete choice/change-event table.', 'alma-facts.tsv'),
 'A04': ('current policy only', 'Two current unit-policy rows; no original disablement-event record.', 'alma-facts.tsv'),
 'A05': ('inner metadata recorded', '72,148 members in three completed implemented store traversals; zero inner opaque rows.', 'store-members.tsv;store-coverage.tsv'),
 'A06': ('metadata only', 'Inner member metadata is present; complete payload receipts and per-member creator events are not emitted.', 'store-members.tsv;store-coverage.tsv'),
 'A07': ('import fields recorded; reason absent', 'One event row with measured import context; no PID/transaction correlation or acquisition-reason field.', 'alma-key-events.tsv;alma-key-event-coverage.tsv'),
 'A08': ('current bytes recorded', 'Two /etc/alsa current-content rows retained, each with saved read evidence.', 'alma-facts.tsv'),
 'A09': ('creator event absent', 'Current contents and bounded extracts do not provide a per-value creator record.', 'alma-facts.tsv'),
 'A10': ('current values recorded', 'One native persistent-SELinux-value row retained.', 'alma-facts.tsv'),
 'A11': ('chooser event absent', 'Values, script source and bounded extracts retained; no per-value chooser event.', 'alma-facts.tsv'),
 'A12': ('decoded values recorded', 'Five compiled-values rows retained.', 'alma-facts.tsv'),
 'A13': ('current schema/readers only', 'Five schema-evidence and five current-reader-snapshot rows; no complete consumer history.', 'alma-facts.tsv'),
 'A14': ('source decoding recorded', '24 of 24 requested cache decodes; font-source/package joins retained.', 'font-cache-sources.tsv;font-source-packages.tsv'),
 'A15': ('reference comparisons recorded', '459 equal npm member comparisons and 52 directory entries against verified references.', 'npm-member-integrity.tsv;npm-archive-sources.tsv'),
 'V01': ('reference comparisons recorded', '41 verified lock-reference archives; 459 equal member comparisons and 23 directory entries.', 'npm-archive-sources.tsv;npm-member-integrity.tsv'),
 'V02': ('reference search/comparisons partial', '17 read sources; 22,282 equal comparisons, 4,294 directory entries and 6,859 no-reference-found rows. Missing references remain missing.', 'old-package-receipt-sources.tsv;old-package-member-integrity.tsv'),
 'V03': ('current sources only', 'Account/group/sudo rows and package sources retained; no per-object choice/creation events.', 'objects.tsv;package-files.tsv;coverage.tsv'),
 'V04': ('inner metadata recorded', 'Three completed implemented store traversals; 72,162 members.', 'store-members.tsv;store-coverage.tsv'),
 'V05': ('metadata only', 'Bounded inner metadata present; complete payload receipt and per-member creator events absent.', 'store-members.tsv;store-coverage.tsv'),
 'V06': ('current bytes/hashes recorded', '11 selected configuration-content rows ok; 11,306 of 11,306 eligible complete digests known.', 'void-configuration-facts.tsv;full-digests.tsv'),
 'V07': ('creator event absent', 'historical_creator retains an unknown marker; current records supply no creation event.', 'void-configuration-facts.tsv;objects.tsv'),
 'V08': ('source decoding recorded', 'One requested font cache decoded; 47 font-source/package rows.', 'font-cache-sources.tsv;font-source-packages.tsv'),
 'V09': ('choice/use events absent', 'No per-value choice-event or complete consumer/use table emitted; current metadata and eligible digests remain.', 'objects.tsv;full-digests.tsv'),
 'G01': ('both levels obtained; partial coverage', '32,775 rows (1,210 level one; 31,565 level two). Eight actions passed and browser_extension failed once. 109,059/109,382 package-file comparisons and 152,215/152,216 full digests known.', 'objects.tsv;metadata.json;package-files.tsv;full-digests.tsv;fact-summary.json'),
 'M01': ('source text only', 'Current sysusers sources and RPM scriptlet query retained; no per-account/group creation-event table.', 's4-microos-sources.tsv;s4-microos-scriptlet-query.tsv'),
 'M02': ('current sources/links recorded', '263 selected unit rows, all selection fields known; 1,318 source-file reads and current link table.', 's4-microos-unit-selected.tsv;s4-microos-unit-links.tsv;s4-microos-sources.tsv'),
 'M03': ('actor/default history absent', 'Current links and script source retained; no per-link enablement-event table.', 's4-microos-unit-links.tsv;s4-microos-scriptlet-query.tsv'),
 'M04': ('current sources/comparisons recorded', 'Supplying sudo source bytes and package-file comparisons retained; unknown comparisons stay unknown.', 's4-microos-sources.tsv;package-files.tsv'),
 'M05': ('choice events absent', 'Current source bytes and comparisons retained; no per-rule choice-event table.', 's4-microos-sources.tsv;package-files.tsv'),
 'M06': ('active subtree recorded', '/etc remains expanded=true with 2,219 descendants in the implemented traversal.', 'objects.tsv;full-digests.tsv;fact-summary.json'),
 'M07': ('manifest/comparisons partial', 'Two snapshot manifest roots; 20,400 rows: 15,817 equal, 20 different, 33 unknown and 4,530 directory-membership-only.', 's4-microos-snapshot-files.tsv'),
 'M08': ('complete pairs recorded', '16,177 snapshot/current full-SHA256 comparisons, all comparison fields known.', 's4-microos-snapshot-current.tsv'),
 'M09': ('current sources/comparisons only', 'Two native SELinux stores listed and snapshot/current comparisons retained; no per-copy original receipt or derivation-event field.', 's4-microos-selinux-stores.tsv;s4-microos-snapshot-files.tsv;s4-microos-snapshot-current.tsv'),
 'M10': ('current bytes recorded', 'grubenv source read status ok, with saved complete bounded bytes.', 's4-microos-sources.tsv'),
 'M11': ('creator/chooser event absent', 'Current grubenv bytes retained; no per-value creation/choice event.', 's4-microos-sources.tsv'),
 'M12': ('snapshot source records retained', 'Snapshot-root RPM source and package membership plus complete path comparisons retained, with per-row unknowns unchanged.', 's4-microos-snapshot-files.tsv;s4-microos-snapshot-current.tsv'),
 'M13': ('solver source/decoding recorded', 'Three solver-cache files; one decoded; content/digest statuses and source evidence retained.', 's4-microos-solver-cache.tsv'),
 'M14': ('choice/use events absent', 'No per-value choice-event or complete consumer/use table emitted; current metadata and eligible digests retained.', 'objects.tsv;full-digests.tsv'),
 'T01': ('current sources only', 'Three current image-source rows; no historical acquisition actor.', 'talos-image-sources.tsv'),
 'T02': ('expanded listings partial', '8,503 members, 1,219 directory listings, zero listing failures and 18 retained boundaries.', 'talos-expanded-members.tsv;talos-listing-coverage.tsv;talos-listing-boundaries.tsv'),
 'T03': ('original reference absent', 'Current listings/hashes/mounts retained; no original installed-image manifest or receipt comparison.', 'talos-content.tsv;talos-expanded-members.tsv;talos-mountinfo.tsv'),
 'T04': ('current namespace recorded; history absent', '29 API-daemon mount rows, query exit0; historical overlay origin and other workload namespaces remain unrecorded.', 'talos-mountinfo.tsv;talos-mountinfo-coverage.tsv;talos-fact-index.tsv'),
 'T05': ('creator/derivation events absent', 'Current listings/hashes retained; no per-member creation/derivation-event record.', 'talos-expanded-members.tsv;talos-content.tsv'),
 'T06': ('bounded hashes/signatures partial', '5,932/5,963 content hashes ok; 31 not-found. Initial Read failures, 34 Copy archive-error attempts, and final refresh results retained.', 'talos-content.tsv;talos-content-attempts.tsv'),
}


def main():
    summary = json.loads((OUT / 'operator/inventory-summary.json').read_text())
    missing = list(csv.DictReader((ROOT / 'S4/MISSING.tsv').open(), delimiter='\t'))
    assert {r['fact'].split(':', 1)[0] for r in missing} == set(FACTS)
    with (OUT / 'MISSING-RECORDED.tsv').open('w', newline='') as file:
        writer = csv.writer(file, delimiter='\t', lineterminator='\n')
        writer.writerow(['machine', 'fact_id', 'fact', 'recorded_fields_status', 'details_and_limits', 'delivery', 'evidence_files'])
        for row in missing:
            machine = row['machine']; code = row['fact'].split(':', 1)[0]
            status, note, filenames = FACTS[code]
            tree = 'raw' if machine == 'alma' else 'handoff'
            paths = ['D1b/' + tree + '/' + machine + '/' + name for name in filenames.split(';')]
            assert all((ROOT / path).is_file() for path in paths)
            writer.writerow([machine, code, row['fact'], status, note,
                             'not delivered: copier exit 1' if machine == 'alma' else 'delivered', ';'.join(paths)])
    n = sum(r['delivered'] for r in summary.values()); k = sum(r['decide'] for r in summary.values()); u = sum(r['unmatched'] for r in summary.values())
    first = f'D1b INVENTORY: {n} of 5 machines; {k} objects to decide; {u} first-night objects without a match'
    lines = [first, '', '2026-11-23 UTC. Operator inventory handoff; independent step review remains responsible for acceptance.', '',
             'The headline counts delivered inventories. All five original observations were obtained and preserved; four handoff copies succeeded. AlmaLinux is not delivered and gives **?** under the committed handoff-failure rule. No object decision is supplied by this record.', '',
             'Inputs: gate `GATES/SUP1-S4-INPUTS-PUSHED`, commit `c62afbb5861fb038aa7da0aa00c0730ad140ec7c`. The required `/usr/bin/python3 -I S4/verify-inputs.py` passed before the first machine; every staged copy also passed. All 49 hash-covered files match; the manifest excludes itself. Release references: `C1/KIT-READY.md`, and for the final MicroOS installation `C1/KIT2-READY.md`, both referenced by `C1/LAB.md`.', '',
             'One operator per machine, no nested work. Gentoo started first with ten free slots observed and four held by its VM; its successful startup preceded the other starts. Every machine was created once and destroyed after its one collector invocation. Native destruction succeeded on all five; no cleanup fallback was needed.', '',
             '| Machine | Original rows (L1 / L2) | Delivered all | Objects to decide | First-night unmatched | Handoff exit |',
             '|---|---:|---:|---:|---:|---:|']
    for m in SYSTEMS:
        s = summary[m]; total, l1, l2 = RAW_COUNTS[m]
        lines.append(f'| {m} | {total} ({l1} / {l2}) | {s["all"]} | {s["decide"]} | {s["unmatched"]} | {1 if m == "alma" else 0} |')
    lines += ['', 'All five copier exit statuses, exact commands and durations: `operator/handoff-status.tsv`. Successful complete audits: `D1b/handoff-audit/{void,gentoo,microos,talos}.json`. AlmaLinux produced no audit or deliverable tree: its exact terminal diagnostic is `_csv.Error: field larger than field limit (131072)` in `operator/handoff-alma.stderr`. The copier was not changed or rerun. All 5,711 original AlmaLinux IDs are listed in `not-delivered-alma.tsv`; its all/part tables contain only the required header.', '',
              'The unchanged matcher ran once per machine with both fixed old tables; all five exits were 0 (`operator/match-status.tsv`). Complete outputs remain in `match/MACHINE/`; machine-specific lists are `match/matched-MACHINE.tsv` and `match/unmatched-MACHINE.tsv`. New IDs in those outputs are unchanged raw IDs; `object-id-map.tsv` maps them to the required prefixed table IDs. Of 2,007 fixed first-night IDs, 1,933 match delivered rows and 74 remain unmatched: 66 AlmaLinux IDs with no delivered inventory, one Void ambiguous-new-key ID, and seven MicroOS ambiguous-first-night-key IDs. All are listed by ID and receive no decision here. No extra first-night input or matching rule was added.', '',
              'Every delivered collector row is preserved in `all-MACHINE.tsv`, in source order. The four non-Gentoo part tables contain exactly matched delivered rows; Gentoo contains all 32,775 rows. Names, machine, members and evidence cells are unchanged. The only table transformations are the required ID prefix, part column and level prefix on kind. Full schemas, fact paths, ID joins, membership and persistence fields are in `FACTS.md`; `MISSING-RECORDED.tsv` records all 45 requested fact groups and their explicit limits.', '']
    for m in SYSTEMS:
        s = summary[m]
        lines += ['## ' + m, '', 'Committed release: **' + RELEASES[m] + '**. ' + LIFECYCLE[m] + '.', '', LIMITS[m], '']
        report = 'report.md' if m == 'talos' else 'REPORT.md'
        lines += [f'Lifecycle, complete separate command outputs and diagnostics: `operator/{m}/`; machine record: `operator/{m}/{report}`. Collector coverage and all failed query streams remain under `D1b/{"raw" if m == "alma" else "handoff"}/{m}/coverage.tsv` and its referenced `raw/` files. Nonzero optional queries were retained, never repaired or repeated.', '']
        if m in ACTION_FILES:
            lines += ['Ordinary actions (`' + ACTION_FILES[m] + '`):', '', '| Action | Exit | Seconds |', '|---|---:|---:|']
            with (OUT / ACTION_FILES[m]).open(newline='') as stream:
                for name, status, seconds in csv.reader(stream, delimiter='\t'):
                    lines.append(f'| {name} | {status} | {seconds} |')
            lines += ['']
            if m == 'gentoo':
                lines += ['`browser_extension` failed once with `UnsupportedOperationException: System access is required` and the emitted `MOZ_REMOTE_ALLOW_SYSTEM_ACCESS=1` diagnostic. Exact full output: `operator/gentoo/actions/actions-logs/browser_extension.stderr` and `.log`. No change or retry; the remaining fixed actions continued. All other eight actions exited 0.', '']
        else:
            lines += ['No ordinary actions assigned.', '']
        lines += ['Facts requested in `S4/MISSING.tsv` (the detailed evidence paths are in `MISSING-RECORDED.tsv`):', '', '| Fact | Recorded fields and limits |', '|---|---|']
        for row in missing:
            if row['machine'] != m:
                continue
            code = row['fact'].split(':', 1)[0]
            status, note, _ = FACTS[code]
            delivery = ' **Not delivered.**' if m == 'alma' else ''
            lines.append(f'| {code} | {status}: {note}{delivery} |')
        lines += ['', f'Objects in `all-{m}.tsv`: {s["all"]}; to decide: {s["decide"]}.', '']
        if s['kinds']:
            lines += ['| Kind | Objects in all |', '|---|---:|']
            lines.extend(f'| {kind} | {count} |' for kind, count in s['kinds'].items())
            lines += ['']
        else:
            lines += ['No delivered kinds; all is header-only. Original count by kind remains in `operator/alma/REPORT.md` and unchanged `D1b/raw/alma/objects.tsv`.', '']
        lines += ['Deviations from committed machine/action/collector/handoff instruments: none.', '']
    lines += ['## Execution disclosures and verification', '',
              'No committed instrument was changed, repaired, substituted or repeated. The Gentoo browser failure and AlmaLinux copier failure were processed exactly by the committed failure rules.', '',
              'Host transport selected the existing user SSH configuration explicitly after the default system configuration ownership error; no configuration changed. Void had one host service submission rejected before process startup because its working-directory syntax was unexpanded; its subsequent submission launched the sole execution. Void monitoring had one transport exit 255 during the network action and continued monitoring the same detached session. An optional adjacent rehearsal diagnostics filename was absent during raw transport; all actual raw files were preserved and verified, and no observation was repeated. Reporting readers increased only their own CSV field-size limit after read-only counting failures; the committed copier was never adjusted. These orchestration/reporting details are recorded in the machine reports and `operator/PROCEDURE.md`.', '',
              'Mechanical preservation checks: `operator/deliverable-verification.json`; handoff copy hashes: `operator/handoff-local-verification.json` and the four copier audits. The final preservation check covers both local originals and handoffs, including complete file sets, all/part selection, raw-ID mapping and member counts. This is operator verification, not independent acceptance.', '',
              'Cleanup evidence: `operator/server-cleanup.json`. All five VM directories were absent before temporary server staging was removed. Original observations, handoffs, audits and operator evidence remain in the task directories; ten shared VM slots are free. In the published AlmaLinux failure traceback, absolute task-root paths are displayed as task-relative paths; the diagnostic and stack line numbers are unchanged (`D1b/handoff-audit/alma-failure.json`).', '']
    (OUT / 'READY.md').write_text('\n'.join(lines))
    print(first)


if __name__ == '__main__':
    main()
