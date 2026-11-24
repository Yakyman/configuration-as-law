#!/usr/bin/env python3
import importlib.util
import pathlib
spec=importlib.util.spec_from_file_location('matcher',pathlib.Path(__file__).resolve().parents[1]/'collector/match.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def obj(ident,kind,name):return (ident,'alma',kind,name)
a=obj('a','L2:stored-ownership-unresolved','/group')
b=obj('b',a[2],a[3])
assert m.match_rows([a],[b])[0][0][:2]==['a','b']
assert m.match_rows([a],[b,obj('c',a[2],a[3])])[1][0][4]=='ambiguous-new-key'
assert m.match_rows([a,obj('a2',a[2],a[3])],[b])[0]==[]
assert not m.match_rows([a],[obj('b','L2:stored-outside-packages','/group')])[0]
assert not m.match_rows([obj('a',a[2],'/lib/modules/1.2')],[obj('b',a[2],'/lib/modules/1.3')])[0]
u1='<REDACTED>';u2='<REDACTED>'
a=obj('a','L1:saved-network','eth:'+u1+':ethernet:eth0');b=obj('b',a[2],'eth:'+u2+':ethernet:eth0')
assert m.match_rows([a],[b])[0][0][-1]=='saved-network-uuid'
assert not m.match_rows([a,obj('a2',a[2],b[3])],[b])[0][0][0]=='a'
assert m.row({'id':'x','machine':'d1b-void','level':'2','kind':'snapshot','name':'/etc','missing_facts':'NEVER_COPY'}, {})==('x','void','L2:snapshot','/etc')
print('PASS: exact group, ambiguous keys, kind changes, version retention, UUID fallback, narrow input projection')
