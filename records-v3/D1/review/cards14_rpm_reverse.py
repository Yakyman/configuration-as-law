import json,re
for machine,fn in [('fedora','D1/adjudication/work/A/deps-A.json'),('tumbleweed','D1/review/cards14-raw/tw-primary-selected.json')]:
 d=json.load(open(fn));no=[]
 for n in ['gnulib-l10n','ncurses-base','poppler-data','adwaita-cursor-theme','fedora-logos','qt6-qttranslations','breeze6-cursors','hicolor-icon-theme','distribution-logos-openSUSE-Tumbleweed']:
  if n not in d:continue
  users=[]
  for p,v in d.items():
   rr=v.get('req',[]) if machine=='fedora' else [q['name'] for q in v.get('requires',[])]
   if n in rr:users.append(p)
  print(machine,n,users)
