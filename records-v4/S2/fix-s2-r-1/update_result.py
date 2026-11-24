"""Build the revised report from the saved pre-fix report and revised data."""
import csv
from pathlib import Path

OUT = Path('S2/fix-s2-r-1')
text = (OUT/'RESULT.before.md').read_text()


def replace(old, new):
    global text
    assert text.count(old) == 1, (old[:90], text.count(old))
    text = text.replace(old, new)


replace('sample outcome ?, 0 of 600 agreements do not follow', 'sample outcome 0, 2 of 600 agreements do not follow')
replace('Supplement 1, step 2; result prepared 2026-11-23 14:42:19 UTC. Review: RV-S2-R (separate party; pending).',
        'Supplement 1, step 2; revised 2026-11-23 14:54:34 UTC under FX-S2-R-1 after RV-S2-R (DISAGREE). Fix record: `S2/FIX-S2-R-1.md`. Separate substantive acceptance of this revision remains pending.')
replace('The first-line sample count is **0 confirmed failures to follow**, with **16 agreements still factually undetermined**; it does not say that all 600 follow. The sample has 584 established agreements. The fifteen family outcomes are taken from `S2/adjudication/FAMILIES.md` and recomputed from all 105 rows of `S2/adjudication/rows.tsv`: 18 object rows with outcome 0, 83 with ?, and 4 with 1. Those give six families with 0, nine with ?, and none with 1. These are inventory rows, including overlapping directory/member rows, not a count of independent physical failures.',
        'The first-line sample count is **2 confirmed failures to follow**, with **16 agreements still factually undetermined** and **582 established agreements**. The two failures are the CUPS hard-link group and its separately sampled snmp member; they are two agreements in the fixed sample, not two independent physical failures. The fifteen family outcomes are recomputed from all 105 rows of `S2/fix-s2-r-1/rows.tsv`: 17 object rows with outcome 0, 84 with ?, and 4 with 1. Those give six families with 0, nine with ?, and none with 1. The boot group is now ?; its two separate archive rows remain 0. These are inventory rows, including overlapping directory/member rows, not a count of independent physical failures. The original adjudication and sample files remain frozen; `S2/fix-s2-r-1/RESULT.before.md` preserves the prior report. Revised sample decisions are in `S2/fix-s2-r-1/sample-adjudication.tsv`; accounting is in `S2/fix-s2-r-1/raw/counts.json`.')
replace('The decisions and declaration differences are the existing family adjudication, not a second adjudication of those objects.',
        'The decisions and declaration differences retain the existing family adjudication except the explicitly documented corrections in `S2/FIX-S2-R-1.md`: the boot-group outcome and the deciding-fact explanations, including removal of the container\'s rejected installer alternative. The original c1/c2 decisions are preserved.')
replace('6 rows. Initramfs files and boot-directory groups; the three 0 rows concern two Void archives and their containing group.<br>0 (3): `void-0d4bff48fce03ced27aa83a4`, `void-386e90812bdecbec21d0785c`, `void-a6e5bb36a961f99d2e09e83e`<br>? (3): `alma-2c25c1a886c5db421b08087b`, `alma-c4a7c6d6eb439eb9d680a65e`, `microos-62ccb03ff56e2af8ff91ff68`',
        '6 rows. Initramfs files and boot-directory groups.<br>0 (2): `void-0d4bff48fce03ced27aa83a4`, `void-a6e5bb36a961f99d2e09e83e`<br>? (4): `alma-2c25c1a886c5db421b08087b`, `alma-c4a7c6d6eb439eb9d680a65e`, `microos-62ccb03ff56e2af8ff91ff68`, `void-386e90812bdecbec21d0785c`')
replace('Other members of the boot group remain undetermined. The saved adjudication establishes the archive producer and treats the remaining unknown sources as affecting the covering line, not the gap.',
        'Other boot-group members have deciding facts unknown, so that group is ? and is not counted as another complete-facts counterexample. For the two separate archive rows, the saved adjudication establishes the producer and treats unknown sources as affecting the covering line, not the gap.')
replace('For the container, c1 gives INSTALLED-OWN or SETTING-OWN and c2 PROGRAM-OWN or SETTING-OWN. Nothing differs in the declaration: all require its own line. This shared gap is carried forward under TASK-S2-J.md. The four images were resolved as PROGRAM-OWN; the engine groups remain unknown.',
        'The revised container gap is PROGRAM-OWN (executable workload) versus SETTING-OWN (saved service values); both require its own line. c1 originally proposed INSTALLED-OWN or SETTING-OWN; its installer alternative is set aside consistently with the four image resolutions. All four container UNKNOWN facts are non-deciding for the remaining pair: own-process execution is known, saved service values are chosen, and neither reading depends on package receipt or designation of an actual declaration. Evidence and sentence-by-sentence explanation: `S2/fix-s2-r-1/FACT-AUDIT.md`, family 8. The four images remain PROGRAM-OWN; the engine groups remain unknown.')
text = text.replace('`S2/sample-adjudication.tsv`', '`S2/fix-s2-r-1/sample-adjudication.tsv`')
replace('| A3 | 300 | 291 | 2 | 0 | 7 | ? |', '| A3 | 300 | 291 | 0 | 2 | 7 | 0 |')
replace('| Total | 600 | 582 | 2 | 0 | 16 | ? |', '| Total | 600 | 582 | 0 | 2 | 16 | 0 |')
replace('**Agreements that do not follow, grouped by cause:** none is established after adjudication. The eight challenges form the following three groups; their rejection or factual uncertainty must not be reported as a confirmed gap.',
        '**Agreements that do not follow, grouped by cause:** one family, additional hard-link names created at installation for unchanged packaged files, contains the two confirmed gaps. The other six challenges retain factual uncertainty and are not counted as gaps.')
old = next(line for line in text.splitlines() if line.startswith('| Additional hard-link names for unchanged packaged files |'))
replace(old, '| Additional hard-link names created at installation for unchanged packaged files | `gaming-0b9c75abae9461b0be7b041d`, `gaming-7b8b804e906bab4f5a36ccf2` | INSTALLED-PACKAGE; both revised to GAP; outcome 0 | Inode equality and unchanged package contents are established (`S2/a2/raw/evidence.txt:1–18`); creation of the additional names by postinst is also established (`S2/b2/raw/cups-daemon-postinst-backends.txt`). Reading the object as the received file gives INSTALLED-PACKAGE and the package line; reading it as the locally created name gives PROGRAM-DERIVED and the installation/link-creation line under S8.2-9/-16. S8.2-7 does not choose between these referents. The earlier resolution chose the file-identity reading without a deciding sentence; that choice is withdrawn. See question 13. |')
replace('For CUPS, the resolution concerns unchanged file identity and does not decide the meaning of a copied file with a new identity (family 10).',
        'The CUPS question and the copied-file question of family 10 both remain reading questions. A hard link and a byte-equal copy are different facts; neither licenses an added textual rule choosing file identity or pathname as the object.')

start = text.index('**Both parties’ answers for every confirmed gap.**')
end = text.index('**Comparison with the expectation recorded before this step.**')
signs = list(csv.DictReader((OUT/'signs.tsv').open(), delimiter='\t'))
b1 = {r['id']:r for r in csv.DictReader(open('S2/b1/answers.tsv'), delimiter='\t')}
b2 = {r['id']:r for r in csv.DictReader(open('S2/b2/answers.tsv'), delimiter='\t')}
sample = list(csv.DictReader((OUT/'sample-adjudication.tsv').open(), delimiter='\t'))
section = '''**Deciding-fact evidence for the shared gaps.** `S2/fix-s2-r-1/unknown-facts-audit.tsv` names all 23 explicit UNKNOWN facts in the 11 shared-gap rows of families 7, 8, 10 (the hook) and 12, with original fact lines, sentence IDs and a reason for each being non-deciding. `S2/fix-s2-r-1/FACT-AUDIT.md` explains the known premises, group scope and additional qualifications about execution rights and historical traces. These facts remain UNKNOWN; no observation was invented. For the container, the unsupported INSTALLED-OWN alternative is withdrawn and the remaining PROGRAM-OWN / SETTING-OWN pair is explained explicitly.

**Both parties’ answers for every confirmed gap.** The following 17 rows cover all outcome-0 inventory rows in the fixed families. The four answer cells are copied verbatim from `S2/c1/decisions.tsv` and `S2/c2/decisions.tsv`. The first question asks whether inclusion is required by meaning; the second asks whether the requirement can be met without forbidding an ordinary action listed in Section 9.2. No answer is supplied by this result.

`PROTOCOL.md` Section 2 does not say whether “the same answer” compares required inclusion alone or also the stated recording line. Both readings are reported, with neither adopted: **14 both / 3 not both by yes/no alone; 11 both / 6 not both including the full line qualification**. Before excluding the boot group these were 15/3 and 11/7, as the review observed. The two archive rows and the K3s-link row differ between the readings. No gap is assigned to either weighting list. Question 12 leaves this choice to the author.

| Family / gap object | c1 by_meaning | c2 by_meaning | c1 without_forbidding | c2 without_forbidding | Signs: yes/no reading; full-answer reading |
|---|---|---|---|---|---|
'''
for s in signs:
    if s['scope'] != 'family':
        continue
    section += f"| {s['family']} / `{s['object']}` | {s['c1_by_meaning']} | {s['c2_by_meaning']} | {s['c1_without_forbidding']} | {s['c2_without_forbidding']} | {s['yes_no_reading']}; {s['full_answer_reading']} |\n"
section += '''
The now-unknown boot group is excluded from both gap totals. Its original answers are retained in `S2/fix-s2-r-1/signs.tsv`: c1 `yes: own line`, c2 `yes: covered by the kernel package lines and the bootloader line`; both second answers `yes`. The old group verdict does not supply a new complete-facts witness.

**Confirmed sample gaps: both parties’ answers.** Both CUPS agreements now belong in the gap answers. Under the yes/no reading, both signs hold for both rows. Comparing the full recording requirement also gives agreement on coverage by the cups package line; the word order differs, but the named line does not. This reports the parties' answers, not an adjudicated recording line or a weighting list.

| Sample gap ID | b1 by_meaning | b2 by_meaning | b1 without_forbidding | b2 without_forbidding | Signs: yes/no reading; full requirement including line |
|---|---|---|---|---|---|
'''
for s in sample:
    if s['verdict'] != 'GAP':
        continue
    oid=s['id']; a,b=b1[oid],b2[oid]
    section += f"| `{oid}` / GAP | {a['by_meaning']} | {b['by_meaning']} | {a['without_forbidding']} | {b['without_forbidding']} | both signs; both signs (same cups package line) |\n"
section += '''
**Other sample answers, retained for all six factually undetermined challenges.** They are copied verbatim. Under the yes/no reading every pair would have both signs if a gap were established. The Steam pairs also match as full answers; the K3s line qualifications differ. These conditional comparisons do not turn unknown facts into gaps and are excluded from the confirmed-gap counts.

| Sample ID / adjudication | b1 by_meaning | b2 by_meaning | b1 without_forbidding | b2 without_forbidding | Conditional signs: yes/no; full answer |
|---|---|---|---|---|---|
'''
for s in sample:
    if s['verdict'] == 'GAP':
        continue
    oid=s['id']; a,b=b1[oid],b2[oid]
    full='both signs' if a['by_meaning']==b['by_meaning'] else 'not both'
    section += f"| `{oid}` / FACT-UNKNOWN | {a['by_meaning']} | {b['by_meaning']} | {a['without_forbidding']} | {b['without_forbidding']} | both signs; {full}; no confirmed gap |\n"
text = text[:start]+section+'\n'+text[end:]
replace('0; three archive-related rows with two decisions.', '0; two separate archive rows with two decisions; their containing group is ?.')
replace('0 confirmed, 16 still undetermined, 584 established. Even if all 16 unresolved agreements eventually failed, the count would be 16, within the unchanged expectation of at most 20. This arithmetic does not make the sample outcome 1.',
        '2 confirmed, 16 still undetermined, 582 established. Even if all 16 unresolved agreements eventually failed, the count would be 18, within the unchanged expectation of at most 20. The two confirmed gaps already give sample outcome 0; this expectation is not a pass threshold.')
replace('6. **A stored container (family 8).** Does the inventoried container stand for the installed or executable contents, or for the person-chosen values that specify what will run? Both parties found two decisions, while all their alternatives require the same own line. `developer-59a4ddfe60a8a1b18f6627c9` in `S2/adjudication/rows.tsv`; S8.2-7, S8.2-9, S8.2-11 and S8.2-13.',
        '6. **A stored container (family 8).** Does the inventoried stored container denote the executable workload (PROGRAM-OWN), or the person-chosen persistent service values that specify what will run (SETTING-OWN)? Both require its own line. The installer reading is set aside; the facts establish both remaining referents, while S8.2-6 orders questions without choosing the referent. `developer-59a4ddfe60a8a1b18f6627c9` in `S2/fix-s2-r-1/rows.tsv` and `FACT-AUDIT.md`; S8.2-9, S8.2-11, S8.2-13 and S8.2-22.')
replace('Until an answer, the side-by-side answers above establish only whether the two signs agree; no gap is assigned to either list.',
        'Does “the same answer” mean the same yes/no on required inclusion, or agreement also on the stated recording line? The alternatives give 14/3 and 11/6 for the 17 family gap rows; the two sample gaps agree on inclusion and cups package coverage. Until an answer, both comparisons are conditional; neither is adopted and no gap is assigned to either list.')
marker='\n**Exact sentences cited.**'
replace(marker, '\n13. **An additional hard-link name created during installation (sample).** In S8.2-7, is the object the unchanged received file, or its additional name created on the computer? The first reading gives INSTALLED-PACKAGE and package coverage; the second gives PROGRAM-DERIVED and coverage by the installation/link-creation line. Same-inode facts and creation by postinst establish both premises but do not choose the reading. The two CUPS rows of `S2/fix-s2-r-1/sample-adjudication.tsv` remain GAP. This is a question about the existing text, not a proposed rule.\n'+marker)
replace('**Mechanical verification.** The required quote check and structural/count checks are recorded in `S2/raw/result-validation.txt`. Independent substantive acceptance remains with review RV-S2-R.',
        '**Mechanical verification.** The required quote check, recomputed sample/family accounting, all 23 UNKNOWN audit entries, verbatim answer tables and preservation of frozen input hashes are checked in `S2/fix-s2-r-1/raw/validation.txt`. Only the revised adjudication/report calculations were run; no probe, machine or new case was added. Independent substantive acceptance of this fix remains with a separate review.')
Path('S2/RESULT.md').write_text(text)
print('Updated S2/RESULT.md from the preserved pre-fix report.')
