from pathlib import Path
from collections import Counter
import json, re

base = Path('B1')
out = base / 'fix-b1-1'
original = (out / 'before/B1/CHANNELS.md').read_text()
lines = original.splitlines()
rows = [[c.strip() for c in re.split(r'(?<!\\)\|', line)[1:-1]] for line in lines if re.match(r'^\| [CM]\d', line)]
index = {row[0].split()[0]: row for row in rows}
changes = []

def edit(key, verdict=None, mechanism=None, evidence=None, cost=None, requirement=None):
    row = index[key]
    before = row.copy()
    for pos, value in [(1, requirement), (2, verdict), (3, mechanism), (4, evidence), (5, cost)]:
        if value is not None:
            row[pos] = value
    if row != before:
        changes.append({'id': key, 'before': before, 'after': row.copy()})

fixref = '[Fix evidence and limits](fix-b1-1/control-audit.md)'
dref = '[T E12](raw/c7-sources.md); [D limits](fix-b1-1/control-audit.md)'

# Apply the same evidence threshold to the named broker rows and dependent routes.
broker = 'C1.1 C1.2 C1.4 C1.5 C2.1 C2.2 C2.5 C3.1 C3.2 C3.3 C3.5 C4.3 C5.2 C5.5 C6.1 C6.2 C6.3 C6.4 C6.5 C9.1 C9.2 C9.3 C9.4 C9.5 C9.6 C10.1 C10.2'.split()
for key in broker:
    row = index[key]
    edit(key, verdict='UNKNOWN', mechanism='Candidate only: ' + row[3] + '; no evidenced complete declaration-only integration',
         evidence=row[4] + '; ' + fixref,
         cost='Proposed workflow: ' + row[5] + '; retained operation not established')

for key in 'C7.03 C7.04 C7.05 C7.06 C7.17 C8.03 C8.06'.split():
    edit(key, verdict='UNKNOWN', mechanism='F/I cooperation for this own-rights input route has no evidenced adopter; D does not mediate arguments, inherited input or environment', evidence=index[key][4] + '; ' + fixref)
edit('C7.03', cost='Equivalent declared-file workflow is a proposal; P01 demonstrates stock argument-code execution under locked bits')
edit('C7.05', mechanism='D covers a new file open only; inherited stdin/FD route lacks evidenced F integration', cost='Path-open case loses unrecorded file reads; retained redirected-input support is unestablished')
edit('C7.17', mechanism='Denying all interactive input removes the interactive shell; record-before-interpret has no cited implementation', cost='Removal option loses all interactive shell use; retained mediated shell is UNKNOWN')
edit('C7.01', mechanism='D denies opening unrecorded script files; declared immutable file remains readable; F is not established', evidence=dref, cost='File execution retained only in restricted read domain; no unrecorded user-document/project-data reads')
edit('C7.02', mechanism='Kernel execute policy plus D for interpreter file reads; no F adopter assumed', evidence='[T E3,E12](raw/c7-sources.md); ' + fixref)
edit('C7.07', mechanism='D denies opening the unrecorded sourced file; an F-only alternative does not cover arbitrary data-to-code dispatch', evidence=dref, cost='No unrecorded document/project-data file reads in this domain; inherited inputs separately unresolved')
edit('C7.08', verdict='CLOSABLE', mechanism='D denies the unrecorded file open, independent of eval/import/custom-dispatch semantics; only this bounded file route is closed', evidence='[T E6–8,E12](raw/c7-sources.md); ' + fixref, cost='Arbitrary admitted scripts lose unrecorded data-file reads; keeping both capabilities permits the Q1 conditional failure')
edit('C2.6', mechanism='N gates native mappings; D gates module/.pth file reads including custom dispatch; no F/I completeness assumed', evidence=index['C2.6'][4] + '; ' + dref, cost='Immutable admitted code only; D removes unrecorded document/project-data reads; caches remain C7.18')
edit('C4.4', mechanism='N gates native library mapping; D denies downloaded script/data file opens, including custom dispatch; noexec alone insufficient', evidence=index['C4.4'][4] + '; ' + dref, cost='Declared files remain usable; interpreter loses unrecorded document/project-data reads')
edit('C4.5', verdict='UNKNOWN', mechanism='Depends on the same unevidenced stream refusal/admission integration as C7.04; noexec or D file-open policy alone does not mediate inherited stdin', evidence=index['C4.5'][4] + '; ' + fixref)
edit('C7.11', verdict='UNKNOWN', mechanism='N closes native child launch, but shell-command child code depends on unevidenced F/I input mediation', evidence=index['C7.11'][4] + '; ' + fixref)
edit('C7.12', mechanism='N authorizes native hooks; D denies opening undeclared script hooks; hook execution via other input routes inherits their UNKNOWNs', evidence='[T E3,E12,E13](raw/c7-sources.md); ' + fixref)
edit('C7.23', mechanism='Control handler registrations; N gates native binaries and D gates foreign-binary file reads; this is not full evaluator input mediation', evidence=index['C7.23'][4] + '; ' + dref)
edit('C8.01', mechanism='Declared immutable startup files and D deny unrecorded startup file opens; F cooperation not established', evidence='[T E9,E10,E12](raw/c7-sources.md); ' + fixref)
edit('C8.02', mechanism='D denies opening environment-selected unrecorded startup files; environment code itself remains C8.03 UNKNOWN', evidence='[T E10,E12](raw/c7-sources.md); ' + fixref)
edit('C8.05', verdict='UNKNOWN', mechanism='D gates configuration file opens and N gates native children; shell snippets/helper arguments still require unevidenced F/I mediation', evidence=index['C8.05'][4] + '; ' + fixref)
edit('C8.07', verdict='UNKNOWN', requirement='R; S2.2-10; S2.2-13 decides code/settings classification', mechanism='Privileged API implementation is own-rights code and must be recorded; complete admission/update/load control not evidenced', evidence='[O10](raw/ordinary-sources.md); [extension evidence](fix-b1-1/evidence-addendum.md)', cost='Recorded extension workflow needs integration; ordinary browsing need not include this extension')
edit('C7.20', requirement='R; S2.2-10; S2.2-13 decides code/settings classification')
edit('M5.02', mechanism='No complete validator established for unrestricted semantic requirements; admissibility and Understanding readings are left open in Q2', evidence='[Q2 below](#q2--an-algorithm-reads-every-script-in-directory-d-from-computer-state); [text audit](fix-b1-1/text-audit.md)', cost='Finite validators are bounded evidence; no admissibility rule is added to the published text')

newrows = [
 ['C7.24 Recorded custom dispatcher interprets unrecorded command file without eval/import', 'R; S2.2-10; S2.2-13; Q1 capability premise', 'CLOSABLE', 'D denies the file open; F/I evaluator-entry checks alone miss dispatch implemented by admitted script', dref + '; [Q1 textual audit](fix-b1-1/text-audit.md)', 'Lose unrecorded document/project-data reads; retaining both arbitrary admitted same-rights interpretation and those reads admits the Q1 conditional failure'],
 ['C7.25 Runtime-selected TCP listening port (also C2/C3/C5/C9.2)', 'R; S2.2-15; S2.3-4,6', 'UNKNOWN', 'Landlock BIND_TCP closes explicit unauthorized bind only; complete listener policy including implicit bind and inherited sockets is not evidenced', '[Network evidence](fix-b1-1/evidence-addendum.md)', 'Declared port/service/rule and matching lifecycle required; arbitrary runtime listeners unavailable; exact retained networking integration unresolved'],
 ['C10.4 Root editor with documented package installer', 'R; S2.2-10; S3-6 versus S3-7; S3-8', 'TEXT-OPEN', 'Documented installer purpose and explicit editor exclusion decide built-in/breaking both ways; card T4', '[Original C10.4 analysis](MECHANICS-research.md); [O6](raw/ordinary-sources.md); [text audit](fix-b1-1/text-audit.md)', 'Installer reading requires declaration mediation; editor-exclusion reading treats privileged bypass as breaking'],
]
for row in newrows:
    prefix = row[0].split()[0].split('.')[0]
    pos = max(i for i, r in enumerate(rows) if r[0].split()[0].split('.')[0] == prefix) + 1
    rows.insert(pos, row)
    index[row[0].split()[0]] = row
    changes.append({'id': row[0].split()[0], 'before': None, 'after': row.copy()})

counts = Counter(row[2] for row in rows)
header = f"CHANNELS: {counts['CLOSABLE']} closable, {counts['CLOSABLE-ONLY-BY-REMOVAL']} closable only by removal, {counts['NOT-CLOSABLE']} not closable, {counts['TEXT-OPEN']} text-open, {counts['UNKNOWN']} unknown"
start = next(i for i,l in enumerate(lines) if l.startswith('| Variant'))
end = max(i for i,l in enumerate(lines) if re.match(r'^\| [CM]\d',l))
table = ['| ' + ' | '.join(row) + ' |' for row in rows]
s = '\n'.join([header] + lines[1:start+2] + table + lines[end+1:])+'\n'

s = s.replace('**R** in each channel row means S2.1-3; S2.2-9;', '**R** in each channel row means S2.1-3; S2.2-9; S2.2-15;')
s = s.replace('Thus every row includes P2 and Removal, not just admission.', 'Thus every row includes P2, Removal and changes to required accounts/rights/rules/ports, not just code admission. C7.25 explicitly analyses the runtime-port route across C2/C3/C5/C7/C9.2; a native launch control does not itself close that route.')
a=s.index('**F** is immutable')
b=s.index('\n\n## Written arguments',a)
s=s[:a]+'''**F** means a proposed cooperating evaluator checking the immutable descriptor it consumes. **I** means its proposed refusal of unrecorded argument, stream, environment and interactive code. Neither F nor I has an evidenced adopter for the own-rights interpreter class here. **D** means the bounded read-open control documented by Landlock: handle READ_FILE, permit only the immutable admitted closure, enforce before opening input, and retain enforcement in descendants. D does not filter argv/environment or revoke already-open FDs, terminal/stdin or IPC. A clean input boundary is a precondition, not an evidenced complete launcher; broader routes stay UNKNOWN. All D rows lose unrecorded document/project-data reads. A mediated reader is not sufficient if it returns arbitrary bytes that a script may interpret; retained data access needs a separately evidenced constraint. **N** is mandatory execution/mapping policy plus restrictions on native memory execution, memfd and injection. Its documented bounded controls do not establish the declaration broker. See [control audit](fix-b1-1/control-audit.md).

Revision FX-B1-1 supersedes contrary conclusions in the retained research notes and raw narrative plans. Those are frozen historical records, not current verdicts. [Disposition of all review findings](FIX-B1-1.md); [corrected probe disposition](fix-b1-1/PROBE-DISPOSITION.md).''' + s[b:]
s=s.replace('3. Mandatory execution/read restrictions and a cooperating evaluator can block a particular unrecorded input while retaining a declared input. The Linux 6.14 `samples/check-exec/inc.c` is a concrete limited-language example, not a conjecture that setting securebits fixes Python.', '3. Documented native execution controls and D can block bounded native/file-open routes. The Linux 6.14 `samples/check-exec/inc.c` is an API example with two counter commands, not evidence of a retained S2.2-10 full-rights interpreter. F/I integration is UNKNOWN, so no positive C7 example with complete input mediation has been established.')
s=s.replace('Q3 retains concrete classes of tools for the six actions, and the design retains controlled code execution in every listed channel.', 'Q3 identifies candidate tool classes for the six actions; retaining controlled code execution in every listed channel remains an unfulfilled design obligation.')
s=s.replace('One remaining downstream-build question qualified for P01:', 'The original work treated a downstream-build question as eligible for P01 without consulting the distribution source package and patches:')
s=s.replace('C7.03 stays CLOSABLE through a cooperating implementation, not this stock binary alone.', 'C7.03 is now UNKNOWN: no relevant cooperating implementation was evidenced. The source-first procedure was incomplete; this cannot be repaired retrospectively or by rerunning the probe.')
s=s.replace('`raw/PROBE-DISPOSITION.md` records why no other question warranted a primitive probe.', '`fix-b1-1/PROBE-DISPOSITION.md` supersedes the original narrative eligibility claims and corrects the refinement timestamp; original raw evidence remains unchanged.')
a=s.index('### T2 — Browser extension')
b=s.index('### T3 — Partial confinement',a)
s=s[:a]+s[b:]
a=s.index('A reviewed proposed fourth card')
b=s.index('These cards report classification questions',a)
s=s[:a]+'''### T4 — Root editor with documented package installation (C10.4)

**What the text lacks:** a priority rule when the same documented program is both an editor and a package installer. S3-6 says exactly: “**Built-in tool.** A program of the system whose purpose, according to its documentation, includes changing what must be recorded: a package manager, including package managers of programming languages and of application packages; account and rights management; the service manager; network and firewall configuration.” S3-7 says exactly: “General-purpose programs—an editor, file copying, link creation, the command shell—are not built-in tools: changing with them, through superuser privileges, what must be recorded is breaking.”

The documented `package-install` installs code executed by the editor with its own rights (S2.2-10; O6; original MECHANICS C10.4). **Reading A:** documented installation purpose makes this program built-in; its privileged bypass violates P4. **Reading B:** the explicit editor exclusion applies; the privileged bypass is breaking. Neither operation-based reclassification nor an editor-priority rule is stated. Restricting both paths technically does not settle this classification.

**Strongest objection:** classify the operation rather than the program. **Answer:** S3-6 and S3-7 classify programs and supply no mode-switch rule. S3-8 explicitly says: “If a program’s documentation does not state its purpose, the case yields ?; if it does and this indicator still does not decide whether the program is a built-in tool, the case is a counterexample to the definitions and yields 0.” This is a hole, with the two readings left unresolved; it is not a universal engineering impossibility.

The former T2 extension card is withdrawn: S2.2-13 classifies the specified privileged implementation as code, and S2.2-10 requires recording it. Its integration is UNKNOWN, not TEXT-OPEN. Q2 below records an additional author question about requirements, separately from the channel/mechanic variant count.

''' + s[b:]
s=s.replace('If separate review determines the text truly cannot decide a covered object, Section 4.1 assigns 0 to that definitional case. This research does not convert an unresolved card or an engineering UNKNOWN into an accepted 0.', 'Under Section 4.1 a demonstrated definitional hole yields 0; UNKNOWN engineering evidence yields ?. These are separate from the whole-system existence question, which remains ?. The review confirms the C7.18/C7.21 holes and identifies C10.4; this correction restores that hole. Q2 does not choose an author reading or assert an unconditional contradiction.')
a=s.index('Possible controls have different costs:')
b=s.index('\n## Q2',a)
s=s[:a]+'''The concrete custom-dispatch route is C7.24. Let recorded script M implement an interpreter for a command file F using ordinary reads, branches, writes and launches of recorded programs, without calling eval/import/source or an execution-check API. Explicit premise: this language exposes the executing program's own rights, so S2.2-10 applies; a small values-only command file is not automatically such code. If unrecorded F can supply these instructions and M can read it after application, S2.2-13 makes F code, S2.1-3 makes it in force, and S2.3-4 fails. An ordinary user's change of F also violates S2.3-6. No superuser breaking is involved. F/I checks at conventional evaluator entry points cannot see M's dispatch.

**Strongest objection:** recording M records its semantics, or a restricted command language may just consume values. **Answer:** the first does not record separate own-rights code F; the second denies the explicit premise and is not a counterexample to this conditional argument. It is not a claim that every data-dependent program executes code, nor an undecidability proof for every possible admission policy.

For C7.07/08/24, D blocks the unrecorded file open at the cost of denying unrecorded user-document/project-data reads. Keeping arbitrary admitted full-capability interpreters plus unrestricted unrecorded data reads admits this conditional failure; evaluator-entry checks alone cannot close it. Refusing active document content or genuinely confining code under S2.2-11 are different bounded options. A cooperative evaluator checking conventional file/eval entries is removed from the list of sufficient controls. A data reader returning arbitrary bytes to M would recreate the premise; no such broker is claimed to solve it. No system-wide NOT-CLOSABLE result follows because systems need not retain both capabilities.
''' + s[b:]
a=s.index('## Q2 —')
b=s.index('\n## Q3',a)
s=s[:a]+'''## Q2 — An algorithm reads “every script in directory D” from computer state

**Author question / unresolved requirement reading (textual hole).** S2.4-1 says exactly: “**Understanding.** If there was no breaking, what is in force on the computer can be read from the declaration alone, without inspecting the computer.” S2.5-3 says exactly: “Nor is the form of the declaration part of the definition: it may be a list or an algorithm that computes what is recorded.” The heading for S2.4 is “Consequences”. Neither admissibility filtering nor a symbolic-only meaning of “read” is added here.

The conditional two-computer construction is:

1. The designated declaration files are identical and compute “every script in directory D”. D is external machine state, not one of those files; the two machines contain different script sets in D. No breaking is assumed.
2. On each separate application, let P1 and P2 hold for the computed set. Let changes to D that affect that set be possible only through declaration application, so P4 does not supply an independent bypass. This is a logical premise, not a built system or an observed test case.
3. If Understanding requires identifying the concrete in-force objects, identical declaration files cannot distinguish the two sets without inspecting D. On that reading Understanding does not follow from these P1/P2/P4 premises alone.

There are **two separate choices** that the text does not settle for this construction:

- **Consequence versus admissibility.** If Understanding is claimed to follow from P1/P2/P4 for any allowed algorithmic form, the construction challenges that implication; if the premises are admitted and the concrete-object reading applies, it is a contradictory-requirement candidate under Section 4.1. If Understanding is instead an additional filter on admissible declaration/input arrangements, this arrangement may be rejected. The latter reading was previously selected in this report; that selection is withdrawn.
- **Concrete versus symbolic reading.** If “read” requires concrete object identities, external D prevents declaration-alone knowledge. If knowing the rule “all scripts in D” suffices, the construction may satisfy Understanding symbolically. Neither reading is selected here.

**Strongest objection:** S2.5 leaves declaration form to design, so no hole follows from permitting algorithms. **Answer:** agreed as to form alone. The question concerns the relation between the asserted consequence and P1/P2/P4, and the meaning of declaration-alone Understanding for external inputs. If D is designated declaration content, or cannot change the result, this construction no longer applies. No syntax restriction, input-pinning requirement or author decision is inferred. This remains an author question with both choices recorded; it is not a universal NOT-CLOSABLE claim or a new counted channel. M5.02 separately remains UNKNOWN for unrestricted validation.
''' + s[b:]
s=s.replace('No intrinsic loss of browsing established; ambiguous extension/partial-confinement cases remain T2/T3.', 'No intrinsic loss of browsing established; privileged-extension integration is C8.07 UNKNOWN, while partial confinement remains T3.')
s=s.replace('A cooperating restricted interpreter retains this route.', 'A complete cooperating own-rights interpreter is not evidenced. D retains only bounded declared-file execution: scripts lose read access to unrecorded documents and project data. Such data workflows are unavailable unless a separately evidenced mediated reader and language/authority restriction prevents returned values from becoming own-rights code; a byte-forwarding reader alone is insufficient.')
s=s.replace('Ordinary dependency installation is retainable with this workflow;', 'This is a candidate workflow, not an evidenced complete pip/npm integration. Under D, build and runtime scripts cannot read unrecorded project data or user documents; a separately constrained reader is unestablished, so those workflows are unavailable under the evidenced control;')
s=s.replace('All actions inherit M1–M5 rather than being considered complete when a backend returns.', 'All actions inherit M1–M5 rather than being considered complete when a backend returns. The mutation broker is unbuilt: the following lines/tools are requirements and candidate workflows, not evidence of complete closure. Runtime listeners additionally require recorded ports and applicable rules under S2.2-15 (C7.25).')
(base/'CHANNELS.md').write_text(s)
(out/'variant-inventory.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
(out/'row-changes.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False)+'\n')
print(header)
print('rows:',len(rows),'; changed/new:',len(changes))
