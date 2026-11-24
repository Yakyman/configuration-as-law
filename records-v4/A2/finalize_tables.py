"""Apply final review dispositions to the sweep records; preserve initial notes."""
import csv
from pathlib import Path

P=Path(__file__).resolve().parent
def read(name):
    with (P/name).open(newline='') as f:
        reader=csv.DictReader(f,delimiter='\t')
        return reader.fieldnames,list(reader)
def write(name,fields,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n')
        w.writeheader();w.writerows(rows)

fields,rows=read('TERMS.tsv')
updates={
'program of the system':('yes S8.1-5,S8.1-8','The documented embedded installer exception places this concrete Emacs case; undefined general membership does not leave this object undecided.','rejected: explicit functional exception'),
'service; enabled':('yes S8.1-11,S8.1-12','The primary documentation explicitly calls static not enabled; activation eligibility is a different fact. A broader meaning is not supplied by the text.','rejected: no opposing property result established'),
'account exists':('yes S8.1-11,S8.2-13','A namespace-local account exists in the specified namespace; the text does not limit accounts to the initial namespace. Adding that limitation creates the proposed ambiguity.','rejected: no host-only qualifier'),
'superuser privileges':('yes S8.1-15','Refined boundary: direct shell append to container /etc/sudoers at mode0440 using mapped namespace CAP_DAC_OVERRIDE. This capability is a unit of superuser privilege; absence of initial-namespace privilege does not negate the power used on this file. See ADDITIONAL_SOURCES.md CAP,SUDO,PODMAN and REVIEW.md.','rejected after strengthened witness: breaking'),
'object; separate object; file versus contained value':('yes S8.2-21,S8.2-23','Ordinary SQLite trigger code is exempt restricted code on the supplied facts. A database relation is read as structured values; an extracted executable source value is distinguishable from the containing file. No mandatory-recording difference established.','rejected: supplied whole-file alternative lacks factual support'),
'with that program rights':('no','Process credentials and language operations differ, but this restricted-code witness cannot establish opposing declarations: S8.2-21 expressly permits omission even on the Q2 program reading.','rejected: explicit exemption equalizes recording'),
'computer as a whole obeys':('yes S8.2-13,S8.2-14','A database service parameter is expressly included; a merely personal nonlaunching/nonaccess value has the explicit personal-program rule. The examined session value did not establish opposite duties on identical facts.','rejected: no surviving contrary declaration'),
'line of its own; line of package':('yes S8.2-16','The coverage sentence contains no remains-as-received condition. Literal package-origin coverage for still-executable modified code therefore remains available; importing the Q1 condition into the later coverage rule would add text.','rejected: broad coverage is determinate, not a repair request'),
'system itself built or obtained; from a line':('yes S8.2-16','A personal Python source is itself executable code whenever its bytecode is non-exempt; its required line covers the compiled copy. Tool-only versus source coverage creates no different complete declaration here. Section8.6 separately says executable history is not built from recorded content, defeating tool-only provenance.','rejected after refutation: no different complete declarations'),
'inside a recorded program; cannot itself launch or change':('no','Returning proxy-selection values is an indirect effect. The evidence does not show direct forbidden capability or two different required declarations; S8.2-21 is a recording exception, not a fifth kind question.','rejected on supplied boundary; no general causal-depth rule invented'),
'executes as code versus only reads as values':('yes S8.2-14,S8.2-23','SSH parses the configuration as values; the extracted Match exec command launches a shell command. This does not establish that the entire containing file is executed as code. The launch value is recorded under either Q2 or Q3.','rejected: consumption mode and launch rule decide this witness'),
'only by breaking':('yes S8.1-15,S8.3-8','Namespace-local CAP_DAC_OVERRIDE actually supplies the superuser power for the refined protected-file write. The stronger all-paths clause gives no exemption for a merely ordinary unprivileged bypass.','rejected: privilege used over changed object is breaking'),
}
for r in rows:
    if r['term'] in updates:
        r['does_text_place_it'],r['reasoning'],r['candidate_gap']=updates[r['term']]
    if r['term']=='list outside declaration; source named':
        r['boundary_object']='SSSD configured with an external LDAP identity provider'
        r['source (passage in TERM_SOURCES.md)']='PAIR10 https://sssd.io/docs/quick-start.html (passage in PAIR_SOURCES.md)'
        r['reasoning']='The named LDAP source may determine the account list under S8.2-18; source-only coverage is expressly permitted rather than a missing account enumeration.'
extra=[
['on the computer: physical or mounted presence','S8.1-9,S8.2-3,S8.2-5,S8.2-9,S8.2-16,S8.2-18','Unread executable in a diskless NFS-root client filesystem','NFSROOT https://docs.kernel.org/admin-guide/nfs/nfsroot.html (ADDITIONAL_SOURCES.md)','no','Physical storage and mounted namespace readings differ in scope, but both require the filesystem/source line; the same line can supply obtained-object/source coverage if remote code is in scope. No additional own line or opposing P1 result established.','rejected after declaration-level refutation: same complete declaration'],
['program runs or can be started: suspension','S8.1-9,S8.2-9,S8.3-1,S8.3-5','Recorded user-space program during normal suspension','PS7 https://docs.kernel.org/admin-guide/pm/sleep-states.html (property_sources.md)','yes S8.1-9','No immediate-execution requirement appears in can be started; ordinary resumption preserves capability. The proposed contradiction adds a time horizon instead of establishing it.','rejected: no opposed P2 result established'],
['code inside structured storage','S8.2-9,S8.2-21,S8.2-23','PostgreSQL untrusted PL/Python source in pg_proc.prosrc','PLSOURCE https://www.postgresql.org/docs/18/catalog-pg-proc.html; PLPOWER https://www.postgresql.org/docs/18/plpython.html (ADDITIONAL_SOURCES.md)','yes S8.2-9,S8.2-23','A stronger code witness can have operating-system effects, but extracted prosrc is executable source while the binary catalog relation is parsed as values; mandatory source coverage does not require all catalog bytes.','rejected: stronger witness still lacks opposing extent'],
['superuser power over a protected settings file','S8.1-8,S8.1-15,S8.2-13,S8.2-17,S8.3-1','Rootless container shell append to /etc/sudoers at its default mode0440','CAP https://man7.org/linux/man-pages/man7/capabilities.7.html; SUDO https://www.sudo.ws/docs/man/1.9.14/sudoers.man.pdf; PODMAN https://docs.podman.io/en/stable/markdown/podman-create.1.html (ADDITIONAL_SOURCES.md)','yes S8.1-15','File ownership alone grants no write bit; namespace capability provides the required power. The changed access rule is a setting, but the direct privileged shell change is breaking. Initial-namespace-only interpretation adds words.','rejected: strongest objection decisive'],
]
for v in extra:
    if not any(r['term']==v[0] for r in rows):rows.append(dict(zip(fields,v)))
write('TERMS.tsv',fields,rows)

fields,rows=read('PROPERTIES.tsv')
for r in rows:
    if 'C-PROP-1' in r['result']:
        r['result']='rejected after independent review'
        r['reason_and_strongest_objection']='Primary sources establish generated bytes, not that those bytes are a person-chosen setting. HostKey path and the generated file contents are different objects. Even if package generation is covered, knowing the described generation does not conflict with P1/P2. Concrete-byte Understanding is not forced; see REVIEW.md.'
    if 'term boundary' in r['result']:
        r['result']='rejected after independent review'
        r['reason_and_strongest_objection']='Ordinary resumption preserves ability to start the program. Neither S8.1-9 nor Q2 requires immediate execution while asleep; the alleged contradiction adds that restriction. No separate declaration difference established.'
    r['reason_and_strongest_objection']=r['reason_and_strongest_objection'].replace('already C-PROP-1','part of the rejected concrete-byte Understanding candidate').replace('Random SSH identity is a cleaner concrete instance of C-PROP-1','The random-identity candidate also failed classification and consequence refutation')
    if r['real_object_or_situation']=='Service access configuration takes an external account list':
        r['real_object_or_situation']='SSSD accounts supplied by its configured LDAP identity provider'
        r['primary_source_reference']='PAIR10 (PAIR_SOURCES.md); S8.2-18'
extra=[
['P1 scope','Filesystem/source coverage','Unread executable in a diskless client NFS root','S8.1-9; S8.2-3; S8.2-13; S8.2-16; S8.2-18; S8.3-4','NFSROOT (ADDITIONAL_SOURCES.md)','Normal documented NFS-root boot; no privileged modification past a declaration is needed.','rejected','Physical and mounted-namespace scope readings leave the same obligatory filesystem/source line. If code is in scope, obtained-object or external-source coverage can use that line. No concrete complete declaration requiring an additional line or opposing P1 result was established.','The scope phrase precedes the questions; order does not define presence, but lack of a different declaration defeats the card filter.'],
['P1 + P4','S8.1-15 breaking exemption','Rootless namespace CAP_DAC_OVERRIDE used for a direct shell append to mode0440 /etc/sudoers','S8.1-8; S8.1-15; S8.2-13; S8.2-17; S8.3-1; S8.3-4; S8.3-8','CAP; SUDO; PODMAN (ADDITIONAL_SOURCES.md); USERNS (TERM_SOURCES.md)','The proposed no-breaking premise fails: actual namespace capability supplies superuser power over the file.','rejected','Absence of initial-namespace privilege does not negate the superuser power used. Reading breaking as host-only would add an unstated condition.','Changed non-code access rule reaches Q3; its own-line duty does not alter the breaking exemption.'],
['P1 + Understanding','Modified package-origin code','Locally edited executable configuration originally shipped in a package','S8.2-7; S8.2-9; S8.2-16; S8.3-4; S8.4-1','DEB (TERM_SOURCES.md)','Unprivileged owner editing would not be breaking; ordinary system noncompliance is not assumed to prove inconsistency.','rejected','S8.2-16 literally permits broad package-origin coverage. That does not promise to show every code byte, and P4 would independently prohibit past-description edits in a conforming system. No two sentences force opposite declarations.','Modified executable configuration takes Q2; the Q1 unchanged test is not silently imported into S8.2-16.'],
]
for v in extra:
    if not any(r['real_object_or_situation']==v[2] for r in rows):rows.append(dict(zip(fields,v)))
write('PROPERTIES.tsv',fields,rows)

fields,rows=read('raw/names_terms_initial.tsv')
rows.append(dict(zip(fields,['Package conffile value changed and later restored to the same default','S8.2-7,S8.2-13,S8.2-17','unchanged installed-object reading','setting/default-value reading','Default package coverage remains available; no different declaration established','DEB; TERM_SOURCES.md'])))
write('NAMES.tsv',fields,rows)
