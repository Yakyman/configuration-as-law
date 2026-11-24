import csv,json,pathlib,collections
root=pathlib.Path('A3/in/raw/developer');out=pathlib.Path('A3/c1/part-developer.tsv')
fields=['id','decision','sentences','what_it_does','basis','reason']
allrows=list(csv.DictReader(open('A3/in/part-developer.tsv'),delimiter='\t'))
done={r['id'] for r in csv.DictReader(open(out),delimiter='\t')}
rows=[r for r in allrows if r['kind'] in ['2:stored-ownership-unresolved','2:image-container-store'] and r['id'] not in done]
# This explicit decision ledger refers to the 225 individually inspected residual groups.
assert len(rows)==225
spec={}
def setrows(indices,decision,what,reason,sentences):
 for i in indices:
  assert i not in spec,i
  spec[i]=(decision,sentences,what,reason)
U='UNKNOWN';R='RECORD';T='RUNTIME'
setrows([0,1],U,'Persistent container storage containing unexpanded images, metadata, and writable layers.','The store was not expanded; its members, executable contents, installed-image provenance, and generated-state boundaries are absent.','S8.2-7,S8.2-9,S8.2-15,S8.2-16')
setrows([2],U,'Account backups, a filesystem script, resolver link, locks, and system directories.','The script contents, resolver target, and member installation or creation provenance are missing; one homogeneous decision cannot be established.','S8.2-7,S8.2-9,S8.2-11,S8.2-15')
setrows([3,183],U,'Alternative implementation selections and their management records.','Automatic installation defaults versus person-selected implementations, link targets, and active selection values are unrecorded; coverage and setting status depend on them.','S8.2-11,S8.2-14,S8.2-15,S8.2-17')
setrows([4,5],U,'Persistent firewall policy and zone definitions, including a backup where listed.','Configuration origin is explicitly unknown; installation defaults versus later chosen policies are unresolved, and backup membership prevents assuming homogeneous settings.','S8.2-11,S8.2-13,S8.2-15,S8.2-17')
setrows([7,8,9],U,'Persistent service resource-control property files.','Values and creation provenance are absent; person-chosen service parameters versus installation defaults or automatically generated state remain unresolved.','S8.2-11,S8.2-13,S8.2-15,S8.2-17')
setrows([10],U,'Persistent service-enablement links under the system target.','Individual link targets and installation-default versus later enablement provenance are missing; SETTING-OWN and SETTING-DEFAULT cannot be distinguished.','S8.2-13,S8.2-17')
setrows([11],U,'Repository definition used by the package manager.','Repository values and creation provenance are absent; installation-supplied defaults, later settings, and program-specific non-launching values cannot be distinguished.','S8.2-7,S8.2-11,S8.2-14,S8.2-17')
setrows([15,102],U,'Git repository control files, configuration, and metadata directories.','Configuration contents are absent; values launching helpers require settings, while repository indexes and references are records. Member provenance is also unresolved.','S8.2-7,S8.2-14,S8.2-15')
setrows([16],R,'Cached Git description of a repository revision.','The describe-cache stores a computed revision-description result, a program cache rather than executed code or chosen system configuration.','S8.2-15')
setrows([17,103],U,'Git sample hooks and, where present, an active commit hook.','Hook payload integrity and copied-template or generated-hook lineage are absent; executable code cannot be assigned package, derived, or own coverage.','S8.2-7,S8.2-9,S8.2-16')
setrows([18,104,120],R,'Git exclusion values and, where listed, a hook checksum record.','Git reads exclusion patterns and checksums as values; they neither launch programs nor grant access and are program records.','S8.2-14,S8.2-15,S8.2-23')
setrows([19,20,21,22,23,24,30,31,32,34,47,60,61,62,63,64,70,71,72,73,74,76,79,80,82,83,86,87,88,89,90,91,92,93,100,160],U,'Development-tool payloads, plugin files, launchers, installation metadata, or containing directories.','Per-member installation integrity and acquisition or generation lineage are absent; first-question package coverage versus later classifications and own or derived coverage cannot be settled.','S8.2-6,S8.2-7,S8.2-9,S8.2-16')
setrows([25,26,27,28],R,'Homebrew management state, linked-package tracking, locks, or temporary storage.','These internal tracking entries and locks record package-manager operation; they are neither installed payloads nor user-selected launch configuration.','S8.2-14,S8.2-15')
setrows([29],U,'Shell startup files, command history, and personal storage directories.','Shell-file contents and provenance, history execution behavior, and directory origins are absent; executable and non-executable members cannot be classified uniformly.','S8.2-7,S8.2-9,S8.2-15,S8.2-23')
setrows([33],U,'Bun registry-response cache files and extracted-package directories.','Registry-response files are records; extracted-package directory provenance and unchanged status remain unknown, preventing a complete member classification.','S8.2-7,S8.2-9,S8.2-15')
setrows([35,36,37,38,39,41,42,43,44,45,46,48,49,50,51,52,53,54,55],R,'Development package-manager metadata caches, download archives, and cache indexes.','Managers record metadata, archive downloads, locks, and cache-directory state; these listed members are not executed code or selected system settings.','S8.2-9,S8.2-15,S8.2-23')
setrows([40],U,'Homebrew cached selections of helper tools.','The saved curl and git selection contents and use are unrecorded; cached status versus values that select program launches cannot be distinguished.','S8.2-14,S8.2-15,S8.2-23')
setrows([57,58,59],R,'Go toolchain usage counters and telemetry storage.','Go records usage counters, upload bookkeeping, and their directories while running; these observed members are telemetry records.','S8.2-15')
setrows([66,67,68],U,'User service and timer definitions or their enablement links.','These launch services, but file contents, link targets, and installation-default versus later configuration provenance are not recorded.','S8.2-13,S8.2-14,S8.2-17')
setrows([69],R,'uv installer receipt describing an installation.','The receipt records installer state; it is read as metadata, not executed or used as chosen launch configuration.','S8.2-15,S8.2-23')
setrows([78],R,'Generated development project summary text.','The inventoried summary service generates a project summary; this stored text is its output record.','S8.2-15')
setrows([81],R,'Cached Ruby gem download archive.','The compressed download is retained package-manager cache data, distinct from the installed gem payload; it is not executed as code.','S8.2-7,S8.2-9,S8.2-15')
setrows([84,85],R,'Stored timestamp recording the user timer trigger.','The timer stamp records when it last triggered; this historical timestamp is a program record, not the timer schedule.','S8.2-15')
setrows([95],U,'Before-and-after shell configuration copies and a source revision record.','Shell copies may be executable code; their complete contents and source-line derivation are absent, while the revision identifier is a record.','S8.2-9,S8.2-15,S8.2-16,S8.2-23')
setrows([96],U,'SSH authorization, client configuration, and outbound key files.','Authorized-key default provenance, client launch/access directives, and key roles are not fully recorded; exact member decisions cannot be established.','S8.2-13,S8.2-14,S8.2-15,S8.2-17')
setrows([98,99,101,105,106,107,109,110,111,112,113,114,115,116,118,119,121,122,123,124,125,126,127,128,129,132,135,136,137,138,139,140,141,142,143,144,146,147,148,150,151,152,153,154,156,157,158],U,'Project source files, language fixtures, build recipes, documentation, or associated directories.','Member contents, compatible execution paths, and acquisition or generation lineage are unrecorded; executable code and its coverage cannot be distinguished reliably from material or records.','S8.2-7,S8.2-9,S8.2-15,S8.2-16,S8.2-20,S8.2-23')
setrows([159],R,'Captured action output and error logs.','These are stored output and error logs produced while commands ran; the files are records, not the actions themselves.','S8.2-4,S8.2-15')
setrows([163],U,'Installation recipes and administrative storage directories.','Recipe contents and whether they are retained records or executable instructions are not collected; directory creation provenance is also absent.','S8.2-9,S8.2-15,S8.2-23')
setrows([164,165],U,'Container-builder tokens, configuration, locks, and metadata directories.','Token roles and builder configuration contents are absent; access-granting or launch-setting values cannot be separated from ordinary bookkeeping.','S8.2-13,S8.2-14,S8.2-15')
setrows([166,167,168,169],R,'Container-builder activity and build-reference records.','Build activity and reference metadata record completed or ongoing builder operations; the listed members contain tracking state rather than image payloads.','S8.2-15')
setrows([170],T,'Kernel network-namespace handle mounted for a container.','dockerd (UNKNOWN: binary integrity unavailable) creates the namespace; raw nsfs magic identifies a kernel runtime handle despite the generic persistence label.','S8.2-5')
setrows([173],U,'Shared-library files, links, and library directories.','Library provenance, integrity, and symlink targets are missing; package-covered originals and independently executable or generated copies cannot be distinguished.','S8.2-7,S8.2-9,S8.2-16')
setrows([181],U,'System state directories and the package-database link.','Directory origins and the link target are absent; installed directory objects versus generated application state cannot be determined for all members.','S8.2-7,S8.2-15')
setrows([182],U,'NetworkManager internal configuration, leases, keys, and network-history records.','Leases and history are records, but internal configuration contents and access-key roles are absent; person-chosen settings versus generated state cannot be settled.','S8.2-11,S8.2-13,S8.2-15,S8.2-17')
setrows([184,185],R,'Repository countme participation bookkeeping.','The countme file tracks repository-client reporting state; it is generated bookkeeping, not a chosen network or access setting.','S8.2-15')
setrows([186],R,'Database recording the most recent account logins.','Last-login timestamps record past activity; they do not define accounts or authorize login.','S8.2-13,S8.2-15')
setrows([187,188,189],T,'Kernel SUNRPC communication directories, pipe, or client information.','Linux SUNRPC (INSTALLED-PACKAGE) creates these kernel interfaces; raw rpc_pipefs magic establishes runtime objects despite the collector generic persistence label.','S8.2-5,S8.2-7,S8.2-16')
setrows([190],R,'Journal-input cursor used by the system logger.','The journal cursor records consumed log position, a program working-state record rather than logging policy.','S8.2-15')
setrows([192],U,'Local SELinux boolean values.','The file contents and whether values are person-selected or installation defaults are absent; own-setting versus package-default coverage cannot be determined.','S8.2-11,S8.2-13,S8.2-17')
setrows(list(range(195,208))+[209,210],U,'SELinux policy module inputs, compiled policy cache, and language metadata.','Module source provenance, installation equality, and compilation lineage are missing; package coverage, default settings, and independently chosen policy cannot be distinguished.','S8.2-7,S8.2-13,S8.2-16,S8.2-17')
setrows([211],U,'System log files, log directories, and a documentation link.','Logs are records, but the README link target and installation provenance are not recorded; exact coverage for every member remains unresolved.','S8.2-7,S8.2-15')
setrows([212,213,214],R,'Persistent audit, journal, or service logs.','These files record service activity and events; persistence does not turn historical logs into settings or programs.','S8.2-15')
setrows(list(range(215,225)),R,'Persistent private temporary directories created for system services.','systemd creates these service working directories on persistent storage; they are program state, not separately chosen settings or executable payloads.','S8.2-5,S8.2-15')
# Remaining entries were individually inspected and contain directories only.
for i,r in enumerate(rows):
 if i in spec:continue
 m=json.loads(r['members']);ms=list(csv.DictReader(open(root/m['file']),delimiter='\t'))
 assert ms and all(x['type']=='directory' and x['persistence']=='persistent' for x in ms),(i,r['id'])
 setrows([i],U,'Persistent containing directories for accounts, applications, configuration, or project files.','Directory installation and creation provenance is not recorded; received package directories, program-created storage, and person-created material directories require different decisions.','S8.2-7,S8.2-15,S8.2-16')
assert len(spec)==225
with open(out,'a',newline='') as f:
 w=csv.DictWriter(f,fields,delimiter='\t',lineterminator='\n')
 with open('A3/c1/part-developer.individual.tsv','w',newline='') as af:
  aw=csv.DictWriter(af,fields,delimiter='\t',lineterminator='\n');aw.writeheader()
  for i,r in enumerate(rows):
   d,s,what,why=spec[i];m=json.loads(r['members'])
   assert len(what.split())<=15 and len(why.split())<=30,(i,why)
   b='raw:A3/in/raw/developer/'+m['file'] if 'file' in m else 'evidence'
   o=dict(zip(fields,[r['id'],d,s,what,b,why]));w.writerow(o);f.flush();aw.writerow(o);af.flush()
print(collections.Counter(v[0] for v in spec.values()))
