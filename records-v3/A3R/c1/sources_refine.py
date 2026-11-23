import csv,pathlib,collections
p=pathlib.Path('A3R/c1/part-1.sources.tsv');r=list(csv.DictReader(p.open(),delimiter='\t'));h=list(r[0]);by={x['id']:x for x in r}
x=by['826005acd8710563f57cf817'];x['decision']='MIXED';x['reason']='MUST: CMakeLists.txt executes CMake language commands. HOLE: C sources and .cmake.in templates are compiler/generator inputs; text does not settle their content-versus-capability boundary.';x['basis']='doc:https://cmake.org/cmake/help/latest/manual/cmake-language.7.html'
x=by['lived-t8e6e523d56'];x['reason']='MUST: CMake language scripts. NOT: README/license/manual/test data. HOLE: compiled-language sources and other build templates; compiler input and indirect execution descriptions lack a settled boundary.'
x=by['387345094555f5064258cb03'];x['reason']='MUST: configure, CMake code, executables and shared library. NOT: documents/logs. HOLE: C sources, build templates and intermediates; compiler-input and regenerable-code boundaries remain unspecified.'
x=by['lived-t9f3f66bacf'];x['reason']='The checkpoint records past observation but detects inconsistent database history; history exemption and behavioral dependency requirement conflict without precedence.';x['basis']='doc:https://raw.githubusercontent.com/golang/go/master/src/cmd/vendor/golang.org/x/mod/sumdb/client.go'
for x in r:
 assert len(x['reason'].split())<=30 and len(x['what_it_does'].split())<=15
with p.open('w') as f:
 w=csv.DictWriter(f,fieldnames=h,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(r)
print(collections.Counter(x['decision'] for x in r))
