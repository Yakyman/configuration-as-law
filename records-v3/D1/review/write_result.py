import collections
import csv
import datetime
import json
import re
from pathlib import Path


def read(path):
    with open(path, encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle, delimiter='\t', quoting=csv.QUOTE_NONE))


stats = json.loads(Path('D1/review/statistics.json').read_text())
extent = read('D1/review/cards-1-4-extent.tsv')
confirmed = [r for r in extent if r['membership'] == 'CONFIRMED']
assert [r['id'] for r in confirmed] == ['mint-854622d42bc8ca5d899db0ff']
sentences = {}
for line in Path('SENTENCES.md').read_text().splitlines():
    match = re.match(r'- \*\*(S\d(?:\.\d)?-\d+)\*\* (.*)', line)
    if match:
        sentences[match[1]] = match[2].replace('**', '')


def quote(key):
    return f'{key}: “{sentences[key]}”'


out = ['CHECK 1: 1 confirmed holes', 'OUTCOME: 0', '',
       'Recorded 2026-11-22 UTC. Verification of the published text; no changes to its definitions or proposals for changes.', '',
       'Section 4.2 fails on the confirmed Mint object below. Section 4.1 therefore makes the combined outcome 0, despite unresolved objects and the missing Talos inventory. The other four machine outcomes remain ?; none is reported as having withstood the check.', '',
       '## Inventory and comparison', '',
       'Source totals: `D1/compare/STATS.md`. Machine breakdown recomputed from `D1/compare/joined.tsv` by `D1/review/statistics.py`; exact values and input hashes are in `D1/review/statistics.json` and `input-sha256.json`. Inventory rows, including root/user duplicates, are counted without deduplication.', '',
       '| Machine | Objects | Matching decisions | Matching share | Cohen’s kappa | Adjudicated | Confirmed-hole rows | Outcome |',
       '|---|---:|---:|---:|---:|---:|---:|:---:|']
for machine in ('fedora', 'tumbleweed', 'mint', 'flatcar', 'talos', 'TOTAL'):
    r = stats[machine]
    share = f"{100*r['matching_share']:.2f}%" if r['objects'] else '—'
    kappa = f"{r['kappa']:.5f}" if r['kappa'] is not None else '—'
    holes = sum(machine == 'TOTAL' or x['machine'] == machine for x in confirmed)
    out.append(f"| {machine} | {r['objects']} | {r['matching']} | {share} | {kappa} | {r['adjudicated']} | {holes} | {'0' if holes else '?'} |")

out += ['', 'The following are the original adjudication verdicts, not a claim that the 924 initial HOLE labels survived this review:', '',
        '| Machine | RESOLVED:MUST | RESOLVED:NOT | HOLE | UNKNOWN in adjudication | Agreed UNKNOWN outside adjudication | Total input UNKNOWN |',
        '|---|---:|---:|---:|---:|---:|---:|']
for machine in ('fedora', 'tumbleweed', 'mint', 'flatcar', 'talos', 'TOTAL'):
    r = stats[machine]
    v = r['verdicts']
    u = v.get('UNKNOWN', 0)
    out.append(f"| {machine} | {v.get('RESOLVED:MUST',0)} | {v.get('RESOLVED:NOT',0)} | {v.get('HOLE',0)} | {u} | {r['unknown']-u} | {r['unknown']} |")
out += ['', 'The 89 input UNKNOWN rows are enumerated in `D1/review/original-unknown.tsv`: Flatcar has 64 stored-object directory groups and one process; Mint has 13 package rows; Fedora has eight RPM and three Flatpak package rows. Talos’s zero UNKNOWN rows means no inventory, not complete knowledge.', '',
        'The resolved sample adds three explicitly unsupported resolutions: `tumbleweed-e0e07676a2b45150a7303e31` (process 12), `flatcar-42cb73fd18430fd11f5d305f` (`/etc/selinux/targeted/contexts`), and `flatcar-8e7f275dda3033c6764dbce1` (`/etc/selinux/mls/contexts/files`). A failed executable-link lookup concatenated two process records; the two SELinux directory inventories do not establish active consumers. The review additionally retains as UNKNOWN the 20 original card-1/card-2 rows with unresolved whole-object facts and the two residual original card-5 firmware rows lacking a demonstrated deciding function. The resulting explicit UNKNOWN set has 114 rows: Fedora 13, Tumbleweed 1, Mint 32, Flatcar 68; exact ids and provenance are in D1/review/final-unknown.tsv. Its main kinds are 67 stored-object groups, 32 dpkg packages, 10 RPM packages, three Flatpak packages and two processes. This set is distinct from broader uncertain hole-membership searches: a search match can have another deciding function and is not automatically an UNKNOWN object.', '', quote('S3-2'), '',
        '## Confirmed hole: Shared presentation content versus loss of capability', '',
        'Removing the shared emoji font can be described either as losing its particular glyph content or as losing the ability to render those glyphs. The text does not decide which description applies while the programs and their general rendering operations remain available.', '',
        quote('S2.2-2'), '', quote('S2.2-4'), '', quote('S2.2-7'), '', quote('S2.2-13'), '',
        'This is one missing distinction, not two sentences that independently and unconditionally give opposite decisions. S2.2-4’s full condition matters: merely calling something a database does not exempt it. Conversely, counting every unavailable rendering of removed content as a lost capability would also defeat the express document exemption. S2.2-13 calls read values settings but does not make content and settings disjoint; the one-program exemption does not decide this shared-font case. The question is whether the object must be recorded, not how a system should treat data under Section 2.5.', '',
        '| Example id | Name | Installed version | Rows |',
        '|---|---|---|---:|',
        '| mint-854622d42bc8ca5d899db0ff | root:fonts-noto-color-emoji | 2.047-0ubuntu0.24.04.1 | 1 |', '',
        'Exact established extent: this one Mint row; Fedora 0, Tumbleweed 0, Flatcar 0, Talos 0 inventoried rows. It is an original card-1 row. Its glyph/font role is recorded in both classifications and the package file list; the installed version is in `D1/in/raw/mint/raw/003-packages-root-dpkg-query.out`. Exact-version package-control evidence in `D1/review/cards14-raw/mint-fonts-noto-color-emoji-control.json` establishes no dependency/relationship fields or maintainer scripts/triggers that independently settle the package. The installed dependency search and source provenance are in `D1/review/cards-1-4.md` and its linked metadata records.', '',
        'The strongest successful refutation of most other card-1/card-2 rows is package metadata: their inventory object is the whole installed package, whose constraints or scripts affect package-manager behaviour even when its payload contains only data. The review applied that same argument consistently to the two samples. It did not transfer a payload-only ambiguity to a package already decided by an independent operational function.', '', quote('S2.2-1'), '',
        'Whole-table search by kind and name is recorded in `D1/review/cards-1-4-extent.tsv`, including names beyond the adjudicated rows. The 602 detailed matches contain 581 independently decided MUST rows, this one confirmed row, and 20 factually unresolved membership candidates (Mint 19; Flatcar 1). Of the original card-1 rows, 405 are excluded by independent MUST reasons, seven have unresolved membership and one is confirmed; of card 2, 148 are independently MUST and 13 have unresolved membership. All 28 additional matches are independently MUST. The enumerated one-row extent is exact for established cases; unresolved payload/version facts are not silently counted as absent or as confirmed holes.', '',
        '## Other cards and refutation records', '',
        'Original-card dispositions: one CONFIRMED in narrowed extent, five REFUTED, two FACT-WRONG, zero OUTSIDE. Each original example is addressed in `D1/review/cards-1-4.md` or `D1/review/cards-5-8.md`; the source adjudication files are unchanged.', '',
        '- Card 2 — REFUTED as an established package-level counterexample: verified metadata/operational controls decide MUST by S2.2-1; unavailable exact payload/metadata facts yield ? by S3-2, not a confirmed content/lookup collision.',
        '- Card 3 — REFUTED: dependency metadata controls later package selection/retention, which S2.2-1 includes; S2.2-2 contains no immediate-only restriction.',
        '- Card 4 — REFUTED: read by one program is not in force only inside one program; the established effects on sessions, other processes and installed-file labels satisfy S2.2-1.',
        '- Card 5 — REFUTED as an established inventory counterexample: verified forward/reverse dependency metadata independently decides 56 original rows; two residual rows lack facts establishing the proposed hardware counterfactual, so S3-2 applies rather than confirming a hole. `D1/review/card5-challenge.md` preserves the competing scope readings without choosing between them.',
        '- Card 6 — REFUTED: the established generated operational inputs satisfy S2.2-1; regeneration is not an exemption, and whether a declaration computes them is outside its required form under S2.5-3.',
        '- Card 7 — FACT-WRONG: API effects were equated with unrestricted rights, and use of an interface with confinement; the saved browser/bridge, XSLT and lens evidence contradicts that premise. Independently, verified dependency metadata decides all 14 package rows MUST.',
        '- Card 8 — FACT-WRONG: SeaBIOS/OVMF packages also contain host-read firmware-selection descriptors used by installed libvirt to configure QEMU; their whole-package code-only premise fails. Guest-only images and ROMs themselves are explicitly exempt under S2.2-11/12.', '',
        quote('S2.2-10'), '', quote('S2.2-11'), '', quote('S2.2-12'), '', quote('S2.5-3'), '',
        'Card 5’s separate whole-table search has 1,314 broad kind/name matches: 1,233 excluded from that proposed gap, 81 with uncertain membership, zero proven included (`D1/review/card5-extent.tsv`). Those membership labels do not assert 81 additional object UNKNOWN decisions and do not alter the confirmed-hole count.', '',
        '## Seeded samples', '',
        'Sampling uses Python `random.Random(seed).sample` on eligible rows in source order, parsed with tab delimiter and `csv.QUOTE_NONE`. Seeds were fixed before reading the selected rows; there was no redraw. Ordered ids, exact cited sentences, factual evidence and every disposition are saved in the two sample TSVs and companion reports. `D1/review/verify_samples.py` reproduces both ordered draws.', '',
        '| Sample | Population | Seed | Drawn | Upheld | Corrected to MUST; candidate REFUTED | OUTSIDE | UNKNOWN | New confirmed holes |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|',
        '| RESOLVED:* adjudication rows | 888 | 2026112201 | 40 | 21 | 9 | 7 | 3 | 0 |',
        '| Agreed rows absent from adjudication | 14681 | 2026112202 | 60 | 57 | 3 | 0 | 0 | 0 |', '',
        '| Machine | Resolved sample | Agreed sample |',
        '|---|---:|---:|',
        '| fedora | 6 | 26 |',
        '| tumbleweed | 6 | 24 |',
        '| mint | 7 | 7 |',
        '| flatcar | 21 | 3 |',
        '| talos | 0 | 0 |',
        '| TOTAL | 40 | 60 |', '',
        'The nine corrected resolved rows and three incorrect agreements overlooked package metadata while reasoning only from payload or immediate runtime effects. They are resolved by S2.2-1, not new holes. In the agreed sample they are `fedora-fe662177103b7d48f6e25461` (`user:default-fonts-syr`), `fedora-4ffd8592f62f9410b26561b5` (`root:default-fonts-el`), and `mint-707cb6be107ec462ef11c223` (`root:gnome-terminal-data`). One otherwise upheld firewall row also had a mistaken c2 factual explanation; the c1 jump-target evidence independently supports MUST. Detailed records: `D1/review/resolved-sample.tsv`, `resolved-report.md`, `agreed-sample.tsv`, and `agreed-report.md`.', '',
        'The seven OUTSIDE candidates concern program-state bookkeeping or a private temporary directory. S2.5-1 disposes of the design question; it does not literally prove a universal NOT-recorded rule for such objects. The process candidate rests on a FACT-WRONG reading of the saved output; the two SELinux candidates lack operational-use facts. All three therefore remain UNKNOWN under S3-2 rather than becoming holes.', '', quote('S2.5-1'), '',
        '## Inventory limits and committed-input deviations', '',
        'Source: `D1/in/READY.md`; committed inputs at `43594a47b72707f836953b6b39d5849d5513f61a`. Inventories exist for four of the five committed systems. Releases were Fedora 45-1.4, Tumbleweed 20261120, Mint 22.3 Cinnamon, Flatcar 4757.2.3 stable and Talos 1.14.6. No release, ordinary-action command body, runner bytes, collector bytes or VM base was substituted. Desktop ordinary actions all recorded success: Fedora 15, Tumbleweed 15, Mint 17; no command was repeated.', '',
        '| Machine | Collector coverage records | Nonzero statuses | Material coverage limit |',
        '|---|---:|---:|---|',
        '| fedora | 118 | 74 | Filesystem query exited 1; zero level-2 rows. One serial-login and two serial-command timeouts. |',
        '| tumbleweed | 118 | 72 | Filesystem query exited 1; zero level-2 rows. Two serial-command timeouts. |',
        '| mint | 110 | 106 | Filesystem query exited 1; zero level-2 rows; inventory contains only accounts, groups and dpkg packages. 96 serial-login timeouts. |',
        '| flatcar | 124 | 84 | Partial failed-query coverage; 852 level-2 rows present. Eight repeated source-id occurrences retained with suffixes. |',
        '| talos | — | — | No inventory: collector terminated with exit -15. |', '',
        'Execution adaptations listed in READY: continuation after failed commands replaced the scripts’ global stop-on-error behaviour; the unchanged runner was deployed as task-local `lab.sh`; Tumbleweed used the committed runner identifier `opensuse`; host-only connection and service-launch adjustments were recorded in `control/operator-notes.md`. These adaptations did not alter committed command bodies. Identifier suffixing did not remove Flatcar rows.', '',
        'Talos termination is an execution deviation: the first pagemap read streamed more than 137 GB over 1,112 seconds, while the saved listing contained 359 pagemap paths and 114,323 regular files that the collector would read without a bound before writing its object table. No repair, selective continuation, synthesized inventory or rerun was performed. Evidence: `D1/in/control/talos/termination.json`, `host-read-observation.json`, `listing-operational-counts.json`, and `review-talos-operation.md`. Missing queries and the terminated collector are data insufficiency, not definition-derived failures. The confirmed Mint counterexample independently sets the overall outcome to 0.', '',
        'Quote validation: `/usr/bin/python3 -I bin/check_quotes.py D1/RESULT.md`; output retained in `D1/review/validation.txt`.']
Path('D1/RESULT.md').write_text('\n'.join(out)+'\n')
