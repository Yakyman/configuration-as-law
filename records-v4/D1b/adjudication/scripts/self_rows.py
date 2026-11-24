import csv,sys
csv.field_size_limit(sys.maxsize)
rows=list(csv.DictReader(open('D1b/compare/to-adjudicate.tsv'),delimiter='\t',quoting=csv.QUOTE_NONE))
Q16="a line from which the system itself built or obtained it"
Q15="if a program recorded the object as it ran, it is a program record […] if a person created or brought the object, it is material"
Q11="Is the object a value chosen by a person that the computer as a whole obeys, rather than only a program that a person runs for himself or herself?"
Q9="Is the object code that the computer executes or can execute: on its own, at a person’s command, or through another program with that program’s rights?"
out=[]
PROFILE={'d1b-gentoo-d4bcdd8be82152fedbb1c210','d1b-gentoo-ce3e687674d6e09c0b0c80b6'}
for r in rows:
    nm=r['name']; c2=r['c2_decision']
    if nm.startswith('/var/db/pkg/'):
        out.append([r['id'],'RESOLVED:MIXED','S8.2-15;S8.2-9;S8.2-16',
          "if a program recorded the object as it ran, it is a program record […] "+Q9+" […] "+Q16,'c1','-',
          'Portage install database: metadata files RECORD; saved .ebuild and environment.bz2, executed at unmerge (bugs.gentoo.org/211833), PROGRAM-DERIVED from package line. c1 misread fact (acquisition is Portage merge).'])
    elif nm.startswith('/var/db/repos/gentoo/'):
        if r['id'] in PROFILE:
            out.append([r['id'],'UNKNOWN','S8.2-11',Q11,'c2','-',
              'Profile values are settings only if obeyed; selected profile chain unrecorded (make.profile target and parent files not read). c2 assumed membership in the chain.'])
            continue
        if c2=='PROGRAM-DERIVED':
            sid,q='S8.2-16',Q16
            n='Code in repository tree: program. Own vs derived line depends on unrecorded acquisition of the tree (Portage sync vs placed by a person); c2 assumed the sync.'
        elif c2=='GAP-TWO':
            sid,q='S8.2-15',Q15
            n='Non-code repository data: record vs material depends on unrecorded acquisition of the tree (Portage sync vs placed by a person); c2 assumed the sync.'
        else:
            sid,q='S8.2-16;S8.2-15',Q16+" […] "+Q15
            n='Members: code (own vs derived line) and data (record vs material) both depend on unrecorded acquisition of the repository tree; c2 assumed Portage sync.'
        out.append([r['id'],'UNKNOWN',sid,q,'c2','-',n])
with open('D1b/adjudication/raw/out-SELF.tsv','w') as f:
    f.write('id\tverdict\tsentence_id\tquote\terred\tgap_label\tgap_text\tnote\n')
    for o in out:
        o=o[:5]+['-','-']+[o[6]] if len(o)==7 else o
        assert all('\t' not in x and '\n' not in x for x in o)
        f.write('\t'.join(o)+'\n')
print(len(out))
