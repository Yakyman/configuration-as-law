"""Enumerate the sentence-pair audit from explicit documented witnesses.

This script checks enumeration, not the truth of the interpretation. The witness
effects and pair dispositions below are the written reasoning of the sweep.
"""
import csv
import itertools
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sentences = dict(re.findall(r'^- \*\*(S8\.[12]-\d+)\*\* (.+)$', (ROOT / 'SENTENCES.md').read_text(), re.M))
assert len(sentences) == 39

# A scope description remains explicit when a witness does not meet a sentence's
# antecedent. No non-applicability is treated as an opposite answer.
scopes = {
'S8.1-1':'defines the description, not an exemption for this object',
'S8.1-2':'requires description-to-computer direction, not a kind assignment',
'S8.1-3':'uses designation to identify description files, not every consumed file',
'S8.1-4':'defines the actor installer, not the kind of every output',
'S8.1-5':'applies only to installer functionality inside a general-purpose program',
'S8.1-6':'defines a package by the installer unit; no such unit is asserted here',
'S8.1-7':'defines configuration/installation tools, not all their data as settings',
'S8.1-8':'excludes general-purpose functionality from built-in tools',
'S8.1-9':'tests presence or executable capability after the kind is decided',
'S8.1-10':'tests a setting value; it does not turn arbitrary data into a setting',
'S8.1-11':'tests services/accounts, not this other kind of object',
'S8.1-12':'leaves required state to the recording line',
'S8.1-13':'defines successful conformity, not an alternative recording exemption',
'S8.1-14':'selects the last reported-successful description, not a new kind',
'S8.1-15':'requires all of past-declaration change, superuser power and outside-tool action',
'S8.1-16':'exempts defined breaking; it does not exempt an ordinary operation',
'S8.2-1':'requires installed objects/settings once those predicates are established',
'S8.2-2':'permits omission only of the rest, after classification',
'S8.2-3':'limits consideration to objects on the computer',
'S8.2-4':'excludes a typed action, not an independently stored artifact',
'S8.2-5':'absorbs a runtime instance into its creator, not a persistent file',
'S8.2-6':'orders the four kind questions; does not supply missing facts',
'S8.2-7':'tests package membership plus unchanged receipt, not every file ever handled by a tool',
'S8.2-8':'is the consequence of an affirmative Q1, not an independent package test',
'S8.2-9':'tests executable code, not merely arbitrary text consumed by software',
'S8.2-10':'is the consequence of an affirmative Q2, not an exemption',
'S8.2-11':'tests a person-chosen system value after Q1 and Q2',
'S8.2-12':'is the consequence of Q3, not a test based on the filename',
'S8.2-13':'enumerates settings; it does not override an earlier affirmative question',
'S8.2-14':'tests personal values for launch/access effects within Q3',
'S8.2-15':'is a fallback after all earlier questions; provenance alone cannot override them',
'S8.2-16':'supplies covering lines for installed objects, not all settings',
'S8.2-17':'supplies own/default-package lines for settings, not a new kind',
'S8.2-18':'allows source coverage when a line takes an external list',
'S8.2-19':'allows optional recording; it never forbids required recording',
'S8.2-20':'excludes unexecutable code from programs, not from installed objects',
'S8.2-21':'permits omission only for code satisfying the inside-program capability restriction',
'S8.2-22':'includes a program with its own process; it does not identify each process instance as a new executable',
'S8.2-23':'distinguishes execution as code from reading values; it does not settle mixed-file granularity',
}
assert scopes.keys() == sentences.keys()

W = []
def witness(key, obj, source, effects):
    W.append(dict(key=key, obj=obj, source=source, effects=effects))

witness('package', 'Unchanged Debian gawk package, including /usr/bin/gawk and /etc/profile.d/gawk.sh', 'PAIR1', {
'S8.1-1':'a declaration can describe installation of this package',
'S8.1-2':'the stated package requirement precedes bringing the computer into conformity',
'S8.1-3':'only person-designated description files form the declaration; package payload is not automatically that description',
'S8.1-6':'the package is the installer unit; its payload is obtained as part of it',
'S8.1-9':'the installed package/payload is in force by presence',
'S8.1-12':'the package line states its required installed state',
'S8.1-13':'application brings the installed package state into conformity with that line',
'S8.1-14':'a later edit alone does not select a new last-successful declaration',
'S8.2-1':'the Q1 installed package and payload require coverage',
'S8.2-2':'this package is not part of the optional rest',
'S8.2-3':'the installed payload is on the computer',
'S8.2-6':'Q1 wins even for executable payload and shell configuration',
'S8.2-7':'Q1 is affirmative for the package and its unchanged payload',
'S8.2-8':'the Q1 result is installed object, including non-code payload',
'S8.2-9':'the executable payload also meets the code predicate, but Q1 is earlier',
'S8.2-10':'the Q2 program conclusion does not displace Q1',
'S8.2-11':'shell configuration values do not displace earlier Q1',
'S8.2-12':'a setting conclusion is later than the unchanged-package answer',
'S8.2-13':'configuration purpose does not bypass Q1',
'S8.2-15':'the installer wrote payload files, but the record fallback loses to Q1',
'S8.2-16':'the package line covers its installed payload',
'S8.2-17':'package-shipped defaults also have package coverage; no contradictory own-line duty',
'S8.2-19':'additional explicit payload recording is permitted',
'S8.2-22':'running gawk has its own process; this does not cancel package coverage',
'S8.2-23':'executed profile code is code even though it sets values; Q1 remains earlier',
})
witness('editor', 'Emacs package-menu installs/removes an extension, contrasted with its ordinary text-editing operation', 'PAIR2; TERM_SOURCES.md EMACS', {
'S8.1-4':'the documented install/remove functionality is an installer',
'S8.1-5':'only the editor functionality that installs is counted as installer',
'S8.1-6':'the extension managed as a whole is a package',
'S8.1-7':'that installer function is a built-in tool',
'S8.1-8':'ordinary editing is excluded, but the installer function is expressly excepted',
'S8.1-15':'an installation through this functionality is inside a built-in tool, so is not breaking on that basis',
'S8.1-16':'a non-breaking installer operation cannot claim the breaking exemption',
'S8.2-4':'typing the package-menu command is an action; the extension is a separate resulting object',
'S8.2-6':'Q1 places the installed extension before asking whether it is code',
'S8.2-7':'the installed extension is an installer-managed package',
'S8.2-8':'the extension is installed even when loaded inside the editor',
'S8.2-9':'extension code is executable through the editor, but Q1 is earlier',
'S8.2-10':'Q2 would identify code; Q1 already decided the package',
'S8.2-16':'the extension package may be covered by its own package line',
'S8.2-22':'an extension need not have a separate process for Q1 to require it',
})
witness('copy', 'GNU install copies a program file and sets its attributes; it is not a package-manager installation', 'PAIR3', {
'S8.1-4':'copying alone does not meet the documented purpose of installing AND removing programs',
'S8.1-5':'the command name install does not establish an embedded installer satisfying S8.1-4',
'S8.1-6':'the copied destination is not an installer unit merely because this command is named install',
'S8.1-7':'attribute-changing functionality must be distinguished from general file copying by S8.1-8',
'S8.1-8':'general file copying is explicitly excluded from built-in tools',
'S8.1-15':'a superuser direct overwrite past the declaration through file copying meets breaking; ordinary owner copying does not',
'S8.1-16':'the breaking exemption is conditional on the preceding privilege/action facts',
'S8.2-4':'the typed copying command is an action, the destination executable is an object',
'S8.2-7':'a file copied outside a package has no Q1 membership merely from the tool name',
'S8.2-9':'the executable destination satisfies Q2',
'S8.2-10':'its source and author do not prevent classification as installed program',
'S8.2-15':'human copying does not outrank executable code Q2',
})
witness('auth', 'An incoming OpenSSH authorized_keys entry added by its ordinary account owner', 'PAIR4', {
'S8.1-1':'incoming authentication can be described as part of computer configuration',
'S8.1-9':'the persistent file is present; presence alone does not decide its effective setting value',
'S8.1-10':'the allowed key must have the required effective value',
'S8.1-11':'the account existence predicate is separate from its permitted login key',
'S8.1-12':'the line can require this specific incoming authentication key',
'S8.1-15':'an owner write without superuser power is not breaking, even when past the declaration',
'S8.1-16':'absence of superuser breaking means the ordinary write gets no exemption',
'S8.2-1':'the incoming login setting must be recorded',
'S8.2-2':'the incoming login setting is not optional rest',
'S8.2-3':'the authorized key entry is on this computer',
'S8.2-4':'typing an editor command does not exempt the saved key entry',
'S8.2-6':'Q1 and Q2 are false for this new non-code entry; Q3 applies before material provenance',
'S8.2-7':'the newly added entry is not unchanged package payload',
'S8.2-9':'the public-key value is not executed as code',
'S8.2-11':'the chosen value controls incoming access to this computer',
'S8.2-12':'its file location does not prevent it being a setting',
'S8.2-13':'means of login to this computer is an explicit setting category',
'S8.2-14':'even if treated as personal-program scope, granting access still makes it a setting',
'S8.2-15':'human creation does not override earlier Q3; the outbound-private-key example is a different object',
'S8.2-17':'a customized nondefault setting needs its own line',
'S8.2-19':'optional-recording permission does not weaken mandatory recording of this setting',
'S8.2-23':'the server reads a key value, not executable code',
})
witness('service', 'A systemd service unit enabled without starting its process, or disabled while its process still runs', 'property_sources.md PS4', {
'S8.1-7':'systemctl is a service-management built-in tool',
'S8.1-9':'the service executable can be in force independently of the service enablement object',
'S8.1-10':'the configured enablement value is distinct from a running process',
'S8.1-11':'service in-force predicate uses enabled, not process currently running',
'S8.1-12':'the line states which service state is required',
'S8.1-13':'application is conformity with the requested state, not merely calling enable',
'S8.1-15':'an enable/disable operation through the service manager is not outside the built-in tools',
'S8.1-16':'this tool operation does not obtain a breaking exemption',
'S8.2-5':'a process instance follows its executable/setting rather than becoming an independent object',
'S8.2-11':'chosen service enablement is a configuration value',
'S8.2-12':'the service state is a setting regardless of storage path',
'S8.2-13':'services and their parameters are expressly included',
'S8.2-14':'the personal-program distinction does not exempt a service parameter',
'S8.2-17':'a chosen nondefault service state requires setting coverage',
'S8.2-22':'the daemon executable remains a program; this is distinct from each runtime process instance',
'S8.2-23':'a parsed unit setting is not code merely because it names a daemon',
})
witness('history', 'A Bash history entry persisted to HISTFILE and later re-executed using fc', 'PAIR5; TERM_SOURCES.md BASH', {
'S8.1-8':'the shell is general-purpose outside installer functionality',
'S8.1-9':'the executable saved command can be started through the shell',
'S8.2-1':'executable history requires installed-code coverage once Q2 applies',
'S8.2-2':'calling the file history does not automatically put it in the optional rest',
'S8.2-3':'saved HISTFILE entries are persistent objects on the computer',
'S8.2-4':'the original typed action is excluded, but the stored replayable entry is a different object',
'S8.2-5':'persistent history is not confined to the lifetime of its creator process',
'S8.2-6':'Q2 precedes the Q4 history example',
'S8.2-7':'a newly written history entry is not unchanged package payload',
'S8.2-9':'fc executes stored command text through Bash',
'S8.2-10':'human authorship and log provenance do not prevent program classification',
'S8.2-14':'if considered a launching value it would still require recording; Q2 is earlier',
'S8.2-15':'program-written history and human authorship are fallback descriptions, defeated here by Q2',
'S8.2-16':'the saved code needs a covering line; being written by a recorded shell alone has the derivation boundary noted in TERMS.tsv',
'S8.2-23':'executing stored commands is code use, unlike a display-only history viewer',
})
witness('bytecode', 'A Python py_compile bytecode cache for a personal project source file, executable by the matching interpreter', 'TERM_SOURCES.md PY; PAIR6', {
'S8.1-9':'matching bytecode can be started through the interpreter',
'S8.2-1':'executable bytecode belongs to what must be recorded',
'S8.2-2':'the cache label does not by itself make the object optional',
'S8.2-3':'the generated bytecode is on the computer',
'S8.2-5':'a disk bytecode cache survives the interpreter run, so is not merely a runtime instance',
'S8.2-6':'Q2 executable code wins before the Q4 cache example',
'S8.2-7':'a cache generated later from a personal source is not unchanged package receipt',
'S8.2-9':'matching bytecode is executed through another program',
'S8.2-10':'being generated rather than shipped does not exempt program code',
'S8.2-15':'program-written cache and project material are later than code Q2',
'S8.2-16':'a declared source can cover its compiled copy; tool-only coverage is the separate derivation term boundary',
'S8.2-20':'the matching interpreter makes this executable; foreign-format appearance is insufficient to exclude it',
'S8.2-23':'compiled code is executed, not merely read as values',
})
witness('foreign', 'A Python .pyc file for an incompatible interpreter format, with no matching interpreter available', 'PAIR6', {
'S8.1-9':'as non-package unexecutable code it does not satisfy the program in-force test',
'S8.2-1':'no installed-code obligation follows once executable capability is absent and package provenance is absent',
'S8.2-2':'a non-setting, non-package unexecutable file can be omitted',
'S8.2-6':'Q2 is false on this specified capability fact, so fallback is reached',
'S8.2-7':'an independently brought incompatible cache is not an installed package by that fact',
'S8.2-9':'the no-compatible-interpreter condition makes Q2 false',
'S8.2-10':'there is no affirmative Q2 on which to invoke the program conclusion',
'S8.2-15':'the person-brought incompatible cache is material after the earlier negative answers',
'S8.2-20':'it expressly is not a program if it cannot execute on this computer',
'S8.2-23':'code representation alone is insufficient without the executable capability condition',
})
witness('launcher', 'A user-created desktop entry containing an Exec value and a display Name', 'PAIR7', {
'S8.1-10':'the launching value can be required as a setting',
'S8.2-1':'the launch setting requires recording',
'S8.2-3':'the desktop file is a persistent on-computer object',
'S8.2-4':'a stored Exec command is not a currently typed action',
'S8.2-6':'the launching value reaches Q3 if treated as data; executable command bytes can reach Q2 first',
'S8.2-7':'a user-created entry is not unchanged package receipt',
'S8.2-9':'whether the containing file is itself code is the granularity boundary, not proof that all values are code',
'S8.2-11':'personal scope alone does not decide the launch extension to Q3',
'S8.2-12':'a launch setting can reside in a per-user file',
'S8.2-13':'service/system-wide status is not needed for the separate launch/access extension',
'S8.2-14':'Exec names a program to launch, so the personal-value exception still requires recording',
'S8.2-15':'the person-created provenance loses to Q2 or Q3 for the launching part',
'S8.2-16':'if classified as executable command code it uses installed-object covering lines',
'S8.2-17':'if classified as a launch setting it uses setting coverage',
'S8.2-23':'the parser reads fields; launching one field does not expressly settle classification of the containing mixed file',
})
witness('sandbox', 'GNU join.awk string-concatenation function saved separately from the manual and used inside recorded gawk', 'PAIR8; PAIR9', {
'S8.1-9':'the function can execute inside the available interpreter',
'S8.2-1':'Q2 makes this executable code installed and requires coverage',
'S8.2-2':'the rest exemption alone does not include code already placed by Q2',
'S8.2-3':'the saved function file is on the computer',
'S8.2-5':'the saved source persists beyond the gawk process',
'S8.2-6':'Q2 decides its kind; whether an explicit recording exemption survives is not another kind question',
'S8.2-7':'this separately saved manual copy is not unchanged installed-package receipt',
'S8.2-9':'the function executes in the interpreter with its process rights',
'S8.2-10':'Q2 concludes it is a program belonging to what is installed',
'S8.2-15':'the downloaded-source/material fallback is later than Q2',
'S8.2-16':'an affirmative required-recording reading needs own or input-derived coverage, not merely naming gawk',
'S8.2-21':'the complete function only concatenates strings and returns the result; it cannot itself launch programs or change installation/settings',
'S8.2-23':'the function source is executed as code',
})
witness('default', 'An SSH server default host key created by its package installation', 'property_sources.md PS1,PS2,PS3', {
'S8.1-10':'effective service identity uses the generated key value',
'S8.1-12':'the covering package line may require a generated default without spelling its random value',
'S8.1-13':'package-driven generation can be part of bringing the service into conformity',
'S8.1-15':'generation inside the installer is not an outside-tool direct edit',
'S8.1-16':'ordinary installer generation has no breaking exemption to invoke',
'S8.2-6':'the order does not make generated bytes present in a covering line',
'S8.2-7':'generated host-key bytes were not received unchanged in the package archive',
'S8.2-11':'person choosing installation versus the resulting generated value is a boundary; the explicit service-parameter clause is closest',
'S8.2-13':'the default host identity is a service parameter',
'S8.2-15':'the outward-login private-key example is not this server-identity parameter',
'S8.2-16':'if treated as a package-derived installed object, package derivation still covers it',
'S8.2-17':'installation-created default values are expressly package-covered',
'S8.2-18':'no external-list source is the cause of these locally generated random bytes',
'S8.2-23':'the host key is read as data, not executed as code',
})
witness('external', 'An SSSD account obtained through its configured LDAP identity provider, with that source named by a declaration line', 'PAIR10; S8.2-18', {
'S8.1-1':'the declaration can describe account configuration by a source',
'S8.1-3':'an external list need not itself become a designated declaration file',
'S8.1-11':'the account in-force predicate is existence, not literal inclusion of every account byte in the text',
'S8.1-12':'the line can require the account source to determine membership',
'S8.1-14':'source changes do not themselves select a new last-successful declaration text',
'S8.2-1':'account recording may be satisfied through the explicit source rule',
'S8.2-3':'the rule concerns accounts present on the computer; the remote server itself need not be an installed local object',
'S8.2-11':'chosen account-source policy is configuration',
'S8.2-12':'accounts supplied through the configured source can be settings',
'S8.2-13':'accounts are expressly within settings',
'S8.2-15':'program-cached source data does not by itself override account-setting classification',
'S8.2-16':'installed-object derivation is not required for this express account-list coverage',
'S8.2-17':'the source line is the recording line under the more specific S8.2-18 provision',
'S8.2-18':'the named source expressly counts as recorded',
'S8.2-19':'enumerating the individual accounts as well is permitted, not required by this provision',
})
witness('nfs', 'An executable not yet read locally in a diskless client root mounted from an NFS server', 'ADDITIONAL_SOURCES.md NFSROOT', {
'S8.1-9':'runnable code can be started on the client even though persistent storage is remote',
'S8.2-3':'physical-location and mounted-namespace readings were examined; neither establishes a different complete declaration here',
'S8.2-5':'the mount point follows its setting; that rule alone does not classify all persistent remote files',
'S8.2-9':'under namespace presence the executable satisfies Q2; under physical absence the prior scope gate excludes the remote stored file',
'S8.2-13':'the NFS filesystem/source configuration must be recorded under either reading',
'S8.2-16':'the same source line can cover what is obtained through the mount; a compulsory additional code line has not been established',
'S8.2-18':'if the remote tree is taken as an external set, naming its source supplies express source coverage',
})
witness('material', 'Ordinary non-executable table records saved by SQLite at a person\'s request, considered separately from trigger code', 'TERM_SOURCES.md SQLITE,TRIGGER', {
'S8.1-12':'if optionally recorded, their required state comes from their line',
'S8.2-1':'ordinary data records are not installed code/settings on the specified facts',
'S8.2-2':'ordinary table data can be omitted',
'S8.2-3':'the stored records are on the computer',
'S8.2-5':'persistent table records are not merely runtime objects',
'S8.2-6':'after negative Q1-Q3 answers, Q4 is reached; it does not order the two Q4 provenance clauses',
'S8.2-7':'new personal table values are not unchanged package payload',
'S8.2-9':'these particular ordinary data values are not executable SQL',
'S8.2-11':'these records are not values configuring the computer',
'S8.2-14':'ordinary data values neither launch code nor grant access on the specified facts',
'S8.2-15':'human creation and program persistence overlap, but both Q4 names permit omission',
'S8.2-19':'a declaration may voluntarily include these data records',
'S8.2-20':'the non-code data are not programs',
'S8.2-23':'reading these rows as values does not make those rows code; mixed-file extent is a separate term boundary',
})

bykey = {w['key']:w for w in W}
q1 = {'S8.2-7','S8.2-8'}
q2 = {'S8.2-9','S8.2-10'}
q3 = {'S8.2-11','S8.2-12','S8.2-13','S8.2-14'}
q4 = {'S8.2-15'}
groups = [q1,q2,q3,q4]

overrides = {}
def override(a,b,key,result,reason):
    overrides[frozenset((a,b))] = (key,result,reason)

# Explicit direct-rule overlaps. The exceptional recording wording is not a
# fifth question: it preserves the kind while expressly excepting the duty.
for a in ['S8.2-1','S8.2-9','S8.2-10','S8.2-16']:
    override(a,'S8.2-21','sandbox','consistent','S8.2-21 is an explicit specific exception to the general recording duty. Q2 still decides program; the exception changes required coverage, not question order. The candidate fails the strongest objection: the text itself says this qualifying code need not be recorded.')
override('S8.2-6','S8.2-21','sandbox','consistent','The question order still selects Q2; the separate recording exception is examined against S8.2-1, not treated as a fifth classification question.')
override('S8.2-5','S8.2-22','service','consistent','A daemon executable and its transient process instance are different objects. S8.2-5 follows the creating program; S8.2-22 confirms that program is not exempt because of its process/container.')
override('S8.2-4','S8.2-9','history','consistent','The typed action is excluded; the separately saved replayable command is code. One sentence does not erase the later persistent artifact.')
override('S8.2-4','S8.2-15','history','consistent','An action and the history artifact produced from it are distinguishable; executable history reaches Q2 before Q4.')
override('S8.2-11','S8.2-14','auth','consistent','The personal launch/access clause supplies an express Q3 inclusion; it is not a contradictory fourth-question fallback.')
override('S8.2-13','S8.2-14','auth','consistent','Incoming access is required under both the explicit login category and the personal access extension.')
override('S8.2-16','S8.2-17','package','consistent','Unchanged shipped defaults have package coverage under both routes. A modified executable configuration would take Q2 before Q3; these are not two competing mandatory lines for the same ordered kind.')
override('S8.2-17','S8.2-18','external','consistent','The explicitly permitted external source line is a setting line; naming the source is an express coverage rule, not a requirement to enumerate the list.')
override('S8.2-9','S8.2-20','foreign','consistent','Executable capability is affirmative for Q2 or absent for S8.2-20; the specified incompatible file with no interpreter meets only the exclusion.')
override('S8.2-10','S8.2-20','foreign','consistent','The program conclusion requires affirmative Q2, which the incapable foreign-format case lacks.')
override('S8.2-20','S8.2-23','foreign','consistent','A representation can contain code yet lack execution capability here. Code representation and being a program are different predicates.')
for x in ['S8.1-4','S8.1-5','S8.1-7']:
    override(x,'S8.1-8','editor','consistent','The embedded-installer functionality exception is explicit; ordinary editing and package management need not receive the same tool status.')
override('S8.1-9','S8.1-11','service','consistent','Service enablement and availability of its executable are predicates of different objects. Neither requires equating a service with its binary.')
override('S8.1-10','S8.1-11','service','consistent','The requested service value and enabled service predicate can both be read; S8.1-12 supplies the line-required state. Static enablement remains a term boundary, not a pairwise opposite recording decision.')
for a in ['S8.1-9','S8.2-5','S8.2-9','S8.2-13','S8.2-16','S8.2-18']:
    override(a,'S8.2-3','nfs','consistent','Remote storage versus mounted namespace is an open scope phrase, but the same obligatory filesystem/source line can cover the remote executable if it is in scope. No different complete declaration or P1 result was established; see REVIEW.md NFS boundary.')

rows=[]
for a,b in itertools.combinations(sentences,2):
    special=overrides.get(frozenset((a,b)))
    if special:
        key,result,reason=special
        w=bykey[key]
    else:
        ga=next((i for i,g in enumerate(groups) if a in g),None)
        gb=next((i for i,g in enumerate(groups) if b in g),None)
        if ga is not None and gb is not None and ga != gb:
            first,last=sorted((ga,gb))
            key={0:'package',1:'history',2:'auth'}[first]
            w=bykey[key]
            result='settled by the order'
            reason=f'Q{first+1} is earlier than Q{last+1}. On this witness the earlier affirmative answer decides; the later predicate/provenance does not reverse it.'
        else:
            # Prefer two directly relevant effects; preserve stable tie order.
            w=max(W,key=lambda x:(int(a in x['effects'])+int(b in x['effects']), int(a in x['effects'] and b in x['effects'])))
            result='consistent'
            reason='The two stated effects do not require opposite declarations on this witness.'
            if a not in w['effects'] or b not in w['effects']:
                reason='The predicates have different scope on this witness; an unmet antecedent is not an opposite answer.'
    ea=w['effects'].get(a,scopes[a])
    eb=w['effects'].get(b,scopes[b])
    rows.append([a,b,w['obj'],result,ea,eb,reason,w['source']])

with (HERE/'PAIRS.tsv').open('w',newline='') as f:
    writer=csv.writer(f,delimiter='\t',lineterminator='\n')
    writer.writerow(['sentence_A','sentence_B','object_tried','result','effect_A','effect_B','reason','source'])
    writer.writerows(rows)
with (HERE/'PAIR_SENTENCES.tsv').open('w',newline='') as f:
    writer=csv.writer(f,delimiter='\t',lineterminator='\n')
    writer.writerow(['id','role','quote'])
    writer.writerows((sid,'definition used by deciding rules' if sid.startswith('S8.1') else 'deciding rule / scope / order / coverage / clarification',q) for sid,q in sentences.items())
assert len(rows)==39*38//2==741
assert len({frozenset(r[:2]) for r in rows})==741
print('39 sentences; 741 distinct unordered pairs; no omitted or duplicate pairs')
print({k:sum(r[3]==k for r in rows) for k in ['consistent','settled by the order','collision']})
