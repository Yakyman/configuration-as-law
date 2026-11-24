from pathlib import Path
import csv,re,json
from collections import Counter
B=Path(__file__).resolve().parents[1]
paths=[B/'part-install/part.tsv',B/'part-config/part.tsv',B/'raw/root-part.tsv']
rows=[]
for p in paths:
 rows+=list(csv.DictReader(p.open(),delimiter='\t',quoting=csv.QUOTE_MINIMAL if p.parent.name=='part-config' else csv.QUOTE_NONE))
d={r['variant'].split()[0]:r for r in rows}
P='Q1 no; Q2 yes: kind=program (S8.2-6, S8.2-9, S8.2-10, S8.2-23); stop'
S='Q1 no; Q2 no; Q3 yes: kind=setting (S8.2-6, S8.2-11, S8.2-12, S8.2-13, S8.2-14); stop'
R='Q1 no; Q2 no; Q3 no; Q4 program-created non-code record: kind=program record (S8.2-6, S8.2-15)'
T='kind=runtime; exists only while the computer runs; not a separate object, follows creating program/setting (S8.2-5), before Q1-Q4'
Z='[wheel format](https://packaging.python.org/en/latest/specifications/binary-distribution-format/) [zipimport](https://docs.python.org/3/library/zipimport.html)'

r=d['C1.3'];r['leaves']=r['leaves'].replace(', database at --dbpath <dbdir>','')
for id in ['C1.4','C2.5']:
 r=d[id];r['leaves']+='; unknown additional hook/backend-created files, registrations or values: the actual hook/backend body is not identified by the variant.'
 r['kind']+='; additional outputs: unknown until their provenance, executability, values and lifetime are established.'
 r['record']+='; additional outputs: recording/coverage unknown for the same missing facts.'

r=d['C2.1']
r['leaves']=r['leaves'].replace('c) compressed HTTP/wheel cache','c) non-code HTTP response metadata cache').replace('under $XDG_CACHE_HOME/pip/ (default $HOME/.cache/pip/)','under $XDG_CACHE_HOME/pip/ (default $HOME/.cache/pip/)')
r['leaves']+='; d) retained .whl ZIP archives under pip cache root; exact payload/import compatibility unspecified. '+Z
r['kind']+='; d) Q1 no (cached, not this installed package instance); Q2 yes for directly loadable Python code => kind=program; otherwise Q2 no/Q3 no/Q4 => kind=program record (S8.2-9, S8.2-15, S8.2-20). Which branch holds for the particular wheel is unknown.'
r['record']+='; d) executable wheel code needs own line or actual source/build line (S8.2-16); non-executable generated archive need not be recorded (S8.2-2, S8.2-15).'
r['status']='FACT_UNKNOWN';r['reason']='Installed payload and generated metadata are decided; documentation permits directly executable wheels but the retained wheel contents and import compatibility are unspecified.'

r=d['C2.2']
r['leaves']=r['leaves'].replace('c) npm cache under $HOME/.npm/; dependency resolution metadata package-lock.json when produced','c) npm non-executable download-cache tarballs and cache index under $HOME/.npm/; d) generated dependency resolution metadata ./package-lock.json when produced')
r['kind']+='; d) '+R
r['record']+='; d) need not be recorded unless designated declaration content (S8.2-2, S8.2-15; S8.1-3).'

r=d['C2.3'];r['leaves']+='; retained wheel archives may contain directly importable code, unlike non-loadable source tarballs. '+Z
r['kind']=r['kind'].replace('b) kind=material; Q1 no; Q2 no; Q3 no; Q4 person-brought (S8.2-15): material','b) Q1 no; Q2 yes for directly loadable wheel code => kind=program (S8.2-9, S8.2-10); otherwise Q2 no/Q3 no/Q4 person-brought => kind=material (S8.2-15); actual archive compatibility unknown')
r['kind']=r['kind'].replace('c) kind=program record; Q1 no; Q2 no; Q3 no; Q4 program-created (S8.2-15): program record','c) installation metadata: '+R+'; generated wheel: Q1 no/Q2 yes if executable => kind=program, otherwise Q4 kind=program record; compatibility unknown')
r['record']=r['record'].replace('b) need not be recorded (S8.2-2/15/19)','b) executable code: own or actual obtained/built-from line (S8.2-16); non-executable brought archive need not be recorded (S8.2-2, S8.2-15)').replace('c) need not be recorded (S8.2-2/15/19)','c) metadata/non-executable cache need not be recorded; executable cached wheel needs own or actual source/build line (S8.2-16)')
r['status']='FACT_UNKNOWN';r['reason']='Source transport does not change installed payload classification; exact retained wheel/archive contents are missing, so code versus material/record and its coverage cannot be fixed.'

r=d['C2.5'];r['leaves']+=' Generated wheels may support direct imports. '+Z
r['kind']=r['kind'].replace('c) kind=program record; Q1 no; Q2 no; Q3 no; Q4 program-created (S8.2-15): program record','c) Q1 no; Q2 yes for directly loadable wheel code => kind=program; otherwise Q3 no/Q4 => kind=program record (S8.2-9, S8.2-15); actual wheel compatibility unknown')
r['record']=r['record'].replace('c) need not be recorded (S8.2-2/15/19)','c) loadable code: own or actual source/build line (S8.2-16); non-loadable generated archive need not be recorded (S8.2-2, S8.2-15)')

r=d['C2.6']
r['leaves']=r['leaves'].replace('c) locally supplied .pth containing only search-directory values, read as values by site initialization','c) locally supplied personal-interpreter .pth containing only search-directory values, read as values, not an executable import line or an independent launch/access grant')
r['kind']=r['kind'].replace('c) kind=program record; Q1 no; Q2 no; Q3 no; Q4 program-created (S8.2-15): program record','c) Q1 no; Q2 no; Q3 personal-only non-launch/non-access value => kind=program record under the express otherwise clause S8.2-14; no claim of program-created origin; S8.2-23 excludes code')
r['record']=r['record'].replace('c) need not be recorded (S8.2-2/15/19)','c) need not be recorded (S8.2-2, S8.2-14); a separately specified system-wide or launch/access value instead reaches Q3 and needs its own line (S8.2-11 to S8.2-14, S8.2-17)')
r['reason']='Package originals stop at Q1; executable additions stop at Q2. A personal-only value neither launching nor granting access is a program record by S8.2-14, regardless of who wrote it.'

r=d['C3.1']
r['leaves']=r['leaves'].replace('b) /var/lib/flatpak/repo/config and refs/ administrative state','b) /var/lib/flatpak/repo/refs/ administrative state')
r['leaves']+='; d) chosen remote URL/policy values in /var/lib/flatpak/repo/config. [flatpak](https://docs.flatpak.org/en/latest/flatpak-command-reference.html)'
r['kind']+='; d) '+S;r['record']+='; d) own setting line, or installing package line for a documented installation default (S8.2-17).'

r=d['C4.3'];r['route']=r['route'].replace('[UNKNOWN] ','').split('; unspecified application self-updater:')[0]
r['status']='DECIDED';r['reason']='Ordinary download/copy/sync is general-purpose; the documented dedicated updater changes installed executable code and is a built-in tool under S8.1-7. Removing programs is required only for the installer label.'

for id in ['C5.1','C5.2','C5.3','C5.5']:
 r=d[id]
 r['route']='[BUILTIN] specialized compiler/build/installation functionality whose documented purpose creates or replaces executable programs (S8.1-7; S8.2-10); no installing-and-removing purpose is inferred under S8.1-4. [GENERAL] separately invoked shell, manual copying/link creation or editor operations (S8.1-8). [compiler output](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html) [CMake purpose and installation](https://cmake.org/cmake/help/latest/manual/cmake.1.html)'
d['C5.3']['reason']='CMake installation and specialized build output change installed programs under S8.1-7; shell/copy/link operations remain general-purpose. Executable startup files are programs; separately chosen launch links are settings.'
d['C5.4']['route']='[BUILTIN] specialized compiler/linker replacing executable output, whose documented purpose changes installed programs (S8.1-7; S8.2-10). [GENERAL] manual user copying/editing (S8.1-8). [BREAKING] separately privileged direct replacement past the declaration outside built-in tools (S8.1-15, S8.1-16). [compiler output](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html)'
d['C5.4']['reason']='Changed executable bytes fail the unchanged-package test and are programs. Specialized compilation is built-in; manual replacement uses the general-purpose or breaking route according to privileges and declaration bypass.'

r=d['C6.3'];r['record']='a,b: no separate line for the transient registration/properties, process or relation; follows the recorded creating program or setting (S8.2-5). A separately retained service-parameter value, if one exists outside this transient object, is a different Q3 setting with its own line (S8.2-13, S8.2-17); the transient command alone establishes no such persistent value.'
r['reason']='The described registration, properties and execution state exist only while the computer runs and follow their creator. A separately retained service setting would require its own line.'

r=d['C6.5'];r['leaves']+='; d) additional saved script/module named by cron shell text or generator, at the supplied source/import path; neither target nor provenance is supplied. [source](https://tiswww.case.edu/php/chet/bash/bashref.html)'
r['kind']+='; d) Q1 yes if unchanged installed-package member => kind=installed object; otherwise Q2 yes if retained executable input => kind=program (S8.2-7 to S8.2-10); actual target/provenance unknown.'
r['record']+='; d) package line if Q1, otherwise own or actual source/build line (S8.2-16); recording the caller alone does not supply input coverage.'
r['status']='FACT_UNKNOWN';r['reason']='The generator, cron code and transient outputs are decided; the additional loaded file and its package/source provenance are not identified, so its exact kind and covering line remain unknown.'

r=d['C8.05'];r['kind']=r['kind'].replace('b,c: Q1 no; Q2 yes: program (S8.2-6/9/10/23); stop','b: '+T+'; c: '+P)
r['record']='a: own setting line (S8.2-17); b: no separate runtime-object line; follows the stored launch value and executing shell (S8.2-5); c: own or actual build/source line (S8.2-16).'
r['route']='[GENERAL] general-purpose Git configuration, shell/editor and recipe execution (S8.1-8); Git reads configuration values and passes !alias/filter commands to a shell; no built-in-installer function is used (S8.1-5, S8.1-8). [git-config](https://git-scm.com/docs/git-config)'
r['reason']='Stored launch-selector values are settings; the passed shell snippet is temporary state. A retained build recipe is code. The general-purpose exclusion has no configuration-mode exception.'

r=d['C8.07'];r['leaves']='a: installed extension bundle under <Firefox-profile>/extensions/; b: generated launch enablement/userDisabled value in <Firefox-profile>/extensions.json; c: generated descriptive extension metadata in that database. [profile](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data?mobile=0) [extension database implementation](https://raw.githubusercontent.com/mozilla-firefox/firefox/main/toolkit/mozapps/extensions/internal/XPIDatabase.sys.mjs)'
r['kind']='a: Q1 yes => kind=installed object, stop (S8.2-6, S8.2-7, S8.2-8); b: '+S+'; c: '+R
r['record']='a: extension package line (S8.2-16); b: package line when created as installation default; own setting line for later chosen enablement/access policy (S8.2-17); c: need not be recorded (S8.2-2, S8.2-15).'

r=d['C8.08'];r['leaves']+=' [actual page-opening behavior](https://support.mozilla.org/en-US/kb/how-to-set-the-home-page)'
r['route']='[GENERAL] browser preference editing without superuser rights; a general-purpose browser changes its stored preference values, outside its installer functionality (S8.1-5, S8.1-8). [home-page UI](https://support.mozilla.org/en-US/kb/how-to-set-the-home-page)'

r=d['C7.19'];r['leaves']='a=web code/JIT in renderer memory; b=when disk caching is enabled and the script qualifies, serialized generated code entry under <configured-cache-path>/Code Cache/js/ (or Code Cache/pc/ with the newer collection backend), keyed by script URL; c=recorded renderer/helper executables. [cache contents and reuse](https://v8.dev/blog/improved-code-caching) [cache root](https://chromium.googlesource.com/chromium/src/+/main/content/browser/storage_partition_impl.cc) [cache subdirectories](https://chromium.googlesource.com/chromium/src/+/main/content/browser/code_cache/generated_code_cache_context.cc) [confinement](https://chromium.googlesource.com/chromium/src/+/main/docs/design/sandbox.md)'
r['kind']='a: '+T+'; b: Q1 no; Q2 yes for reusable generated code => kind=program (S8.2-9, S8.2-10); non-code cache keys/metadata instead Q1-Q3 no/Q4 kind=program record (S8.2-15); c: Q1 yes if unchanged packaged executable => kind=installed object; otherwise Q2 kind=program (S8.2-7 to S8.2-10).'
r['record']='a: no separate runtime line, follows renderer/program (S8.2-5); b: saved code needs its own or actual source/build line (S8.2-16), unless it cannot itself launch programs or change installed objects/settings (S8.2-21); the cited sandbox purpose establishes no persistent changes but not the separate no-launch condition for all browser interfaces, so exemption unknown; non-code cache metadata need not be recorded (S8.2-2, S8.2-15); c: package/program line for every separate helper executable (S8.2-16, S8.2-22).'
r['status']='FACT_UNKNOWN'
r['reason']='Saved generated code is documented. Its S8.2-21 exemption additionally requires inability to launch programs; that capability restriction is not established by the cited no-persistent-changes sandbox purpose.'

r=d['C7.24']
r['leaves']='a=recorded dispatcher script; b=instruction file at its read path or instruction bytes supplied through stdin, argv/environment, inherited descriptor or socket/IPC; c=dispatcher-created persistent outputs, unspecified. The original CHANNELS.md paragraphs beginning For C7.07/08/24 and The concrete custom-dispatch variant explicitly stipulate that these instructions execute with the dispatcher\'s own rights. No implementation or per-operation outputs are supplied. [execution interface example](https://docs.python.org/3/extending/embedding.html)'
r['kind']='a: Q1 no for the described custom script; Q2 yes => kind=program (S8.2-9, S8.2-10); b saved instructions: Q1 no; Q2 yes => kind=program under the explicit code/own-rights premise (S8.2-9, S8.2-10, S8.2-23); b non-file stream: '+T+'; c: Q1-Q4 unknown until actual retained outputs are identified.'
r['record']='a: supplied recorded script line; b saved code: own line or actual system-built/obtained-from line (S8.2-16), not covered merely by naming the dispatcher; b stream: no separate line, follows its creating program/setting (S8.2-5); c: unknown for unidentified outputs.'
r['reason']='Executable instruction semantics are an explicit inventory premise. The dispatcher implementation, concrete persistent side effects, and documented installation/configuration purpose are absent.'

r=d['C7.21'];r['leaves']=r['leaves'].replace('Permissions and contents of the supplied directory are not fixed.','The CLI grants WASI read/write permissions; effective host permissions, reachable contents and module effects are not fixed.')+' [CLI read/write implementation](https://raw.githubusercontent.com/bytecodealliance/wasmtime/main/src/common.rs)'
r['reason']='CLI WASI read/write authority is documented. Effective host permissions, reachable files and module behavior are unspecified, so ability to change installed code/settings and actual additional outputs cannot be established.'

# Canonical numbered quotations, and explicit locally numbered imported passages.
sent={m.group(1):m.group(2).replace('**','') for m in re.finditer(r'^- \*\*(S[\d.-]+)\*\* (.*)$',(B.parent/'SENTENCES.md').read_text(),re.M)}
def q(s):return s+': «'+sent[s]+'»'
ch='B1-9.3-channel (local ID): «A channel is anything that such a command tries to leave behind: saving and running a file, registering a service, a timer or an autostart, changing a setting.»'
co='B1-9.3-command (local ID): «A command typed by a person is not considered a channel for bypassing the declaration.»'
st='B1-9.3-stream (local ID): «A separate case: a command downloads and executes code without saving it; after a reboot, nothing that was executed must be in force.»'
for r in rows:
 id=r['variant'].split()[0]
 extras=[]
 if '[BREAKING]' in r['route']:extras+=[q('S8.1-15'),q('S8.1-16')]
 if id.startswith('M') or id in ['C1.6','C6.6','C9.6']:
  extras += [q('S8.3-1'),q('S8.3-4'),q('S8.3-5'),q('S8.1-14'),'B1-A.4.3-removal (local ID): «after application of a declaration without a line, something the line contributed and the remaining lines do not cover is in force (Removal, P1).» This is the imported failure condition, not an implementation prescription.']
 r['law']=' '.join([q('S8.3-6'),q('S8.3-7'),q('S8.3-8'),ch]+([co,st] if id in ['C4.5','C7.03','C7.04','C7.06','C7.15','C7.16','C7.17'] else [])+extras)
 r['leaves']=r['leaves'].replace('Evidence: B1/part-config/sources.md.','Evidence: SOURCES.md.')
 if 'installer: pip' in r['route']:
  r['route']+=' [pip removal purpose](https://pip.pypa.io/en/stable/cli/pip_uninstall/)'
 # Expand compact citations into valid, separately identifiable sentence IDs.
 for field in ['kind','record','route','reason']:
  r[field]=re.sub(r'(S\d\.\d)-(\d+(?:/\d+)+)',lambda m:', '.join(m[1]+'-'+n for n in m[2].split('/')),r[field])
  r[field]=re.sub(r'(S\d\.\d)-(\d+) to (S\d\.\d)-(\d+)',lambda m:', '.join(m[1]+'-'+str(n) for n in range(int(m[2]),int(m[4])+1)) if m[1]==m[3] else m[0],r[field])

names=json.loads((B/'raw/variants.json').read_text())
byname={r['variant']:r for r in rows};rows=[byname[n] for n in names]
with (B/'CHANNELS-V4.tsv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',quoting=csv.QUOTE_NONE,quotechar=None,lineterminator='\n');w.writeheader();w.writerows(rows)

gap='''# Gaps in the 88-row classification

This is the separate, unweighted investigation required by PROTOCOL.md Section 5. The sole TWO_WAYS row is C8.08; there are no NOT_DECIDED rows. Missing tool/artifact facts are listed in the table as FACT_UNKNOWN and are not textual gaps.

## Home-page navigation and launching something

S8.2-14 does not say whether opening the chosen home page is launching something: for C8.08 the same stored URL is either a setting under S8.2-14 requiring its own line under S8.2-17, or a program record under S8.2-14 that need not be recorded under S8.2-2.

The documented objects are a chosen theme value and a home-page URL in the browser profile preferences. The homepage is opened on browser start, a new window, or the Home button, as documented in [home-page behavior](https://support.mozilla.org/en-US/kb/how-to-set-the-home-page); [preference storage](https://support.mozilla.org/en-US/kb/firefox-support-troubleshooting-guide?mobile=0) documents the stored values. Short primary excerpts are in [SOURCES.md](SOURCES.md).

Both values fail Q1 (not unchanged package contents) and Q2 (read as values, not executed as code). The theme is a program record under S8.2-14 under both readings. For the URL, the broad reading includes page opening in launching something; the narrow reading means launching an executable/program and treats page display as ordinary work within the already-running browser. No sentence selects between these meanings.

The declarations differ by the required home-page setting line. Under the broad reading, changing that URL must follow the declaration and P4 disallows an ordinary bypass; under the narrow reading, the URL need not be recorded and this preference change is outside P4's installed-object/setting requirement. Voluntary recording remains permitted by S8.2-19. The result concerns the requirement, not the mechanism by which it is enforced.

'''
for s in ['S8.2-6','S8.2-14','S8.2-17','S8.2-2','S8.3-6','S8.3-8']:
 gap+=q(s)+'\n\n'
(B/'GAPS.md').write_text(gap)
print(Counter(r['status'] for r in rows))
