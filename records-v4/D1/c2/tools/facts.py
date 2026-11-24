import json, sys, collections, csv, os, re
csv.field_size_limit(10**9)
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../in/raw/microos")
fs = {}
for l in open(base + "/raw/0004-filesystem.out"):
    d = json.loads(l)
    if "path" in d: fs[d["path"]] = d
rpm = collections.defaultdict(list)  # path -> [(pkg, size, digest, mode, linkto)]
for l in open(base + "/raw/0010-package-files-rpm.out"):
    f = l.rstrip("\n").split("\t")
    if len(f) < 7: f += [""] * (7 - len(f))
    rpm[f[1]].append((f[0], f[2], f[3], f[5], f[6]))
integ = collections.defaultdict(list)
for r in csv.DictReader(open(base + "/package-files.tsv"), delimiter="\t"):
    integ[r["path"]].append(r["integrity"])
objs = list(csv.DictReader(open(base + "/objects.tsv"), delimiter="\t"))
def h(sig): return sig.split(":", 1)[1] if sig and ":" in sig else ""
def live_unchanged(L): return bool(integ.get(L)) and all(i == "unchanged" for i in integ[L])
