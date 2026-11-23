import json
for m,fn in [('fedora','D1/adjudication/work/A/deps-A.json'),('tumbleweed','D1/review/cards14-raw/tw-primary-selected.json')]:
 d=json.load(open(fn));installed={l.split('\t')[0] for l in open('D1/in/raw/'+m+'/raw/004-packages-root-rpm.out') if '\t' in l}
 for n in ['qt6-qttranslations','desktop-translations','kImageAnnotator-lang','libksane-lang','libqt5-qttranslations','libstorage-ng-lang','ocean-sound-theme6','openal-soft-data','publicsuffix','qt6-translations','snapper-lang','poppler-data']:
  if n not in d:continue
  users=[]
  for p,v in d.items():
   if p not in installed:continue
   rr=v.get('rec',[]) if m=='fedora' else [q['name'] for q in v.get('recommends',[])]
   if n in rr:users.append(p)
  print(m,n,users)
