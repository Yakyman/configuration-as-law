import csv,json,collections,random,pathlib
csv.field_size_limit(10000000)
base=pathlib.Path('D1/in/raw/alma')
rows=[r for r in csv.DictReader(open('D1/in/part-alma.tsv'),delimiter='\t') if r['kind']=='L1:package']
out=pathlib.Path('D1/c1/part-alma.tsv')
header=['id','decision','sentences','what_it_does','basis','reason']
existing={r['id'] for r in csv.DictReader(out.open(),delimiter='\t')} if out.exists() else set()
# Provenance facts refer to package entities; individual files require their own integrity join.
groups=collections.defaultdict(list)
with out.open('a') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 if not existing:w.writerow(header)
 for r in rows:
  m=json.loads(r['members']); mgr=m['manager']; reason=m['reason']; native=m.get('native_package_ids',[])
  basis='raw:D1/in/raw/alma/objects.tsv'; s='S8.1-6,S8.2-7,S8.2-8,S8.2-16'; what=f'Installed {mgr} package managed as a distribution unit.'
  if native:
   rule='package-native-provenance'; decision='INSTALLED-PACKAGE'
   why='Installed distribution obtained with the native package identified by its metadata ownership; that package line covers it regardless of language-manager reason.'
  elif mgr=='python' and reason=='unknown':
   rule='python-transaction'; decision='INSTALLED-DERIVED'; basis='raw:D1/in/control/alma/actions-logs/browser_extension.log'
   why='The retained pip transaction names this distribution as a marionette_driver dependency; its source package line covers the installation.'
  elif reason=='explicit':
   rule='package-reason'; decision='INSTALLED-OWN'; why='Installed package explicitly requested; no containing package or dependency source is identified, so it requires its own line.'
  elif reason=='dependency':
   rule='package-reason'; decision='INSTALLED-DERIVED'; why='Installed package has retained dependency provenance; the line of the package requiring it covers it.'
  else:
   rule='package-reason'; decision='UNKNOWN'; why='Package installation is established, but explicit versus dependency provenance is unknown; choosing its own versus a source package line requires that fact.'
  groups[rule].append((r,decision))
  if r['id'] not in existing:
   w.writerow([r['id'],decision,s,what,basis,why]); f.flush()
notes=pathlib.Path('D1/c1/part-alma.notes.md')
with notes.open('w') as f:
 f.write('# Classification c1: alma\n\nScope: the supplied alma inventory only. No other classification was consulted. Results are appended by id; independent partitions are merged after completion.\n\n')
 f.write('## Package rules\n\nThe object in an L1 package row is the installed distribution unit, not its metadata file. An installed package satisfies the first half of S8.2-7 even if a constituent file changes. A native metadata owner establishes the distribution provenance given in the collector; its installation reason is not transferred to the language package. Individual stored files are decided separately and require installation-integrity facts.\n\n')
 f.write('**package-reason:** For packages without native enclosing-package provenance, apply S8.2-7 and S8.2-8 first. Under S8.2-16, explicit installation needs its own line; retained dependency provenance uses the source line. Unknown installation reason gives UNKNOWN because own and derived lines differ. No historical intent is inferred from a package name, group selection, directory nesting, or absence of REQUESTED. Flatpak reason values are used as supplied, including their stated app/runtime interpretation.\n\n')
 f.write('**package-native-provenance:** An installed language distribution with retained native_package_ids is obtained with the identified native package, and S8.2-16 permits its package line. This does not transfer the native package installation reason. For the 195 npm distributions, additionally checked every observed non-directory descendant against the native manifest: all are unchanged files owned by nodejs-npm. For Python, the package entity is identified by the native-owned installed-distribution metadata; no rule of directory containment is applied to separate file objects.\n\n')
 f.write('**python-transaction:** The sixteen local Python distributions with unknown stored reason are explicitly named as dependencies in the retained pip transaction in D1/in/control/alma/actions-logs/browser_extension.log. Its Collecting lines identify their parent dependencies and Successfully installed confirms installation. S8.2-16 therefore selects INSTALLED-DERIVED. The distro row has a misleading collected display name; its directory, version and transaction identify distro 1.9.0.\n\n')
 # Include exact supplied sentences, not paraphrased substitute definitions.
 lines=pathlib.Path('SENTENCES.md').read_text().splitlines()
 for key in ['S8.1-6','S8.2-6','S8.2-7','S8.2-8','S8.2-16']:
  f.write(next(l for l in lines if f'**{key}**' in l)+'\n\n')
 f.write('## Public documentation\n\nhttps://packaging.python.org/en/latest/specifications/recording-installed-packages/ — “This document specifies a common format of recording information about Python projects installed in an environment.” Installed-distribution metadata also supports integration by system package managers.\n\nhttps://peps.python.org/pep-0376/ — “the presence of this file indicates that the project installation was explicitly requested (i.e., not installed as a dependency).” This describes REQUESTED; the retained inventory reason remains authoritative where unknown.\n\nhttps://docs.npmjs.com/cli/v10/configuring-npm/folders/ — “Packages are dropped into the `node_modules` folder under the `prefix`.” Directory structure establishes package layout, not historical installation reason.\n\n')
 f.write('## Manual package-rule checks\n\nEach listed row was inspected with its retained manager, reason, provenance and/or transaction entry before applying the rule.\n\n')
 for rule,vals in groups.items():
  if rule=='package-reason':
   ids=['alma-e7c6fc3e717bdc39acbe0e65','alma-d15afe8d066344657cce9f0e','alma-6494449f525eb29a533ddefb','alma-77ccb9a9685c546ff4b596ea','alma-4426938d9cfaf66a2d7f76ac','alma-fae4303fc7ec8aa0b6457dcc','alma-84f4a95a340da8476f366e48','alma-fd960653df1f48027cf22150','alma-aa07c56096e3c04d8b47f08b','alma-1de7785d06643decb0c982c5']
  elif rule=='package-native-provenance':
   ids=['alma-5781f1c5e748b32ec6bd2bfd','alma-8785c4d0afae73edf6ff40d6','alma-7c534288e3b1770ca609b28a','alma-2545403355ad142b45a00324','alma-c208634804bba39ca48e3228','alma-912cb46ce54333de07fa3bd7','alma-9c23ebcd29c06347fc2c9da3','alma-1f13e5d5fde8f28562017c50','alma-f49733d837fa2b7abe12b867','alma-f620e45c5f534d79f98b0a79']
  else:ids=['alma-317678ed0ffc7c1ad32d2df1','alma-b321ebb1d8d25e3ff86b1922','alma-5e792ad7daa2de59dfabb7dd','alma-82505a705d69df249b2672db','alma-0faeaaa180720d4201db3105','alma-2478b390d4b644352dc24f74','alma-325919992f6861836a62dbc6','alma-afbb55e45941dbf71aea7846','alma-69424af0c27db54b28852bb0','alma-c9bb0ec522288aabf4ffe0fd']
  f.write(f'### {rule}\n\n')
  for rid in ids:
   r,d=next(v for v in vals if v[0]['id']==rid);m=json.loads(r['members']); name=r['name'].split('@')[0]
   f.write(f'- {rid}: {name}; retained reason {m["reason"]}; decision {d}. '+('Native metadata provenance inspected.' if m.get('native_package_ids') else 'Reason/transaction evidence inspected.')+'\n')
  f.write('\n')
print(collections.Counter(r['decision'] for r in csv.DictReader(out.open(),delimiter='\t')))
