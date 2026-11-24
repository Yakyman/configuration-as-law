from pathlib import Path
import csv, json, re
from collections import Counter

B = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((B/'CHANNELS-V4.tsv').open(), delimiter='\t', quoting=csv.QUOTE_NONE))
sources = {}
def add(url, title, quote, note=''):
    if url not in sources:
        sources[url] = (title, quote, note)

# One short primary-source excerpt per URL; intermediate ledgers are audit inputs.
for block in re.split(r'^## ', (B/'raw/root-sources.md').read_text(), flags=re.M)[1:]:
    title = block.splitlines()[0]
    url = re.search(r'\]\((https?://[^)]+)\)', block)[1]
    quote = re.search(r'Documentation excerpt: «(.*?)»', block)[1]
    note = block.split('»', 1)[1].strip()
    add(url, title, quote, note)
for block in re.split(r'^## ', (B/'part-config/sources.md').read_text(), flags=re.M)[1:]:
    title = block.splitlines()[0]
    url = re.search(r'^https?://\S+', block, re.M)[0]
    quote = ' '.join(re.findall(r'^> ?(.*)', block, re.M))
    add(url, title, quote)
for line in (B/'part-install/sources.md').read_text().splitlines():
    m = re.match(r'- \*\*(.*?)\*\* \[.*?\]\((https?://[^)]+)\): “(.*)”', line)
    if m: add(m[2], m[1], m[3])
for block in re.split(r'^## ', (B/'raw/supplement-sources.md').read_text(), flags=re.M)[1:]:
    title = block.splitlines()[0]
    url = re.search(r'\]\((https?://[^)]+)\)', block)[1]
    quote = ' '.join(re.findall(r'^> ?(.*)', block, re.M))
    note = re.split(r'^> .*\n', block, flags=re.M)[-1].strip()
    add(url, title, quote, note)
add('https://pip.pypa.io/en/stable/cli/pip_uninstall/', 'pip removal purpose',
    'pip is able to uninstall most installed packages.', 'Together with pip install, this establishes the installing-and-removing purpose required by S8.1-4.')
add('https://gcc.gnu.org/onlinedocs/gcc/G_002b_002b-and-GCC.html', 'Compiler purpose',
    'GCC is an integrated distribution of compilers for several major programming languages.',
    'The output-options manual documents compilation and executable output. The route decision applies S8.1-7 to that specialized purpose; it does not infer an installer/removal purpose.')
add('https://cmake.org/cmake/help/latest/manual/cmake.1.html', 'Build and installation purpose',
    'CMake provides a command-line signature to install an already-generated project binary tree:',
    'The Description identifies a dedicated build-system generator; the Install a Project section documents cmake --install. Generic shell/copy/link operations are separate operations under S8.1-8.')
add('https://packaging.python.org/en/latest/specifications/binary-distribution-format/', 'Direct imports from some wheels',
    'a subset of wheel files do support being placed directly on `sys.path`.',
    'The direct-import FAQ and zipimport documentation distinguish executable archive members from non-loadable archives. A cache label alone does not establish Q4. The actual retained wheel contents are unspecified in C2.1, C2.3 and C2.5.')
add('https://v8.dev/blog/improved-code-caching', 'Serialized executable-code cache',
    'Chrome stores the serialized generated code onto the disk cache and keys it with the URL of the script resource.',
    'Background explains later deserialization and reuse instead of recompilation, subject to compatibility checks. Cache presence depends on policy and eligibility; a single channel invocation does not guarantee a new entry.')
add('https://chromium.googlesource.com/chromium/src/+/main/content/browser/storage_partition_impl.cc', 'Browser code-cache root',
    'code_cache_path = settings.path().AppendASCII("Code Cache");',
    'The branch uses this path only for an enabled, non-memory cache. Partition settings supply the cache root.')
add('https://chromium.googlesource.com/chromium/src/+/main/content/browser/code_cache/generated_code_cache_context.cc', 'Browser code-cache subdirectories',
    'base::FilePath generated_js_code_cache_path = path.AppendASCII("js");',
    'The same initialization code names pc for the newer persistent collection backend; it can remove the older js cache. These are alternative layouts, not two entries asserted for every run.')
add('https://raw.githubusercontent.com/mozilla-firefox/firefox/main/toolkit/mozapps/extensions/internal/XPIDatabase.sys.mjs', 'Extension registration database',
    'const FILE_JSON_DB = "extensions.json";',
    'PROP_JSON_FIELDS includes userDisabled; toJSON serializes these fields, setUserDisabled updates activation state, and database property updates save the JSON database in the profile. Generated state is distinguished from the installed extension bundle.')

# Clarify the narrower evidence from the sandbox source after independent review.
url = 'https://chromium.googlesource.com/chromium/src/+/main/docs/design/sandbox.md'
t, q, _ = sources[url]
sources[url] = (t, q, 'This documents inability to make persistent changes. It does not establish the separate no-program-launch condition for every browser interface required by S8.2-21. C7.19 therefore leaves the saved-code exemption fact-unknown; renderer/helper executables still require recording.')
url = 'https://docs.wasmtime.dev/security.html'
t, q, n = sources[url]
sources[url] = (t, q, n+' The CLI implementation cited separately fixes its WASI permission to ReadWrite; effective host permissions and reachable content remain unspecified.')

out = '''# Primary source excerpts

Checked 2026-11-23 UTC. These excerpts support the directly linked documentation in CHANNELS-V4.tsv. Classification and coverage are deductions from the fixed text, not assertions made by the tool manuals. No virtual machines, builds, installations, or runtime probes were used.

Paths containing $HOME, <profile>, <prefix>, <path>, or similar parameters are documented path templates, not paths of the host. Optional artifacts are identified conditionally. The table does not assert that every possible cache, history entry, or script-created output appears in every invocation.

The original first-column names and the explicit custom-dispatch premise come from the authorized previous CHANNELS.md. Its version-3 verdicts are not evidence for the present decisions. Raw and part files preserve intermediate drafting evidence; CHANNELS-V4.tsv, GAPS.md, and RESULT.md are the final classification.

S8 sentence IDs refer to SENTENCES.md. B1-9.3-command, B1-9.3-channel, B1-9.3-stream, and B1-A.4.3-removal are local labels for the exact imported passages in TEXT.md; they are not new numbered hypothesis sentences. Quoting P4 follows the published label of the property called C4 in the task.

'''
for i,(url,(title,quote,note)) in enumerate(sources.items(),1):
    out += f'## E{i:03d} — {title}\n\n[{title}]({url})\n\n> {quote}\n\n'
    if note: out += note+'\n\n'
(B/'SOURCES.md').write_text(out)

# Nonexclusive row incidence, including explicitly classified conditional branches.
# I=installed object, P=program, S=setting, R=program record, M=material,
# T=exists only while the computer runs (S8.2-5; not a separate object).
groups = {
 'C1.': ['IR','IR','IRPM','IST','SIT','RPI'],
 'C2.': ['IRP','ISR','IPMR','PSRI','IPRT','IPR'],
 'C3.': ['IRS','ISM','IST','PST','PTM'],
 'C4.': ['PST','MP','P','PT','T'],
 'C5.': ['PMTR','PRT','PS','P','PI'],
 'C6.': ['S','ST','T','SP','PTI','ST'],
 'C7.': ['PT','PT','T','TR','PT','TPR','PIT','PT','IPT','PT','IPT','PST','IPT','IPT','T','T','IPTR','PIT','TPRI','PT','PT','TP','IPTS','PT','TIP'],
 'C8.': ['P','PTS','TP','PI','STP','TP','ISR','RS'],
 'C9.': ['IPST','IPST','PIS T','IPMS','SIPT','IPST'],
 'C10.': ['IRST','ST','I','ISP'],
}
kind_names = {'I':'Installed object','P':'Program','S':'Setting','R':'Program record','M':'Material','T':'Exists only while the computer runs'}
kind_rows = {v:[] for v in kind_names.values()}
for r in rows:
    rid = r['variant'].split()[0]
    if rid.startswith('M'): continue
    prefix, number = rid.rsplit('.',1)
    for code in set(groups[prefix+'.'][int(number)-1].replace(' ','')):
        kind_rows[kind_names[code]].append(rid)
route_names = {'INSTALLER':'Installer','BUILTIN':'Other built-in tool','GENERAL':'General-purpose program without superuser rights','BREAKING':'Privileged change past the declaration outside built-in tools','UNKNOWN':'Acting route not established'}
route_rows = {v:[] for v in route_names.values()}
for r in rows:
    for tag in set(re.findall(r'\[(INSTALLER|BUILTIN|GENERAL|BREAKING|UNKNOWN)\]',r['route'])):
        route_rows[route_names[tag]].append(r['variant'].split()[0])
counts = Counter(r['status'] for r in rows)
line = f"CHANNELS: {counts['DECIDED']} decided, {counts['NOT_DECIDED']} not decided, {counts['TWO_WAYS']} two ways, {counts['FACT_UNKNOWN']} fact unknown"
result = line+'''

All 88 identifiers and names are preserved in original order: 76 C rows and 12 M rows. This is the separate, unweighted investigation under PROTOCOL.md Section 5; it makes no system-feasibility verdict and adds no weighted failure to the planned checks.

Counts below are nonexclusive row counts: a composite variant may contain several routes and kinds. Explicit alternatives are included; therefore columns need not sum to 88. The twelve M rows identify cross-channel obligations without an actual tool or artifact inventory; their generic classification rules are not counted as established object kinds. Unknown extra outputs in other rows are likewise excluded. Exact row membership is saved in raw/counts.json.

## Counts per route

| Route | Rows |
|---|---:|
'''
for name,ids in route_rows.items(): result += f'| {name} | {len(ids)} |\n'
result += '''
Installer is counted separately from other built-in functionality, although S8.1-7 includes installers among built-in tools. Breaking is counted only for the explicitly described privileged, outside-tool, past-declaration branch; root use of a built-in tool is not breaking.

## Counts per kind

| Kind | Rows |
|---|---:|
'''
for name,ids in kind_rows.items(): result += f'| {name} | {len(ids)} |\n'
result += '''
The runtime category follows S8.2-5 and is not an additional separate-object class. The kind counts include known parts and expressly classified alternatives of FACT_UNKNOWN rows, as well as both readings of C8.08; they are not counts of observed installations.

## Kinds of gap

- **Home-page navigation and launching something** — C8.08 (TWO_WAYS): the saved home-page URL is either a setting requiring a line or a program record requiring none, depending on the meaning of launching something in S8.2-14. See GAPS.md for the two declaration and system-behaviour consequences and exact quotations.

No NOT_DECIDED rows. The other incomplete rows identify missing tool/artifact facts in their status and reason cells; no missing implementation mechanism from Section 8.5 is counted as a gap.

Evidence: CHANNELS-V4.tsv contains each row's facts, ordered decisions, required coverage, route and exact law quotations; SOURCES.md supplies short primary excerpts. The quotation check output is raw/check-quotes.txt; the independent review is review.md.
'''
(B/'RESULT.md').write_text(result)
(B/'raw/counts.json').write_text(json.dumps({'status':dict(counts),'routes':route_rows,'kinds':kind_rows},indent=2)+'\n')
print(line)
print('Sources:',len(sources))
print('Routes:',{k:len(v) for k,v in route_rows.items()})
print('Kinds:',{k:len(v) for k,v in kind_rows.items()})
