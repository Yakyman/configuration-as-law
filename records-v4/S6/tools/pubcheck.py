import json,hashlib,subprocess,os,sys
R=sys.argv[1]; L=sys.argv[2]; SEAL=sys.argv[3]
P="check-inputs-v4/supplement-1/step-6-cases/B2/"
seal=json.load(open(SEAL))["files"]
names=subprocess.run(["git","-C",R,"ls-tree","-r","--name-only","c0de5e63",P],capture_output=True,text=True).stdout.split()
print("published files under step-6-cases/B2 at c0de5e63:",len(names))
ok=mism=notsealed=0
for n in names:
    rel=n[len(P):]
    b=subprocess.run(["git","-C",R,"show",f"c0de5e63:{n}"],capture_output=True).stdout
    h=hashlib.sha256(b).hexdigest()
    if rel not in seal: notsealed+=1; print("NOT IN SEAL",rel,h)
    elif seal[rel]!=h: mism+=1; print("MISMATCH",rel,h,seal[rel])
    else: ok+=1
print("equal to seal:",ok,"mismatch:",mism,"not in seal:",notsealed)
pub=set(n[len(P):] for n in names)
print("sealed but not published:",len([s for s in seal if s not in pub]))
for s in ["build/bc4-run-case.py","build/bc4-compare.py","lab.py","raw/round-4-prep/inputs-seal.json"]:
    print(" ",s,"published:",s in pub)
lm=[s for s,h in seal.items() if os.path.exists(L+s) and hashlib.sha256(open(L+s,'rb').read()).hexdigest()!=h]
print("local B2 copies differing from seal:",lm)
print("remote main:",subprocess.run(["git","-C",R,"ls-remote","origin","main"],capture_output=True,text=True).stdout.strip())
