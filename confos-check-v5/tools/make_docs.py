#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.dont_write_bytecode=True
from casedefs import CASES
header='''# Cases for the source-built terminal system

2026-11-26 UTC. Specification: paper 6 §5 (version 5) and §7, paper 5 §9
Table 9, and the stand review R1–R10 where §5 does not supersede them.
PROGRAMS.md chooses the minimum programs; PORT.md preserves every old case ID.
There has been no operating-system run. These are portable case definitions.

## Execution and evidence

`python3 -B run --list`, `run --validate`, and `run --case ID --plan` inspect
these definitions. `casedefs.py` is authoritative; `plans.json` contains its
fully expanded primitive steps and assertions. Release-specific operations are
translated only by adapter.py and must be bound before a real run. Unknown
capabilities and missing evidence are unobserved, never refusals or passes.
Every variant listed below is a separate execution from a clean installation,
with its own commands, probes and inventories. A generic variant name is an
adapter binding requirement; it is not evidence of an executed command.

Each installation starts from the same designated D-test and the named release,
with recorded positive controls. Before a negative probe, its marker/effect is
absent and its actual consumer exists. The attempt's exit code does not decide
refusal: independent probes and the whole inventory decide. An absent executable,
unsupported syntax or failed setup cannot establish refusal. Positive ordinary
work must actually succeed. All effects use disposable guest state.

At each checkpoint, externally read the committed declaration and independently
inventory stored and effective objects. P1 checks for unrecorded installed things
or settings, P2 for missing/different requirements, UND for the complete strict
derivation. Missing observations stay explicit. Refused saved code can be personal
material only with origin and actual direct-route evidence (R1/R4/R5). Paths or
hashes copied from the implementation's ownership ledger are not observations.
For processes and ports use actual executable bytes through process roots (R9).
Observe modules, kernel parameters, saved networks and Bluetooth pairs explicitly;
the stand's extra-run omissions must not recur.

After candidate edits, use the last successful committed law. Do not advance it
on a progress message, reconnect or candidate-file write. A reported-success
power cut must record the exact success observation, cut ordering and subsequent
boot identity. Each add/change/remove cut occurs three times. Network loss is
triggered only after captured progress, with old-law evidence before retry.

OW-2 and OW-3 are one sequence on the same installation: T0 → T1, restart,
T1 → T2, restart. `fresh` on OW-3 means the existing sequence installation and
must not silently rebuild T1; an independent T1 setup is useful only as a
supplement. The adapter must preserve and report sequence identity. A changed
test greeting does not count as a system update. REPRO uses independent builds,
not clones; compare the named source/recipe and every named setting, retaining
byte comparisons as diagnostics rather than a byte-reproducibility requirement.

No operating-system event is called breaking by the case party alone. W5-BREAK
runs only in an owned disposable guest and needs independent review; an installer
under root is not breaking. Q4/R10 permits behavior of a recorded personal reader,
but its installation/configuration effects remain subject to the law.

Outcomes: pass (all required observations hold); fail (a requirement is violated
under both readings); undecided (named question, only one reading met); unobserved
(missing capability, failed capture, unavailable hardware or unresolved binding,
with exact command/error). A failing setup blocks dependent checks and emits their
unobserved rows. Each case also gets a summary row. Every fail/unobserved row is
included by `request_entries` in the builder-request evidence. Fixture reports are
labelled FIXTURE ONLY and are never RUN-n.md. Logical rule checks are separate
from machine observations and cannot establish an operating-system property.

## All cases

The steps column names primitive captures/actions; their exact requests, shell
texts, reference comparisons and assertions are printed by `run --case ID --plan`
and frozen in plans.json. Tokens and semantic line kinds are defined in
ASSUMPTIONS.md and FORMATS.md; undocumented native commands are not invented here.

| ID | Version-5 labels | Purpose | Steps |
|---|---|---|---|
'''
lines=[header.rstrip()]
for c in CASES:
    steps=' → '.join(s['request']['op']+':'+s['name'] for s in c['steps']) or 'fixture verdict matrix (logic only)'
    lines.append('| '+' | '.join([c['id'],', '.join(c['statements']),c['purpose'],steps])+' |')
lines+=['','## Required variant executions','']
for c in CASES:
    if c.get('variants'):lines.append('- **'+c['id']+'**: '+'; '.join(c['variants'])+'.')
lines+=['','## Previously untested and partial statements','',
'| TABLE.md gap | Case | Limit retained |','|---|---|---|',
'| N | N-VERDICT | Logical reporting test only, not an empirical definition test. |',
'| W1d | W1d-MULTI | Requires actual multi-file designated description, not merely input payload files. |',
'| W3d | W3d-OPEN, W3d-LATEST, REPRO-2b | Unsupported omission/selector remains unobserved. |',
'| W4a, Q1 | OPEN-IN, OPEN-OUT, OPEN-VISIBLE, OPEN-BOUNDARY | One kind of real folder-opening line; no fixture substitutes for native execution. |',
'| W4c | W4c-DEFAULT | Default result retained even if a later prohibition succeeds; logical aggregation also fixture-tested. |',
'| W5b | W5-BREAK | Successful raw event and independent classification required; lack of full root is unobserved. |',
'| Q9 | Q9-SOURCE | Actual account lookups from named server, not a mock list disconnected from login/account mechanisms. |',
'| Q2 updaters | G-UPDATER | Small recorded downloader/installer, user and root variants; does not claim every updater tested. |',
'| Q4 recorded reader | G-READER | Same saved input through ordinary interpreter vs personally recorded file reader; persistent effects checked. |',
'| Q6 guest system | Q6-GUEST | In-system VM program required; outer VM not a substitute. |',
'| Q7 harmless values | Q7-VALUES | Plain theme/user-agent data contrasted with executable/access configuration. |',
'| Q8 port attribution | Q8-PORT | Listening port and process attributed by executable bytes, no extra line. |','',
'## Freeze and runs','',
'''READY.md lists the publication set and the native-binding addendum required before
run 1. Part 1 does not start a VM, install an OS, or issue a system verdict. The set is
published before the first complete run; these tools do not publish. Every complete run later names one
release, source hash and declaration/binding hash and attempts every variant,
including hardware cases as unobserved when hardware is unavailable. No clean
VM result substitutes for the required real-hardware result. At most eight
complete runs; search results are added before the next complete run.''','']
(ROOT/'CASES.md').write_text('\n'.join(lines))
(ROOT/'plans.json').write_text(json.dumps(CASES,indent=2)+'\n')
print('CASES.md and plans.json generated')
