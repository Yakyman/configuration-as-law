import csv,json,pathlib,collections,re
b=pathlib.Path('D1b/c1')
def read(p):return list(csv.DictReader(open(p),delimiter='\t'))
inputs={r['id']:r for r in read('D1b/in/part-gentoo.tsv')}
led=read(b/'gentoo-member-decisions.tsv')
checks=json.load(open(b/'gentoo-group-manual-checks.json'))
restchecks=json.load(open(b/'gentoo-rest-manual-checks.json'))
# Exact rows checked in the preceding manual inspection are retained; updated direct-directory branches are separately noted.
text='''# Gentoo c1 classification notes

2026-11-23 UTC.

The work used COMMON.md, the fixed definition and numbered sentences, this part's input, FACTS.md and the Gentoo handoff. No other classification, rehearsal output, adjudication or earlier-night records were used. The current classification did not participate in supplement step 4 parts 1–3. Current parallel shards were combined only within c1.

The table contains direct member objects listed by each group, not an inferred recursive expansion. Every named member TSV was completely parsed and its row count checked against `members.count`; all were complete. A directory's search bit is not executable program code. Its separately inventoried contents do not substitute for the directory object. All package-file entries were read, as were package reasons, creation-origin facts, persistence and the raw filesystem scan. The full-digest table supplies observations, not an original reference or a historical creator. Missing factual predicates yield UNKNOWN, not a textual gap.

The two parallel parts are documented in `part-gentoo.1.notes.md` and `part-gentoo.2.notes.md`; their rules and hand checks are incorporated below. Group code is in `gentoo-groups.py` and `gentoo-groups-rest.py`. `gentoo-refine.py` records the pre-freeze clarification of direct directories and runtime parent names. All decisions were written incrementally; only these explanations and direct-directory interpretations were refined before the completed table was verified and frozen. There was no pre-existing output from an earlier attempt.

## Literal deciding text

'''
sentences=pathlib.Path('SENTENCES.md').read_text()
for line in sentences.splitlines():
 if re.search(r'S8\.2-(?:[1-9]|1[0-9]|2[0-3])\*\*',line):text+=line+'\n\n'
text+='''## Evidence joins

`raw:D1b/handoff/gentoo/...` in the table is a handoff evidence path, not the forbidden inventory original. Groups cite their complete member tables. Package coverage is joined by exact path after resolving only five observed directory aliases from `raw/0004-filesystem.out`: `/bin` and `/sbin` to `/usr/bin`, `/lib` to `/usr/lib`, `/lib64` to `/usr/lib64`, and `/usr/sbin` to `/usr/bin`. The actual symlink targets are respectively `usr/bin`, `usr/bin`, `usr/lib`, `usr/lib64`, and `bin`. No basename or digest matching substitutes for provenance. For every INSTALLED-PACKAGE result, an unchanged package-files.tsv comparison is required. Unknown package installation reason does not invalidate coverage of a component by that package's line.

The supplied package-file comparison does not compare unlisted directory nodes with originally installed metadata. Such nodes remain UNKNOWN unless their documented role establishes program-created working state. A timestamp, location or prefix signature is not treated as a creation event. `configuration-origin.tsv` has unknown origins for the inspected settings; this prevents assuming a personal choice or an installation default.

`gentoo-member-decisions.tsv` gives exact member partitions for the 901 remaining groups, including every MIXED row with a long partition. The 125 homogeneous kernel MIXED groups have the simpler exhaustive partition stated directly in their reasons: all regular files are unchanged package members; every directory has unrecorded provenance. The 861 homogeneous file-only groups have all members unchanged. A group with only UNKNOWN members is UNKNOWN, not MIXED merely because the possible underlying classes differ.

## Public documentation and factual limits

- [Gentoo ebuild format](https://devmanual.gentoo.org/ebuild-writing/file-format/index.html): “An ebuild is a `bash` script which is executed within a special environment.” This establishes executable recipes, not their historical acquisition on this machine.
- [Gentoo repository layout](https://devmanual.gentoo.org/general-concepts/tree/index.html): identifies ebuilds, manifests, patches, metadata, profiles and directories. Repository data has no installation/reference comparison or acquisition history in this handoff. Code may require its own or a source line; noncode may be a program record or material. A repository name does not decide that missing fact.
- [Portage configuration reference](https://dev.gentoo.org/~zmedico/portage/doc/man/portage.5.html): `/var/db/pkg/` is a “database to track installed packages”; `/var/cache/edb/` contains “misc internal cache files”. VDB directories, local counters, installed CONTENTS and consolidated metadata are written bookkeeping. Other receipt fields can originate in binary-package metadata or local build output; neither original-copy comparisons nor a causal source-line record is supplied.
- [Portage database implementation](https://github.com/gentoo/portage/blob/master/lib/portage/dbapi/vartree.py): counter writing and database metadata handling establish local bookkeeping roles. This source's descriptions do not establish this machine's historical acquisition of every receipt.
- [Portage ebuild executor](https://github.com/gentoo/portage/blob/master/bin/ebuild.sh): it sources the saved environment. [Portage API](https://dev.gentoo.org/~zmedico/portage/doc/api/portage.package.ebuild.doebuild.html) describes extraction of `environment.bz2`. Consequently executable receipt content cannot simply be called a record by its database location.
- [pip caching](https://pip.pypa.io/en/stable/topics/caching/): “This cache functions like a web browser cache.” The documentation identifies HTTP response storage and locally built wheels. Metadata and cache directories are RECORD; opaque bodies/wheels lack the content needed to decide executable code. A wheel can contain importable code; a response body can instead be noncode data. The observed hash alone does not choose.
- [Python zipimport](https://docs.python.org/3/library/zipimport.html) documents imports from ZIP archives. [Python modules](https://docs.python.org/3/tutorial/modules.html#compiled-python-files) documents compiled-module caching. A `__pycache__` directory is bookkeeping, not the bytecode stored inside it.
- [Firefox HTTP cache](https://firefox-source-docs.mozilla.org/networking/cache2/doc.html): entry files store responses. [JavaScript startup bytecode cache](https://blog.mozilla.org/javascript/2017/12/12/javascript-startup-bytecode-cache/) establishes that a browser cache can contain code. Opaque payloads therefore cannot receive RECORD solely from their path. Browser profiles and telemetry bookkeeping are distinct from launch/access preferences and unread databases.
- [Firefox profiles](https://github.com/mozilla-firefox/firefox-dev/blob/main/toolkit/profile/docs/index.md) describes profile directory and selection bookkeeping. A stored directory itself is separated from its unread descendants.
- [Hardware database](https://www.freedesktop.org/software/systemd/man/262/hwdb.html) describes compilation into `hwdb.bin`; [iconvconfig](https://man7.org/linux/man-pages/man8/iconvconfig.8.html) describes the conversion-module configuration cache. These generated noncode lookup caches are records when no package comparison or chosen setting value is established by the inventory.
- [GNU Texinfo](https://www.gnu.org/s/texinfo/manual/texinfo/texinfo.pdf) describes install-info updating the top-level `dir` index. These are program-written lookup indexes.

Documentation establishes program behavior and object purpose, not an unrecorded historical event. It does not turn UNKNOWN into a gap. Section 8.5 mechanisms and declaration design are outside the classification.

## Homogeneous group rules and hand checks

Each rule applies only after member lists, persistence and package comparisons are inspected. The four questions remain in order. Below are the ten manually checked rows per rule; if a branch has fewer than ten applicable rows, all its applicable rows are checked. No additional test objects were introduced.

'''
rulewords={
'repository-provenance':('S8.2-7,S8.2-9,S8.2-15,S8.2-16','Persistent repository entries have no package comparison or historical acquisition/source-line record. Record UNKNOWN; this is a factual distinction between system acquisition and personally supplied entries, for both code and noncode.'),
'unchanged-package-members':('S8.2-6,S8.2-7,S8.2-8,S8.2-16','Every member has an unchanged package comparison after observed alias resolution. The first question decides INSTALLED-PACKAGE, even for executable modules.'),
'package-files-and-unverified-directories':('S8.2-7,S8.2-8,S8.2-15,S8.2-16','Every regular file has an unchanged package comparison; directory nodes have no original metadata/creator record. MIXED partitions files as INSTALLED-PACKAGE and directories as UNKNOWN.'),
'unverified-module-directories':('S8.2-7,S8.2-15','All direct members are persistent directory nodes without original directory metadata or creator history. UNKNOWN; no executable meaning is assigned to directory search permission.')}
for rule,ids in checks.items():
 s,why=rulewords[rule];text+=f'### {rule}\n\n{s}. {why}\n\n'
 for i in ids:text+=f'- `{i}` — `{inputs[i]["name"]}`. Full direct-member type and persistence pattern checked; original package comparison presence/absence checked.\n'
 text+='\n'
for rule,ids in restchecks.items():
 examples=[a for a in led if a['rule']==rule]
 text+=f'### Member branch: {rule}\n\n'
 if examples:
  text+='S8.2-6 determines precedence; S8.2-7/8 and S8.2-16 cover unchanged package members; S8.2-9/10/23 cover code; S8.2-11/13/14/17 cover settings; S8.2-15 covers records/material; S8.2-5 covers transient members. '
  text+=examples[0]['reason']+' The script predicate restricts this branch to the documented object role or the named missing fact.\n\n'
 for i in ids:text+=f'- `{i}` — `{inputs[i]["name"]}`. Member role, listed type, persistence and applicable evidence checked.\n'
 text+='\n'
text+='''## Individual groups and finalization

All remaining groups were inspected by their listed members. The per-member ledger records each member's concrete reason rather than substituting the inventory's class-like `kind` label. Boot files lack reference/source lineage; configuration values lack historical default provenance; persistent FIFOs and temporary files are not called runtime merely by name. Long groups in command/library directories are partitioned by actual package comparison, not by directory name.

Before freeze, eight direct-directory interpretations were clarified: the directory member `docker` in the parent library-state group was not recursively replaced by the separately classified store; browser storage directory entries were classified as working-state records rather than as their unread database descendants. Runtime explanations were expanded to identify parents and use INSTALLED-PACKAGE for executables with unchanged comparisons. Unknown boot/session creators are explicitly retained, because any possible parent leaves their runtime lifetime unchanged. These refinements precede the final full-table verification and meaning answers.

'''
for fn in ['part-gentoo.1.notes.md','part-gentoo.2.notes.md']:
 text+=f'## Incorporated current shard notes: {fn}\n\n'+(b/fn).read_text()+'\n'
(b/'part-gentoo.notes.md').write_text(text)
print('Notes written',len(text),'characters')
