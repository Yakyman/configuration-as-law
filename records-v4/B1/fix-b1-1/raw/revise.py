"""Apply only FX-B1-1 corrections to the preserved original classification."""
from pathlib import Path
from collections import Counter
import csv
import json
import re

F = Path(__file__).resolve().parents[1]
B = F.parent
rows = list(csv.DictReader((B / 'CHANNELS-V4.tsv').open(), delimiter='\t', quoting=csv.QUOTE_NONE))
original = {r['variant'].split()[0]: dict(r) for r in rows}
d = {r['variant'].split()[0]: r for r in rows}

# Finding 1: retain both readings; do not adopt one as a new interpretation rule.
for rid in ['C5.1', 'C5.2', 'C5.3', 'C5.4', 'C5.5']:
    r = d[rid]
    r['route'] = ('TWO_WAYS for the specialized build/output operation: reading A [BUILTIN], '
        'documented executable production/replacement changes what is installed via S8.2-10, '
        'so falls under S8.1-7; reading B [GENERAL], compilation/build processing or copying '
        'an output is general-purpose work, with S8.1-8 expressly excluding copying and link creation; '
        'the text does not say which reading governs this functionality. Separately invoked shell, '
        'editor, manual copy and link operations are [GENERAL] (S8.1-8). '
        '[compiler purpose](https://gcc.gnu.org/onlinedocs/gcc/G_002b_002b-and-GCC.html) '
        '[compiler output](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html) '
        '[build and install purpose](https://cmake.org/cmake/help/latest/manual/cmake.1.html). '
        'Evidence: SOURCES.md E083, E085, E093, E094; GAPS.md.')
    if rid == 'C5.3':
        r['route'] += (' The documented install target strengthens reading A; reading B treats '
            'its output copying/linking as the expressly excluded functionality. S8.1-8 names '
            'an installer exception, but no removing-programs purpose under S8.1-4 is established here.')
    if rid == 'C5.4':
        r['route'] += (' [BREAKING] separately privileged direct replacement outside built-in tools '
            'past the declaration (S8.1-15, S8.1-16); this is not a claim that root use of a built-in tool is breaking.')
    r['law'] += (' Under reading A, S8.3-7 requires the acting build tool itself to record its changes. '
        'Under reading B, that tool-specific duty is not established; S8.3-6 and S8.3-8 still '
        'disallow an ordinary unrecorded installed-program change. The output recording duty '
        'under S8.2-1 and S8.2-16 is unchanged under both readings.')
    r['status'] = 'TWO_WAYS'
    r['reason'] = ('Executable output is decided. Its producer has two route readings: built-in because it '
        'changes installed programs, or general-purpose build/copy functionality. The text does not '
        'select the tool-specific recording obligation.')

# Finding 2: this variant already specifies confined browser web code.
r = d['C7.19']
r['record'] = ('a: no separate runtime line, follows renderer/program (S8.2-5); '
    'b: the saved generated web-page code runs inside the recorded renderer and need not be recorded '
    'under the express web-page example in S8.2-21; serialization for later reuse does not introduce '
    'a separate host execution route. Non-code cache metadata need not be recorded (S8.2-2, S8.2-15). '
    'c: package/program line for every separate helper executable (S8.2-16, S8.2-22). '
    'Evidence: SOURCES.md E096-E098. No general exemption for arbitrary browser-related executables is inferred.')
r['law'] += (' For b, apply the S8.2-21 web-page exemption; the cache need not receive a declaration '
    'line. The recorded renderer/helper executables remain subject to the quoted properties.')
r['status'] = 'DECIDED'
r['reason'] = ('The fixed variant is confined web-page code inside recorded renderer/helper programs. '
    'S8.2-21 expressly exempts that web-page code, including its reusable generated form; separate '
    'renderer/helper executables remain recorded.')

# Finding 3: make the interpretation dispute visible rather than request syntax facts.
history_kind = ('Q1 no; reading A: S8.2-23 applies to the documented history-file reader, '
    'which reads entries as values, so Q2 no, Q3 no, Q4 kind=program record (S8.2-15). '
    'Reading B: saved language statements are code the computer can execute at a person\u2019s command '
    '(S8.2-9), so Q2 yes, kind=program (S8.2-10), stop; S8.2-6 says clarifications do not '
    'change question order. The text does not delimit only reads as values against this capability reading.')
history_record = ('reading A: need not be recorded (S8.2-2, S8.2-15, S8.2-23); '
    'reading B: own line or an actual source/build line (S8.2-16), not merely the interpreter line. '
    'The dispute is the scope of S8.2-23 versus S8.2-9, not an asserted unknown syntax fact.')
for rid, label in [('C7.06', 'b'), ('C7.17', 'c')]:
    r = d[rid]
    r['kind'] = r['kind'].split('; ' + label + ':', 1)[0] + '; ' + label + ': ' + history_kind
    r['record'] = r['record'].split('; ' + label + ':', 1)[0] + '; ' + label + ': ' + history_record
    r['law'] += (' For saved history, reading A creates no recording duty or P4 requirement for '
        'that record; reading B requires recording the program and forbids an ordinary '
        'unrecorded program change. The original typed command remains an action (S8.2-4).')
    r['status'] = 'TWO_WAYS'
    r['reason'] = ('History is read as values under S8.2-23, yet retained language statements fit '
        'the execution-capability reading of S8.2-9. The text does not delimit those readings; '
        'missing syntax is not used to choose between them.')
    r['leaves'] += '; history-use evidence: SOURCES.md E005, E105.'

# Finding 4: remove an explicitly hypothetical, uninstantiated kind from the row and counts.
r = d['C7.07']
r['kind'] = r['kind'].replace(' (Q1 instead wins if supplied unchanged in an installed package)', '')

# Findings 5 and 6: separate evidenced system mount from an unidentified updater.
r = d['C3.5']
r['route'] = ('[GENERAL] archive extraction and application launching without superuser rights; '
    'these functions have no documented installation/configuration purpose meeting S8.1-7; '
    'manual copy/link/shell functions are expressly general-purpose under S8.1-8. '
    '[BUILTIN] the system mount utility configures filesystems (S8.1-7; S8.2-13), '
    'documented as part of util-linux. [UNKNOWN] bundled/external updater: the generic '
    'AppImage documentation does not identify the actual updater or establish its status '
    'as a program of the system under S8.1-7. No installer label is inferred without '
    'the installing-and-removing purpose of S8.1-4. '
    '[mount purpose](https://man7.org/linux/man-pages/man8/mount.8.html) '
    '[AppImage update modes](https://docs.appimage.org/packaging-guide/optional/updates.html). '
    'Evidence: SOURCES.md E078, E103.')
r['status'] = 'FACT_UNKNOWN'
r['reason'] = ('Extracted and updated code remains Q2. Mount purpose is documented. The generic '
    'updater description does not identify the actual program or establish that it is a '
    'program of the system under S8.1-7.')
r = d['C4.3']
r['route'] = ('[GENERAL] download/copy/synchronization without superuser rights. The documented '
    'curl purpose is data transfer, not installation/configuration meeting S8.1-7; '
    'S8.1-8 explicitly covers copying, not downloading. [UNKNOWN] AppImage updater: '
    'the generic update-mode description does not identify the actual updater or establish '
    'a program of the system under S8.1-7; no S8.1-4 installing-and-removing purpose is inferred. '
    '[curl purpose](https://curl.se/docs/manpage.html) '
    '[AppImage update modes](https://docs.appimage.org/packaging-guide/optional/updates.html). '
    'Evidence: SOURCES.md E078, E079, E104.')
r['status'] = 'FACT_UNKNOWN'
r['reason'] = ('Ordinary download/copy is general-purpose. The updater\u2019s identity and status as a '
    'program of the system are unestablished. The output\u2019s Q2 recording duty does not '
    'depend on resolving the acting route.')
for rid in ['C3.5', 'C4.3']:
    d[rid]['law'] += (' The output-program recording duty is established; whether the '
        'unidentified updater itself has the built-in-tool duty in S8.3-7 remains fact-unknown.')

# Finding 7: document locations and qualify the conditional hook-directory default.
d['C6.3']['leaves'] += ' User-mode load-path table: SOURCES.md E100.'
r = d['C9.5']
r['leaves'] = r['leaves'].replace('b: hook JSON under /etc/containers/oci/hooks.d/*.json',
    'b: configured hook JSON under <hooks-dir>/*.json; /etc/containers/oci/hooks.d/*.json '
    'is one deprecated default for root callers when --hooks-dir is unset, not a universal rootless path')
r['leaves'] += ' Exact options and hook-directory conditions: SOURCES.md E101-E102.'

with (F / 'CHANNELS-V4.tsv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t', quoting=csv.QUOTE_NONE, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)

changes = {rid: {k: {'before': original[rid][k], 'after': r[k]}
    for k in r if original[rid][k] != r[k]} for rid, r in d.items() if original[rid] != r}
(F / 'raw/changes.json').write_text(json.dumps(changes, indent=2, ensure_ascii=False) + '\n')

# Reaggregate changed row tags and the corrected membership ledger; no probes are rerun.
old_counts = json.loads((B / 'raw/counts.json').read_text())
kind_rows = old_counts['kinds']
kind_rows['Installed object'].remove('C7.07')
route_names = {'INSTALLER': 'Installer', 'BUILTIN': 'Other built-in tool',
    'GENERAL': 'General-purpose program without superuser rights',
    'BREAKING': 'Privileged change past the declaration outside built-in tools',
    'UNKNOWN': 'Acting route not established'}
route_rows = {v: [] for v in route_names.values()}
for r in rows:
    for tag in set(re.findall(r'\[(INSTALLER|BUILTIN|GENERAL|BREAKING|UNKNOWN)\]', r['route'])):
        route_rows[route_names[tag]].append(r['variant'].split()[0])
counts = Counter(r['status'] for r in rows)
(F / 'raw/counts.json').write_text(json.dumps({'status': dict(counts), 'routes': route_rows,
    'kinds': kind_rows}, indent=2) + '\n')
(F / 'raw/kind-count-method.md').write_text('''# Kind membership correction

Use the original raw/counts.json membership ledger for unchanged classifications. Remove C7.07 from Installed object: its original extra Q1 clause was hypothetical, not the classification of either described file. The revised row removes that clause. The other changed rows retain their object kinds; history rows still contribute both Program and Program record, now as textual readings rather than unknown facts. C7.19 changes recording exemption, not its Q2 kind. Evidence additions do not change kinds. No other kind membership changes.

Counts are nonexclusive row incidence for described objects and explicit classified branches, including both textual readings and known conditional branches. This does not count generic hypothetical rules, unidentified extra outputs, or the twelve M rows. Counts are not observations of particular installations. Branches such as packaged versus unpackaged existing executables remain explicit branches; C7.07 instead describes both inputs as Q2 programs.
''')
line = (f"CHANNELS: {counts['DECIDED']} decided, {counts['NOT_DECIDED']} not decided, "
        f"{counts['TWO_WAYS']} two ways, {counts['FACT_UNKNOWN']} fact unknown")
result = line + '''

FX-B1-1 revision. The current classification, gaps and primary excerpts are in [fix-b1-1/](fix-b1-1/); the original CHANNELS-V4.tsv, GAPS.md, SOURCES.md, raw outputs and reviews are preserved. The original result is [fix-b1-1/inputs/RESULT-before.md](fix-b1-1/inputs/RESULT-before.md). Finding-by-finding disposition: [FIX-B1-1.md](FIX-B1-1.md).

All 88 identifiers and names remain in their original order: 76 C rows and 12 M rows. This remains the separate, unweighted investigation under PROTOCOL.md Section 5. No planned-check outcome, system-feasibility verdict, or gap weight is assigned.

Counts are nonexclusive row counts for described objects and explicitly classified branches, including both textual readings and factual alternatives. Generic hypothetical rules, unidentified additional outputs, and the twelve M rows' generic kind rules are excluded. Exact membership and the one kind-membership correction are in [counts.json](fix-b1-1/raw/counts.json) and [kind-count-method.md](fix-b1-1/raw/kind-count-method.md).

## Counts per route

| Route | Rows |
|---|---:|
'''
for name, ids in route_rows.items():
    result += f'| {name} | {len(ids)} |\n'
result += '''
Installer is separate from other built-in functionality. The five C5 rows count both route readings. C3.5 counts the established mount route and an unknown updater route; C4.3 no longer asserts a built-in updater. Root use of a built-in tool is not itself breaking (S8.1-15).

## Counts per kind

| Kind | Rows |
|---|---:|
'''
for name, ids in kind_rows.items():
    result += f'| {name} | {len(ids)} |\n'
result += '''
The runtime category follows S8.2-5 and is not an additional separate-object class. C7.07 is counted only as Program and runtime; its hypothetical installed-package alternative is excluded. History contributes both textual readings. C7.19 remains code at Q2, with the S8.2-21 recording exemption.

## Kinds of gap

- **Home-page navigation and launching something** — C8.08: setting with its own line versus program record requiring none.
- **Compiler and build-tool purpose versus general-purpose work** — C5.1, C5.2, C5.3, C5.4, C5.5: built-in versus general-purpose route; output recording is required under both readings, but the tool-specific recording duty differs.
- **Saved history: values read versus executable statements** — C7.06, C7.17: program record requiring no line versus program requiring a line.

All eight gap rows are TWO_WAYS; none is NOT_DECIDED. [GAPS.md](fix-b1-1/GAPS.md) gives exact quotations and the declaration/system-behaviour consequences without choosing a reading or proposing a text change.

Evidence: [CHANNELS-V4.tsv](fix-b1-1/CHANNELS-V4.tsv), [SOURCES.md](fix-b1-1/SOURCES.md), [cell changes](fix-b1-1/raw/changes.json), [validation](fix-b1-1/raw/validation.txt), and [quotation checks](fix-b1-1/raw/check-quotes.txt). Only affected rows and dependent aggregates were regenerated; no runtime experiment was repeated. Original inputs and artifacts are hash-checked in validation. Independent acceptance of this revision is pending; the preserved reviews concern the earlier result.
'''
(B / 'RESULT.md').write_text(result)
print(line)
print('Changed rows:', ', '.join(changes))
print('Routes:', {k: len(v) for k, v in route_rows.items()})
print('Kinds:', {k: len(v) for k, v in kind_rows.items()})
