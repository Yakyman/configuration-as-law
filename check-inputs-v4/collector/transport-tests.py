"""Targeted transport failure tests against the disposable Debian guest."""
import json,pathlib,types
import main
root=pathlib.Path(__file__).resolve().parent.parent
ctx=main.Context(types.SimpleNamespace(machine='col-debian',output=str(root/'transport-controls')),[str(root/'lab.sh'),'run','col-debian','--root'],{'system':'debian'})
ctx.deployed=True;main.PROBE='/tmp/c1-tests/probe'
try:
 out,rc,ev=ctx.query('forced-timeout','sleep 10',timeout=1);assert rc==124,(rc,out)
 out,rc,ev=ctx.query('forced-output-cap','seq 1 100000',timeout=3,max_bytes=1024);assert rc==75,(rc,len(out))
 out,rc,ev=ctx.query('after-failure','printf "continued\\n"',timeout=3);assert rc==0 and out==b'continued\n',(rc,out)
 print(json.dumps({'passed':True,'checks':['query timeout','output cap','continued after both failures']}))
finally:ctx.finish()
