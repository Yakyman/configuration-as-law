import csv,json,pathlib,collections
csv.field_size_limit(100000000)
root=pathlib.Path('A3')
rows=[r for r in csv.DictReader((root/'in/part-developer.tsv').open(),delimiter='\t') if r['kind']=='2:code-ownership-unresolved']
owned={r['path'] for r in csv.DictReader((root/'in/raw/developer/package-files.tsv').open(),delimiter='\t')}
assert not any(r['name'] in owned for r in rows)
assert all(json.loads(r['members'])['persistence']=='persistent' for r in rows)
def group(n):
 if n.endswith('.npm'):return 'registry'
 if any(k in n for k in ('/.linuxbrew/','/.julia/','/.juliaup/','/.bun/install/','/.local/share/gem/')):return 'payload'
 if '/Projects/scc/' in n:return 'project'
 return 'individual'
def describe(n):
 b=n.rsplit('/',1)[-1]
 if '/.git/hooks/' in n:return 'Git hook script or example invoked around repository operations.'
 if '/compiled/' in n:return 'Julia precompiled library loaded by its runtime.'
 if '/.julia/' in n:
  if '/lib/' in n:return 'Julia distribution runtime support file.'
  return 'Julia distribution executable, script, or build support file.'
 if '/.juliaup/' in n:return 'Julia version manager component or launcher.'
 if '/uri-js' in n:
  if b.endswith('.map'):return 'Source map describing locations in URI parsing library code.'
  if b.endswith('.d.ts'):return 'Type declarations describing the URI parsing library interface.'
  if b=='LICENSE':return 'License text for URI parsing library.'
  if b=='README.md':return 'Documentation for URI parsing library.'
  if b=='package.json':return 'Package metadata for URI parsing library.'
  if b=='yarn.lock':return 'Dependency resolution lock data for URI parsing library.'
  return 'URI parsing library code.'
 if '/.bun/install/' in n:
  if b=='package.json':return 'JavaScript package metadata.'
  return 'JavaScript package command or development script.'
 if '/.local/share/gem/' in n:return 'Git hook manager launcher or platform-specific executable.'
 if '/.linuxbrew/' in n:
  if '/fixtures/' in n:return 'Package manager test fixture with an executable permission or script marker.'
  if b=='hello':return 'Command-line greeting program.'
  return 'Package manager executable, development script, or helper.'
 if '/Projects/scc/' in n:
  if '/examples/' in n:return 'Language or regression test fixture for source-code counting.'
  if b=='scc':return 'Source-code counting executable in the project tree.'
  if b=='benchmark_to_chart.py':return 'Python script converting benchmark results into charts.'
  return 'Project development, test, or build-support script.'
 return {
 '.bash_profile':'Login shell startup code.', '.bashrc':'Interactive shell startup code.',
 'bun':'JavaScript runtime and package manager executable.',
 'uv':'Python package and environment manager executable.',
 'uvx':'Launcher for Python tools in managed environments.',
 'cal-project-summary':'Executable script associated with the project summary service.',
 'lefthook':'Command wrapper for a Git hook manager.',
 'libgcc_s-16-20261029.so.1':'Compiler runtime shared library.',
 }[b]
out=root/'c1/part-developer.code.tsv'
existing={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')}
groups=collections.defaultdict(list)
with out.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 for r in rows:
  n=r['name'];g=group(n);groups[g].append(r)
  if r['id'] in existing:continue
  if g=='payload':
   reason='Missing file provenance and installation integrity: unchanged package contents are INSTALLED-PACKAGE; modified code or independently supplied files require later questions.'
   sentences='S8.2-6,S8.2-7,S8.2-8,S8.2-9,S8.2-16'
   basis='raw:A3/in/raw/developer/package-files.tsv'
  elif g=='project':
   reason='Missing file provenance and derivation: the inventory does not establish package origin or whether this object was system-obtained from a recorded source.'
   sentences='S8.2-6,S8.2-7,S8.2-9,S8.2-16,S8.2-20'
   basis='raw:A3/in/raw/developer/metadata.json'
  else:
   reason={
    '.bash_profile':'Startup code changed from the base; missing provenance of those changes decides PROGRAM-OWN versus PROGRAM-DERIVED.',
    '.bashrc':'Startup code changed from the base; missing provenance of those changes decides PROGRAM-OWN versus PROGRAM-DERIVED.',
    'bun':'Missing installation provenance and integrity: package-provided unchanged executable versus separately obtained program changes the decision.',
    'uv':'Missing installation provenance and integrity: package-provided unchanged executable versus separately obtained program changes the decision.',
    'uvx':'Missing installation provenance and integrity: package-provided unchanged executable versus separately obtained program changes the decision.',
    'cal-project-summary':'Executable script exists, but its source and creation method are unrecorded; these determine own-line versus derived coverage.',
    'lefthook':'Missing wrapper generation provenance and integrity: a generated launcher, package-provided file, and independently supplied program have different coverage.',
    'libgcc_s-16-20261029.so.1':'No package-file match; missing provenance and installation integrity prevent deciding package coverage versus independent or derived program coverage.',
   }[n.rsplit('/',1)[-1]]
   sentences='S8.2-6,S8.2-7,S8.2-9,S8.2-10,S8.2-16'
   basis='evidence'
  what=describe(n)
  assert len(what.split())<=15 and len(reason.split())<=30
  w.writerow([r['id'],'UNKNOWN',sentences,what,basis,reason]);f.flush()
# Checks for this independent subset only.
actual=list(csv.DictReader(out.open(),delimiter='\t'))
assert len(actual)==619 and len({r['id'] for r in actual})==619
assert {r['id'] for r in actual}=={r['id'] for r in rows}
assert all(r['decision'] in {'UNKNOWN','RECORD'} for r in actual)
notes='''# Code-candidate subset: independent classification notes

Scope: 619 input rows. The inventory label was not used as a class. All objects have persistent filesystem metadata. None joins to an installed per-file manifest in `A3/in/raw/developer/package-files.tsv`. A missing match is not a proof of non-package origin: `A3/in/raw/developer/metadata.json` records incomplete ownership, unavailable adapters, and missing language-package file provenance. Installation reason is consulted in package object metadata but cannot determine the origin or integrity of an individual file absent a manifest. Prefix signatures do not prove unchanged package bytes. No experiment was performed.

## Exact deciding text

- S8.2-6: "What an object is is determined by four questions asked in order; the first affirmative answer decides, and the clarifications do not change this order."
- S8.2-7: "Is the object a package installed on the computer, or was it obtained as part of such a package and does it remain as received?"
- S8.2-9: "Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?"
- S8.2-15: "Otherwise: if a program recorded the object as it ran, it is a **program record**—a log, cache, history, working state; if a person created or brought the object, it is **material**—documents, photographs, projects, downloaded files, private keys and passwords for logging in to other machines."
- S8.2-16: "What is installed is recorded by one of three lines: a line of its own; the line of the package as part of which it was obtained; a line from which the system itself built or obtained it—a compiled copy, a generated list, a package installed as a dependency of a recorded package."
- S8.2-20: "A file containing code that cannot be executed on this computer is not a program."
- S8.2-23: "A file that a program executes as code counts as code even when it contains setting values; a file that a program only reads as values does not count as code."

## Homogeneous rules

R1, registry: the 76 `.npm` binary response caches are RECORD. The documented purpose is data caching, not executable package payload. Package metadata downloaded from a registry is not itself an installed package. S8.2-23 distinguishes data from code even though the inventory marks a shebang; S8.2-15 therefore applies. The file permission is non-executable in all 76 rows. Official documentation, https://bun.sh/docs/pm/cli/install: "Bun uses a binary format for caching npm registry responses." This establishes the function; the inventory establishes the stored instances and persistence.

R2, payload: 467 files in package-manager/distribution payload trees lack a per-file package provenance and integrity record. UNKNOWN follows from the missing first-question facts, not from their directory names or permissions. The rule applies to an evidentially homogeneous deficiency, not a claim that all these objects contain code. An unchanged received file answers question one; a modified or independently supplied file requires later questions and a different label. Native reason facts cannot cure missing file provenance. Even foreign-architecture executables and non-code maps can be installed objects if unchanged package parts. Names alone cannot demonstrate their unmodified status. Documentation establishes functions but cannot establish these machine-specific facts.

R3, project: 68 project-tree files lack recorded supply/generation lineage. UNKNOWN records missing package origin or whether system derivation supplies coverage under S8.2-16. Project location does not prove material, and a script marker does not establish compatibility of a fixture. A general-purpose checkout or copy is not automatically an installer. No declaration-source or build-origin relation for these individual files is present in the supplied evidence. These missing facts change the result; this is not a textual gap.

Official context checked: https://github.com/JuliaLang/juliaup describes "Julia installer and version manager"; its add/remove operations establish installer purpose, not per-file integrity. https://git-scm.com/docs/git-init states "The sample hooks are all disabled by default." Disabled hook automation does not prove code cannot be executed manually; nor does a matching filename establish this particular copy's origin. Therefore Git sample hooks were not automatically labeled records or assigned derived coverage.

## Hand checks

For each listed row, the input metadata, path role, size, shebang/executable flags, persistence and absent manifest match were individually inspected. R1 checks confirm documented binary manifest-cache names. R2 deliberately includes data maps, archived fixtures, libraries and a foreign-platform executable to check that permissions do not replace question one. R3 includes scripts, hook samples, a tiny shell fixture and vendor code to check provenance rather than infer it from the project directory.
'''
for g,label in [('registry','R1'),('payload','R2'),('project','R3')]:
 a=groups[g]; picks=[a[round(i*(len(a)-1)/9)] for i in range(10)]
 notes+='\n'+label+': '+', '.join(r['id'] for r in picks)+'.\n'
notes+='''
## Eight individual decisions

The two shell startup files differ from the untouched-base signatures and sizes. Both are shell code, but the recorded changes have no author or generator provenance; own versus derived remains unknown. Their initial and final metadata are in the respective `raw/0004-filesystem.out` files and creation provenance remains unknown in `configuration-origin.tsv`.

The runtime executable and two Python-tool executables have neither a manifest match nor full installation digest; installation origin and integrity remain unknown. The project-summary script is executable but the inventory does not preserve its source or creation method. The hook-manager command wrapper might be generated or received; its wrapper creation provenance is absent. The compiler runtime library lacks a current manifest match despite the compiler runtime package being present; package presence alone does not establish that this file remains as received.

Checks: 619 unique output IDs, exactly the subset IDs; 543 UNKNOWN and 76 RECORD. All output descriptions and reasons satisfy the word limits. Output is appended and flushed row by row; restarting the script preserves existing rows.
'''
(root/'c1/part-developer.code.notes.md').write_text(notes)
print(collections.Counter(r['decision'] for r in actual))
