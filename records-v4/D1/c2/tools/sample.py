import random
from facts import *
random.seed(1123)
out = {l.split("\t")[0]: l.rstrip("\n").split("\t") for l in open("../part-microos.tsv")}
part = {r["id"]: r for r in csv.DictReader(open("../../in/part-microos.tsv"), delimiter="\t")}
def pick(pred, n=10):
    ids = [i for i in out if i != "id" and pred(part[i], out[i])]
    return random.sample(ids, min(n, len(ids)))
rules = {
 "R1-package": lambda p, o: p["kind"] == "L1:package",
 "R2-snap-IP-group": lambda p, o: p["kind"].endswith("stored-outside-packages") and o[1] == "INSTALLED-PACKAGE",
 "R2b-snap-IP-exec": lambda p, o: p["kind"].endswith("executable-code-outside-packages") and o[1] == "INSTALLED-PACKAGE",
 "R3-unknown-copy": lambda p, o: p["kind"].startswith("L2") and o[1] == "UNKNOWN",
 "R4-runtime-group": lambda p, o: p["kind"].startswith("L2") and o[1] == "RUNTIME",
 "R5-unit-file": lambda p, o: p["kind"].endswith("unit-file"),
 "R6-polkit": lambda p, o: p["kind"] == "L1:polkit-action",
 "R7-runtime-L1": lambda p, o: p["kind"] in ("L1:process", "L1:module-name", "L1:driver", "L1:service", "L1:timer"),
 "R8-gap-two": lambda p, o: o[1] == "GAP-TWO",
 "R9-accounts": lambda p, o: p["kind"] in ("L1:account", "L1:group"),
}
import sys
for name, pr in rules.items():
    if len(sys.argv) > 1 and name not in sys.argv[1:]: continue
    print("##", name)
    for i in pick(pr):
        p = part[i]
        print(i, "|", p["name"][:80], "|", p["members"][:120].replace('""', '"'))
        print("    ->", out[i][1], "|", out[i][3], "|", out[i][5][:200])
