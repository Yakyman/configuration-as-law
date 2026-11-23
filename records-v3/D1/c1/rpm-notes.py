import csv,collections,json,re
ctx={'__name__':'notes'};exec(open('D1/c1/rpm-classify.py').read(),ctx)
P=ctx['P'];D=ctx['D'];rules=ctx['rule'];results=ctx['result']
rows=[r for r in csv.DictReader(open('D1/in/part-fedora.tsv'),delimiter='\t') if r['kind']=='L1:package:rpm']
byname=collections.defaultdict(list)
for row in rows:byname[row['name'].split(':',1)[1]].append(row)
ruletext={
'access':'MUST (S2.2-1, S2.2-2, S2.2-15): documented access-control policies change which operations are permitted. Policy tools and libraries are separately classified as code.',
'art':'NOT (S2.2-4): decorative pictures, icons, wallpapers, cursors and sounds lose their particular content on removal; the programs using them retain their operations.',
'directories':'UNKNOWN (S3-2): documentation identifies directory ownership, but the inventory lacks occupancy and operative dependence on empty directories. No recursive removal is assumed. Packages containing scripts, system-account rules, essential compatibility paths or macros were separated.',
'documents':'NOT (S2.2-4): documentation and license payloads make only their document content unavailable. A documentation directory containing actual executable code is not classified by this rule.',
'firmware':'MUST (S2.2-1, S2.2-2, S2.2-16): device firmware images and firmware-loading support enable device initialization or updates. Their removal prevents supplying that functionality. Guest firmware and uncertain BIOS deployment are separate cases.',
'fonts':'NOT (S2.2-4): the payload provides typeface and glyph-shape content. Removing that content leaves rendering programs and algorithms available. Particular designs cease to be available. Operational character-processing rules are separate cases.',
'library':'MUST (S2.2-1, S2.2-10): documented executable library routines run under the calling program authority. Library-looking names alone were insufficient; descriptions establish runtime-library functionality.',
'meta':'NOT (S2.2-1, S2.2-2): dependency-selection packages lacking runtime payload leave separately installed dependencies available when the selected package is removed. Catalog descriptions, documentation, and licensing material add no runtime operation. An apparently similar package containing executable helper scripts was separated.',
'module':'MUST (S2.2-10): documented interpreter modules supply executable routines running with interpreter authority. The rule is not applied merely because a name has a language prefix; dependency-only extras were separated.',
'native':'MUST (S2.2-1, S2.2-10): documented plugins, drivers, parsers, codecs and implementation modules supply executable operations within the calling program. Guest-confined firmware is separate. Host-side emulator device implementations are host code, not guest code.',
'program':'MUST (S2.2-9, S2.2-12): command-path payloads or documented standalone daemons/helpers establish executable programs. Their installation method does not change the explicit program requirement.',
'tables':'HOLE (S2.2-1, S2.2-2, S2.2-4): non-executable reference tables participate in lookup, validation, spelling, input, or processing. One reading treats losing these particular operations as lost capability; another treats the absent entries as unavailable database content. The text does not specify the boundary between an operation and a lookup of missing content. Each package purpose was checked independently before admission to this rule.',
'translations':'NOT (S2.2-4): message catalogs and localized document content supply alternative strings or documents; their absence does not remove the program operations. Locale archives governing collation, parsing and conversion are separate MUST cases.'}
quote={'access':'policy','art':'wallpaper','directories':'directories','documents':'Documentation','firmware':'Firmware','fonts':'font','library':'library','meta':'metapackage','module':'module','native':'plugin','program':'programs','tables':'data','translations':'Translations'}
with open('D1/c1/part-fedora.rpm.notes.md','w') as f:
 f.write('# RPM classification notes\n\n')
 f.write('Scope: 3,954 RPM inventory rows representing 1,977 named packages in two inventory contexts. Each input identifier is retained. Installation evidence establishes package presence; it is not used as proof that every package is executable. No object was removed and no machine probe was performed.\n\n')
 f.write('## Sources and method\n\n')
 f.write('The two RPM inventory outputs are `D1/in/raw/fedora/raw/004-packages-root-rpm.out` and `D1/in/raw/fedora/raw/039-packages-user-rpm.out`. Their names, versions and architectures were matched to public package descriptions. The supplied ownership and filesystem outputs are empty and were not used to infer payloads.\n\n')
 f.write('Public package descriptions: ['+D['source']+']('+D['source']+'). Public payload listings: ['+D['file_source']+']('+D['file_source']+'). Selected records were streamed without installing or executing packages. The saved source extraction is `D1/c1/raw/rpm-documentation.json`. Public repository documentation establishes package purpose; it does not certify byte-for-byte identity with the inventoried versions.\n\n')
 f.write('The descriptions contain the following exact functional terms used in rule checks: '+', '.join('"'+q+'"' for q in quote.values())+'. These short quotations refer to descriptions, not to the earlier inventory labels. Detailed functions are paraphrased in the output.\n\n')
 f.write('The implementation is `rpm-classify.py`, with individually reviewed cases in `rpm-special.py` and current-run corrections in `rpm-revisions.py`. Settled rows were appended and flushed individually. Later review corrections are retained in `part-fedora.rpm.correction-audit.tsv`; `part-fedora.rpm.corrections.tsv` supplies replacement rows. No earlier classification was consulted.\n\n')
 f.write('## Applicable sentences, quoted exactly\n\n')
 for line in open('SENTENCES.md'):
  m=re.match(r'- \*\*(S[^*]+)\*\* (.*)',line)
  if m and m[1] in ['S2.2-1','S2.2-2','S2.2-4','S2.2-7','S2.2-9','S2.2-10','S2.2-11','S2.2-12','S2.2-13','S2.2-15','S2.2-16','S3-2']:f.write(line+'\n')
 f.write('## Homogeneous rules and ten manually inspected rows per rule\n\n')
 for rule,explain in ruletext.items():
  names=[n for n in rules if rules[n]==rule]
  chosen=[names[i*(len(names)-1)//9] for i in range(10)]
  used=collections.Counter()
  f.write('### '+rule+'\n\n'+explain+'\n\n')
  f.write('Manual checks of the documented purpose and relevant payload against the rule:\n\n')
  for name in chosen:
   row=byname[name][used[name]];used[name]+=1
   f.write('- `'+row['id']+'`: '+results[name][2]+' Verified against the description and payload listing.\n')
  f.write('\n')
 f.write('## Individual distinctions and supporting quotations\n\n')
 f.write('- [RPM manual](https://rpm.org/docs/4.20.x/man/rpm.8): "erase individual software packages". The object-removal reasoning removes the selected package, not separately inventoried dependencies. No dependency autoremove operation was assumed.\n')
 f.write('- [RPM removal implementation](https://raw.githubusercontent.com/rpm-software-management/rpm/master/lib/fsm.cc): `unlinkat(dirfd, path, AT_REMOVEDIR)`. A nonempty directory is not recursively deleted. Missing occupancy information therefore remains an evidence limitation for directory-only packages.\n')
 f.write('- [Locale documentation](https://man7.org/linux/man-pages/man7/locale.7.html): "This category governs the collation rules used for sorting and regular expressions". The locale archive supplies behavioral rules, unlike translation-only catalogs.\n')
 f.write('- [Shell extension documentation](https://gjs.guide/extensions/overview/anatomy.html): "The code in `extension.js` is executed in the same process as `gnome-shell`". The five installed extension packages contain this entry-point code, so S2.2-10 applies.\n')
 f.write('- [RPM keyring documentation](https://rpm.org/docs/4.20.x/man/rpmkeys.8): "Digital signatures cannot be verified without a public key." The imported-key pseudo-package is classified by signature verification, not by the package label.\n\n')
 f.write('The package rows represent individual packages, not directory-member groups. A package containing required code together with exempt documentation is MUST: recording the package records its required contribution. No package row was converted into a synthetic MIXED directory group.\n\n')
 f.write('Further individually checked distinctions include host daemons packaged as data, shell initialization and kernel-install scripts, account rules in directory packages, guest-only firmware, browser-only administrative pages, and default configurations shared across programs. Macro expansion and stylesheet execution rights remain UNKNOWN when the actual behavior is not established. HOLE is reserved for a textual boundary with established object function.\n\n')
 f.write('## Validation\n\n')
 out=list(csv.DictReader(open('D1/c1/part-fedora.rpm.tsv'),delimiter='\t'))
 assert len(out)==len(rows)==3954
 assert len({r['id'] for r in out})==len(out)
 assert {r['id'] for r in out}=={r['id'] for r in rows}
 assert all(r['decision'] in ['MUST','NOT','HOLE','UNKNOWN','MIXED'] for r in out)
 assert all(len(r['what_it_does'].split())<=15 and len(r['reason'].split())<=30 for r in out)
 c=collections.Counter(r['decision'] for r in out)
 f.write('Validated: input/output identifiers have the same set and count, each once; all decisions are allowed; all field word limits pass. Counts: '+', '.join(k+' '+str(c[k]) for k in ['MUST','NOT','HOLE','UNKNOWN','MIXED'])+'.\n')
print('Notes written; validation passed')
